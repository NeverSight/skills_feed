---
name: langfuse-prompt-view
description: View Langfuse prompts. Use when checking prompt contents, comparing versions, or debugging prompt issues.
license: MIT
compatibility: Node.js 18+ (native fetch required)
metadata:
  author: neuradex
  category: observability
allowed-tools:
  - Bash(npx tsx *scripts/langfuse-prompt-view.ts*)
---

# Langfuse Prompt View

Display the content of a specific prompt.

## Setup

Set the following environment variables before use:

| Variable | Required | Description |
|----------|----------|-------------|
| `LANGFUSE_PUBLIC_KEY` | Yes | Langfuse public key |
| `LANGFUSE_SECRET_KEY` | Yes | Langfuse secret key |
| `LANGFUSE_HOST` or `LANGFUSE_BASE_URL` | No | Langfuse host URL (default: `https://us.cloud.langfuse.com`) |

## When to Use

- Checking prompt content
- Verifying a specific label's version
- Debugging prompts

## Commands

### 1. Show Prompt Content

Get the latest version:
```bash
npx tsx scripts/langfuse-prompt-view.ts <prompt-name>
```

Get a specific label's version:
```bash
npx tsx scripts/langfuse-prompt-view.ts <prompt-name> --label=development
npx tsx scripts/langfuse-prompt-view.ts <prompt-name> --label=production
```

## Output Example

```
============================================================
Prompt: librarian-system
Version: 3
Labels: development
============================================================

--- Content ---

You are an excellent librarian...

--- End ---
```

## Notes

- If no label is specified, the latest version is returned
- Specifying a non-existent prompt name or label will result in an error
