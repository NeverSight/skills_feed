---
name: deep-research
description: Async deep research via Gemini Interactions API (no Gemini CLI dependency). RAG-ground queries on local files (--context), preview costs (--dry-run), structured JSON output, adaptive polling. Universal skill for 30+ AI agents including Claude Code, Amp, Codex, and Gemini CLI.
license: MIT
metadata:
  version: "1.3.0"
  author: "24601"
---

# Deep Research Skill

Perform deep research powered by Google Gemini's deep research agent. Upload documents to file search stores for RAG-grounded answers. Manage research sessions with persistent workspace state.

## For AI Agents

Get a full capabilities manifest, decision trees, and output contracts:

```bash
uv run {baseDir}/scripts/onboard.py --agent
```

See [AGENTS.md]({baseDir}/AGENTS.md) for the complete structured briefing.

| Command | What It Does |
|---------|-------------|
| `uv run {baseDir}/scripts/research.py start "question"` | Launch deep research |
| `uv run {baseDir}/scripts/research.py start "question" --context ./path --dry-run` | Estimate cost |
| `uv run {baseDir}/scripts/research.py start "question" --context ./path --output report.md` | RAG-grounded research |
| `uv run {baseDir}/scripts/store.py query <name> "question"` | Quick Q&A against uploaded docs |

## Prerequisites

