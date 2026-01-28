---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session or facing 3+ independent issues that can be investigated without shared state or dependencies - dispatches fresh subagent for each task with code review between tasks, enabling fast iteration with quality gates
---

# Subagent-Driven Development

Create and execute plan by dispatching fresh subagent per task or issue, with code and output review after each or batch of tasks.

**Core principle:** Fresh subagent per task + review between or after tasks = high quality, fast iteration.

## Overview

Executing Plans through agents:

- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Code review after each or batch of task (catch issues early)
- Faster iteration (no human-in-loop between tasks)

## Supported Types of Execution

### Sequential Execution

When tasks are tightly coupled and need to be executed in order.

- Dispatch one agent per task or issue
- Let it work sequentially
- Review the output and code after each task or issue

### Parallel Execution

When you have multiple unrelated tasks (different files, different subsystems, different bugs).

- Dispatch one agent per independent problem domain
- Let them work concurrently
- Overall review after all tasks are completed

### Parallel Investigation

Special case for multiple unrelated failures that can be investigated without shared state or dependencies.

## Progressive Loading

**L2 Content** (loaded when sequential execution process needed):
- See: [references/sequential-process.md](./references/sequential-process.md)

**L3 Content** (loaded when parallel execution or investigation needed):
- See: [references/parallel-process.md](./references/parallel-process.md)
- See: [references/parallel-investigation.md](./references/parallel-investigation.md)
