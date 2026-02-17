---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

## When to Use

**Use when:**

- Have implementation plan
- Tasks are mostly independent
- Want to stay in current session
- Want fast iteration with review checkpoints

**vs. Executing Plans (parallel session):**

- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task: spec compliance first, then code quality
- Faster iteration (no human-in-loop between tasks)

## The Process

### Setup

1. **Read plan, extract all tasks** with full text and context
2. **Create TodoWrite** with all tasks

### Per Task

1. **Dispatch implementer subagent** with full task text + context
2. **If subagent asks questions** - Answer, provide context
3. **Implementer implements, tests, commits, self-reviews**
4. **Dispatch spec reviewer subagent** - Verify code matches spec
5. **If spec issues** - Implementer fixes, reviewer re-reviews
6. **Dispatch code quality reviewer subagent** - Review for quality
7. **If quality issues** - Implementer fixes, reviewer re-reviews
8. **Mark task complete in TodoWrite**

### After All Tasks

1. **Dispatch final code reviewer** for entire implementation
2. **Use ltk:finishing-a-development-branch** to complete

## Two-Stage Review

**Stage 1: Spec Compliance**

- Does implementation match spec EXACTLY?
- Nothing missing?
- Nothing extra (over-building)?

**Stage 2: Code Quality** (only after spec passes)

- Clean code?
- Good test coverage?
- Maintainable?

## Advantages

**vs. Manual execution:**

- Subagents follow TDD naturally
- Fresh context per task (no confusion)
- Parallel-safe (subagents don't interfere)
- Subagent can ask questions (before AND during work)

**Quality gates:**

- Self-review catches issues before handoff
- Two-stage review: spec compliance, then code quality
- Review loops ensure fixes actually work

## Red Flags

**Never:**

- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Dispatch multiple implementation subagents in parallel (conflicts)
- Make subagent read plan file (provide full text instead)
- Skip scene-setting context
- Ignore subagent questions
- Accept "close enough" on spec compliance
- Skip review loops
- **Start code quality review before spec compliance passes**
- Move to next task while either review has open issues

**If subagent asks questions:**

- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

**If reviewer finds issues:**

- Implementer (same subagent) fixes them
- Reviewer reviews again
- Repeat until approved

## Integration

**Required workflow skills:**

- **ltk:writing-plans** - Creates the plan this skill executes
- **ltk:requesting-code-review** - Code review template for reviewer subagents
- **ltk:finishing-a-development-branch** - Complete development after all tasks

**Subagents should use:**

- **ltk:test-driven-development** - Subagents follow TDD for each task

**Alternative workflow:**

- **ltk:executing-plans** - Use for parallel session instead of same-session execution
