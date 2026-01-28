---
name: github-tools
type: complex
depth: base
description: >-
  Executes GitHub operations via gh CLI wrapper. Use when managing issues,
  pull requests, workflows, CI runs, projects, releases, cache, labels, or
  searching repositories and code.
---

# [H1][GITHUB-TOOLS]
>**Dictum:** *Standardized invocation reduces agent errors.*

<br>

Invokes gh CLI commands through Python wrapper.

[IMPORTANT] Zero-arg commands default to `state=open`, `limit=30`. System auto-configures OAuth scopes.

```bash
# Zero-arg commands
uv run .claude/skills/github-tools/scripts/gh.py issue-list
uv run .claude/skills/github-tools/scripts/gh.py pr-list
uv run .claude/skills/github-tools/scripts/gh.py run-list
uv run .claude/skills/github-tools/scripts/gh.py workflow-list
uv run .claude/skills/github-tools/scripts/gh.py label-list
uv run .claude/skills/github-tools/scripts/gh.py release-list
uv run .claude/skills/github-tools/scripts/gh.py cache-list
uv run .claude/skills/github-tools/scripts/gh.py project-list
uv run .claude/skills/github-tools/scripts/gh.py repo-view
```

---
## [1][ISSUES]

```bash
uv run .claude/skills/github-tools/scripts/gh.py issue-list --state closed
uv run .claude/skills/github-tools/scripts/gh.py issue-view --number 42
uv run .claude/skills/github-tools/scripts/gh.py issue-create --title "Bug report" --body "Details"
uv run .claude/skills/github-tools/scripts/gh.py issue-comment --number 42 --body "Comment"
uv run .claude/skills/github-tools/scripts/gh.py issue-close --number 42
uv run .claude/skills/github-tools/scripts/gh.py issue-edit --number 42 --title "New title" --labels "bug,urgent"
```

---
## [2][PULL_REQUESTS]

```bash
uv run .claude/skills/github-tools/scripts/gh.py pr-list --state closed
uv run .claude/skills/github-tools/scripts/gh.py pr-view --number 99
uv run .claude/skills/github-tools/scripts/gh.py pr-create --title "Feature" --body "Description" --base main
uv run .claude/skills/github-tools/scripts/gh.py pr-diff --number 99
uv run .claude/skills/github-tools/scripts/gh.py pr-files --number 99
uv run .claude/skills/github-tools/scripts/gh.py pr-checks --number 99
uv run .claude/skills/github-tools/scripts/gh.py pr-merge --number 99
uv run .claude/skills/github-tools/scripts/gh.py pr-review --number 99 --event APPROVE --body "LGTM"
```

---
## [3][WORKFLOWS]

```bash
uv run .claude/skills/github-tools/scripts/gh.py run-list --limit 10
uv run .claude/skills/github-tools/scripts/gh.py run-view --run-id 12345
uv run .claude/skills/github-tools/scripts/gh.py run-logs --run-id 12345 --failed
uv run .claude/skills/github-tools/scripts/gh.py run-rerun --run-id 12345
uv run .claude/skills/github-tools/scripts/gh.py workflow-view --workflow ci.yml
uv run .claude/skills/github-tools/scripts/gh.py workflow-run --workflow ci.yml --ref main
```

---
## [4][SEARCH]

```bash
uv run .claude/skills/github-tools/scripts/gh.py search-repos --query "nx monorepo" --limit 10
uv run .claude/skills/github-tools/scripts/gh.py search-code --query "dispatch table" --limit 10
uv run .claude/skills/github-tools/scripts/gh.py search-issues --query "is:open label:bug" --limit 10
```

---
## [5][DISCUSSIONS]

**Queries**
```bash
uv run .claude/skills/github-tools/scripts/gh.py discussion-list
uv run .claude/skills/github-tools/scripts/gh.py discussion-list --category "D_kwDOCat123" --limit 10 --answered
uv run .claude/skills/github-tools/scripts/gh.py discussion-view --number 42
uv run .claude/skills/github-tools/scripts/gh.py discussion-category-list
uv run .claude/skills/github-tools/scripts/gh.py discussion-pinned
```

**Lifecycle**
```bash
uv run .claude/skills/github-tools/scripts/gh.py discussion-create --category-id "D_kwDOCat123" --title "Topic" --body "Content"
uv run .claude/skills/github-tools/scripts/gh.py discussion-update --discussion-id "D_kwDOABC123" --title "New title" --body "Updated"
uv run .claude/skills/github-tools/scripts/gh.py discussion-delete --discussion-id "D_kwDOABC123"
uv run .claude/skills/github-tools/scripts/gh.py discussion-close --discussion-id "D_kwDOABC123" --reason RESOLVED
uv run .claude/skills/github-tools/scripts/gh.py discussion-reopen --discussion-id "D_kwDOABC123"
```

