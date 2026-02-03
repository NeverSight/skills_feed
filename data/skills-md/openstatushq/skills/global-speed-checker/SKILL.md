---
name: global-speed-checker
version: 0.3.0
description: Run global performance checks on HTTP endpoints from multiple regions worldwide. Use when users want to check speed, latency, performance, or test endpoints globally.
---

# Global Speed Checker

Check HTTP endpoint performance from 28 regions worldwide.

## When to Use

- "check the speed of https://openstatus.dev"
- "test https://openstatus.dev globally"
- "how fast is my API from different regions"

## Workflow

### 1. Parse Request

Extract from user's message:
- **URL** (required)
- **Method** (optional, default: GET)
- **Headers** (optional)
- **Body** (optional)

### 2. Make API Call

```bash
curl -s -L -X POST "https://openstatus.dev/play/checker/api?compact=true" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","method":"GET"}'
```

The response contains newline-delimited JSON. Each line is a region result. Final line is the check ID.

**Note**: The `compact=true` parameter reduces response size by removing headers/body and returning calculated timing phases.

### 3. Process and Display Results

Parse the response (newline-delimited JSON) and create a markdown table sorted by latency (fastest first):
- **Columns**: Region | Latency | Status | DNS | Connection | TLS | TTFB | Transfer
- **Region**: Map code to name using the Read tool to load [references/regions-detailed.md](references/regions-detailed.md) (e.g., `fra` → "Frankfurt (Fly) 🇩🇪")
- **Timing phases**: In compact mode, timing phases are pre-calculated in the response (dns, connection, tls, ttfb, transfer). Otherwise, calculate from raw `timing` object (e.g., DNS = `dnsDone - dnsStart`)
- **Sorting**: Sort the parsed results array by latency value before rendering the table

### 4. Add Summary

```markdown
**Fastest**: [region] ([latency]) • **Slowest**: [region] ([latency]) • **Average**: [avg]ms • **Success rate**: [x/y] ([%])

[View and share results](https://openstatus.dev/play/checker/[check-id])
```

Then ask: `Would you like to see detailed insights or structured JSON data?`

### 5. Optional: Insights (if requested)

Analyze results (3-5 observations):
- Status codes, regional gaps, TLS/TTFB/DNS performance
- See [references/insights-generation-guide.md](references/insights-generation-guide.md)

### 6. Optional: JSON Export (if requested)

Provide complete results as structured JSON.

## Region Mapping

Common codes:
- `fra` → Frankfurt (Fly) 🇩🇪
- `iad` → Virginia (Fly) 🇺🇸
- `sin` → Singapore (Fly) 🇸🇬
- `lhr` → London (Fly) 🇬🇧
- `koyeb_fra` → Frankfurt (Koyeb) 🇩🇪
- `railway_us-west2` → California (Railway) 🇺🇸

Full list: [references/regions-detailed.md](references/regions-detailed.md)

## Error Handling

**Rate Limit (429)**: Show limit, remaining, reset time

**Invalid Request (400)**: Show error message and details from response

**No Client IP (400)**: Explain VPN/proxy may cause this

## Reference Files

- [regions-detailed.md](references/regions-detailed.md) - Complete region mapping
- [timing-phases.md](references/timing-phases.md) - Timing explanations and optimization
- [insights-generation-guide.md](references/insights-generation-guide.md) - Insight patterns
- [performance-benchmarks.md](references/performance-benchmarks.md) - Expected performance ranges
- [common-issues.md](references/common-issues.md) - Troubleshooting guide

## Notes

- Tests from 28 regions (Fly.io, Koyeb, Railway)
- Takes ~2-5 seconds
- Rate limit: 5 requests per 60 seconds
- Results cached for 7 days
