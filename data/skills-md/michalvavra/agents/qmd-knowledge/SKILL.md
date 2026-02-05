---
name: qmd-knowledge
description: Knowledge management with QMD (Quick Markdown Search). Search, retrieve, and organize your personal knowledge base, notes, docs, and meeting transcripts. Use when asking about past notes, documentation, meetings, or when needing to recall information from your indexed markdown files.
license: See https://github.com/hjanuschka/pi-qmd
---

# QMD Knowledge Management

QMD (Quick Markdown Search) is an on-device search engine for your knowledge base. It indexes markdown notes, meeting transcripts, documentation, and more, providing fast keyword search, semantic search, and hybrid search with LLM reranking.

## Available Tools

| Tool | Best For | Speed |
|------|----------|-------|
| `qmd_search` | Exact keywords, known terms | Fast |
| `qmd_vsearch` | Conceptual queries, fuzzy matching | Medium |
| `qmd_query` | Best quality, complex questions | Slower |
| `qmd_get` | Retrieve full document content | Fast |
| `qmd_multi_get` | Get multiple docs at once | Fast |
| `qmd_status` | Check index health | Fast |

## Search Strategy

### 1. Start with the right search type

**Use `qmd_search` when:**
- User mentions specific terms they know exist
- Looking for exact matches (error codes, function names, dates)
- Need fast results

**Use `qmd_vsearch` when:**
- Query is conceptual ("how do I deploy", "authentication flow")
- User's words may differ from document terms
- Looking for related content

**Use `qmd_query` when:**
- Need highest quality results
- Complex or ambiguous queries
- First two methods returned poor results

### 2. Retrieve relevant documents

After searching, use `qmd_get` with the path or docid to fetch full content:

```
# By path (from search results)
qmd_get { "path": "notes/meeting-2024-01-15.md" }

# By docid (the #xxx from results)
qmd_get { "path": "#abc123" }

# Multiple documents
qmd_multi_get { "pattern": "docs/api/*.md" }
```

### 3. Refine if needed

- If results are too broad: add collection filter (`collection: "notes"`)
- If results are too few: try semantic search or lower `minScore`
- If results are irrelevant: use hybrid `qmd_query`

## Search Examples

### Finding meeting notes
```
qmd_search { "query": "quarterly planning 2024", "collection": "meetings" }
```

### Finding how-to documentation
```
qmd_vsearch { "query": "how to set up CI/CD pipeline" }
```

### Complex lookup
```
qmd_query { "query": "authentication flow for API users" }
```

### Getting specific content
```
qmd_get { "path": "#a1b2c3", "full": true }
```

## Understanding Results

Search results include:
- **path**: File path relative to collection
- **docid**: Short hash (use with `qmd_get #xxx`)
- **title**: Document title (from first heading)
- **context**: Collection/path context description
- **score**: Relevance 0-100% (green >70%, yellow >40%)
- **snippet**: Matching excerpt with context

## Collections

Users organize content into collections. Check what's available:
```
qmd_status {}
```

Common collections:
- `notes` - Personal notes
- `docs` - Documentation
- `meetings` - Meeting transcripts
- `work` - Work-related content

Filter searches by collection when user's intent is clear.

## Best Practices

1. **Start broad, then narrow**: Begin with `qmd_query` if unsure, refine with filters

2. **Combine tools**: Search first, then `qmd_get` to retrieve full content

3. **Use appropriate search type**: 
   - Keywords → `qmd_search`
   - Concepts → `qmd_vsearch`
   - Complex → `qmd_query`

4. **Check status first**: If searches fail, `qmd_status` can reveal issues

5. **Respect user's collections**: Don't search everywhere if user mentions specific notes

## Troubleshooting

**"No results found":**
- Try semantic search (`qmd_vsearch`)
- Lower or remove `minScore`
- Check `qmd_status` for collection names

**"Embeddings not ready":**
- User needs to run `qmd embed`
- `qmd_search` still works (BM25 only)

**"Command not found":**
- QMD not installed
- QMD requires Bun runtime
- Tell user to install Bun first, then QMD:
  ```bash
  brew install oven-sh/bun/bun
  bun install -g https://github.com/tobi/qmd
  ```

## Installation & Setup (for users)

```bash
# Install Bun (required runtime for QMD)
brew install oven-sh/bun/bun

# Install QMD
bun install -g https://github.com/tobi/qmd

# Add collections
qmd collection add ~/notes --name notes
qmd collection add ~/Documents/meetings --name meetings

# Generate embeddings (for semantic search)
qmd embed
```

## Quick Reference

```bash
# Keyword search
qmd search "API authentication"

# Semantic search
qmd vsearch "how to log in"

# Hybrid (best quality)
qmd query "user auth flow"

# Get document
qmd get "docs/api.md"
qmd get "#abc123"

# Multiple documents
qmd multi-get "journals/2025-05*.md"

# Status
qmd status
```
