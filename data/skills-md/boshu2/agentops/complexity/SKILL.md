---
name: complexity
description: 'Analyze code complexity and find refactor targets using radon/gocyclo. Triggers: "complexity", "analyze complexity", "find complex code", "refactor targets", "cyclomatic complexity", "code metrics".'
---

# Complexity Skill

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Analyze code complexity to identify refactoring targets.

## Execution Steps

Given `/complexity [path]`:

### Step 1: Determine Target

**If path provided:** Use it directly.

**If no path:** Use current directory or recent changes:
```bash
git diff --name-only HEAD~5 2>/dev/null | grep -E '\.(py|go)$' | head -10
```

### Step 2: Detect Language

```bash
# Check for Python files
ls *.py **/*.py 2>/dev/null | head -1 && echo "Python detected"

# Check for Go files
ls *.go **/*.go 2>/dev/null | head -1 && echo "Go detected"
```

### Step 3: Run Complexity Analysis

**For Python (using radon):**
```bash
# Check if radon is installed
which radon || pip install radon

# Run cyclomatic complexity
radon cc <path> -a -s

# Run maintainability index
radon mi <path> -s
```

**For Go (using gocyclo):**
```bash
# Check if gocyclo is installed
which gocyclo || go install github.com/fzipp/gocyclo/cmd/gocyclo@latest

# Run complexity analysis
gocyclo -over 10 <path>
```

### Step 4: Interpret Results

**Cyclomatic Complexity Grades:**

| Grade | CC Score | Meaning |
|-------|----------|---------|
| A | 1-5 | Low risk, simple |
| B | 6-10 | Moderate, manageable |
| C | 11-20 | High risk, complex |
| D | 21-30 | Very high risk |
| F | 31+ | Untestable, refactor now |

### Step 5: Identify Refactor Targets

List functions/methods that need attention:
- CC > 10: Should refactor
- CC > 20: Must refactor
- CC > 30: Critical, immediate action

### Step 6: Write Complexity Report

**Write to:** `.agents/complexity/YYYY-MM-DD-<target>.md`

```markdown
# Complexity Report: <Target>

**Date:** YYYY-MM-DD
**Language:** <Python/Go>
**Files Analyzed:** <count>

## Summary
- Average CC: <score>
- Highest CC: <score> in <function>
- Functions over threshold: <count>

## Refactor Targets

### Critical (CC > 20)
| Function | File | CC | Recommendation |
|----------|------|-----|----------------|
| <name> | <file:line> | <score> | <how to simplify> |

### High (CC 11-20)
| Function | File | CC | Recommendation |
|----------|------|-----|----------------|
| <name> | <file:line> | <score> | <how to simplify> |

## Refactoring Recommendations

1. **<Function>**: <specific suggestion>
   - Extract: <what to extract>
   - Simplify: <how to simplify>

## Next Steps
- [ ] Address critical complexity first
- [ ] Create issues for high complexity
- [ ] Consider refactoring sprint
```

### Step 7: Report to User

Tell the user:
1. Overall complexity summary
2. Number of functions over threshold
3. Top 3 refactoring targets
4. Location of full report

## Key Rules

- **Use the right tool** - radon for Python, gocyclo for Go
- **Focus on high CC** - prioritize 10+
- **Provide specific fixes** - not just "refactor this"
- **Write the report** - always produce artifact

## Quick Reference

**Simplifying High Complexity:**
- Extract helper functions
- Replace conditionals with polymorphism
- Use early returns
- Break up long functions
- Simplify nested loops
