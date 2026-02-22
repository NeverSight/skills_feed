---
name: qmd
description: |
  Local semantic search engine for markdown knowledge bases using qmd (tobi/qmd).
  Indexes markdown files with BM25 keyword search, vector embeddings for semantic search,
  and hybrid reranked queries. Auto-indexes on file edits via Claude Code hooks and
  refreshes embeddings overnight via launchd. Use when searching project docs,
  knowledge bases, meeting notes, or any indexed markdown collection.
allowed-tools: Bash Read Write Edit
---

# qmd - Local Search for Knowledge Bases

Search indexed markdown collections using keyword, semantic, or hybrid search.

## When to Use

- Searching project documentation or knowledge bases
- Finding related files before making changes
- Discovering context across many markdown files
- Answering questions that span multiple documents

## Quick Start

```bash
# Keyword search (fast, BM25)
qmd search "your query" --json -n 10

# Find related files
qmd search "topic" --files -n 20

# Semantic search (requires embeddings)
qmd vsearch "conceptual question" -n 10

# Hybrid search with reranking (best quality, slower)
qmd query "natural language question" --json -n 10

# Get full document content
qmd get "path/to/file.md" --full
```

## Search Modes

| Mode | Command | Speed | Best For |
|------|---------|-------|----------|
| Keyword (BM25) | `qmd search` | Fast | Exact terms, known keywords |
| Semantic | `qmd vsearch` | Medium | Conceptual queries, synonyms |
| Hybrid | `qmd query` | Slow | Complex questions needing both |
| File list | `qmd search --files` | Fast | Finding all related files |

## Workflows

### Before answering a question
```bash
qmd search "relevant keywords" --json -n 10
```
Review results, then read specific files for full context.

### After making changes (update cascade)
```bash
qmd search "topic you changed" --files -n 20
```
Review all related files and update any that reference the changed topic.

### Writing content that needs project context
```bash
qmd search "positioning voice tone" --json -n 10
qmd search "topic for content" --json -n 10
```

## Index Management

```bash
# Update text index (fast, ~1 sec)
qmd update

# Update embeddings (slow, ~3-4 min)
qmd embed

# Check index health
qmd status

# List collections
qmd collection list
```

## Setup & Troubleshooting

If qmd is not installed or broken, run the doctor script:

```bash
bash ~/.claude/skills/qmd/scripts/doctor.sh
```

For full installation and automation setup, see [setup/README.md](setup/README.md).

For the complete command reference, see [references/commands.md](references/commands.md).

## Tips

- Results below score 0.3 are noise - ignore them
- `qmd search` (BM25) is good enough for day-to-day use
- Only use `vsearch` when keywords don't match concepts
- After changes, always run `--files` query to catch ripple effects
- Combine with Read tool: qmd finds files, Read gets full content

## Self-Learning

Read [LEARNED.md](LEARNED.md) before using this skill. It contains hard-won lessons about what works and what doesn't.

**Update LEARNED.md when you discover:**
- A query that returned bad results and what worked instead
- Search mode choice that was wrong (e.g. `search` missed something `vsearch` found)
- Index issues (stale embeddings, missing files, broken binary)
- Installation or automation gotchas
- CLAUDE.md patterns that worked or failed for enforcing context-first behavior

**Consolidation (keep LEARNED.md under 50 lines):**
Before adding a new entry, check the file length. If it's over 50 lines:
1. Merge duplicate/overlapping entries into single proven patterns
2. Remove entries older than 3 months that haven't been reinforced
3. Drop one-off observations that never recurred
4. Move detailed historical context to `LEARNED-archive.md` if worth preserving
5. Keep only entries that would change behavior - if it's obvious, cut it
