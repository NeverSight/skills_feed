---
name: llms-txt-crawler
description: Fetch and crawl llms.txt files from websites. Parses the llms.txt format to extract page URLs and downloads all listed content. Use when you need to gather documentation or content from a website that provides an llms.txt file.
compatibility: Requires Node.js 18+ and network access
metadata:
  author: agy-kit
  version: "1.0"
---

# llms.txt Crawler Skill

This skill enables you to fetch `llms.txt` files from websites and crawl all pages listed within them. The `llms.txt` format is a standard way for websites to provide LLM-friendly content listings.

## Overview

The `llms.txt` file typically follows this format:

```
# Site Name

## Section Name

- [Page Title](https://example.com/page.md): Description of the page
- [Another Page](https://example.com/another.md): Another description
```

This skill parses these files and downloads all linked content.

## Usage

### Basic Usage

Run the crawl script with a target URL:

```bash
cd /path/to/skills/llms-txt-crawler/scripts
npm install  # First time only
node crawl.js --url https://example.com
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--url` | `-u` | Base URL of the site with llms.txt | Required |
| `--output` | `-o` | Output directory for crawled files | `./output` |
| `--format` | `-f` | Output format: `md`, `json`, or `txt` | `md` |
| `--delay` | `-d` | Delay between requests in milliseconds | `500` |
| `--concurrent` | `-c` | Maximum concurrent requests | `3` |

### Examples

**Crawl agentskills.io documentation:**
```bash
node crawl.js --url https://agentskills.io --output ./agentskills-docs
```

**Crawl with custom rate limiting:**
```bash
node crawl.js --url https://example.com --delay 1000 --concurrent 2
```

**Output as JSON:**
```bash
node crawl.js --url https://example.com --format json
```

## Output Structure

The script creates the following output structure:

```
output/
├── llms.txt              # Original llms.txt file
├── index.json            # Metadata about all crawled pages
└── pages/
    ├── page-1.md
    ├── page-2.md
    └── ...
```

## Error Handling

- **Network errors**: Retries up to 3 times with exponential backoff
- **Rate limiting**: Respects delay settings between requests
- **Missing pages**: Logs warnings but continues crawling other pages
- **Invalid URLs**: Skips and logs invalid URLs

## Integration Tips

When using this skill in an agent workflow:

1. First run the crawler to download content
2. The `index.json` file contains metadata about all pages
3. Use the downloaded markdown files for context or analysis

## See Also

- [llms.txt Specification](https://llmstxt.org/)
- [scripts/crawl.js](scripts/crawl.js) - The main crawler script
