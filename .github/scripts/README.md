# GitHub Scripts Documentation

This directory contains the scripts used by the GitHub Actions workflows.

## Comment Lifecycle Management

### comment-verification-results.js

Manages verification comment lifecycle to keep PR comment threads clean:

**Features:**
- Creates new verification comments with current results
- Archives previous verification comments using collapsible sections
- Identifies verification comments using unique HTML markers
- Preserves comment history for accountability

**Usage:**
```javascript
// In GitHub Actions workflow (from repository root)
const commentVerificationResults = require('./.github/scripts/comment-verification-results.js');
const result = await commentVerificationResults(github, context, core);
```

**Environment Variables Required:**
- `VERIFICATION_STATUS`: 'success' or 'failed'
- `REPORT_CONTENT`: Full verification report content
- `GITHUB_RUN_ID`: Current workflow run ID

**Comment Structure:**
- New comments show full verification details prominently
- Old comments are collapsed with "Previous verification results (archived)" header
- All verification comments have `<!-- VERIFICATION_COMMENT_MARKER -->` for identification
- Timestamps and run IDs help track verification history

**Benefits:**
- ✅ Only latest verification is prominently visible
- ✅ Historical data preserved but collapsed
- ✅ Clean PR comment threads
- ✅ Easy identification of verification comments
- ✅ Graceful error handling for individual comment updates

### report-production-links.js

Keeps one issue, labelled `broken-links`, tracking the production link check
(`production-verification.yml`). A failed check opens the issue or adds the
report to it as a comment; a passing check closes it. Issues are recognised by
the `<!-- PRODUCTION_LINK_CHECK -->` marker in their body.

**Environment Variables Required:**
- `CHECK_STATUS`: 'success' or 'failed'
- `REPORT_CONTENT`: Full verification report content
- `GITHUB_RUN_ID`: Current workflow run ID

## Link Checking

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

### Other Scripts

- `generate-pr-directory-name.js`: Generates slugified directory names (`pr-preview-deploy.yml`)
- `generate-preview-index.sh`: Builds the preview.wafer.space index page (`pr-preview-deploy.yml`, `cleanup-previews.yml`)
- `verify-preview-site.sh`: Runs the preview checks by hand (see `.github/docs/preview-verification.md`)

Preview deployment records and PR comments are created inline in `pr-preview-deploy.yml`.

## Best Practices

1. **Error Handling**: All scripts include comprehensive error handling
2. **Input Validation**: User inputs are validated and sanitized
3. **Idempotent Operations**: Scripts can be run multiple times safely
4. **Logging**: Detailed console output for debugging
5. **Security**: Path validation and input sanitization throughout
