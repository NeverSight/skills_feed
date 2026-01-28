---
name: executing-plans
description: Structured approach for implementing architect-provided plans through controlled batch execution with review checkpoints - execute in batches (default 3 tasks), verify each step, stop on blockers; don't force through blockers
version: 2025-11-04
related_skills:
  - writing-plans (creates the plans you execute)
  - starwards-tdd (use TDD for each task)
  - starwards-verification (verify batch completion)
  - using-superpowers (announce skill usage)
---

# Executing Implementation Plans

## Overview

Structured approach for implementing architect-provided plans through controlled batch execution with review checkpoints.

## Process Steps

### 1. Load and Review

- Read the plan completely
- Understand the full scope
- Raise concerns BEFORE starting
- Ask questions about unclear steps
- Verify you have all dependencies

### 2. Batch Execution

- Execute tasks in batches (default: 3 tasks per batch)
- Complete each task fully before moving to next
- Follow verification steps built into each task
- Commit after each task as specified in plan

### 3. Checkpoint Reviews

- After each batch completes, report results
- Show what was accomplished
- Report any issues or deviations
- Wait for feedback before proceeding to next batch

### 4. Completion Protocol

Upon finishing all tasks:
- Verify all tests pass
- Check nothing was skipped
- Transition to finishing-a-development-branch skill to finalize

## Critical Safeguards

**STOP IMMEDIATELY when encountering:**
- Missing dependencies
- Failed tests that can't be resolved
- Unclear instructions
- Blockers of any kind

**Don't:**
- Force through blockers
- Make assumptions
- Skip verification steps
- Modify plan mid-execution

**Do:**
- Stop and ask
- Report the blocker clearly
- Wait for guidance

## Plan Adherence

- Follow plan steps exactly
- Don't skip verification procedures
- Maintain communication checkpoints
- Treat plan updates as requiring return to review phase

## Batch Size

Default: 3 tasks per batch

Adjust based on:
- Task complexity
- Interdependencies
- Your confidence level
- Feedback from reviewer

## When to Stop

- Encountering blockers
- Tests failing unexpectedly
- Instructions unclear
- Need architectural decision
- Pattern doesn't match reality

## Integration with Other Skills

- **writing-plans** - Creates the plans you execute
- **finishing-a-development-branch** - Final verification after all tasks complete
- **verification-before-completion** - Use before claiming batch is complete
