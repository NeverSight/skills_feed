---
name: writing-skills
description: Author and maintain Agent Skills in this repo. Use when creating or updating SKILL.md files, scripts, references, or skill documentation.
---

# Writing Skills

## When to Use This Skill

Use this skill when you need to create or update skills in this repository, including SKILL docs, scripts, references, or assets.

## Structure

- Every skill directory must include `SKILL.md` at the root.
- Optional directories: `scripts/`, `references/`, and `assets/`.
- Keep `SKILL.md` concise (aim under ~500 lines). Move long procedures into `references/`.
- Use relative paths from the skill root when linking to other files.

## Frontmatter Rules

- `name`: lowercase letters and hyphens only, must match the directory name.
- `description`: describe what the skill does and when to use it; include trigger keywords.
- Optional fields: `license`, `compatibility`, `metadata`.

## Progressive Disclosure

- Metadata loads at startup, so keep it short and specific.
- `SKILL.md` should be the main playbook.
- Detailed references and examples live in `references/` and load only when needed.

## Documentation Conventions (This Repo)

- Commands should use full paths: `uv run ~/.claude/skills/<skill-name>/scripts/<script>.py`
- Provide `.example` configs and keep real configs out of git.
- `uv.lock` is tracked intentionally for reproducible builds.
- Keep examples runnable and realistic.

## Checklist

- `SKILL.md` frontmatter is valid and matches the folder name.
- Usage examples run from the skill root.
- Long procedures moved to `references/`.
- Scripts document prerequisites and error handling.
- `README.md` skill list updated when adding/removing skills.
