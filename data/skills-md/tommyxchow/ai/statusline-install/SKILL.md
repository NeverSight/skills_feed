---
name: statusline-install
description: Install a pre-configured Claude Code statusline with model, tokens, cost, lines changed, and context usage. A batteries-included alternative to /statusline with formatting and color thresholds already defined.
argument-hint: 'Opus │ ↑15k ↓4k $1.23 │ 5m(2m) +10 -5 │ 42%'
model: haiku
context: fork
agent: statusline-setup
disable-model-invocation: true
---

# Statusline Specification

Create a statusline with this exact format:

```
Model │ ↑Tokens ↓Tokens $Cost │ Duration +Lines -Lines │ Context%
```

Example output:

```
Opus │ ↑15k ↓4k $1.23 │ 5m (2m) +156 -23 │ 42%
```

## Data Sources

| Field          | JSON Path                             |
| -------------- | ------------------------------------- |
| Model          | `.model.display_name`                 |
| Total duration | `.cost.total_duration_ms`             |
| API duration   | `.cost.total_api_duration_ms`         |
| Input tokens   | `.context_window.total_input_tokens`  |
| Output tokens  | `.context_window.total_output_tokens` |
| Cost           | `.cost.total_cost_usd`                |
| Lines added    | `.cost.total_lines_added`             |
| Lines removed  | `.cost.total_lines_removed`           |
| Context %      | `.context_window.used_percentage`     |

## Formatting Rules

**Duration**: Show as `Xs`, `Xm`, or `Xh Ym` — total time followed by API time in parentheses (always shown)

- `5m (2m)` = 5 min total, 2 min waiting for API
- `1h 15m (45m)` = 1 hour 15 min total, 45 min waiting for API
- Empty state: `0s (0s)`

**Tokens**:

- Raw number if < 1,000 → `850`
- Lowercase `k` for thousands → `15k`
- Lowercase `m` with 1 decimal for millions → `1.2m`

**Cost**:

- 4 decimal places if < $0.01 → `$0.0012`
- 2 decimal places if ≥ $0.01 → `$0.12`

**Lines changed**: Green for `+added`, Red for `-removed`

**Model name**: Reset/default terminal color (wrap with `${RESET}`)

**Separators**: Dim box-drawing character `│` (U+2502)

**General styling**: Duration, tokens, and cost should be dim

## Context % Color Thresholds

Auto-compact triggers at ~78%, so thresholds are calibrated accordingly:

| Range  | Color  | Meaning                   |
| ------ | ------ | ------------------------- |
| 0-49%  | Green  | Plenty of room            |
| 50-64% | Yellow | Getting used              |
| 65-74% | Orange | Approaching auto-compact  |
| 75%+   | Red    | Near auto-compact trigger |

## ANSI Color Definitions (Bash)

Define colors using `$'...'` syntax so escape sequences are interpreted.
Use 24-bit true color format `\033[38;2;R;G;Bm` for precise colors:

```bash
DIM=$'\033[38;2;153;153;153m'      # #999999
GREEN=$'\033[38;2;55;166;96m'      # #37A660
YELLOW=$'\033[33m'
ORANGE=$'\033[38;5;208m'
RED=$'\033[38;2;187;106;122m'      # #BB6A7A
RESET=$'\033[0m'
```

Always wrap colored output with `${COLOR}text${RESET}`.

## Null Handling

Default to `0` for numeric fields when null/missing:

- Tokens: `0`
- Cost: `$0.0000`
- Duration: `0s (0s)`
- Lines: `+0` / `-0`
- Context: `0%`

Only show `--` for non-numeric fields like model name if truly unavailable.

## Platform Notes

- **macOS/Linux**: Use bash with the ANSI definitions above
- **Windows**: Use PowerShell 7+ (`pwsh`). Use backtick syntax instead:

```powershell
$Dim = "`e[38;2;153;153;153m"      # #999999
$Green = "`e[38;2;55;166;96m"      # #37A660
$Yellow = "`e[33m"
$Orange = "`e[38;5;208m"
$Red = "`e[38;2;187;106;122m"      # #BB6A7A
$Reset = "`e[0m"
```

Install to `~/.claude/` and update `~/.claude/settings.json` with the statusLine configuration.
