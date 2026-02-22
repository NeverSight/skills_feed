---
name: kestra
description: |
  Generate, debug, and optimize Kestra workflow orchestration YAML files. Kestra is an open-source, declarative data orchestration platform using YAML syntax.
  
  Use this skill when:
  - Creating new Kestra flows (workflows)
  - Debugging or fixing existing Kestra YAML
  - Adding triggers (schedule, webhook, flow-based)
  - Implementing error handling, retries, or timeouts
  - Writing script tasks (Python, Shell, Node.js, etc.)
  - Building parallel or conditional workflows
  - Converting from Airflow/Prefect to Kestra
  - Any question about Kestra syntax, plugins, or best practices
---

# Kestra Workflow Generator

Kestra uses declarative YAML to define workflows. Every flow requires `id`, `namespace`, and `tasks`.

## Core YAML Structure

```yaml
id: flow-name              # Required: unique within namespace, lowercase with hyphens
namespace: company.team    # Required: dot-separated hierarchy
description: |             # Optional: supports Markdown
  Flow description
labels:                    # Optional: key-value pairs for organization
  env: prod
  team: data-engineering
inputs:                    # Optional: typed parameters
  - id: my_input
    type: STRING
    required: false
    defaults: "default value"
variables:                 # Optional: reusable values
  base_url: "https://api.example.com"
tasks:                     # Required: list of tasks to execute
  - id: task-name
    type: io.kestra.plugin...
triggers:                  # Optional: automatic execution
  - id: schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"
errors:                    # Optional: error handling tasks
  - id: notify
    type: io.kestra.plugin.core.log.Log
    message: "Flow failed!"
```

## Task Generation Workflow

1. Identify the task type needed (script, HTTP, flowable, etc.)
2. Use fully qualified plugin type: `io.kestra.plugin.[category].[TaskName]`
3. Include all required properties for the task type
4. Use Pebble templating for dynamic values: `{{ inputs.name }}`, `{{ outputs.taskId.property }}`

## Input Types

| Type | Description | Example |
|------|-------------|---------|
| STRING | Text value | `defaults: "hello"` |
| INT | Integer | `defaults: 42` |
| FLOAT | Decimal | `defaults: 3.14` |
| BOOLEAN | True/false | `defaults: true` |
| DATETIME | ISO 8601 datetime | `defaults: "2024-01-01T00:00:00Z"` |
| DATE | ISO 8601 date | `defaults: "2024-01-01"` |
| TIME | ISO 8601 time | `defaults: "09:00:00"` |
| DURATION | ISO 8601 duration | `defaults: "PT1H"` |
| FILE | Uploaded file | (stored in internal storage) |
| JSON | JSON object | `defaults: '{"key": "value"}'` |
| ARRAY | List of items | `itemType: STRING` required |
| SELECT | Dropdown | `values: [a, b, c]` |

## Common Task Types

### Logging & Debug
```yaml
- id: log_message
  type: io.kestra.plugin.core.log.Log
  message: "Hello {{ inputs.name }}!"
  level: INFO  # DEBUG, INFO, WARN, ERROR
```

### HTTP Requests
```yaml
- id: api_call
  type: io.kestra.plugin.core.http.Request
  uri: "https://api.example.com/data"
  method: GET
  headers:
    Authorization: "Bearer {{ secret('API_TOKEN') }}"
```

### Python Scripts
```yaml
- id: python_task
  type: io.kestra.plugin.scripts.python.Script
  containerImage: python:3.11-slim
  beforeCommands:
    - pip install pandas requests
  script: |
    import pandas as pd
    from kestra import Kestra
    
    data = {"result": "success"}
    Kestra.outputs(data)  # Pass outputs to next tasks
  outputFiles:
    - "*.csv"  # Files to capture
```

### Shell Commands
```yaml
- id: shell_task
  type: io.kestra.plugin.scripts.shell.Commands
  commands:
    - echo "Processing {{ inputs.filename }}"
    - cat {{ outputs.download.uri }}
```

