---
name: stream-coding
version: 3.4.0
description: >
  Documentation-first development methodology. The goal is AI-ready
  documentation - when docs are clear enough, code generation becomes automatic.
author: Francesco Marinoni Moretto
license: CC-BY-4.0
repository: https://github.com/frmoretto/stream-coding
triggers:
  - stream coding
  - documentation-first
  - build
  - create
  - implement
  - document
  - spec out
capabilities:
  - documentation-methodology
  - clarity-gate-integration
  - ai-ready-specs
spec_version: "3.4"
---

# Stream Coding v3.4: Documentation-First Development

## ⚠️ CRITICAL REFRAME: THIS IS A DOCUMENTATION METHODOLOGY, NOT A CODING METHODOLOGY

**The Goal:** AI-ready documentation. When documentation is clear enough, code generation becomes automatic.

**The Insight:**
> "If your docs are good enough, AI writes the code. The hard work IS the documentation. Code is just the printout."

**v3.4 Core Addition:** Complete 13-item Clarity Gate with scoring rubric. The gate is the methodology—skip it and you're back to vibe coding.

---

## CHANGELOG

| Version | Changes |
|---------|---------|
| 3.0 | Initial Stream Coding methodology |
| 3.1 | Clearer terminology, mandatory Clarity Gate |
| 3.3 | Document-type-aware placement (Anti-patterns, Test Cases, Error Handling in implementation docs) |
| 3.3.1 | Corrected time allocation (40/40/20), added Phase 4, added Rule of Divergence |
| **3.4** | **Complete 13-item Clarity Gate, scoring rubric with weights, self-assessment questions, 4 mandatory section templates, Documentation Audit integrated into Phase 1** |

---

## THE STREAM CODING TRUTH

```
Messy Docs → Vague Specs → AI Guesses → Rework Cycles → 2-3x Velocity
Clear Docs → Clear Specs → AI Executes → Minimal Rework → 10-20x Velocity
```

**Why Most "AI-Assisted Development" Fails:**
- People feed AI messy docs
- AI generates code based on assumptions
- Code doesn't match intent
- Endless revision cycles
- Result: Marginally faster than manual coding

**Why Stream Coding Achieves 10-20x:**
- Documentation is clarified FIRST
- AI has zero ambiguity
- Code matches intent on first pass
- Minimal revision
- Result: Documentation time + automatic code generation

---

## DOCUMENT TYPE ARCHITECTURE

**The Rule:** Not all documents need all sections. Putting implementation details in strategic documents violates single-source-of-truth.

> "If AI has to decide where to find information, you've already lost velocity."

### Document Types

| Type | Purpose | Examples |
|------|---------|----------|
| **Strategic** | WHAT and WHY | Master Blueprint, PRD, Vision docs, Business cases |
| **Implementation** | HOW | Technical Specs, API docs, Module specs, Architecture docs |
| **Reference** | Lookup | Schema Reference, Glossary, Configuration |

### Section Placement Matrix

| Section | Strategic Docs | Implementation Docs | Reference Docs |
|---------|---------------|---------------------|----------------|
| **Deep Links (References)** | ✅ Required | ✅ Required | ✅ Required |
| **Anti-patterns** | ❌ Pointer only | ✅ Required | ❌ N/A |
| **Test Case Specifications** | ❌ Pointer only | ✅ Required | ❌ N/A |
| **Error Handling Matrix** | ❌ Pointer only | ✅ Required | ❌ N/A |

### Why This Matters

**Wrong (violates single-source-of-truth):**
```
Master Blueprint
├── Strategy content
├── Anti-patterns ← WRONG: duplicates Technical Spec
├── Test Cases ← WRONG: duplicates Testing doc
└── Error Matrix ← WRONG: duplicates Error Handling doc
```

**Right (single-source-of-truth):**
```
Master Blueprint (Strategic)
├── Strategy content
└── References
    └── Pointer: "Anti-patterns → Technical Spec, Section 7"

Technical Spec (Implementation)
├── Implementation details
├── Anti-patterns ← CORRECT: lives here
├── Test Cases ← CORRECT: lives here
└── Error Matrix ← CORRECT: lives here
```

---

