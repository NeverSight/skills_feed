---
name: scheduler
description: Schedules Claude Code tasks to run automatically at specific times using native OS schedulers (launchd on macOS, crontab on Linux, Task Scheduler on Windows). Handles one-time tasks like "today at 3pm remind me to deploy", "tomorrow morning run the test suite", "next Tuesday at 2pm review the API changes", "January 15th check the quarterly metrics". Also handles recurring tasks like "every weekday at 9am review yesterday's code", "daily at 6pm summarize what I accomplished", "every Monday at 10am check for security vulnerabilities", "every 4 hours check API health". Recognizes time formats like "at 9am", "at 1015am", "at 10:30pm", "at noon", relative times like "tomorrow", "tonight", "later", "next week", and dates like "January 15th". Use this skill instead of executing immediately whenever the user's request contains a time expression like "at Xam", "tomorrow", or any future time reference.
allowed-tools: Read, Bash(python:*), Bash(launchctl:*), Bash(crontab:*), Bash(schtasks:*)
---

# Scheduling Assistant

You help users set up and manage scheduled Claude Code tasks. You can:

- Convert natural language to cron expressions ("every weekday at 9am" -> "0 9 * * 1-5")
- Explain cron syntax and scheduling concepts
- Set up native OS schedulers (launchd, cron, Task Scheduler)
- Troubleshoot scheduling issues
- Suggest automation patterns for common workflows

## Quick Start

To create a scheduled task:
```
/scheduler:schedule-add
```

To view all scheduled tasks:
```
/scheduler:schedule-list
```

## One-Time vs Recurring Tasks

The scheduler supports both **one-time** and **recurring** tasks:

### One-Time Tasks
For tasks that run once at a specific time:
- "run at 3pm today"
- "tomorrow at noon"
- "next Tuesday at 2pm"

One-time tasks **automatically clean up** after execution.

### Recurring Tasks
For tasks that repeat on a schedule:
- "every day at 9am"
- "daily at 6pm"
- "weekdays at 10am"
- Cron expressions like `0 9 * * 1-5`

**Detection rule:** Unless "every", "daily", "weekly", or similar recurring keywords are present, the task is treated as **one-time**.

### Git Worktree Mode (Isolated Branches)

For tasks that make changes, worktree mode runs them in isolation:

```
You: Every night at 2am, refactor deprecated API calls and push for review

Claude: Should this run in an isolated git worktree?
        → Yes, create branch and push changes
        → No, run in main working directory

You: Yes

Claude: ✓ Task created with worktree isolation
        Branch prefix: claude-task/
        Remote: origin
```

**How it works:**
1. Task triggers → creates fresh worktree with new branch
2. Claude runs in the worktree (isolated from main)
3. Changes are committed and pushed to remote
4. Worktree is cleaned up after successful push
5. You review the PR at your convenience

**Configuration options:**
| Option | Default | Description |
|--------|---------|-------------|
| `worktree.enabled` | `false` | Enable worktree isolation |
| `worktree.branchPrefix` | `"claude-task/"` | Branch name prefix |
| `worktree.remoteName` | `"origin"` | Remote to push to |

If push fails, the worktree is kept for manual review.

## Cron Quick Reference

```
* * * * *
| | | | |
| | | | +-- Day of week (0-6, Sun=0)
| | | +---- Month (1-12)
| | +------ Day of month (1-31)
| +-------- Hour (0-23)
+---------- Minute (0-59)
```

**Common patterns:**
| Pattern | Description |
|---------|-------------|
| `0 9 * * *` | Daily at 9:00 AM |
| `0 9 * * 1-5` | Weekdays at 9:00 AM |
| `*/15 * * * *` | Every 15 minutes |
| `0 */2 * * *` | Every 2 hours |
| `0 9 1 * *` | First of month at 9:00 AM |
| `0 9 * * 1` | Every Monday at 9:00 AM |

For complete syntax, see [CRON_REFERENCE.md](CRON_REFERENCE.md).

## Platform Setup

Tasks are executed by your OS's native scheduler:
- **macOS:** launchd (LaunchAgents)
- **Linux:** crontab
- **Windows:** Task Scheduler

For platform-specific details, see [PLATFORM_SETUP.md](PLATFORM_SETUP.md).

## Common Use Cases

### Daily Code Review
```
Schedule: 0 9 * * 1-5 (weekdays at 9am)
Command: /review-code --scope=yesterday
```

### Weekly Dependency Audit
```
Schedule: 0 10 * * 1 (Mondays at 10am)
Command: Check for outdated dependencies and security vulnerabilities
```

### Automated Testing
```
Schedule: 0 */4 * * * (every 4 hours)
Command: Run test suite and report failures
```

## Troubleshooting

**Task not running?**
1. Check `/scheduler:schedule-status` for health
2. Verify task is enabled: `/scheduler:schedule-list`
3. Check logs: `/scheduler:schedule-logs <task-id>`
4. Ensure `claude` CLI is in PATH for scheduler

**Common issues:**
- PATH not set correctly in scheduler environment
- Working directory doesn't exist
- Command syntax errors
- Scheduler daemon not running

## Helper Scripts

To validate a cron expression:
```bash
python scripts/parse-cron.py "0 9 * * 1-5"
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/scheduler:schedule-add` | Create a new scheduled task |
| `/scheduler:schedule-list` | View all scheduled tasks |
| `/scheduler:schedule-remove <id>` | Remove a scheduled task |
| `/scheduler:schedule-status` | Check scheduler health |
| `/scheduler:schedule-run <id>` | Manually run a task |
| `/scheduler:schedule-logs <id>` | View execution logs |
