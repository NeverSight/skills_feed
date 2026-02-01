---
name: cosmos-delegate-to-agent
description: Teaches agents how to effectively use the delegateToAgent tool for orchestrating multi-agent work. Covers dependency graph analysis, parallel vs serial execution patterns, and progress tracking. Use when an agent needs to delegate tasks to specialist agents, especially when working with plans, todos, or multi-step requests.
---

# Delegate to Agent Skill

Master the `delegateToAgent` tool to orchestrate work across specialist agents efficiently.

## Tool Overview

The `delegateToAgent` tool allows you to delegate tasks to other specialist agents. Key capabilities:

```typescript
delegateToAgent({
  agentName: string,  // Name of the agent to delegate to
  task: string        // Specific task or question for that agent
})
```

**Critical Feature**: Multiple `delegateToAgent` calls can run **in parallel**. The tool uses immutable context branching - each call is isolated and doesn't interfere with others.

## Discovering Available Agents

Before delegating, you need to know which agents are available. Use `manageAgent` with the `list` action:

```typescript
manageAgent({ action: "list" })
```

This returns all specialist agents defined in the project. If you're unsure which agent is appropriate for a task, **ask the user** which agent they'd like you to delegate to.

**Workflow**:
1. Run `manageAgent({ action: "list" })` to see available agents
2. Match task requirements to agent specializations
3. If unclear, ask the user: "Which agent should handle this task? Available: [agent1, agent2, ...]"
4. Proceed with `delegateToAgent` using the chosen agent

## Core Principle: Dependency-Driven Execution

Before delegating, always analyze task dependencies to determine:
- **Parallel tasks**: Independent work that can run simultaneously
- **Serial tasks**: Work that depends on prior task completion

```
┌─────────────────────────────────────────────────────────┐
│                   EXECUTION STRATEGY                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Independent tasks?  ──YES──►  Delegate in PARALLEL    │
│          │                                              │
│          NO                                             │
│          │                                              │
│          ▼                                              │
│   Has dependencies?   ──YES──►  Delegate in SERIAL      │
│          │                      (wait for dependency)   │
│          NO                                             │
│          │                                              │
│          ▼                                              │
│   Single task         ──────►  Delegate immediately     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Dependency Detection

### Explicit Markers

Look for dependency markers in plans and task lists:

| Marker | Example | Meaning |
|--------|---------|---------|
| `Depends on:` | `Depends on: Phase 1` | Must complete Phase 1 first |
| `Requires:` | `Requires: Task 2.1` | Must complete Task 2.1 first |
| `After:` | `After: API implementation` | Sequential dependency |
| Task numbering | `3.2` follows `3.1` | Implicit ordering within phase |

### Implicit Dependencies

Infer dependencies from task semantics when markers are absent:

| First Task | Dependent Task | Reasoning |
|------------|----------------|-----------|
| Create schema/types | Use schema/types | Definition before usage |
| Implement feature | Write tests for feature | Code before tests |
| Design API | Implement API | Design before implementation |
| Build component | Integrate component | Build before integration |
| Research/analyze | Implement based on research | Information before action |

**Heuristic**: If Task B references output, artifacts, or decisions from Task A, then B depends on A.

## Execution Patterns

For detailed sequence diagrams showing parallel, serial, and mixed execution with plan updates, see [assets/EXAMPLE.md](assets/EXAMPLE.md).

### Pattern 1: Parallel Independent Tasks

When tasks have no dependencies on each other, delegate simultaneously:

```
User: "Review the auth module for security, performance, and code style"

Analysis:
- Security review: independent
- Performance review: independent  
- Code style review: independent

Execution: Call all three delegateToAgent in parallel
┌─────────────────────────────────────────┐
│  delegateToAgent(security, "review")    │──┐
│  delegateToAgent(performance, "review") │──┼──► All run simultaneously
│  delegateToAgent(codestyle, "review")   │──┘
└─────────────────────────────────────────┘
```

### Pattern 2: Serial Dependent Tasks

When tasks have dependencies, execute sequentially:

```
User: "Design the API, then implement it, then write tests"

Analysis:
- Design API: no dependencies
- Implement API: depends on design
- Write tests: depends on implementation

