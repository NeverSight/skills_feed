---
name: spike
description: Time-boxed technical investigation with structured output. Use for feasibility studies, architecture exploration, integration assessment, performance analysis, or risk evaluation. Creates spike tasks in ohno, enforces time-boxing, generates spike reports, and creates actionable follow-up tasks. Triggers on "spike on X", "investigate whether we can", "how hard would it be to", "what's the best approach for", or any exploratory technical question needing bounded research.
---

# Spike

Structured technical investigation to reduce uncertainty. Answer specific questions, not "explore X."

**Integrates with:**
- `ohno` — Creates spike task, tracks time-box, logs findings
- `project-harness` — Works within session workflow
- All domain skills — May invoke for specialized investigation

## Core Philosophy

```
┌─────────────────────────────────────────────────────────────────┐
│                   SPIKE = BOUNDED UNCERTAINTY                    │
├─────────────────────────────────────────────────────────────────┤
│  INPUT: Vague concern or unknown → "Can we use GraphQL?"        │
│  OUTPUT: Decision + evidence    → "Yes, with caveats. Here's    │
│                                    the proof-of-concept."       │
├─────────────────────────────────────────────────────────────────┤
│  TIME-BOXED: 2-4 hours default, never >1 day                    │
│  QUESTION-FOCUSED: Answer ONE specific question                 │
│  OUTPUT-DRIVEN: End with decision, not more questions           │
│  DOCUMENTED: Learnings captured even if answer is "no"          │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Frame the Question

Transform vague concerns into spike-able questions:

| Vague | Spike Question |
|-------|----------------|
| "Look into caching" | "Can Redis reduce our API latency to <100ms for user lookups?" |
| "Explore auth options" | "Can we use OAuth2 with Google for our auth flow?" |
| "Check if X is possible" | "Can library X handle 10k concurrent connections?" |

**Good spike questions have:**
- A yes/no or A/B answer
- Measurable success criteria
- Clear scope boundaries

### 2. Define Time Box & Success Criteria

```markdown
## Spike Definition

**Question**: Can we use Cloudflare D1 for our multi-tenant data model?

**Time Box**: 3 hours
**Type**: Feasibility

**Success Criteria**:
- [ ] Row-level security works for tenant isolation
- [ ] Query performance acceptable (<50ms for typical queries)
- [ ] Migration path from current PostgreSQL clear

**Out of Scope**:
- Full migration implementation
- Performance tuning
- Production deployment
```

### 3. Create Spike Task in ohno

```bash
# Create spike task
ohno add "Spike: D1 multi-tenant feasibility" --type spike --estimate 3h

# Or via MCP
create_task({
  title: "Spike: D1 multi-tenant feasibility",
  type: "spike",
  estimate: "3h",
  tags: ["spike", "feasibility", "database"]
})
```

### 4. Investigate (with checkpoints)

```
START → 25% checkpoint → 50% checkpoint → 75% checkpoint → CONCLUDE
 │           │                │                │              │
 │           │                │                │              └─ Write report
 │           │                │                └─ Evaluate findings
 │           │                └─ Check: On track? Pivot needed?
 │           └─ Initial findings assessment
 └─ Begin investigation
```

**50% Checkpoint (critical):**
```markdown
## Spike Checkpoint: 1.5h of 3h elapsed

**Progress**: 
- [x] Set up D1 database
- [x] Created test tenant structure
- [ ] Performance benchmarks
- [ ] Migration path analysis

**On Track?**: Yes / No / Pivoting
**Blockers**: None
**Adjustment**: [if any]
```

### 5. Conclude with Decision

Every spike ends with ONE of:
- **GO**: Proceed with approach, create implementation tasks
- **NO-GO**: Don't proceed, document why
- **PIVOT**: Different approach needed, create new spike
- **MORE-INFO**: Specific additional info needed (rare, max 1 re-spike)

---

## Spike Types

| Type | Purpose | Typical Duration | Output |
|------|---------|------------------|--------|
| **Feasibility** | Can we do X? | 2-4h | Yes/no + proof |
| **Architecture** | How should we structure X? | 3-6h | Design decision |
| **Integration** | How connect to service X? | 2-4h | Working connection |
| **Performance** | Can X meet requirements? | 2-4h | Benchmarks |
| **Risk** | What could go wrong? | 2-4h | Risk register |

See [references/spike-types.md](references/spike-types.md) for detailed type-specific guidance.

---

## Spike Report Format

Generate report in `.claude/spikes/` folder:

```markdown
# Spike Report: [Title]

**Date**: 2026-01-18
**Duration**: 2.5h (of 3h budget)
**Type**: Feasibility
**Decision**: GO ✓ | NO-GO ✗ | PIVOT ↺ | MORE-INFO ?

## Question
Can we use Cloudflare D1 for multi-tenant data model with row-level security?

## Answer
**YES** — D1 supports row-level filtering, performance is acceptable for our scale.

## Evidence

### What Worked
- Created test database with 3 tenants, 10k rows each
- Queries with tenant_id filter: 15-30ms average
- No cross-tenant data leakage in security tests

### What Didn't Work
- Bulk inserts >1000 rows timeout (need batching)
- No native RLS — must enforce in application layer

