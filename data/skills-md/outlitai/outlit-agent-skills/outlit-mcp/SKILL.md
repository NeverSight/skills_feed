---
name: outlit-mcp
description: Use when querying Outlit customer data via MCP tools (outlit_*). Triggers on customer analytics, revenue metrics, activity timelines, cohort analysis, churn risk assessment, SQL queries against analytics data, or any Outlit data exploration task.
---

# Outlit MCP Server

Query customer intelligence data through 6 MCP tools covering customer and user profiles, revenue metrics, activity timelines, and raw SQL analytics access.

## Quick Start

| What you need | Tool |
|---------------|------|
| Browse/filter customers | `outlit_list_customers` |
| Browse/filter users | `outlit_list_users` |
| Single customer deep dive | `outlit_get_customer` |
| Customer activity history | `outlit_get_timeline` |
| Custom analytics / aggregations | `outlit_query` (SQL) |
| Discover tables & columns | `outlit_schema` |

**Before writing SQL:** Always call `outlit_schema` first to discover available tables and columns.

### Common Patterns

**Find at-risk customers:**
```json
{
  "tool": "outlit_list_customers",
  "billingStatus": "PAYING",
  "noActivityInLast": "30d",
  "orderBy": "mrr_cents",
  "orderDirection": "desc"
}
```

**Revenue breakdown (SQL):**
```json
{
  "tool": "outlit_query",
  "sql": "SELECT billing_status, count(*) as customers, sum(mrr_cents)/100 as mrr_dollars FROM customer_dimensions GROUP BY 1 ORDER BY 3 DESC"
}
```

---

## MCP Setup

### Get an API Key

