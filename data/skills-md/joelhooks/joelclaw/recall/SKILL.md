---
name: recall
displayName: Recall
description: "Fan-out search across all memory sources when context is unclear or vaguely referenced. Triggers on: 'from earlier', 'remember when', 'what we discussed', 'that thing with', 'the conversation about', 'did we ever', 'what happened with', 'you mentioned', 'we talked about', 'earlier today', 'last session', 'the other day', or any vague reference to past context that needs resolution before the agent can act."
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, memory, recall, context, retrieval]
---

# Recall — Find What Was Said

When Joel references something vaguely, don't guess — fan out across all memory sources and find it.

## Trigger Detection

Phrases that indicate a recall is needed (case-insensitive):
- "from earlier", "earlier today", "earlier this week"
- "remember when", "remember that", "you mentioned"
- "what we discussed", "what we talked about", "the conversation about"
- "that thing with", "the thing about", "what was that"
- "did we ever", "have we", "wasn't there"
- "last session", "the other day", "yesterday"
- "correlate with", "connect to what we"
- Any vague pronoun reference to past context ("those photos", "that idea", "the notes")

**Key principle**: If you'd have to guess what "earlier" or "that" refers to, you need recall.

## Fan-Out Search Pattern

Search these sources **in parallel** where possible, with timeouts on each:

### 1. Today's Daily Log (fastest, most likely)
```bash
# Always check first — most "from earlier" references are same-day
cat ~/.joelclaw/workspace/memory/$(date +%Y-%m-%d).md
```

### 2. Recent Daily Logs (if today's doesn't have it)
```bash
# Yesterday and day before
cat ~/.joelclaw/workspace/memory/$(date -v-1d +%Y-%m-%d).md
cat ~/.joelclaw/workspace/memory/$(date -v-2d +%Y-%m-%d).md
```

### 3. Curated Memory
```bash
cat ~/.joelclaw/workspace/MEMORY.md
```
Search for keywords from the vague reference.

### 4. Session Transcripts
Use the `session_context` tool to search recent sessions:
```
sessions(limit: 10)  # find recent session IDs
session_context(session_id: "...", query: "what was discussed about <topic>")
```

### 5. Vault Notes
```bash
# Keyword search across Vault
grep -ri "<keywords>" ~/Vault/ --include="*.md" -l | head -10
```

### 6. System Log
```bash
slog tail --count 20  # recent infrastructure changes
```

### 7. Processed Media
```bash
# Check for images/audio that were processed
ls /tmp/joelclaw-media/ 2>/dev/null
```

### 8. Redis State
```bash
# Memory proposals, loop state, etc.
redis-cli LRANGE memory:review:pending 0 -1 2>/dev/null
```

## Workflow

1. **Extract keywords** from the vague reference. "Those photos from earlier" → keywords: photos, images, media, telegram.
2. **Fan out** across sources 1-8 above. Use `timeout 5` on any command that might hang.
3. **Synthesize** — combine findings into a coherent summary of what was found.
4. **Present context** — show Joel what you found, then continue with the original task.
5. **If nothing found** — say so honestly. Don't fabricate. Ask Joel to clarify.

## Timeouts Are Mandatory

Every external call (Redis, grep over large dirs, session reads) MUST have a timeout. The gateway session cannot hang on a recall operation.

```bash
# Good
timeout 5 grep -ri "keyword" ~/Vault/ --include="*.md" -l | head -10

# Bad — can hang indefinitely
grep -ri "keyword" ~/Vault/ --include="*.md"
```

## Anti-Patterns

- **Don't grep one file and call it done.** The whole point is fan-out.
- **Don't guess when recall fails.** Say "I couldn't find it" and ask.
- **Don't read entire session transcripts.** Use `session_context` with a focused query.
- **Don't skip media.** Photos, audio, processed images in `/tmp/joelclaw-media/` are often what "from earlier" refers to.
