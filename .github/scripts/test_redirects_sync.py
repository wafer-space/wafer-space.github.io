"""Tests for redirects-sync.py against a local stand-in for the Worker.

Run with: python3 -m unittest discover -s .github/scripts
"""

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

spec = importlib.util.spec_from_file_location("redirects_sync", Path(__file__).with_name("redirects-sync.py"))
rs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rs)

OURS = "b" * 40
OLDER = "a" * 40


def revision(number, commit):
    return {"number": number, "commit": commit, "comment": f"v0.0-{number} {commit[:7]}"}


class Server:
    """An HTTP server answering each request with respond(method, path), which
    returns (status, body, headers), or None to drop the connection."""

    def __init__(self, respond):
        self.requests = []
        server = self

        class Handler(BaseHTTPRequestHandler):
            def handle_one(self):
                server.requests.append((self.command, self.path.split("?")[0], self.headers.get("Authorization")))
                answer = respond(self.command, self.path.split("?")[0])
                if answer is None:
                    self.close_connection = True
                    return
                status, body, headers = (*answer, {})[:3]
                raw = body if isinstance(body, bytes) else json.dumps(body).encode()
                self.send_response(status)
                for key, value in headers.items():
                    self.send_header(key, value)
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            do_GET = do_POST = handle_one

            def log_message(self, *args):
                pass

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()

    def count(self, method, path):
        return sum(1 for m, p, _ in self.requests if (m, p) == (method, path))


class Clock:
    """A clock that only moves when sync() sleeps."""

    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


class SyncTest(unittest.TestCase):
    def run_sync(self, respond, timeout=600):
        server = Server(respond)
        self.addCleanup(server.close)
        clock = Clock()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = rs.sync(rs.Worker(server.url, "s3cret", "preview_wafer_space"), 500, OURS, timeout,
                             clock=clock, sleep=clock.sleep)
        return status, server, clock, out.getvalue()

    def test_an_applied_sync_finishes(self):
        def respond(method, path):
            return {
                "/list": (200, {"status": "ok", "list": revision(499, OLDER)}),
                "/source": (200, {"status": "ok", "source": revision(500, OURS)}),
                "/sync": (200, {"status": "applied", "list": revision(500, OURS)}),
            }[path]
        status, server, clock, out = self.run_sync(respond)
        self.assertEqual(status, 0)
        self.assertEqual(server.count("POST", "/sync"), 1)
        self.assertEqual(server.count("GET", "/list"), 1)
        self.assertEqual(clock.sleeps, [])
        self.assertIn("holds revision 500 (applied)", out)
        self.assertTrue(all(auth == "Bearer s3cret" for _, _, auth in server.requests))

    def test_a_sync_that_loads_nothing_waits_rather_than_spinning(self):
        # The site serves 500 to /source but /sync's own fetch still sees 499
        def respond(method, path):
            return {
                "/list": (200, {"status": "ok", "list": revision(499, OLDER)}),
                "/source": (200, {"status": "ok", "source": revision(500, OURS)}),
                "/sync": (200, {"status": "up_to_date", "source": revision(499, OLDER), "list": revision(499, OLDER)}),
            }[path]
        status, server, clock, out = self.run_sync(respond, timeout=120)
        self.assertEqual(status, 1)
        # One sync per round: 10 + 20 + 40 + 50 seconds of waiting, five rounds
        self.assertEqual(clock.sleeps, [10, 20, 40, 50])
        self.assertEqual(server.count("POST", "/sync"), 5)
        self.assertEqual(clock.now, 120)
        self.assertIn("doesn't hold revision 500 after 120s", out)

    def test_a_newer_list_counts(self):
        status, server, _, _ = self.run_sync(lambda m, p: (200, {"status": "ok", "list": revision(501, "c" * 40)}))
        self.assertEqual((status, server.count("GET", "/source")), (0, 0))

    def test_the_site_serving_an_older_copy_waits(self):
        answers = iter([revision(499, OLDER), revision(499, OLDER), revision(500, OURS)])

        def respond(method, path):
            if path == "/list":
                return 200, {"status": "ok", "list": revision(499, OLDER)}
            if path == "/source":
                return 200, {"status": "ok", "source": next(answers)}
            return 200, {"status": "applied", "list": revision(500, OURS)}
        status, server, clock, _ = self.run_sync(respond)
        self.assertEqual(status, 0)
        self.assertEqual(clock.sleeps, [10, 20])
        self.assertEqual(server.count("POST", "/sync"), 1)

    def test_a_dropped_connection_is_retried(self):
        dropped = []

        def respond(method, path):
            if not dropped:
                dropped.append(path)
                return None
            return 200, {"status": "ok", "list": revision(500, OURS)}
        status, _, clock, out = self.run_sync(respond)
        self.assertEqual((status, clock.sleeps), (0, [10]))
        self.assertIn("RemoteDisconnected", out)

    def test_an_answer_that_isnt_a_json_object_is_retried(self):
        answers = iter([(200, [1, 2]), (200, b"<html>captive portal</html>"), (502, b"Bad gateway"),
                        (200, {"status": "ok", "list": revision(500, OURS)})])

        def respond(method, path):
            if path == "/list":
                return next(answers)
            return 200, {"status": "ok", "source": revision(499, OLDER)}
        status, _, clock, _ = self.run_sync(respond)
        self.assertEqual((status, clock.sleeps), (0, [10, 20, 40]))

    def test_busy_and_pending_are_retried(self):
        answers = iter([(503, {"status": "busy"}), (202, {"status": "pending"}),
                        (200, {"status": "ok", "list": revision(500, OURS)})])
        status, _, clock, _ = self.run_sync(lambda m, p: next(answers) if p == "/list" else (200, {}))
        self.assertEqual((status, clock.sleeps), (0, [10, 20]))

    def test_answers_that_wont_change_stop_at_once(self):
        for code in (400, 401, 404, 409):
            with self.subTest(code=code):
                status, server, clock, out = self.run_sync(lambda m, p: (code, {"status": "error"}))
                self.assertEqual((status, clock.sleeps, len(server.requests)), (1, [], 1))
                self.assertIn(f"HTTP {code}", out)

    def test_a_commit_mismatch_stops_at_once(self):
        # main() reports it and exits 1 (see MainTest)
        with self.assertRaisesRegex(ValueError, "The list has revision 500 with commit a+, not b+"):
            self.run_sync(lambda m, p: (200, {"status": "ok", "list": revision(500, OLDER)}))

    def test_redirects_arent_followed_so_the_secret_stays_put(self):
        elsewhere = Server(lambda m, p: (200, {"status": "ok", "list": revision(500, OURS)}))
        self.addCleanup(elsewhere.close)
        status, server, clock, out = self.run_sync(lambda m, p: (302, b"", {"Location": f"{elsewhere.url}/list"}))
        self.assertEqual((status, clock.sleeps), (1, []))
        self.assertEqual(elsewhere.requests, [])
        self.assertIn("HTTP 302", out)

    def test_requests_only_get_the_time_left(self):
        timeouts = []
        worker = mock.Mock(name="worker")
        worker.name = "wafer_space"

        def call(method, path, timeout):
            timeouts.append(timeout)
            return None, {"error": "timed out"}
        worker.call.side_effect = call
        clock = Clock()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(rs.sync(worker, 500, OURS, 45, clock=clock, sleep=clock.sleep), 1)
        # Rounds at 0, 10 and 30 s get the full 30 s; the last, at 45 s, gets the minimum
        self.assertEqual(timeouts, [30, 30, 15, 1])
        self.assertEqual(clock.sleeps, [10, 20, 15])


class MainTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.dir = Path(directory.name)

    def write(self, source_url, comment="v0.0-487-g" + OURS, commit=OURS):
        path = self.dir / "redirects.json"
        path.write_text(json.dumps([{"comment": comment, "redirect": {
            "source_url": source_url, "target_url": f"https://github.com/x/y/commit/{commit}", "status_code": 302}}]))
        return str(path)

    def main(self, *argv, env=None):
        out, err = io.StringIO(), io.StringIO()
        with (mock.patch.dict(os.environ, env or {}, clear=True), contextlib.redirect_stdout(out),
              contextlib.redirect_stderr(err)):
            status = rs.main(list(argv))
        self.stderr = err.getvalue()
        return status, out.getvalue()

    def test_print_revision(self):
        path = self.write("wafer.space/revision")
        self.assertEqual(self.main("--list", "wafer_space", "--from-file", path, "--print-revision"),
                         (0, f"number=487\ncommit={OURS}\n"))

    def test_the_revision_item_must_name_the_lists_host(self):
        for source in ("wafer.space/revision", "evil.preview.wafer.space/revision", "preview.wafer.space/revision/"):
            with self.subTest(source=source):
                status, out = self.main("--list", "preview_wafer_space", "--from-file", self.write(source),
                                        "--print-revision")
                self.assertEqual(status, 1)
                # Nothing on stdout, which goes to $GITHUB_OUTPUT
                self.assertEqual(out, "")
                self.assertIn("doesn't start with a preview.wafer.space/revision item", self.stderr)

    def test_from_file_and_number_dont_mix(self):
        path = self.write("wafer.space/revision")
        for argv in (["--from-file", path, "--number", "5", "--commit", OURS], ["--from-file", path, "--commit", OURS]):
            with self.subTest(argv=argv), self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                self.main("--list", "wafer_space", *argv)

    def test_commit_must_be_a_full_hash(self):
        for commit in ("abc1234", OURS.upper(), ""):
            with self.subTest(commit=commit), self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                self.main("--list", "wafer_space", "--number", "5", "--commit", commit)

    def test_missing_secrets_skip_unless_required(self):
        argv = ["--list", "wafer_space", "--number", "5", "--commit", OURS]
        self.assertEqual(self.main(*argv)[0], 0)
        status, out = self.main(*argv, "--require-secrets", env={"REDIRECTS_SYNC_URL": "https://example.com"})
        self.assertEqual(status, 1)
        self.assertIn("::error::", out)

    def test_a_commit_mismatch_fails(self):
        server = Server(lambda m, p: (200, {"status": "ok", "list": revision(5, OLDER)}))
        self.addCleanup(server.close)
        # main() insists on https, so point it at the local server through sync's Worker
        worker = rs.Worker
        with mock.patch.object(rs, "Worker", lambda base, secret, name: worker(server.url, secret, name)):
            status, out = self.main("--list", "wafer_space", "--number", "5", "--commit", OURS,
                                    env={"REDIRECTS_SYNC_URL": "https://example.com", "REDIRECTS_SYNC_SECRET": "x"})
        self.assertEqual(status, 1)
        self.assertIn("::error::The list has revision 5 with commit", out)

    def test_the_worker_url_must_be_https(self):
        status, out = self.main("--list", "wafer_space", "--number", "5", "--commit", OURS,
                                env={"REDIRECTS_SYNC_URL": "http://example.com", "REDIRECTS_SYNC_SECRET": "x"})
        self.assertEqual(status, 1)
        self.assertIn("must be an https:// URL", out)


if __name__ == "__main__":
    unittest.main()
