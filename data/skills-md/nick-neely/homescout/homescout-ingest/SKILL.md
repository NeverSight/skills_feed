---
name: homescout-ingest
description: Analyze Homescout output directories (current.json, history/*.jsonl(.gz), speedtests.jsonl, speedtests/*.jsonl(.gz)) with CLI tools like jq/rg/awk to answer questions about device presence, outages, scan stats, or speedtest trends. Use when an agent needs to ingest Homescout outputs, especially from remote/Tailscale/Taildrive output paths.
---

# Homescout Ingest

## Overview

Ingest Homescout output artifacts and answer analysis questions using command-line tools without changing the underlying data. Focus on JSON and JSONL files, including gzip-compressed history and speedtest archives.

## Workflow

1. Locate the output directory.
   - Use the user-provided path or look up `output_dir` in the Homescout config.
   - Treat the directory as read-only.
2. Identify the available files.
   - `current.json` for the latest snapshot.
   - `history/YYYY-MM-DD.jsonl` (or `.jsonl.gz`) for scan history.
   - `speedtests.jsonl` plus `speedtests/YYYY-MM-DD.jsonl` (or `.jsonl.gz`) for speedtest history.
3. Choose the correct data source for the question.
   - "Right now" questions: `current.json`.
   - "Over time" device or scan questions: `history/*.jsonl(.gz)`.
   - Speedtest trends or degradations: `speedtests*.jsonl(.gz)`.
4. Parse with jq and standard CLI tools.
   - Use `jq` for JSON/JSONL, `rg` for filtering text, and `gzip -cd` for `.gz` files.
5. Summarize results with timestamps and counts.
   - Include UTC timestamps and the file range you used.

## Quick Commands

- Inspect latest snapshot metadata:
  - `jq '.metadata' current.json`
- List devices currently offline:
  - `jq -r '.devices[] | select(.status=="offline") | [.ip,.hostname,.last_seen] | @tsv' current.json`
- Count devices by status:
  - `jq -r '.devices[].status' current.json | sort | uniq -c`
- Pull scan duration and average response time:
  - `jq '.metadata.scan_duration_ms, .stats.avg_response_time_ms' current.json`
- Read history JSONL (plain):
  - `jq -r '.metadata.timestamp' history/2026-02-04.jsonl`
- Read history JSONL (gzipped):
  - `gzip -cd history/2026-02-04.jsonl.gz | jq -r '.metadata.timestamp'`
- Inspect speedtests:
  - `jq -r '[.timestamp,.download_mbps,.upload_mbps,.latency_ms,.degraded] | @tsv' speedtests.jsonl`

## Analysis Recipes

- Find new devices in a specific day:
  - `jq -r 'select(.stats.new_devices_this_scan > 0) | [.metadata.timestamp,.stats.new_devices_this_scan] | @tsv' history/2026-02-04.jsonl`
- Detect devices that went offline since last scan:
  - Compare `current.json` with the last history entry for status changes.
- Track a specific MAC or IP across history:
  - `rg -n '"mac":"AA:BB:CC' history/2026-02-*.jsonl`
  - For gzipped files: `gzip -cd history/2026-02-04.jsonl.gz | rg -n '"mac":"AA:BB:CC'`
- Identify slow responders in current scan:
  - `jq -r '.devices[] | select(.response_time_ms >= 200) | [.ip,.response_time_ms] | @tsv' current.json`
- Summarize speedtest degradations:
  - `jq -r 'select(.degraded==true) | [.timestamp,.download_mbps,.upload_mbps] | @tsv' speedtests.jsonl`

## Schema Reference

- Read `references/output_schema.md` for the snapshot, device, and speedtest field definitions.

## Guardrails

- Do not modify or delete output files unless explicitly requested.
- Handle `.jsonl.gz` with `gzip -cd` to avoid altering archives.
- Treat timestamps as UTC and preserve them in summaries.
