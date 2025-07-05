#!/bin/bash
# Comprehensive preview site verification script
# This script performs detailed verification of PR preview deployments

set -e

PREVIEW_URL="$1"
PR_NUMBER="$2"

if [ -z "$PREVIEW_URL" ] || [ -z "$PR_NUMBER" ]; then
    echo "Usage: $0 <preview_url> <pr_number>"
    echo "Example: $0 https://preview.wafer.space/pr-2/ 2"
    exit 1
fi

# Check for required dependencies
echo "Checking dependencies..."

# Check for jq (required for JSON processing)
if ! command -v jq &> /dev/null; then
    echo "ERROR: jq is required but not installed"
    echo ""
    echo "Please install jq:"
    echo "  Ubuntu/Debian: sudo apt-get install jq"
    echo "  macOS:         brew install jq"
    echo "  CentOS/RHEL:   sudo yum install jq"
    echo "  Alpine:        apk add jq"
    echo ""
    echo "Or visit: https://jqlang.github.io/jq/download/"
    exit 1
fi

# Check for curl (should be available on most systems)
if ! command -v curl &> /dev/null; then
    echo "ERROR: curl is required but not installed"
    echo "Please install curl using your system's package manager"
    exit 1
fi

# Check for bc (used for floating-point arithmetic)
if ! command -v bc &> /dev/null; then
    echo "WARNING: bc is not installed - performance calculations may be limited"
    echo "Install with: sudo apt-get install bc (Ubuntu/Debian)"
fi

echo "✅ Dependencies verified"

echo "Starting comprehensive verification of: $PREVIEW_URL"
echo "PR Number: $PR_NUMBER"

# Create detailed verification report
REPORT_FILE="detailed-verification.json"
echo "{" > $REPORT_FILE
echo "  \"pr_number\": $PR_NUMBER," >> $REPORT_FILE
echo "  \"preview_url\": \"$PREVIEW_URL\"," >> $REPORT_FILE
echo "  \"timestamp\": \"$(date -u --iso-8601=seconds)\"," >> $REPORT_FILE
echo "  \"checks\": {" >> $REPORT_FILE

# Function to add check result to JSON
add_check_result() {
    local check_name="$1"
    local status="$2"
    local details="$3"
    
    echo "    \"$check_name\": {" >> $REPORT_FILE
    echo "      \"status\": \"$status\"," >> $REPORT_FILE
    echo "      \"details\": \"$details\"" >> $REPORT_FILE
    echo "    }," >> $REPORT_FILE
}

# 1. HTTP Response Check
echo "Checking HTTP response..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$PREVIEW_URL" || echo "000")
RESPONSE_TIME=$(curl -s -w "%{time_total}" -o /dev/null "$PREVIEW_URL" || echo "0")

if [ "$HTTP_STATUS" = "200" ]; then
    add_check_result "http_response" "pass" "HTTP $HTTP_STATUS, Response time: ${RESPONSE_TIME}s"
else
    add_check_result "http_response" "fail" "HTTP $HTTP_STATUS, Response time: ${RESPONSE_TIME}s"
fi

# 2. Content Verification
echo "Verifying page content..."
CONTENT=$(curl -s "$PREVIEW_URL" 2>/dev/null || echo "")

# Check for key content elements
CONTENT_CHECKS=(
    "wafer.space:Site title present"
    "Budget silicon manufacturing:Tagline present"
    "<!DOCTYPE html:Valid HTML document"
    "<title>:Page title tag"
)

# Check baseurl configuration (flexible check)
if echo "$CONTENT" | grep -q "window.siteBaseurl = '/pr-$PR_NUMBER'"; then
    add_check_result "baseurl_configuration" "pass" "JavaScript baseurl configuration found"
elif echo "$CONTENT" | grep -q "src=\"/pr-$PR_NUMBER/"; then
    add_check_result "baseurl_configuration" "pass" "Assets use correct PR baseurl paths"
else
    add_check_result "baseurl_configuration" "warn" "Baseurl configuration not detected (may use alternative method)"
fi

for check in "${CONTENT_CHECKS[@]}"; do
    IFS=':' read -r pattern description <<< "$check"
    if echo "$CONTENT" | grep -q "$pattern"; then
        add_check_result "content_$(echo "$description" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')" "pass" "$description found"
    else
        add_check_result "content_$(echo "$description" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')" "fail" "$description missing"
    fi
done

# 3. Asset Verification - Test actual HTML-referenced assets
echo "Verifying critical assets from HTML..."

# Extract all CSS and JS assets from the actual HTML
echo "Extracting asset URLs from HTML content..."
CSS_ASSETS=$(echo "$CONTENT" | grep -oE 'href="[^"]*\.css"' | grep -oE '"[^"]*"' | tr -d '"')
JS_ASSETS=$(echo "$CONTENT" | grep -oE 'src="[^"]*\.js"' | grep -oE '"[^"]*"' | tr -d '"')
IMAGE_ASSETS=$(echo "$CONTENT" | grep -oE '(src|href)="[^"]*\.(png|jpg|jpeg|webp|ico)"' | grep -oE '"[^"]*"' | tr -d '"' | head -5)

# Test all extracted assets
ALL_ASSETS="$CSS_ASSETS"$'\n'"$JS_ASSETS"$'\n'"$IMAGE_ASSETS"

TOTAL_ASSETS=0
FAILED_ASSETS=0

