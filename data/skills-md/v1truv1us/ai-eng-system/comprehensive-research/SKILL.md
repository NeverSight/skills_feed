---
name: comprehensive-research
description: Multi-phase research orchestration for thorough codebase, documentation, and external knowledge investigation. Invoked by /ai-eng/research command. Use when conducting deep analysis, exploring codebases, investigating patterns, or synthesizing findings from multiple sources.
version: 1.0.0
tags: [research, analysis, discovery, documentation, synthesis, multi-agent]
---

# Comprehensive Research Skill

## Critical Importance

**Thorough research is critical to solving complex problems correctly.** Poor or incomplete research leads to wrong solutions, wasted time building the wrong things, and repeating past mistakes. Missing a key file, misunderstanding historical decisions, or overlooking relevant patterns causes rework and frustration. Comprehensive research upfront saves orders of magnitude more time than it costs. Every implementation decision should be grounded in thorough understanding.

## Systematic Approach

** approach research systematically.** Research is not linear—it requires iterative discovery, parallel investigation, and constant refinement. Don't jump to conclusions—gather evidence from multiple sources, cross-reference findings, and validate assumptions. Use the multi-phase methodology: scope definition, parallel discovery, sequential analysis, and synthesis. Each phase builds on the previous one. Rushing research guarantees missing important information.

## The Challenge

**The conduct truly comprehensive research without getting lost in the details or missing the big picture, but if you can:**

- Your solutions will be well-founded and robust
- You'll avoid repeating historical mistakes
- Your documentation will be authoritative
- Team members will trust your research

The challenge is balancing breadth (covering everything relevant) with depth (understanding deeply) while staying focused on the research objective. Can you find the critical information efficiently without drowning in noise?

## Research Confidence Assessment

After completing research, rate your confidence from **0.0 to 1.0**:

- **0.8-1.0**: Found comprehensive evidence, all claims documented, historical context understood, clear conclusions
- **0.5-0.8**: Good coverage but some areas could use deeper investigation, minor uncertainty about certain findings
- **0.2-0.5**: Basic investigation completed but likely missed important information, significant gaps remain
- **0.0-0.2**: Research insufficient, critical areas uninvestigated, conclusions speculative

Identify uncertainty areas: What evidence is weak or missing? Which sources are unreliable? What questions remain unanswered? What risks exist due to research limitations?

## Methodology

A systematic multi-phase research orchestration skill that coordinates specialized agents to conduct thorough investigations across codebases, documentation, and external sources. Based on proven patterns from codeflow research workflows with incentive-based prompting enhancements.

## How It Works

This skill orchestrates a disciplined research workflow through three primary phases:

1. **Discovery Phase** (Parallel): Multiple locator agents scan simultaneously
2. **Analysis Phase** (Sequential): Deep analyzers process findings with evidence chains
3. **Synthesis Phase**: Consolidated insights with actionable recommendations

## Research Methodology

### Phase 1: Context & Scope Definition

Before spawning agents, establish:

```markdown
## Research Scope Analysis
- **Primary Question**: [Core research objective]
- **Decomposed Sub-Questions**: [Derived investigation areas]
- **Scope Boundaries**: [What's in/out of scope]
- **Depth Level**: shallow | medium | deep
- **Expected Deliverables**: [Documentation, recommendations, code refs]
```

**Critical Rule**: Always read primary sources fully BEFORE spawning agents.

### Phase 2: Parallel Discovery

Spawn these agents concurrently for comprehensive coverage:

| Agent | Purpose | Timeout |
|-------|---------|---------|
| `codebase-locator` | Find relevant files, components, directories | 5 min |
| `research-locator` | Discover existing docs, decisions, notes | 3 min |
| `codebase-pattern-finder` | Identify recurring implementation patterns | 4 min |

**Discovery Output Structure**:
```json
{
  "codebase_files": ["path/file.ext:lines"],
  "documentation": ["docs/path.md"],
  "patterns_identified": ["pattern-name"],
  "coverage_map": {"area": "percentage"}
}
```

