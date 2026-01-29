---
name: feature-council
description: Multi-agent feature implementation. Spawns independent solver agents that each implement the feature from scratch, then synthesizes the best elements from each. Use when building complex features where you want diverse approaches and comprehensive edge case coverage.
---

# Feature Council: Multi-Agent Feature Implementation

Spawns multiple agents to implement the same feature independently, then synthesizes the best parts from each. Unlike code-council (majority voting for bugs), this skill **merges strengths** because features have multiple valid approaches.

**Use this for complex features where you want diverse implementations and comprehensive coverage.**

## Step 0: Ask User How Many Agents

Before doing anything else, **ask the user how many solver agents to use**:

```
How many solver agents would you like me to use? (3-10)

Recommendations:
- 3 agents: Faster, good for straightforward features
- 5 agents: Good balance of diversity and speed
- 7 agents: Comprehensive coverage
- 10 agents: Maximum diversity (complex features)

Note: Each agent will independently implement the entire feature.
More agents = more diverse approaches and edge case coverage.
```

Wait for the user's response. If they specified a number (e.g., "feature council of 5"), use that.

**Minimum: 3 agents** | **Maximum: 10 agents**

---

## CRITICAL: Pure Independence

### What This Means

1. **NO orchestrator exploration** - Do NOT read files or gather context before spawning agents
2. **Raw user prompt to all agents** - Each agent gets the user's original request, unchanged
3. **Each agent explores independently** - Agents discover the codebase themselves
4. **Each agent implements fully** - Complete, working implementations

### Why This Matters

Independent implementations mean:
- Different architectural choices to compare
- Different edge cases discovered
- Different error handling approaches
- More comprehensive final solution

---

## Workflow

### Step 1: Capture the Raw User Prompt

Take the user's request **exactly as stated**. Do NOT:
- ❌ Read files first
- ❌ Explore the codebase
- ❌ Add context
- ❌ Rephrase or enhance the prompt

Just capture what the user said.

### Step 2: Spawn Agents IN PARALLEL with RAW PROMPT

Spawn ALL agents simultaneously. Each gets the **exact same raw prompt**:

```
Task(agent: "feature-solver-1", prompt: "[USER'S EXACT WORDS]")
Task(agent: "feature-solver-2", prompt: "[USER'S EXACT WORDS]")
Task(agent: "feature-solver-3", prompt: "[USER'S EXACT WORDS]")
... (all in the SAME batch - parallel execution)
```

**DO NOT modify the prompt. DO NOT add context. Raw user words only.**

### Step 3: Agents Work Independently

Each agent will:
1. Read and understand the user's feature request
2. Explore the codebase to understand existing patterns
3. Design their approach
4. Implement the complete feature
5. Handle edge cases they identify
6. Verify their implementation

**Each agent works in complete isolation.**

### Step 4: Track Progress & Collect Solutions

As agents complete, **show progress to the user**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                     AGENT PROGRESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
☑ Agent 1 - Complete
☑ Agent 2 - Complete  
☑ Agent 3 - Complete
☐ Agent 4 - Working...
☐ Agent 5 - Working...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Collect all outputs when complete.

### Step 5: Analyze & Compare Implementations

**DO NOT use majority voting.** Instead, analyze each implementation for:

| Category | What to Look For |
|----------|------------------|
| **Architecture** | Design patterns, code organization, modularity |
| **Edge Cases** | What edge cases did each agent handle? |
| **Error Handling** | How robust is the error handling? |
| **Type Safety** | Type definitions, null checks, validation |
| **Performance** | Efficiency, caching, optimization |
| **Maintainability** | Readability, documentation, testability |
| **Codebase Fit** | How well does it match existing patterns? |

Create a comparison matrix:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                  IMPLEMENTATION COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Aspect          | Agent 1 | Agent 2 | Agent 3 | Agent 4 | Agent 5 |
|-----------------|---------|---------|---------|---------|---------|
| Architecture    | MVC     | Service | MVC     | MVC     | Modular |
| Edge Cases      | 3       | 5       | 4       | 3       | 6       |
| Error Handling  | Basic   | Robust  | Good    | Basic   | Robust  |
| Type Safety     | ✓       | ✓✓      | ✓       | ✓       | ✓✓      |
| Codebase Match  | 90%     | 75%     | 95%     | 85%     | 80%     |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 6: Synthesize Best Solution

**Combine the best elements from each agent:**

1. **Select base implementation** - Choose the one that best matches codebase patterns
2. **Incorporate edge cases** - Add edge cases from other agents the base missed
3. **Enhance error handling** - Use the most robust error handling approach
4. **Improve type safety** - Merge type definitions and validations
5. **Document sources** - Track which elements came from which agent

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                     SYNTHESIS DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Base: Agent 3 (best codebase pattern match)

Incorporating from other agents:
├─ Agent 2: Robust error handling pattern
├─ Agent 5: Edge cases for [empty input, concurrent access]
├─ Agent 2: Type definitions for [UserInput, ValidationResult]
└─ Agent 4: Caching optimization

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 7: Create Finalized Implementation Plan

Before implementing, create a **detailed execution plan** from the synthesized solution:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                 📋 IMPLEMENTATION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Files to Create

