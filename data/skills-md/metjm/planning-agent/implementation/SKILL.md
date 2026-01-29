---
name: implementation
description: Expert implementation agent that executes approved plans. Implements features step-by-step following the plan precisely. Use when you have an approved plan and need to implement it.
---

# Implementation Agent

Expert implementation agent that executes approved plans using parallel sub-agents for maximum efficiency.

## Overview

This skill uses a parallel sub-agent strategy:
1. Analyze the plan and identify all work items
2. Launch sub-agents in parallel to implement changes (no build/test during this phase)
3. Fix integration issues after all parallel work completes
4. Launch sub-agents in parallel to validate each part of the plan
5. If validation finds gaps, loop back to step 1

## Implementation Process

### Phase 1: Analyze the Plan

Read the plan file completely and create a structured breakdown:

1. **List all files** that must be created or modified
2. **Group changes** into independent work units (changes that don't depend on each other)
3. **Identify dependencies** - which changes must happen before others
4. **Create work items** - each work item should be a self-contained unit that one sub-agent can complete

Output a todo list with all work items before proceeding.

### Phase 2: Parallel Implementation

Launch sub-agents to implement changes in parallel:

1. **Batch independent work** - Group work items that can run simultaneously (aim for ~10 parallel agents when possible)
2. **Instruct sub-agents clearly**:
   - Give each agent its specific files and changes to make
   - Tell agents: "Do NOT run build, lint, or tests - they won't pass until all work is complete"
   - Provide relevant context from the plan
3. **Use the Task tool** with `subagent_type: "general-purpose"` for each work item
4. **Run dependent work after** - Once a batch completes, start the next batch that depended on it

Example sub-agent invocation:
```
Task tool with:
- subagent_type: "general-purpose"
- prompt: "Implement [specific change] in [file]. Context from plan: [relevant section]. Do NOT run build/lint/tests."
```

### Phase 3: Fix Integration Issues

After all parallel implementation completes:

1. **Run the build** - `cargo build` or equivalent
2. **Run lints** - `cargo clippy` or equivalent
3. **Fix any errors** - Resolve compilation errors, type mismatches, missing imports
4. **Run tests** - Fix any test failures

This phase runs sequentially since issues often cascade.

### Phase 4: Parallel Validation

Launch sub-agents to validate the implementation:

1. **Create validation tasks** - One task per major section of the plan
2. **Launch validation agents in parallel** with prompts like:
   - "Verify that [plan section X] has been fully implemented. Check [specific files]. Report any gaps or missing functionality."
3. **Collect validation results** from all agents

### Phase 5: Loop or Complete

Based on validation results:

- **If all validations pass** → Implementation complete
- **If gaps found** → Create new work items for the gaps and return to Phase 2

## Sub-Agent Guidelines

When launching sub-agents:

- **Be specific** - Give exact file paths and precise instructions
- **Include context** - Copy relevant plan sections into the prompt
- **Set boundaries** - "Only modify these files: X, Y, Z"
- **Suppress noise** - "Do not run build/test commands"

## Constraints

- **DO** follow the plan exactly as written
- **DO** use absolute paths for all file operations
- **DO** maximize parallelism for independent work
- **DO** fix unrelated lint/build issues that block progress (document them)
- **DO NOT** add features not in the plan
- **DO NOT** add dead code or `allow(dead_code)` annotations
- **DO NOT** leave TODO comments - implement fully or note blockers
- **DO NOT** have sub-agents run build/test until Phase 3

## Quality Standards

- Match existing code style and patterns
- Maintain consistent naming conventions
- Handle errors appropriately
- Don't leave debug code or commented-out code
