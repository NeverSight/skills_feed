---
name: parsearger-core
description: Core functionality for parseArger. Use this skill to GENERATE new bash argument parsers or PARSE/MODIFY existing ones. Handles definition of positional arguments, flags, and options.
license: MIT
compatibility: Requires parseArger executable in the working directory or PATH.
---

# ParseArger Core Skills

## Critical Decision Tree

**Before running any command, decide:**

1. **Does the target file exist?**
   - YES → Use `parse` (modify EXISTING parseArger script)
   - NO → Use `generate` (create NEW script)

2. **Check parseArger availability:**
   - Run `parseArger` if in PATH
   - Otherwise use `./parseArger` (from project root)

## Invocation Rules

1. Check `which parseArger` → if found, use `parseArger`
2. Fallback: `./parseArger` (in project root)
3. Never assume location - always check first

## CRITICAL: Generated Code Sections

**All parseArger scripts contain generated code between:**
- `# @parseArger-parsing`
- `# @parseArger-parsing-end`

**DO NOT manually edit code between these markers.**

To modify argument parsing:
1. Edit the `# @parseArger` declarations at the top of the file
2. Run `parseArger parse FILE --inplace` to regenerate the parsing logic

The generated parsing code is regenerated every time you use `parseArger parse`.

---

## 1. Generate a NEW Parser (`generate`)

**Use when creating a NEW script that doesn't exist yet.**

### CRITICAL: Always Use `--output`

```bash
parseArger generate --output /path/to/script.sh [OPTIONS]
```

Without `--output`, output goes to stdout only.

### Core Definitions

Define arguments using specific flags. The value is a **quoted string** containing the name, description, and specific settings.

**Positional Arguments (`--pos`)**
Syntax: `--pos 'NAME "DESCRIPTION" [SETTINGS]'`

Settings:
- `--optional`: Make the argument optional.
- `--repeat`: Allow multiple values (creates an array `_arg_name`).
- `--repeat-min N`: Min repetitions (implies --repeat).
- `--repeat-max N`: Max repetitions.
- `--one-of "VAL"`: Restrict to specific values (repeatable).
- `--complete "FUNC"`: Bash built-in completion (e.g., `file`, `directory`).
- `--complete-custom "CMD"`: Custom dynamic completion command.
- `--match "REGEX"`: Validate input against a regex pattern (e.g. `^[0-9]+$`).
- `--subcommand`: Mark as a subcommand (see Subcommands below).

**Options (`--opt`)`
Syntax: `--opt 'NAME "DESCRIPTION" [SETTINGS]'`

Settings:
- `--short "C"`: Short flag character (e.g., `o`).
- `--default-value "VAL"`: Default value if not provided.
- `--repeat`: Allow multiple occurrences.
- `--alias "NAME"`: Alternative long name.
- `--empty`: Allow usage without value (acts like flag).
- `--empty-value "VAL"`: Value to set if used without value (requires `--empty`).
- `--env "VAR"`: Fallback to environment variable if option not provided.
- `--required`: Mark option as mandatory (script fails if missing).
- `--match "REGEX"`: Validate input against a regex pattern (e.g. `^[0-9]+$`).

**Flags (`--flag`)**
Syntax: `--flag 'NAME "DESCRIPTION" [SETTINGS]'`

Settings:
- `--short "C"`: Short flag character (e.g., `f`).
- `--on`: Flag is on by default (passing it turns it off).
- `--alias "NAME"`: Alias.
- `--no-name "NAME"`: Custom name for negation (e.g., `--dont-do-it`).

**Nested Options (`--nested`)**
Syntax: `--nested 'NAME "DESCRIPTION" [SETTINGS]'`
Creates an associative array for namespaced options (e.g., `--config-db value`).
Settings:
- `--one-of "KEY"`: Restrict accepted keys.
- `--complete "FUNC"`, `--complete-custom "CMD"`.

**Global Settings**
- `--help-message "MSG"`: Main help text.
- `--help-option "OPT"`: Custom help flag (default `help`).
- `--version-opt`: Enable `--version`.
- `--set-version "VER"`: Set version number.
- `--leftovers`: Enable collecting extra arguments (into `_arg_leftovers`).
- `--verbose-level N`: Default verbose level (default 0).
- `--die-fn-name "NAME"`: Rename internal die function.
- `--log-fn-name "NAME"`: Rename internal log function.

### Example: Generate a New Script

```bash
parseArger generate --output /path/to/my-script.sh \
  --pos 'filename "Input file" --complete file' \
  --opt 'output "Output file" --short o --default-value "out.txt"' \
  --flag 'force "Overwrite existing" --short f' \
  --nested 'config "Configuration namespace"' \
  --leftovers
```

### Using Generated Variables

```bash
# Variables follow pattern $_arg_<name> (hyphens -> underscores)
echo "File: $_arg_filename"
echo "Output: $_arg_output"
if [ "$_arg_force" == "on" ]; then echo "Forcing..."; fi

# Nested options are associative arrays
# CLI: --config-db sqlite
echo "DB: ${_arg_config[db]}"
```

---

## 2. Parse/Modify EXISTING File (`parse`)

**Use when the file EXISTS and was created with `parseArger`.**

```bash
parseArger parse FILE [OPTIONS]
```

### Common Options

- `-i` or `--inplace`: Modify the file directly (RECOMMENDED).
- `--pos`, `--opt`, `--flag`: Add *new* arguments to the existing ones.
- `--set-version "VER"`: Update the version.

### Example: Modify Existing Script

```bash
# Add a new verbose flag to an existing script
parseArger parse my-script.sh --inplace \
  --flag 'verbose "Enable verbose logging" --short v'
```

**CRITICAL**: Only use `parse` on files that:
- Already exist
- Contain `# @parseArger` comments
- Were created with parseArger

---

## 3. Subcommands

To create a subcommand structure:
1. Define a positional argument with `--subcommand`.
2. Use `--subcommand-directory "DIR"` to point to a directory of scripts.
3. `parseArger` will treat files in that directory as subcommands.

Example:
```bash
parseArger generate --output /path/to/main.sh \
  --pos 'action "What to do" --subcommand --subcommand-directory ./bin'
```

Specific Subcommand Settings:
- `--subcommand-directory "DIR"`: Auto-populate valid values from scripts in DIR.
- `--subcommand-run`: Immediately execute the subcommand script found.
- `--subcommand-use-leftovers`: Pass any leftover arguments to the subcommand.
- `--subcommand-variable "VAR"`: Store subcommand parts in a specific variable (default `__subcommand`).

---

## Quick Reference: generate vs parse

| Scenario | Command | Key Options |
|----------|---------|-------------|
| Create new script | `generate` | `--output PATH` (REQUIRED) |
| Modify existing script | `parse` | `--inplace` (RECOMMENDED) |
| Add arguments to existing | `parse` | `--pos`, `--opt`, `--flag` |
| Update version | `parse` | `--set-version` |