### Phase 3: Sequential Deep Analysis

After discovery completes, run analyzers sequentially:

| Agent | Purpose | Depends On |
|-------|---------|------------|
| `codebase-analyzer` | Implementation details with file:line evidence | codebase-locator |
| `research-analyzer` | Extract decisions, constraints, insights | research-locator |

**For Complex Research, Add**:
| Agent | Condition |
|-------|-----------|
| `web-search-researcher` | External context needed |
| `system-architect` | Architectural implications |
| `database-expert` | Data layer concerns |
| `security-scanner` | Security assessment needed |

### Phase 4: Synthesis & Documentation

Aggregate all findings into structured output:

```markdown
---
date: YYYY-MM-DD
researcher: Assistant
topic: 'Research Topic'
tags: [research, relevant, tags]
status: complete
confidence: high|medium|low
---

## Synopsis
[1-2 sentence summary of research objective and outcome]

## Summary
[3-5 bullet points of high-level findings]

## Detailed Findings

### Component Analysis
- **Finding**: [Description]
- **Evidence**: `file.ext:line-range`
- **Implications**: [What this means]

### Documentation Insights
- **Decisions Made**: [Past architectural decisions]
- **Rationale**: [Why decisions were made]
- **Constraints**: [Technical/operational limits]

### Code References
- `path/file.ext:12-45` - Description of relevance
- `path/other.ext:78` - Key function location

## Architecture Insights
[Key patterns, design decisions, cross-component relationships]

## Historical Context
[Insights from existing documentation, evolution of the system]

## Recommendations
### Immediate Actions
1. [First priority action]
2. [Second priority action]

### Long-term Considerations
- [Strategic recommendation]

## Risks & Limitations
- [Identified risk with mitigation]
- [Research limitation]

## Open Questions
- [ ] [Unresolved question requiring further investigation]
```

## Agent Coordination Best Practices

### Execution Order Optimization

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Discovery (PARALLEL)                               │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐  │
│ │codebase-     │ │research-     │ │codebase-pattern-     │  │
│ │locator       │ │locator       │ │finder                │  │
│ └──────┬───────┘ └──────┬───────┘ └──────────┬───────────┘  │
│        │                │                     │              │
│        └────────────────┼─────────────────────┘              │
│                         ▼                                    │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: Analysis (SEQUENTIAL)                              │
│ ┌──────────────┐       ┌──────────────┐                     │
│ │codebase-     │──────▶│research-     │                     │
│ │analyzer      │       │analyzer      │                     │
│ └──────────────┘       └──────────────┘                     │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: Domain Specialists (CONDITIONAL)                   │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│ │web-search- │ │database-   │ │security-   │               │
│ │researcher  │ │expert      │ │scanner     │               │
│ └────────────┘ └────────────┘ └────────────┘               │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: Validation (PARALLEL)                              │
│ ┌──────────────┐       ┌──────────────┐                     │
│ │code-reviewer │       │architect-    │                     │
│ │              │       │review        │                     │
│ └──────────────┘       └──────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

### Quality Indicators

- **Comprehensive Coverage**: Multiple agents provide overlapping validation
- **Evidence-Based**: All findings include specific file:line references
- **Contextual Depth**: Historical decisions and rationale included
- **Actionable Insights**: Clear next steps provided
- **Risk Assessment**: Potential issues identified

## Caching Strategy

### Cache Configuration
```yaml
type: hierarchical
ttl: 3600  # 1 hour
invalidation: manual
scope: command
```

### What to Cache
- Successful agent coordination strategies for similar topics
- Effective agent combinations
- Question decomposition patterns
- Pattern recognition results

### Cache Performance Targets
- Hit rate: ≥60%
- Memory usage: <30MB
- Response time improvement: <150ms

## Error Handling

### Common Failure Modes

