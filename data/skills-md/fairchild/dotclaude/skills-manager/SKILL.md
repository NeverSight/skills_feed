---
name: skills-manager
description: Use when the user wants to list, search, install, remove, inspect, validate, audit,
  or update skills. Use when asking "what skills do I have", "is there a skill for X",
  "check my skills for issues", or "install a skill". Also use when checking skill health
  across agents (Claude Code, Codex, Agents CLI).
metadata:
  status: experimental
---

# Skills Manager

Unified skill lifecycle management across agents.

## Usage

```
/skills-manager                    # Quick status overview
/skills-manager list               # All skills with origin, description, agent
/skills-manager search <query>     # Search skills.sh ecosystem
/skills-manager install <source>   # Install from ecosystem or GitHub
/skills-manager remove <name>      # Remove a skill
/skills-manager inspect <name>     # Deep-read: frontmatter, scripts, structure
/skills-manager validate [path]    # Validate structure and frontmatter
/skills-manager audit              # System-wide health check
/skills-manager update             # Check and apply ecosystem updates
/skills-manager create             # Guided creation (delegates to skill-creator)
```

## Status (/skills-manager)

Quick overview of all installed skills.

```bash
bun ~/.claude/skills/skills-manager/scripts/manage.ts status
```

Shows: total count, breakdown by origin (local/ecosystem/symlink) and agent, lock file stats, validation issue count.

---

## List (/skills-manager list)

All installed skills across agents with metadata.

**Local skills:**
```bash
bun ~/.claude/skills/skills-manager/scripts/manage.ts list
```

**Ecosystem skills (via npx):**
```bash
npx skills list -g
```

Present both outputs together — local list shows origin/agent/description, ecosystem list shows remote registry state.

---

## Search (/skills-manager search <query>)

Search the skills.sh ecosystem for installable skills.

```bash
npx skills find <query>
```

Present results with name, source, and install command. If no results, suggest `npx skills find` (interactive mode) or creating a custom skill.

---

## Install (/skills-manager install <source>)

Install a skill from the ecosystem or GitHub.

```bash
npx skills add <source> -g -y
```

Source formats:
- `owner/repo@skill-name` — from skills.sh registry
- `https://github.com/owner/repo` — from GitHub directly
- Local path — for development

The `-g` flag installs globally (user-level), `-y` skips confirmation.

After install, run validate to confirm the skill is well-formed:
```bash
bun ~/.claude/skills/skills-manager/scripts/manage.ts validate ~/.agents/skills/<name>
```

---

## Remove (/skills-manager remove <name>)

Remove an installed skill.

```bash
npx skills remove <name> -g -y
```

---

## Inspect (/skills-manager inspect <name>)

Deep-read a specific skill by name.

```bash
bun ~/.claude/skills/skills-manager/scripts/manage.ts inspect <name>
```

Shows: path, origin, agent, symlink target, frontmatter fields, scripts with size and executable status, references directory listing, SKILL.md heading structure.

---

## Validate (/skills-manager validate [path])

Validate skill structure and frontmatter against the spec.

```bash
bun ~/.claude/skills/skills-manager/scripts/manage.ts validate <path>
```

Path can be:
- A single skill directory (containing SKILL.md)
- A directory of skills (e.g., `~/.claude/skills`)

### Checks performed

**Errors (blocking):**
- SKILL.md exists with valid frontmatter
- Required fields: name, description
- Name: hyphen-case, max 64 chars, no leading/trailing/consecutive hyphens
- Description: 50+ chars, max 1024 chars, no angle brackets
- No forbidden files (README.md, CHANGELOG.md, etc.)

**Warnings:**
- Non-spec frontmatter keys (origin, inspired-by, hooks, status) — suggest metadata: migration
- Unexpected keys beyond spec-allowed set
- SKILL.md over 500 lines
- Scripts not executable
- Broken internal file references

---

## Audit (/skills-manager audit)

System-wide health check across all agents.

```bash
bun ~/.claude/skills/skills-manager/scripts/manage.ts audit
```

Runs:
1. **Validation** — every skill checked against spec
2. **Symlink health** — dead symlinks flagged
3. **Lock file consistency** — lock entries with missing directories
4. **Name overlap** — same skill name across agents

Returns exit code 1 if any errors found.

---

## Update (/skills-manager update)

Check for and apply ecosystem skill updates.

**Check for updates:**
```bash
npx skills check
```

**Apply updates:**
```bash
npx skills update
```

---

## Create (/skills-manager create)

Delegates to the skill-creator skill for guided 6-step creation.

When user runs `/skills-manager create`:
1. Invoke `/skill-creator` which provides the full guided workflow
2. After creation, run validate on the new skill:
   ```bash
   bun ~/.claude/skills/skills-manager/scripts/manage.ts validate <new-skill-path>
   ```

---

## Cross-Agent Reference

| Agent | Skills Dir | Lock File |
|-------|-----------|-----------|
| Claude Code | `~/.claude/skills/` | `~/.agents/.skill-lock.json` |
| Codex | `~/.codex/skills/` | `~/.agents/.skill-lock.json` |
| Agents CLI | `~/.agents/skills/` | `~/.agents/.skill-lock.json` |

All agents share the same lock file. The `npx skills` CLI auto-detects which agents are installed and manages skills for all of them.

## Skill Conventions

- **Frontmatter**: name (hyphen-case), description (50-1024 chars), license (Apache-2.0)
- **Structure**: SKILL.md + optional scripts/, references/, assets/
- **Forbidden**: README.md, CHANGELOG.md, INSTALLATION.md, QUICK_REFERENCE.md
- **Non-spec keys**: origin, inspired-by, status, hooks — should migrate to metadata:
- **Experimental skills**: `status: experimental` in frontmatter (no directory prefix)
