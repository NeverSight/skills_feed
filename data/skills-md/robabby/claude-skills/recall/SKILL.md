---
name: recall
description: Search Obsidian memories by keyword and concept
---

# Recall

Search stored memories using keyword/concept matching.

## Workflow

1. Parse the search query from $ARGUMENTS
   - If no arguments provided, ask what to search for

2. Determine search strategy:
   - Content search: Grep for query in memory file content
   - Concept search: Grep for query in frontmatter concepts
   - Type filter: Optionally narrow to specific memory type folder

3. Execute searches in `<vault>/Areas/AI/Memory`:

   ```
   # Content search
   Grep pattern="$QUERY" path="<vault>/Areas/AI/Memory" glob="*.md"

   # Concept search (frontmatter)
   Grep pattern="concepts:.*$QUERY" path="<vault>/Areas/AI/Memory" glob="*.md"

   # Type-filtered (if specified)
   Grep pattern="$QUERY" path="<vault>/Areas/AI/Memory/Strategic" glob="*.md"
   ```

4. Read the matching files (up to limit, default 10)

5. Sort by importance if multiple results

6. Present findings:
   - "Found X memories about [topic]..."
   - Summarize top 2-3 findings
   - Note memory types and importance
   - Mention if more results available

## Search Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Query | required | Search terms |
| Limit | 10 | Max results to read |
| Type | all | Filter: episodic/semantic/procedural/strategic |

## Search Patterns

```bash
# General content search
Grep pattern="metatron" path="<vault>/Areas/AI/Memory" glob="*.md"

# Concept frontmatter search
Grep pattern="concepts:.*interview" path="<vault>/Areas/AI/Memory" glob="*.md"

# Type-filtered search
Grep pattern="deploy" path="<vault>/Areas/AI/Memory/Procedural" glob="*.md"

# High importance only
Grep pattern="importance: 0\\.[89]" path="<vault>/Areas/AI/Memory" glob="*.md"

# Recent memories (Glob sorts by mtime)
Glob pattern="Areas/AI/Memory/**/*.md" path="<vault>"
```

## Examples

User: `/recall hexis integration`
-> Search content and concepts for "hexis" and "integration"
-> Present matching memories with type and importance

User: `/recall deployment procedural`
-> Search in Areas/AI/Memory/Procedural/ for "deployment"
-> Focus on how-to memories

User: `/recall`
-> Ask: "What would you like to search for?"

## Response Format

Present findings conversationally:
- "Found X memories about [topic]..."
- Summarize the most relevant 2-3 findings
- Note memory types and importance levels
- Mention if there are more results available
- Offer to read specific memories in full if needed
