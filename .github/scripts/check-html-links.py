#!/usr/bin/env python3
"""Fail when a source file links to an internal URL ending in ".html".

Pages are served at their canonical URL without the extension (about.html
is https://wafer.space/about), and Cloudflare redirects /about.html to it, so
an internal link written as /about.html costs every visitor a redirect. This
checks the files tracked by git (except .github/ and the _theme submodule)
for links in:

- HTML attributes: href, src, action, and the url= of a meta refresh;
- Markdown inline links, images and reference definitions;
- Liquid strings passed to relative_url or absolute_url;
- YAML values of keys such as url, button_url, link, href and redirect.

A link is internal when it has no scheme or host (root-relative or relative),
or its host is wafer.space. URLs built with Liquid ({{ ... }}) are skipped.
Each problem is printed as "file:line: message" and as a GitHub Actions
::error:: annotation, and the script exits with status 1.

Uses only the standard library so it runs on a bare GitHub runner.
"""

import re
import subprocess
import sys
import urllib.parse

EXTENSIONS = (".html", ".md", ".markdown", ".yml", ".yaml", ".liquid")
EXCLUDE_PREFIXES = (".github/", "_theme/")
HOSTS = {"wafer.space", "www.wafer.space"}

PATTERNS = [
    # HTML attributes
    re.compile(r"""\b(?:href|src|action)\s*=\s*(["'])(?P<url>.*?)\1""", re.I),
    re.compile(r"""\bcontent\s*=\s*(["'])\s*\d+\s*;\s*url=(?P<url>[^"']*)\1""", re.I),
    # Markdown inline links and images, and reference definitions
    re.compile(r"\]\(\s*<?(?P<url>[^)\s>]+)"),
    re.compile(r"^\s*\[[^\]]+\]:\s*<?(?P<url>[^\s>]+)"),
    # Liquid strings piped to the URL filters
    re.compile(r"""(["'])(?P<url>[^"']*)\1\s*\|\s*(?:relative_url|absolute_url)\b"""),
    # YAML values of link-like keys
    re.compile(
        r"""^\s*(?:-\s+)?(?:[\w-]*_url|url|link|href|redirect)\s*:\s*(["']?)(?P<url>[^"'\s#][^"'\s]*)\1\s*(?:#.*)?$""",
        re.I,
    ),
]


def tracked_files():
    out = subprocess.run(["git", "ls-files", "-z"], capture_output=True, text=True, check=True).stdout
    for path in out.split("\0"):
        if path.endswith(EXTENSIONS) and not path.startswith(EXCLUDE_PREFIXES):
            yield path


def internal_html_path(url):
    """Return the URL's path if it is an internal link ending in .html."""
    if "{{" in url or "{%" in url:
        return None
    parts = urllib.parse.urlsplit(url)
    if parts.scheme and parts.scheme not in ("http", "https"):
        return None  # mailto:, tel:, data:, ...
    if parts.netloc and parts.netloc.lower() not in HOSTS:
        return None
    return parts.path if parts.path.endswith(".html") else None


def suggestion(url):
    """The same URL with the .html (or index.html) dropped from its path."""
    parts = urllib.parse.urlsplit(url)
    path = parts.path
    if path.endswith("/index.html") or path == "index.html":
        path = path[: -len("index.html")] or "/"
    else:
        path = path[: -len(".html")]
    return urllib.parse.urlunsplit(parts._replace(path=path))


def check(path):
    problems = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for number, line in enumerate(f, 1):
            seen = set()
            for pattern in PATTERNS:
                for match in pattern.finditer(line):
                    url = match.group("url").strip()
                    if internal_html_path(url) and url not in seen:
                        seen.add(url)
                        problems.append((path, number, url, suggestion(url)))
    return problems


def main():
    problems = [problem for path in tracked_files() for problem in check(path)]
    for path, line, url, fixed in problems:
        message = f'internal link "{url}" ends in .html; link to "{fixed}" instead'
        print(f"{path}:{line}: {message}")
        print(f"::error file={path},line={line}::{message}")
    if problems:
        print(f"\n{len(problems)} internal .html link(s) found", file=sys.stderr)
        return 1
    print("No internal .html links found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
