---
name: ast-grep
description: >-
  AST-aware code search and refactoring using ast-grep (sg). Use INSTEAD of grep/ripgrep
  for searching code structure. Finds functions, classes, patterns, anti-patterns across
  Go, Python, Bash, Terraform/HCL codebases. Triggers on "ast-grep", "sg", "find function",
  "find class", "find method", "find all usages", "where is X used", "search for pattern",
  "find anti-pattern", "code smell", "refactor pattern", "structural search", "AST search",
  "find error handling", "find imports", "find decorators", "find struct", "find interface",
  "search code", "locate function", "grep for function", "find definition".
  PROACTIVE: Use for ANY code search task; prefer over grep/ripgrep for code files.
allowed-tools: Read, Bash, Glob, Grep
---

# ABOUTME: ast-grep universal guide for AST-aware code search and analysis
# ABOUTME: Provides patterns for Go, Python, Bash, Terraform/HCL; replaces grep for structural search

# ast-grep Skill

## Overview

ast-grep (sg) is the preferred tool for code search. It matches code structure, not text.

## When to Use ast-grep vs grep

| Tool | Matches | False Positives | Comments/Strings |
|------|---------|-----------------|------------------|
| grep/ripgrep | Text patterns | Many | Included |
| ast-grep | AST structure | None | Ignored |

**Use grep when:** Searching non-code files, paths, or full-text documentation.

**Use ast-grep when:** Searching code for patterns, refactoring, finding anti-patterns.

---

## Quick Reference

```bash
# Basic search
sg -p 'pattern' -l go .

# With context
sg -p 'pattern' -l python -C 3 .

# JSON output for parsing
sg -p 'pattern' -l go --json .

# Replace (dry run)
sg -p 'old_pattern' -r 'new_pattern' -l python --dry-run .

# Multiple patterns
sg scan --rule rules.yml .
```

---

## Pattern Syntax

| Syntax | Meaning | Example |
|--------|---------|---------|
| `$VAR` | Single identifier | `$func($arg)` |
| `$_` | Any single node (wildcard) | `for $_ := range $_` |
| `$$$` | Zero or more items | `func($$$)` |
| `$$` | Optional element | `func($$, $last)` |

---

## Go Patterns

### Function Definitions

```bash
# Any function
sg -p 'func $NAME($$$) $$$' -l go .

# Method on type
sg -p 'func ($RECV $TYPE) $NAME($$$) $$$' -l go .

# Function returning error
sg -p 'func $NAME($$$) ($$$, error)' -l go .

# Exported functions only
sg -p 'func [A-Z]$NAME($$$) $$$' -l go .
```

### Error Handling

```bash
# Naked error return (anti-pattern)
sg -p 'if err != nil { return err }' -l go .

# Error with context (correct)
sg -p 'if err != nil { return fmt.Errorf($$$) }' -l go .

# Ignored errors (anti-pattern)
sg -p '$_, _ := $CALL($$$)' -l go .

# errors.Is usage
sg -p 'errors.Is($ERR, $TARGET)' -l go .

# errors.As usage
sg -p 'errors.As($ERR, &$TARGET)' -l go .
```

### Concurrency Patterns

```bash
# Goroutine spawn
sg -p 'go $FUNC($$$)' -l go .

# Goroutine with anonymous function
sg -p 'go func($$$) { $$$ }($$$)' -l go .

# Channel operations
sg -p '$CH <- $VALUE' -l go .     # Send
sg -p '$VAR := <-$CH' -l go .     # Receive

# Select statement
sg -p 'select { $$$ }' -l go .

# sync.Mutex usage
sg -p '$M.Lock()' -l go .
sg -p '$M.Unlock()' -l go .

# Context cancellation
sg -p 'ctx.Done()' -l go .
```

### Struct and Interface

```bash
# Struct definition
sg -p 'type $NAME struct { $$$ }' -l go .

# Interface definition
sg -p 'type $NAME interface { $$$ }' -l go .

# Embedding
sg -p 'type $NAME struct { $EMBED; $$$ }' -l go .

# JSON tags
sg -p '`json:"$TAG"`' -l go .
```

### Common Anti-Patterns

```bash
# Global mutable state
sg -p 'var $NAME = $VALUE' -l go .

# Panic in library code
sg -p 'panic($MSG)' -l go .

# Empty interface{}
sg -p 'interface{}' -l go .

# Problematic defer (arguments evaluated immediately)
sg -p 'defer require.$FUNC(t, $CALL($$$))' -l go .

# JSON tag security issue ("-,omitempty" still allows unmarshaling)
sg -p '`json:"-,$_"`' -l go .
```

---

## Python Patterns

### Function Definitions

```bash
# Any function
sg -p 'def $NAME($$$): $$$' -l python .

# Async function
sg -p 'async def $NAME($$$): $$$' -l python .

# Method with self
sg -p 'def $NAME(self, $$$): $$$' -l python .

# Class method
sg -p '@classmethod
def $NAME(cls, $$$): $$$' -l python .
```

### Class Definitions

```bash
# Any class
sg -p 'class $NAME: $$$' -l python .

# Class with inheritance
sg -p 'class $NAME($PARENT): $$$' -l python .

# Dataclass
sg -p '@dataclass
class $NAME: $$$' -l python .

# Pydantic model
sg -p 'class $NAME(BaseModel): $$$' -l python .
```

### Error Handling

```bash
# Try/except
sg -p 'try: $$$ except $EXC: $$$' -l python .

# Bare except (anti-pattern)
sg -p 'try: $$$ except: $$$' -l python .

# Catching Exception (usually bad)
sg -p 'except Exception: $$$' -l python .

# Raise with chaining
sg -p 'raise $EXC from $CAUSE' -l python .
```

