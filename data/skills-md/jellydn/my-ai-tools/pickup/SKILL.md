---
name: pickup
description: Resumes work from a previous handoff session which are stored in `.claude/handoffs/`
license: MIT
compatibility: claude, opencode, codex, gemini
hint: Use when resuming work from a previous handoff session
user-invocable: true
metadata:
  audience: all
  workflow: workflow
---

# Pickup Handoff

Resumes work from a previous handoff session which are stored in `.claude/handoffs/`.

## Usage

`/pickup [HANDOFF_FILE]`

If no handoff file is specified, will show available handoffs and prompt for selection.

## Process

1. Find available handoffs in `.claude/handoffs/`
2. Read the selected handoff file
3. Present the handoff summary to the user
4. Ask the user to confirm they want to continue
5. If confirmed, proceed with the next step described in the handoff

## Available Handoffs

To see available handoffs:

```bash
ls -la .claude/handoffs/
```

Handoffs are named in format: `[YYYY-MM-DD]-[slug].md`
