---
name: browserbase
description: Cloud browser infrastructure for AI agents - create sessions, persist contexts, and automate browsers
vm0_secrets:
  - BROWSERBASE_API_KEY
  - BROWSERBASE_PROJECT_ID
---

# Browserbase

Cloud browser infrastructure for AI agents and automation. Create browser sessions, persist authentication with contexts, debug live sessions, and retrieve session recordings.

> Official docs: https://docs.browserbase.com/

---

## When to Use

Use this skill when you need to:

- Create cloud browser sessions for Playwright/Puppeteer automation
- Persist login state and cookies across sessions using Contexts
- Debug browser sessions in real-time with live URLs
- Retrieve session recordings and logs for debugging
- Manage browser sessions programmatically (list, get, update)
- Run browser automation with proxy and stealth support

---

## Prerequisites

1. Create an account at https://www.browserbase.com/
2. Get your API Key from the dashboard Settings page
3. Get your Project ID from the dashboard Settings page

Set environment variables:

```bash
export BROWSERBASE_API_KEY="your-api-key-here"
export BROWSERBASE_PROJECT_ID="your-project-id-here"
```

> **Note:** Free plans have a concurrent session limit of 1. You'll receive a 429 error if you exceed this limit. Check your plan details in the Browserbase dashboard.

