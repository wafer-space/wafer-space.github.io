# Preview Site Verification System

This document describes the automated verification system for PR preview deployments.

## Overview

The preview verification system automatically tests PR preview sites to ensure they work correctly. It runs after each successful preview deployment and provides detailed feedback directly in the PR.

## Verification Workflow

### Trigger
- Started with `workflow_dispatch` by `pr-preview-deploy.yml` once a preview is deployed, passing the PR number, preview URL and commit (see `.github/workflows/pr-preview.md`)
- It runs from `main`, so its runs appear in the Actions tab rather than in the PR's checks
- Can also be started by hand from the Actions tab, giving a PR number and preview URL. Leave the commit blank to use the PR's current head

### Verification Checks

1. **Basic Connectivity**
   - HTTP response status
   - Site accessibility
   - Response time measurement

2. **Content Verification**
   - Presence of expected content ("wafer.space", tagline)
   - Correct baseurl configuration
   - Valid HTML structure

3. **Asset Verification**
   - Critical assets load correctly (CSS, JS, images)
   - Favicon availability
   - Asset file sizes

4. **Link Verification**
   - Internal links functionality
   - Comprehensive link checking using `muffet`
   - Broken link detection

5. **Mobile Responsiveness**
   - Viewport meta tag presence
   - Mobile user agent testing

6. **Performance Check**
   - Page load time analysis
   - Performance thresholds

7. **Security Headers**
   - Basic security header presence
   - Content security validation

## Tools Used

- **muffet**: Comprehensive link checker
- **curl**: HTTP testing and performance measurement
- **lynx**: Text-based browser for content verification
- **jq**: JSON processing for detailed reports

## Verification Results

### Success Criteria
- All critical checks must pass
- No broken links detected
- Assets load within acceptable timeframes
- Content properly configured for preview environment

### Failure Handling
- Detailed error reporting in PR comments
- Workflow fails if critical issues detected
- Provides actionable feedback for fixing issues

## Integration

### PR Comments
Verification results are automatically posted as PR comments with:
- ✅/❌ Status indicators
- Detailed check results
- Performance metrics
- Recommendations for fixes

### Workflow Status
- Shows as separate workflow run in Actions tab
- Can be used as required status check
- Provides historical verification data

## Manual Verification

The verification script can also be run manually. Ensure dependencies are installed first:

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get install jq bc curl

# Run verification for specific PR
.github/scripts/verify-preview-site.sh https://preview.wafer.space/pr-2/ 2

# View detailed JSON report
cat detailed-verification.json | jq '.'
```

### Dependencies
- **jq**: Required for JSON processing and report generation
- **curl**: Required for HTTP requests and testing
- **bc**: Optional, used for floating-point arithmetic in performance calculations
- **muffet**: Downloaded automatically by the script if not available

## Customization

The checks are the `verify` action in [wafer-space/actions](https://github.com/wafer-space/actions/tree/main/pr-preview/verify), mostly `pr-preview/scripts/run-verification.sh` there. To change them, open a pull request there, then update the commit `preview-verification.yml` pins it to.

### Excluded URLs
The URLs muffet skips are the `muffet-excludes` input in `.github/workflows/preview-verification.yml`. Find out why a link fails before adding one (see `CLAUDE.md`).

### Thresholds and asset list
The load-time threshold and the `CRITICAL_ASSETS` list are in `run-verification.sh` in the actions repository; `verify-preview-site.sh` here has its own copies for running by hand.

## Troubleshooting

### Common Issues

1. **Link Verification Failures**
   - Check for broken internal links
   - Verify external links are accessible
   - Review baseurl configuration

2. **Asset Loading Issues**
   - Ensure assets use correct baseurl paths
   - Check file permissions and availability
   - Verify Jekyll build includes all assets

3. **Performance Issues**
   - Monitor asset sizes
   - Check for slow-loading external resources
   - Review CDN configuration

### Debug Mode
Enable debug output by setting environment variables:
```yaml
env:
  DEBUG: 1
  VERBOSE: 1
```

## Security Considerations

- Uses read-only permissions where possible
- No sensitive data exposed in verification
- Link checking excludes sensitive patterns
- Results are public in PR comments

## Future Enhancements

- Visual regression testing
- Accessibility compliance checking
- SEO verification
- Performance budgeting
- Integration with third-party monitoring tools