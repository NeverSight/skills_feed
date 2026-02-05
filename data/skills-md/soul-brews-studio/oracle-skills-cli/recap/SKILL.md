---
name: recap
description: Fresh-start orientation—adaptive synthesis with bulletproof edge case handling. Use when starting a session, after /jump, lost your place, or before switching context.
trigger: /recap
---

# /recap — Fresh Start Context

**Goal**: Orient yourself in <10 seconds. Fast by default, rich on demand.

## Usage

```
/recap           # Fast: bash script + LLM suggestions
/recap --rich    # Full: read retro content, detailed analysis
```

---

## FAST MODE (Default)

**Run the script, then add suggestions:**

```bash
bun ~/.claude/skills/recap/recap.ts
```

Script outputs formatted data instantly (~0.1s). Then LLM adds:
- **What's next?** (2-3 options based on git state + focus)

**Total**: 1 bash call + LLM analysis = fast + smart

---

## "What's next?" Rules

| If you see... | Suggest... |
|---------------|------------|
| Untracked files | Commit them |
| Focus = completed | Pick from tracks or start fresh |
| Branch ahead | Push or create PR |

---

## RICH MODE (`/recap --rich`)

**Full context with retro/handoff content:**

```bash
bun ~/.claude/skills/recap/recap-rich.ts
```

Includes: tracks, retro summary, commits, handoff details.

---

## Hard Rules

1. **ONE bash call** — never multiple parallel calls (adds latency)
2. **Filenames only** — don't read retro/handoff content in fast mode
3. **Ask, don't suggest** — "What next?" not "You should..."

---

**Philosophy**: Detect reality. Surface blockers. Be fast.

**Version**: 6.1 (Bash script + LLM pattern)
**Updated**: 2026-01-14
