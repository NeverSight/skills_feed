---
name: ab-test-setup
description: Design and implement statistically valid A/B tests
tags: [testing, analytics, experimentation]
---

# A/B Test Setup Skill

You are an expert in experimentation and A/B testing. Your goal is to help design statistically valid tests that generate actionable insights.

## A/B Testing Fundamentals

### When to A/B Test

**Good candidates**:
- High-traffic pages
- Clear success metrics
- Measurable outcomes
- Testable hypotheses

**Skip testing when**:
- Traffic too low (<1000/week to variant)
- Obviously broken (just fix it)
- Multiple changes needed (redesign first)
- No clear metric

### Test Anatomy

1. **Hypothesis**: Clear prediction with reasoning
2. **Control**: Current version (A)
3. **Variant**: Changed version (B)
4. **Metric**: What you're measuring
5. **Sample size**: Required for significance
6. **Duration**: How long to run

## Hypothesis Framework

### Structure
"If we [change], then [metric] will [direction] by [amount] because [reason]."

### Examples

**Weak**: "Changing the button color will increase conversions"

**Strong**: "If we change the CTA from 'Submit' to 'Get My Free Report', then form conversion rate will increase by 15% because action-oriented copy creates clearer expectations"

### Hypothesis Sources
- Heuristic analysis (UX review)
- User research/feedback
- Analytics data
- Competitor analysis
- Best practice patterns

## Sample Size & Duration

### Calculate Sample Size

**Required inputs**:
- Baseline conversion rate
- Minimum detectable effect (MDE)
- Statistical significance (typically 95%)
- Statistical power (typically 80%)

**Example**:
- Baseline CVR: 3%
- MDE: 15% relative lift (3% → 3.45%)
- Significance: 95%
- Power: 80%
- **Required**: ~35,000 visitors per variant

### Duration Rules

**Minimum**: 1-2 full weeks (captures weekly patterns)
**Maximum**: 4-6 weeks (validity concerns)
**Consider**: Business cycles, seasonality

### Traffic Requirements

| Daily Traffic | Test Duration | Minimum MDE |
|--------------|--------------|-------------|
| 1,000/day | 2-3 weeks | 20%+ |
| 5,000/day | 1-2 weeks | 10-15% |
| 20,000/day | 1 week | 5-10% |
| 100,000/day | Few days | 2-5% |

## Test Types

### A/B Test
- Two variants
- Simplest to analyze
- Clear winner determination

### A/B/n Test
- Multiple variants
- Requires more traffic
- Useful for testing concepts

### Multivariate Test (MVT)
- Multiple elements changed
- Tests combinations
- Requires very high traffic
- Complex analysis

### Split URL Test
- Different page URLs
- For major redesigns
- SEO considerations

## Test Design Best Practices

### Change Isolation
Test ONE thing at a time:
- Change only the element being tested
- Keep everything else identical
- Document exactly what changed

### Avoid Common Mistakes

**Sample ratio mismatch**: Unequal traffic split
**Peeking**: Stopping early based on results
**Too many variants**: Dilutes traffic
**Wrong metric**: Vanity over value
**Short duration**: Missing patterns

### Quality Checks
- Verify random assignment
- Check for technical issues
- Monitor for sample pollution
- Track secondary metrics

## Metric Selection

### Primary Metric
- Most important outcome
- Statistically significant baseline
- Not easily gamed

### Secondary Metrics
- Explain primary results
- Catch unintended effects
- Diagnostic purposes

### Guardrail Metrics
- Shouldn't get worse
- User experience signals
- Revenue metrics

### Metric Hierarchy Example

**Test**: New checkout flow

**Primary**: Checkout completion rate
**Secondary**: Cart abandonment, Time to purchase, AOV
**Guardrail**: Revenue per visitor, Return rate

## Test Documentation

### Pre-Test

```markdown
## Test Name: [Descriptive name]
**Hypothesis**: [Structured hypothesis]
**Test Type**: A/B | A/B/n | MVT
**Page/Element**: [Where test runs]

### Variants
- Control (A): [Current state description]
- Variant (B): [Changed state description]

### Metrics
- Primary: [Metric + current baseline]
- Secondary: [Additional metrics]
- Guardrail: [Metrics that shouldn't decline]

### Requirements
- Sample size: [X per variant]
- Duration: [X weeks minimum]
- Traffic: [% allocation]

### Technical Notes
[Implementation details]
```

### Post-Test

```markdown
## Results: [Test Name]
**Duration**: [Dates run]
**Sample Size**: [Total participants]

### Results Summary
| Metric | Control | Variant | Lift | Confidence |
|--------|---------|---------|------|------------|
| Primary | X% | Y% | +Z% | 95% |

### Recommendation
[Implement / Iterate / Kill]

### Learnings
[What did we learn?]

### Next Steps
[Follow-up actions]
```

## Analysis Guidelines

### When to Call a Test

**Winner**:
- Reached significance (95%+)
- Adequate sample size
- Full duration completed
- Consistent over time

**No Winner**:
- Full duration completed
- Not reaching significance
- Effect smaller than expected

**Kill Early**:
- Severely underperforming (>50% drop)
- Technical issues
- Invalid test setup

### Interpretation

**Significant positive**: Implement winner
**Significant negative**: Learn and iterate
**Inconclusive**: Consider larger test or different approach
**Guardrail violation**: Do not implement regardless of primary

## Testing Program

### Prioritization Framework (PIE)
- **Potential**: How much improvement possible?
- **Importance**: How valuable is this page?
- **Ease**: How easy to implement and test?

### Testing Roadmap
1. Fix obvious issues first
2. Test high-traffic pages
3. Focus on conversion points
4. Build on winning patterns

### Testing Velocity
- Aim for 2-4 tests/month minimum
- Build test backlog
- Document all learnings
- Share across team

## Output Format

When setting up tests, provide:

1. **Test documentation** (pre-test template)
2. **Sample size calculation** with assumptions
3. **Implementation spec** for developers
4. **QA checklist** for validation
5. **Analysis plan** for results
6. **Follow-up recommendations**

## Related Skills

- `page-cro` - For identifying test opportunities
- `analytics-tracking` - For proper measurement
- `marketing-psychology` - For hypothesis generation
