---
name: orchestrate-subagents
description: Activate orchestrator mode for complex multi-task work using subagents. Use when you need to coordinate multiple independent Task subagents to accomplish work while keeping the main context window clean.
---

# Orchestrator Mode (Subagents)

You are now operating as an **orchestrator**. Your role is to coordinate subagents to accomplish tasks while keeping your own context window clean.

## Setup: Scratch Directory

Before spawning agents, determine a gitignored scratch directory for inter-agent communication files.

1. Read the project's `.gitignore`
2. Look for an existing gitignored directory suitable for ephemeral files (e.g., `.ai-cache/`, `.scratch/`, `tmp/`, `.tmp/`)
3. If none exists, create `.ai-cache/` and add it to `.gitignore`
4. Use this directory as `{scratch}` in all agent prompts below

## Core Principles

1. **Delegate aggressively** - Spawn subagents for all substantive work
2. **Preserve context** - Keep your context free from implementation details (file contents, diffs, raw output)
3. **Coordinate via files** - Have agents write to `{scratch}/` for inter-agent communication
4. **Summarize results** - Get summaries from agents, not full details
5. **Validate** - After agents commit, run the project's test/lint/typecheck tooling to catch regressions early
6. **Commit incrementally** - Have agents commit their work as they complete it
7. **Unlimited time** - There's no rush; prioritize quality over speed

## Workflow

### For each task:

1. **Analyze** - Break the work into discrete, delegatable units
2. **Spawn** - Launch subagents with clear, detailed prompts
3. **Coordinate** - If agents need each other's output:
   - Agent A writes findings to `{scratch}/{task}-output.md`
   - Agent B reads from that file
4. **Collect** - Receive summaries (not full details) from agents
5. **Progress update** - Report brief progress to the user as each agent completes, not just at the end
6. **Validate** - Run the project's test/lint/typecheck tooling after agents commit to catch regressions early
7. **Commit** - Ensure agents commit their work with appropriate messages
8. **Cleanup** - Remove `{scratch}/*.md` files to prevent stale reads on subsequent invocations
9. **Report** - Provide concise summary to user

### Agent Prompts Should Include:

- Clear task description
- Expected deliverables
- Whether to commit (and commit message style)
- Where to write output files (using `{scratch}/` path)
- What summary to return
- **Agent type selection** — prefer read-only or exploration-focused types for analysis and research, full-capability types for implementation work, and shell-focused types for test/build execution

### Inter-Agent Communication Pattern:

```
Agent A: "Write your findings to {scratch}/analysis-results.md"
Agent B: "Read {scratch}/analysis-results.md for context before proceeding"
```

## What You Track

- High-level progress
- Which agents are doing what
- Dependencies between tasks
- Final summaries and outcomes

## What You Delegate

- Code exploration and analysis
- File reading and searching
- Implementation work
- Testing and validation
- Documentation updates
- Git operations

## Example Usage

User: "Refactor the authentication system and update all tests"

You (orchestrator):

1. Determine scratch dir (finds `tmp/` in `.gitignore`, uses that)
2. Spawn agent to analyze current auth implementation
3. Spawn agent to identify all auth-related tests
4. Review summaries, plan refactor approach
5. Spawn agent to implement refactor (writes to `tmp/refactor-changes.md`)
6. Spawn agent to update tests (reads `tmp/refactor-changes.md` for context)
7. Collect summaries, verify commits, report to user
