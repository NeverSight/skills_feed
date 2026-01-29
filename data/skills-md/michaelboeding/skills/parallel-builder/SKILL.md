---
name: parallel-builder
description: Divide-and-conquer implementation from specs/plans. Decomposes a reference document into independent tasks, assigns each to a builder agent, executes in parallel waves respecting dependencies, then integrates results. Use when you have a spec, PRD, plan, or large feature to implement quickly with parallel execution.
---

# Parallel Builder: Divide-and-Conquer Implementation

Decomposes a plan/spec into independent tasks, spawns builder agents to implement each piece in parallel, and integrates the results. Unlike feature-council (same task, diverse approaches), this skill gives each agent a **different piece** of the work for maximum speed.

**Use this when you have a spec, PRD, or plan and want fast parallel implementation.**

## When to Use

✅ **Use parallel-builder for:**
- Implementing a PRD or spec document
- Large features that can be decomposed into parts
- When speed matters more than approach diversity
- Building from a reference file or detailed plan
- Multi-file implementations with clear boundaries

❌ **Don't use for:**
- Bugs (use debug-council)
- Features where you want diverse approaches (use feature-council)
- Tasks that can't be parallelized
- Simple single-file changes

---

## Where Parallel-Builder Shines

### 🚀 Maximum Speedup: Multi-File Specs

Parallel-builder is **fastest** when your spec produces **multiple independent files**:

```
┌─────────────────────────────────────────────────────────────┐
│  IDEAL: Each agent owns different files                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Wave 2: TRUE PARALLEL EXECUTION                            │
│  ┌─────────────────┐ ┌─────────────────┐ ┌────────────────┐│
│  │ Agent 1         │ │ Agent 2         │ │ Agent 3        ││
│  │ userService.ts  │ │ authService.ts  │ │ apiClient.ts   ││
│  └─────────────────┘ └─────────────────┘ └────────────────┘│
│          ↓                   ↓                   ↓          │
│      [PARALLEL - All 3 run simultaneously]                  │
│                                                             │
│  Speedup: ~3× faster than sequential                        │
└─────────────────────────────────────────────────────────────┘
```

**Great use cases:**
- Full-stack features (types + services + routes + UI components)
- Microservice implementations (multiple independent services)
- CRUD APIs (each resource in its own files)
- Plugin/module systems (each module independent)
- Test suites (test files for different modules)

### ⚠️ Falls Back to Sequential: Single-File Specs

When multiple tasks modify the **same file**, parallel execution would cause conflicts. The skill automatically falls back to sequential:

```
┌─────────────────────────────────────────────────────────────┐
│  LIMITED: All agents modify same file                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Wave 3: SEQUENTIAL (conflict avoidance)                    │
│  ┌─────────────────┐                                       │
│  │ Agent 1         │ → modifies BG600L.cpp                 │
│  └────────┬────────┘                                       │
│           ↓                                                 │
│  ┌─────────────────┐                                       │
│  │ Agent 2         │ → modifies BG600L.cpp                 │
│  └────────┬────────┘                                       │
│           ↓                                                 │
│  ┌─────────────────┐                                       │
│  │ Agent 3         │ → modifies BG600L.cpp                 │
│  └─────────────────┘                                       │
│                                                             │
│  No speedup, but still provides organized task breakdown    │
└─────────────────────────────────────────────────────────────┘
```

**Still useful for:**
- Organized task breakdown and tracking
- Clear separation of concerns
- Systematic implementation of complex single-file changes

### Speedup Estimate

| Spec Type | Parallel Potential | Expected Speedup |
|-----------|-------------------|------------------|
| Multi-file, independent modules | High | 50-80% faster |
| Multi-file, some shared | Medium | 30-50% faster |
| Few files, many functions | Low | 10-20% faster |
| Single file, many changes | Minimal | ~0% (sequential) |

The skill will show you the estimated speedup in the execution plan before you confirm.

---

## Step 0: Accept Plan Input

First, get the plan from the user. Accept one of:

1. **File path**: User provides path to a spec, PRD, or plan file
2. **Inline description**: User describes what to build
3. **Reference file**: User points to existing code to replicate/extend

```
What would you like me to build? You can provide:
- A file path to a spec/PRD/plan
- A description of the feature
- A reference file to work from

I'll decompose it into parallel tasks for fast implementation.
```

---

## Step 1: Analyze & Decompose

Read the plan and identify work units. For each unit, determine:

1. **Independence**: Can it be built without waiting for others?
2. **Dependencies**: What must exist before this can be built?
3. **Outputs**: What files/interfaces does this create?
4. **Complexity**: Rough estimate (small/medium/large)

