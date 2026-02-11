---
name: review-codebase
description: Architecture and design review for specified files/dirs/repo. Covers tech debt, patterns, quality. Diff-only review use review-diff. Complements review-code (orchestrated).
tags: [eng-standards]
version: 1.3.0
license: MIT
related_skills: [review-code, review-diff]
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review Codebase

## Purpose

From a **senior full-stack and production code-review** perspective, review **the current state of a given scope** (single file, directory, or whole repo): architecture, design, tech debt, patterns, and overall quality. Does not depend on git diff. Complements [review-code](../review-code/SKILL.md): review-code focuses on **the current change** (impact, regression, compatibility, side effects); this skill focuses on **the current state of the given scope**.

---

## Use Cases

- **New module/service**: Architecture and implementation review for a given dir or file.
- **Legacy audit**: Quality and risk review for a path or repo.
- **Pair / sampling**: Review files or dirs specified by a colleague, without requiring a current diff.
- **Teaching and standards**: Explain or check arbitrary code against the same review dimensions.

**When to use**: When the user wants to review **given path(s), directory(ies), or repo**, not “only the current diff.” For reviewing only local changes, use [review-diff](../review-diff/SKILL.md). For a full orchestrated review, use [review-code](../review-code/SKILL.md).

**Scope**: This skill focuses on **current state** (architecture, design, tech debt) of the given scope and does not depend on diff. It complements `review-code` (orchestrated). skills.sh options like `code-review-excellence` are more general; this skill emphasizes boundaries, patterns, and overall quality.

---

## Behavior

### Scope

- **Input defines scope**: Single file, directory, or “repo root” etc., as specified by the user; multiple paths allowed.
- **Not diff-bound**: Analyze **current file content** in the given scope; does not require a git change set. If the user also provides a diff, it can inform context but is not the sole input.

### For each file in scope (state/design-centric)

1. **Architecture and boundaries**: Are module/service boundaries clear, responsibilities single, dependency direction sensible?
2. **Design patterns and consistency**: Are patterns used appropriately? Style and patterns consistent with the rest of the repo/module?
3. **Tech debt and maintainability**: Duplication, complexity, testability, docs and comments vs. current state.
4. **Cross-module dependencies and coupling**: Too many dependencies, cycles, stable and clear interfaces?
5. **Security and performance (current)**: Input validation, sensitive data, permissions, resource use and concurrency risks in the current implementation.
6. **Concrete suggestions**: Actionable refactor or improvement (with file:line).

This skill looks at **full implementation and place in the whole**, not “this diff.”

### Tone and references

- **Professional and engineering-focused**: Review as if this will run in production.
- **Precise**: Reference specific locations (file:line).

### Scope and priority

- If the scope is large (e.g. whole repo), output by layer (module/dir) or agree with the user on a priority subset to avoid shallow, generic conclusions.

---

## Input & Output

### Input

- **Paths**: One or more file or directory paths (relative to workspace root or user-given root).
- **Optional**: Language/framework constraints, focus (e.g. security only, performance only).

**Defaults (confirm or choose; avoid free-text):**

| Item | Default | When to deviate |
| :--- | :--- | :--- |
| **Path(s)** | **Repo root** | Offer: [Repo root] [Current file's directory] [List top-level dirs to pick]; user selects. |
| **Large scope** | **By layer** (output by module/dir) | User can choose a **priority subset** (e.g. pick from top-level dirs). |

**Confirm before running**: (1) *Review repo root?* [default] or user selects path(s) from options. (2) If scope is large, use default "by layer" or user chooses a priority subset from offered list.

### Output

- **Per file or module**: Conclusions and suggestions for the dimensions above.
- **Format**: Headings (file or module), lists, and references (file:line) so the reader can follow the source.

---

## Restrictions

- **Do not** assume “review only diff” when scope is not clearly “diff”; this skill defaults to **full code in the given scope**.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** use vague language (e.g. “might be wrong” without type and fix direction).

---

## Self-Check

- [ ] Does the review scope match the user’s path(s)/dir(s)?
- [ ] Are boundaries, patterns, tech debt, dependencies and coupling, and current security/performance covered?
- [ ] Are issues referenced with file:line?
- [ ] Are concrete refactor or improvement suggestions given for important issues?

---

## Examples

### Example 1: Single directory

- **Input**: Path `src/auth/`; review all relevant code under it.
- **Expected**: Per file, list architecture and boundaries, design patterns and consistency, tech debt and maintainability, cross-module dependencies and coupling, current security and performance; reference line numbers and give improvement suggestions; do not depend on current git change.

### Example 2: Single file

- **Input**: Path `pkg/validator/validator.go`.
- **Expected**: Full review of the file: its role and boundaries, entry points and dependencies, patterns and consistency, tech debt and testability, current security and performance; reference line numbers.

### Edge case: Whole repo

- **Input**: Path is repo root or “whole project.”
- **Expected**: Output by layer (module/dir) or give a high-level summary and risk list (architecture, dependencies, tech debt), then agree with the user on a subset for deeper review; avoid one long, shallow pass.

---

## Appendix: Output contract

When this skill produces a review, it follows this contract so that findings can be aggregated with other atomic skills (e.g. by [review-code](../review-code/SKILL.md)):

| Element | Requirement |
| :--- | :--- |
| Scope | User-specified path(s); full code in scope; not diff-bound. |
| **Findings format** | Each finding MUST include **Location** (`path/to/file.ext` or file:line), **Category** (`scope` for this skill), **Severity** (`critical` \| `major` \| `minor` \| `suggestion`), **Title**, **Description**, and optionally **Suggestion**. |
| Per file/module | Headings, lists, references (file:line). |
| Dimensions | Architecture and boundaries; design patterns and consistency; tech debt and maintainability; cross-module dependencies and coupling; security and performance; concrete suggestions. |
| Large scope | Output by layer or agree on priority subset; avoid shallow pass. |

Example finding compatible with aggregation:

```markdown
- **Location**: `pkg/auth/service.go:31`
- **Category**: scope
- **Severity**: major
- **Title**: Module boundary unclear; auth logic mixed with HTTP handling
- **Description**: Controller contains validation and token logic; hard to test and reuse.
- **Suggestion**: Extract auth logic into a dedicated service; keep controller thin.
```
