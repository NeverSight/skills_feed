---
name: token-optimizer
description: Optimization suite for OpenClaw agents to prevent token leaks and context bloat. Use when an agent needs to implement background task isolation (Cron) or a Reset & Summarize workflow (RAG).
version: 1.1.0
authors:
  - Pépère (shAde)
  - Zayan (Clément)
---

# Token Optimizer Skill

This skill provides the procedural knowledge to keep your OpenClaw instance lean and efficient.

## Quick Reference

| Problem | Solution |
|---------|----------|
| Background tasks bloating context | Cron isolation (`sessionTarget: "isolated"`) |
| Reading entire history every turn | Local RAG with `memory_search` |
| Context exceeds 100k tokens | Reset & Summarize protocol |
| Finding old conversations | Session transcript indexing |

---

## Workflow 1: Periodic Task Isolation

To prevent background tasks from bloating your main conversation context, always isolate them.

### Steps

1. Locate your `openclaw.json` config.
2. In the `cron.jobs` array, set `sessionTarget: "isolated"` for any task that doesn't need to be part of the main chat history.
3. Use the `message` tool within the task's payload if human intervention is required.

### Example Config

```json
{
  "cron": {
    "jobs": [
      {
        "name": "Background Check",
        "schedule": { "kind": "every", "everyMs": 1800000 },
        "sessionTarget": "isolated",
        "payload": {
          "kind": "agentTurn",
          "message": "Check for updates. If found, use message tool to notify user.",
          "deliver": true
        }
      }
    ]
  }
}
```

### Key Points

- `sessionTarget: "isolated"` runs the task in a separate, transient session
- Use `deliver: true` to send results back to the main channel
- Isolated sessions don't pollute your main context with heartbeat/check history

---

## Workflow 2: Reset & Summarize (The "Digital Soul" Protocol)

When your context usage (visible via `📊 session_status`) exceeds 100k tokens, perform a manual consolidation.

### Steps

1. **Check Context**: Run `📊 session_status` to see current token usage
2. **Scan History**: Review the current session for new facts, preferences, or project updates
3. **Update MEMORY.md**: Append these new facts to your long-term memory file
4. **Daily Log**: Ensure `memory/YYYY-MM-DD.md` is up to date with today's events
5. **Restart**: Run `openclaw gateway restart` to clear the active history

### When to Trigger

- Context > 100k tokens
- Session running for several days
- Noticeably slower responses
- User explicitly requests a "fresh start"

---

## Workflow 3: Local RAG Configuration

For efficient recall without token burn, configure local embeddings.

### Configuration (`openclaw.json`)

```json
{
  "memorySearch": {
    "embedding": {
      "provider": "local",
      "model": "hf:second-state/All-MiniLM-L6-v2-Embedding-GGUF"
    },
    "store": "sqlite",
    "paths": ["memory/", "MEMORY.md"],
    "extraPaths": []
  }
}
```

### Usage

Use `memory_search` to retrieve context from your logs instead of loading everything:

```
memory_search(query="what did we decide about the API design")
```

The tool returns relevant snippets with file paths and line numbers. Use `memory_get` to pull specific sections.

---

## Workflow 4: Session Transcript Indexing (Advanced)

Index your session transcripts (`.jsonl` files) for searchable conversation history.

### How It Works

OpenClaw stores session transcripts in `~/.openclaw/sessions/`. These can be indexed for semantic search, allowing you to find old conversations without loading them into context.

### Configuration

Add transcript paths to `memorySearch.extraPaths`:

```json
{
  "memorySearch": {
    "extraPaths": [
      "~/.openclaw/sessions/*.jsonl"
    ]
  }
}
```

### Best Practices

- Index selectively (recent sessions, important conversations)
- Use date-based filtering to limit search scope
- Archive old transcripts to cold storage after indexing

---

## Workflow 5: Hybrid Search (Vector + BM25)

Combine semantic search with keyword matching for more accurate retrieval.

### Why Hybrid?

| Search Type | Strengths | Weaknesses |
|-------------|-----------|------------|
| Vector (semantic) | Finds conceptually similar content | May miss exact terms |
| BM25 (keyword) | Finds exact matches | Misses synonyms/paraphrases |
| **Hybrid** | Best of both worlds | Slightly more compute |

### How to Use

When `memory_search` returns low-confidence results:

1. Try the search with different phrasing (semantic variation)
2. Search for exact keywords you remember (BM25 behavior)
3. Combine results manually if needed

### Future Enhancement

OpenClaw's RAG system may support native hybrid search in future versions. For now, run multiple queries when precision matters.

---

## Troubleshooting

### "My context is growing too fast"

1. Check cron jobs: Are they isolated?
2. Check heartbeat frequency: Too frequent = more tokens
3. Are you loading large files unnecessarily?

### "memory_search returns nothing"

1. Verify `memorySearch` is configured in `openclaw.json`
2. Check that the embedding model is downloaded
3. Ensure memory files exist and have content

### "Restart didn't clear context"

The restart clears the session history, but:
- System prompt is always loaded
- Workspace files (MEMORY.md, etc.) are injected fresh
- This is by design for continuity

---

## Credits

- **Pépère** (shAde) — Original concept and documentation
- **Zayan** (Clément) — Implementation and testing

*Built for the OpenClaw community.* 🦦😸
