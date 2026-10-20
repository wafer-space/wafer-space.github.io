# GitHub Scripts

- `verify-preview-site.sh`: Runs the preview checks by hand (see `.github/docs/preview-verification.md`)

The PR preview workflows (`pr-preview-build.yml`, `pr-preview-deploy.yml`, `preview-verification.yml` and `cleanup-previews.yml`) run actions from [wafer-space/actions](https://github.com/wafer-space/actions/tree/main/pr-preview), pinned to a commit. Their scripts and templates live there, so the privileged preview jobs never run code from the pull request being previewed. See `.github/workflows/pr-preview.md`.

## Production Link Check

### report-production-links.js

Keeps one issue, labelled `broken-links`, tracking the production link check
(`production-verification.yml`). A failed check opens the issue or adds the
report to it as a comment; a passing check closes it. Issues are recognised by
the `<!-- PRODUCTION_LINK_CHECK -->` marker in their body.

**Environment Variables Required:**
- `CHECK_STATUS`: 'success' or 'failed'
- `REPORT_CONTENT`: Full verification report content
- `GITHUB_RUN_ID`: Current workflow run ID

### Link Checking

- `check-links.sh <site-url> <json-report> [extra muffet options...]`: runs
  muffet with the shared configuration, including the exclude list (don't
  extend it without asking, see `CLAUDE.md`). Exits 0 (all fine), 1 (broken
  links in the report) or 2 (muffet couldn't check the site; its stderr is in
  the `.err` file next to the report). Used by both the preview and the
  production checks.
- `summarise-muffet.py`: turns muffet's JSON into the broken-link list and the
  TLS-certificate warnings for the report.
- `wait-for-commit.py <site-url> [--commit SHA [--or-descendant]]`: waits
  until a deployed copy of the site is serving, or is serving the given commit
  (or, with `--or-descendant`, a later one).
- `sibling-sites.py`: lists the organisation's other GitHub Pages sites, which
  share the production domain, as names or as muffet `--exclude` arguments.
- `check-sibling-links.py`: checks this site's links into those sibling sites
  (status and fragment), since muffet is told not to follow them.