- A Google API key (`GOOGLE_API_KEY` or `GEMINI_API_KEY` environment variable)
- [uv](https://docs.astral.sh/uv/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Quick Start

```bash
# Run a deep research query
uv run {baseDir}/scripts/research.py "What are the latest advances in quantum computing?"

# Check research status
uv run {baseDir}/scripts/research.py status <interaction-id>

# Save a completed report
uv run {baseDir}/scripts/research.py report <interaction-id> --output report.md

# Research grounded in local files (auto-creates store, uploads, cleans up)
uv run {baseDir}/scripts/research.py start "How does auth work?" --context ./src --output report.md

# Export as HTML or PDF
uv run {baseDir}/scripts/research.py start "Analyze the API" --context ./src --format html --output report.html

# Auto-detect prompt template based on context files
uv run {baseDir}/scripts/research.py start "How does auth work?" --context ./src --prompt-template auto --output report.md
```

## Environment Variables

Set one of the following (checked in order of priority):

| Variable | Description |
|----------|-------------|
| `GEMINI_DEEP_RESEARCH_API_KEY` | Dedicated key for this skill (highest priority) |
| `GOOGLE_API_KEY` | Standard Google AI key |
| `GEMINI_API_KEY` | Gemini-specific key |

Optional model configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_DEEP_RESEARCH_MODEL` | Model for file search queries | `models/gemini-flash-latest` |
| `GEMINI_MODEL` | Fallback model name | `models/gemini-flash-latest` |
| `GEMINI_DEEP_RESEARCH_AGENT` | Deep research agent identifier | `deep-research-pro-preview-12-2025` |

## Research Commands

### Start Research

```bash
uv run {baseDir}/scripts/research.py start "your research question"
```

| Flag | Description |
|------|-------------|
| `--report-format FORMAT` | Output structure: `executive_summary`, `detailed_report`, `comprehensive` |
| `--store STORE_NAME` | Ground research in a file search store (display name or resource ID) |
| `--no-thoughts` | Hide intermediate thinking steps |
| `--follow-up ID` | Continue a previous research session |
| `--output FILE` | Wait for completion and save report to a single file |
| `--output-dir DIR` | Wait for completion and save structured results to a directory (see below) |
| `--timeout SECONDS` | Maximum wait time when polling (default: 1800 = 30 minutes) |
| `--no-adaptive-poll` | Disable history-adaptive polling; use fixed interval curve instead |
| `--context PATH` | Auto-create ephemeral store from a file or directory for RAG-grounded research |
| `--context-extensions EXT` | Filter context uploads by extension (e.g. `py,md` or `.py .md`) |
| `--keep-context` | Keep the ephemeral context store after research completes (default: auto-delete) |
| `--dry-run` | Estimate costs without starting research (prints JSON cost estimate) |
| `--format {md,html,pdf}` | Output format for the report (default: md; pdf requires weasyprint) |
| `--prompt-template {typescript,python,general,auto}` | Domain-specific prompt prefix; auto detects from context file extensions |

The `start` subcommand is the default, so `research.py "question"` and `research.py start "question"` are equivalent.

### Check Status

```bash
uv run {baseDir}/scripts/research.py status <interaction-id>
```

Returns the current status (`in_progress`, `completed`, `failed`) and outputs if available.

### Save Report

```bash
uv run {baseDir}/scripts/research.py report <interaction-id>
```

| Flag | Description |
|------|-------------|
| `--output FILE` | Save report to a specific file path (default: `report-<id>.md`) |
| `--output-dir DIR` | Save structured results to a directory |

## Structured Output (`--output-dir`)

When `--output-dir` is used, results are saved to a structured directory:

```
<output-dir>/
  research-<id>/
    report.md          # Full final report
    metadata.json      # Timing, status, output count, sizes
    interaction.json   # Full interaction data (all outputs, thinking steps)
    sources.json       # Extracted source URLs/citations
```

A compact JSON summary (under 500 chars) is printed to stdout:

```json
{
  "id": "interaction-123",
  "status": "completed",
  "output_dir": "research-output/research-interaction-1/",
  "report_file": "research-output/research-interaction-1/report.md",
  "report_size_bytes": 45000,
  "duration_seconds": 154,
  "summary": "First 200 chars of the report..."
}
```

This is the recommended pattern for AI agent integration -- the agent receives a small JSON payload while the full report is written to disk.

## Adaptive Polling

When `--output` or `--output-dir` is used, the script polls the Gemini API until research completes. By default, it uses **history-adaptive polling** that learns from past research completion times:

- Completion times are recorded in `.gemini-research.json` under `researchHistory` (last 50 entries, separate curves for grounded vs non-grounded research).
- When 3+ matching data points exist, the poll interval is tuned to the historical distribution:
  - Before any research has ever completed: slow polling (30s)
  - In the likely completion window (p25-p75): aggressive polling (5s)
  - In the tail (past p75): moderate polling (15-30s)
  - Unusually long runs (past 1.5x the longest ever): slow polling (60s)
- All intervals are clamped to [2s, 120s] as a fail-safe.

When history is insufficient (<3 data points) or `--no-adaptive-poll` is passed, a fixed escalating curve is used: 5s (first 30s), 10s (30s-2min), 30s (2-10min), 60s (10min+).

## Cost Estimation (`--dry-run`)

Preview estimated costs before running research:

```bash
uv run {baseDir}/scripts/research.py start "Analyze security architecture" --context ./src --dry-run
```

Outputs a JSON cost estimate to stdout with context upload costs, research query costs, and a total. Estimates are heuristic-based (the Gemini API does not return token counts or billing data) and clearly labeled as such.

After research completes with `--output-dir`, the `metadata.json` file includes a `usage` key with post-run cost estimates based on actual output size and duration.

## File Search Store Commands

Manage file search stores for RAG-grounded research and Q&A.

### Create a Store

```bash
uv run {baseDir}/scripts/store.py create "My Project Docs"
```

### List Stores

```bash
uv run {baseDir}/scripts/store.py list
```

### Query a Store

```bash
uv run {baseDir}/scripts/store.py query <store-name> "What does the auth module do?"
```

| Flag | Description |
|------|-------------|
| `--output-dir DIR` | Save response and metadata to a directory |

### Delete a Store

```bash
uv run {baseDir}/scripts/store.py delete <store-name>
```

Use `--force` to skip the confirmation prompt. When stdin is not a TTY (e.g., called by an AI agent), the prompt is automatically skipped.

## File Upload

Upload files or entire directories to a file search store.

```bash
uv run {baseDir}/scripts/upload.py ./src fileSearchStores/abc123
```

| Flag | Description |
|------|-------------|
| `--smart-sync` | Skip files that haven't changed (hash comparison) |
| `--extensions EXT [EXT ...]` | File extensions to include (comma or space separated, e.g. `py,ts,md` or `.py .ts .md`) |

Hash caches are always saved on successful upload, so a subsequent `--smart-sync` run will correctly skip unchanged files even if the first upload did not use `--smart-sync`.

### MIME Type Support

36 file extensions are natively supported by the Gemini File Search API. Common programming files (JS, TS, JSON, CSS, YAML, etc.) are automatically uploaded as `text/plain` via a fallback mechanism. Binary files are rejected. See `references/file_search_guide.md` for the full list.

**File size limit**: 100 MB per file.

## Session Management

Research IDs and store mappings are cached in `.gemini-research.json` in the current working directory.

### Show Session State

```bash
uv run {baseDir}/scripts/state.py show
```

### Show Research Sessions Only

```bash
uv run {baseDir}/scripts/state.py research
```

### Show Stores Only

```bash
uv run {baseDir}/scripts/state.py stores
```

### JSON Output for Agents

Add `--json` to any state subcommand to output structured JSON to stdout:

```bash
uv run {baseDir}/scripts/state.py --json show
uv run {baseDir}/scripts/state.py --json research
uv run {baseDir}/scripts/state.py --json stores
```

### Clear Session State

```bash
uv run {baseDir}/scripts/state.py clear
```

Use `-y` to skip the confirmation prompt. When stdin is not a TTY (e.g., called by an AI agent), the prompt is automatically skipped.

## Non-Interactive Mode

All confirmation prompts (`store.py delete`, `state.py clear`) are automatically skipped when stdin is not a TTY. This allows AI agents and CI pipelines to call these commands without hanging on interactive prompts.

## Workflow Example

A typical grounded research workflow:

```bash
# 1. Create a file search store
STORE_JSON=$(uv run {baseDir}/scripts/store.py create "Project Codebase")
STORE_NAME=$(echo "$STORE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['name'])")

# 2. Upload your documents
uv run {baseDir}/scripts/upload.py ./docs "$STORE_NAME" --smart-sync

# 3. Query the store directly
uv run {baseDir}/scripts/store.py query "$STORE_NAME" "How is authentication handled?"

# 4. Start grounded deep research (blocking, saves to directory)
uv run {baseDir}/scripts/research.py start "Analyze the security architecture" \
  --store "$STORE_NAME" --output-dir ./research-output --timeout 3600

# 5. Or start non-blocking and check later
RESEARCH_JSON=$(uv run {baseDir}/scripts/research.py start "Analyze the security architecture" --store "$STORE_NAME")
RESEARCH_ID=$(echo "$RESEARCH_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 6. Check progress
uv run {baseDir}/scripts/research.py status "$RESEARCH_ID"

# 7. Save the report when completed
uv run {baseDir}/scripts/research.py report "$RESEARCH_ID" --output-dir ./research-output
```

## Output Convention

All scripts follow a dual-output pattern:
- **stderr**: Rich-formatted human-readable output (tables, panels, progress bars)
- **stdout**: Machine-readable JSON for programmatic consumption

This means `2>/dev/null` hides the human output, and piping stdout gives clean JSON.

