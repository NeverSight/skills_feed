---
name: evaluation-rubrics
description: Use when need explicit quality criteria and scoring scales to evaluate work consistently, compare alternatives objectively, set acceptance thresholds, reduce subjective bias, or when user mentions rubric, scoring criteria, quality standards, evaluation framework, inter-rater reliability, or grade/assess work.
---
# Evaluation Rubrics

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Evaluation Rubrics provide explicit criteria and performance scales to assess quality consistently, fairly, and transparently. This skill guides you through rubric design—from identifying meaningful criteria to writing clear performance descriptors—to enable objective evaluation, reduce bias, align teams on standards, and give actionable feedback.

## When to Use

Use this skill when:

- **Quality assessment**: Code reviews, design critiques, writing evaluation, product launches, academic grading
- **Competitive evaluation**: Vendor selection, hiring candidates, grant proposals, pitch competitions, award judging
- **Progress tracking**: Sprint reviews, skill assessments, training completion, certification exams
- **Standardization**: Multiple reviewers need to score consistently (inter-rater reliability), reduce subjective bias
- **Feedback delivery**: Provide clear, actionable feedback tied to specific criteria (not just "good" or "needs work")
- **Threshold setting**: Define minimum acceptable quality (e.g., "must score ≥3/5 on all criteria to pass")
- **Process improvement**: Identify systematic weaknesses (many submissions score low on same criterion → need better guidance)

Trigger phrases: "rubric", "scoring criteria", "evaluation framework", "quality standards", "how do we grade this", "what does good look like", "consistent assessment", "inter-rater reliability"

## What Is It?

An evaluation rubric is a structured scoring tool with:
- **Criteria**: What dimensions of quality are being assessed (e.g., clarity, completeness, originality)
- **Scale**: Numeric or qualitative levels (e.g., 1-5, Novice-Expert, Below/Meets/Exceeds)
- **Descriptors**: Explicit descriptions of what each level looks like for each criterion
- **Weighting** (optional): Importance of each criterion (some more critical than others)

**Core benefits:**
- **Consistency**: Same work scored similarly by different reviewers (inter-rater reliability)
- **Transparency**: Evaluatees know expectations upfront, can self-assess
- **Actionable feedback**: Specific areas for improvement, not vague critique
- **Fairness**: Reduces bias, focuses on observable work not subjective impressions
- **Efficiency**: Faster evaluation with clear benchmarks, less debate

**Quick example:**

**Scenario**: Evaluating technical blog posts

**Rubric (1-5 scale)**:

| Criterion | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|-----------|----------|--------------|---------------|
| **Technical Accuracy** | Multiple factual errors, misleading | Mostly correct, minor inaccuracies | Fully accurate, technically rigorous |
| **Clarity** | Confusing, jargon-heavy, poor structure | Clear to experts, some structure | Accessible to target audience, well-organized |
| **Practical Value** | No actionable guidance, theoretical only | Some examples, limited applicability | Concrete examples, immediately applicable |
| **Originality** | Rehashes common knowledge, no new insight | Some fresh perspective, builds on existing | Novel approach, advances understanding |

**Scoring**: Post A scores [4, 5, 3, 2] = 3.5 avg. Post B scores [5, 4, 5, 4] = 4.5 avg → Post B higher quality.

**Feedback for Post A**: "Strong clarity (5) and good accuracy (4), but needs more practical examples (3) and offers less original insight (2). Add code samples and explore edge cases to improve."

## Workflow

Copy this checklist and track your progress:

```
Rubric Development Progress:
- [ ] Step 1: Define purpose and scope
- [ ] Step 2: Identify evaluation criteria
- [ ] Step 3: Design the scale
- [ ] Step 4: Write performance descriptors
- [ ] Step 5: Test and calibrate
- [ ] Step 6: Use and iterate
```

**Step 1: Define purpose and scope**

Clarify what you're evaluating, who evaluates, who uses results, what decisions depend on scores. See [resources/template.md](resources/template.md#purpose-definition-template) for scoping questions.

**Step 2: Identify evaluation criteria**

