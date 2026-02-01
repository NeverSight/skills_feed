---
name: datadog-operations
description: "Comprehensive Datadog operations: query APM/logs/metrics/RUM/database, create monitors/dashboards/synthetics, manage incidents, trigger workflows, analyze costs and LLM usage. 73% platform coverage including service catalog, uptime monitoring, and frontend performance. Use for debugging, automation, incident response, and cost optimization."
author: ryan-maclean
version: 3.0.0
---

# Datadog Operations

Complete Datadog automation: query APIs, create infrastructure, manage incidents, and automate responses. 73% platform coverage with 17 working scripts.

## What This Skill Does

**Investigation & Analysis:**
- Query APM traces to identify performance bottlenecks
- Search logs for error patterns and anomalies
- Detect security threats and attack attempts
- Analyze Watchdog anomaly detection alerts
- Query metrics with statistical analysis
- Analyze Datadog usage and costs (FinOps)
- Monitor LLM observability for GenAI applications
- Query SLO status and error budgets
- List services from service catalog
- Analyze database query performance
- Track frontend performance with RUM

**Automation & Creation:**
- Create and manage monitors with alert thresholds
- Generate dashboards for APM, security, costs, and LLM observability
- Trigger Datadog workflows for incident response
- Create and update incidents
- Mute/unmute monitors during maintenance
- Create synthetic uptime checks and browser tests

## Prerequisites

Set environment variables:

```bash
export DD_API_KEY=your_api_key
export DD_APP_KEY=your_application_key
export DD_SITE=datadoghq.com  # or datadoghq.eu, us3.datadoghq.com, etc.
```

Get keys from Datadog: Organization Settings > API Keys and Application Keys

## Working Scripts

### 1. Query APM Performance

Find slow endpoints and performance issues:

```bash
bash scripts/query-apm.sh --service my-service --duration 1h --limit 20
```

Returns:
- Endpoints sorted by P95 latency
- Request counts per endpoint
- P50, P95, P99 latency
- Problem endpoints (P95 > 500ms)

### 2. Query Security Signals

Find security threats and attack attempts:

```bash
bash scripts/query-security-signals.sh --service my-service --duration 24h
```

Returns:
- Security signals by severity (critical, high, medium, low)
- Attack types (SQL injection, XSS, auth failures)
- Affected services and hosts
- Recent security events with details

### 3. Query Watchdog Anomalies

Automated anomaly detection from Datadog Watchdog:

```bash
bash scripts/query-watchdog.sh --service my-service --type latency --duration 7d
```

Returns:
- Anomalies by type (latency, error_rate, traffic)
- Affected services and resources
- Start timestamps and severity
- Baseline vs observed values

### 4. Search Logs

Search logs for error patterns:

```bash
bash scripts/search-logs.sh --query "status:error service:my-service" --duration 1h
```

Returns:
- Error messages grouped by frequency
- Associated trace IDs for investigation
- Service and host breakdowns
- Common error patterns

### 5. Query Metrics

Fetch metric data with statistical analysis:

```bash
bash scripts/query-metrics.sh --metric "trace.express.request.duration" --service my-service --duration 24h
```

Returns:
- Time series data
- Statistics (min, max, avg, p50, p95, p99)
- Trend analysis (increasing, decreasing, stable)
- Anomaly detection (values > 2 std dev)

### 6. Analyze Usage and Costs

FinOps cost analysis and optimization:

```bash
bash scripts/analyze-usage-cost.sh --duration 30d --product all
```

Returns:
- APM span ingestion (indexed vs ingested)
- Log volume breakdown
- Infrastructure hosts and container hours
- Custom metrics count
- Estimated monthly costs by product
- Cost optimization recommendations

### 7. Analyze LLM Performance

For GenAI applications, analyze LLM observability data:

```bash
bash scripts/analyze-llm.sh --service my-llm-app --duration 24h
```

Returns:
- Token usage statistics (prompt + completion)
- Cost estimates based on model pricing
- Model latency (P50, P95, P99)
- Error rates by model
- Most expensive operations
- Token usage trends

### 8. Manage Monitors

Create, list, mute, and manage Datadog monitors:

