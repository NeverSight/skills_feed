---
name: multi-agent-architecture-reference
description: 'Decision matrix for selecting multi-agent topologies (Supervisor, Swarm, Hierarchical, Conductor) with token economics, failure modes, and escalation paths'
version: 1.1.0
verified: true
lastVerifiedAt: '2026-03-01'
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, WebSearch, WebFetch]
agents: [architect, planner, master-orchestrator]
category: 'Planning & Architecture'
tags:
  [
    multi-agent,
    architecture,
    topology,
    orchestration,
    decision-matrix,
    conductor,
    supervisor,
    swarm,
    hierarchical,
  ]
---

# Multi-Agent Architecture Reference

<identity>
Canonical reference for multi-agent topology selection — provides a 6-topology decision matrix with token economics, failure modes, escalation paths, and links to existing agent-studio patterns.
</identity>

<capabilities>
- Select the optimal multi-agent topology for a given task based on complexity, cost constraints, and fault tolerance requirements
- Estimate token cost multiplier for each topology relative to single-agent baseline
- Identify known failure modes (SE-M01 through SE-M05) and their mitigations
- Map tasks to existing agent-studio patterns (wave-executor, consensus-voting, swarm-coordination)
- Provide escalation path guidance: when to upgrade TRIVIAL → Supervisor → Hierarchical
- Reference conductor pattern as agent-studio's default recommendation
</capabilities>

<instructions>

## Step 1: Characterize the Task

Answer these four questions before selecting a topology:

1. **Task independence**: Can sub-tasks run in parallel without shared state? (YES → Swarm or Fan-out)
2. **Task types known**: Is the set of task types stable and deterministic at design time? (YES → Supervisor)
3. **Phase complexity**: Does the work require multi-stage sub-orchestration? (YES → Hierarchical or Conductor)
4. **Stakes**: Does an incorrect outcome require multi-reviewer agreement? (YES → Consensus Voting)

## Step 2: Apply the Topology Decision Matrix

| Topology             | Token Cost | Best For                                                             | Failure Modes                                                              | Existing Skill           |
| -------------------- | ---------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------ |
| **Conductor**        | ~6x        | Sequential phases, ordered agent steps, default agent-studio pattern | Orchestrator overload (SE-M01)                                             | `master-orchestrator.md` |
| **Supervisor**       | ~5x        | Known task types, specialist agents, deterministic routing           | Single point of failure; router miscalibration (SE-M01)                    | Built into Router        |
| **Fan-out/Fan-in**   | ~8x        | Parallel review/analysis, map-reduce, search                         | Result aggregation complexity                                              | `wave-executor`          |
| **Swarm**            | ~8x        | Independent tasks, load balancing, fault-tolerant processing         | Coordination overhead; consensus deadlock; orphaned tasks (SE-M02, SE-M05) | `swarm-coordination`     |
| **Consensus Voting** | ~12x       | High-stakes decisions requiring multi-reviewer agreement             | Deadlock on split votes (SE-M02)                                           | `consensus-voting`       |
| **Hierarchical**     | ~15x       | EPIC complexity, multiple distinct phases with sub-orchestration     | Cascade failures; token runaway at depth >3 (SE-M03, SE-M04)               | Custom per project       |

**Token costs are relative to single-agent baseline (as of 2026). Use as order-of-magnitude guidance.**

## Step 3: Check Failure Mode Taxonomy

Before finalizing topology, verify mitigation for relevant failure modes:

**SE-M01: Coordinator Overload**

- Topologies affected: Supervisor, Conductor, Hierarchical root
- Symptom: Single coordinator receives more traffic than it can route
- Fix: Distribute coordination or add routing replicas; use `wave-executor` for fan-out

**SE-M02: Swarm Deadlock**

- Topologies affected: Swarm, Consensus Voting
- Symptom: Agents wait for each other's consensus indefinitely
- Fix: Timeout + majority-vote with tie-breaker; set consensus_timeout_ms

**SE-M03: Cascade Failure**

- Topologies affected: Hierarchical
- Symptom: A mid-level agent failure halts all downstream agents
- Fix: Circuit breakers at each tier; retry with backoff; fallback agents

**SE-M04: Token Runaway**

- Topologies affected: Hierarchical
- Symptom: Spawning too many levels burns tokens exponentially
- Fix: Set max_depth=3; monitor token budget per level; prefer Conductor over deep Hierarchical

**SE-M05: Orphaned Tasks**

- Topologies affected: Swarm
- Symptom: Agents drop tasks when no ownership is clear
- Fix: Assign task IDs; use TaskUpdate tracking; require TaskUpdate(in_progress) on pickup

## Step 4: Apply Escalation Path

Use the complexity escalation ladder when initial topology is insufficient:

```
TRIVIAL → Single agent (no multi-agent needed)
    ↓ (task types > 1, > 3 files)
LOW → Supervisor (router delegates to 2-3 specialists)
    ↓ (parallel processing needed)
MEDIUM → Conductor + Fan-out (master-orchestrator + wave-executor)
    ↓ (multi-phase with sub-orchestration)
HIGH → Hierarchical (orchestrators at multiple tiers)
    ↓ (high-stakes decision required)
EPIC → Hierarchical + Consensus Voting (max 3 tiers + voting gate)
```

## Step 5: Reference Existing agent-studio Patterns

