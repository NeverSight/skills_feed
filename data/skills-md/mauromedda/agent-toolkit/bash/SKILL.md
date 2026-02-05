---
name: bash
description: >-
  Guide for writing production-quality bash scripts following modern idiomatic practices.
  Enforces set -euo pipefail, [[ ]] conditionals, ${var} syntax, ShellCheck compliance.
  Triggers on "bash script", "shell script", ".sh file", "write a script", "automation script",
  "bash function", "shellcheck", "bash template", "pre-commit hook", "deploy script",
  "build script", "install script", "setup script", "bash error handling", "bash arrays",
  "bash loop", "bash conditional", "parse arguments", "getopts", "bash logging",
  "#!/bin/bash", "source script", "dot script", "shell function",
  "edit script", "update script", "modify script", "change script",
  "edit .sh", "update .sh", "modify .sh", "statusline.sh", "hook script".
  PROACTIVE: MUST invoke BEFORE editing/writing ANY .sh file or pre-commit hook.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ABOUTME: Bash scripting skill for production-quality scripts with Bash 4.x+
# ABOUTME: Emphasizes safety, readability, maintainability, and mandatory ShellCheck compliance

# Bash Scripting Skill

**Target**: Bash 4.0+ with mandatory ShellCheck compliance.

**Detailed patterns**: See `references/script-template.md` and `references/advanced-patterns.md`

---

## 🛑 FILE OPERATION CHECKPOINT (BLOCKING)

**Before EVERY `Write` or `Edit` tool call on a `.sh` file or shell script:**

```
╔══════════════════════════════════════════════════════════════════╗
║  🛑 STOP - BASH SKILL CHECK                                      ║
║                                                                  ║
║  You are about to modify a shell script.                         ║
║                                                                  ║
║  QUESTION: Is /bash skill currently active?                      ║
║                                                                  ║
║  If YES → Proceed with the edit                                  ║
║  If NO  → STOP! Invoke /bash FIRST, then edit                    ║
║                                                                  ║
║  This check applies to:                                          ║
║  ✗ Write tool with file_path ending in .sh                       ║
║  ✗ Edit tool with file_path ending in .sh                        ║
║  ✗ Files named "pre-commit", "post-commit", etc. (git hooks)     ║
║  ✗ ANY shell script, regardless of conversation topic            ║
║                                                                  ║
║  Examples that REQUIRE this skill:                               ║
║  - "update the statusline" (edits statusline.sh)                 ║
║  - "add a feature to the hook" (edits pre-commit)                ║
║  - "fix the deploy script" (edits deploy.sh)                     ║
╚══════════════════════════════════════════════════════════════════╝
```

**Why this matters:** Shell scripts without proper safety headers (`set -euo pipefail`)
can fail silently or cause data corruption. The skill ensures ShellCheck compliance.

---

## Quick Reference

| Pattern | Use | Avoid |
|---------|-----|-------|
| Conditionals | `[[ "${var}" == "x" ]]` | `[ $var == "x" ]` |
| Variables | `"${var}"` (quoted) | `$var` (unquoted) |
| Command sub | `$(command)` | `` `command` `` |
| Arithmetic | `(( count++ ))` | `let count++` |
| Error handling | `set -euo pipefail` | No safety flags |

---

## When to Use Bash

**USE for** (< 200 lines):
- Quick automation tasks
- Build/deployment scripts
- System administration
- Glue code between tools

**DON'T USE for**:
- Complex business logic
- Robust error handling with recovery
- Long-running services
- Code requiring unit testing

If script exceeds ~200 lines, consider Python or Go.

---

## 🔄 RESUMED SESSION CHECKPOINT

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION RESUMED - BASH SKILL VERIFICATION                  │
│                                                             │
│  Before continuing:                                         │
│  1. Does script have set -euo pipefail?                     │
│  2. Are all variables quoted: "${var}"?                     │
│  3. Using [[ ]] conditionals (not [ ])?                     │
│  4. Run: shellcheck <script>.sh                             │
│  5. Re-invoke /bash if skill context was lost               │
└─────────────────────────────────────────────────────────────┘
```

---

## Mandatory Header

Every script MUST start with:

```bash
#!/bin/bash
set -euo pipefail

