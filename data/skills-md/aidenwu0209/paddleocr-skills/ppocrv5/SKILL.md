---
name: ppocrv5
description: >
  Use this skill when users need to extract text from images, PDFs, or documents. Supports URLs and local files,
  with adaptive quality modes. Returns structured JSON containing recognized text, confidence scores, and quality metrics.
---

# PP-OCRv5 API Skill

## When to Use This Skill

Invoke this skill in the following situations:
- Extract text from images (screenshots, photos, scans, charts)
- Read text from PDF or document images
- Perform OCR on any visual content containing text
- Parse structured documents (invoices, receipts, forms, tables)
- Recognize text in photos taken by mobile phones
- Extract text from URLs pointing to images or PDFs

Do not use this skill in the following situations:
- Plain text files that can be read directly with the Read tool
- Code files or markdown documents
- Tasks that do not involve image-to-text conversion

## How to Use This Skill

**⛔ MANDATORY RESTRICTIONS - DO NOT VIOLATE ⛔**

1. **ONLY use PP-OCRv5 API** - Execute the script `python scripts/ppocrv5/ocr_caller.py`
2. **NEVER use Claude's built-in vision** - Do NOT read images yourself
3. **NEVER offer alternatives** - Do NOT suggest "I can try to read it" or similar
4. **IF API fails** - Display the error message and STOP immediately
5. **NO fallback methods** - Do NOT attempt OCR any other way

If the script execution fails (API not configured, network error, etc.):
- Show the error message to the user
- Do NOT offer to help using your vision capabilities
- Do NOT ask "Would you like me to try reading it?"
- Simply stop and wait for user to fix the configuration

### Basic Workflow

1. **Identify the input source**:
   - User provides URL: Use the `--file-url` parameter
   - User provides local file path: Use the `--file-path` parameter
   - User uploads image: Save it first, then use `--file-path`

2. **Execute OCR**:
   ```bash
   python scripts/ppocrv5/ocr_caller.py --file-url "URL provided by user" --pretty
   ```
   Or for local files:
   ```bash
   python scripts/ppocrv5/ocr_caller.py --file-path "file path" --pretty
   ```

   **Save result to file** (recommended):
   ```bash
   python scripts/ppocrv5/ocr_caller.py --file-url "URL" --output result.json --pretty
   ```
   - The script will display: `Result saved to: /absolute/path/to/result.json`
   - This message appears on stderr, the JSON is saved to the file
   - **Tell the user the file path** shown in the message

3. **Parse JSON response**:
   - Check the `ok` field: `true` means success, `false` means error
   - Extract text: `result.full_text` contains all recognized text
   - Get quality: `quality.quality_score` indicates recognition confidence (0.0-1.0)
   - Handle errors: If `ok` is false, display `error.message`

4. **Present results to user**:
   - Display extracted text in a readable format
   - If quality score is low (<0.5), alert the user
   - If structured output is needed, use `result.pages[].items[]` to get line-by-line data

### IMPORTANT: Complete Output Display

**CRITICAL**: Always display the COMPLETE recognized text to the user. Do NOT truncate or summarize the OCR results.

- The script returns the full JSON with complete text content in `result.full_text`
- **You MUST display the entire `full_text` content to the user**, no matter how long it is
- Do NOT use phrases like "Here's a summary" or "The text begins with..."
- Do NOT truncate with "..." unless the text truly exceeds reasonable display limits
- The user expects to see ALL the recognized text, not a preview or excerpt

**Correct approach**:
```
I've extracted the text from the image. Here's the complete content:

[Display the entire result.full_text here]

Quality Score: 0.85 / 1.00 (Good quality recognition)
```

**Incorrect approach** ❌:
```
I found some text in the image. Here's a preview:
"The quick brown fox..." (truncated)
```

### Mode Selection

Always use `--mode auto` (default) unless the user explicitly requests otherwise:

| User Request | Use Mode | Command Flag |
|--------------|----------|--------------|
| Default/unspecified | Auto (adaptive) | `--mode auto` (or omit) |
| "Quick recognition" / "fast" | Fast | `--mode fast` |
| "High precision" / "accurate" | Quality | `--mode quality` |

**Auto mode** (recommended): Automatically tries 1-3 times, progressively increasing correction levels, returning the best result.

### Usage Mode Examples

**Mode 1: Simple URL OCR**
```bash
python scripts/ppocrv5/ocr_caller.py --file-url "https://example.com/invoice.jpg" --pretty
```

