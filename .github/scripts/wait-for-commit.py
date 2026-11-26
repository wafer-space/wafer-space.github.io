#!/usr/bin/env python3
"""Wait until a deployed copy of the site is serving, optionally a given commit.

    wait-for-commit.py <site-url> [--commit SHA [--or-descendant]] [--timeout SECONDS]

Every page carries the commit it was built from (commit_hash_plugin.rb writes
a <meta name="git-commit"> tag and an HTML comment). With --commit, keep
fetching the page until it reports that commit; without it, until it looks
like the site at all. Exits 0 when ready, 1 on timeout.

With --or-descendant, a page built from a later commit also counts as ready:
when two deploys land close together, the earlier one's check would otherwise
wait for a commit the site has already moved past. "Later" means the expected
commit is an ancestor of the served one in the current checkout, so the
checkout needs enough history to contain both (actions/checkout fetch-depth: 0).

Uses only the standard library so it runs on a bare GitHub runner.
"""

import argparse
import http.client
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

COMMIT_PATTERNS = (
    re.compile(r'<meta name="git-commit" content="([a-f0-9]{40})"'),
    re.compile(r"<!-- Generated from git commit: ([a-f0-9]{40})"),
)
SITE_MARKER = "wafer.space"
POLL_SECONDS = 5


def fetch(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; wafer.space-link-checker; +https://wafer.space/)",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def served_commit(page):
    for pattern in COMMIT_PATTERNS:
        match = pattern.search(page)
        if match:
            return match.group(1)
    return None


def is_descendant(commit, ancestor):
    """True if `ancestor` is reachable from `commit` in the current checkout.

    Unknown commits (not fetched) just make this false.
    """
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, commit],
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def check(url, expected, or_descendant):
    """Return (ready, message) for one attempt."""
    try:
        page = fetch(url)
    except (urllib.error.URLError, http.client.HTTPException, OSError, TimeoutError) as e:
        return False, f"not responding ({e})"

    if SITE_MARKER not in page:
        return False, "responding but not serving the site yet"

    found = served_commit(page)
    if expected is None:
        return True, f"serving the site (commit {found or 'unknown'})"
    if found == expected:
        return True, f"serving commit {found}"
    if found is None:
        return False, "serving the site but no commit hash found"
    if or_descendant and is_descendant(found, expected):
        return True, f"serving commit {found}, a descendant of {expected}"
    return False, f"serving commit {found}, waiting for {expected}"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("site_url", help="page to fetch, e.g. https://wafer.space/")
    parser.add_argument("--commit", help="full 40-hex commit the page must report")
    parser.add_argument(
        "--or-descendant",
        action="store_true",
        help="also accept a commit that has --commit as an ancestor (needs git history)",
    )
    parser.add_argument("--timeout", type=int, default=600, help="seconds to keep trying (default 600)")
    args = parser.parse_args()

    if args.commit and not re.fullmatch(r"[a-f0-9]{40}", args.commit):
        parser.error("--commit must be a full 40-character hex hash")
    if args.or_descendant and not args.commit:
        parser.error("--or-descendant needs --commit")

    deadline = time.monotonic() + args.timeout
    attempt = 0
    while True:
        attempt += 1
        ready, message = check(args.site_url, args.commit, args.or_descendant)
        print(f"Attempt {attempt}: {args.site_url} {message}", flush=True)
        if ready:
            return 0
        if time.monotonic() >= deadline:
            print(f"ERROR: not ready after {args.timeout}s", file=sys.stderr)
            return 1
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    sys.exit(main())
