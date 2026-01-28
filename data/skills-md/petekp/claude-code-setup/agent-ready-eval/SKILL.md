---
name: agent-ready-eval
description: Evaluate a codebase for agent-friendliness based on autonomous agent best practices. Use when asked to "evaluate for agents", "check agent readiness", "audit for autonomous execution", "assess agent-friendliness", or when reviewing infrastructure for unattended agent operation. Also use when asked about making a codebase more suitable for AI agents or autonomous workflows.
---

# Agent-Ready Evaluation

Evaluate how well a codebase supports autonomous agent execution based on the "How to Get Out of Your Agent's Way" principles.

## Core Philosophy

Autonomous agents fail for predictable reasons—most are system design failures, not model failures. This evaluation checks whether infrastructure enables true autonomy: agents that run unattended, isolated, reproducible, and bounded by system constraints rather than human intervention.

## Evaluation Process

### 1. Gather Evidence

Explore the codebase for indicators across all 12 principles. Key files to examine:

**Environment & Isolation:**
- `Dockerfile`, `docker-compose.yml`, `.devcontainer/`
- `Makefile`, `setup.sh`, `bootstrap.sh`
- CI configs (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`)
- Nix files, `devbox.json`, `flake.nix`

**Dependencies & State:**
- Lockfiles (`package-lock.json`, `yarn.lock`, `Pipfile.lock`, `Cargo.lock`, `go.sum`)
- Database configs, migration files, seed scripts
- `.env.example`, config templates

**Execution & Interfaces:**
- CLI entry points, `bin/` scripts
- API definitions, OpenAPI specs
- Background job configs (Sidekiq, Celery, Bull)
- Timeout/limit configurations

**Quality & Monitoring:**
- Test suites, benchmark files
- Logging configuration
- Cost tracking, rate limiting setup

### 2. Score Each Principle

Read [evaluation-criteria.md](references/evaluation-criteria.md) for detailed scoring rubric.

Score each of the 12 principles 0-3:
- **3**: Fully implemented with clear evidence
- **2**: Partially implemented, room for improvement
- **1**: Minimal awareness, significant gaps
- **0**: No evidence

### 3. Generate Report

Output format:

```markdown
# Agent-Ready Evaluation Report

**Overall Score: X/36** (Y%)
**Rating: [Excellent|Good|Needs Work|Not Agent-Ready]**

## Summary
[2-3 sentence assessment of overall agent-readiness]

## Principle Scores

| Principle | Score | Evidence |
|-----------|-------|----------|
| 1. Sandbox Everything | X/3 | [brief evidence] |
| 2. No External DB Dependencies | X/3 | [brief evidence] |
| 3. Clean Environment | X/3 | [brief evidence] |
| 4. Session-Independent Execution | X/3 | [brief evidence] |
| 5. Outcome-Based Instructions | X/3 | [brief evidence] |
| 6. Direct Low-Level Interfaces | X/3 | [brief evidence] |
| 7. Minimal Framework Overhead | X/3 | [brief evidence] |
| 8. Explicit State Persistence | X/3 | [brief evidence] |
| 9. Early Benchmarks | X/3 | [brief evidence] |
| 10. Cost Planning | X/3 | [brief evidence] |
| 11. Verifiable Output | X/3 | [brief evidence] |
| 12. Infrastructure-Bounded Permissions | X/3 | [brief evidence] |

## Top 3 Improvements

1. **[Highest impact improvement]**
   - Current state: ...
   - Recommendation: ...
   - Impact: ...

2. **[Second improvement]**
   ...

3. **[Third improvement]**
   ...

## Strengths
- [What the codebase does well for agents]

## Detailed Findings
[Optional: deeper analysis of specific areas]
```

## Rating Scale

- **30-36 (83-100%)**: Excellent - Ready for autonomous agent execution
- **24-29 (67-82%)**: Good - Minor improvements needed
- **18-23 (50-66%)**: Needs Work - Significant gaps to address
- **0-17 (<50%)**: Not Agent-Ready - Major architectural changes needed

## Quick Checks

If time is limited, prioritize these high-signal indicators:

1. **Dockerfile exists?** → Sandboxing potential
2. **Lockfiles present?** → Reproducibility
3. **No external DB in default config?** → Isolation
4. **CLI scripts in bin/ or Makefile?** → Direct interfaces
5. **Tests with assertions?** → Verifiable output
