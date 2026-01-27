---
name: parallel-agent-spawner
description: Spawn and coordinate parallel agents for faster completion. Use when running parallel tasks, spawning subagents, coordinating concurrent work, or optimizing throughput.
version: 1.0.0
category: autonomous-coding
layer: orchestration
---

# Parallel Agent Spawner

Spawns and coordinates parallel agents for faster feature completion.

## Quick Start

### Spawn Parallel Agents
```python
from scripts.parallel_spawner import ParallelSpawner

spawner = ParallelSpawner(project_dir)
results = await spawner.spawn_parallel(
    tasks=["feature-1", "feature-2", "feature-3"],
    agent_type="coding"
)
```

### Coordinate Results
```python
await spawner.wait_all()
summary = spawner.get_results_summary()
```

## Parallel Execution Model

```
┌─────────────────────────────────────────────────────────────┐
│                   PARALLEL EXECUTION                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MAIN ORCHESTRATOR                                          │
│  ├─ Analyzes feature dependencies                          │
│  ├─ Identifies parallelizable work                         │
│  ├─ Spawns worker agents                                   │
│  └─ Coordinates results                                    │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ Agent 1  │  │ Agent 2  │  │ Agent 3  │                 │
│  │          │  │          │  │          │                 │
│  │ feature-1│  │ feature-2│  │ feature-3│                 │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                 │
│       │             │             │                        │
│       ▼             ▼             ▼                        │
│  ┌─────────────────────────────────────────┐              │
│  │           RESULT AGGREGATOR              │              │
│  │  ├─ Collects all results                │              │
│  │  ├─ Resolves conflicts                  │              │
│  │  ├─ Merges code changes                 │              │
│  │  └─ Updates feature list                │              │
│  └─────────────────────────────────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Agent Types

| Type | Purpose | Parallelizable |
|------|---------|----------------|
| **coding** | Implement features | Yes, if independent |
| **testing** | Run E2E tests | Yes |
| **review** | Code review | Yes |
| **research** | Explore codebase | Yes |

## Spawn Configuration

```python
@dataclass
class SpawnConfig:
    max_parallel: int = 3
    timeout_per_agent: int = 1800  # 30 min
    retry_failed: bool = True
    merge_strategy: str = "sequential"  # or "git-merge"
```

## Integration Points

- **autonomous-loop**: Provides work to parallelize
- **coding-agent**: Worker agents for features
- **checkpoint-manager**: Create checkpoints before spawn
- **error-recoverer**: Handle agent failures

## References

- `references/PARALLELIZATION-STRATEGY.md` - Strategy guide
- `references/CONFLICT-RESOLUTION.md` - Merge conflicts

## Scripts

- `scripts/parallel_spawner.py` - Core spawner
- `scripts/agent_pool.py` - Agent pool management
- `scripts/result_aggregator.py` - Aggregate results
- `scripts/dependency_analyzer.py` - Find parallelizable work
