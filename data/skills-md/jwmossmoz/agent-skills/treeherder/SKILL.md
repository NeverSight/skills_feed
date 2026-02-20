---
name: treeherder
description: >
  Query Firefox Treeherder for CI job results using treeherder-cli (primary) and lumberjackth (secondary).
  Use after commits land to check test/build results.
  Triggers on "treeherder", "job results", "check tests", "ci status".
---

# Treeherder

Query Mozilla Treeherder for CI job results, failure analysis, and performance data.

## Tools

This skill uses two CLI tools:

| Tool | Role | Install | Strengths |
|------|------|---------|-----------|
| **treeherder-cli** | Primary | `cargo install --git https://github.com/padenot/treeherder-cli` | Failure analysis, revision comparison, test history, log fetching, artifact downloads |
| **lumberjackth** | Secondary | `uvx --from lumberjackth lj` (zero-install) | Push listing, failures-by-bug, error suggestions, perf alerts, result/tier/state filtering |

**Use treeherder-cli** for revision-based failure analysis, comparing revisions, test history, log searching, and artifact downloads.

**Use lumberjackth** for listing pushes, querying failures by bug ID, viewing error lines with bug suggestions, performance alerts, and filtering by result/state/tier.

## Quick Start

### treeherder-cli (primary)

```bash
# Get failed jobs for a revision
treeherder-cli a13b9fc22101 --json

# Filter by job name or platform
treeherder-cli a13b9fc22101 --filter "mochitest" --json
treeherder-cli a13b9fc22101 --platform "linux.*64" --json

# Group failures by test (cross-platform view)
treeherder-cli a13b9fc22101 --group-by test --json

# Compare revisions to find regressions
treeherder-cli a13b9fc22101 --compare b2c3d4e5f678 --json

# Check test history for intermittent detection
treeherder-cli --history "test_audio_playback" --history-count 10 --repo try --json

# Show similar job history for a failed job ID
treeherder-cli --similar-history 543981186 --similar-count 100 --repo try --json

# Fetch logs with pattern matching
treeherder-cli a13b9fc22101 --fetch-logs --pattern "ASSERTION|CRASH" --json

# Download artifacts
treeherder-cli a13b9fc22101 --download-artifacts --artifact-pattern "screenshot|errorsummary"

# Watch mode with notification
treeherder-cli a13b9fc22101 --watch --notify

# Switch repository (default: autoland)
treeherder-cli a13b9fc22101 --repo try --json
```

### lumberjackth (secondary)

```bash
# List recent pushes
uvx --from lumberjackth lj pushes autoland -n 10

# Get jobs for a push with result/tier filtering
uvx --from lumberjackth lj jobs autoland --push-id 12345 --result testfailed --tier 1

# Watch jobs with auto-refresh
uvx --from lumberjackth lj jobs try -r abc123 -w -i 60

# Query failures by bug ID
uvx --from lumberjackth lj failures 2012615 -t autoland -p "windows.*24h2"

# Show errors and bug suggestions
uvx --from lumberjackth lj errors autoland 545896732

# Performance alerts
uvx --from lumberjackth lj perf-alerts -r autoland -n 10

# JSON output
uvx --from lumberjackth lj --json jobs autoland --push-id 12345
```

## When to Use Which Tool

| Task | Tool | Example |
|------|------|---------|
| Analyze failures for a revision | treeherder-cli | `treeherder-cli abc123 --json` |
| Compare two revisions | treeherder-cli | `treeherder-cli abc123 --compare def456 --json` |
| Check test history | treeherder-cli | `treeherder-cli --history "test_name" --json` |
| Compare a failed job to similar jobs | treeherder-cli | `treeherder-cli --similar-history 543981186 --repo try --json` |
| Fetch/search logs | treeherder-cli | `treeherder-cli abc123 --fetch-logs --pattern "ERROR"` |
| Download artifacts | treeherder-cli | `treeherder-cli abc123 --download-artifacts` |
| Watch a revision | treeherder-cli | `treeherder-cli abc123 --watch --notify` |
| Performance/resource data | treeherder-cli | `treeherder-cli abc123 --perf --json` |
| List recent pushes | lumberjackth | `lj pushes autoland -n 10` |
| Filter by result/state/tier | lumberjackth | `lj jobs autoland --push-id 123 --result testfailed --tier 1` |
| Get single job details | lumberjackth | `lj job autoland "guid" --logs` |
| Failures by bug ID | lumberjackth | `lj failures 2012615 -t autoland` |
| Error lines + bug suggestions | lumberjackth | `lj errors autoland 545896732` |
| Performance alerts | lumberjackth | `lj perf-alerts -r autoland` |
| List repositories | lumberjackth | `lj repos` |

## Prerequisites

- **treeherder-cli**: `cargo install --git https://github.com/padenot/treeherder-cli`
- **lumberjackth**: No install needed, uses `uvx` for zero-install execution

No authentication required for either tool.

## References

- `references/cli-reference.md` - Complete CLI reference for both tools
- `references/sheriff-workflows.md` - Sheriff workflow examples
- `references/api-reference.md` - REST API documentation
- `references/similar-jobs-comparison.md` - Compare failed jobs using Treeherder's `similar_jobs` API

## External Documentation

- **Treeherder**: https://treeherder.mozilla.org/
- **treeherder-cli**: https://github.com/padenot/treeherder-cli
- **lumberjackth**: https://pypi.org/project/lumberjackth/