# -e: Exit on error
# -u: Error on unset variables
# -o pipefail: Pipeline fails on first error
```

---

## Core Syntax Rules

### Conditionals (Always `[[ ]]`)

```bash
if [[ "${var}" =~ ^[0-9]+$ ]]; then
    echo "Numeric"
fi

if [[ -f "${file}" && -r "${file}" ]]; then
    echo "File exists and readable"
fi
```

### Variable Expansion (Always quoted)

```bash
echo "Value: ${config_path}"
echo "Array: ${my_array[@]}"
```

### Command Substitution

```bash
current_date=$(date +"%Y-%m-%d")
file_count=$(find . -type f | wc -l)
```

### Arithmetic

```bash
(( count++ ))
(( total = value1 + value2 ))
if (( count > 10 )); then
    echo "Exceeded"
fi
```

---

## Error Handling Patterns

### Pattern 1: Need output AND status

```bash
output=$(complex_command 2>&1)
rc=$?
if [[ ${rc} -ne 0 ]]; then
    log_error "Failed: ${output}"
    return 1
fi
```

### Pattern 2: Status check only

```bash
if ! simple_command --flag; then
    die "Command failed"
fi

# Or short form
simple_command || die "Failed"
```

---

## Essential Functions

```bash
# Logging
log_info()  { echo "[INFO] $(date +%H:%M:%S) ${*}" >&2; }
log_error() { echo "[ERROR] $(date +%H:%M:%S) ${*}" >&2; }
die()       { log_error "${*}"; exit 1; }

# Validation
validate_file() {
    local -r f="${1}"
    [[ -f "${f}" ]] || die "Not found: ${f}"
    [[ -r "${f}" ]] || die "Not readable: ${f}"
}

# Cleanup
cleanup() {
    [[ -d "${TEMP_DIR:-}" ]] && rm -rf "${TEMP_DIR}"
}
trap cleanup EXIT
```

---

## Argument Parsing

```bash
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "${1}" in
            -h|--help)    help; exit 0 ;;
            -v|--verbose) VERBOSE=true; shift ;;
            -f|--file)
                [[ -z "${2:-}" ]] && die "-f requires argument"
                FILE="${2}"; shift 2
                ;;
            -*)           die "Unknown: ${1}" ;;
            *)            break ;;
        esac
    done
    ARGS=("${@}")
}
```

---

## ShellCheck Compliance

**All scripts MUST pass ShellCheck with zero warnings.**

### Common Fixes

| Warning | Fix |
|---------|-----|
| SC2086: Quote to prevent globbing | `rm "${file}"` not `rm $file` |
| SC2155: Declare separately | `local x; x=$(cmd)` not `local x=$(cmd)` |
| SC1090: Can't follow source | `# shellcheck source=/dev/null` |
| SC2046: Quote command sub | Use `while read` instead of `for x in $(cmd)` |

### Run ShellCheck

```bash
shellcheck script.sh
shellcheck -s bash script.sh
find . -name "*.sh" -exec shellcheck {} +
```

---

## Arrays Quick Reference

### Indexed Arrays

```bash
declare -a files=()
files+=("item")
for f in "${files[@]}"; do echo "${f}"; done
echo "Count: ${#files[@]}"
```

### Associative Arrays (Bash 4+)

```bash
declare -A config=()
config["key"]="value"
for k in "${!config[@]}"; do echo "${k}=${config[${k}]}"; done
```

---

## Security Rules

1. **Never use `eval`**
2. **Sanitize all inputs**
3. **Use absolute paths** for system commands
4. **Use `readonly`** for constants
5. **Don't store secrets** in scripts

---

## Checklist

Before script is complete:

- [ ] `set -euo pipefail` at top
- [ ] All variables use `"${var}"` syntax
- [ ] Uses `[[ ]]` for conditionals
- [ ] Uses `$(command)` for substitution
- [ ] ShellCheck passes (zero warnings)
- [ ] Has `help()` function
- [ ] Has cleanup trap
- [ ] Variables properly scoped (local/readonly)
- [ ] **If > 100 lines**: Has bats tests

---

## Full Template

See `references/script-template.md` for complete production script template.

## Advanced Patterns

See `references/advanced-patterns.md` for:
- Arrays and associative arrays
- String manipulation
- Parallel processing
- Progress indicators
- Input validation
- bats-core testing