### Type Hints

```bash
# Function with return type
sg -p 'def $NAME($$$) -> $TYPE: $$$' -l python .

# Optional type
sg -p '$VAR: Optional[$TYPE]' -l python .

# Union type
sg -p '$VAR: $TYPE1 | $TYPE2' -l python .
```

### Common Anti-Patterns

```bash
# Mutable default argument
sg -p 'def $NAME($ARG=[]): $$$' -l python .
sg -p 'def $NAME($ARG={}): $$$' -l python .

# eval usage (security risk)
sg -p 'eval($$$)' -l python .

# exec usage (security risk)
sg -p 'exec($$$)' -l python .

# Using assert for validation (stripped in -O)
sg -p 'assert $COND, $MSG' -l python .

# print debugging
sg -p 'print($$$)' -l python .
```

---

## Bash Patterns

```bash
# Function definition
sg -p '$NAME() { $$$ }' -l bash .

# If statement with [[ ]]
sg -p 'if [[ $COND ]]; then $$$; fi' -l bash .

# Old-style [ ] test (anti-pattern)
sg -p 'if [ $COND ]; then $$$; fi' -l bash .

# For loop
sg -p 'for $VAR in $$$; do $$$; done' -l bash .

# Command substitution (correct)
sg -p '$($CMD)' -l bash .

# Backticks (anti-pattern)
sg -p '`$CMD`' -l bash .
```

---

## Terraform/HCL Patterns

```bash
# Resource blocks
sg -p 'resource "$TYPE" "$NAME" { $$$ }' -l hcl .

# Data blocks
sg -p 'data "$TYPE" "$NAME" { $$$ }' -l hcl .

# Variable definitions
sg -p 'variable "$NAME" { $$$ }' -l hcl .

# Output definitions
sg -p 'output "$NAME" { $$$ }' -l hcl .

# Module calls
sg -p 'module "$NAME" { $$$ }' -l hcl .

# Provider configuration
sg -p 'provider "$NAME" { $$$ }' -l hcl .

# Locals block
sg -p 'locals { $$$ }' -l hcl .
```

### Terraform Anti-Patterns

```bash
# Hardcoded secrets
sg -p 'password = "$VALUE"' -l hcl .
sg -p 'secret = "$VALUE"' -l hcl .

# Missing description on variable
sg -p 'variable "$NAME" {
  type = $TYPE
}' -l hcl .

# Using count (prefer for_each)
sg -p 'count = $VALUE' -l hcl .
```

---

## YAML Rule Files

For complex searches, use rule files:

```yaml
# rules.yml
id: naked-error-return
language: go
rule:
  kind: if_statement
  pattern: |
    if err != nil {
      return err
    }
message: "Error returned without context; wrap with fmt.Errorf"
severity: warning
---
id: ignored-error
language: go
rule:
  pattern: '$_, _ := $CALL($$$)'
message: "Error ignored; handle or explicitly document reason"
severity: error
```

Run with:

```bash
sg scan --rule rules.yml .
```

---

## Workflow: Finding Technical Debt

```bash
# Find TODOs, FIXMEs in code
sg -p '// TODO$$$' -l go .
sg -p '# TODO$$$' -l python .
sg -p '# TODO$$$' -l bash .

# Find FIXMEs
sg -p '// FIXME$$$' -l go .
sg -p '# FIXME$$$' -l python .
```

---

## Workflow: Security Audit

```bash
# SQL injection risks
sg -p 'db.Query($SQL + $VAR)' -l go .
sg -p 'cursor.execute($SQL % $VAR)' -l python .
sg -p 'cursor.execute(f"$SQL")' -l python .

# Command injection
sg -p 'exec.Command($CMD + $VAR)' -l go .
sg -p 'os.system($CMD)' -l python .
sg -p 'subprocess.call($CMD, shell=True)' -l python .

# Hardcoded credentials
sg -p 'password := "$VAL"' -l go .
sg -p 'password = "$VAL"' -l python .
sg -p 'api_key = "$VAL"' -l python .
```

---

## Workflow: Performance Analysis

```bash
# N+1 query patterns (Go)
sg -p 'for $_ := range $ITEMS {
    $DB.$METHOD($$$)
}' -l go .

# Goroutine leaks (missing done channel)
sg -p 'go func() {
    for {
        $$$
    }
}()' -l go .

# Python: list append in loop (prefer list comprehension)
sg -p 'for $VAR in $ITER:
    $LIST.append($$$)' -l python .
```

---

## Integration with Claude Code

When using Claude Code, prefer ast-grep for structural searches:

```bash
# Instead of:
grep -r "func.*error" --include="*.go" .

# Use:
sg -p 'func $NAME($$$) ($$$, error)' -l go .
```

**Benefits:**
- No false positives from comments or strings
- Matches actual code structure
- Works across renamed variables
- Provides semantic understanding

---

## Checklist

Before completing a code search task:

- [ ] Used ast-grep for structural code patterns
- [ ] Used grep/ripgrep only for non-code or full-text searches
- [ ] Applied correct language flag (-l go, -l python, etc.)
- [ ] Used metavariables ($VAR, $$$, $_) appropriately
- [ ] Considered creating a rule file for complex multi-pattern searches

---

## Resources

- [ast-grep Documentation](https://ast-grep.github.io/)
- [Pattern Playground](https://ast-grep.github.io/playground.html)
- [Rule Reference](https://ast-grep.github.io/reference/rule.html)
