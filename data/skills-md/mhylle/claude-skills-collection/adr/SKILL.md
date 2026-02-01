---
name: adr
description: Document architectural decisions in standardized ADR format. This skill should be used when making significant technical decisions, choosing between approaches, establishing patterns, or when other skills (create-plan, implement-plan, brainstorm) identify decisions that need documentation. Triggers on "document decision", "create ADR", "architectural decision", or automatically when invoked by other skills during planning and implementation.
argument-hint: "[decision-title?]"
---

# Architectural Decision Records (ADR)

Document significant architectural and technical decisions in a standardized, searchable format optimized for LLM context efficiency.

## Design Principles

### Context Conservation

ADRs are designed for efficient LLM consumption:

1. **Small, focused files** - One decision per ADR, minimal content
2. **Quick Reference block** - First 5 lines summarize the entire ADR
3. **Central INDEX.md** - Single file listing all ADRs with one-line summaries

### LLM Reading Strategy

When consulting ADRs, follow this tiered approach:

```
TIER 1: Read INDEX.md (one file, all summaries)
        ↓ Identify potentially relevant ADRs
TIER 2: Read Quick Reference block only (first 10 lines of candidate ADRs)
        ↓ Confirm relevance
TIER 3: Read full ADR content (only when details are needed)
```

**Implementation**:
```
# Tier 1: Scan index
Read("docs/decisions/INDEX.md")

# Tier 2: Quick reference only (use limit parameter)
Read("docs/decisions/ADR-0001-title.md", limit=10)

# Tier 3: Full content (only if needed)
Read("docs/decisions/ADR-0001-title.md")
```

## When to Use This Skill

**Directly invoked when:**
- Making a significant technical decision
- Choosing between architectural approaches
- Establishing patterns or conventions
- Documenting why a particular technology was selected

**Automatically invoked by other skills when:**
- **create-plan**: Design decision is made in Phase 4
- **implement-plan**: Mismatch discovered or architectural choice made during implementation
- **brainstorm**: Key decisions identified during analysis

## ADR Location and Naming

**Directory**: `docs/decisions/`

**Naming Convention**: `ADR-NNNN-short-title.md`
- `NNNN`: Zero-padded sequential number (0001, 0002, etc.)
- `short-title`: Lowercase, hyphenated description (max 50 chars)

**Examples**:
- `ADR-0001-use-jwt-for-authentication.md`
- `ADR-0002-postgresql-over-mongodb.md`
- `ADR-0003-event-sourcing-for-audit.md`

## Getting the Next ADR Number

Before creating an ADR, determine the next sequence number:

```bash
# Find highest existing ADR number
ls docs/decisions/ADR-*.md 2>/dev/null | sort -t- -k2 -n | tail -1 | grep -oP 'ADR-\K\d+' || echo "0000"
```

If no ADRs exist, start with `0001`.

## ADR Status Values

| Status | Meaning |
|--------|---------|
| **Proposed** | Under consideration, not yet decided |
| **Accepted** | Decision made, ready for implementation |
| **Deprecated** | Was accepted, now superseded |
| **Superseded** | Replaced by another ADR (link to replacement) |

## Creating an ADR

### Required Information

Gather these inputs (ask user if not provided):

| Field | Description | Required |
|-------|-------------|----------|
| Title | Short, descriptive title | Yes |
| Context | Why is this decision needed? | Yes |
| Options | What alternatives were considered? | Yes |
| Decision | What was decided? | Yes |
| Rationale | Why this option? | Yes |
| Consequences | What are the implications? | Yes |
| Related ADRs | Links to related decisions | If applicable |

### ADR Template

Use this format (also in `references/adr-template.md`):

```markdown
# ADR-NNNN: [Title]

> **Quick Reference** | Status: [Accepted] | Date: [YYYY-MM-DD]
> **Decision**: [One sentence: what was decided]
> **Context**: [One sentence: why this decision was needed]
> **Alternatives**: [Rejected options, comma-separated]
> **Impact**: [Key areas affected, comma-separated]

---

## Context

[2-3 sentences max. The problem or opportunity being addressed.]

## Decision

**We will use [chosen option].**

[1-2 sentences explaining the decision.]

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| [Option A] | [Key pro] | [Key con] | [Brief reason] |
| [Option B] | [Key pro] | [Key con] | [Brief reason] |

## Consequences

- **Positive**: [Key benefit]
- **Negative**: [Key trade-off]
- **Requires**: [What must be done as a result]

## Related

- [ADR-XXXX](./ADR-XXXX-title.md): [Relationship]
```

