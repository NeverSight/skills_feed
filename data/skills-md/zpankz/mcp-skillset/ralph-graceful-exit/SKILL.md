---
name: ralph-graceful-exit
description: |
  Detects Ralph Loop completion beyond <promise> tags. Use when checking if a task
  is complete, verifying completion status, or detecting graceful exit conditions.
  Implements 4-signal detection: test loops, done signals, completion indicators,
  and fix plan verification.
allowed-tools: Read, Grep, Bash
model: haiku
context: fork
agent: ralph-domain-agent
user-invocable: false
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "$HOME/.claude/hooks/ralph-activity-log.sh"
---

# Ralph Graceful Exit

## Purpose

Detect when a Ralph Loop iteration has truly completed its task, beyond just the `<promise>DONE</promise>` tag. This skill implements 4-signal detection to verify genuine completion.

## Integrations

| Type | References |
|------|------------|
| hooks | ralph-circuit-breaker, ralph-rate-limiter, ralph-activity-log |
| plugins | ralph-loop@claude-plugins-official |

## 4-Signal Detection

| Signal | Threshold | Detection Method |
|--------|-----------|------------------|
| test_loops | ≥3 consecutive | Only running tests, no code changes |
| done_signals | ≥2 occurrences | "done", "complete", "finished" in output |
| completion_indicators | ≥2 patterns | Strong completion language patterns |
| fix_plan_check | all items ✓ | All @fix_plan.md items checked |

## Detection Logic

When evaluating completion:

1. **Check activity log** for test-only iterations
   ```bash
   grep -c "test\|pytest\|jest\|npm test" ~/.ralph-state/activity.log
   ```

2. **Scan recent output** for done_signals patterns
   - "done", "complete", "finished", "all tests pass"
   - "implementation complete", "task finished"

3. **Look for completion_indicators** in conversation
   - Strong completion language
   - Summary of what was accomplished
   - No pending TODO items mentioned

4. **Verify fix_plan** if exists
   - Check if @fix_plan.md exists
   - Verify all checkbox items are checked `[x]`

## Exit Recommendation

If ≥2 signals detected, recommend outputting:

```
<promise>DONE</promise>
```

## Signal Weights

| Signal | Weight | Confidence |
|--------|--------|------------|
| fix_plan_check (all ✓) | 1.0 | High |
| test_loops ≥3 | 0.8 | High |
| done_signals ≥2 | 0.6 | Medium |
| completion_indicators ≥2 | 0.5 | Medium |

Total weight ≥1.5 → Strong recommendation to exit
Total weight ≥1.0 → Suggest checking completion status
