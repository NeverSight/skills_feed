---
name: findall-api
description: Findall API integration of Parallel. Use when building applications with Parallel FindAll API.
---

<!-- https://contextarea.com/rules-httpsrawg-kg7bzo8k5ybkv4 -->

# FindAll API - Complete Reference

The FindAll API discovers and evaluates entities that match complex criteria from natural language objectives. Submit a high-level goal and the service automatically generates structured match conditions, discovers relevant candidates, and evaluates each against the criteria. Returns comprehensive results with detailed reasoning, citations, and confidence scores for each match decision.

## Table of Contents

- [Quickstart](#quickstart)
- [Core Concepts](#core-concepts)
  - [Candidates](#candidates)
  - [Lifecycle](#lifecycle)
  - [Generators & Pricing](#generators--pricing)
- [API Operations](#api-operations)
  - [Create & Ingest](#create--ingest)
  - [Retrieve & Monitor](#retrieve--monitor)
  - [Modify & Control](#modify--control)
- [Advanced Features](#advanced-features)
  - [Streaming Events](#streaming-events)
  - [Enrichments](#enrichments)
  - [Webhooks](#webhooks)
  - [Preview & Refresh](#preview--refresh)
- [Migration Guide](#migration-guide)

---

## Quickstart

### Basic FindAll Run

```python
from parallel import Parallel

client = Parallel(api_key="your_api_key")

# Create a FindAll run
run = client.findall.runs.create(
    objective="Find all AI companies that raised Series A funding in 2024",
    entity_type="companies",
    match_conditions=[
        {
            "name": "developing_ai_products_check",
            "description": "Company must be developing artificial intelligence (AI) products"
        },
        {
            "name": "raised_series_a_2024_check",
            "description": "Company must have raised Series A funding in 2024"
        }
    ],
    generator="core",
    match_limit=50
)

# Poll for results
while run.status.is_active:
    run = client.findall.runs.retrieve(run.findall_id)
    time.sleep(5)

# Get final results
result = client.findall.runs.result(run.findall_id)
for candidate in result.candidates:
    if candidate.match_status == "matched":
        print(f"Match: {candidate.name} - {candidate.url}")
```

### Using Ingest for Auto-Generation

```python
# Let the API generate match conditions from your objective
schema = client.findall.ingest.create(
    objective="Find all AI companies that raised Series A funding in 2024"
)

# Review and customize the generated schema
print(f"Entity type: {schema.entity_type}")
print(f"Match conditions: {schema.match_conditions}")

# Create run with the generated schema
run = client.findall.runs.create(
    objective=schema.objective,
    entity_type=schema.entity_type,
    match_conditions=schema.match_conditions,
    generator="core",
    match_limit=50
)
```

---

## Core Concepts

### Candidates

A **candidate** represents a potential match for your FindAll objective. Candidates progress through different states during evaluation:

#### Match Statuses

- **`generated`**: Candidate has been discovered but not yet evaluated
- **`matched`**: Candidate satisfies all match conditions
- **`unmatched`**: Candidate fails to satisfy one or more match conditions
- **`discarded`**: Candidate was determined to be irrelevant or duplicate

#### Candidate Structure

```json
{
  "candidate_id": "candidate_7594eb7c-4f4a-487f-9d0c-9d1e63ec240c",
  "name": "Cognition AI",
  "url": "cognition.ai",
  "description": "AI software engineering company",
  "match_status": "matched",
  "output": {
    "developing_ai_products_check": "yes",
    "raised_series_a_2024_check": "yes"
  },
  "basis": [
    {
      "field": "developing_ai_products_check",
      "citations": [
        {
          "title": "Cognition - Devin and Cognition AI",
          "url": "https://cognition.ai/",
          "excerpts": ["We're the makers of Devin..."]
        }
      ],
      "reasoning": "The search results repeatedly state that Cognition AI is an 'applied AI lab building the future of software engineering'...",
      "confidence": "high"
    }
  ]
}
```

#### Output Field

The `output` object contains the evaluation results for each match condition. Each field in `output` corresponds to a match condition name and contains the evaluation result (typically "yes" or "no").

#### Basis Field

The `basis` array provides evidence supporting each output field:

- **`field`**: Name of the output field being supported
- **`citations`**: Web sources with URLs, titles, and excerpts
- **`reasoning`**: Explanation of how the evidence supports the conclusion
- **`confidence`**: Confidence level (low/medium/high) when available

### Lifecycle

FindAll runs progress through several states:

```
queued → running → completed
              ↓
         action_required (if needed)
              ↓
         cancelling → cancelled
              ↓
           failed
```

#### Status Descriptions

- **`queued`**: Run is waiting to start
- **`action_required`**: Run needs user input (rare)
- **`running`**: Actively discovering and evaluating candidates
- **`completed`**: Run finished successfully
- **`failed`**: Run encountered an error
- **`cancelling`**: Cancellation in progress
- **`cancelled`**: Run was cancelled by user

#### Run Object

```json
{
  "findall_id": "findall_56ccc4d188fb41a0803a935cf485c774",
  "status": {
    "status": "running",
    "is_active": true,
    "metrics": {
      "generated_candidates_count": 10,
      "matched_candidates_count": 3
    }
  },
  "generator": "core",
  "metadata": {},
  "created_at": "2025-09-10T21:02:08.626446Z",
  "modified_at": "2025-09-10T21:02:08.627376Z"
}
```

#### Termination Reasons

When a run reaches a terminal state, `termination_reason` explains why:

- **`match_limit_met`**: Found the requested number of matches
- **`candidates_exhausted`**: No more candidates to evaluate
- **`low_match_rate`**: Too few matches found relative to candidates evaluated
- **`user_cancelled`**: User cancelled the run
- **`error_occurred`**: System error
- **`timeout`**: Run exceeded time limit

### Generators & Pricing

Generators control the quality, speed, and cost of FindAll runs:

| Generator   | Quality      | Speed    | Price per Match |
| ----------- | ------------ | -------- | --------------- |
| **base**    | Good         | Fast     | $0.30           |
| **core**    | Better       | Moderate | $1.50           |
| **pro**     | Best         | Slower   | $3.00           |
| **preview** | Experimental | Varies   | $1.50           |

#### Selecting a Generator

```python
# Fast and economical
run = client.findall.runs.create(
    objective="...",
    generator="base",
    match_limit=100
)

# Balanced quality and cost (recommended)
run = client.findall.runs.create(
    objective="...",
    generator="core",
    match_limit=50
)

# Maximum quality
run = client.findall.runs.create(
    objective="...",
    generator="pro",
    match_limit=20
)
```

#### Cost Calculation

Cost is calculated per **matched** candidate only. Unmatched, discarded, or generated candidates don't incur charges.

Example:

- Generator: core ($1.50 per match)
- Matched candidates: 15
- Total cost: 15 × $1.50 = $22.50

---

## API Operations

### Create & Ingest

#### Ingest FindAll Run

Transforms a natural language objective into a structured FindAll specification.

**Note**: Requires `parallel-beta` header.

**Endpoint**: `POST /v1beta/findall/ingest`

**Request**:

```json
{
  "objective": "Find all AI companies that raised Series A funding in 2024"
}
```

**Response**:

```json
{
  "objective": "Find all AI companies that raised Series A funding in 2024",
  "entity_type": "companies",
  "match_conditions": [
    {
      "name": "developing_ai_products_check",
      "description": "Company must be developing artificial intelligence (AI) products"
    },
    {
      "name": "raised_series_a_2024_check",
      "description": "Company must have raised Series A funding in 2024"
    }
  ],
  "generator": "core"
}
```

**Python SDK**:

```python
schema = client.findall.ingest.create(
    objective="Find all AI companies that raised Series A funding in 2024"
)
```

**Error Responses**:

- **422**: Validation error

---

#### Create FindAll Run

Starts a FindAll run that discovers and evaluates entities.

**Endpoint**: `POST /v1beta/findall/runs`

**Request**:

```json
{
  "objective": "Find all AI companies that raised Series A funding in 2024",
  "entity_type": "companies",
  "match_conditions": [
    {
      "name": "developing_ai_products_check",
      "description": "Company must be developing artificial intelligence (AI) products"
    },
    {
      "name": "raised_series_a_2024_check",
      "description": "Company must have raised Series A funding in 2024"
    }
  ],
  "generator": "core",
  "match_limit": 50,
  "exclude_list": [
    {
      "name": "OpenAI",
      "url": "openai.com"
    }
  ],
  "metadata": {
    "project": "Q1 research"
  },
  "webhook": {
    "url": "https://example.com/webhook",
    "event_types": ["task_run.status"]
  }
}
```

**Response**:

```json
{
  "findall_id": "findall_56ccc4d188fb41a0803a935cf485c774",
  "status": {
    "status": "queued",
    "is_active": true,
    "metrics": {
      "generated_candidates_count": 0,
      "matched_candidates_count": 0
    }
  },
  "generator": "core",
  "metadata": {
    "project": "Q1 research"
  },
  "created_at": "2025-09-10T21:02:08.626446Z",
  "modified_at": "2025-09-10T21:02:08.627376Z"
}
```

**Python SDK**:

```python
run = client.findall.runs.create(
    objective="Find all AI companies that raised Series A funding in 2024",
    entity_type="companies",
    match_conditions=[
        {
            "name": "developing_ai_products_check",
            "description": "Company must be developing artificial intelligence (AI) products"
        }
    ],
    generator="core",
    match_limit=50,
    exclude_list=[
        {"name": "OpenAI", "url": "openai.com"}
    ],
    metadata={"project": "Q1 research"}
)
```

**Parameters**:

| Parameter          | Type    | Required | Description                                       |
| ------------------ | ------- | -------- | ------------------------------------------------- |
| `objective`        | string  | Yes      | Natural language description of what to find      |
| `entity_type`      | string  | Yes      | Type of entity (e.g., "companies", "people")      |
| `match_conditions` | array   | Yes      | List of conditions entities must satisfy          |
| `generator`        | string  | Yes      | One of: base, core, pro, preview                  |
| `match_limit`      | integer | Yes      | Max matches to find (5-1000)                      |
| `exclude_list`     | array   | No       | Entities to exclude from results                  |
| `metadata`         | object  | No       | Custom metadata (string, int, float, bool values) |
| `webhook`          | object  | No       | Webhook configuration for notifications           |

**Error Responses**:

- **402**: Insufficient credit
- **422**: Validation error (invalid parameters)
- **429**: Rate limit exceeded

---

### Retrieve & Monitor

#### Retrieve FindAll Run Status

Get the current status of a FindAll run.

**Endpoint**: `GET /v1beta/findall/runs/{findall_id}`

**Python SDK**:

```python
run = client.findall.runs.retrieve("findall_56ccc4d188fb41a0803a935cf485c774")
print(f"Status: {run.status.status}")
print(f"Matches: {run.status.metrics.matched_candidates_count}")
```

---

#### Get FindAll Run Result

Retrieve the complete result snapshot including all evaluated candidates.

**Endpoint**: `GET /v1beta/findall/runs/{findall_id}/result`

**Response**:

```json
{
  "run": {
    "findall_id": "findall_56ccc4d188fb41a0803a935cf485c774",
    "status": {
      "status": "running",
      "is_active": true,
      "metrics": {
        "generated_candidates_count": 1,
        "matched_candidates_count": 1
      }
    },
    "generator": "core",
    "metadata": {},
    "created_at": "2025-09-10T21:02:08.626446Z",
    "modified_at": "2025-09-10T21:02:08.627376Z"
  },
  "candidates": [
    {
      "candidate_id": "candidate_7594eb7c-4f4a-487f-9d0c-9d1e63ec240c",
      "name": "Cognition AI",
      "url": "cognition.ai",
      "match_status": "matched",
      "output": {
        "developing_ai_products_check": "yes",
        "raised_series_a_2024_check": "yes"
      },
      "basis": [...]
    }
  ],
  "last_event_id": "56cee734dbc84172bfc491327f2a0183"
}
```

**Python SDK**:

```python
result = client.findall.runs.result("findall_56ccc4d188fb41a0803a935cf485c774")

# Access run metadata
print(f"Status: {result.run.status.status}")

# Iterate through candidates
for candidate in result.candidates:
    if candidate.match_status == "matched":
        print(f"{candidate.name}: {candidate.url}")

# Resume streaming from last event
last_event = result.last_event_id
```

---

#### Get FindAll Run Schema

Retrieve the schema (objective, entity type, match conditions) for a run.

**Endpoint**: `GET /v1beta/findall/runs/{findall_id}/schema`

**Response**:

```json
{
  "objective": "Find all AI companies that raised Series A funding in 2024",
  "entity_type": "companies",
  "match_conditions": [
    {
      "name": "developing_ai_products_check",
      "description": "Company must be developing artificial intelligence (AI) products"
    }
  ],
  "enrichments": [
    {
      "processor": "core",
      "output_schema": {
        "json_schema": {
          "type": "object",
          "properties": {
            "ceo_name": {
              "type": "string",
              "description": "Name of the current CEO"
            }
          }
        },
        "type": "json"
      }
    }
  ],
  "generator": "core",
  "match_limit": 50
}
```

**Python SDK**:

```python
schema = client.findall.runs.schema("findall_56ccc4d188fb41a0803a935cf485c774")
```

---

### Modify & Control

#### Extend FindAll Run

Add more matches to an existing run by increasing the match limit.

**Endpoint**: `POST /v1beta/findall/runs/{findall_id}/extend`

**Request**:

```json
{
  "additional_match_limit": 25
}
```

**Response**: Returns updated FindAll schema with new match limit.

**Python SDK**:

```python
# Original run had match_limit=50
# This increases it to 75
schema = client.findall.runs.extend(
    findall_id="findall_56ccc4d188fb41a0803a935cf485c774",
    additional_match_limit=25
)
```

**Use Cases**:

- Initial results were promising, want more matches
- Market research needs expanded
- Competitive analysis requires deeper coverage

**Error Responses**:

- **404**: FindAll run not found
- **422**: Additional match limit must be greater than 0

---

#### Add Enrichment to FindAll Run

Add structured data extraction to matched candidates.

**Endpoint**: `POST /v1beta/findall/runs/{findall_id}/enrich`

**Request**:

```json
{
  "processor": "core",
  "output_schema": {
    "json_schema": {
      "type": "object",
      "properties": {
        "ceo_name": {
          "type": "string",
          "description": "Name of the current CEO of the company"
        },
        "funding_amount": {
          "type": "string",
          "description": "Total funding amount in USD"
        }
      },
      "required": ["ceo_name"]
    },
    "type": "json"
  },
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://api.example.com/mcp",
      "name": "company_data",
      "headers": {
        "Authorization": "Bearer token"
      },
      "allowed_tools": ["get_company_info"]
    }
  ]
}
```

**Response**: Returns updated FindAll schema with enrichments.

**Python SDK**:

```python
schema = client.findall.runs.enrich(
    findall_id="findall_56ccc4d188fb41a0803a935cf485c774",
    processor="core",
    output_schema={
        "json_schema": {
            "type": "object",
            "properties": {
                "ceo_name": {"type": "string"},
                "employee_count": {"type": "integer"}
            }
        },
        "type": "json"
    }
)
```

**Enriched Candidate Structure**:

```json
{
  "candidate_id": "candidate_123",
  "name": "Cognition AI",
  "match_status": "matched",
  "output": {
    "developing_ai_products_check": "yes",
    "raised_series_a_2024_check": "yes",
    "ceo_name": "Scott Wu",
    "employee_count": 50
  },
  "basis": [
    {
      "field": "ceo_name",
      "citations": [...],
      "reasoning": "...",
      "confidence": "high"
    }
  ]
}
```

**Error Responses**:

- **404**: FindAll run not found
- **422**: Validation error (invalid schema)

---

#### Cancel FindAll Run

Stop an active FindAll run.

**Endpoint**: `POST /v1beta/findall/runs/{findall_id}/cancel`

**Python SDK**:

```python
client.findall.runs.cancel("findall_56ccc4d188fb41a0803a935cf485c774")
```

**Notes**:

- Run status transitions to `cancelling`, then `cancelled`
- Partial results remain accessible
- Cannot cancel runs in terminal states (completed, failed, cancelled)

**Error Responses**:

- **404**: FindAll run not found
- **409**: Cannot cancel a terminated run

---

## Advanced Features

### Streaming Events

Monitor FindAll runs in real-time using Server-Sent Events (SSE).

**Endpoint**: `GET /v1beta/findall/runs/{findall_id}/events`

**Query Parameters**:

- `last_event_id` (optional): Resume from specific event
- `timeout` (optional): Connection timeout in seconds

**Event Types**:

1. **`findall.schema.updated`**: Schema was modified
2. **`findall.status`**: Run status changed
3. **`findall.candidate.generated`**: New candidate discovered
4. **`findall.candidate.matched`**: Candidate matched all conditions
5. **`findall.candidate.unmatched`**: Candidate failed conditions
6. **`findall.candidate.discarded`**: Candidate was discarded
7. **`findall.candidate.enriched`**: Candidate enrichment completed
8. **`error`**: Error occurred

**Python SDK**:

```python
# Stream all events
for event in client.findall.runs.events("findall_56ccc4d188fb41a0803a935cf485c774"):
    if event.type == "findall.candidate.matched":
        candidate = event.data
        print(f"New match: {candidate.name}")
    elif event.type == "findall.status":
        run = event.data
        print(f"Status: {run.status.status}")

# Resume from last event
for event in client.findall.runs.events(
    findall_id="findall_123",
    last_event_id="56cee734dbc84172bfc491327f2a0183"
):
    process_event(event)

# With timeout
for event in client.findall.runs.events(
    findall_id="findall_123",
    timeout=60  # Close after 60 seconds
):
    process_event(event)
```

**Example Event**:

```json
{
  "type": "findall.candidate.matched",
  "timestamp": "2025-09-10T21:02:08.626446Z",
  "event_id": "56cee734dbc84172bfc491327f2a0183",
  "data": {
    "candidate_id": "candidate_52e1e30b-4e0a-49d8-82eb-79e64e0ed015",
    "name": "Pika",
    "url": "pika.art",
    "match_status": "matched",
    "output": {...},
    "basis": [...]
  }
}
```

**Real-time Dashboard Example**:

```python
def create_live_dashboard(findall_id):
    matched = []

    for event in client.findall.runs.events(findall_id):
        if event.type == "findall.candidate.matched":
            matched.append(event.data.name)
            print(f"\rMatches: {len(matched)}", end="")

        elif event.type == "findall.status":
            if not event.data.status.is_active:
                print(f"\n\nFinal count: {len(matched)}")
                break
```

---

### Enrichments

Add structured data fields to matched candidates after initial matching.

**When to Use Enrichments**:

- Extract additional details from matched entities
- Gather data not needed for matching criteria
- Add custom fields using MCP servers

**Example Flow**:

```python
# 1. Create run without enrichments
run = client.findall.runs.create(
    objective="Find AI companies",
    entity_type="companies",
    match_conditions=[...],
    generator="core",
    match_limit=50
)

# 2. Wait for some matches
while run.status.metrics.matched_candidates_count < 10:
    time.sleep(5)
    run = client.findall.runs.retrieve(run.findall_id)

# 3. Add enrichment for matched candidates
schema = client.findall.runs.enrich(
    findall_id=run.findall_id,
    processor="core",
    output_schema={
        "json_schema": {
            "type": "object",
            "properties": {
                "ceo_name": {"type": "string"},
                "headquarters": {"type": "string"},
                "employee_count": {"type": "integer"}
            }
        },
        "type": "json"
    }
)

# 4. Get enriched results
result = client.findall.runs.result(run.findall_id)
for candidate in result.candidates:
    if candidate.match_status == "matched":
        print(f"{candidate.name}: CEO = {candidate.output.get('ceo_name')}")
```

**Using MCP Servers**:

```python
schema = client.findall.runs.enrich(
    findall_id=run.findall_id,
    processor="core",
    output_schema={
        "json_schema": {
            "type": "object",
            "properties": {
                "stock_price": {"type": "number"},
                "market_cap": {"type": "string"}
            }
        },
        "type": "json"
    },
    mcp_servers=[
        {
            "type": "url",
            "url": "https://api.stockdata.com/mcp",
            "name": "stock_data",
            "headers": {"API-Key": "secret"},
            "allowed_tools": ["get_stock_price", "get_market_cap"]
        }
    ]
)
```

---

### Webhooks

Receive HTTP notifications when FindAll events occur.

**Configuration**:

```python
run = client.findall.runs.create(
    objective="...",
    match_conditions=[...],
    generator="core",
    match_limit=50,
    webhook={
        "url": "https://your-app.com/webhook",
        "event_types": ["task_run.status"]
    }
)
```

**Webhook Payload**:

```json
{
  "type": "findall.candidate.matched",
  "timestamp": "2025-09-10T21:02:08.626446Z",
  "event_id": "56cee734dbc84172bfc491327f2a0183",
  "findall_id": "findall_56ccc4d188fb41a0803a935cf485c774",
  "data": {
    "candidate_id": "candidate_123",
    "name": "Company Name",
    "url": "company.com",
    "match_status": "matched"
  }
}
```

**Webhook Handler Example**:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    event = request.json

    if event['type'] == 'findall.candidate.matched':
        candidate = event['data']
        # Store in database
        db.save_match(candidate)

    elif event['type'] == 'findall.status':
        run = event['data']
        if run['status']['status'] == 'completed':
            # Send notification
            notify_team(f"FindAll {event['findall_id']} completed")

    return '', 200
```

---

### Preview & Refresh

#### Preview Mode

Test your FindAll configuration before committing to a full run.

**Use Cases**:

- Validate match conditions
- Test different generators
- Estimate costs
- Debug criteria

**How It Works**:

1. Use `generator="preview"`
2. Run evaluates a small sample of candidates
3. Review results to refine conditions
4. Create full run with optimized config

**Example**:

```python
# Preview run
preview = client.findall.runs.create(
    objective="Find AI companies with SOC2 certification",
    entity_type="companies",
    match_conditions=[
        {
            "name": "soc2_certified",
            "description": "Company has SOC2 Type II certification"
        }
    ],
    generator="preview",
    match_limit=10  # Small sample
)

# Review results
result = client.findall.runs.result(preview.findall_id)
match_rate = result.run.status.metrics.matched_candidates_count / max(1, result.run.status.metrics.generated_candidates_count)

print(f"Match rate: {match_rate:.1%}")

# Adjust conditions if needed
if match_rate < 0.1:
    print("Match conditions may be too strict")
elif match_rate > 0.5:
    print("Match conditions may be too loose")

# Run full search with validated config
full_run = client.findall.runs.create(
    objective=preview.objective,
    entity_type=preview.entity_type,
    match_conditions=preview.match_conditions,
    generator="core",
    match_limit=100
)
```

---

#### Refresh Results

Re-evaluate candidates with updated web data or revised match conditions.

**When to Refresh**:

- Source websites have updated
- Need fresher data
- Want to recheck with stricter/looser criteria

**Example**:

```python
# Original run from 3 months ago
old_run = client.findall.runs.retrieve("findall_old_123")

# Create new run with same config but fresh data
fresh_run = client.findall.runs.create(
    objective=old_run.objective,
    entity_type=old_run.entity_type,
    match_conditions=old_run.match_conditions,
    generator=old_run.generator,
    match_limit=old_run.match_limit
)

# Compare results
old_result = client.findall.runs.result(old_run.findall_id)
new_result = client.findall.runs.result(fresh_run.findall_id)

old_matches = {c.name for c in old_result.candidates if c.match_status == "matched"}
new_matches = {c.name for c in new_result.candidates if c.match_status == "matched"}

print(f"Newly matched: {new_matches - old_matches}")
print(f"No longer match: {old_matches - new_matches}")
```

---

## Migration Guide

### From Tasks API to FindAll API

The FindAll API is purpose-built for discovering multiple entities, replacing the pattern of running many parallel Task API calls.

#### Before: Tasks API Pattern

```python
# Old approach: Multiple task runs for discovery
companies = ["Company A", "Company B", "Company C", ...]

results = []
for company in companies:
    task = client.tasks.create(
        objective=f"Check if {company} has SOC2 certification",
        processor="core"
    )
    results.append(task)

# Wait and aggregate
matches = [r for r in results if r.output.get("has_soc2") == "yes"]
```

**Problems**:

- Manual candidate list required
- High cost (every task charged)
- Slow (sequential or complex parallel code)
- Limited discovery (only checks provided list)

#### After: FindAll API

```python
# New approach: Single FindAll run
run = client.findall.runs.create(
    objective="Find companies with SOC2 Type II certification",
    entity_type="companies",
    match_conditions=[
        {
            "name": "soc2_type_ii_check",
            "description": "Company must have SOC2 Type II certification"
        }
    ],
    generator="core",
    match_limit=50
)

# Automatically discovers and evaluates candidates
result = client.findall.runs.result(run.findall_id)
matches = [c for c in result.candidates if c.match_status == "matched"]
```

**Benefits**:

- Automatic candidate discovery
- Only pay for matches
- Parallel evaluation at scale
- Comprehensive coverage

#### Migration Checklist

1. **Replace manual lists**: Let FindAll discover candidates
2. **Combine match logic**: Use match_conditions instead of separate tasks
3. **Use streaming**: Replace polling with SSE for real-time updates
4. **Add enrichments**: Extract additional data only for matches
5. **Leverage generators**: Choose appropriate quality/cost tradeoff

#### Feature Comparison

| Feature                  | Tasks API             | FindAll API     |
| ------------------------ | --------------------- | --------------- |
| **Discovery**            | Manual list           | Automatic       |
| **Parallelization**      | Custom code           | Built-in        |
| **Pricing**              | Per task              | Per match       |
| **Monitoring**           | Poll individual tasks | Single stream   |
| **Enrichment**           | Separate tasks        | Native support  |
| **Excluding duplicates** | Manual                | Built-in        |
| **Cost control**         | Hard to predict       | match_limit cap |

#### Code Examples

**Task pattern → FindAll equivalent**:

```python
# OLD: Check multiple URLs
for url in urls:
    client.tasks.create(
        objective=f"Extract CEO name from {url}",
        processor="core"
    )

# NEW: Single FindAll with enrichment
run = client.findall.runs.create(
    objective="Find all tech companies",
    match_conditions=[...],
    generator="core",
    match_limit=100
)

client.findall.runs.enrich(
    findall_id=run.findall_id,
    output_schema={
        "json_schema": {
            "properties": {
                "ceo_name": {"type": "string"}
            }
        }
    }
)
```

**Task group → FindAll**:

```python
# OLD: Task group for batch processing
group = client.tasks.groups.create([
    {"objective": "Check company A..."},
    {"objective": "Check company B..."},
    {"objective": "Check company C..."}
])

# NEW: FindAll discovers automatically
run = client.findall.runs.create(
    objective="Find companies matching criteria",
    match_conditions=[...],
    generator="core",
    match_limit=50
)
```

---

## Best Practices

### Writing Match Conditions

**Be Specific**:

```python
# ❌ Too vague
"Company must be successful"

# ✅ Specific and verifiable
"Company must have raised Series A funding of at least $10M in 2024"
```

**Include Evidence Hints**:

```python
{
    "name": "soc2_certified",
    "description": """
    Company must have SOC2 Type II certification (not Type I).
    Look for evidence in:
    - Trust centers
    - Security/compliance pages
    - Audit reports
    - Press releases specifically mentioning 'SOC2 Type II'

    If no explicit SOC2 Type II mention is found, consider requirement not satisfied.
    """
}
```

**Use Negative Examples**:

```python
{
    "name": "series_a_only",
    "description": """
    Company must be at Series A stage (not seed, Series B, C, or later).
    Confirm they have closed Series A and have not announced Series B.
    """
}
```

### Excluding Entities

Use the `exclude_list` parameter to prevent known entities from being evaluated:

```python
run = client.findall.runs.create(
    objective="Find AI companies",
    match_conditions=[...],
    generator="core",
    match_limit=50,
    exclude_list=[
        {"name": "OpenAI", "url": "openai.com"},
        {"name": "Anthropic", "url": "anthropic.com"}
    ]
)
```

### Cost Optimization

1. **Start with preview**: Test with `generator="preview"` first
2. **Use base for scale**: Use `base` generator for large searches (100+ matches)
3. **Set appropriate limits**: Don't request more matches than you need
4. **Leverage extend**: Start small, extend if needed rather than over-requesting
5. **Enrich selectively**: Only add enrichments for final matched entities

### Monitoring Best Practices

**Use SSE for Real-time Needs**:

```python
# Real-time monitoring
for event in client.findall.runs.events(run.findall_id):
    if event.type == "findall.candidate.matched":
        process_immediately(event.data)
```

**Use Polling for Async Workflows**:

```python
# Background job
while True:
    run = client.findall.runs.retrieve(run.findall_id)
    if not run.status.is_active:
        break
    time.sleep(30)
```

**Use Webhooks for Integration**:

```python
# System-to-system integration
run = client.findall.runs.create(
    objective="...",
    webhook={
        "url": "https://your-system.com/findall-webhook",
        "event_types": ["task_run.status"]
    }
)
```

---

## Error Handling

### Common Errors

**402 Payment Required**:

```python
try:
    run = client.findall.runs.create(...)
except Exception as e:
    if "insufficient credit" in str(e).lower():
        print("Add credits to your account")
```

**422 Validation Error**:

```python
try:
    run = client.findall.runs.create(
        match_limit=5000  # Over max of 1000
    )
except Exception as e:
    print(f"Invalid parameters: {e}")
```

**429 Rate Limit**:

```python
import time

def create_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.findall.runs.create(...)
        except Exception as e:
            if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

### Event Stream Error Handling

```python
def robust_stream(findall_id, max_reconnects=5):
    reconnects = 0
    last_event_id = None

    while reconnects < max_reconnects:
        try:
            for event in client.findall.runs.events(
                findall_id=findall_id,
                last_event_id=last_event_id
            ):
                if event.type == "error":
                    print(f"Error event: {event.error.message}")
                    continue

                last_event_id = event.event_id
                yield event

            break  # Stream ended normally

        except Exception as e:
            print(f"Stream interrupted: {e}")
            reconnects += 1
            time.sleep(min(30, 2 ** reconnects))
```

---

## Complete Example: Company Research Pipeline

```python
from parallel import Parallel
import time

client = Parallel(api_key="your_api_key")

# Step 1: Ingest objective
print("Generating FindAll schema...")
schema = client.findall.ingest.create(
    objective="Find YC-backed AI companies founded in 2023 with active products"
)

print(f"Generated {len(schema.match_conditions)} match conditions:")
for condition in schema.match_conditions:
    print(f"  - {condition['name']}")

# Step 2: Start FindAll run
print("\nStarting FindAll run...")
run = client.findall.runs.create(
    objective=schema.objective,
    entity_type=schema.entity_type,
    match_conditions=schema.match_conditions,
    generator="core",
    match_limit=50,
    metadata={"project": "Q1_2025_research"}
)

# Step 3: Monitor with SSE
print(f"\nMonitoring run {run.findall_id}...")
matched_count = 0

for event in client.findall.runs.events(run.findall_id):
    if event.type == "findall.candidate.matched":
        matched_count += 1
        candidate = event.data
        print(f"✓ Match #{matched_count}: {candidate.name}")

    elif event.type == "findall.status":
        run_status = event.data.status
        print(f"Status: {run_status.status} | "
              f"Generated: {run_status.metrics.generated_candidates_count} | "
              f"Matched: {run_status.metrics.matched_candidates_count}")

        if not event.data.status.is_active:
            break

# Step 4: Add enrichments for matched companies
print("\nAdding enrichments...")
client.findall.runs.enrich(
    findall_id=run.findall_id,
    processor="core",
    output_schema={
        "json_schema": {
            "type": "object",
            "properties": {
                "ceo_name": {"type": "string"},
                "employee_count": {"type": "integer"},
                "total_funding": {"type": "string"}
            }
        },
        "type": "json"
    }
)

# Wait for enrichments to complete
while True:
    run = client.findall.runs.retrieve(run.findall_id)
    if not run.status.is_active:
        break
    time.sleep(5)

# Step 5: Get final results
print("\nFinal results:")
result = client.findall.runs.result(run.findall_id)

for candidate in result.candidates:
    if candidate.match_status == "matched":
        output = candidate.output
        print(f"\n{candidate.name} ({candidate.url})")
        print(f"  CEO: {output.get('ceo_name', 'N/A')}")
        print(f"  Employees: {output.get('employee_count', 'N/A')}")
        print(f"  Funding: {output.get('total_funding', 'N/A')}")

print(f"\n✓ Found {matched_count} companies matching criteria")
```

---

## API Reference Summary

| Endpoint                           | Method | Purpose                                |
| ---------------------------------- | ------ | -------------------------------------- |
| `/v1beta/findall/ingest`           | POST   | Generate FindAll schema from objective |
| `/v1beta/findall/runs`             | POST   | Create FindAll run                     |
| `/v1beta/findall/runs/{id}`        | GET    | Get run status                         |
| `/v1beta/findall/runs/{id}/result` | GET    | Get complete results                   |
| `/v1beta/findall/runs/{id}/schema` | GET    | Get run schema                         |
| `/v1beta/findall/runs/{id}/events` | GET    | Stream events (SSE)                    |
| `/v1beta/findall/runs/{id}/extend` | POST   | Increase match limit                   |
| `/v1beta/findall/runs/{id}/enrich` | POST   | Add enrichments                        |
| `/v1beta/findall/runs/{id}/cancel` | POST   | Cancel run                             |

---

## Additional Resources

- **API Reference**: https://docs.parallel.ai/api-reference/findall-api-beta/
- **Python SDK**: https://github.com/parallelinc/parallel-python
- **Support**: support@parallel.ai
- **Status Page**: https://status.parallel.ai

---

_Last Updated: January 2025_
_API Version: 0.1.2_
