---
name: github-issue
description: "Create GitHub issues in this repo using the Codex issue template and the gh CLI. Use when the user asks to file/open/create a GitHub issue, track work, or request a Codex implementation run via .github/ISSUE_TEMPLATE/codex-task.md."
---

# Github Issue

## Overview

Create well-scoped GitHub issues using the repo’s Codex issue template and `gh issue create`.
Keep issues detailed enough for a Codex Argo workflow to execute the full request in one run.

## Workflow

### 1) Gather the required details

- Ensure you have: summary, context, desired outcome, scope (in/out), constraints/risks, rollout notes, validation, and a Codex prompt.
- If the user already provided content, reuse it verbatim and only ask for missing fields.

### 2) Start from the template

- Use `.github/ISSUE_TEMPLATE/codex-task.md` as the base.
- Copy it into a temp file and fill in every section. Keep it concise but complete.

### 3) Write a precise Codex prompt

- The prompt should be an explicit, step-by-step plan with exact file paths, constraints, and expected outputs.
- If multiple fixes are needed, enumerate them and specify validation.
- Avoid ambiguity; Codex should be able to execute without follow-up.

### 4) Create the issue with gh

```bash
cp .github/ISSUE_TEMPLATE/codex-task.md /tmp/issue.md
$EDITOR /tmp/issue.md
gh issue create --title "<clear, scoped title>" --body-file /tmp/issue.md --label codex
```

### 5) Report the result

- Return the issue URL and a short confirmation.
- If the repo requires extra labels or assignees, add them explicitly.

## Notes

- Prefer one issue per coherent workstream.
- When a request spans multiple components, ensure scope boundaries are clear in the template.
