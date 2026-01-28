---
name: decision-matrix
description: Use when comparing multiple named alternatives across several criteria, need transparent trade-off analysis, making group decisions requiring alignment, choosing between vendors/tools/strategies, stakeholders need to see decision rationale, balancing competing priorities (cost vs quality vs speed), user mentions "which option should we choose", "compare alternatives", "evaluate vendors", "trade-offs", or when decision needs to be defensible and data-driven.
---

# Decision Matrix

## What Is It?

A decision matrix is a structured tool for comparing multiple alternatives against weighted criteria to make transparent, defensible choices. It forces explicit trade-off analysis by scoring each option on each criterion, making subjective factors visible and comparable.

**Quick example:**

| Option | Cost (30%) | Speed (25%) | Quality (45%) | Weighted Score |
|--------|-----------|------------|---------------|----------------|
| Option A | 8 (2.4) | 6 (1.5) | 9 (4.05) | **7.95** ← Winner |
| Option B | 6 (1.8) | 9 (2.25) | 7 (3.15) | 7.20 |
| Option C | 9 (2.7) | 4 (1.0) | 6 (2.7) | 6.40 |

The numbers in parentheses show criterion score × weight. Option A wins despite not being fastest or cheapest because quality matters most (45% weight).

## Workflow

Copy this checklist and track your progress:

```
Decision Matrix Progress:
- [ ] Step 1: Frame the decision and list alternatives
- [ ] Step 2: Identify and weight criteria
- [ ] Step 3: Score each alternative on each criterion
- [ ] Step 4: Calculate weighted scores and analyze results
- [ ] Step 5: Validate quality and deliver recommendation
```

**Step 1: Frame the decision and list alternatives**

