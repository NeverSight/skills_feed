---
name: building-dashboards
description: Designs and builds Axiom dashboards via API. Covers chart types, APL patterns, SmartFilters, layout, and configuration options. Use when creating dashboards, migrating from Splunk, or configuring chart options.
---

# Building Dashboards

You design dashboards that help humans make decisions quickly. Dashboards are products: audience, questions, and actions matter more than chart count.

## Philosophy

1. **Decisions first.** Every panel answers a question that leads to an action.
2. **Overview → drilldown → evidence.** Start broad, narrow on click/filter, end with raw logs.
3. **Rates and percentiles over averages.** Averages hide problems; p95/p99 expose them.
4. **Simple beats dense.** One question per panel. No chart junk.
5. **Validate with data.** Never guess fields—discover schema first.

---

## Entry Points

Choose your starting point:

| Starting from | Workflow |
|---------------|----------|
| **Vague description** | Intake → design blueprint → APL per panel → deploy |
| **Template** | Pick template → customize dataset/service/env → deploy |
| **Splunk dashboard** | Extract SPL → translate via spl-to-apl → map to chart types → deploy |
| **Exploration** | Use axiom-sre to discover schema/signals → productize into panels |

---

## Intake: What to Ask First

Before designing, clarify:

1. **Audience & decision**
   - Oncall triage? (fast refresh, error-focused)
   - Team health? (daily trends, SLO tracking)
   - Exec reporting? (weekly summaries, high-level)

2. **Scope**
   - Service, environment, region, cluster, endpoint?
   - Single service or cross-service view?

3. **Datasets**
   - Which Axiom datasets contain the data?
   - Run `getschema` to discover fields—never guess:
   ```apl
   ['dataset'] | where _time between (ago(1h) .. now()) | getschema
   ```

4. **Golden signals**
   - Traffic: requests/sec, events/min
   - Errors: error rate, 5xx count
   - Latency: p50, p95, p99 duration
   - Saturation: CPU, memory, queue depth, connections

5. **Drilldown dimensions**
   - What do users filter/group by? (service, route, status, pod, customer_id)

---

## Dashboard Blueprint

Use this 4-section structure as the default:

### 1. At-a-Glance (Statistic panels)
Single numbers that answer "is it broken right now?"
- Error rate (last 5m)
- p95 latency (last 5m)
- Request rate (last 5m)
- Active alerts (if applicable)

### 2. Trends (TimeSeries panels)
Time-based patterns that answer "what changed?"
- Traffic over time
- Error rate over time
- Latency percentiles over time
- Stacked by status/service for comparison

### 3. Breakdowns (Table/Pie panels)
Top-N analysis that answers "where should I look?"
- Top 10 failing routes
- Top 10 error messages
- Worst pods by error rate
- Request distribution by status

### 4. Evidence (LogStream + SmartFilter)
Raw events that answer "what exactly happened?"
- LogStream filtered to errors
- SmartFilter for service/env/route
- Key fields projected for readability

---

## Chart Types

**Note:** Dashboard queries inherit time from the UI picker—no explicit `_time` filter needed.

**Validation:** TimeSeries, Statistic, Table, Pie, LogStream, Note, MonitorList are fully validated by `dashboard-validate`. Heatmap, ScatterPlot, SmartFilter work but may trigger warnings.

### Statistic
**When:** Single KPI, current value, threshold comparison.

```apl
['logs']
| where service == "api"
| summarize 
    total = count(),
    errors = countif(status >= 500)
| extend error_rate = round(100.0 * errors / total, 2)
| project error_rate
```

**Pitfalls:** Don't use for time series; ensure query returns single row.

### TimeSeries
**When:** Trends over time, before/after comparison, rate changes.

```apl
// Single metric - use bin_auto for automatic sizing
['logs']
| summarize ['req/min'] = count() by bin_auto(_time)

// Latency percentiles - use percentiles_array for proper overlay
['logs']
| summarize percentiles_array(duration_ms, 50, 95, 99) by bin_auto(_time)
```

