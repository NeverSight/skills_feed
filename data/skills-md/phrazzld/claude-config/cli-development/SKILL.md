---
name: cli-development
description: |
  Command-line tool development patterns, conventions, and toolchain. Use when:
  - Building CLI applications
  - Designing command interfaces  
  - Choosing CLI frameworks (Commander.js, oclif, Ink, Cobra, Thor)
  - Implementing help and error messages
  - Following Unix conventions
  Keywords: CLI, command line, terminal, help text, exit codes,
  flags, arguments, Commander, Thor, Cobra, oclif
---

# CLI Development

Verb-noun commands, progressive disclosure, helpful errors.

## Command Structure

**Verb-noun pattern:**
```
tool create project
tool deploy app
tool logs get
tool config set key value
```

**Max 2 levels deep. Use common verbs:** create, delete, list, show, update, get, set.

## Flags

```
-h, --help         Always support both
-v, --verbose      Increase output detail
-f, --force        Skip confirmations
-o, --output json  Format specifier
--dry-run          Show what would happen
```

**Boolean flags don't take values. Value flags use space or `=`.**

## Help Text

```
USAGE
  tool deploy <app> [flags]

DESCRIPTION
  Deploy an application to the specified environment.

FLAGS
  -e, --env string    Target environment (default: "staging")
  -f, --force         Skip confirmation prompt
  --dry-run           Show what would be deployed

EXAMPLES
  # Deploy to staging
  tool deploy my-app

  # Deploy to production with confirmation bypass
  tool deploy my-app --env production --force

SEE ALSO
  tool deploy logs    View deployment logs
  tool deploy status  Check deployment status
```

## Error Messages

```
Error: Configuration file not found

The file 'config.yaml' does not exist in the current directory.

To fix this:
  1. Run 'tool init' to create a new config file
  2. Or specify a path with --config /path/to/config.yaml

See 'tool init --help' for more information.
```

**Include:** what went wrong, context, specific fix, help reference.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse (invalid arguments) |
| 126 | Not executable |
| 127 | Command not found |

## Output

**Human-readable by default, machine-readable on request:**
```bash
tool list users              # Pretty table
tool list users --format json  # JSON output
tool list users -o yaml        # YAML output
```

## Progressive Disclosure

- Simple commands with sensible defaults
- Advanced options available but not prominent
- Help organized by experience level
- Discovery through `--help` and suggestions

## Anti-Patterns

- Cryptic abbreviations (`-x` without long form)
- Stack traces in user output
- Silent failures (no output on error)
- Required flags for common cases
- Deep command hierarchies (>2 levels)
- Inconsistent verbs across commands

## Toolchain

See `references/toolchain.md` for framework-specific guidance:
- **Commander.js** (default for Node.js)
- **oclif** (enterprise CLIs)
- **Ink** (React for terminals)
- **Cobra** (Go CLIs)
- **Thor** (Ruby CLIs)
