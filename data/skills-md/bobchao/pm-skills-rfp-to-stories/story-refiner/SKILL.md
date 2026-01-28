---
name: "Story Refiner"
description: "Evaluates User Story quality and automatically corrects items not meeting standards. Reviews from developer, QA, and stakeholder perspectives, directly producing improved versions for low-quality Stories, reducing manual intervention."
---

# Story Refiner Skill

## Language Preference

**Default**: Respond in the same language as the user's input or as explicitly requested by the user.

If the user specifies a preferred language (e.g., "請用中文回答", "Reply in Japanese"), use that language for all outputs. Otherwise, match the language of the provided Stories.

---

## Role Definition

You simultaneously play three roles to review User Stories:

1. **Senior Developer**: Evaluates technical feasibility and estimation clarity
2. **QA Engineer**: Evaluates testability and acceptance criteria clarity
3. **Product Stakeholder**: Evaluates requirement coverage and value clarity

## Core Principles

### Correction Over Reporting

- **Don't just point out problems, directly fix them**
- Every flagged issue must have a corresponding improved version
- Humans only need final confirmation, not manual correction

### Conservative Correction

- Only correct Stories with "obvious problems"
- Don't correct for the sake of correcting
- Stories that already pass don't need changes

### Transparent Annotation

- Clearly explain why corrections were made
- Provide original vs. improved version comparison
- Let humans choose to accept or keep original version

---

## Input Format

This Skill accepts the following inputs:

1. **Story Writer output** (recommended)
2. **Any format User Stories list**
3. **Original RFP + Stories** (can cross-reference coverage)

---

## Evaluation Criteria Reference

**All scoring and evaluation must follow the standards defined in `references/evaluation-criteria.md`.**

This document defines:
- Three scoring dimensions (Development Clarity, Testability, Value Clarity)
- Detailed scoring criteria for each dimension (1-5 points)
- Specific checkpoints and common deduction patterns
- Final score calculation method

**Important**: Both Quick Scan (Phase 1) and Detailed Evaluation (Phase 2) use these same criteria, with different levels of depth.

---

## Evaluation Flow

### Phase 1: Quick Scan

Score each Story initially (1-5 points) using the three dimensions from `references/evaluation-criteria.md`:

**Scoring Method**:
1. Quickly assess each dimension (Development Clarity, Testability, Value Clarity) on a 1-5 scale
2. Calculate final score: `round((Development Clarity + Testability + Value Clarity) / 3)`
3. Use the scoring criteria tables in `references/evaluation-criteria.md` as reference

**Quick Assessment Focus**:
- Development Clarity: Is action specific? Scope clear? Dependencies clear?
- Testability: Can write test cases? Acceptance criteria present? Value verifiable?
- Value Clarity: Value clear? Role correct? Maps to requirements?

| Score | Level | Action |
|-------|-------|--------|
| 5 | Excellent | Keep, no modification |
| 4 | Good | Keep, may have minor suggestions |
| 3 | Passing | Mark for observation, may need minor adjustments |
| 2 | Insufficient | **Must correct** |
| 1 | Severely insufficient | **Must rewrite** |

Only Stories scoring ≤ 3 enter Phase 2 detailed evaluation.

### Phase 2: Multi-Perspective Detailed Evaluation

For Stories needing review, perform detailed evaluation from three perspectives using the **Specific Checkpoints** and **Common Deduction Patterns** defined in `references/evaluation-criteria.md`.

#### 👨‍💻 Developer Perspective

**Reference**: `references/evaluation-criteria.md` - Dimension 1: Development Clarity

**Detailed Checkpoints** (from evaluation-criteria.md):
- [ ] Is action description specific?
  - 5 points: "Upload JPG/PNG format images, limited to 5MB"
  - 3 points: "Upload images"
  - 1 point: "Handle images"
- [ ] Does scope have boundaries?
  - 5 points: "Edit article title and content"
  - 3 points: "Edit article"
  - 1 point: "Manage articles"
- [ ] Are dependencies clear?
  - 5 points: Clearly marked "requires US-001 login feature completed first"
  - 3 points: Implied dependency but not marked
  - 1 point: Confusing or circular dependencies

**Common Problems** (see evaluation-criteria.md for deduction patterns):
- Vague verbs: "manage", "handle", "maintain" (-1~2 points)
- No scope boundary: "all settings", "various reports" (-1~2 points)
- Compound features: "create and edit" (-1 point)
- Technical details mixed in: "load using AJAX" (-1 point)

#### 🧪 QA Perspective

**Reference**: `references/evaluation-criteria.md` - Dimension 2: Testability

**Detailed Checkpoints** (from evaluation-criteria.md):
- [ ] Are acceptance criteria clear?
  - 5 points: Has specific Given-When-Then or checklist
  - 3 points: Has general direction but not specific
  - 1 point: No acceptance criteria, or vague like "should be user-friendly"
- [ ] Is value verifiable?
  - 5 points: "so that I can find target article within 3 seconds" (measurable)
  - 3 points: "so that I can find articles faster" (relative but comparable)
  - 1 point: "so that I can have a better experience" (not measurable)
