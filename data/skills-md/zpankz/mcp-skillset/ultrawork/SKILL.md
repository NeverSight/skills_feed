---
name: ultrawork
description: |
  Metasuperhypergraph orchestrator with fractal scale-invariant recursion. Activates maximum
  performance mode through renormalization-group optimization, power-law resource allocation,
  and homoiconic self-improvement. Triggers on "ultrawork", complex multi-domain tasks,
  or when parallelization/delegation yields superlinear returns.
allowed-tools: Task, Bash, Read, Write, Edit, Grep, Glob
model: opus
context: fork
agent: ultrawork-agent
user-invocable: true
---

<!-- Extended Metadata (lambda.omicron.tau framework) -->
<!-- o.class: "occurrent" | o.mode: "independent" -->
<!-- lambda.in: learn, delegate-router | lambda.out: all domain agents | lambda.kin: sisyphus, ralph -->
<!-- tau.goal: maximum parallelization; preserve eta>=4, convergence detection -->

# Ultrawork

> G_meta(lambda, Kappa, Sigma).tau' -- Orchestrate at all scales, compound gains exponentially.

## Navigation

**Concepts**: [scale-invariance](../learn/concepts/scale-invariance.md), [metagraph](../learn/concepts/metagraph.md), [homoiconicity](../learn/concepts/homoiconicity.md), [pareto-governance](../learn/concepts/pareto-governance.md), [convergence](../learn/concepts/convergence.md)

**Integration**: [delegate-router](../routers/delegate-router/SKILL.md), [learn](../learn/SKILL.md), [ARCHITECTURE](../../agents/ARCHITECTURE.md)

## Metasuperhypergraph Architecture

```
Level 0 (Sigma):     Entire Claude Config (self-referential schema)
Level 1 (G_meta):    Skills + Routers + Agents (hyperedges connecting triads)
Level 2 (G):         Individual component files
Level 3 (V):         Sections within files (frontmatter, body, graph)
Level 4 (v):         Individual properties/concepts

                    SCALE INVARIANCE
    structure(Level_n) ≅ structure(Level_{n+1}) ≅ lambda.o.tau
```

## Core Principles

### 1. Renormalization Group Optimization

Apply the same optimization at each scale level:

```python
def renormalize(G_level):
    """Coarse-grain, identify universality class, extract relevant operators."""
    # Identify redundant patterns
    redundant = find_duplicates(G_level)
    # Merge into canonical forms
    canonical = merge_to_canonical(redundant)
    # Project to lower-dimension effective theory
    return project(canonical, dim=relevant_operators_only)
```

| Scale | Renormalization Action | Universality Class |
|-------|------------------------|-------------------|
| Config | Consolidate routers (15 -> 7) | Delegation pattern |
| Skill | Merge duplicate content | lambda.o.tau triad |
| Agent | Domain agents absorb specialists | Execution pattern |
| File | Deduplicate sections | Frontmatter schema |

### 2. Power Law Resource Allocation (Pareto)

```
P(k) ~ k^{-alpha}  where alpha approx 2.5

Top 20% of agents handle 80% of tasks:
  oracle, sisyphus-junior, explore, engineer (4/20 = 20%)

Top 20% of skills deliver 80% of value:
  learn, ultrawork, git-master, lambda-skill, obsidian (5/23 approx 22%)
```

### 3. Homoiconic Self-Improvement

```python
# Ultrawork can improve itself
assert ultrawork.can_process(ultrawork.schema) == True

def self_improve(skill):
    analysis = skill.analyze(skill.schema)
    improvements = skill.generate_improvements(analysis)
    validated = skill.validate(improvements)
    return skill.apply(validated) if validated else skill
```

## Agent Routing Matrix (Power-Law Optimized)

### Tier 1: High-Frequency (80% of delegations)

| Agent | Model | Complexity | Use When |
|-------|-------|------------|----------|
| sisyphus-junior | Sonnet | 0.4-0.7 | Focused task execution, implementation |
| explore | Haiku | 0.1-0.3 | Pattern matching, file discovery, quick search |
| oracle | Opus | 0.7-1.0 | Root cause analysis, architecture decisions |
| engineer | Sonnet | 0.5-0.8 | Production-ready implementation |

### Tier 2: Medium-Frequency (15% of delegations)

| Agent | Model | Complexity | Use When |
|-------|-------|------------|----------|
| librarian | Sonnet | 0.3-0.5 | Documentation research, codebase understanding |
| architect | Opus | 0.8-1.0 | System design, multi-domain decomposition |
| prometheus | Sonnet | 0.5-0.7 | Strategic planning, roadmap design |
| researcher | Sonnet | 0.4-0.6 | Deep research with MCP tools |

### Tier 3: Low-Frequency (5% of delegations)

