---
name: ubs
description: Ultimate Bug Scanner - scan code for bugs across 7 languages (JS/TS, Python, Go, Rust, Java, C++, Ruby). Use before commits to catch null safety issues, security holes, async bugs, and memory leaks.
---

# UBS - Ultimate Bug Scanner

Fast static analysis that catches real bugs across multiple languages in seconds.

## Prerequisites

Install UBS:
```bash
curl -sSL https://raw.githubusercontent.com/Dicklesworthstone/ultimate_bug_scanner/main/install.sh | bash
```

Dependencies (auto-detected):
- `rg` (ripgrep) - Pattern matching
- `ast-grep` - AST analysis
- `jq` - JSON processing

## CLI Reference

### Basic Scanning
```bash
# Scan specific files (fastest, <1s)
ubs file.ts file2.py

# Scan directory
ubs src/

# Scan current directory
ubs .

# Scan staged files (pre-commit)
ubs --staged

# Scan modified files (working tree vs HEAD)
ubs --diff
```

### Output Formats
```bash
# Text (default)
ubs src/

# JSON
ubs src/ --format=json

# JSONL (streaming)
ubs src/ --format=jsonl

# SARIF (for CI integration)
ubs src/ --format=sarif
```

### Strictness Modes
```bash
# Strict - fail on warnings
ubs src/ --fail-on-warning
ubs src/ --ci --fail-on-warning

# CI mode
ubs src/ --ci

# Quiet (summary only)
ubs src/ -q
```

### Language Filtering
```bash
# Only specific languages (3-5x faster)
ubs src/ --only=js,python
ubs src/ --only=typescript,rust
ubs src/ --only=go,java
```

### Category Filtering
```bash
# Focus on specific category packs
ubs src/ --category=resource-lifecycle
```

### Verbose Mode
```bash
# Show more code examples per finding
ubs src/ --verbose
```

### Baseline Comparison
```bash
# Save baseline
ubs src/ --format=json > baseline.json

# Compare against baseline (detect regressions)
ubs src/ --comparison=baseline.json

# Generate reports
ubs src/ --comparison=baseline.json --report-json=report.json --html-report=report.html
```

### Doctor/Health Check
```bash
# Check installation and dependencies
ubs doctor
```

### View Session Logs
```bash
# Tail latest session log
ubs sessions --entries 1
```

## Output Format

```
Warning/Error: Category (N errors)
    file.ts:42:5 - Issue description
    Suggested fix
Exit code: 1
```

Parse format:
- `file:line:col` - Location
- `Suggested fix` - How to fix
- Exit 0/1 - Pass/fail

## Bug Categories Detected

### Critical (Always Fix)
- Null/undefined safety issues
- XSS and injection vulnerabilities
- async/await problems
- Memory leaks
- Use-after-free

### Important (Production)
- Type narrowing issues
- Division by zero risks
- Resource leaks (unclosed handles)
- Race conditions

### Contextual (Use Judgment)
- TODO/FIXME comments
- Console.log statements
- Dead code

## Workflow Patterns

### Pre-Commit Hook
```bash
# In .git/hooks/pre-commit
#!/bin/bash
ubs --staged --fail-on-warning || exit 1
```

### CI Pipeline
```bash
# Strict mode for CI
ubs . --ci --fail-on-warning
```

### Quick Check During Development
```bash
# Scan just the file you're working on
ubs src/component.tsx

# Scan modified files
ubs --diff
```

### Fixing Findings

1. Read the finding (category + description)
2. Navigate to `file:line:col`
3. View context
4. Verify it's a real issue (not false positive)
5. Fix the root cause, not symptom
6. Re-run `ubs <file>` to verify
7. Exit code 0 = fixed

## Speed Tips

- **Scope to changed files** - `ubs src/file.ts` (<1s) vs `ubs .` (30s)
- **Use language filter** - `--only=js,python` for 3-5x speedup
- **Never full scan for small edits** - Always scope to modified files

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Ignore findings | Investigate each |
| Full scan per edit | Scope to changed files |
| Fix symptom (`if (x) { x.y }`) | Fix root cause (`x?.y`) |
| Add suppression comments | Fix the actual issue |

## Best Practices

1. **Run before every commit** - `ubs --staged`
2. **Exit 0 = safe to commit** - Exit >0 = fix and re-run
3. **Trust the suggestions** - They point to real issues
4. **Fix root cause** - Don't just silence the warning
5. **Use in CI** - Catch regressions before merge
