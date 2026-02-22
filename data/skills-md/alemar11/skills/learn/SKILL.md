---
name: learn
description: Capture durable corrections or preferences and write confirmed learnings to AGENTS.md. Use when the user sets lasting guidance.
---

# Learn From Mistakes

## Quick flow
- Find the most recent **durable** correction/avoidance/preference in the current conversation.
- Determine scope before proposing a target:
  - If the rule is clearly **project-specific** (e.g., tied to repo structure, tooling, or workflows), suggest **project** AGENTS.md first.
  - Otherwise, default to **global** unless the user explicitly says "project", "project-root", or "workspace".
  - Do not pick local just because it exists.
- If the learning is new (not already in AGENTS.md), propose:
  - Short summary (1 line)
  - Detailed instruction (1–3 bullets)
- Confirmation should be lightweight: state what you will write and where.
- Assume it is durable and that global is OK unless the user says otherwise. User can reply "no", "stop", "project", or similar to change/cancel.
- If nothing new is found in context (or it already exists), run `scripts/extract_recent_transcript.py`, scan the JSONL from the last user message backward to find the most recent **durable** correction, then repeat the steps above.
- After this flow finishes, do not continue writing durable changes into AGENTS.md without following the steps above.
- Always confirm before writing into AGENTS.md when triggered by a durable preference.

## Durability filter
- Keep long-lived preferences and permanent mistake corrections.
- Exclude one-off or context-specific instructions tied only to the current task/files.
- Examples:
  - Project-specific: “Use `pnpm` in this repo,” “Update `docs/ARCHITECTURE.md` when changing auth.”
  - Global: “Always use `rg` for file search,” “Ask before writing to AGENTS.md.”

## AGENTS.md write
- Use section `## Codex Learnings` (create if missing).
- Bullets should be concise and specific ("Avoid X" / "Do Y instead of Z").
- Skip duplicates. If a conflict exists, ask how to resolve before writing.

## Target labels
- **global** (default): `~/.codex/AGENTS.md`
- **project**: `AGENTS.md` at repo root (or cwd if no repo)
- If both repo root and cwd have AGENTS.md, label them **project-root** and **workspace**.
- If multiple AGENTS.md exist in subfolders, consider whether the rule is better scoped to a sub-area:
  - If the rule is likely relevant to the current project but scoped to a specific subfolder, suggest the closest existing sub-AGENTS.md first.
  - If no sub-AGENTS.md exists, propose the repo AGENTS.md first.
  - Always show the full path when suggesting a sub-AGENTS.md so the user can evaluate the scope.
  - Always leave the final choice to the user.
- If the chosen target does not exist, ask to create it (still default to global unless user says otherwise).

## Script output
`scripts/extract_recent_transcript.py` returns JSON with `session_id`, `rollout_path`, `cwd`, and AGENTS.md candidates/suggestions.
