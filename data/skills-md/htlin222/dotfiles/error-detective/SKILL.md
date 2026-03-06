---
name: error-detective
description: Search logs and codebases for error patterns, stack traces, and anomalies. Use when debugging issues, analyzing logs, or investigating production errors.
---

# Error Detection

Find and analyze errors across logs and code.

## When to use

- Investigating production errors
- Analyzing log patterns
- Finding error root causes
- Correlating errors across systems

## Log analysis

### Find errors

```bash
# Recent errors
grep -i "error\|exception\|fatal" /var/log/app.log | tail -100

# Errors with context
grep -B 5 -A 10 "ERROR" /var/log/app.log

# Count by error type
grep -oE "Error: [^:]*" app.log | sort | uniq -c | sort -rn

# Errors in time range
awk '/2024-01-15 14:/ && /ERROR/' app.log
```

### Pattern detection

```bash
# Find repeated errors
grep "ERROR" app.log | cut -d']' -f2 | sort | uniq -c | sort -rn | head -20

# Correlate request IDs
grep "req-12345" *.log | sort -t' ' -k1,2

# Find error spikes
grep "ERROR" app.log | cut -d' ' -f1-2 | uniq -c | sort -rn
```

## Stack trace analysis

### Parse stack traces

```python
import re

def parse_stack_trace(log_content: str) -> list[dict]:
    pattern = r'(?P<exception>\w+Error|\w+Exception): (?P<message>.*?)\n(?P<trace>(?:\s+at .+\n)+)'

    traces = []
    for match in re.finditer(pattern, log_content):
        traces.append({
            'type': match.group('exception'),
            'message': match.group('message'),
            'trace': match.group('trace').strip().split('\n')
        })
    return traces
```

### Common patterns

| Pattern            | Indicates          | Action                   |
| ------------------ | ------------------ | ------------------------ |
| NullPointer        | Missing null check | Add validation           |
| Timeout            | Slow dependency    | Add timeout, retry       |
| Connection refused | Service down       | Check health, retry      |
| OOM                | Memory leak        | Profile, increase limits |
| Rate limit         | Too many requests  | Add backoff, queue       |

## Investigation checklist

1. **Capture** - Get full error message and stack trace
2. **Timestamp** - When did it start?
3. **Frequency** - How often? Increasing?
4. **Scope** - All users or specific?
5. **Changes** - Recent deployments?
6. **Dependencies** - External services affected?

## Correlation queries

```sql
-- Errors by endpoint
SELECT endpoint, count(*) as errors
FROM logs
WHERE level = 'ERROR' AND time > NOW() - INTERVAL '1 hour'
GROUP BY endpoint ORDER BY errors DESC;

-- Error rate over time
SELECT
  date_trunc('minute', time) as minute,
  count(*) filter (where level = 'ERROR') as errors,
  count(*) as total
FROM logs
WHERE time > NOW() - INTERVAL '1 hour'
GROUP BY minute ORDER BY minute;
```

## Examples

**Input:** "Find why API is returning 500 errors"
**Action:** Search logs for 500 status, find stack traces, identify root cause

**Input:** "Analyze error patterns from last hour"
**Action:** Aggregate errors by type, find spikes, correlate with events