### Quick Reference Block (Mandatory)

The first 5 lines after the title form the **Quick Reference** block. This enables LLMs to assess relevance without reading the full document.

**Format** (must fit in ~5 lines):
```markdown
> **Quick Reference** | Status: [Status] | Date: [Date]
> **Decision**: [One sentence summary of what was decided]
> **Context**: [One sentence on why this decision was needed]
> **Alternatives**: [Comma-separated list of rejected options]
> **Impact**: [Comma-separated list of affected areas/components]
```

**Example**:
```markdown
> **Quick Reference** | Status: Accepted | Date: 2024-01-15
> **Decision**: Use JWT tokens for API authentication instead of sessions.
> **Context**: Need stateless auth for horizontal scaling of API servers.
> **Alternatives**: Session cookies, OAuth tokens, API keys
> **Impact**: Auth service, API gateway, client SDKs
```

### Keeping ADRs Small

**Target size**: 30-50 lines maximum (excluding Quick Reference)

**One decision per ADR**. If you find yourself documenting multiple decisions, split into separate ADRs:

| Instead of | Create |
|------------|--------|
| "Database and caching choices" | ADR-0001: PostgreSQL for primary database |
| | ADR-0002: Redis for session caching |
| "Authentication architecture" | ADR-0003: JWT for API auth |
| | ADR-0004: OAuth2 for third-party integration |

**Use tables over prose** - More scannable, less verbose:

```markdown
## Alternatives Considered

| Option | Pros | Cons | Why Not |
|--------|------|------|---------|
| MongoDB | Flexible schema | No ACID | Need transactions |
| MySQL | Mature, fast | Less JSON support | PostgreSQL better fit |
```

## Workflow

### Step 1: Detect ADR Trigger

An ADR should be created when:

1. **Explicit request**: User asks to document a decision
2. **Design choice**: During planning, a significant choice between approaches is made
3. **Pattern establishment**: A new convention or pattern is being introduced
4. **Technology selection**: A library, framework, or service is chosen
5. **Architecture change**: Structural changes to the system
6. **Deviation from plan**: Implementation differs from original plan for good reason

### Step 2: Gather Information

If invoked automatically by another skill, extract:
- Context from the current discussion
- Options that were considered
- The decision that was made
- Rationale from the analysis

If information is incomplete, ask the user:

```
To document this architectural decision, I need:
1. What problem or context led to this decision?
2. What options were considered?
3. Why was this option chosen over others?
4. What are the expected consequences?
```

### Step 3: Create ADR File

1. Determine next ADR number
2. Generate filename from title
3. Write ADR using template
4. Report creation to calling context

### Step 4: Update INDEX.md (Required)

**Always update `docs/decisions/INDEX.md`** when creating, modifying, or deprecating an ADR.

#### INDEX.md Structure

```markdown
# Architectural Decision Records

Quick reference index for all architectural decisions. Read this file first to identify relevant ADRs.

## Active Decisions

| ADR | Decision | Impact | Date |
|-----|----------|--------|------|
| [0001](./ADR-0001-use-jwt-auth.md) | Use JWT for API authentication | Auth, API | 2024-01-15 |
| [0002](./ADR-0002-postgresql-database.md) | PostgreSQL as primary database | Data layer | 2024-01-16 |
| [0003](./ADR-0003-redis-caching.md) | Redis for session and query caching | Performance | 2024-01-17 |

## Superseded Decisions

| ADR | Was | Replaced By | Date |
|-----|-----|-------------|------|
| [0000](./ADR-0000-example.md) | Session-based auth | ADR-0001 | 2024-01-10 |

## By Category

### Authentication & Security
- [ADR-0001](./ADR-0001-use-jwt-auth.md): JWT for API authentication

### Data & Storage
- [ADR-0002](./ADR-0002-postgresql-database.md): PostgreSQL as primary database
- [ADR-0003](./ADR-0003-redis-caching.md): Redis for caching

### API Design
(none yet)

### Infrastructure
(none yet)
```

#### Updating INDEX.md

When adding a new ADR:
1. Add row to "Active Decisions" table
2. Add entry under appropriate category (create category if needed)

When deprecating an ADR:
1. Move row from "Active Decisions" to "Superseded Decisions"
2. Add "Replaced By" reference
3. Update category listing

