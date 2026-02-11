---
name: jina
description: "Extract content from URLs and search with Jina. Use when you need to: (1) read and extract content from any URL, (2) perform site-specific searches, or (3) scrape web page content."
version: 1.0.0
skillId: skp-t0gx8xqrep79hau0t7qn6yrp
workflowId: c-ee1nlrsdlebaodpn5fvs3sj2
installationId: skpi-jqzppbf80ss2qz3kx7wtqwsw
category: text-data
---

# Jina

Extract content from URLs and search with Jina. Use when you need to: (1) read and extract content from any URL, (2) perform site-specific searches, or (3) scrape web page content.

## Input

Provide input as JSON:

```json
{
  "url": "URL to read and extract content from (e.g., https://example.com/article)",
  "query": "Search query for finding relevant content (e.g., 'AI workflow automation')",
  "site": "Optional: specific site to search within (e.g., 'github.com' to search only GitHub)"
}
```

## Execution (Pattern B: Text/Data)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-jqzppbf80ss2qz3kx7wtqwsw --input '{
  "url": "https://example.com/article",
  "query": "AI workflow"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-ee1nlrsdlebaodpn5fvs3sj2"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Extract Text Content

```bash
# Get text content from toolcalls
CONTENT=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.nodes[].content')
echo "$CONTENT"
```

## Expected Output

- **Type**: Text content
- **Format**: Extracted URL content or search results
- **Action**: Display content to user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