while IFS= read -r asset_path; do
    if [ -n "$asset_path" ]; then
        TOTAL_ASSETS=$((TOTAL_ASSETS + 1))
        
        # Handle relative vs absolute paths
        if [[ "$asset_path" == /* ]]; then
            FULL_ASSET_URL="https://preview.wafer.space$asset_path"
        else
            FULL_ASSET_URL="$PREVIEW_URL$asset_path"
        fi
        
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FULL_ASSET_URL")
        ASSET_NAME=$(basename "$asset_path")
        
        if [ "$HTTP_CODE" = "200" ]; then
            add_check_result "asset_$(echo "$ASSET_NAME" | tr '.' '_')" "pass" "$ASSET_NAME loaded successfully"
        else
            add_check_result "asset_$(echo "$ASSET_NAME" | tr '.' '_')" "fail" "$ASSET_NAME failed (HTTP $HTTP_CODE) - $asset_path"
            FAILED_ASSETS=$((FAILED_ASSETS + 1))
            echo "FAILED ASSET: $asset_path -> $FULL_ASSET_URL (HTTP $HTTP_CODE)"
        fi
    fi
done <<< "$ALL_ASSETS"

echo "Asset verification: $FAILED_ASSETS/$TOTAL_ASSETS failed"

# 4. Comprehensive Link and Asset Verification with muffet
echo "Running comprehensive link and asset verification with muffet..."

# Check if muffet is available
if ! command -v muffet &> /dev/null; then
    add_check_result "muffet_availability" "fail" "muffet not installed - install with: go install github.com/raviqqe/muffet/v2@latest"
    echo "ERROR: muffet is required but not installed"
    exit 1
fi

# Run muffet for comprehensive verification
if muffet --timeout=30 --max-connections=10 --exclude=".*mailto:.*" "$PREVIEW_URL" > muffet-report.txt 2>&1; then
    add_check_result "muffet_verification" "pass" "All links and assets verified by muffet"
    echo "✅ muffet verification passed"
else
    # Count and categorize failures
    TOTAL_FAILURES=$(wc -l < muffet-report.txt 2>/dev/null || echo "0")
    HTTP_404=$(grep -c "404" muffet-report.txt 2>/dev/null || echo "0")
    
    add_check_result "muffet_verification" "fail" "muffet found $TOTAL_FAILURES issues ($HTTP_404 x 404 errors)"
    
    echo "❌ muffet verification failed with $TOTAL_FAILURES issues"
    echo "Top 10 failures:"
    head -10 muffet-report.txt || echo "Could not read muffet report"
    
    # This is a critical failure for asset verification
    echo "CRITICAL: muffet detected broken links or assets"
fi

# 5. Mobile Responsiveness Check
echo "Checking mobile responsiveness..."
MOBILE_CONTENT=$(curl -s -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15" "$PREVIEW_URL" 2>/dev/null || echo "")

if echo "$MOBILE_CONTENT" | grep -q 'name="viewport"'; then
    add_check_result "mobile_viewport" "pass" "Viewport meta tag present"
else
    add_check_result "mobile_viewport" "fail" "Viewport meta tag missing"
fi

# 6. Performance Check
echo "Performing performance check..."
if (( $(echo "$RESPONSE_TIME < 3.0" | bc -l 2>/dev/null) )); then
    add_check_result "performance_load_time" "pass" "Load time acceptable: ${RESPONSE_TIME}s"
elif (( $(echo "$RESPONSE_TIME < 5.0" | bc -l 2>/dev/null) )); then
    add_check_result "performance_load_time" "warn" "Load time slow: ${RESPONSE_TIME}s"
else
    add_check_result "performance_load_time" "fail" "Load time too slow: ${RESPONSE_TIME}s"
fi

# 7. Security Headers Check
echo "Checking security headers..."
SECURITY_HEADERS=$(curl -s -I "$PREVIEW_URL" 2>/dev/null || echo "")

if echo "$SECURITY_HEADERS" | grep -qi "x-frame-options"; then
    add_check_result "security_xframe" "pass" "X-Frame-Options header present"
else
    add_check_result "security_xframe" "info" "X-Frame-Options header missing (may be handled by CDN)"
fi

if echo "$SECURITY_HEADERS" | grep -qi "x-content-type-options"; then
    add_check_result "security_content_type" "pass" "X-Content-Type-Options header present"
else
    add_check_result "security_content_type" "info" "X-Content-Type-Options header missing (may be handled by CDN)"
fi

# Close JSON structure (remove last comma)
sed -i '$ s/,$//' $REPORT_FILE
echo "  }" >> $REPORT_FILE
echo "}" >> $REPORT_FILE

echo "Verification completed. Report saved to: $REPORT_FILE"

# Generate summary
TOTAL_CHECKS=$(jq '.checks | length' $REPORT_FILE)
PASSED_CHECKS=$(jq '.checks | to_entries | map(select(.value.status == "pass")) | length' $REPORT_FILE)
FAILED_CHECKS=$(jq '.checks | to_entries | map(select(.value.status == "fail")) | length' $REPORT_FILE)
WARN_CHECKS=$(jq '.checks | to_entries | map(select(.value.status == "warn")) | length' $REPORT_FILE)

echo ""
echo "=== VERIFICATION SUMMARY ==="
echo "Total checks: $TOTAL_CHECKS"
echo "Passed: $PASSED_CHECKS"
echo "Failed: $FAILED_CHECKS"
echo "Warnings: $WARN_CHECKS"
echo ""

if [ "$FAILED_CHECKS" -gt 0 ]; then
    echo "❌ VERIFICATION FAILED"
    echo "Failed checks:"
    jq -r '.checks | to_entries | map(select(.value.status == "fail")) | .[] | "  - \(.key): \(.value.details)"' $REPORT_FILE
    exit 1
else
    echo "✅ VERIFICATION PASSED"
    if [ "$WARN_CHECKS" -gt 0 ]; then
        echo "Warnings:"
        jq -r '.checks | to_entries | map(select(.value.status == "warn")) | .[] | "  - \(.key): \(.value.details)"' $REPORT_FILE
    fi
fi