---
name: tapestry
description: This skill should be used when the user says "tapestry <URL>", "weave <URL>", "help me plan <URL>", "extract and plan <URL>", "make this actionable <URL>", or wants to extract content from a URL and create an action plan. Automatically detects content type (YouTube video, article, PDF) and orchestrates the full extract-to-plan workflow.
allowed-tools: Bash,Read,Write
---

# Tapestry: Unified Content Extraction + Action Planning

Master skill that orchestrates the entire Tapestry workflow:
1. Detect content type from URL
2. Extract content using appropriate method
3. Create a Ship-Learn-Next action plan automatically

## Prerequisites

This skill requires [UV](https://docs.astral.sh/uv/) for dependency management. Run from the tapestry-skills project root.

## Workflow Overview

```
URL → Validate → Detect Type → Extract Content → Create Plan → Save Files
```

**Output**: Two files saved:
- Content file: `[Title].txt`
- Plan file: `Ship-Learn-Next Plan - [Quest].md`

## Security Requirements

**CRITICAL**: Before processing ANY URL, validate it first using the tapestry security utilities.

All security utilities are available via UV from the project root.

### URL Validation (Required)

```bash
URL="$1"

# Run security validation (checks protocol, blocks SSRF, etc.)
uv run tapestry-validate-url "$URL" || exit 1
```

### Filename Sanitization (Required)

```bash
# Use tapestry sanitization utility for all titles
SAFE_TITLE=$(uv run tapestry-sanitize-filename "$TITLE")
```

## Step 1: Detect Content Type

```bash
detect_content_type() {
    local URL="$1"

    # YouTube patterns
    if [[ "$URL" =~ youtube\.com/watch || "$URL" =~ youtu\.be/ || "$URL" =~ youtube\.com/shorts ]]; then
        echo "youtube"
        return
    fi

    # PDF by extension
    if [[ "$URL" =~ \.pdf($|\?) ]]; then
        echo "pdf"
        return
    fi

    # PDF by Content-Type header
    if curl -sI --max-time 10 "$URL" | grep -iq "Content-Type:.*application/pdf"; then
        echo "pdf"
        return
    fi

    # Default to article
    echo "article"
}

CONTENT_TYPE=$(detect_content_type "$URL")
echo "Detected: $CONTENT_TYPE"
```

## Step 2: Extract Content

### YouTube Extraction

Use the youtube-transcript skill workflow:

```bash
# yt-dlp is available through UV
VIDEO_TITLE=$(uv run yt-dlp --print "%(title)s" "$URL" 2>/dev/null)
SAFE_TITLE=$(uv run tapestry-sanitize-filename "$VIDEO_TITLE")

# Create temp file
TEMP_DIR=$(mktemp -d)
trap "rm -rf '$TEMP_DIR'" EXIT

# Download transcript (try manual first, then auto-generated)
if ! uv run yt-dlp --write-sub --skip-download --sub-langs en -o "$TEMP_DIR/transcript" "$URL" 2>/dev/null; then
    uv run yt-dlp --write-auto-sub --skip-download --sub-langs en -o "$TEMP_DIR/transcript" "$URL"
fi

# Find and convert VTT to clean text
VTT_FILE=$(find "$TEMP_DIR" -name "*.vtt" | head -n 1)
uv run tapestry-vtt-to-text "$VTT_FILE" --output "${SAFE_TITLE}.txt"

CONTENT_FILE="${SAFE_TITLE}.txt"
```

### Article Extraction

Use the article-extractor skill workflow:

```bash
# Check for extraction tools
if command -v reader &> /dev/null; then
    TOOL="reader"
else
    TOOL="trafilatura"
fi

TEMP_FILE=$(mktemp)
trap "rm -f '$TEMP_FILE'" EXIT

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

# Fallback if extraction failed
if [ ! -s "$TEMP_FILE" ]; then
    uv run tapestry-extract-html "$URL" --output "$TEMP_FILE"
    TITLE=$(head -n 1 "$TEMP_FILE" | sed 's/^# //')
fi

SAFE_TITLE=$(uv run tapestry-sanitize-filename "$TITLE")
CONTENT_FILE="${SAFE_TITLE}.txt"
mv "$TEMP_FILE" "$CONTENT_FILE"
trap - EXIT
```

### PDF Extraction

```bash
# Sanitize filename from URL
URL_BASENAME=$(basename "$URL" | cut -d'?' -f1)
SAFE_PDF=$(uv run tapestry-sanitize-filename "$URL_BASENAME")

# Ensure .pdf extension
[[ "$SAFE_PDF" != *.pdf ]] && SAFE_PDF="${SAFE_PDF}.pdf"

# Download with security checks
uv run tapestry-safe-download "$URL" "$SAFE_PDF" --max-size 104857600

# Verify it's actually a PDF
if ! head -c 4 "$SAFE_PDF" | grep -q '%PDF'; then
    echo "Error: Downloaded file is not a valid PDF"
    rm -f "$SAFE_PDF"
    exit 1
fi

# Extract text if pdftotext available
if command -v pdftotext &> /dev/null; then
    CONTENT_FILE="${SAFE_PDF%.pdf}.txt"
    pdftotext "$SAFE_PDF" "$CONTENT_FILE"
    echo "Extracted text to: $CONTENT_FILE"
else
    echo "Note: pdftotext not found. Install with: brew install poppler"
    CONTENT_FILE="$SAFE_PDF"
fi
```

## Step 3: Create Action Plan

After extracting content, invoke the ship-learn-next skill logic:

1. Read the extracted content file
2. Extract 3-5 core actionable lessons
3. Define a specific 4-8 week quest
4. Design Rep 1 (shippable this week)
5. Outline Reps 2-5 (progressive iterations)
6. Save as: `Ship-Learn-Next Plan - [Quest Title].md`

**Key points**:
- Focus on actionable lessons, not summaries
- Rep 1 must be completable in 1-7 days
- Each rep produces real artifacts
- Emphasize doing over studying

## Step 4: Present Results

```
Tapestry Workflow Complete!

Content Extracted:
  Type: [youtube/article/pdf]
  Title: [Title]
  Saved to: [filename.txt]
  Words: [X]

Action Plan Created:
  Quest: [Quest title]
  Saved to: Ship-Learn-Next Plan - [Title].md

Rep 1 (This Week): [Rep 1 goal]

When will you ship Rep 1?
```

## Error Handling

| Issue | Action |
|-------|--------|
| UV not installed | Install with `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Invalid URL | Reject with clear message |
| No subtitles (YouTube) | Offer Whisper transcription (with consent) |
| Paywall/login required | Inform user, cannot extract |
| Download failed | Check URL, retry, inform user |
| Empty extraction | Verify before planning, don't create empty plan |

## Dependencies

All dependencies are managed via UV and `pyproject.toml`:

- **yt-dlp**: YouTube downloads (pinned version)
- **trafilatura**: Article extraction (pinned version)
- **openai-whisper** (optional): For videos without subtitles

**System tools** (install separately if needed):
- **pdftotext**: PDF text extraction (`brew install poppler`)
- **reader**: Mozilla Readability (`npm install -g reader-cli`)

## Security Reference

For detailed security guidelines, see: `../shared/references/security-guidelines.md`

Key requirements:
- Validate all URLs before processing
- Sanitize all filenames
- Use temp files with cleanup traps
- Set download size limits
- Quote all variables in shell commands
