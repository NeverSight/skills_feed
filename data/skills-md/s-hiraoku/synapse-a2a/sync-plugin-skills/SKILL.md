---
name: sync-plugin-skills
description: This skill synchronizes plugin skills (plugins/synapse-a2a/skills/) with the current implementation, README.md, and guides folder. Use this skill when implementation changes have been made, new features added, or documentation updated, to ensure plugin skills stay up-to-date. Triggered by /sync-plugin-skills command or when significant code changes are detected.
---

# Sync Plugin Skills

Synchronize plugin skills with the current implementation and documentation.

## Purpose

Ensure that skills in `plugins/synapse-a2a/skills/` accurately reflect:
- Current implementation in `synapse/` directory
- README.md documentation
- Guides in `guides/` folder

## When to Use

- After implementing new features or parameters
- After updating README.md or guides
- Before releasing a new version
- When `/sync-plugin-skills` is invoked

## Workflow

### Step 1: Gather Current State

Read the following files to understand current implementation and documentation:

1. **Implementation**: Key files in `synapse/`
   - `synapse/tools/a2a.py` - CLI tool implementation
   - `synapse/a2a_client.py` - A2A client
   - `synapse/cli.py` - Main CLI entry point
   - `synapse/commands/*.py` - Command implementations

2. **Documentation**:
   - `README.md` - Main documentation
   - `guides/usage.md` - Usage guide
   - `guides/settings.md` - Settings documentation
   - `guides/delegation.md` - Delegation guide

3. **Current Skills**:
   - `plugins/synapse-a2a/skills/synapse-a2a/SKILL.md`
   - `plugins/synapse-a2a/skills/synapse-a2a/references/*.md`
   - `plugins/synapse-a2a/skills/delegation/SKILL.md`
   - `plugins/synapse-a2a/skills/delegation/references/*.md`

### Step 2: Identify Gaps

Compare and identify:
- New CLI options/parameters not documented in skills
- Changed command syntax or behavior
- New features mentioned in README but missing from skills
- Deprecated or removed features still in skills
- Endpoint path inconsistencies

### Step 3: Update Skills

Update skill files to match current state:

**synapse-a2a/SKILL.md**:
- Quick Reference table
- Command examples
- Feature descriptions

**synapse-a2a/references/commands.md**:
- Full CLI command documentation
- All options and parameters
- Example usage

**synapse-a2a/references/api.md**:
- Endpoint paths
- Request/response formats
- Extension endpoints

**delegation/SKILL.md**:
- Delegation patterns
- Command examples

**delegation/references/modes.md**:
- Communication methods
- A2A patterns

### Step 4: Verify Consistency

Ensure consistency across:
- Endpoint paths match between README and skills
- Command syntax is identical
- Option names and defaults match implementation
- Examples use correct syntax

## Key Areas to Check

### Command Options

```bash
# Check synapse/tools/a2a.py for current options
synapse send <target> <message> [options]
```

Key options to verify:
- `--from` / `-f`: Sender identification
- `--priority` / `-p`: Priority levels (1-5)
- `--response` / `--no-response`: Roundtrip control
- `--reply-to`: Reply to specific task

### API Endpoints

```
/.well-known/agent.json    # Agent Card
/tasks/send                # Standard A2A
/tasks/send-priority       # Synapse extension
/tasks/{id}                # Task status
/status                    # Agent status
```

### Settings Commands

```bash
synapse init               # Initialize .synapse/
synapse config             # Interactive TUI
synapse config show        # View settings
synapse reset              # Reset to defaults
```

## Output

After synchronization, report:
1. Files that were updated
2. Specific changes made
3. Any manual review needed

## Notes

- Preserve skill file structure (YAML frontmatter + markdown)
- Keep descriptions concise and actionable
- Use imperative form for instructions
- Avoid duplicating content between SKILL.md and references/
