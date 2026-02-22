---
name: problem-based-srs
description: Complete Problem-Based Software Requirements Specification methodology following Gorski & Stadzisz research. Use when you need to perform requirements engineering from business problems to functional requirements with full traceability.
license: MIT
metadata:
  author: rafael-gorski
  version: "1.2"
  methodology: problem-based-srs
---

# Problem-Based SRS

Orchestrate requirements engineering using the Problem-Based SRS methodology (Gorski & Stadzisz). This skill coordinates a 5-step process that ensures every requirement traces back to a real business problem.

## Methodology Overview

```
Business Context
       ↓
┌──────────────────┐
│ Step 1: CP       │ → See references/step1-customer-problems.md
│ Customer Problems│
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Step 2: SG       │ → See references/step2-software-glance.md
│ Software Glance  │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Step 3: CN       │ → See references/step3-customer-needs.md
│ Customer Needs   │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Step 4: SV       │ → See references/step4-software-vision.md
│ Software Vision  │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Step 5: FR/NFR   │ → See references/step5-functional-requirements.md
│ Requirements     │
└──────────────────┘
```

**Traceability Chain:** FR → CN → CP (every requirement traces back to a problem)

**Domain Mapping (WHY → WHAT → HOW):**
| Domain | Artifact | Question Answered |
|--------|----------|-------------------|
| **WHY** | Customer Problems (CP) | Why is the solution needed? (Business justification) |
| **WHAT** | Customer Needs (CN) | What outcomes must the software provide? |
| **HOW** | Functional Requirements (FR) | How will the system behave? |

## 📁 Saving Progress (CRITICAL)

**IMPORTANT:** At each step, you MUST save the produced artifacts to files. Progress is NOT automatically saved between sessions.

### First Time Setup

When starting a new project, ask the user:

```
Before we begin, where would you like to save your SRS artifacts?

Options:
1. `docs/srs/` (recommended - keeps SRS separate from code docs)
2. `requirements/` (alternative - at project root)
3. Custom path: [specify your preferred location]

All artifacts will be saved in this folder with consistent naming.
```

### Artifact File Structure

Create the following folder structure as you progress through each step:

```
[chosen-folder]/                      # e.g., docs/srs/
├── 00-context.md                     # Business context and project overview
├── 01-customer-problems.md           # Step 1: CPs (WHY)
├── 02-software-glance.md             # Step 2: High-level solution view
├── 03-customer-needs.md              # Step 3: CNs (WHAT)
├── 04-software-vision.md             # Step 4: Architecture and scope
├── functional-requirements/          # Step 5: Individual FR files
│   ├── _index.md                     # FR summary and traceability matrix
│   ├── FR-001.md                     # Individual FR file
│   ├── FR-002.md                     # Individual FR file
│   └── ...                           # One file per FR
├── non-functional-requirements/      # NFR files (quality attributes)
│   ├── _index.md                     # NFR summary
│   ├── NFR-001.md                    # Individual NFR file
│   └── ...                           # One file per NFR
└── traceability-matrix.md            # CP → CN → FR complete mapping
```

### Why Individual FR/NFR Files?

Each Functional Requirement and Non-Functional Requirement is saved as a **separate file** so that:

1. **Engineers can work independently** on different requirements
2. **Version control** tracks changes to individual requirements
3. **Code reviews** can focus on specific requirements
4. **Traceability** is maintained at the file level
5. **Status tracking** is easier (draft, approved, implemented, tested)

### FR File Template (FR-XXX.md)

Each FR file follows this template:

```markdown
# FR-XXX: [Brief Title]

## Requirement

**Statement:** The [System] shall [verb] [object] [constraint] [condition].

**Priority:** [Must Have | Should Have | Could Have | Won't Have]
**Status:** [Draft | Review | Approved | Implemented | Tested]

## Traceability

| Traces To | ID | Description |
|-----------|-----|-------------|
| Customer Need | CN-XXX | [Brief CN description] |
| Customer Problem | CP-XXX | [Brief CP description] |

## Acceptance Criteria

- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (testable)

## Notes

[Any additional context, assumptions, or dependencies]

<!-- ⚠️ NO CODE SNIPPETS: Do not include code examples, SQL, or implementation details here.
     Construction details belong in design/ folder (see design/implementation-notes/) -->

---
*Created: [Date]*
*Last Updated: [Date]*
*Author: [Name]*
```

