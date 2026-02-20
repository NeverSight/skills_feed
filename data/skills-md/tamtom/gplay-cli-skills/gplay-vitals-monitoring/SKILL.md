---
name: gplay-vitals-monitoring
description: App vitals monitoring for crashes, ANRs, performance metrics, and errors via gplay vitals commands. Use when asked to check app stability, crash rates, ANR rates, or performance data from Google Play Console.
---

# App Vitals Monitoring

Use this skill when you need to monitor app stability, performance, and errors from Google Play Console.

## Preconditions
- Ensure credentials are set (`gplay auth login` or `GPLAY_SERVICE_ACCOUNT` env var).
- Service account needs "View app information and download bulk reports" permission.
- App must have active installs generating vitals data.

## Crash Monitoring

### List crash clusters
```bash
gplay vitals crashes list \
  --package com.example.app
```

### Get crash cluster details
```bash
gplay vitals crashes get \
  --package com.example.app \
  --cluster-id CLUSTER_ID
```

### Filter by time range
```bash
gplay vitals crashes list \
  --package com.example.app \
  --start-time 2026-01-01T00:00:00Z \
  --end-time 2026-02-01T00:00:00Z
```

### Filter by version code
```bash
gplay vitals crashes list \
  --package com.example.app \
  --version-code 42
```

### Filter by app version name
```bash
gplay vitals crashes list \
  --package com.example.app \
  --version-name "1.2.0"
```

### Paginate through all crash clusters
```bash
gplay vitals crashes list \
  --package com.example.app \
  --paginate
```

### Output as table for readability
```bash
gplay vitals crashes list \
  --package com.example.app \
  --output table
```

## ANR Monitoring

### List ANR clusters
```bash
gplay vitals crashes list \
  --package com.example.app \
  --type anr
```

### Get ANR cluster details
```bash
gplay vitals crashes get \
  --package com.example.app \
  --cluster-id CLUSTER_ID \
  --type anr
```

## Performance Metrics

### Get performance overview
```bash
gplay vitals performance overview \
  --package com.example.app
```

### Startup time metrics
```bash
gplay vitals performance startup \
  --package com.example.app
```

### Filter by device type
```bash
gplay vitals performance overview \
  --package com.example.app \
  --device-type phone
```

### Filter by OS version
```bash
gplay vitals performance overview \
  --package com.example.app \
  --os-version 14
```

### Rendering metrics (slow/frozen frames)
```bash
gplay vitals performance rendering \
  --package com.example.app
```

### Battery metrics
```bash
gplay vitals performance battery \
  --package com.example.app
```

### Permission denials
```bash
gplay vitals performance permissions \
  --package com.example.app
```

## Error Reporting

### List error clusters
```bash
gplay vitals errors list \
  --package com.example.app
```

### Get error details
```bash
gplay vitals errors get \
  --package com.example.app \
  --error-id ERROR_ID
```

### Filter errors by severity
```bash
gplay vitals errors list \
  --package com.example.app \
  --severity critical
```

### Filter errors by time range
```bash
gplay vitals errors list \
  --package com.example.app \
  --start-time 2026-01-01T00:00:00Z \
  --end-time 2026-02-01T00:00:00Z
```

## Common Flags

| Flag | Description |
|------|-------------|
| `--package` | App package name (required) |
| `--start-time` | Start of time range (RFC 3339) |
| `--end-time` | End of time range (RFC 3339) |
| `--version-code` | Filter by version code |
| `--version-name` | Filter by version name |
| `--type` | Event type (`crash`, `anr`) |
| `--output` | Output format (`json`, `table`, `markdown`) |
| `--paginate` | Fetch all pages |
| `--pretty` | Pretty-print JSON output |

## Workflow Examples

### Daily stability check
```bash
# Check crash rate for the latest version
gplay vitals crashes list \
  --package com.example.app \
  --version-name "2.1.0" \
  --output table

# Check ANR rate
gplay vitals crashes list \
  --package com.example.app \
  --version-name "2.1.0" \
  --type anr \
  --output table

# Review performance
gplay vitals performance overview \
  --package com.example.app \
  --output table
```

### Investigate a crash spike
```bash
# 1. List top crash clusters
gplay vitals crashes list \
  --package com.example.app \
  --start-time 2026-02-10T00:00:00Z \
  --output table

# 2. Get details for the top cluster
CLUSTER=$(gplay vitals crashes list \
  --package com.example.app \
  --start-time 2026-02-10T00:00:00Z | jq -r '.[0].clusterId')

gplay vitals crashes get \
  --package com.example.app \
  --cluster-id $CLUSTER \
  --pretty

# 3. Check if it's version-specific
gplay vitals crashes list \
  --package com.example.app \
  --version-code 105 \
  --output table
```

### CI/CD stability gate
```bash
# Check if crash rate exceeds threshold before promoting
CRASH_COUNT=$(gplay vitals crashes list \
  --package com.example.app \
  --version-name "$VERSION" | jq 'length')

if [ "$CRASH_COUNT" -gt 10 ]; then
  echo "Too many crash clusters ($CRASH_COUNT). Halting promotion."
  exit 1
fi

gplay promote \
  --package com.example.app \
  --from beta \
  --to production \
  --rollout 10
```

## Best Practices

1. **Monitor after every release** - Check vitals within 24-48 hours of rollout.
2. **Upload deobfuscation files** - Ensure crash stack traces are readable.
3. **Set up CI stability gates** - Block promotion when crash rates exceed thresholds.
4. **Track ANRs separately** - ANRs impact Play Store ranking more than crashes.
5. **Compare across versions** - Filter by version code to detect regressions.
6. **Use JSON output in scripts** - Parse with `jq` for automated monitoring.
