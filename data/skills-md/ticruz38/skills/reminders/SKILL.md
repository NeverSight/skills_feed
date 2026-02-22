---
name: reminders
description: "Local reminder system with natural language scheduling"
version: 1.0.0
author: OpenClaw
entry: ./dist/cli.js
type: script
---

# Reminders Skill

Set and manage one-time or recurring reminders. Stores all data locally in SQLite. No external APIs required.

## Features

- **One-time reminders**: Set reminders for specific dates/times
- **Recurring reminders**: Daily, weekly, or monthly recurring reminders
- **Natural language parsing**: "in 2 hours", "tomorrow", "14:30"
- **Snooze functionality**: Temporarily dismiss reminders
- **Daemon mode**: Check for due reminders (for cron/systemd integration)
- **SQLite storage**: All data stored locally

## Capabilities

### Add a one-time reminder

```bash
npx reminders add "<datetime>" "<message>"
```

**Datetime formats:**
- `"2026-02-15 14:00"` - Specific date and time
- `"tomorrow"` - Tomorrow at current time
- `"in 2 hours"` - Relative time
- `"in 30 minutes"` - Relative time in minutes
- `"in 3 days"` - Relative time in days
- `"14:30"` - Today at specific time (or tomorrow if passed)

**Examples:**
```bash
npx reminders add "in 30 minutes" "Call mom"
npx reminders add "tomorrow" "Dentist appointment"
npx reminders add "2026-02-15 09:00" "Team meeting"
npx reminders add "14:30" "Standup meeting"
```

### Add a recurring reminder

```bash
npx reminders recurring <type> "<time>" "<message>"
```

**Types:** `daily`, `weekly`, `monthly`

**Examples:**
```bash
npx reminders recurring daily "09:00" "Take vitamins"
npx reminders recurring weekly "Monday 10:00" "Weekly review"
npx reminders recurring monthly "1st 12:00" "Pay rent"
```

### List reminders

```bash
npx reminders list                    # List pending reminders
npx reminders list --all              # Include completed
npx reminders list --limit 20         # Limit results
```

### List due reminders

```bash
npx reminders due                     # Show reminders that are due now
```

### Get reminder details

```bash
npx reminders get <id>
```

### Complete a reminder

```bash
npx reminders complete <id>
```

For recurring reminders, this schedules the next occurrence. For one-time reminders, it moves to history.

### Snooze a reminder

```bash
npx reminders snooze <id> <minutes>
```

**Example:**
```bash
npx reminders snooze 123 30          # Snooze for 30 minutes
```

### Delete a reminder

```bash
npx reminders delete <id>
```

### View history

```bash
npx reminders history                 # Show completed reminders
npx reminders history --limit 50      # Show last 50
```

### View statistics

```bash
npx reminders stats                   # Show pending, completed, overdue counts
```

### Daemon mode

Check for due reminders (for use with cron or systemd):

```bash
npx reminders daemon                  # Output JSON with due reminders
```

**Cron example:**
```cron
# Check for reminders every minute
* * * * * /usr/bin/node /path/to/dist/cli.js daemon | some-notifier
```

### Health check

```bash
npx reminders health                  # Check database status
```

### Test natural language parsing

```bash
npx reminders parse "in 2 hours"      # Test how a datetime string is parsed
```

## Storage

SQLite database at `~/.openclaw/skills/reminders/reminders.db`:

- `reminders` - All active reminders with schedule info
- `history` - Completed one-time reminders

## API Usage

```typescript
import { RemindersSkill } from '@openclaw/reminders';

const reminders = new RemindersSkill();

// Add a one-time reminder
const reminder = await reminders.addReminder({
  message: "Call mom",
  scheduledAt: new Date("2026-02-15T14:00:00"),
});

// Parse natural language datetime
const when = reminders.parseNaturalDateTime("in 2 hours");
await reminders.addReminder({
  message: "Take a break",
  scheduledAt: when,
});

// Add recurring reminder
await reminders.addRecurringReminder({
  message: "Take vitamins",
  type: "daily",
});

// List due reminders
const due = await reminders.getDueReminders();

// Complete a reminder
await reminders.completeReminder(reminder.id);

// Snooze for 30 minutes
await reminders.snoozeReminder(reminder.id, 30);

// Close connection
await reminders.close();
```

## No External Dependencies

This skill works entirely offline:
- No API keys required
- No external services
- All data stored in local SQLite
- Natural language parsing is done locally
