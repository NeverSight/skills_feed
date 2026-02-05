---
name: techdebt
description: "Technical debt detection and remediation. Run at session end to find duplicated code, dead imports, security issues, and complexity hotspots. Triggers: 'find tech debt', 'scan for issues', 'check code quality', 'wrap up session', 'ready to commit', 'before merge', 'code review prep'. Always uses parallel subagents for fast analysis."
---

# Tech Debt Scanner

Automated technical debt detection using parallel subagents. Designed to run at session end to catch issues while context is fresh.

## Quick Start

```bash
# Session end - scan changes since last commit (default)
/techdebt

# Deep scan - analyze entire codebase
/techdebt --deep

# Specific categories
/techdebt --duplicates    # Only duplication
/techdebt --security      # Only security issues
/techdebt --complexity    # Only complexity hotspots
/techdebt --deadcode      # Only dead code

# Auto-fix mode (interactive)
/techdebt --fix
```

## Architecture

**Always uses parallel subagents** for fast analysis:

```
Main Agent (orchestrator)
    │
    ├─> Subagent 1: Duplication Scanner
    ├─> Subagent 2: Security Scanner
    ├─> Subagent 3: Complexity Scanner
    └─> Subagent 4: Dead Code Scanner

    ↓ All run in parallel (2-15s depending on scope)

Main Agent: Consolidate findings → Rank by severity → Generate report
```

**Benefits:**
- 🚀 Parallel execution - all scans run simultaneously
- 🧹 Clean main context - no pollution from analysis work
- 💪 Scalable - handles large codebases efficiently
- 🎯 Fast - even small diffs benefit from parallelization

## Workflow

### Step 1: Determine Scope

**Default (no flags):**
- Scan files changed since last commit: `git diff --name-only HEAD`
- Fast session-end workflow (~2-3 seconds)
- Perfect for "wrap up" scenarios

**Deep scan (`--deep` flag):**
- Scan entire codebase
- Comprehensive analysis (~10-15 seconds for medium projects)
- Use when refactoring or preparing major releases

**Specific category (e.g., `--duplicates`):**
- Run only specified scanner
- Fastest option for targeted analysis

### Step 2: Spawn Parallel Subagents

Launch 4 subagents simultaneously (or subset if category specified):

**Subagent 1: Duplication Scanner**
- Task: Find duplicated code blocks using AST similarity
- Tools: `ast-grep`, structural search, token analysis
- Output: List of duplicate code blocks with similarity scores

**Subagent 2: Security Scanner**
- Task: Detect security vulnerabilities and anti-patterns
- Checks: Hardcoded secrets, SQL injection, XSS, insecure crypto
- Output: Security findings with severity and remediation guidance

**Subagent 3: Complexity Scanner**
- Task: Identify overly complex functions and methods
- Metrics: Cyclomatic complexity, nested depth, function length
- Output: Complexity hotspots with refactoring suggestions

**Subagent 4: Dead Code Scanner**
- Task: Find unused imports, variables, and unreachable code
- Checks: Unused imports, dead branches, orphaned functions
- Output: Dead code list with safe removal instructions

**Subagent instructions template:**
```
Scan {scope} for {category} issues.

Scope: {file_list or "entire codebase"}
Language: {detected from file extensions}
Focus: {category-specific patterns}

Output format:
- File path + line number
- Issue description
- Severity (P0-P3)
- Suggested fix (if available)

Use appropriate tools:
- Duplication: ast-grep for structural similarity
- Security: pattern matching + known vulnerability patterns
- Complexity: cyclomatic complexity calculation
- Dead Code: static analysis for unused symbols
```

### Step 3: Consolidate Findings

Main agent collects results from all subagents and:

1. **Deduplicate** - Remove duplicate findings across categories
2. **Rank by severity:**
   - **P0 (Critical):** Security vulnerabilities, blocking issues
   - **P1 (High):** Major duplication, high complexity
   - **P2 (Medium):** Minor duplication, moderate complexity
   - **P3 (Low):** Dead code, style issues
