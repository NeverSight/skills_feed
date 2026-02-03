---
name: deep-research
description: Extended investigation for technology evaluation, competitive analysis, architectural exploration, and best practices research. Unlike spike (time-boxed hours), deep-research supports multi-day comprehensive investigation producing reports for major decisions. Triggers on "research X solutions", "compare frameworks for our use case", "evaluate vendors for X", "what are best practices for Y", "how do competitors handle Z", or any investigation requiring comprehensive analysis across multiple sources.
---

# Deep Research

Comprehensive investigation that informs major decisions. Produces structured reports for stakeholders.

**Integrates with:**
- `ohno` — Creates research task, tracks progress, logs findings
- `project-harness` — Works within session workflow
- `spike` — May spawn focused spikes for specific technical questions
- Domain skills — May invoke for specialized analysis

## When to Use Deep Research vs Spike

```
┌────────────────────────────────────────────────────────────────────────────┐
│  SPIKE (hours)                │  DEEP RESEARCH (days)                      │
├────────────────────────────────────────────────────────────────────────────┤
│  "Can we use X?"              │  "Which of X, Y, Z should we use?"         │
│  Single question              │  Multiple related questions                │
│  2-4h time box               │  1-5 days investigation                    │
│  Team/self audience           │  Stakeholder audience                      │
│  Decision + brief report      │  Comprehensive report + recommendations   │
│  PoC optional                │  Usually no code                          │
└────────────────────────────────────────────────────────────────────────────┘
```

**Use deep-research when:**
- Decision impacts architecture, budget, or team direction
- Multiple viable options need systematic comparison
- Stakeholders need comprehensive rationale
- Industry context or competitive landscape matters

**Use spike instead when:**
- Single yes/no question
- Technical feasibility is the only concern
- Time-boxed answer is sufficient

---

## Research Types

| Type | Purpose | Duration | Key Output |
|------|---------|----------|------------|
| **Technology Evaluation** | Compare frameworks, libraries, services | 2-3 days | Comparison matrix + recommendation |
| **Competitive Analysis** | How others solve this problem | 1-2 days | Pattern synthesis + insights |
| **Architecture Exploration** | Design patterns for complex requirements | 2-4 days | Options analysis + trade-offs |
| **Best Practices** | Industry standards for X | 1-2 days | Consolidated guidelines |
| **Vendor Evaluation** | SaaS/tool selection | 2-3 days | Evaluation matrix + recommendation |

See [references/research-types.md](references/research-types.md) for detailed type-specific guidance.

---

## Research Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. SCOPE    Define questions, criteria, constraints                     │
│       ↓                                                                  │
│ 2. GATHER   Identify sources, collect documentation, find examples      │
│       ↓                                                                  │
│ 3. ANALYZE  Compare options against criteria, identify trade-offs       │
│       ↓                                                                  │
│ 4. SYNTHESIZE  Form recommendations, document rationale                 │
│       ↓                                                                  │
│ 5. PRESENT  Structured report for stakeholders                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Phase 1: Scope

Frame the investigation with clear boundaries:

```markdown
## Research Definition

**Topic**: Authentication solutions for multi-tenant SaaS

**Primary Questions**:
1. Which auth providers support enterprise SSO + social login?
2. What are the cost implications at 10k, 100k, 1M users?
3. How complex is integration with our existing stack?

**Evaluation Criteria** (weighted):
- Enterprise features: 30%
- Developer experience: 25%
- Cost scalability: 25%
- Community/support: 20%

**Constraints**:
- Must support SAML and OIDC
- Self-hosted option preferred
- Budget: <$10k/month at scale

**Out of Scope**:
- Custom auth implementation
- Compliance certification research
```

**Scoping Questions:**
- What decision will this research inform?
- Who are the stakeholders?
- What criteria matter most?
- What constraints are non-negotiable?
- What's explicitly out of scope?

### Phase 2: Gather

Build a comprehensive source base:

**Source Priority (high to low):**
1. Official documentation, API references
2. Engineering blogs from adopters at scale
3. GitHub repos, sample implementations
4. Conference talks, case studies
5. Community discussions, Stack Overflow
6. Marketing materials (verify claims)

See [references/source-quality.md](references/source-quality.md) for evaluation criteria.

**Gathering Patterns:**
- Start with official docs for feature matrix
- Search for "[tool] at scale" case studies
- Check GitHub issues for pain points
- Look for migration stories (to AND from)
- Find pricing calculators, estimate at your scale

### Phase 3: Analyze

Compare systematically against criteria:

```markdown
## Comparison Matrix: Auth Providers

| Criteria | Auth0 | Clerk | Supabase Auth | WorkOS |
|----------|-------|-------|---------------|--------|
| Enterprise SSO | ✓ All major | ✓ All major | Limited | ✓ All major |
| Social Login | ✓ Extensive | ✓ Good | ✓ Good | ✓ Good |
| Self-hosted | ✗ No | ✗ No | ✓ Yes | ✗ No |
| Pricing (100k MAU) | $2,400/mo | $1,200/mo | $0 (self) | $4,500/mo |
| Next.js Integration | Good | Excellent | Good | Good |
| **Score** | 78/100 | 85/100 | 72/100 | 80/100 |
```

**Analysis Patterns:**
- Create comparison matrix for each criterion
- Document evidence for each claim
- Note gaps in information
- Identify hidden costs, complexity
- Consider migration/lock-in implications