### Proof of Concept
Location: `/spikes/d1-multi-tenant/`
\```typescript
// Key pattern: tenant isolation
const getData = async (tenantId: string) => {
  return db.prepare(
    "SELECT * FROM data WHERE tenant_id = ?"
  ).bind(tenantId).all();
};
\```

## Recommendation
Proceed with D1. Application-layer tenant isolation is acceptable given our controlled access patterns.

## Follow-up Tasks
1. [ ] Design tenant isolation middleware
2. [ ] Create migration script from PostgreSQL
3. [ ] Set up batch insert utility for bulk operations

## Time Log
- 0:30 - Environment setup, D1 database creation
- 1:00 - Schema design, test data generation
- 1:30 - Query performance testing
- 2:00 - Security boundary testing
- 2:30 - Documentation and report
```

---

## ohno Integration

### Creating Spike Tasks

Spikes are tasks with `type: spike`:

```bash
# CLI
ohno add "Spike: [question]" --type spike --estimate 3h --tags spike,feasibility

# After completion
ohno done <spike-id> --notes "GO - see .claude/spikes/spike-name.md"
```

### Creating Follow-up Tasks

After spike concludes, create implementation tasks:

```bash
# From spike findings
ohno add "Design tenant isolation middleware" --parent <epic-id> --tags d1,security
ohno add "Create PostgreSQL to D1 migration script" --parent <epic-id>
ohno add "Implement batch insert utility" --parent <epic-id>
```

### Spike Task States

```
planned → in_progress → done (with decision)
                     └→ blocked (if external dependency)
```

---

## Anti-Patterns

### During Definition

| Anti-Pattern | Example | Fix |
|--------------|---------|-----|
| Vague question | "Investigate caching" | "Can Redis reduce latency to <100ms?" |
| No success criteria | "See if it works" | Define measurable outcomes |
| Unbounded scope | "Explore all options" | Pick ONE option to test |
| Too long | "1 week spike" | Max 1 day, usually 2-4h |

### During Investigation

| Anti-Pattern | Example | Fix |
|--------------|---------|-----|
| Scope creep | "While I'm here, let me also..." | Stay on question |
| Rabbit holes | Deep-diving tangent | 50% checkpoint catches this |
| Building too much | Full implementation | Proof-of-concept only |
| No checkpoints | Realize late you're stuck | Check at 25%, 50%, 75% |

### At Conclusion

| Anti-Pattern | Example | Fix |
|--------------|---------|-----|
| No decision | "It depends" | Force GO/NO-GO/PIVOT |
| No documentation | Knowledge lost | Write spike report |
| Vague follow-ups | "Continue investigating" | Specific actionable tasks |
| Re-spike loop | Endless "more info needed" | Max 1 re-spike, then decide |

---

## Workflow Protocol

### Starting a Spike

```markdown
## Spike Start Checklist

1. [ ] Question clearly framed (yes/no or A/B answer)
2. [ ] Success criteria defined (measurable)
3. [ ] Time box set (default 2-4h, max 1 day)
4. [ ] Spike type identified
5. [ ] Spike task created in ohno
6. [ ] Out-of-scope boundaries documented
```

### During Investigation

```markdown
## Investigation Log

### Checkpoint 1 (25%)
- [Initial findings]
- [Blockers/surprises]

### Checkpoint 2 (50%) — DECISION POINT
- [Progress assessment]
- [On track? Pivot needed?]
- [Adjusted approach if any]

### Checkpoint 3 (75%)
- [Near-final findings]
- [Start forming decision]
```

### Concluding a Spike

```markdown
## Spike End Checklist

1. [ ] Decision made: GO / NO-GO / PIVOT / MORE-INFO
2. [ ] Evidence documented
3. [ ] Spike report written to `.claude/spikes/`
4. [ ] Proof-of-concept code saved (if applicable)
5. [ ] Follow-up tasks created in ohno
6. [ ] Spike task marked done with decision notes
7. [ ] Knowledge shared (not just filed away)
```

---

## Decision Framework

### When to GO

- Success criteria met
- Risks acceptable and mitigatable
- Clear implementation path
- Performance/feasibility confirmed

### When to NO-GO

- Fundamental blockers discovered
- Performance requirements unachievable
- Complexity too high for value
- Better alternatives identified

### When to PIVOT

- Original approach won't work
- New approach emerged during investigation
- Scope needs significant adjustment

### When to MORE-INFO (use sparingly)

- Specific, bounded additional info needed
- Can be obtained in ≤2h additional work
- NOT "let's investigate more"

---

## Question Framing Guide

Transform vague concerns into spike-able questions:

| Concern Type | Vague Version | Spike Question |
|--------------|---------------|----------------|
| Feasibility | "Can we use X?" | "Can X handle [specific requirement] within [constraint]?" |
| Performance | "Is it fast enough?" | "Can X achieve <[target]ms for [operation]?" |
| Integration | "Will it work with Y?" | "Can X connect to Y using [method] with [auth]?" |
| Architecture | "How should we build it?" | "Should we use A or B for [specific aspect]?" |
| Risk | "What could go wrong?" | "What are the top 3 failure modes of X?" |

See [references/question-patterns.md](references/question-patterns.md) for comprehensive examples.

---

## Output Location

All spike outputs go to `.claude/spikes/`:

```
.claude/
├── spikes/
│   ├── d1-multi-tenant-2026-01-18.md    ← Spike report
│   └── d1-multi-tenant/                  ← Proof-of-concept code
├── PROJECT.md
└── tasks.db
```

---

## References

- [references/spike-types.md](references/spike-types.md) — Detailed guidance per spike type
- [references/question-patterns.md](references/question-patterns.md) — Question framing techniques
- [references/output-templates.md](references/output-templates.md) — Report templates