#### Creating INDEX.md

If `docs/decisions/INDEX.md` doesn't exist, create it:

```bash
mkdir -p docs/decisions
```

Then write the initial structure with the first ADR entry.

## Integration with Other Skills

### From create-plan

When create-plan makes a design decision in Phase 4, it should invoke this skill:

```
TRIGGER: Design option selected in create-plan Phase 4
ACTION: Create ADR documenting the decision
LINK: Reference ADR in plan's "Design Decision" section
```

The plan should include:
```markdown
## Design Decision

[Brief description]

See [ADR-NNNN](../decisions/ADR-NNNN-title.md) for full rationale.
```

### From implement-plan

When implement-plan encounters an architectural choice:

```
TRIGGER:
- Mismatch between plan and reality requiring decision
- New pattern being established
- Technology choice during implementation

ACTION: Create ADR documenting the decision
LINK: Note in plan file and inline status
```

### From brainstorm

When brainstorm identifies key decisions:

```
TRIGGER: Analysis identifies significant decisions that should be documented
ACTION: Create ADRs for each major decision (can be "Proposed" status)
LINK: Reference in brainstorm output's "Key Decisions" section
```

## Response Format (for subagent use)

When this skill is invoked by another skill (as a subagent), return concise output:

```
STATUS: CREATED
ADR: docs/decisions/ADR-NNNN-title.md
INDEX: docs/decisions/INDEX.md (updated)
DECISION: [One-line summary of decision]
IMPACT: [Comma-separated affected areas]
```

**Always confirm INDEX.md was updated** - this is critical for LLM discoverability.

## Listing Existing ADRs

To review existing decisions:

```bash
# List all ADRs with status
grep -l "Status.*Accepted" docs/decisions/ADR-*.md | while read f; do
  title=$(head -1 "$f" | sed 's/# //')
  echo "$f: $title"
done
```

## Searching ADRs

Find ADRs related to a topic:

```bash
# Search ADR content
grep -l "authentication" docs/decisions/ADR-*.md
```

## Deprecating an ADR

When a decision is superseded:

1. Update old ADR status: `**Status**: Superseded by [ADR-NNNN](./ADR-NNNN-title.md)`
2. Create new ADR referencing the old one in "Related Decisions"
3. Update any plans or docs referencing the old ADR

## Quality Checklist

Before finalizing an ADR:

**Structure (Context Conservation)**:
- [ ] Quick Reference block is complete (all 5 lines)
- [ ] Quick Reference fits in first 10 lines of file
- [ ] Total ADR is under 50 lines
- [ ] One decision per ADR (no bundled decisions)
- [ ] Uses tables instead of verbose prose

**Content**:
- [ ] Decision is clearly stated in one sentence
- [ ] Context is 2-3 sentences max
- [ ] At least 2 alternatives listed with pros/cons
- [ ] Consequences include positive AND negative

**Index**:
- [ ] INDEX.md updated with new entry
- [ ] Category section updated
- [ ] Impact areas listed accurately

## Best Practices

### Writing Concise ADRs

1. **One sentence, one decision**: If you can't state the decision in one sentence, you may be bundling multiple decisions
2. **Tables over paragraphs**: Alternatives table is more scannable than prose
3. **Impact over rationale**: Focus on what's affected, not lengthy justification
4. **Quick Reference is the ADR**: If someone only reads the Quick Reference, they should understand the decision

### Size Guidelines

| Section | Target Length |
|---------|---------------|
| Quick Reference | 5 lines (mandatory) |
| Context | 2-3 sentences |
| Decision | 1-2 sentences |
| Alternatives table | 2-4 rows |
| Consequences | 3 bullets |
| Total ADR | 30-50 lines |

### When to Split ADRs

Split into multiple ADRs when:
- Decision covers multiple technologies
- Decision affects unrelated areas
- You're writing "and" in the decision statement
- Different stakeholders care about different parts

### When NOT to Create an ADR

- Minor implementation details
- Obvious choices with no real alternatives
- Temporary decisions that will be revisited
- Style preferences (unless establishing standards)

### ADR Maintenance

- Review ADRs quarterly for relevance
- Deprecate outdated decisions promptly
- Keep INDEX.md as the single source of truth
- Categories in INDEX.md should match project structure

## Resources

### references/
- `adr-template.md`: Standalone ADR template (30-50 lines target)
- `index-template.md`: INDEX.md template for new projects
