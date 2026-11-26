#!/usr/bin/env bash
# Run muffet over a deployed copy of the site and write its JSON report.
#
#   check-links.sh <site-url> <json-report-path> [extra muffet options...]
#
# Exits 0 when every link and asset resolved, 1 when some didn't (the JSON
# report lists them), and 2 when muffet couldn't check the site at all (it
# couldn't fetch the root page, or an option was wrong): muffet itself exits 1
# for both, so the two are told apart by whether it wrote a JSON report. Its
# stderr is copied to <json-report-path> with .err in place of .json, for the
# report. Summarise the report with summarise-muffet.py.
#
# Extra options go to muffet after the shared ones; the production check uses
# them to keep muffet out of the sibling project sites (see
# production-verification.yml).
#
# This is the one place the link checker is configured, so the preview
# check (preview-verification.yml) and the production check
# (production-verification.yml) can't drift apart. In particular the
# --exclude list is shared: never add to it without asking first (CLAUDE.md).
#
# Identify honestly as a link checker: Cloudflare-fronted sites (e.g.
# sourceforge.io, linuxgizmos.com) challenge requests that claim to be Chrome
# but don't behave like it.
# Invalid TLS certificates on linked sites are only warned about (by
# summarise-muffet.py), so muffet skips verification.
# Crowd Supply (and buy.wafer.space, which redirects there) blocks automated
# fetches with 403s and bot challenges, so it is skipped.

set -u

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <site-url> <json-report-path> [extra muffet options...]" >&2
  exit 2
fi

SITE_URL="$1"
REPORT="$2"
shift 2
ERRORS="${REPORT%.json}.err"

STATUS=0
muffet \
  --skip-tls-verification \
  --format=json \
  --verbose \
  --timeout=30 \
  --max-connections=10 \
  --max-connections-per-host=5 \
  --rate-limit=20 \
  --buffer-size=16384 \
  --exclude=".*mailto:.*" \
  --exclude=".*linkedin\.com.*" \
  --exclude=".*hawaii\.edu.*" \
  --exclude=".*timeanddate\.com.*" \
  --exclude=".*reddit\.com.*" \
  --exclude=".*electronics-lab\.com.*" \
  --exclude=".*matrix\.to.*" \
  --exclude=".*tinytapeout\.com/chips/silicon-proven.*" \
  --exclude=".*siliconprawn\.org.*" \
  --exclude=".*rc2014\.co\.uk.*" \
  --exclude="^https?://(www\.)?crowdsupply\.com([/?#:]|$)" \
  --exclude="^https?://buy\.wafer\.space([/?#:]|$)" \
  --header="User-Agent:Mozilla/5.0 (compatible; wafer.space-link-checker; +https://wafer.space/)" \
  --header="Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8" \
  --header="Accept-Language:en-US,en;q=0.9" \
  --header="Accept-Encoding:gzip, deflate, br" \
  --header="Cache-Control:no-cache" \
  --header="Pragma:no-cache" \
  "$@" \
  "$SITE_URL" > "$REPORT" 2> "$ERRORS" || STATUS=$?
cat "$ERRORS" >&2

if [ "$STATUS" -eq 0 ]; then
  exit 0
fi
# A JSON report means muffet checked the site and some links failed
if python3 -m json.tool "$REPORT" > /dev/null; then
  exit 1
fi
echo "muffet produced no report (exit status $STATUS)" >&2
exit 2
