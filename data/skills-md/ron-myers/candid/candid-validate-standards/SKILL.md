---
name: candid-validate-standards
description: Validate Technical.md for vague rules, linter overlaps, and effectiveness issues
---

# Technical.md Validator

Analyze a Technical.md file and identify rules that may be ineffective, vague, or redundant with existing tooling.

## Workflow

### Step 1: Locate Technical.md

Find the Technical.md file to validate:

1. If path argument provided → use that path
2. Check `./Technical.md`
3. Check `./.candid/Technical.md`

If no file found:
```
❌ No Technical.md found.

Looked in:
- ./Technical.md
- ./.candid/Technical.md

Create one with: /candid-init
```

### Step 2: Detect Linter Configs

Check for existing linter configurations:

```bash
# JavaScript/TypeScript
ls .eslintrc* eslint.config.* .prettierrc* biome.json 2>/dev/null

# Python
ls .flake8 pyproject.toml setup.cfg .ruff.toml ruff.toml 2>/dev/null

# Go
ls .golangci.yml .golangci.yaml 2>/dev/null

# Ruby
ls .rubocop.yml 2>/dev/null
```

Store detected linters for Step 4.

### Step 3: Parse Technical.md

Read the Technical.md file and extract rules.

**Rule detection:**
- Lines starting with `-` or `*` (list items)
- Lines starting with numbers (numbered lists)
- Lines following a `##` heading