**Moderation**
```bash
uv run .claude/skills/github-tools/scripts/gh.py discussion-lock --discussion-id "D_kwDOABC123" --reason SPAM
uv run .claude/skills/github-tools/scripts/gh.py discussion-unlock --discussion-id "D_kwDOABC123"
```

**Comments**
```bash
uv run .claude/skills/github-tools/scripts/gh.py discussion-comment --discussion-id "D_kwDOABC123" --body "Comment"
uv run .claude/skills/github-tools/scripts/gh.py discussion-comment --discussion-id "D_kwDOABC123" --body "Reply" --reply-to "DC_kwDOCmt456"
uv run .claude/skills/github-tools/scripts/gh.py discussion-comment-update --comment-id "DC_kwDOCmt456" --body "Edited"
uv run .claude/skills/github-tools/scripts/gh.py discussion-comment-delete --comment-id "DC_kwDOCmt456"
```

**Answers**
```bash
uv run .claude/skills/github-tools/scripts/gh.py discussion-mark-answer --comment-id "DC_kwDOCmt456"
uv run .claude/skills/github-tools/scripts/gh.py discussion-unmark-answer --comment-id "DC_kwDOCmt456"
```

**Labels**
```bash
uv run .claude/skills/github-tools/scripts/gh.py discussion-add-label --discussion-id "D_kwDOABC123" --label-ids '["LA_kwDOLbl789"]'
uv run .claude/skills/github-tools/scripts/gh.py discussion-remove-label --discussion-id "D_kwDOABC123" --label-ids '["LA_kwDOLbl789"]'
```

**Reactions**
```bash
uv run .claude/skills/github-tools/scripts/gh.py discussion-react --subject-id "D_kwDOABC123" --reaction THUMBS_UP
```

[NOTE] Get `discussion-id` from `discussion-view` output `id` field. Get `category-id` from `discussion-category-list`. Get `comment-id` from comment nodes in `discussion-view`. Get `label-ids` from `label-list` (use `node_id` field). Reaction values: `THUMBS_UP`, `THUMBS_DOWN`, `LAUGH`, `HOORAY`, `CONFUSED`, `HEART`, `ROCKET`, `EYES`.

---
## [6][PROJECTS_V2]

```bash
# View/List
uv run .claude/skills/github-tools/scripts/gh.py project-view --project 1
uv run .claude/skills/github-tools/scripts/gh.py project-item-list --project 1
uv run .claude/skills/github-tools/scripts/gh.py project-field-list --project 1

# CRUD
uv run .claude/skills/github-tools/scripts/gh.py project-create --title "Sprint 1"
uv run .claude/skills/github-tools/scripts/gh.py project-close --project 1
uv run .claude/skills/github-tools/scripts/gh.py project-delete --project 1

# Items
uv run .claude/skills/github-tools/scripts/gh.py project-item-add --project 1 --url "https://github.com/owner/repo/issues/42"
uv run .claude/skills/github-tools/scripts/gh.py project-item-edit --id ITEM_ID --project-id PROJECT_NODE_ID --field-id FIELD_ID --single-select-option-id OPT_ID
uv run .claude/skills/github-tools/scripts/gh.py project-item-delete --project 1 --id ITEM_ID
uv run .claude/skills/github-tools/scripts/gh.py project-item-archive --project 1 --id ITEM_ID

# Fields
uv run .claude/skills/github-tools/scripts/gh.py project-field-create --project 1 --name "Priority" --data-type SINGLE_SELECT --single-select-options "High,Medium,Low"
```

[NOTE] Get `ITEM_ID`, `FIELD_ID` from `project-item-list`/`project-field-list`. Get `PROJECT_NODE_ID` from `project-view` output `id` field. Field edit supports: `--text`, `--number`, `--date`, `--single-select-option-id`, `--iteration-id`.

---
## [7][OTHER]

```bash
uv run .claude/skills/github-tools/scripts/gh.py release-view --tag v1.0.0
uv run .claude/skills/github-tools/scripts/gh.py api --endpoint "/repos/{owner}/{repo}/issues" --method GET
```

---
## [8][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [PATTERN]         | [RESPONSE]                           |
| :-----: | ----------------- | ------------------------------------ |
|   [1]   | List commands     | `{items: object[]}`                  |
|   [2]   | View commands     | `{item: object}`                     |
|   [3]   | Mutation commands | `{number: int, action: bool}`        |
|   [4]   | Search commands   | `{query: string, results: object[]}` |
|   [5]   | Diff commands     | `{number: int, diff: string}`        |
