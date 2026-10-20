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

### Other Scripts

- `generate-pr-directory-name.js`: Generates slugified directory names (`pr-preview-deploy.yml`)
- `generate-preview-index.sh`: Builds the preview.wafer.space index page (`pr-preview-deploy.yml`, `cleanup-previews.yml`)
- `summarise-muffet.py`: Turns muffet's JSON output into the link report and warns about invalid TLS certificates (`preview-verification.yml`)
- `update-muffet.py`: Finds the latest muffet release and updates the pinned version and checksum (`update-muffet.yml`)
- `verify-preview-site.sh`: Runs the preview checks by hand (see `.github/docs/preview-verification.md`)

Preview deployment records and PR comments are created inline in `pr-preview-deploy.yml`.

## Best Practices

1. **Error Handling**: All scripts include comprehensive error handling
2. **Input Validation**: User inputs are validated and sanitized
3. **Idempotent Operations**: Scripts can be run multiple times safely
4. **Logging**: Detailed console output for debugging
5. **Security**: Path validation and input sanitization throughout
