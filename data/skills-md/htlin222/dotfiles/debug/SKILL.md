---
name: debug
description: Debug errors, test failures, and unexpected behavior with log analysis and correlation. Use when encountering issues, error messages, analyzing logs, or investigating production errors.
---

# Debug

Systematic debugging for errors, test failures, unexpected behavior, and production issues.

## Usage

```
/debug [issue] [--logs] [--correlate] [--trace] [--type bug|build|perf|deploy]
```

## Options

| Flag          | Purpose                                                      |
| ------------- | ------------------------------------------------------------ |
| `--logs`      | Enable log pattern analysis (error spikes, frequency, types) |
| `--correlate` | Run SQL correlation queries on structured logs               |
| `--trace`     | Deep stack trace analysis with context                       |
| `--type`      | Issue category: bug, build, perf(ormance), deploy(ment)      |

## When to Use

- Error messages or stack traces appear
- Tests are failing
- Code behaves unexpectedly
- User says "it's broken" or "not working"
- Production errors need investigation (`--logs`)
- Need to correlate errors across systems (`--correlate`)
- Deep stack analysis required (`--trace`)

## Debugging Process

1. **Capture** - Get error message, stack trace, and reproduction steps
2. **Isolate** - Narrow down the failure location
3. **Hypothesize** - Form theories about the cause
4. **Test** - Validate hypotheses with evidence
5. **Fix** - Implement minimal fix
6. **Verify** - Confirm solution works

## Investigation Steps

```bash
# Check recent changes that might have caused the issue
git log --oneline -10
git diff HEAD~3

# Find error patterns in logs
grep -r "error\|Error\|ERROR" logs/ 2>/dev/null | tail -20

# Check test output
npm test 2>&1 | tail -50  # or pytest, cargo test, etc.
```

## Log Analysis (`--logs`)

### Find Errors

```bash
# Recent errors with context
grep -B 5 -A 10 "ERROR" /var/log/app.log

# Count by error type
grep -oE "Error: [^:]*" app.log | sort | uniq -c | sort -rn

# Errors in time range
awk '/2024-01-15 14:/ && /ERROR/' app.log

# Find repeated errors
grep "ERROR" app.log | cut -d']' -f2 | sort | uniq -c | sort -rn | head -20

# Find error spikes
grep "ERROR" app.log | cut -d' ' -f1-2 | uniq -c | sort -rn
```

### Common Patterns

| Pattern            | Indicates          | Action                   |
| ------------------ | ------------------ | ------------------------ |
| NullPointer        | Missing null check | Add validation           |
| Timeout            | Slow dependency    | Add timeout, retry       |
| Connection refused | Service down       | Check health, retry      |
| OOM                | Memory leak        | Profile, increase limits |
| Rate limit         | Too many requests  | Add backoff, queue       |

## Correlation Queries (`--correlate`)

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

-- Correlate request IDs across services
SELECT service, message, time
FROM logs
WHERE request_id = 'req-12345'
ORDER BY time;
```

## Stack Trace Analysis (`--trace`)

### Parse Stack Traces

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

## Investigation Checklist

1. **Capture** - Get full error message and stack trace
2. **Timestamp** - When did it start?
3. **Frequency** - How often? Increasing?
4. **Scope** - All users or specific?
5. **Changes** - Recent deployments?
6. **Dependencies** - External services affected?

## Output Format

```markdown
## Debug Report

**Issue:** [Brief description]
**Root Cause:** [What's actually wrong]

### Evidence

- [Finding 1]
- [Finding 2]

### Fix

[Code or configuration change]

### Verification

[How to confirm the fix works]

### Prevention

[How to prevent this in the future]
```

## Examples

**Input:** "TypeError: Cannot read property 'map' of undefined"
**Action:** Trace the undefined value, find where data should be initialized, fix the source

**Input:** "Tests are failing"
**Action:** Run tests, capture failures, analyze each failure, fix underlying issues

**Input:** `/debug --logs "API returning 500 errors"`
**Action:** Search logs for 500 status, find stack traces, identify root cause, check error frequency

**Input:** `/debug --correlate "intermittent failures"`
**Action:** Run correlation queries to find patterns, identify affected endpoints, correlate with events
