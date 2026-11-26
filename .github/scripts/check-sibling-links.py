#!/usr/bin/env python3
"""Check this site's links into the sibling project sites muffet was kept out of.

    check-sibling-links.py <muffet-json> --site-url URL --sites FILE --failures FILE

The production check runs muffet with the sibling sites (sibling-sites.py)
excluded, so it doesn't crawl other repositories' content. muffet then
neither follows nor checks links into them, so this script does the checking
part: it fetches every page muffet crawled (listed in its JSON report),
collects the href/src/poster targets under a sibling site, fetches each once,
and requires a 2xx response and, for a URL with a fragment, an element with
that id (or name) on the page, as muffet would.

Failures are written to --failures in muffet's text format (page URL, then
tab-indented "<error>\t<link>" lines), ready to append to muffet's own list.
Exits 0 when every link is fine, 1 when some aren't, 2 for usage errors and
3 if the script itself failed.

Uses only the standard library so it runs on a bare GitHub runner.
"""

import argparse
import collections
import html
import http.client
import json
import re
import sys
import traceback
import urllib.error
import urllib.parse
import urllib.request

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; wafer.space-link-checker; +https://wafer.space/)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Cache-Control": "no-cache",
}
# The attributes muffet reads. The lookbehind keeps data-src, data-id and the
# like out, as muffet ignores data-* attributes.
ATTRIBUTE = re.compile(r"""(?<![\w-])(?:href|src|poster)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)
SRCSET = re.compile(r"""(?<![\w-])srcset\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)
ID_ATTRIBUTE = re.compile(r"""(?<![\w-])(?:id|name)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)


def fetch(url):
    """Return (status, body) for a GET of url, following redirects."""
    request = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


def attribute_values(page, pattern):
    for match in pattern.finditer(page):
        yield html.unescape(match.group(1) if match.group(1) is not None else match.group(2))


def sibling_prefix(url, site_host, sites):
    """The sibling site a URL belongs to, or None."""
    parsed = urllib.parse.urlsplit(url)
    if parsed.hostname != site_host:
        return None
    first = parsed.path.lstrip("/").split("/", 1)[0]
    return first if first in sites else None


def link_values(page):
    yield from attribute_values(page, ATTRIBUTE)
    # srcset is "url [descriptor], url [descriptor], ..."
    for srcset in attribute_values(page, SRCSET):
        for candidate in srcset.split(","):
            url = candidate.strip().split()[0] if candidate.strip() else ""
            if url:
                yield url


def links_into_siblings(page_url, page, site_host, sites):
    found = set()
    for value in link_values(page):
        value = value.strip()
        if not value or value.startswith(("#", "mailto:", "javascript:", "data:", "tel:")):
            continue
        target = urllib.parse.urljoin(page_url, value)
        if sibling_prefix(target, site_host, sites):
            found.add(target)
    return found


def check_target(url, cache):
    """Return an error string for url, or None if it's fine. Fetches each page once."""
    without_fragment, fragment = urllib.parse.urldefrag(url)
    if without_fragment not in cache:
        try:
            cache[without_fragment] = fetch(without_fragment)
        except (urllib.error.URLError, http.client.HTTPException, OSError, TimeoutError) as e:
            cache[without_fragment] = (None, str(e))
    status, body = cache[without_fragment]
    if status is None:
        return body
    if not 200 <= status < 300:
        return str(status)
    if fragment:
        fragment = urllib.parse.unquote(fragment)
        if fragment not in set(attribute_values(body, ID_ATTRIBUTE)):
            return f"id #{fragment} not found"
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("json_report", help="muffet --format=json --verbose output")
    parser.add_argument("--site-url", required=True, help="URL muffet was run against")
    parser.add_argument("--sites", required=True, help="file with one sibling site name per line")
    parser.add_argument("--failures", required=True, help="where to write broken links")
    args = parser.parse_args()

    site_host = urllib.parse.urlsplit(args.site_url).hostname
    if not site_host:
        parser.error("--site-url must be an absolute URL")
    with open(args.sites, encoding="utf-8") as f:
        sites = {line.strip() for line in f if line.strip()}

    with open(args.json_report, encoding="utf-8") as f:
        try:
            pages = json.load(f)
        except json.JSONDecodeError:
            # muffet didn't get as far as a report; there is nothing to check
            pages = []

    page_urls = sorted({page["url"] for page in pages if urllib.parse.urlsplit(page["url"]).hostname == site_host})
    targets_by_page = collections.OrderedDict()
    for page_url in page_urls:
        try:
            status, body = fetch(page_url)
        except (urllib.error.URLError, http.client.HTTPException, OSError, TimeoutError) as e:
            print(f"::warning::could not re-fetch {page_url} to look for sibling links: {e}", file=sys.stderr)
            continue
        if not 200 <= status < 300:
            print(f"::warning::{page_url} returned {status} on re-fetch", file=sys.stderr)
            continue
        found = links_into_siblings(page_url, body, site_host, sites)
        if found:
            targets_by_page[page_url] = sorted(found)

    cache = {}
    failures = []
    checked = set()
    for page_url, targets in targets_by_page.items():
        broken = []
        for target in targets:
            checked.add(target)
            error = check_target(target, cache)
            if error is not None:
                broken.append((error, target))
        if broken:
            failures.append(page_url)
            failures.extend(f"\t{error}\t{target}" for error, target in broken)

    with open(args.failures, "w", encoding="utf-8") as f:
        f.write("".join(f"{line}\n" for line in failures))

    print(
        f"Checked {len(checked)} links from {len(targets_by_page)} pages into "
        f"{len(sites)} sibling sites; {sum(1 for line in failures if line.startswith(chr(9)))} broken",
        file=sys.stderr,
    )
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001 - a crash must not look like "links broken" (exit 1)
        traceback.print_exc()
        sys.exit(3)
