---
name: review-scoring
description: "ALWAYS load before starting any task. Provides the 10-dimension weighted scoring rubric (0-10 scale) used to evaluate all implementations in WRFC loops. Dimensions include correctness, completeness, error handling, type safety, security, performance, maintainability, testing, accessibility, and documentation. Includes deterministic validation scripts and score thresholds for pass/revise/reject decisions."
metadata:
  version: 1.0.0
  category: protocol
  tags: [review, scoring, rubric, wrfc, quality, validation]
---

## Resources
```
scripts/
  validate-review.sh
  validate-fix.sh
references/
  scoring-examples.md
```

# Review Scoring Protocol

This skill defines the precise scoring rubric and review format used in Work-Review-Fix-Check (WRFC) loops. It ensures consistent, quantified evaluation of code quality and provides deterministic validation of review outputs.

## Scoring Rubric (1-10 Scale)

Every review evaluates code across 10 dimensions. Each dimension receives a score from 1 to 10, where:

- **1-3**: Critical deficiencies, fundamental issues
- **4-5**: Significant problems, below acceptable standards
- **6-7**: Acceptable but with notable issues
- **8-9**: Good quality with minor issues
- **10**: Exceptional, production-ready

### The 10 Dimensions

#### 1. Correctness (Weight: 20%)
Does the code work as intended?

**Scoring criteria:**
- **10**: Logic is flawless, all edge cases handled, null/undefined checks present, no off-by-one errors
- **7-9**: Minor edge cases missed, some defensive checks could be added
- **4-6**: Logic errors in common paths, missing null checks, incorrect conditionals
- **1-3**: Fundamental logic errors, crashes on common inputs, broken core functionality

**Common issues:**
- Missing null/undefined checks
- Off-by-one errors in loops/arrays
- Incorrect boolean logic
- Race conditions in async code
- Unhandled promise rejections

#### 2. Completeness (Weight: 15%)
Is everything implemented fully?

**Scoring criteria:**
- **10**: Feature fully implemented, no TODOs, no placeholders, no commented-out code
- **7-9**: Minor TODO comments for future enhancements (not core functionality)
- **4-6**: Core features stubbed out, placeholder implementations, missing critical paths
- **1-3**: Mostly placeholders, incomplete implementation, major features missing

**Common issues:**
- TODO comments in production code
- Placeholder functions returning hardcoded values
- Missing error states
- Incomplete form validation
- Mock data instead of real API calls

#### 3. Security (Weight: 15%)
Are vulnerabilities prevented?

**Scoring criteria:**
- **10**: Input validated, auth checked, secrets not exposed, injection-safe, CORS configured
- **7-9**: Minor security hardening opportunities (rate limiting, additional logging)
- **4-6**: Missing input validation, auth checks bypassed in some paths, secrets in code
- **1-3**: Critical vulnerabilities (SQL injection, XSS, exposed credentials, no auth)

**Common issues:**
- Secrets hardcoded or committed to git
- Missing authentication checks
- SQL injection via string concatenation
- XSS via innerHTML or dangerouslySetInnerHTML
- CORS set to `*` in production
- Missing CSRF protection
- Sensitive data in client-side code

#### 4. Performance (Weight: 10%)
Is it efficient?

**Scoring criteria:**
- **10**: No N+1 queries, appropriate indexes, caching where needed, optimized re-renders
- **7-9**: Minor optimization opportunities (memoization, lazy loading)
- **4-6**: N+1 queries present, missing indexes, unnecessary re-renders
- **1-3**: Severe performance issues (blocking operations, memory leaks, infinite loops)

**Common issues:**
- N+1 database queries
- Missing database indexes
- Unnecessary React re-renders (missing useMemo/useCallback)
- Large bundle sizes (missing code splitting)
- Synchronous operations blocking event loop
- Memory leaks (event listeners not cleaned up)

#### 5. Conventions (Weight: 10%)
Does it follow project patterns?

**Scoring criteria:**
- **10**: Matches existing naming, file structure, import ordering, code style
- **7-9**: Minor style inconsistencies (formatting, import order)
- **4-6**: Different naming conventions, wrong file locations, inconsistent patterns
- **1-3**: Completely ignores project conventions, introduces conflicting patterns

**Common issues:**
- Inconsistent naming (camelCase vs snake_case)
- Wrong file locations (components in utils/)
- Import ordering violations
- Mixing tabs and spaces
- Different error handling patterns than rest of codebase

#### 6. Testability (Weight: 10%)
Are tests present and meaningful?

