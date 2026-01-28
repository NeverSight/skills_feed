---
name: findall-openapi
description: Findall API integration of Parallel. Use when building applications with Parallel FindAll API.
# https://contextarea.com/rules-httpsrawg-9u7y7y9mb3sw4m
---

````yaml
openapi: 3.1.0
info:
  title: Parallel FindAll API
  version: 0.1.2
  description: |
    # FindAll API

    The FindAll API discovers and evaluates entities that match complex criteria from natural language objectives. Submit a high-level goal and the service automatically generates structured match conditions, discovers relevant candidates, and evaluates each against the criteria. Returns comprehensive results with detailed reasoning, citations, and confidence scores for each match decision.

    ## Core Concepts

    ### FindAll Lifecycle

    A FindAll run progresses through several statuses:

    1. **queued** - Run has been created and is waiting to start
    2. **action_required** - User input needed (e.g., schema review)
    3. **running** - Actively discovering and evaluating candidates
    4. **completed** - Successfully finished with all results available
    5. **failed** - Encountered an error during execution
    6. **cancelling** - Cancel request received, shutting down
    7. **cancelled** - Successfully cancelled by user

    **Active statuses**: queued, action_required, running, cancelling
    **Terminal statuses**: completed, failed, cancelled

    Termination reasons when in terminal status:
    - `low_match_rate` - Too few matches found relative to candidates evaluated
    - `match_limit_met` - Reached the specified match limit
    - `candidates_exhausted` - No more candidates to evaluate
    - `user_cancelled` - User requested cancellation
    - `error_occurred` - System error during execution
    - `timeout` - Run exceeded maximum allowed time

    ### FindAll Candidates

    Candidates represent entities being evaluated against match conditions. Each candidate has:

    - **candidate_id** - Unique identifier
    - **name** - Entity name
    - **url** - Context URL for disambiguation
    - **description** - Brief description (optional)
    - **match_status** - One of: generated, matched, unmatched, discarded
    - **output** - Structured results of match condition evaluations
    - **basis** - Citations, reasoning, and confidence for each field

    A candidate is considered a **match** only if ALL match conditions are satisfied.

    Match status progression:
    1. `generated` - Candidate discovered and queued for evaluation
    2. `matched` - All match conditions satisfied
    3. `unmatched` - One or more match conditions not satisfied
    4. `discarded` - Removed from evaluation (duplicate, invalid, etc.)

    ### Generator Pricing

    FindAll supports multiple generator tiers with different cost/quality tradeoffs:

    - **base** - Fast, economical for simple criteria
    - **core** - Balanced performance and accuracy (recommended)
    - **pro** - Higher accuracy for complex requirements
    - **preview** - Latest experimental features

    Costs vary by generator tier and number of candidates evaluated. See pricing documentation for details.

    ## Features

    ### Match Conditions

    Match conditions define what makes an entity a match. Each condition has:
    - **name** - Identifier for the condition
    - **description** - Detailed criteria (be specific for best results)

    Example:
    ```json
    {
      "name": "soc2_type_ii_certified",
      "description": "Company must have SOC2 Type II certification (not Type I). Look for evidence in: trust centers, security/compliance pages, audit reports, or press releases specifically mentioning 'SOC2 Type II'. If no explicit SOC2 Type II mention is found, consider requirement not satisfied."
    }
    ```

    ### Enrichment

    After initial matching, enrich candidates with additional structured data:

    - Define custom output schema for enrichment data
    - Specify processor tier (base, core, pro, preview)
    - Use MCP servers for specialized data sources
    - Enrichment runs on matched candidates only

    ### Extension

    Increase the match limit of an active run to find more matches:

    - Specify additional matches to find
    - New limit = current limit + additional matches
    - Only works on active runs
    - Useful when initial results are promising

    ### Cancellation

    Stop a FindAll run before completion:

    - Only works on active runs (not terminal statuses)
    - Run transitions to 'cancelling' then 'cancelled'
    - Partial results remain available
    - Termination reason set to 'user_cancelled'

    ### Real-time Updates (SSE)

    Stream events via Server-Sent Events for real-time progress:

    Event types:
    - `findall.schema.updated` - Schema modified (e.g., after ingest)
    - `findall.status` - Run status changed
    - `findall.candidate.generated` - New candidate discovered
    - `findall.candidate.matched` - Candidate matched all conditions
    - `findall.candidate.unmatched` - Candidate failed one or more conditions
    - `findall.candidate.discarded` - Candidate removed from evaluation
    - `findall.candidate.enriched` - Enrichment data added

    Resume from specific event using `last_event_id` parameter.

    ### Webhooks

    Receive HTTP notifications for run events:

    - Specify webhook URL and event types during run creation
    - Receive POST requests with event data
    - Useful for async workflows and integrations

    Supported event types: `task_run.status`

    ### Preview Features

    Access experimental capabilities via the `parallel-beta` header:

    - Schema auto-generation from natural language
    - Advanced matching algorithms
    - Specialized processors

    Features may change or be deprecated without notice.

    ## Migration Guide

    When migrating existing code:

    1. Update endpoint URLs to `/v1beta/findall/*`
    2. Replace task-based polling with SSE streaming
    3. Use structured match conditions instead of free-form objectives
    4. Leverage enrichment for additional data extraction
    5. Implement webhook handlers for production workflows

    ## Quick Start

    Basic workflow:

    1. **(Optional) Generate schema** - Use `/v1beta/findall/ingest` to convert natural language to structured schema
    2. **Create run** - POST to `/v1beta/findall/runs` with objective, entity_type, match_conditions, and generator
    3. **Monitor progress** - Stream events via `/v1beta/findall/runs/{id}/events` or poll status
    4. **Get results** - Retrieve snapshot via `/v1beta/findall/runs/{id}/result`
    5. **(Optional) Extend** - Add more matches if needed
    6. **(Optional) Enrich** - Add structured data to matches

    Example:
    ```json
    {
      "objective": "Find all AI companies that raised Series A funding in 2024",
      "entity_type": "companies",
      "match_conditions": [
        {
          "name": "developing_ai_products",
          "description": "Company must be developing artificial intelligence products"
        },
        {
          "name": "raised_series_a_2024",
          "description": "Company must have raised Series A funding in 2024"
        }
      ],
      "generator": "core",
      "match_limit": 50
    }
    ```
  contact:
    name: Parallel Support
    url: https://parallel.ai
    email: support@parallel.ai