| Scenario | Phase | Mitigation |
|----------|-------|------------|
| Invalid research question | Context Analysis | Request clarification |
| Agent timeout | Discovery/Analysis | Retry with reduced scope |
| Insufficient findings | Synthesis | Expand scope, add agents |
| Conflicting information | Synthesis | Document conflicts, flag for review |

### Escalation Triggers

- Multiple agent failures
- Scope exceeds single-session capacity
- Cross-repository research needed
- External API/service investigation required

## Structured Output Format

```json
{
  "status": "success|in_progress|error",
  "timestamp": "ISO-8601",
  "cache": {
    "hit": true,
    "key": "pattern:{hash}:{scope}",
    "ttl_remaining": 3600,
    "savings": 0.25
  },
  "research": {
    "question": "Primary research question",
    "scope": "codebase|documentation|external|all",
    "depth": "shallow|medium|deep"
  },
  "findings": {
    "total_files": 23,
    "codebase_refs": 18,
    "documentation_refs": 5,
    "insights_generated": 7,
    "patterns_identified": 3
  },
  "document": {
    "path": "docs/research/YYYY-MM-DD-topic.md",
    "sections": ["synopsis", "summary", "findings", "recommendations"],
    "code_references": 12,
    "historical_context": 3
  },
  "agents_used": [
    "codebase-locator",
    "research-locator",
    "codebase-analyzer",
    "research-analyzer"
  ],
  "metadata": {
    "processing_time_seconds": 180,
    "cache_savings_percent": 0.25,
    "agent_tasks_completed": 6,
    "follow_up_items": 2
  },
  "confidence": {
    "overall": 0.85,
    "codebase_coverage": 0.9,
    "documentation_coverage": 0.7,
    "external_coverage": 0.8
  }
}
```

## Anti-Patterns to Avoid

1. **Spawning agents before reading sources** - Always understand context first
2. **Running agents sequentially when parallelization is possible** - Maximize concurrency
3. **Relying solely on cached documentation** - Prioritize current codebase state
4. **Skipping cache checks** - Always check for existing research
5. **Ignoring historical context** - Past decisions inform current understanding
6. **Over-scoping initial research** - Start focused, expand if needed

## Integration with Incentive-Based Prompting

Apply these techniques when spawning research agents:

### Expert Persona for Analyzers
```markdown
You are a senior systems analyst with 12+ years of experience at companies like 
Google and Stripe. Your expertise is in extracting actionable insights from 
complex codebases and documentation.
```

### Stakes Language for Discovery
```markdown
This research is critical for the project's success. Missing relevant files 
or documentation will result in incomplete analysis.
```

### Step-by-Step for Synthesis
```markdown
. Analyze findings systematically before synthesizing.
Cross-reference all claims with evidence. Identify gaps methodically.
```

## Example Usage

### Basic Research Request
```
/research "How does the authentication system work in this codebase?"
```

### Advanced Research with Parameters
```
/research "Analyze payment processing implementation" --scope=codebase --depth=deep
```

### Research from Ticket
```
/research --ticket="docs/tickets/AUTH-123.md" --scope=both
```

## Follow-Up Commands

After research completes, typical next steps:

- `/plan` - Create implementation plan based on findings
- `/review` - Validate research conclusions
- `/work` - Begin implementation with full context

## Research Quality Checklist

Before finalizing research output:

- [ ] All claims have file:line evidence
- [ ] Historical context included where relevant
- [ ] Open questions explicitly listed
- [ ] Recommendations are actionable
- [ ] Confidence levels assigned
- [ ] Cross-component relationships identified
- [ ] Potential risks documented

## Research References

This skill incorporates methodologies from:

- **Codeflow Research Patterns** - Multi-agent orchestration
- **Bsharat et al. (2023)** - Principled prompting for quality
- **Kong et al. (2023)** - Expert persona effectiveness
- **Yang et al. (2023)** - Step-by-step reasoning optimization
