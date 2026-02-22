---
name: os-integrations
description: >
  Run Firefox mach try commands with pre-configured flags for os-integration testing
  on Windows and Linux alpha worker pools. Use when testing Firefox changes against
  Windows 10, Windows 11, Ubuntu 24.04, hardware workers, ARM64, or AMD configurations.
  Triggers on "os-integration", "mach try", "windows testing", "linux testing", "alpha image".
---

# OS Integrations

Run Firefox `mach try` commands with pre-configured worker pool overrides for testing against alpha images.

## Usage

```bash
# Run with preset (dry-run to preview)
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --dry-run

# Push to try server
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --push

# Filter to specific test types (recommended)
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 -t xpcshell -t mochitest-browser-chrome --push
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 -t mochitest-devtools-chrome -t mochitest-chrome-1proc --dry-run

# Override query (advanced)
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 -q "test-windows11-64-24h2" --push
```

## Build Behavior

By default, the script reuses builds from the latest mozilla-central decision task (skipping the 45+ minute Firefox build). Use `--fresh-build` to force a full build instead:

```bash
# Default: reuses existing Firefox builds
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 -t xpcshell --push

# Use a specific decision task
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --task-id ABC123 -t mochitest-browser-chrome --push

# Force a fresh Firefox build
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --fresh-build --push
```

## Watching Test Results

Use `--watch` to automatically monitor test results with lumberjackth after pushing:

```bash
# Push and watch all test results
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 -t xpcshell --watch

# Watch with filter (regex)
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --watch --watch-filter "xpcshell|mochitest"

# Combine with fresh build and watch
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --fresh-build -t xpcshell --watch
```

## Watching Lando Job Status

Use `--watch-lando` to poll the Lando landing job status until it lands or fails:

```bash
# Push and watch Lando job (polls every 90 seconds by default)
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 -t xpcshell --watch-lando

# Custom polling interval (in seconds)
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --watch-lando --lando-interval 60

# Combine with test watching (Lando check runs first, then test watching)
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --watch-lando --watch
```

## Named Query Sets

Use `--query-set` to run a predefined set of test queries. Query sets can bundle specific suites with their own settings (e.g., skipping os-integration):

```bash
# Run targeted test suites
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --query-set targeted --push

# Preview what a query set will run
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --query-set targeted --dry-run

# Watch results from a query set
uv run ~/.claude/skills/os-integrations/scripts/run_try.py win11-24h2 --query-set targeted --watch
```

Query sets are defined per-preset in `references/presets.yml` under the `query_sets` key.

## Common Test Types

Use `-t` to filter to specific test suites:

- `xpcshell` - XPCShell tests
- `mochitest-browser-chrome` - Browser chrome mochitests
- `mochitest-chrome-1proc` - Chrome mochitests (single process)
- `mochitest-devtools-chrome` - DevTools mochitests
- `mochitest-plain` - Plain mochitests
- `reftest` - Reference tests
- `crashtest` - Crash tests

## Available Presets

- `win11-24h2` - Windows 11 24H2 standard
- `win11-hw` - Windows 11 hardware workers
- `win10-2009` - Windows 10 2009
- `win11-amd` - Windows 11 AMD configuration
- `win11-source` - Source image testing
- `b-win2022` - Build worker testing
- `win11-arm64` - ARM64 architecture

## Prerequisites

- Firefox repository at `~/firefox`
- Must be on a feature branch (not main/master)
- Mozilla Auth0 authentication (for Lando-based pushes)

## Additional Documentation

- **Presets Configuration**: See `references/presets.yml`
- **Linux Worker Overrides**: See `references/linux-worker-overrides.md`
- **Pushing to Try**: See `references/pushing-to-try.md`
- **Script Help**: Run `uv run ~/.claude/skills/os-integrations/scripts/run_try.py --help`

## Official Documentation

For more information on mach try and Taskcluster:

- **Firefox Try Documentation**: https://firefox-source-docs.mozilla.org/tools/try/
- **Taskcluster Documentation**: https://docs.taskcluster.net/
- **Firefox Source Docs**: https://firefox-source-docs.mozilla.org/
