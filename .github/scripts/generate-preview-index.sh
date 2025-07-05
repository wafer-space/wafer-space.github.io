#!/bin/bash
set -e  # Exit on any error

# Generate the preview index page
TEMPLATE_FILE=".github/templates/preview-index.html"
OUTPUT_FILE="index.html"

# Validate template file exists
if [ ! -f "$TEMPLATE_FILE" ]; then
  echo "ERROR: Template file $TEMPLATE_FILE not found!"
  echo "This indicates a problem with the workflow setup."
  exit 1
fi

# Start with the template
if ! cp "$TEMPLATE_FILE" "$OUTPUT_FILE"; then
  echo "ERROR: Failed to copy template file to $OUTPUT_FILE"
  exit 1
fi

# Generate preview items HTML
PREVIEW_ITEMS=""
FOUND_PREVIEWS=false
PREVIEW_COUNT=0

for dir in pr-*/; do
  if [ -d "$dir" ] && [ "$dir" != "pr-preview/" ]; then
    # Validate directory contains expected files
    if [ ! -f "$dir/index.html" ]; then
      echo "Warning: $dir appears to be incomplete (no index.html), skipping..."
      continue
    fi
    
    # Extract PR number from directory name (handles both old pr-123 and new pr-123-title formats)
    pr_num=$(basename "$dir" | sed 's/pr-\([0-9][0-9]*\).*/\1/')
    # Validate PR number is numeric
    if ! [[ "$pr_num" =~ ^[0-9]+$ ]]; then
      echo "Warning: $dir has invalid PR number format, skipping..."
      continue
    fi
    
    # Extract title part if it exists (for display purposes)
    title_part=$(basename "$dir" | sed 's/pr-[0-9][0-9]*-\(.*\)/\1/' | sed 's/-/ /g')
    if [ "$title_part" = "$(basename "$dir")" ]; then
      # No title part found, use empty string
      title_part=""
    fi
    
    # Additional validation: PR number must be reasonable range
    if [ "$pr_num" -lt 1 ] || [ "$pr_num" -gt 99999 ]; then
      echo "Warning: $dir has PR number out of valid range, skipping..."
      continue
    fi
    
    # HTML escape the directory name to prevent injection
    dir_escaped=$(echo "$dir" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g; s/'"'"'/\&#x27;/g')
    pr_num_escaped=$(echo "$pr_num" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g; s/'"'"'/\&#x27;/g')
    title_part_escaped=$(echo "$title_part" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g; s/'"'"'/\&#x27;/g')
    
    # Create display title
    if [ -n "$title_part" ]; then
      display_title="PR #$pr_num_escaped: $title_part_escaped"
    else
      display_title="PR #$pr_num_escaped Preview"
    fi
    
    PREVIEW_ITEMS+="<li>"
    PREVIEW_ITEMS+="<a href=\"/$dir_escaped\">$display_title</a>"
    PREVIEW_ITEMS+="<div class=\"preview-url\">https://preview.wafer.space/$dir_escaped</div>"
    PREVIEW_ITEMS+="</li>"
    FOUND_PREVIEWS=true
    PREVIEW_COUNT=$((PREVIEW_COUNT + 1))
  fi
done

# If no previews found, show empty state
if [ "$FOUND_PREVIEWS" = false ]; then
  PREVIEW_ITEMS="<script>document.getElementById('empty-state').style.display = 'block';</script>"
fi

# Replace placeholder with actual items
if ! sed -i "s|<!-- PREVIEW_ITEMS_PLACEHOLDER -->|$PREVIEW_ITEMS|g" "$OUTPUT_FILE"; then
  echo "ERROR: Failed to replace placeholder in template"
  echo "Check template file format and placeholder existence"
  exit 1
fi

# Validate output file was created successfully
if [ ! -f "$OUTPUT_FILE" ] || [ ! -s "$OUTPUT_FILE" ]; then
  echo "ERROR: Output file $OUTPUT_FILE was not created or is empty"
  exit 1
fi

echo "Generated preview index with $PREVIEW_COUNT active previews"