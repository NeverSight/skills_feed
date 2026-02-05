---
name: sling-hooks
description: >
  Pre/post actions and hooks for Sling replications and pipelines.
  Use when adding actions before/after replications, executing SQL queries, sending HTTP webhooks, validating data with checks, running shell commands, copying/deleting files, or implementing notifications.
---

# Hooks and Steps Reference

Hooks are custom actions that execute at specific points in replications. Steps are the same concept used in pipelines.

## Hook Locations (Replications)

| Location | When | Use Case |
|----------|------|----------|
| `start` | Before any stream runs | Setup, notifications |
| `end` | After all streams complete | Cleanup, notifications |
| `pre` | Before each stream | Validation, setup |
| `post` | After each stream | Logging, notifications |
| `pre_merge` | Before merge (in transaction) | Session settings |
| `post_merge` | After merge (in transaction) | Additional SQL |

## Configuration

### Replication-Level Hooks
```yaml
hooks:
  start:
    - type: log
      message: "Starting replication"
  end:
    - type: check
      check: execution.status.error == 0

defaults:
  ...
streams:
  ...
```

### Stream-Level Hooks
```yaml
streams:
  my_table:
    hooks:
      pre:
        - type: query
          connection: source
          query: "SELECT 1"
      post:
        - type: http
          url: "https://webhook.example.com"
```

## Common Properties

| Property | Description |
|----------|-------------|
| `type` | Hook type (required) |
| `id` | Identifier for referencing output |
| `if` | Conditional execution |
| `on_failure` | abort, warn, quiet, skip, break |

## Hook Types

### log
```yaml
- type: log
  level: info  # debug, info, warn, error
  message: "Processed {run.total_rows} rows"
```

### query
```yaml
- type: query
  connection: MY_DB
  query: |
    UPDATE status SET last_run = NOW()
    WHERE table_name = '{stream.table}'
  into: result  # Optional: store result
  id: update_status
```

### http
```yaml
- type: http
  url: "https://api.example.com/webhook"
  method: POST
  headers:
    Authorization: "Bearer {env.API_TOKEN}"
    Content-Type: "application/json"
  payload: |
    {
      "table": "{stream.table}",
      "rows": {run.total_rows},
      "status": "{run.status}"
    }
  into: response
```

### check
```yaml
- type: check
  check: "run.total_rows > 0"
  failure_message: "No rows processed"
  on_failure: abort
  vars:
    threshold: 100
```

### command
```yaml
- type: command
  command: "python validate.py {object.table}"
  working_dir: "/scripts"
  print: true
  into: output
```

### copy
```yaml
- type: copy
  from: "file://data/source.csv"
  to: "s3://bucket/archive/{YYYY}/{MM}/"
  recursive: true
```

### delete
```yaml
- type: delete
  location: "s3://bucket/temp/"
  recursive: true
```

### write
```yaml
- type: write
  to: "file://logs/run_{timestamp.file_name}.txt"
  content: |
    Run completed at {timestamp.datetime}
    Rows: {run.total_rows}
    Status: {run.status}
```

### read
```yaml
- type: read
  from: "file://config/settings.json"
  into: settings
```

### list
```yaml
- type: list
  location: "s3://bucket/data/"
  recursive: false
  only: files  # files or folders
  id: file_list
```

### store
```yaml
- type: store
  key: my_value
  value: "{run.total_rows}"
```

### replication
```yaml
- type: replication
  path: /path/to/other_replication.yaml
  select_streams: ["table1"]
  mode: incremental
```

### group
```yaml
- type: group
  loop: ["users", "orders", "products"]
  steps:
    - type: log
      message: "Processing {loop.value}"
    - type: query
      connection: DB
      query: "ANALYZE {loop.value}"
```

## Variables

Variables use `{variable.path}` syntax within hook properties.

### Debug: Print All Variables
```yaml
- type: log
  message: '{runtime_state}'  # Prints all available variables as JSON
```

### Variable Scopes

| Scope | Description | Example |
|-------|-------------|---------|
| `env.*` | Environment variables | `{env.API_TOKEN}` |
| `store.*` | Values from `store` hooks | `{store.my_key}` |
| `state.*` | Hook outputs by ID | `{state.my_query.result[0].id}` |
| `timestamp.*` | Date/time parts | `{timestamp.YYYY}-{timestamp.MM}` |
| `execution.*` | Replication-level info | `{execution.total_rows}` |
| `source.*` | Source connection | `{source.name}`, `{source.type}` |
| `target.*` | Target connection | `{target.database}` |
| `stream.*` | Current stream | `{stream.table}`, `{stream.file_name}` |
| `object.*` | Target object | `{object.full_name}` |
| `run.*` | Current run | `{run.total_rows}`, `{run.status}` |
| `runs.*` | All runs by ID | `{runs.my_stream.status}` |

### Commonly Used Variables

```yaml
# Timestamps
timestamp.date              # "2025-01-19"
timestamp.datetime          # "2025-01-19 08:27:31"
timestamp.YYYY / MM / DD    # Year, month, day parts
timestamp.file_name         # "2025_01_19_082731" (safe for filenames)
timestamp.unix              # 1737286051

# Run metrics
run.total_rows              # Rows processed
run.total_bytes             # Bytes processed
run.status                  # "success" or "error"
run.duration                # Seconds

# Execution totals
execution.total_rows        # All rows across streams
execution.status.error      # Count of failed streams
execution.status.success    # Count of successful streams

# Stream/Object names
stream.table / stream.schema      # Source table info
object.table / object.full_name   # Target table info
```

## Error Handling

### on_failure Options

| Option | Behavior |
|--------|----------|
| `abort` | Stop immediately (default) |
| `warn` | Log warning, continue |
| `quiet` | Silent, continue |
| `skip` | Skip this hook, continue |
| `break` | Exit current group/hook sequence |

### Check Pattern
```yaml
hooks:
  end:
    # Stop if any errors
    - type: check
      check: execution.status.error == 0
      on_failure: break

    # Only run if check passed
    - type: http
      url: "https://webhook.example.com"
      payload: '{"status": "success"}'
```

## Complete Example

```yaml
hooks:
  start:
    - type: log
      message: "Starting replication at {timestamp.datetime}"

    - type: query
      connection: '{source.name}'
      query: "SELECT MAX(updated_at) as max_date FROM audit"
      into: audit_check
      id: pre_check

  end:
    - type: check
      check: execution.status.error == 0
      on_failure: break

    - type: http
      url: "{env.SLACK_WEBHOOK}"
      method: POST
      payload: |
        {
          "text": "Replicated {execution.total_rows} rows"
        }

defaults:
  hooks:
    pre:
      - type: log
        message: "Starting {stream.table}"

    post:
      - type: log
        message: "{stream.table}: {run.total_rows} rows in {run.duration}s"

streams:
  public.users:
    hooks:
      post:
        - type: query
          connection: '{target.name}'
          query: "ANALYZE {object.full_name}"
```

## Full Documentation

See https://docs.slingdata.io/concepts/hooks.md for complete reference.
