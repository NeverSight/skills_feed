---
name: design-synthesis
type: simple
depth: extended
description: >-
  Synthesizes research findings into design decisions via codebase investigation.
  Use when (1) translating research into implementation approaches, (2) selecting
  between design alternatives, (3) executing after /research or deep-research, or
  (4) preparing input for /plan phase.
---

# [H1][DESIGN-SYNTHESIS]
>**Dictum:** *Design decisions require grounded context before implementation.*

<br>

Synthesize research findings into design decisions via light codebase investigation.

**Workflow:**
1. §INGEST — Load research artifact, parse original request
2. §SCAN — Light codebase investigation via `parallel-dispatch` (3-4 agents)
3. §EXPLORE — Generate 2-3 approaches with trade-offs
4. §SELECT — Commit to best approach with rationale
5. §OUTPUT — Structured design document

**Dependencies:**
- `parallel-dispatch` — Agent orchestration for codebase scan
- Research artifact — External findings from `deep-research`

**Input:**
- `Research`: Path to research artifact (`research_{slug}.md`)
- `Request`: Original user request/intent

---
## [1][INGEST]
>**Dictum:** *Grounded context prevents speculative design.*

<br>

Load and parse inputs:

| [INDEX] | Source        | Extract                                    |
| :-----: | ------------- | ------------------------------------------ |
|   [1]   | Research file | Findings, confidence levels, key sources   |
|   [2]   | Request       | Intent, scope boundaries, success criteria |

**Parse research structure:**
- `## [1][FINDINGS]` → Domain knowledge by category
- `## [2][CONFIDENCE]` → High/Medium/Low ratings
- `## [3][SOURCES]` → Attribution for decisions

[IMPORTANT]:
- [ALWAYS] Extract high-confidence findings as primary input.
- [ALWAYS] Note low-confidence areas as design risks.
- [NEVER] Proceed without understanding request intent.

---
## [2][SCAN]
>**Dictum:** *Pattern awareness prevents reinvention.*

<br>

Dispatch 3-4 agents via `parallel-dispatch` for codebase context.

**Agent Assignment:**

| [INDEX] | [AGENT]         | [SCOPE]                             | [RETURNS]                                    |
| :-----: | --------------- | ----------------------------------- | -------------------------------------------- |
|   [1]   | **Patterns**    | Similar implementations in codebase | Conventions, reusable patterns, prior art    |
|   [2]   | **Constraints** | Project rules, architecture limits  | Hard boundaries, style requirements          |
|   [3]   | **Interfaces**  | Entry/exit points for feature area  | Touch points, consumers, integration surface |

**Agent Prompt Template:**
```
Scope: [Specific investigation area]
Objective: Surface [patterns|constraints|interfaces] relevant to: [request summary]
Output: Bullet list of findings with file paths
Context: Research indicates: [key findings summary]
Exclusions: Do NOT analyze implementation details or specific file contents
```

[CRITICAL]:
- [ALWAYS] Dispatch ALL agents in ONE message block.
- [ALWAYS] Scope to patterns/constraints/interfaces—NOT implementation.
- [NEVER] Deep-dive into file contents—that's plan's job.

---
## [3][EXPLORE]
>**Dictum:** *Comparison reveals optimal trade-offs.*

<br>

Generate 2-3 distinct approaches from research + scan findings.

**Per Approach:**

| [INDEX] | Aspect     | Content                               |
| :-----: | ---------- | ------------------------------------- |
|   [1]   | Strategy   | High-level implementation direction   |
|   [2]   | Alignment  | How it leverages research findings    |
|   [3]   | Patterns   | Which codebase conventions it follows |
|   [4]   | Trade-offs | Pros and cons                         |

**Approach Generation Criteria:**
- Approach A: Most aligned with existing patterns (conservative)
- Approach B: Best leverage of research findings (optimal)
- Approach C: Simplest implementation path (minimal) — optional

