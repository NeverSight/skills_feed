---
name: spec-knowledge
description: Maintains consistency when creating, modifying, reading, reviewing, or working with specifications. Use when user mentions SPEC.md, requirements, or any specification documents to ensure consistent handling. Provides specification knowledge—quality criteria, editing methods, and three-layer framework (Intent/Design/Consistency).
license: Apache-2.0
metadata:
  author: Aotokitsuruya
---

# Specification

Expertise for working with software specifications.

## What Makes a Good Specification

A specification describes the **target state**—what the system looks like when complete.

| Specification IS | Specification is NOT |
|-----------------|---------------------|
| Target state description | Implementation plan |
| Design decisions (what) | Decision rationale (why) |
| Declarative statements | Narrative explanations |

**Core principle: Constrain design, open implementation.**

- Specify all user-visible decisions
- Leave internal implementation choices to implementers
- If an implementer must guess a design decision, the specification is incomplete

**Anti-patterns:**
- `Note:` — If clarification needed, specification is unclear. Rewrite directly.
- `(Future)`, `(v2)` — Describes target state, not phases. Remove or split into separate spec.
- `(Optional)` — Either required for target state or belongs in Non-goals.

## Three Layers

Complete specifications address three layers:

| Layer | Purpose | Key Question |
|-------|---------|--------------|
| Intent | Why this exists | What problem for whom? |
| Design | What to build | What boundaries, interfaces, behaviors? |
| Consistency | How to stay unified | What patterns for similar problems? |

### Intent Layer

Provides context for judgment calls:

| Element | Role | Core |
|---------|------|------|
| Purpose | What problem the system solves | ✓ |
| Users | Who uses it, what they accomplish | ✓ |
| Impacts | What behavior changes indicate success (drives priority) | |
| Success criteria | What defines "done" and "working" | |
| Non-goals | What is explicitly out of scope | |

Without intent, implementers make technically correct but misaligned decisions.

### Design Layer

Defines observable behaviors and boundaries:

| Element | Role | Format | Core |
|---------|------|--------|------|
| System boundary | What's inside vs outside | See Boundary types | |
| User journeys | Task flows achieving impacts | Context → Action → Outcome | |
| Interfaces | Contracts between internal modules | - | |
| Presenter | How system presents to users | UI: colors, layout / CLI: output format / API: response structure | |
| Behaviors | Outcomes for each state × operation | State + Operation → Result | ✓ |
| Error scenarios | How failures are handled | - | ✓ |

**Boundary types:**

| Type | Defines | Example |
|------|---------|---------|
| Responsibility | What system does / does not do | "Validates input; does not store history" |
| Interaction | Input assumptions / Output guarantees | "Assumes authenticated user; Returns JSON only" |
| Control | What system controls / depends on | "Controls order state; Depends on payment service" |

### Consistency Layer

Establishes patterns for uniform implementation (all items enhance quality, none required for minimal spec):

| Concept | Role | Example |
|---------|------|---------|
| Context | Shared understanding | "This is event-driven" |
| Terminology | Same concept uses same name throughout | "Order" not "Purchase/Transaction/Request" |
| Pattern | Recurring situation → approach | "State changes via events" |
| Form | Expected structure | "Events have type, payload", "Primary: #FF0000", "Errors to stderr" |
| Contract | Interaction agreement | "Handlers must be idempotent" |

Weave these into relevant sections rather than listing separately.

### Implementation Standards (Optional)

For projects requiring code-level consistency across multiple contributors or extended development periods.

| Category | Purpose | Examples |
|----------|---------|----------|
| Architecture | Module boundaries and dependencies | Clean Architecture, Hexagonal, Layered |
| Design Patterns | Reusable solutions | Repository, Factory, Strategy |
| Testing Style | Test structure and conventions | Given-When-Then, Arrange-Act-Assert |
| Code Organization | Directory structure and naming | Feature-based, layer-based, naming conventions |

**When to include:**
- Multiple contributors work on the codebase
- Development spans extended periods
- Codebase requires shared conventions

**When to skip:**
- Simple scripts or single-file utilities
- Prototypes or proof-of-concept
- Short-lived projects

## Quality Criteria

### Specification Rubric

Rate each item Y (yes) or N (no).

**Intent Layer**
| # | Criterion | Required | Y/N |
|---|-----------|----------|-----|
| 1 | Purpose stated in one sentence? | ✓ | |
| 2 | Target users identified? | ✓ | |
| 3 | Impacts (behavior changes) identified? | | |
| 4 | Success criteria measurable or verifiable? | | |

**Design Layer**
| # | Criterion | Required | Y/N |
|---|-----------|----------|-----|
| 5 | Each documented feature has defined behavior? | ✓ | |
| 6 | Error scenarios cover all documented features? | ✓ | |
| 7 | Interaction points (internal and external) have explicit contracts? | | |
| 8 | Implementer can build without clarifying questions? | ✓ | |

**Consistency Layer**
| # | Criterion | Required | Y/N |
|---|-----------|----------|-----|
| 9 | Key terms defined and used consistently throughout? | | |
| 10 | Recurring situations have named patterns? | | |
| 11 | Two implementers would produce compatible results? | | |

