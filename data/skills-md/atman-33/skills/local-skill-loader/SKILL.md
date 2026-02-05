---
name: local-skill-loader
description: Loads (copies) a skill from a local source directory into the current project's skill library (.claude/skills). Use this when the user wants to import or copy a skill from another location on the filesystem.
---

# Local Skill Loader

## Overview

This skill enables the importing of skills from external local directories into the current project's skill structure. It copies the entire skill directory (including `SKILL.md` and resources) to `.claude/skills/<skill-name>`.

## Usage

To load a skill, execute the `load_skill.py` script.

### Command

```bash
python3 {path}/scripts/load_skill.py <source_path> [--dest-root <destination_directory>]
```

- `<source_path>`: The absolute path to the skill directory you want to copy (e.g., `/home/user/repo/skills/my-skill`).
- `--dest-root`: (Optional) The root directory where skills should be installed. Defaults to `.claude/skills`.

### Example

If the user asks to "load the daily-task-creator skill from /home/atman/.codex/skills/daily-task-creator":

```bash
python3 {path}/scripts/load_skill.py /home/atman/.codex/skills/daily-task-creator
```

This will create `.claude/skills/daily-task-creator` in the current working directory and copy the contents.