Go to **Settings > MCP Integration** in the Outlit dashboard ([app.outlit.ai](https://app.outlit.ai)).

### Auto-Detection Setup

Detect the current environment and run the appropriate setup command:

1. **Check for Claude Code** — If running inside Claude Code (check if `claude` CLI is available), run:
   ```bash
   claude mcp add outlit https://mcp.outlit.ai/mcp -- --header "Authorization: Bearer API_KEY"
   ```

2. **Check for Cursor** — If `.cursor/mcp.json` exists in the project or home directory, add to that file:
   ```json
   {
     "mcpServers": {
       "outlit": {
         "url": "https://mcp.outlit.ai/mcp",
         "headers": { "Authorization": "Bearer API_KEY" }
       }
     }
   }
   ```

3. **Check for Claude Desktop** — If `claude_desktop_config.json` exists at `~/Library/Application Support/Claude/` (macOS) or `%APPDATA%/Claude/` (Windows), add to that file:
   ```json
   {
     "mcpServers": {
       "outlit": {
         "url": "https://mcp.outlit.ai/mcp",
         "headers": { "Authorization": "Bearer API_KEY" }
       }
     }
   }
   ```

Ask the user for their API key if not provided. Replace `API_KEY` with the actual key.

### Verify Connection

Call `outlit_schema` to confirm the connection is working.

---

## Tool Reference

### outlit_list_customers

Filter and paginate customers.

| Key Params | Values |
|------------|--------|
| `billingStatus` | NONE, TRIALING, PAYING, CHURNED |
| `hasActivityInLast` / `noActivityInLast` | 7d, 14d, 30d, 90d (mutually exclusive) |
| `mrrAbove` / `mrrBelow` | cents (10000 = $100) |
| `search` | name or domain |
| `orderBy` | last_activity_at, first_seen_at, name, mrr_cents |
| `limit` | 1-1000 (default: 20) |
| `cursor` | pagination token |

### outlit_list_users

Filter and paginate users.

| Key Params | Values |
|------------|--------|
| `journeyStage` | DISCOVERED, SIGNED_UP, ACTIVATED, ENGAGED, INACTIVE |
| `customerId` | filter by customer |
| `hasActivityInLast` / `noActivityInLast` | Nd, Nh, or Nm (e.g., 7d, 24h) — mutually exclusive |
| `search` | email or name |
| `orderBy` | last_activity_at, first_seen_at, email |
| `limit` | 1-1000 (default: 20) |
| `cursor` | pagination token |

### outlit_get_customer

Single customer deep dive. Accepts customer ID, domain, or name.

| Key Params | Values |
|------------|--------|
| `customer` | customer ID, domain, or name (required) |
| `include` | `users`, `revenue`, `recentTimeline`, `behaviorMetrics` |
| `timeframe` | 7d, 14d, 30d, 90d (default: 30d) |

Only request the `include` sections you need — omitting unused ones is faster.

### outlit_get_timeline

Activity timeline for a customer.

| Key Params | Values |
|------------|--------|
| `customer` | customer ID or domain (required) |
| `channels` | SDK, EMAIL, SLACK, CALL, CRM, BILLING, SUPPORT, INTERNAL |
| `eventTypes` | filter by specific event types |
| `timeframe` | 7d, 14d, 30d, 90d, all (default: 30d) |
| `startDate` / `endDate` | ISO 8601 (mutually exclusive with timeframe) |
| `limit` | 1-1000 (default: 50) |
| `cursor` | pagination token |

### outlit_query

Raw SQL against ClickHouse analytics tables. **SELECT only.** See [SQL Reference](references/sql-reference.md) for ClickHouse syntax and security model.

| Key Params | Values |
|------------|--------|
| `sql` | SQL SELECT query (required) |
| `limit` | 1-10000 (default: 1000) |

Available tables: `events`, `customer_dimensions`, `user_dimensions`, `mrr_snapshots`.

### outlit_schema

Discover tables and columns. Call with no params for all tables, or `table: "events"` for a specific table. Always call this before writing SQL.

---

## Data Model

**Billing status:** NONE → TRIALING → PAYING → CHURNED

**Journey stages:** DISCOVERED → SIGNED_UP → ACTIVATED → ENGAGED → INACTIVE

**Data formats:**
- Monetary values in cents (divide by 100 for dollars)
- Timestamps in ISO 8601
- IDs with string prefixes (`cust_`, `contact_`, `evt_`)

**Pagination:** All list endpoints use cursor-based pagination. Check `pagination.hasMore` before requesting more pages. Pass `pagination.nextCursor` as `cursor` for the next page.

---

## Best Practices

1. **Call `outlit_schema` before writing SQL** — discover columns, don't guess
2. **Use customer tools for single lookups** — don't use SQL for individual customer queries
3. **Filter at the source** — use tool params and WHERE clauses, not post-fetch filtering
4. **Only request needed includes** — omit unused `include` options for faster responses
5. **Always add time filters to event SQL** — `WHERE occurred_at >= now() - INTERVAL N DAY`
6. **Convert cents to dollars** — divide monetary values by 100 for display
7. **Use LIMIT in SQL** — cap result sets to avoid large data transfers

## Known Limitations

1. **SQL is read-only** — no INSERT, UPDATE, DELETE
2. **Organization isolation** — cannot query other organizations' data
3. **Timeline requires a customer** — cannot query timeline across all customers
4. **MRR filtering is post-fetch** — may be slower on large datasets in list_customers
5. **Event queries need time filters** — queries without date ranges scan all data
6. **ClickHouse syntax** — uses different functions than MySQL/PostgreSQL (see [SQL Reference](references/sql-reference.md))

---

## Tool Gotchas

| Tool | Gotcha |
|------|--------|
| `outlit_list_customers` | `hasActivityInLast` and `noActivityInLast` are mutually exclusive |
| `outlit_list_customers` | `search` checks name and domain only |
| `outlit_get_customer` | `behaviorMetrics` depends on timeframe — extend it if empty |
| `outlit_get_timeline` | `timeframe` and `startDate`/`endDate` are mutually exclusive |
| `outlit_query` | Use ClickHouse date syntax: `now() - INTERVAL 30 DAY`, not `DATE_SUB()` |
| `outlit_query` | `properties` column is JSON — use `JSONExtractString(properties, 'key')` |

---

## References

| Reference | When to Read |
|-----------|--------------|
| [SQL Reference](references/sql-reference.md) | ClickHouse syntax, security model, query patterns |
| [Workflows](references/workflows.md) | Multi-step analysis: churn risk, revenue dashboards, account health |