Execution: Sequential chain
┌──────────────────────────────────────────────────────┐
│  delegateToAgent(architect, "design API")            │
│         │                                            │
│         ▼ (wait for completion)                      │
│  delegateToAgent(developer, "implement API")         │
│         │                                            │
│         ▼ (wait for completion)                      │
│  delegateToAgent(developer, "write tests")           │
└──────────────────────────────────────────────────────┘
```

### Pattern 3: Mixed Parallel/Serial (Dependency Graph)

Complex work often has parallel branches with serial dependencies:

```
Plan Phase 2:
- Task 2.1: Create database schema (no deps)
- Task 2.2: Create API types (no deps)
- Task 2.3: Implement API endpoints (requires 2.1, 2.2)
- Task 2.4: Write integration tests (requires 2.3)

Execution:
┌─────────────────────────────────────────────────────┐
│  WAVE 1 (parallel):                                 │
│    delegateToAgent(developer, "create schema")      │
│    delegateToAgent(developer, "create API types")   │
│         │                                           │
│         ▼ (wait for both)                           │
│  WAVE 2 (serial):                                   │
│    delegateToAgent(developer, "implement endpoints")│
│         │                                           │
│         ▼ (wait)                                    │
│  WAVE 3 (serial):                                   │
│    delegateToAgent(developer, "write tests")        │
└─────────────────────────────────────────────────────┘
```

## Progress Tracking

### With a Plan Document

When executing tasks from a plan markdown file, update it as work progresses:

**Checkbox Updates**:
```markdown
Before: - [ ] Create user schema
After:  - [x] Create user schema
```

**Status Field Updates**:
```markdown
Before: **Status**: ☐ Not Started
After:  **Status**: ✓ Complete
```

**Phase Status**:
```markdown
Before: **Status**: In Progress
After:  **Status**: Complete
```

**Timestamp Comments** (optional, for audit trail):
```markdown
##### 2.1 Create Database Schema
**Status**: ✓ Complete  
**Completed**: 2026-01-31 14:32
```

### Without a Plan Document

When given a general request without a plan, use available tracking tools:

1. **Analyze the request** - Break into discrete tasks
2. **Build mental dependency graph** - Determine parallel/serial
3. **Use todo tool** (if available) - Track progress
4. **Execute systematically** - Parallel waves, then serial chains

Example mental model:
```
User: "Set up authentication with JWT, add user roles, and create admin dashboard"

Dependency analysis:
├── JWT auth implementation (independent)
├── User roles system (depends on auth? check...)
│   └── Roles need users → depends on auth
└── Admin dashboard (depends on roles)

Execution order:
1. delegateToAgent(developer, "implement JWT auth")
2. delegateToAgent(developer, "add user roles system") 
3. delegateToAgent(developer, "create admin dashboard")
```

## Best Practices

### DO

- **Analyze before executing** - Spend time understanding dependencies
- **Maximize parallelism** - Independent tasks should run simultaneously
- **Provide clear task context** - Each delegated task should be self-contained
- **Update progress immediately** - Mark tasks complete as delegations return
- **Include relevant context** - Pass outputs from dependencies to dependent tasks

### DON'T

- **Don't serialize everything** - Unnecessary sequential execution wastes time
- **Don't parallelize blindly** - Dependent tasks will fail or produce inconsistent results
- **Don't forget to track** - Progress visibility helps with long-running orchestration
- **Don't delegate circular chains** - The tool prevents A→B→A but design your graph correctly

## Tool Constraints

The `delegateToAgent` tool has built-in safeguards:

| Constraint | Limit | Error |
|------------|-------|-------|
| Max depth | 5 levels | `MAX_DEPTH_EXCEEDED` |
| Circular reference | A→B→A | `CIRCULAR_REFERENCE` |
| Missing context | No session | `CONTEXT_NOT_INITIALIZED` |

If you hit max depth, the task is too deeply nested. Consider restructuring to reduce delegation layers.

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION CHECKLIST                  │
├─────────────────────────────────────────────────────────────┤
│  1. □ Parse tasks from plan/request                         │
│  2. □ Identify explicit dependency markers                  │
│  3. □ Infer implicit dependencies from semantics            │
│  4. □ Group into parallel waves                             │
│  5. □ Execute wave 1 (all parallel)                         │
│  6. □ Wait for wave 1 completion                            │
│  7. □ Update plan/todos with completed tasks                │
│  8. □ Execute wave 2 (may be parallel or serial)            │
│  9. □ Repeat until all tasks complete                       │
│ 10. □ Final plan/status update                              │
└─────────────────────────────────────────────────────────────┘
```
