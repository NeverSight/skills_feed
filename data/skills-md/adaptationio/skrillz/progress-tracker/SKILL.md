---
name: progress-tracker
description: Track and report progress across autonomous coding sessions. Use when generating progress reports, calculating metrics, visualizing completion, or estimating time to completion.
version: 1.0.0
category: autonomous-coding
layer: core-workflow
---

# Progress Tracker

Tracks and reports progress across autonomous coding sessions with metrics, visualization, and completion estimation.

## Quick Start

### Get Progress Metrics
```python
from scripts.progress_tracker import ProgressTracker

tracker = ProgressTracker(project_dir)
metrics = tracker.get_progress()

print(f"Features: {metrics.passing}/{metrics.total}")
print(f"Progress: {metrics.percentage:.1f}%")
```

### Generate Report
```python
report = tracker.generate_report(format="markdown")
print(report)
```

### Visualize Progress
```python
visualization = tracker.visualize_progress()
print(visualization)
# ████████████░░░░░░░░ 60% (30/50)
```

## Progress Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                    PROGRESS DASHBOARD                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Overall Progress                                            │
│  ████████████████░░░░░░░░░░░░░░░░░░░░  45%                  │
│                                                              │
│  Features: 45/100 passing                                    │
│  Sessions: 12 completed                                      │
│  Commits: 87 made                                            │
│                                                              │
│  By Category                                                 │
│  ├─ auth:     ████████████████████ 100% (5/5)              │
│  ├─ crud:     ██████████████░░░░░░  70% (14/20)            │
│  ├─ ui:       ████████░░░░░░░░░░░░  40% (12/30)            │
│  ├─ api:      ██████████████████░░  90% (9/10)             │
│  ├─ testing:  ██░░░░░░░░░░░░░░░░░░  10% (2/20)             │
│  └─ other:    ██████░░░░░░░░░░░░░░  30% (3/10)             │
│                                                              │
│  Estimated Completion                                        │
│  ├─ At current rate: ~15 sessions remaining                 │
│  ├─ Time estimate: ~7.5 hours                               │
│  └─ Sessions per day: 3                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Metrics Tracked

| Metric | Description |
|--------|-------------|
| **Features** | Passing/total feature count |
| **Progress %** | Completion percentage |
| **Sessions** | Number of sessions completed |
| **Commits** | Number of git commits |
| **Velocity** | Features per session |
| **ETA** | Estimated sessions to completion |

## Integration Points

- **context-state-tracker**: Reads feature and progress data
- **coding-agent**: Tracks feature completion
- **autonomous-loop**: Uses metrics for continuation decisions

## References

- `references/METRICS.md` - Detailed metrics documentation
- `references/REPORT-FORMATS.md` - Report format options

## Scripts

- `scripts/progress_tracker.py` - Core ProgressTracker class
- `scripts/metrics_calculator.py` - Metrics calculations
- `scripts/report_generator.py` - Report generation
- `scripts/visualization.py` - ASCII visualization
