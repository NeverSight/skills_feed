---
name: code-review
description: Guide for making code reviews. Use this when asked to make code reviews, or ask to use it before committing changes.
license: MIT
---

# Code review

Always start by inspecting the changes. If you're on the `main` git branch, typically the (staged) git diff. If you're on a different branch, the committed and uncommitted changes compared to the main branch.

## Method

Please dispatch two subagents to carefully review the code changes. Tell them that they're competing with another agent. Make sure they look at both architecture and implementation. Tell them that whomever finds more issues wins honour and glory.
