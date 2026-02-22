---
name: create-cli
description: Design CLI tools with consistent UX patterns.
---

# Create CLI

Design CLI surface area: syntax, flags, output, error handling.

## Conventions

- Long options preferred (`--from` not `-f`)
- stdout for data, stderr for progress/errors
- Exit codes: 0=success, 1=runtime error, 2=usage error
- Include `--help`, `--json`, `--quiet`
- Validate early, fail fast

## Output

- Default: human-readable tables
- `--json`: JSON output (implies quiet)
- `--quiet`: suppress progress
- Respect `NO_COLOR` env

## Errors

```
<name>: <message>
Try '<name> --help'
```

## Destructive Operations

- Confirm when stdin is TTY
- `--force` to skip confirmation
- `--dry-run` to preview

## Help Format

```
<name> - <one-line description>

USAGE
    <name> [OPTIONS] <ARGS>

OPTIONS
    --option <VALUE>    Description [default: X]
    --help              Show this help

EXAMPLES
    <name> arg1 arg2
```

---

See [references/node-js.md](references/node-js.md) - Node.js with parseArgs
See [references/python-uv.md](references/python-uv.md) - Python with uv

See [clig.dev](https://clig.dev/) for comprehensive guidelines.
