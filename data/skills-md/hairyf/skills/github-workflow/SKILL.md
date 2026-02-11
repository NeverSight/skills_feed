---
name: github-workflow
description: "Standard flow from any task source (link or description) to creating a PR: resolve task, create branch and TODO.md, wait for fixes, create PR against origin only. Use find-skills to discover data-source query methods; after confirmation save to global config so the discovery step can be skipped next time. Use when the user provides a task link/description, asks to 'follow GitHub workflow', or 'create PR from task'."
metadata:
  author: hairy
  version: "2026.2.6"
---

# GitHub Workflow (Task → Environment Setup → Fix → PR)

## Goal

Standard flow from "task link or description" to "create PR (no merge)". Task source is **any data source**: first determine the query method via global config or find-skills, write to global config after confirmation, then use it directly next time.

**Output**: Branch created, `TODO.md` written, PR link targeting `dev` (origin only).

---

## Prerequisites

This workflow depends on **GitHub PR creation** (Step 4). Ensure one of the following before or when the user first runs the workflow:

1. **GitHub skill** is available in the user’s skills directory (e.g. `~/.agents/skills/github/` or your agent’s equivalent). The user can install it via:
   - `npx skills add hairyf/skills --skill github-cli -g` (or your environment’s skill discovery), then install the suggested skill.
