---
name: umple-diagram-generator
description: Use this skill when user asks to generate state machine or class diagram with umple.
allowed-tools: Bash(npx -y bun:*), Bash(command -v umple:*), Bash(umple --help:*), Bash(umple:*), Bash(mktemp:*), Bash(mkdir:*), Bash(cat:*), Bash(ls:*), Bash(cp:*), Bash(command -v dot:*), Bash(dot:*), Bash(date:*)
---

# Umple Diagram Generator Skill

## Overview

Generates UML diagrams from natural-language requirements using Umple CLI.

### Supported Diagram Types & Guidance

| Diagram Type | Umple Generator | Guidance File | When to Use |
|--------------|-----------------|---------------|-------------|
| State Machine | `GvStateDiagram` | `references/state-machine-guidance.md` | User requests state machine diagram |
| Class Diagram | `GvClassDiagram` | `references/class-diagram-guidance.md` | User requests class diagram |
| Unsupported | - | - | Inform user it's not yet supported |

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/main.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

## Quick Start

```bash
# Folder mode: organized output with all files (.ump, .gv, .svg)
npx -y bun ${SKILL_DIR}/scripts/main.ts --input model.ump --output ./diagrams --name "light-controller"

# Exact path mode: save SVG to specific file path
npx -y bun ${SKILL_DIR}/scripts/main.ts --input model.ump --output ./my-diagram.svg

# Class diagram with custom name
npx -y bun ${SKILL_DIR}/scripts/main.ts --input model.ump --output ./diagrams --name "user-system" --type class-diagram
```

### Script Options

| Option | Description |
|--------|-------------|
| `-i, --input <path>` | Input `.ump` file (required) |
| `-o, --output <path>` | Output path: directory for folder mode, or `.svg` file for exact path (required) |
| `-n, --name <name>` | Diagram name for folder mode (optional, triggers folder mode) |
| `-t, --type <type>` | Diagram type: `state-machine` (default), `class-diagram` |
| `-s, --suboption <opt>` | GvStateDiagram suboption (repeatable) |
| `--json` | JSON output with details |
| `-h, --help` | Show help |

### Output Modes

**Folder Mode** (when `--name` is specified or `--output` is a directory):
- Creates organized folder with timestamped name
- Includes all files: `.ump` (source), `.gv` (graphviz), `.svg` (diagram)

**Folder naming**:
- With `--name`: `<sanitized-name>_<timestamp>/`
- Without `--name`: `<diagram-type>_<timestamp>/`

**Example**:
```
diagrams/
└── light-controller_20260121_183045/
    ├── model.ump
    ├── model.gv
    └── model.svg
```

**Exact Path Mode** (when `--output` ends with `.svg`):
- Saves only the SVG file to the exact specified path
- Useful when user specifies a specific output location

**Example**:
```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts --input model.ump --output /path/to/my-diagram.svg
# Result: /path/to/my-diagram.svg (only SVG, no folder created)
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Missing dependencies (umple or dot) |
| 2 | Umple validation/compilation failed |
| 3 | SVG generation failed or unsupported diagram type |

## Pre-flight checks (must do before running Umple)

### Dependencies

| Dependency | Check Command | Installation | Required |
|------------|---------------|--------------|----------|
| Umple CLI | `command -v umple` | [Download](https://cruise.umple.org/umpleonline/download_umple.shtml) | Yes |
| Graphviz | `command -v dot` | `brew install graphviz` | Yes |

If dependencies are missing, stop and inform the user.

## Workflow (do this every time)

### Step 1 — Clarify only what you must

If ambiguous, propose your plan and ask minimal clarifying questions:

| Diagram Type | Key Questions |
|--------------|---------------|
| State Machine | Initial state? Events? Final states? Guards/actions? |
| Class Diagram | Main entities? Attributes? Relationships? Multiplicities? |

### Step 2 — Write the Umple model

**Critical**: Read the appropriate guidance file from the table above before writing code.

### Step 3 — Determine output path and generate the diagram

**Agent should choose the appropriate mode**:
- **Folder mode** (recommended): Use when generating for user review/documentation
- **Exact path mode**: Use only when user explicitly specifies a file path

**Folder mode example**:

```bash
tmpdir="$(mktemp -d)"
cat >"$tmpdir/model.ump" <<'EOF'
// (generated Umple goes here)
EOF

npx -y bun ${SKILL_DIR}/scripts/main.ts --input "$tmpdir/model.ump" --output <output-dir> --name "<meaningful-name>" --type [state-machine|class-diagram]
```

**Folder naming guidelines**:
- Use `--name` with a descriptive name derived from user requirements (e.g., "user-authentication", "order-workflow")
- If no clear name from requirements, omit `--name` to use auto-generated name
- The script automatically adds timestamp to prevent conflicts

**Exact path mode example** (when user specifies):

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts --input "$tmpdir/model.ump" --output /path/specified/by/user.svg --type [state-machine|class-diagram]
```

### Step 4 — Validate output correctness

Check exit code (see table above). If non-zero, read error output, fix Umple, and retry up to 3 times.

## Repair loop (required)

On each failure:
1. Identify the root cause from script output (syntax error, unknown state, missing semicolon, etc.).
2. Apply a focused fix to the Umple model.
3. Re-run: `npx -y bun ${SKILL_DIR}/scripts/main.ts --input "$tmpdir/model.ump" --output <output-dir> --name "<name>" --type [state-machine|class-diagram]`

## Output contract

1. Specify which diagram type was generated.
2. Show the generated Umple code (single `umple` code block).
3. Confirm the exact command you ran.
4. **Folder mode**: Provide the output folder path and SVG file location.
   **Exact path mode**: Provide the SVG file path.
