---
name: setup
description: >
  Install behavioral skills from trousse. Use FIRST when onboarding a new machine
  or after fresh Claude Code install. Creates symlinks for session lifecycle, utilities,
  and optionally offers tool repos (todoist-gtd, garde-manger).
  Triggers on 'help me set up', 'install skills', '/setup'. (user)
---

# Setup

Install Claude behavioral skills with one command.

## When to Use

- Fresh Claude Code installation
- New machine setup
- After cloning trousse for the first time
- When `/open` or `/close` commands don't work

## When NOT to Use

- Skills are already installed and working
- Just want to update existing skills (use `git pull` instead)
- Installing a single skill (manually symlink it)

## Quick Start

```
/setup           # Interactive — installs all behavioral skills, offers tool repos
/setup --verify  # Check existing setup
```

## What Gets Installed

**Behavioral skills** (all installed together):
- Session lifecycle: `/open`, `/close`
- Utilities: diagram, screenshot, filing, github-cleanup, picture, server-checkup, skill-check, sprite, dbt

**Optional tool repos** (offered after core install):
- `todoist-gtd` — GTD-flavored Todoist integration
- `garde-manger` — Searchable memory across sessions

## Workflow

### Phase 1: Check Prerequisites

```bash
# Check for required tools
command -v gh &>/dev/null || echo "MISSING: GitHub CLI (brew install gh)"
command -v uv &>/dev/null || echo "MISSING: uv (brew install uv)"

# Create directories
mkdir -p ~/.claude/skills
mkdir -p ~/.claude/scripts
mkdir -p ~/.claude/hooks
```

### Phase 2: Clone and Symlink

```bash
# Clone trousse if not present
if [ ! -d ~/Repos/trousse ]; then
    gh repo clone spm1001/trousse ~/Repos/trousse
fi

SUITE="$HOME/Repos/trousse"

# Symlink all skills
for skill in "$SUITE/skills/"*/; do
    name=$(basename "$skill")
    ln -sf "$skill" ~/.claude/skills/"$name"
done
```

### Phase 3: Symlink Scripts and Hooks

```bash
# Scripts (if present)
if [ -d "$SUITE/scripts" ]; then
    for script in "$SUITE/scripts/"*.sh; do
        [ -f "$script" ] && ln -sf "$script" ~/.claude/scripts/
    done
fi

# Hooks (if present)
if [ -d "$SUITE/hooks" ]; then
    for hook in "$SUITE/hooks/"*.sh; do
        [ -f "$hook" ] && ln -sf "$hook" ~/.claude/hooks/
    done
fi
```

### Phase 4: Offer Tool Repos

Use AskUserQuestion:

```
Core skills installed. Want to add tool integrations?

[ ] todoist-gtd — GTD task management with Todoist
[ ] garde-manger — Search past sessions
```

**If todoist-gtd selected:**
```bash
gh repo clone spm1001/todoist-gtd ~/Repos/todoist-gtd
ln -sf ~/Repos/todoist-gtd/skills/todoist-gtd ~/.claude/skills/todoist-gtd

# Run OAuth
todoist auth
```

**If garde-manger selected:**
```bash
gh repo clone spm1001/garde-manger ~/Repos/garde-manger
cd ~/Repos/garde-manger && uv sync
ln -sf ~/Repos/garde-manger/skill ~/.claude/skills/garde

# Initial scan
cd ~/Repos/garde-manger && uv run garde scan
```

### Phase 5: Verify

```bash
# List installed skills
ls ~/.claude/skills/

# Test key skills
ls -la ~/.claude/skills/open
```

Tell user to restart Claude (`/exit` then `claude`) to load new skills.

## Verification

| Check | Command | Expected |
|-------|---------|----------|
| Skills directory | `ls ~/.claude/skills/` | 13+ skill symlinks |
| Session skills | `ls -la ~/.claude/skills/open` | Points to trousse |

## Updating

```bash
cd ~/Repos/trousse && git pull
# Symlinks automatically point to updated content
```

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Running setup when skills exist | Overwrites custom symlinks | Use `--verify` first |
| Skipping OAuth for todoist-gtd | Skill fails silently | Complete auth flow |
| Not restarting Claude after install | Skills not loaded | `/exit` then `claude` |
