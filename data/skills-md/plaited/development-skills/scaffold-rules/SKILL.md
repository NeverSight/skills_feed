---
name: scaffold-rules
description: Scaffold development rules for AI coding agents. Auto-invoked when user asks about setting up rules, coding conventions, or configuring their AI agent environment.
license: ISC
compatibility: Requires bun
allowed-tools: Bash
---

# Scaffold Rules

Scaffold shared development rules for AI coding agent environments.

## When to Use

Use when the user wants to:
- Set up development rules or coding conventions
- Configure their AI coding agent environment
- Add project guidelines for Claude, Cursor, or other agents

## Workflow

### Step 1: Preview Changes (Optional)

```bash
bunx @plaited/development-skills scaffold-rules --dry-run
```

Review the `actions` array to see what will be created.

### Step 2: Run Scaffold

```bash
bunx @plaited/development-skills scaffold-rules
```

This will:
1. Copy rules to `.agents/rules/` (canonical location)
2. Create symlinks in `.claude/rules` and `.cursor/rules` (if those directories exist)
3. Fallback: append links to `AGENTS.md` if no agent directories found

### Step 3: Report to User

Tell the user what was created based on the `actions` output.

## CLI Options

| Flag | Description |
|------|-------------|
| `--list`, `-l` | List available rules without scaffolding |
| `--dry-run`, `-n` | Preview actions without making changes |

## How It Works

```
.agents/rules/          ← Canonical location (files copied here)
    ├── testing.md
    ├── bun.md
    └── ...

.claude/rules -> ../.agents/rules   ← Symlink (if .claude/ exists)
.cursor/rules -> ../.agents/rules   ← Symlink (if .cursor/ exists)
```

| Project has... | Copy | Symlinks | AGENTS.md |
|----------------|------|----------|-----------|
| `.agents/` only | ✓ | None | No |
| `.claude/` only | ✓ | `.claude/rules` | No |
| `.cursor/` only | ✓ | `.cursor/rules` | No |
| `.agents/` + `.claude/` | ✓ | `.claude/rules` | No |
| `.agents/` + `.cursor/` | ✓ | `.cursor/rules` | No |
| `.agents/` + `.claude/` + `.cursor/` | ✓ | Both | No |
| None of the above | ✓ | None | ✓ Append links |

## Related Skills

- **validate-skill** - Validate skill directories against AgentSkills spec
