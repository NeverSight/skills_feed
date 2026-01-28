---
name: generate-analytics-reports
description: >
  Generate analytics reports from Olakai data using CLI commands.

  AUTO-INVOKE when user wants: usage summaries, KPI trends, risk analysis,
  ROI reports, efficiency metrics, agent comparisons, token usage reports,
  cost analysis, compliance reports, or any analytics without using the web dashboard.

  TRIGGER KEYWORDS: olakai, analytics, reports, usage summary, KPI trends,
  risk analysis, ROI, efficiency, agent comparison, token usage, cost analysis,
  metrics report, dashboard data, CLI analytics, terminal report, compliance,
  usage report, event summary, performance metrics, AI usage stats.

  DO NOT load for: setting up monitoring (use olakai-add-monitoring),
  troubleshooting (use olakai-troubleshoot), or creating new agents
  (use olakai-create-agent).
license: MIT
metadata:
  author: olakai
  version: "1.8.0"
---

# Generate Analytics Reports

This skill enables terminal-based analytics report generation using the Olakai CLI, eliminating the need to access the web UI for analytics insights.

For full documentation, see: https://app.olakai.ai/llms.txt

## Prerequisites

Before generating reports, ensure:

```bash
# 1. CLI is authenticated
olakai whoami

# 2. You have the agent ID (if reporting on specific agent)
olakai agents list --json | jq '.[] | {id, name}'
```

---

## Report Generation Workflow

1. **Gather context** - Determine agent ID, date range, and report type
2. **Query data** - Use CLI commands with `--json` flag
3. **Process output** - Extract relevant metrics using `jq`
4. **Generate visualizations** - Create ASCII charts and markdown tables
5. **Present report** - Format and display the complete report

---

## Available Data Sources

| Command | Data Retrieved |
|---------|---------------|
| `olakai activity list --json` | Events with tokens, model, risk, status |
| `olakai activity list --include-analytics --json` | + task, subtask, time saved, risk score |
| `olakai activity kpis --json` | Core KPIs (executions, compliance, ROI) + custom KPIs |
| `olakai activity kpis --period daily --json` | Time-series breakdown |
| `olakai activity kpis --include-atoms --json` | Per-event KPI values |
| `olakai agents list --json` | Agent metadata |
| `olakai kpis list --json` | KPI definitions |

---

## Report Type 1: Usage Summary Report

Shows total usage metrics across events, tokens, models, and agents.

### Data Collection

```bash
# Get recent events with analytics
olakai activity list --limit 100 --include-analytics --json > /tmp/events.json

# Extract summary metrics
cat /tmp/events.json | jq '{
  total_events: (.prompts | length),
  total_tokens: ([.prompts[].tokens // 0] | add),
  avg_tokens: ([.prompts[].tokens // 0] | add / length | floor),
  unique_models: ([.prompts[].model] | unique | length),
  models: ([.prompts[].model] | group_by(.) | map({model: .[0], count: length})),
  unique_agents: ([.prompts[].app] | unique | length),
  agents: ([.prompts[].app] | group_by(.) | map({agent: .[0], count: length})),
  success_rate: (([.prompts[] | select(.status != "error")] | length) / (.prompts | length) * 100 | floor)
}'
```

### Report Template

```markdown
# Usage Summary Report
Generated: [DATE]
Period: Last [N] events

## Overview
| Metric | Value |
|--------|-------|
| Total Events | [COUNT] |
| Total Tokens | [TOKENS] |
| Avg Tokens/Event | [AVG] |
| Success Rate | [RATE]% |

## Events by Model
[ASCII BAR CHART]

## Events by Agent
[ASCII BAR CHART]
```

### Example Output

```
# Usage Summary Report
Generated: 2025-01-21
Period: Last 100 events

## Overview
| Metric | Value |
|--------|-------|
| Total Events | 100 |
| Total Tokens | 45,230 |
| Avg Tokens/Event | 452 |
| Success Rate | 98% |

## Events by Model
gpt-4o          ████████████████████████████████████ 45
gpt-4o-mini     ██████████████████████ 28
claude-3-5      ████████████████ 20
gpt-3.5-turbo   █████ 7

## Events by Agent
code-assistant  ████████████████████████████████ 40
data-analyzer   ████████████████████████ 30
chat-support    ████████████████████ 25
test-agent      ████ 5
```

---

## Report Type 2: KPI Trends Report

Shows KPI values over time with period-over-period comparisons.

### Data Collection

```bash
# Get KPIs with daily breakdown
olakai activity kpis --period daily --json > /tmp/kpis_daily.json

# Get KPIs with weekly breakdown
olakai activity kpis --period weekly --json > /tmp/kpis_weekly.json

# Extract trend data
cat /tmp/kpis_daily.json | jq '{
  period: "daily",
  kpis: [.kpis[] | {
    name: .name,
    current: .value,
    trend: .trend,
    breakdown: .breakdown
  }]
}'
```

