---
name: cli-patterns
description: "Patterns for building production-quality CLI tools with predictable behavior, parseable output, and agentic workflows. Triggers: cli tool, command line tool, build cli, cli patterns, agentic cli, cli design, typer cli, click cli."
compatibility: "Python 3.11+, Typer, Click"
allowed-tools: "Read, Write, Edit"
depends-on: []
related-skills: [python-cli-patterns, python-async-patterns]
---

# CLI Patterns for Agentic Workflows

Patterns for building CLI tools that AI assistants and power users can chain, parse, and rely on.

## Philosophy

Build CLIs for **agentic workflows** - AI assistants and power users who chain commands, parse output programmatically, and expect predictable behavior.

### Core Principles

| Principle | Meaning | Why It Matters |
|-----------|---------|----------------|
| **Self-documenting** | `--help` is comprehensive and always current | LLMs discover capabilities without external docs |
| **Predictable** | Same patterns across all commands | Learn once, use everywhere |
| **Composable** | Unix philosophy - do one thing well | Tools chain together naturally |
| **Parseable** | `--json` always available, always valid | Machine consumption without parsing hacks |
| **Quiet by default** | Data only, no decoration unless requested | Scripts don't break on unexpected output |
| **Fail fast** | Invalid input = immediate error | No silent failures or partial results |

### Design Axioms

1. **stdout is sacred** - Only data. Never progress, never logging, never decoration.
2. **stderr is for humans** - Progress bars, colors, tables, warnings live here.
3. **Exit codes have meaning** - Scripts can branch on failure mode.
4. **Help includes examples** - The fastest path to understanding.
5. **JSON shape is predictable** - Same structure across all commands.

---

## Command Architecture

### Structural Pattern

```
<tool> [global-options] <resource> <action> [options] [arguments]
```

Every CLI follows this hierarchy:

```
<tool>
├── --version, --help              # Global flags
├── auth                           # Authentication (if required)
│   ├── login
│   ├── status
│   └── logout
└── <resource>                     # Domain resources (plural nouns)
    ├── list                       # Get many
    ├── get <id>                   # Get one by ID
    ├── create                     # Make new (if supported)
    ├── update <id>                # Modify existing (if supported)
    ├── delete <id>                # Remove (if supported)
    └── <custom-action>            # Domain-specific verbs
```

### Naming Conventions

| Element | Convention | Valid Examples | Invalid Examples |
|---------|------------|----------------|------------------|
| Tool name | lowercase, 2-12 chars | `mytool`, `datactl` | `MyTool`, `my-tool-cli` |
| Resource | plural noun, lowercase | `invoices`, `users` | `Invoice`, `user` |
| Action | verb, lowercase | `list`, `get`, `sync` | `listing`, `getter` |
| Long flags | kebab-case | `--dry-run`, `--output-format` | `--dryRun`, `--output_format` |
| Short flags | single letter | `-n`, `-q`, `-v` | `-num`, `-quiet` |

### Standard Resource Actions

| Action | HTTP Equiv | Returns | Idempotent |
|--------|------------|---------|------------|
| `list` | GET /resources | Array | Yes |
| `get <id>` | GET /resources/:id | Object | Yes |
| `create` | POST /resources | Created object | No |
| `update <id>` | PATCH /resources/:id | Updated object | Yes |
| `delete <id>` | DELETE /resources/:id | Confirmation | Yes |
| `search` | GET /resources?q= | Array | Yes |

---

## Flags & Options

### Mandatory Flags

Every command MUST support:

| Flag | Short | Behavior | Output |
|------|-------|----------|--------|
| `--help` | `-h` | Show help with examples | Help text to stdout, exit 0 |
| `--json` | | Machine-readable output | JSON to stdout |

Root command MUST additionally support:

| Flag | Short | Behavior | Output |
|------|-------|----------|--------|
| `--version` | `-V` | Show version | `<tool> <version>` to stdout, exit 0 |

### Recommended Flags

