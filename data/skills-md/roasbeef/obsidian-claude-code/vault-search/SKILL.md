---
name: vault-search
description: Semantic search and Dataview-style queries across the Obsidian vault. Use when searching for notes by meaning, finding related content, querying frontmatter metadata, or answering questions about vault contents. Trigger phrases include "search vault", "find notes about", "what do I have on", "related notes", "list tasks", "show positions".
allowed-tools: Read, Bash(python:*)
---

# Vault Search Skill

Provides semantic search and SQL queries over the Obsidian vault using sqlite-vec for vector storage and ChromaDB's embedding function.

## Python Environment

**Interpreter:** `/Users/roasbeef/vault/.claude/venv/bin/python`

**Required packages:**
- sqlite-vec (vector search extension)
- chromadb (embedding function only)

## Database Location

**Path:** `/Users/roasbeef/vault/.claude/vault_search/vault.db`

Contains:
- `notes` table: frontmatter metadata for all markdown files
- `vec_chunks` table: vector embeddings for semantic search

## Available Scripts

### search.py - Semantic Search

Find notes by meaning using vector similarity.

```bash
# Basic semantic search
python scripts/search.py --query "options trading strategies" --n-results 5

# Filter by folder
python scripts/search.py --query "earnings analysis" --folder "investing"

# Filter by metadata
python scripts/search.py --query "task automation" --where "status='open'"

# Combined: semantic + metadata
python scripts/search.py --query "portfolio risk" --where "folder LIKE 'investing%' AND status='open'"
```

**Arguments:**
- `--query` (required): Search query text
- `--n-results`: Number of results (default: 5)
- `--folder`: Filter by folder prefix
- `--where`: SQL WHERE clause for metadata filtering
- `--db-path`: Database path (default: .claude/vault_search/vault.db)

**Output:**
- Human-readable results with snippets
- JSON block for programmatic use

### dataview.py - SQL Queries (Dataview Replacement)

Query frontmatter metadata using SQL.

```bash
# Open tasks due this week
python scripts/dataview.py --sql "SELECT path, due, priority FROM notes
                                   WHERE status = 'open'
                                   AND due < date('now', '+7 days')
                                   ORDER BY due"

# Tasks by folder
python scripts/dataview.py --sql "SELECT path, status, priority FROM notes
                                   WHERE folder LIKE 'TaskNotes%'
                                   AND status != 'done'"

# Investing positions
python scripts/dataview.py --sql "SELECT path, ticker, strategy, expiry FROM notes
                                   WHERE folder LIKE 'investing/Portfolio/Positions%'"

# Query by tags (using json_each)
python scripts/dataview.py --sql "SELECT DISTINCT n.path, n.title
                                   FROM notes n, json_each(n.tags) t
                                   WHERE t.value = 'automation'"
```

**Arguments:**
- `--sql` (required): SQL query to execute
- `--db-path`: Database path (default: .claude/vault_search/vault.db)
- `--format`: Output format: "table" or "json" (default: table)

**Available columns:**
- `path`, `folder`, `filename`, `title`, `modified`
- Frontmatter: `status`, `priority`, `due`, `scheduled`, `tags`, `projects`, `contexts`
- Investing: `ticker`, `strategy`, `expiry`

### index.py - Build/Rebuild Index

Rebuild the search index from vault files.

```bash
# Full rebuild
python scripts/index.py --vault-path /Users/roasbeef/vault --rebuild

# Incremental update (default)
python scripts/index.py --vault-path /Users/roasbeef/vault

# Show statistics
python scripts/index.py --stats
```

**Arguments:**
- `--vault-path`: Path to vault root (default: /Users/roasbeef/vault)
- `--db-path`: Database path (default: .claude/vault_search/vault.db)
- `--rebuild`: Force full rebuild
- `--stats`: Show index statistics

## When to Use This Skill

**Use semantic search (search.py) when:**
- User asks to "find notes about X"
- User wants "related notes" to a topic
- Answering questions about vault contents
- Exploring a topic across the vault

**Use dataview queries (dataview.py) when:**
- User asks to "list tasks" or "show open tasks"
- Filtering by specific metadata (status, due date, tags)
- Aggregating or counting notes
- Building dashboards or summaries

**Use combined queries when:**
- "Find notes about X that are also open tasks"
- "Show investing notes related to Y"

## Example Usage

### Find Related Notes
```
User: "What notes do I have about HTLC routing?"
→ python scripts/search.py --query "HTLC routing payment channels" --n-results 5
```

### List Open Tasks
```
User: "Show my open high-priority tasks"
→ python scripts/dataview.py --sql "SELECT path, due FROM notes
                                     WHERE status='open' AND priority='high'
                                     ORDER BY due"
```

### Combined Search
```
User: "Find investing notes about semiconductor supply chain"
→ python scripts/search.py --query "semiconductor supply chain"
                           --folder "investing"
                           --n-results 10
```

## Rebuilding the Index

Use the `/vault-index` command to rebuild the index when:
- Many files have changed
- Search results seem stale
- After bulk imports

## Technical Details

- **Embeddings:** ChromaDB DefaultEmbeddingFunction (ONNX MiniLM, 384 dims)
- **Storage:** sqlite-vec virtual tables
- **Chunking:** Split by markdown headings (v1)
- **Excluded folders:** `.obsidian`, `.smart-env`, `.claude`, `assets`, `Templates`
