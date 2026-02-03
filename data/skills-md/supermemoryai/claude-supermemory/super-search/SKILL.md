---
name: super-search
description: Search your coding memory. Use when user asks about past work, previous sessions, how something was implemented, what they worked on before, or wants to recall information from earlier sessions.
allowed-tools: Bash(node:*)
---

# Super Search

Search Supermemory for past coding sessions, decisions, and saved information.

## How to Search

Run the search script with the user's query:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" "USER_QUERY_HERE"
```

Replace `USER_QUERY_HERE` with what the user is searching for.

## Examples

- User asks "what did I work on yesterday":
  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" "work yesterday recent activity"
  ```

- User asks "how did I implement auth":
  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" "authentication implementation"
  ```

## Present Results

The script outputs formatted memory results. Present them clearly to the user and offer to search again with different terms if needed.
