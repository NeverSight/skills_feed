---
name: review
description: Review current uncommitted git changes with full file context and produce a structured report with severity levels, actionable fixes, and an approval verdict.
---

# Review

## Overview

Use this skill to review uncommitted changes in the current git workspace.  
Focus on correctness, safety, maintainability, and alignment with project standards.

The review must produce:

1. A concise summary of what changed
2. Prioritized findings with severity labels
3. Actionable fix suggestions
4. A final verdict (`Approve` or `Request Changes`)

## Workflow

### Step 1: Gather Context

1. Inspect current changes:
   - `git diff`
   - `git diff --cached` (if staged changes exist)
2. Read the full modified files (not only the diff hunks) to understand surrounding logic and architecture.
3. Check project documentation before judging style/patterns:
   - `docs/code-standard.md`
   - `docs/architecture.md`
   - `docs/codebase.md`
   - `docs/project-pdr.md`
4. Run relevant quality checks for touched areas (lint/type/tests when practical).

### Step 2: Analyze Changes

Evaluate each change across these dimensions:

1. **Correctness** - Does behavior match intended requirements?
2. **Safety & Security** - Are there vulnerabilities, data leaks, auth gaps, or unsafe assumptions?
3. **Reliability** - Are edge cases, null states, retries, and error paths handled?
4. **Style & Consistency** - Does code follow project conventions and established patterns?
5. **Performance** - Any unnecessary expensive operations or regressions?
6. **Testing** - Are critical paths covered with appropriate tests?
7. **Maintainability** - Is the code clear, modular, and easy to evolve?

### Step 3: Classify Findings by Severity

Assign one severity per finding using this rubric:

- **S0 - Critical**
  - Production-breaking issue, severe security risk, data corruption/loss, or irreversible side effects
  - Must be fixed before merge

- **S1 - High**
  - Likely bug, correctness flaw, significant reliability issue, or major missing validation
  - Should be fixed before merge

- **S2 - Medium**
  - Non-blocking but meaningful issue affecting maintainability, performance, or clarity
  - Fix recommended soon

- **S3 - Low**
  - Minor improvement, polish, or style-level suggestion
  - Optional unless team standards require it

### Step 4: Produce Structured Review Report

Use the report format below in this exact section order.

## Output Format

### 1) Summary

- What changed (2-6 bullets)
- Risk profile (low/medium/high)
- Areas reviewed (files/modules)

### 2) Findings

For each finding, use this template:

- **ID**: `R-001` (incrementing)
- **Severity**: `S0 | S1 | S2 | S3`
- **Category**: `Correctness | Security | Reliability | Style | Performance | Testing | Maintainability`
- **Location**: `path/to/file.ext#Lx-Ly` (or function/class name)
- **Issue**: Clear statement of the problem
- **Why it matters**: User/system impact
- **Suggestion**: Concrete fix guidance
- **Confidence**: `High | Medium | Low`

If no findings exist, explicitly write: **No actionable findings**.

### 3) Positive Notes

List good practices observed, such as:

- Strong test coverage additions
- Clean separation of concerns
- Thoughtful error handling
- Consistent style and naming

### 4) Must-Fix Checklist

Include only `S0` and `S1` findings:

- [ ] `R-00X` short fix description
- [ ] `R-00Y` short fix description

If none, state: **No must-fix items**.

### 5) Verdict

Use one of:

- **Approve** - No blocking issues (`S0/S1`) remain.
- **Request Changes** - One or more blocking issues (`S0/S1`) found.

Optionally include:

- **Re-review focus**: exact files/areas to re-check after fixes.

## Rules

- Be specific and cite exact locations whenever possible.
- Do not judge code in isolation; always consider surrounding context.
- Prefer actionable suggestions over vague criticism.
- Distinguish clearly between blocking and non-blocking feedback.
- Avoid speculative claims; if uncertain, lower confidence and explain why.
- Align feedback with project documentation and coding standards.

## Review Quality Checklist

Before finalizing, confirm:

- All modified files were reviewed with context
- Each finding has severity, impact, and fix suggestion
- Blocking issues are separated into a must-fix checklist
- Final verdict matches the finding severities
- Feedback is concise, precise, and implementable
