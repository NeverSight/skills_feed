---
name: parallel-deep-research
description: "ONLY use when user explicitly says 'deep research', 'exhaustive', 'comprehensive report', or 'thorough investigation'. Slower and more expensive than parallel-web-search. For normal research/lookup requests, use parallel-web-search instead."
compatibility: Requires parallel-cli and internet access.
allowed-tools: Bash(parallel-cli:*)
metadata:
  author: parallel
---

# Deep Research

Research topic: $ARGUMENTS

## When to use (vs parallel-web-search)

ONLY use this skill when the user explicitly requests deep/exhaustive research. Deep research is 10-100x slower and more expensive than parallel-web-search. For normal "research X" requests, quick lookups, or fact-checking, use **parallel-web-search** instead.

## Step 1: Start the research

```bash
parallel-cli research run "$ARGUMENTS" --processor pro-fast --no-wait --json
```

This returns instantly. Do NOT omit `--no-wait` — without it the command blocks for minutes and will time out.

Processor options (choose based on user request):

| Processor | Expected latency | Use when |
|-----------|-----------------|----------|
| `pro-fast` | 30s – 5 min | Default — good balance of depth and speed |
| `ultra-fast` | 1 – 10 min | Deeper analysis, more sources (~2x cost) |
| `ultra` | 5 – 25 min | Maximum depth, only when explicitly requested (~3x cost) |

Parse the JSON output to extract the `run_id` and monitoring URL. Immediately tell the user:
- Deep research has been kicked off
- The expected latency for the processor tier chosen (from the table above)
- The monitoring URL where they can track progress

Tell them they can background the polling step to continue working while it runs.

## Step 2: Poll for results

Choose a descriptive filename based on the topic (e.g., `ai-chip-market-2026`, `react-vs-vue-comparison`). Use lowercase with hyphens, no spaces.

```bash
parallel-cli research poll "$RUN_ID" -o "$FILENAME" --timeout 540
```

Important:
- Use `--timeout 540` (9 minutes) to stay within tool execution limits
- Do NOT pass `--json` — the full output is large and will flood context. The `-o` flag writes results to files instead.
- The `-o` flag generates two output files:
  - `$FILENAME.json` — metadata and basis
  - `$FILENAME.md` — formatted markdown report
- The poll command prints an **executive summary** to stdout when the research completes. Share this executive summary with the user — it gives them a quick overview without having to open the files.

### If the poll times out

Higher processor tiers can take longer than 9 minutes. If the poll exits without completing:
1. Tell the user the research is still running server-side
2. Re-run the same `parallel-cli research poll` command to continue waiting

## Response format

**After step 1:** Share the monitoring URL (for tracking progress only — it is not the final report).

**After step 2:**
1. Share the **executive summary** that the poll command printed to stdout
2. Tell the user the two generated file paths:
   - `$FILENAME.md` — formatted markdown report
   - `$FILENAME.json` — metadata and basis

Do NOT re-share the monitoring URL after completion — the results are in the files, not at that link.

Ask the user if they would like to read through the files for more detail. Do NOT read the file contents into context unless the user asks.

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