servers:
  - url: https://api.parallel.ai
    description: Parallel API Production

security:
  - ApiKeyAuth: []

tags:
  - name: Schema Generation
    description: Convert natural language objectives to structured FindAll specifications
  - name: Run Management
    description: Create and monitor FindAll runs
  - name: Results
    description: Retrieve FindAll results and status
  - name: Extensions
    description: Modify active FindAll runs (extend, enrich, cancel)
  - name: Streaming
    description: Real-time event streams for FindAll runs

paths:
  /v1beta/findall/ingest:
    post:
      tags:
        - Schema Generation
      summary: Generate FindAll Schema
      description: |
        Transforms a natural language search objective into a structured FindAll specification.

        **Note**: This endpoint requires the `parallel-beta` header.

        The generated specification serves as a suggested starting point and can be further customized before creating a run.

        Use this to:
        - Convert free-form objectives to structured match conditions
        - Get suggested entity types and field definitions
        - Bootstrap FindAll runs with AI-generated schemas

        The output can be directly used as input to `POST /v1beta/findall/runs` or modified as needed.
      operationId: ingestFindAllRun
      parameters:
        - $ref: "#/components/parameters/ParallelBeta"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/IngestInput"
      responses:
        "200":
          description: Successfully generated FindAll schema
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FindAllSchema"
        "422":
          $ref: "#/components/responses/ValidationError"

  /v1beta/findall/runs:
    post:
      tags:
        - Run Management
      summary: Create FindAll Run
      description: |
        Starts a new FindAll run to discover and evaluate entities matching specified criteria.

        This endpoint immediately returns a FindAll run object with status 'queued'. The run will progress through various statuses as it executes.

        **Track Progress**:
        - Poll status: `GET /v1beta/findall/runs/{findall_id}`
        - Stream events: `GET /v1beta/findall/runs/{findall_id}/events` (recommended)
        - Webhooks: Specify webhook in request body

        **Get Results**:
        - Snapshot: `GET /v1beta/findall/runs/{findall_id}/result`

        **Match Limit**: Specifies maximum matches to find (5-1000). Run may terminate early if:
        - Match rate is too low (insufficient quality candidates)
        - All candidates exhausted
        - System timeout reached

        **Exclude List**: Optionally specify entities to exclude from results by name/URL.

        **Metadata**: Attach arbitrary key-value pairs for tracking and organization.
      operationId: createFindAllRun
      parameters:
        - $ref: "#/components/parameters/ParallelBeta"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/FindAllRunInput"
      responses:
        "200":
          description: FindAll run created successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FindAllRun"
        "402":
          $ref: "#/components/responses/PaymentRequired"
        "422":
          $ref: "#/components/responses/UnprocessableEntity"
        "429":
          $ref: "#/components/responses/TooManyRequests"

  /v1beta/findall/runs/{findall_id}:
    get:
      tags:
        - Results
      summary: Get FindAll Run Status
      description: |
        Retrieves current status and metadata for a FindAll run.

        Use this to:
        - Check run progress (status, metrics)
        - Determine if run is still active
        - Get termination reason for completed runs

        For detailed results including candidates, use `GET /v1beta/findall/runs/{findall_id}/result` instead.

        For real-time updates, use `GET /v1beta/findall/runs/{findall_id}/events` (SSE streaming).
      operationId: getFindAllRun
      parameters:
        - $ref: "#/components/parameters/FindAllId"
        - $ref: "#/components/parameters/ParallelBeta"
      responses:
        "200":
          description: FindAll run status retrieved
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FindAllRun"
        "422":
          $ref: "#/components/responses/ValidationError"

  /v1beta/findall/runs/{findall_id}/result:
    get:
      tags:
        - Results
      summary: Get FindAll Run Result
      description: |
        Retrieves a complete snapshot of FindAll run results at the time of request.

        Returns:
        - Run metadata and status
        - All evaluated candidates with match status
        - Output data and reasoning for each candidate
        - Last event ID (for resuming event streams)

        This is a point-in-time snapshot. For active runs, results will continue to update. Use the `last_event_id` from the response to resume streaming from this point.

        **Result Structure**:
        - `run` - Current run status and metadata
        - `candidates` - Array of all evaluated candidates
        - `last_event_id` - ID of most recent event (for SSE resumption)

        Candidates include full details: output data, citations, reasoning, and confidence scores.
      operationId: getFindAllResult
      parameters:
        - $ref: "#/components/parameters/FindAllId"
        - $ref: "#/components/parameters/ParallelBeta"
      responses:
        "200":
          description: FindAll result snapshot retrieved
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FindAllRunResult"
        "422":
          $ref: "#/components/responses/ValidationError"

  /v1beta/findall/runs/{findall_id}/schema:
    get:
      tags:
        - Results
      summary: Get FindAll Run Schema
      description: |
        Retrieves the schema definition for a FindAll run.

        Returns:
        - Objective (natural language goal)
        - Entity type
        - Match conditions with descriptions
        - Enrichment configurations (if any)
        - Generator tier
        - Match limit

        Useful for:
        - Understanding run configuration
        - Debugging match conditions
        - Replicating runs with modifications
      operationId: getFindAllSchema
      parameters:
        - $ref: "#/components/parameters/FindAllId"
        - $ref: "#/components/parameters/ParallelBeta"
      responses:
        "200":
          description: FindAll schema retrieved
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FindAllSchema"
        "422":
          $ref: "#/components/responses/ValidationError"

  /v1beta/findall/runs/{findall_id}/events:
    get:
      tags:
        - Streaming
      summary: Stream FindAll Events (SSE)
      description: |
        Opens a Server-Sent Events (SSE) stream for real-time FindAll run updates.

        **Event Types**:
        - `findall.schema.updated` - Schema modified (e.g., after ingest)
        - `findall.status` - Run status changed
        - `findall.candidate.generated` - New candidate discovered
        - `findall.candidate.matched` - Candidate matched all conditions
        - `findall.candidate.unmatched` - Candidate failed conditions
        - `findall.candidate.discarded` - Candidate removed from evaluation
        - `findall.candidate.enriched` - Enrichment data added

        **Resumption**: Use `last_event_id` parameter to resume from a specific point. Get this ID from:
        - Previous event stream disconnect
        - Result snapshot (`GET /v1beta/findall/runs/{id}/result`)

        **Timeout**: Optional timeout in seconds. If not specified, connection stays open while run is active. If set, stream closes after specified duration.

        **Best Practices**:
        - Implement reconnection logic with exponential backoff
        - Store last_event_id to resume from disconnects
        - Handle all event types gracefully
        - Close connection when run reaches terminal status
      operationId: streamFindAllEvents
      parameters:
        - $ref: "#/components/parameters/FindAllId"
        - name: last_event_id
          in: query
          required: false
          description: Event ID to resume streaming from (for reconnection)
          schema:
            type: string
            nullable: true
        - name: timeout
          in: query
          required: false
          description: Timeout in seconds. If not set, keeps connection alive while run is active
          schema:
            type: number
            nullable: true
        - $ref: "#/components/parameters/ParallelBeta"
      responses:
        "200":
          description: Event stream opened successfully
          content:
            text/event-stream:
              schema:
                oneOf:
                  - $ref: "#/components/schemas/FindAllSchemaUpdatedEvent"
                  - $ref: "#/components/schemas/FindAllRunStatusEvent"
                  - $ref: "#/components/schemas/FindAllCandidateEvent"
                  - $ref: "#/components/schemas/ErrorEvent"
        "404":
          $ref: "#/components/responses/NotFound"
        "422":
          $ref: "#/components/responses/ValidationError"

  /v1beta/findall/runs/{findall_id}/extend:
    post:
      tags:
        - Extensions
      summary: Extend FindAll Run
      description: |
        Increases the match limit of an active FindAll run to find more matches.

        **When to Use**:
        - Initial results are promising and you want more
        - Original match_limit was too conservative
        - Business needs changed during run execution

        **Requirements**:
        - Run must be in active status (queued, action_required, running)
        - Additional match limit must be > 0

        **Behavior**:
        - New limit = current limit + additional_match_limit
        - Run continues from current state
        - Does not restart evaluation

        **Example**: If original limit was 50 and you extend by 25, new limit is 75.

        **Note**: Extension does not guarantee finding additional matches. Run may still terminate early if candidates are exhausted or match rate is too low.
      operationId: extendFindAllRun
      parameters:
        - $ref: "#/components/parameters/FindAllId"
        - $ref: "#/components/parameters/ParallelBeta"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/FindAllExtendInput"
      responses:
        "200":
          description: FindAll run extended successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FindAllSchema"
        "404":
          $ref: "#/components/responses/NotFound"
        "422":
          $ref: "#/components/responses/ValidationError"

  /v1beta/findall/runs/{findall_id}/enrich:
    post:
      tags:
        - Extensions
      summary: Add Enrichment to FindAll Run
      description: |
        Adds structured data enrichment to matched candidates in a FindAll run.

        **Use Cases**:
        - Extract additional fields from matched entities
        - Get company financials, tech stack, team size, etc.
        - Integrate with external data sources via MCP servers

        **Enrichment Flow**:
        1. Define output schema (JSON Schema format)
        2. Select processor tier (base, core, pro, preview)
        3. Optionally configure MCP servers for specialized tools
        4. Enrichment runs on matched candidates only

        **Output Schema**: Specify the structure of enrichment data using JSON Schema. Only a subset of JSON Schema is supported (see examples).

        **MCP Servers**: Configure Model Context Protocol servers for accessing external APIs, databases, or specialized tools during enrichment.

        **Processor Selection**:
        - base: Fast, economical
        - core: Balanced (recommended)
        - pro: Higher accuracy
        - preview: Experimental features

        **Note**: Enrichment is applied to candidates that have matched all conditions. Unmatched candidates are not enriched.
      operationId: enrichFindAllRun
      parameters:
        - $ref: "#/components/parameters/FindAllId"
        - $ref: "#/components/parameters/ParallelBeta"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/FindAllEnrichInput"
      responses:
        "200":
          description: Enrichment added successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FindAllSchema"
        "404":
          $ref: "#/components/responses/NotFound"
        "422":
          $ref: "#/components/responses/ValidationError"

  /v1beta/findall/runs/{findall_id}/cancel:
    post:
      tags:
        - Extensions
      summary: Cancel FindAll Run
      description: |
        Cancels an active FindAll run before completion.

        **Requirements**:
        - Run must be in active status (queued, action_required, running, cancelling)
        - Cannot cancel terminal runs (completed, failed, cancelled)

        **Behavior**:
        - Run transitions to 'cancelling' status immediately
        - Current work completes gracefully
        - Status changes to 'cancelled' when shutdown complete
        - Termination reason set to 'user_cancelled'

        **Partial Results**: All candidates evaluated before cancellation remain available via the result endpoint.

        **Use Cases**:
        - Accidentally started wrong run
        - Results no longer needed
        - Want to modify parameters and restart
        - Cost control
      operationId: cancelFindAllRun
      parameters:
        - $ref: "#/components/parameters/FindAllId"
        - $ref: "#/components/parameters/ParallelBeta"
      responses:
        "200":
          description: FindAll run cancellation initiated
          content:
            application/json:
              schema:
                type: object
        "404":
          $ref: "#/components/responses/NotFound"
        "409":
          description: Cannot cancel a terminated FindAll run
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
        "422":
          $ref: "#/components/responses/ValidationError"

