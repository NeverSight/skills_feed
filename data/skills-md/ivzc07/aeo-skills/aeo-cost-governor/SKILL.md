---
name: aeo-cost-governor
description: Track token usage and enforce budget limits. Optional skill for cost-conscious projects.
---

# AEO Cost Governor

**Purpose:** Track token usage and enforce budget limits. Optional skill for cost-conscious projects.

## Configuration

Create budget config at `$PAI_DIR/USER/aeo-budget.json`:

```json
{
  "daily_budget_usd": 10.00,
  "per_task_budget_usd": 2.00,
  "alert_threshold_percent": 80,
  "hard_limit_percent": 100,
  "enable_tracking": true
}
```

**Defaults (if no config):**
- Daily budget: $10.00
- Per-task budget: $2.00
- Alert at: 80%
- Hard limit: 100%

## Model Pricing (per 1M tokens)

**Claude Models (Jan 2025):**
- **Claude Opus 4:** Input $15.00, Output $75.00
- **Claude Sonnet 4.5:** Input $3.00, Output $15.00
- **Claude Haiku 4:** Input $0.80, Output $4.00

**Cost Calculation Formula:**
```javascript
cost_usd = (input_tokens / 1_000_000 * input_price) + (output_tokens / 1_000_000 * output_price)
```

## When to Track

Track costs during:
- Tool execution (PreToolUse hook)
- Task completion
- Session end

## Cost Tracking

### Per-Task Tracking

When a task starts:

```bash
# Initialize task cost tracking
echo '{
  "task_id": "unique-id",
  "task_description": "Add user authentication",
  "start_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "model": "claude-sonnet-4.5",
  "budget_usd": 2.00,
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "cost_usd": 0.00
  }
}' > ~/.claude/MEMORY/aeo-task-cost.json
```

After each tool use:

```bash
# Update task cost
# (Read existing, add new usage, write back)
jq '.usage.cost_usd += 0.15' ~/.claude/MEMORY/aeo-task-cost.json > /tmp/cost.json
mv /tmp/cost.json ~/.claude/MEMORY/aeo-task-cost.json
```

### Daily Tracking

Append to daily log:

```bash
echo '{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "date": "$(date -u +%Y-%m-%d)",
  "task_id": "unique-id",
  "model": "claude-sonnet-4.5",
  "input_tokens": 1250,
  "output_tokens": 850,
  "cost_usd": 0.15
}' >> ~/.claude/MEMORY/aeo-costs.jsonl
```

## Budget Checks

### Check Before Task

```bash
# Get today's total cost
today_total=$(jq -s "map(select(.date == \"$(date -u +%Y-%m-%d)\")) | map(.cost_usd) | add" \
  ~/.claude/MEMORY/aeo-costs.jsonl)

# Get budget
budget=$(jq '.daily_budget_usd' ~/.claude/USER/aeo-budget.json)

# Calculate percentage
percent=$(echo "$today_total / $budget * 100" | bc)

# Check if over limit
if (( $(echo "$percent >= 100" | bc -l) )); then
  echo "❌ BUDGET EXCEEDED - $today_total spent of $budget"
  exit 1
fi
```

### Check During Task

After each operation:

```bash
# Read task cost
task_cost=$(jq '.usage.cost_usd' ~/.claude/MEMORY/aeo-task-cost.json)
task_budget=$(jq '.per_task_budget_usd' ~/.claude/USER/aeo-budget.json)

# Check if over task budget
if (( $(echo "$task_cost > $task_budget" | bc -l) )); then
  echo "⚠️ TASK BUDGET EXCEEDED - $task_cost spent of $task_budget"
  # Invoke aeo-escalation
fi
```

## Alerts

### Warning Alert (80%)

```
⚠️ COST ALERT - 80% BUDGET CONSUMED

Daily Budget: $10.00
Used: $8.47 (84.7%)
Remaining: $1.53

Tasks completed today: 7
Average cost per task: $1.21

Options:
1. Continue anyway - Proceed with current task
2. Pause and review - Assess completed work
3. Switch to cheaper model - Use Haiku instead of Sonnet

Recommended: Option 3 - Switch to Haiku for routine tasks

Your choice (1-3):
```

### Hard Limit (100%)

```
❌ BUDGET EXCEEDED - HARD LIMIT REACHED

Daily Budget: $10.00
Used: $10.23 (102.3%)
Overage: $0.23

Action Required:
• All tasks blocked until budget resets
• Budget resets at midnight UTC
• Consider increasing daily_budget_usd in config

Current time: $(date -u +%H:%M UTC)
Time until reset: [hours remaining]

Options:
1. Wait for reset - Resume at midnight UTC
2. Increase budget - Modify aeo-budget.json
3. Override limit - Not recommended

Contact: [Admin email if configured]
```