| Flag | Short | Type | Purpose | Default |
|------|-------|------|---------|---------|
| `--quiet` | `-q` | bool | Suppress non-essential stderr | false |
| `--verbose` | `-v` | bool | Increase detail level | false |
| `--dry-run` | | bool | Preview without executing | false |
| `--limit` | `-n` | int | Max results to return | 20 |
| `--output` | `-o` | path | Write output to file | stdout |
| `--format` | `-f` | enum | Output format | varies |

### Flag Behavior Rules

1. **Boolean flags take no value**: `--json` not `--json=true`
2. **Short flags can combine**: `-vq` equals `-v -q`
3. **Unknown flags are errors**: Never silently ignore
4. **Repeated flags**: Last value wins (or error if inappropriate)

---

## Output Specification

### Stream Separation

This is the most critical rule:

| Stream | Content | When |
|--------|---------|------|
| **stdout** | Data only | Always |
| **stderr** | Everything else | Interactive mode |

**stdout** receives:
- JSON when `--json` is set
- Minimal text output when interactive
- Nothing else. Ever.

**stderr** receives:
- Progress indicators (spinners, bars)
- Status messages ("Fetching...", "Done")
- Warnings
- Rich formatted tables
- Colors and decoration
- Debug information (`--verbose`)

### Interactive Detection

```python
import sys

def is_interactive() -> bool:
    """True if connected to a terminal, not piped."""
    return sys.stdout.isatty() and sys.stderr.isatty()
```

| Context | stdout.isatty() | Behavior |
|---------|-----------------|----------|
| Terminal | True | Rich output to stderr, summary to stdout |
| Piped (`\| jq`) | False | Minimal/JSON to stdout |
| Redirected (`> file`) | False | Minimal to stdout |
| `--json` flag | Any | JSON to stdout, suppress stderr noise |

### JSON Output Schema

See [references/json-schemas.md](references/json-schemas.md) for complete JSON response patterns.

**Key conventions:**
- List responses: `{"data": [...], "meta": {...}}`
- Single item: `{"data": {...}}`
- Errors: `{"error": {"code": "...", "message": "..."}}`
- ISO 8601 dates, decimal money, string IDs

---

## Exit Codes

Semantic exit codes that scripts can rely on:

| Code | Name | Meaning | When |
|------|------|---------|------|
| 0 | SUCCESS | Operation completed | Everything worked |
| 1 | ERROR | General/unknown error | Unexpected failures |
| 2 | AUTH_REQUIRED | Not authenticated | No token, token expired |
| 3 | NOT_FOUND | Resource missing | ID doesn't exist |
| 4 | VALIDATION | Invalid input | Bad arguments, failed validation |
| 5 | FORBIDDEN | Permission denied | Authenticated but not authorized |
| 6 | RATE_LIMITED | Too many requests | API throttling |
| 7 | CONFLICT | State conflict | Concurrent modification, duplicate |

### Usage

```bash
# Script can branch on exit code
mytool items get item-001 --json
case $? in
  0) echo "Success" ;;
  2) echo "Need to authenticate" && mytool auth login ;;
  3) echo "Item not found" ;;
  *) echo "Error occurred" ;;
esac
```

### Implementation

```python
# Constants
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_AUTH_REQUIRED = 2
EXIT_NOT_FOUND = 3
EXIT_VALIDATION = 4
EXIT_FORBIDDEN = 5
EXIT_RATE_LIMITED = 6
EXIT_CONFLICT = 7

# Usage
raise typer.Exit(EXIT_NOT_FOUND)
```

---

## Error Handling

### Error Output Format

With `--json`, errors output structured JSON to stdout AND a message to stderr:

**stderr:**
```
Error: Item not found
```

