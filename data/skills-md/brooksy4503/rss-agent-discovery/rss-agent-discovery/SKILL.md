---
name: rss-agent-discovery
description: 'AI agent-focused RSS feed discovery tool with JSON output. Use when Claude needs to discover RSS/Atom feeds from websites for monitoring, aggregation, or content syndication purposes. Triggered by: "find RSS feed", "discover RSS", "find Atom feed", "get RSS URLs", "find feeds from [URL]", or when working with content aggregation, feed readers, or RSS monitoring workflows.'
license: MIT
---

# RSS Agent Discovery

AI agent-focused RSS feed discovery tool with machine-parseable JSON output.

## Quick start

```bash
npx -y rss-agent-discovery https://vercel.com
```

Output:
```json
{
  "success": true,
  "results": [{
    "url": "https://vercel.com/",
    "feeds": [{
      "url": "https://vercel.com/atom",
      "title": "atom",
      "type": "atom"
    }],
    "error": null
  }]
}
```

## Core workflow

```bash
npx -y rss-agent-discovery <url> [url2] [url3]...
```

Parse JSON output:
```bash
npx -y rss-agent-discovery https://example.com | jq '.results[0].feeds'
```

## Output schema

```typescript
{
  success: boolean,           // true if no URLs had errors
  partialResults?: boolean,   // true if success=false but some feeds found
  results: [{
    url: string,              // scanned URL
    feeds: [{
      url: string,            // feed URL
      title: string,          // feed title from HTML
      type: 'rss' | 'atom' | 'unknown'
    }],
    error: string | null      // error message if scan failed
  }]
}
```

## Exit codes

- `0` - One or more feeds found (or `--help` / `--version` used)
- `1` - No feeds found
- `2` - Error occurred

Use exit code for automation:
```bash
npx -y rss-agent-discovery https://example.com 2>/dev/null
if [ $? -eq 0 ]; then
  echo "Feeds found!"
fi
```

## Options

```bash
--timeout <ms>          # Timeout per URL (default: 10000)
--skip-blogs           # Skip blog subdirectory scanning
--max-blogs <n>        # Limit blog scans (default: 3)
--blog-paths <paths>   # Custom blog paths (comma or pipe separated)
--verbose              # Debug logging to stderr
--help                 # Show help
--version              # Show version
```

Examples:
```bash
npx -y rss-agent-discovery --timeout 15000 https://example.com
npx -y rss-agent-discovery --skip-blogs https://example.com
npx -y rss-agent-discovery --blog-paths '/blog,/news,/articles' https://example.com
npx -y rss-agent-discovery --blog-paths '/blog|/updates' https://example.com
npx -y rss-agent-discovery --max-blogs 5 https://example.com
```

## Features

- Discovers feeds from HTML `<link>` tags
- Tests common paths (`/rss.xml`, `/atom`, `/feed`, etc.)
- Scans blog subdirectories (`/blog`, `/news`, `/articles`)
- Parallel processing for multiple URLs
- Deduplicates feeds across all sources
- Validates feeds actually return XML
- JSON output to stdout, errors to stderr

## Common patterns

### Single URL discovery
```bash
npx -y rss-agent-discovery https://example.com | jq '.results[0].feeds[].url'
```

### Multiple URLs (parallel)
```bash
npx -y rss-agent-discovery https://site1.com https://site2.com https://site3.com
```

### Extract all feed URLs
```bash
npx -y rss-agent-discovery https://example.com | jq -r '.results[0].feeds[].url'
```

### Check if feeds exist without parsing
```bash
npx -y rss-agent-discovery https://example.com 2>/dev/null
exit_code=$?
[ $exit_code -eq 0 ] && echo "Feeds found"
```

### Custom timeout for slow sites
```bash
npx -y rss-agent-discovery --timeout 20000 https://slow-site.com
```

### Skip blog scanning for faster results
```bash
npx -y rss-agent-discovery --skip-blogs https://example.com
```

## Integration examples

### Shell script
```bash
#!/bin/bash
result=$(npx -y rss-agent-discovery "$1" 2>/dev/null)
if [ $? -eq 0 ]; then
  echo "Found feeds:"
  echo "$result" | jq '.results[0].feeds'
fi
```

### Python
```python
import subprocess
import json

result = subprocess.run(
  ['npx', '-y', 'rss-agent-discovery', url],
  capture_output=True,
  text=True
)

if result.returncode == 0:
  data = json.loads(result.stdout)
  feeds = data['results'][0]['feeds']
```

### JavaScript/Node.js
```javascript
const { execSync } = require('child_process');
const result = JSON.parse(
  execSync('npx -y rss-agent-discovery https://example.com').toString()
);
const feeds = result.results[0].feeds;
```

## Why use this tool

Existing RSS discovery tools (`rss-url-finder`, `rss-finder`) are designed for humans:
- Output human-readable text
- Don't validate feeds exist
- Lack structured machine output

This tool is designed for AI agents:
- JSON-only output (machine-parseable)
- Errors to stderr (separated channel)
- Semantic exit codes
- Validates feeds return XML
- Discovers feeds AI agents miss

## Testing

Test the tool works:
```bash
npx -y rss-agent-discovery https://vercel.com
npx -y rss-agent-discovery https://news.ycombinator.com
```

## More information

- NPM: https://www.npmjs.com/package/rss-agent-discovery
- GitHub: https://github.com/brooksy4503/rss-agent-discovery
