---
name: parallel-data-enrichment
description: "Bulk data enrichment. Adds web-sourced fields (CEO names, funding, contact info) to lists of companies, people, or products. Use for enriching CSV files or inline data."
compatibility: Requires parallel-cli and internet access.
allowed-tools: Bash(parallel-cli:*)
metadata:
  author: parallel
---

# Data Enrichment

Enrich: $ARGUMENTS

## Before starting

Inform the user that enrichment may take several minutes depending on the number of rows and fields requested.

## Step 1: Start the enrichment

Use ONE of these command patterns (substitute user's actual data):

For inline data:

```bash
parallel-cli enrich run --data '[{"company": "Google"}, {"company": "Microsoft"}]' --intent "CEO name and founding year" --target "output.csv" --no-wait
```

For CSV file:

```bash
parallel-cli enrich run --source-type csv --source "input.csv" --target "output.csv" --source-columns '[{"name": "company", "description": "Company name"}]' --intent "CEO name and founding year" --no-wait
```

**IMPORTANT:** Always include `--no-wait` so the command returns immediately instead of blocking.

Parse the output to extract the `taskgroup_id` and monitoring URL. Immediately tell the user:
- Enrichment has been kicked off
- The monitoring URL where they can track progress

Tell them they can background the polling step to continue working while it runs.

## Step 2: Poll for results

```bash
parallel-cli enrich poll "$TASKGROUP_ID" --timeout 540
```

Important:
- Use `--timeout 540` (9 minutes) to stay within tool execution limits

### If the poll times out

Enrichment of large datasets can take longer than 9 minutes. If the poll exits without completing:
1. Tell the user the enrichment is still running server-side
2. Re-run the same `parallel-cli enrich poll` command to continue waiting

## Response format

**After step 1:** Share the monitoring URL (for tracking progress).

**After step 2:**
1. Report number of rows enriched
2. Preview first few rows of the output CSV
3. Tell user the full path to the output CSV file

Do NOT re-share the monitoring URL after completion — the results are in the output file.

## Setup

If `parallel-cli` is not found, install and authenticate:

```bash
curl -fsSL https://parallel.ai/install.sh | bash
```

If unable to install that way, install via pipx instead:

```bash
pipx install "parallel-web-tools[cli]"
pipx ensurepath
```

Then authenticate:

```bash
parallel-cli login
```

Or set an API key: `export PARALLEL_API_KEY="your-key"`