components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: x-api-key
      description: |
        API key for authentication. Get your API key from the Parallel dashboard.

        Include in all requests as: `x-api-key: YOUR_API_KEY`

  parameters:
    FindAllId:
      name: findall_id
      in: path
      required: true
      description: Unique identifier for the FindAll run
      schema:
        type: string

    ParallelBeta:
      name: parallel-beta
      in: header
      required: false
      description: |
        Optional header to enable beta features.

        Comma-separated list of beta features to enable.
        Some endpoints require this header for access.
      schema:
        type: string
        nullable: true

  schemas:
    IngestInput:
      type: object
      required:
        - objective
      properties:
        objective:
          type: string
          description: |
            Natural language objective to convert into a FindAll run specification.

            Be specific and include all requirements. The AI will generate:
            - Suggested entity type
            - Structured match conditions
            - Field definitions
          example: Find all AI companies that raised Series A funding in 2024

    FindAllRunInput:
      type: object
      required:
        - objective
        - entity_type
        - match_conditions
        - generator
        - match_limit
      properties:
        objective:
          type: string
          description: Natural language objective describing what to find
          example: Find all AI companies that raised Series A funding in 2024
        entity_type:
          type: string
          description: |
            Type of entity being searched for (e.g., companies, people, products, events).

            Should be a plural noun that describes the category of entities.
        match_conditions:
          type: array
          items:
            $ref: "#/components/schemas/MatchCondition"
          description: |
            List of conditions that must ALL be satisfied for an entity to match.

            Each condition should be atomic and specific. Use detailed descriptions for best results.
        generator:
          type: string
          enum: [base, core, pro, preview]
          description: |
            Generator tier to use for the FindAll run.

            - base: Fast, economical for simple criteria
            - core: Balanced performance and accuracy (recommended)
            - pro: Higher accuracy for complex requirements
            - preview: Latest experimental features
        match_limit:
          type: integer
          minimum: 5
          maximum: 1000
          description: |
            Maximum number of matches to find.

            Run may terminate early if:
            - Match rate too low
            - Candidates exhausted
            - System timeout
        exclude_list:
          type: array
          items:
            $ref: "#/components/schemas/ExcludeCandidate"
          nullable: true
          description: |
            Optional list of entities to exclude from results.

            Specify by name and/or URL. Useful for filtering out known entities or duplicates.
        metadata:
          type: object
          additionalProperties:
            oneOf:
              - type: string
              - type: integer
              - type: number
              - type: boolean
          nullable: true
          description: |
            Optional metadata key-value pairs for tracking and organization.

            Stored with run and returned in all status/result queries.
        webhook:
          $ref: "#/components/schemas/Webhook"
          nullable: true
          description: Optional webhook configuration for event notifications

    FindAllExtendInput:
      type: object
      required:
        - additional_match_limit
      properties:
        additional_match_limit:
          type: integer
          minimum: 1
          description: |
            Number of additional matches to find.

            This value is added to the current match limit.
            Example: Current limit 50 + additional 25 = new limit 75

    FindAllEnrichInput:
      type: object
      required:
        - output_schema
      properties:
        processor:
          type: string
          default: core
          description: Processor tier to use for enrichment (base, core, pro, preview)
        output_schema:
          $ref: "#/components/schemas/JsonSchema"
          description: |
            JSON Schema defining the structure of enrichment data to extract.

            Only a subset of JSON Schema is supported. See examples for details.
        mcp_servers:
          type: array
          items:
            $ref: "#/components/schemas/McpServer"
          nullable: true
          description: |
            Optional list of Model Context Protocol servers for specialized tools.

            Use MCP servers to access external APIs, databases, or custom tools during enrichment.

    MatchCondition:
      type: object
      required:
        - name
        - description
      properties:
        name:
          type: string
          description: Identifier for this match condition (used in output fields)
        description:
          type: string
          description: |
            Detailed description of what must be true for this condition to be satisfied.

            **Be specific**: Include details about what evidence to look for, where to find it, and how to interpret it.

            **Good practices**:
            - Specify exact terms or certifications
            - List acceptable sources of evidence
            - Define edge cases and how to handle them
            - Include what constitutes insufficient evidence
          example: |
            Company must have SOC2 Type II certification (not Type I). Look for evidence in: trust centers, security/compliance pages, audit reports, or press releases specifically mentioning 'SOC2 Type II'. If no explicit SOC2 Type II mention is found, consider requirement not satisfied.

    ExcludeCandidate:
      type: object
      required:
        - name
        - url
      properties:
        name:
          type: string
          description: Name of the entity to exclude
        url:
          type: string
          description: URL of the entity to exclude

    Webhook:
      type: object
      required:
        - url
      properties:
        url:
          type: string
          format: uri
          description: URL to receive webhook POST requests
        event_types:
          type: array
          items:
            type: string
            enum: [task_run.status]
          default: []
          description: |
            Event types to send webhook notifications for.

            Currently supported: task_run.status

    JsonSchema:
      type: object
      required:
        - json_schema
      properties:
        json_schema:
          type: object
          additionalProperties: true
          description: |
            JSON Schema object defining output structure.

            Only a subset of JSON Schema is supported:
            - type: string, number, integer, boolean, object, array
            - properties: object with property definitions
            - required: array of required property names
            - description: field descriptions
            - additionalProperties: typically false

            Not supported: $ref, allOf, anyOf, oneOf, complex validation rules
          example:
            type: object
            additionalProperties: false
            required: [ceo_name, employee_count]
            properties:
              ceo_name:
                type: string
                description: Name of the current CEO
              employee_count:
                type: integer
                description: Approximate number of full-time employees
        type:
          type: string
          const: json
          default: json
          description: Schema type (always "json")

    McpServer:
      type: object
      required:
        - url
        - name
      properties:
        type:
          type: string
          const: url
          default: url
          description: Type of MCP server (always "url")
        url:
          type: string
          format: uri
          description: URL of the MCP server endpoint
        headers:
          type: object
          additionalProperties:
            type: string
            format: password
            writeOnly: true
          nullable: true
          description: Optional HTTP headers for MCP server requests
        name:
          type: string
          description: Name identifier for this MCP server
        allowed_tools:
          type: array
          items:
            type: string
          nullable: true
          description: |
            Optional list of allowed tools from this server.

            If not specified, all tools are allowed.

    FindAllSchema:
      type: object
      required:
        - objective
        - entity_type
        - match_conditions
      properties:
        objective:
          type: string
          description: Natural language objective of the FindAll run
          example: Find all AI companies that raised Series A funding in 2024
        entity_type:
          type: string
          description: Type of entity being searched for
        match_conditions:
          type: array
          items:
            $ref: "#/components/schemas/MatchCondition"
          description: List of conditions that must all be satisfied
        enrichments:
          type: array
          items:
            $ref: "#/components/schemas/FindAllEnrichInput"
          nullable: true
          description: List of enrichment configurations (if any)
        generator:
          type: string
          enum: [base, core, pro, preview]
          default: core
          description: Generator tier used for this run
        match_limit:
          type: integer
          nullable: true
          description: Maximum number of matches to find

    FindAllRun:
      type: object
      required:
        - findall_id
        - status
        - generator
      properties:
        findall_id:
          type: string
          description: Unique identifier for this FindAll run
        status:
          $ref: "#/components/schemas/FindAllRunStatus"
        generator:
          type: string
          enum: [base, core, pro, preview]
          description: Generator tier used for this run
        metadata:
          type: object
          additionalProperties:
            oneOf:
              - type: string
              - type: integer
              - type: number
              - type: boolean
          nullable: true
          description: User-provided metadata
        created_at:
          type: string
          format: date-time
          nullable: true
          description: Timestamp when run was created (RFC 3339 format)
        modified_at:
          type: string
          format: date-time
          nullable: true
          description: Timestamp of last result modification (RFC 3339 format)

    FindAllRunStatus:
      type: object
      required:
        - status
        - is_active
        - metrics
      properties:
        status:
          type: string
          enum:
            [
              queued,
              action_required,
              running,
              completed,
              failed,
              cancelling,
              cancelled,
            ]
          description: |
            Current status of the FindAll run.

            Active: queued, action_required, running, cancelling
            Terminal: completed, failed, cancelled
        is_active:
          type: boolean
          description: True if run is in an active (non-terminal) status
        metrics:
          $ref: "#/components/schemas/FindAllCandidateMetrics"
        termination_reason:
          type: string
          enum:
            [
              low_match_rate,
              match_limit_met,
              candidates_exhausted,
              user_cancelled,
              error_occurred,
              timeout,
            ]
          nullable: true
          description: |
            Reason for termination (only set when status is terminal).

            - low_match_rate: Too few matches relative to candidates evaluated
            - match_limit_met: Reached specified match limit
            - candidates_exhausted: No more candidates available
            - user_cancelled: User requested cancellation
            - error_occurred: System error during execution
            - timeout: Run exceeded maximum allowed time

    FindAllCandidateMetrics:
      type: object
      properties:
        generated_candidates_count:
          type: integer
          default: 0
          description: Number of candidates discovered and queued for evaluation
        matched_candidates_count:
          type: integer
          default: 0
          description: Number of candidates that matched all conditions

    FindAllRunResult:
      type: object
      required:
        - run
        - candidates
      properties:
        run:
          $ref: "#/components/schemas/FindAllRun"
          description: Current run status and metadata
        candidates:
          type: array
          items:
            $ref: "#/components/schemas/FindAllCandidate"
          description: All evaluated candidates at time of snapshot
        last_event_id:
          type: string
          nullable: true
          description: |
            ID of the most recent event at time of snapshot.

            Use this to resume event streaming from this point.

    FindAllCandidate:
      type: object
      required:
        - candidate_id
        - name
        - url
        - match_status
      properties:
        candidate_id:
          type: string
          description: Unique identifier for this candidate
        name:
          type: string
          description: Entity name
        url:
          type: string
          format: uri
          description: URL providing context for entity disambiguation
        description:
          type: string
          nullable: true
          description: Brief description of the entity
        match_status:
          type: string
          enum: [generated, matched, unmatched, discarded]
          description: |
            Current match status:
            - generated: Discovered, queued for evaluation
            - matched: Satisfied all match conditions
            - unmatched: Failed one or more conditions
            - discarded: Removed from evaluation
        output:
          type: object
          additionalProperties: true
          nullable: true
          description: |
            Structured results of match condition evaluations.

            Contains field values determined during evaluation. A candidate is a match only if ALL match conditions are satisfied.
        basis:
          type: array
          items:
            $ref: "#/components/schemas/FieldBasis"
          nullable: true
          description: Citations, reasoning, and confidence for each output field

    FieldBasis:
      type: object
      required:
        - field
        - reasoning
      properties:
        field:
          type: string
          description: Name of the output field this basis supports
        citations:
          type: array
          items:
            $ref: "#/components/schemas/Citation"
          default: []
          description: Sources supporting this field's value
        reasoning:
          type: string
          description: Explanation of how the value was determined
        confidence:
          type: string
          nullable: true
          description: |
            Confidence level (low, medium, high).

            Only certain processors provide confidence levels.
          example: high

    Citation:
      type: object
      required:
        - url
      properties:
        title:
          type: string
          nullable: true
          description: Title of the cited source
        url:
          type: string
          format: uri
          description: URL of the cited source
        excerpts:
          type: array
          items:
            type: string
          nullable: true
          description: |
            Relevant excerpts from the source.

            Only certain processors provide excerpts.

    # Event schemas for SSE
    FindAllSchemaUpdatedEvent:
      type: object
      required:
        - type
        - timestamp
        - event_id
        - data
      properties:
        type:
          type: string
          const: findall.schema.updated
        timestamp:
          type: string
          format: date-time
          description: When the event occurred
        event_id:
          type: string
          description: Unique event identifier for resumption
        data:
          $ref: "#/components/schemas/FindAllSchema"
          description: Updated schema

    FindAllRunStatusEvent:
      type: object
      required:
        - type
        - timestamp
        - event_id
        - data
      properties:
        type:
          type: string
          const: findall.status
        timestamp:
          type: string
          format: date-time
        event_id:
          type: string
        data:
          $ref: "#/components/schemas/FindAllRun"
          description: Updated run status

    FindAllCandidateEvent:
      type: object
      required:
        - type
        - timestamp
        - event_id
        - data
      properties:
        type:
          type: string
          enum:
            [
              findall.candidate.generated,
              findall.candidate.matched,
              findall.candidate.unmatched,
              findall.candidate.discarded,
              findall.candidate.enriched,
            ]
          description: |
            Type of candidate event:
            - generated: New candidate discovered
            - matched: Candidate matched all conditions
            - unmatched: Candidate failed one or more conditions
            - discarded: Candidate removed from evaluation
            - enriched: Enrichment data added
        timestamp:
          type: string
          format: date-time
        event_id:
          type: string
        data:
          $ref: "#/components/schemas/FindAllCandidate"
          description: Candidate with updated status

    ErrorEvent:
      type: object
      required:
        - type
        - error
      properties:
        type:
          type: string
          const: error
        error:
          $ref: "#/components/schemas/Error"

    # Error schemas
    Error:
      type: object
      required:
        - ref_id
        - message
      properties:
        ref_id:
          type: string
          description: Reference ID for error tracking
        message:
          type: string
          description: Human-readable error message
        detail:
          type: object
          additionalProperties: true
          nullable: true
          description: Optional additional error details

    ErrorResponse:
      type: object
      required:
        - type
        - error
      properties:
        type:
          type: string
          const: error
        error:
          $ref: "#/components/schemas/Error"

    HTTPValidationError:
      type: object
      properties:
        detail:
          type: array
          items:
            $ref: "#/components/schemas/ValidationError"

    ValidationError:
      type: object
      required:
        - loc
        - msg
        - type
      properties:
        loc:
          type: array
          items:
            oneOf:
              - type: string
              - type: integer
          description: Location of the validation error
        msg:
          type: string
          description: Error message
        type:
          type: string
          description: Error type

  responses:
    NotFound:
      description: FindAll run not found
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

    ValidationError:
      description: Validation error in request
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/HTTPValidationError"

    UnprocessableEntity:
      description: Unprocessable content - request validation error
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

    PaymentRequired:
      description: Payment required - insufficient credit in account
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

    TooManyRequests:
      description: Too many requests - quota temporarily exceeded
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
````