---

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
> ```

## How to Use

### 1. Create a Session

Create a new browser session:

Write `/tmp/request.json`:
```json
{
  "projectId": "<your-project-id>"
}
```

```bash
bash -c 'curl -s -X POST "https://api.browserbase.com/v1/sessions" --header "Content-Type: application/json" --header "X-BB-API-Key: $BROWSERBASE_API_KEY" -d @/tmp/request.json'
```

**With timeout and keepAlive:**

Write `/tmp/request.json`:
```json
{
  "projectId": "<your-project-id>",
  "timeout": 300,
  "keepAlive": true
}
```

```bash
bash -c 'curl -s -X POST "https://api.browserbase.com/v1/sessions" --header "Content-Type: application/json" --header "X-BB-API-Key: $BROWSERBASE_API_KEY" -d @/tmp/request.json'
```

**With proxy enabled (requires paid plan):**

Write `/tmp/request.json`:
```json
{
  "projectId": "<your-project-id>",
  "proxies": true
}
```

```bash
bash -c 'curl -s -X POST "https://api.browserbase.com/v1/sessions" --header "Content-Type: application/json" --header "X-BB-API-Key: $BROWSERBASE_API_KEY" -d @/tmp/request.json'
```

> **Note:** Proxies are not available on the free plan. You'll receive a 402 error if you try to use this feature without upgrading.

**With specific region (us-west-2, us-east-1, eu-central-1, ap-southeast-1):**

Write `/tmp/request.json`:
```json
{
  "projectId": "<your-project-id>",
  "region": "us-west-2"
}
```

```bash
bash -c 'curl -s -X POST "https://api.browserbase.com/v1/sessions" --header "Content-Type: application/json" --header "X-BB-API-Key: $BROWSERBASE_API_KEY" -d @/tmp/request.json'
```

**Response includes:**
- `id` - Session ID to use for connections
- `connectUrl` - WebSocket URL for Playwright/Puppeteer
- `seleniumRemoteUrl` - URL for Selenium connections
- `signingKey` - Key for HTTP connections

### 2. List Sessions

List all sessions with optional filters:

```bash
bash -c 'curl -s -X GET "https://api.browserbase.com/v1/sessions" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
```

**Filter by status (RUNNING, ERROR, TIMED_OUT, COMPLETED):**

```bash
bash -c 'curl -s -X GET "https://api.browserbase.com/v1/sessions?status=RUNNING" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
```

**Query by user metadata:**

> **Note:** The query syntax for user metadata filtering uses single quotes: `user_metadata['key']:'value'`. To avoid complex shell escaping, write the query to a file and use `--data-urlencode "q@filename"`.

Write `/tmp/query.txt` with content:
```
user_metadata['test']:'true'
```

Then query sessions:
```bash
bash -c 'curl -s -X GET -G "https://api.browserbase.com/v1/sessions" --data-urlencode "q@/tmp/query.txt" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
```

**More examples:**

Query by stagehand metadata - write `/tmp/query.txt`:
```
user_metadata['stagehand']:'true'
```

Query by environment - write `/tmp/query.txt`:
```
user_metadata['env']:'production'
```

Then run:
```bash
bash -c 'curl -s -X GET -G "https://api.browserbase.com/v1/sessions" --data-urlencode "q@/tmp/query.txt" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
```

### 3. Get Session Details

Get details of a specific session. Replace `<your-session-id>` with the actual session ID:

```bash
bash -c 'curl -s -X GET "https://api.browserbase.com/v1/sessions/<your-session-id>" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
```

### 4. Update Session (Release)

Request to release a session before its timeout to avoid additional charges. Replace `<your-session-id>` with the actual session ID:

Write `/tmp/request.json`:
```json
{
  "status": "REQUEST_RELEASE"
}
```

```bash
bash -c 'curl -s -X POST "https://api.browserbase.com/v1/sessions/<your-session-id>" --header "Content-Type: application/json" --header "X-BB-API-Key: $BROWSERBASE_API_KEY" -d @/tmp/request.json'
```

The session status will change to `COMPLETED` and `endedAt` timestamp will be set.

### 5. Get Debug/Live URLs

Get live debugging URLs for a running session. Replace `<your-session-id>` with the actual session ID:

```bash
bash -c 'curl -s -X GET "https://api.browserbase.com/v1/sessions/<your-session-id>/debug" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
```

> **Note:** Debug URLs may only be available after a browser client has connected to the session via WebSocket.

**Response includes:**
- `debuggerUrl` - Chrome DevTools debugger URL
- `debuggerFullscreenUrl` - Fullscreen debugger view
- `wsUrl` - WebSocket URL
- `pages` - Array of open pages with their debugger URLs

### 6. Get Session Logs

Retrieve logs from a session. Replace `<your-session-id>` with the actual session ID:

```bash
bash -c 'curl -s -X GET "https://api.browserbase.com/v1/sessions/<your-session-id>/logs" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
```

### 7. Get Session Recording

Get the rrweb recording of a session. Replace `<your-session-id>` with the actual session ID:

```bash
bash -c 'curl -s -X GET "https://api.browserbase.com/v1/sessions/<your-session-id>/recording" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
```

### 8. Get Session Downloads

Retrieve files downloaded during a session (returns ZIP file). Replace `<your-session-id>` with the actual session ID:

```bash
bash -c 'curl -s -X GET "https://api.browserbase.com/v1/sessions/<your-session-id>/downloads" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"' --output downloads.zip
```

### 9. Upload Files to Session

Upload files to use in a browser session. Replace `<your-session-id>` with the actual session ID:

```bash
bash -c 'curl -s -X POST "https://api.browserbase.com/v1/sessions/<your-session-id>/uploads" --header "X-BB-API-Key: $BROWSERBASE_API_KEY" -F "file=@/path/to/file.pdf"'
```

---

## Contexts API

Contexts allow you to persist cookies, cache, and session storage across multiple browser sessions.

### Create a Context

Write `/tmp/request.json`:
```json
{
  "projectId": "<your-project-id>"
}
```

```bash
bash -c 'curl -s -X POST "https://api.browserbase.com/v1/contexts" --header "Content-Type: application/json" --header "X-BB-API-Key: $BROWSERBASE_API_KEY" -d @/tmp/request.json'
```

Save the returned `id` to use in sessions.

### Get Context Details

Retrieve details of a specific context. Replace `<your-context-id>` with the actual context ID:

```bash
bash -c 'curl -s -X GET "https://api.browserbase.com/v1/contexts/<your-context-id>" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
```

**Response includes:**
- `id` - Context identifier
- `createdAt` - Creation timestamp
- `updatedAt` - Last update timestamp
- `projectId` - The Project ID linked to the context

### Create Session with Context

Use an existing context to restore cookies and login state. Replace `<your-context-id>` with the actual context ID:

Write `/tmp/request.json`:
```json
{
  "projectId": "<your-project-id>",
  "browserSettings": {
    "context": {
      "id": "<your-context-id>",
      "persist": true
    }
  }
}
```

```bash
bash -c 'curl -s -X POST "https://api.browserbase.com/v1/sessions" --header "Content-Type: application/json" --header "X-BB-API-Key: $BROWSERBASE_API_KEY" -d @/tmp/request.json'
```

Set `persist: true` to save updates back to the context after the session ends.

### Delete Context

Delete a context when it's no longer needed. Replace `<your-context-id>` with the actual context ID:

```bash
bash -c 'curl -s -X DELETE "https://api.browserbase.com/v1/contexts/<your-context-id>" --header "X-BB-API-Key: $BROWSERBASE_API_KEY" -w "\nHTTP Status: %{http_code}"'
```

Successful deletion returns HTTP 204 (No Content).

---

## Projects API

### Get Project Usage

Retrieve project-wide usage statistics (browser minutes and proxy bytes). Replace `<your-project-id>` with your actual project ID:

```bash
bash -c 'curl -s -X GET "https://api.browserbase.com/v1/projects/<your-project-id>/usage" --header "X-BB-API-Key: $BROWSERBASE_API_KEY"'
```

---

## API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/sessions` | POST | Create a new browser session |
| `/v1/sessions` | GET | List all sessions |
| `/v1/sessions/{id}` | GET | Get session details (returns array) |
| `/v1/sessions/{id}` | POST | Update session (release) |
| `/v1/sessions/{id}/debug` | GET | Get live debug URLs |
| `/v1/sessions/{id}/logs` | GET | Get session logs |
| `/v1/sessions/{id}/recording` | GET | Get session recording (rrweb) |
| `/v1/sessions/{id}/downloads` | GET | Get downloaded files (ZIP) |
| `/v1/sessions/{id}/uploads` | POST | Upload files to session |
| `/v1/contexts` | POST | Create a new context |
| `/v1/contexts/{id}` | GET | Get context details |
| `/v1/contexts/{id}` | DELETE | Delete a context |
| `/v1/projects/{id}/usage` | GET | Get project usage stats |

---

## Session Status Values

| Status | Description |
|--------|-------------|
| `RUNNING` | Session is currently active |
| `COMPLETED` | Session ended successfully |
| `ERROR` | Session ended with an error |
| `TIMED_OUT` | Session exceeded timeout |
| `REQUEST_RELEASE` | Request to end session |

---

## Guidelines

1. **Session Lifecycle**: Sessions auto-terminate after timeout (default 5 minutes). Use `keepAlive: true` for longer sessions.
2. **Contexts**: Use contexts to persist login state and avoid repeated authentication.
3. **Proxies**: Enable proxies for geo-restricted content or to avoid rate limiting.
4. **Regions**: Choose a region close to your target websites for better performance.
5. **Debug URLs**: Use debug URLs for real-time human-in-the-loop debugging.
6. **Recordings**: Session replays use rrweb DOM reconstruction, not video files.
7. **Rate Limits**: Check your plan limits in the Browserbase dashboard.
