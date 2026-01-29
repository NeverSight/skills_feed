---
name: gap-analysis
description: Product and feature evaluation. Use when (1) Evaluating product/feature feasibility and market viability (2) Assessing product-market fit before investment (3) Comparing opportunities for roadmap prioritization (4) Competitive analysis to identify gaps (5) User asks "should we build X?" or "is this viable?" (6) Risk assessment for product decisions
---

# Gap Analysis

Evaluate product and feature ideas using structured frameworks. Produce actionable recommendations with evidence.

## 1. Gather Context

Collect before proceeding. Do not analyze with incomplete information.

| Input | Required Information |
|-------|---------------------|
| Idea | Problem solved, proposed solution |
| Users | Target segment, estimated count, current behavior |
| Alternatives | Existing solutions, workarounds, competitors |
| Success criteria | Measurable outcomes defining success |
| Constraints | Budget, timeline, team capabilities, technology limits |

Ask clarifying questions for any missing inputs.

## 2. DVFI Assessment

Score each dimension 1-5. Require evidence for each score.

| Dimension | Core Question | Evidence Sources |
|-----------|---------------|------------------|
| **Desirability** | Do users want this? | Problem frequency, pain severity, active solution-seeking, willingness to pay |
| **Viability** | Does the business case work? | Unit economics (LTV:CAC ≥3:1), margin structure, strategic alignment |
| **Feasibility** | Can the team build this? | Technical capability, resource availability, timeline realism |
| **Integrity** | Should this exist? | Ethics, regulatory compliance, societal impact, brand risk |

### Scoring Scale

| Score | Criteria |
|-------|----------|
| 5 | Strong evidence, low risk, clear path forward |
| 4 | Solid evidence, minor concerns with known mitigations |
| 3 | Mixed signals, material uncertainties requiring validation |
| 2 | Weak evidence, significant concerns, major unknowns |
| 1 | Red flags, likely blockers, insufficient evidence to proceed |

## 3. Deep-Dive Triggers

Apply additional frameworks when DVFI scores indicate risk.

| Condition | Action | Reference |
|-----------|--------|-----------|
| Desirability < 4 | Run validation methods (MVP types, interviews, JTBD) | [references/validation.md](references/validation.md) |
| Feasibility < 4 | Apply TELOS framework (Technical, Economic, Legal, Operational, Schedule) | [references/feasibility.md](references/feasibility.md) |
| Viability < 4 | Calculate TAM/SAM/SOM with bottom-up validation | [references/market-sizing.md](references/market-sizing.md) |

## 4. Risk Assessment

Calculate: `Risk Score = Likelihood (1-5) × Impact (1-5)`

| Score | Level | Required Action |
|-------|-------|-----------------|
| 1-4 | Low | Document and monitor |
| 5-12 | Medium | Define mitigation plan before proceeding |
| 13-25 | High | Resolve or accept at executive level before proceeding |

Evaluate risks in each category: Market, Technical, Financial, Operational, Legal/Regulatory, Competitive.

## 5. Prioritization

Use when comparing multiple opportunities. Default to RICE scoring.

`RICE = (Reach × Impact × Confidence) / Effort`

| Factor | Definition | Values |
|--------|------------|--------|
| Reach | Users affected per quarter | Actual count |
| Impact | Effect magnitude | 3=Massive, 2=High, 1=Medium, 0.5=Low, 0.25=Minimal |
| Confidence | Estimate certainty | 100%=High, 80%=Medium, 50%=Low |
| Effort | Work required | Person-months |

For alternative frameworks (ICE, Kano, MoSCoW), see [references/prioritization.md](references/prioritization.md).

## 6. Competitive Analysis

Include when competitors exist in the space.

| Gap Type | Definition | Strategic Implication |
|----------|------------|----------------------|
| Advantage | We lead | Defend and extend |
| Parity | Competitors have, we lack | Close gap to compete |
| Opportunity | No one has | First-mover potential |
| Investment | Requires major effort | Evaluate ROI carefully |

Map features using: ● Full support, ◐ Partial, ○ None

## 7. Recommendation

Conclude with one of four verdicts.

| Verdict | Criteria | Next Action |
|---------|----------|-------------|
| **GO** | All DVFI ≥ 4, no high risks | Proceed to implementation planning |
| **CONDITIONAL GO** | Mixed scores with addressable gaps | Proceed after specified conditions met |
| **PIVOT** | Core value exists, current approach flawed | Redesign with specific changes |
| **NO GO** | Blockers in ≥2 dimensions or unmitigable high risk | Archive learnings, do not proceed |

Every recommendation includes:
- Key findings summary (3-5 bullets)
- Critical assumptions that must hold true
- Specific next steps with owners
- Success metrics to track post-launch

## Output Format

```markdown
## Gap Analysis: [Idea Name]

### Executive Summary
[Verdict] - [2-sentence rationale with key evidence]

### DVFI Assessment
| Dimension | Score | Evidence | Concerns |
|-----------|-------|----------|----------|
| Desirability | X/5 | [specific data points] | [or "None"] |
| Viability | X/5 | [specific data points] | [or "None"] |
| Feasibility | X/5 | [specific data points] | [or "None"] |
| Integrity | X/5 | [specific data points] | [or "None"] |

### Key Risks
| Risk | Score | Mitigation |
|------|-------|------------|
| [Risk 1] | L×I=X | [Specific action] |

### Competitive Position
[Include only if competitors exist]

### Recommendation
**[GO / CONDITIONAL GO / PIVOT / NO GO]**

Conditions (if applicable): [specific requirements]

### Next Steps
1. [Action] - Owner: [name] - By: [date/milestone]
```

## Reference Thresholds

### Product-Market Fit

| Metric | Pass Threshold |
|--------|----------------|
| Sean Ellis Test | ≥40% "very disappointed" |
| LTV:CAC ratio | ≥3:1 |
| DAU/MAU (SaaS) | ≥20% |
| NPS | ≥30 (acceptable), ≥50 (strong) |

### Validation Tests

| Method | Pass Threshold |
|--------|----------------|
| Landing page signup | ≥10% conversion |
| Pre-order/deposit | ≥5% conversion |
| User interviews | 8/10 express strong intent |
| Fake door test | ≥3x baseline CTR |

### Failure Pattern Data (CB Insights)

| Cause | Frequency |
|-------|-----------|
| No market need | 42% |
| Lack of product-market fit | 34% |
| Overall new product failure rate | 70-80% |
