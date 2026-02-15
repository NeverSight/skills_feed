---
name: ast-grep
description: Searches code by AST patterns and performs structural refactoring across files. Use when finding function calls, replacing code patterns, or refactoring syntax that regex cannot reliably match.
---

# ast-grep

Structural code search and rewriting using AST matching.

## Pattern Syntax

| Pattern  | Description                                                 |
| -------- | ----------------------------------------------------------- |
| `$VAR`   | Match a single AST node and capture it as `VAR`             |
| `$$$VAR` | Match zero or more AST nodes (spread) and capture as `VAR`  |
| `$_`     | Anonymous placeholder (matches any single node, no capture) |
| `$$$_`   | Anonymous spread placeholder (matches any number of nodes)  |

**Shell quoting:** Escape `$` as `\$VAR` or wrap in single quotes.

## Supported Languages

javascript, typescript, tsx, html, css, python, go, rust, java, c, cpp, csharp, ruby, php, yaml

## Commands

| Command         | Description                          |
| --------------- | ------------------------------------ |
| `ast-grep run`  | One-time search or rewrite (default) |
| `ast-grep scan` | Scan and rewrite by configuration    |
| `ast-grep test` | Test ast-grep rules                  |
| `ast-grep new`  | Create new project or rules          |

## Search Examples

```bash
# Find console.log calls
ast-grep run --pattern 'console.log($$$ARGS)' --lang javascript .

# Find React useState hooks
ast-grep run --pattern 'const [$STATE, $SETTER] = useState($INIT)' --lang tsx .

# Find async functions
ast-grep run --pattern 'async function $NAME($$$ARGS) { $$$BODY }' --lang typescript .

# Find Express route handlers
ast-grep run --pattern 'app.$METHOD($PATH, ($$$ARGS) => { $$$BODY })' --lang javascript .

# Find Python function definitions
ast-grep run --pattern 'def $NAME($$$ARGS): $$$BODY' --lang python .

# Find Go error handling
ast-grep run --pattern 'if $ERR != nil { $$$BODY }' --lang go .

# Find all function calls
ast-grep run --pattern '$FUNCTION($$$_)' --lang typescript .

# Find specific function calls
ast-grep run --pattern 'fetch($$$_)' --lang typescript .

# Find try-catch blocks
ast-grep run --pattern 'try { $$$BODY } catch ($$$_)' --lang typescript .

# Find Promise error handling
ast-grep run --pattern '.catch($$$_)' --lang typescript .
```

## Search and Replace (Dry Run)

```bash
# Replace == with ===
ast-grep run --pattern '$A == $B' --rewrite '$A === $B' --lang javascript .

# Replace != with !==
ast-grep run --pattern '$A != $B' --rewrite '$A !== $B' --lang typescript .

# Convert function to arrow function
ast-grep run --pattern 'function $NAME($$$ARGS) { $$$BODY }' \
  --rewrite 'const $NAME = ($$$ARGS) => { $$$BODY }' --lang javascript .

# Replace var with let
ast-grep run --pattern 'var $NAME = $VALUE' --rewrite 'let $NAME = $VALUE' --lang javascript .

# Add optional chaining
ast-grep run --pattern '$OBJ && $OBJ.$PROP' --rewrite '$OBJ?.$PROP' --lang javascript .

# Replace console.log with logger
ast-grep run --pattern 'console.log($$$_)' --rewrite 'logger.info($$$_)' --lang typescript .
```

## Apply Changes

```bash
# Apply changes with --update-all
ast-grep run --pattern '$A == $B' --rewrite '$A === $B' --lang javascript --update-all .
```

## Configuration-Based Rules

```yaml
# rules/my-rules.yaml
patterns:
  - pattern: "console.log($$$_)"
    rewrite: "logger.info($$$_)"
    languages: [javascript, typescript]
    message: "Use logger instead of console.log"
```

```bash
# Run custom rules
ast-grep scan --project my-rules

# Dry-run preview
ast-grep scan --project my-rules --dry-run
```

## Tips

- Use `--dry-run` to preview changes before applying
- Use `--update-all` to apply to all matching files
- Use single quotes for patterns with `$` variables
- Combine with `--verbose` for detailed matching info