**Best practices:**
- Use `bin_auto(_time)` instead of fixed `bin(_time, 1m)` — auto-adjusts to time window
- Use `percentiles_array()` instead of multiple `percentile()` calls — renders as one chart
- Too many series = unreadable; use `top N` or filter

### Table
**When:** Top-N lists, detailed breakdowns, exportable data.

```apl
['logs']
| where status >= 500
| summarize errors = count() by route, error_message
| top 10 by errors
| project route, error_message, errors
```

**Pitfalls:**
- Always use `top N` to prevent unbounded results
- Use `project` to control column order and names

### Pie
**When:** Share-of-total for LOW cardinality dimensions (≤6 slices).

```apl
['logs']
| summarize count() by status_class = case(
    status < 300, "2xx",
    status < 400, "3xx",
    status < 500, "4xx",
    "5xx"
  )
```

**Pitfalls:**
- Never use for high cardinality (routes, user IDs)
- Prefer tables for >6 categories
- Always aggregate to reduce slices

### LogStream
**When:** Raw event inspection, debugging, evidence gathering.

```apl
['logs']
| where service == "api" and status >= 500
| project-keep _time, trace_id, route, status, error_message, duration_ms
| take 100
```

**Pitfalls:**
- Always include `take N` (100-500 max)
- Use `project-keep` to show relevant fields only
- Filter aggressively—raw logs are expensive

### Heatmap
**When:** Distribution visualization, latency patterns, density analysis.

```apl
['logs']
| summarize histogram(duration_ms, 15) by bin_auto(_time)
```

**Best for:** Latency distributions, response time patterns, identifying outliers.

### Scatter Plot
**When:** Correlation between two metrics, identifying patterns.

```apl
['logs']
| summarize avg(duration_ms), avg(resp_size_bytes) by route
```

**Best for:** Response size vs latency correlation, resource usage patterns.

### SmartFilter (Filter Bar)
**When:** Interactive filtering for the entire dashboard.

SmartFilter is a **chart type** that creates dropdown/search filters. Requires:
1. A `SmartFilter` chart with filter definitions
2. `declare query_parameters` in each panel query

**Filter types:**
- `selectType: "apl"` — Dynamic dropdown from APL query
- `selectType: "list"` — Static dropdown with predefined options
- `type: "search"` — Free-text input

**Panel query pattern:**
```apl
declare query_parameters (country_filter:string = "");
['logs'] | where isempty(country_filter) or ['geo.country'] == country_filter
```

See `reference/smartfilter.md` for full JSON structure and cascading filter examples.

### Monitor List
**When:** Display monitor status on operational dashboards.

No APL needed—select monitors from the UI. Shows:
- Monitor status (normal/triggered/off)
- Run history (green/red squares)
- Dataset, type, notifiers

### Note
**When:** Context, instructions, section headers.

Use GitHub Flavored Markdown for:
- Dashboard purpose and audience
- Runbook links
- Section dividers
- On-call instructions

---

## Chart Configuration

Charts support JSON configuration options beyond the query. See `reference/chart-config.md` for full details.

**Quick reference:**

| Chart Type | Key Options |
|------------|-------------|
| Statistic | `colorScheme`, `customUnits`, `unit`, `showChart` (sparkline), `errorThreshold`/`warningThreshold` |
| TimeSeries | `aggChartOpts`: `variant` (line/area/bars), `scaleDistr` (linear/log), `displayNull` |
| LogStream/Table | `tableSettings`: `columns`, `fontSize`, `highlightSeverity`, `wrapLines` |
| Pie | `hideHeader` |
| Note | `text` (markdown), `variant` |

**Common options (all charts):**
- `overrideDashboardTimeRange`: boolean
- `overrideDashboardCompareAgainst`: boolean  
- `hideHeader`: boolean

---

## APL Patterns

### Time Filtering in Dashboards vs Ad-hoc Queries

