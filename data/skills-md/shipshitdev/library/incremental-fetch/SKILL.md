---
name: incremental-fetch
description: "Build resilient data ingestion pipelines from APIs. Use when creating scripts that fetch paginated data from external APIs (Twitter, exchanges, any REST API) and need to track progress, avoid duplicates, handle rate limits, and support both incremental updates and historical backfills. Triggers: 'ingest data from API', 'pull tweets', 'fetch historical data', 'sync from X', 'build a data pipeline', 'fetch without re-downloading', 'resume the download', 'backfill older data'. NOT for: simple one-shot API calls, websocket/streaming connections, file downloads, or APIs without pagination."
---

# Incremental Fetch

Build data pipelines that never lose progress and never re-fetch existing data.

## The Two Watermarks Pattern

Track TWO cursors to support both forward and backward fetching:

| Watermark | Purpose | API Parameter |
|-----------|---------|---------------|
| `newest_id` | Fetch new data since last run | `since_id` |
| `oldest_id` | Backfill older data | `until_id` |

A single watermark only fetches forward. Two watermarks enable:

- Regular runs: fetch NEW data (since `newest_id`)
- Backfill runs: fetch OLD data (until `oldest_id`)
- No overlap, no gaps

## Critical: Data vs Watermark Saving

These are different operations with different timing:

| What | When to Save | Why |
|------|--------------|-----|
| **Data records** | After EACH page | Resilience: interrupted on page 47? Keep 46 pages |
| **Watermarks** | ONCE at end of run | Correctness: only commit progress after full success |

```
fetch page 1 → save records → fetch page 2 → save records → ... → update watermarks
```

## Workflow Decision Tree

```
First run (no watermarks)?
├── YES → Full fetch (no since_id, no until_id)
└── NO → Backfill flag set?
    ├── YES → Backfill mode (until_id = oldest_id)
    └── NO → Update mode (since_id = newest_id)
```

## Implementation Checklist

1. **Database**: Create ingestion_state table (see patterns.md)
2. **Fetch loop**: Insert records immediately after each API page
3. **Watermark tracking**: Track newest/oldest IDs seen in this run
4. **Watermark update**: Save watermarks ONCE at end of successful run
5. **Retry**: Exponential backoff with jitter
6. **Rate limits**: Wait for reset or skip and record for next run

## Pagination Types

This pattern works best with **ID-based pagination** (numeric IDs that can be compared). For other pagination types:

| Type | Adaptation |
|------|------------|
| **Cursor/token** | Store cursor string instead of ID; can't compare numerically |
| **Timestamp** | Use `last_timestamp` column; compare as dates |
| **Offset/limit** | Store page number; resume from last saved page |

See [references/patterns.md](references/patterns.md) for schemas and code examples.