3. **Group by file** - Organize findings by affected file
4. **Calculate debt score** - Overall technical debt metric

### Step 4: Generate Report

Create actionable report with:

```markdown
# Tech Debt Report

**Scope:** {X files changed | Entire codebase}
**Scan Time:** {duration}
**Debt Score:** {0-100, lower is better}

## Summary

| Category | Findings | P0 | P1 | P2 | P3 |
|----------|----------|----|----|----|----|
| Duplication | X | - | X | X | - |
| Security | X | X | - | - | - |
| Complexity | X | - | X | X | - |
| Dead Code | X | - | - | X | X |

## Critical Issues (P0)

### {file_path}:{line}
**Category:** {Security}
**Issue:** Hardcoded API key detected
**Impact:** Credential exposure risk
**Fix:** Move to environment variable

## High Priority (P1)

### {file_path}:{line}
**Category:** {Duplication}
**Issue:** 45-line block duplicated across 3 files
**Impact:** Maintenance burden, inconsistency risk
**Fix:** Extract to shared utility function

[... continue for all findings ...]

## Recommendations

1. Address all P0 issues before merge
2. Consider refactoring high-complexity functions
3. Remove dead code to reduce maintenance burden

## Auto-Fix Available

Run `/techdebt --fix` to interactively apply safe automated fixes.
```

### Step 5: Auto-Fix Mode (Optional)

If `--fix` flag provided:

1. **Identify safe fixes:**
   - Dead import removal (safe)
   - Simple duplication extraction (review required)
   - Formatting fixes (safe)

2. **Interactive prompts:**
   ```
   Fix: Remove unused import 'requests' from utils.py:5
   [Y]es / [N]o / [A]ll / [Q]uit
   ```

3. **Apply changes:**
   - Edit files with confirmed fixes
   - Show git diff of changes
   - Prompt for commit

**Safety rules:**
- Never auto-fix security issues (require manual review)
- Never auto-fix complexity (requires design decisions)
- Only auto-fix with explicit user confirmation

## Detection Patterns

### Duplication

**AST Similarity Detection:**
- Use `ast-grep` for structural pattern matching
- Detect code blocks with >80% structural similarity
- Ignore trivial differences (variable names, whitespace)

**Token-based Analysis:**
- Compare token sequences for exact duplicates
- Minimum threshold: 6 consecutive lines
- Group similar duplicates across files

**Thresholds:**
- P1: 30+ lines duplicated in 3+ locations
- P2: 15+ lines duplicated in 2+ locations
- P3: 6+ lines duplicated in 2 locations

### Security

**Pattern Detection:**

| Pattern | Severity | Example |
|---------|----------|---------|
| Hardcoded secrets | P0 | `API_KEY = "sk-..."` |
| SQL injection risk | P0 | `f"SELECT * FROM users WHERE id={user_id}"` |
| Insecure crypto | P0 | `hashlib.md5()`, `random.random()` for tokens |
| Path traversal | P0 | `open(user_input)` without validation |
| XSS vulnerability | P0 | Unescaped user input in HTML |
| Eval/exec usage | P1 | `eval(user_input)` |
| Weak passwords | P2 | Hardcoded default passwords |

**Language-specific checks:**
- Python: `pickle` usage, `yaml.load()` without SafeLoader
- JavaScript: `eval()`, `innerHTML` with user data
- SQL: String concatenation in queries

### Complexity

**Metrics:**

| Metric | P1 Threshold | P2 Threshold |
|--------|--------------|--------------|
| Cyclomatic Complexity | >15 | >10 |
| Function Length | >100 lines | >50 lines |
| Nested Depth | >5 levels | >4 levels |
| Number of Parameters | >7 | >5 |

**Refactoring suggestions:**
- Extract method for long functions
- Introduce parameter object for many parameters
- Simplify conditionals with guard clauses
- Break up deeply nested logic

### Dead Code

