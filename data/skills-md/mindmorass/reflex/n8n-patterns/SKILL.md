---
name: n8n-patterns
description: Design and implement n8n workflow automations with best practices
---

# n8n Workflow Patterns

> Build robust workflow automations with n8n - the open-source workflow automation tool.

## Overview

n8n is a self-hostable workflow automation platform that connects apps and services. Key features:
- Visual workflow builder with 400+ integrations
- Self-hosted or cloud deployment
- Code nodes for custom logic (JavaScript/Python)
- Webhook triggers for real-time automation
- Sub-workflows for modular design

## Core Concepts

### Workflow Structure

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Trigger   │───▶│    Node     │───▶│   Output    │
│  (Start)    │    │  (Process)  │    │  (Action)   │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Node Types

| Type | Purpose | Examples |
|------|---------|----------|
| **Trigger** | Start workflow | Webhook, Schedule, App trigger |
| **Action** | Perform operations | HTTP Request, Database, Email |
| **Transform** | Modify data | Set, Code, IF, Switch |
| **Flow** | Control execution | Merge, Split, Wait, Loop |

## Trigger Patterns

### Webhook Trigger

```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "my-webhook",
        "responseMode": "responseNode",
        "options": {
          "rawBody": true
        }
      }
    }
  ]
}
```

**Best Practices:**
- Use `responseNode` for custom responses
- Enable `rawBody` for signature verification
- Add authentication (Header Auth, Basic Auth)

### Schedule Trigger

```json
{
  "name": "Schedule Trigger",
  "type": "n8n-nodes-base.scheduleTrigger",
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "cronExpression",
          "expression": "0 9 * * 1-5"
        }
      ]
    }
  }
}
```

**Common Schedules:**
- `0 * * * *` - Every hour
- `0 9 * * 1-5` - Weekdays at 9 AM
- `0 0 * * 0` - Weekly on Sunday midnight
- `*/15 * * * *` - Every 15 minutes

### App Trigger (Polling)

```json
{
  "name": "GitHub Trigger",
  "type": "n8n-nodes-base.githubTrigger",
  "parameters": {
    "owner": "{{$env.GITHUB_OWNER}}",
    "repository": "{{$env.GITHUB_REPO}}",
    "events": ["issues", "pull_request"]
  }
}
```

## Data Transformation Patterns

### Set Node (Transform Data)

```json
{
  "name": "Transform Data",
  "type": "n8n-nodes-base.set",
  "parameters": {
    "mode": "manual",
    "duplicateItem": false,
    "assignments": {
      "assignments": [
        {
          "name": "fullName",
          "value": "={{ $json.firstName }} {{ $json.lastName }}",
          "type": "string"
        },
        {
          "name": "timestamp",
          "value": "={{ DateTime.now().toISO() }}",
          "type": "string"
        }
      ]
    }
  }
}
```

### Code Node (JavaScript)

```javascript
// Process items with custom logic
const results = [];

for (const item of $input.all()) {
  const data = item.json;

  // Transform data
  results.push({
    json: {
      id: data.id,
      processed: true,
      score: calculateScore(data),
      timestamp: new Date().toISOString()
    }
  });
}

function calculateScore(data) {
  return data.value * 0.8 + data.bonus * 0.2;
}

return results;
```

### Code Node (Python)

```python
# Enable Python in n8n settings
import json
from datetime import datetime

results = []

for item in _input.all():
    data = item.json

    # Transform data
    results.append({
        "json": {
            "id": data.get("id"),
            "processed": True,
            "timestamp": datetime.now().isoformat()
        }
    })

return results
```

## Control Flow Patterns

### IF Node (Conditional)

```json
{
  "name": "Check Status",
  "type": "n8n-nodes-base.if",
  "parameters": {
    "conditions": {
      "options": {
        "caseSensitive": true,
        "leftValue": "",
        "typeValidation": "strict"
      },
      "conditions": [
        {
          "leftValue": "={{ $json.status }}",
          "rightValue": "active",
          "operator": {
            "type": "string",
            "operation": "equals"
          }
        }
      ],
      "combinator": "and"
    }
  }
}
```

### Switch Node (Multi-branch)

```json
{
  "name": "Route by Type",
  "type": "n8n-nodes-base.switch",
  "parameters": {
    "mode": "rules",
    "rules": {
      "values": [
        {
          "outputKey": "order",
          "conditions": {
            "conditions": [
              {
                "leftValue": "={{ $json.type }}",
                "rightValue": "order",
                "operator": { "type": "string", "operation": "equals" }
              }
            ]
          }
        },
        {
          "outputKey": "refund",
          "conditions": {
            "conditions": [
              {
                "leftValue": "={{ $json.type }}",
                "rightValue": "refund",
                "operator": { "type": "string", "operation": "equals" }
              }
            ]
          }
        }
      ]
    },
    "fallbackOutput": "extra"
  }
}
```