**Skip:**
- Code blocks (between ```)
- Empty lines
- Comments (HTML or markdown)
- Heading lines themselves

Store each rule with:
- Line number
- Section heading it belongs to
- Full rule text

### Step 4: Validate Each Rule

Check each rule against these issue categories:

#### 4.1 Vague Language (🌫️)

Flag rules containing vague terms without specifics:

| Vague Term | Why It's Vague |
|------------|----------------|
| "clean" | Subjective, no definition |
| "good" | Subjective |
| "proper" / "appropriate" | Undefined standard |
| "well-designed" / "well-structured" | No criteria |
| "readable" / "maintainable" | Without metrics |
| "best practices" | Circular reference |
| "when necessary" / "when appropriate" | Undefined trigger |
| "avoid" (alone) | No guidance on alternatives |
| "consider" | Not a requirement |

**Exception:** Terms are OK if followed by specific criteria:
- "readable (functions under 50 lines)" ✓
- "maintainable" ✗

#### 4.2 Missing Thresholds (📏)

Flag rules that imply quantity without numbers:

| Pattern | Issue |
|---------|-------|
| "small functions" | How small? |
| "short methods" | How short? |
| "limit parameters" | To how many? |
| "minimal dependencies" | What's minimal? |
| "few levels of nesting" | How few? |
| "reasonable timeout" | What's reasonable? |

**Fix pattern:** Add specific numbers (e.g., "functions under 50 lines")

#### 4.3 Linter Overlap (🔧)

Flag rules that linters typically handle (based on Step 2):

**If ESLint/Prettier detected:**
- Semicolon usage
- Quote style (single vs double)
- Indentation rules
- Trailing commas
- Import ordering
- Unused variables
- No console.log

**If Flake8/Ruff detected:**
- Line length
- Import sorting
- Whitespace rules
- Naming conventions (snake_case)

**If any linter detected:**
- Formatting rules in general
- Basic syntax style

#### 4.4 Multiple Concerns (🎯)

Flag rules that try to do too much:

- Rules with "and" connecting unrelated concerns
- Rules over 2 lines long
- Rules with multiple "must" statements

**Example:**
```
❌ "Functions should be small, well-documented, and handle errors properly"
✓ Split into three rules
```

#### 4.5 Unverifiable Rules (❓)

Flag rules that can't be checked by reading code:

- "Think about edge cases"
- "Be consistent"
- "Follow team conventions"
- "Use common sense"
- References to external documents without specifics

### Step 5: Generate Report

Present findings organized by severity:

```markdown
# Technical.md Validation Report

**File:** ./Technical.md
**Rules analyzed:** [N]
**Issues found:** [M]

---

## 🔴 Critical Issues

Rules that won't be effective in reviews.

### 🌫️ Vague Language

| Line | Rule | Issue |
|------|------|-------|
| 12 | "Write clean code" | "clean" is subjective |
| 24 | "Use appropriate error handling" | "appropriate" undefined |

### 📏 Missing Thresholds

| Line | Rule | Issue |
|------|------|-------|
| 18 | "Keep functions small" | No size specified |
| 31 | "Limit nesting depth" | No depth specified |

---

## 🟡 Warnings

Rules that may have issues.

### 🔧 Linter Overlap

| Line | Rule | Linter |
|------|------|--------|
| 8 | "Use semicolons" | ESLint handles this |
| 15 | "Sort imports alphabetically" | Prettier/ESLint handles this |

### 🎯 Multiple Concerns

| Line | Rule | Suggestion |
|------|------|------------|
| 22 | "Functions should be pure, small, and documented" | Split into 3 rules |

---

## ✅ Good Rules

[List of rules that passed validation]
```

### Step 6: Suggest Fixes (if --fix flag)

If `--fix` argument provided, include specific rewrites:

```markdown
## 💡 Suggested Rewrites

### Line 12: "Write clean code"
**Original:** Write clean code
**Suggested:**
- Functions must be under 50 lines
- No single-letter variable names except loop counters
- Maximum 3 levels of nesting

### Line 18: "Keep functions small"
**Original:** Keep functions small
**Suggested:** Functions must be under 50 lines (warning at 30)

### Line 24: "Use appropriate error handling"
**Original:** Use appropriate error handling
**Suggested:**
- All async functions must have try/catch or .catch()
- Errors must be logged with context before re-throwing
- User-facing errors must not expose stack traces
```

### Step 7: Summary

End with actionable summary:

```markdown
---

## Summary

- **[X] rules** are effective and specific ✅
- **[Y] rules** need thresholds or specifics 📏
- **[Z] rules** overlap with linters 🔧
- **[W] rules** are too vague to enforce 🌫️

### Recommended Actions

1. Remove [Z] linter-overlap rules (your linter handles these)
2. Add numbers to [Y] threshold rules
3. Rewrite [W] vague rules with specific criteria

Run `/candid-validate-standards --fix` for suggested rewrites.
```

## Output Examples

### Clean Technical.md

```
✅ Technical.md Validation Passed

File: ./Technical.md
Rules analyzed: 24
Issues found: 0

All rules are specific and verifiable. Nice work!
```

### Issues Found

```
⚠️ Technical.md Validation: 8 issues found

File: ./Technical.md
Rules analyzed: 24
Issues found: 8

🌫️ Vague Language (3)
  Line 12: "clean code" - subjective term
  Line 18: "proper error handling" - "proper" undefined
  Line 31: "when necessary" - undefined trigger

📏 Missing Thresholds (2)
  Line 15: "small functions" - no size specified
  Line 22: "limit nesting" - no depth specified

🔧 Linter Overlap (3)
  Line 5: semicolons - handled by ESLint
  Line 8: quote style - handled by Prettier
  Line 11: import order - handled by ESLint

Run `/candid-validate-standards --fix` for suggested rewrites.
```

## Vague Terms Reference

Use this list to detect vague language:

```
clean, good, proper, appropriate, suitable, adequate
well-designed, well-structured, well-organized, well-written
readable, maintainable, scalable, flexible, robust
best practices, industry standards, conventions
simple, straightforward, intuitive, obvious
reasonable, sensible, meaningful, significant
when necessary, when appropriate, when needed, as needed
avoid, prefer, consider, try to, should (without specifics)
minimal, few, some, many, several, various
```

## Threshold Patterns Reference

Patterns that need numbers:

```
small/short/brief + (function|method|class|file|module)
limit/restrict/cap + (parameters|arguments|nesting|depth|complexity)
maximum/minimum + (without number following)
too many/too few + (without threshold)
keep ... under/below + (without number)
no more than + (without number)
```

## Remember

The goal is to help users write Technical.md files that:
1. Candid can actually enforce
2. Don't duplicate existing tooling
3. Focus on what matters (architecture, security, patterns)
4. Are specific enough to be useful

A validated Technical.md leads to better code reviews.
