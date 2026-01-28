---
name: cass-memory
description: Contextual learning system that remembers patterns and rules from past sessions. Use to get relevant context before tasks, record outcomes, and build a personal playbook of coding patterns.
---

# CASS Memory - Contextual Learning System

Build and use a personal playbook of coding patterns learned from your sessions.

## Prerequisites

The `cm` CLI should be available (part of cass-memory system).

Initialize:
```bash
cm init
# Or with a starter playbook
cm init --starter typescript
cm init --starter react
cm init --starter python
cm init --starter go
```

## CLI Reference

### Get Context for a Task
```bash
# THE main command - get relevant rules before starting work
cm context "Description of your task" --json
```

This returns:
- Relevant rules from your playbook
- Anti-patterns to avoid
- History snippets from similar past work

### Reflection (Extract Patterns)
```bash
# Run reflection on recent sessions
cm reflect --json

# Specify lookback period
cm reflect --days 7 --json
cm reflect --days 30 --json
```

### Playbook Management
```bash
# List all rules
cm playbook list --json

# Get specific rule details
cm playbook get b-8f3a2c --json

# Add a new rule
cm playbook add "Always use optional chaining for nested object access" --json
```

### Feedback on Rules
```bash
# Mark rule as helpful
cm mark b-8f3a2c --helpful --json
cm mark b-8f3a2c --helpful --reason "Prevented null error" --json

# Mark rule as harmful
cm mark b-8f3a2c --harmful --json
cm mark b-8f3a2c --harmful --reason "Caused false positive" --json
```

### Record Session Outcomes
```bash
# Record success
cm outcome --status success --json
cm outcome --status success --rules "b-8f3a2c,b-4d2e1f" --json

# Record failure
cm outcome --status failure --text "Build failed due to type error" --json

# Mixed results
cm outcome --status mixed --text "Partial completion" --json
```

### Statistics
```bash
# Get playbook stats
cm stats --json
```

### Top Rules
```bash
# Show most effective rules
cm top --json
cm top 5 --json
cm top 20 --json
```

### Health Check
```bash
# Check system health
cm doctor --json

# Auto-fix issues
cm doctor --fix --json
```

### Find Stale Rules
```bash
# Rules without recent feedback
cm stale --json
cm stale --days 30 --json
cm stale --days 60 --json
```

### Validate Rules
```bash
# Validate a proposed rule against history
cm validate "Proposed rule text" --json
```

### Explain Rule Origin
```bash
# Show evidence and reasoning for a rule
cm why b-8f3a2c --json
```

### Usage Statistics
```bash
cm usage --json
```

### Starter Playbooks
```bash
# List available starters
cm starters --json
```

## Workflow Patterns

### Session Start
```bash
# Get context before starting a task
cm context "Implement user authentication with JWT" --json
```

### During Work
When a rule helps:
```bash
cm mark b-8f3a2c --helpful --json
```

When a rule leads astray:
```bash
cm mark b-8f3a2c --harmful --reason "Not applicable to this framework" --json
```

### Session End
```bash
# Record outcome
cm outcome --status success --rules "b-8f3a2c,b-4d2e1f" --json
```

### Periodic Maintenance
```bash
# Weekly: Run reflection to extract new patterns
cm reflect --days 7 --json

# Monthly: Review stale rules
cm stale --days 30 --json

# Check system health
cm doctor --json
```

### Building Your Playbook
```bash
# Manually add a pattern you've learned
cm playbook add "Use React.memo() for components receiving complex objects as props" --json

# After adding, use it in context queries
cm context "Create a list component with filtering" --json
```

## Rule Lifecycle

1. **Creation** - Rules emerge from reflection or manual addition
2. **Usage** - Rules surface in context queries
3. **Feedback** - Mark as helpful/harmful based on experience
4. **Evolution** - High-feedback rules rise, low-feedback rules become stale
5. **Retirement** - Stale rules get reviewed and pruned

## Best Practices

1. **Always get context first** - Run `cm context "task"` before starting work
2. **Provide feedback** - Mark rules as helpful/harmful
3. **Record outcomes** - Track session success/failure
4. **Run reflection regularly** - Weekly reflection extracts new patterns
5. **Review stale rules** - Don't let old rules accumulate
6. **Add rules manually** - When you learn something important

## Integration Tips

### Pre-Task Context
Before any significant coding task:
```bash
CONTEXT=$(cm context "Your task description" --json)
# Use context to inform your approach
```

### Post-Session Recording
At end of coding session:
```bash
cm outcome --status success --text "Completed feature X" --json
```