- [ ] Are error scenarios considered?
  - 5 points: Clearly states error handling
  - 3 points: Only happy path, but error handling can be inferred
  - 1 point: Error scenarios completely unconsidered, and important to feature

**Common Problems** (see evaluation-criteria.md for deduction patterns):
- No acceptance criteria: None at all (-1~2 points, important features deduct more)
- Vague criteria: "should be fast", "should look good" (-1 point)
- Untestable value: "so that I can have better experience" (-2 points)

#### 👤 Stakeholder Perspective

**Reference**: `references/evaluation-criteria.md` - Dimension 3: Value Clarity

**Detailed Checkpoints** (from evaluation-criteria.md):
- [ ] Does "so that..." state real value?
  - 5 points: "so that I can pull up data within 10 seconds when customer calls"
  - 3 points: "so that I can quickly view data"
  - 1 point: "so that I can use this feature" (circular reasoning)
- [ ] Is role correct?
  - 5 points: Role is clear and is the true beneficiary of this feature
  - 3 points: Role too generic (e.g., "user" covers too much)
  - 1 point: Wrong role (e.g., giving admin feature to regular user)
- [ ] Maps to original requirements?
  - 5 points: Can directly trace to a specific RFP paragraph
  - 3 points: Is reasonably derived implied requirement
  - 1 point: Can't see connection to original requirements

**Common Problems** (see evaluation-criteria.md for deduction patterns):
- Circular reasoning: "so that I can use this feature" (-2 points)
- Role too generic: Everything is "user" (-1 point)
- Technical task disguised: "As a developer" (-3 points)
- Deviates from original requirements: Features RFP didn't mention (-1~2 points)

### Phase 3: Auto-Correction

For Stories scoring ≤ 3, execute corrections based on problem type:

#### Correction Strategies

| Problem Type | Correction Method |
|--------------|-------------------|
| Scope too large | Split into multiple Stories |
| Scope vague | Add specific operation description |
| Value unclear | Rewrite "so that..." part |
| Not testable | Add specific acceptance criteria |
| Format issue | Adjust to standard format |
| Wrong role | Correct to proper role |
| Improper granularity | Split or merge |

#### Correction Principles

1. **Minimum change**: If small change works, don't make big changes
2. **Preserve intent**: Don't change original requirement intent
3. **Clear annotation**: Explain what was changed and why

### Phase 4: Iterative Validation (Max 3 Rounds)

Corrected Stories need re-evaluation to ensure quality meets standards. This is the core of iterative refinement.

#### Why Iteration Is Needed

| Situation | Single-Pass Refinement Problem | Iterative Solution |
|-----------|-------------------------------|-------------------|
| Story is split | New Stories aren't evaluated | ✅ Next round evaluates new Stories |
| Over-correction | Might break something | ✅ Next round catches and fine-tunes |
| Acceptance criteria still not specific | Passes through | ✅ Next round strengthens |

#### Iteration Flow

```
Round 1: Evaluate all Stories → Correct low-scoring items → Produce corrected version
    ↓
Round 2: Evaluate "corrected" + "newly generated" Stories → Correct again if needed
    ↓
Round 3: (If still issues) Final fine-tuning
    ↓
Terminate: Output final version
```

#### Termination Conditions (Stop when any is met)

1. **Quality achieved**: All Stories score ≥ 4
2. **No corrections needed**: This round had no Story corrections
3. **Limit reached**: Already executed 3 rounds
4. **Convergence failed**: Same Story corrected 2 rounds in a row but score didn't improve

#### Iteration Rules

| Rule | Description |
|------|-------------|
| **Progressive convergence** | Each round should reduce problems, not increase them |
| **History memory** | Track each Story's correction history, avoid back-and-forth changes |
| **Correction limit** | Same Story can only be majorly changed once, then only fine-tuned |
| **New Story priority** | From round 2, prioritize evaluating Stories generated in previous round |

#### Decreasing Correction Intensity

| Round | Allowed Correction Types |
|-------|-------------------------|
| Round 1 | All corrections (split, rewrite, add acceptance criteria, etc.) |
| Round 2 | Moderate corrections (add acceptance criteria, adjust wording, minor splits) |
| Round 3 | Fine-tuning only (word corrections, add details, no splitting or rewriting) |

This design ensures:
- Round 1 solves structural problems
- Round 2 handles omissions and fine-tuning
- Round 3 is just wrap-up, avoiding infinite modification

#### Iteration Summary Output

Record at end of each round:

```markdown
### Round N Refinement Summary

| Metric | Value |
|--------|-------|
| Stories Evaluated | XX |
| Corrections Made | XX |
| New (from splits) | XX |
| Average Score Improvement | +X.X |

**This Round's Corrections**:
- US-XXX: [Correction summary]
- US-XXX: [Correction summary]

**Continue?**: [Yes/No, reason]
```

---

## Output Format

### Structure Overview