**stdout:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Item not found",
    "details": {
      "item_id": "bad-id"
    }
  }
}
```

### Error Codes

| Code | Exit | Meaning |
|------|------|---------|
| `AUTH_REQUIRED` | 2 | Must authenticate first |
| `TOKEN_EXPIRED` | 2 | Token needs refresh |
| `FORBIDDEN` | 5 | Insufficient permissions |
| `NOT_FOUND` | 3 | Resource doesn't exist |
| `VALIDATION_ERROR` | 4 | Invalid input |
| `INVALID_ARGUMENT` | 4 | Bad argument value |
| `MISSING_ARGUMENT` | 4 | Required argument missing |
| `RATE_LIMITED` | 6 | Too many requests |
| `CONFLICT` | 7 | State conflict |
| `ALREADY_EXISTS` | 7 | Duplicate resource |
| `INTERNAL_ERROR` | 1 | Unexpected error |
| `API_ERROR` | 1 | Upstream API failed |
| `NETWORK_ERROR` | 1 | Connection failed |

### Implementation Pattern

```python
def _error(
    message: str,
    code: str = "ERROR",
    exit_code: int = EXIT_ERROR,
    details: dict = None,
    as_json: bool = False,
):
    """Output error and exit."""
    error_obj = {"error": {"code": code, "message": message}}
    if details:
        error_obj["error"]["details"] = details

    if as_json:
        print(json.dumps(error_obj, indent=2))

    # Always print human message to stderr
    console.print(f"[red]Error:[/red] {message}")
    raise typer.Exit(exit_code)
```

---

## Help System

### Help Requirements

Every `--help` output MUST include:

1. **Brief description** (one line)
2. **Usage syntax**
3. **Options with descriptions**
4. **Examples** (critical for discovery)

### Help Format Template

```
<one-line description>

Usage: <tool> <resource> <action> [OPTIONS] [ARGS]

Arguments:
  <arg>          Description of positional argument

Options:
  -s, --status TEXT    Filter by status
  -n, --limit INTEGER  Max results [default: 20]
  --json               Output as JSON
  -h, --help           Show this help

Examples:
  <tool> <resource> <action>
  <tool> <resource> <action> --status active
  <tool> <resource> <action> --json | jq '.[0]'
```

### Examples Are Critical

Examples should show:
1. **Basic usage** - Simplest invocation
2. **Common filters** - Most-used options
3. **JSON piping** - How to chain with `jq`
4. **Real-world scenarios** - Actual use cases

---

## Authentication

### Auth Commands

Tools requiring authentication MUST implement:

```
<tool> auth login      # Interactive authentication
<tool> auth status     # Check current state
<tool> auth logout     # Clear credentials
```

### Credential Storage Priority

**Recommended:** OS keyring with fallbacks for maximum security

1. **Environment variable** (CI/CD, testing)
   - `MYTOOL_API_TOKEN` or similar
   - Highest priority, overrides all other sources

2. **OS Keyring** (primary storage - secure)
   - Windows: Credential Manager
   - macOS: Keychain
   - Linux: Secret Service (GNOME Keyring, KWallet)
   - Encrypted at rest, per-user isolation

3. **.env file** (development fallback)
   - Plain text in current directory
   - Convenient for local development
   - Must be in `.gitignore`

**Dependencies:**
```toml
dependencies = [
    "keyring>=24.0.0",      # OS keyring access
    "python-dotenv>=1.0.0", # .env file support
]
```

**Simple alternative:** Just config file in `~/.config/<tool>/`
- Good for tools without sensitive credentials
- Or when OS keyring adds too much complexity

See [references/implementation.md](references/implementation.md) for complete credential storage implementations.

### Unauthenticated Behavior

When auth is required but missing:

```bash
$ mytool items list
Error: Not authenticated. Run: mytool auth login
# exit code: 2
```

```bash
$ mytool items list --json
# stderr: Error: Not authenticated. Run: mytool auth login
{"error": {"code": "AUTH_REQUIRED", "message": "Not authenticated. Run: mytool auth login"}}
# exit code: 2
```

---

## Data Conventions

### Date Handling

**Input (Flexible):** Accept multiple formats for user convenience

| Format | Example | Interpretation |
|--------|---------|----------------|
| ISO date | `2025-01-15` | Exact date |
| ISO datetime | `2025-01-15T10:30:00Z` | Exact datetime |
| Relative | `today`, `yesterday`, `tomorrow` | Current/previous/next day |
| Relative | `last`, `this` (with context) | Previous/current period |

**Output (Strict):** Always output ISO 8601

```json
{
  "created_at": "2025-01-15T10:30:00Z",
  "due_date": "2025-02-15",
  "month": "2025-01"
}
```

### Money

- Store as decimal number, not cents
- Include currency when ambiguous
- Never format (no "$" or "," in JSON)

```json
{
  "total": 1250.50,
  "currency": "USD"
}
```

### IDs

- Always strings (even if numeric)
- Preserve exact format from source

```json
{
  "id": "abc_123",
  "legacy_id": "12345"
}
```

### Enums

- UPPER_SNAKE_CASE in JSON
- Case-insensitive input

```bash
# All equivalent
--status DRAFT
--status draft
--status Draft
```

```json
{"status": "IN_PROGRESS"}
```

---

## Filtering & Pagination

### Common Filter Patterns

```bash
# By status
--status DRAFT
--status active,pending    # Multiple values

