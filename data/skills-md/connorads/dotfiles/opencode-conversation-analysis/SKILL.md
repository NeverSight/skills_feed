---
name: opencode-conversation-analysis
description: Analyze OpenCode conversation history to identify themes and patterns in user messages. Use when asked to analyze conversations, find themes, review how a user steers agents, or extract insights from session history.
compatibility: OpenCode-specific (relies on OpenCode session storage format). Requires jq, bash.
---

# Conversation Analysis

Analyze user messages from OpenCode sessions to identify recurring themes, communication patterns, and steering behaviours.

## Critical Rules

1. **NEVER cat or read chunk files directly** - they're huge and will explode your context
2. **Pass file paths to subagents** - let them read and analyze independently
3. **Use parallel subagents** - one per chunk, they run concurrently
4. **Subagents return structured JSON** - you synthesize at the end

## Workflow

### Step 1: Run Extraction

```bash
~/.agents/skills/opencode-conversation-analysis/scripts/extract.sh
```

This script:
- Finds all main sessions (excludes subagent child sessions)
- Extracts user messages with metadata (session_id, title, timestamp, text)
- Filters out messages < 10 characters
- Chunks into ~320k char files (~80k tokens each)
- Outputs to `/tmp/opencode-analysis/chunk_*.jsonl`

Review the output summary to see how many chunks were created.

### Step 2: Launch Parallel Subagents

For each chunk file, spawn a `general` subagent with this prompt template:

```
Read the file /tmp/opencode-analysis/chunk_N.jsonl which contains user messages from coding sessions (JSONL format with fields: session_id, session_title, timestamp, text).

Analyze these messages to identify recurring themes in how the user steers/guides AI coding assistants. Look for patterns like:
- How they give feedback
- How they correct mistakes
- How they scope/refine requests
- Communication style preferences
- Technical approaches they emphasize

For each theme you identify, provide:
1. Theme name (short, descriptive)
2. Description (1-2 sentences)
3. 2-3 direct quote examples from the messages

Return ONLY valid JSON in this format:
{
  "themes": [
    {
      "name": "Theme Name",
      "description": "Description of the pattern",
      "examples": ["quote 1", "quote 2"]
    }
  ]
}
```

Launch ALL chunk subagents in parallel (single message, multiple Task tool calls).

### Step 3: Synthesize Results

Once all subagents return:

1. Collect all theme objects from all chunks
2. Group similar themes (same name or overlapping descriptions)
3. Merge examples from duplicate themes
4. Rank themes by how many chunks they appeared in
5. Pick the best 2-3 examples per theme

### Step 4: Output Format

Present the final analysis as markdown with this structure:

```markdown
# Themes in How You Steer AI Coding Assistants

Analysis of N messages across M sessions (date range)

---

## 1. Theme Name

Description of the pattern.

**Examples:**
- "direct quote 1"
- "direct quote 2"
- "direct quote 3"

---

## 2. Next Theme
...
```

Output directly to the user - don't write to a file unless asked.

## Customisation Options

The user may request:
- **Different chunk sizes**: Edit `CHUNK_SIZE` in extract.sh (default 320000 chars)
- **Different message filter**: Edit the `${#text} -ge 10` check in extract.sh
- **Include subagent sessions**: Remove the `parentID == null` filter in extract.sh
- **Time period filtering**: Add timestamp filtering in extract.sh

## Storage Format Reference

See [references/storage-format.md](references/storage-format.md) for details on OpenCode's conversation storage structure.
