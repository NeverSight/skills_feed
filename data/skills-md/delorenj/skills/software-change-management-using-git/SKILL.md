---
name: software-change-management-using-git
description: Use this skill when any task is complete, before beginning any non-trivial task, or whenever working with git or tasked with commiting code.
---

# Software Change Management Using Git

## Workflow Automation for Git Commit Management

1. **Examine all changes since the last commit**:


    - It should do a deepthink to truely understand the changes from a high-level. Think about the consequences and what the main purpose for this change is in terms of the direction we're going. Also, do a diff between the trunk for a further zoomed out view in terms of the full branch and how this commit contributes to the full story. Hand off findings via stream chaining to step 2.
    - Look at any untracked files and determine if they should be added to the commit or inserted into the .gitignore. Perform the correct action.

2. **Craft an idiomatic git commit message**:


    - Take the data handed to you from step 1 and create a single-line description, followed by a blank line and then an itemized high-level changelist
    - Commit and push to HEAD

3. **Resolve any edge cases**:


    - If push fails, resolve by pulling from head, resolving any conflicts, rebasing, or whatever needs to be done to rectify the situation
