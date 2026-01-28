---
name: cronlytic
description: Cronlytic cron job scheduler API via curl. Use this skill to create, manage, pause/resume scheduled HTTP requests and webhook automation.
vm0_secrets:
  - CRONLYTIC_API_KEY
vm0_vars:
  - CRONLYTIC_USER_ID
---

# Cronlytic

Use Cronlytic via direct `curl` calls to **schedule and manage cron jobs** that trigger HTTP requests/webhooks.

> Official docs: `https://www.cronlytic.com/api-documentation`

---

## When to Use

Use this skill when you need to:

- **Schedule recurring HTTP requests** (webhooks, API calls)
- **Automate background tasks** without managing servers
- **Create cron jobs** with standard 5-field expressions
- **Pause/resume jobs** dynamically
- **Monitor job execution** via logs

---

## Prerequisites

1. Sign up at [Cronlytic](https://www.cronlytic.com/signup)
2. Go to Dashboard → API Keys → Generate New API Key
3. Copy your API Key and User ID

```bash
export CRONLYTIC_API_KEY="your-api-key"
export CRONLYTIC_USER_ID="your-user-id"
```

### Base URL

```
https://api.cronlytic.com/prog/
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## How to Use

---

### 1. Health Check (Ping)

Check if API is available (no auth required):

```bash
bash -c 'curl -s -X GET "https://api.cronlytic.com/prog/ping"'
```

Response: `{"message": "pong"}`

---

### 2. Create a Cron Job

Create a scheduled job to call a webhook.

Write to `/tmp/cronlytic_request.json`:

```json
{
  "name": "daily-backup",
  "url": "https://api.example.com/backup",
  "method": "POST",
  "headers": {"Authorization": "Bearer token123"},
  "body": "{\"type\": \"full\"}",
  "cron_expression": "0 2 * * *"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.cronlytic.com/prog/jobs" -H "X-API-Key: ${CRONLYTIC_API_KEY}" -H "X-User-ID: ${CRONLYTIC_USER_ID}" -H "Content-Type: application/json" -d @/tmp/cronlytic_request.json' | jq '{job_id, name, status, next_run_at}'
```

---

### 3. Create GET Request Job

Simple health check every 5 minutes.

Write to `/tmp/cronlytic_request.json`:

```json
{
  "name": "health-check",
  "url": "https://api.example.com/health",
  "method": "GET",
  "headers": {},
  "body": "",
  "cron_expression": "*/5 * * * *"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.cronlytic.com/prog/jobs" -H "X-API-Key: ${CRONLYTIC_API_KEY}" -H "X-User-ID: ${CRONLYTIC_USER_ID}" -H "Content-Type: application/json" -d @/tmp/cronlytic_request.json' | jq '{name, status}'
```

---

### 4. List All Jobs

Get all your scheduled jobs:

```bash
bash -c 'curl -s -X GET "https://api.cronlytic.com/prog/jobs" -H "X-API-Key: ${CRONLYTIC_API_KEY}" -H "X-User-ID: ${CRONLYTIC_USER_ID}"' | jq '.[] | {job_id, name, status, cron_expression, next_run_at}'
```

---

### 5. Update a Job

Update an existing job (all fields required). Replace `<your-job-id>` with the actual job ID:

Write to `/tmp/cronlytic_request.json`:

```json
{
  "name": "daily-backup-v2",
  "url": "https://api.example.com/backup/v2",
  "method": "POST",
  "headers": {"Authorization": "Bearer newtoken"},
  "body": "{\"type\": \"incremental\"}",
  "cron_expression": "0 3 * * *"
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://api.cronlytic.com/prog/jobs/<your-job-id>" -H "X-API-Key: ${CRONLYTIC_API_KEY}" -H "X-User-ID: ${CRONLYTIC_USER_ID}" -H "Content-Type: application/json" -d @/tmp/cronlytic_request.json' | jq '{job_id, name, status, next_run_at}'
```

---

### 6. Pause a Job

Stop a job from executing. Replace `<your-job-id>` with the actual job ID:

```bash
bash -c 'curl -s -X POST "https://api.cronlytic.com/prog/jobs/<your-job-id>/pause" -H "X-API-Key: ${CRONLYTIC_API_KEY}" -H "X-User-ID: ${CRONLYTIC_USER_ID}"'
```

---

### 7. Resume a Job

Resume a paused job. Replace `<your-job-id>` with the actual job ID:

```bash
bash -c 'curl -s -X POST "https://api.cronlytic.com/prog/jobs/<your-job-id>/resume" -H "X-API-Key: ${CRONLYTIC_API_KEY}" -H "X-User-ID: ${CRONLYTIC_USER_ID}"'
```

---

### 8. Get Job Logs

View execution history (last 50 entries). Replace `<your-job-id>` with the actual job ID:

```bash
bash -c 'curl -s -X GET "https://api.cronlytic.com/prog/jobs/<your-job-id>/logs" -H "X-API-Key: ${CRONLYTIC_API_KEY}" -H "X-User-ID: ${CRONLYTIC_USER_ID}"' | jq '.logs[] | {timestamp, status, response_code, response_time}'
```

---

### 9. Delete a Job

Permanently delete a job and its logs. Replace `<your-job-id>` with the actual job ID:

```bash
bash -c 'curl -s -X DELETE "https://api.cronlytic.com/prog/jobs/<your-job-id>" -H "X-API-Key: ${CRONLYTIC_API_KEY}" -H "X-User-ID: ${CRONLYTIC_USER_ID}"'
```

---

## Cron Expression Format

Standard 5-field cron: `minute hour day month day-of-week`

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * *
```

### Common Examples

| Expression | Description |
|------------|-------------|
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour at minute 0 |
| `0 9 * * *` | Daily at 9:00 AM |
| `0 9 * * 1-5` | Weekdays at 9:00 AM |
| `0 0 1 * *` | First day of month at midnight |
| `30 14 * * 0` | Sunday at 2:30 PM |
| `0 */6 * * *` | Every 6 hours |

---

## Job Status Values

| Status | Description |
|--------|-------------|
| `pending` | Scheduled, waiting for next_run_at |
| `paused` | Paused, won't execute |
| `success` | Last execution succeeded |
| `failed` | Last execution failed |
| `quota_reached` | Skipped due to plan quota |

---

## Create Job Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Job name (1-50 chars, alphanumeric/-/_) |
| `url` | string | Yes | Target URL (HTTP/HTTPS) |
| `method` | string | Yes | HTTP method (GET, POST, PUT, DELETE) |
| `headers` | object | Yes | Request headers (can be `{}`) |
| `body` | string | Yes | Request body (can be `""`) |
| `cron_expression` | string | Yes | 5-field cron expression |

### Job Name Rules

- Only letters, numbers, hyphens (`-`), underscores (`_`)
- Length: 1-50 characters
- Regex: `^[a-zA-Z0-9_-]+$`

**Valid:** `my-job`, `test_job_1`, `API-Health-Check`
**Invalid:** `my job` (space), `test@job` (@), `api.health` (.)

---

## Response Fields

| Field | Description |
|-------|-------------|
| `job_id` | Unique job identifier |
| `name` | Job name |
| `url` | Target URL |
| `method` | HTTP method |
| `status` | Current job status |
| `cron_expression` | Schedule expression |
| `next_run_at` | Next scheduled execution (ISO timestamp) |
| `created_at` | Creation timestamp |

---

## Guidelines

1. **Ping first**: Call `/ping` to warm up the API (Lambda cold start)
2. **All fields required**: When creating/updating, provide all fields
3. **Valid cron only**: Use standard 5-field cron format
4. **Job names**: Use alphanumeric with hyphens/underscores only
5. **Check logs**: Use the logs endpoint to debug failed jobs
6. **Dashboard**: Use https://www.cronlytic.com/dashboard for visual management
7. **Plan limits**: Free tier has job limits - upgrade if needed
