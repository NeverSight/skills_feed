---
name: resolve-pegasus-conflicts
description: Resolve merge conflicts when upgrading SaaS Pegasus. Use when the user has merge conflicts after running git merge during a Pegasus upgrade, or when they need help with the merge process.
---

# Resolve Pegasus Conflicts

## Instructions

This skill helps users resolve merge conflicts when upgrading their SaaS Pegasus codebase. Most users will invoke this skill when they have merge conflicts after merging their main branch into a Pegasus upgrade branch, but you can also help run the merge process for them.

### When invoked

First, determine what the user needs help with by checking their current state:

1. **Check git status**: Run `git status` to see if there's an active merge in progress
2. **Ask the user**: If unclear, ask whether they:
   - Already ran `git merge` and need help resolving conflicts (most common)
   - Want you to run the merge process for them
   - Need help understanding which conflicts to prioritize

### If there's an active merge with conflicts

The user has already run `git merge <main branch>` and has conflicts to resolve. Help them resolve the conflicts using these strategies:

#### Database Migrations
- **Strategy**: Discard Pegasus migration changes, keep the user's changes
- **Reason**: Migration files should be regenerated, not merged
- **Action**: For conflicted migration files, accept theirs (the user's version from main), then run `./manage.py makemigrations` after all conflicts are resolved
- **Git command**: `git checkout --theirs <migration-file>` for each conflicted migration

#### Dependency Lock Files (uv.lock, requirements.txt, package-lock.json)
- **Strategy**: Accept Pegasus changes to lock files, merge source files manually
- **Source files**: `pyproject.toml`, `requirements.in`, `package.json`
- **Lock files**: `uv.lock`, `requirements.txt`, `package-lock.json`
- **Action**:
  1. For source files: Merge carefully, keeping customizations
  2. For lock files: Accept ours (Pegasus version) with `git checkout --ours <lock-file>` and `git add <lock-file>`
  3. **Immediately regenerate**: Run `uv sync` (for uv.lock) or `npm install` (for package-lock.json) right after resolving to ensure dependencies are properly synced
- **Important**: Don't wait until post-merge steps - regenerate lock files immediately after resolving them

#### Static Assets (JavaScript/CSS bundles in static/)
- **Strategy**: Delete and regenerate
- **Action**: Accept either version (doesn't matter), will be rebuilt
- **Regenerate**: Run `npm run build` or `npm run dev` after merge

#### Configuration Files (.env.example, settings files)
- **Strategy**: Merge carefully, keep customizations
- **Action**: Review both sides and combine them intelligently

#### Other Files
- **Strategy**: Evaluate case-by-case
- **Action**: Read both versions, understand the changes, merge intelligently

### If running the full merge process

If the user wants you to run the merge:

1. **Fetch latest changes**: Run `git fetch` to download the latest branches and commits from the remote (this ensures you can see the latest Pegasus upgrade branch)
2. **Find the latest upgrade branch**: Run `git branch -a` to list all branches and look for the latest Pegasus upgrade branch (usually prefixed with `pegasus-YYYY.MM`, e.g., `pegasus-2025.01`)
3. **Check current branch**: Run `git status` to see if they're already on the upgrade branch
4. **Checkout the upgrade branch**: If not already on it, run `git checkout <pegasus-branch-name>`
5. **Pull latest changes**: Run `git pull` to ensure the upgrade branch is up to date with the remote
6. **Identify main branch**: Determine the main development branch (usually `main` or `master`)
7. **Run merge**: Execute `git merge <main-branch>` to merge the main development branch into the Pegasus upgrade branch
8. **Handle result**:
   - If no conflicts: Success! Proceed to post-merge steps
   - If conflicts: Follow the conflict resolution strategies above

### Post-merge steps

After all conflicts are resolved and the merge is complete, **ask the user if they want to proceed with the post-merge steps** or if they prefer to do them manually later.

If the user wants to proceed, run these steps:

1. **Database migrations**: Run `./manage.py makemigrations` to create new migrations if needed
2. **Dependency sync**:
   - Python: `uv sync` (or `pip install -r requirements.txt`)
   - JavaScript: `npm install`
3. **Build assets**: `npm run build` (or `npm run dev` for development)
4. **Optional - Run migrations**: `./manage.py migrate` to apply database changes
5. **Optional - Docker users**: They can run `make upgrade` instead of manual steps above
6. **Push to GitHub**: Run `git push` to push the merged changes to GitHub. Once pushed, the upgrade branch should be ready to merge into the main branch via pull request

If the user prefers to do these manually, inform them what steps they should take when ready.

### Important reminders

- **Enable rerere**: Suggest running `git config rerere.enabled true` to remember conflict resolutions for future upgrades
- **Never squash**: When merging Pegasus PRs in GitHub, always use "Create a merge commit" (not squash or rebase)
- **Review changes**: Always review what changed in the upgrade before committing

### Examples

#### Example 1: User has conflicts (most common)
```
User: "I have merge conflicts after upgrading Pegasus"
You: [Check git status, see conflicts in migrations and uv.lock]
You: "I can see you have conflicts in migrations and uv.lock. Let me help resolve these:
- For migrations: I'll keep your version and we'll regenerate them
- For uv.lock: I'll accept the Pegasus version and regenerate it
[Proceed to resolve conflicts]"
```

#### Example 2: User wants help with the merge
```
User: "Can you help me merge my changes into the Pegasus upgrade branch?"
You: "I can help with that. Let me:
1. Find the latest Pegasus upgrade branch
2. Check out that branch (or confirm you're already on it)
3. Merge your main development branch into it
4. Help resolve any conflicts that come up
[Proceed with finding branch and running git merge main]"
```

### Edge cases

- **No pegasus upgrade branch**: If the user doesn't have a `pegasus-YYYY.MM` branch, direct them to the Pegasus upgrade documentation
- **Too many conflicts**: If there are dozens of conflicts across many files, suggest reviewing them in priority order (migrations first, then lock files, then configuration)
- **Custom modifications**: Be conservative with user customizations - when in doubt, keep their changes and note what was different in Pegasus
- **Unfamiliar file types**: If you encounter conflicts in files you're not sure how to handle, explain both sides of the conflict and ask the user which approach makes sense