```bash
# List all monitors
bash scripts/manage-monitors.sh list

# Create error rate monitor
bash scripts/manage-monitors.sh create \
  --name "High Error Rate" \
  --query "avg(last_5m):sum:trace.express.request.errors{service:my-service}.as_count() > 10" \
  --message "Error rate is high @slack-alerts"

# Mute monitor for 2 hours
bash scripts/manage-monitors.sh mute --id 12345 --duration 2

# Unmute monitor
bash scripts/manage-monitors.sh unmute --id 12345
```

Returns:
- Monitor list with states (alert, warn, OK)
- Created monitor ID and details
- Mute/unmute confirmations

### 9. Create Dashboards

Generate dashboards from templates:

```bash
# Create APM performance dashboard
bash scripts/create-dashboard.sh --service payment-api --title "Payment API Performance" --type apm

# Create security monitoring dashboard
bash scripts/create-dashboard.sh --service payment-api --title "Security Dashboard" --type security

# Create cost analysis dashboard
bash scripts/create-dashboard.sh --title "Infrastructure Costs" --type cost

# Create LLM observability dashboard
bash scripts/create-dashboard.sh --service my-genai-app --title "LLM Performance" --type llm
```

Dashboard types:
- apm: Latency, errors, throughput by endpoint
- logs: Log volume and error analysis
- security: Security threats and attack patterns
- cost: APM, logs, infrastructure costs
- llm: Token usage, costs, model performance

### 10. Query SLOs

Check Service Level Objectives and error budgets:

```bash
# List all SLOs
bash scripts/query-slos.sh

# List SLOs for service
bash scripts/query-slos.sh --service payment-api

# List SLOs with tag
bash scripts/query-slos.sh --tag team:backend
```

Returns:
- SLO status (breaching, warning, OK)
- Current value vs target threshold
- Error budget remaining
- Error budget status (exhausted, low, healthy)

### 11. Trigger Workflows

Execute Datadog workflow automation:

```bash
# List available workflows
bash scripts/trigger-workflow.sh list

# Trigger workflow
bash scripts/trigger-workflow.sh run --id abc123

# Trigger with input data
bash scripts/trigger-workflow.sh run --id abc123 --input '{"service": "payment-api", "severity": "high"}'
```

Returns:
- Workflow list with IDs and descriptions
- Workflow instance ID when triggered
- Execution status

### 12. Manage Incidents

Create and manage incident response:

```bash
# List active incidents
bash scripts/manage-incidents.sh list --status active

# Create critical incident
bash scripts/manage-incidents.sh create \
  --title "Payment API Down" \
  --service payment-api \
  --severity SEV-1

# Update incident status
bash scripts/manage-incidents.sh update --id abc123 --status resolved

# Get incident details
bash scripts/manage-incidents.sh get --id abc123
```

Returns:
- Incident list with status and severity
- Created incident ID and details
- Incident timeline and updates

### 13. Query Service Catalog

List services and ownership metadata:

```bash
# List all services
bash scripts/query-service-catalog.sh list

# List services for team
bash scripts/query-service-catalog.sh list --team backend

# Get service details
bash scripts/query-service-catalog.sh get --service payment-api
```

Returns:
- Service metadata (kind, tier, lifecycle)
- Team ownership and contacts
- Repository links
- Integration details

### 14. Manage Synthetic Tests

Create uptime checks and API tests:

```bash
# List all synthetic tests
bash scripts/manage-synthetics.sh list

# Create API uptime check
bash scripts/manage-synthetics.sh create-api \
  --name "Payment API Uptime" \
  --url "https://api.example.com/health" \
  --method GET

# Create browser test
bash scripts/manage-synthetics.sh create-browser \
  --name "Login Flow" \
  --url "https://app.example.com/login"

# Get test results
bash scripts/manage-synthetics.sh get --id abc-123-def
```

Returns:
- Test list with status (active, paused)
- Created test ID and configuration
- Test results and uptime status

### 15. Query Database Performance

Analyze database queries and performance:

```bash
# Query database performance
bash scripts/query-database.sh --host postgres-prod --duration 1h

# Get slow queries
bash scripts/query-database.sh --host mysql-01 --duration 24h
```

Returns:
- Slow query patterns
- P95/avg query duration
- Connection metrics
- Top queries by latency

### 16. Query RUM (Real User Monitoring)

Analyze frontend performance and user experience:

```bash
# Query RUM data for application
bash scripts/query-rum.sh --application abc-123-def --duration 1h

# Get page load performance
bash scripts/query-rum.sh --application abc-123-def --duration 24h
```

