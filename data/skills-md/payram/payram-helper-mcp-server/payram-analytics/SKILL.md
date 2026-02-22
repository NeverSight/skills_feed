---
name: payram-analytics
description: Query PayRam analytics via MCP tools to retrieve payments, user growth, transaction summaries, and project metrics. Covers discovery, graph data fetching, and ready-to-run workflows for dashboards and reports. Use when building analytics dashboards, generating reports, monitoring payment trends, or automating insights from PayRam.
---

# PayRam Analytics

> **Need deployment first?** See [`payram-setup`](https://github.com/payram/payram-mcp/tree/main/skills/payram-setup) or [`payram-agent-onboarding`](https://github.com/payram/payram-mcp/tree/main/skills/payram-agent-onboarding).

PayRam Analytics exposes MCP tools that query the PayRam analytics API and return formatted summaries or pretty-printed JSON. Use these tools to power dashboards, weekly reports, or agent-driven insights.

## When to Use

- Build analytics dashboards for payments and revenue
- Monitor daily transaction volume and amounts
- Compare periods (last 7 days vs last 30 days)
- Track paying user growth and retention
- Generate project-level summaries and recent transactions

---

## Authentication

Most analytics tools require:

- `PAYRAM_ANALYTICS_TOKEN` (Bearer token)
- `PAYRAM_ANALYTICS_BASE_URL` (API base URL)

You can override per call using `token` and `base_url`.

---

## Quick Start

### 1) Discover available groups and graphs

```json
{
  "name": "payram_discover_analytics",
  "arguments": {}
}
```

### 2) Fetch graph data

```json
{
  "name": "payram_fetch_graph_data",
  "arguments": {
    "group_id": 2,
    "graph_id": 8,
    "date_filter": "last_30_days"
  }
}
```

---

## Common Workflows

### Payments Summary (amount + count)

```json
{
  "name": "payram_payments_summary",
  "arguments": {
    "date_filter": "last_30_days"
  }
}
```

### Payment Status Totals

```json
{
  "name": "payram_payment_summary",
  "arguments": {
    "project_id": 42
  }
}
```

### Daily Transaction Stats

```json
{
  "name": "payram_daily_stats",
  "arguments": {
    "date_filter": "last_14_days",
    "currency_codes": ["USDT", "USDC"],
    "include_amounts": true,
    "include_counts": true
  }
}
```

### Recent Transactions

```json
{
  "name": "payram_recent_transactions",
  "arguments": {
    "limit": 20
  }
}
```

### Search Payments

```json
{
  "name": "payram_payment_search",
  "arguments": {
    "query": "invoice_123",
    "limit": 50,
    "sort_by": "createdAt",
    "sort_direction": "DESC"
  }
}
```

---

## Tool Catalog

| Tool | Purpose |
|------|---------|
| `payram_discover_analytics` | List analytics groups, graphs, and filters |
| `payram_fetch_graph_data` | Fetch data for a specific graph by group/graph id |
| `payram_payments_summary` | Payment amount and count graphs (auto-discovery) |
| `payram_payment_summary` | Totals by payment status (open, closed, cancelled) |
| `payram_projects_list` | List external platform projects (id, name) |
| `payram_payment_search` | Search payments with filters and pagination |
| `payram_payment_link` | Create payment link for a project |
| `payram_numbers_summary` | Key numeric metrics from Numbers group |
| `payram_transaction_counts` | Per-day transaction counts and amounts |
| `payram_daily_stats` | Daily stats with optional counts/amounts |
| `payram_deposit_distribution` | Distribution by currency or blockchain |
| `payram_currency_breakdown` | Currency breakdown over time |
| `payram_paying_users` | New vs recurring paying users |
| `payram_user_growth` | Paying user growth and retention |
| `payram_recent_transactions` | Recent payments table |
| `payram_projects_summary` | Project-level analytics graphs |
| `payram_compare_periods` | Compare two periods for amount/count |
| `payram_analytics` | Raw analytics tool (list_groups, graph_data) |

---

## Date Filters and Ranges

Common options for `date_filter`:
- `today`, `yesterday`
- `last_7_days`, `last_14_days`, `last_30_days`
- `this_month`, `last_month`

For custom windows, use `custom_start_date` and `custom_end_date` in RFC3339 format.

---

## Notes and Tips

- Prefer `payram_discover_analytics` when unsure of available groups/graphs.
- Use `currency_codes` to narrow results to specific currencies.
- The tools return a `text` payload that is formatted for humans; parse only if necessary.

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| [`payram-payment-integration`](https://github.com/payram/payram-mcp/tree/main/skills/payram-payment-integration) | Integrate payments into your app |
| [`payram-webhook-integration`](https://github.com/payram/payram-mcp/tree/main/skills/payram-webhook-integration) | Receive payment events in real time |
| [`payram-setup`](https://github.com/payram/payram-mcp/tree/main/skills/payram-setup) | Deploy PayRam server with web dashboard |
| [`payram-agent-onboarding`](https://github.com/payram/payram-mcp/tree/main/skills/payram-agent-onboarding) | Agent onboarding — CLI-only deployment for agents |