### For Custom KPIs with Agent Filter

```bash
# Get custom KPIs for specific agent
olakai activity kpis --agent-id AGENT_ID --period daily --json | jq '.kpis'

# List KPI definitions
olakai kpis list --agent-id AGENT_ID --json | jq '.[] | {name, unit, aggregation}'
```

### Report Template

```markdown
# KPI Trends Report
Generated: [DATE]
Agent: [AGENT_NAME] (or "All Agents")
Period: [PERIOD]

## Core KPIs
| KPI | Current | Previous | Change |
|-----|---------|----------|--------|
| Total Executions | [VAL] | [PREV] | [+/-]% |
| Compliance Rate | [VAL]% | [PREV]% | [+/-]% |
| Estimated ROI | $[VAL] | $[PREV] | [+/-]% |

## Custom KPIs
| KPI | Value | Unit | Aggregation |
|-----|-------|------|-------------|
| [NAME] | [VAL] | [UNIT] | [AGG] |

## Daily Trend (Last 7 Days)
[ASCII LINE CHART]
```

### Example Output

```
# KPI Trends Report
Generated: 2025-01-21
Agent: code-assistant
Period: Last 7 days

## Core KPIs
| KPI | Current | Previous | Change |
|-----|---------|----------|--------|
| Total Executions | 847 | 792 | +7% |
| Compliance Rate | 99.2% | 98.5% | +0.7% |
| Estimated ROI | $4,235 | $3,960 | +7% |

## Custom KPIs
| KPI | Value | Unit | Aggregation |
|-----|-------|------|-------------|
| Code Reviews | 156 | count | SUM |
| Bugs Found | 23 | count | SUM |
| Avg Response Quality | 4.7 | score | AVERAGE |

## Daily Executions (Last 7 Days)
     150 ┤                           ╭──
     125 ┤              ╭────────────╯
     100 ┤    ╭─────────╯
      75 ┤────╯
      50 ┤
         └──────────────────────────────
          Mon  Tue  Wed  Thu  Fri  Sat  Sun
```

---

## Report Type 3: Risk Analysis Report

Shows risk distribution, blocked events, and sensitivity patterns.

### Data Collection

```bash
# Get events with risk data
olakai activity list --limit 200 --include-analytics --json > /tmp/events.json

# Extract risk metrics
cat /tmp/events.json | jq '{
  total_events: (.prompts | length),
  high_risk: ([.prompts[] | select(.riskScore >= 7)] | length),
  medium_risk: ([.prompts[] | select(.riskScore >= 4 and .riskScore < 7)] | length),
  low_risk: ([.prompts[] | select(.riskScore < 4)] | length),
  blocked: ([.prompts[] | select(.status == "blocked")] | length),
  blocked_percentage: (([.prompts[] | select(.status == "blocked")] | length) / (.prompts | length) * 100),
  sensitivity_labels: ([.prompts[].sensitivityLabel] | group_by(.) | map({label: .[0], count: length})),
  avg_risk_score: ([.prompts[].riskScore // 0] | add / length)
}'
```

### Report Template

```markdown
# Risk Analysis Report
Generated: [DATE]
Period: Last [N] events

## Risk Overview
| Metric | Value |
|--------|-------|
| Total Events Analyzed | [COUNT] |
| High Risk Events | [COUNT] ([%]%) |
| Blocked Events | [COUNT] ([%]%) |
| Average Risk Score | [SCORE]/10 |

## Risk Distribution
[ASCII BAR CHART]

## Events by Sensitivity Label
[ASCII BAR CHART]

## High-Risk Event Details (Recent)
| Time | Agent | Risk Score | Reason |
|------|-------|------------|--------|
| [TIME] | [AGENT] | [SCORE] | [REASON] |
```

### Example Output

```
# Risk Analysis Report
Generated: 2025-01-21
Period: Last 200 events

## Risk Overview
| Metric | Value |
|--------|-------|
| Total Events Analyzed | 200 |
| High Risk Events | 8 (4%) |
| Blocked Events | 3 (1.5%) |
| Average Risk Score | 2.3/10 |

## Risk Distribution
Low (0-3)     ████████████████████████████████████████ 172 (86%)
Medium (4-6)  ████████ 20 (10%)
High (7-10)   ████ 8 (4%)

## Events by Sensitivity Label
Public        ████████████████████████████████████ 145
Internal      ██████████████████ 42
Confidential  ████ 10
Restricted    █ 3

## High-Risk Events (Recent 5)
| Time | Agent | Score | Model |
|------|-------|-------|-------|
| 10:23 | data-export | 8.5 | gpt-4o |
| 09:15 | chat-support | 7.2 | gpt-4o |
| 08:42 | code-assist | 7.0 | claude-3-5 |
```

