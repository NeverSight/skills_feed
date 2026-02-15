---
name: explore-codebase
description: Use when navigating unfamiliar code or understanding architecture, tracing call flows or symbol definitions, answering where-is-this-defined or how-does-this-work questions, finding files by name or pattern, or doing pre-refactoring analysis to locate all references before changing code
context: fork
user-invocable: true
model: opus
allowed-tools:
  - Bash(ast-grep:*)
  - Bash(sg:*)
  - Bash(rg:*)
  - Bash(fd:*)
---

# Explore Codebase

## Tool Selection

| Need                                       | Tool              |
| ------------------------------------------ | ----------------- |
| Structural patterns (functions, classes)   | `sg` (ast-grep)   |
| Text/regex patterns (strings, names)       | `rg` (ripgrep)    |
| File discovery by name/extension           | `fd`              |

**Decision flow**: Find files first? `fd` → pipe to `rg`/`sg`. Syntax-aware match needed? `sg`. Fast text search? `rg`. Uncertain? Start with `rg`, escalate to `sg` if structure matters.

## ast-grep Essentials

ast-grep is the least familiar tool -- key syntax summarized here. See [references/ast-grep.md](references/ast-grep.md) for language-specific patterns and YAML rule files.

```bash
sg -p 'PATTERN' -l LANG [PATH]
sg -p 'PATTERN' --has 'INNER' -l LANG       # Must contain
sg -p 'PATTERN' --not-has 'INNER' -l LANG   # Must not contain
sg -p 'PATTERN' --inside 'OUTER' -l LANG    # Must be within
```

### Metavariables

| Syntax   | Captures              | Example                              |
| -------- | --------------------- | ------------------------------------ |
| `$VAR`   | Single node           | `console.log($MSG)`                  |
| `$$$VAR` | Zero or more nodes    | `function($$$ARGS)` -- any arity     |
| `$_`     | Non-capturing         | `$_FUNC($_)` -- match without capture |

Rules: must be UPPERCASE, same name = same content (`$A == $A` matches `x == x` not `x == y`).

### Examples

```bash
sg -p 'function $NAME($$$ARGS) { $$$ }' -l js
sg -p 'async function $NAME($$$) { $$$ }' --has 'await $EXPR' -l js
sg -p 'class $NAME extends $PARENT { $$$ }' -l ts
sg -p 'def $NAME($$$): $$$' -l py
```

## ripgrep / fd Quick Reference

Standard CLI tools -- use [references/ripgrep.md](references/ripgrep.md) and [references/fd.md](references/fd.md) for full flag tables.

```bash
rg PATTERN -t TYPE [PATH]         # Search by file type
rg -F 'LITERAL' -t TYPE           # Fixed string (no regex)
rg PATTERN -l                     # List matching files only
rg PATTERN -C 3                   # With context lines

fd -e EXT [PATH]                  # Find by extension
fd PATTERN [PATH]                 # Find by name regex
fd -e py | xargs rg 'pattern'    # Pipe fd into rg
```

## Performance

- Narrow scope first: `fd -e py src/ | xargs rg 'class.*Test'`
- Always use type filters: `rg PATTERN -t rust`, `sg -p 'PATTERN' -l rs`
- Exclude artifacts: `rg PATTERN -g '!node_modules' -g '!dist'`
