#!/usr/bin/env python3
"""List the organisation's other GitHub Pages sites, which share this site's host.

    sibling-sites.py --owner OWNER --repo REPO --site-url URL [--format names|muffet-excludes]

Every repository of OWNER with GitHub Pages enabled is served as a project
site under the organisation site's domain, at <site-url>/<repo>/. Those
sites are other repositories' content, so the production link check must not
crawl into them (one of them has over a thousand pages, and its links to
github.com get rate limited); check-sibling-links.py checks the links from
this site into them instead.

--format names prints one repository name per line; --format muffet-excludes
prints a --exclude=<regex> argument per line for check-links.sh. REPO itself
is left out. GITHUB_TOKEN, if set, is sent for the higher API rate limit.

Repositories served on their own domain (a CNAME) are listed too; their
excludes match nothing, which is harmless. The converse matters: a repository
with Pages whose name equals one of this site's top-level pages (say "about")
would take that page out of the crawl. Don't name repositories after pages.

Uses only the standard library so it runs on a bare GitHub runner.
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

API = "https://api.github.com"


def list_repos(owner):
    token = os.environ.get("GITHUB_TOKEN")
    page = 1
    while True:
        url = f"{API}/orgs/{owner}/repos?per_page=100&type=public&page={page}"
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "wafer.space-link-checker"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
            repos = json.load(response)
        if not repos:
            return
        yield from repos
        page += 1


def sibling_sites(owner, repo):
    return sorted(r["name"] for r in list_repos(owner) if r.get("has_pages") and r["name"] != repo)


def muffet_exclude(site_url, name):
    parts = urllib.parse.urlsplit(site_url)
    # Either scheme (muffet doesn't rewrite http to https before matching),
    # then the site itself or anything under it: /<repo>, /<repo>/..., /<repo>?...
    return f"--exclude=^https?://{re.escape(parts.netloc)}/{re.escape(name)}([/?#]|$)"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--owner", required=True, help="GitHub organisation, e.g. wafer-space")
    parser.add_argument("--repo", required=True, help="this repository's name, left out of the list")
    parser.add_argument("--site-url", required=True, help="the organisation site, e.g. https://wafer.space/")
    parser.add_argument("--format", choices=["names", "muffet-excludes"], default="names")
    args = parser.parse_args()

    if not urllib.parse.urlsplit(args.site_url).hostname:
        parser.error("--site-url must be an absolute URL")

    names = sibling_sites(args.owner, args.repo)
    for name in names:
        if args.format == "names":
            print(name)
        else:
            print(muffet_exclude(args.site_url, name))
    print(f"{len(names)} sibling sites of {args.owner}/{args.repo}", file=sys.stderr)


if __name__ == "__main__":
    main()
