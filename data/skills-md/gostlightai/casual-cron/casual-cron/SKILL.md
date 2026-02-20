---
name: casual-cron
description: "Create Clawdbot cron jobs from natural language with strict run-guard rules. Use when: users ask to schedule reminders or messages (recurring or one-shot), especially via Telegram, or when they use /at or /every. Examples: 'Create a daily reminder at 8am', 'Remind me in 20 minutes', 'Send me a Telegram message at 3pm', '/every 2h'."
metadata: {"openclaw":{"emoji":"⏰","requires":{"bins":["python3","openclaw"],"env":["CRON_DEFAULT_CHANNEL"]}}}
---

# Casual Cron

Create Clawdbot cron jobs from natural language. Supports one-shot and repeating schedules with safe run-guard rules.

## Cron Run Guard (Hard Rules)

- When running inside a cron job: do NOT troubleshoot, do NOT restart gateway, and do NOT check time.
- Do NOT send acknowledgements or explanations.
- Output ONLY the exact message payload and then stop.

---

## How It Works

1. Agent detects scheduling intent from user message (or `/at` / `/every` command)
2. Parses: time, frequency, channel, destination, message
3. Builds `openclaw cron add` command with correct flags
4. Confirms parsed time, job name, and job id with user before executing

---

## Scheduling Rules

When a message starts with `/at` or `/every`, schedule via the CLI (NOT the cron tool API).

Use: `openclaw cron add`

### /at (one-shot)

- If user gives a clock time (e.g., "3pm"), convert to ISO with offset computed for America/New_York on that date (DST-safe).
- Prefer relative times for near-term reminders (e.g., `--at "20m"`).
- Use `--session isolated --message "Output exactly: <task>"`.
- Always include `--delete-after-run`.
- Always include `--deliver --channel <channel> --to <destination>`.

### /every (repeating)

- If interval: use `--every "<duration>"` (no timezone needed).
- If clock time: use `--cron "<expr>" --tz "America/New_York"`.
- Use `--session isolated --message "Output exactly: <task>"`.
- Always include `--deliver --channel <channel> --to <destination>`.

### Confirmation

- Always confirm parsed time, job name, and job id with the user before finalizing.

---

## Command Reference

One-shot (clock time, DST-aware):
```
openclaw cron add \
  --name "Reminder example" \
  --at "2026-01-28T15:00:00-05:00" \
  --session isolated \
  --message "Output exactly: <TASK>" \
  --deliver --channel telegram --to <TELEGRAM_CHAT_ID> \
  --delete-after-run
```

One-shot (relative time):
```
openclaw cron add \
  --name "Reminder in 20m" \
  --at "20m" \
  --session isolated \
  --message "Output exactly: <TASK>" \
  --deliver --channel telegram --to <TELEGRAM_CHAT_ID> \
  --delete-after-run
```

Repeating (clock time, DST-aware):
```
openclaw cron add \
  --name "Daily 3pm reminder" \
  --cron "0 15 * * *" --tz "America/New_York" \
  --session isolated \
  --message "Output exactly: <TASK>" \
  --deliver --channel telegram --to <TELEGRAM_CHAT_ID>
```

Repeating (interval):
```
openclaw cron add \
  --name "Every 2 hours" \
  --every "2h" \
  --session isolated \
  --message "Output exactly: <TASK>" \
  --deliver --channel telegram --to <TELEGRAM_CHAT_ID>
```

---

## Configuration

| Setting | Value |
|---------|-------|
| Default timezone | `America/New_York` (DST-aware) |
| Default channel | `telegram` (override via `CRON_DEFAULT_CHANNEL` env var) |
| Supported channels | telegram, whatsapp, slack, discord, signal |

---

## Supported Patterns

### Time Formats

| Input | Cron |
|-------|------|
| `8am` | `0 8 * * *` |
| `8:45pm` | `45 20 * * *` |
| `noon` | `0 12 * * *` |
| `midnight` | `0 0 * * *` |
| `14:30` | `30 14 * * *` |

### Frequencies

| Input | Behavior |
|-------|----------|
| `daily` / `every day` | Daily at specified time |
| `weekdays` / `mon-fri` | Mon-Fri at specified time |
| `mondays` / `every monday` | Weekly on Monday |
| `hourly` / `every hour` | Every hour at :00 |
| `every 2 hours` | `0 */2 * * *` |
| `weekly` | Weekly (defaults to Monday) |
| `monthly` | Monthly (1st of month) |

