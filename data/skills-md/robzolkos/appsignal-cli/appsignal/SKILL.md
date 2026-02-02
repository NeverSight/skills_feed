---
name: appsignal
description: Fetch and analyze AppSignal error incidents. Use when debugging errors, investigating exceptions, or when the user mentions AppSignal, incidents, or error monitoring.
argument-hint: "[incidents|samples] [command] [options]"
allowed-tools: Bash(appsignal-cli *)
---

# AppSignal CLI

Use the `appsignal-cli` CLI to fetch error incidents and samples from AppSignal for debugging and analysis.

## Prerequisites

Ensure `APPSIGNAL_TOKEN` and `APPSIGNAL_APP_ID` environment variables are set, or a `.appsignal-cli.yaml` config file exists.

## Common Workflows

### Investigate Recent Errors

```bash
# List open incidents
appsignal-cli incidents list

# Get details for a specific incident
appsignal-cli incidents get <number>
```

### Filter Incidents

```bash
# By state: open, closed, wip
appsignal-cli incidents list --state open

# By namespace: web, background, frontend
appsignal-cli incidents list --namespace web

# By date (ISO 8601)
appsignal-cli incidents list --since 2024-01-15

# By minimum occurrences
appsignal-cli incidents list --min-occurrences 10

# Combine filters
appsignal-cli incidents list --namespace background --min-occurrences 5
```

### Get Detailed Error Information

```bash
# Standard detail view
appsignal-cli incidents get <number>

# With params and session data
appsignal-cli --verbose incidents get <number>

# Export as markdown for analysis
appsignal-cli incidents export <number> -o error-report.md
```

### Work with Error Samples

```bash
# List recent error samples
appsignal-cli samples list --limit 10

# Get full sample details (params, session, environment)
appsignal-cli samples get <sample-id>
```

### Manage Incidents

```bash
# Close a resolved incident
appsignal-cli incidents close <number>

# Reopen if issue recurs
appsignal-cli incidents reopen <number>
```

## Output Formats

Use `--compact` for token-efficient output when analyzing errors:

```bash
appsignal-cli --compact incidents list
appsignal-cli --compact incidents get <number>
```

Use `--json` for structured data:

```bash
appsignal-cli --json incidents list
```

## Debugging Steps

When asked to debug an AppSignal error:

1. **List incidents** to find the relevant error
2. **Get incident details** including backtrace
3. **Analyze the backtrace** to identify the root cause
4. **Find the relevant code** in the codebase
5. **Propose a fix** based on the error context

## Available Commands

| Command | Description |
|---------|-------------|
| `apps` | List all applications |
| `incidents list` | List error incidents |
| `incidents get <n>` | Get incident details |
| `incidents close <n>` | Close an incident |
| `incidents reopen <n>` | Reopen an incident |
| `incidents export <n>` | Export to markdown |
| `samples list` | List error samples |
| `samples get <id>` | Get sample details |
| `config show` | Show current config |
| `config init` | Initialize config file |
| `config set <k> <v>` | Set config value |
