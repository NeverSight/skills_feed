---
name: designing
description: Design Session - collaborative brainstorming to turn ideas into actionable implementation plans using the Unified Pipeline methodology. Use when user types "ds" or wants to explore/design a feature before implementation. "pl" triggers phases 5-10 (STANDALONE/ALIAS/NO-OP modes). MUST load maestro-core skill first for routing.
---

# Design & Planning

Turn ideas into fully-formed, implementation-ready designs through a unified 10-phase pipeline.

## Entry Points

| Trigger | Action |
|---------|--------|
| `ds` | Start unified pipeline (all 10 phases) |
| `/conductor-design` | Start unified pipeline (alias) |
| `cn`, `/conductor-newtrack` | Create spec + plan + beads from existing design.md |
| `pl`, `/plan` | Planning phases (5-10) - see pl Entry Modes below |
| "design a feature" | Start unified pipeline |
| "let's think through X" | Start unified pipeline |

## Quick Reference

### Unified Pipeline (10 Phases)

| # | Phase | Type | Purpose | Exit Criteria |
|---|-------|------|---------|---------------|
| 1 | **DISCOVER** | Diverge | Explore problem + research context | Problem articulated |
| 2 | **DEFINE** | Converge | Frame problem + select approach | Approach selected |
| 3 | **DEVELOP** | Diverge | Architecture + components | Interfaces defined |
| 4 | **VERIFY** | Converge | Oracle audit + risk assessment | Oracle APPROVED |
| 5 | **DECOMPOSE** | Execute | Create beads (fb) | Beads filed |
| 6 | **VALIDATE** | Execute | Dependency check (bv) + Oracle review | Dependencies valid |
| 7 | **ASSIGN** | Execute | Track assignments | Tracks assigned |
| 8 | **READY** | Complete | Handoff to ci/co/ca | Execution ready |
| 9 | **EXECUTE** | Implement | Run ci/co/ca on tracks | All beads completed |
| 10 | **FINISH** | Archive | Extract learnings + archive track | Track archived |

See [pipeline.md](references/pipeline.md) for full details.

## Mode Routing

Complexity scoring determines execution mode:

| Score | Mode | Phases | A/P/C | Research |
|-------|------|--------|-------|----------|
| < 4 | **SPEED** | 1,2,4,8 | No | 1 hook (start) |
| 4-6 | **ASK** | User chooses | Optional | User chooses |
| > 6 | **FULL** | 1-10 | Yes | 2 hooks |

### Mode Comparison

| Aspect | SPEED (< 4) | FULL (> 6) |
|--------|-------------|------------|
| Phases | 1,2,4,8 | All 10 |
| A/P/C | No | Yes |
| Research | 1 hook | 2 hooks |
| Beads | No | Yes |
| Tracks | No | Yes |
| Verification | Advisory | Mandatory |
| Use `[E]` to escalate | Yes | N/A |

## Core Principles

- **One question at a time** - Don't overwhelm
- **Multiple choice preferred** - Easier to answer
- **YAGNI ruthlessly** - Remove unnecessary features
- **Explore alternatives** - Always propose 2-3 approaches
- **Research consolidated** - 2 strategic hooks, not 5

## ⛔ EXECUTION BLOCKS (CRITICAL)

**This skill contains EXECUTION BLOCKS marked with ⛔. When you encounter one, you MUST:**
1. **STOP** what you're doing
2. **EXECUTE** the tool calls specified (Task(), oracle(), skill())
3. **WAIT** for results before proceeding

**EXECUTION BLOCKS are NOT documentation - they are COMMANDS you must execute.**

See [pipeline.md](references/pipeline.md) for all execution blocks.

## Session Flow

0. **Load Core** - Load [maestro-core](../maestro-core/SKILL.md) for routing table and fallback policies
1. **Initialize** - Load handoffs, CODEMAPS, verify conductor setup → [session-init.md](references/session-init.md)
2. **Research** - ⛔ EXECUTION BLOCK at Phase 1 start (spawn 3 Task() agents)
3. **Route** - Score complexity (< 4 = SPEED, > 6 = FULL) → [design-routing-heuristics.md](references/design-routing-heuristics.md)
4. **Execute** - 10-phase pipeline with A/P/C checkpoints → [pipeline.md](references/pipeline.md)
5. **Validate** - ⛔ EXECUTION BLOCK at Phase 4 (call oracle())
6. **Complete** - Phase 8 (READY) triggers `ci`/`co`/`ca` → Phase 9 (EXECUTE) → Phase 10 (FINISH)

### Research Hooks (Consolidated)

| Hook | Trigger | Agents | Purpose |
|------|---------|--------|---------|
| **research-start** | Phase 1 (DISCOVER) | Locator + Pattern + CODEMAPS + Architecture | All initial context |
| **research-verify** | Phase 3→4 (DEVELOP→VERIFY) | Analyzer + Pattern + Impact + Web | Design verification |

### Validation Gates

| Checkpoint | Focus | Enforcement |
|------------|-------|-------------|
| CP1 (DISCOVER) | Product alignment, no duplicate features | WARN |
| CP2 (DEFINE) | Problem clear, success measurable, scope explicit | WARN |
| CP3 (DEVELOP) | 3+ options, tech-stack alignment, risk analysis | WARN |
| CP4 (VERIFY) | Full validation + grounding + impact scan | SPEED=WARN, FULL=HALT |

## Adaptive A/P/C System

A/P/C checkpoints work **adaptively** across the entire workflow.

### State Ladder

```
INLINE → MICRO_APC → NUDGE → DS_FULL → DS_BRANCH → BRANCH_MERGE
```

