---
name: task-decomposition
description: Break down complex tasks into atomic, actionable goals with clear dependencies and success criteria. Use this skill when you need to plan multi-step projects, coordinate agents, or decompose complex user requests into manageable sub-tasks.
---

# Task Decomposition

Enable effective planning and execution by decomposing high-level objectives into manageable, testable sub-tasks.

## When to Use

- Complex user requests with multiple components
- Multi-phase projects requiring coordination
- Tasks that could benefit from parallel execution
- When planning agent coordination strategies

## Decomposition Framework

### 1. Requirements Analysis

**Extract Information**:
- Primary objective (what user wants to achieve)
- Implicit requirements (quality, performance, documentation)
- Constraints (time, resources, compatibility)
- Success criteria (how to measure completion)

**Questions to Ask**:
- What is the core goal?
- What are the sub-goals that contribute to the main goal?
- What are the dependencies between sub-goals?
- What could go wrong and how to prevent it?

### 2. Goal Hierarchy

**Top-Down Decomposition**:
```
Main Goal: [High-level objective]
├─ Sub-goal 1: [Component 1]
│  ├─ Task 1.1: [Atomic action]
│  └─ Task 1.2: [Atomic action]
├─ Sub-goal 2: [Component 2]
│  ├─ Task 2.1: [Atomic action]
│  └─ Task 2.2: [Atomic action]
└─ Sub-goal 3: [Component 3]
   └─ Task 3.1: [Atomic action]
```

**Atomic Task Criteria**:
- Single, clear action
- Well-defined inputs and outputs
- Can be completed by one agent
- Testable/verifiable completion
- Time-bounded (estimable duration)

### 3. Dependency Mapping

**Dependency Types**:

**Sequential Dependencies**:
```
Task A → Task B → Task C
(B requires A's output, C requires B's output)
```

**Parallel Independent**:
```
Task A ─┐
Task B ─┼─ [All can run simultaneously]
Task C ─┘
```

**Converging Dependencies**:
```
Task A ─┐
Task B ─┼─> Task D (requires A, B, C)
Task C ─┘
```

**Resource Dependencies**:
```
Task A (needs resource X)
Task B (needs resource X)
→ Sequential or resource pooling required
```

### 4. Success Criteria Definition

For each task, define:

**Input Requirements**:
- What data/state is needed to start
- What resources must be available
- What preconditions must be met

**Output Expectations**:
- What artifacts will be produced
- What state changes will occur
- What metrics define success

**Quality Standards**:
- Performance requirements
- Code quality standards (from AGENTS.md)
- Testing requirements
- Documentation requirements

## Decomposition Process

### Step 1: Understand the Goal

```markdown
User Request: [Original request]

Analysis:
- Primary Goal: [Main objective]
- Type: [Implementation/Debug/Refactor/Analysis]
- Domain: [Specific area of codebase]
- Complexity: [Simple/Medium/Complex]
```

### Step 2: Identify Major Components

Break main goal into 3-7 major components:

```markdown
Main Goal: Implement batch pattern update feature

Major Components:
1. Database layer (Turso + redb)
2. API layer (public interface)
3. Business logic (batch processing)
4. Testing (unit + integration)
5. Documentation (API docs + examples)
```

### Step 3: Decompose Each Component

For each component, identify atomic tasks:

```markdown
Component: Database layer

Tasks:
1. Design batch schema/structure
   - Input: Pattern data structures
   - Output: Schema definition
   - Success: Supports efficient batch operations

2. Implement Turso batch operations
   - Input: Schema, patterns array
   - Output: Batch insert/update functions
   - Success: Atomic transaction, proper error handling

3. Implement redb batch caching
   - Input: Schema, patterns array
   - Output: Batch cache update functions
   - Success: Fast writes, consistency maintained
```

### Step 4: Map Dependencies

```markdown
Dependency Graph:

[Design schema] ──┬──> [Implement Turso batch] ──┐
                  │                               ├──> [Write tests]
                  └──> [Implement redb batch] ───┘

[Write tests] ──> [Write documentation]
```

### Step 5: Assign Priorities

**Priority Levels**:
- **P0 (Critical)**: Must complete for goal achievement
- **P1 (Important)**: Significantly improves quality/functionality
- **P2 (Nice-to-have)**: Enhances but not essential

**Prioritization Factors**:
- Blocks other tasks (critical path)
- High user value
- Risk reduction (address unknowns early)
- Quick wins (early validation)

