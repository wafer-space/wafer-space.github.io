#!/usr/bin/env python3
"""Get the redirects sync Worker to load a revision of a redirect list.

The Worker is https://github.com/wafer-space/cloudflare-redirects-sync. Give
this the redirects.json just deployed (--from-file), or its revision
(--number and --commit). Until the Cloudflare list holds that revision or a
newer one, it repeats:

1. GET /list: done if the list holds the revision or a newer one;
2. GET /source: wait if the site doesn't serve it yet (GitHub Pages can take
   minutes to publish, and caches can serve an older copy for a while);
3. POST /sync, which writes the site's file if it's newer than the list.

The Worker doesn't retry, so this does, backing off up to a minute between
rounds until --timeout. Checking /list again after each sync also catches
another sync's older write landing just after this one's.

Reads the Worker's URL from REDIRECTS_SYNC_URL and its bearer token from
REDIRECTS_SYNC_SECRET. When either is missing (as on pull requests from
forks) it says so and exits successfully: the Worker's cron trigger catches
up within a few minutes.

With --print-revision it only prints the file's revision as number=... and
commit=... lines (for $GITHUB_OUTPUT), so a later job can sync without the
file.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

LISTS = ("wafer_space", "preview_wafer_space")
COMMENT = re.compile(r"^v\d+(?:\.\d+)*-(\d+)(?:\b|$)")
COMMIT = re.compile(r"/commit/([0-9a-f]{40})$")
# Answers that won't change by asking again
FATAL = {400, 401, 404, 405, 409}


def file_revision(path):
    """The (number, commit) the file's first item records."""
    with open(path) as f:
        items = json.load(f)
    first = items[0] if isinstance(items, list) and items else {}
    redirect = first.get("redirect") or {}
    number = COMMENT.match(first.get("comment") or "")
    commit = COMMIT.search(redirect.get("target_url") or "")
    if not str(redirect.get("source_url", "")).endswith("/revision") or not number or not commit:
        raise ValueError(f"{path} doesn't start with a revision item")
    return int(number.group(1)), commit.group(1)


class Worker:
    def __init__(self, base, secret, name):
        self.base, self.secret, self.name = base, secret, name

    def call(self, method, path):
        """(status, body) for one request, or (None, error text)."""
        url = f"{self.base}{path}?{urllib.parse.urlencode({'list': self.name})}"
        # Cloudflare's Browser Integrity Check refuses urllib's default
        # User-Agent on workers.dev ("error code: 1010")
        headers = {"Authorization": f"Bearer {self.secret}",
                   "User-Agent": "wafer-space/wafer-space.github.io/.github/scripts/redirects-sync.py"}
        request = urllib.request.Request(url, method=method, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                status, raw = response.status, response.read()
        except urllib.error.HTTPError as err:
            status, raw = err.code, err.read()
        except (urllib.error.URLError, TimeoutError) as err:
            print(f"{method} {path}: {err}")
            return None, {}
        try:
            body = json.loads(raw)
        except ValueError:
            body = {"error": raw.decode("utf-8", "replace")}
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


def sync(worker, number, commit, timeout):
    """Exit status: 0 once the list holds our revision or a newer one."""
    deadline = time.monotonic() + timeout
    delay = 10
    while True:
        status, body = worker.call("GET", "/list")
        if status == 200 and compare(body.get("list"), number, commit, "The list") >= 0:
            print(f"The list holds revision {body['list']['number']}")
            return 0
        if status in FATAL:
            break
        if status == 200:
            status, body = worker.call("GET", "/source")
            if status in FATAL:
                break
            if status == 200 and compare(body.get("source"), number, commit, "The site") >= 0:
                status, body = worker.call("POST", "/sync")
                if status in FATAL:
                    break
                if status == 200:
                    continue  # check what the list holds now
        if time.monotonic() + delay > deadline:
            print(f"::error::The {worker.name} list doesn't hold revision {number} after {timeout}s")
            return 1
        print(f"Retrying in {delay}s")
        time.sleep(delay)
        delay = min(delay * 2, 60)
    print(f"::error::Redirects sync failed: HTTP {status} {body.get('status') or body.get('error') or ''}".rstrip())
    return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", choices=LISTS)
    parser.add_argument("--from-file", metavar="REDIRECTS_JSON", help="sync the revision this file records")
    parser.add_argument("--number", type=int, help="the revision number to sync (with --commit)")
    parser.add_argument("--commit", help="the revision's full commit hash (with --number)")
    parser.add_argument("--print-revision", action="store_true", help="print the file's revision and exit")
    parser.add_argument("--timeout", type=int, default=600, help="seconds to keep retrying (default 600)")
    args = parser.parse_args()

    if args.from_file:
        args.number, args.commit = file_revision(args.from_file)
    if args.print_revision:
        if not args.from_file:
            parser.error("--print-revision needs --from-file")
        print(f"number={args.number}\ncommit={args.commit}")
        return 0
    if not args.list or args.number is None or not args.commit:
        parser.error("give --list and either --from-file, or --number and --commit")

    base = os.environ.get("REDIRECTS_SYNC_URL", "").rstrip("/")
    secret = os.environ.get("REDIRECTS_SYNC_SECRET", "")
    if not base or not secret:
        print("REDIRECTS_SYNC_URL or REDIRECTS_SYNC_SECRET is not set; skipping (the cron trigger will sync)")
        return 0

    print(f"Syncing {args.list} to revision {args.number} ({args.commit})")
    try:
        return sync(Worker(base, secret, args.list), args.number, args.commit, args.timeout)
    except ValueError as err:
        print(f"::error::{err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
