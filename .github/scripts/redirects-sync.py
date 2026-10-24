#!/usr/bin/env python3
"""Get the redirects sync Worker to load a revision of a redirect list.

The Worker is https://github.com/wafer-space/cloudflare-redirects-sync. Give
this the redirects.json just deployed (--from-file), or its revision
(--number and --commit). Until the Cloudflare list holds that revision or a
newer one, it repeats:

1. GET /list: done if the list holds the revision or a newer one;
2. GET /source: wait if the site doesn't serve it yet (GitHub Pages can take
   minutes to publish, and caches can serve an older copy for a while);
3. POST /sync, which writes the site's file if it's newer than the list, and
   answers with what the list holds: done if that's the revision or newer.

The Worker doesn't retry, so this does. Every round that doesn't finish waits
before the next, backing off up to a minute, and the last round is made at
--timeout; each request may only take the time left (and at least a
second), so a hanging Worker can't stretch that. Checking /list each round
also catches another sync's older write landing just after this one's. A
dropped
connection, a timeout or an answer that isn't the Worker's JSON is retried;
answers that won't change by asking again (a bad request, a wrong secret, a
commit mismatch, a redirect) stop it at once. Redirects aren't followed, so
the secret is only ever sent to REDIRECTS_SYNC_URL, which must be https.

Reads the Worker's URL from REDIRECTS_SYNC_URL and its bearer token from
REDIRECTS_SYNC_SECRET. When either is missing (as on pull requests from
forks) it says so and exits successfully, as the Worker's cron trigger
catches up within a few minutes; with --require-secrets it fails instead.

With --print-revision it only prints the file's revision as number=... and
commit=... lines (for $GITHUB_OUTPUT), so a later job can sync without the
file.
"""

import argparse
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Each list, and the host its revision item names (as the Worker requires)
LISTS = {"wafer_space": "wafer.space", "preview_wafer_space": "preview.wafer.space"}
COMMENT = re.compile(r"^v\d+(?:\.\d+)*-(\d+)(?:\b|$)")
COMMIT = re.compile(r"/commit/([0-9a-f]{40})$")
FULL_HASH = re.compile(r"^[0-9a-f]{40}$")
# Answers that won't change by asking again (3xx: redirects aren't followed)
FATAL = {300, 301, 302, 303, 307, 308, 400, 401, 404, 405, 409}
USER_AGENT = "wafer-space/wafer-space.github.io/.github/scripts/redirects-sync.py"
# The longest a single request may take, and the longest wait between rounds
CALL_TIMEOUT = 30
MAX_DELAY = 60


def file_revision(path, host):
    """The (number, commit) the file's first item records for `host`."""
    with open(path) as f:
        items = json.load(f)
    first = items[0] if isinstance(items, list) and items and isinstance(items[0], dict) else {}
    redirect = first.get("redirect") if isinstance(first.get("redirect"), dict) else {}
    comment, target = first.get("comment"), redirect.get("target_url")
    number = COMMENT.match(comment) if isinstance(comment, str) else None
    commit = COMMIT.search(target) if isinstance(target, str) else None
    if redirect.get("source_url") != f"{host}/revision" or not number or not commit:
        raise ValueError(f"{path} doesn't start with a {host}/revision item")
    return int(number.group(1)), commit.group(1)


class NoRedirects(urllib.request.HTTPRedirectHandler):
    """Hand a redirect back as an HTTPError rather than following it, as urllib
    would send the Authorization header on to wherever it points."""

    def redirect_request(self, *args, **kwargs):
        return None


class Worker:
    def __init__(self, base, secret, name):
        self.base, self.secret, self.name = base, secret, name
        self.opener = urllib.request.build_opener(NoRedirects)

    def call(self, method, path, timeout=CALL_TIMEOUT):
        """(status, body dict) for one request, or (None, {"error": ...}) if it failed."""
        url = f"{self.base}{path}?{urllib.parse.urlencode({'list': self.name})}"
        # Cloudflare's Browser Integrity Check refuses urllib's default
        # User-Agent on workers.dev ("error code: 1010")
        headers = {"Authorization": f"Bearer {self.secret}", "User-Agent": USER_AGENT}
        request = urllib.request.Request(url, method=method, headers=headers)
        try:
            try:
                with self.opener.open(request, timeout=timeout) as response:
                    status, raw = response.status, response.read()
            except urllib.error.HTTPError as err:
                status, raw = err.code, err.read()
        # Connection refused, reset or dropped, a timeout, a bad TLS handshake
        # or a truncated response: all worth asking again
        except (urllib.error.URLError, http.client.HTTPException, OSError) as err:
            print(f"{method} {path}: {err!r}")
            return None, {"error": repr(err)}
        try:
            body = json.loads(raw)
        except ValueError:
            body = None
        if not isinstance(body, dict):
            body = {"error": raw.decode("utf-8", "replace")[:300]}
        print(f"{method} {path}: HTTP {status} {json.dumps(body)}")
        return status, body


