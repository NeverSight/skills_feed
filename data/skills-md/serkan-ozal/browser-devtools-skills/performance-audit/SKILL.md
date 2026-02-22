---
name: performance-audit
description: Analyze web and backend performance using Web Vitals, network timing, and Node.js metrics. Use when the user asks about page performance, load times, Core Web Vitals (LCP, CLS, INP), slow pages, backend bottlenecks, or SEO performance factors.
allowed-tools: Bash(browser-devtools-cli:*), Bash(node-devtools-cli:*)
---

# Performance Audit Skill

Analyze web page performance using Web Vitals and network timing metrics.

## When to Use

This skill activates when:
- User asks about page performance or speed
- User wants to optimize load times
- User mentions slow page, slow API, or poor user experience
- User needs Core Web Vitals metrics
- User asks about backend bottlenecks or TTFB
- User asks about SEO performance factors

## Capabilities

### Web Vitals Analysis
```bash
browser-devtools-cli o11y get-web-vitals
browser-devtools-cli --json o11y get-web-vitals
browser-devtools-cli --json o11y get-web-vitals --wait-ms 3000
browser-devtools-cli --json o11y get-web-vitals --include-debug
```

### Network Performance
```bash
browser-devtools-cli --json o11y get-http-requests
browser-devtools-cli --json o11y get-http-requests --resource-type script,stylesheet
browser-devtools-cli --json o11y get-http-requests --status-min 400
```

### Visual Analysis
```bash
browser-devtools-cli content take-screenshot --name "above-fold"
browser-devtools-cli content take-screenshot --name "full-page" --full-page
```

### JavaScript Execution Analysis
```bash
browser-devtools-cli run js-in-browser --script "performance.getEntriesByType('longtask')"
browser-devtools-cli run js-in-browser --script "performance.getEntriesByType('resource')"
```

## Performance Thresholds

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP | ≤2.5s | 2.5-4s | >4s |
| INP | ≤200ms | 200-500ms | >500ms |
| CLS | ≤0.1 | 0.1-0.25 | >0.25 |
| TTFB | ≤800ms | 800-1800ms | >1800ms |
| FCP | ≤1.8s | 1.8-3s | >3s |

## Audit Workflow

```bash
SESSION="--session-id perf-audit"

# 1. Navigate to page
browser-devtools-cli $SESSION navigation go-to --url "https://example.com"

# 2. Wait for page to settle
browser-devtools-cli $SESSION sync wait-for-network-idle

# 3. Get Web Vitals
browser-devtools-cli $SESSION --json o11y get-web-vitals --wait-ms 2000

# 4. Analyze network requests
browser-devtools-cli $SESSION --json o11y get-http-requests

# 5. Check for console errors
browser-devtools-cli $SESSION --json o11y get-console-messages --types error,warn

# 6. Take screenshot for reference
browser-devtools-cli $SESSION content take-screenshot --name "performance-audit"

# 7. Cleanup
browser-devtools-cli session delete perf-audit
```

## Detailed Analysis

### Check Large Resources
```bash
browser-devtools-cli --json o11y get-http-requests --resource-type image,script,stylesheet
```

### Check Slow Requests
```bash
browser-devtools-cli --json o11y get-http-requests
# Look for requests with high timing values
```

### Check Render-Blocking Resources
```bash
browser-devtools-cli run js-in-browser --script "
  performance.getEntriesByType('resource')
    .filter(r => r.renderBlockingStatus === 'blocking')
    .map(r => ({name: r.name, duration: r.duration}))
"
```

### Check Long Tasks
```bash
browser-devtools-cli run js-in-browser --script "
  performance.getEntriesByType('longtask')
    .map(t => ({startTime: t.startTime, duration: t.duration}))
"
```

## Backend Performance (node-devtools-cli)

When TTFB or API latency suggests backend bottlenecks, inspect the Node.js process:

```bash
# Connect to API/server process
node-devtools-cli --session-id perf debug connect --pid 12345

# Check memory and CPU
node-devtools-cli --session-id perf run js-in-node --script "process.memoryUsage()"
node-devtools-cli --session-id perf run js-in-node --script "require('os').loadavg()"

# Tracepoint on slow handler to capture call context
node-devtools-cli --session-id perf debug put-tracepoint \
  --url-pattern "routes/heavy.ts" \
  --line-number 30
```

## Common Issues

- Large unoptimized images
- Render-blocking CSS/JS
- Too many HTTP requests
- Slow server response (TTFB)
- Layout shifts from dynamic content
- Uncompressed resources
- Missing caching headers
- Third-party scripts blocking main thread

## Best Practices

1. **Run multiple times** for consistent results
2. **Wait for network idle** before measuring
3. **Use --wait-ms** for LCP/CLS to settle
4. **Check network requests** for slow/large resources
5. **Take screenshots** at different load stages
6. **Test on different network conditions** (throttle if needed)
7. **Compare before/after** for optimization validation
