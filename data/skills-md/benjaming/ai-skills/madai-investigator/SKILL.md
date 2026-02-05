---
name: madai-investigator
description: Investigate MadAI/MadKudu support tickets from Jira or Zendesk. This skill should be used when analyzing ticket context, checking tenant health, querying knowledge bases, and producing structured investigation reports. Triggers on requests like "investigate this ticket", "look into Zendesk/Jira issue", "check tenant health", or "why is tenant X having issues".
---

# MadAI Support Ticket Investigator

Investigate MadKudu support tickets systematically using available MCP tools.

## Investigation Workflow

Follow these steps in order for thorough investigation:

### Step 1: Fetch Ticket Details

Extract ticket information based on source:

**Zendesk tickets:**
```
mcp__MadAI_Prod__get_zendesk_ticket(ticket_url)
```

**Jira tickets:**
```
mcp__MadAI_Prod__get_jira_ticket(issue_key)  # e.g., "SUPPORT-123"
```

Identify from ticket:
- Tenant ID (look for tenant mentions, domain, or company name)
- Issue description and symptoms
- Timeline (when did the issue start?)
- Any error messages or screenshots

### Step 2: Identify Tenant

If tenant ID not explicit in ticket, search by domain:
```
mcp__MadAI_Prod__get_argo_data(endpoint="tenant", params={"domain": "example.com"})
```

Or search by user email:
```
mcp__MadAI_Prod__get_argo_data(endpoint="users/search", params={"email": "user@example.com"})
```

Get full tenant details:
```
mcp__MadAI_Prod__get_argo_data(endpoint="tenant/{tenant_id}")
```

### Step 3: Health Checks

Run health checks in parallel when possible:

**Tenant active status:**
```
mcp__MadAI_Prod__check_tenant_active(tenant_id)
```

**Connector connectivity:**
```
mcp__MadAI_Prod__check_connector_connectivity(tenant_id)
```

**Fill rate (scoring health):**
```
mcp__MadAI_Prod__get_fill_rate_data(tenant_id, look_back_hours=24)
```

**Process status:**
```
mcp__MadAI_Prod__get_pull_processes_status(tenant_id, look_back_hours=24)
mcp__MadAI_Prod__get_push_processes_status(tenant_id, look_back_hours=24)
mcp__MadAI_Prod__get_data_workers_status(tenant_id, look_back_hours=24)
```

### Step 4: Dig Deeper (as needed)

**Check connector details:**
```
mcp__MadAI_Prod__get_argo_data(endpoint="tenant/{tenant_id}/connectors/{connector_name}")
# connector_name: salesforce, hubspot, marketo, etc.
```

**Query Datadog logs for errors:**
```
mcp__MadAI_Prod__query_datadog_logs(query="@tenant:{tenant_id} status:error", look_back_hours=72)
```

**Query tenant databases:**
```
# Redshift (analytics data)
mcp__MadAI_Prod__execute_redshift_query(tenant_id, query="SELECT ...")

# Postgres - emback (main app data)
mcp__MadAI_Prod__execute_postgres_query(tenant_id, query="SELECT ...", database="emback")

# Postgres - honk (playbooks data)
mcp__MadAI_Prod__execute_postgres_query(tenant_id, query="SELECT ...", database="honk")
```

**Check tenant config in GitHub:**
```
mcp__MadAI_Prod__get_github_tenant_config_file_content(file_path="path/to/config")
```

### Step 5: Query Knowledge Bases

Search for similar issues or solutions:

**Product questions:**
```
mcp__MadAI_Prod__answer_product_question(question="How does X feature work?")
```

**Engineering how-to:**
```
mcp__MadAI_Prod__answer_engineering_question(question="How to debug Y issue?")
```

### Step 6: Produce Investigation Report

Structure findings as:

```markdown
## Investigation Summary

**Ticket:** [ticket ID/URL]
**Tenant:** [tenant_id] - [company name]
**Issue:** [brief description]

## Findings

### Health Status
- Tenant Active: ✅/❌
- Connectors: [status]
- Fill Rate: [percentage]
- Processes: [status]

### Root Cause Analysis
[What's causing the issue based on evidence]

### Evidence
- [Log entries, error messages, data points]

## Recommendations

1. [Action item]
2. [Action item]

## Next Steps
[What should happen next - escalate, fix, follow up]
```

## Common Investigation Patterns

### Scoring Issues
1. Check fill rate data
2. Verify connector connectivity
3. Query pull/push process status
4. Check Datadog for scoring errors

### Connector Problems
1. Check connector connectivity
2. Get specific connector details from Argo
3. Query Datadog for connector-specific errors
4. Verify credentials/config in tenant settings

### Data Sync Issues
1. Check data workers status
2. Query pull processes
3. Check Redshift for data freshness
4. Look for sync errors in Datadog

### Missing Scores/Signals
1. Verify tenant is active
2. Check if model is deployed (tenant config)
3. Query Postgres for signal configuration
4. Check fill rate trends over time
