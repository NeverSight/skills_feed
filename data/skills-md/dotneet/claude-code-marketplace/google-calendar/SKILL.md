---
name: google-calendar
description: Accesses the Google Calendar and Tasks API. Use this skill to view or manage calendars, events, schedules, or Google tasks.
---

# Google Calendar + Tasks Access

## Quick start

- Create a Google Cloud OAuth client (Desktop app) and save the credentials JSON to `~/.config/google-calendar/credentials.json`.
- Install dependencies (venv recommended):
  ```bash
  python3 -m venv ~/.config/google-calendar/venv
  ~/.config/google-calendar/venv/bin/pip install -r <skill_dir>/scripts/requirements.txt
  ```
- Authenticate and store a token:
  - Calendar only:
    - `<skill_dir>/scripts/gcal-auth`
  - Tasks only:
    - `<skill_dir>/scripts/gcal-auth --scopes https://www.googleapis.com/auth/tasks`
  - Calendar + Tasks (single token):
    - `<skill_dir>/scripts/gcal-auth --scopes https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/tasks`
- Call the API:
  - `<skill_dir>/scripts/gcal list-calendars`

## Credentials and tokens

- Credentials are expected at `~/.config/google-calendar/credentials.json` by default.
- Tokens are stored at `~/.config/google-calendar/token.json` by default.
- Use `--token` or `GCAL_TOKEN_PATH` to switch accounts or isolate environments.

## Date/time rules

- Use RFC3339 for timed events (e.g., `2026-01-22T10:00:00-08:00`).
- Use `YYYY-MM-DD` for all-day events and set `end` to the next day (exclusive).
- Set `--time-zone` when the datetime has no offset.

## Common commands

- List calendars:
  - `<skill_dir>/scripts/gcal list-calendars`
- List events:
  - `<skill_dir>/scripts/gcal list-events --calendar-id primary --time-min 2026-01-22T00:00:00-08:00 --time-max 2026-01-22T23:59:59-08:00`
- Search events:
  - `<skill_dir>/scripts/gcal list-events --calendar-id primary --q "standup" --time-min ... --time-max ...`
- Create event (simple):
  - `<skill_dir>/scripts/gcal create-event --calendar-id primary --summary "Review" --start 2026-01-22T10:00:00-08:00 --end 2026-01-22T11:00:00-08:00`
- Update event (simple):
  - `<skill_dir>/scripts/gcal update-event --calendar-id primary --event-id <id> --summary "New title"`
- Delete event:
  - `<skill_dir>/scripts/gcal delete-event --calendar-id primary --event-id <id>`
- Free/busy:
  - `<skill_dir>/scripts/gcal freebusy --calendars primary,team@company.com --time-min ... --time-max ...`
- List task lists:
  - `<skill_dir>/scripts/gcal list-tasklists`
- List tasks:
  - `<skill_dir>/scripts/gcal list-tasks --tasklist <tasklist_id>`
- Create task:
  - `<skill_dir>/scripts/gcal create-task --tasklist <tasklist_id> --title "Buy milk" --due 2026-01-22T10:00:00-08:00`
- Update task:
  - `<skill_dir>/scripts/gcal update-task --tasklist <tasklist_id> --task-id <id> --notes "Bring receipt"`
- Delete task:
  - `<skill_dir>/scripts/gcal delete-task --tasklist <tasklist_id> --task-id <id>`

## Advanced usage

- Use `call` to hit any Calendar API endpoint:
  - `<skill_dir>/scripts/gcal call GET /users/me/calendarList`
  - `<skill_dir>/scripts/gcal call POST /calendars/primary/events --body-file /path/to/event.json`
- Use `--body-file` or `--body` (JSON string) for complex payloads (attendees, recurrence, conferenceData).
- Run multiple accounts by using different token files with `--token`.

## Safety

- Confirm intent before creating, updating, or deleting events.
- Keep OAuth credentials and token files out of git.
