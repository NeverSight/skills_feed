---
name: parsearger-utils
description: Utilities for parseArger. Use this skill for PROJECT scaffolding, DOCUMENTATION generation, COMPLETION scripts, and HTML FORMS.
license: MIT
compatibility: Requires parseArger executable.
---

# ParseArger Utilities

This skill provides tools for managing full projects, generating documentation, bash completion, and web forms.

## Invocation Rules

1. Check `which parseArger` → if found, use `parseArger`
2. Fallback: `./parseArger` (in project root)
3. Never assume location - always check first

---

## 1. Project Scaffolding (`project`)

Create a full directory structure for a new CLI tool, including subcommands, tests, and documentation support.

```bash
parseArger project NAME [OPTIONS]
```

**Options:**
- `--description "DESC"`: Project description.
- `--project-subcommand "NAME"`: Create specific subcommands (repeatable).
- `--directory "DIR"`: Output directory (default `./NAME`).
- `--git-repo "USER/REPO"`: Set git repository URL.
- `--installer-git-service "HOST"`: Git host (default `github.com`).
- `--no-readme`: Skip README generation.
- `--no-git`: Skip `git init`.

#### Example: Full CLI Tool Setup

```bash
# Create a complex tool with multiple subcommands
parseArger project mdd \
  --description "Markdown tools for my blog" \
  --git-repo "DimitriGilbert/mdd" \
  --project-subcommand article \
  --project-subcommand build \
  --project-subcommand deploy
```

This generates:
- `mdd/bin/article` (and others)
- `mdd/mdd.rc` (source this to setup aliases)
- `mdd/documentation.md`
- `mdd/completely.yaml`

---

## 2. Bash Completion (`completely`)

Generate bash completion scripts and configuration using `completely` library.

```bash
parseArger completely COMMAND-NAME SCRIPT-FILE [OPTIONS]
```

**Dependency**: Requires the `completely` Ruby gem OR Docker installation. Use `--completely-cmd` to specify a custom command (e.g., via Docker).

**Options:**
- `--subcommand-directory "DIR"`: Scan directory for subcommands to include in completion.
- `--completion-file "FILE"`: Output bash script (default `completely.bash`).
- `--yaml-file "FILE"`: Output intermediate YAML config (default `completely.yaml`).
- `--run-completely`: Run the generator (default on). Use `--no-run-completely` to only output YAML.
- `--completely-cmd "CMD"`: Custom command to run `completely` (e.g. via Docker).

#### Example

```bash
parseArger completely my-tool ./bin/my-tool --subcommand-directory ./bin
```

---

## 3. Documentation (`document`)

Generate Markdown documentation from argument definitions.

```bash
parseArger document [OPTIONS]
```

**Options:**
- `--file "FILE"`: File to document (repeatable).
- `--directory "DIR"`: Document all scripts in directory (repeatable).
- `--out "FILE"`: Output file (stdout if omitted).
- `--append-output`: Append to existing file (default on).
- `--title "TITLE"`: Main title (default "Usage").
- `--tag "##"`: Markdown tag level.

#### Example

```bash
parseArger document --directory ./bin --out DOCUMENTATION.md
```

---

## 4. HTML Forms (`html-form`)

Generate a standalone HTML form that maps to the CLI arguments. Useful for web interfaces.

**Output**: Generates an HTML file you can open in a browser. The form lets users interactively build command-line arguments.

```bash
parseArger html-form FILE [OPTIONS]
```

**Options:**
- `--out "FILE"`: Output HTML file.
- `--command "CMD"`: The command string to build (defaults to filename).
- `--action "URL"`: Form action URL.
- `--js` / `--no-js`: Generate JavaScript for dynamic command building (default on).
- **Styling (Bootstrap defaults):**
  - `--form-class`, `--input-class`, `--label-class`
  - `--checkbox-class`, `--select-class`, etc.

#### Example

```bash
parseArger html-form ./bin/my-script --out form.html
```

---

## 5. Bulk Parse (`bulk-parse`)

Perform operations on multiple files at once.

```bash
parseArger bulk-parse [OPTIONS]
```

**Options:**
- `--file "FILE"`, `--directory "DIR"`.
- `--bump "VERSION"`: Bump version number across all files.

#### Examples

```bash
# Bump version to 2.0.0 across multiple specific files
parseArger bulk-parse --file bin/script1.sh --file bin/script2.sh --bump "2.0.0"

# Bump version across all scripts in a directory
parseArger bulk-parse --directory ./bin --bump "1.5.0"

# Bump version across multiple directories
parseArger bulk-parse --directory ./bin --directory ./scripts --bump "3.0.0"
```
