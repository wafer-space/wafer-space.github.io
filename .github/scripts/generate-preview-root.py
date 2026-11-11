#!/usr/bin/env python3
"""Generate the root of preview.wafer.space: index.html and redirects.json.

Run from the root of the preview.wafer.space repository, just before the
commit that will hold the result (pr-preview.yml and cleanup-previews.yml run
it after adding or removing previews, and pr-preview.yml again after merging
in another deploy's push). Both files are built first and only then written,
so a failure leaves the previous pair in place. The workflows run the base
branch's copy of this script and its template, not a pull request's.

A preview is a pr-NNN directory with an index.html, or its pr-NNN-title
alias; both files only cover those.

index.html lists every preview, from .github/templates/preview-index.html
next to this script.

redirects.json is the body of Cloudflare's "replace list items" call for the
preview_wafer_space Bulk Redirect list, which the redirects sync Worker
(https://github.com/wafer-space/cloudflare-redirects-sync) loads as is, so a
bad entry would stop the whole list loading. Each pr-NNN preview's
redirects.json (written by _plugins/redirect_list.rb for the production
hostname) is moved under the preview, keeping only the fields this sets:

- source wafer.space/<path> becomes preview.wafer.space/pr-NNN/<path>, and
  a source already seen in that preview is skipped;
- a target on https://wafer.space follows it under
  https://preview.wafer.space/pr-NNN/, any other absolute http(s) target is
  left as is, and an entry with any other target is skipped;
- the status becomes 302, because browsers cache a 301 indefinitely and a
  preview's redirects change with every push;
- the preview's own revision item (wafer.space/revision) is left out, and
  so are the entries for other hosts (the buy.wafer.space campaign links),
  as previews only cover the preview host.

Its first item records the revision, as the Worker requires:
preview.wafer.space/revision redirects to PREVIEW_SOURCE_COMMIT (the site
commit whose deploy or cleanup wrote this), and its comment is the git
describe number of the preview repository commit that will hold the file
(HEAD's plus one). Because each run commits straight after this, including
after merging in another deploy's push, the numbers only go up. They count
commits since the v0.0 tag, so the preview repository's history must not be
rewritten and no other v* tag added, or the numbers would drop and the
Worker would stop loading the list until it is forced to.
"""

import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "preview-index.html"
PLACEHOLDER = "<!-- PREVIEW_ITEMS_PLACEHOLDER -->"
HIDDEN_EMPTY_STATE = 'id="empty-state" style="display: none;"'

PRODUCTION_HOST = "wafer.space"
PREVIEW_HOST = "preview.wafer.space"
COMMIT_URL = "https://github.com/wafer-space/wafer-space.github.io/commit/"
# pr-123, or its pr-123-some-title alias
LISTED_DIR = re.compile(r"^pr-([0-9]+)(?:-(.*))?$")
TARGET = re.compile(r"^https://wafer\.space(?=$|[/?#])/?(.*)$", re.S)
ABSOLUTE = re.compile(r"^https?://[^/?#\s]+", re.I)
# A source on some host: <host>/<path>
HOSTED = re.compile(r"^[a-z0-9.-]+/", re.I)
# The fields of a redirect this writes, besides source_url and target_url
KEPT_FIELDS = ("preserve_query_string", "preserve_path_suffix")
# Cloudflare's Free plan allows 10,000 redirects across all lists
WARN_TOTAL = 9000


def previews(directories):
    """(directory, PR number, title) for each preview, in PR number order."""
    found = []
    for directory in directories:
        match = LISTED_DIR.match(directory.name)
        if not match:
            continue
        if not (directory / "index.html").is_file():
            print(f"Warning: {directory.name}/ appears to be incomplete (no index.html), skipping...")
            continue
        number, title = int(match.group(1)), (match.group(2) or "").replace("-", " ")
        if not 1 <= number <= 99999:
            print(f"Warning: {directory.name}/ has PR number out of valid range, skipping...")
            continue
        found.append((directory, number, title))
    return sorted(found, key=lambda preview: (preview[1], preview[0].name))


