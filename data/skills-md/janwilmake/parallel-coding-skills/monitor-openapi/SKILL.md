---
name: monitor-openapi
description: Monitor API integration of Parallel. Use when building applications with Parallel Monitor API.
# https://contextarea.com/rules-httpsrawg-3zcqa0m97o2o36
---

````yaml
openapi: 3.1.0
info:
  title: Parallel Monitor API
  version: 1.0.0-alpha
  description: |
    # Monitor API

    The Monitor API lets you continuously track the web for changes relevant to a query, on a schedule you control. Create a monitor with a natural-language query, choose a cadence (hourly, daily, weekly), and receive webhook notifications.

    **Alpha Notice**: The Monitor API is currently in public alpha. Endpoints and request/response formats are subject to change.

    ## Features and Use Cases

    - **News tracking**: Alert when there's notable news about a company or product
    - **Competitive monitoring**: Detect when competitors launch new features or pricing changes
    - **Regulatory updates**: Track new rules or guidance impacting your industry
    - **Deal/research watchlists**: Surface events about entities you care about
    - **Product tracking**: Track modifications to product listings

    ## Supported Features

    - **Scheduling**: Set update cadence to Hourly, Daily, or Weekly
    - **Webhooks**: Receive updates when events are detected or when monitors finish a scheduled run
    - **Events history**: Retrieve updates from recent runs or via a lookback window (e.g., `10d`)
    - **Lifecycle management**: Update cadence, webhook, or metadata; delete to stop future runs
    - **Structured outputs**: Define JSON schemas for consistent, machine-readable event data

    ## Best Practices

    ### Event Tracking
    Use Monitor to track when something happens on the web:

    | Use Case | Example Query |
    |----------|---------------|
    | Brand mentions | "Let me know when someone mentions Parallel Web Systems on the web" |
    | News tracking | "What is the latest AI funding news?" |
    | Product announcements | "Alert me when Apple announces new MacBook models" |
    | Regulatory updates | "Notify me of any new FDA guidance on AI in medical devices" |

    ### Change Tracking
    Use Monitor to detect when something changes:

    | Use Case | Example Query |
    |----------|---------------|
    | Price monitoring | "Let me know when the price for AirPods drops below $150" |
    | Stock availability | "Alert me when the PS5 Pro is back in stock at Best Buy" |
    | Content updates | "Notify me when the React documentation is updated" |
    | Policy changes | "Track changes to OpenAI's terms of service" |

    ### Writing Effective Queries

    Monitor works best with natural language queries that clearly describe what you're looking for.

    **Good practices:**
    - ✅ Use natural language that describes intent: "Parallel Web Systems (parallel.ai) launch or funding updates"
    - ✅ Focus on what you want to track: "AI startup funding announcements"
    - ✅ Be specific about the topic: "Tesla news and announcements"

    **Avoid:**
    - ❌ Keyword-heavy queries: "Parallel OR Parallel Web Systems OR Parallel AI AND Funding OR Launch"
    - ❌ Historical research queries: "Find all AI funding news from the last 2 years" (use Deep Research API instead)
    - ❌ Including specific dates: "Tesla news after December 12, 2025" (Monitor tracks from creation automatically)

    ## Events and Event Groups

    Monitors produce a stream of events each time they run. These events capture:
    - New results detected by your query (events)
    - Run completions
    - Errors (if a run fails)

    Related events are grouped by an `event_group_id` so you can fetch the full set of results that belong to the same discovery.

    ### Event Groups
    Event groups collect related results under a single `event_group_id`. When a monitor detects new results, it creates an event group. Subsequent runs can add additional events to the same group if they're related to the same discovery.

    Use event groups to present the full context of a discovery (multiple sources, follow-up updates) as one unit. To fetch the complete set of results for a discovery, use the GET event group endpoint with the `event_group_id` received in your webhook payload.

    ### Other Events
    Besides events with new results, monitors emit:
    - **Completion** (`type: "completion"`): indicates a run finished successfully
    - **Error** (`type: "error"`): indicates a run failed

    **Note**: Runs with non-empty events are not included in completions. This means that a run will correspond to only one of successful event detection, completion or failure.

    ## Accessing Events

    You can receive events via webhooks (recommended) or retrieve them via endpoints.

    - **Webhooks (recommended)**: lowest latency, push-based delivery. Subscribe to `monitor.event.detected`, `monitor.execution.completed`, and `monitor.execution.failed`.
    - **Endpoints (for history/backfill)**:
      - List monitor events — list events for a monitor in reverse chronological order (up to recent ~300 runs). This flattens out events, meaning that multiple events from the same event group will be listed as different events.
      - Retrieve event group — list all events given an `event_group_id`.

    ## Webhooks

    Webhooks allow you to receive real-time notifications when a Monitor execution completes, fails, or when material events are detected, eliminating the need for polling.

    ### Setup
    Include a `webhook` parameter when creating the monitor with:
    - `url`: Your webhook endpoint URL (can be any domain you control)
    - `event_types`: Array of event types to subscribe to

    ### Event Types
    - `monitor.event.detected`: Emitted when a run detects one or more material events
    - `monitor.execution.completed`: Emitted when a Monitor run completes successfully (without detected events)
    - `monitor.execution.failed`: Emitted when a Monitor run fails due to an error

    **Note**: `monitor.event.detected` and `monitor.execution.completed` are mutually distinct and correspond to different runs.

    ### Webhook Payload Structure

    The `data` object contains:
    - `monitor_id`: The unique ID of the Monitor
    - `event`: The event record for this run
    - `metadata`: User-provided metadata from the Monitor (if any)

    ### Security & Verification

    **Prerequisites**: Before implementing Monitor webhooks, refer to the Webhook Setup & Verification guide for:
    - Recording your webhook secret
    - Verifying HMAC signatures
    - Security best practices
    - Retry policies

    ## Structured Outputs

    Structured outputs enable you to define a JSON schema for monitor events. Each detected event conforms to the specified schema, returning data in a consistent, machine-readable format suitable for downstream processing.

    **Schema Complexity**: Output schemas are currently limited to the complexity supported by the core processor. Use flat schemas with a small number of clearly defined fields.

    ### Best Practices for Schemas
    - Include property descriptions for each property to improve extraction accuracy
    - Use primitive types (limit to `string` and `enum` for reliable parsing)
    - Maintain flat schemas (3-5 properties with single-level object structure)
    - Define edge case handling (specify how missing or inapplicable values should be represented)

    ## Slack Integration

    The Parallel Slack app brings Monitor directly into your Slack workspace. Create monitors with slash commands and receive updates in dedicated threads.

    ### Installation
    1. Go to platform.parallel.ai and navigate to the Integrations section
    2. Click **Add to Slack** to begin the OAuth flow
    3. Authorize the Parallel app in your workspace
    4. Invite the bot to any channel: `/invite @Parallel`

    ### Commands
    - `/monitor <query>` - Create a daily monitor
    - `/hourly <query>` - Create an hourly monitor
    - `/help` - View available commands
    - Reply with `cancelmonitor` in a monitoring thread to cancel

    ## Rate Limits

    See the Rate Limits documentation for default quotas and how to request higher limits.

    ## Pricing

    See the Pricing documentation for a detailed schedule of rates.
  contact:
    name: Parallel Support
    url: https://parallel.ai
    email: support@parallel.ai

