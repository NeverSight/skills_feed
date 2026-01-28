---
name: web-scraper
description: Fetch and extract content from web pages, converting HTML to clean markdown. Use when users want to read web articles, extract information from URLs, scrape web content, or when the built-in WebFetch tool fails due to network restrictions. Trigger when user provides URLs to read, asks to fetch web content, or needs to extract text from websites.
---

# Web Scraper

Fetch web page content and convert to clean markdown format.

## Usage

Run the fetch script to get web content:

```bash
python3 scripts/fetch_url.py <url> [options]
```

### Options

- `--timeout <seconds>`: Request timeout (default: 30)
- `--max-length <chars>`: Maximum output length (default: 100000)
- `--raw`: Output raw HTML instead of markdown

### Examples

**Fetch single URL:**
```bash
python3 scripts/fetch_url.py "https://example.com/article"
```

**Fetch with custom timeout:**
```bash
python3 scripts/fetch_url.py "https://example.com/article" --timeout 60
```

**Fetch multiple URLs in parallel:**
```bash
for url in "https://url1.com" "https://url2.com"; do
  python3 scripts/fetch_url.py "$url" &
done
wait
```

## Workflow

1. **Single URL**: Run `fetch_url.py` with the URL
2. **Multiple URLs**: Run multiple fetch commands in parallel using background processes
3. **Handle errors**: If a URL fails, check:
   - Network connectivity
   - URL validity
   - Website may block automated requests (try different User-Agent or use browser automation)

## Output Format

The script converts HTML to clean markdown:
- Headings → `#`, `##`, `###`, etc.
- Lists → `-` for unordered, `1.` for ordered
- Bold/Italic → `**bold**`, `*italic*`
- Code blocks preserved
- Navigation, footer, and ads removed

## Troubleshooting

**403 Forbidden**: Website blocks automated requests. Consider:
- Some sites require JavaScript rendering (not supported by this script)
- Try accessing from a different network

**Timeout errors**: Increase timeout with `--timeout 60`

**Empty content**: Website may require JavaScript to render content
