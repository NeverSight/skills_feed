---
name: opensearch-docs-search
description: Search OpenSearch documentation, blogs, and community forums. Use when the user asks about OpenSearch features, configuration, APIs, troubleshooting, k-NN, neural search, cluster settings, index mappings, query DSL, or any OpenSearch-related questions.
---

# OpenSearch Documentation Search

Search OpenSearch docs, blogs, and forum using the bundled script (Python 3.10+, no dependencies).

## Usage

```bash
python scripts/search.py docs "k-NN"
python scripts/search.py blogs "performance" --limit 5
python scripts/search.py forum "cluster health"
```

Options: `-v/--version` (docs/blogs), `-l/--limit`, `-o/--offset` (docs/blogs)

## Query Tips

- Version search: use dot notation (`"opensearch 3.5"`), not hyphenated slug (`"3-5"`)
- Blog release posts: search `"opensearch {major}.{minor}"` (e.g., `"opensearch 3.5"`)
- The `-v/--version` flag filters documentation version, not blog post version. For blogs, include the version number in the query string itself.
