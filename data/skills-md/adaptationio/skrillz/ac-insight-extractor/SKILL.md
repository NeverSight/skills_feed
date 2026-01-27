---
name: ac-insight-extractor
description: Extract insights from autonomous coding sessions. Use when learning from completions, extracting patterns, analyzing decisions, or improving future performance.
---

# AC Insight Extractor

Extract insights and learnings from autonomous coding sessions.

## Purpose

Analyzes completed sessions to extract patterns, learnings, and improvements for future sessions.

## Quick Start

```python
from scripts.insight_extractor import InsightExtractor

extractor = InsightExtractor(project_dir)
insights = await extractor.extract_session_insights()
await extractor.apply_learnings(insights)
```

## API Reference

See `scripts/insight_extractor.py` for full implementation.
