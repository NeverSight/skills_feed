---
name: sync-skills
description: (hal-9000) Syncs the Skills section in CLAUDE.md and skill entries in hal_dotfiles.json with skills/ directory.
context: fork
user-invocable: true
model: haiku
allowed-tools:
  - Glob
  - Read
  - Edit
  - Bash(hal sync:*)
---

# Instructions

**IMPORTANT**: Only use this skill in `/usr/local/hal-9000`. Otherwise, abort.

1. **Discover skills**
   - Glob `skills/*/SKILL.md` in `/usr/local/hal-9000` only
   - Extract `name` and `description` from each YAML frontmatter

2. **Update `dotfiles/.claude/CLAUDE.md`** (the `## Skills` section)
   - Format: `- \`name\`: description`
   - Add new skills, remove deleted skills, update changed descriptions
   - Preserve existing entry order; append new entries at end
   - Description: one short sentence (~10 words max) saying what it does — no "Use when" triggers, no verbatim frontmatter

3. **Update `dotfiles/hal_dotfiles.json`** (the `links` array)
   - Format: `{"dest": "{{HOME}}/.claude/skills/<name>/", "src": "{{REPO_ROOT}}/skills/<name>/"}`
   - Add new skill dirs, remove entries whose `"src"` matches `{{REPO_ROOT}}/skills/*` but no longer has a matching skill
   - Preserve existing entry order; append new entries at end
   - Leave non-skill entries and `copies` array as-is

4. **Run `./bin/hal sync`**, then report what changed.
