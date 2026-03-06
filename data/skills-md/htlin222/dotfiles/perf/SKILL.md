---
name: perf
description: Profile applications, optimize bottlenecks, and implement caching. Use for performance issues or optimization tasks.
---

# Performance Engineering

Profile, analyze, and optimize application performance.

## When to Use

- Application is slow or unresponsive
- User reports performance issues
- Before scaling infrastructure
- Optimizing critical paths
- Setting up monitoring

## Optimization Process

1. **Measure** - Profile before optimizing
2. **Identify** - Find the biggest bottlenecks
3. **Optimize** - Fix highest-impact issues first
4. **Verify** - Confirm improvements with metrics

## Profiling Commands

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Python profiling
python -m cProfile -o output.prof script.py
python -m pstats output.prof

# Go profiling
go tool pprof http://localhost:6060/debug/pprof/profile
```

## Common Bottlenecks

### Database

- Missing indexes (add indexes on WHERE/JOIN columns)
- N+1 queries (use eager loading)
- Large result sets (add pagination)

### Memory

- Memory leaks (check event listeners, closures)
- Large objects (stream instead of buffer)
- Cache without TTL (add expiration)

### CPU

- Synchronous operations (make async)
- Complex algorithms (optimize or cache)
- Unnecessary computation (memoize)

### Network

- Too many requests (batch/combine)
- Large payloads (compress, paginate)
- No caching (add CDN, browser cache)

## Performance Budgets

| Metric         | Target |
| -------------- | ------ |
| Load Time (3G) | <3s    |
| Load Time (4G) | <1s    |
| API Response   | <200ms |
| Bundle Size    | <500KB |
| LCP            | <2.5s  |
| FID            | <100ms |
| CLS            | <0.1   |

## Output Format

```markdown
## Performance Report

**Before:** [baseline metrics]
**After:** [improved metrics]
**Improvement:** [percentage]

### Bottlenecks Identified

1. [Issue] - Impact: High/Medium/Low

### Optimizations Applied

1. [Change] → [Result]
```

## Examples

**Input:** "The API is slow"
**Action:** Profile endpoints, identify slow queries, optimize, verify improvement

**Input:** "Page load is taking too long"
**Action:** Analyze bundle, check network, optimize critical path, add caching
