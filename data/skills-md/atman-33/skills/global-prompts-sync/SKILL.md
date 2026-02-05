---
name: global-prompts-sync
description: Synchronizes prompt files (agents, rules, commands) from the skill's prompts directory to both GitHub Copilot and OpenCode global configuration directories. Use when the user wants to update their AI editor prompt libraries.
---

# Global Prompts Sync

## Overview

This skill synchronizes prompt files from the `prompts/` directory to both GitHub Copilot and OpenCode global configuration directories:

- **agents**: Agent definition files
- **rules**: Instruction/rules files
- **commands**: Command prompt files

## Directory Structure

```
global-prompts-sync/
├── SKILL.md
├── scripts/
│   └── sync_prompts.py
└── prompts/
    ├── agents/       # Agent files (*.agent.md for Copilot, *.md for OpenCode)
    ├── rules/        # Instruction files (*.instructions.md for Copilot, merged into AGENTS.md for OpenCode)
    └── commands/     # Command files (*.prompt.md for Copilot, *.md for OpenCode)
```

## Target Directories

### GitHub Copilot

All files are synced to:
- Windows: `/mnt/c/Users/<USERNAME>/AppData/Roaming/Code/User/prompts`
- File naming conventions:
  - agents: `*.agent.md`
  - rules: `*.instructions.md`
  - commands: `*.prompt.md`

### OpenCode

Files are synced to separate directories:
- agents: `~/.config/opencode/agent/` or `/mnt/c/Users/<USERNAME>/.config/opencode/agent/`
- rules: `~/.config/opencode/AGENTS.md` (merged from all rules files, front matter removed)
- commands: `~/.config/opencode/command/` or `/mnt/c/Users/<USERNAME>/.config/opencode/command/`

## Usage

To synchronize prompts to both GitHub Copilot and OpenCode:

```python
python3 {path}/scripts/sync_prompts.py
```

The script will:
1. Detect the environment (WSL/Windows)
2. Determine the Windows username
3. Sync agents, rules, and commands to GitHub Copilot directories
4. Sync agents, rules (merged), and commands to OpenCode directories
5. Handle file naming conventions for each editor
6. Report the status of each operation

## Options

Run with specific targets:

```bash
# Sync to GitHub Copilot only
python3 scripts/sync_prompts.py --target copilot

# Sync to OpenCode only
python3 scripts/sync_prompts.py --target opencode

# Sync to both (default)
python3 scripts/sync_prompts.py
```

## Adding Prompts

1. **Agents**: Add `.md` files to `prompts/agents/`
2. **Rules**: Add `.md` files to `prompts/rules/`
3. **Commands**: Add `.md` files to `prompts/commands/`

The script will automatically handle naming conventions for each target editor.

## Special Rules Processing

For OpenCode, multiple rule files are merged into a single `AGENTS.md` file:
- Front matter (YAML) is removed from each file
- Files are concatenated in alphabetical order
- A single `AGENTS.md` is created in OpenCode's config directory