**Scoring criteria:**
- **10**: Comprehensive tests, edge cases covered, meaningful assertions, high coverage
- **7-9**: Tests exist but miss some edge cases or have weak assertions
- **4-6**: Minimal tests, only happy path, no edge cases
- **1-3**: No tests or tests that don't verify behavior

**Common issues:**
- No tests at all
- Tests only for happy path
- Tests with no assertions (smoke tests only)
- Missing edge case coverage
- Brittle tests tied to implementation details

#### 7. Readability (Weight: 5%)
Is it easy to understand?

**Scoring criteria:**
- **10**: Clear naming, appropriate abstraction, complex logic explained, self-documenting
- **7-9**: Mostly clear, a few cryptic variable names or unexplained complex logic
- **4-6**: Poor naming, overly complex, lacks comments where needed
- **1-3**: Incomprehensible, single-letter variables, deeply nested, no explanation

**Common issues:**
- Single-letter variable names (except loop counters)
- Functions over 50 lines
- Nesting over 4 levels deep
- Cryptic abbreviations
- Complex logic without explanatory comments

#### 8. Error Handling (Weight: 5%)
Are errors handled gracefully?

**Scoring criteria:**
- **10**: All errors caught, logged appropriately, user-facing messages clear, no silent failures
- **7-9**: Errors caught but logging could be improved, some generic messages
- **4-6**: Some try/catch blocks missing, silent failures, poor error messages
- **1-3**: No error handling, crashes on errors, no user feedback

**Common issues:**
- Empty catch blocks (silent failures)
- Generic error messages ("Something went wrong")
- Errors not logged
- Unhandled promise rejections
- No user-facing error states

#### 9. Type Safety (Weight: 5%)
Are types correct and comprehensive?

**Scoring criteria:**
- **10**: Types accurate, no `any`, generics used appropriately, strict mode enabled
- **7-9**: Mostly typed, a few `any` types with TODO comments to fix
- **4-6**: Many `any` types, type assertions without validation, loose typing
- **1-3**: TypeScript disabled, `any` everywhere, type assertions hiding errors

**Common issues:**
- Excessive use of `any`
- Type assertions (`as`) without runtime validation
- Missing return type annotations
- Incorrect generic constraints
- Disabling strict mode

#### 10. Integration (Weight: 5%)
Does it work with existing code?

**Scoring criteria:**
- **10**: Integrates seamlessly, doesn't break existing features, follows API contracts
- **7-9**: Minor integration points need adjustment
- **4-6**: Breaks existing features, violates API contracts, requires large changes elsewhere
- **1-3**: Incompatible with existing systems, breaks multiple features

**Common issues:**
- Breaking changes to public APIs
- Incompatible with existing auth flow
- Breaks other features (regression)
- Doesn't use shared utilities (reinvents wheel)
- Conflicts with existing state management

## Overall Score Calculation

The overall score is a weighted average of the 10 dimensions:

```
Overall = (Correctness x 0.20) + 
          (Completeness x 0.15) + 
          (Security x 0.15) + 
          (Performance x 0.10) + 
          (Conventions x 0.10) + 
          (Testability x 0.10) + 
          (Readability x 0.05) + 
          (Error Handling x 0.05) + 
          (Type Safety x 0.05) + 
          (Integration x 0.05)
```

**Example:**
```
Correctness: 9
Completeness: 8
Security: 10
Performance: 7
Conventions: 9
Testability: 6
Readability: 8
Error Handling: 7
Type Safety: 9
Integration: 9

Overall = (9x0.20) + (8x0.15) + (10x0.15) + (7x0.10) + (9x0.10) + 
          (6x0.10) + (8x0.05) + (7x0.05) + (9x0.05) + (9x0.05)
        = 1.8 + 1.2 + 1.5 + 0.7 + 0.9 + 0.6 + 0.4 + 0.35 + 0.45 + 0.45
        = 8.35/10
```

## Pass/Fail Thresholds

The overall score determines the verdict:

| Score Range | Verdict | Action Required |
|-------------|---------|----------------|
| **>= 9.5** | PASS | Ship it -- production ready |
| **8.0-9.49** | CONDITIONAL PASS | Minor issues -- fix and re-check (8.0 is inclusive, no full re-review) |
| **6.0-7.9** | FAIL | Significant issues -- fix and full re-review required |
| **Below 6.0** | FAIL | Major rework needed -- fix and full re-review required |

**Critical dimension rule**: If any dimension scores below 4, the overall verdict is automatically FAIL regardless of the calculated score.

