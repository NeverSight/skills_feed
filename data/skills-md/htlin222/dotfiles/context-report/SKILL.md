---
name: context-report
description: Analyze Claude Code context efficiency for current project. Invoke when evaluating session efficiency or optimizing Claude Code usage.
allowed-tools: Bash(jq:*), Bash(find:*), Bash(wc:*), Bash(du:*), Bash(sort:*), Bash(uniq:*), Bash(head:*), Bash(cat:*), Bash(basename:*), Bash(dirname:*), Bash(bc:*), Bash(date:*), Bash(ls:*), Bash(tr:*)
---

# Context efficiency report

Analyze the Claude Code JSONL session data for the current project to generate a context efficiency report.

## When to invoke

- When reviewing Claude Code session efficiency
- To understand model usage patterns
- When optimizing for cost reduction
- After completing a project to review usage

## Instructions

### Project path detection

The current working directory is: `$ARGUMENTS` (if provided) or `$CWD`

Convert the path to the Claude projects folder format:

- Replace `/` with `-`
- The projects folder is at: `~/.dotfiles/claude.symlink/projects/`

### Analysis script

Run this analysis for the current project:

```bash
#!/bin/bash
CWD="${ARGUMENTS:-$(pwd)}"
PROJECT_KEY=$(echo "$CWD" | sed 's|/|-|g; s|\.|-|g')
PROJECTS_BASE="$HOME/.dotfiles/claude.symlink/projects"
PROJECT_DIR="$PROJECTS_BASE/$PROJECT_KEY"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "No session data found for: $CWD"
  echo "Looking in: $PROJECT_DIR"
  exit 1
fi

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║              Context Efficiency Report: $(basename "$CWD" | head -c 20)"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo "Project: $CWD"
echo ""

# Session counts
session_count=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" ! -name "agent-*.jsonl" 2>/dev/null | wc -l | tr -d ' ')
agent_count=$(find "$PROJECT_DIR" -maxdepth 1 -name "agent-*.jsonl" 2>/dev/null | wc -l | tr -d ' ')
echo "📁 SESSIONS"
echo "────────────────────────────────────────────────────────────────────"
echo "Main Sessions: $session_count"
echo "Agent Sessions: $agent_count"
if [ "$session_count" -gt 0 ]; then
  ratio=$(echo "scale=2; $agent_count / $session_count" | bc)
  echo "Delegation Ratio: ${ratio}:1"
fi
echo ""

# Model usage
echo "🤖 MODEL USAGE"
echo "────────────────────────────────────────────────────────────────────"
find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -size +1k -exec cat {} + 2>/dev/null | \
  jq -r 'select(.message.model != null) | .message.model' 2>/dev/null | \
  sort | uniq -c | sort -rn
echo ""

# Tool usage
echo "🔧 TOOL USAGE"
echo "────────────────────────────────────────────────────────────────────"
find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -size +1k -exec cat {} + 2>/dev/null | \
  jq -r '.message.content[]? | select(.type == "tool_use") | .name' 2>/dev/null | \
  sort | uniq -c | sort -rn | head -15
echo ""

# Size
echo "📊 DATA SIZE"
echo "────────────────────────────────────────────────────────────────────"
total_size=$(du -sh "$PROJECT_DIR" 2>/dev/null | cut -f1)
msg_count=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -exec cat {} + 2>/dev/null | wc -l | tr -d ' ')
echo "Total Size: $total_size"
echo "Message Records: $msg_count"
echo ""

# Collect tool data once
all_tools=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -size +1k -exec cat {} + 2>/dev/null | jq -r '.message.content[]? | select(.type == "tool_use") | .name' 2>/dev/null)
all_models=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.jsonl" -size +1k -exec cat {} + 2>/dev/null | jq -r '.message.model // empty' 2>/dev/null)

# Model counts
opus=$(echo "$all_models" | grep -c "opus" || echo 0)
sonnet=$(echo "$all_models" | grep -c "sonnet" || echo 0)
haiku=$(echo "$all_models" | grep -c "haiku" || echo 0)
model_total=$((opus + sonnet + haiku))

# Tool counts
bash_count=$(echo "$all_tools" | grep -c "^Bash$" || echo 0)
grep_count=$(echo "$all_tools" | grep -c "^Grep$" || echo 0)
glob_count=$(echo "$all_tools" | grep -c "^Glob$" || echo 0)
todo_count=$(echo "$all_tools" | grep -c "^TodoWrite$" || echo 0)
task_count=$(echo "$all_tools" | grep -c "^Task$" || echo 0)

# Calculate scores
score=0
warnings=""

# 1. Model score (30 pts): 50% opus = 30pts, 100% opus = 0pts
if [ "$model_total" -gt 0 ]; then
  opus_pct=$((opus * 100 / model_total))
  model_score=$((30 - (opus_pct - 50) * 30 / 50))
  [ "$model_score" -lt 0 ] && model_score=0
  [ "$model_score" -gt 30 ] && model_score=30
  score=$((score + model_score))
  [ "$opus_pct" -gt 80 ] && warnings="${warnings}⚠️  Opus ${opus_pct}% - apply --model haiku for exploration\n"
else
  opus_pct=0
  model_score=15
  score=$((score + model_score))
fi

# 2. Delegation score (25 pts): 3:1 = 25pts, 0:1 = 0pts
if [ "$session_count" -gt 0 ]; then
  delegation_ratio_x100=$((agent_count * 100 / session_count))
  delegation_score=$((delegation_ratio_x100 * 25 / 300))
  [ "$delegation_score" -gt 25 ] && delegation_score=25
  score=$((score + delegation_score))
  [ "$delegation_ratio_x100" -lt 100 ] && warnings="${warnings}⚠️  Low delegation - apply Task agents more\n"
else
  delegation_score=0
fi

# 3. Tool efficiency score (25 pts): native tools vs bash
native_search=$((grep_count + glob_count))
if [ "$bash_count" -gt 0 ]; then
  tool_ratio_x100=$((native_search * 100 / bash_count))
  tool_score=$((tool_ratio_x100 * 25 / 50))
  [ "$tool_score" -gt 25 ] && tool_score=25
  score=$((score + tool_score))
  [ "$tool_ratio_x100" -lt 10 ] && warnings="${warnings}⚠️  Bash/Native ratio - prefer Grep/Glob tools\n"
else
  tool_score=25
  score=$((score + tool_score))
fi

# 4. TodoWrite score (20 pts): task tracking
if [ "$msg_count" -gt 0 ]; then
  todo_ratio_x1000=$((todo_count * 1000 / msg_count))
  todo_score=$((todo_ratio_x1000 * 20 / 50))
  [ "$todo_score" -gt 20 ] && todo_score=20
  score=$((score + todo_score))
  [ "$todo_count" -eq 0 ] && warnings="${warnings}⚠️  No TodoWrite - apply for task tracking\n"
else
  todo_score=0
fi

# Output
echo "📈 EFFICIENCY SCORE"
echo "────────────────────────────────────────────────────────────────────"
echo ""
echo "  ┌─────────────────────────────────────┐"
printf "  │         SCORE: %3d / 100            │\n" "$score"
echo "  └─────────────────────────────────────┘"
echo ""
echo "  Breakdown:"
printf "    Model efficiency:    %2d/30  (Opus %d%%)\n" "$model_score" "$opus_pct"
del_ratio=$(echo "scale=1; $agent_count / ($session_count + 0.001)" | bc)
printf "    Task delegation:     %2d/25  (ratio %s:1)\n" "$delegation_score" "$del_ratio"
printf "    Tool efficiency:     %2d/25  (Grep+Glob: %d, Bash: %d)\n" "$tool_score" "$native_search" "$bash_count"
printf "    Task tracking:       %2d/20  (TodoWrite: %d)\n" "$todo_score" "$todo_count"
echo ""

if [ -n "$warnings" ]; then
  echo "  Warnings:"
  printf "  $warnings"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "Generated: $(date '+%Y-%m-%d %H:%M')"
```

## Output

Present the results and provide recommendations based on:

1. Model usage distribution (aim for <50% Opus)
2. Tool efficiency (Grep > bash grep, Glob > bash find)
3. Task delegation ratio (aim for >2:1)
4. TodoWrite usage for task tracking
