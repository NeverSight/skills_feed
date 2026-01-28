---
name: monitor-api
description: Monitor API integration of Parallel. Use when building applications with Parallel Monitor API.
---

<!--
https://contextarea.com/rules-httpsrawg-fr4kfek206psz4

https://github.com/parallel-web/parallel-skills
-->

# Monitor API Complete Reference

> Track web changes continuously with scheduled queries and webhook notifications

The Monitor API lets you continuously track the web for changes relevant to a query, on a schedule you control. Create a monitor with a natural-language query, choose a cadence (hourly, daily, weekly), and receive webhook notifications when changes are detected.

<Note>
  **Alpha Notice**: The Monitor API is currently in public alpha. Endpoints and
  request/response formats are subject to change.
</Note>

## Table of Contents

- [Features and Use Cases](#features-and-use-cases)
- [Getting Started](#getting-started)
- [Creating Monitors](#creating-monitors)
- [Events and Event Groups](#events-and-event-groups)
- [Webhooks](#webhooks)
- [Structured Outputs](#structured-outputs)
- [Testing with Simulate Event](#testing-with-simulate-event)
- [Managing Monitors](#managing-monitors)
- [Slack Integration](#slack-integration)
- [Best Practices](#best-practices)

## Features and Use Cases

The Monitor API automates continuous research for any topic, including companies, products, or regulatory areas—without building complicated web monitoring infrastructure. Define a query once along with the desired schedule, and the service will detect relevant changes and deliver concise updates (with source links) to your systems via webhooks.

**Current Features:**

- **Scheduling**: Set update cadence to Hourly, Daily, or Weekly
- **Webhooks**: Receive updates when events are detected or when monitors finish a scheduled run
- **Events history**: Retrieve updates from recent runs or via a lookback window (e.g., `10d`)
- **Lifecycle management**: Update cadence, webhook, or metadata; delete to stop future runs
- **Structured outputs**: Return events as JSON conforming to your schema

**Common Use Cases:**

| Use Case              | Example Query                                                       |
| --------------------- | ------------------------------------------------------------------- |
| News tracking         | "What is the latest AI funding news?"                               |
| Brand mentions        | "Let me know when someone mentions Parallel Web Systems on the web" |
| Product announcements | "Alert me when Apple announces new MacBook models"                  |
| Regulatory updates    | "Notify me of any new FDA guidance on AI in medical devices"        |
| Price monitoring      | "Let me know when the price for AirPods drops below $150"           |
| Stock availability    | "Alert me when the PS5 Pro is back in stock at Best Buy"            |
| Content updates       | "Notify me when the React documentation is updated"                 |
| Policy changes        | "Track changes to OpenAI's terms of service"                        |

## Getting Started

### Prerequisites

Generate your API key on [Platform](https://platform.parallel.ai), then set it in your shell:

```bash
export PARALLEL_API_KEY="PARALLEL_API_KEY"
```

### Quick Example

Create a monitor that gathers daily AI news:

```bash
curl --request POST \
  --url https://api.parallel.ai/v1alpha/monitors \
  --header 'Content-Type: application/json' \
  --header "x-api-key: $PARALLEL_API_KEY" \
  --data '{
    "query": "Extract recent news about quantum in AI",
    "cadence": "daily",
    "webhook": {
      "url": "https://example.com/webhook",
      "event_types": ["monitor.event.detected"]
    },
    "metadata": { "key": "value" }
  }'
```

**Response:**

```json
{
  "monitor_id": "monitor_b0079f70195e4258a3b982c1b6d8bd3a",
  "query": "Extract recent news about quantum in AI",
  "status": "active",
  "cadence": "daily",
  "metadata": { "key": "value" },
  "webhook": {
    "url": "https://example.com/webhook",
    "event_types": ["monitor.event.detected"]
  },
  "created_at": "2025-04-23T20:21:48.037943Z"
}
```

## Creating Monitors

### POST /v1alpha/monitors

Creates a monitor that periodically runs the specified query over the web at the specified cadence (hourly, daily, or weekly). The monitor runs once at creation and then continues according to the specified frequency.

**Request Body:**

| Parameter       | Type           | Required | Description                                                                                                                                                                                                                                                                                                |
| --------------- | -------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `query`         | string         | Yes      | Search query to monitor for material changes.                                                                                                                                                                                                                                                              |
| `cadence`       | string         | Yes      | Cadence of the monitor. One of: `daily`, `weekly`, `hourly`                                                                                                                                                                                                                                                |
| `webhook`       | object \| null | No       | Webhook to receive notifications about the monitor's execution.                                                                                                                                                                                                                                            |
| `metadata`      | object \| null | No       | User-provided metadata stored with the monitor. This field is returned in webhook notifications and GET requests, enabling you to map responses to corresponding objects in your application. For example, if you are building a Slackbot that monitors changes, you could store the Slack thread ID here. |
| `output_schema` | object \| null | No       | Output schema for the monitor event. See [Structured Outputs](#structured-outputs).                                                                                                                                                                                                                        |

**Webhook Object:**

| Parameter     | Type           | Required | Description                                                                               |
| ------------- | -------------- | -------- | ----------------------------------------------------------------------------------------- |
| `url`         | string         | Yes      | URL for the webhook.                                                                      |
| `event_types` | array\[string] | No       | Event types to send webhook notifications for. See [Webhooks](#webhooks) for event types. |

**Response:**

Returns a `MonitorResponse` object with status code `201`.

**Example Request:**

<CodeGroup>
  ```bash cURL
  curl --request POST \
    --url https://api.parallel.ai/v1alpha/monitors \
    --header 'Content-Type: application/json' \
    --header "x-api-key: $PARALLEL_API_KEY" \
    --data '{
      "query": "Extract recent news about AI",
      "cadence": "daily",
      "webhook": {
        "url": "https://example.com/webhook",
        "event_types": ["monitor.event.detected"]
      },
      "metadata": { "key": "value" }
    }'
  ```

```python Python
from httpx import Response
from parallel import Parallel

client = Parallel(api_key="PARALLEL_API_KEY")

res = client.post(
  "/v1alpha/monitors",
  cast_to=Response,
  body={
    "query": "Extract recent news about AI",
    "cadence": "daily",
    "webhook": {
      "url": "https://example.com/webhook",
      "event_types": ["monitor.event.detected"],
    },
    "metadata": {"key": "value"},
  },
).json()

print(res["monitor_id"])
```

```typescript TypeScript
import Parallel from "parallel-web";

const client = new Parallel({ apiKey: process.env.PARALLEL_API_KEY! });

async function create_monitor() {
  const monitor = await client.post("/v1alpha/monitors", {
    body: {
      query: "Extract recent news about AI",
      cadence: "daily",
      webhook: {
        url: "https://example.com/webhook",
        event_types: ["monitor.event.detected"],
      },
      metadata: { key: "value" },
    },
  });
  console.log(monitor.monitor_id);
}

create_monitor();
```

</CodeGroup>

## Events and Event Groups

Monitors produce a stream of events each time they run. These events capture:

- new results detected by your query (events)
- run completions
- errors (if a run fails)

Related events are grouped by an `event_group_id` so you can fetch the full set of results that belong to the same discovery.

### Event Groups

<Note>
  Event groups are primarily relevant for webhook users. When a webhook fires
  with a `monitor.event.detected` event, it returns an `event_group_id` that you
  use to retrieve the complete set of results.
</Note>

Event groups collect related results under a single `event_group_id`. When a monitor detects new results, it creates an event group. Subsequent runs can add additional events to the same group if they're related to the same discovery.

Use event groups to present the full context of a discovery (multiple sources, follow-up updates) as one unit.

### Event Types

Besides events with new results, monitors emit:

- **Event** (`type: "event"`): indicates a material change was detected
- **Completion** (`type: "completion"`): indicates a run finished successfully without detected events
- **Error** (`type: "error"`): indicates a run failed

<Note>
  Runs with non-empty events are not included in completions. This means that a
  run will correspond to only one of successful event detection, completion or
  failure.
</Note>

### GET /v1alpha/monitors/{monitor_id}/event_groups/{event_group_id}

Retrieves all events for a specific event group.

**Path Parameters:**

| Parameter        | Type   | Required | Description           |
| ---------------- | ------ | -------- | --------------------- |
| `monitor_id`     | string | Yes      | ID of the monitor     |
| `event_group_id` | string | Yes      | ID of the event group |

**Example Request:**

<CodeGroup>
  ```bash cURL
  curl --request GET \
    --url "https://api.parallel.ai/v1alpha/monitors/<monitor_id>/event_groups/<event_group_id>" \
    --header "x-api-key: $PARALLEL_API_KEY"
  ```

```python Python
from httpx import Response
from parallel import Parallel

client = Parallel(api_key="PARALLEL_API_KEY")

group = client.get(
  f"/v1alpha/monitors/{monitor_id}/event_groups/{event_group_id}",
  cast_to=Response,
).json()

print(group["events"])
```

```typescript TypeScript
import Parallel from "parallel-web";

const client = new Parallel({ apiKey: process.env.PARALLEL_API_KEY! });

async function getEventGroup(monitorId: string, eventGroupId: string) {
  const res = (await client.get(
    `/v1alpha/monitors/${monitorId}/event_groups/${eventGroupId}`,
  )) as any;
  console.log(res.events);
}

getEventGroup();
```

</CodeGroup>

**Response:**

```json
{
  "events": [
    {
      "type": "event",
      "event_group_id": "mevtgrp_b0079f70195e4258eab1e7284340f1a9ec3a8033ed236a24",
      "output": "New product launch announced",
      "event_date": "2025-01-15",
      "source_urls": ["https://example.com/news"],
      "result": {
        "type": "text",
        "content": "New product launch announced"
      }
    }
  ]
}
```

### GET /v1alpha/monitors/{monitor_id}/events

Retrieves events from the monitor, including events with errors and material changes. The endpoint checks up to the specified lookback period or the previous 300 event groups, whichever is less.

Events will be returned in reverse chronological order, with the most recent event groups first. All events from an event group will be flattened out into individual entries in the list.

**Path Parameters:**

| Parameter    | Type   | Required | Description       |
| ------------ | ------ | -------- | ----------------- |
| `monitor_id` | string | Yes      | ID of the monitor |

**Query Parameters:**

| Parameter         | Type   | Default | Description                                                                                                                                                 |
| ----------------- | ------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lookback_period` | string | `10d`   | Lookback period to fetch events from. Sample values: `10d`, `1w`. A minimum of 1 day is supported with one day increments. Use `d` for days, `w` for weeks. |

**Example Request:**

```bash
curl --request GET \
  --url "https://api.parallel.ai/v1alpha/monitors/<monitor_id>/events?lookback_period=10d" \
  --header "x-api-key: $PARALLEL_API_KEY"
```

**Response:**

```json
{
  "events": [
    {
      "type": "event",
      "event_group_id": "mevtgrp_b0079f70195e4258eab1e7284340f1a9ec3a8033ed236a24",
      "output": "New product launch announced",
      "event_date": "2025-01-15",
      "source_urls": ["https://example.com/news"],
      "result": {
        "type": "text",
        "content": "New product launch announced"
      }
    },
    {
      "type": "completion",
      "monitor_ts": "completed_2025-01-15T10:30:00Z"
    },
    {
      "type": "error",
      "error": "Error occurred while processing the event",
      "id": "error_2025-01-15T10:30:00Z",
      "date": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### Accessing Events

You can receive events via webhooks (recommended) or retrieve them via endpoints.

- **Webhooks (recommended)**: lowest latency, push-based delivery. Subscribe to `monitor.event.detected`, `monitor.execution.completed`, and `monitor.execution.failed`. See [Webhooks](#webhooks) for more details.

- **Endpoints (for history/backfill)**:
  - `GET /v1alpha/monitors/{monitor_id}/events` — list events for a monitor in reverse chronological order (up to recent ~300 runs). This flattens out events, meaning that multiple events from the same event group will be listed as different events.
  - `GET /v1alpha/monitors/{monitor_id}/event_groups/{event_group_id}` - list all events given an `event_group_id`.

## Webhooks

<Note>
  **Prerequisites:** Before implementing Monitor webhooks, read **[Webhook Setup & Verification](/resources/webhook-setup)** for critical information on:

- Recording your webhook secret
- Verifying HMAC signatures
- Security best practices
- Retry policies

This guide focuses on Monitor-specific webhook events and payloads.
</Note>

Webhooks allow you to receive real-time notifications when a Monitor execution completes, fails, or when material events are detected, eliminating the need for polling. This is especially useful for scheduled monitors that run at long gaps (hourly, daily, or weekly) and notify your systems only when relevant changes occur.

### Setup

To register a webhook for a Monitor, include a `webhook` parameter when creating the monitor:

```bash
curl --request POST \
  --url https://api.parallel.ai/v1alpha/monitors \
  --header "Content-Type: application/json" \
  --header "x-api-key: $PARALLEL_API_KEY" \
  --data '{
    "query": "Extract recent news about AI",
    "cadence": "daily",
    "webhook": {
      "url": "https://your-domain.com/webhooks/monitor",
      "event_types": [
        "monitor.event.detected",
        "monitor.execution.completed",
        "monitor.execution.failed"
      ]
    },
    "metadata": { "team": "research" }
  }'
```

**Webhook Parameters:**

| Parameter     | Type           | Required | Description                                               |
| ------------- | -------------- | -------- | --------------------------------------------------------- |
| `url`         | string         | Yes      | Your webhook endpoint URL. Can be any domain you control. |
| `event_types` | array\[string] | Yes      | Event types to subscribe to. See Event Types below.       |

### Event Types

Monitors support the following webhook event types:

| Event Type                    | Description                                                                  |
| ----------------------------- | ---------------------------------------------------------------------------- |
| `monitor.event.detected`      | Emitted when a run detects one or more material events.                      |
| `monitor.execution.completed` | Emitted when a Monitor run completes successfully (without detected events). |
| `monitor.execution.failed`    | Emitted when a Monitor run fails due to an error.                            |

You can subscribe to any combination of these event types in your webhook configuration. Note that `monitor.event.detected` and `monitor.execution.completed` are mutually distinct and correspond to different runs.

### Webhook Payload Structure

For Monitor webhooks, the `data` object contains:

- `monitor_id`: The unique ID of the Monitor
- `event`: The event record for this run
- `metadata`: User-provided metadata from the Monitor (if any)

<CodeGroup>
  ```json monitor.event.detected
  {
    "type": "monitor.event.detected",
    "timestamp": "2025-10-27T14:56:05.619331Z",
    "data": {
      "monitor_id": "monitor_0c9d7f7d5a7841a0b6c269b2b9b1e6aa",
      "event": {
        "event_group_id": "mevtgrp_b0079f70195e4258eab1e7284340f1a9ec3a8033ed236a24"
      },
      "metadata": { "team": "research" }
    }
  }
  ```

```json monitor.execution.completed
{
  "type": "monitor.execution.completed",
  "timestamp": "2025-10-27T14:56:05.619331Z",
  "data": {
    "monitor_id": "monitor_0c9d7f7d5a7841a0b6c269b2b9b1e6aa",
    "event": {
      "type": "completion",
      "monitor_ts": "completed_2025-01-15T10:30:00Z"
    },
    "metadata": { "team": "research" }
  }
}
```

```json monitor.execution.failed
{
  "type": "monitor.execution.failed",
  "timestamp": "2025-10-27T14:57:30.789012Z",
  "data": {
    "monitor_id": "monitor_0c9d7f7d5a7841a0b6c269b2b9b1e6aa",
    "event": {
      "type": "error",
      "error": "Error occurred while processing the event",
      "id": "error_2025-01-15T10:30:00Z",
      "date": "2025-01-15T10:30:00Z"
    },
    "metadata": { "team": "research" }
  }
}
```

</CodeGroup>

When you receive a webhook with an `event_group_id` (for a detected change), fetch the full set of related events using the event group endpoint described above.

### Security & Verification

For HMAC signature verification and language-specific examples, see the **[Webhook Setup Guide - Security & Verification](/resources/webhook-setup#security--verification)**.

### Retry Policy

See **[Webhook Setup Guide - Retry Policy](/resources/webhook-setup#retry-policy)** for delivery retries and backoff details.

## Structured Outputs

Structured outputs enable you to define a JSON schema for monitor events. Each detected event conforms to the specified schema, returning data in a consistent, machine-readable format suitable for downstream processing in databases, analytics pipelines, or automation workflows.

<Note>
  **Schema Complexity**: Output schemas are currently limited to the complexity supported by the core processor. Use flat schemas with a small number of clearly defined fields.
</Note>

### Defining an Output Schema

Include an `output_schema` field when creating a monitor:

```bash
curl --request POST \
  --url https://api.parallel.ai/v1alpha/monitors \
  --header 'Content-Type: application/json' \
  --header "x-api-key: $PARALLEL_API_KEY" \
  --data '{
    "query": "monitor ai news",
    "cadence": "daily",
    "output_schema": {
      "type": "json",
      "json_schema": {
        "type": "object",
        "properties": {
          "company_name": {
            "type": "string",
            "description": "Name of the company the news is about, NA if not company-specific"
          },
          "sentiment": {
            "type": "string",
            "description": "Sentiment of the news: positive or negative"
          },
          "description": {
            "type": "string",
            "description": "Brief description of the news"
          }
        }
      }
    }
  }'
```

### Retrieving Structured Events

Events from monitors configured with structured outputs include a `result` field containing the parsed JSON object:

```bash
curl --request GET \
  --url "https://api.parallel.ai/v1alpha/monitors/<monitor_id>/events" \
  --header "x-api-key: $PARALLEL_API_KEY"
```

**Response:**

```json
{
  "events": [
    {
      "type": "event",
      "event_group_id": "mevtgrp_f9727e22dd4a42ba5e7fdcaa36b2b8ea2ef7c11f15fb4061",
      "event_date": "2025-12-02",
      "source_urls": [
        "https://www.cnbc.com/2025/12/02/youtube-ai-biometric-data-creator-deepfake.html"
      ],
      "result": {
        "type": "json",
        "content": {
          "company_name": "YouTube/Google",
          "sentiment": "negative",
          "description": "YouTube expanded a likeness detection deepfake tracking tool; experts warn the sign-up requires government ID and a biometric video."
        }
      }
    },
    {
      "type": "event",
      "event_group_id": "mevtgrp_f9727e22dd4a42ba5e7fdcaa36b2b8ea2ef7c11f15fb4061",
      "event_date": "2025-12-02",
      "source_urls": [
        "https://fox59.com/business/press-releases/globenewswire/9595236/kloudfuse-launches-kloudfuse-3-5"
      ],
      "result": {
        "type": "json",
        "content": {
          "company_name": "Kloudfuse",
          "sentiment": "positive",
          "description": "Kloudfuse announced version 3.5 with AI-native observability features including LLM observability integrated into APM."
        }
      }
    }
  ]
}
```

### Best Practices for Structured Outputs

- **Include property descriptions**: Provide clear `description` fields for each property to improve extraction accuracy
- **Use primitive types**: Limit properties to `string` and `enum` types for reliable parsing
- **Maintain flat schemas**: Use 3–5 properties with a single-level object structure
- **Define edge case handling**: Specify how missing or inapplicable values should be represented

## Testing with Simulate Event

The simulate event endpoint allows you to test your webhook integration without waiting for a scheduled monitor run.

### POST /v1alpha/monitors/{monitor_id}/simulate_event

**Path Parameters:**

| Parameter    | Type   | Required | Description       |
| ------------ | ------ | -------- | ----------------- |
| `monitor_id` | string | Yes      | ID of the monitor |

**Query Parameters:**

| Parameter    | Type   | Default                  | Description                                                                                                         |
| ------------ | ------ | ------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| `event_type` | string | `monitor.event.detected` | Event type to simulate. One of: `monitor.event.detected`, `monitor.execution.completed`, `monitor.execution.failed` |

**Response:**

Returns `204 No Content` on success.

**Errors:**

| Status | Description                             |
| ------ | --------------------------------------- |
| 400    | Webhook not configured for this monitor |
| 404    | Monitor not found                       |

**Example:**

```bash
curl --request POST \
  --url "https://api.parallel.ai/v1alpha/monitors/<monitor_id>/simulate_event?event_type=monitor.event.detected" \
  --header "x-api-key: $PARALLEL_API_KEY"
```

### Test Event Groups

When you simulate a `monitor.event.detected` event, the webhook payload includes a test `event_group_id`. You can retrieve this test event group using the standard endpoint:

```bash
curl --request GET \
  --url "https://api.parallel.ai/v1alpha/monitors/<monitor_id>/event_groups/<test_event_group_id>" \
  --header "x-api-key: $PARALLEL_API_KEY"
```

**Response:**

<CodeGroup>
  ```json No Structured Output
  {
      "events": [
          {
              "type": "event",
              "event_group_id": "test_abc",
              "output": "",
              "event_date": "2025-12-05",
              "source_urls": [
                  "https://test.example.com"
              ],
              "result": {
                  "type": "text",
                  "content": "This is a test event."
              }
          }
      ]
  }
  ```

```json Structured Output
{
  "events": [
    {
      "type": "event",
      "event_group_id": "test_def",
      "output": "",
      "event_date": "2025-12-05",
      "source_urls": ["https://test.example.com"],
      "result": {
        "type": "json",
        "content": {
          "sentiment": "",
          "stock_ticker_symbol": "",
          "description": ""
        }
      }
    }
  ]
}
```

</CodeGroup>

Test event group IDs return dummy event data, allowing you to verify your full webhook processing pipeline—from receiving the webhook to fetching event details.

## Managing Monitors

### GET /v1alpha/monitors

List all monitors for your account.

**Example:**

```bash
curl --request GET \
  --url https://api.parallel.ai/v1alpha/monitors \
  --header "x-api-key: $PARALLEL_API_KEY"
```

### GET /v1alpha/monitors/{monitor_id}

Retrieve a specific monitor by ID.

**Path Parameters:**

| Parameter    | Type   | Required | Description       |
| ------------ | ------ | -------- | ----------------- |
| `monitor_id` | string | Yes      | ID of the monitor |

**Example:**

```bash
curl --request GET \
  --url "https://api.parallel.ai/v1alpha/monitors/<monitor_id>" \
  --header "x-api-key: $PARALLEL_API_KEY"
```

### PATCH /v1alpha/monitors/{monitor_id}

Update a monitor's configuration. You can update the cadence, webhook, and metadata.

**Path Parameters:**

| Parameter    | Type   | Required | Description       |
| ------------ | ------ | -------- | ----------------- |
| `monitor_id` | string | Yes      | ID of the monitor |

**Request Body:**

| Parameter  | Type           | Required | Description                                         |
| ---------- | -------------- | -------- | --------------------------------------------------- |
| `cadence`  | string         | No       | Cadence of the monitor: `daily`, `weekly`, `hourly` |
| `webhook`  | object \| null | No       | Webhook configuration                               |
| `metadata` | object \| null | No       | User-provided metadata                              |

**Example:**

```bash
curl --request PATCH \
  --url "https://api.parallel.ai/v1alpha/monitors/<monitor_id>" \
  --header 'Content-Type: application/json' \
  --header "x-api-key: $PARALLEL_API_KEY" \
  --data '{
    "cadence": "weekly",
    "metadata": { "updated": "true" }
  }'
```

### DELETE /v1alpha/monitors/{monitor_id}

Delete a monitor, stopping all future executions. Deleted monitors can no longer be updated or retrieved.

**Path Parameters:**

| Parameter    | Type   | Required | Description       |
| ------------ | ------ | -------- | ----------------- |
| `monitor_id` | string | Yes      | ID of the monitor |

**Example:**

```bash
curl --request DELETE \
  --url "https://api.parallel.ai/v1alpha/monitors/<monitor_id>" \
  --header "x-api-key: $PARALLEL_API_KEY"
```

## Slack Integration

The Parallel Slack app brings Monitor directly into your Slack workspace. Create monitors with slash commands and receive updates in dedicated threads.

### Installation

1. Go to [platform.parallel.ai](https://platform.parallel.ai) and navigate to the Integrations section
2. Click **Add to Slack** to begin the OAuth flow
3. Authorize the Parallel app in your workspace
4. Invite the bot to any channel where you want to use monitoring: `/invite @Parallel`

<Note>
  Your Parallel API key is securely linked during the OAuth flow. All monitors created via Slack use your account's quota and billing.
</Note>

### Commands

#### /monitor

Create a **daily** monitor:

```
/monitor latest AI research papers
```

The bot posts your query and replies in a thread when changes are detected.

#### /hourly

Create an **hourly** monitor for fast-moving topics:

```
/hourly breaking news about OpenAI
```

#### /help

View available commands:

```
/help
```

#### Cancel a Monitor

Reply to the monitoring thread with:

```
cancelmonitor
```

The bot will cancel the monitor and confirm in the thread.

### Pricing

Monitors created via Slack use the same pricing as the Monitor API. See [Pricing](/resources/pricing) for details.

## Best Practices

### Scope Your Query

Clear queries with explicit instructions lead to higher-quality event detection. Monitor works best with natural language queries that clearly describe what you're looking for.

| ❌ Bad Query                                                                            | ✅ Good Query                                                  |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| "Parallel OR Parallel Web Systems OR Parallel AI AND Funding OR Launch OR Announcement" | "Parallel Web Systems (parallel.ai) launch or funding updates" |

Unlike a search engine, the query doesn't need to be keyword-heavy—it needs to be intent-heavy.

### Choose the Right Cadence

- Use `hourly` for fast-moving topics
- Use `daily` for most news
- Use `weekly` for slower changes

### Use for Current Events, Not Historical Research

**Don't use for historical research**: Monitor is designed to track _new_ updates as they happen, not to retrieve past news. Use [Deep Research](/task-api/task-deep-research) for historical queries.

| ❌ Bad Query                                     | ✅ Good Query                      |
| ------------------------------------------------ | ---------------------------------- |
| "Find all AI funding news from the last 2 years" | "AI startup funding announcements" |

### Don't Include Dates

Monitor automatically tracks updates from when it's created. Adding specific dates to your query is unnecessary and can cause confusion.

| ❌ Bad Query                         | ✅ Good Query                  |
| ------------------------------------ | ------------------------------ |
| "Tesla news after December 12, 2025" | "Tesla news and announcements" |

### Prefer Webhooks

Use webhooks to avoid unnecessary polling and reduce latency to updates. This is especially important for hourly and daily monitors.

### Manage Lifecycle

Cancel monitors you no longer need to reduce your usage bills.

## Lifecycle

The Monitor API follows a straightforward lifecycle:

1. **Create**: Define your `query`, `cadence`, and optional `webhook` and `metadata`
2. **Update**: Change cadence, webhook, or metadata
3. **Delete**: Delete a monitor and stop future executions

At any point, you can retrieve the list of events for a monitor or events within a specific event group.

## Rate Limits

See [Rate Limits](/resources/rate-limits) for default quotas and how to request higher limits.

## Pricing

<Note>
  See [Pricing](/pricing) for a detailed schedule of rates.
</Note>

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.parallel.ai/llms.txt