### Loop Over Items

```json
{
  "name": "Loop Over Items",
  "type": "n8n-nodes-base.splitInBatches",
  "parameters": {
    "batchSize": 10,
    "options": {
      "reset": false
    }
  }
}
```

### Merge Node (Combine Data)

```json
{
  "name": "Merge Results",
  "type": "n8n-nodes-base.merge",
  "parameters": {
    "mode": "combine",
    "mergeByFields": {
      "values": [
        {
          "field1": "id",
          "field2": "userId"
        }
      ]
    },
    "options": {}
  }
}
```

## Error Handling Patterns

### Try/Catch with Error Trigger

```json
{
  "nodes": [
    {
      "name": "Error Trigger",
      "type": "n8n-nodes-base.errorTrigger",
      "parameters": {}
    },
    {
      "name": "Send Alert",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#alerts",
        "text": "Workflow failed: {{ $json.workflow.name }}\nError: {{ $json.execution.error.message }}"
      }
    }
  ]
}
```

### Retry on Failure

```json
{
  "name": "HTTP Request",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.example.com/data",
    "options": {}
  },
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 1000
}
```

### Stop and Error Node

```json
{
  "name": "Validation Failed",
  "type": "n8n-nodes-base.stopAndError",
  "parameters": {
    "errorMessage": "Invalid input: {{ $json.error }}"
  }
}
```

## Sub-Workflow Pattern

### Execute Workflow Node

```json
{
  "name": "Process Order",
  "type": "n8n-nodes-base.executeWorkflow",
  "parameters": {
    "source": "database",
    "workflowId": "order-processing-workflow-id",
    "mode": "each",
    "options": {
      "waitForSubWorkflow": true
    }
  }
}
```

**Best Practices:**
- Use sub-workflows for reusable logic
- Pass minimal data between workflows
- Set `waitForSubWorkflow` based on needs
- Use workflow tags for organization

## HTTP Request Patterns

### REST API Call

```json
{
  "name": "API Request",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "POST",
    "url": "https://api.example.com/v1/resource",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    },
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "data",
          "value": "={{ JSON.stringify($json) }}"
        }
      ]
    },
    "options": {
      "timeout": 30000,
      "response": {
        "response": {
          "fullResponse": false,
          "responseFormat": "json"
        }
      }
    }
  }
}
```

### Pagination Pattern

```javascript
// Code node for API pagination
const allResults = [];
let page = 1;
let hasMore = true;

while (hasMore) {
  const response = await this.helpers.httpRequest({
    method: 'GET',
    url: `https://api.example.com/items?page=${page}&limit=100`,
    headers: {
      'Authorization': `Bearer ${$env.API_TOKEN}`
    }
  });

  allResults.push(...response.data);
  hasMore = response.hasNextPage;
  page++;

  // Rate limiting
  await new Promise(r => setTimeout(r, 100));
}

return allResults.map(item => ({ json: item }));
```

## Credential Management

### Environment Variables

```javascript
// Access in expressions
{{ $env.API_KEY }}
{{ $env.DATABASE_URL }}

// Access in Code node
const apiKey = $env.API_KEY;
```

### Credential Types

| Type | Use Case |
|------|----------|
| `httpBasicAuth` | Basic authentication |
| `httpHeaderAuth` | API key in header |
| `oAuth2Api` | OAuth 2.0 flows |
| `httpQueryAuth` | API key in query string |

## Self-Hosting Patterns

### Docker Compose

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_HOST=${N8N_HOST}
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - NODE_ENV=production
      - WEBHOOK_URL=https://${N8N_HOST}/
      - GENERIC_TIMEZONE=UTC
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - EXECUTIONS_DATA_PRUNE=true
      - EXECUTIONS_DATA_MAX_AGE=168
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  n8n_data:
  postgres_data:
```

### Environment Variables (.env)

```bash
# n8n Configuration
N8N_HOST=n8n.example.com
N8N_USER=admin
N8N_PASSWORD=secure-password-here
N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)

# Database
POSTGRES_USER=n8n
POSTGRES_PASSWORD=secure-db-password

# Optional: Queue mode for scaling
EXECUTIONS_MODE=queue
QUEUE_BULL_REDIS_HOST=redis
```

