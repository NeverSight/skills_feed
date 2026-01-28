---
name: article-extractor
description: This skill should be used when the user wants to "download article", "extract article", "save blog post", "get article text", or provides a web URL and asks to extract the main content without ads, navigation, or clutter. Saves clean, readable text from web articles and blog posts.
allowed-tools: Bash,Read,Write
---

# Article Extractor

Extract main content from web articles and blog posts, removing navigation, ads, and clutter. Saves clean, readable text.

## Prerequisites

This skill requires [UV](https://docs.astral.sh/uv/) for dependency management. Run from the tapestry-skills project root.

## Workflow

```
URL → Validate → Detect Tool → Extract Content → Sanitize Filename → Save
```

**Tools (in priority order)**:
1. `reader` (Mozilla Readability) - best for most articles
2. `trafilatura` - excellent for blogs/news (included in dependencies)
3. Fallback (`tapestry-extract-html`) - works without external tools

## Security Requirements

All security utilities are available via UV from the project root.

### URL Validation

```bash
# Run security validation (checks protocol, blocks SSRF, etc.)
uv run tapestry-validate-url "$URL" || exit 1
```

### Filename Sanitization

```bash
# Use tapestry sanitization utility
SAFE_TITLE=$(uv run tapestry-sanitize-filename "$TITLE")
```

## Step 1: Check Available Tools

```bash
if command -v reader &> /dev/null; then
    TOOL="reader"
else
    # trafilatura is included in project dependencies
    TOOL="trafilatura"
fi

echo "Using: $TOOL"
```

### Optional: Install reader (npm)

For best results, install reader separately:

```bash
npm install -g @aspect/readability-cli
# or
npm install -g reader-cli
```

## Step 2: Extract Content

### Using reader

```bash
TEMP_FILE=$(mktemp)
trap "rm -f '$TEMP_FILE'" EXIT

reader "$URL" > "$TEMP_FILE"

# Get title (first line in markdown format)
TITLE=$(head -n 1 "$TEMP_FILE" | sed 's/^# //')
```

### Using trafilatura (via UV)

```bash
TEMP_FILE=$(mktemp)
trap "rm -f '$TEMP_FILE'" EXIT

# Get content
uv run trafilatura --URL "$URL" --output-format txt --no-comments > "$TEMP_FILE"

# Get title from metadata
TITLE=$(uv run trafilatura --URL "$URL" --json 2>/dev/null | \
    python3 -c "import json,sys; print(json.load(sys.stdin).get('title','Article'))" 2>/dev/null || echo "Article")
```

### Fallback Method (tapestry-extract-html)

Use the built-in HTML extractor when other tools aren't available:

```bash
# Extract content using tapestry's HTML extractor
uv run tapestry-extract-html "$URL" --output article.txt
```

Or get title and content separately:

```bash
TEMP_FILE=$(mktemp)
trap "rm -f '$TEMP_FILE'" EXIT

# Fetch and extract
uv run tapestry-extract-html "$URL" --output "$TEMP_FILE"

# Title is on first line (after "# ")
TITLE=$(head -n 1 "$TEMP_FILE" | sed 's/^# //')
```

## Step 3: Save with Clean Filename

```bash
SAFE_TITLE=$(uv run tapestry-sanitize-filename "$TITLE")
CONTENT_FILE="${SAFE_TITLE}.txt"

# Verify content was extracted
if [ ! -s "$TEMP_FILE" ]; then
    echo "Error: No content extracted"
    exit 1
fi

mv "$TEMP_FILE" "$CONTENT_FILE"
trap - EXIT

WORD_COUNT=$(wc -w < "$CONTENT_FILE" | tr -d ' ')

echo "Extracted: $TITLE"
echo "Saved to: $CONTENT_FILE"
echo "Words: $WORD_COUNT"
```

## Complete Workflow Script

```bash
#!/bin/bash
set -e

URL="$1"

# Validate URL
uv run tapestry-validate-url "$URL" || exit 1

# Detect tool
if command -v reader &> /dev/null; then
    TOOL="reader"
else
    TOOL="trafilatura"
fi

echo "Extracting with: $TOOL"

# Create temp file
TEMP_FILE=$(mktemp)
trap "rm -f '$TEMP_FILE'" EXIT

# Extract based on tool
case $TOOL in
    reader)
        reader "$URL" > "$TEMP_FILE"
        TITLE=$(head -n 1 "$TEMP_FILE" | sed 's/^# //')
        ;;
    trafilatura)
        uv run trafilatura --URL "$URL" --output-format txt --no-comments > "$TEMP_FILE"
        TITLE=$(uv run trafilatura --URL "$URL" --json 2>/dev/null | \
            python3 -c "import json,sys; print(json.load(sys.stdin).get('title','Article'))" 2>/dev/null || echo "Article")
        ;;
esac

# If extraction failed, try fallback
if [ ! -s "$TEMP_FILE" ]; then
    echo "Primary extraction failed, trying fallback..."
    uv run tapestry-extract-html "$URL" --output "$TEMP_FILE"
    TITLE=$(head -n 1 "$TEMP_FILE" | sed 's/^# //')
fi

# Verify extraction
if [ ! -s "$TEMP_FILE" ]; then
    echo "Error: No content extracted. Site may require authentication."
    exit 1
fi

# Save with clean filename
SAFE_TITLE=$(uv run tapestry-sanitize-filename "$TITLE")
CONTENT_FILE="${SAFE_TITLE}.txt"
mv "$TEMP_FILE" "$CONTENT_FILE"
trap - EXIT

# Show results
WORD_COUNT=$(wc -w < "$CONTENT_FILE" | tr -d ' ')
echo ""
echo "Extracted: $TITLE"
echo "Saved to: $CONTENT_FILE"
echo "Words: $WORD_COUNT"
echo ""
echo "Preview:"
head -n 10 "$CONTENT_FILE"
```

## Error Handling

| Issue | Solution |
|-------|----------|
| UV not installed | Install with `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Invalid URL | Reject with clear message |
| Internal URL (SSRF) | Block localhost/private IPs |
| Paywall/login required | Inform user, cannot extract |
| Empty extraction | Try fallback method, inform user |
| Timeout | Fallback uses 30s timeout |

## What Gets Extracted

**Included**:
- Article title
- Author (if available)
- Main text content
- Section headings

**Removed**:
- Navigation menus
- Ads and promotions
- Newsletter signups
- Related articles
- Comment sections
- Social buttons
- Cookie notices

## Tool Comparison

| Tool | Strengths | Availability |
|------|-----------|--------------|
| reader | Best overall, Firefox algorithm | npm install separately |
| trafilatura | News/blogs, multi-language | Included in dependencies |
| tapestry-extract-html | No external dependencies | Built-in fallback |

## Dependencies

All dependencies are managed via UV and `pyproject.toml`:

- **trafilatura**: Article extraction (pinned version)
- **tapestry-extract-html**: Built-in fallback extractor

Optional (install separately):
- **reader**: Mozilla Readability CLI (`npm install -g reader-cli`)

## Security Reference

For complete security guidelines: `../shared/references/security-guidelines.md`
