---
name: context-compactor
description: Automatic context summarization for long-running sessions. Use when context is approaching limits, summarizing completed work, preserving critical information, or managing token budgets.
version: 1.0.0
category: autonomous-coding
layer: context-engineering
---

# Context Compactor

Automatically summarizes and compacts context when approaching token limits while preserving critical information.

## Quick Start

### Check if Compaction Needed
```python
from scripts.compactor import ContextCompactor

compactor = ContextCompactor()
if compactor.should_compact(context, limit=100000):
    compacted = compactor.compact(context)
```

### Compact Context
```python
compacted = compactor.compact(context)
# Preserves: architectural decisions, bugs, current state
# Discards: stale tool outputs, redundant messages
```

## Preservation Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                  PRESERVATION PRIORITY                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  MUST PRESERVE (Never remove)                               │
│  ├─ Architectural decisions                                 │
│  ├─ Unresolved bugs and blockers                           │
│  ├─ Current feature state                                   │
│  ├─ Recent file changes (last 5)                           │
│  └─ Error patterns and solutions                           │
│                                                              │
│  CAN SUMMARIZE (Compress to summary)                        │
│  ├─ Completed features (list of IDs)                       │
│  ├─ Resolved errors (brief mention)                        │
│  └─ Historical decisions (key points)                      │
│                                                              │
│  CAN DISCARD (Remove entirely)                              │
│  ├─ Redundant tool outputs                                 │
│  ├─ Stale search results                                   │
│  ├─ Superseded messages                                    │
│  └─ Verbose logging                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Compaction Process

1. **Score Importance**: Assign score to each message/content
2. **Identify Critical**: Mark must-preserve content
3. **Summarize Middle**: Compress can-summarize content
4. **Discard Stale**: Remove can-discard content
5. **Validate**: Ensure compacted context is coherent

## Token Budgets

| Context Type | Limit | Action |
|--------------|-------|--------|
| < 50% | Normal | No action |
| 50-75% | Warning | Prepare for compaction |
| 75-90% | Compact | Trigger compaction |
| > 90% | Critical | Aggressive compaction |

## Integration Points

- **autonomous-session-manager**: Triggers compaction check
- **memory-manager**: Stores compacted summaries
- **handoff-coordinator**: Uses compacted state for handoffs

## References

- `references/COMPACTION-STRATEGY.md` - Detailed strategy
- `references/TOKEN-BUDGETS.md` - Budget management

## Scripts

- `scripts/compactor.py` - Core ContextCompactor
- `scripts/importance_scorer.py` - Message scoring
- `scripts/summarizer.py` - Content summarization
- `scripts/token_estimator.py` - Token counting
