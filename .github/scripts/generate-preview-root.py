#!/usr/bin/env python3
"""Generate the root of preview.wafer.space: index.html and redirects.json.

Run from the root of the preview.wafer.space repository, just before the
commit that will hold the result (pr-preview.yml and cleanup-previews.yml run
it after adding or removing previews). Both files are built first and only
then written, so a failure leaves the previous pair in place.

index.html lists every pr-NNN preview (and its pr-NNN-title alias), from
.github/templates/preview-index.html next to this script.

redirects.json is the body of Cloudflare's "replace list items" call for the
preview_wafer_space Bulk Redirect list, which the redirects sync Worker
(https://github.com/wafer-space/cloudflare-redirects-sync) loads as is. Each
pr-NNN preview's redirects.json (written by _plugins/redirect_list.rb for the
production hostname) is moved under the preview:

- source wafer.space/<path> becomes preview.wafer.space/pr-NNN/<path>;
- a target on https://wafer.space follows it under
  https://preview.wafer.space/pr-NNN/, and any other target is left as is;
- the status becomes 302, because browsers cache a 301 indefinitely and a
  preview's redirects change with every push.

Its first item records the revision, as the Worker requires:
preview.wafer.space/revision redirects to PREVIEW_SOURCE_COMMIT (the site
commit whose deploy or cleanup wrote this), and its comment is the git
describe number of the preview repository commit that will hold the file
(HEAD's plus one), so the numbers only go up as the preview repository's
history grows, including when a deploy merges in another one's push.
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
EMPTY_STATE = "<script>document.getElementById('empty-state').style.display = 'block';</script>"

PRODUCTION_HOST = "wafer.space"
PREVIEW_HOST = "preview.wafer.space"
COMMIT_URL = "https://github.com/wafer-space/wafer-space.github.io/commit/"
# pr-123, or its pr-123-some-title alias
LISTED_DIR = re.compile(r"^pr-([0-9]+)(?:-(.*))?$")
# Only the pr-123 directories hold a preview's own redirects.json
PREVIEW_DIR = re.compile(r"^pr-[0-9]+$")
TARGET = re.compile(r"^https://wafer\.space(?=$|[/?#])/?(.*)$", re.S)
# Cloudflare's Free plan allows 10,000 redirects across all lists
WARN_TOTAL = 9000


def index_html(directories):
    """The preview index page, and how many previews it lists."""
    items = []
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
        name = html.escape(f"{directory.name}/")
        label = f"PR #{number}: {html.escape(title)}" if title else f"PR #{number} Preview"
        items.append(f'<li><a href="/{name}">{label}</a>'
                     f'<div class="preview-url">https://{PREVIEW_HOST}/{name}</div></li>')
    template = TEMPLATE.read_text()
    if PLACEHOLDER not in template:
        raise ValueError(f"{TEMPLATE} has no {PLACEHOLDER}")
    return template.replace(PLACEHOLDER, "".join(items) or EMPTY_STATE), len(items)


def next_revision():
    """git describe for the commit that will hold the file, without its hash."""
    describe = subprocess.run(
        ["git", "describe", "--tags", "--long", "--match", "v[0-9]*", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
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
    for item in data:
        redirect = item.get("redirect") if isinstance(item, dict) else None
        source = redirect.get("source_url") if isinstance(redirect, dict) else None
        target = redirect.get("target_url") if isinstance(redirect, dict) else None
        if not isinstance(source, str) or not source.startswith(f"{PRODUCTION_HOST}/") or not isinstance(target, str):
            print(f"Warning: skipping an entry of {path}: {json.dumps(item)[:200]}")
            continue
        match = TARGET.match(target)
        items.append({
            **({"comment": item["comment"]} if "comment" in item else {}),
            "redirect": {
                **redirect,
                "source_url": f"{PREVIEW_HOST}/{directory.name}/{source[len(PRODUCTION_HOST) + 1:]}",
                "target_url": f"https://{PREVIEW_HOST}/{directory.name}/{match.group(1)}" if match else target,
                "status_code": 302,
            },
        })
    return items


def redirects_json(directories, commit):
    """The preview list, starting with its revision item, and how many previews it covers."""
    items = []
    previews = 0
    for directory in directories:
        if PREVIEW_DIR.match(directory.name) and (directory / "redirects.json").is_file():
            found = preview_items(directory)
            previews += bool(found)
            items += found
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
    return items, previews, revision


def main():
    commit = os.environ.get("PREVIEW_SOURCE_COMMIT", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        print("ERROR: PREVIEW_SOURCE_COMMIT must be the full hash of the site commit being deployed")
        return 1
    directories = sorted(d for d in Path(".").iterdir() if d.is_dir() and d.name.startswith("pr-"))
    page, listed = index_html(directories)
    items, previews, revision = redirects_json(directories, commit)

    Path("index.html").write_text(page)
    Path("redirects.json").write_text(json.dumps(items, indent=2) + "\n")
    print(f"Generated preview index with {listed} active previews")
    print(f"Wrote redirects.json at {revision}: {len(items)} entries from {previews} preview(s)")
    if len(items) > WARN_TOTAL:
        print(f"::warning::The preview redirect list has {len(items)} entries; Cloudflare allows 10,000 across all lists")
    return 0


if __name__ == "__main__":
    sys.exit(main())
