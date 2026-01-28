---
name: plan
description: "Create implementation plans from spec via iterative codebase research and strategic questions. Produces mini-PR plans optimized for iterative development. Use after $spec or when you have clear requirements. Triggers: plan, implementation plan, how to build."
metadata:
  short-description: "Implementation planning with codebase research"
---

**User request**: $ARGUMENTS

Build implementation plan through structured discovery. Takes spec (from `$spec` or inline), iteratively researches codebase + asks high-priority technical questions that shape implementation direction → detailed plan.

**Focus**: HOW not WHAT. Spec=what; plan=architecture, files, functions, chunks, dependencies, tests.

**Loop**: Research → Expand todos → Ask questions → Write findings → Repeat until complete

**Output files**:
- Plan: `/tmp/plan-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md`
- Research log: `/tmp/plan-research-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` (external memory)

## Boundaries

- Spec=requirements; this skill=architecture, files, chunks, tests
- Don't modify spec; flag gaps for user
- Surface infeasibility before proceeding
- No implementation until approved

## Phase 1: Initial Setup

### 1.1 Create todos (update_plan immediately)

Todos = **areas to research/decide**, not steps. Expand when research reveals: (a) files/modules to modify beyond those already in todos, (b) 2+ valid implementation patterns with different trade-offs, (c) dependencies on code/systems not yet analyzed, or (d) questions that must be answered before completing an existing todo.

**Starter seeds**:
```
- [ ] Read/infer spec requirements
- [ ] Codebase research (patterns, files to modify)
- [ ] Approach identification (if >1 valid approach → trade-off analysis → user decision)
- [ ] Architecture decisions (within chosen approach)
- [ ] (expand as research reveals)
- [ ] Read full research log and spec (context refresh before output)
- [ ] Finalize chunks
```

**Evolution example** - "Add real-time notifications":
```
- [x] Read spec → 3 types, mobile+web
- [x] Codebase research → found ws.ts, notification-service.ts, polling in legacy/
- [x] Approach selection → WebSocket vs polling? User chose WebSocket
- [ ] Architecture decisions (within WebSocket approach)
- [ ] Offline storage (IndexedDB vs localStorage)
- [ ] Sync conflict resolution
- [ ] Service worker integration
- [ ] Read full research log and spec (context refresh)
- [ ] Finalize chunks
```

Note: Approach selection shows **user decision**—not auto-decided. Found two valid approaches, presented trade-offs, user chose.

**Key**: Never prune todos prematurely. Circular dependencies → merge into single todo: "Research {A} + {B} (merged: circular)".

**Adapt to scope**: Simple (1-2 files) → omit approach identification if single valid approach. Complex (5+ files) → add domain-specific todos.

### 1.2 Create research log

Path: `/tmp/plan-research-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md`

```markdown
# Research Log: {feature}
Started: {timestamp} | Spec: {path or "inline"}

## Codebase Research
## Approach Trade-offs
## Spec Gaps
## Conflicts
## Risks & Mitigations
## Architecture Decisions
## Questions & Answers
## Unresolved Items
```

## Phase 2: Context Gathering

### 2.1 Read/infer spec

Extract: requirements, user stories, acceptance criteria, constraints, out-of-scope.

**No formal spec?** Infer from conversation, tool outputs, user request. If spec and conversation together provide fewer than 2 concrete requirements, ask user: "I need at least 2 concrete requirements to plan. Please provide: [list what's missing]" before proceeding.

### 2.2 Research codebase

Explore existing implementations, files to modify, patterns, integration points, test patterns. Use file search and code reading to understand:
- How similar features are implemented
- What files need modification
- Existing patterns and conventions
- Test structure and patterns

### 2.3 Read ALL recommended files

No skipping. Gives firsthand knowledge of patterns, architecture, integration, tests.

### 2.4 Update research log

After EACH step:
```markdown
### {timestamp} - {what researched}
- Explored: {areas}
- Key findings: {files, patterns, integration points}
- New areas: {list}
- Architectural questions: {list}
```

