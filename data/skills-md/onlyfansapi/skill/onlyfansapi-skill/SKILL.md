---
name: onlyfansapi-skill
description: >-
  Query OnlyFans data and analytics via the OnlyFansAPI.com platform. Get revenue
  summaries across all models, identify top-performing models, analyze
  Free Trial and Tracking Link conversion rates, compare link earnings, and much more!
  Use when users ask about anything related to OnlyFans.
compatibility: Requires curl, jq, and network access to app.onlyfansapi.com
metadata:
  author: OnlyFansAPI.com
  version: "1.0"
allowed-tools: Bash(curl:*) Bash(jq:*) Read
---

# OnlyFans API Skill

This skill queries the OnlyFansAPI.com platform to answer questions about OnlyFans agency analytics — revenue, model performance, and link conversion metrics.

## Prerequisites

The user must set the environment variable `ONLYFANSAPI_API_KEY` with their API key from <https://app.onlyfansapi.com/api-keys>.

If the key is not set, remind the user:

```
Export your OnlyFansAPI key:
  export ONLYFANSAPI_API_KEY="your_api_key_here"
```

## API Basics

- **Base URL:** `https://app.onlyfansapi.com`
- **Auth header:** `Authorization: Bearer $ONLYFANSAPI_API_KEY`
- All dates use URL-encoded format: `YYYY-MM-DD HH:MM:SS`
- If not specific time is specified use start of day or end of day (for date range ending date)
- Pagination: use `limit` and `offset` query params. Check `hasMore` or `_pagination.next_page` in responses.
- Whenever possible use User-Agent with value: OnlyFansAPI-Skill
- Try your best to infer schema from the example response of the endpoint. Eg "data.total.total" for earnings scalar value from endpoint.

## Workflows

### 1. Get revenue of all models for the past N days

**Steps:**

1. **List all connected accounts:**

   ```bash
   curl -s -H "Authorization: Bearer $ONLYFANSAPI_API_KEY" \
     "https://app.onlyfansapi.com/api/accounts" | jq .
   ```

   Each account object has `"id"` (e.g. `"acct_xxx"`), `"onlyfans_username"`, and `"display_name"`.

2. **For each account, get earnings:**

   ```bash
   START=$(date -u -v-7d '+%Y-%m-%d+00%%3A00%%3A00')  # macOS
   # Linux: START=$(date -u -d '7 days ago' '+%Y-%m-%d+00%%3A00%%3A00')
   END=$(date -u '+%Y-%m-%d+23%%3A59%%3A59')

   curl -s -H "Authorization: Bearer $ONLYFANSAPI_API_KEY" \
     "https://app.onlyfansapi.com/api/{account_id}/statistics/statements/earnings?start_date=$START&end_date=$END&type=total" | jq .
   ```

   Response fields:
   - `data.total` — net earnings
   - `data.gross` — gross earnings
   - `data.chartAmount` — daily earnings breakdown array
   - `data.delta` — percentage change vs. prior period

3. **Summarize:** Present a table of each model's display name, username, net revenue, and gross revenue. Sum the totals.

### 2. Which model is performing the best

Use the same workflow as above. Rank models by `data.total` (net earnings) descending. The model with the highest value is the best performer.

Optionally also pull the statistics overview for richer context:

```bash
curl -s -H "Authorization: Bearer $ONLYFANSAPI_API_KEY" \
  "https://app.onlyfansapi.com/api/{account_id}/statistics/overview?start_date=$START&end_date=$END" | jq .
```

This adds subscriber counts, visitor stats, post/message earnings breakdown.

### 3. Which Free Trial Link has the highest conversion rate (subscribers → spenders)

1. **List free trial links:**

   ```bash
   curl -s -H "Authorization: Bearer $ONLYFANSAPI_API_KEY" \
     "https://app.onlyfansapi.com/api/{account_id}/trial-links?limit=100&offset=0&sort=desc&field=subscribe_counts&synchronous=true" | jq .
   ```

   Key response fields per link:
   - `id`, `trialLinkName`, `url`
   - `claimCounts` — total subscribers who claimed the trial
   - `clicksCounts` — total clicks
   - `revenue.total` — total revenue from this link
   - `revenue.spendersCount` — number of subscribers who spent money
   - `revenue.revenuePerSubscriber` — average revenue per subscriber

2. **Calculate conversion rate:**

   ```
   conversion_rate = spendersCount / claimCounts
   ```

   Rank links by conversion rate descending.

3. **Present results** as a table: link name, claims, spenders, conversion rate, total revenue.

### 4. Which Tracking Link has the highest conversion rate

1. **List tracking links:**

   ```bash
   curl -s -H "Authorization: Bearer $ONLYFANSAPI_API_KEY" \
     "https://app.onlyfansapi.com/api/{account_id}/tracking-links?limit=100&offset=0&sort=desc&sortby=claims&synchronous=true" | jq .
   ```

   Key response fields per link:
   - `id`, `campaignName`, `campaignUrl`
   - `subscribersCount` — total subscribers from this link
   - `clicksCount` — total clicks
   - `revenue.total` — total revenue
   - `revenue.spendersCount` — subscribers who spent
   - `revenue.revenuePerSubscriber` — avg revenue per subscriber
   - `revenue.revenuePerClick` — avg revenue per click

2. **Calculate conversion rate:**

   ```
   conversion_rate = revenue.spendersCount / subscribersCount
   ```

3. **Present results** as a table: campaign name, subscribers, spenders, conversion rate, total revenue, revenue per subscriber.

### 5. Which Free Trial / Tracking Link made the most money

Use the same listing endpoints above. Sort by `revenue.total` descending. Present the top links with their name, type (trial vs. tracking), total revenue, and subscriber/spender counts.

## Multi-Account (Agency) Queries

For agency-level queries that span all models, always:

1. First fetch all accounts via `GET /api/accounts`
2. Loop through each account and gather the relevant data
3. Aggregate and present combined results with per-model breakdowns

## Earnings Type Filters

When querying `GET /api/{account}/statistics/statements/earnings`, the `type` parameter filters by category:

- `total` — all earnings combined
- `subscribes` — subscription revenue
- `tips` — tips received
- `post` — paid post revenue
- `messages` — paid message revenue
- `stream` — stream revenue

## When In Doubt

If you are unsure about an endpoint, parameter, response format, or how to accomplish a specific task with the OnlyFans API, consult the official documentation at <https://docs.onlyfansapi.com>. The site contains full API reference details, guides, and examples for all available endpoints. Always check the docs before guessing.

## Error Handling

- If `ONLYFANSAPI_API_KEY` is not set, stop and ask the user to configure it.
- If an API call returns a non-200 status, show the error message and HTTP status code.
- If `_meta._rate_limits.remaining_minute` or `remaining_day` is 0, warn the user about rate limits.
- If an account has `"is_authenticated": false`, note that the account needs re-authentication.

## Output Formatting

- Always present data in markdown tables for readability.
- Include currency values formatted to 2 decimal places.
- When showing percentages (conversion rates, deltas), format as `XX.X%`.
- For multi-model summaries, include a **Total** row at the bottom.