[IMPORTANT]:
- [ALWAYS] Ground approaches in scan findings—no speculation.
- [ALWAYS] Include trade-off analysis per approach.
- [ALWAYS] Apply YAGNI—cut unnecessary scope from all approaches.
- [NEVER] Generate approaches without codebase evidence.

---
## [4][SELECT]
>**Dictum:** *Committed direction enables focused planning.*

<br>

Select best approach via weighted criteria:

| [INDEX] | Criterion         | Weight | Evaluation                            |
| :-----: | ----------------- | ------ | ------------------------------------- |
|   [1]   | Pattern alignment | High   | Matches existing codebase conventions |
|   [2]   | Research support  | High   | Backed by high-confidence findings    |
|   [3]   | Simplicity        | Medium | Minimal moving parts                  |
|   [4]   | Risk profile      | Medium | Low-confidence areas minimized        |

**Selection Output:**
- Selected approach name
- Primary rationale (1-2 sentences)
- Key trade-off accepted

[CRITICAL]:
- [ALWAYS] Commit to ONE approach—no hedging.
- [ALWAYS] Document trade-off accepted.
- [NEVER] Defer selection to downstream phases.

---
## [5][OUTPUT]
>**Dictum:** *Downstream consumers require predictable structure.*

<br>

Produce `brainstorm.md` with structure:

```markdown
# [H1][DESIGN]: [Title]
>**Dictum:** *[Build target—refined from request]*

<br>

**Research Summary:** [Key findings relevant to design]

---
## [1][APPROACHES]

### [1.1][APPROACH_A]: [Name]

| [INDEX] | [ASPECT]  | [DETAIL]                        |
| :-----: | --------- | ------------------------------- |
|   [1]   | Strategy  | [High-level direction]          |
|   [2]   | Alignment | [Research findings leveraged]   |
|   [3]   | Patterns  | [Codebase conventions followed] |
|   [4]   | Pros      | [Benefits]                      |
|   [5]   | Cons      | [Drawbacks]                     |

---
### [1.2][APPROACH_B]: [Name]

| [INDEX] | [ASPECT]  | [DETAIL]                        |
| :-----: | --------- | ------------------------------- |
|   [1]   | Strategy  | [High-level direction]          |
|   [2]   | Alignment | [Research findings leveraged]   |
|   [3]   | Patterns  | [Codebase conventions followed] |
|   [4]   | Pros      | [Benefits]                      |
|   [5]   | Cons      | [Drawbacks]                     |

---
## [2][SELECTED_APPROACH]

| [INDEX] | [KEY]              | [VALUE]                |
| :-----: | ------------------ | ---------------------- |
|   [1]   | Choice             | [Approach name]        |
|   [2]   | Rationale          | [Why this approach]    |
|   [3]   | Trade-off Accepted | [What we're giving up] |

---
## [3][DESIGN_CONSTRAINTS]

| [INDEX] | [CONSTRAINT]    | [SOURCE]        |
| :-----: | --------------- | --------------- |
|   [1]   | [Hard boundary] | [Codebase scan] |
|   [2]   | ...             | ...             |

---
## [4][KEY_DECISIONS]

| [INDEX] | [DECISION]      | [CHOICE]          | [RATIONALE] |
| :-----: | --------------- | ----------------- | ----------- |
|   [1]   | [Design choice] | [Selected option] | [Why]       |
|   [2]   | [Design choice] | [Selected option] | [Why]       |
```

[CRITICAL]:
- [ALWAYS] Include all sections—downstream depends on structure.
- [ALWAYS] Table format for approaches and decisions.
- [NEVER] Prose paragraphs—tables and lists only.

---
## [6][VALIDATION]
>**Dictum:** *Incomplete synthesis cascades errors downstream.*

<br>

[VERIFY]:
- [ ] Ingest: Research parsed, request intent extracted
- [ ] Scan: 3-4 agents dispatched in ONE message
- [ ] Explore: 2-3 approaches with trade-offs generated
- [ ] Select: ONE approach committed with rationale
- [ ] Output: All sections present, table format used
- [ ] YAGNI: Unnecessary scope cut from all approaches
