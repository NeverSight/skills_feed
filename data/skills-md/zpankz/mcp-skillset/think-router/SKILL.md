---
name: think-router
description: |
  Unified router for reasoning, research, and analysis tasks.
  Consolidates reasoning-router + research-router + analysis-router.
---

# Think Router (Unified)

**Consolidates**: reasoning-router + research-router + analysis-router
**Purpose**: All analytical/cognitive tasks

## Triggers
```yaml
patterns:
  - analyze, debug, troubleshoot, audit
  - reason, think, prove, verify
  - research, investigate, deep-dive, study
  - security, performance, optimization
```

## Thinking Modes

### Analysis Mode
```yaml
triggers: [analyze, debug, troubleshoot, audit, security, performance]
agent: oracle
workflows:
  - Root cause analysis
  - Security audit
  - Performance profiling
  - Code review

sc_commands:
  - sc:analyze → Codebase analysis
  - sc:troubleshoot → Systematic debugging
```

### Research Mode
```yaml
triggers: [research, investigate, deep-dive, study, learn]
agent: researcher
skills:
  - deep-research (db/skill-db) - 7-phase methodology
  - codebase-researcher (db/skill-db) - Systematic codebase analysis
workflows:
  - Classify → Scope → Hypothesize → Plan → Query → Triangulate → Synthesize
```

### Reasoning Mode
```yaml
triggers: [reason, think, prove, verify, logic]
skills:
  - hierarchical-reasoning (db/skill-db) - Strategic/Tactical/Operational
  - think (db/skill-db) - ThoughtBox + mental models
  - reason (db/skill-db) - Parse → Branch → Reduce → Ground → Emit

patterns:
  - Forward thinking (goal → actions)
  - Backward thinking (goal ← requirements)
  - Branching (explore alternatives)
  - First principles (fundamental truths)
  - Meta-reflection (reasoning about reasoning)
```

## Integration with Skills
```yaml
unified_skills:
  deep-research:
    core: 7-phase research methodology
    extensions: codebase analysis, web extraction

  hierarchical-reasoning:
    core: 3-level cognitive architecture
    extensions: ThoughtBox patterns, mental models
```

## References
- Original reasoning-router: ~/.claude/db/skills/routers/reasoning-router/
- Original research-router: ~/.claude/db/skills/routers/research-router/
- Original analysis-router: ~/.claude/db/skills/routers/analysis-router/
