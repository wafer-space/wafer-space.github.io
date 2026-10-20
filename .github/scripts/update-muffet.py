#!/usr/bin/env python3
"""Update the pinned muffet version and checksum in a workflow file.

preview-verification.yml installs muffet from a pinned release:

    MUFFET_VERSION="v2.11.6"
    MUFFET_SHA256="<sha256 of muffet_linux_amd64.tar.gz>"

This script finds muffet's latest release and, if it is newer than the
pinned one and at least --min-age-days old:

1. Downloads muffet_linux_amd64.tar.gz and checks its SHA256 against the
   release's own checksums file.
2. Runs the new binary's --help and checks that it still accepts every
   option the workflow passes to muffet.
3. Rewrites MUFFET_VERSION and MUFFET_SHA256 in the workflow.

Writes updated/version/previous_version/release_url to $GITHUB_OUTPUT when
set. Uses only the standard library plus the `gh` CLI (for an
authenticated GitHub API request), so it runs on a bare GitHub runner.
"""

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

REPO = "raviqqe/muffet"
ASSET = "muffet_linux_amd64.tar.gz"
VERSION_RE = re.compile(r'^(\s*MUFFET_VERSION=")(v[0-9][^"]*)(")$', re.M)
SHA256_RE = re.compile(r'^(\s*MUFFET_SHA256=")([0-9a-f]{64})(")$', re.M)
# The muffet invocation runs from `if muffet \` to the line with "$PREVIEW_URL"
INVOCATION_RE = re.compile(r"^\s*if muffet \\\n(.*?)\"\$PREVIEW_URL\"", re.M | re.S)


def parse_version(tag):
    return tuple(int(part) for part in re.findall(r"\d+", tag))


def single_match(pattern, text, what):
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        sys.exit(f"Expected exactly one {what} in the workflow, found {len(matches)}")
    return matches[0]


def latest_release():
    out = subprocess.run(
        ["gh", "api", f"repos/{REPO}/releases/latest"],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out)


def download(url, dest):
    with urllib.request.urlopen(url, timeout=60) as resp, open(dest, "wb") as f:
        f.write(resp.read())


def published_checksum(release):
    name = f"muffet_{release['tag_name'].lstrip('v')}_checksums.txt"
    asset = next((a for a in release["assets"] if a["name"] == name), None)
    if asset is None:
        sys.exit(f"{release['tag_name']} has no {name} asset")
    with urllib.request.urlopen(asset["browser_download_url"], timeout=60) as resp:
        for line in resp.read().decode().splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[1] == ASSET:
                return parts[0]
    sys.exit(f"{name} has no entry for {ASSET}")


def check_options(binary, invocation):
    """Fail if the new muffet no longer accepts an option the workflow uses."""
    used = sorted(set(re.findall(r"(--[a-z][a-z0-9-]*)", invocation)))
    help_text = subprocess.run([binary, "--help"], capture_output=True, text=True).stdout
    missing = [opt for opt in used if not re.search(rf"{re.escape(opt)}\b", help_text)]
    if missing:
        sys.exit(f"New muffet doesn't accept options the workflow uses: {', '.join(missing)}")
    print(f"New muffet accepts all {len(used)} options the workflow uses")


def set_outputs(**outputs):
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            for key, value in outputs.items():
                f.write(f"{key}={value}\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("workflow", type=pathlib.Path)
    parser.add_argument("--min-age-days", type=int, default=7,
                        help="skip releases newer than this, to let problems surface first")
    args = parser.parse_args()

    text = args.workflow.read_text(encoding="utf-8")
    current = single_match(VERSION_RE, text, "MUFFET_VERSION").group(2)
    single_match(SHA256_RE, text, "MUFFET_SHA256")
    invocation = single_match(INVOCATION_RE, text, "muffet invocation").group(1)

    release = latest_release()
    latest = release["tag_name"]
    print(f"Pinned: {current}, latest release: {latest}")
    # The tag ends up in a branch name and the workflow file, so insist on vX.Y.Z
    if not re.fullmatch(r"v\d+\.\d+\.\d+", latest):
        sys.exit(f"Unexpected muffet release tag {latest!r}")
    if parse_version(latest) <= parse_version(current):
        set_outputs(updated="false")
        return

    published = datetime.datetime.fromisoformat(release["published_at"].replace("Z", "+00:00"))
    age = datetime.datetime.now(datetime.timezone.utc) - published
    if age < datetime.timedelta(days=args.min_age_days):
        print(f"{latest} is only {age.days} days old (minimum {args.min_age_days}), not updating yet")
        set_outputs(updated="false")
        return

    asset = next((a for a in release["assets"] if a["name"] == ASSET), None)
    if asset is None:
        sys.exit(f"{latest} has no {ASSET} asset")
    expected = published_checksum(release)

    with tempfile.TemporaryDirectory() as tmp:
        tarball = pathlib.Path(tmp, ASSET)
        download(asset["browser_download_url"], tarball)
        actual = hashlib.sha256(tarball.read_bytes()).hexdigest()
        if actual != expected:
            sys.exit(f"Checksum mismatch for {ASSET}: published {expected}, downloaded {actual}")
        print(f"{ASSET} matches the published SHA256 {expected}")

        with tarfile.open(tarball) as tar:
            tar.extract("muffet", tmp, filter="data")
        binary = pathlib.Path(tmp, "muffet")
        binary.chmod(0o755)
        check_options(str(binary), invocation)

    text = VERSION_RE.sub(lambda m: f"{m.group(1)}{latest}{m.group(3)}", text)
    text = SHA256_RE.sub(lambda m: f"{m.group(1)}{expected}{m.group(3)}", text)
    args.workflow.write_text(text, encoding="utf-8")
    print(f"Updated {args.workflow} from {current} to {latest}")
    set_outputs(updated="true", version=latest, previous_version=current,
                release_url=release["html_url"])


if __name__ == "__main__":
    main()
