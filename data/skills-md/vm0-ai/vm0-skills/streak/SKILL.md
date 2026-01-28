---
name: streak
description: Gmail-integrated CRM for managing pipelines, deals (boxes), contacts, and email threads
vm0_secrets:
  - STREAK_API_KEY
---

# Streak CRM

Streak is a CRM built entirely inside Gmail. Use this skill to manage pipelines, boxes (deals), contacts, organizations, tasks, and email threads via the Streak API.

> Official docs: `https://streak.readme.io/reference`

---

## When to Use

Use this skill when you need to:

- Manage sales pipelines and deal stages
- Track leads, contacts, and organizations
- Associate email threads with deals
- Create tasks and comments on deals
- Search across boxes, contacts, and organizations

---

## Prerequisites

1. Install the Streak extension in Gmail
2. Navigate to Gmail > Streak icon > Integrations > Streak API > Create New Key
3. Copy your API key

Set environment variable:

```bash
export STREAK_API_KEY="your-api-key"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

### Authentication

Streak uses HTTP Basic Auth with your API key as the username and no password. In curl, use `-u ${STREAK_API_KEY}:` (note the trailing colon).

---

### 1. Get Current User

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/users/me" -u "${STREAK_API_KEY}:"'
```

---

### 2. List All Pipelines

Pipelines represent business processes (Sales, Hiring, Projects, etc.).

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/pipelines" -u "${STREAK_API_KEY}:"'
```

---

### 3. Get a Pipeline

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/pipelines/{pipelineKey}" -u "${STREAK_API_KEY}:"'
```

---

### 4. Create a Pipeline

Write to `/tmp/streak_request.json`:

```json
{
  "name": "New Sales Pipeline"
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://api.streak.com/api/v1/pipelines" -u "${STREAK_API_KEY}:" --header "Content-Type: application/json" -d @/tmp/streak_request.json'
```

---

### 5. List Boxes in Pipeline

Boxes are the core data objects (deals, leads, projects) within a pipeline.

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/pipelines/{pipelineKey}/boxes" -u "${STREAK_API_KEY}:"'
```

---

### 6. Get a Box

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/boxes/{boxKey}" -u "${STREAK_API_KEY}:"'
```

---

### 7. Create a Box

Write to `/tmp/streak_request.json`:

```json
{
  "name": "Acme Corp Deal"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.streak.com/api/v1/pipelines/{pipelineKey}/boxes" -u "${STREAK_API_KEY}:" --header "Content-Type: application/json" -d @/tmp/streak_request.json'
```

---

### 8. Update a Box

Write to `/tmp/streak_request.json`:

```json
{
  "name": "Updated Deal Name",
  "stageKey": "stageKey123"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.streak.com/api/v1/boxes/{boxKey}" -u "${STREAK_API_KEY}:" --header "Content-Type: application/json" -d @/tmp/streak_request.json'
```

---

### 9. List Stages in Pipeline

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/pipelines/{pipelineKey}/stages" -u "${STREAK_API_KEY}:"'
```

---

### 10. List Fields in Pipeline

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/pipelines/{pipelineKey}/fields" -u "${STREAK_API_KEY}:"'
```

---

### 11. Get a Contact

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/contacts/{contactKey}" -u "${STREAK_API_KEY}:"'
```

---

### 12. Create a Contact

Write to `/tmp/streak_request.json`:

```json
{
  "teamKey": "teamKey123",
  "emailAddresses": ["john@example.com"],
  "givenName": "John",
  "familyName": "Doe"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.streak.com/api/v1/contacts" -u "${STREAK_API_KEY}:" --header "Content-Type: application/json" -d @/tmp/streak_request.json'
```

---

### 13. Get an Organization

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/organizations/{organizationKey}" -u "${STREAK_API_KEY}:"'
```

---

### 14. Search Boxes, Contacts, and Organizations

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/search?query=acme" -u "${STREAK_API_KEY}:"'
```

---

### 15. Get Tasks in a Box

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/boxes/{boxKey}/tasks" -u "${STREAK_API_KEY}:"'
```

---

### 16. Create a Task

Write to `/tmp/streak_request.json`:

```json
{
  "text": "Follow up with client",
  "dueDate": 1735689600000
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.streak.com/api/v1/boxes/{boxKey}/tasks" -u "${STREAK_API_KEY}:" --header "Content-Type: application/json" -d @/tmp/streak_request.json'
```

---

### 17. Get Comments in a Box

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/boxes/{boxKey}/comments" -u "${STREAK_API_KEY}:"'
```

---

### 18. Create a Comment

Write to `/tmp/streak_request.json`:

```json
{
  "message": "Spoke with client today, they are interested."
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.streak.com/api/v1/boxes/{boxKey}/comments" -u "${STREAK_API_KEY}:" --header "Content-Type: application/json" -d @/tmp/streak_request.json'
```

---

### 19. Get Threads in a Box

Email threads associated with a box.

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/boxes/{boxKey}/threads" -u "${STREAK_API_KEY}:"'
```

---

### 20. Get Files in a Box

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/boxes/{boxKey}/files" -u "${STREAK_API_KEY}:"'
```

---

### 21. Get Meetings in a Box

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/boxes/{boxKey}/meetings" -u "${STREAK_API_KEY}:"'
```

---

### 22. Create a Meeting Note

Write to `/tmp/streak_request.json`:

```json
{
  "meetingDate": 1735689600000,
  "meetingNotes": "Discussed pricing and timeline.",
  "title": "Sales Call"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.streak.com/api/v1/boxes/{boxKey}/meetings" -u "${STREAK_API_KEY}:" --header "Content-Type: application/json" -d @/tmp/streak_request.json'
```

---

### 23. Get Box Timeline

```bash
bash -c 'curl -s -X GET "https://api.streak.com/api/v1/boxes/{boxKey}/timeline" -u "${STREAK_API_KEY}:"'
```

---

## Guidelines

1. **Keys**: Pipeline keys, box keys, and other identifiers are alphanumeric strings returned by the API
2. **Timestamps**: Use Unix timestamps in milliseconds for date fields (e.g., `dueDate`, `meetingDate`)
3. **Rate Limits**: Be mindful of API rate limits; add delays between bulk operations
4. **Stages**: To move a box to a different stage, update the box with the new `stageKey`
5. **Email Integration**: Streak is tightly integrated with Gmail; threads are Gmail thread IDs
6. **Team Key**: When creating contacts, you need a `teamKey` which can be obtained from the teams endpoint
