---
name: learning
description: Self-improving agent patterns. Use when detecting corrections, proposing rules, or managing learned behaviors.
---

# Claude Learner - Self-Improvement Skill

You have access to claude-learner, a system that turns corrections into permanent rules.

## When to Use

- User corrects you ("No, don't do X, do Y instead")
- You make a repeated mistake
- User expresses a preference
- A better pattern is discovered

## Available Commands

| Command | What It Does |
|---------|--------------|
| `/learner:status` | Check daemon and rules status |
| `/learner:rules` | List all rules |
| `/learner:approve <id>` | Approve a pending rule |
| `/learner:reject <id>` | Reject a pending rule |
| `/learner:start` | Start the learning daemon |
| `/learner:stop` | Stop the learning daemon |

## MCP Tools

If MCP is connected, you have these tools:

- `log_correction` - Log a correction event
- `propose_rule` - Propose a new rule
- `get_rules` - Get active rules
- `get_pending_rules` - Get rules awaiting approval
- `approve_rule` - Approve a rule
- `reject_rule` - Reject a rule
- `get_stats` - Get learning statistics

## Best Practices

1. **Detect corrections automatically** - When user says "actually...", "no, use...", "don't do X", log it
2. **Propose rules for patterns** - If you see repeated corrections, propose a rule
3. **Check rules periodically** - Use `get_rules` to remind yourself of learned behaviors
4. **Don't over-rule** - Not every correction needs a permanent rule

## Example Flow

```
User: "Don't use rm, use trash instead"

1. Log correction: log_correction({ 
     pattern: "using rm command",
     correction: "use trash instead of rm",
     context: "file deletion"
   })

2. If pattern repeats, propose rule: propose_rule({
     content: "Always use `trash` instead of `rm` for file deletion",
     trigger: "rm command usage"
   })

3. Rule goes to pending → user approves → permanently active
```
