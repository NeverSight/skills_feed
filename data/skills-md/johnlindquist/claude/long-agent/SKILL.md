---
name: long-agent
description: Manage long-running agent sessions. Use for tracking progress in extended tasks, maintaining context across long sessions, and managing multi-step workflows.
---

# Long Agent Sessions

Manage extended agent sessions with progress tracking and context management.

## Session Management

### Initialize Session

```bash
# Create session file
SESSION_ID=$(date +%Y%m%d-%H%M%S)
SESSION_FILE=~/.claude/sessions/$SESSION_ID.md

mkdir -p ~/.claude/sessions

cat > $SESSION_FILE << EOF
# Session: $SESSION_ID
Started: $(date)
Task: [Describe task]

## Progress
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Context
[Important context to remember]

## Notes
[Running notes]
EOF

echo "Session: $SESSION_FILE"
```

### Track Progress

```bash
# Update progress
echo "- [x] Completed: [description]" >> $SESSION_FILE

# Add note
echo "### $(date +%H:%M) - [title]" >> $SESSION_FILE
echo "[notes]" >> $SESSION_FILE
```

### Resume Session

```bash
# List recent sessions
ls -lt ~/.claude/sessions/ | head -10

# View session
cat ~/.claude/sessions/SESSION_ID.md

# Continue from last checkpoint
tail -50 ~/.claude/sessions/SESSION_ID.md
```

## Progress Patterns

### Checkpoint System

```bash
#!/bin/bash
# checkpoint.sh SESSION_ID DESCRIPTION

SESSION_FILE=~/.claude/sessions/$1.md
CHECKPOINT=$2

echo "" >> $SESSION_FILE
echo "## Checkpoint: $(date +%H:%M)" >> $SESSION_FILE
echo "Status: $CHECKPOINT" >> $SESSION_FILE
echo "Can resume from here." >> $SESSION_FILE
```

### Milestone Tracking

```markdown
# Session Progress

## Milestones
- [x] M1: Environment setup
- [x] M2: Core implementation
- [ ] M3: Testing
- [ ] M4: Documentation

## Current: M3 - Testing

### Completed
- Unit tests for auth module
- Integration test setup

### In Progress
- API endpoint tests

### Blocked
- Need test fixtures for edge cases
```

## Context Management

### Save Important Context

```bash
#!/bin/bash
# save-context.sh SESSION_ID

SESSION_FILE=~/.claude/sessions/$1.md

cat >> $SESSION_FILE << 'CONTEXT'

## Critical Context (Don't Lose)

### File Locations
- Main entry: src/index.ts
- Config: src/config.ts
- Tests: tests/

### Key Decisions
- Using JWT for auth (not sessions)
- PostgreSQL for persistence
- Redis for caching

### Current State
- Auth module: complete
- API routes: 80% done
- Tests: 40% coverage
CONTEXT
```

### Context Recovery

```bash
# Get context for resumption
CONTEXT=$(grep -A 50 "## Critical Context" ~/.claude/sessions/$SESSION_ID.md)

gemini -m pro -o text -e "" "I'm resuming a long coding session. Here's the context:

$CONTEXT

Help me remember:
1. Where was I?
2. What's the next step?
3. Any gotchas to remember?"
```

## Bearings Check

### Get Your Bearings

```bash
#!/bin/bash
# bearings.sh - Where am I in this task?

echo "=== Current Session Status ==="
echo ""

# Git status
echo "### Git Status"
git status --short

echo ""
echo "### Recent Commits"
git log --oneline -5

echo ""
echo "### Modified Files"
git diff --stat HEAD~3

echo ""
echo "### TODO Items"
grep -r "TODO\|FIXME" src/ --include="*.ts" | head -10
```

### Progress Summary

```bash
# Generate progress summary
gemini -m pro -o text -e "" "Summarize progress on this session:

Session log:
$(tail -100 ~/.claude/sessions/$SESSION_ID.md)

Git activity:
$(git log --oneline -10)

Provide:
1. What's been accomplished
2. Current status
3. Remaining work
4. Estimated completion"
```

## Long Task Patterns

### Multi-Day Task

```markdown
# Multi-Day Task: [Name]

## Day 1 - [Date]
### Accomplished
- [items]

### Blocked
- [items]

### Tomorrow
- [items]

---

## Day 2 - [Date]
### Context from Yesterday
[summary]

### Accomplished
- [items]
```

### Handoff Document

When handing off to another session or agent:

```markdown
# Task Handoff

## What This Is
[Brief description]

## Current State
- [Bullet points of where things stand]

## What's Working
- [Completed items]

## What's Not Working
- [Issues/blockers]

## Next Steps
1. [Specific step]
2. [Specific step]

## Key Files
- `src/main.ts` - Entry point
- `src/auth/` - Auth module (done)
- `src/api/` - API routes (in progress)

## Commands to Know
```bash
npm run dev    # Start development
npm test       # Run tests
npm run build  # Build for production
```

## Gotchas
- [Things that might trip you up]
```

## Session Templates

### Feature Development

```bash
cat > ~/.claude/sessions/feature-template.md << 'EOF'
# Feature: [Name]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Design
[Architecture notes]

## Implementation Progress
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Documentation
- [ ] Code comments
- [ ] README update
- [ ] API docs
EOF
```

### Bug Fix

```bash
cat > ~/.claude/sessions/bugfix-template.md << 'EOF'
# Bug Fix: [Issue ID/Description]

## Symptom
[What's happening]

## Expected
[What should happen]

## Investigation
- [ ] Reproduced locally
- [ ] Found root cause
- [ ] Identified fix

## Fix
[Description of fix]

## Verification
- [ ] Fix works
- [ ] No regressions
- [ ] Tests added
EOF
```

## Best Practices

1. **Log frequently** - Update progress often
2. **Save context** - What would you need to resume?
3. **Create checkpoints** - Mark safe resume points
4. **Summarize before breaks** - Capture state of mind
5. **Use templates** - Consistent structure helps
6. **Track blockers** - Note what's waiting
7. **Handoff cleanly** - Assume fresh context next time
