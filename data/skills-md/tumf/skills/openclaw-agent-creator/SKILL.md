---
name: openclaw-agent-creator
description: |
  Create and maintain OpenClaw agent workspaces using the "Memory as Documentation" layout.
  Use when you need to: (1) create a new OpenClaw workspace/profile, (2) generate bootstrap files
  (AGENTS.md, SOUL.md, USER.md, IDENTITY.md, TOOLS.md, MEMORY.md, memory/YYYY-MM-DD.md),
  (3) keep instructions/persona/memory separated and token-lean, or (4) set up a safe git backup
  of an OpenClaw workspace without committing secrets.
---

# OpenClaw Agent Creator

This skill helps you create a new OpenClaw "agent persona" by generating a clean workspace and the standard bootstrap files.

## Quick Start

1) Create a new workspace directory with templates:

```bash
python3 "$SKILL_ROOT/scripts/init_workspace.py" \
  --workspace "$HOME/.openclaw/workspace-myprofile" \
  --agent-name "Claw" \
  --agent-vibe "sharp, concise, helpful" \
  --agent-emoji ":lobster:" \
  --user-name "tumf" \
  --user-language "Japanese" \
  --create-today-log
```

By default, this also creates a safe starter `.gitignore` to reduce the risk of committing secrets.
Disable with `--no-gitignore`.

2) Point OpenClaw at the workspace:

- Prefer profiles: set `OPENCLAW_PROFILE=myprofile` when launching OpenClaw.
  - By default, this maps the workspace to `~/.openclaw/workspace-myprofile`.
- Or set the workspace path in `~/.openclaw/openclaw.json`.

If OpenClaw is installed, `openclaw setup --workspace <path>` can also seed missing bootstrap files without overwriting existing ones.

## Files and Responsibilities (keep them separated)

- `IDENTITY.md`: stable identity metadata (name/vibe/emoji). Avoid tasks.
- `SOUL.md`: stable behavioral rules (values, boundaries). Avoid temporary tasks.
- `USER.md`: user preferences (language, formatting, expectations).
- `AGENTS.md`: operating instructions (workflow, safety bar, memory policy).
- `TOOLS.md`: local environment notes and "dangerous command" guardrails (guidance only).

Memory layer:

- `memory/YYYY-MM-DD.md`: daily running log (append-only, messy is OK).
- `MEMORY.md`: curated durable facts/decisions/lessons (keep small).

## Safety / Hygiene

- Do not store secrets in the workspace (even if backed up privately).
- Keep bootstrap files short; OpenClaw may truncate them when injecting.
- Prefer writing durable notes into `MEMORY.md` and transient notes into `memory/YYYY-MM-DD.md`.

## Scripts

Note: Always call scripts via `python3 "$SKILL_ROOT/scripts/<name>.py" ...`.

### init_workspace.py

Create an OpenClaw workspace folder and seed bootstrap files. Defaults to safe behavior (no overwrites).

```bash
python3 "$SKILL_ROOT/scripts/init_workspace.py" --help
```

### promote_keep.py

Promote `KEEP:` bullet lines from a daily log into `MEMORY.md`.

```bash
python3 "$SKILL_ROOT/scripts/promote_keep.py" \
  --daily "$HOME/.openclaw/workspace/memory/2026-02-19.md" \
  --memory "$HOME/.openclaw/workspace/MEMORY.md"
```
