---
name: tasknotes
description: This skill should be used when users mention tasks, todos, work items, Obsidian notes, or need to manage their personal task list. It integrates with the TaskNotes CLI (tn) to list, create, update, complete, and organize tasks stored in Obsidian. Triggers on keywords like "task", "todo", "任务", "工作", "待办", "Obsidian", or when users ask about their schedule, deadlines, or what they need to do.
---

# TaskNotes CLI Skill

Manage tasks in Obsidian using the TaskNotes CLI (`tn`) tool.

## When to Use

Activate this skill when users:
- Ask about their tasks, todos, or work items
- Want to see what they need to do today or this week
- Need to create, update, or complete tasks
- Mention keywords: task, todo, 任务, 工作, 待办, Obsidian, 日程, deadline, overdue
- Ask questions like "我今天要做什么", "有什么任务", "帮我看看工作进度"

## Core Commands

### List Tasks

```bash
# List active tasks (default limit: 20)
tn list --limit 10

# Today's tasks
tn list --today

# Overdue tasks
tn list --overdue

# Completed tasks
tn list --completed

# JSON output (for parsing)
tn list --json --limit 10
```

### Filter Tasks

Use `--filter` for advanced queries:

```bash
# By status
tn list --filter "status:in-progress"
tn list --filter "status:done"

# By priority
tn list --filter "priority:high"

# By context (工作/学习/生活)
tn list --filter "contexts:@工作"

# By project
tn list --filter "projects:拓扑灵犀"

# Combined filters
tn list --filter "priority:high AND status:in-progress"
tn list --filter "(status:in-progress OR status:open) AND contexts:@工作"

# Date-based
tn list --filter "due:before:2026-01-25"
```

**Available Statuses**: open, deep-research, plan-mode, in-progress, done, pending

**Available Priorities**: none, low, normal, high

**Available Contexts**: @@学习, @@工作, @@生活, @work, @cleanup

### Search Tasks

```bash
tn search "关键词"
```

### Create Tasks

**⚠️ 重要**: `tn create` 的自然语言解析功能**不稳定**，可能会把 `due:today` 等关键字直接写入标题而非 frontmatter。

**推荐做法**: 先创建任务（仅标题），然后用 `tn update` 设置属性：

```bash
# 推荐方式：分两步创建
tn create "完成项目报告"
tn update "Calendar/Tasks/完成项目报告.md" --due tomorrow --priority high

# 或者一行完成（先创建再更新）
tn create "开会讨论需求" && tn update "Calendar/Tasks/开会讨论需求.md" --scheduled 2026-01-25
```

**不推荐**（自然语言解析可能失败）：
```bash
# 可能导致 "due:tomorrow priority:high" 被写入标题
tn create "完成项目报告 due:tomorrow priority:high"
```

### Update Tasks

Task IDs are file paths like `Calendar/Tasks/任务名.md`

```bash
# Update status
tn update "Calendar/Tasks/任务名.md" --status in-progress
tn update "Calendar/Tasks/任务名.md" --status done

# Update priority
tn update "Calendar/Tasks/任务名.md" --priority high

# Update dates
tn update "Calendar/Tasks/任务名.md" --due 2026-01-30
tn update "Calendar/Tasks/任务名.md" --scheduled 2026-01-25

# Update title
tn update "Calendar/Tasks/任务名.md" --title "新的任务标题"

# Manage tags/contexts/projects
tn update "Calendar/Tasks/任务名.md" --add-tags "urgent,important"
tn update "Calendar/Tasks/任务名.md" --add-contexts "@工作"
tn update "Calendar/Tasks/任务名.md" --add-projects "项目名"
```

### Complete Tasks

```bash
tn complete "Calendar/Tasks/任务名.md"
```

### Toggle Task Status

```bash
tn toggle "Calendar/Tasks/任务名.md"
```

### Delete Tasks

```bash
tn delete "Calendar/Tasks/任务名.md" --force
```

### Archive Tasks

```bash
tn archive "Calendar/Tasks/任务名.md"
```

## Statistics & Projects

```bash
# Overall statistics
tn stats

# List projects
tn projects list

# Show project details
tn projects show "项目名"

# Project statistics
tn projects stats "项目名" --period month
```

## Time Tracking

```bash
# Start timer for a task
tn timer start --task "Calendar/Tasks/任务名.md"

# Stop timer
tn timer stop

# Check timer status
tn timer status

# View time log
tn timer log --period today
tn timer log --period week
```

## Pomodoro Timer

```bash
# Start pomodoro session
tn pomodoro start --task "Calendar/Tasks/任务名.md"
tn pomodoro start --duration 25

# Control pomodoro
tn pomodoro pause
tn pomodoro resume
tn pomodoro stop

# View stats
tn pomodoro status
tn pomodoro stats --week
tn pomodoro sessions --limit 10
```

## Filter Syntax Reference

| Property | Operators | Example |
|----------|-----------|---------|
| status | is, is-not | `status:in-progress` |
| priority | is, is-not | `priority:high` |
| tags | contains | `tags:urgent` |
| contexts | contains | `contexts:@工作` |
| projects | contains | `projects:项目名` |
| due | before, after, on-or-before | `due:before:2026-01-25` |
| scheduled | before, after | `scheduled:after:2026-01-20` |
| title | contains | `title:contains:"会议"` |
| archived | checked, not-checked | `archived:not-checked` |

**Logical Operators**: AND, OR, parentheses for grouping

## Workflow Guidelines

1. **Start of day**: Run `tn list --today` or `tn list --overdue` to check pending work
2. **Before starting work**: Update task status to `in-progress`
3. **When blocked**: Update status to `pending` or add context
4. **After completion**: Run `tn complete <taskId>` to mark done
5. **Weekly review**: Run `tn stats` and `tn projects list` to review progress

## Notes

- Task IDs are Obsidian file paths relative to vault root
- Suppress deprecation warnings by redirecting stderr: `2>/dev/null`
- Use `--json` flag for programmatic parsing
- Vault location: `/Users/cdd/Documents/notes/oldwinter-notes`