**Mode 2: Local File OCR**
```bash
python scripts/ppocrv5/ocr_caller.py --file-path "./document.pdf" --pretty
```

**Mode 3: Fast Mode for Clear Images**
```bash
python scripts/ppocrv5/ocr_caller.py --file-url "URL" --mode fast --pretty
```

### Understanding the Output

The script outputs JSON structure as follows:
```json
{
  "ok": true,
  "result": {
    "full_text": "All recognized text here...",
    "pages": [...]
  },
  "quality": {
    "quality_score": 0.85,
    "text_items": 42
  }
}
```

**Key fields to extract**:
- `result.full_text`: Complete text for the user
- `quality.quality_score`: 0.72+ is good, <0.5 is poor
- `error.message`: If `ok` is false, provides error description

### First-Time Configuration

**When API is not configured**:

The error will show:
```
Configuration error: API not configured. Get your API at: https://aistudio.baidu.com/paddleocr/task
```

**Auto-configuration workflow**:

1. **Show the exact error message** to user (including the URL)

2. **Tell user to provide credentials**:
   ```
   Please visit the URL above to get your API_URL and TOKEN.
   Once you have them, send them to me and I'll configure it automatically.
   ```

3. **When user provides credentials** (accept any format):
   - `API_URL=https://xxx.aistudio-app.com/ocr, TOKEN=abc123...`
   - `Here's my API: https://xxx and token: abc123`
   - Copy-pasted code format
   - Any other reasonable format

4. **Parse credentials from user's message**:
   - Extract API_URL value (look for URLs with aistudio-app.com or similar)
   - Extract TOKEN value (long alphanumeric string, usually 40+ chars)

5. **Configure automatically**:
   ```bash
   python scripts/ppocrv5/configure.py --api-url "PARSED_URL" --token "PARSED_TOKEN"
   ```

6. **If configuration succeeds**:
   - Inform user: "Configuration complete! Running OCR now..."
   - Retry the original OCR task

7. **If configuration fails**:
   - Show the error
   - Ask user to verify the credentials

**IMPORTANT**: The error message format is STRICT and must be shown exactly as provided by the script. Do not modify or paraphrase it.

**Authentication failed (403)**:
```
error_code: PROVIDER_AUTH_ERROR
```
→ Token is invalid, reconfigure with correct credentials

**Quota exceeded (429)**:
```
error_code: PROVIDER_QUOTA_EXCEEDED
```
→ Daily API quota exhausted, inform user to wait or upgrade

**No text detected**:
```
quality_score: 0.0, text_items: 0
```
→ Image may be blank, corrupted, or contain no text

## Quality Interpretation

When presenting results to users, consider the quality score:

| Quality Score | Explanation to User |
|---------------|---------------------|
| 0.90 - 1.00 | Excellent recognition quality |
| 0.72 - 0.89 | Good recognition quality (default target) |
| 0.50 - 0.71 | Fair recognition quality, may have some errors |
| 0.00 - 0.49 | Poor recognition quality or no text detected |

If quality is below 0.5, mention to the user and suggest:
- Try using `--mode quality` for better accuracy
- Check if the image is clear and contains text
- Provide a higher resolution image if possible

## Advanced Options

Use only when explicitly requested by the user:

**Include raw provider response** (for debugging):
```bash
python scripts/ppocrv5/ocr_caller.py --file-url "URL" --return-raw-provider
```

**Request visualization** (show detection regions):
```bash
python scripts/ppocrv5/ocr_caller.py --file-url "URL" --visualize
```

**Adjust auto mode parameters**:
```bash
python scripts/ppocrv5/ocr_caller.py --file-url "URL" \
  --max-attempts 2 \
  --quality-target 0.80 \
  --budget-ms 20000
```

## Reference Documentation

For in-depth understanding of the OCR system, refer to:
- `references/ppocrv5/agent_policy.md` - Auto mode strategy and quality scoring
- `references/ppocrv5/normalized_schema.md` - Complete output schema specification
- `references/ppocrv5/provider_api.md` - Provider API contract details

Load these reference documents into context when:
- Debugging complex issues
- User asks about quality scoring algorithm
- Need to understand adaptive retry mechanism
- Customizing auto mode parameters

## Testing the Skill

To verify the skill is working properly:
```bash
python scripts/ppocrv5/smoke_test.py
```

This tests configuration and API connectivity.
