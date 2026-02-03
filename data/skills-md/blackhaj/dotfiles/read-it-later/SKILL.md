---
name: read-it-later
description: Sends markdown (rendered to HTML) or URLs to Readwise Reader for later reading. Use when an agent needs to save summaries, notes, or links to Readwise Reader.
---

# Read It Later (Readwise Reader)

Send markdown or URLs to Readwise Reader using Bun scripts.

## Setup

1. Ensure Bun v1.3.8+ is installed.
2. Set the Readwise token in your shell profile:
   ```bash
   export READWISE_ACCESS_TOKEN="your-token"
   ```

## Send Markdown

Convert markdown to HTML with Bun's markdown parser and send it to Readwise Reader.

```bash
{baseDir}/scripts/send-markdown.ts "# Project Summary\n\nThis is a summary." --title "Project Summary"
```

To avoid shell escaping, stream markdown via stdin:

```bash
cat summary.md | {baseDir}/scripts/send-markdown.ts --stdin --title "Project Summary"
```

## Send a URL

Use the Readwise wrapper directly to send a URL:

```bash
{baseDir}/scripts/readwise.ts url https://example.com/article --title "Example Article"
```

## Send Raw HTML

```bash
cat article.html | {baseDir}/scripts/readwise.ts html --stdin --title "Article"
```

## Notes

- Both scripts accept `--source <source>` to set the Readwise `source` field.
- Use `--url <url>` to supply a canonical URL for HTML/markdown saves (otherwise a placeholder URL is generated).
- Errors are printed with response details if the Readwise API rejects the request.