## THE 4-PHASE METHODOLOGY

### Time Allocation

| Phase | Time | Focus |
|-------|------|-------|
| Phase 1: Strategic Thinking | 40% | WHAT to build, WHY it matters |
| Phase 2: AI-Ready Documentation | 40% | HOW to build (specs so clear AI has zero decisions) |
| Phase 3: Execution | 15% | Code generation + implementation |
| Phase 4: Quality & Iteration | 5% | Testing, refinement, divergence prevention |

**The Counterintuitive Truth:** 80% of time goes to documentation. 20% to code. This is why velocity is 10-20x—not because coding is faster, but because rework approaches zero.

---

## PHASE 1: STRATEGIC THINKING (40% of time)

### Decision Tree: Where Do You Start?

```
Phase 1: Strategic Product Thinking
│
├─ Have existing documentation?
│   └─ YES → Start with Documentation Audit → then 7 Questions
│
└─ Starting fresh?
    └─ Skip to 7 Questions
```

### Documentation Audit (Conditional)

**Skip this step if starting from scratch.** The Documentation Audit only applies when you have existing documentation—previous specs, inherited docs, or accumulated notes.

**Why clean existing docs?** Because most documentation accumulates cruft:
- Aspirational statements ("We will revolutionize...")
- Speculative futures ("In 2030, we might...")
- Outdated decisions (v1 architecture in v3 docs)
- Duplicate information across files
- Motivational fluff with no implementation value

**The Audit Process:**

Apply the Clarity Test to all existing documentation:

| Check | Question |
|-------|----------|
| **Actionable** | Can AI act on this? If aspirational, delete it. |
| **Current** | Is this still the decision? If changed, update or remove. |
| **Single Source** | Is this said elsewhere? Consolidate to one place. |
| **Decision** | Is this decided? If not, don't include it. |
| **Prompt-Ready** | Would you put this in an AI prompt? If not, delete. |

**Audit Checklist:**
- [ ] Remove all "vision" and "future state" language
- [ ] Delete motivational conclusions and preambles
- [ ] Consolidate duplicate information to single source
- [ ] Update all outdated architectural decisions
- [ ] Remove speculative features not in current scope

**Target:** 40-50% reduction in volume without losing actionable information.

Once clean, proceed to the 7 Questions.

---

### The 7 Questions Framework

Before ANY new documentation, answer these with specificity. Vague answers = vague code.

| # | Question | ❌ Reject | ✅ Require |
|---|----------|-----------|------------|
| 1 | What exact problem are you solving? | "Help users manage tasks" | "Help [specific persona] achieve [measurable outcome] in [specific context]" |
| 2 | What are your success metrics? | "Users save time" | Numbers + timeline: "100 users, 25% conversion, 3 months" |
| 3 | Why will you win? | "Better UI and features" | Structural advantage: architecture, data moat, business model |
| 4 | What's the core architecture decision? | "Let AI decide" | Human decides based on explicit trade-off analysis |
| 5 | What's the tech stack rationale? | "Node.js because I like it" | Business rationale: "Node—team expertise, ship fast" |
| 6 | What are the MVP features? | 10+ "must-have" features | 3-5 truly essential, rest explicitly deferred |
| 7 | What are you NOT building? | "We'll see what users want" | Explicit exclusions with rationale |

### Phase 1 Exit Criteria

- [ ] All 7 questions answered at "Require" level
- [ ] Strategic Blueprint document created
- [ ] Architecture Decision Records (ADRs) for major choices
- [ ] Zero ambiguity about WHAT you're building

---

## PHASE 2: AI-READY DOCUMENTATION (40% of time)

### The 4 Mandatory Sections (Implementation Docs)

Every implementation document MUST include these four sections. Without them, AI guesses—and guessing creates the velocity mirage.

#### 1. Anti-Patterns Section

**Why:** AI needs to know what NOT to do.

```markdown
## Anti-Patterns (DO NOT)

| ❌ Don't | ✅ Do Instead | Why |
|----------|---------------|-----|
| Store timestamps as Date objects | Use ISO 8601 strings | Serialization issues |
| Hardcode configuration values | Use environment variables | Deployment flexibility |
| Use generic error messages | Specific error codes per failure | Debugging impossible otherwise |
| Skip validation on internal calls | Validate everything | Internal calls can have bugs too |
| Expose internal IDs in APIs | Use UUIDs or slugs | Security and flexibility |
```