| Pattern             | Skill/File                                            | Use Case                                            |
| ------------------- | ----------------------------------------------------- | --------------------------------------------------- |
| Conductor (DEFAULT) | `.claude/agents/orchestrators/master-orchestrator.md` | Sequential phase execution; TaskUpdate coordination |
| Fan-out/Fan-in      | `wave-executor` skill                                 | Parallel batch processing; EPIC-tier pipelines      |
| Swarm               | `swarm-coordination` skill                            | Concurrent independent task execution               |
| Consensus           | `consensus-voting` skill                              | High-stakes decisions; multi-reviewer agreement     |
| Supervisor          | Built into `router.md`                                | Task routing to specialist agents                   |

**When in doubt, start with Conductor.** The master-orchestrator pattern drives sequential phases with explicit TaskUpdate coordination — the lowest-risk default for most MEDIUM/HIGH tasks.

</instructions>

<examples>

### Example 1: Code Review Pipeline

- Task: Review 5 files for security, quality, and style
- Character: Tasks are independent (YES), parallel OK (YES)
- Topology: Fan-out/Fan-in (~8x)
- Pattern: `wave-executor` skill — spawn 3 reviewers in parallel, aggregate results

### Example 2: Feature Implementation

- Task: Design → Implement → Test → Document
- Character: Sequential phases, ordered steps (YES)
- Topology: Conductor (~6x)
- Pattern: `master-orchestrator` with TaskUpdate coordination between phases

### Example 3: Architecture Decision

- Task: Choose between 3 database options for production system
- Character: High stakes, requires agreement (YES)
- Topology: Consensus Voting (~12x)
- Pattern: `consensus-voting` skill — 3 architect agents vote, majority decides

### Example 4: Batch Agent Creation

- Task: Create 10 new agents from specs
- Character: Independent tasks (YES), fault tolerance > ordering (YES)
- Topology: Swarm (~8x)
- Pattern: `swarm-coordination` skill with task ID assignment per agent

</examples>

<best_practices>

- Default to Conductor (master-orchestrator) — it is the lowest-risk pattern for most tasks
- Never use Hierarchical beyond depth=3 (token runaway risk SE-M04)
- Always assign TaskUpdate(in_progress) on task pickup in Swarm to prevent SE-M05
- Use Fan-out (wave-executor) instead of Swarm when tasks have clear aggregation boundary
- Add consensus gate only for genuinely high-stakes decisions — 12x token cost is significant
- Document token budget per topology tier when spawning Hierarchical
- Cross-reference failure mode taxonomy before finalizing topology choice
  </best_practices>

## Iron Laws

1. **ALWAYS start with Conductor** — default to master-orchestrator for MEDIUM/HIGH tasks; only escalate to Hierarchical when sub-orchestration is explicitly required by the task structure.
2. **NEVER exceed depth=3 in Hierarchical** — token cost grows exponentially at each tier; depth >3 triggers SE-M04 (token runaway) and is considered an architectural defect.
3. **ALWAYS assign TaskUpdate(in_progress) on Swarm task pickup** — missing task ownership is the root cause of SE-M05 (orphaned tasks); every agent in a swarm must call TaskUpdate before doing work.
4. **NEVER use Consensus Voting for low-stakes decisions** — 12x token multiplier is justified only for architecture decisions, security approvals, or irreversible production changes.
5. **ALWAYS cross-reference the failure mode taxonomy before finalizing topology** — each topology has documented failure modes (SE-M01 through SE-M05); skipping this review leads to production incidents.

## Anti-Patterns

| Anti-Pattern                                                             | Problem                                                                                      | Fix                                                                                                        |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Defaulting to Hierarchical for every complex task                        | Token runaway at depth >3; cascade failure risk; over-engineering most tasks                 | Use Conductor (sequential phases) first; only escalate to Hierarchical when sub-orchestration is mandatory |
| Using Swarm for ordered, dependent tasks                                 | Swarm agents run concurrently and cannot enforce ordering; produces race conditions          | Use Conductor or Fan-out/Fan-in when task ordering matters                                                 |
| Skipping TaskUpdate(in_progress) in Swarm                                | Tasks become orphaned (SE-M05); no ownership tracking; duplicated or dropped work            | Require every swarm agent to call TaskUpdate(in_progress) as its first action                              |
| Adding Consensus Voting speculatively                                    | 12x token overhead kills budget for non-critical decisions; slowdown on all downstream tasks | Reserve consensus gate for genuinely high-stakes, irreversible decisions only                              |
| Mixing topology concerns (Supervisor + Swarm + Hierarchical in one flow) | Complexity explosion; routing ambiguity; impossible to debug failures                        | Pick one primary topology per orchestration scope; compose only at well-defined phase boundaries           |

## Memory Protocol (MANDATORY)

**Before starting:**

Read `.claude/context/memory/learnings.md` to check for prior multi-agent architecture decisions.

**After completing:**

- New topology decision → Append to `.claude/context/memory/decisions.md`
- Failure mode encountered → Append to `.claude/context/memory/issues.md`
- New pattern discovered → Append to `.claude/context/memory/learnings.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.

## Related Skills

- `wave-executor` — Fan-out/Fan-in implementation
- `swarm-coordination` — Swarm topology execution
- `consensus-voting` — Byzantine consensus for high-stakes decisions
- `architecture-review` — Validate topology choices against NFRs
- `complexity-assessment` — Determine complexity level before topology selection
