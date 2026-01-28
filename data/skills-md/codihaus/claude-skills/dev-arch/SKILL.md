---
name: dev-arch
description: Architecture decisions and technical design for features
version: 1.1.0
---

# /dev-arch - Architecture Design

> **Skill Awareness**: See `skills/_registry.md` for all available skills.
> - **Called by**: `/debrief` (can architecture support this?), `/dev-specs` (what patterns to use?)
> - **Reads**: `_quality-attributes.md` (Architecture Level sections)
> - **After**: Informs `/dev-specs` with architecture decisions

Make architecture decisions for features. Ensures scalability, maintainability, and quality from the start.

## When to Use

- New feature that requires structural decisions
- Existing feature that needs significant changes
- When `/debrief` needs to validate feasibility
- When `/dev-specs` needs patterns for implementation
- Technical debt evaluation

## Usage

```
/dev-arch auth                    # Architecture for auth feature
/dev-arch billing --new           # New feature (more thorough)
/dev-arch payments --evaluate     # Evaluate existing architecture
```

## When Called

### From `/debrief`

```
/debrief creates use cases
    ↓
Calls /dev-arch with question:
    "Can current architecture support these requirements?"
    ↓
/dev-arch returns:
    - Yes, existing patterns work
    - Yes, with minor additions (specify)
    - No, need new architecture (propose)
```

### From `/dev-specs`

```
/dev-specs starts generating specs
    ↓
Calls /dev-arch with question:
    "What patterns should specs use?"
    ↓
/dev-arch returns:
    - API patterns (REST/GraphQL, conventions)
    - Data patterns (models, relationships)
    - Component patterns (structure, state)
    - Integration patterns (how pieces connect)
```

## Output

```
plans/features/{feature}/
├── architecture.md          # Architecture decisions
├── adrs/                    # Architecture Decision Records
│   ├── ADR-001-api-style.md
│   ├── ADR-002-auth-strategy.md
│   └── ...
├── scout.md                 # From /dev-scout
└── specs/                   # From /dev-specs (uses architecture.md)
```

## Expected Outcome

Architecture decisions for what's **NEW**. Follow existing for what's **KNOWN**.

**Outputs:**
- `architecture.md` - If architecture decisions made
- `adrs/ADR-*.md` - For new decisions only (not for following existing patterns)
- Patterns to follow (API, data, component, auth)
- Quality assessment against `_quality-attributes.md`

## Success Criteria

- Existing patterns followed automatically (no questions asked)
- Only ask about gaps (missing tech, new requirements)
- Quality attributes checked (scalability, security, performance, etc.)
- Team stays in their comfort zone
- Minimal output for Follow mode, detailed for Design mode

## Modes

Auto-detect based on scout:

| Condition | Mode | Behavior |
|-----------|------|----------|
| Scout has established patterns | **Follow** | Use existing patterns, no questions, minimal output |
| Scout exists but feature needs NEW tech | **Extend** | Ask ONLY about the gap |
| No scout / greenfield OR `--new` flag | **Design** | Ask constraint questions, present options |

## Context Sources

Read to understand current state:
- `plans/scout/README.md` - Project-level patterns
- `plans/features/{feature}/scout.md` - Feature-level patterns
- `plans/features/{feature}/README.md` - Feature requirements
- `plans/brd/use-cases/{feature}/*.md` - Use cases
- `_quality-attributes.md` - Architecture Level checklists
- `plans/docs-graph.json` - Dependencies

## Follow Mode

**When:** Scout shows established patterns

**Approach:** Extract and apply automatically

**Extract from scout:**
- API style (REST, GraphQL, tRPC)
- Database (PostgreSQL + Prisma, MySQL, etc.)
- Frontend (React + Zustand, Vue + Pinia, etc.)
- Auth (JWT, session, OAuth)
- Folder structure

**Apply to new feature:**
- New endpoints follow existing API pattern
- New models use existing ORM conventions
- New components follow existing structure
- Only flag if requirements CANNOT fit

**Output:** Minimal architecture.md noting patterns applied

## Extend Mode

**When:** Existing patterns but feature needs something new

**Approach:** Ask ONLY about the gap

**Identify gaps:**
- Feature needs real-time (no WebSocket configured)
- Feature needs payments (no payment provider)
- Feature needs file uploads (no storage)
- Feature needs queue (no background jobs)