| # | File Path | Purpose | Source |
|---|-----------|---------|--------|
| 1 | path/to/NewService.ts | Main service class | Agent 3 base |
| 2 | path/to/types.ts | Type definitions | Agent 2 |
| 3 | path/to/utils.ts | Helper functions | Agent 5 |

## Files to Modify

| # | File Path | Changes | Source |
|---|-----------|---------|--------|
| 1 | path/to/index.ts | Add export | Agent 3 |
| 2 | path/to/config.ts | Add config entry | Agent 4 |
| 3 | path/to/app.ts | Register service | Agent 3 |

## Implementation Order

1. **Create types.ts** (no dependencies)
   - Define interfaces and types
   - From: Agent 2

2. **Create utils.ts** (depends on types)
   - Add helper functions
   - From: Agent 5

3. **Create NewService.ts** (depends on types, utils)
   - Main implementation
   - From: Agent 3 + Agent 2 error handling

4. **Modify config.ts** (no dependencies)
   - Add configuration
   - From: Agent 4

5. **Modify index.ts** (depends on NewService)
   - Export new service
   - From: Agent 3

6. **Modify app.ts** (depends on all above)
   - Register and initialize
   - From: Agent 3

## Edge Cases to Handle

| Edge Case | How Handled | Source |
|-----------|-------------|--------|
| Empty input | Return early with default | Agent 5 |
| Null values | Null coalescing + validation | Agent 2 |
| Concurrent access | Mutex lock | Agent 5 |
| Network timeout | Retry with backoff | Agent 4 |

## Error Handling Strategy

- Pattern: [from Agent 2]
- Logging: [approach]
- Recovery: [approach]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

This plan ensures:
- Correct dependency order
- All edge cases addressed
- Clear traceability to source agents

### Step 8: Execute Implementation Plan

Follow the plan step-by-step. For each step:
1. Create/modify the file as specified
2. Verify it matches the synthesized approach
3. Move to next step

### Step 9: Report Results

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    FEATURE COUNCIL RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📊 Implementation Comparison

| Agent | Architecture | Edge Cases | Error Handling | Codebase Fit |
|-------|--------------|------------|----------------|--------------|
| 1     | [approach]   | [count]    | [quality]      | [%]          |
| 2     | [approach]   | [count]    | [quality]      | [%]          |
| ...   | ...          | ...        | ...            | ...          |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔍 What Each Agent Contributed

### Agent 1
- Approach: [brief description]
- Unique strength: [what this agent did best]
- Used in final: [what was incorporated]

### Agent 2
- Approach: [brief description]
- Unique strength: [what this agent did best]
- Used in final: [what was incorporated]

... (for each agent)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📋 Implementation Plan Executed

| Step | File | Action | Status |
|------|------|--------|--------|
| 1 | path/to/types.ts | Created | ✅ |
| 2 | path/to/utils.ts | Created | ✅ |
| 3 | path/to/Service.ts | Created | ✅ |
| 4 | path/to/config.ts | Modified | ✅ |
| 5 | path/to/index.ts | Modified | ✅ |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🧬 Synthesis Breakdown

| Element | Source Agent | Reason |
|---------|--------------|--------|
| Base architecture | Agent 3 | Best codebase pattern match (95%) |
| Error handling | Agent 2 | Most comprehensive try/catch + logging |
| Edge case: empty input | Agent 5 | Only agent that handled this |
| Edge case: concurrent | Agent 5 | Race condition prevention |
| Type definitions | Agent 2 | Strictest typing |
| Caching layer | Agent 4 | Performance optimization |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📈 Final Solution Quality

- **Edge Cases Covered**: [total unique from all agents]
- **Error Handling**: [description]
- **Codebase Fit**: [% and explanation]
- **Type Safety**: [description]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ✅ Implemented Solution

[The synthesized implementation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📁 Files Created/Modified

[List of all files with brief descriptions]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Configuration

| Mode | Agents | Use Case |
|------|--------|----------|
| `feature council of 3` | 3 | Simple features, faster |
| `feature council of 5` | 5 | Good balance |
| `feature council of 7` | 7 | Complex features |
| `feature council of 10` | 10 | Maximum coverage |

If user just says `feature council`, ask them to choose.

---

## Difference from Code Council

| Aspect | Code Council | Feature Council |
|--------|--------------|-----------------|
| **Purpose** | Bug fixes, algorithms | Feature implementation |
| **Selection** | Majority voting | Synthesis/merge |
| **Output** | Single winning solution | Best-of-all combined |
| **Metric** | Correctness consensus | Comprehensiveness |

---

## Agents

10 feature solver agents in `agents/` directory:
- `feature-solver-1` through `feature-solver-10`

All agents:
- Same instructions (focused on feature implementation)
- Same temperature (0.7)
- Same tools (Read, Grep, Glob, LS)
- Use ultrathink (extended thinking)
- Emphasize codebase pattern matching and edge case coverage

---

## Why Synthesis > Voting for Features

With bugs, there's ONE correct answer. With features:
- Multiple valid architectures exist
- One agent might catch edge cases others miss
- Error handling approaches can be combined
- Type safety can be merged

Synthesis captures the **union of good ideas** rather than picking one.

---

## When to Use

✅ **Use feature-council for:**
- Complex features with many edge cases
- Features where you're unsure of best approach
- High-stakes production code
- When you want comprehensive coverage

❌ **Don't use for:**
- Simple CRUD operations
- Bug fixes (use code-council instead)
- When speed matters more than coverage
