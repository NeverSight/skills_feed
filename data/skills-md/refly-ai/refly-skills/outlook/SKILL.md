---
name: outlook
description: "Integrate with Microsoft Outlook for email. Use when you need to: (1) send and manage emails, (2) create calendar events, or (3) automate email communication workflows."
version: 1.0.0
skillId: skp-e7yge6th72mkony9odceglg9
workflowId: c-ijhh2q58vevqx5aq2ynciwrx
installationId: skpi-p7fc1qhsbq4qo59qh99ibjk9
category: action
---

# Outlook

Integrate with Microsoft Outlook for email. Use when you need to: (1) send and manage emails, (2) create calendar events, or (3) automate email communication workflows.

## Input

Provide input as JSON:

```json
{
  "recipient_email": "Email address of the recipient",
  "email_subject": "Subject line for the email",
  "email_body": "Content of the email message",
  "event_title": "Title of the calendar event",
  "event_start_time": "Start time of the event (e.g., 2024-03-15T10:00:00)",
  "event_duration": "Duration of the event in minutes",
  "event_attendees": "Email addresses of attendees (comma-separated)"
}
```

## Execution (Pattern C: Action)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-p7fc1qhsbq4qo59qh99ibjk9 --input '{
  "to": "recipient@example.com",
  "subject": "Meeting Follow-up",
  "body": "Thank you for attending the meeting."
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-ijhh2q58vevqx5aq2ynciwrx"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Confirm Action Status

```bash
# Confirm email sent
STATUS=$(refly workflow detail "$RUN_ID" | jq -r '.payload.status')
echo "Action completed with status: $STATUS"
```

## Expected Output

- **Type**: API Response
- **Format**: JSON email confirmation
- **Action**: Confirm email sent successfully

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
