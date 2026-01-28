---
name: n8n-workflow
description: Use when creating, deploying, or managing N8N workflows. Automatically uses N8N_HOST and N8N_API_KEY from environment.
---

# N8N Workflow Deployment

Deploy workflows to N8N using the REST API.

## Environment Variables

```bash
N8N_HOST="https://your-n8n-instance.com"  # Or http://localhost:5678
N8N_API_KEY="your-api-key"                 # From N8N Settings > API
```

## Quick Deploy

```python
import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

def deploy_n8n_workflow(workflow: dict, activate: bool = False) -> dict:
    """
    Deploy a workflow to N8N.

    Args:
        workflow: Complete workflow JSON with nodes, connections, settings
        activate: Whether to activate the workflow after creation

    Returns:
        dict with id, name, and URL of created workflow
    """
    host = os.environ.get('N8N_HOST', 'http://localhost:5678')
    api_key = os.environ.get('N8N_API_KEY')

    if not api_key:
        raise ValueError("N8N_API_KEY environment variable not set")

    # Ensure workflow has required fields
    if 'name' not in workflow:
        workflow['name'] = 'Untitled Workflow'
    if 'nodes' not in workflow:
        workflow['nodes'] = []
    if 'connections' not in workflow:
        workflow['connections'] = {}
    if 'settings' not in workflow:
        workflow['settings'] = {}

    # Remove 'active' field if present - it's read-only on creation
    workflow.pop('active', None)

    url = f"{host.rstrip('/')}/api/v1/workflows"

    request = Request(
        url,
        data=json.dumps(workflow).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'X-N8N-API-KEY': api_key
        },
        method='POST'
    )

    with urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))

    workflow_id = result.get('id')
    workflow_url = f"{host}/workflow/{workflow_id}"

    print(f"✅ Workflow deployed to N8N!")
    print(f"   ID: {workflow_id}")
    print(f"   Name: {result.get('name')}")
    print(f"   URL: {workflow_url}")

    # Activate if requested (requires separate PATCH call)
    is_active = False
    if activate:
        is_active = set_workflow_active(workflow_id, True).get('active', False)
        print(f"   Active: {is_active}")
    else:
        print(f"   Active: False (not activated)")

    return {
        'id': workflow_id,
        'name': result.get('name'),
        'active': is_active,
        'url': workflow_url
    }
```

## Activate/Deactivate Workflow

```python
def set_workflow_active(workflow_id: str, active: bool = True) -> dict:
    """Activate or deactivate an existing workflow."""
    host = os.environ.get('N8N_HOST', 'http://localhost:5678')
    api_key = os.environ.get('N8N_API_KEY')

    url = f"{host.rstrip('/')}/api/v1/workflows/{workflow_id}"

    request = Request(
        url,
        data=json.dumps({'active': active}).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'X-N8N-API-KEY': api_key
        },
        method='PATCH'
    )

    with urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))

    status = "activated" if active else "deactivated"
    print(f"✅ Workflow {workflow_id} {status}")
    return result
```

## List Workflows

```python
def list_n8n_workflows(active_only: bool = False) -> list:
    """List all workflows in N8N instance."""
    host = os.environ.get('N8N_HOST', 'http://localhost:5678')
    api_key = os.environ.get('N8N_API_KEY')

    url = f"{host.rstrip('/')}/api/v1/workflows"
    if active_only:
        url += "?active=true"

    request = Request(
        url,
        headers={
            'Content-Type': 'application/json',
            'X-N8N-API-KEY': api_key
        }
    )

    with urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))

    workflows = result.get('data', [])
    print(f"Found {len(workflows)} workflows")
    for wf in workflows:
        status = "🟢" if wf.get('active') else "⚪"
        print(f"  {status} [{wf['id']}] {wf['name']}")

    return workflows
```

## Example: Anomaly Detection Workflow

```python
# Build an anomaly detection workflow
anomaly_workflow = {
    "name": "Daily Anomaly Detection",
    "nodes": [
        {
            "id": "schedule",
            "name": "Daily 9am",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1,
            "position": [250, 300],
            "parameters": {
                "rule": {
                    "interval": [{"field": "hours", "hoursInterval": 24}]
                }
            }
        },
        {
            "id": "bigquery",
            "name": "Query Metrics",
            "type": "n8n-nodes-base.googleBigQuery",
            "typeVersion": 2,
            "position": [450, 300],
            "parameters": {
                "operation": "executeQuery",
                "projectId": "={{ $env.BIGQUERY_PROJECT_ID }}",
                "sqlQuery": "SELECT date, registration_starts, paid_conversions FROM metrics WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)"
            }
        },
        {
            "id": "code",
            "name": "Detect Anomalies",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [650, 300],
            "parameters": {
                "jsCode": '''
const data = $input.all();
const values = data.map(d => d.json.registration_starts);
const mean = values.reduce((a,b) => a+b, 0) / values.length;
const std = Math.sqrt(values.map(x => Math.pow(x - mean, 2)).reduce((a,b) => a+b, 0) / values.length);

const anomalies = data.filter(d => {
  const zscore = Math.abs((d.json.registration_starts - mean) / std);
  return zscore > 2;
});

return anomalies.length > 0 ? anomalies : [];
'''
            }
        },
        {
            "id": "if",
            "name": "Has Anomaly?",
            "type": "n8n-nodes-base.if",
            "typeVersion": 1,
            "position": [850, 300],
            "parameters": {
                "conditions": {
                    "number": [{
                        "value1": "={{ $json.length }}",
                        "operation": "larger",
                        "value2": 0
                    }]
                }
            }
        },
        {
            "id": "slack",
            "name": "Send Alert",
            "type": "n8n-nodes-base.slack",
            "typeVersion": 2,
            "position": [1050, 250],
            "parameters": {
                "channel": "#alerts",
                "text": "🔴 Anomaly detected in registration_starts"
            }
        }
    ],
    "connections": {
        "Daily 9am": {"main": [[{"node": "Query Metrics", "type": "main", "index": 0}]]},
        "Query Metrics": {"main": [[{"node": "Detect Anomalies", "type": "main", "index": 0}]]},
        "Detect Anomalies": {"main": [[{"node": "Has Anomaly?", "type": "main", "index": 0}]]},
        "Has Anomaly?": {"main": [[{"node": "Send Alert", "type": "main", "index": 0}], []]}
    },
    "settings": {
        "executionOrder": "v1"
    }
}

# Deploy it
result = deploy_n8n_workflow(anomaly_workflow, activate=False)
print(f"Workflow ready at: {result['url']}")
```

## cURL Examples

### Create Workflow
```bash
curl -X POST "$N8N_HOST/api/v1/workflows" \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -d @workflow.json
```

### List Workflows
```bash
curl -X GET "$N8N_HOST/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

### Activate Workflow
```bash
curl -X PATCH "$N8N_HOST/api/v1/workflows/WORKFLOW_ID" \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -d '{"active": true}'
```

## Error Handling

```python
from urllib.error import HTTPError

try:
    result = deploy_n8n_workflow(workflow)
except HTTPError as e:
    error_body = e.read().decode('utf-8')
    print(f"N8N API error: {e.code}")
    print(f"  {error_body}")
except ValueError as e:
    print(f"Configuration error: {e}")
```

## Getting Your N8N API Key

1. Open your N8N instance
2. Go to **Settings** (gear icon)
3. Click **API** in the left menu
4. Click **Create API Key**
5. Copy the key and set it as `N8N_API_KEY`
