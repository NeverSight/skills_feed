---
name: pull-request
description: Create or update pull requests for the current branch
argument-hint: "[issue-number]"
arguments:
  - name: issue_number
    description: 関連するGitHub Issue番号
    required: false
user-invocable: true
model: Haiku
---

## Usage

```
/pull-request [issue_number]
```

### Arguments
- `issue_number` (optional): 関連するGitHub Issue番号

## Dependencies

- use git-operations-specialist skill

## Your task

**IMPORTANT: Do exactly what is instructed below, nothing more, nothing less. Do not add any additional "helpful" behavior like checking for unstaged changes or suggesting to push first.**

Delegate all operations to the git-operations-specialist skill:

- ask the skill to check if a pull request already exists for current branch
  - Use command: `gh pr list --head $(git branch --show-current) --state open --json number,title`
- if existing PR found:
  - ask the skill to update the existing pull request with current branch changes
  - update PR title and description based on latest commits
  - preserve the existing PR description structure as much as possible
  - if issue_number argument is provided, add "Related: #<issue_number>" to the description
- if no existing PR found:
  - ask the skill to create a new pull request with current branch
  - if issue_number argument is provided, add "Related: #<issue_number>" to the description

## Constraints

- Do NOT check git status or suggest pushing changes first
- Do NOT display messages about unstaged changes
- Do NOT add any preparatory steps beyond the specified tasks
- Proceed directly with PR creation/update regardless of repository state