**Dashboard panel queries do NOT need explicit time filters.** The dashboard UI time picker automatically scopes all queries to the selected time window.

```apl
// DASHBOARD QUERY — no time filter needed
['logs']
| where service == "api"
| summarize count() by bin_auto(_time)
```

**Ad-hoc queries (Axiom Query tab, axiom-sre exploration) MUST have explicit time filters:**

```apl
// AD-HOC QUERY — always include time filter
['logs']
| where _time between (ago(1h) .. now())
| where service == "api"
| summarize count() by bin_auto(_time)
```

### Bin Size Selection

**Prefer `bin_auto(_time)`** — it automatically adjusts to the dashboard time window.

Manual bin sizes (only when auto doesn't fit your needs):

| Time window | Bin size |
|-------------|----------|
| 15m | 10s–30s |
| 1h | 1m |
| 6h | 5m |
| 24h | 15m–1h |
| 7d | 1h–6h |

### Cardinality Guardrails
Prevent query explosion:

```apl
// GOOD: bounded
| summarize count() by route | top 10 by count_

// BAD: unbounded high-cardinality grouping
| summarize count() by user_id  // millions of rows
```

### Field Escaping
Fields with dots need bracket notation:

```apl
| where ['kubernetes.pod.name'] == "frontend"
```

Fields with dots IN the name (not hierarchy) need escaping:

```apl
| where ['kubernetes.labels.app\\.kubernetes\\.io/name'] == "frontend"
```

### Golden Signal Queries

**Traffic:**
```apl
| summarize requests = count() by bin_auto(_time)
```

**Errors (as rate %):**
```apl
| summarize total = count(), errors = countif(status >= 500) by bin_auto(_time)
| extend error_rate = iff(total > 0, round(100.0 * errors / total, 2), 0.0)
| project _time, error_rate
```

**Latency (use percentiles_array for proper chart overlay):**
```apl
| summarize percentiles_array(duration_ms, 50, 95, 99) by bin_auto(_time)
```

---

## Layout Composition

### Grid Principles
- Dashboard width = 12 units
- Typical panel: w=3 (quarter), w=4 (third), w=6 (half), w=12 (full)
- Stats row: 4 panels × w=3, h=2
- TimeSeries row: 2 panels × w=6, h=4
- Tables: w=6 or w=12, h=4–6
- LogStream: w=12, h=6–8

### Section Layout Pattern

```
Row 0-1:  [Stat w=3] [Stat w=3] [Stat w=3] [Stat w=3]
Row 2-5:  [TimeSeries w=6, h=4] [TimeSeries w=6, h=4]
Row 6-9:  [Table w=6, h=4] [Pie w=6, h=4]
Row 10+:  [LogStream w=12, h=6]
```

### Naming Conventions
- Use question-style titles: "Error rate by route" not "Errors"
- Prefix with context if multi-service: "[API] Error rate"
- Include units: "Latency (ms)", "Traffic (req/s)"

---

## Dashboard Settings

### Refresh Rate
Dashboard auto-refreshes at configured interval. Options: 15s, 30s, 1m, 5m, etc.

**⚠️ Query cost warning:** Short refresh (15s) + long time range (90d) = expensive queries running constantly.

Recommendations:
| Use case | Refresh rate |
|----------|-------------|
| Oncall/real-time | 15s–30s |
| Team health | 1m–5m |
| Executive/weekly | 5m–15m |

### Sharing
- **Just Me**: Private, only you can access
- **Group**: Specific team/group in your org
- **Everyone**: All users in your Axiom org

Data visibility is still governed by dataset permissions—users only see data from datasets they can access.

### URL Time Range Parameters

`?t_qr=24h` (quick range), `?t_ts=...&t_te=...` (custom), `?t_against=-1d` (comparison)

---

## Setup

Run `scripts/setup` to check requirements (curl, jq, ~/.axiom.toml).

Config in `~/.axiom.toml` (shared with axiom-sre):
```toml
[deployments.prod]
url = "https://api.axiom.co"
token = "xaat-your-token"
org_id = "your-org-id"
```

---

## Deployment

### Scripts

| Script | Usage |
|--------|-------|
| `scripts/get-user-id <deploy>` | Get your user ID for `owner` field |
| `scripts/dashboard-list <deploy>` | List all dashboards |
| `scripts/dashboard-get <deploy> <id>` | Fetch dashboard JSON |
| `scripts/dashboard-validate <file>` | Validate JSON structure |
| `scripts/dashboard-create <deploy> <file>` | Create dashboard |
| `scripts/dashboard-update <deploy> <id> <file>` | Update (needs version) |
| `scripts/dashboard-copy <deploy> <id>` | Clone dashboard |
| `scripts/dashboard-link <deploy> <id>` | Get shareable URL |
| `scripts/dashboard-delete <deploy> <id>` | Delete (with confirm) |
| `scripts/axiom-api <deploy> <method> <path>` | Low-level API calls |

### Workflow

**⚠️ CRITICAL: Always validate queries BEFORE deploying.**

1. Design dashboard (sections + panels)
2. Write APL for each panel
3. Build JSON (from template or manually)
4. **Validate queries** using axiom-sre with explicit time filter
5. `dashboard-validate` to check structure
6. `dashboard-create` or `dashboard-update` to deploy
7. **`dashboard-link` to get URL** — NEVER construct Axiom URLs manually (org IDs and base URLs vary per deployment)
8. Share link with user

---

## Sibling Skill Integration

**spl-to-apl:** Translate Splunk SPL → APL. Map `timechart` → TimeSeries, `stats` → Statistic/Table. See `reference/splunk-migration.md`.

**axiom-sre:** Discover schema with `getschema`, explore baselines, identify dimensions, then productize into panels.

---

## Templates

Pre-built templates in `reference/templates/`:

| Template | Use case |
|----------|----------|
| `service-overview.json` | Single service oncall dashboard with Heatmap |
| `service-overview-with-filters.json` | Same with SmartFilter (route/status dropdowns) |
| `api-health.json` | HTTP API with traffic/errors/latency |
| `blank.json` | Minimal skeleton |

**Placeholders:** `{{owner_id}}`, `{{service}}`, `{{dataset}}`

**Usage:**
```bash
USER_ID=$(scripts/get-user-id prod)
scripts/dashboard-from-template service-overview "my-service" "$USER_ID" "my-dataset" ./dashboard.json
scripts/dashboard-validate ./dashboard.json
scripts/dashboard-create prod ./dashboard.json
```

**⚠️ Templates assume field names** (`service`, `status`, `route`, `duration_ms`). Discover your schema first and use `sed` to fix mismatches.

---

## Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| "unable to find dataset" errors | Dataset name doesn't exist in your org | Check available datasets in Axiom UI |
| "creating dashboards for other users" 403 | Owner ID doesn't match your token | Use `scripts/get-user-id prod` to get your UUID |
| All panels show errors | Field names don't match your schema | Discover schema first, use sed to fix field names |
| Dashboard shows no data | Service filter too restrictive | Remove or adjust `where service == 'x'` filters |
| Queries time out | Missing time filter or too broad | Dashboard inherits time from picker; ad-hoc queries need explicit time filter |
| Wrong org in dashboard URL | Manually constructed URL | **Always use `dashboard-link <deploy> <id>`** — never guess org IDs or base URLs |

---

## Reference

- `reference/chart-config.md` — All chart configuration options (JSON)
- `reference/smartfilter.md` — SmartFilter/FilterBar full configuration
- `reference/chart-cookbook.md` — APL patterns per chart type
- `reference/layout-recipes.md` — Grid layouts and section blueprints
- `reference/splunk-migration.md` — Splunk panel → Axiom mapping
- `reference/design-playbook.md` — Decision-first design principles
- `reference/templates/` — Ready-to-use dashboard JSON files

For APL syntax: https://axiom.co/docs/apl/introduction