### 2.5 Approach Identification & Trade-off Analysis

**CRITICAL**: Before implementation details, identify whether multiple valid approaches exist. This is THE question that cuts option space—answering it eliminates entire planning branches.

Valid approach = (1) fulfills all spec requirements, (2) technically feasible, (3) has at least one "When it wins" condition. Don't present invalid approaches.

**When**: After initial research (2.2-2.4), before any implementation details.

**What counts as multiple approaches**: different architectural layers, implementation patterns (eager/lazy, push/pull), integration points (modify existing vs create new), scopes (filter at source vs consumer). Multiple valid locations = multiple approaches; multiple valid patterns = multiple approaches.

**Process**:
1. From research: Where could this live? How implemented? Who consumes what we're modifying?
2. **One valid approach** → document why in log, proceed
3. **Multiple valid** → STOP until user decides

**Trade-off format** (research log `## Approach Trade-offs`):
```markdown
### Approaches: {what deciding}

**Approach A: {name}**
- How: {description}
- Pros: {list}
- Cons: {list}
- When it wins: {conditions}
- Affected consumers: {list}

**Approach B: {name}**
- How: {description}
- Pros: {list}
- Cons: {list}
- When it wins: {conditions}
- Affected consumers: {list}

**Existing codebase pattern**: {how similar solved}
**Recommendation**: {approach} — {why}
**Choose alternative if**: {honest conditions where other approach wins}
```

**Recommendation = cleanest**: (1) separation of concerns (if unsure: use layer where similar features live), (2) matches codebase patterns, (3) minimizes blast radius, (4) most reversible. Prioritize 1>2>3>4.

**Be honest**: State clearly when alternative wins. User has context you don't (future plans, team preferences, business constraints).