def index_html(found):
    """The preview index page."""
    items = []
    for directory, number, title in found:
        name = html.escape(f"{directory.name}/")
        label = f"PR #{number}: {html.escape(title)}" if title else f"PR #{number} Preview"
        items.append(f'<li><a href="/{name}">{label}</a>'
                     f'<div class="preview-url">https://{PREVIEW_HOST}/{name}</div></li>')
    page = TEMPLATE.read_text()
    for marker in (PLACEHOLDER, HIDDEN_EMPTY_STATE):
        if marker not in page:
            raise ValueError(f"{TEMPLATE} has no {marker}")
    if not items:
        page = page.replace(HIDDEN_EMPTY_STATE, 'id="empty-state"')
    return page.replace(PLACEHOLDER, "".join(items))


def next_revision():
    """git describe for the commit that will hold the file, without its hash."""
    try:
        describe = subprocess.run(
            ["git", "describe", "--tags", "--long", "--match", "v[0-9]*", "HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as err:
        print(f"ERROR: git describe failed: {err.stderr.strip()}")
        raise
    match = re.fullmatch(r"(.+)-([0-9]+)-g[0-9a-f]+", describe)
    if not match:
        raise ValueError(f"unexpected git describe output {describe!r}")
    return f"{match.group(1)}-{int(match.group(2)) + 1}"


def preview_items(directory):
    """The preview's redirects, moved under it, or [] with a warning."""
    path = directory / "redirects.json"
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as err:
        print(f"Warning: skipping {path}: {err}")
        return []
    if not isinstance(data, list):
        print(f"Warning: skipping {path}: not a JSON array")
        return []
    items = []
    seen = set()
    other_hosts = 0
    for item in data:
        redirect = item.get("redirect") if isinstance(item, dict) else None
        source = redirect.get("source_url") if isinstance(redirect, dict) else None
        target = redirect.get("target_url") if isinstance(redirect, dict) else None
        if isinstance(source, str) and HOSTED.match(source) and not source.startswith(f"{PRODUCTION_HOST}/"):
            # The buy.wafer.space campaign links: previews only cover the preview host
            other_hosts += 1
            continue
        if (not isinstance(source, str) or not source.startswith(f"{PRODUCTION_HOST}/")
                or not isinstance(target, str) or not ABSOLUTE.match(target)):
            print(f"Warning: skipping an entry of {path}: {json.dumps(item)[:200]}")
            continue
        if source == f"{PRODUCTION_HOST}/revision":
            continue
        if source in seen:
            print(f"Warning: skipping a second entry for {source} in {path}")
            continue
        seen.add(source)
        match = TARGET.match(target)
        comment = item.get("comment")
        items.append({
            **({"comment": comment} if isinstance(comment, str) else {}),
            "redirect": {
                "source_url": f"{PREVIEW_HOST}/{directory.name}/{source[len(PRODUCTION_HOST) + 1:]}",
                "target_url": f"https://{PREVIEW_HOST}/{directory.name}/{match.group(1)}" if match else target,
                "status_code": 302,
                **{key: redirect[key] for key in KEPT_FIELDS if isinstance(redirect.get(key), bool)},
            },
        })
    if other_hosts:
        print(f"Left out {other_hosts} entries of {path} for other hosts")
    return items


def redirects_json(found, commit):
    """The preview list, starting with its revision item, and how many previews it covers."""
    items = []
    covered = 0
    for directory, _, title in found:
        # The pr-NNN-title aliases only redirect to their pr-NNN directory
        if not title and (directory / "redirects.json").is_file():
            moved = preview_items(directory)
            covered += bool(moved)
            items += moved
    items.sort(key=lambda item: item["redirect"]["source_url"])
    revision = next_revision()
    items.insert(0, {
        "comment": f"{revision} {commit[:7]}",
        "redirect": {
            "source_url": f"{PREVIEW_HOST}/revision",
            "target_url": f"{COMMIT_URL}{commit}",
            "status_code": 302,
        },
    })
    return items, covered, revision


def main():
    commit = os.environ.get("PREVIEW_SOURCE_COMMIT", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        print("ERROR: PREVIEW_SOURCE_COMMIT must be the full hash of the site commit being deployed")
        return 1
    found = previews(d for d in Path(".").iterdir() if d.is_dir())
    page = index_html(found)
    items, covered, revision = redirects_json(found, commit)

    Path("index.html").write_text(page)
    Path("redirects.json").write_text(json.dumps(items, indent=2) + "\n")
    print(f"Generated preview index with {len(found)} active previews")
    print(f"Wrote redirects.json at {revision}: {len(items)} entries from {covered} preview(s)")
    if len(items) > WARN_TOTAL:
        print(f"::warning::The preview redirect list has {len(items)} entries; Cloudflare allows 10,000 across all lists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