| State | Description | Trigger |
|-------|-------------|---------|
| **INLINE** | Normal flow (conductor/beads) | Default |
| **MICRO_APC** | Lightweight checkpoint at boundaries | End of spec/plan section |
| **NUDGE** | Suggest upgrade to DS | 3+ design iterations |
| **DS_FULL** | Full 10-phase with A/P/C | `ds` command or upgrade |
| **DS_BRANCH** | DS attached to design branch | Design rethink in track |
| **BRANCH_MERGE** | Apply branch changes | Branch complete |

### A/P/C in FULL Mode

At end of phases 1-4:

- **[A] Advanced** - Phase-specific deep dive
- **[P] Party** - Multi-agent feedback (BMAD v6) → [bmad/](references/bmad/)
- **[C] Continue** - Proceed to next phase
- **[↩ Back]** - Return to previous phase

| After Phase | A Option |
|-------------|----------|
| 1 (DISCOVER) | Advanced assumption audit |
| 2 (DEFINE) | Scope stress-test |
| 3 (DEVELOP) | Architecture deep-dive |
| 4 (VERIFY) | Oracle runs BEFORE showing menu |

### Priority Rules

1. **Explicit commands** (`ds`) always win
2. **Active DS/Branch** blocks passive triggers
3. **Branch safety** preferred when in implementation
4. **Micro A/P/C** at checkpoint boundaries
5. **Nudge** after 3+ iterations

See [apc-checkpoints.md](references/apc-checkpoints.md) for implementation details.

## Phase 4: VERIFY - Spike Execution

When risk assessment identifies HIGH risk items:

```
HIGH risk items → MUST spawn spike Task()
                       │
                       ▼
              For each HIGH risk:
              1. Create spike bead + dir
              2. MUST spawn Task() with time-box
              3. Wait for completion
              4. Capture result (YES/NO)
                       │
                       ▼
              MUST call oracle() for 6-dimension audit
                       │
               ┌───────┴───────┐
               │               │
        All spikes YES   Any spike NO
               │               │
               ▼               ▼
           Continue       HALT - user decision
```

⚠️ **MANDATORY:** You MUST call `oracle()` at Phase 4 - see [pipeline.md](references/pipeline.md#phase-4-verify-converge)

## Phase 6: VALIDATE - Oracle Beads Review

⚠️ **MANDATORY:** After `bv` validation, you MUST call `oracle()` to review beads completeness.

See [pipeline.md](references/pipeline.md#phase-6-validate-execute)

## Phase 8: READY - Auto-Orchestration

```
Ready to execute. Found N tracks:
• Track A (BlueLake): 4 beads
• Track B (GreenCastle): 3 beads

[O] Orchestrate (spawn workers)
[S] Sequential (run ci manually)
[R] Ralph (autonomous loop - ca)

Default: [O] after 30s
```

> **Note:** `[R]` is available when `ralph.enabled == true` in track `metadata.json`.

⚠️ **MANDATORY:** If user selects [O] and ≥2 tracks exist, you MUST spawn `Task()` for each track.

See [pipeline.md](references/pipeline.md#phase-8-ready-complete)

## `pl` Entry Gate

⚠️ **MANDATORY:** Before running `pl`, detect input and bootstrap if needed:

```
pl triggered
    │
    ▼
Input detection (priority order):
    1. design.md exists? → ALIAS mode (skip discovery)
    2. PRD file exists?  → STANDALONE mode (parse PRD)
    3. User file attached? → STANDALONE mode
    4. No input?         → BOOTSTRAP mode (prompt → create track)
```

| Input Source | Mode | Action |
|--------------|------|--------|
| design.md | ALIAS | Skip Phase 5, run 6-10 |
| PRD file | STANDALONE | Parse PRD, run 5-10 |
| User file | STANDALONE | Use as context, run 5-10 |
| None | BOOTSTRAP | Prompt → create track → run 5-10 |

**BOOTSTRAP creates:** `conductor/tracks/<id>/` with design.md + metadata.json

## `pl` Compatibility

| Scenario | Mode | Behavior |
|----------|------|----------|
| `pl` after `ds` Phase 4 | NO-OP | Not needed - phases 5-10 auto-run in FULL mode |
| `pl` with design.md | ALIAS | Skip Phase 5 discovery, run 6-10 |
| `pl` with PRD file | STANDALONE | Parse PRD, run full 5-10 |
| `pl` with user request | STANDALONE | Run full discovery, phases 5-10 |
| `pl` without any input | ERROR | Prompt for input source |

## Anti-Patterns

- ❌ Jumping to solutions before understanding the problem
- ❌ Skipping verification at Phase 4 (VERIFY)
- ❌ Asking multiple questions at once
- ❌ Over-engineering simple features (use SPEED mode)
- ❌ Running `pl` after `ds` completes (no longer needed)

## Next Steps (after Phase 8: READY)

| Command | Description | Phase |
|---------|-------------|-------|
| `ci` | `/conductor-implement` - Execute track | Phase 9 (EXECUTE) |
| `co` | `/conductor-orchestrate` - Spawn parallel workers | Phase 9 (EXECUTE) |
| `ca` | `/conductor-autonomous` - Ralph loop | Phase 9 (EXECUTE) |
| `/conductor-finish` | Archive track + extract learnings | Phase 10 (FINISH) |

See [maestro-core](../maestro-core/SKILL.md) for full routing table.

## Dependencies

**Auto-loads:** [maestro-core](../maestro-core/SKILL.md) for routing and fallback policies.

## Related

- [conductor](../conductor/SKILL.md) - Track creation and implementation
- [tracking](../tracking/SKILL.md) - Issue tracking after design
- [orchestrator](../orchestrator/SKILL.md) - Parallel execution in Phase 9 (EXECUTE)