servers:
  - url: https://api.parallel.ai
    description: Parallel API

security:
  - ApiKeyAuth: []

tags:
  - name: Monitors
    description: Monitor lifecycle operations (create, retrieve, update, delete)
  - name: Events
    description: Event retrieval and event group operations
  - name: Testing
    description: Webhook testing and simulation

paths:
  /v1alpha/monitors:
    post:
      tags:
        - Monitors
      summary: Create Monitor
      operationId: create_monitor
      description: |
        Creates a monitor that periodically runs the specified query over the web at the specified cadence (hourly, daily, or weekly). The monitor runs once at creation and then continues according to the specified frequency.

        Updates will be sent to the webhook if provided. Use the events endpoints to retrieve execution history for a monitor.

        ## Lifecycle

        The Monitor API follows a straightforward lifecycle:
        1. **Create**: Define your `query`, `cadence`, and optional `webhook` and `metadata`
        2. **Update**: Change cadence, webhook, or metadata
        3. **Delete**: Delete a monitor and stop future executions

        ## Best Practices

        1. **Scope your query**: Clear queries with explicit instructions lead to higher-quality event detection
        2. **Choose the right cadence**: Use `hourly` for fast-moving topics, `daily` for most news, `weekly` for slower changes
        3. **Use webhooks**: Prefer webhooks to avoid unnecessary polling and reduce latency to updates
        4. **Manage lifecycle**: Cancel monitors you no longer need to reduce your usage bills
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateMonitorRequest"
            examples:
              basic:
                summary: Basic daily monitor
                value:
                  query: "Extract recent news about AI"
                  cadence: "daily"
              with_webhook:
                summary: Monitor with webhook
                value:
                  query: "Extract recent news about quantum in AI"
                  cadence: "daily"
                  webhook:
                    url: "https://example.com/webhook"
                    event_types: ["monitor.event.detected"]
                  metadata:
                    key: "value"
              structured_output:
                summary: Monitor with structured output
                value:
                  query: "monitor ai news"
                  cadence: "daily"
                  output_schema:
                    type: "json"
                    json_schema:
                      type: "object"
                      properties:
                        company_name:
                          type: "string"
                          description: "Name of the company the news is about, NA if not company-specific"
                        sentiment:
                          type: "string"
                          description: "Sentiment of the news: positive or negative"
                        description:
                          type: "string"
                          description: "Brief description of the news"
      responses:
        "201":
          description: Monitor created successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MonitorResponse"
              example:
                monitor_id: "monitor_b0079f70195e4258a3b982c1b6d8bd3a"
                query: "Extract recent news about AI"
                status: "active"
                cadence: "daily"
                metadata:
                  key: "value"
                webhook:
                  url: "https://example.com/webhook"
                  event_types:
                    - "monitor.event.detected"
                created_at: "2025-04-23T20:21:48.037943Z"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "422":
          $ref: "#/components/responses/ValidationError"

    get:
      tags:
        - Monitors
      summary: List Monitors
      operationId: list_monitors
      description: |
        Retrieves a list of all monitors for the authenticated user.

        Returns monitors in reverse chronological order (most recently created first).
      responses:
        "200":
          description: List of monitors
          content:
            application/json:
              schema:
                type: object
                properties:
                  monitors:
                    type: array
                    items:
                      $ref: "#/components/schemas/MonitorResponse"
        "401":
          $ref: "#/components/responses/Unauthorized"

  /v1alpha/monitors/{monitor_id}:
    get:
      tags:
        - Monitors
      summary: Retrieve Monitor
      operationId: get_monitor
      description: |
        Retrieves details of a specific monitor by ID.

        Returns the monitor's current configuration, status, and metadata.
      parameters:
        - $ref: "#/components/parameters/MonitorId"
      responses:
        "200":
          description: Monitor details
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MonitorResponse"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/MonitorNotFound"

    patch:
      tags:
        - Monitors
      summary: Update Monitor
      operationId: update_monitor
      description: |
        Updates a monitor's configuration.

        You can update:
        - `cadence`: Change the monitoring frequency
        - `webhook`: Update webhook URL or event types
        - `metadata`: Update user-provided metadata

        The query cannot be updated after creation. To change the query, create a new monitor.
      parameters:
        - $ref: "#/components/parameters/MonitorId"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UpdateMonitorRequest"
            examples:
              update_cadence:
                summary: Update cadence
                value:
                  cadence: "weekly"
              update_webhook:
                summary: Update webhook
                value:
                  webhook:
                    url: "https://new-endpoint.com/webhook"
                    event_types:
                      ["monitor.event.detected", "monitor.execution.failed"]
              update_metadata:
                summary: Update metadata
                value:
                  metadata:
                    team: "product"
                    priority: "high"
      responses:
        "200":
          description: Monitor updated successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MonitorResponse"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/MonitorNotFound"
        "422":
          $ref: "#/components/responses/ValidationError"

    delete:
      tags:
        - Monitors
      summary: Delete Monitor
      operationId: delete_monitor
      description: |
        Deletes a monitor, stopping all future executions.

        Deleted monitors can no longer be updated or retrieved. This action is irreversible.

        Use this to clean up monitors you no longer need and reduce usage.
      parameters:
        - $ref: "#/components/parameters/MonitorId"
      responses:
        "200":
          description: Monitor deleted successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MonitorResponse"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/MonitorNotFound"

  /v1alpha/monitors/{monitor_id}/events:
    get:
      tags:
        - Events
      summary: List Events
      operationId: list_monitor_events
      description: |
        Lists events for a monitor from up to the last 300 event groups.

        Retrieves events from the monitor, including events with errors and material changes. The endpoint checks up to the specified lookback period or the previous 300 event groups, whichever is less.

        Events will be returned in reverse chronological order, with the most recent event groups first. All events from an event group will be flattened out into individual entries in the list.

        ## Event Types Returned

        - **Event** (`type: "event"`): Material change or discovery detected by the monitor
        - **Completion** (`type: "completion"`): Monitor run completed successfully without detected events
        - **Error** (`type: "error"`): Monitor run failed

        ## Structured Output Events

        When a monitor is configured with an output schema, events include a `result` field containing the parsed JSON object conforming to the schema.
      parameters:
        - $ref: "#/components/parameters/MonitorId"
        - name: lookback_period
          in: query
          required: false
          schema:
            type: string
            default: "10d"
            pattern: '^\d+[dw]$'
          description: |
            Lookback period to fetch events from. Sample values: `10d`, `1w`.

            - A minimum of 1 day is supported with one day increments
            - Use `d` for days, `w` for weeks
            - Examples: `7d` (7 days), `2w` (2 weeks)
      responses:
        "200":
          description: List of monitor events
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/MonitorEventList"
              examples:
                mixed_events:
                  summary: Mixed event types
                  value:
                    events:
                      - type: "event"
                        event_group_id: "mevtgrp_b0079f70195e4258eab1e7284340f1a9ec3a8033ed236a24"
                        output: "New product launch announced"
                        event_date: "2025-01-15"
                        source_urls:
                          - "https://example.com/news"
                        result:
                          type: "text"
                          content: "New product launch announced"
                      - type: "completion"
                        monitor_ts: "completed_2025-01-15T10:30:00Z"
                      - type: "error"
                        error: "Error occurred while processing the event"
                        id: "error_2025-01-15T10:30:00Z"
                        date: "2025-01-15T10:30:00Z"
                structured_output:
                  summary: Events with structured output
                  value:
                    events:
                      - type: "event"
                        event_group_id: "mevtgrp_f9727e22dd4a42ba5e7fdcaa36b2b8ea2ef7c11f15fb4061"
                        output: ""
                        event_date: "2025-12-02"
                        source_urls:
                          - "https://www.cnbc.com/2025/12/02/youtube-ai-biometric-data-creator-deepfake.html"
                        result:
                          type: "json"
                          content:
                            company_name: "YouTube/Google"
                            sentiment: "negative"
                            description: "YouTube expanded a likeness detection deepfake tracking tool"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/MonitorNotFound"
        "422":
          $ref: "#/components/responses/ValidationError"

  /v1alpha/monitors/{monitor_id}/event_groups/{event_group_id}:
    get:
      tags:
        - Events
      summary: Retrieve Event Group
      operationId: get_event_group
      description: |
        Retrieves all events within a specific event group.

        Event groups collect related results under a single `event_group_id`. Use this endpoint to fetch the complete set of results for a discovery when you receive an `event_group_id` in a webhook payload.

        ## Use with Webhooks

        When a webhook fires with a `monitor.event.detected` event, it returns an `event_group_id`. Use this endpoint to retrieve the full context of the discovery.

        ## Test Event Groups

        When you simulate a `monitor.event.detected` event, the webhook payload includes a test `event_group_id`. You can retrieve this test event group using this endpoint to verify your full webhook processing pipeline.
      parameters:
        - $ref: "#/components/parameters/MonitorId"
        - name: event_group_id
          in: path
          required: true
          schema:
            type: string
          description: The event group ID to retrieve
      responses:
        "200":
          description: Event group details
          content:
            application/json:
              schema:
                type: object
                properties:
                  events:
                    type: array
                    items:
                      $ref: "#/components/schemas/MonitorEventDetail"
              examples:
                text_result:
                  summary: Text output event group
                  value:
                    events:
                      - type: "event"
                        event_group_id: "mevtgrp_b0079f70195e4258eab1e7284340f1a9ec3a8033ed236a24"
                        output: "New product launch announced"
                        event_date: "2025-01-15"
                        source_urls:
                          - "https://example.com/news"
                        result:
                          type: "text"
                          content: "New product launch announced"
                json_result:
                  summary: Structured output event group
                  value:
                    events:
                      - type: "event"
                        event_group_id: "mevtgrp_f9727e22dd4a42ba5e7fdcaa36b2b8ea2ef7c11f15fb4061"
                        output: ""
                        event_date: "2025-12-02"
                        source_urls:
                          - "https://www.cnbc.com/2025/12/02/youtube-ai-biometric-data-creator-deepfake.html"
                        result:
                          type: "json"
                          content:
                            company_name: "YouTube/Google"
                            sentiment: "negative"
                            description: "YouTube expanded a likeness detection deepfake tracking tool"
                test_event_group:
                  summary: Test event group (no structured output)
                  value:
                    events:
                      - type: "event"
                        event_group_id: "test_abc"
                        output: ""
                        event_date: "2025-12-05"
                        source_urls:
                          - "https://test.example.com"
                        result:
                          type: "text"
                          content: "This is a test event."
                test_event_group_structured:
                  summary: Test event group (with structured output)
                  value:
                    events:
                      - type: "event"
                        event_group_id: "test_def"
                        output: ""
                        event_date: "2025-12-05"
                        source_urls:
                          - "https://test.example.com"
                        result:
                          type: "json"
                          content:
                            sentiment: ""
                            stock_ticker_symbol: ""
                            description: ""
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/NotFound"

  /v1alpha/monitors/{monitor_id}/simulate_event:
    post:
      tags:
        - Testing
      summary: Simulate Event
      operationId: simulate_event
      description: |
        Tests your webhook integration by simulating monitor events.

        The simulate event endpoint allows you to test your webhook integration without waiting for a scheduled monitor run.

        ## Test Event Groups

        When you simulate a `monitor.event.detected` event, the webhook payload includes a test `event_group_id`. You can retrieve this test event group using the standard retrieve event group endpoint.

        Test event group IDs return dummy event data, allowing you to verify your full webhook processing pipeline—from receiving the webhook to fetching event details.

        ## Prerequisites

        - The monitor must have a webhook configured
        - The webhook URL must be accessible
      parameters:
        - $ref: "#/components/parameters/MonitorId"
        - name: event_type
          in: query
          required: false
          schema:
            type: string
            enum:
              - monitor.event.detected
              - monitor.execution.completed
              - monitor.execution.failed
            default: monitor.event.detected
          description: Event type to simulate
      responses:
        "204":
          description: Event simulated successfully (webhook notification sent)
        "400":
          description: Webhook not configured for this monitor
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
              example:
                type: "error"
                error:
                  ref_id: "fcb2b4f3-c75e-4186-87bc-caa1a8381331"
                  message: "Webhook not configured for this monitor"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "404":
          $ref: "#/components/responses/MonitorNotFound"