**Detection methods:**
- Unused imports (language-specific linters)
- Unreachable code (after return/break/continue)
- Unused variables (written but never read)
- Orphaned functions (never called in codebase)

**Safe removal criteria:**
- No external references found
- Not part of public API
- Not dynamically imported/called

## Language Support

**Tier 1 (Full support):**
- Python: `ast-grep`, `radon`, `pylint`
- JavaScript/TypeScript: `ast-grep`, `eslint`, `jscpd`
- Go: `gocyclo`, `golangci-lint`
- Rust: `clippy`, `cargo-audit`

**Tier 2 (Basic support):**
- Java, C#, Ruby, PHP: Pattern-based detection only

**Language detection:**
- Auto-detect from file extensions
- Use appropriate tools per language
- Fallback to universal patterns if specific tools unavailable

## Integration Patterns

### Session End Automation

Add to your workflow:

```markdown
## Session Wrap-Up Checklist

- [ ] Run `/techdebt` to scan changes
- [ ] Address any P0 issues found
- [ ] Create tasks for P1/P2 items
- [ ] Commit clean code
```

### Pre-Commit Hook

Create `.claude/hooks/pre-commit.sh`:

```bash
#!/bin/bash
# Auto-run tech debt scan before commits

echo "🔍 Scanning for tech debt..."
claude skill techdebt --quiet

if [ $? -eq 1 ]; then
  echo "❌ P0 issues detected. Fix before committing."
  exit 1
fi

echo "✅ No critical issues found"
```

### CI/CD Integration

Run deep scan on pull requests:

```yaml
# .github/workflows/techdebt.yml
name: Tech Debt Check
on: [pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tech debt scan
        run: claude skill techdebt --deep --ci
```

## Advanced Usage

### Baseline Tracking

Track debt over time:

```bash
# Initial baseline
/techdebt --deep --save-baseline

# Compare against baseline
/techdebt --compare-baseline
# Output: "Debt increased by 15% since baseline"
```

Baseline stored in `.claude/techdebt-baseline.json`:

```json
{
  "timestamp": "2026-02-03T10:00:00Z",
  "commit": "a28f0fb",
  "score": 42,
  "findings": {
    "duplication": 8,
    "security": 0,
    "complexity": 12,
    "deadcode": 5
  }
}
```

### Custom Patterns

Add project-specific patterns in `.claude/techdebt-rules.json`:

```json
{
  "security": [
    {
      "pattern": "TODO.*security",
      "severity": "P0",
      "message": "Security TODO must be resolved"
    }
  ],
  "complexity": {
    "cyclomatic_threshold": 12,
    "function_length_threshold": 80
  }
}
```

### Report Formats

```bash
/techdebt --format=json     # JSON output for tooling
/techdebt --format=markdown # Markdown report (default)
/techdebt --format=sarif    # SARIF for IDE integration
```

## Troubleshooting

**Issue: Scan times out**
- Solution: Use `--deep` only on smaller modules, or increase timeout
- Consider: Break large codebases into smaller scan chunks

**Issue: Too many false positives**
- Solution: Adjust thresholds in `.claude/techdebt-rules.json`
- Consider: Use `--ignore-patterns` flag to exclude test files

**Issue: Missing dependencies (ast-grep, etc.)**
- Solution: Install tools via `npm install -g @ast-grep/cli` or skip category
- Fallback: Pattern-based detection still works without specialized tools

## Best Practices

1. **Run at every session end** - Catch debt while context is fresh
2. **Address P0 immediately** - Don't commit critical issues
3. **Create tasks for P1/P2** - Track technical debt in backlog
4. **Use baselines for trends** - Monitor debt accumulation over time
5. **Automate in CI/CD** - Prevent debt from merging
6. **Educate team** - Share findings, discuss refactoring strategies

## References

See also:
- [Anthropic's Agent Skills](https://github.com/anthropics/skills) - Subagent patterns
- [references/patterns.md](references/patterns.md) - Language-specific debt patterns
- [references/severity-guide.md](references/severity-guide.md) - How to rank findings
