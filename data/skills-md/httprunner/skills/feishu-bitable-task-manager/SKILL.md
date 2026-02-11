---
name: feishu-bitable-task-manager
description: Manage task records in Feishu Bitable (飞书多维表格) using a fixed task-status table schema and TASK_FIELD_* overrides. Use to fetch/claim/update/create tasks, look up drama metadata by BookID, or derive tasks from a source Bitable (JSON/JSONL in/out).
---

# Feishu Bitable Task Manager

Use this skill to read/write tasks in a Feishu Bitable “task status table” while staying compatible with its schema conventions.

## Path Convention

Canonical install and execution directory: `~/.agents/skills/feishu-bitable-task-manager/`. Run commands from this directory:

```bash
cd ~/.agents/skills/feishu-bitable-task-manager
```

One-off (safe in scripts/loops from any working directory):

```bash
(cd ~/.agents/skills/feishu-bitable-task-manager && npx tsx scripts/bitable_task.ts --help)
```

## Quick start

Run:

```bash
npx tsx scripts/bitable_task.ts <subcommand> [flags]
```

## Required env

- `FEISHU_APP_ID`, `FEISHU_APP_SECRET`
- `TASK_BITABLE_URL`
- Optional: `FEISHU_BASE_URL`
- Optional: `TASK_FIELD_*` (override task table column names)

## Key defaults (compat rules)

- Treat date presets as literal strings: `Today`, `Yesterday`, `Any` (`Any` means no date constraint).
- Prefer fetching by `--task-id` / `--biz-task-id` when possible (it overrides `--app/--scene/--status/--date`).
- Ignore view filtering by default; use view filtering only when explicitly enabled (see `references/task-fetch.md`).
- Keep only decoded rows with `TaskID != 0` and at least one of `Params/ItemID/BookID/URL/UserID/UserName`.
- Allow comma-separated priority lists for `--status` / `--scene`.
- `fetch` supports `--limit`; earlier scene/status values are filled first when `--limit` is set.
- `claim` is single-task only; do not use `--limit`. `--candidate-limit` only controls candidate attempts (see `references/task-claim.md`).
- `fetch` and `claim` both split comma-separated `--scene` values and query each scene in order (do not treat the full CSV as one literal scene).
- When ingesting JSON/JSONL, pass through keys that match column names; map `CDNURL`/`cdn_url` into `Extra` when present.

## Commands

### Fetch

```bash
npx tsx scripts/bitable_task.ts fetch --app com.smile.gifmaker --scene 综合页搜索 --status pending --date Today --limit 10
npx tsx scripts/bitable_task.ts fetch --task-id "1326,1327" --raw
npx tsx scripts/bitable_task.ts fetch --biz-task-id ext-20240101-001 --raw
```

### Claim (multi-worker safe)

```bash
npx tsx scripts/bitable_task.ts claim \
  --app com.tencent.mm \
  --scene 个人页搜索,综合页搜索 \
  --device-serial <serial> \
  --status pending,failed \
  --date Today \
  --candidate-limit 5
```

Claim behavior details are in `references/task-claim.md`.

### Update

```bash
npx tsx scripts/bitable_task.ts update --task-id 180413 --status running --device-serial <serial> --dispatched-at now
npx tsx scripts/bitable_task.ts update --input updates.jsonl
```

### Create

```bash
npx tsx scripts/bitable_task.ts create \
  --input tasks.jsonl \
  --app com.smile.gifmaker \
  --scene 单个链接采集 \
  --status pending \
  --date YYYY-MM-DD \
  --skip-existing BizTaskID
```

### Drama Fetch (read-only)

Fetch rows from source drama Bitable by optional BookID filter. Use `--format meta` when callers need normalized drama metadata fields:

```bash
npx tsx scripts/drama_fetch.ts --bitable-url "<DRAMA_BITABLE_URL>" --book-id "id1,id2" --format meta
```

### Derive tasks from a source Bitable (原始多维表格)

`sync` accepts either `--input` or `--bitable-url` (optionally with `--book-id`) and handles task creation:

```bash
npx tsx scripts/drama_sync_task.ts \
  --bitable-url "https://.../base/SOURCE_APP?table=SOURCE_TABLE" \
  --task-url "https://.../base/TASK_APP?table=TASK_TABLE" \
  --app com.smile.gifmaker \
  --extra 春节档专项 \
  --params-list \
  --limit 10 \
  --skip-existing
```

## Resources

- Read `references/task-fetch.md` for filters, pagination, validation, and field mapping.
- Read `references/task-claim.md` for cross-machine safe task claiming.
- Read `references/task-update.md` for status updates, timing fields, and batch update rules.
- Read `references/task-create.md` for create payload rules and batch create behavior.
- Read `references/feishu-integration.md` for Feishu API endpoints and request/response payloads.
- Use `scripts/bitable_task.ts` / `scripts/drama_fetch.ts` / `scripts/drama_sync_task.ts` as the source of truth for flags and behavior.
