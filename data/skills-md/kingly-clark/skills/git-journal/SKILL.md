---
name: git-journal
description: Capture the "Why" behind code changes during AI-assisted development. Creates branch-scoped markdown journals preserving reasoning, tradeoffs, and context that would otherwise be lost. Use before commits, PRs, or multi-file changes. Use when significant reasoning happened in conversation that should be preserved. Use when the user asks to document why a decision was made. Use when the user says "remember to journal", "anything to journal", or similar prompts.
license: MIT
metadata:
  author: git-journal
  version: "1.0.0"
---

# Git Journal

Capture the "Why" behind code changes. Git tracks what/where/when/who—this skill captures **why**.

## Trigger Phrases

Users invoke this skill with phrases like:

| Phrase | Behavior |
|--------|----------|
| **"remember to journal"** | Set a session-long reminder. Throughout the conversation, proactively consider journaling when significant decisions are made, tradeoffs are discussed, or non-obvious solutions are chosen. |
| **"anything to journal?"** | Reflect on the current session. Review recent commits, code changes, and conversation to identify anything worth preserving in the journal. |
| **"journal this"** | Immediately capture the current context/decision in the journal. |
| **"update the journal"** | Run the update script and prompt for Why content. |

### "Remember to Journal" Mode

When activated, keep journaling in mind for the entire session:
- After complex problem-solving → consider journaling the reasoning
- After architectural decisions → capture the tradeoffs
- After rejected approaches → document why they were rejected
- Before commits → prompt if there's unjournaled context

### "Anything to Journal?" Reflection

When asked, review:
1. Recent git commits on the current branch
2. Code changes made during this conversation
3. Decisions and tradeoffs discussed
4. Non-obvious solutions or workarounds implemented

Then suggest specific entries for the journal, or confirm nothing significant needs capturing.

## Quick Start

1. Ensure journal exists:
   ```bash
   python skills/git-journal/scripts/ensure_git_journal.py
   ```

2. Update with current state:
   ```bash
   python skills/git-journal/scripts/update_git_journal.py
   ```

3. Write the **Why** section (automation handles Who/When/What).

## Journal Location

```
journals/YYYY-MM-DD_<branch-name>.md
```

- One journal per branch
- Flat file structure (no nested folders)
- Branch names normalized (slashes → hyphens)

## The 5 W's Priority

1. **Why** ← Primary. Always capture this.
2. **What** — Conceptual summary
3. **Where** — Key areas affected
4. **Who** — From git config
5. **When** — Timestamps

If time is limited, **only Why must be correct**.

## What to Write in Why

```markdown
## Why, current summary

**Intent**
- Refactored auth to support background token refresh

**Constraints**
- Must work offline after initial auth

**Tradeoffs**
- Added complexity for better UX

**Alternatives considered**
- Redux approach: rejected due to complexity

**Non-obvious nuance**
- Retry loop looks like a bug but handles edge case where...
```

Include:
- Problem being solved
- Why this solution was chosen
- Constraints (time, platform, APIs, business)
- Rejected alternatives and why
- Things that look wrong but are correct

## Journal Structure

Two layers:
- **Top**: Aggregated summary (periodically consolidated)
- **Bottom**: Detailed log (append-only entries with timestamps)

## Integration

See `references/cursor-rule-template.md` for a ready-to-use Cursor rule.

Optional pre-commit hook:
```bash
#!/bin/sh
python skills/git-journal/scripts/ensure_git_journal.py
```

## Files

- `scripts/ensure_git_journal.py` — Create journal if missing
- `scripts/update_git_journal.py` — Update Who/When/What
- `assets/git-journal-template.md` — Template for new journals
- `references/cursor-rule-template.md` — Cursor rule template