# By date range
--from 2025-01-01 --to 2025-01-31
--month 2025-01
--month last

# By related entity
--user "Alice"
--project "Project X"

# Text search
--search "keyword"
-q "keyword"

# Boolean filters
--archived
--no-archived
--include-deleted
```

### Pagination

```bash
# Limit results
--limit 50
-n 50

# Offset-based
--page 2
--offset 20

# Cursor-based
--cursor "eyJpZCI6MTIzfQ=="
--after "item_123"
```

---

## Implementation

See [references/implementation.md](references/implementation.md) for complete Python implementation templates including:

- CLI skeleton with Typer
- Client pattern with httpx
- Error handling
- Authentication flows
- Testing patterns

---

## Anti-Patterns

### ❌ Output Pollution

```bash
# BAD: Progress to stdout
$ bad-tool items list --json
Fetching items...
[{"id": "1"}]
Done!

# GOOD: Only JSON to stdout
$ good-tool items list --json
[{"id": "1"}]
```

### ❌ Interactive Prompts

```bash
# BAD: Prompts in non-interactive context
$ bad-tool items create
Enter name: _

# GOOD: Fail fast with required flags
$ good-tool items create
Error: --name is required
```

### ❌ Inconsistent Flags

```bash
# BAD: Different flags for same concept
$ tool1 list -j
$ tool2 list --format=json

# GOOD: Same flags everywhere
$ tool1 list --json
$ tool2 list --json
```

### ❌ Silent Failures

```bash
# BAD: Success exit code on failure
$ bad-tool items delete bad-id
Item not found
$ echo $?
0

# GOOD: Semantic exit code
$ good-tool items delete bad-id
Error: Item not found: bad-id
$ echo $?
3
```

---

## Quick Reference

### Must-Have Checklist

- [ ] `<tool> --version`
- [ ] `<tool> --help` with examples
- [ ] `<tool> <resource> list [--json]`
- [ ] `<tool> <resource> get <id> [--json]`
- [ ] Semantic exit codes (0, 1, 2, 3, 4, 5, 6, 7)
- [ ] Errors to stderr, data to stdout
- [ ] Valid JSON on `--json`
- [ ] Stream separation (stdout = data, stderr = UI)

### Recommended Additions

- [ ] Authentication commands (`auth login`, `auth status`, `auth logout`)
- [ ] Create/Update/Delete operations
- [ ] `--quiet` and `--verbose` modes
- [ ] `--dry-run` for mutations
- [ ] Pagination (`--limit`, `--page`)
- [ ] Filtering (status, date range, search)
- [ ] Automated tests

---

## Framework Choice

**Typer** (preferred for new tools):
- Type hints provide automatic validation
- Built-in help generation
- Rich integration for beautiful output
- Less boilerplate than Click

**Click** (acceptable for existing tools):
- Typer is built on Click (100% compatible)
- Well-structured Click code doesn't need migration
- Both must follow same output conventions

```python
# Typer (preferred)
import typer
from rich.console import Console

app = typer.Typer()
console = Console(stderr=True)  # UI to stderr

# Click (acceptable)
import click
from rich.console import Console

console = Console(stderr=True)  # Same pattern
```
