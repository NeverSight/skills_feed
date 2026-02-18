---
name: result-bitable-reporter
description: "Collect app events via evalpkgs into sqlite, then filter/report capture_results to Feishu Bitable with retry-safe writeback. Use for collect-start/collect-stop/filter/report/retry-reset workflows."
---

# Result Bitable Reporter

Use this skill for a deterministic `sqlite -> Feishu` result pipeline around `capture_results`.

## Path Convention

Canonical install and execution directory: `~/.agents/skills/result-bitable-reporter/`. Run commands from this directory:

```bash
cd ~/.agents/skills/result-bitable-reporter
```

One-off (safe in scripts/loops from any working directory):

```bash
(cd ~/.agents/skills/result-bitable-reporter && npx tsx scripts/result_reporter.ts --help)
```

## Workflow

1) Optional data collection:
- `collect-start`: start background `evalpkgs run` for one device (`SerialNumber`) with `TaskID` (digits only).
- `collect-stop`: stop that collector and print summary metrics (`delta`, `task_delta`, `records_jsonl`, `tracking_events`, `runtime_sec`).

2) Data selection:
- `filter`: preview target sqlite rows (`capture_results`) before upload.
- Task-scoped selection: pass `--task-id <TASK_ID>` to constrain rows to one task.
- Default status filter is pending+failed (`reported IN (0, -1)`).

Optional:
- `stat`: print total sqlite row count for one `--task-id` (used for “did new rows arrive?” checks).

3) Data reporting:
- `report`: batch create Feishu records and write back sqlite status.
- Optional `--max-rows <n>` sets total cap for one report run (default: process all matched rows).
- For per-task workflows, always pass `--task-id <TASK_ID>` to avoid cross-task uploads.
- Success writeback: `reported=1`, `reported_at=now_ms`, `report_error=NULL`.
- Failure writeback: `reported=-1`, `reported_at=now_ms`, `report_error=<truncated error>`.

4) Retry:
- `retry-reset`: move failed rows (`reported=-1`) back to pending (`reported=0`), then rerun `report`.

## Run

CLI entry:

```bash
npx tsx scripts/result_reporter.ts <subcommand> [flags]
```

Subcommands:
- `collect-start`
- `collect-stop`
- `stat`
- `filter`
- `report`
- `retry-reset`

Required env by phase:
- Collection: `BUNDLE_ID`, `SerialNumber`
- Feishu report: `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `RESULT_BITABLE_URL`
- Optional overrides: `FEISHU_BASE_URL`, `TRACKING_STORAGE_DB_PATH`, `RESULT_SQLITE_TABLE`

## Resources

- `scripts/result_reporter.ts`: executable source of truth for flags and behavior.
- `references/sqlite-and-field-mapping.md`: sqlite schema, collect-start/collect-stop semantics, SQL operations, command examples.
- `references/feishu-api-and-errors.md`: Feishu APIs, URL rules, failures, field mapping env overrides, command examples.