## Detailed References

### Core Workflow Components
- **Core Plugins (HTTP, KV Store, Storage, Logging)**: See [references/core.md](references/core.md)
- **Script Tasks (Python, Shell, Node.js)**: See [references/scripts.md](references/scripts.md)
- **Triggers (Schedule, Webhook, Flow)**: See [references/triggers.md](references/triggers.md)
- **Flowable Tasks (Parallel, If, Switch, ForEach)**: See [references/flowable.md](references/flowable.md)
- **Error Handling & Retries**: See [references/error-handling.md](references/error-handling.md)
- **Pebble Templating & Expressions**: See [references/templating.md](references/templating.md)
- **Internal Storage & File Access**: See [references/storage.md](references/storage.md) - URI schemes (`kestra:///`, `nsfile:///`, `file:///`), fetchType modes, Ion format, `read()` function, `inputFiles`/`outputFiles`, and storage management tasks

### Plugins
- **Elasticsearch**: See [references/elasticsearch.md](references/elasticsearch.md)
- **AI & LLM (OpenAI, Agents, RAG)**: See [references/ai-llm.md](references/ai-llm.md)
- **SerDes (CSV, JSON, Avro, Parquet)**: See [references/serdes.md](references/serdes.md)

### Architecture & Patterns
- **Best Practices (Task Runners, Subflows, Python)**: See [references/best-practices.md](references/best-practices.md)
- **Common Patterns & Examples**: See [references/patterns.md](references/patterns.md)
- **Gotchas & Hard-Won Lessons**: See [references/gotchas.md](references/gotchas.md) - Critical pitfalls including `kestra:///` URI auto-resolution, ForEachItem merge outputs, shell quoting, and debugging techniques

### Additional Resources
- **Ask Kestra AI API**: See [references/ask-kestra-ai.md](references/ask-kestra-ai.md) - Query Kestra's documentation AI when you need more specific answers or the latest documentation

> **Tip**: If a Kestra MCP server is configured, use it to validate flows, list executions, or trigger runs directly. This skill focuses on generating correct YAML; the MCP server handles runtime interaction.

> **Tip**: If you can't find an answer in the static references, use the Ask Kestra AI API to query their documentation assistant. It's especially useful for:
> - Edge cases not covered in common patterns
> - Latest plugin features or changes
> - Complex output structures (e.g., ForEachItem merging)
> - Troubleshooting specific error messages

## Quick Debugging Checklist

- [ ] **Indentation**: Exactly 2 spaces (no tabs)
- [ ] **Task IDs**: Unique within flow, use lowercase with hyphens
- [ ] **Plugin types**: Fully qualified (`io.kestra.plugin.core.log.Log`)
- [ ] **Expressions**: Use `{{ }}` for Pebble templating
- [ ] **Secrets**: Use `{{ secret('SECRET_NAME') }}`
- [ ] **Outputs**: Reference as `{{ outputs.taskId.property }}`
- [ ] **Inputs**: Reference as `{{ inputs.inputId }}`
- [ ] **Strings with colons**: Quote them (`message: "Time: 10:00"`)
- [ ] **Multi-line scripts**: Use `|` for literal block scalar

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| "Task type not found" | Plugin not available or typo | Verify exact plugin type string |
| "Invalid YAML syntax" | Bad indentation or special chars | Use 2-space indent, quote strings with `:` |
| "Variable not found" | Wrong expression syntax | Check `{{ outputs.taskId.prop }}` format |
| "Required property missing" | Missing required task field | Check plugin docs for required fields |
| "Cannot coerce" | Type mismatch in expression | Verify input/output types match |
| Broken JSON body / 400 errors | User data contains `"` quotes | Use `{{ value \| json }}` filter (no surrounding quotes) |
| Fix deployed but restart still fails | `restart` uses original revision | Use `replay` with `latest_revision: true` instead |