---

## Report Type 4: ROI/Efficiency Report

Shows time saved, cost metrics, and productivity gains.

### Data Collection

```bash
# Get KPIs (includes ROI data)
olakai activity kpis --json > /tmp/kpis.json

# Get events with time saved data
olakai activity list --limit 100 --include-analytics --json > /tmp/events.json

# Extract efficiency metrics
cat /tmp/events.json | jq '{
  total_events: (.prompts | length),
  total_time_saved_minutes: ([.prompts[].timeSavedMinutes // 0] | add),
  avg_time_saved: ([.prompts[].timeSavedMinutes // 0] | add / length),
  total_tokens: ([.prompts[].tokens // 0] | add),
  by_task: ([.prompts[] | select(.task != null)] | group_by(.task) | map({
    task: .[0].task,
    count: length,
    time_saved: ([.[].timeSavedMinutes // 0] | add)
  }))
}'

# Get ROI from KPIs
cat /tmp/kpis.json | jq '.kpis[] | select(.name | contains("ROI") or contains("Compliance"))'
```

### Report Template

```markdown
# ROI/Efficiency Report
Generated: [DATE]
Period: Last [N] events

## Efficiency Summary
| Metric | Value |
|--------|-------|
| Total Events | [COUNT] |
| Total Time Saved | [HOURS] hours |
| Avg Time Saved/Event | [MIN] minutes |
| Estimated Cost Savings | $[AMOUNT] |

## Governance Compliance
| Metric | Value |
|--------|-------|
| Compliance Rate | [RATE]% |
| Policy Violations | [COUNT] |
| Auto-Blocked | [COUNT] |

## Time Saved by Task Type
[ASCII BAR CHART]

## ROI Breakdown
[ASCII PIE CHART or TABLE]
```

### Example Output

```
# ROI/Efficiency Report
Generated: 2025-01-21
Period: Last 100 events

## Efficiency Summary
| Metric | Value |
|--------|-------|
| Total Events | 100 |
| Total Time Saved | 12.5 hours |
| Avg Time Saved/Event | 7.5 minutes |
| Estimated Cost Savings | $1,875 |

## Governance Compliance
| Metric | Value |
|--------|-------|
| Compliance Rate | 99.2% |
| Policy Violations | 2 |
| Auto-Blocked | 1 |

## Time Saved by Task Type
Code Review      ████████████████████████████████ 4.2 hrs
Bug Analysis     ██████████████████████████ 3.5 hrs
Documentation    ████████████████████ 2.7 hrs
Refactoring      ████████████████ 2.1 hrs

## Productivity Multiplier
Based on avg 7.5 min saved per interaction:
- Daily (50 events): 6.25 hours saved
- Weekly (250 events): 31.25 hours saved
- Monthly (1000 events): 125 hours saved
```

---

## Report Type 5: Agent Comparison Report

Side-by-side comparison of metrics across multiple agents.

### Data Collection

```bash
# Get all agents
olakai agents list --json > /tmp/agents.json

# Get events for comparison
olakai activity list --limit 500 --include-analytics --json > /tmp/events.json

# Extract per-agent metrics
cat /tmp/events.json | jq '{
  agents: ([.prompts[].app] | unique | map(. as $agent | {
    name: $agent,
    events: ([($parent.prompts // [])[] | select(.app == $agent)] | length),
    tokens: ([($parent.prompts // [])[] | select(.app == $agent) | .tokens // 0] | add),
    avg_risk: ([($parent.prompts // [])[] | select(.app == $agent) | .riskScore // 0] | add / length)
  }))
}'

# Alternative: Get KPIs per agent
for agent_id in $(olakai agents list --json | jq -r '.[].id'); do
  echo "Agent: $agent_id"
  olakai activity kpis --agent-id $agent_id --json | jq '.kpis[] | {name, value}'
done
```

### Report Template

```markdown
# Agent Comparison Report
Generated: [DATE]
Agents Compared: [COUNT]

## Activity Volume
| Agent | Events | Tokens | Avg Tokens |
|-------|--------|--------|------------|
| [NAME] | [COUNT] | [TOKENS] | [AVG] |

## KPI Comparison
| KPI | [AGENT1] | [AGENT2] | [AGENT3] |
|-----|----------|----------|----------|
| Executions | [VAL] | [VAL] | [VAL] |
| Compliance | [VAL]% | [VAL]% | [VAL]% |
| ROI | $[VAL] | $[VAL] | $[VAL] |

## Risk Profile
[ASCII GROUPED BAR CHART]

## Activity Trend by Agent
[ASCII MULTI-LINE CHART]
```

### Example Output