Ask user for decision context (what are we choosing and why), list of alternatives (specific named options, not generic categories), constraints or dealbreakers (must-have requirements), and stakeholders (who needs to agree). Understanding must-haves helps filter options before scoring. See [Framing Questions](#framing-questions) for clarification prompts.

**Step 2: Identify and weight criteria**

Collaborate with user to identify criteria (what factors matter for this decision), determine weights (which criteria matter most, as percentages summing to 100%), and validate coverage (do criteria capture all important trade-offs). If user is unsure about weighting → Use [resources/template.md](resources/template.md) for weighting techniques. See [Criterion Types](#criterion-types) for common patterns.

**Step 3: Score each alternative on each criterion**

For each option, score on each criterion using consistent scale (typically 1-10 where 10 = best). Ask user for scores or research objective data (cost, speed metrics) where available. Document assumptions and data sources. For complex scoring → See [resources/methodology.md](resources/methodology.md) for calibration techniques.

**Step 4: Calculate weighted scores and analyze results**

Calculate weighted score for each option (sum of criterion score × weight). Rank options by total score. Identify close calls (options within 5% of each other). Check for sensitivity (would changing one weight flip the decision). See [Sensitivity Analysis](#sensitivity-analysis) for interpretation guidance.

**Step 5: Validate quality and deliver recommendation**

Self-assess using [resources/evaluators/rubric_decision_matrix.json](resources/evaluators/rubric_decision_matrix.json) (minimum score ≥ 3.5). Present decision-matrix.md file with clear recommendation, highlight key trade-offs revealed by analysis, note sensitivity to assumptions, and suggest next steps (gather more data on close calls, validate with stakeholders).

## Framing Questions

**To clarify the decision:**
- What specific decision are we making? (Choose X from Y alternatives)
- What happens if we don't decide or choose wrong?
- When do we need to decide by?
- Can we choose multiple options or only one?

**To identify alternatives:**
- What are all the named options we're considering?
- Are there other alternatives we're ruling out immediately? Why?
- What's the "do nothing" or status quo option?

**To surface must-haves:**
- Are there absolute dealbreakers? (Budget cap, timeline requirement, compliance need)
- Which constraints are flexible vs rigid?

## Criterion Types

Common categories for criteria (adapt to your decision):

**Financial Criteria:**
- Upfront cost, ongoing cost, ROI, payback period, budget impact
- Typical weight: 20-40% (higher for cost-sensitive decisions)

**Performance Criteria:**
- Speed, quality, reliability, scalability, capacity, throughput
- Typical weight: 30-50% (higher for technical decisions)

**Risk Criteria:**
- Implementation risk, reversibility, vendor lock-in, technical debt, compliance risk
- Typical weight: 10-25% (higher for enterprise/regulated environments)

**Strategic Criteria:**
- Alignment with goals, future flexibility, competitive advantage, market positioning
- Typical weight: 15-30% (higher for long-term decisions)

**Operational Criteria:**
- Ease of use, maintenance burden, training required, integration complexity
- Typical weight: 10-20% (higher for internal tools)

**Stakeholder Criteria:**
- Team preference, user satisfaction, executive alignment, customer impact
- Typical weight: 5-15% (higher for change management contexts)

## Weighting Approaches

**Method 1: Direct Allocation (simplest)**
Stakeholders assign percentages totaling 100%. Quick but can be arbitrary.

**Method 2: Pairwise Comparison (more rigorous)**
Compare each criterion pair: "Is cost more important than speed?" Build ranking, then assign weights.

**Method 3: Must-Have vs Nice-to-Have (filters first)**
Separate absolute requirements (pass/fail) from weighted criteria. Only evaluate options that pass must-haves.

**Method 4: Stakeholder Averaging (group decisions)**
Each stakeholder assigns weights independently, then average. Reveals divergence in priorities.

See [resources/methodology.md](resources/methodology.md) for detailed facilitation techniques.

## Sensitivity Analysis

After calculating scores, check robustness:

**1. Close calls:** Options within 5-10% of winner → Need more data or second opinion
**2. Dominant criteria:** One criterion driving entire decision → Is weight too high?
**3. Weight sensitivity:** Would swapping two criterion weights flip the winner? → Decision is fragile
**4. Score sensitivity:** Would adjusting one score by ±1 point flip the winner? → Decision is sensitive to that data point

**Red flags:**
- Winner changes with small weight adjustments → Need stakeholder alignment on priorities
- One option wins every criterion → Matrix is overkill, choice is obvious
- Scores are mostly guesses → Gather more data before deciding

## Common Patterns

**Technology Selection:**
- Criteria: Cost, performance, ecosystem maturity, team familiarity, vendor support
- Weight: Performance and maturity typically 50%+

**Vendor Evaluation:**
- Criteria: Price, features, integration, support, reputation, contract terms
- Weight: Features and integration typically 40-50%

**Strategic Choices:**
- Criteria: Market opportunity, resource requirements, risk, alignment, timing
- Weight: Market opportunity and alignment typically 50%+

**Hiring Decisions:**
- Criteria: Experience, culture fit, growth potential, compensation expectations, availability
- Weight: Experience and culture fit typically 50%+

**Feature Prioritization:**
- Criteria: User impact, effort, strategic value, risk, dependencies
- Weight: User impact and strategic value typically 50%+

## When NOT to Use This Skill

**Skip decision matrix if:**
- Only one viable option (no real alternatives to compare)
- Decision is binary yes/no with single criterion (use simpler analysis)
- Options differ on only one dimension (just compare that dimension)
- Decision is urgent and stakes are low (analysis overhead not worth it)
- Criteria are impossible to define objectively (purely emotional/aesthetic choice)
- You already know the answer (using matrix to justify pre-made decision is waste)

**Use instead:**
- Single criterion → Simple ranking or threshold check
- Binary decision → Pro/con list or expected value calculation
- Highly uncertain → Scenario planning or decision tree
- Purely subjective → Gut check or user preference vote

## Quick Reference

**Process:**
1. Frame decision → List alternatives
2. Identify criteria → Assign weights (sum to 100%)
3. Score each option on each criterion (1-10 scale)
4. Calculate weighted scores → Rank options
5. Check sensitivity → Deliver recommendation

**Resources:**
- [resources/template.md](resources/template.md) - Structured matrix format and weighting techniques
- [resources/methodology.md](resources/methodology.md) - Advanced techniques (group facilitation, calibration, sensitivity analysis)
- [resources/evaluators/rubric_decision_matrix.json](resources/evaluators/rubric_decision_matrix.json) - Quality checklist before delivering

**Deliverable:** `decision-matrix.md` file with table, rationale, and recommendation
