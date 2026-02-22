---
name: oura-ring
description: Syncs daily health and fitness data from Oura Ring into markdown files. Provides sleep, readiness, activity, heart rate, stress, SpO2, and workout data.
disable-model-invocation: true
metadata:
  openclaw:
    primaryEnv: OURA_TOKEN
    requires:
      bins: ["uv"]
      env: ["OURA_TOKEN"]
    config:
      - id: oura_token
        label: Oura Personal Access Token
        type: secret
        env: OURA_TOKEN
---

# Oura Ring

This skill syncs your daily health data from Oura Ring into readable markdown files.

## Syncing Data

Sync today's data:

```bash
uv run {baseDir}/scripts/sync_oura.py
```

Sync a specific date:

```bash
uv run {baseDir}/scripts/sync_oura.py --date 2026-02-07
```

Sync the last N days:

```bash
uv run {baseDir}/scripts/sync_oura.py --days 7
```

## Reading Health Data

Health files are stored at `{baseDir}/health/YYYY-MM-DD.md` — one file per day.

To answer health or fitness questions, read the relevant date's file from the `{baseDir}/health/` directory. If the file doesn't exist for the requested date, run the sync command for that date first.

## Cron Setup

Schedule the sync script to run every morning using OpenClaw's `cron` tool so your health data stays up to date automatically.