## Required Review Output Format

Every review MUST produce this exact structure. Validation scripts check for these sections.

```markdown
## Review Summary
- **Overall Score**: X.X/10
- **Verdict**: PASS | CONDITIONAL PASS | FAIL
- **Files Reviewed**: [list of files]

## Dimension Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Correctness | X/10 | [specific findings] |
| Completeness | X/10 | [specific findings] |
| Security | X/10 | [specific findings] |
| Performance | X/10 | [specific findings] |
| Conventions | X/10 | [specific findings] |
| Testability | X/10 | [specific findings] |
| Readability | X/10 | [specific findings] |
| Error Handling | X/10 | [specific findings] |
| Type Safety | X/10 | [specific findings] |
| Integration | X/10 | [specific findings] |

## Issues Found

### Critical (must fix)
- [FILE:LINE] Description of issue. Fix: [specific fix]
- [FILE:LINE] Description of issue. Fix: [specific fix]

### Major (should fix)
- [FILE:LINE] Description of issue. Fix: [specific fix]
- [FILE:LINE] Description of issue. Fix: [specific fix]

### Minor (nice to fix)
- [FILE:LINE] Description of issue. Fix: [specific fix]
- [FILE:LINE] Description of issue. Fix: [specific fix]

## What Was Done Well
- [specific positive observation with file reference]
- [specific positive observation with file reference]
```

### Format Requirements

1. **Overall score**: Must be numeric (X.X/10 format, one decimal place)
2. **Verdict**: Must exactly match one of: PASS, CONDITIONAL PASS, FAIL
3. **Dimension scores**: All 10 dimensions present with X/10 format, notes must contain specific findings (not generic phrases like "looks good")
4. **Issue categorization**: Every issue must be in Critical/Major/Minor category
5. **FILE:LINE references**: Every issue must reference specific file and line number
6. **Fix suggestions**: Every issue must include specific fix guidance (what to change, how to change it, example code)
7. **What Was Done Well**: Must be present with at least one positive observation

### Issue Severity Guidelines

**Critical**: Must be fixed before shipping. Examples:
- Security vulnerabilities
- Data corruption bugs
- Authentication bypasses
- Crashes on common inputs
- Exposed secrets

**Major**: Should be fixed before shipping. Examples:
- Performance issues (N+1 queries)
- Missing error handling on important paths
- Accessibility violations
- Type safety violations (excessive `any`)
- Convention violations that affect maintainability

**Minor**: Nice to fix but not blockers. Examples:
- Suboptimal naming
- Missing comments on complex logic
- Minor style inconsistencies
- Opportunities for refactoring
- Weak test assertions

**Note**: Severity can depend on system risk context (e.g., performance issue may be Critical in high-scale systems).

## Fix Agent Requirements

When a fix agent receives a review with issues:

### Must Fix
1. **ALL Critical issues** -- No exceptions
2. **ALL Major issues** -- No exceptions
3. **Minor issues** -- Unless explicitly deprioritized by orchestrator

### Must Document
After applying fixes, the fix agent must produce:

```markdown
## Fixes Applied

### Critical Issues Addressed
- [FILE:LINE] [Original issue] -> Fixed by: [what was changed]
- [FILE:LINE] [Original issue] -> Fixed by: [what was changed]

### Major Issues Addressed
- [FILE:LINE] [Original issue] -> Fixed by: [what was changed]

### Minor Issues Addressed
- [FILE:LINE] [Original issue] -> Fixed by: [what was changed]

### Issues Not Fixed
- [FILE:LINE] [Original issue] -> Reason: [why it wasn't fixed]

**Example**:
- [src/api/legacy.ts:45] Complex refactoring of legacy code -> Reason: Out of scope for this PR, tracked in ticket #1234
```

### Prohibited Behaviors
1. **NO CLAIMING FIXED WITHOUT CHANGES**: Do not mark an issue as fixed without actually changing the code
2. **NO PARTIAL FIXES**: Either fix the issue completely or document why it can't be fixed
3. **NO SILENT SKIPS**: If you skip an issue, document it in "Issues Not Fixed" with reason
4. **NO NEW ISSUES**: Fixes should not introduce new bugs (check with re-review)

## Re-Review Requirements

After fixes are applied, a re-reviewer must:

### Verification Steps
1. **Check each previously flagged issue**
   - Verify the fix was applied
   - Verify the fix actually resolves the issue
   - Verify the fix didn't introduce new issues or just move the problem elsewhere

