---
name: parallel-execution
description: Execute multiple independent tasks simultaneously using parallel agent coordination to maximize throughput and minimize execution time. Use when tasks have no dependencies, results can be aggregated, and agents are available for concurrent work.
---

# Parallel Execution

Execute multiple independent tasks simultaneously to maximize throughput and minimize total execution time.

## When to Use

- Multiple independent tasks (no dependencies)
- Tasks benefit from concurrent execution
- Maximizing throughput is priority
- Available agents for parallel work
- Results can be aggregated after completion

## Core Concepts

### Independence

**Tasks are independent when**:
- ✓ No data dependencies (one doesn't need other's output)
- ✓ No resource conflicts (different files, databases)
- ✓ No ordering requirements (either can complete first)
- ✓ Failures are isolated (one failing doesn't block others)

**Example - Independent**:
```markdown
✓ Task A: Review code quality (code-reviewer)
✓ Task B: Run test suite (test-runner)
→ Can run in parallel
```

**Example - NOT Independent**:
```markdown
✗ Task A: Implement feature (feature-implementer)
✗ Task B: Test feature (test-runner)
→ B depends on A's output, must run sequentially
```

### Concurrency

**Critical**: Use **single message** with **multiple Task tool calls**

**Correct**:
```markdown
Send one message containing:
- Task tool call #1 → Agent A
- Task tool call #2 → Agent B
- Task tool call #3 → Agent C

All three agents start simultaneously.
```

**Incorrect**:
```markdown
Message 1: Task tool → code-reviewer
[wait]
Message 2: Task tool → test-runner
[wait]

This is sequential, NOT parallel!
```

### Synchronization

**Collection Point**:
- Wait for all parallel agents to complete
- Collect results from each agent
- Validate each result independently
- Aggregate results into final output

## Parallel Execution Process

### Step 1: Identify Independent Tasks

**Independence Checklist**:
- [ ] No data dependencies
- [ ] No shared writes (read-only or different targets)
- [ ] No execution order requirements
- [ ] Failures don't cascade
- [ ] Results can be validated independently

### Step 2: Agent Assignment

**Match Tasks to Agents**:
```markdown
Task 1: Review code quality → code-reviewer
Task 2: Run test suite → test-runner
Task 3: Run benchmarks → test-runner
```

**Agent Availability Check**:
- Ensure sufficient agents available
- Check for specialization overlap
- Consider workload balance

### Step 3: Launch Parallel Execution

```markdown
Single message with multiple Task tool calls:

<Task tool> → code-reviewer (review task)
<Task tool> → test-runner (test task)
<Task tool> → test-runner (benchmark task)

All agents start simultaneously.
```

### Step 4: Monitor Execution

**Track Progress**:
```markdown
Agent 1 (code-reviewer): In Progress
  Task: Code quality review

Agent 2 (test-runner): Completed ✓
  Task: Test suite
  Result: 45/45 tests passed

Agent 3 (test-runner): In Progress
  Task: Benchmarks
```

### Step 5: Collect & Validate Results

**As Each Agent Completes**:
1. Collect output
2. Validate against success criteria
3. Check for errors
4. Mark as complete or failed

### Step 6: Aggregate Results

```markdown
## Parallel Execution Results

### Completed Tasks:
1. ✓ Code quality review (code-reviewer)
   - Result: 3 minor issues found

2. ✓ Test suite (test-runner)
   - Result: All tests passing (45/45)

3. ✓ Performance benchmarks (test-runner)
   - Result: All benchmarks acceptable

### Overall Status: ✓ Success (with minor issues)
```

## Execution Patterns

### Pattern 1: Homogeneous Parallel

**All agents same type, different inputs**:
```markdown
Use Case: Test multiple modules

├─ test-runner: Test memory-core
├─ test-runner: Test memory-storage-turso
└─ test-runner: Test memory-storage-redb

Single message, 3 Task tool calls
```

### Pattern 2: Heterogeneous Parallel

**Different agent types, related task**:
```markdown
Use Case: Comprehensive code check

├─ code-reviewer: Quality analysis
├─ test-runner: Test execution
└─ debugger: Performance profiling

Single message, 3 Task tool calls
```

### Pattern 3: Parallel with Convergence

**Parallel execution → Single synthesis**:
```markdown
Phase 1: Parallel Investigation
├─ debugger: Profile performance
├─ code-reviewer: Analyze efficiency
└─ test-runner: Run benchmarks

[All complete]

Phase 2: Synthesis
└─ Combine findings, identify root cause
```

## Synchronization Strategies

### Wait for All (AND)

**Most Common**:
- Wait for ALL agents to complete
- Proceed only when all finished
- Useful when all results needed

### Wait for Any (OR)

**Early Termination**:
- Proceed when ANY agent completes successfully
- Cancel or continue others
- Useful for redundant approaches

### Wait for Threshold

**Partial Completion**:
- Proceed when N out of M agents complete
- Useful for resilience
- Handle missing results gracefully

## Resource Management

### Available Agents
- code-reviewer (1 instance)
- test-runner (1 instance)
- feature-implementer (1 instance)
- refactorer (1 instance)
- debugger (1 instance)

**Parallelization Limit**: Maximum 5 agents simultaneously (one of each type)

### Workload Balancing

**Distribute Evenly**:
```markdown
Tasks: [T1, T2, T3, T4, T5, T6]
Agents: [A, B, C]

Distribution:
- Agent A: T1, T4 (2 tasks)
- Agent B: T2, T5 (2 tasks)
- Agent C: T3, T6 (2 tasks)
```

## Error Handling

### Independent Failures

**Isolation**:
- One agent failing doesn't stop others
- Continue collecting successful results
- Report failed tasks separately

```markdown
Parallel Execution:
├─ Agent A: ✓ Success
├─ Agent B: ✗ Failed (error in code)
└─ Agent C: ✓ Success

Result:
- Collect: Results from A and C
- Report: B failed with error
- Decision: Retry B or proceed without
```

### Partial Success Handling

**Strategies**:

1. **Fail Fast**: If any fails, stop and report
2. **Best Effort**: Collect all successful results
3. **Retry Failed**: Let successful complete, retry failures

## Performance Optimization

### Speedup Calculation

```
Sequential time = T1 + T2 + T3 + ... + Tn
Parallel time = max(T1, T2, T3, ..., Tn)

Speedup = Sequential time / Parallel time
```

**Example**:
```markdown
Tasks:
- Task A: 10 minutes
- Task B: 15 minutes
- Task C: 8 minutes

Sequential: 10 + 15 + 8 = 33 minutes
Parallel: max(10, 15, 8) = 15 minutes

Speedup: 33 / 15 = 2.2x faster
```

### Optimal Parallelization

**Identify Bottlenecks**:
- Find longest-running task
- Can it be decomposed further?
- Can it be optimized?
- Start slow tasks first

## Best Practices

### DO:
✓ Verify independence before parallelizing
✓ Use single message with multiple Task tool calls
✓ Balance workload across agents
✓ Set appropriate timeouts for each task
✓ Handle failures gracefully (isolation)
✓ Validate each result independently
✓ Aggregate comprehensively at the end

### DON'T:
✗ Parallelize dependent tasks
✗ Send sequential messages thinking they're parallel
✗ Overload single agent while others idle
✗ Skip validation because "it's parallel"
✗ Assume all will succeed
✗ Ignore agent failures

## Examples

### Example 1: Simple Parallel Review

```markdown
Task: "Check code quality and run tests"

Analysis: Independent tasks, different agents

Plan:
├─ code-reviewer: Review code quality
└─ test-runner: Run test suite

Execution: [Single message with 2 Task tool calls]

Results:
- code-reviewer: 2 issues found ✓
- test-runner: 45/45 tests pass ✓

Speedup: 2x
```

### Example 2: Multi-Module Testing

```markdown
Task: "Test all crates in workspace"

Analysis: 3 independent crates, same agent type

Plan:
├─ test-runner: Test memory-core
├─ test-runner: Test memory-storage-turso
└─ test-runner: Test memory-storage-redb

Execution: [Single message with 3 Task tool calls]

Results:
- memory-core: 25/25 pass ✓
- memory-storage-turso: 15/15 pass ✓
- memory-storage-redb: 10/10 pass ✓

Speedup: 3x
```

### Example 3: Comprehensive Quality Check

```markdown
Task: "Pre-release quality validation"

Analysis: 4 independent checks, maximum parallelization

Plan:
├─ code-reviewer: Code quality (fmt, clippy)
├─ test-runner: Test suite execution
├─ test-runner: Performance benchmarks
└─ debugger: Memory leak detection

Execution: [Single message with 4 Task tool calls]

Results: All checks pass ✓

Speedup: 4x
```

## Integration

Parallel execution is one coordination strategy used by the agent-coordination skill:

```markdown
Coordination Strategy Selection:
├─ Independent tasks → Use parallel-execution (this skill)
├─ Dependent tasks → Use sequential coordination
├─ Complex mix → Use hybrid coordination
└─ Multiple perspectives → Use swarm (with parallel)
```

## Summary

Parallel execution maximizes efficiency for independent tasks by:
- **Concurrent agent execution** (single message, multiple tools)
- **Independent task validation** (no cross-dependencies)
- **Synchronized result collection** (wait for completion)
- **Comprehensive aggregation** (synthesize final output)

When done correctly, parallel execution provides significant speedup while maintaining quality and reliability.
