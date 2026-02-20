---
name: macos-calendar
description: Create, list, and manage macOS Calendar events via AppleScript. Use when the user asks to add a reminder, schedule an event, create a calendar entry, set a deadline, or anything involving Apple Calendar on macOS. Triggers on requests like "remind me in 3 days", "add to my calendar", "schedule a meeting next Monday at 2pm", "create a recurring weekly event". macOS only.
license: MIT
compatibility: Requires macOS with Calendar.app. Uses osascript (AppleScript) and python3 for JSON parsing.
metadata:
  author: lucaperret
  version: "1.2.0"
  openclaw:
    os: macos
    emoji: "\U0001F4C5"
    homepage: https://github.com/lucaperret/agent-skills
    requires:
      bins:
        - osascript
        - python3
---

# macOS Calendar

Manage Apple Calendar events via `$SKILL_DIR/scripts/calendar.sh`. All date handling uses relative math (`current date + N * days`) to avoid locale issues (FR/EN/DE date formats).

## Quick start

### List calendars

Always list calendars first to find the correct calendar name:

```bash
"$SKILL_DIR/scripts/calendar.sh" list-calendars
```

### Create an event

```bash
echo '<json>' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

JSON fields:

| Field | Required | Default | Description |
|---|---|---|---|
| `summary` | yes | - | Event title |
| `calendar` | no | first calendar | Calendar name (from list-calendars) |
| `description` | no | "" | Event notes |
| `offset_days` | no | 0 | Days from today (0=today, 1=tomorrow, 7=next week) |
| `iso_date` | no | - | Absolute date `YYYY-MM-DD` (overrides offset_days) |
| `hour` | no | 9 | Start hour (0-23) |
| `minute` | no | 0 | Start minute (0-59) |
| `duration_minutes` | no | 30 | Duration |
| `alarm_minutes` | no | 0 | Alert N minutes before (0=no alarm) |
| `all_day` | no | false | All-day event |
| `recurrence` | no | - | iCal RRULE string. See [references/recurrence.md](references/recurrence.md) |

## Interpreting natural language

Map user requests to JSON fields:

| User says | JSON |
|---|---|
| "tomorrow at 2pm" | `offset_days: 1, hour: 14` |
| "in 3 days" | `offset_days: 3` |
| "next Monday at 10am" | Calculate offset_days from today to next Monday, `hour: 10` |
| "February 25 at 3:30pm" | `iso_date: "2026-02-25", hour: 15, minute: 30` |
| "every weekday at 9am" | `hour: 9, recurrence: "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"` |
| "remind me 1 hour before" | `alarm_minutes: 60` |
| "all day event on March 1" | `iso_date: "2026-03-01", all_day: true` |

For "next Monday", "next Friday" etc: compute the day offset using the current date. Use `date` command if needed:

```bash
# Days until next Monday (1=Monday)
target=1; today=$(date +%u); echo $(( (target - today + 7) % 7 ))
```


## Example prompts

These are real user prompts and the commands you should run:

**"Remind me to call the dentist in 2 days"**
```bash
"$SKILL_DIR/scripts/calendar.sh" list-calendars
```
Then:
```bash
echo '{"calendar":"Personnel","summary":"Call dentist","offset_days":2,"hour":9,"duration_minutes":15,"alarm_minutes":30}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**"Schedule a team sync every Tuesday at 2pm with a 10-min reminder"**
```bash
echo '{"calendar":"Work","summary":"Team sync","hour":14,"duration_minutes":60,"recurrence":"FREQ=WEEKLY;BYDAY=TU","alarm_minutes":10}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**"Block July 15 as a vacation day"**
```bash
echo '{"calendar":"Personnel","summary":"Vacances","iso_date":"2026-07-15","all_day":true}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**"I have a doctor appointment next Thursday at 3:30pm, remind me 1 hour before"**
```bash
# First compute offset_days to next Thursday (4=Thursday)
target=4; today=$(date +%u); offset=$(( (target - today + 7) % 7 )); [ "$offset" -eq 0 ] && offset=7
```
Then:
```bash
echo "{\"calendar\":\"Personnel\",\"summary\":\"Doctor appointment\",\"offset_days\":$offset,\"hour\":15,\"minute\":30,\"duration_minutes\":60,\"alarm_minutes\":60}" | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**"Set up a daily standup at 9am on weekdays for the next 4 weeks"**
```bash
echo '{"calendar":"Work","summary":"Daily standup","hour":9,"duration_minutes":15,"recurrence":"FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=20"}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

**"Add a biweekly 1-on-1 with my manager on Fridays at 11am"**
```bash
echo '{"calendar":"Work","summary":"1-on-1 Manager","hour":11,"duration_minutes":30,"recurrence":"FREQ=WEEKLY;INTERVAL=2;BYDAY=FR","alarm_minutes":5}' | "$SKILL_DIR/scripts/calendar.sh" create-event
```

## Critical rules

1. **Always list calendars first** if the user hasn't specified one — calendars marked `[read-only]` cannot be used for event creation
2. **Never use hardcoded date strings** in AppleScript — always use `offset_days` or `iso_date`
3. **Confirm the calendar name** with the user if multiple personal calendars exist
4. **Never target a `[read-only]` calendar** — the script will reject it with an error
5. **For recurring events**, consult [references/recurrence.md](references/recurrence.md) for RRULE syntax
6. **Pass JSON via stdin** — never as a CLI argument (avoids leaking data in process list)
7. **All fields are validated** by the script (type coercion, range checks, format validation) — invalid input is rejected with an error message
8. **All actions are logged** to `logs/calendar.log` with timestamp, command, calendar, and summary
