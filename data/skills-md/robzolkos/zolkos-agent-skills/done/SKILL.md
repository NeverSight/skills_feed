---
name: done
description: Reset the working directory for the next task by ensuring no uncommitted changes exist, then switching to the main branch and pulling latest.
disable-model-invocation: true
allowed-tools: Bash(git *)
---

# Done - Reset for next task

You are finishing up the current work and resetting the repo to be ready for the next task.

## Steps

1. **Check for uncommitted changes**: Run `git status --porcelain`. If there is ANY output (staged, unstaged, or untracked files), stop immediately and tell the user:
   - List the uncommitted/untracked files
   - Tell them to commit or stash their changes before running `/done`
   - Do NOT proceed to the next steps

2. **Determine the default branch**: Run `git branch --list master main` to check which exists. Prefer `master` if it exists, otherwise use `main`. If neither exists, tell the user that no master or main branch was found and stop.

3. **Switch to the default branch**: Run `git checkout <branch>` where `<branch>` is the branch determined in step 2.

4. **Pull latest changes**: Run `git pull` to fetch and merge the latest changes from the remote.

5. **Confirm**: Tell the user they are now on the default branch with the latest changes and ready to start the next task.