Brainstorm quality dimensions, prioritize most important/observable, balance coverage vs. simplicity (4-8 criteria typical). See [resources/template.md](resources/template.md#criteria-identification-template) for brainstorming framework.

**Step 3: Design the scale**

Choose number of levels (1-5, 1-4, 1-10), scale type (numeric, qualitative), anchors (what does each level mean?). See [resources/methodology.md](resources/methodology.md#scale-design-principles) for scale selection guidance.

**Step 4: Write performance descriptors**

For each criterion × level, write observable description of what that performance looks like. See [resources/template.md](resources/template.md#descriptor-writing-template) for writing guidelines.

**Step 5: Test and calibrate**

Have multiple reviewers score sample work, compare scores, discuss discrepancies, refine rubric. See [resources/methodology.md](resources/methodology.md#calibration-techniques) for inter-rater reliability testing.

**Step 6: Use and iterate**

Apply rubric, collect feedback from evaluators and evaluatees, revise criteria/descriptors as needed. Validate using [resources/evaluators/rubric_evaluation_rubrics.json](resources/evaluators/rubric_evaluation_rubrics.json). **Minimum standard**: Average score ≥ 3.5.

## Common Patterns

**Pattern 1: Analytic Rubric (Most Common)**
- **Structure**: Multiple criteria (rows), multiple levels (columns), descriptor for each cell
- **Use case**: Detailed feedback needed, want to see performance across dimensions, diagnostic assessment
- **Pros**: Specific feedback, identifies strengths/weaknesses by criterion, high reliability
- **Cons**: Time-consuming to create and use, can feel reductive
- **Example**: Code review rubric (Correctness, Efficiency, Readability, Maintainability × 1-5 scale)

**Pattern 2: Holistic Rubric**
- **Structure**: Single overall score, descriptors integrate multiple criteria
- **Use case**: Quick overall judgment, summative assessment, criteria hard to separate
- **Pros**: Fast, intuitive, captures gestalt quality
- **Cons**: Less actionable feedback, lower reliability, can't diagnose specific weaknesses
- **Example**: Essay holistic scoring (1=poor essay, 3=adequate essay, 5=excellent essay with detailed descriptors)

**Pattern 3: Single-Point Rubric**
- **Structure**: Criteria listed with only "meets standard" descriptor, space to note above/below
- **Use case**: Growth mindset feedback, encourage self-assessment, less punitive feel
- **Pros**: Emphasizes improvement not deficit, simpler to create, encourages dialogue
- **Cons**: Less precision, requires written feedback to supplement
- **Example**: Design critique (list criteria like "Visual hierarchy", "Accessibility", note "+Clear focal point, -Poor contrast")

**Pattern 4: Checklist (Binary)**
- **Structure**: List of yes/no items, must-haves for acceptance
- **Use case**: Compliance checks, minimum quality gates, pass/fail decisions
- **Pros**: Very clear, objective, easy to use
- **Cons**: No gradations, misses quality beyond basics, can feel rigid
- **Example**: Pull request checklist (Tests pass? Code linted? Documentation updated? Security review?)

**Pattern 5: Standards-Based Rubric**
- **Structure**: Criteria tied to learning objectives/competencies, levels = degree of mastery
- **Use case**: Educational assessment, skill certification, training evaluation, criterion-referenced
- **Pros**: Aligned to standards, shows progress toward mastery, diagnostic
- **Cons**: Requires clear standards, can be complex to design
- **Example**: Data science skills (Proficiency in: Data cleaning, Modeling, Visualization, Communication × Novice/Competent/Expert)

## Guardrails

**Critical requirements:**

1. **Criteria must be observable and measurable**: Not "good attitude" (subjective), but "arrives on time, volunteers for tasks, helps teammates" (observable). Vague criteria lead to unreliable scoring. Test: Can two independent reviewers score this criterion consistently?

2. **Descriptors must distinguish levels clearly**: Each level should have concrete differences from adjacent levels (not just "better" or "more"). Avoid: "5=very good, 4=good, 3=okay". Better: "5=zero bugs, meets all requirements, 4=1-2 minor bugs, meets 90% requirements, 3=3+ bugs or missing key feature".

3. **Use appropriate scale granularity**: 1-3 too coarse (hard to differentiate), 1-10 too fine (false precision, hard to define all levels). Sweet spot: 1-4 (forced choice, no middle) or 1-5 (allows neutral middle). Match granularity to actual observable differences.

4. **Balance comprehensiveness with simplicity**: More criteria = more detailed feedback but longer to use. Aim for 4-8 criteria covering essential quality dimensions. If >10 criteria, consider grouping or prioritizing.

5. **Calibrate for inter-rater reliability**: Have multiple reviewers score same work, measure agreement (Kappa, ICC). If <70% agreement, refine descriptors. Schedule calibration sessions where reviewers discuss discrepancies.

6. **Provide examples at each level**: Abstract descriptors are ambiguous. Include concrete examples of work at each level (anchor papers, reference designs, code samples) to calibrate reviewers.

7. **Make rubric accessible before evaluation**: If evaluatees see rubric only after being scored, it's just grading not guidance. Share rubric upfront so people know expectations and can self-assess.

8. **Weight criteria appropriately**: Not all criteria equally important. If "Security" matters more than "Code style", weight it (Security ×3, Style ×1). Or use thresholds (must score ≥4 on Security to pass, regardless of other scores).

**Common pitfalls:**

- ❌ **Subjective language**: "Shows effort", "creative", "professional" - not observable without concrete descriptors
- ❌ **Overlapping criteria**: "Clarity" and "Organization" often conflated - define boundaries clearly
- ❌ **Hidden expectations**: Rubric doesn't mention X, but evaluators penalize for missing X - document all criteria
- ❌ **Central tendency bias**: Reviewers avoid extremes (always score 3/5) - use even-number scales (1-4) to force choice
- ❌ **Halo effect**: High score on one criterion biases other scores up - score each criterion independently before looking at others
- ❌ **Rubric drift**: Descriptors erode over time, reviewers interpret differently - periodic re-calibration required

## Quick Reference

**Key resources:**

- **[resources/template.md](resources/template.md)**: Purpose definition, criteria brainstorming, scale selection, descriptor templates, rubric formats
- **[resources/methodology.md](resources/methodology.md)**: Scale design principles, descriptor writing techniques, inter-rater reliability testing, bias mitigation
- **[resources/evaluators/rubric_evaluation_rubrics.json](resources/evaluators/rubric_evaluation_rubrics.json)**: Quality criteria for rubric design (criteria clarity, scale appropriateness, descriptor specificity)

**Scale Selection Guide**:

| Scale | Use When | Pros | Cons |
|-------|----------|------|------|
| **1-3** | Need quick categorization, clear tiers | Fast, forces clear decision | Too coarse, less feedback |
| **1-4** | Want forced choice (no middle) | Avoids central tendency, clear differentiation | No neutral option, feels binary |
| **1-5** | General purpose, most common | Allows neutral, familiar, good granularity | Central tendency bias (everyone gets 3) |
| **1-10** | Need fine gradations, large sample | Maximum differentiation, statistical analysis | False precision, hard to distinguish adjacent levels |
| **Qualitative** (Novice/Proficient/Expert) | Educational, skill development | Intuitive, growth-oriented | Less quantitative, harder to aggregate |
| **Binary** (Yes/No, Pass/Fail) | Compliance, gatekeeping | Objective, simple | No gradations, misses quality differences |

**Criteria Types**:

- **Product criteria**: Evaluate the artifact itself (correctness, clarity, completeness, aesthetics, performance)
- **Process criteria**: How work was done (methodology followed, collaboration, iteration, time management)
- **Impact criteria**: Outcomes/effects (user satisfaction, business value, learning achieved)
- **Meta criteria**: Quality of quality (documentation, testability, maintainability, scalability)

**Inter-Rater Reliability Benchmarks**:

- **<50% agreement**: Rubric unreliable, needs major revision
- **50-70% agreement**: Marginal, refine descriptors and calibrate reviewers
- **70-85% agreement**: Good, acceptable for most uses
- **>85% agreement**: Excellent, highly reliable scoring

**Typical Rubric Development Time**:

- **Simple rubric** (3-5 criteria, 1-4 scale, known domain): 2-4 hours
- **Standard rubric** (5-7 criteria, 1-5 scale, some complexity): 6-10 hours + calibration session
- **Complex rubric** (8+ criteria, multiple scales, novel domain): 15-25 hours + multiple calibration rounds

**When to escalate beyond rubrics**:

- High-stakes decisions (hiring, admissions, awards) → Add structured interviews, portfolios, multi-method assessment
- Subjective/creative work (art, poetry, design) → Supplement rubric with critique, discourse, expert judgment
- Complex holistic judgment (leadership, cultural fit) → Rubrics help but don't capture everything, use thoughtfully
→ Rubrics are tools not replacements for human judgment. Use to structure thinking, not mechanize decisions.

**Inputs required:**

- **Artifact type** (what are we evaluating? essays, code, designs, proposals?)
- **Criteria** (quality dimensions to assess, 4-8 most common)
- **Scale** (1-5 default, or specify 1-4, 1-10, qualitative labels)

**Outputs produced:**

- `evaluation-rubrics.md`: Purpose, criteria definitions, scale with descriptors, usage instructions, weighting/thresholds, calibration notes
