---
name: install-agent-skills
description: Deploy generated skills to system locations. Use after /generate-agent-skills to install skills.
---

# Install Agent Skills

Deploy generated skills from `dotfiles/` to system locations.

## Usage

```
/install-agent-skills              # Install ALL skills
/install-agent-skills zod-docs     # Install only zod-docs skill
```

Run after `/generate-agent-skills`.

## How It Works

The install script:
1. Copies `SKILL.md` from `dotfiles/<agent>/skills/<skill>/`
2. Creates a symlink `references/` pointing to `dotfiles/shared/<skill>/`

This keeps the repo clean (no symlinks) while installed skills link to shared docs.

## Instructions

### Step 1: Check Arguments

Check if `$ARGUMENTS` is provided:
- If **argument provided**: Install only that specific skill
- If **no argument**: Install all skills

### Step 2: Verify skills exist

**If installing a specific skill:**
- Verify `dotfiles/shared/{argument}/` exists
- Verify `dotfiles/claude/skills/{argument}/` exists
- If not found, tell user to run `/generate-agent-skills {argument}` first

**If installing all skills:**
- Check that `dotfiles/shared/` and `dotfiles/*/skills/` contain skills
- If empty, tell user to run `/generate-agent-skills` first

### Step 3: Install skills

Use the install.sh script:

**For a specific skill:**
```bash
SKILL="{argument}"

# Claude Code
.claude/skills/install-agent-skills/scripts/install.sh "dotfiles/claude/skills/$SKILL" ~/.claude/skills

# Codex CLI
.claude/skills/install-agent-skills/scripts/install.sh "dotfiles/codex/skills/$SKILL" ~/.codex/skills

# OpenCode
.claude/skills/install-agent-skills/scripts/install.sh "dotfiles/opencode/skills/$SKILL" ~/.config/opencode/skills
```

**For all skills:**
```bash
# Claude Code skills -> ~/.claude/skills/
for skill in dotfiles/claude/skills/*/; do
  .claude/skills/install-agent-skills/scripts/install.sh "$skill" ~/.claude/skills
done

# Codex skills -> ~/.codex/skills/
for skill in dotfiles/codex/skills/*/; do
  .claude/skills/install-agent-skills/scripts/install.sh "$skill" ~/.codex/skills
done

# OpenCode skills -> ~/.config/opencode/skills/
for skill in dotfiles/opencode/skills/*/; do
  .claude/skills/install-agent-skills/scripts/install.sh "$skill" ~/.config/opencode/skills
done
```

### Step 4: Report results

Summarize skills installed per agent.

## Standalone Usage

```bash
# Default: symlink mode (references/ links to shared docs)
.claude/skills/install-agent-skills/scripts/install.sh dotfiles/claude/skills/codex-docs ~/.claude/skills

# Copy mode: copies docs, creates standalone skill
.claude/skills/install-agent-skills/scripts/install.sh dotfiles/claude/skills/codex-docs ~/.claude/skills --copy
```

## Installed Structure

After installation, each skill in `~/.claude/skills/` (or equivalent) contains:
- `SKILL.md` - Agent-specific skill definition
- `references/` - Symlink to `<repo>/dotfiles/shared/<docs>/`

Updates to `dotfiles/shared/` are immediately reflected in all installed skills.