### Queue Mode (Scaling)

```yaml
# docker-compose.queue.yml
services:
  n8n:
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_HEALTH_CHECK_ACTIVE=true

  n8n-worker:
    image: n8nio/n8n:latest
    command: worker
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
    deploy:
      replicas: 3

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
```

## Common Workflow Templates

### Webhook to Database

```json
{
  "name": "Webhook to Database",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "POST",
        "path": "ingest",
        "responseMode": "responseNode"
      }
    },
    {
      "name": "Validate",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.id }}",
              "rightValue": "",
              "operator": { "type": "string", "operation": "notEmpty" }
            }
          ]
        }
      }
    },
    {
      "name": "Insert",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "insert",
        "table": "events",
        "columns": "id,type,data,created_at"
      }
    },
    {
      "name": "Success Response",
      "type": "n8n-nodes-base.respondToWebhook",
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ { \"success\": true, \"id\": $json.id } }}"
      }
    }
  ]
}
```

### Scheduled Sync

```json
{
  "name": "Daily Data Sync",
  "nodes": [
    {
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{ "field": "cronExpression", "expression": "0 2 * * *" }]
        }
      }
    },
    {
      "name": "Fetch Source",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.source.com/data",
        "authentication": "predefinedCredentialType"
      }
    },
    {
      "name": "Transform",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "return $input.all().map(item => ({ json: { ...item.json, synced_at: new Date().toISOString() } }));"
      }
    },
    {
      "name": "Upsert Destination",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "upsert",
        "table": "synced_data"
      }
    }
  ]
}
```

### Event-Driven Notification

```json
{
  "name": "Alert Pipeline",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": { "path": "alert" }
    },
    {
      "name": "Route by Severity",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "rules": {
          "values": [
            { "outputKey": "critical", "conditions": { "conditions": [{ "leftValue": "={{ $json.severity }}", "rightValue": "critical" }] } },
            { "outputKey": "warning", "conditions": { "conditions": [{ "leftValue": "={{ $json.severity }}", "rightValue": "warning" }] } }
          ]
        }
      }
    },
    {
      "name": "Page On-Call",
      "type": "n8n-nodes-base.pagerDuty"
    },
    {
      "name": "Slack Alert",
      "type": "n8n-nodes-base.slack"
    }
  ]
}
```

## Expression Cheat Sheet

| Expression | Description |
|------------|-------------|
| `{{ $json.field }}` | Access field from current item |
| `{{ $json["field-name"] }}` | Access field with special chars |
| `{{ $('NodeName').item.json.field }}` | Access data from specific node |
| `{{ $input.first().json }}` | First input item |
| `{{ $input.all() }}` | All input items |
| `{{ $env.VAR_NAME }}` | Environment variable |
| `{{ $now }}` | Current datetime |
| `{{ $today }}` | Current date |
| `{{ $runIndex }}` | Current execution run index |
| `{{ $itemIndex }}` | Current item index |
| `{{ $workflow.id }}` | Workflow ID |
| `{{ $execution.id }}` | Execution ID |

## Luxon DateTime Examples

```javascript
// n8n uses Luxon for dates
{{ $now.toISO() }}                    // ISO format
{{ $now.toFormat('yyyy-MM-dd') }}     // Custom format
{{ $now.plus({ days: 7 }).toISO() }}  // Add 7 days
{{ $now.startOf('month').toISO() }}   // Start of month
{{ DateTime.fromISO($json.date) }}    // Parse ISO string
```

## Best Practices

1. **Naming**: Use descriptive node names (verb + noun)
2. **Error Handling**: Always add error workflows
3. **Credentials**: Never hardcode secrets
4. **Batching**: Use `splitInBatches` for large datasets
5. **Timeouts**: Set appropriate timeouts on HTTP nodes
6. **Logging**: Use `console.log` in Code nodes for debugging
7. **Testing**: Use manual execution before activating
8. **Version Control**: Export workflows as JSON to git
9. **Documentation**: Add sticky notes for complex logic
10. **Modular Design**: Use sub-workflows for reusability

## Debugging Tips

```javascript
// In Code node - log to n8n console
console.log('Debug:', JSON.stringify($json, null, 2));

// Return debug info
return [{
  json: {
    debug: true,
    input: $json,
    env: $env.NODE_ENV,
    timestamp: new Date().toISOString()
  }
}];
```

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [Workflow Templates](https://n8n.io/workflows/)
- [Node Reference](https://docs.n8n.io/integrations/)
