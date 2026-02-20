---
name: bye
description: >-
  Use when the user says /bye, "wrap up", "end session", or similar.
  Reconstructs full session history including compacted context,
  creates a sessionlog, commits changes, and summarizes next steps.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: 2.1.0
compatibility: Designed for Claude Code and Cursor
---

# Session Wrap-up

## CRITICAL: Restore Full Session History First

**Nothing proceeds until full history is reconstructed.** Context compaction hides earlier work — you must recover it or the sessionlog will be incomplete.

1. Use a subagent to analyze the session file (see [subagent-tasks.md](./subagent-tasks.md))
2. Follow the tool-specific restoration guide:
   - **Claude Code:** [claude-code-session-restoration.md](./claude-code-session-restoration.md)
   - **Cursor:** [cursor-session-restoration.md](./cursor-session-restoration.md)
3. Combine restored history with current context before continuing

If restoration finds **no prior work beyond current context**, proceed — but log that restoration was attempted.

> **Parallel session safety:** The user may have multiple sessions running. Filter by `$CLAUDE_SESSION_ID` and timestamp correlation. Never combine work from other sessions. If uncertain, ASK.

## Session Type Detection

After restoring history, classify the session:

| Signal | Type | Action |
|--------|------|--------|
| `"isSidechain": true` or in `subagents/` dir | Subagent | **STOP** — do not run /bye |
| `messageCount <= 2`, first msg contains `"Context: This summary"` | Metadata session | **SKIP** — not a real work session |
| First messages reference executing a plan; recent file in `~/.claude/plans/` | Plan execution | Read plan file; sessionlog documents execution vs plan |
| System message contains `"Plan mode is active"` | Plan creation | Plan file is the deliverable |
| None of above | Normal | Continue with checklist |

## Session Wrap-up Checklist

1. **Determine scope** — everything between last /bye (or session start) and now. Verify each item was discussed in THIS conversation.
2. **Assess work** — files created, files modified, decisions made, research done, tasks completed, tasks remaining.
3. **Trivial session?** If just Q&A with no file changes, ask: "Skip sessionlog?"
4. **Create or update sessionlog** — see [sessionlog-template.md](./sessionlog-template.md) for format, naming, and create-vs-update logic.
5. **Update project status** — if work relates to `projects/*/`, update its `status.md`.
6. **Handle git** — see git decision table below.
7. **Print final summary** — see template below.

## Git Decision Table

| Situation | Action |
|-----------|--------|
| Files I created/edited THIS session | Auto-commit |
| Untracked files from before | **ASK** |
| Modified files I didn't touch | **ASK** — likely parallel session |
| .env, credentials, secrets | **NEVER**, warn user |

Commit message: `[Brief description]\n\nSession wrap-up: YYYY-MM-DD`

Push if remote tracking exists.

## Final Summary Template

```
## Session Complete

**Accomplished:**
- [item 1]
- [item 2]

**Committed:** [hash]
- [file list]

**Pending:**
- [ ] [task 1]

**Sessionlog:** `sessionlogs/[file].md`

Ready to clear context.
```