**Skip asking only when**: genuinely ONE valid approach (document why others don't work) OR ALL five measurable skip criteria true:
1. Same files changed by both
2. No consumer behavior change
3. Reversible in <1 chunk (<200 lines)
4. No schema/API/public interface changes
5. No different error/failure modes

If ANY fails → ask user.

### 2.6 Write initial draft

**Precondition**: Approach decided (single documented OR user chose/delegated after trade-offs). Don't write until approach resolved.

First draft with `[TBD]` markers. Same file path for all updates.

## Phase 3: Iterative Discovery Interview

### Memento Loop

1. Mark todo `in_progress`
2. Research (codebase) OR ask question
3. **Write findings immediately** to research log
4. Expand todos for new questions/integration points/dependencies
5. Update plan (replace `[TBD]`)
6. Mark todo `completed`
7. Repeat until no pending todos

**NEVER proceed without writing findings** — research log = external memory.

**If user answer contradicts prior decisions**: (1) Inform user: "This contradicts earlier decision X. Proceeding with new answer." (2) Log in research log under `## Conflicts` with both decisions. (3) Re-evaluate affected todos. (4) Update plan accordingly. If contradiction cannot be resolved, ask user to clarify priority.

### Research Log Update Format

```markdown
### {timestamp} - {what}
**Todo**: {which}
**Finding/Answer**: {result}
**Impact**: {what revealed/decided}
**New areas**: {list or "none"}
```

Architecture decisions:
```markdown
- {Area}: {choice} — {rationale}
```

### Todo Expansion Triggers

| Research Reveals | Add Todos For |
|------------------|---------------|
| Existing similar code | Integration approach |
| Multiple valid patterns | Pattern selection |
| External dependency | Dependency strategy |
| Complex state | State architecture |
| Cross-cutting concern | Concern isolation |
| Performance-sensitive | Performance strategy |
| Migration needed | Migration path |

### Interview Rules

**Unbounded loop**: Iterate until ALL completion criteria met. No fixed round limit. If user says "just decide", "you pick", "I don't care", "skip this", or otherwise explicitly delegates the decision, document remaining decisions with `[INFERRED: {choice} - {rationale}]` markers and finalize.

**Spec-first**: Business scope and requirements belong in spec. Questions here are TECHNICAL only—architecture, patterns, implementation approach. If spec has gaps affecting implementation: (1) flag in research log under `## Spec Gaps`, (2) ask user whether to pause for spec update OR proceed with stated assumption, (3) document choice and continue.

1. **Prioritize questions that eliminate other questions** - Ask questions where the answer changes what other questions you need to ask, or eliminates entire branches of implementation. If knowing X makes Y irrelevant, ask X first.

2. **Interleave discovery and questions**:
   - User answer reveals new area → research codebase
   - Need external context → use web search
   - Update plan after each iteration, replacing `[TBD]` markers

3. **Question priority order**:

   | Priority | Type | Purpose | Examples |
   |----------|------|---------|----------|
   | 0 | Approach Selection | Fundamental architecture | WebSocket vs polling? Modify existing vs create new? Filter at source vs consumer? Where should this live? |
   | 1 | Implementation Phasing | How much to build now vs later | Full impl vs stub? Include migration? Optimize or simple first? |
   | 2 | Branching | Open/close implementation paths | Sync vs async? Polling vs push? In-memory vs persistent? |
   | 3 | Technical Constraints | Non-negotiable technical limits | Must integrate with X? Performance requirements? Backward compatibility? |
   | 4 | Architectural | Choose between patterns | Error strategy? State management? Concurrency model? |
   | 5 | Detail Refinement | Fine-grained technical details | Test coverage scope? Retry policy? Logging verbosity? |

   **P0 rules**: If P0 question exists, ask P0 **first** before ANY implementation details. Wrong approach = entire plan wasted. P0 is mandatory when >1 valid approach (section 2.5).

4. **Always mark one option "(Recommended)"** - put first with reasoning in description. When options are equivalent AND easily reversible (changes affect only 1-2 files, where each changed file is imported by 5 or fewer other files, and there are no data migrations, schema changes, or public API changes), decide yourself (lean toward existing codebase patterns).

5. **Be thorough via technique**:
   - Cover technical decisions from each applicable priority category (1-5 in the priority table)—don't skip categories to save time
   - Reduce cognitive load through HOW you ask: concrete options, good defaults
   - **Batching**: Group related questions together (batch questions that share a common decision—e.g., multiple state management questions, or multiple error handling questions—where answers to one inform the others)
   - Make decisions yourself when codebase research suffices
   - Complete plan with easy questions > incomplete plan with fewer questions

6. **Ask non-obvious questions** - Error handling strategies, edge cases affecting correctness, performance implications, testing approach for complex logic, rollback/migration needs, failure modes

7. **Ask vs Decide** - Codebase patterns and technical standards are authority; user decides significant trade-offs.

   **Ask user when**:
   | Category | Examples |
   |----------|----------|
   | Trade-offs affecting measurable outcomes | Estimated >20% change to latency/throughput vs current implementation, adds abstraction layers, locks approach for >6 months, changes user-facing behavior |
   | No clear codebase precedent | New pattern not yet established |
   | Multiple valid approaches | Architecture choice with different implications |
   | Phasing decisions | Full impl vs stub, migration included or deferred |
   | Breaking changes | API changes, schema migrations |
   | Resource allocation | Cache size, connection pools, batch sizes with cost implications |

   **Decide yourself when**:
   | Category | Examples |
   |----------|----------|
   | Existing codebase pattern | Error format, naming conventions, file structure |
   | Industry standard | HTTP status codes, retry with exponential backoff |
   | Sensible defaults | Timeout 30s, pagination 50 items, debounce 300ms |
   | Easily changed later | Internal function names, log messages, test structure |
   | Implementation detail | Which hook to use, internal state shape, helper organization |
   | Clear best practice | Dependency injection, separation of concerns |

   **Test**: "If I picked wrong, would user say 'that's not what I meant' (ASK) or 'that works, I would have done similar' (DECIDE)?"

## Phase 4: Finalize & Present

### 4.1 Final research log update

```markdown
## Planning Complete
Finished: {timestamp} | Research log entries: {count} | Architecture decisions: {count}
## Summary
{Key decisions}
```

### 4.2 Refresh context

Read the full research log file to restore all findings, decisions, and rationale into context before writing the final plan.

### 4.3 Finalize plan

Remove `[TBD]`, ensure chunk consistency, verify dependency ordering, add line ranges for files >500 lines.

### 4.4 Mark all todos complete

### 4.5 Present approval summary

```
## Plan Approval Summary: {Feature}

**Plan file**: /tmp/plan-{...}.md

### At a Glance
| Aspect | Summary |
|--------|---------|
| Approach | {Chosen approach from P0 decision} |
| Chunks | {count} |
| Parallel | {which chunks can run in parallel} |
| Risk | {primary risk or "Low - standard patterns"} |

### Execution Flow

{ASCII dependency diagram}

Example format:
┌─────────────┐
│  1. Types   │
└──────┬──────┘
       │
  ┌────┴────┐
  ▼         ▼
┌─────┐   ┌─────┐
│ 2.A │   │ 2.B │  ← Parallel
└──┬──┘   └──┬──┘
   └────┬────┘
        ▼
   ┌─────────┐
   │ 3. Integ│
   └─────────┘

### Chunks
1. **{Name}**: {one-line description}
2. **{Name}**: {one-line description}
...

### Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| {Area} | {Choice} | {Brief why} |

### Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| {Risk} | {How addressed} |

---
Review full plan. Approve to start implementation.
```

**Diagram guidelines**:
- Show chunk dependencies and parallel opportunities
- Number chunks to match plan
- Use box characters: `┌ ┐ └ ┘ │ ─ ┬ ┴ ├ ┤ ▼` or simple ASCII
- Label parallel opportunities
- Keep to actual chunk count

### 4.6 Wait for approval

Do NOT implement until user explicitly approves. After approval: create todos from chunks, execute.

---

# Planning Methodology

## 1. Principles

| Principle | Description |
|-----------|-------------|
| **Safety** | Never skip gates (type checks, tests, lint); every chunk tests+demos independently |
| **Clarity** | Full paths, numbered chunks, rationale for context files, line ranges |
| **Minimalism** | Ship today's requirements; parallelize where possible |
| **Forward focus** | Don't prioritize backward compatibility unless requested or public API/schema contracts would be broken |
| **Cognitive load** | Deep modules with simple interfaces > many shallow; reduce choices |
| **Conflicts** | Safety > Clarity > Minimalism > Forward focus |

**Definitions**:
- **Gates**: Quality checks every chunk must pass—type checks (0 errors), tests (pass), lint (clean)
- **Mini-PR**: A chunk sized to be its own small pull request—complete, mergeable, reviewable independently
- **Deep modules**: Modules that hide complexity behind simple interfaces (few public methods, rich internal logic)

### Code Quality (P1-P10)

User's explicit intent takes precedence for implementation choices (P2-P10). P1 (Correctness) and Safety gates (type checks 0 errors, tests pass, lint clean) are non-negotiable—if user requests skipping these, flag as risk but do not skip.

| # | Principle | Planning Implication |
|---|-----------|---------------------|
| P1 | Correctness | Every chunk must demonstrably work |
| P2 | Observability | Plan logging, error visibility |
| P3 | Illegal States Unrepresentable | Design types preventing compile-time bugs |
| P4 | Single Responsibility | Each chunk ONE thing |
| P5 | Explicit Over Implicit | Clear APIs, no hidden behaviors |
| P6 | Minimal Surface Area | YAGNI—don't add features beyond spec |
| P7 | Tests | Specific cases, not "add tests" |
| P8 | Safe Evolution | Public API/schema changes need migration |
| P9 | Fault Containment | Plan failure isolation, retry/fallback |
| P10 | Comments Why | Document complex logic why, not what |

P1-P10 apply to code quality within chunks. Principle conflicts (Safety > Clarity > Minimalism > Forward focus) govern planning-level decisions. When both apply, Safety (gates) takes precedence over all P2-P10.

**Values**: Mini-PR > monolithic; parallel > sequential; function-level > code details; dependency clarity > implicit coupling; ship-ready > half-built

## 2. Mini-PR Chunks

Each chunk must:
1. Ship complete value (demo independently)
2. Pass all gates (type checks, tests, lint)
3. Be mergeable alone (1-3 functions, <200 lines of code)
4. Include its tests (name specific inputs/scenarios, e.g., "valid email accepts user@domain.com", "invalid rejects missing @")

## 3. Chunk Sizing

| Complexity | Chunks | Guidance |
|------------|--------|----------|
| Simple | 1-2 | 1-3 functions each |
| Medium | 3-5 | <200 lines of code per chunk |
| Complex | 5-8 | Each demo-able |
| Integration | +1 final | Connect prior work |

**Decision guide**: New model/schema → types chunk first | >3 files or >5 functions → split by concern | Complex integration → foundation then integration | One module <200 lines of code → single chunk OK

## 4. Dependency Ordering

- **True dependencies**: uses types, calls functions, extends
- **False dependencies**: same feature, no interaction (parallelize these)
- Minimize chains: A→B and A→C, then B,C→D (not A→B→C→D)
- Circular dependencies: If chunks form a cycle (A needs B, B needs C, C needs A), extract shared interfaces/types into a new foundation chunk that breaks the cycle
- Number chunks; mark parallel opportunities

## 5. What Belongs

| Belongs | Does Not Belong |
|---------|-----------------|
| Numbered chunks, gates, todo descriptions | Code snippets |
| File manifests with reasons | Extra features, future-proofing |
| Function names only | Performance tuning, assumed knowledge |

## 6. Cognitive Load

- Deep modules first: fewer with simple interfaces, hide complexity
- Minimize indirection: layers only for concrete extension
- Composition root: one wiring point
- Decide late: abstraction only when PR needs extension
- Framework at edges: core logic agnostic, thin adapters
- Reduce choices: one idiomatic approach per concern
- Measure: if understanding the chunk's purpose requires reading more than 3 files or tracing more than 5 function calls, simplify it

## 7. Common Patterns

| Pattern | Flow |
|---------|------|
| Sequential | Model → Logic → API → Error handling |
| Parallel after foundation | Model → CRUD ops (parallel) → Integration |
| Pipeline | Types → Parse/Transform (parallel) → Format → Errors |
| Authentication | User model → Login → Auth middleware → Logout |
| Search | Data structure → Algorithm → API → Ranking |

## 8. Plan Template

```markdown
# IMPLEMENTATION PLAN: [Feature]

[1-2 sentences]

Gates: Type checks (0 errors), Tests (pass), Lint (clean)

---

## Requirement Coverage
- [Spec requirement] → Chunk N
- [Spec requirement] → Chunk M, Chunk N

---

## 1. [Name]

Depends on: - | Parallel: -

[What this delivers]

Files to modify:
- path.ts - [changes]

Files to create:
- new.ts - [purpose]

Context files:
- reference.ts - [why relevant]

Notes: [Assumptions, alternatives considered]

Risks:
- [Specific risk] → [mitigation]

Tasks:
- Implement fn() - [purpose]
- Tests - [cases]
- Run gates

Acceptance criteria:
- Gates pass
- [Specific verifiable criterion]

Key functions: fn(), helper()
Types: TypeName
```

### Good Example

```markdown
## 2. Add User Validation Service

Depends on: 1 (User types) | Parallel: 3

Implements email/password validation with rate limiting.

Files to modify:
- src/services/user.ts - Add validateUserInput()

Files to create:
- src/services/validation.ts - Validation + rate limiter

Context:
- src/services/auth.ts:45-80 - Existing validation patterns
- src/types/user.ts - User types from chunk 1

Tasks:
- validateEmail() - RFC 5322
- validatePassword() - Min 8, 1 number, 1 special
- rateLimit() - 5 attempts/min/IP
- Tests: valid email, invalid formats, password edges, rate limit
- Run gates

Acceptance criteria:
- Gates pass
- validateEmail() rejects invalid formats, accepts valid RFC 5322
- validatePassword() enforces min 8, 1 number, 1 special
- Rate limiter blocks after 5 attempts/min/IP

Functions: validateUserInput(), validateEmail(), rateLimit()
Types: ValidationResult, RateLimitConfig
```

### Bad Example

```markdown
## 2. User Stuff
Add validation for users.
Files: user.ts
Tasks: Add validation, Add tests
```

**Why bad**: No dependencies, vague description, missing full paths, no context files, generic tasks, no functions listed, no acceptance criteria.

## 9. File Manifest & Context

- Every file to modify/create; specify changes and purpose
- Full paths; zero prior knowledge assumed
- Context files: explain WHY; line ranges for files >500 lines

## 10. Quality Criteria

| Level | Criteria |
|-------|----------|
| Good | Each chunk ships value; dependencies ordered; parallel identified; files explicit; context has reasons; tests in todos; gates listed |
| Excellent | + optimal parallelization, line numbers, clear integration, risks, alternatives, reduces cognitive load |

### Quality Checklist

**MUST verify**:
- [ ] Correctness: boundaries, null/empty, error paths
- [ ] Type Safety: types prevent invalid states; validation at boundaries
- [ ] Tests: critical + error + boundary paths

**SHOULD verify**:
- [ ] Observability: errors logged with context
- [ ] Resilience: timeouts, retries with backoff, cleanup
- [ ] Clarity: descriptive names, no magic values
- [ ] Modularity: single responsibility, <200 lines of code, minimal coupling
- [ ] Evolution: public API/schema changes have migration

### Test Priority

| Priority | What | Requirement |
|----------|------|-------------|
| 9-10 | Data mutations, money, auth, state machines | MUST |
| 7-8 | Business logic, API contracts, errors | SHOULD |
| 5-6 | Edge cases, boundaries, integration | GOOD |
| 1-4 | Trivial getters, pass-through | OPTIONAL |

### Error Handling

For external systems/user input, specify:
1. What can fail
2. How failures surface
3. Recovery strategy

Avoid: empty catch, catch-return-null, silent fallbacks, broad catching.

## 11. Problem Scenarios

| Scenario | Action |
|----------|--------|
| No detailed requirements | Research → core requirements/constraints unclear: ask user OR stop → non-critical: assume+document |
| Extensive requirements | MUSTs first → research scope → ask priority trade-offs → defer SHOULD/MAY |
| Multiple approaches | Research first → ask only when significantly different implications |
| Everything dependent | Start from types → question each dependency → find false dependencies → foundation → parallel → integration |

## Planning Mantras

**Memento (always):**
1. Write findings BEFORE next step (research log = external memory)
2. Every discovery needing follow-up → todo
3. Update research log after EACH step

**Primary:**
4. Smallest shippable increment?
5. Passes all gates?
6. Explicitly required?
7. Passes review first submission?

**Secondary:**
8. Ship with less?
9. Dependencies determine order?
10. Researched first, asked strategically?
11. Reduces cognitive load?
12. Satisfies P1-P10?
13. Error paths planned?

### Never Do

- Proceed without writing findings
- Keep discoveries as mental notes
- Skip todos
- Write to project directories (always `/tmp/`)
- Ask scope/requirements questions (that's spec phase)
- Finalize with `[TBD]`
- Implement without approval
- Forget expanding todos on new areas

## Recognize & Adjust

| Symptom | Action |
|---------|--------|
| Chunk >200 lines of code | Split by concern |
| No clear value | Merge or refocus |
| Dependencies unclear | Make explicit, number |
| Context missing | Add files + line numbers |
| Alternative approach after draft | STOP. Back to 2.5. Document, ask, may restart |
| "Obvious" location without checking consumers | STOP. Search usages. Multiple consumers → ask user |
| User rejects approach during/after impl | Should have been asked earlier. Document lesson, present alternatives |