### Phase 4: Synthesize

Form actionable recommendations:

```markdown
## Synthesis

### Key Findings
1. All evaluated providers meet baseline requirements
2. Clerk offers best DX for our stack (Next.js + React)
3. Supabase Auth is cost-effective but enterprise features lag
4. Auth0 has most mature enterprise features but highest cost

### Trade-off Analysis
- **Clerk**: Best DX, good features, moderate cost
  - Risk: Smaller company, less enterprise track record
- **Auth0**: Enterprise-proven, comprehensive features
  - Risk: Cost scales aggressively, migration complexity

### Recommendation
**Primary**: Clerk for new development
**Rationale**: Best DX alignment, adequate enterprise features, competitive cost
**Contingency**: Auth0 if enterprise requirements expand significantly
```

### Phase 5: Present

Deliver structured report:

```markdown
# Research Report: Authentication Solutions

## Executive Summary
[1-2 paragraphs: context, key findings, recommendation]

## Background
[Why this research was needed, decision context]

## Methodology
[How research was conducted, sources used]

## Options Evaluated
[Brief description of each option]

## Comparison
[Matrix and detailed analysis]

## Recommendation
[Primary recommendation with rationale]

## Trade-offs & Risks
[What we're accepting with this choice]

## Follow-up Actions
[Spikes, implementation tasks, or additional research]

## Appendix
[Detailed data, sources, pricing breakdowns]
```

See [assets/templates/research-report.md](assets/templates/research-report.md) for full template.

---

## ohno Integration

### Creating Research Tasks

```bash
# Create research task
ohno add "Research: Auth solutions for multi-tenant SaaS" \
  --type research \
  --estimate 2d \
  --tags research,auth,architecture

# Track progress with subtasks
ohno add "Gather Auth0 documentation" --parent <research-id>
ohno add "Gather Clerk documentation" --parent <research-id>
ohno add "Create comparison matrix" --parent <research-id>
ohno add "Write research report" --parent <research-id>
```

### Progress Checkpoints

```
Day 1: Scope defined, sources identified
Day 2: Gathering complete, analysis started
Day 3: Synthesis forming, draft report
Day 4: Report complete, review
Day 5: Finalize and present
```

### Creating Follow-up Tasks

Research often spawns additional work:

```bash
# Spike for technical validation
ohno add "Spike: Clerk integration with our Next.js setup" --type spike

# Implementation tasks
ohno add "Implement Clerk auth integration" --type task
ohno add "Create SSO onboarding flow" --type task
```

---

## Output Structure

```
.claude/
├── research/
│   ├── auth-solutions-2026-01-18/
│   │   ├── report.md              ← Main research report
│   │   ├── comparison-matrix.md   ← Detailed comparisons
│   │   ├── sources.md             ← Source log with notes
│   │   └── raw-notes/             ← Gathering artifacts
├── PROJECT.md
└── tasks.db
```

---

## Anti-Patterns

### During Scoping

| Anti-Pattern | Example | Fix |
|--------------|---------|-----|
| No clear question | "Research auth" | Define decision to be informed |
| Unbounded scope | "Evaluate all options" | Set explicit constraints |
| Missing criteria | "Find the best one" | Define weighted evaluation criteria |
| No stakeholders | Research for its own sake | Identify who needs this |

### During Gathering

| Anti-Pattern | Example | Fix |
|--------------|---------|-----|
| Marketing as evidence | "Vendor says it's fast" | Find independent benchmarks |
| Single source | Only official docs | Diversify source types |
| Confirmation bias | Only positive reviews | Actively seek criticisms |
| Dated information | 3-year-old blog posts | Verify currency of sources |

### During Synthesis

| Anti-Pattern | Example | Fix |
|--------------|---------|-----|
| Analysis paralysis | "Need more data" | Decide with available info |
| No recommendation | "It depends" | Make a call, document trade-offs |
| Hidden agenda | Cherry-picked evidence | Present all options fairly |
| Vague conclusion | "Consider X" | Specific, actionable recommendation |

---

## Quality Checklist

### Research Definition
- [ ] Primary questions clearly stated
- [ ] Evaluation criteria weighted
- [ ] Constraints documented
- [ ] Out of scope defined
- [ ] Timeline realistic for scope

### Gathering
- [ ] Multiple source types used
- [ ] Official docs reviewed
- [ ] Real-world case studies found
- [ ] Pain points researched
- [ ] Sources documented with dates

### Analysis
- [ ] All options evaluated fairly
- [ ] Comparison matrix complete
- [ ] Evidence cited for claims
- [ ] Gaps in knowledge noted
- [ ] Trade-offs explicit

### Synthesis
- [ ] Clear recommendation made
- [ ] Rationale documented
- [ ] Risks acknowledged
- [ ] Alternatives noted
- [ ] Follow-up actions defined

### Presentation
- [ ] Executive summary present
- [ ] Appropriate depth for audience
- [ ] Sources cited
- [ ] Appendix with details
- [ ] Report filed in `.claude/research/`

---

## References

- [references/research-types.md](references/research-types.md) — Detailed guidance per research type
- [references/source-quality.md](references/source-quality.md) — Evaluating source quality
- [references/synthesis-patterns.md](references/synthesis-patterns.md) — Forming recommendations
- [assets/templates/research-report.md](assets/templates/research-report.md) — Full report template
- [assets/templates/comparison-matrix.md](assets/templates/comparison-matrix.md) — Matrix template
