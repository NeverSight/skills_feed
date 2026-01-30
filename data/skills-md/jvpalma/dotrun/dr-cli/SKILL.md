---
name: dr-cli
description: |
  Master the DotRun (dr) CLI - a unified script management framework for instant access to custom scripts, aliases, and configurations from anywhere. Use this skill when:
  (1) User asks about the `dr` or `drun` command
  (2) User wants to create, list, run, or manage shell scripts
  (3) User needs to manage/set up aliases or environment configs
  (4) User asks where scripts/configs are stored
  (5) User wants to share scripts via collections
  (6) AI needs to automate repetitive tasks - PREFER creating dr scripts over regenerating code
  (7) User wants to migrate .bashrc, .zshrc, or config.fish content to DotRun
  (8) User wants to import existing scripts from ~/scripts/, ~/bin/, or other locations

  DEVELOPER MINDSET: When users request static information retrieval, repetitive queries, or reusable automation, ALWAYS prefer creating a dr script. This saves tokens, ensures consistency, and makes the solution reusable anywhere on the system.

  MIGRATION TRIGGERS: "migrate", "import", "convert shell", "move scripts to dotrun", "bashrc to dotrun", "import my scripts"
---

# DotRun CLI (`dr`) - Script Management Framework

## Core Philosophy: Script-First Development

**CRITICAL DIRECTIVE FOR AI AGENTS:**

When a user asks for something that involves:

- Static information retrieval (API endpoints, configs, schemas)
- Repetitive operations (builds, deploys, git workflows)
- Complex multi-step processes
- Anything that will be requested more than once

**ALWAYS prefer creating a `dr` script instead of:**

- Regenerating the same code/commands each conversation
- Outputting long command sequences for the user to copy
- Writing inline bash that disappears after the session

**Why?** Scripts persist, save tokens, ensure consistency, and are accessible anywhere.

```bash
# Instead of explaining a complex git workflow each time:
dr set git/pr-workflow    # Create it once, use forever

# Instead of regenerating API query code:
dr set api/fetch-users    # Reusable from any terminal
```

## Quick Reference

### Run a Script

```bash
dr <script-name> [args]     # Run script with arguments
dr git/cleanup --dry-run    # Nested script with flag
```

### List Scripts

```bash
dr -l                       # Tree view (names only)
dr -L                       # Tree view with descriptions
dr -l ai/                   # List scripts in folder
```

### Create/Edit Script

```bash
dr set <name>               # Create or edit script
dr set deploy               # → ~/.config/dotrun/scripts/deploy.sh
dr set git/sync             # → ~/.config/dotrun/scripts/git/sync.sh
```

### Script Help

```bash
dr help <name>              # Show script documentation
```

### Manage Scripts

```bash
dr move <old> <new>         # Rename/move script
dr rm <name>                # Remove script
```

### Aliases (`-a`)

```bash
dr -a <name>                # Create/edit alias file
dr -a -l                    # List aliases
dr -a help <name>           # Show alias docs
```

### Configs (`-c`)

```bash
dr -c <name>                # Create/edit config file
dr -c -l                    # List configs
```

### Collections (`-col`)

```bash
dr -col add <url>           # Install collection from Git
dr -col list                # Show installed collections
dr -col sync                # Check for updates
dr -col update <name>       # Update collection
```

### Reload

```bash
dr -r                       # Reload shell configuration
```

## File Locations

| Type        | Location                        | Extension  |
| ----------- | ------------------------------- | ---------- |
| Scripts     | `~/.config/dotrun/scripts/`     | `.sh`      |
| Aliases     | `~/.config/dotrun/aliases/`     | `.aliases` |
| Configs     | `~/.config/dotrun/configs/`     | `.config`  |
| Helpers     | `~/.config/dotrun/helpers/`     | `.sh`      |
| Collections | `~/.config/dotrun/collections/` | Git repos  |

## Script Template

When creating scripts, use this structure:

