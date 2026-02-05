---
name: delegate
description: |
  Multi-AI orchestration primitive. Delegate to specialized AI tools, collect outputs, synthesize.
  Use when: analysis, review, audit, investigation tasks need multiple expert perspectives.
  Keywords: orchestrate, delegate, multi-ai, parallel, synthesis, consensus, dag, swarm
---

# /delegate

> You orchestrate. Specialists do the work.

Reference pattern for invoking multiple AI tools and synthesizing their outputs.

## Your Role

You don't analyze/review/audit yourself. You:
1. **Route** — Send work to appropriate specialists
2. **Collect** — Gather their outputs
3. **Curate** — Validate, filter, resolve conflicts
4. **Synthesize** — Produce unified output

## Your Team

### Moonbridge MCP — Unified Agent Interface

**One interface, multiple backends.** Moonbridge wraps both Codex and Kimi:

| Adapter | Strengths | When to Use |
|---------|-----------|-------------|
| `codex` | Long-context, tool calling, security | Refactors, migrations, debugging, backend |
| `kimi`  | Native vision, extended thinking | UI from designs, visual debugging, frontend |

**Single agent:**
```
mcp__moonbridge__spawn_agent({
  "prompt": "...",
  "adapter": "codex",           // or "kimi"
  "reasoning_effort": "high"    // codex: low/medium/high/xhigh
  // OR
  "thinking": true              // kimi: extended reasoning
})
```

**Timeout:** Moonbridge defaults: Codex=30min, Kimi=10min. Override for edge cases:

| Task | Timeout |
|------|---------|
| Quick check | `60` |
| Large refactor | `3600` |

```
mcp__moonbridge__spawn_agent({ ..., "timeout_seconds": 3600 })
```

**Parallel agents (same or mixed adapters):**
```
mcp__moonbridge__spawn_agents_parallel({
  "agents": [
    {"prompt": "Backend API", "adapter": "codex", "reasoning_effort": "high"},
    {"prompt": "Frontend UI", "adapter": "kimi", "thinking": true},
    {"prompt": "Tests", "adapter": "codex", "reasoning_effort": "medium"}
  ]
})
```

### Gemini CLI — Researcher, deep reasoner
- Web grounding, thinking_level control, agentic vision
- Best at: current best practices, pattern validation, design research
- Invocation: `gemini "..."` (bash)

### Non-Agentic (Opinions Only)

**Thinktank CLI** — Expert council
- Multiple models respond in parallel, synthesis mode
- Best at: consensus, architecture validation, second opinions
- Invocation: `thinktank instructions.md ./files --synthesis` (bash)
- **Note**: Cannot take action. Use for validation, not investigation.

### Internal Agents (Task tool)

Domain specialists for focused review:
- `go-concurrency-reviewer`, `react-pitfalls`, `security-sentinel`
- `data-integrity-guardian`, `architecture-guardian`, `config-auditor`

## How to Delegate

Apply `/llm-communication` principles — state goals, not steps:

### To Moonbridge Agents (Codex, Kimi)

Give them latitude to investigate:
```
"Investigate this stack trace. Find root cause. Propose fix with file:line."
```

NOT:
```
"Step 1: Read file X. Step 2: Check line Y. Step 3: ..."
```

### To Thinktank (Non-Agentic)

Provide context, ask for judgment:
```
"Here's the code and proposed fix. Is this approach sound?
What are we missing? Consensus and dissent."
```

### Parallel Execution

Run independent reviews in parallel:
- Multiple moonbridge agents in same call (`spawn_agents_parallel`)
- Multiple Task tool calls in same message
- Gemini + Thinktank can run concurrently (both bash)

## Dependency-Aware Orchestration

For large work (10+ subtasks, multiple phases), use DAG-based scheduling:

### The Pattern

```
Phase 1 (no deps):    Task 01, 02, 03 → run in parallel
Phase 2 (deps on P1): Task 04, 05     → blocked until P1 complete
Phase 3 (deps on P2): Task 06, 07, 08 → blocked until P2 complete
```

Key principles:
1. **Task decomposition** — Break feature into atomic subtasks
2. **Dependency graph** — DAG defines execution order
3. **Parallel execution** — Independent tasks run simultaneously
4. **Fresh context** — Each subagent starts clean (~40-75k tokens)

### Step 1: Decompose

Split feature into atomic tasks. Ask:
- What can run independently? → Same phase
- What requires prior output? → Blocked

### Step 2: Declare Dependencies

Use TaskCreate/TaskUpdate primitives:
```
TaskCreate({subject: "Install packages", activeForm: "Installing packages"})
TaskCreate({subject: "cRPC builder", activeForm: "Building cRPC"})
TaskUpdate({taskId: "2", addBlockedBy: ["1"]})  # Task 2 waits for Task 1
```

### Step 3: Execute Phases

Spawn all unblocked tasks in single message:
```
# Phase 1 - all parallel via moonbridge
mcp__moonbridge__spawn_agents_parallel({
  agents: [
    {prompt: "Task 1: ...", adapter: "codex"},
    {prompt: "Task 2: ...", adapter: "codex"},
    {prompt: "Task 3: ...", adapter: "kimi", thinking: true}
  ]
})
```

### Step 4: Progress

After each phase:
1. Mark completed tasks: `TaskUpdate({taskId: "1", status: "completed"})`
2. Check newly-unblocked: `TaskList()`
3. Spawn next phase

### When to Use DAG Orchestration

| Scenario | Use DAG? |
|----------|----------|
| Large migration (10+ files, phases) | ✅ Yes |
| Multi-feature release | ✅ Yes |
| Single feature (1-5 files) | ❌ Overkill |
| Quick fix | ❌ Overkill |

For typical feature work, simple parallel spawning is sufficient.

## Curation (Your Core Job)

For each finding:

**Validate**: Real issue or false positive? Applies to our context?
**Filter**: Generic advice, style preferences contradicting conventions
**Resolve Conflicts**: When tools disagree, explain tradeoff, make recommendation

## Output Template

```markdown
## [Task]: [subject]

### Action Plan

#### Critical
- [ ] `file:line` — Issue — Fix: [action] (Source: [tool])

#### Important
- [ ] `file:line` — Issue — Fix: [action] (Source: [tool])

#### Suggestions
- [ ] [improvement] (Source: [tool])

### Synthesis

**Agreements** — Multiple tools flagged:
- [issue]

**Conflicts** — Differing opinions:
- [Tool A] vs [Tool B]: [your recommendation]

**Research** — From Gemini:
- [finding with citation]
```

## When to Use

- **Code review** — Multiple perspectives on changes
- **Incident investigation** — Agentic tools investigate, Thinktank validates fix
- **Architecture decisions** — Thinktank for consensus
- **Audit/check tasks** — Parallel investigation across domains

## Note

All Codex delegation goes through Moonbridge MCP. Use `mcp__moonbridge__spawn_agent` with `adapter: "codex"`. This gives you:
- Single interface for both Kimi and Codex
- Mixed-adapter parallel spawning
- Consistent parameter naming

## Related

- `/llm-communication` — Prompt writing principles
- `/review-branch` — Example implementation
- `/thinktank` — Multi-model synthesis
- `/codex-coworker` — Codex delegation patterns
