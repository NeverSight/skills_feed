---
name: mistral-ocr
description: Extract text from images and PDFs using Mistral OCR API. Convert scanned documents to Markdown, JSON, or plain text. No external dependencies required. Use when you need OCR, extract text from images, convert PDFs to markdown, or digitize documents.
user-invocable: true
allowed-tools: Bash(curl:*), Read, Write
metadata:
  version: "2.0.9"
---

# Mistral OCR

Extract text from images and PDFs using Mistral's dedicated OCR API. No external dependencies required.

## Requirements

This skill requires a Mistral API key. If you don't have one, follow the guide in [reference/getting-started.md](reference/getting-started.md).

## API Key

The user must provide their Mistral API key. **Ask for it if not available.**

**Option 1 (Recommended for AI agents):** User provides key directly in message:
```
"Use this Mistral key: aBc123XyZ..."
"Convert this PDF to markdown, my API key is aBc123XyZ..."
```

**Option 2:** Environment variable `$MISTRAL_API_KEY`

**Option 3:** Claude Code settings (`~/.claude/settings.json`)

If no key is available, guide the user to get one at [console.mistral.ai](https://console.mistral.ai/).

---

## API Endpoint

Use the dedicated OCR endpoint for all document processing:

```
POST https://api.mistral.ai/v1/ocr
```

**Model:** `mistral-ocr-latest`

---

## Features

### 1. PDF → Markdown (Direct, no conversion needed!)

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "document_url",
      "document_url": "https://example.com/document.pdf"
    }
  }'
```

### 2. Image → Text

Works with JPG, PNG, WEBP, GIF:

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "image_url",
      "image_url": "https://example.com/image.jpg"
    }
  }'
```

### 3. Local Files (Base64 Data URL)

For local PDFs or images, encode as base64 and use a data URL.

**ALWAYS use curl** (works on all platforms including Windows via Git Bash):

```bash
# For local PDF
BASE64=$(base64 -w0 document.pdf)
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "document_url",
      "document_url": "data:application/pdf;base64,'"$BASE64"'"
    }
  }'

# For local images (PNG, JPG, etc.)
BASE64=$(base64 -w0 image.png)
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "image_url",
      "image_url": "data:image/png;base64,'"$BASE64"'"
    }
  }'
```

**MIME types:**
- PDF: `data:application/pdf;base64,...`
- PNG: `data:image/png;base64,...`
- JPG: `data:image/jpeg;base64,...`
- WEBP: `data:image/webp;base64,...`

### 4. Structured JSON Output

For invoices, forms, tables - ask for JSON in a follow-up or use Document AI annotations.

---

## Response Format

The API returns markdown directly:

```json
{
  "pages": [
    {
      "index": 0,
      "markdown": "# Document Title\n\nExtracted content here...",
      "images": [],
      "tables": [],
      "dimensions": {"dpi": 200, "height": 842, "width": 595}
    }
  ],
  "model": "mistral-ocr-latest",
  "usage_info": {"pages_processed": 1, "doc_size_bytes": 12345}
}
```

---

## Workflow

### User requests OCR from image or PDF

1. **Get API key** - Ask user if not in environment
2. Determine input type (URL or local file)
3. **For local files, ALWAYS use temp file approach** (avoids "Argument list too long" error):

```bash
# Cross-platform temp directory
TMPDIR="${TMPDIR:-${TEMP:-/tmp}}"

# Step 1: Encode file to base64
base64 -w0 "document.pdf" > "$TMPDIR/b64.txt"

# Step 2: Create JSON request file
echo '{"model":"mistral-ocr-latest","document":{"type":"document_url","document_url":"data:application/pdf;base64,'$(cat "$TMPDIR/b64.txt")'"}}' > "$TMPDIR/request.json"

# Step 3: Call API with -d @file (use actual key, not variable)
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer YOUR_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d @"$TMPDIR/request.json" > "$TMPDIR/response.json"

# Step 4: Extract markdown with node (NOT jq - not available on all systems)
node -e "const fs=require('fs'); const r=JSON.parse(fs.readFileSync('$TMPDIR/response.json')); console.log(r.pages.map(p=>p.markdown).join('\n\n---\n\n'))"
```

4. **Save to .md file** using Write tool
5. Confirm file location to user

### IMPORTANT: Cross-Platform Compatibility

- **ALWAYS use curl** (works on Windows via Git Bash)
- **ALWAYS use `-d @file`** for request body (handles large files)
- **NEVER use jq** - use node instead to parse JSON
- **Use `${TMPDIR:-${TEMP:-/tmp}}`** for temp files (works on all systems)
- **Copy response.json to user directory** before parsing with node on Windows

---

## Usage Examples

When the user says:

| User Request | Action |
|--------------|--------|
| "Convert this PDF to markdown" | OCR the PDF, save as .md file |
| "Extract text from this image" | OCR the image, return text |
| "Give me a .md of this document" | OCR and save as .md file |
| "What does this PDF say?" | OCR and summarize content |
| "OCR this receipt" | Extract text, optionally structure as JSON |

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify key, guide to getting-started.md |
| 400 Bad Request | Invalid document | Check format and URL accessibility |
| 3310 File fetch error | URL not accessible | Use base64 for local files |
| Rate limit | Too many requests | Wait and retry |

---

## Supported Formats

| Format | Support |
|--------|---------|
| PDF | ✅ Direct (no conversion) |
| PNG | ✅ Direct |
| JPG/JPEG | ✅ Direct |
| WEBP | ✅ Direct |
| GIF | ✅ Direct |

**No external dependencies required!** Unlike other OCR solutions, Mistral OCR handles PDFs directly without needing pdftoppm, ImageMagick, or any other tools.

---

## Pricing

As of 2025, Mistral OCR pricing:
- **$2 per 1,000 pages**
- **50% discount** with Batch API

Check current rates at [mistral.ai/pricing](https://mistral.ai/pricing/)

---

## References

- [Getting Started](reference/getting-started.md) - How to get your API key
- [PDF to Markdown](reference/pdf-to-markdown.md) - PDF conversion examples
- [Output Formats](reference/formats.md) - JSON, Markdown, plain text
- [Step-by-Step Guide](reference/guide.md) - Complete tutorial with examples

---

*Skill by [Parlamento AI](https://parlamento.ai)*
