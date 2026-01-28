---
name: ralph-invoke
description: |
  Allows Claude to directly start Ralph-Wiggum autonomous loops without user commands.
  Use when user asks to "start a ralph loop", "run ralph", "keep working until done",
  or when a complex task would benefit from multiple iterations.
allowed-tools: Read, Bash
model: haiku
context: fork
agent: ralph-domain-agent
user-invocable: false
---

# Ralph Invoke Skill

**Allows Claude to directly start Ralph-Wiggum autonomous loops without user commands.**

## Prerequisites

The `ralph-wiggum` plugin must be installed and enabled:
```
/plugin install ralph-wiggum@claude-code-plugins
/plugin enable ralph-wiggum@claude-code-plugins
```

## Triggers

Use this skill when:
- User asks to "start a ralph loop" or "run ralph"
- User wants autonomous iteration on a task
- User says "keep working until done" or "iterate until complete"
- A complex task would benefit from multiple iterations
- User explicitly requests Claude to invoke ralph

## How to Start a Ralph Loop

Run this bash command:

```bash
"$HOME/.claude/plugins/cache/claude-code-plugins/ralph-wiggum/1.0.0/scripts/setup-ralph-loop.sh" \
  "<TASK_DESCRIPTION>" \
  --max-iterations <N> \
  --completion-promise "<PROMISE_TEXT>"
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| TASK_DESCRIPTION | Yes | - | The task to work on |
| --max-iterations | Recommended | unlimited | Safety limit (use 20-100) |
| --completion-promise | Recommended | null | Text to output when truly done |

### Example Invocations

**Simple task:**
```bash
"$HOME/.claude/plugins/cache/claude-code-plugins/ralph-wiggum/1.0.0/scripts/setup-ralph-loop.sh" \
  "Fix all TypeScript type errors" \
  --max-iterations 50 \
  --completion-promise "ALL_ERRORS_FIXED"
```

**Complex refactor:**
```bash
"$HOME/.claude/plugins/cache/claude-code-plugins/ralph-wiggum/1.0.0/scripts/setup-ralph-loop.sh" \
  "Migrate all API handlers to the new v2 pattern" \
  --max-iterations 100 \
  --completion-promise "MIGRATION_COMPLETE"
```

## How the Loop Works

1. **Claude runs the setup script** → Creates state file at `.claude/ralph-loop.local.md`
2. **Claude works on the task** → Normal operation
3. **Claude tries to exit** → Stop hook intercepts
4. **Hook re-injects prompt** → Claude continues with same task
5. **Repeat** until:
   - Max iterations reached, OR
   - Claude outputs `<promise>PROMISE_TEXT</promise>`

## Completing the Loop

When the task is genuinely complete, output the completion promise in XML tags:

```
<promise>ALL_ERRORS_FIXED</promise>
```

**CRITICAL RULES:**
- Only output the promise when the statement is TRUE
- Do NOT lie to exit the loop
- Do NOT output false promises even if stuck
- Trust the process - if stuck, iterate and try differently

## Canceling a Loop

If needed, cancel with:
```bash
rm .claude/ralph-loop.local.md
```

Or use: `/ralph-wiggum:cancel-ralph`

## Best Practices

1. **Always set --max-iterations** - Prevents runaway costs (50-100 is reasonable)
2. **Use specific completion promises** - "ALL_TESTS_PASS" not "DONE"
3. **Include success criteria in task** - Be explicit about what "done" means
4. **Monitor progress** - `head -10 .claude/ralph-loop.local.md`
5. **Start small** - Test with 3-5 iterations first

## Cost Warning

Autonomous loops consume tokens rapidly. A 50-iteration loop can cost $50-100+ in API usage. Always use --max-iterations as a safety net.

## Why This Skill Exists

The official ralph-wiggum plugin requires users to run `/ralph-loop` commands. This skill enables Claude to invoke loops directly, enabling:
- Claude-initiated iteration on complex tasks
- Programmatic loop triggers from other skills/agents
- Automated workflows without manual commands
