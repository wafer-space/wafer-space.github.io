# GitHub Scripts Documentation

This directory contains reusable JavaScript modules for GitHub Actions workflows.

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

### comment-pr-preview.js

Manages PR preview deployment comments with update capability:
- Updates existing preview comments instead of creating duplicates
- Handles preview deployment status changes
- Uses template-based comment generation

### Other Scripts

- `create-deployment.js`: Creates GitHub deployment records
- `update-deployment-status.js`: Updates deployment status
- `comment-pr-cleanup.js`: Comments when previews are cleaned up
- `cleanup-deployments.js`: Marks deployments as inactive
- `generate-pr-directory-name.js`: Generates slugified directory names

## Best Practices

1. **Error Handling**: All scripts include comprehensive error handling
2. **Input Validation**: User inputs are validated and sanitized
3. **Idempotent Operations**: Scripts can be run multiple times safely
4. **Logging**: Detailed console output for debugging
5. **Security**: Path validation and input sanitization throughout

## Testing and Validation

### Manual Testing
This PR demonstrates the comment lifecycle management through:
1. **Integration Testing**: Multiple verification runs on PR #12 validate the archival system
2. **UI Testing**: Verification that collapsed sections render correctly in GitHub interface
3. **Error Handling**: Graceful handling when comment updates fail

### Recommended Unit Tests
Future improvements could include:
- **Archive Logic**: Test comment identification and archival transformation
- **Error Scenarios**: Test behavior when GitHub API calls fail
- **Comment Parsing**: Test extraction of verification markers and content
- **Environment Validation**: Test required environment variable handling

### Testing Notes

This documentation update is used to test the verification comment lifecycle management system by triggering a second verification run.