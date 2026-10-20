#!/usr/bin/env python3
"""Summarise muffet's verbose JSON output for the preview verification report.

muffet runs with --skip-tls-verification so that a site with an expired or
otherwise invalid certificate doesn't fail the check. This script:

1. Writes the broken links in muffet's usual text format (page URL followed
   by tab-indented "<status or error>\t<link>" lines) to --failures.
2. Checks the TLS certificate of every external HTTPS host muffet visited and
   writes a Markdown list of invalid ones to --tls-warnings, also printing a
   GitHub Actions ::warning:: annotation for each. These never fail the job.

Uses only the standard library so it runs on a bare GitHub runner.
"""

import argparse
import concurrent.futures
import json
import socket
import ssl
import sys
import urllib.parse


def load_results(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        # muffet failed before producing JSON (e.g. the site was unreachable);
        # pass its raw output through so the report still shows something
        return [], text


def format_failures(results):
    lines = []
    for page in results:
        broken = [link for link in page.get("links", []) if "error" in link]
        if not broken:
            continue
        lines.append(page["url"])
        for link in broken:
            lines.append(f"\t{link['error']}\t{link['url']}")
    return lines


def https_hosts(results, own_host):
    hosts = set()
    for page in results:
        for link in page.get("links", []):
            parsed = urllib.parse.urlsplit(link["url"])
            if parsed.scheme == "https" and parsed.hostname and parsed.hostname != own_host:
                hosts.add((parsed.hostname, parsed.port or 443))
    return sorted(hosts)


def certificate_problem(host, port):
    """Return a description of the certificate problem, or None if it's valid.

    Connection failures are not reported here; muffet already reports hosts
    it couldn't reach.
    """
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=15) as sock:
            with context.wrap_socket(sock, server_hostname=host):
                return None
    except ssl.SSLCertVerificationError as e:
        return e.verify_message or str(e)
    except (OSError, ssl.SSLError):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("json_report", help="muffet --format=json --verbose output")
    parser.add_argument("--site-url", required=True, help="URL muffet was run against")
    parser.add_argument("--failures", required=True, help="where to write broken links")
    parser.add_argument("--tls-warnings", required=True, help="where to write TLS warnings")
    args = parser.parse_args()

    results, raw = load_results(args.json_report)

    with open(args.failures, "w", encoding="utf-8") as f:
        if raw is not None:
            f.write(raw)
        else:
            f.write("".join(f"{line}\n" for line in format_failures(results)))

    own_host = urllib.parse.urlsplit(args.site_url).hostname
    hosts = https_hosts(results, own_host)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        problems = list(pool.map(lambda hp: certificate_problem(*hp), hosts))

    with open(args.tls_warnings, "w", encoding="utf-8") as f:
        for (host, port), problem in zip(hosts, problems):
            if problem is None:
                continue
            name = host if port == 443 else f"{host}:{port}"
            f.write(f"- ⚠️ `{name}`: {problem}\n")
            print(f"::warning title=Invalid TLS certificate::{name}: {problem}")

    print(f"Checked TLS certificates of {len(hosts)} external hosts", file=sys.stderr)


if __name__ == "__main__":
    main()