### NFR File Template (NFR-XXX.md)

```markdown
# NFR-XXX: [Brief Title]

## Requirement

**Category:** [Performance | Security | Usability | Reliability | Scalability | Maintainability]
**Statement:** The [System] shall [quality attribute with measurable criteria].

**Priority:** [Must Have | Should Have | Could Have | Won't Have]
**Status:** [Draft | Review | Approved | Implemented | Tested]

## Traceability

| Traces To | ID | Description |
|-----------|-----|-------------|
| Customer Need | CN-XXX | [Brief CN description] |
| Applies To FRs | FR-XXX, FR-YYY | [Related functional requirements] |

## Acceptance Criteria

- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (measurable)

## Measurement Method

[How this NFR will be verified/tested]

<!-- ⚠️ NO CODE SNIPPETS: Do not include code examples or implementation details here.
     Technical specifications belong in design/ folder -->

---
*Created: [Date]*
*Last Updated: [Date]*
```

### Save After Each Step

**After completing each step, ALWAYS:**

1. **Create or update** the corresponding file(s)
2. **Confirm with user** that files were saved
3. **Show the file paths** for reference

Example handoff for Step 5:

```
✅ Step 5 Complete: Functional Requirements Specified

📁 Saved to: docs/srs/functional-requirements/
   ├── _index.md (summary with 8 FRs)
   ├── FR-001.md → CN-001 (User Registration)
   ├── FR-002.md → CN-001 (User Authentication)
   ├── FR-003.md → CN-002 (Data Validation)
   ├── FR-004.md → CN-002 (Error Handling)
   ├── FR-005.md → CN-003 (Report Generation)
   ├── FR-006.md → CN-003 (Export Functionality)
   ├── FR-007.md → CN-004 (Search Capability)
   └── FR-008.md → CN-004 (Filter Options)

📁 Updated: docs/srs/traceability-matrix.md

Engineers can now work on individual requirements independently.
Each FR file contains full context and acceptance criteria.
```

### Context File (00-context.md)

Create this file at the start of every project:

```markdown
# Project Context: [Project Name]

## Business Domain
[Description of the business area]

## Current Situation
[Description of current state/problems]

## Stakeholders
| Role | Name/Group | Interest |
|------|------------|----------|
| [Role] | [Who] | [What they care about] |

## Scope
- **In Scope:** [What's included]
- **Out of Scope:** [What's excluded]

## Constraints
- [Constraint 1]
- [Constraint 2]

---
*Created: [Date]*
*Last Updated: [Date]*
```

## How to Use This Skill

### Starting Fresh
When user provides business context or problem description:
1. **Ask where to save artifacts** (if not already specified)
2. **Create 00-context.md** with the business context
3. Detect current step (see Detection Heuristics below)
4. Load the appropriate reference file
5. Follow instructions from that reference
6. **Save output to the corresponding file(s)**
7. Guide user through the process

### Continuing Work
If user has existing artifacts (CPs, CNs, etc.):
1. **Check for existing SRS folder** (docs/srs/, requirements/, etc.)
2. **Read existing files** to understand current state
3. Identify what they have
4. Jump to appropriate step
5. Load that step's reference file
6. Continue from there, **updating files as needed**

### Validation
At any point, use references/zigzag-validator.md to check consistency.

## Detection Heuristics

Determine current step by checking what artifacts exist:

| If user has... | Current Step | Load Reference | Save To |
|----------------|--------------|----------------|---------|
| Nothing / business idea only | 1 | step1-customer-problems.md | 01-customer-problems.md |
| Customer Problems (CPs) | 2 | step2-software-glance.md | 02-software-glance.md |
| CPs + Software Glance | 3 | step3-customer-needs.md | 03-customer-needs.md |
| CPs + CNs + Software Glance | 4 | step4-software-vision.md | 04-software-vision.md |
| CPs + CNs + Software Vision | 5 | step5-functional-requirements.md | functional-requirements/*.md |

## The 5 Steps (Quick Reference)

### Step 1: Customer Problems (CP)
**Purpose:** Identify and document business problems  
**Input:** Business context  
**Output:** List of CPs classified as Obligation/Expectation/Hope  
**Syntax:** `[Subject] [must/expects/hopes] [Object] [Penalty]`  
**Save to:** `01-customer-problems.md`  
**Details:** See [step1-customer-problems.md](references/step1-customer-problems.md)

### Step 2: Software Glance (SG)
**Purpose:** Create initial abstract solution view  
**Input:** Customer Problems  
**Output:** High-level system description with boundaries and components  
**Save to:** `02-software-glance.md`  
**Details:** See [step2-software-glance.md](references/step2-software-glance.md)

### Step 3: Customer Needs (CN)
**Purpose:** Specify outcomes software must provide  
**Input:** CPs + Software Glance  
**Output:** CNs with outcome classes (Information/Control/Construction/Entertainment)  
**Syntax:** `[Subject] needs [system] to [Verb] [Object] [Condition]`  
**Save to:** `03-customer-needs.md`  
**Details:** See [step3-customer-needs.md](references/step3-customer-needs.md)

### Step 4: Software Vision (SV)
**Purpose:** Define high-level scope and positioning  
**Input:** CNs + Software Glance  
**Output:** Vision document with stakeholders, features, architecture  
**Save to:** `04-software-vision.md`  
**Details:** See [step4-software-vision.md](references/step4-software-vision.md)

### Step 5: Functional Requirements (FR) & Non-Functional Requirements (NFR)
**Purpose:** Generate detailed requirements  
**Input:** CNs + Software Vision  
**Output:** Individual FR and NFR files with traceability  
**Syntax FR:** `The [System] shall [Verb] [Object] [Constraint] [Condition]`  
**Save to:** `functional-requirements/FR-XXX.md` and `non-functional-requirements/NFR-XXX.md`  
**Details:** See [step5-functional-requirements.md](references/step5-functional-requirements.md)

## Quality Gates

**IMPORTANT:** Zigzag validation using [references/zigzag-validator.md](references/zigzag-validator.md) is **MANDATORY** after Steps 3 and 5 to verify traceability and identify gaps.

### After Step 1 (CPs)
- [ ] All CPs use structured notation
- [ ] Classifications assigned (Obligation/Expectation/Hope)
- [ ] No solutions embedded in problem statements
- [ ] **File saved:** `01-customer-problems.md`

### After Step 2 (SG)
- [ ] System boundaries defined
- [ ] Main actors and interfaces identified
- [ ] High-level components described
- [ ] **File saved:** `02-software-glance.md`

### After Step 3 (CNs)
- [ ] Every CP has at least one CN
- [ ] All CNs use structured notation
- [ ] Outcome classes assigned
- [ ] **File saved:** `03-customer-needs.md`
- [ ] **MANDATORY: Run zigzag validation** (CP → CN mapping)

### After Step 4 (SV)
- [ ] Positioning statement clear
- [ ] All stakeholders identified
- [ ] Major features listed
- [ ] **File saved:** `04-software-vision.md`

### After Step 5 (FRs/NFRs)
- [ ] Every CN has at least one FR
- [ ] All FRs use "shall" or "should"
- [ ] Each FR saved as individual file in `functional-requirements/`
- [ ] Each NFR saved as individual file in `non-functional-requirements/`
- [ ] Index files created (`_index.md`)
- [ ] Traceability matrix complete (FR → CN → CP)
- [ ] No code snippets or programming examples in FR/NFR files
- [ ] Construction details in separate `design/` folder (not in FR/NFR files)
- [ ] **File saved:** `traceability-matrix.md`
- [ ] **MANDATORY: Run zigzag validation** (full chain verification)

## Problem-First Enforcement

If user attempts to skip to solutions, redirect:

**Detect:** User mentions specific technology, feature, or implementation before CPs exist

**Redirect:**
```
I notice you're describing a solution. Let's first understand the problem.

Before we design [mentioned solution], help me understand:
1. What business obligation, expectation, or hope drives this need?
2. What negative consequences occur without this?
3. Who is impacted?

→ Loading: references/step1-customer-problems.md
```

## Quick Syntax Reference

| Artifact | Syntax Pattern |
|----------|----------------|
| **CP** | [Subject] [must/expects/hopes] [Object] [Penalty] |
| **CN** | [Subject] needs [system] to [Verb] [Object] [Condition] |
| **FR** | The [System] shall [Verb] [Object] [Constraint] [Condition] |
| **NFR** | The [System] shall [quality attribute with measurable criteria] |

## Handoff Protocol

When completing each step:

1. **Save** outputs to the appropriate file(s)
2. **Summary** of outputs produced
3. **Validation** that gate criteria are met
4. **Next step** recommendation
5. **Required inputs** for next step

Example:
```
✅ Step 3 Complete: Customer Needs Specified

📁 Saved to: docs/srs/03-customer-needs.md

Outputs:
- CN-001: [Information] User needs system to display...
- CN-002: [Control] Admin needs system to manage...
- CN-003: [Information] Manager needs system to report...

Gate Check:
- [x] All CNs use structured notation
- [x] Outcome classes assigned
- [x] Every CP has at least one CN
- [x] File saved

→ Next: Step 4 - Software Vision
→ Loading: references/step4-software-vision.md
→ Will save to: docs/srs/04-software-vision.md
→ Input: The CNs documented above
```

## Usage Patterns

### Pattern 1: Full Process (New Project)
Start with Step 1 and progress through all 5 steps sequentially.
**Remember:** Ask where to save files, create context file first.

### Pattern 2: Jump In (Existing Artifacts)
Detect what artifacts exist, skip completed steps, resume at current step.
**Remember:** Check for existing SRS folder and read current files.

### Pattern 3: Iterative Refinement
Complete initial pass, then iterate on specific steps as understanding improves.
**Remember:** Update existing files rather than creating new ones.

### Pattern 4: Validation Only
Use zigzag-validator.md to check existing artifacts without generating new ones.

### Pattern 5: Independent Development
After Step 5, engineers can pick up individual FR files and develop independently.
Each FR file contains all context needed (traceability, acceptance criteria).

### Pattern 6: Agile/Sprint Integration
Use Problem-Based SRS iteratively within agile workflows:
- **Sprint 0:** Steps 1-2 (CPs + Software Glance) for product vision
- **Sprint 1+:** Steps 3-5 for specific feature sets
- **Per Feature:** Complete CP→CN→FR chain for one feature at a time
- **Validation:** Run zigzag after each sprint to ensure traceability

### Pattern 7: Minimal Viable SRS
For quick prototypes or MVPs:
1. Identify 2-3 core CPs (Obligations only)
2. Create minimal Software Glance
3. Derive essential CNs
4. Generate only critical FRs
5. Skip detailed validation until expansion

## When to Load Each Reference

- **Step 1 (CP):** User has business context but no structured problems
- **Step 2 (SG):** User has CPs and needs high-level solution view
- **Step 3 (CN):** User has CPs + SG and needs to specify outcomes
- **Step 4 (SV):** User has CNs and needs detailed vision document
- **Step 5 (FR/NFR):** User has CNs + SV and needs functional requirements
- **Validation:** User needs to check traceability or consistency
- **Complexity (Optional):** User explicitly requests Axiomatic Design analysis

## Optional: Complexity Analysis

For deeper quality analysis, users can explicitly invoke:
- **Reference:** [complexity-analysis.md](references/complexity-analysis.md)
- **Purpose:** Axiomatic Design-based specification quality analysis
- **When to use:** Critical systems, large specifications, formal reviews

This is **NOT** part of the standard flow. It provides:
- Independence analysis (coupled vs. uncoupled specifications)
- Completeness levels (C/P markers for traceability)
- Information content assessment

## Examples

For complete walkthroughs, see:
- [CRM Example](references/crm-example.md) — Business domain (Customer Relationship Management)
- [MicroER Example](references/microer-example.md) — Technical domain (Renewable Energy System)

**Always load only one reference at a time** based on current step to minimize context usage.