```
# Agent Comparison Report
Generated: 2025-01-21
Agents Compared: 4

## Activity Volume
| Agent | Events | Tokens | Avg Tokens |
|-------|--------|--------|------------|
| code-assistant | 245 | 98,450 | 402 |
| data-analyzer | 189 | 156,230 | 827 |
| chat-support | 312 | 78,540 | 252 |
| test-agent | 54 | 12,340 | 229 |

## KPI Comparison
| KPI | code-assist | data-analyze | chat-support |
|-----|-------------|--------------|--------------|
| Compliance | 99.5% | 98.2% | 99.8% |
| Avg Risk | 1.8 | 3.2 | 1.2 |
| Time Saved | 18.5 hrs | 12.3 hrs | 8.7 hrs |

## Risk Profile by Agent
           Low    Medium    High
code-assist ████████████████████ █    │   92%  6%  2%
data-analyze ██████████████████ ████  ██  85% 10%  5%
chat-support █████████████████████ │   │   97%  2%  1%
test-agent  ███████████████████ ██    │   90%  8%  2%
```

---

## ASCII Visualization Functions

### Bar Chart Generator

To create horizontal bar charts, use this pattern:

```bash
# Generate bar chart from jq output
cat /tmp/events.json | jq -r '
  [.prompts[].model] | group_by(.) | map({model: .[0], count: length}) |
  sort_by(-.count) |
  (max_by(.count).count) as $max |
  .[] |
  "\(.model | .[0:15] | . + " " * (15 - length))  " +
  ("█" * ((.count / $max * 40) | floor)) +
  " \(.count)"
'
```

Example output:
```
gpt-4o           ████████████████████████████████████████ 45
gpt-4o-mini      █████████████████████████ 28
claude-3-5       ██████████████████ 20
```

### Percentage Bar

```bash
# Show percentage with visual bar
echo "Compliance: ████████████████████░░░░░ 85%"
```

Pattern:
```
[LABEL]: [FILLED █ * percentage/4][EMPTY ░ * (25-filled)] [VALUE]%
```

### Trend Indicators

```
↑ +7%   (increase)
↓ -3%   (decrease)
→ 0%    (stable)
```

---

## Quick Reference Commands

```bash
# Usage Summary
olakai activity list --limit 100 --json | jq '{
  events: (.prompts | length),
  tokens: ([.prompts[].tokens // 0] | add),
  models: ([.prompts[].model] | unique)
}'

# KPI Snapshot
olakai activity kpis --json | jq '.kpis[] | {name, value, unit}'

# Risk Summary
olakai activity list --limit 100 --json | jq '{
  high_risk: ([.prompts[] | select(.riskScore >= 7)] | length),
  blocked: ([.prompts[] | select(.status == "blocked")] | length)
}'

# Agent List
olakai agents list --json | jq '.[] | {id, name}'

# Per-Agent KPIs
olakai activity kpis --agent-id AGENT_ID --json

# Time-Series Data
olakai activity kpis --period daily --json
olakai activity kpis --period weekly --json
```

---

## Generating a Complete Report

Follow this workflow for any report type:

```bash
# 1. Determine scope
AGENT_ID="your-agent-id"  # or leave empty for all
LIMIT=100

# 2. Collect data
olakai activity list --limit $LIMIT --include-analytics --json > /tmp/activity.json
olakai activity kpis --agent-id $AGENT_ID --json > /tmp/kpis.json
olakai agents list --json > /tmp/agents.json

# 3. Process and format (example for usage summary)
echo "# Usage Summary Report"
echo "Generated: $(date +%Y-%m-%d)"
echo ""
echo "## Overview"
cat /tmp/activity.json | jq -r '"| Metric | Value |
|--------|-------|
| Total Events | \(.prompts | length) |
| Total Tokens | \([.prompts[].tokens // 0] | add) |
| Unique Models | \([.prompts[].model] | unique | length) |"'
```

---

## Error Handling

### No Data Available

```bash
# Check if events exist
olakai activity list --limit 1 --json | jq '.prompts | length'

# If 0, inform user:
# "No events found. Ensure your agent is sending events to Olakai."
```

### Agent Not Found

```bash
# Verify agent exists
olakai agents list --json | jq '.[] | select(.id == "AGENT_ID")'

# If empty, list available agents:
olakai agents list --json | jq '.[] | {id, name}'
```

### Missing Permissions

```bash
# Re-authenticate if needed
olakai logout && olakai login
olakai whoami  # Verify
```

---

## Best Practices

1. **Always use `--json` flag** for programmatic processing
2. **Pipe through `jq`** for clean data extraction
3. **Cache data locally** when generating multi-section reports
4. **Include timestamps** in all reports
5. **Show data freshness** - how recent the events are
6. **Handle empty states** gracefully with informative messages