| Agent | Model | Complexity | Use When |
|-------|-------|------------|----------|
| document-writer | Haiku | 0.2-0.4 | README, API docs, technical writing |
| multimodal-looker | Sonnet | 0.3-0.5 | Screenshots, diagrams, visual analysis |
| momus | Haiku | 0.3-0.5 | Critical plan review, devil's advocate |
| metis | Sonnet | 0.4-0.6 | Pre-planning, hidden requirements |
| frontend-engineer | Sonnet | 0.4-0.7 | UI/UX, components, styling |

### External CLI Agents (Token Conservation)

| Agent | Binary | Context Limit | Use When |
|-------|--------|---------------|----------|
| gemini | /opt/homebrew/bin/gemini | 2M tokens | Large context analysis (>100K) |
| codex | ~/.local/bin/codex | 128K tokens | GPT code generation preference |
| amp | ~/.amp/bin/amp | 200K tokens | Claude-specific delegation |

## Execution Patterns

### Parallel Execution (Independent Tasks)

```yaml
# Launch simultaneously in single message
spawn:
  - Task(explore, "find auth files", run_in_background: true)
  - Task(librarian, "search auth docs", run_in_background: true)
  - Task(researcher, "find auth best practices", run_in_background: true)
collect: TaskOutput for each
merge: Deduplicate by content hash
```

### Sequential Execution (Dependent Tasks)

```yaml
# Chain with explicit dependencies
pipeline:
  - result_1 = Task(explore, "find relevant code")
  - result_2 = Task(oracle, "analyze: ${result_1}")
  - result_3 = Task(engineer, "implement fix: ${result_2}")
```

### Background Execution (Long-Running)

```yaml
background_operations:
  - Package installation: npm install, pip install, cargo build
  - Build processes: npm run build, make, tsc
  - Test suites: npm test, pytest, cargo test
  - Docker operations: docker build, docker pull
  - Large file operations: >1000 files
  - Subagent delegations: complexity > 0.7

foreground_operations:
  - Quick status: git status, ls, pwd (<5s)
  - File reads/edits
  - Simple commands
  - Verification checks
```

## Convergence Detection

### Fixed-Point Termination

```python
def at_fixed_point(state, epsilon=0.001):
    """Detect when further iteration yields no improvement."""
    new_state = iterate(state)
    return distance(state, new_state) < epsilon

def ultrawork_loop(task):
    state = initialize(task)
    while not at_fixed_point(state):
        state = parallel_execute(state)
        state = assess(state)
        if converged(state):
            break
    return finalize(state)
```

### Convergence Thresholds

| Pipeline | Threshold | Use When |
|----------|-----------|----------|
| R1 (Simple) | 0.85 | Single-domain, <10 files |
| R2 (Moderate) | 0.92 | Multi-domain, 10-50 files |
| R3 (Complex) | 0.96 | Architecture-level, >50 files |

## Verification Checklist (Invariants)

Before stopping, ALL must be true:

- [ ] **TODO LIST**: Zero pending/in_progress tasks
- [ ] **FUNCTIONALITY**: All requested features work
- [ ] **TESTS**: All tests pass (if applicable)
- [ ] **ERRORS**: Zero unaddressed errors
- [ ] **TOPOLOGY**: eta >= 4 (if knowledge graph modified)
- [ ] **MONOTONICITY**: len(K') >= len(K) (no knowledge lost)

**If ANY checkbox is unchecked, CONTINUE WORKING.**

## Integration with Learn Skill

Ultrawork extends [learn](../learn/SKILL.md) with:

```haskell
-- Learn: Sequential knowledge compounding
lambda(o, K, Sigma).tau' = renormalize . compound . assess . execute . route . parse

-- Ultrawork: Parallel orchestration with scale invariance
G_meta(lambda, K, Sigma).tau' = parallelize . delegate . renormalize . compound
```

### Post-Task Learning Loop

```yaml
after_completion:
  - Extract learnings via learn skill
  - Crystallize patterns with vertex-sharing
  - Update knowledge graph (K -> K')
  - If schema improvement identified: propose to user
```

## Invariants Preserved

| Invariant | Expression | Enforcement |
|-----------|------------|-------------|
| K-monotonicity | len(K') >= len(K) | Never delete knowledge |
| Topology | eta >= 4 | Minimum connectivity maintained |
| Homoiconicity | Sigma.can_process(Sigma) | Self-referential capability |
| Scale Invariance | structure(L_n) cong structure(L_{n+1}) | Same patterns at all levels |
| Power Law | P(k) ~ k^{-alpha} | 80/20 resource allocation |

## Quick Reference

```haskell
G_meta(lambda,K,Sigma).tau'   Parallelize -> Delegate -> Renormalize -> Compound
K grows                       Sigma evolves              eta>=4 preserved
Scale-invariant               Power-law optimized        Fixed-point convergent
```