Returns:
- Page load times (avg, P95)
- Frontend errors
- Top pages by traffic
- Error rate and types

### 17. Verify Setup

Validate Datadog configuration:

```bash
bash scripts/verify-setup.sh
```

Returns:
- Environment variable validation
- Agent connectivity check
- Tracer installation detection

## Incident Investigation Workflow

When investigating production issues:

**1. Identify scope**
```bash
# Check for security threats
bash scripts/query-security-signals.sh --severity critical --duration 1h

# Check for anomalies
bash scripts/query-watchdog.sh --service affected-service --duration 24h
```

**2. Find performance issues**
```bash
# Find slow endpoints
bash scripts/query-apm.sh --service affected-service --duration 1h

# Check error patterns
bash scripts/search-logs.sh --service affected-service --status error --duration 1h
```

**3. Analyze metrics**
```bash
# Check latency trends
bash scripts/query-metrics.sh --metric "trace.express.request.duration" --service affected-service --duration 24h

# Check error rate trends
bash scripts/query-metrics.sh --metric "trace.express.request.errors" --service affected-service --duration 24h
```

**4. Get specific traces**
```bash
# Get error traces
bash scripts/query-apm.sh --service affected-service --status error --limit 10

# Search logs for trace context
bash scripts/search-logs.sh --query "trace_id:abc123def456"
```

## Security Analysis Workflow

Monitor and investigate security threats:

```bash
# Check critical security signals
bash scripts/query-security-signals.sh --severity critical --duration 7d

# Analyze specific service
bash scripts/query-security-signals.sh --service payment-api --duration 24h

# Search for attack patterns in logs
bash scripts/search-logs.sh --query "sql injection OR xss OR authentication failed" --duration 24h
```

## Cost Optimization Workflow

Analyze and optimize Datadog costs:

```bash
# Get full cost breakdown
bash scripts/analyze-usage-cost.sh --duration 30d --product all

# Focus on APM costs
bash scripts/analyze-usage-cost.sh --duration 30d --product apm

# Extract high-priority recommendations
bash scripts/analyze-usage-cost.sh --duration 30d --product all | jq '.recommendations[] | select(.priority == "high")'

# Track weekly trends
bash scripts/analyze-usage-cost.sh --duration 7d --product all | jq '.cost_summary'
```

## LLM Observability Workflow

For GenAI applications, monitor token usage and costs:

```bash
# Analyze LLM performance
bash scripts/analyze-llm.sh --service my-genai-app --duration 24h

# Filter by specific model
bash scripts/analyze-llm.sh --service my-genai-app --model gpt-4 --duration 7d

# Find most expensive operations
bash scripts/analyze-llm.sh --service my-genai-app --duration 30d | jq '.operations | sort_by(.total_cost_usd) | reverse | .[0:5]'

# Track token usage trends
bash scripts/analyze-llm.sh --service my-genai-app --duration 7d | jq '.summary.token_usage'
```

## Deployment Impact Analysis

Compare metrics before/after deployment:

```bash
# Before deployment
bash scripts/query-apm.sh --service my-service --duration 1h > before.json
bash scripts/query-metrics.sh --metric "trace.express.request.duration" --service my-service --duration 1h >> before_metrics.json

# Deploy...

# After deployment
bash scripts/query-apm.sh --service my-service --duration 1h > after.json
bash scripts/query-metrics.sh --metric "trace.express.request.duration" --service my-service --duration 1h >> after_metrics.json

# Compare latency
jq -s '.[0].summary.avg_p95_ms - .[1].summary.avg_p95_ms' before.json after.json

# Check for new errors
bash scripts/search-logs.sh --service my-service --status error --duration 30m
```

## Monitor Creation Workflow

Set up monitoring for new services:

```bash
# Create latency monitor
bash scripts/manage-monitors.sh create \
  --name "Payment API - High Latency" \
  --query "avg(last_5m):avg:trace.express.request.duration{service:payment-api} > 500" \
  --message "P95 latency above 500ms @slack-ops"

# Create error rate monitor
bash scripts/manage-monitors.sh create \
  --name "Payment API - Error Rate" \
  --query "avg(last_5m):sum:trace.express.request.errors{service:payment-api}.as_count() / sum:trace.express.request.hits{service:payment-api}.as_count() > 0.05" \
  --message "Error rate above 5% @pagerduty"

# Create APM dashboard
bash scripts/create-dashboard.sh --service payment-api --title "Payment API Performance" --type apm

# Create security dashboard
bash scripts/create-dashboard.sh --service payment-api --title "Payment API Security" --type security
```