**Passing Criteria:**
- All Required Y → Specification is usable. Stop unless improving quality.
- All items Y → Specification is complete. Stop.
- Any Required N → Must address before implementation.
- Non-required N → Address only if relevant to project scope.

### Balance Check

| Question | Design Decision (specify) | Implementation Detail (open) |
|----------|---------------------------|------------------------------|
| User-visible? | Error messages, CLI output | Log format, variable names |
| Affects modules? | Interface signatures | Internal functions |
| Needs consistency? | Error handling pattern | Algorithm choice |
| Could misalign? | Business rules | Performance optimization |

**Test:** "If implemented differently, would users notice or would modules conflict?"

**Warning signs of over-specification:** internal implementation details, algorithm choices (unless user-visible)

**Warning signs of under-specification:** vague terms ("appropriate", "reasonable"), undefined behavior for reachable states

## Common Problems

| Problem | Symptom | Cause | Fix |
|---------|---------|-------|-----|
| Missing intent | Technical tasks instead of user value | No purpose/users defined | Add intent layer |
| Undefined scenarios | Inconsistent edge case behavior | Incomplete state coverage | Enumerate all combinations |
| Over-specification | Implementer constrained unnecessarily | Implementation details included | Keep only observable behaviors |
| Inconsistent patterns | Similar problems solved differently | No shared conventions | Extract and reference patterns |
| Inconsistent terminology | Same concept has multiple names | No shared vocabulary | Define key terms, use consistently |
| Vague language | Ambiguous interpretation | "Handle appropriately" | Use specific values or criteria |
| Hidden assumptions | Works only in specific context | Unstated prerequisites | Make all assumptions explicit |
| Explanatory notes | "Note: because..." appears | Mixing rationale with spec | Rewrite as direct statement |
| Phase markers | "(Future)", "(v2)" in spec | Mixing planning with spec | Remove; spec describes target state |

## Applying This Knowledge

### Progressive Approach

Apply to both writing new specifications and improving existing ones. When improving, identify current phase and proceed from there.

| Phase | Focus | Output | Confirm |
|-------|-------|--------|---------|
| 1. Intent | Why and for whom | Purpose, Users, Impacts | Rubric #1-2 Y |
| 2. Scope | What's included | Feature list, User journeys (Context → Action → Outcome) | List complete |
| 3. Behavior | How it works | Feature behaviors, Error scenarios | Rubric #5-6, #8 Y |
| 4. Refinement | Quality | Patterns, Contracts, Terminology | Rubric #7, #9-11 as needed |

**Rules:**
- Do not write Phase 3 details until Phase 2 is confirmed
- Phase 2 defines user-facing flows; Phase 3 defines internal behaviors
- Return to earlier phases when new understanding emerges
- Specification is usable after Phase 3 (all Required Y)

### When Reviewing

Assess against three layers:

1. **Intent**: Can I explain why this system exists and for whom?
2. **Design**: Can I predict behavior for any user action?
3. **Consistency**: Will similar situations be handled similarly?

Key questions:
- Is this complete enough to implement without guessing?
- Are all design decisions explicit?
- Will two implementers produce compatible results?

Flag: missing layers, vague language, implementation details that should be open, design decisions that should be specified.

### Splitting Content

**Default: Keep everything in SPEC.md.**

Use this decision table to determine when to extract content:

| Decides | Expands | External | → Action |
|---------|---------|----------|----------|
| Y | - | - | Keep in SPEC.md |
| N | N | - | Keep in SPEC.md |
| N | Y | N | May extract (summary + link) |
| N | Y | Y | Extract (link only) |

**Conditions:**
- **Decides**: Cannot understand what to build without reading this
- **Expands**: Complete definition of a decision (all fields, all cases)
- **External**: Maintained by different role/tool

**Examples:**

| Content | Decides | Expands | External | → Action |
|---------|---------|---------|----------|----------|
| Feature behavior | Y | - | - | Keep |
| Decision table | Y | - | - | Keep |
| Error handling rules | Y | - | - | Keep |
| API endpoints (3-5) | N | N | - | Keep |
| Full DB schema (50+ fields) | N | Y | N | May extract |
| Complete test cases | N | Y | N | May extract |
| Figma design | N | Y | Y | Extract |

**When extracting:**
- SPEC.md keeps the decision/summary
- Link: `See [Schema](docs/schema.md) for field definitions`
- Detail documents follow same principles

| Type | Location |
|------|----------|
| Data structures | `docs/schema.md` |
| Visual design | `docs/design.md` or external |
| Test cases | `docs/tests.md` |

**When updating specifications:**
- First determine: decision or detail?
- Decisions go in SPEC.md, details may go in referenced documents
- If adding to external document, verify SPEC.md has the governing decision

**Writing tip:** Use tables (like this decision table) to define boundaries and rules. Tables make conditions explicit and reduce ambiguity.

## Handling Uncertainty

### Undecided design choices

Do not leave gaps. Instead:

1. Present options with tradeoffs
2. Request a decision
3. Document the choice

### Incomplete information

Mark explicitly what is decided vs pending:

```
## Technical Stack

Decided:
- Runtime: Node.js >= 20

To be decided:
- Database: PostgreSQL or SQLite
  (depends on deployment target)
```

### Conflicting requirements

Surface the conflict explicitly and request resolution rather than making assumptions.