**Rules:** Minimum 5 anti-patterns per implementation document.

#### 2. Test Case Specifications

**Why:** AI needs concrete verification criteria.

```markdown
## Test Case Specifications

### Unit Tests Required
| Test ID | Component | Input | Expected Output | Edge Cases |
|---------|-----------|-------|-----------------|------------|
| TC-001 | Tier classifier | 100 contacts | 20-30 in Critical tier | Empty list, all same score |
| TC-002 | Score calculator | Activity array | Score 0-100 | No events, >1000 events |

### Integration Tests Required
| Test ID | Flow | Setup | Verification | Teardown |
|---------|------|-------|--------------|----------|
| IT-001 | Auth flow | Create test user | Token refresh works | Delete test user |
```

**Rules:** Minimum 5 unit tests, 3 integration tests per component.

#### 3. Error Handling Matrix

**Why:** AI needs to know how to handle every failure mode.

```markdown
## Error Handling Matrix

### External Service Errors
| Error Type | Detection | Response | Fallback | Logging | Alert |
|------------|-----------|----------|----------|---------|-------|
| API timeout | >5s response | Retry 3x exponential | Return cached | ERROR | If 3 in 5 min |
| Rate limit | 429 response | Pause 15 min | Queue for retry | WARN | If >5/hour |

### User-Facing Errors
| Error Type | User Message | Code | Recovery Action |
|------------|--------------|------|-----------------|
| Quota exceeded | "You've used all checks this month." | 403 | Show upgrade CTA |
| Session expired | "Please sign in again." | 401 | Redirect to login |
```

**Rules:** Every external service and user-facing error must be specified.

#### 4. Deep Links (All Document Types)

**Why:** AI needs to navigate to exact locations. "See Technical Annexes" is useless.

```markdown
## References

### Schema References
| Topic | Location | Anchor |
|-------|----------|--------|
| User profiles | [Schema Reference](../schemas/schema.md#user_profiles) | `user_profiles` |
| Events table | [Schema Reference](../schemas/schema.md#events) | `events` |

### Implementation References
| Topic | Document | Section |
|-------|----------|---------|
| Auth flow | [API Spec](../specs/api.md#authentication) | Section 3.2 |
| Rate limiting | [API Spec](../specs/api.md#rate-limiting) | Section 5 |
```

**Rules:** NEVER use vague references. ALWAYS include document path + section anchor.

---

## ⚠️ THE CLARITY GATE (v3.4 - COMPLETE)

**⛔ NEVER SKIP THIS GATE.**

This is the difference between stream coding and vibe coding. A 7/10 spec generates 7/10 code that needs 30% rework.

### The 13-Item Clarity Gate Checklist

Before ANY code generation, verify ALL items pass:

#### Foundation Checks (7 items)

| # | Check | Question |
|---|-------|----------|
| 1 | **Actionable** | Can AI act on every section? (No aspirational content) |
| 2 | **Current** | Is everything up-to-date? (No outdated decisions) |
| 3 | **Single Source** | No duplicate information across docs? |
| 4 | **Decision, Not Wish** | Every statement is a decision, not a hope? |
| 5 | **Prompt-Ready** | Would you put every section in an AI prompt? |
| 6 | **No Future State** | All "will eventually," "might," "ideally" language removed? |
| 7 | **No Fluff** | All motivational/aspirational content removed? |

#### Document Architecture Checks (6 items - v3.3 Critical)

| # | Check | Question |
|---|-------|----------|
| 8 | **Type Identified** | Document type clearly marked? (Strategic vs Implementation vs Reference) |
| 9 | **Anti-patterns Placed** | Anti-patterns in implementation docs only? (Strategic docs have pointers) |
| 10 | **Test Cases Placed** | Test cases in implementation docs only? (Strategic docs have pointers) |
| 11 | **Error Handling Placed** | Error handling matrix in implementation docs only? |
| 12 | **Deep Links Present** | Deep links in ALL documents? (No vague "see elsewhere") |
| 13 | **No Duplicates** | Strategic docs use pointers, not duplicate content? |

