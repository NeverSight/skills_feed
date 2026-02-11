---
name: teamcity-cli
description: Use when working with TeamCity CI/CD. Use `tc` CLI for builds, logs, jobs, queues, agents, and pipelines.
---

# TeamCity CLI (`tc`)

Interact with TeamCity CI/CD servers using the `tc` command-line tool.

## Quick Start

```bash
tc auth status                    # Check authentication
tc run list --status failure      # Find failed builds
tc run log <id> --failed          # View failed build log
```

## Core Commands

| Area     | Commands                                                                                  |
|----------|-------------------------------------------------------------------------------------------|
| Builds   | `run list`, `view`, `start`, `watch`, `log`, `cancel`, `restart`, `tests`, `changes`     |
| Artifacts| `run artifacts`, `run download`                                                           |
| Metadata | `run pin/unpin`, `run tag/untag`, `run comment`                                           |
| Jobs     | `job list`, `view`, `pause/resume`, `param list/get/set/delete`                           |
| Projects | `project list`, `view`, `param`, `token put/get`, `settings export/status/validate`       |
| Queue    | `queue list`, `approve`, `remove`, `top`                                                  |
| Agents   | `agent list`, `view`, `enable/disable`, `authorize`, `exec`, `term`, `reboot`, `move`     |
| Pools    | `pool list`, `view`, `link/unlink`                                                        |
| API      | `tc api <endpoint>` — raw REST API access                                                 |

## Common Workflows

**Investigate failure:** `tc run list --status failure` → `tc run log <id> --failed` → `tc run tests <id> --failed`
**Start build:** `tc run start <job-id> --branch <branch> --watch`
**Personal build:** `tc run start <job-id> --local-changes --watch`
**Find jobs:** `tc project list` → `tc job list --project <id>`
**Remote agent:** `tc agent term <id>` or `tc agent exec <id> "command"`
**Stream logs:** `tc run watch <id> --logs`

## References

- [Command Reference](references/commands.md) - All commands and flags
- [Workflows](references/workflows.md) - Detailed workflow examples
- [Output Formats](references/output.md) - JSON, plain text, scripting
