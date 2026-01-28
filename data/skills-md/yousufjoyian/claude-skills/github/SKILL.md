---
name: github
description: Clone, pull, and manage GitHub repositories using SSH authentication. Handles yousufjoyian repos and third-party repos.
---

# GitHub Repository Manager

This skill manages GitHub repositories via SSH - cloning, pulling, and pushing code.

## Account Details

| Setting | Value |
|---------|-------|
| Username | `yousufjoyian` |
| SSH Key | `~/.ssh/github_ed25519` |
| Default Clone Location | `/home/yousuf/local_workspaces/` |

## When to Use This Skill

- Cloning a repository from GitHub
- Pulling latest changes from a repo
- Pushing commits to GitHub
- Checking repo status
- Listing user's repositories

## What This Skill Does

1. **Clone Repos**: Downloads repositories via SSH
2. **Pull Updates**: Fetches and merges latest changes
3. **Push Changes**: Uploads commits to GitHub
4. **Smart Defaults**: Assumes `yousufjoyian/` for bare repo names

## How to Use

### Clone Your Own Repo

```
Pull triclaude
```

```
Clone my youtube-transcripts repo
```

```
Get repo living-contract
```

### Clone Someone Else's Repo

```
Clone anthropics/claude-code
```

```
Pull microsoft/vscode
```

### Update Existing Repo

```
Update triclaude with latest changes
```

```
Pull latest on youtube-transcripts
```

### Push Changes

```
Push my changes to triclaude
```

## Commands Reference

### Clone a repo (yousufjoyian)
```bash
git clone git@github.com:yousufjoyian/<repo>.git /home/yousuf/local_workspaces/<repo>
```

### Clone third-party repo
```bash
git clone git@github.com:<owner>/<repo>.git /home/yousuf/local_workspaces/<repo>
```

### Pull latest
```bash
cd /home/yousuf/local_workspaces/<repo> && git pull
```

### Push changes
```bash
cd /home/yousuf/local_workspaces/<repo> && git push
```

### Check status
```bash
cd /home/yousuf/local_workspaces/<repo> && git status
```

### Test SSH connection
```bash
ssh -T git@github.com
```

## Workflow

1. **Parse repo name**:
   - `triclaude` → `yousufjoyian/triclaude`
   - `anthropics/claude-code` → `anthropics/claude-code`

2. **Check if exists locally**:
   - If `/home/yousuf/local_workspaces/<repo>/` exists → `git pull`
   - Otherwise → `git clone`

3. **Execute and report**:
   - Show clone/pull output
   - Report final path

## Trigger Words

| Phrase | Action |
|--------|--------|
| "pull", "clone", "get repo" | Clone or pull repo |
| "push", "upload" | Push commits |
| "github pull", "fetch from github" | Clone/pull |
| "update repo" | Git pull |

## Example Session

**User**: "Pull triclaude"

**Assistant**:
```
Cloning yousufjoyian/triclaude...

git clone git@github.com:yousufjoyian/triclaude.git /home/yousuf/local_workspaces/triclaude

Cloning into '/home/yousuf/local_workspaces/triclaude'...
remote: Enumerating objects: 245, done.
remote: Counting objects: 100% (245/245), done.
Receiving objects: 100% (245/245), 1.2 MiB | 5.00 MiB/s, done.

Done: /home/yousuf/local_workspaces/triclaude/
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `git-commit` | Local commits with smart staging and message crafting |

**Workflow:** Use `git-commit` skill for staging and committing locally, then this skill for push/pull.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission denied (publickey) | Run `ssh-add ~/.ssh/github_ed25519` |
| Repository not found | Check repo name/owner spelling |
| Already exists | Use `git pull` instead of clone |
| Merge conflicts on pull | Resolve conflicts manually or stash changes |

## SSH Setup (Already Configured)

Key location: `~/.ssh/github_ed25519`

If SSH agent needs the key:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github_ed25519
```

Verify connection:
```bash
ssh -T git@github.com
# Expected: Hi yousufjoyian! You've successfully authenticated...
```
