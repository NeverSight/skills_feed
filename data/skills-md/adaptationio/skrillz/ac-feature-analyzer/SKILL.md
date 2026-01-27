---
name: ac-feature-analyzer
description: Analyze features and their dependencies. Use when mapping feature relationships, detecting blockers, optimizing build order, or identifying critical paths.
---

# AC Feature Analyzer

Analyze features, dependencies, and critical paths for optimal implementation order.

## Purpose

Analyzes feature relationships to determine optimal build order, identify blockers, and calculate critical paths for efficient autonomous implementation.

## Quick Start

```python
from scripts.feature_analyzer import FeatureAnalyzer

analyzer = FeatureAnalyzer(project_dir)
analysis = await analyzer.analyze()
print(analysis.critical_path)
print(analysis.next_feature)
```

## Analysis Output

```json
{
  "dependency_graph": {
    "auth-001": [],
    "auth-002": ["auth-001"],
    "api-001": ["auth-001", "data-001"]
  },
  "critical_path": ["data-001", "auth-001", "auth-002", "api-001"],
  "blockers": {
    "api-001": ["auth-001", "data-001"]
  },
  "categories": {
    "authentication": {"total": 10, "completed": 3},
    "api": {"total": 15, "completed": 0}
  },
  "next_features": ["data-001", "auth-003"],
  "bottlenecks": ["auth-001"],
  "parallel_opportunities": [
    ["ui-001", "ui-002", "ui-003"],
    ["test-001", "test-002"]
  ]
}
```

## Analysis Types

### Dependency Analysis
- Build dependency graph
- Detect circular dependencies
- Identify missing dependencies
- Calculate dependency depth

### Critical Path
- Find longest dependency chain
- Identify features that block most others
- Calculate minimum completion time
- Optimize for parallel execution

### Progress Analysis
- Track completion by category
- Identify stalled areas
- Calculate velocity
- Predict completion time

### Blocker Detection
- Find blocked features
- Identify blocking features
- Suggest unblocking order
- Calculate blocker impact

## Workflow

1. **Load**: Read feature list
2. **Graph**: Build dependency graph
3. **Analyze**: Calculate paths and blockers
4. **Optimize**: Determine optimal order
5. **Report**: Output analysis results

## Integration

- Input: Feature list from `ac-state-tracker`
- Output: Analysis for `ac-session-manager`
- Used by: `ac-complexity-assessor`, orchestration skills

## API Reference

See `scripts/feature_analyzer.py` for full implementation.
