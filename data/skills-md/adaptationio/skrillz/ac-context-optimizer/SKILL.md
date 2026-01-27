---
name: ac-context-optimizer
description: Optimize context usage for autonomous coding. Use when managing context window, prioritizing information, reducing token usage, or improving efficiency.
---

# AC Context Optimizer

Optimize context window usage for efficient autonomous operation.

## Purpose

Manages and optimizes context usage to maximize effective operation within token limits.

## Quick Start

```python
from scripts.context_optimizer import ContextOptimizer

optimizer = ContextOptimizer(project_dir)
optimized = await optimizer.optimize_context(current_context)
priority = await optimizer.prioritize_information(items)
```

## API Reference

See `scripts/context_optimizer.py` for full implementation.