components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: x-api-key
      description: |
        API key for authentication. Generate your API key on the Parallel Platform.

        Set your API key in the `x-api-key` header for all requests.

  parameters:
    MonitorId:
      name: monitor_id
      in: path
      required: true
      schema:
        type: string
      description: The unique identifier for the monitor

  responses:
    Unauthorized:
      description: "Unauthorized: invalid or missing credentials"
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            type: "error"
            error:
              ref_id: "fcb2b4f3-c75e-4186-87bc-caa1a8381331"
              message: "Unauthorized: invalid or missing credentials"

    ValidationError:
      description: "Unprocessable content: request validation error"
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            type: "error"
            error:
              ref_id: "fcb2b4f3-c75e-4186-87bc-caa1a8381331"
              message: "Unprocessable content: request validation error"

    MonitorNotFound:
      description: Monitor not found
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            type: "error"
            error:
              ref_id: "fcb2b4f3-c75e-4186-87bc-caa1a8381331"
              message: "Monitor not found"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            type: "error"
            error:
              ref_id: "fcb2b4f3-c75e-4186-87bc-caa1a8381331"
              message: "Resource not found"

  schemas:
    CreateMonitorRequest:
      type: object
      required:
        - query
        - cadence
      properties:
        query:
          type: string
          description: |
            Search query to monitor for material changes.

            Write queries in natural language that clearly describe what you're looking for. The query should focus on intent rather than keywords.
          examples:
            - "Extract recent news about AI"
            - "Let me know when someone mentions Parallel Web Systems on the web"
            - "Alert me when the price for AirPods drops below $150"
        cadence:
          type: string
          enum:
            - hourly
            - daily
            - weekly
          description: |
            Cadence of the monitor.

            - `hourly`: For fast-moving topics
            - `daily`: For most news and updates
            - `weekly`: For slower changes
        webhook:
          $ref: "#/components/schemas/MonitorWebhook"
        metadata:
          type: object
          additionalProperties:
            type: string
          nullable: true
          description: |
            User-provided metadata stored with the monitor.

            This field is returned in webhook notifications and GET requests, enabling you to map responses to corresponding objects in your application.

            For example, if you are building a Slackbot that monitors changes, you could store the Slack thread ID here to properly route webhook responses back to the correct conversation thread.
          example:
            slack_thread_id: "1234567890.123456"
            user_id: "U123ABC"
        output_schema:
          $ref: "#/components/schemas/JsonSchema"

    UpdateMonitorRequest:
      type: object
      properties:
        cadence:
          type: string
          enum:
            - hourly
            - daily
            - weekly
          description: Updated cadence for the monitor
        webhook:
          $ref: "#/components/schemas/MonitorWebhook"
        metadata:
          type: object
          additionalProperties:
            type: string
          nullable: true
          description: Updated user-provided metadata

    MonitorResponse:
      type: object
      required:
        - monitor_id
        - query
        - status
        - cadence
        - created_at
      properties:
        monitor_id:
          type: string
          description: Unique identifier for the monitor
        query:
          type: string
          description: The query being monitored
          example: "Recent news about LLM models."
        status:
          type: string
          enum:
            - active
            - canceled
          description: Current status of the monitor
        cadence:
          type: string
          enum:
            - hourly
            - daily
            - weekly
          description: Frequency of monitor runs
        metadata:
          type: object
          additionalProperties:
            type: string
          nullable: true
          description: User-provided metadata stored with the monitor
        webhook:
          $ref: "#/components/schemas/MonitorWebhook"
        created_at:
          type: string
          format: date-time
          description: Timestamp when the monitor was created
          example: "2025-01-15T10:30:00Z"
        last_run_at:
          type: string
          format: date-time
          nullable: true
          description: Timestamp of the last monitor run
          example: "2025-01-15T10:30:00Z"

    MonitorWebhook:
      type: object
      required:
        - url
      properties:
        url:
          type: string
          format: uri
          description: |
            URL for the webhook endpoint.

            This can be any domain you control. The endpoint will receive POST requests with event payloads.
          example: "https://example.com/webhook"
        event_types:
          type: array
          items:
            type: string
            enum:
              - monitor.event.detected
              - monitor.execution.completed
              - monitor.execution.failed
          description: |
            Event types to send webhook notifications for.

            - `monitor.event.detected`: Emitted when a run detects one or more material events
            - `monitor.execution.completed`: Emitted when a Monitor run completes successfully (without detected events)
            - `monitor.execution.failed`: Emitted when a Monitor run fails due to an error

            Note: `monitor.event.detected` and `monitor.execution.completed` are mutually distinct and correspond to different runs.
      description: |
        Webhook configuration for a monitor.

        ## Webhook Payload Structure

        For `monitor.event.detected`:
        ```json
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

        For `monitor.execution.completed`:
        ```json
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

        For `monitor.execution.failed`:
        ```json
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

    JsonSchema:
      type: object
      required:
        - json_schema
      properties:
        type:
          type: string
          const: json
          default: json
          description: The type of schema being defined. Always `json`.
        json_schema:
          type: object
          additionalProperties: true
          description: |
            A JSON Schema object. Only a subset of JSON Schema is supported.

            ## Best Practices

            - Include property descriptions for each property to improve extraction accuracy
            - Use primitive types (limit to `string` and `enum` for reliable parsing)
            - Maintain flat schemas (3-5 properties with single-level object structure)
            - Define edge case handling (specify how missing or inapplicable values should be represented)

            ## Schema Complexity

            Output schemas are currently limited to the complexity supported by the core processor. Use flat schemas with a small number of clearly defined fields.
          example:
            type: "object"
            properties:
              gdp:
                type: "string"
                description: "GDP in USD for the year, formatted like '$3.1 trillion (2023)'"
            required:
              - gdp
            additionalProperties: false

    MonitorEventList:
      type: object
      required:
        - events
      properties:
        events:
          type: array
          description: List of execution events for the monitor
          items:
            oneOf:
              - $ref: "#/components/schemas/MonitorEventDetail"
              - $ref: "#/components/schemas/MonitorCompletion"
              - $ref: "#/components/schemas/MonitorExecutionError"
            discriminator:
              propertyName: type
              mapping:
                event: "#/components/schemas/MonitorEventDetail"
                completion: "#/components/schemas/MonitorCompletion"
                error: "#/components/schemas/MonitorExecutionError"

    MonitorEventDetail:
      type: object
      required:
        - type
        - event_group_id
        - output
        - source_urls
        - result
      properties:
        type:
          type: string
          enum:
            - event
          const: event
          default: event
          description: Type of the event
        event_group_id:
          type: string
          description: |
            Event group ID.

            Related events share the same event_group_id. Use this with the retrieve event group endpoint to fetch all events in the group.
        output:
          type: string
          deprecated: true
          description: "Detected change or event. Deprecated: use 'result' field instead."
        event_date:
          type: string
          format: date
          nullable: true
          description: Date when event occurred
          example: "2025-01-15"
        source_urls:
          type: array
          items:
            type: string
            format: uri
          description: List of source URLs supporting the event
          example:
            - "https://example.com/news"
        result:
          oneOf:
            - $ref: "#/components/schemas/MonitorEventTextResult"
            - $ref: "#/components/schemas/MonitorEventJsonResult"
          discriminator:
            propertyName: type
            mapping:
              text: "#/components/schemas/MonitorEventTextResult"
              json: "#/components/schemas/MonitorEventJsonResult"
          description: |
            Output from the event. Either Text or JSON output.

            For monitors without an output schema, this will be a text result. For monitors with an output schema, this will be a JSON result conforming to the schema.

    MonitorEventTextResult:
      type: object
      required:
        - type
        - content
      properties:
        type:
          type: string
          enum:
            - text
          const: text
          default: text
          description: Type of the result
        content:
          type: string
          description: Text content of the result

    MonitorEventJsonResult:
      type: object
      required:
        - type
        - content
      properties:
        type:
          type: string
          enum:
            - json
          const: json
          default: json
          description: Type of the result
        content:
          type: object
          additionalProperties: true
          description: |
            JSON content of the result.

            This object conforms to the output schema defined when creating the monitor.

    MonitorCompletion:
      type: object
      required:
        - type
        - monitor_ts
      properties:
        type:
          type: string
          enum:
            - completion
          const: completion
          default: completion
          description: Type of the event
        monitor_ts:
          type: string
          description: Identifier for the completed event
          example: "completed_2025-01-15T10:30:00Z"

    MonitorExecutionError:
      type: object
      required:
        - type
        - error
        - id
        - date
      properties:
        type:
          type: string
          enum:
            - error
          const: error
          default: error
          description: Type of the event
        error:
          type: string
          description: Human-readable error message
        id:
          type: string
          description: Identifier for the error event
        date:
          type: string
          format: date-time
          description: Timestamp when the error occurred

    ErrorResponse:
      type: object
      required:
        - type
        - error
      properties:
        type:
          type: string
          const: error
          description: Always 'error'
        error:
          $ref: "#/components/schemas/Error"

    Error:
      type: object
      required:
        - ref_id
        - message
      properties:
        ref_id:
          type: string
          description: Reference ID for the error
        message:
          type: string
          description: Human-readable error message
        detail:
          type: object
          additionalProperties: true
          nullable: true
          description: Optional detail supporting the error
````
