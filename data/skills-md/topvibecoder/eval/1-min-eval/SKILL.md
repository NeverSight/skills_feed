---
name: 1-min-eval
description: Fast codebase evaluation using Claude CLI. Scans code to extract repo tree and source files, then runs parallel metric evaluations (impact, technical, creativity, presentation, prompt_design) via claude -p. Automatically submits to TopVibeCoder ranking API and tracks progress over time. Use when evaluating LLM apps, hackathon projects, or code quality.
---

# 1-Minute Codebase Evaluation

Fast, parallel evaluation of codebases using Claude CLI with structured metrics.

## Features

- ✅ **Smart Scanning**: Automatically skips `.claude/`, `node_modules/`, `.git/`, and previous `eval_*` results
- ✅ **Parallel Evaluation**: Runs multiple metrics concurrently for speed
- ✅ **Auto Ranking**: Submits to TopVibeCoder API and gets your rank
- ✅ **Progress Tracking**: Saves ranking history to track improvements over time
- ✅ **Detailed Reports**: Generates comprehensive markdown reports with citations
- ✅ **Terminal Bar Chart**: Visual score display with Unicode block characters

## Quick Start

```bash
# Evaluate current directory (use by default)
.claude/skills/1-min-eval/scripts/run_eval.sh .

# Evaluate with specific metrics
.claude/skills/1-min-eval/scripts/run_eval.sh /path/to/project --metrics impact,technical

# Full evaluation with all metrics (DO NOT use by default)
.claude/skills/1-min-eval/scripts/run_eval.sh /path/to/project --all-metrics
```

## How It Works

1. **Scan**: `scan_codebase.py` extracts repo tree and source code with line numbers
2. **Evaluate**: Runs parallel `claude -p` calls for each metric
3. **Aggregate**: Combines JSON results into a final report
4. **Visualize**: Displays terminal bar chart with scores

## Example Output

After evaluation completes, you'll see a visual bar chart:

```
==================================================
📊 Evaluation Scores
==================================================
  presentation    6.25 | ████████████░░░░░░░░
  impact          5.25 | ██████████░░░░░░░░░░
  technical       1.75 | ███░░░░░░░░░░░░░░░░░
  creativity      0.50 | █░░░░░░░░░░░░░░░░░░░
  prompt_design   0.00 | ░░░░░░░░░░░░░░░░░░░░
==================================================
```

## Available Metrics

| Metric | Description |
|--------|-------------|
| impact | Real-world problem solving, usable experience |
| technical | Architecture, robustness, LLM integration |
| creativity | Originality, novel LLM usage |
| presentation | UX clarity, onboarding, demo quality |
| prompt_design | Prompt structure, staging, constraints |
| security | Secure coding, auth, dependency hygiene |
| completion | Description-to-code alignment |
| monetization | Business potential analysis |

## Scoring Scale (0.00-10.00)

| Range | Meaning |
|-------|---------|
| 0.00-2.50 | Barely functional, major gaps |
| 2.51-4.50 | Minimal implementation, weak |
| 4.51-6.50 | Working but basic, clear gaps |
| 6.51-8.50 | Solid implementation, good quality |
| 8.51-10.00 | Excellent, production-ready |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| EVAL_PARALLEL | 4 | Number of parallel evaluations |
| EVAL_TIMEOUT | 300 | Timeout per metric (seconds) |
| EVAL_MAX_CHARS | 300000 | Max chars to include |
| EVAL_MODEL | claude-sonnet-4-5-20250929 | Model to use for evaluation |

## Ranking & Progress Tracking

Results are automatically submitted to the TopVibeCoder ranking API to get:
- Overall rank and percentile
- Per-metric rankings (individual rank for each metric)
- Comparison with nearby apps
- Historical progress tracking

Rankings are saved to `ranking_history.jsonl` in the output directory and to `.evals/history.jsonl` for unified tracking across all evaluations.

**Note:** The ranking API uses browser-like headers to bypass Cloudflare protection, ensuring reliable submissions. If the API fails, the evaluation continues and results are still saved locally.

## Output Structure

Results saved to `.evals/<timestamp>_<project>/` (hidden directory):
- `codebase.md` - Scanned source code
- `codebase.json` - Structured metadata
- `prompts/` - Generated evaluation prompts
- `results/` - JSON results per metric
- `logs/` - Execution logs
- `report.md` - Aggregated markdown report with ranking
- `ranking_history.jsonl` - Historical ranking data (one entry per evaluation)

**Note:** Evaluation results are saved to a hidden `.evals/` directory to keep your workspace clean. Add `.evals/` to your `.gitignore` if you don't want to commit evaluation results.

## Manual Usage

You can also run components individually:

```bash
# 1. Scan codebase
python3 .claude/skills/1-min-eval/scripts/scan_codebase.py ./project \
    --output /tmp/code.md --max-chars 300000

# 2. Run single metric evaluation
cat /tmp/code.md | claude -p "Evaluate for IMPACT..." --output-format json

# 3. Aggregate results
python3 .claude/skills/1-min-eval/scripts/aggregate.py \
    --input-dir ./results --output ./report.md
```

## Adding Custom Metadata

Create `metadata.json` in project root:

```json
{
  "name": "My App",
  "description": "An AI-powered tool that...",
  "author": "Your Name"
}
```

## Tips

1. **Large codebases**: Use `--max-chars 500000` for more context
2. **Debugging**: Add `--verbose` to see detailed output
3. **Resume**: Results are cached; re-run skips completed metrics
4. **Single metric**: Use `--metrics impact` for quick test