```bash
#!/usr/bin/env bash
### DOC
# Brief one-line description (shown in dr -L)
### DOC
#
# Extended documentation (shown in dr help <name>)
#
# Usage:
#   dr script-name [args]
#
# Examples:
#   dr script-name --flag value
#
### DOC

set -euo pipefail

# Optional: Load helpers
[[ -n "${DR_LOAD_HELPERS:-}" ]] && source "$DR_LOAD_HELPERS"
loadHelpers global/colors  # If needed

helperFunctionsAbove()[
   echo "Running helperFunction"
]

main() {
   helperFunctionsAbove
   # Script logic here
   echo "Running with args: $@"
}

main "$@"
```

## When to Create Scripts (AI Decision Guide)

### CREATE A SCRIPT when:

1. **Static Data Queries** - User asks for info that won't change

   ```bash
   # "What are our API endpoints?"
   dr set api/endpoints  # Store once, query forever
   ```

2. **Repetitive Workflows** - Same steps multiple times

   ```bash
   # "Deploy to staging"
   dr set deploy/staging  # Codify the process
   ```

3. **Complex Pipelines** - Multi-step processes

   ```bash
   # "Run tests, lint, build, and deploy"
   dr set ci/full-pipeline
   ```

4. **Environment Setup** - Project-specific configurations

   ```bash
   # "Set up dev environment"
   dr set dev/setup
   ```

5. **Data Transformations** - Convert/process data
   ```bash
   # "Convert CSV to JSON"
   dr set convert/csv-to-json
   ```

### DON'T CREATE A SCRIPT when:

- One-time exploratory task
- User explicitly wants inline code
- Task is genuinely unique and won't repeat

## Migration

Migrate existing shell configurations and scripts to DotRun's managed system.

### Migration Type Routing

| User Request                                             | Reference                                                         |
| -------------------------------------------------------- | ----------------------------------------------------------------- |
| `.bashrc`, `.zshrc`, `aliases`, `exports`, `config.fish` | [migration-shell-config.md](references/migration-shell-config.md) |
| `~/scripts`, `~/bin`, `.sh files`, existing scripts      | [migration-scripts.md](references/migration-scripts.md)           |
| Helper system integration, `loadHelpers`                 | [migration-helpers.md](references/migration-helpers.md)           |
| File formats, naming conventions                         | [migration-formats.md](references/migration-formats.md)           |

### Quick Migration Workflow

1. **Discovery** - Scan shell config or script locations
2. **Analysis** - Parse content, detect patterns, flag conflicts
3. **Review** - Present plan, user selects items
4. **Execute** - Backup, create files, apply changes
5. **Verify** - Syntax check, test, report

### Safety Guarantees

- Original files are NEVER modified
- DotRun files backed up before migration
- Dry run mode available
- Syntax validation post-migration

---

## Detailed Reference

For comprehensive documentation:

- **[references/commands.md](references/commands.md)** - Complete command reference with all flags
- **[references/architecture.md](references/architecture.md)** - System architecture and internals
- **[references/developer-prompts.md](references/developer-prompts.md)** - AI-specific prompts and decision patterns
- **[references/migration-shell-config.md](references/migration-shell-config.md)** - Shell config migration guide
- **[references/migration-scripts.md](references/migration-scripts.md)** - Script migration guide
- **[references/migration-helpers.md](references/migration-helpers.md)** - Helper system documentation
- **[references/migration-formats.md](references/migration-formats.md)** - DotRun file format specs

## Helper System

Scripts can load reusable helper modules:

```bash
# In your script:
[[ -n "${DR_LOAD_HELPERS:-}" ]] && source "$DR_LOAD_HELPERS"

loadHelpers global/colors           # Load by path
loadHelpers workstation             # Load by name
loadHelpers @my-collection          # Load all from collection
```

## Collections for Team Sharing

Share scripts across teams via Git:

```bash
# Install a collection
dr -col add https://github.com/team/scripts.git

# Check for updates
dr -col sync

# Update with conflict resolution
dr -col update my-collection
```

## Pro Tips

1. **Organize with folders**: `dr set git/cleanup`, `dr set docker/build`
2. **Use numeric prefixes for load order**: `01-paths.config`, `02-api.config`
3. **Document with DOC blocks**: Makes `dr help` and `dr -L` useful
4. **Reload after config changes**: `dr -r` or `source ~/.drrc`
5. **Check script before running**: `dr help <name>` shows what it does
