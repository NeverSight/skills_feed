---
name: skills-manager
description: Manage your agent skills - save, clone, and install skills from GitHub. Use when user wants to save/bookmark a skill, clone a skill to customize, add/install a skill, list saved skills, or install all saved skills. Triggers on "save skill", "clone skill", "add skill", "install skill", "list skills", "unsave skill", "setup skills".
license: MIT
metadata:
  author: nicmeriano
  version: "2.0.0"
---

# Skills Manager

Manage your agent skills repository. Save remote skills to a registry, clone skills to customize, or just install skills directly.

## Commands

| Command | Description |
|---------|-------------|
| `save <owner/repo> [skill]` | Bookmark a skill in your registry |
| `save <owner/repo> [skill] --install` | Bookmark + install |
| `unsave <skill-name>` | Remove a skill from registry |
| `clone <owner/repo> [skill]` | Copy a skill to your skills/ directory to customize |
| `add <owner/repo> [skill] [--global]` | Install a skill (no tracking) |
| `list` | Show all saved skills |
| `install` | Install all saved skills from registry |
| `setup [path]` | Set up your agent-skills repository |

## Configuration

Skills-manager needs to know where your agent-skills repository is located.

**Priority order:**
1. `$AGENT_SKILLS_REPO` environment variable
2. `config.json` in the skill's directory

If neither is configured, you'll be prompted to run setup.

## Setup Flow

When a user runs any command without configuration:

1. Check for `$AGENT_SKILLS_REPO` environment variable
2. Check for `config.json` in the skill's directory
3. If neither exists, prompt:
   ```
   No agent-skills repository configured.
   Would you like to create one?
   - Current directory: /path/to/current
   - Custom path: let me specify
   ```
4. Create the repository structure and save config

## Scripts

Run scripts from the skill's directory:

```bash
# Get the skill directory (where this SKILL.md is located)
SKILL_DIR="$(dirname "$0")"

# Setup
$SKILL_DIR/scripts/setup.sh [path]

# Save a skill
$SKILL_DIR/scripts/save.sh owner/repo [skill-name] [--install]

# Unsave a skill
$SKILL_DIR/scripts/unsave.sh skill-name

# Clone a skill
$SKILL_DIR/scripts/clone.sh owner/repo [skill-name]

# Add/install a skill (passthrough to npx)
$SKILL_DIR/scripts/add.sh owner/repo [skill-name] [--global]

# List saved skills
$SKILL_DIR/scripts/list.sh

# Install all saved skills
$SKILL_DIR/scripts/install.sh
```

## Registry Format

The `skills-registry.json` in your agent-skills repo:

```json
{
  "skills": {
    "react-best-practices": {
      "source": "vercel-labs/agent-skills",
      "path": "skills/react-best-practices",
      "savedAt": "2025-01-21T00:00:00Z"
    }
  }
}
```

## Repository Structure

When you run setup, this structure is created:

```
agent-skills/
├── skills-registry.json    # Your saved/bookmarked skills
├── skills/                  # Your authored + cloned skills
│   └── (cloned skills go here)
├── README.md
└── AGENTS.md
```

## Workflow Examples

**Save a skill for later:**
```
> save vercel-labs/agent-skills react-best-practices
Saved 'react-best-practices' to registry.
```

**Save and install immediately:**
```
> save vercel-labs/agent-skills react-best-practices --install
Saved 'react-best-practices' to registry.
Installing...
Done!
```

**Clone a skill to customize:**
```
> clone vercel-labs/agent-skills react-best-practices
Cloned 'react-best-practices' to your skills/ directory.
You can now modify it as your own skill.
```

**Install a skill without saving:**
```
> add vercel-labs/agent-skills react-best-practices
Installing react-best-practices...
Done! (not saved to registry)
```

**Install all saved skills (e.g., on a new machine):**
```
> install skills from registry
Installing 5 saved skills...
✓ react-best-practices
✓ typescript-patterns
✓ testing-guidelines
...
Done!
```

## For New Users

If you don't have an agent-skills repository yet, the skill will help you create one:

1. Run any command (e.g., "save a skill")
2. You'll be prompted to set up your repository
3. Choose a location (current directory or custom path)
4. The skill creates the structure and saves the config
5. Continue using the skill!
