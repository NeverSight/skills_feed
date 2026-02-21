---
name: web-fetch
description: Use this skill when users want to scrape web content and convert it to clean Markdown or PDF. Handles workflows like "Save this webpage as PDF", "Fetch this article", "抓取网页内容", or "转换为PDF". Supports crawl4ai for general web scraping and Playwright-based WeChat (微信公众号) article fetching with anti-bot bypass. Automatically converts to PDF by default unless user specifies Markdown-only.
---

# Web Fetch

Fetch web content and convert to clean Markdown and PDF formats. Supports general websites and WeChat (微信公众号) articles.

## Features

- Automatic noise removal (navigation, headers, footers, sidebars)
- Image preservation with alt text
- WeChat article special handling (lazy-loaded images, metadata extraction)
- Clean Markdown output ready for translation or processing
- **PDF conversion with clean reading style**
- **CJK font support for Chinese content**
- **Both MD and PDF output by default** 

## Dependencies

```bash
# Core dependencies
pip install crawl4ai requests beautifulsoup4 markdownify

# WeChat article fetching
pip install playwright
playwright install chromium

# PDF conversion with CJK font support
pip install reportlab markdown beautifulsoup4
```

**Note**: `reportlab` provides excellent CJK font support and works on Windows/Mac/Linux without system dependencies.

## Usage

### General Web Pages

For most websites, use the crawl4ai-based fetcher:

```bash
python scripts/fetch_web_content.py <url> <output_filename>
```

Example:
```bash
python scripts/fetch_web_content.py https://example.com/article article.md
```

### WeChat Articles (微信公众号)

For WeChat articles, use the Playwright-based fetcher with anti-bot bypass:

```bash
python scripts/fetch_weixin.py <url> [output_filename]
```

Examples:
```bash
# Auto-generate filename (YYYYMMDD+Title format)
python scripts/fetch_weixin.py "https://mp.weixin.qq.com/s/xxxxx"

# Custom filename
python scripts/fetch_weixin.py "https://mp.weixin.qq.com/s/xxxxx" article.md
```

**Features:**
- Uses real Chromium browser to bypass anti-bot protections
- Handles lazy-loaded images automatically
- Auto-generates filename from publish date + title (YYYYMMDD格式)
- Supports both visible browser (for debugging) and headless mode

### Convert Markdown to PDF

After fetching content to Markdown, convert to PDF:

```bash
python scripts/md_to_pdf.py <markdown_file> [--output output.pdf]
```

Examples:
```bash
# Convert single file to PDF (auto-generates output name)
python scripts/md_to_pdf.py article.md

# Convert with custom output name
python scripts/md_to_pdf.py article.md --output custom_name.pdf

# Batch convert entire directory
python scripts/md_to_pdf.py ./articles_folder --concurrency 4
```

**Features:**
- Excellent Chinese (CJK) font support using Microsoft YaHei
- Image rendering support (HTTP/HTTPS URLs and local paths)
- Automatic image scaling with aspect ratio preservation
- Both single file and batch directory conversion
- Clean, readable typography optimized for Chinese content

## Response Pattern (Updated)

When user requests web content fetching:

1. **Identify URL type:**
   - WeChat URL (`mp.weixin.qq.com`) → use `fetch_weixin.py`
   - Other URLs → use `fetch_web_content.py`

2. **Determine output format:**
   - User mentions "PDF" explicitly → MD + PDF
   - User says "only MD"/"no PDF"/"markdown only" → MD only
   - **Ambiguous request** → Ask: "Would you like PDF format as well?"

   **Detection examples:**
   - "Fetch as PDF" / "转换为PDF" → MD + PDF
   - "Save to PDF" → MD + PDF
   - "Get markdown only" / "只要markdown" → MD only
   - "Fetch this article" → **Ask user**
   - "抓取网页内容" → **Ask user**

3. **Execute fetching:**
   ```bash
   python scripts/fetch_web_content.py <url> <output>.md
   # or
   python scripts/fetch_weixin.py <url> [output].md
   ```

   **Note:** For WeChat articles, output filename is optional - it auto-generates as YYYYMMDD+Title

4. **Convert to PDF (if requested):**
   ```bash
   python scripts/md_to_pdf.py <output>.md
   ```
   This creates `<output>.pdf` alongside `<output>.md`

5. **Report results:**
   - Confirm both files saved (if PDF)
   - Show statistics for both formats
   - Suggest next steps

## Example Workflows

### Workflow 1: Fetch with PDF (Explicit Request)

```bash
# User: "Fetch this article as PDF: https://example.com/article"

# Step 1: Fetch markdown
python scripts/fetch_web_content.py https://example.com/article article.md

# Step 2: Convert to PDF
python scripts/md_to_pdf.py article.md

# Result:
# ✓ Saved: article.md (45 KB, 8,234 words)
# ✓ PDF: article.pdf (with images embedded)
```

### Workflow 2: Fetch Markdown Only

```bash
# User: "Get the markdown only"

# Step 1: Fetch markdown
python scripts/fetch_web_content.py https://example.com/article article.md

# Step 2: Skip PDF conversion

# Result:
# ✓ Saved: article.md (45 KB, 8,234 words)
```

### Workflow 3: Ambiguous Request

```bash
# User: "Fetch this article: https://example.com/article"

# Claude asks: "I'll fetch this article. Would you like me to convert it to PDF as well?"
# User: "Yes"

# Then proceed with Workflow 1
```

### Workflow 4: WeChat Article with PDF

```bash
# User: "抓取微信文章为PDF"

# Step 1: Fetch markdown (auto-generates filename as YYYYMMDD+Title)
python scripts/fetch_weixin.py "https://mp.weixin.qq.com/s/xxxxx"

# Step 2: Convert to PDF (use the auto-generated filename)
python scripts/md_to_pdf.py 20251214关于财政政策和货币政策的关系.md

# Result:
# ✓ Saved: 20251214关于财政政策和货币政策的关系.md (中文内容)
# ✓ PDF: 20251214关于财政政策和货币政策的关系.pdf (完美支持中文和图片)
```

### Batch Processing

For multiple URLs, loop through and fetch each:
```bash
for url in url1 url2 url3; do
  filename="output_$(date +%s)"
  python scripts/fetch_web_content.py "$url" "$filename.md"
  python scripts/md_to_pdf.py "$filename.md"  # Optional: add PDF
done
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty content | Try different CSS selector or use WeChat Playwright fetcher |
| Missing images | Check if site blocks external requests |
| Encoding issues | Content is saved as UTF-8 by default |
| WeChat blocked | Use Playwright fetcher - it launches real browser to bypass anti-bot |
| **WeChat timeout** | Script has 60s timeout with retry - usually succeeds on second attempt |
| **Playwright not installed** | Run: `pip install playwright && playwright install chromium` |
| **PDF conversion failed** | Install dependencies: `pip install reportlab markdown beautifulsoup4` |
| **Chinese characters in PDF** | Microsoft YaHei font is automatically used (excellent CJK support) |
| **Images missing in PDF** | Check that image URLs are accessible or local image paths are correct |
| **PDF too large** | Images are embedded and scaled; original image size affects PDF size |
