---
name: reportei
description: Reportei marketing report generation API via curl. Use this skill to manage clients, reports, templates, integrations and webhooks for automated marketing analytics.
vm0_secrets:
  - REPORTEI_API_TOKEN
---

# Reportei

Use Reportei via direct `curl` calls to **generate and manage marketing reports** with automated analytics.

> Official docs: `https://app.reportei.com/docs/api`

---

## When to Use

Use this skill when you need to:

- **Retrieve company and template information**
- **List and manage client projects**
- **Generate and access marketing reports**
- **Manage integrations** (Google Analytics, Meta, etc.)
- **Set up webhooks** for automated notifications

---

## Prerequisites

1. Sign up at [Reportei](https://www.reportei.com/)
2. Go to Dashboard → Generate API Token
3. Copy your API token

```bash
export REPORTEI_API_TOKEN="your-api-token"
```

### Base URL

```
https://app.reportei.com/api/v1
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

---

### 1. Get Company Details

Retrieve details of your company associated with the token:

```bash
bash -c 'curl -s -X GET "https://app.reportei.com/api/v1/me" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}"'
```

Response:

```json
{
  "company": {
  "id": 1,
  "name": "Your Company",
  "logo": "logo.jpeg",
  "type": "agency",
  "potential_clients": "11-15",
  "company_specialty": "paid traffic"
  }
}
```

---

### 2. List Templates

Retrieve all report templates in your company:

```bash
bash -c 'curl -s -X GET "https://app.reportei.com/api/v1/templates" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}"' | jq '.data[] | {id, title, used_count}'
```

---

### 3. List Clients (Projects)

Retrieve all client projects:

```bash
bash -c 'curl -s -X GET "https://app.reportei.com/api/v1/clients" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}"'
```

---

### 4. Get Client Details

Retrieve details of a specific client. Replace `<your-client-id>` with the actual client ID:

```bash
bash -c 'curl -s -X GET "https://app.reportei.com/api/v1/clients/<your-client-id>" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}"'
```

---

### 5. List Client Reports

Get all reports for a specific client. Replace `<your-client-id>` with the actual client ID:

```bash
bash -c 'curl -s -X GET "https://app.reportei.com/api/v1/clients/<your-client-id>/reports" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}"'
```

---

### 6. Get Report Details

Retrieve details of a specific report. Replace `<your-report-id>` with the actual report ID:

```bash
bash -c 'curl -s -X GET "https://app.reportei.com/api/v1/reports/<your-report-id>" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}"'
```

---

### 7. List Client Integrations

Get all integrations for a specific client. Replace `<your-client-id>` with the actual client ID:

```bash
bash -c 'curl -s -X GET "https://app.reportei.com/api/v1/clients/<your-client-id>/integrations" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}"'
```

---

### 8. Get Integration Details

Retrieve details of a specific integration. Replace `<your-integration-id>` with the actual integration ID:

```bash
bash -c 'curl -s -X GET "https://app.reportei.com/api/v1/integrations/<your-integration-id>" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}"'
```

---

### 9. Get Integration Widgets

List available widgets for an integration. Replace `<your-integration-id>` with the actual integration ID:

```bash
bash -c 'curl -s -X GET "https://app.reportei.com/api/v1/integrations/<your-integration-id>/widgets" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}"'
```

---

### 10. Get Widget Value

Retrieve the value of specific widgets.

Write to `/tmp/reportei_request.json`:

```json
{
  "widgets": ["widget_id_1", "widget_id_2"],
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

Then run (replace `<your-integration-id>` with the actual integration ID):

```bash
bash -c 'curl -s -X POST "https://app.reportei.com/api/v1/integrations/<your-integration-id>/widgets/value" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/reportei_request.json'
```

---

### 11. Create Report (Connector Action)

Create a new report programmatically.

Write to `/tmp/reportei_request.json`:

```json
{
  "client_id": "your-client-id",
  "template_id": "your-template-id",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://app.reportei.com/api/v1/create_report" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/reportei_request.json'
```

---

### 12. Create Dashboard (Connector Action)

Create a new dashboard.

Write to `/tmp/reportei_request.json`:

```json
{
  "client_id": "your-client-id",
  "name": "My Dashboard"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://app.reportei.com/api/v1/create_dashboard" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/reportei_request.json'
```

---

### 13. Add to Timeline (Connector Action)

Add an entry to the client timeline.

Write to `/tmp/reportei_request.json`:

```json
{
  "client_id": "your-client-id",
  "title": "Campaign Launched",
  "description": "New marketing campaign started"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://app.reportei.com/api/v1/add_to_timeline" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/reportei_request.json'
```

---

### 14. List Webhook Events

Get available webhook event types:

```bash
bash -c 'curl -s -X GET "https://app.reportei.com/api/v1/webhook/events" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}"'
```

---

### 15. Subscribe to Webhook

Subscribe to webhook notifications.

Write to `/tmp/reportei_request.json`:

```json
{
  "url": "https://your-webhook-endpoint.com/webhook",
  "events": ["report.created", "report.updated"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://app.reportei.com/api/v1/webhooks/subscribe" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/reportei_request.json'
```

---

### 16. Unsubscribe from Webhook

Unsubscribe from webhook notifications.

Write to `/tmp/reportei_request.json`:

```json
{
  "webhook_id": "your-webhook-id"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://app.reportei.com/api/v1/webhooks/unsubscribe" -H "Authorization: Bearer ${REPORTEI_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/reportei_request.json'
```

---

## Company Types

| Type | Description |
|------|-------------|
| `agency` | Marketing agency |
| `freelancer` | Independent professional |
| `company` | In-house marketing team |

---

## Response Fields

### Company Object

| Field | Description |
|-------|-------------|
| `id` | Company unique identifier |
| `name` | Company name |
| `logo` | Logo filename |
| `type` | Company type |
| `potential_clients` | Client range |
| `company_specialty` | Main focus area |

### Template Object

| Field | Description |
|-------|-------------|
| `id` | Template unique identifier |
| `title` | Template name |
| `description` | Template description |
| `used_count` | Times template has been used |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |

---

## Guidelines

1. **Bearer Token**: Always include the Authorization header with Bearer token
2. **Rate Limits**: Be mindful of API rate limits
3. **Date Format**: Use ISO format (YYYY-MM-DD) for date parameters
4. **Client IDs**: Get client IDs from the `/clients` endpoint first
5. **Template IDs**: Get template IDs from the `/templates` endpoint
6. **Webhooks**: Use webhooks for real-time notifications instead of polling
7. **Dashboard**: Use https://app.reportei.com for visual report management