## Model Selection Guidelines

**Use Opus for:**
- Complex architectural decisions
- Multi-file refactoring with deep implications
- Critical security analysis
- Performance optimization requiring deep reasoning

**Use Sonnet for:**
- Feature implementation
- Bug fixing
- Code review
- Most development tasks

**Use Haiku for:**
- Documentation generation
- Simple code modifications
- Test writing
- Routine refactoring

## Cost Optimization Tips

1. **Use Haiku for documentation** - Saves ~85% on docs
2. **Provide clear specs** - Reduces back-and-forth
3. **Batch similar tasks** - Amortize context loading
4. **Use targeted file reads** - Instead of reading entire codebase
5. **Enable caching** - Reuse previous responses when possible

## Reporting

### Daily Summary

Generate at end of day:

```bash
# Get today's costs
jq -s "
  select(.date == \"$(date -u +%Y-%m-%d)\")
  | {
      total_cost: map(.cost_usd) | add,
      task_count: length,
      avg_cost: (map(.cost_usd) | add / length),
      by_model: group_by(.model) | map({
          model: .[0].model,
          cost: map(.cost_usd) | add,
          tasks: length
      })
    }
" ~/.claude/MEMORY/aeo-costs.jsonl
```

**Output:**
```json
{
  "total_cost": 8.47,
  "task_count": 7,
  "avg_cost": 1.21,
  "by_model": [
    {"model": "claude-sonnet-4.5", "cost": 6.32, "tasks": 5},
    {"model": "claude-haiku-4", "cost": 2.15, "tasks": 2}
  ]
}
```

### Weekly Analysis

```bash
# Last 7 days
jq -s "
  group_by(.date)
  | map({
      date: .[0].date,
      total_cost: map(.cost_usd) | add,
      task_count: length
    })
  | .[-7:]
" ~/.claude/MEMORY/aeo-costs.jsonl
```

## Integration

**Hooks Integration:**

```javascript
// In PreToolUse hook
if (cost_governor_enabled) {
  const cost = estimate_tool_cost(tool_name, tool_input);
  const daily_total = get_daily_total();
  const remaining = budget - daily_total;

  if (cost > remaining) {
    invoke_skill('aeo-escalation', {
      type: 'cost_limit',
      cost: cost,
      remaining: remaining
    });
  }
}
```

## Best Practices

**DO:**
- Set realistic budgets based on usage patterns
- Use alerts to stay informed before hitting limits
- Track costs per task to identify expensive operations
- Use cheaper models when appropriate
- Review cost reports weekly to optimize spending

**DON'T:**
- Set budgets too low and constantly hit limits
- Ignore alerts until hard limit is reached
- Use Opus for routine tasks
- Forget to account for input tokens (not just output)
- Track only at session end - track during tasks too

## Example Session

```
User: /aeo
User: Refactor the authentication system

AEO-Core: [Calculating confidence...]
          [Invokes aeo-cost-governor]

Cost Governor: Checking budget...

              Daily Budget: $10.00
              Used: $8.47 (84.7%)
              Remaining: $1.53
              Task Estimate: ~$2.50

              ⚠️ ALERT: Task may exceed daily budget

Options:
1. Continue anyway - May exceed budget
2. Use Haiku instead - Estimated cost ~$0.50
3. Break into smaller tasks - Spread across multiple days

Recommended: Option 3 - Break into smaller tasks

User: 3

Cost Governor: [Recording decision]
              Suggesting subtasks:
              1. Extract auth logic to service (Day 1)
              2. Implement JWT tokens (Day 2)
              3. Migrate existing sessions (Day 3)

AEO-Core: Proceeding with subtask 1: Extract auth logic
```

## Cleanup

**Archive old cost logs:**
```bash
# Keep last 90 days, archive older
cat ~/.claude/MEMORY/aeo-costs.jsonl | \
  jq -r 'select(.date >= "$(date -u -d '90 days ago' +%Y-%m-%d)")' \
  > /tmp/costs-recent.jsonl

cat ~/.claude/MEMORY/aeo-costs.jsonl | \
  jq -r 'select(.date < "$(date -u -d '90 days ago' +%Y-%m-%d)")' \
  > ~/.claude/MEMORY/aeo-costs.archive.jsonl

mv /tmp/costs-recent.jsonl ~/.claude/MEMORY/aeo-costs.jsonl
```

## Disable Cost Tracking

To disable cost tracking for a project:

```json
{
  "enable_tracking": false
}
```

Or delete the config file entirely - AEO will use defaults but won't enforce limits.
