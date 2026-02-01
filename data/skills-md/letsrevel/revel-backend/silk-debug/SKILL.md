---
name: silk-debug
description: Analyze Django Silk profiling data to debug slow requests, detect N+1 queries, and optimize database performance. Use when analyzing request IDs, investigating slow endpoints, or optimizing query performance.
allowed-tools: Bash(python:*), Bash(.venv/bin/python:*), Read, Grep
---

# Silk Debug Tool

A CLI tool for analyzing Django Silk profiling data to debug slow requests, detect N+1 queries, and optimize database performance.

## Tool Location

```bash
.venv/bin/python scripts/silk_debug.py
```

## Quick Reference

### Analyze a Specific Request

When given a Silk request ID (UUID), use `--full` for comprehensive analysis:

```bash
.venv/bin/python scripts/silk_debug.py <request_id> --full
```

This shows:
- Request info (path, method, status, time, query count)
- Duplicate/similar queries (N+1 detection)
- Slow queries (>5ms by default)
- Queries grouped by table
- Query execution timeline
- Python cProfile data (if enabled)

### List and Filter Requests

```bash
# List recent requests
.venv/bin/python scripts/silk_debug.py --list

# Sort by different criteria
.venv/bin/python scripts/silk_debug.py --list --sort queries     # Most queries
.venv/bin/python scripts/silk_debug.py --list --sort duration    # Slowest total time
.venv/bin/python scripts/silk_debug.py --list --sort db_time     # Most DB time

# Filter requests
.venv/bin/python scripts/silk_debug.py --list --path /api/events --min-queries 20
.venv/bin/python scripts/silk_debug.py --list --method POST --min-time 100
```

### Aggregate Analysis

```bash
# Overall statistics
.venv/bin/python scripts/silk_debug.py --stats

# Endpoint summary (grouped by path pattern, shows P95)
.venv/bin/python scripts/silk_debug.py --endpoints

# Find slow endpoints
.venv/bin/python scripts/silk_debug.py --slow-endpoints --slow-endpoint-threshold 100
```

## Interpreting Results

### N+1 Query Detection

When you see duplicate queries like:
```
🔴 15x similar queries:
SELECT "events_ticket"."id" FROM "events_ticket" WHERE "events_ticket"."event_id" = '<UUID>'
```

This indicates an N+1 problem. Fix with:
- `select_related()` for ForeignKey fields
- `prefetch_related()` for reverse relations or M2M fields

### Slow Queries

Common causes of slow queries:
1. **COUNT on complex DISTINCT**: Pagination wrapping complex visibility subqueries
   - Fix: Materialize IDs in Python first, then filter with simple `IN` clause
2. **Missing indexes**: Full table scans
   - Fix: Add database indexes on filtered/joined columns
3. **Complex JOINs**: Multiple related tables
   - Fix: Optimize query structure or denormalize if appropriate

### Timeline Analysis

The timeline shows query execution order with visual bars:
```
  1. +    0.0ms [  2.5ms] █ "accounts_reveluser"
  7. +   60.2ms [  2.8ms] █ "__count"
```

Look for:
- Large gaps between queries (indicates Python processing time)
- Queries that could run in parallel but are sequential
- Expensive queries that block subsequent operations

## Common Optimization Patterns

### Expensive COUNT with DISTINCT

When you see:
```sql
SELECT COUNT(*) FROM (SELECT DISTINCT ... complex subquery ...)
```

Fix by materializing IDs:
```python
# Before (slow COUNT)
qs = Event.objects.for_user(user).filter(...).distinct()

# After (fast COUNT)
event_ids = list(Event.objects.for_user(user).values_list("id", flat=True).distinct())
qs = Event.objects.full().filter(id__in=event_ids)
```

### Redundant Visibility Checks

When the same `for_user()` query appears multiple times:
- Create a method that accepts already-checked objects
- Cache visibility results within the request

### Batch Operations

When creating multiple objects:
- Use `bulk_create()` instead of individual `.save()` calls
- Fetch shared data (settings, related objects) once before the loop
- Send notifications in batches, not per-item

## CLI Options Reference

### Single Request Analysis
- `--full, -f`: Run all analyses
- `--duplicates, -d`: Show N+1 candidates
- `--slow, -s`: Show slow queries
- `--slow-threshold N`: Slow query threshold in ms (default: 5)
- `--tables, -t`: Group queries by table
- `--timeline`: Show execution timeline
- `--traceback, -tb`: Show code locations for duplicates
- `--profile, -prof`: Show Python cProfile data

### Listing and Filtering
- `--list, -l`: List requests
- `--limit N`: Number of results (default: 20)
- `--sort {recent,queries,duration,db_time}`: Sort order
- `--path, -p`: Filter by path (contains)
- `--method, -m`: Filter by HTTP method
- `--status`: Filter by status code
- `--min-queries N`: Minimum query count
- `--min-time N`: Minimum response time (ms)
- `--min-db-time N`: Minimum DB time (ms)

### Aggregate Views
- `--stats`: Show aggregate statistics
- `--endpoints`: Show endpoint summary with P95
- `--slow-endpoints`: Group slow requests by endpoint
- `--slow-endpoint-threshold N`: Threshold in ms (default: 200)
- `--min-count N`: Minimum requests for endpoint summary
