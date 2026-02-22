---
name: gitclaw-backup
description: GitHub backup for OpenClaw workspace. Use when user says "同步", "备份", "backup", "sync", "push to github", or asks about backup status/history/failures. Manages git-based full backup of ~/.openclaw to GitHub.
---

# GitClaw Backup

Full backup of `/home/node/.openclaw/` to GitHub via git.

## Quick Reference

- **Repo**: `https://github.com/blessonism/openclaw-backup.git`
- **Branch**: `main`
- **Script**: `/home/node/.openclaw/gitclaw/auto_backup.sh`
- **Cron**: `daily-workspace-backup` — 每天 UTC 16:00 (北京时间 0:00)
- **Exclude rules**: `/home/node/.openclaw/.gitignore`

## Manual Sync

Run the backup script directly:

```bash
bash /home/node/.openclaw/gitclaw/auto_backup.sh
```

Script behavior:
- Lock-based (prevents concurrent runs)
- Stages all changes (`git add -A`), respects `.gitignore`
- Skips commit if no changes
- Pushes to `origin main`
- Logs to `/home/node/.openclaw/gitclaw/backup.log`

## Post-Sync Response

After a successful sync, **always** include a clickable link to the latest commit in your reply:

```bash
# Get the latest commit short hash
cd /home/node/.openclaw && git log --oneline -1
```

Then format the response like:

> ✅ 同步完成 — [查看 commit](https://github.com/blessonism/openclaw-backup/commit/<full_hash>)

- If no changes were detected, report "无变更，跳过" (no link needed).
- If the push failed, report the error and suggest troubleshooting steps.

## Check Status

```bash
# Last backup log
tail -5 /home/node/.openclaw/gitclaw/backup.log

# Git status (uncommitted changes)
cd /home/node/.openclaw && git status --short

# Recent commits
cd /home/node/.openclaw && git log --oneline -5
```

## Exclude Files from Backup

Edit `/home/node/.openclaw/.gitignore` — standard gitignore syntax.

Current notable exclusions: `workspace/images/`, `workspace/node_modules/`, `workspace/.micromamba/`, `workspace/bin/`, large binary files.

## Troubleshooting

- **"already running"** in log → stale lock at `/home/node/.openclaw/gitclaw/lock/`, remove it: `rmdir /home/node/.openclaw/gitclaw/lock`
- **Push rejected** → likely force-push or diverged history on remote; check with `git log --oneline -5 origin/main`
- **Auth failure** → credentials in `~/.git-credentials`; verify with `git credential fill <<< "host=github.com"`