### Gate Enforcement

```
- [ ] All 7 Foundation Checks pass
- [ ] All 6 Document Architecture Checks pass
- [ ] AI Coder Understandability Score ≥ 9/10

If ANY item fails → Fix before proceeding to Phase 3
```

---

## AI CODER UNDERSTANDABILITY SCORING

Use this rubric to score documentation. Target: 9+/10 before Phase 3.

### The 6-Criterion Rubric

| Criterion | Weight | 10/10 Requirement |
|-----------|--------|-------------------|
| **Actionability** | 25% | Every section has Implementation Implication |
| **Specificity** | 20% | All numbers concrete, all thresholds explicit |
| **Consistency** | 15% | Single source of truth, no duplicates across docs |
| **Structure** | 15% | Tables over prose, clear hierarchy, predictable format |
| **Disambiguation** | 15% | Anti-patterns present (5+ per impl doc), edge cases explicit |
| **Reference Clarity** | 10% | Deep links only, no vague references |

### Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 10/10 | AI can implement with zero clarifying questions | Proceed to Phase 3 |
| 9/10 | 1 minor clarification needed | Fix, then proceed |
| 7-8/10 | 3-5 ambiguities exist | Major revision required |
| <7/10 | Not AI-ready, fundamental issues | Return to Phase 2 |

### Self-Assessment Questions

Before Phase 3, ask yourself:

1. **Actionability:** "Does every section tell AI exactly what to do?"
2. **Specificity:** "Are there any numbers I left vague?"
3. **Consistency:** "Is any information stated in more than one place?"
4. **Structure:** "Could I convert any prose paragraphs to tables?"
5. **Disambiguation:** "Have I listed at least 5 anti-patterns per implementation doc?"
6. **Reference Clarity:** "Do any references say 'see elsewhere' without exact location?"

If you answer "no" or "yes" to any question that should be opposite → Fix before proceeding.

---

## AI-ASSISTED CLARITY GATE (Meta-Prompt)

Use this prompt to have Claude score your documentation:

```markdown
**ROLE:** You are the Clarity Gatekeeper. Your job is to ruthlessly 
evaluate software specifications for ambiguity, incompleteness, and 
"vibe coding" tendencies.

**INPUT:** I will provide a technical specification document.

**TASK:** Grade this document on a scale of 1-10 using this rubric:

**RUBRIC:**
1. **Actionability (25%):** Does every section dictate a specific 
   implementation detail? (Reject aspirational like "fast" or 
   "scalable" without metrics)
2. **Specificity (20%):** Are data types, error codes, thresholds, 
   and edge cases explicitly defined? (Reject "handle errors appropriately")
3. **Consistency (15%):** Single source of truth? No duplicates?
4. **Structure (15%):** Tables over prose? Clear hierarchy?
5. **Disambiguation (15%):** Anti-patterns present? Edge cases explicit?
6. **Reference Clarity (10%):** Deep links only? No vague references?

**OUTPUT FORMAT:**
1. **Score:** [X]/10
2. **Criterion Breakdown:** Score each of the 6 criteria
3. **Hallucination Risks:** List specific lines where an AI developer 
   would have to guess or make an assumption
4. **The Fix:** Rewrite the 3 most ambiguous sections into AI-ready specs

**THRESHOLD:** 
- 9-10: Ready for code generation
- 7-8: Needs revision before proceeding
- <7: Return to Phase 2
```

---

## PHASE 3: EXECUTION (15% of time)

### The Generate-Verify-Integrate Loop

```
1. GENERATE: Feed spec to AI → Receive code
2. VERIFY: Run tests → Check against spec
   - Does output match spec exactly?
   - Yes → Continue
   - No → Fix SPEC first, then regenerate
3. INTEGRATE: Commit → Update documentation if needed
```

### The Golden Rule of Phase 3

> **"When code fails, fix the spec—not the code."**

If generated code doesn't work:
1. ❌ Don't patch the code manually
2. ✅ Ask: "What was unclear in my spec?"
3. ✅ Fix the spec
4. ✅ Regenerate

