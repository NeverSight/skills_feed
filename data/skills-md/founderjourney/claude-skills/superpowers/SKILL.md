---
name: superpowers
description: Structured software development framework for coding agents. Composable skills enforcing planning, testing, and systematic execution. Prevents code-first chaos.
original_source: https://github.com/obra/superpowers
author: obra (Jesse Vincent)
license: MIT
---

# Superpowers

A structured software development framework that transforms how coding agents approach development—preventing the "write code immediately" antipattern.

## When to Use This Skill

- Complex feature development
- Multi-file refactoring
- Test-driven development
- Code review processes
- Systematic debugging
- Team collaboration with AI

## The Philosophy

**Traditional AI coding:**
```
User: "Add auth to the app"
AI: *immediately writes 500 lines of code*
```

**Superpowers approach:**
```
User: "Add auth to the app"
AI: "Let me understand requirements first..."
   → Questions → Design → Plan → Execute → Review
```

## Core Workflow

### Phase 1: Understanding
```
1. Ask clarifying questions
2. Explore existing codebase
3. Understand constraints
4. Validate assumptions
```

### Phase 2: Design
```
1. Create isolated workspace (git branch)
2. Break work into 2-5 minute tasks
3. Define exact specifications
4. Get approval before coding
```

### Phase 3: Execution
```
1. RED: Write failing test
2. GREEN: Minimum code to pass
3. REFACTOR: Clean up
4. Review before next task
```

### Phase 4: Review
```
1. Specification compliance check
2. Code quality review
3. Integration verification
4. Branch completion decision
```

## Key Principles

### 1. Design Before Code
Never write code without understanding:
- What problem are we solving?
- What are the constraints?
- How does it fit existing code?
- What are the edge cases?

### 2. Small, Focused Tasks
Each task should be:
- Completable in 2-5 minutes
- Single responsibility
- Independently testable
- Clear success criteria

### 3. Test-First Development
```
RED → GREEN → REFACTOR
```
- Write test first
- Minimum code to pass
- Clean up afterward
- Never skip this cycle

### 4. Systematic, Not Ad-hoc
```
┌─────────────────────────────────────┐
│ Systematic          vs.    Ad-hoc  │
├─────────────────────────────────────┤
│ Plan then execute   │ Jump in      │
│ Verify with tests   │ Hope it works│
│ Review each step    │ Review at end│
│ Evidence-based      │ Assumption   │
└─────────────────────────────────────┘
```

### 5. Evidence Over Assumption
- Don't assume code works—verify
- Don't assume understanding—validate
- Don't assume completion—prove

## Skills Library

### Testing
- Unit test patterns
- Integration testing
- Test coverage analysis
- Mocking strategies

### Debugging
```
1. Reproduce the issue
2. Isolate the cause
3. Root cause analysis
4. Verify the fix
5. Prevent regression
```

### Collaboration
- **Brainstorming**: Explore options
- **Planning**: Structure approach
- **Parallel execution**: Multiple agents
- **Review**: Quality gates

### Meta-Skills
- Extending the framework
- Custom skill creation
- Workflow optimization

## How to Use

### Starting a Feature
```
I want to add user authentication.

Help me think through:
1. What auth mechanism?
2. Session vs JWT?
3. Where to store credentials?
4. What existing code to modify?
```

### During Development
```
I'm implementing the login endpoint.

Current state:
- User model exists
- Password hashing ready

Next: Create POST /login endpoint

Tests first, then implementation.
```

### Code Review
```
Review my changes:
[paste diff]

Check against:
- Original spec
- Test coverage
- Code quality
- Security concerns
```

## Example: Adding a Feature

### 1. Discovery
```
User: "Add forgot password feature"

Agent: "Before we start, let me understand:
1. How should the reset link be delivered? (email?)
2. What's the token expiry? (1 hour?)
3. Should we rate limit attempts?
4. Any existing email infrastructure?"
```

### 2. Planning
```
Tasks:
1. Create password_reset_tokens table
2. Add POST /forgot-password endpoint
3. Add POST /reset-password endpoint
4. Create email template
5. Add rate limiting middleware
```

### 3. Execution (Task 1)
```
## Task: Create password_reset_tokens table

### Test (RED)
- Test migration creates table
- Test table has correct columns

### Implementation (GREEN)
- Create migration file
- Define schema

### Verify
- Run migration
- Check table exists
```

### 4. Review
```
## Task 1 Complete

✓ Migration runs successfully
✓ Table has: id, user_id, token, expires_at
✓ Foreign key constraint works

Ready for Task 2?
```

## Best Practices

1. **Don't Rush**: Speed comes from fewer mistakes
2. **Ask Questions**: Clarify before implementing
3. **Small Steps**: Easier to verify and debug
4. **Test Everything**: Trust comes from evidence
5. **Review Often**: Catch issues early

## Integration

Available for:
- **Claude Code**: Via marketplace
- **Codex**: Plugin installation
- **OpenCode**: Direct integration

## Anti-Patterns to Avoid

- Writing code without understanding requirements
- Skipping tests "to save time"
- Large PRs with multiple concerns
- Assuming code works without verification
- Declaring done without evidence
