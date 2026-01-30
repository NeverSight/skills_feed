---
name: marp-lens
description: Semantic search for Marp presentations using vector embeddings. Use when finding relevant slides by topic, retrieving slide content, or exploring presentation materials. Triggers on "find slides about...", "search presentations for...", "get slide content", "what slides cover...", or any Marp/presentation search query.
---

# marp-lens

Vector-based semantic search CLI for Marp presentations.

## Quick Reference

```bash
# Search slides by meaning
npx marp-lens search "機械学習の基礎" --limit 5

# Get specific slide content
npx marp-lens get "presentation.md #3"

# View database stats
npx marp-lens stats

# Index new/changed files
npx marp-lens index -d ./slides

# Index with image descriptions
npx marp-lens index -d ./slides --with-images
```

## Commands

### Search
```bash
npx marp-lens search "<query>" [options]
```
| Option | Description |
|--------|-------------|
| `-l, --limit <n>` | Max results (default: 10) |
| `-t, --threshold <0-1>` | Min similarity (default: 0) |
| `-o, --format <type>` | Output: `table` or `json` |

### Get Slide
```bash
npx marp-lens get "<file> #<number>"
```
Retrieves full content of a specific slide. Supports partial path matching.

### Index
```bash
npx marp-lens index [options]
```
| Option | Description |
|--------|-------------|
| `-d, --dir <path>` | Directory to index |
| `-f, --file <path>` | Single file to index |
| `-r, --rebuild` | Clear and rebuild index |
| `-i, --with-images` | Include image descriptions |

### Stats
```bash
npx marp-lens stats
```
Shows file count, slide count, embedding count, and database size.

## Workflow

1. **Find relevant slides**: `npx marp-lens search "topic"`
2. **Get full content**: `npx marp-lens get "file.md #N"` for slides of interest
3. **Re-index if needed**: `npx marp-lens index -d ./slides` after adding files

## Output Format

Search results show similarity score, file path, slide number, heading, and content preview. Use `--format json` for structured output.