**Why:** Manual code patches create divergence between spec and reality. Divergence compounds. Eventually your spec is fiction and you're back to manual development.

---

## PHASE 4: QUALITY & ITERATION (5% of time)

### The Rule of Divergence

> **Every time you manually edit AI-generated code without updating the spec, you create Divergence. Divergence is technical debt.**

**Why Divergence is Dangerous:**
- If you fix a bug in code but not spec, you can never regenerate that module
- Future AI iterations will reintroduce the bug
- You've broken the stream

### Preventing Divergence

| Scenario | ❌ Wrong | ✅ Right |
|----------|----------|----------|
| Bug in generated code | Fix code manually | Fix spec, regenerate |
| Missing edge case | Add code patch | Add to spec, regenerate |
| Performance issue | Optimize code | Document constraint, regenerate |
| "Quick fix" needed | "Just this once..." | No. Fix spec. |

### The "Day 2" Workflow

1. **Isolate the Module:** Target the specific module, not the whole app
2. **Update the Spec:** Add the new edge case, requirement, or fix
3. **Regenerate the Module:** Feed updated spec to AI
4. **Verify Integration:** Run test suite for regressions

This takes 5 minutes longer than a quick hotfix. But it ensures your documentation never drifts from reality.

---

## TRIGGER BEHAVIOR

This methodology activates when the user says:
- "Build [feature]" → Full methodology (Phases 1-4)
- "Create [component]" → Full methodology
- "Implement [system]" → Check: Do clear docs exist?
- "Document [project]" → Phases 1-2 only
- "Spec out [feature]" → Phases 1-2 only
- "Clean up docs for [X]" → Documentation Audit only

### Response Protocol

1. **Check for existing docs:** "Do you have existing documentation for this project?"
2. **If existing docs:** "Let's start with a Documentation Audit to clean them before building."
3. **If Phase 1 incomplete:** "Before building, let's clarify strategy. [Ask 7 Questions]"
4. **If Phase 2 incomplete:** "Before coding, let's ensure documentation is AI-ready. [Run Clarity Gate]"
5. **If Clarity Gate not passed:** "Documentation scores [X]/10. Let's fix [specific issues] before proceeding."
6. **If Phase 3 ready:** "Documentation passes Clarity Gate (9+/10). Generating implementation..."
7. **If maintaining (Phase 4):** "Is this change spec-conformant? Let's update docs first."

---

## THE STREAM CODING CONTRACT

### YOU MUST:

**Documentation Audit (if existing docs):**
- [ ] Run Clarity Test on all existing documentation
- [ ] Remove aspirational/future state language
- [ ] Consolidate duplicates to single source
- [ ] Target 40-50% reduction without losing actionable content

**Phase 1:**
- [ ] Answer all 7 questions at "Require" level
- [ ] Create Strategic Blueprint with Implementation Implications
- [ ] Write ADRs for major architectural decisions

**Phase 2:**
- [ ] Identify document type (Strategic vs Implementation vs Reference)
- [ ] Add 4 mandatory sections to each implementation doc
- [ ] Add deep links to ALL documents
- [ ] Use pointers (not duplicates) in strategic docs

**Clarity Gate:**
- [ ] Pass all 13 checklist items
- [ ] Score 9+/10 on AI Coder Understandability
- [ ] Answer all 6 self-assessment questions correctly

**Phase 3-4:**
- [ ] Show code before creating files
- [ ] Run quality gates (lint, type, test)
- [ ] When code fails: fix spec, regenerate
- [ ] Never create divergence (update spec with every code change)

### YOU CANNOT:

- ❌ Build on existing docs without running Documentation Audit first
- ❌ Skip to coding without clear docs
- ❌ Accept vague specs ("handle errors appropriately")
- ❌ Skip Clarity Gate (even if you wrote the docs yourself)
- ❌ Put Anti-patterns/Test Cases/Error Handling in strategic docs
- ❌ Use vague references ("see Technical Annexes")
- ❌ Duplicate content across document types
- ❌ Iterate on code when problem is in spec
- ❌ Edit code without updating spec (creates Divergence)

---

## DOCUMENT TEMPLATES

