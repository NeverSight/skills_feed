---
name: fetch-url-md
description: Fetch web content with automatic markdown version detection using curl. Use when Claude needs to retrieve documentation from websites that offer both HTML and markdown formats. First checks if a .md version exists (more efficient and cleaner), then falls back to HTML if unavailable. Ideal for fetching documentation from sites like ui.shadcn.com, GitHub wikis, or any documentation site that mirrors content in markdown format.
---

# Fetch URL with Markdown Detection

## Overview

Efficiently fetch web content by prioritizing markdown versions when available. Uses curl to check for .md versions first, then falls back to the original URL.

## Workflow

Follow these steps sequentially:

### 1. Parse the original URL

Extract the base URL and path from the user-provided URL.

**Example:**
- Input: `https://ui.shadcn.com/docs/components/radix/aspect-ratio`
- Markdown URL: `https://ui.shadcn.com/docs/components/radix/aspect-ratio.md`

### 2. Check for .md version

Use curl with HEAD request to check if .md version exists:

```bash
curl -sI "https://ui.shadcn.com/docs/components/radix/aspect-ratio.md" | head -n 1
```

- **200 OK** - Markdown version exists, fetch it
- **404 Not Found** - Markdown version doesn't exist, use original URL
- **3xx redirect** - Follow the redirect or use original URL

### 3. Fetch content

**If .md exists:**
```bash
curl -s "https://ui.shadcn.com/docs/components/radix/aspect-ratio.md"
```

**If .md doesn't exist (fallback):**
```bash
curl -s "https://ui.shadcn.com/docs/components/radix/aspect-ratio"
```

## Decision Tree

```
User provides URL
       │
       ▼
Construct .md URL (append .md)
       │
       ▼
curl -sI <markdown-url> | head -n 1
       │
   ┌───┴───┐
   │       │
200 OK   404/Other
   │       │
   ▼       ▼
Fetch    Fetch original
.md      HTML URL
```

## Quick Reference

| Check Command | Fetch Command |
|---------------|---------------|
| `curl -sI "<url>.md" \| head -n 1` | `curl -s "<url>.md"` |
| `curl -sI "<url>" \| head -n 1` | `curl -s "<url>"` |

## Examples

**Example 1: Markdown version available**
```bash
# Check
curl -sI "https://ui.shadcn.com/docs/components/radix/aspect-ratio.md" | head -n 1
# Output: HTTP/2 200

# Fetch
curl -s "https://ui.shadcn.com/docs/components/radix/aspect-ratio.md"
```

**Example 2: Markdown version not available**
```bash
# Check
curl -sI "https://example.com/docs/guide.md" | head -n 1
# Output: HTTP/2 404

# Fallback - fetch original
curl -s "https://example.com/docs/guide"
```
