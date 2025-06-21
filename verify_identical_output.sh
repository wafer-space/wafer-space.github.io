#!/bin/bash

# Script to verify that the refactored Jekyll theme generates identical output
# to the target commit, and cleanup temporary files if verification passes.

set -e

# Configuration
TARGET_COMMIT="a0a205bc9ed76b1a7625ef0fa14df95169f50987"
REFERENCE_DIR="_site_reference"
REFACTORED_DIR="_site_refactored_verify"
PATH="$PATH:/home/tim/.local/share/gem/ruby/3.2.0/bin"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Jekyll Theme Verification Script ===${NC}"
echo "Target commit: $TARGET_COMMIT"
echo

# Function to cleanup temporary directories
cleanup() {
    echo -e "${YELLOW}Cleaning up temporary directories...${NC}"
    rm -rf "$REFERENCE_DIR" "$REFACTORED_DIR"
    echo -e "${GREEN}Cleanup complete.${NC}"
}

# Function to build reference site from target commit
build_reference() {
    echo -e "${BLUE}Building reference site from target commit...${NC}"
    
    # Save current state
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    
    # Build reference
    git checkout "$TARGET_COMMIT" --quiet
    bundle exec jekyll build --destination "$REFERENCE_DIR" --quiet
    
    # Restore current state
    git checkout "$CURRENT_BRANCH" --quiet
    
    echo -e "${GREEN}Reference site built successfully.${NC}"
}

# Function to build refactored site
build_refactored() {
    echo -e "${BLUE}Building refactored site...${NC}"
    bundle exec jekyll build --destination "$REFACTORED_DIR" --quiet
    echo -e "${GREEN}Refactored site built successfully.${NC}"
}

# Function to count files
count_files() {
    local dir="$1"
    find "$dir" -name "*.html" | wc -l
}

# Function to perform verification
verify_identical() {
    echo -e "${BLUE}=== Verification Results ===${NC}"
    
    # Count HTML files
    local ref_count=$(count_files "$REFERENCE_DIR")
    local refactored_count=$(count_files "$REFACTORED_DIR")
    
    echo "HTML files in reference: $ref_count"
    echo "HTML files in refactored: $refactored_count"
    
    # Check file counts
    if [ "$ref_count" -ne "$refactored_count" ]; then
        echo -e "${RED}❌ FAIL: File count mismatch${NC}"
        return 1
    fi
    
    # Check for differences (all files must be identical except XML timestamps)
    local diff_output=$(diff -r "$REFERENCE_DIR" "$REFACTORED_DIR" 2>/dev/null || true)
    
    # Filter out timestamp differences in XML files
    local significant_diffs=$(echo "$diff_output" | grep -v "updated>" | grep -v "\.xml" || true)
    
    if [ -z "$significant_diffs" ]; then
        echo -e "${GREEN}✅ PASS: Sites are identical (ignoring XML timestamps)${NC}"
        return 0
    else
        echo -e "${RED}❌ FAIL: Significant differences found${NC}"
        echo
        echo -e "${YELLOW}Differences (first 20 lines):${NC}"
        echo "$significant_diffs" | head -20
        return 1
    fi
}

# Function to run three verification checks
run_verification_checks() {
    echo -e "${BLUE}Running three verification checks...${NC}"
    
    local checks_passed=0
    
    for i in 1 2 3; do
        echo -e "${BLUE}Verification Check $i:${NC}"
        if verify_identical; then
            ((checks_passed++))
        fi
        echo
    done
    
    if [ "$checks_passed" -eq 3 ]; then
        echo -e "${GREEN}🎯 All 3 verification checks PASSED!${NC}"
        return 0
    else
        echo -e "${RED}❌ Only $checks_passed/3 verification checks passed${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo -e "${BLUE}Starting verification process...${NC}"
    echo
    
    # Clean up any existing directories
    cleanup 2>/dev/null || true
    
    # Build both sites
    build_reference
    build_refactored
    
    echo
    
    # Run verification checks
    if run_verification_checks; then
        echo
        echo -e "${GREEN}🎉 SUCCESS: Refactored theme generates identical output!${NC}"
        echo -e "${YELLOW}Cleaning up temporary files...${NC}"
        cleanup
        echo
        echo -e "${GREEN}✅ Verification complete - all files cleaned up.${NC}"
        exit 0
    else
        echo
        echo -e "${RED}❌ FAILURE: Sites are not identical${NC}"
        echo -e "${YELLOW}Temporary directories preserved for debugging:${NC}"
        echo "  Reference: $REFERENCE_DIR"
        echo "  Refactored: $REFACTORED_DIR"
        echo
        echo -e "${YELLOW}To cleanup manually: rm -rf $REFERENCE_DIR $REFACTORED_DIR${NC}"
        exit 1
    fi
}

# Handle Ctrl+C
trap cleanup INT

# Run main function
main "$@"