```markdown
# Story Refinement Report

## 📊 Refinement Summary

### Overall Results
- Original Story Count: XX
- Final Story Count: XX (including split additions)
- Refinement Rounds: X / 3
- Termination Reason: [Quality achieved / No corrections needed / Limit reached]

### Per-Round Statistics
| Round | Evaluated | Corrected | Added | Average Score |
|-------|-----------|-----------|-------|---------------|
| Round 1 | XX | XX | XX | X.X |
| Round 2 | XX | XX | XX | X.X |
| ... | ... | ... | ... | ... |

## 🔄 Refinement History
[Per-round correction summaries, collapsible]

## ✅ Final Passing Stories
[Stories scoring ≥ 4]

## 🔧 Corrected Stories
[Original → Final version comparison, noting correction round]

## ➕ Split-Generated Stories
[New Stories from splits]

## 🗑️ Recommended for Removal
[Stories not matching requirements or duplicates]

## 📋 Final Story List
[Complete integrated list, ready for use]
```

### Correction Detail Format

```markdown
### 🔧 US-XXX: [Title]

**Original Version**:
> As a [role], I want [action], so that [value].

**Problem Diagnosis**:
- 🧪 QA Perspective: Acceptance criteria unclear, can't write tests
- 👨‍💻 Developer Perspective: Scope includes multiple independent features

**Correction Method**: Split into two Stories + add acceptance criteria

**Improved Version**:

**US-XXX-A**: As a [role], I want [action A], so that [value].
- Acceptance Criteria:
  - [ ] Condition 1
  - [ ] Condition 2

**US-XXX-B**: As a [role], I want [action B], so that [value].
- Acceptance Criteria:
  - [ ] Condition 1

---
```

---

## Special Situation Handling

### Situation 1: Large Number of Stories Need Correction (>50%)

This may indicate systematic issues in Story Writer phase:

1. Don't correct one by one (too inefficient)
2. Identify common problem patterns
3. Propose systematic suggestions
4. Recommend re-running Story Writer

### Situation 2: Discovered Missing Features

If comparing to RFP reveals features not covered by Stories:

1. Mark as "recommended addition"
2. Produce suggested Story
3. Mark source (derived from which part of RFP)

### Situation 3: Discovered Duplicate Stories

1. Mark duplicate items
2. Recommend which to keep (or merge)
3. Explain judgment basis

### Situation 4: Story Quality Is Excellent

If all Stories score ≥ 4:

1. Briefly confirm "Quality is good, no corrections needed"
2. Can provide minor optimization suggestions (not mandatory)
3. Directly output final list

---

## Output Example

Refer to `assets/refine-example.md` for complete output example.

---

## Reference Documents

- **Evaluation Criteria**: `references/evaluation-criteria.md` - Defines detailed scoring standards for all three dimensions
- **Output Example**: `assets/refine-example.md` - Complete refinement report example

---

## Integration with Other Skills

### Standard Flow

```
[rfp-analyzer] → [story-writer] → [story-refiner] → Final output
```

**Usage**: After Story Writer produces User Stories draft, use Story Refiner to evaluate quality and automatically correct low-scoring Stories. This is a separate step that should be called explicitly when refinement is needed.

---

## Quality Threshold Settings

### Default Threshold

- Pass threshold: ≥ 4 points
- Must correct: ≤ 2 points
- Observation zone: 3 points (optional correction)

### Strict Mode

When user requests "strict check" or project risk is higher:

- Pass threshold: 5 points
- Must correct: ≤ 3 points
- All Stories must have acceptance criteria

### Lenient Mode

When user requests "quick pass" or project is MVP/POC:

- Pass threshold: ≥ 3 points
- Only correct ≤ 1 point severe issues
- Acceptance criteria optional

---

## Checklist

After completing refinement, confirm the following items:

- [ ] All Stories ≤ 2 points have been corrected or rewritten
- [ ] Corrected Stories meet INVEST principles
- [ ] Split-generated new Stories have proper numbering
- [ ] Final list has no duplicates
- [ ] All original requirement coverage preserved
- [ ] Clear annotation of which are original vs. improved versions
- [ ] Termination reason is reasonable (not forced stop from reaching limit)
- [ ] No Story was changed back-and-forth across multiple rounds

---

## Iterative vs. Single-Pass Refinement

### When to Use Iterative (Default)

- Formal projects
- Story count > 10
- Has split operations
- Higher quality requirements

### When to Use Single-Pass

When user explicitly says "quick refine" or "one pass only":

- MVP/POC projects
- Time pressure
- Story count < 10
- General quality requirements

### Why 3 Round Limit

1. **Rule of thumb**: Most problems resolved within 2 rounds
2. **Diminishing returns**: Round 3+ corrections are usually nitpicking
3. **Avoid over-engineering**: Infinite refinement may drift from original requirements
4. **Time cost**: Each round requires processing time

If large numbers of low-scoring Stories remain after 3 rounds:
1. Output current results with annotations
2. Suggest returning to Story Writer to regenerate
3. Analyze whether RFP itself has systematic issues