2. **`gh` CLI** is installed and authenticated:
   - Install: [GitHub CLI](https://cli.github.com/)
   - Then run: `gh auth login`

**When to check**: At the start of the workflow (e.g. after the user provides the task), optionally run `gh auth status`. If it fails or the user has no GitHub skill, prompt: *"To create the PR in Step 4, the GitHub skill or `gh` CLI is required. Install the GitHub skill (see Prerequisites above) or install and log in with `gh auth login`. You can continue with Steps 1–3 now and set this up before Step 4."* Then continue; if Step 4 is reached and `gh` is still missing, use the edge case handling below.

---

## Global Data Source Config (Persistent)

- **Path**: `~/.bonfire/source.json` (user-level, applies across projects)
- **Purpose**: Once the user confirms a data source's query method, write it here; for the same type of input next time, use it directly and **skip find-skills**.

**Example config** (ClickUp):

```json
{
  "dataSourceType": "clickup",
  "description": "ClickUp task link",
  "matchPatterns": ["clickup.com/t/", "app.clickup.com"],
  "taskIdPlaceholder": "<task_id>",
  "commands": {
    "get": "node ~/.bonfire/skills/clickup/query.mjs get <task_id> --subtasks",
    "comments": "node ~/.bonfire/skills/clickup/query.mjs comments <task_id>"
  },
  "envCheck": "~/.bonfire/skills/clickup/.env"
}
```

- `matchPatterns`: If input URL or text contains any of these, treat as match and run commands from this config.
- `commands.get` / `commands.comments`: Replace `task_id` with the ID parsed from input, then execute.
- `envCheck`: Optional; if present, check that the .env at this path is configured; if not, prompt the user.

---

## Step 1: Get Task Content from Link or Description

### 1.1 Check Global Config

1. Read `~/.bonfire/source.json`.
2. If it exists and current input (URL or pasted text) matches any `matchPatterns`:
   - Parse task ID from input (common: last path segment of URL or `t/<id>`).
   - Use `commands.get`, `commands.comments` (replace `task_id` with parsed value) to fetch task title, description, status, comments, etc.
   - **Skip 1.2 (do not run find-skills)**, go to 1.3 output.

### 1.2 Not Configured or No Match: Discover Data Source (find-skills)

1. **Analyze input**: Is it a URL or plain text?
   - URL: Infer type from domain/path (e.g. clickup, jira, notion, linear, asana).
   - Plain text: Infer from keywords (e.g. "ClickUp task", "Jira requirement").

2. **Find skill**: Use find-skills to find how to "query tasks from this data source":
   - Run: `npx skills find <type or keyword>`  
     e.g. `npx skills find clickup`, `npx skills find jira task`, `npx skills find task management`.
   - If a matching skill exists (e.g. ~/.bonfire/skills/clickup/), prefer SKILL.md or scripts to confirm get-task / get-comments commands.

3. **Present options**: List the found skills or command usage (including install and usage) briefly; ask the user to confirm which method to use for "task title, description, comments".

4. **After confirmation, save to global**:
   - Fill `dataSourceType`, `matchPatterns`, `commands`, optional `envCheck` using the structure above.
   - Write to `~/.bonfire/source.json`.
   - Tell the user: "Data source config saved; next time for the same type of task it will be used directly and find-skills will be skipped."

5. Run the confirmed method once to get task info.

### 1.3 Output

- Task title, status, project/list (if any), issue description (body + comment summary).
- **kebab-case short description** for branch name (from title or ask user to supply).

**Fallback**: If .env is not configured or find-skills has no usable result, prompt the user to provide "task title, description, and short description for branch"; you can still proceed to Step 2 (branch and TODO.md can use pasted or later-filled content).

---

## Step 2: Prepare Environment (Create Branch, Write TODO.md)

- **Branch**:
  - `git checkout dev` → `git pull origin dev` → `git checkout -b fix/<short-desc-kebab-case>` (or `feature/...` depending on task type).
- **TODO.md**: Create `TODO.md` at project root with this structure:

```markdown
# Task: <task title>

**Task link**: <user-provided link or "see description">
**Status**: <current status>
**Project**: <project/list name, if any>

## Problem description
<task description and comments>

## Todo
- [ ] Analyze root cause
- [ ] Locate relevant code files
- [ ] Plan fix
- [ ] Implement fix
- [ ] Run checks (typecheck/test/lint)
- [ ] Commit

## Related files
<fill after analysis>

## Approach
1. Search for relevant keywords
2. Check API calls and type definitions
3. Inspect related components and pages
4. Understand data flow and display logic
```

- **Optional**: Update `.bonfire/index.md` with current branch and "Next Session Priorities".

---

## Step 3: Wait for User to Finish Fixes

Agent does not change business code; the user completes the fix, self-test, and commit. After the user says "fix done", proceed to Step 4.

---

## Step 4: Create PR with GitHub Skill (Origin Only)

- **Precondition**: Confirm current branch has the fix commits and will be pushed to **origin**.
- **Actions**:
  1. `git push -u origin <branch>` (push to origin only).
  2. `gh pr create --base dev --head <branch> --title "<title>" --body "<body with task link etc>"` (do not pass `--repo`; use current repo = origin).
- **Constraint**: Do not use `--repo <other-org/repo>` or any other remote for the PR. If `origin` is read-only or archived, output an error and suggest updating `origin` or creating the PR manually on the repo’s web UI.
- **End**: Output the PR link; do not merge.

---

## Edge Cases

| Case | Handling |
|------|----------|
| No global config and find-skills has no result | Ask user to provide task title, description, and short branch description; still create branch and TODO.md. |
| Data source .env not set or token invalid | Prompt to configure (e.g. .env at `envCheck` path), or ask user to provide task info directly. |
| `git pull origin dev` fails | Suggest checking network and `origin` access; or create branch from current local `dev` and note "latest not pulled". |
| Branch `fix/<name>` already exists | Ask whether to continue on existing branch or use a new name (e.g. `fix/<name>-v2`). |
| `origin` is archived or read-only | Do not add another remote; report error and suggest updating `origin` or creating PR on the repo’s web UI. |
| User asks for PR before saying "fix done" | If there are new commits and user explicitly requests, run Step 4; otherwise remind to finish fix and commit first. |
| `gh` not installed or not logged in | See **Prerequisites**. Prompt to install the GitHub skill or run `gh auth login`; or give steps to create PR from branch on GitHub web. |

---

## Reference

- Full spec and decision table: [github-workflow-spec.md](reference/github-workflow-spec.md)
- Task data source example: project ClickUp skill `~/.bonfire/skills/clickup/SKILL.md` (`query.mjs get/comments`)
- PR tool: `~/.agents/skills/github/SKILL.md` (`gh` CLI)
- Discover more data source skills: use find-skills (`npx skills find <keyword>`)
