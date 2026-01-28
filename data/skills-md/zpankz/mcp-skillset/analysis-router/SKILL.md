---
name: analysis-router
description: Routes analysis and debugging tasks. Triggers on analyze, debug, troubleshoot, review, audit, security, performance, optimize, investigate, trace.
---

# Analysis Router

Routes analysis, debugging, and review tasks to specialized skills.

## Subcategories

### Code Analysis
```yaml
triggers: [analyze, review, understand, trace, flow, structure]
skills:
  - sc:analyze: Code quality, security, performance, architecture analysis
  - systematic-debugging: Structured debugging approach
```

### Security Analysis
```yaml
triggers: [security, audit, vulnerability, injection, auth, permissions]
skills:
  - dev:security:security-audit: Security vulnerability scanning
  - dev:security:secure-prompts: Prompt injection defense
  - dev:security:check-best-practices: Security best practices
```

### Performance Analysis
```yaml
triggers: [performance, optimize, bottleneck, profiling, memory, speed]
skills:
  - sc:improve: Systematic improvements
  - parallel-debug-orchestrator: Parallel debugging
```

### Architecture Analysis
```yaml
triggers: [architecture, design, patterns, refactor, structure]
skills:
  - dev:architecture:explain-architecture-pattern: Pattern explanation
  - sc:design: System design
```

## Routing Decision Tree

```
analysis request
    │
    ├── Security focus?
    │   ├── Audit? → security-audit
    │   ├── Prompts? → secure-prompts
    │   └── Best practices → check-best-practices
    │
    ├── Performance focus?
    │   ├── Debugging? → parallel-debug-orchestrator
    │   └── Optimization → sc:improve
    │
    ├── Architecture focus?
    │   └── explain-architecture-pattern
    │
    └── General analysis?
        ├── Debugging? → systematic-debugging
        └── Review → sc:analyze
```

## Managed Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| sc:analyze | Code analysis | "analyze code", "review" |
| systematic-debugging | Structured debug | "debug", "troubleshoot" |
| parallel-debug-orchestrator | Parallel debug | "complex bug", "multiple issues" |
| security-audit | Security scan | "security audit", "vulnerabilities" |
| secure-prompts | Prompt security | "prompt injection", "secure prompts" |
| sc:improve | Improvements | "improve", "optimize" |
