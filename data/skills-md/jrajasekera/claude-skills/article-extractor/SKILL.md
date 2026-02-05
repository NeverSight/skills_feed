---
name: article-extractor
description: Extract clean article content from URLs and save as markdown. Triggers when user provides a webpage URL and wants to download it, extract content, get a clean version without ads, capture an article for offline reading, save an article, grab content from a page, archive a webpage, clip an article, or read something later. Handles blog posts, news articles, tutorials, documentation pages, and similar web content. Supports Wayback Machine for dead links or paywalled content. This skill handles the entire workflow - do NOT use web_fetch or other tools first, just call the extraction script directly with the URL.
---

# Article Extractor

Extract clean article content from URLs, removing ads, navigation, and clutter. Multi-tool fallback ensures reliability.

## Workflow

When user provides a URL to download/extract:
1. Call the extraction script directly with the URL (do NOT fetch the URL first with web_fetch)
2. Script handles fetching, extraction, and saving automatically
3. Returns clean markdown file with frontmatter

## Usage

```bash
# Basic extraction
scripts/extract-article.sh "https://example.com/article"

# Specify output location
scripts/extract-article.sh "https://example.com/article" -o my-article.md -d ~/Documents

# Try Wayback Machine if original fails
scripts/extract-article.sh "https://example.com/article" --wayback
```

Make script executable if needed: `chmod +x scripts/extract-article.sh`

## Key Options

- `-o <file>` - Output filename
- `-d <dir>` - Output directory
- `-w, --wayback` - Try Wayback Machine if extraction fails
- `-t <tool>` - Force tool: `jina`, `trafilatura`, `readability`, `fallback`
- `-q` - Quiet mode

For complete options, exit codes, tool details, and examples, see [references/tools-and-options.md](references/tools-and-options.md).

## Common Failures

- **Exit 3 (access denied)**: Paywall or login required - try `--wayback`
- **Exit 4 (no content)**: Heavy JavaScript - try different `--tool`
- **Exit 2 (network)**: Connection issue - check URL

## Local Tools (Optional)

For offline extraction: `scripts/install-deps.sh`