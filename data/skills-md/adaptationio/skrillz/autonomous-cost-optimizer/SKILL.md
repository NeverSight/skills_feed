---
name: autonomous-cost-optimizer
description: Token and cost optimization for autonomous coding. Use when tracking token usage, optimizing API costs, managing budgets, or improving efficiency.
version: 1.0.0
category: autonomous-coding
layer: orchestration
---

# Autonomous Cost Optimizer

Tracks and optimizes token usage and API costs during autonomous coding.

## Quick Start

### Track Usage
```python
from scripts.cost_optimizer import CostOptimizer

optimizer = CostOptimizer(project_dir)
optimizer.track_usage(input_tokens=1500, output_tokens=500)

report = optimizer.get_usage_report()
print(f"Total cost: ${report.total_cost:.4f}")
```

### Check Budget
```python
if optimizer.is_within_budget(budget=10.00):
    # Continue working
    pass
else:
    # Trigger cost-saving measures
    await optimizer.enter_efficiency_mode()
```

## Cost Optimization Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                 COST OPTIMIZATION                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TRACK                                                      │
│  ├─ Monitor token usage per request                        │
│  ├─ Calculate cost per feature                             │
│  ├─ Track cumulative session cost                          │
│  └─ Log usage to history                                   │
│                                                             │
│  ANALYZE                                                    │
│  ├─ Identify high-cost operations                          │
│  ├─ Compare efficiency across features                     │
│  ├─ Detect wasteful patterns                               │
│  └─ Calculate ROI per feature                              │
│                                                             │
│  OPTIMIZE                                                   │
│  ├─ Compact context when approaching limits                │
│  ├─ Cache repeated queries                                 │
│  ├─ Batch similar operations                               │
│  └─ Prioritize high-ROI features                           │
│                                                             │
│  REPORT                                                     │
│  ├─ Generate cost breakdown                                │
│  ├─ Show efficiency metrics                                │
│  └─ Recommend optimizations                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Pricing Reference

| Model | Input (per 1M) | Output (per 1M) |
|-------|----------------|-----------------|
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Opus | $15.00 | $75.00 |
| Claude 3 Haiku | $0.25 | $1.25 |

## Efficiency Metrics

```python
@dataclass
class EfficiencyMetrics:
    tokens_per_feature: float
    cost_per_feature: float
    features_per_dollar: float
    context_utilization: float
    cache_hit_rate: float
```

## Optimization Strategies

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| **Context compaction** | 20-40% | Slight context loss |
| **Response caching** | 30-50% | Storage needed |
| **Batch operations** | 15-25% | Higher latency |
| **Model selection** | 50-90% | Capability reduction |

## Integration Points

- **context-compactor**: Reduce context size
- **memory-manager**: Cache common queries
- **autonomous-loop**: Budget enforcement
- **progress-tracker**: Efficiency metrics

## References

- `references/PRICING-GUIDE.md` - Cost calculations
- `references/OPTIMIZATION-STRATEGIES.md` - Strategies

## Scripts

- `scripts/cost_optimizer.py` - Core optimizer
- `scripts/usage_tracker.py` - Track token usage
- `scripts/budget_manager.py` - Budget enforcement
- `scripts/efficiency_analyzer.py` - Analyze efficiency