## Incident Response Workflow

Automated incident management:

```bash
# Check for SLO breaches
bash scripts/query-slos.sh --service payment-api | jq '.slos[] | select(.status == "breaching")'

# Create incident if SLO breached
bash scripts/manage-incidents.sh create \
  --title "Payment API SLO Breach" \
  --service payment-api \
  --severity SEV-2

# Trigger remediation workflow
bash scripts/trigger-workflow.sh run --id remediation-workflow-123 --input '{"service": "payment-api"}'

# Mute non-critical monitors during incident
bash scripts/manage-monitors.sh list --service payment-api | \
  jq '.monitors[] | select(.name | contains("non-critical")) | .id' | \
  xargs -I {} bash scripts/manage-monitors.sh mute --id {} --duration 2

# Update incident when resolved
bash scripts/manage-incidents.sh update --id abc123 --status resolved
```

## SLO Monitoring Workflow

Track service level objectives:

```bash
# Check all SLOs
bash scripts/query-slos.sh

# Alert if error budget exhausted
EXHAUSTED=$(bash scripts/query-slos.sh | jq '.summary.budget_exhausted')
if [ "$EXHAUSTED" -gt 0 ]; then
  bash scripts/manage-incidents.sh create \
    --title "Error Budget Exhausted" \
    --service affected-service \
    --severity SEV-3
fi

# Weekly SLO report
bash scripts/query-slos.sh | jq '{
  total: .total_slos,
  breaching: .summary.breaching,
  low_budget: .summary.budget_low,
  at_risk: [.slos[] | select(.error_budget_remaining < 20) | {name, budget: .error_budget_remaining}]
}'
```

## Output Format

All scripts return structured JSON for programmatic parsing:

```json
{
  "status": "ok|warning|critical|error",
  "summary": {
    "...": "aggregated metrics"
  },
  "data": [...],
  "recommendations": [...]
}
```

Status messages go to stderr, JSON to stdout. This allows:

```bash
# Silent execution, capture JSON
bash scripts/query-apm.sh --service my-service --duration 1h 2>/dev/null | jq '.summary'

# Log messages only
bash scripts/query-apm.sh --service my-service --duration 1h >/dev/null

# Both
bash scripts/query-apm.sh --service my-service --duration 1h
```

## Best Practices

**Query Optimization**
- Use specific time ranges to reduce API calls
- Filter by service/environment early
- Paginate large result sets
- Cache results when appropriate

**Alert Investigation**
- Start with Watchdog anomalies (automated detection)
- Correlate security signals with application errors
- Check metrics for trend confirmation
- Search logs for detailed context

**Cost Control**
- Run analyze-usage-cost.sh monthly
- Implement high-priority recommendations first
- Monitor sampling rates for high-volume services
- Track custom metric growth

**Security Monitoring**
- Query security signals daily (automated check)
- Filter by critical severity for alerting
- Correlate with log patterns
- Track attack trends over time

## Limitations

- API rate limits apply (varies by endpoint)
- Historical data retention depends on Datadog plan
- Real-time queries have eventual consistency
- Requires live Datadog data (APM, logs, security monitoring)

## Resources

- [Datadog API Documentation](https://docs.datadoghq.com/api/)
- [APM Query Syntax](https://docs.datadoghq.com/tracing/trace_explorer/query_syntax/)
- [Log Query Syntax](https://docs.datadoghq.com/logs/explorer/search_syntax/)
- [Watchdog Alerts](https://docs.datadoghq.com/watchdog/alerts/)
- [Security Monitoring](https://docs.datadoghq.com/security/application_security/)
- [Usage Metering API](https://docs.datadoghq.com/api/latest/usage-metering/)

## Notes

This skill provides comprehensive Datadog automation: query live data to investigate issues AND create infrastructure (monitors, dashboards, incidents) for ongoing operations. It does not handle installation or initial setup - use Datadog documentation for that.

**Investigation:** Query APM, logs, metrics, security signals, SLOs, costs, and LLM usage to debug production issues.

**Automation:** Create monitors, generate dashboards, trigger workflows, manage incidents, and mute alerts during maintenance.

All scripts return structured JSON for integration with CI/CD pipelines, ChatOps workflows, and automation platforms.