### Decomposition Rules

| Rule | Description |
|------|-------------|
| **File boundaries** | One agent per file or closely related file group |
| **Feature boundaries** | One agent per distinct feature/capability |
| **Layer boundaries** | Separate by layer (types, services, API, UI) |
| **Minimize coupling** | Tasks should have minimal interface dependencies |

### Create Dependency Graph

Identify three categories:

```
WAVE 1 (Foundation - No Dependencies):
- Shared types/interfaces
- Configuration
- Constants
- Base utilities

WAVE 2 (Core - Depends on Wave 1):
- Services
- Business logic
- Data access
- Core components

WAVE 3+ (Integration - Depends on Previous):
- API routes that use services
- UI that uses components
- Integration code
- Tests
```

---

## Step 2: Define Shared Contracts

**CRITICAL**: Before spawning agents, define the contracts they share.

Create a shared context that ALL agents receive:

```markdown
## Shared Contracts

### Interfaces
[Define all shared types/interfaces that multiple agents need]

### File Ownership
[Map which agent owns which files - no overlaps]

### Naming Conventions
[Consistent naming across all agents' work]

### Import Paths
[How agents should import from each other's domains]
```

This prevents conflicts and ensures pieces fit together.

---

## Step 3: Present Execution Plan to User

Show the decomposition and get confirmation:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    PARALLEL BUILD PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Source: [file path or "inline description"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                      TASK BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Wave 1: Foundation (3 agents in parallel)

| Task | Agent | Files | Complexity |
|------|-------|-------|------------|
| Create shared types | builder-solver-1 | types/*.ts | Small |
| Database schema | builder-solver-2 | schema.prisma | Medium |
| Config & constants | builder-solver-3 | config/*.ts | Small |

## Wave 2: Core (2 agents in parallel, after Wave 1)

| Task | Agent | Files | Depends On |
|------|-------|-------|------------|
| User service | builder-solver-4 | services/user.ts | Wave 1 types |
| Auth service | builder-solver-5 | services/auth.ts | Wave 1 types |

## Wave 3: Integration (1 agent, after Wave 2)

| Task | Agent | Files | Depends On |
|------|-------|-------|------------|
| API routes + wiring | builder-solver-6 | routes/*.ts, index.ts | Wave 1, 2 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                       SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Tasks: 6
Total Waves: 3
Parallel Agents: Up to 3 concurrent
Estimated Speedup: ~50-60% faster than sequential

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proceed with this plan? (y/n/modify)
```

If user says "modify", let them adjust task boundaries or wave assignments.

---

## Step 4: Execute Wave by Wave

### For Each Wave

1. **Prepare agent prompts** with:
   - Their specific task
   - Shared contracts (from Step 2)
   - Outputs from previous waves (if any)
   - Files they own (and must NOT touch others)

2. **Spawn agents IN PARALLEL**:

```
Task(agent: "builder-solver-1", prompt: "[TASK 1 PROMPT]")
Task(agent: "builder-solver-2", prompt: "[TASK 2 PROMPT]")
Task(agent: "builder-solver-3", prompt: "[TASK 3 PROMPT]")
... (all in the SAME batch - parallel execution)
```

3. **Track progress**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                  WAVE 1 PROGRESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ builder-solver-1 - Complete (types/*.ts)
☑ builder-solver-2 - Complete (schema.prisma)
☐ builder-solver-3 - Working... (config/*.ts)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

4. **Collect outputs** when wave completes

5. **Pass context to next wave** - Include relevant outputs from completed waves

---

## Step 5: Agent Prompt Template

Each builder-solver agent receives a structured prompt:

```markdown
# Builder Task: [TASK NAME]

## Your Assignment

[SPECIFIC DESCRIPTION OF WHAT TO BUILD]

## Files You Own

You are responsible for creating/modifying ONLY these files:
- [file1.ts]
- [file2.ts]

⚠️ DO NOT modify any other files.

## Shared Contracts

[PASTE SHARED INTERFACES/TYPES FROM STEP 2]

## Context from Previous Waves

[PASTE RELEVANT OUTPUTS FROM EARLIER WAVES, IF ANY]

## Requirements

1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

## Expected Output

Create the files listed above with complete, production-ready implementations.
Follow the shared contracts exactly.
```

---

## Step 6: Integration & Verification

After all waves complete:

### 6.1 Apply All Changes

Agents propose changes - orchestrator applies them to the codebase.

### 6.2 Check for Conflicts

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                  CONFLICT CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No file conflicts (agents stayed in their lanes)
✅ Interface contracts honored
✅ Import paths valid
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If conflicts exist, resolve them:
- Prefer later wave's version for integration files
- Merge compatible changes
- Flag incompatible changes for user decision

### 6.3 Run Verification

```bash
# Type check
npm run typecheck  # or equivalent

# Lint
npm run lint

# Tests (if any)
npm run test
```

Fix any issues found.

---

## Step 7: Report Results

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                 PARALLEL BUILD COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📊 Execution Summary

| Wave | Agents | Tasks | Status |
|------|--------|-------|--------|
| 1 | 3 | Foundation | ✅ Complete |
| 2 | 2 | Core Services | ✅ Complete |
| 3 | 1 | Integration | ✅ Complete |

Total Time: [X seconds]
Sequential Estimate: [Y seconds]  
Speedup: [Z%]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📁 Files Created/Modified

### Wave 1 Output
| Agent | Files Created |
|-------|--------------|
| builder-solver-1 | types/user.ts, types/auth.ts |
| builder-solver-2 | prisma/schema.prisma |
| builder-solver-3 | config/index.ts, config/constants.ts |

### Wave 2 Output
| Agent | Files Created |
|-------|--------------|
| builder-solver-4 | services/user.ts |
| builder-solver-5 | services/auth.ts |

### Wave 3 Output
| Agent | Files Created |
|-------|--------------|
| builder-solver-6 | routes/user.ts, routes/auth.ts, index.ts |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ✅ Verification

- Type Check: ✅ Passed
- Lint: ✅ Passed  
- Tests: ✅ Passed (or N/A)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔍 What Each Agent Built

### builder-solver-1: Shared Types
- Created User, AuthToken, Session interfaces
- Defined validation schemas

### builder-solver-2: Database Schema
- Created User, Session, Token models
- Set up relations and indexes

... (for each agent)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📋 Implementation from Spec

| Spec Requirement | Status | Implemented By |
|------------------|--------|----------------|
| User registration | ✅ | builder-solver-4, 6 |
| Authentication | ✅ | builder-solver-5, 6 |
| Session management | ✅ | builder-solver-5 |
| API endpoints | ✅ | builder-solver-6 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Error Handling

### Agent Failure

If an agent fails:

1. **Retry once** with the same prompt
2. If still fails, **report to user** with error details
3. Ask if user wants to:
   - Skip this task and continue
   - Provide guidance and retry
   - Abort the build

### Dependency Failure

If Wave N fails and Wave N+1 depends on it:

1. **Block dependent waves**
2. **Report the blocker**
3. **Offer options**: fix and continue, or abort

---

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| Max parallel agents | 5 | Maximum agents running simultaneously |
| Agent timeout | 5 min | Max time per agent |
| Auto-verify | true | Run type check/lint after completion |
| Show progress | true | Display progress updates |

User can specify: `parallel-builder with 3 max agents`

---

## Agents

10 builder solver agents in `agents/` directory:
- `builder-solver-1` through `builder-solver-10`

All agents:
- Same instructions (focused on implementing their assigned piece)
- Lower temperature (0.4) for consistency
- Full tool access (Read, Write, Grep, Glob, LS, Shell)
- Respect file ownership boundaries
- Follow shared contracts exactly

---

## Difference from Other Skills

| Aspect | debug-council | feature-council | parallel-builder |
|--------|---------------|-----------------|------------------|
| **Input** | Bug to fix | Feature to build | Spec/plan to implement |
| **Agent task** | Same problem | Same feature | Different pieces |
| **Goal** | Find correct fix | Diverse approaches | Fast parallel execution |
| **Selection** | Majority vote | Synthesis/merge | Integration |
| **Speed** | N agents, 1 problem | N agents, 1 feature | N pieces, ~N× speedup |

---

## Examples

### Example 1: From PRD File

```
User: parallel-builder from docs/auth-prd.md

Orchestrator:
1. Reads docs/auth-prd.md
2. Decomposes into: types, user-service, auth-service, middleware, routes
3. Creates 3 waves
4. Executes in parallel
5. Integrates and verifies
```

### Example 2: From Description

```
User: parallel-builder a full CRUD API for a blog with posts, comments, and users

Orchestrator:
1. Decomposes: types, 3 services, 3 route files, integration
2. Wave 1: types (1 agent)
3. Wave 2: 3 services in parallel (3 agents)
4. Wave 3: 3 route files in parallel (3 agents)
5. Wave 4: integration (1 agent)
```

### Example 3: From Reference

```
User: parallel-builder something like src/features/users but for products

Orchestrator:
1. Reads src/features/users to understand pattern
2. Creates parallel tasks to replicate for products
3. Executes maintaining same architecture
```