### Step 6: Estimate Complexity

For each task:
```markdown
Task: [Name]
- Complexity: [Low/Medium/High]
- Effort: [Small/Medium/Large]
- Risk: [Low/Medium/High]
- Dependencies: [List]
```

## Decomposition Patterns

### Pattern 1: Layer-Based Decomposition

For architectural changes:
```
1. Data/Storage layer
2. Business logic layer
3. API/Interface layer
4. Testing layer
5. Documentation layer
```

### Pattern 2: Feature-Based Decomposition

For new features:
```
1. Core functionality (MVP)
2. Error handling & edge cases
3. Performance optimization
4. Integration with existing system
5. Testing & validation
6. Documentation & examples
```

### Pattern 3: Phase-Based Decomposition

For large projects:
```
Phase 1: Research & Design
Phase 2: Foundation & Infrastructure
Phase 3: Core Implementation
Phase 4: Integration & Testing
Phase 5: Optimization & Polish
Phase 6: Documentation & Release
```

### Pattern 4: Problem-Solution Decomposition

For debugging/fixing:
```
1. Reproduce issue
2. Diagnose root cause
3. Design solution
4. Implement fix
5. Verify fix
6. Prevent regression (tests)
```

## Example Decompositions

### Example 1: Simple Task

```markdown
Request: "Fix failing test in pattern extraction"

Analysis: Simple, focused task

Decomposition:
1. Run test to observe failure
2. Identify failure cause
3. Apply fix
4. Verify test passes
5. Check for similar issues

Dependencies: Sequential (1→2→3→4→5)
Complexity: Low
Strategy: Single agent, sequential execution
```

### Example 2: Medium Task

```markdown
Request: "Add caching to episode retrieval"

Analysis: Medium complexity, multiple components

Decomposition:
1. Design cache strategy
2. Implement cache layer
3. Integrate with retrieval
4. Add tests
5. Measure performance

Dependencies:
- 1 → 2 → 3 (sequential)
- 4 depends on 3
- 5 depends on 3

Strategy: Sequential with parallel testing
```

### Example 3: Complex Task

```markdown
Request: "Refactor storage layer to support multiple backends"

Analysis: High complexity, architectural change

Major Components:
1. Storage abstraction layer
2. Turso backend implementation
3. redb backend implementation
4. Backend factory & configuration
5. Migration utilities
6. Testing infrastructure
7. Documentation

Strategy: Multi-phase hybrid execution
Coordination: GOAP agent + multiple specialized agents
```

## Quality Checklist

### Good Decomposition Characteristics

✓ Each task is atomic and actionable
✓ Dependencies are clearly identified
✓ Success criteria are measurable
✓ Complexity is appropriately estimated
✓ All requirements are covered
✓ No task is too large (>4 hours work)
✓ Parallelization opportunities identified

### Common Pitfalls

✗ Tasks too large or vague
✗ Missing dependencies
✗ Unclear success criteria
✗ Over-decomposition (too granular)
✗ Missing quality/testing tasks
✗ No consideration for error handling
✗ Forgetting documentation tasks

## Integration with GOAP Agent

The GOAP agent uses task decomposition as its first phase:

1. **Receive user request**
2. **Apply decomposition framework** (this skill)
3. **Create execution plan** (agent-coordination skill)
4. **Execute with monitoring** (parallel-execution skill)
5. **Report results**

## Tips for Effective Decomposition

### 1. Start with Why
- Understand the true goal behind the request
- Identify implicit requirements
- Consider broader context

### 2. Think Top-Down
- Start with high-level components
- Decompose each component separately
- Stop at appropriate granularity

### 3. Consider the User
- What value does each task provide?
- Can tasks be reordered for faster feedback?
- What's the minimum viable solution?

### 4. Plan for Quality
- Include testing tasks
- Include documentation tasks
- Include review/validation tasks

### 5. Anticipate Issues
- What could go wrong?
- What are the unknowns?
- Where are the risks?

### 6. Enable Parallelization
- Identify truly independent tasks
- Break dependencies where possible
- Consider resource constraints

## Summary

Good task decomposition is the foundation of effective planning and coordination. By breaking complex goals into atomic, well-defined tasks with clear dependencies, you enable:

- Optimal execution strategies (parallel/sequential)
- Clear success criteria and validation
- Effective agent coordination
- Better progress tracking
- Higher quality outcomes

Use this skill as the first step in any complex task planning workflow.