2. **Re-score all dimensions**
   - Do NOT just copy previous scores
   - Evaluate current state from scratch: (a) read modified files, (b) apply rubric criteria, (c) score based on current state
   - Document score changes ("Security: 6 -> 9")

3. **Identify new issues**
   - Issues found during re-review are NEW findings
   - Not counted as regressions unless they're directly caused by fixes
   - Categorize as Critical/Major/Minor using same rubric

### Re-Review Output Format

```markdown
## Re-Review Summary
- **Overall Score**: X.X/10 (was Y.Y/10)
- **Verdict**: PASS | CONDITIONAL PASS | FAIL
- **Previous Issues**: X critical, Y major, Z minor
- **Issues Resolved**: X critical, Y major, Z minor
- **New Issues Found**: X critical, Y major, Z minor

## Dimension Score Changes
| Dimension | Previous | Current | Change |
|-----------|----------|---------|--------|
| Correctness | X/10 | X/10 | +/- X |
| [etc] | ... | ... | ... |

## Previous Issues - Resolution Status

### Critical Issues
- [RESOLVED] [FILE:LINE] [Original issue] -> RESOLVED
- [NOT FIXED] [FILE:LINE] [Original issue] -> NOT FIXED: [reason]

### Major Issues
- [RESOLVED] [FILE:LINE] [Original issue] -> RESOLVED

### Minor Issues
- [RESOLVED] [FILE:LINE] [Original issue] -> RESOLVED

## New Issues Found
[Use standard Critical/Major/Minor format]
```

## WRFC Loop Context

This skill is a critical component of the Work-Review-Fix-Check loop:

1. **Work**: Engineer implements feature
2. **Review**: Reviewer applies this scoring rubric -> produces scored review
3. **Fix**: Fix agent addresses all Critical/Major issues -> produces fix report
4. **Check**: Re-reviewer verifies fixes -> re-scores -> determines if another loop needed

The orchestrator uses the numeric score and verdict to make decisions:
- **PASS (9.5+)**: Exit loop, mark complete
- **CONDITIONAL PASS (8.0-9.49)**: One more quick fix+check cycle
- **FAIL (<8.0)**: Full review-fix-check loop again

## Common Scoring Mistakes to Avoid

### Score Inflation
**Wrong**: Giving 8-9 scores when significant issues exist
**Right**: Use the rubric literally -- 6-7 means "acceptable but with notable issues"

### Inconsistent Severity
**Wrong**: Marking a security vulnerability as "Major" instead of "Critical"
**Right**: Use severity guidelines -- auth bypass is ALWAYS Critical

### Missing FILE:LINE References
**Wrong**: "The error handling is poor"
**Right**: "src/api/users.ts:42 - Empty catch block silently swallows errors"

### Vague Fix Suggestions
**Wrong**: "Fix the type safety issues"
**Right**: "Replace `any` with `User` type and add runtime validation with zod schema"

### Subjective Score Withholding
**Wrong**: Scoring 9.5 instead of 10 because "the domain is complex" or "staying below perfection"
**Right**: If no issues are identified, the score is 10. Scores must be objective and based solely on identified, actionable issues. A 10/10 is always achievable and must be awarded when no deficiencies are found. Never withhold points for subjective reasons like domain complexity, code novelty, or philosophical caution.

### Ignoring Positive Observations
**Wrong**: Only listing problems
**Right**: Also document what was done well (encourages good patterns)

### Verdict Mismatch
**Wrong**: Overall score 7.2/10 with verdict "PASS"
**Right**: Score 7.2 -> Verdict FAIL (threshold is 8.0 for conditional, 9.5 for pass)

## Validation Scripts

This skill includes deterministic validation scripts:

- **scripts/validate-review.sh**: Checks review output format compliance
- **scripts/validate-fix.sh**: Checks fix agent output addresses all critical/major issues

See `scripts/` directory for implementation details.

## Quick Reference

### Dimension Weights
```
Correctness:      20%  (most important)
Completeness:     15%
Security:         15%
Performance:      10%
Conventions:      10%
Testability:      10%
Readability:       5%
Error Handling:    5%
Type Safety:       5%
Integration:       5%
```

### Verdict Thresholds
```
9.5+ -> PASS
8.0-9.49 -> CONDITIONAL PASS
6.0-7.9 -> FAIL
<6.0 -> FAIL (major rework)
```

### Issue Severity
```
Critical: Security, crashes, data corruption -> MUST FIX
Major: Performance, missing features, poor practices -> SHOULD FIX
Minor: Style, optimization opportunities -> NICE TO FIX
```