### Strategic Document Template

```markdown
# [Document Title] (Strategic)

## 1. [Strategic Section]
[Strategic content]

**Implementation Implication:** [Concrete effect on code/architecture]

## 2. [Another Section]
[Strategic content]

**Implementation Implication:** [Concrete effect on code/architecture]

## N. REFERENCES

### Implementation Details Location
| Content Type | Location |
|--------------|----------|
| Anti-patterns | [Technical Spec, Section 7](path#anchor) |
| Test Cases | [Testing Doc, Section 3](path#anchor) |
| Error Handling | [Error Handling Doc](path#anchor) |

### Schema References
| Topic | Location | Anchor |
|-------|----------|--------|
| [Topic] | [Path](path#anchor) | `anchor` |

*This document provides strategic overview. Technical documents provide implementation specifications.*
```

### Implementation Document Template

```markdown
# [Document Title] (Implementation)

## 1. [Implementation Section]
[Technical details]

## N-3. ANTI-PATTERNS (DO NOT)

| ❌ Don't | ✅ Do Instead | Why |
|----------|---------------|-----|
| [Anti-pattern] | [Correct approach] | [Reason] |

## N-2. TEST CASE SPECIFICATIONS

### Unit Tests
| Test ID | Component | Input | Expected Output | Edge Cases |
|---------|-----------|-------|-----------------|------------|
| TC-XXX | [Component] | [Input] | [Output] | [Edge cases] |

### Integration Tests
| Test ID | Flow | Setup | Verification | Teardown |
|---------|------|-------|--------------|----------|
| IT-XXX | [Flow] | [Setup] | [Verify] | [Cleanup] |

## N-1. ERROR HANDLING MATRIX

| Error Type | Detection | Response | Fallback | Logging |
|------------|-----------|----------|----------|---------|
| [Error] | [How detected] | [Response] | [Fallback] | [Level] |

## N. REFERENCES

| Topic | Location | Anchor |
|-------|----------|--------|
| [Topic] | [Path](path#anchor) | `anchor` |
```

---

## QUICK REFERENCE

### The 13-Item Clarity Gate

**Foundation (7):**
1. Actionable? 2. Current? 3. Single source? 4. Decision not wish?
5. Prompt-ready? 6. No future state? 7. No fluff?

**Architecture (6):**
8. Type identified? 9. Anti-patterns placed correctly? 10. Test cases placed correctly?
11. Error handling placed correctly? 12. Deep links present? 13. No duplicates?

### The Scoring Rubric

| Criterion | Weight |
|-----------|--------|
| Actionability | 25% |
| Specificity | 20% |
| Consistency | 15% |
| Structure | 15% |
| Disambiguation | 15% |
| Reference Clarity | 10% |

### Time Allocation

```
┌─────────────────────────────────────────────────────────────┐
│ Have existing docs? → Documentation Audit (conditional)     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1 (Strategy): 40% ──┐                                │
│  Phase 2 (Specs): 40% ─────┼── 80% Documentation            │
│                            │                                │
│  ⚠️ CLARITY GATE ──────────┘                                │
│                            │                                │
│  Phase 3 (Code): 15% ──────┼── 20% Code                     │
│  Phase 4 (Quality): 5% ────┘                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Core Mantras

1. "Documentation IS the work. Code is just the printout."
2. "When code fails, fix the spec—not the code."
3. "A 7/10 spec generates 7/10 code that needs 30% rework."
4. "If AI has to decide where to find information, you've already lost velocity."

---

**Version:** 3.4
**Changes from 3.3.1:**
- Complete 13-item Clarity Gate (was 5 items)
- Scoring rubric with 6 weighted criteria
- Self-assessment questions before Phase 3
- AI-assisted scoring meta-prompt included
- 4 mandatory section templates with examples
- Phase 1 questions with reject/require examples
- Documentation Audit integrated into Phase 1 (replaces "Phase 0")

**Core Insight:** The Clarity Gate is the methodology. Everything else supports getting docs to 9+/10.

---

*Stream Coding by Francesco Marinoni Moretto — CC BY 4.0*
*github.com/frmoretto/stream-coding*

**END OF STREAM CODING v3.4**
