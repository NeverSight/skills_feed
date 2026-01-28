---
name: git-commit
description: Create Git Commits Following Conventional Commits Specification. Use when the user asks to commit, craft a commit message, stage changes, or split work into multiple commits.
---

# Git Commit

## Goal
Make commits that are easy to review and safe to ship:
- only intended changes are included
- commits are logically scoped (split when needed)
- commit messages describe what changed and why

## Workflow Checklist
1. Inspect the working tree before staging.
   - `git status`
   - `git diff` (unstaged)
     - If many changes: `git diff --stat`
   - `git diff --staged` (unstaged)
     - If many changes: `git diff --staged --stat`
2. Decide commit boundaries (split if needed).
   - Split by: feature vs refactor, backend vs frontend, formatting vs logic, tests vs prod code, dependency bumps vs behavior changes.
   - If changes are mixed in one file, plan to use patch staging.
3. Stage only what belongs in the next commit.
   - Prefer patch staging for mixed changes: `git add -p`
   - To unstage a hunk/file: `git restore --staged -p` or `git restore --staged <path>`
4. Review what will actually be committed.
   - Sanity checks:
     - no secrets or tokens
     - no accidental debug logging
     - no unrelated formatting churn
5. Describe the staged change in 1-2 sentences (before writing the message)
   - "What changed?" + "Why?"
   - If you cannot describe it cleanly, the commit is probably too big or mixed; go back to step 2.
6. Commit directly without user confirmation.
   - Use Conventional Commits (required):
     - `type(scope): <summary>`(type and scope MUST be English lowercase, summary MUST be Chinese, no period)
     - blank line
     - body (MUST be Chinese, describe what/why, Use imperative mood for summary, MUST be `-` prefix markdown list format, no period)
     - footer (MUST be Chinese, for BREAKING CHANGE) if needed
7. Repeat for the next commit until the working tree is clean.

**Types:**
| Type | Use |
|------|-----|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation |
| style | Formatting |
| refactor | Restructure |
| perf | Performance |
| test | Tests |
| build | Build system |
| ci | CI config |
| chore | Other |
| revert | Revert |

**Example:**
```text
feat(auth): 添加用户登录功能

- 实现基于JWT的用户认证机制
- 支持邮箱和手机号两种登录方式

BREAKING CHANGE: 移除旧版session认证，需要重新登录
```

## Deliverable
Provide:
- the final commit message(s)
- a short summary per commit (what/why)
