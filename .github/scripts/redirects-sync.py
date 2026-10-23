#!/usr/bin/env python3
"""Ask the redirects sync Worker to load a revision of a redirect list.

The Worker is https://github.com/wafer-space/cloudflare-redirects-sync. Give
it the redirects.json just deployed (--from-file): the script reads the
revision from its first item and asks the Worker for exactly that revision.

The Worker doesn't retry, so this script does: while the site still serves
an older file (GitHub Pages publishing delay or a cache: HTTP 409
not_published), another bulk operation is pending (503 busy), or Cloudflare
hadn't finished the write (202 pending), it waits and asks again, until
--timeout. It also asks again when the revision the Worker read back from
the list is older than the one requested, which happens when another sync's
older write lands just after this one's. A newer revision already loaded
counts as success: the deploy that brought it syncs it.

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
RETRY = {(409, "not_published"), (503, "busy"), (202, "pending")}


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


def post(url, secret):
    """POST to the Worker: (status, parsed or raw body), or (None, error)."""
    request = urllib.request.Request(url, method="POST", headers={"Authorization": f"Bearer {secret}"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            status, body = response.status, response.read()
    except urllib.error.HTTPError as err:
        status, body = err.code, err.read()
    except (urllib.error.URLError, TimeoutError) as err:
        return None, str(err)
    try:
        return status, json.loads(body)
    except ValueError:
        return status, body.decode("utf-8", "replace")


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
    if not args.list:
        parser.error("--list is required")
    if (args.number is None) != (args.commit is None):
        parser.error("give --number and --commit together, or --from-file")

    base = os.environ.get("REDIRECTS_SYNC_URL", "").rstrip("/")
    secret = os.environ.get("REDIRECTS_SYNC_SECRET", "")
    if not base or not secret:
        print("REDIRECTS_SYNC_URL or REDIRECTS_SYNC_SECRET is not set; skipping (the cron trigger will sync)")
        return 0

    query = {"list": args.list}
    if args.number is not None:
        query.update(number=str(args.number), commit=args.commit)
    url = f"{base}/sync?{urllib.parse.urlencode(query)}"
    print(f"Syncing {args.list}" + (f" to revision {args.number} ({args.commit})" if args.number is not None else ""))

    deadline = time.monotonic() + args.timeout
    delay = 10
    while True:
        status, body = post(url, secret)
        print(f"HTTP {status}: {json.dumps(body, indent=2) if isinstance(body, dict) else body}")
        state = body.get("status") if isinstance(body, dict) else None
        # A 200 reports the revision the list holds (read back after a write).
        # Another sync's older write can land just after this one's, so only
        # stop once the list holds at least our revision; otherwise retry.
        held = (body.get("list") or {}).get("number", -1) if isinstance(body, dict) else -1
        if status == 200 and (args.number is None or held >= args.number):
            return 0
        if status not in (None, 200) and (status, state) not in RETRY:
            print(f"::error::Redirects sync failed: HTTP {status} {state or ''}".rstrip())
            return 1
        if time.monotonic() + delay > deadline:
            print(f"::error::Redirects sync still {state or 'unreachable'} after {args.timeout}s")
            return 1
        print(f"Retrying in {delay}s")
        time.sleep(delay)
        delay = min(delay * 2, 60)


if __name__ == "__main__":
    sys.exit(main())
