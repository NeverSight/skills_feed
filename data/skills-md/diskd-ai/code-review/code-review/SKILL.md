---
name: code-review
description: "Review code with a structured, high-signal review process. Use when asked to review code, review a PR/MR (GitHub PRs via `gh`, GitLab MRs via `glab`), review a codebase, give feedback on a changelist, audit code quality, or perform a code review. Supports both diff/PR reviews and full codebase reviews. Produces actionable findings with severity labels, exact file+line citations, and a final verdict. Covers design, functionality, complexity, tests, naming, comments, style, documentation, security, and performance."
---

# Code Review

Perform a structured code review. Produce actionable findings with exact file+line citations.

## Determine Review Mode

1. **Change review** (PR, diff, CL): review only code introduced by the change. Go to "Change Review Workflow."
2. **Codebase review** (full repo, specific files/modules): review the code as-is. Go to "Codebase Review Workflow."

---

## Change Review Workflow

### 1. Establish what to review

Obtain access to the post-change files for accurate line citations.

- Local checkout: use `git diff` (unstaged/staged) or a commit range
- GitHub PR: use `gh` to clone/checkout the PR branch (see [references/github-gh.md](references/github-gh.md))
- GitLab MR: use `glab` to clone/checkout the MR branch (see [references/gitlab-glab.md](references/gitlab-glab.md))
- If only a diff snippet is provided: ask for a branch/commit or full file contents

### 2. Scope the change

Constrain the review to code introduced by the change:

```bash
git diff --name-only          # changed files (working tree)
git diff --stat               # change size per file (working tree)
python scripts/diff_changed_ranges.py --json  # changed line ranges per file (working tree)

# PR/MR branch: diff vs base branch (use base from `gh pr view` / `glab mr view`)
git diff --name-only origin/main...HEAD
git diff --stat origin/main...HEAD
python scripts/diff_changed_ranges.py --range origin/main...HEAD --json
```

### 3. Broad assessment

Read the CL/PR description and skim all changed files. Ask: "Does this change make sense as a whole?"

- If the change should not proceed at all, provide immediate feedback with reasoning
- If the overall design is wrong, flag it before reviewing details

### 4. Critical components

Identify the most significant files (largest logical changes) and review those first. This provides context for smaller modifications.

If fundamental design issues emerge, communicate immediately -- major restructuring may invalidate subsequent code.

### 5. Systematic review

Review remaining files in logical order. Read tests before implementation when it helps clarify intent. Apply the review checklist (step 6 below).

Rules:
- Do not comment on pre-existing issues unless the change makes them newly reachable
- Prefer blocker/high-severity items over nits
- Review every line of human-written code

### 6. Verdict

- **Approve** if the CL improves overall code health, even if imperfect
- **Request changes** if the CL degrades code health or has blocking issues
- Technical facts override personal preference; accept the author's valid approach when multiple exist

---

## Codebase Review Workflow

### 1. Establish scope

Determine what to review:

- **Entire repo**: scan project structure, identify key modules
- **Specific files/modules**: focus on the requested scope
- **Specific concern** (e.g., "review security," "review architecture"): focus the checklist on that area

### 2. Understand the architecture

- Read project structure, entry points, and dependency graph
- Identify layers (domain, infrastructure, API, etc.)
- Note the tech stack, patterns, and conventions in use

### 3. Systematic review

Walk through the code module by module. Apply the review checklist below, focusing on all areas or the specific concern requested.

### 4. Summary

Provide an overall assessment of code health with prioritized findings.

---

## Review Checklist

For each file/hunk under review, evaluate against these areas (see [references/what-to-look-for.md](references/what-to-look-for.md) for full details):

| Area | Key questions |
|------|--------------|
| **Design** | Right architecture? Belongs here? Proper separation of concerns? |
| **Functionality** | Does what's intended? Edge cases handled? |
| **Complexity** | Simplest correct solution? Over-engineered? |
| | |
| **Security** | Injection, XSS, secrets, auth, IDOR, input validation? |
| **Performance** | N+1, missing indexes, re-renders, memory leaks, blocking async, caching? |
| | |
| **Code Quality** | DRY, SRP, deep nesting, magic values, error handling, type coverage? |
| **Tests** | Present, correct, edge cases, no flaky patterns, mocked at boundaries? |
| | |
| **Naming** | Descriptive, follows conventions? |
| **Comments** | Explain why, not what? |
| **Style** | Follows style guide? Consistent? |
| **Docs** | Updated if behavior changed? Breaking changes documented? |

## Verify Citations

Before writing each finding, verify exact line numbers:

```bash
python scripts/print_lines.py <file> <startLine> <endLine>
```

Use citation format: `path/to/file.ts#L10-L42`

## Write Comments

Follow comment best practices (see [references/review-comments.md](references/review-comments.md) for full guide):

- Comment on the **code**, never the developer
- Explain **why** the issue matters
- Use severity labels: **Blocker**, **High**, **Nit:**, **Optional:**, **FYI:**
- One issue per comment
- Acknowledge good work

## Produce the Review

Fill the template from `assets/review_template.md`. Each finding must include:

- Severity (Blocker / High / Medium / Low)
- Actionable fix direction
- Exact `file#Lx-Ly` citation

End with:
- **Verdict**: `approve`, `request changes`, or `comment only`
- 1-2 sentence justification
- **Confidence**: 0.0 to 1.0

## Reference Files

- **[references/review-standard.md](references/review-standard.md)** -- Core review standard: when to approve vs request changes, conflict resolution
- **[references/what-to-look-for.md](references/what-to-look-for.md)** -- Full checklist of review areas with details for each
- **[references/review-comments.md](references/review-comments.md)** -- How to write effective comments, severity labels, handling pushback
- **[references/github-gh.md](references/github-gh.md)** -- GitHub PR review workflow using `gh`
- **[references/gitlab-glab.md](references/gitlab-glab.md)** -- GitLab MR review workflow using `glab`
