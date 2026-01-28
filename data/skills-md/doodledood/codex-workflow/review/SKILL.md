---
name: review
description: "Comprehensive code review orchestrator. Runs multiple focused review analyses (bugs, types, maintainability, simplicity, coverage, docs, AGENTS.md) and consolidates findings. Use before PR or after implementation. Triggers: review, code review, review my changes, PR review."
---

**User request**: $ARGUMENTS

Orchestrate comprehensive code review by running specialized review skills and consolidating findings.

**Flags**:
- `--autonomous` → no user prompts, run all applicable reviews, return consolidated report
- `--skip <types>` → skip specific review types (comma-separated: bugs, types, maintainability, simplicity, testability, coverage, docs, agents-md)
- `--only <types>` → run only specific review types

**Output**: Consolidated review report to user.

## Phase 1: Setup

### 1.1 Determine Scope

**Priority order for scope**:
1. **User specifies files/directories in $ARGUMENTS** → use those
2. **Otherwise** → diff against `origin/main` or `origin/master`
3. **No changes found** → ask user what to review

### 1.2 Select Reviews

Determine which reviews to run based on scope and arguments:

| Review Type | Skill | When to Include |
|-------------|-------|-----------------|
| Bugs | `$review-bugs` | Always (unless skipped) |
| Type Safety | `$review-type-safety` | TypeScript/typed Python detected |
| Maintainability | `$review-maintainability` | Always (unless skipped) |
| Simplicity | `$review-simplicity` | Always (unless skipped) |
| Testability | `$review-testability` | Always (unless skipped) |
| Coverage | `$review-coverage` | Test files exist in project |
| Docs | `$review-docs` | Always (unless skipped) |
| AGENTS.md | `$review-agents-md-adherence` | AGENTS.md file exists |

**Detection logic**:
- TypeScript: `tsconfig.json` exists
- Typed Python: `pyproject.toml` with mypy config OR `py.typed` marker
- Test files: `*.test.*`, `*.spec.*`, `__tests__/`, `tests/` exist
- AGENTS.md: file exists in project root or parent directories

### 1.3 Create Todo List

```
- [ ] Run bug review
- [ ] Run type safety review (if applicable)
- [ ] Run maintainability review
- [ ] Run simplicity review
- [ ] Run testability review
- [ ] Run coverage review (if applicable)
- [ ] Run docs review
- [ ] Run AGENTS.md review (if applicable)
- [ ] Consolidate findings
```

## Phase 2: Execute Reviews

### 2.1 Review Loop

For each selected review type:

1. Mark todo `in_progress`
2. Execute the review skill
3. Capture findings (severity, location, description, suggested fix)
4. Mark todo `completed`
5. Continue to next review

### 2.2 Individual Review Execution

Run each review against the same scope:

**Bug Review**:
```
$review-bugs {scope}
```

**Type Safety Review** (if TypeScript/typed Python):
```
$review-type-safety {scope}
```

**Maintainability Review**:
```
$review-maintainability {scope}
```

**Simplicity Review**:
```
$review-simplicity {scope}
```

**Testability Review**:
```
$review-testability {scope}
```

**Coverage Review** (if tests exist):
```
$review-coverage {scope}
```

**Docs Review**:
```
$review-docs {scope}
```

**AGENTS.md Review** (if AGENTS.md exists):
```
$review-agents-md-adherence {scope}
```

### 2.3 Capture Findings

From each review, extract issues with:
- **Category**: bugs | type-safety | maintainability | simplicity | testability | coverage | docs | agents-md
- **Severity**: Critical | High | Medium | Low
- **Location**: file:line
- **Description**: What the issue is
- **Suggested Fix**: How to resolve

## Phase 3: Consolidate

### 3.1 Merge and Deduplicate

Combine all findings:
1. Group by severity (Critical → High → Medium → Low)
2. Within severity, group by category
3. Deduplicate: same file:line with similar description → merge, keep highest severity

### 3.2 Generate Report

```markdown
# Code Review Report

**Scope**: {files/changes reviewed}
**Reviews run**: {list of review types executed}

## Summary

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Bugs | N | N | N | N |
| Type Safety | N | N | N | N |
| Maintainability | N | N | N | N |
| Simplicity | N | N | N | N |
| Testability | N | N | N | N |
| Coverage | N | N | N | N |
| Docs | N | N | N | N |
| AGENTS.md | N | N | N | N |
| **Total** | N | N | N | N |

## Critical Issues

### [BUG] {Title}
**Location**: `file.ts:line`
**Description**: {issue}
**Suggested Fix**: {fix}

### [TYPE] {Title}
...

## High Issues
{Same format}

## Medium Issues
{Same format}

## Low Issues
{Same format}

## Review Status

| Review | Status | Issues Found |
|--------|--------|--------------|
| Bugs | ✓ Complete | N |
| Type Safety | ✓ Complete | N |
| Maintainability | ✓ Complete | N |
| Simplicity | ✓ Complete | N |
| Testability | ✓ Complete | N |
| Coverage | ✓ Complete | N |
| Docs | ✓ Complete | N |
| AGENTS.md | ✓ Complete | N |

## Recommendations

### Priority Fixes (do first)
1. {Critical/High issue with highest impact}
2. {Second priority}
3. {Third priority}

### Quick Wins (easy fixes)
- {Low-effort issues that can be fixed quickly}

### Deferred (consider later)
- {Low-severity issues that don't block merge}
```

### 3.3 Clean Report

If no issues found:

```markdown
# Code Review Report

**Scope**: {files/changes reviewed}
**Reviews run**: {list}
**Status**: ALL CLEAR

No issues found. Code is ready for merge.

## Review Status

| Review | Status | Issues Found |
|--------|--------|--------------|
| Bugs | ✓ Complete | 0 |
| Type Safety | ✓ Complete | 0 |
...
```

## Phase 4: Present Results

### 4.1 If `--autonomous`

Return consolidated report without prompts.

### 4.2 If Interactive

Present summary and ask:

```
## Review Complete

Found {N} issues across {M} categories.

Critical: {N} | High: {N} | Medium: {N} | Low: {N}

### Top Priority Fixes
1. {Issue 1}
2. {Issue 2}
3. {Issue 3}

What would you like to do?
Options:
  - Fix issues - run $fix-review-issues (Recommended if Critical/High exist)
  - Show full report - see all findings
  - Done - I'll address manually
```

## Edge Cases

| Case | Action |
|------|--------|
| No scope (no changes, no files specified) | Ask user what to review |
| No applicable reviews (e.g., no TS, no tests, no AGENTS.md) | Run only applicable reviews, note skipped |
| Review skill errors | Note error in report, continue with other reviews |
| All reviews clean | Report "ALL CLEAR" |
| Very large scope | Warn user, proceed (reviews handle internally) |

## Guidelines

- **Comprehensive**: Run all applicable reviews unless explicitly skipped
- **Consolidated**: Single unified report, not multiple separate outputs
- **Actionable**: Prioritize findings, suggest fix order
- **Efficient**: Skip inapplicable reviews (no TypeScript = skip type review)
- **Autonomous**: Support `--autonomous` for CI/automation use