**Present options for gap only:**
- Recommend based on constraints
- Pros/cons of each option
- Ask user to choose

**Everything else:** Follow existing patterns

## Design Mode

**When:** No existing patterns OR `--new` flag

**Approach:** Ask constraint questions, present options

**Ask about:**
- Project context (new/existing/rebuild)
- Team & deployment (solo/small/large, VPS/cloud)
- Key constraints (tech, budget, timeline, compliance)

**Present recommendations based on constraints:**
- Recommended stack with rationale
- Alternatives considered (why not)
- Ask user to approve or modify

## Gap Analysis

For any mode, identify gaps:

**Compare:**
- Requirements (what feature needs)
- Current capabilities (what exists)
- Gaps (what's missing)
- Actions (decisions needed)

**Output:**
- Requirements vs Capabilities table
- Gaps requiring decisions

## Decision Making

**Only create ADRs for NEW decisions**, not for following existing patterns.

**Decision categories:**
- API (REST vs GraphQL, versioning, conventions)
- Data (database, ORM, schema design)
- Auth (JWT/session/OAuth, permissions)
- Frontend (state management, component structure)
- Integration (service connections, event-driven)
- Infrastructure (caching, queues, storage, email)

**Each decision includes:**
- Context (why needed)
- Options considered (pros/cons/effort)
- Decision (chosen option + rationale)
- Consequences (trade-offs accepted)

## Quality Assessment

Apply `_quality-attributes.md` Architecture Level checklists:

- **Scalability:** Stateless design, pagination, caching, background jobs
- **Maintainability:** Module boundaries, consistent structure, abstracted dependencies
- **Security:** Auth strategy, permission model, data encryption
- **Reliability:** No single points of failure, graceful degradation
- **Performance:** Latency targets, CDN, optimizations
- **Testability:** Injectable dependencies, test strategy

## Architecture Document

Create `plans/features/{feature}/architecture.md` with:
- Overview (high-level description)
- Architecture diagram (Mermaid)
- Key decisions table
- Patterns to follow (API, data, component, auth)
- Quality checklist
- ADRs (if created)
- Risks & mitigations
- Next steps

## ADR Format

Create `plans/features/{feature}/adrs/ADR-{NNN}-{slug}.md` with:
- Status (Proposed/Accepted/Deprecated/Superseded)
- Context (why this decision)
- Decision (what we're doing)
- Options considered (with pros/cons)
- Consequences (positive/negative/neutral)
- Related decisions

## Decision Categories

### API Design

| Question | Options |
|----------|---------|
| Style | REST, GraphQL, tRPC, gRPC |
| Versioning | URL path, header, none |
| Auth header | Bearer token, cookie, API key |
| Response format | JSON:API, custom, none |

### Database

| Question | Options |
|----------|---------|
| Type | PostgreSQL, MySQL, MongoDB, SQLite |
| ORM | Prisma, TypeORM, Drizzle, raw SQL |
| Migrations | ORM-managed, manual, none |
| Soft deletes | Yes (deletedAt), no |

### Frontend State

| Question | Options |
|----------|---------|
| Global state | Redux, Zustand, Jotai, Context |
| Server state | React Query, SWR, manual |
| Forms | React Hook Form, Formik, native |

### Authentication

| Question | Options |
|----------|---------|
| Strategy | JWT, session, OAuth only |
| Token storage | httpOnly cookie, localStorage, memory |
| Refresh | Sliding window, explicit refresh |
| Permissions | RBAC, ABAC, simple roles |

### Infrastructure

| Question | Options |
|----------|---------|
| Caching | Redis, in-memory, CDN |
| Queue | Redis/BullMQ, SQS, RabbitMQ |
| File storage | S3, local, Cloudinary |
| Email | SendGrid, SES, SMTP |

## Tools Used

| Tool | Purpose |
|------|---------|
| `Read` | Load requirements, scout, quality attributes |
| `Write` | Create architecture.md, ADRs |
| `Glob` | Find existing patterns |
| `Grep` | Search for conventions |
| `AskUserQuestion` | Clarify decisions |
| `Context7` | Look up architecture best practices |
| `WebSearch` | Find architecture patterns |

### Context7 for Architecture Research

When making architecture decisions, use Context7 to look up best practices:

```
1. Resolve library ID
   → mcp__context7__resolve-library-id({
       libraryName: "prisma",
       query: "database schema design patterns"
     })

2. Query documentation
   → mcp__context7__query-docs({
       libraryId: "/prisma/prisma",
       query: "relations and foreign keys best practices"
     })
```

**Use for:**
- ORM patterns (Prisma, TypeORM, Drizzle)
- Framework architecture (Next.js, NestJS)
- Auth library patterns (NextAuth, Lucia)
- API design (REST, GraphQL, tRPC)

## Integration

| Skill | Relationship |
|-------|--------------|
| `/debrief` | Calls to validate feasibility |
| `/dev-scout` | Provides current state analysis |
| `/dev-specs` | Consumes architecture decisions |
| `/utils/diagram` | Validates mermaid diagrams |
| `_quality-attributes.md` | Provides checklists |

## Key Principle

> **Use existing patterns. Only ask about what's truly new.**

The team's current architecture is their comfort zone. They know it, they control it.
Don't suggest microservices to a monolith team. Don't ask about database choice when they're already on PostgreSQL.

```
Existing patterns → Follow automatically
New requirements that don't fit → Ask only about those
Greenfield → Ask constraint questions
```

## Example Flows

### Example 1: Follow Mode (Most Common)

```
User: /dev-arch notifications

1. Mode detection
   → Scout exists with established patterns
   → Mode: FOLLOW

2. Load context
   → Project uses: Next.js, REST API, PostgreSQL, Prisma
   → Feature needs: notification preferences, email sending

3. Apply existing patterns (NO QUESTIONS)
   → API: POST /api/notifications, GET /api/notifications
   → Database: Notification model with Prisma
   → Frontend: NotificationSettings component

4. Check for gaps
   → Email sending needed
   → Project already has SendGrid configured ✓
   → No gaps!

5. Output (minimal)
   "Using existing patterns. No architecture changes needed.
    - New Notification model
    - New API endpoints following REST convention
    - Uses existing SendGrid for emails"

No ADRs created. No questions asked.
```

### Example 2: Extend Mode (New Part Only)

```
User: /dev-arch billing

1. Mode detection
   → Scout exists with established patterns
   → Mode: FOLLOW initially...

2. Load context
   → Project uses: Next.js, REST, PostgreSQL
   → Feature needs: payment processing, subscriptions

3. Check for gaps
   → Payment processing needed
   → Project has NO payment provider ← Gap found!
   → Mode switches to: EXTEND

4. Ask ONLY about the gap
   "Feature needs payment processing. No provider configured.
    Options:
    A: Stripe (Recommended) - Popular, good docs
    B: Paddle - Handles taxes
    C: LemonSqueezy - Simpler

    Which provider?"

   → User: "Stripe"

5. Everything else follows existing patterns
   → API: REST endpoints for billing
   → Database: Prisma models
   → Frontend: Existing component patterns

6. Output
   → architecture.md (documents Stripe choice)
   → ADR-001-payment-provider.md (only for the NEW decision)

   "Stripe selected. All other patterns follow existing project architecture."
```

### Example 3: Design Mode (Greenfield)

```
User: /dev-arch auth --new

1. Mode detection
   → --new flag provided
   → Mode: DESIGN

2. Ask constraint questions
   Q1: "Team size?"
   → Small team (3 devs)

   Q2: "Deployment target?"
   → Vercel

   Q3: "Constraints?"
   → Tight timeline

3. Present options based on constraints
   "Based on: Small team, Vercel, tight timeline

    Recommended:
    - NextAuth.js (simple, works with Vercel)
    - JWT in httpOnly cookies
    - RBAC for permissions

    Alternatives considered:
    - Auth0: Good but adds external dependency
    - Custom JWT: More work, tight timeline

    Proceed with NextAuth.js?"

   → User: "Yes"

4. Generate full architecture
   → architecture.md (complete auth design)
   → ADR-001-auth-strategy.md
   → ADR-002-permission-model.md
```

## Summary

| Mode | Questions Asked | ADRs Created |
|------|-----------------|--------------|
| Follow | None | None |
| Extend | Only for gaps | Only for new decisions |
| Design | Full constraint gathering | For all decisions |

**Default to Follow mode. Only escalate when necessary.**