def compare(revision, number, commit, what):
    """-1, 0 or 1 for a revision older than, equal to or newer than ours.

    Raises if it has our number but a different commit."""
    if not isinstance(revision, dict) or not isinstance(revision.get("number"), int):
        return -1
    if revision["number"] == number and revision.get("commit") != commit:
        raise ValueError(f"{what} has revision {number} with commit {revision.get('commit')}, not {commit}")
    return (revision["number"] > number) - (revision["number"] < number)


def sync(worker, number, commit, timeout, clock=time.monotonic, sleep=time.sleep):
    """Exit status: 0 once the list holds our revision or a newer one."""
    deadline = clock() + timeout
    delay = 10

    def call(method, path):
        return worker.call(method, path, timeout=max(1, min(CALL_TIMEOUT, deadline - clock())))

    while True:
        status, body = call("GET", "/list")
        if status == 200 and compare(body.get("list"), number, commit, "The list") >= 0:
            print(f"The list holds revision {body['list']['number']}")
            return 0
        if status == 200:
            status, body = call("GET", "/source")
            if status == 200 and compare(body.get("source"), number, commit, "The site") >= 0:
                status, body = call("POST", "/sync")
                # The answer says what the list holds: the readback after a
                # write, or the list as it was when /sync found nothing newer
                # (its own fetch of the site can still see an older copy)
                if status == 200 and compare(body.get("list"), number, commit, "The list") >= 0:
                    print(f"The list holds revision {body['list']['number']} ({body.get('status')})")
                    return 0
        if status in FATAL:
            print(f"::error::Redirects sync failed: HTTP {status} {body.get('status') or body.get('error') or ''}".rstrip())
            return 1
        remaining = deadline - clock()
        if remaining <= 0:
            print(f"::error::The {worker.name} list doesn't hold revision {number} after {timeout}s")
            return 1
        wait = min(delay, remaining)
        print(f"Retrying in {wait:.0f}s")
        sleep(wait)
        delay = min(delay * 2, MAX_DELAY)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", choices=sorted(LISTS), required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--from-file", metavar="REDIRECTS_JSON", help="sync the revision this file records")
    source.add_argument("--number", type=int, help="the revision number to sync (with --commit)")
    parser.add_argument("--commit", help="the revision's full commit hash (with --number)")
    parser.add_argument("--print-revision", action="store_true", help="print the file's revision and exit")
    parser.add_argument("--timeout", type=int, default=600, help="seconds to keep retrying (default 600)")
    parser.add_argument("--require-secrets", action="store_true",
                        help="fail, rather than skip, without REDIRECTS_SYNC_URL and REDIRECTS_SYNC_SECRET")
    args = parser.parse_args(argv)

    if args.from_file:
        if args.commit:
            parser.error("--commit goes with --number, not --from-file")
        try:
            args.number, args.commit = file_revision(args.from_file, LISTS[args.list])
        except (OSError, ValueError) as err:
            # stderr: with --print-revision, stdout goes to $GITHUB_OUTPUT
            print(f"::error::{err}", file=sys.stderr)
            return 1
    elif args.print_revision:
        parser.error("--print-revision needs --from-file")
    elif args.number < 0 or not args.commit or not FULL_HASH.match(args.commit):
        parser.error("--number needs a revision number and --commit its full 40-character commit hash")
    if args.print_revision:
        print(f"number={args.number}\ncommit={args.commit}")
        return 0

    base = os.environ.get("REDIRECTS_SYNC_URL", "").rstrip("/")
    secret = os.environ.get("REDIRECTS_SYNC_SECRET", "")
    if not base or not secret:
        if args.require_secrets:
            print("::error::REDIRECTS_SYNC_URL or REDIRECTS_SYNC_SECRET is not set")
            return 1
        print("REDIRECTS_SYNC_URL or REDIRECTS_SYNC_SECRET is not set; skipping (the cron trigger will sync)")
        return 0
    if not base.startswith("https://"):
        print("::error::REDIRECTS_SYNC_URL must be an https:// URL")
        return 1

    print(f"Syncing {args.list} to revision {args.number} ({args.commit})")
    try:
        return sync(Worker(base, secret, args.list), args.number, args.commit, args.timeout)
    except ValueError as err:
        print(f"::error::{err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
