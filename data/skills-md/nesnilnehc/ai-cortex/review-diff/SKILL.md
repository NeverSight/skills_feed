---
name: review-diff
description: Review only git diff for impact, regression, correctness, compatibility, and side effects. Scope-only atomic skill; output is a findings list for aggregation.
tags: [eng-standards]
related_skills: [review-codebase, review-code]
version: 1.3.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
---

# Skill: Review Diff

## Purpose

Review **only the current change** (git diff, staged and unstaged) along a single dimension: **scope = diff**. Cover intent and impact, regression and correctness, breaking changes and compatibility, side effects and idempotency, and observability. Emit a **findings list** in the standard format so a meta skill (e.g. [review-code](../review-code/SKILL.md)) can aggregate with language, framework, and cognitive skills. Do not perform architecture, security, or language-specific analysis; those are separate atomic skills.

---

## Use Cases

- **Pre-commit**: Quick diff-only check before commit.
- **Orchestrated review**: Used as the scope step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive.
- **Focused change review**: When the user explicitly wants only "what changed" analyzed.

**When to use**: When the input is a git diff and the task is to review the change set itself, not the full codebase or language/framework/cognitive dimensions.

---

## Behavior

### Scope

- **Analyze**: Only files in the change set — diff (staged + unstaged) and **untracked files** that are part of the same change (included by default). Do not analyze unchanged or out-of-scope files.
- **Untracked files**: Included by default. When the invoker passes paths and full content of untracked files (e.g. new files to be committed), treat each as a full-file addition and apply the same review checklist; reference file path and line ranges as for added lines.
- **Do not**: Review whole repo, or cover architecture/security/language-specific rules; defer to review-codebase, review-security, review-dotnet, etc.

### Review checklist (diff dimension only)

For each changed file, evaluate and emit findings for:

1. **Intent and impact**: What changed and why (if inferable); impact on callers, data, config, deployment.
2. **Regression and correctness**: Does this change introduce bugs or miss edge cases? If it is a fix, is the fix complete?
3. **Breaking changes and compatibility**: Does it break API/data/config contracts? Backward compatibility or versioning/deprecation?
4. **Side effects and idempotency**: Unintended side effects, data corruption, duplication, or idempotency issues?
5. **Observability and debugging**: Does the change add or fix logs, metrics, or error messages for production debugging?
6. **Concrete suggestions**: Actionable fix or improvement with file:line or @@ block references.

### Tone and references

- **Professional and engineering-focused**: Review as if this will run in production.
- **Precise**: Reference specific locations (file:line or @@ block in the diff).

### Special cases

- **Bug fix**: Verify the fix is correct and note any remaining or partial issues.
- **Format/comments only**: State briefly "format/comments only, no behavior change"; if comments contradict or mislead, still emit a finding with suggestion.

---

## Input & Output

### Input

- **git diff**: Changes on the current branch vs HEAD (staged + unstaged), provided when invoking this skill.
- **Untracked files** (in scope by default): Paths and full content of untracked files that belong to the same change set. The invoker should include them so they are reviewed as full-file additions.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Each finding MUST include Location, Category, Severity, Title, Description, and optionally Suggestion.
- Category for this skill is always **scope**.

---

## Restrictions

- **Do not** review files outside the diff or the whole repo.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** use vague language (e.g. "might be wrong" without type and fix direction).
- **Do not** perform security, architecture, or language/framework-specific checks; stay within the diff scope dimension.

---

## Self-Check

- [ ] Was only the diff (and untracked files in the change set, when included) reviewed?
- [ ] Were intent, impact, regression, correctness, compatibility, side effects, and observability covered?
- [ ] Is each finding emitted with Location, Category=scope, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line or @@?
- [ ] For bug fixes, was fix logic verified and any remaining issues noted?

---

## Examples

### Example 1: API change

- **Input**: Diff adds a query param and changes response shape.
- **Expected**: Emit findings for intent/impact on callers, backward compatibility risk, breaking-change risk with suggestion (e.g. versioning or deprecation); reference specific lines or @@ blocks. Do not emit security or architecture findings in this skill.

### Example 2: Bug fix

- **Input**: Diff fixes a null pointer and one error code.
- **Expected**: Emit finding(s) confirming the fix and any regression (e.g. similar null-pointer or error-code issues); note observability (logs/errors); reference changed lines. Category = scope for all.

### Edge case: Format/comments only

- **Input**: Diff only has indentation, spaces, or comment changes.
- **Expected**: Either no findings or a single minor/suggestion finding: "format/comments only, no behavior change"; if comments contradict code, emit a finding with Title and Suggestion.

### Edge case: New (untracked) file in change set

- **Input**: Diff plus one untracked file (path + full content) as part of the change set (included by default).
- **Expected**: Review the new file as a full-file addition; apply the same checklist (intent, impact, regression, compatibility, side effects, observability); emit findings with Location = path and line references. Category = scope for all.

---

## Appendix: Output contract

When this skill produces a review, it emits a **findings list** compatible with aggregation by [review-code](../review-code/SKILL.md). Each finding MUST follow:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range, e.g. `src/api.go:42` or @@ block). |
| **Category** | `scope` (this skill only produces scope findings). |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example finding:

```markdown
- **Location**: `pkg/handler.go:31`
- **Category**: scope
- **Severity**: major
- **Title**: New query param may break existing clients
- **Description**: Response shape changed without versioning. Old clients may fail.
- **Suggestion**: Add API version or deprecation header; document in CHANGELOG.
```
