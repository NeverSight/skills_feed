---
name: experiment-design-checklist
description: Generates a rigorous experiment design given a hypothesis. Use when asked to design experiments, plan experiments, create an experimental setup, or figure out how to test a research hypothesis. Covers controls, baselines, ablations, metrics, statistical tests, and compute estimates.
---

# Experiment Design Checklist

Prevent the "I ran experiments for 3 months and they're meaningless" disaster through rigorous upfront design.

## The Core Principle

Before running ANY experiment, you should be able to answer:
1. What specific claim will this experiment support or refute?
2. What would convince a skeptical reviewer?
3. What could go wrong that would invalidate the results?

## Process

### Step 1: State the Hypothesis Precisely

Convert your research question into falsifiable predictions:

**Template:**
```
If [intervention/method], then [measurable outcome], because [mechanism].
```

**Examples:**
- "If we add auxiliary contrastive loss, then downstream task accuracy increases by >2%, because representations become more separable."
- "If we use learned positional encodings, then performance on sequences >4096 tokens improves, because the model can extrapolate beyond training length."

**Null hypothesis:** What does "no effect" look like? This is what you're trying to reject.

### Step 2: Identify Variables

**Independent Variables (what you manipulate):**
| Variable | Levels | Rationale |
|----------|--------|-----------|
| [Var 1] | [Level A, B, C] | [Why these levels] |

**Dependent Variables (what you measure):**
| Metric | How Measured | Why This Metric |
|--------|--------------|-----------------|
| [Metric 1] | [Procedure] | [Justification] |

**Control Variables (what you hold constant):**
| Variable | Fixed Value | Why Fixed |
|----------|-------------|-----------|
| [Var 1] | [Value] | [Prevents confound X] |

### Step 3: Choose Baselines

Every experiment needs comparisons. No result is meaningful in isolation.

**Baseline Hierarchy:**

1. **Random/Trivial Baseline**
   - What does random chance achieve?
   - Sanity check that the task isn't trivial

2. **Simple Baseline**
   - Simplest reasonable approach
   - Often embarrassingly effective

3. **Standard Baseline**
   - Well-known method from literature
   - Apples-to-apples comparison

4. **State-of-the-Art Baseline**
   - Current best published result
   - Only if you're claiming SOTA

5. **Ablated Self**
   - Your method minus key components
   - Shows each component contributes

**For each baseline, document:**
- Source (paper, implementation)
- Hyperparameters used
- Whether you re-ran or used reported numbers
- Any modifications made

### Step 4: Design Ablations

Ablations answer: "Is each component necessary?"

**Ablation Template:**
| Variant | What's Removed/Changed | Expected Effect | If No Effect... |
|---------|----------------------|-----------------|-----------------|
| Full Model | Nothing | Best performance | - |
| w/o Component A | Remove A | Performance drops X% | A isn't helping |
| w/o Component B | Remove B | Performance drops Y% | B isn't helping |
| Component A only | Only A, no B | Shows A's isolated contribution | - |

**Good ablations are:**
- Surgical (one change at a time)
- Interpretable (clear what was changed)
- Informative (result tells you something)

### Step 5: Address Confounds

Things that could explain your results OTHER than your hypothesis:

**Common Confounds:**

| Confound | How to Check | How to Control |
|----------|--------------|----------------|
| Hyperparameter tuning advantage | Same tuning budget for all | Report tuning procedure |
| Compute advantage | Matched FLOPs/params | Report compute used |
| Data leakage | Check train/test overlap | Strict separation |
| Random seed luck | Multiple seeds | Report variance |
| Implementation bugs (baseline) | Verify baseline numbers | Use official implementations |
| Cherry-picked examples | Random or systematic selection | Pre-register selection criteria |

### Step 6: Statistical Rigor

**Sample Size:**
- How many random seeds? (Minimum: 3, better: 5+)
- How many data splits? (If applicable)
- Power analysis: Can you detect expected effect size?

**What to Report:**
- Mean ± standard deviation (or standard error)
- Confidence intervals where appropriate
- Statistical significance tests if claiming "better"

**Appropriate Tests:**
| Comparison | Test | Assumptions |
|------------|------|-------------|
| Two methods, normal data | t-test | Normality, equal variance |
| Two methods, unknown dist | Mann-Whitney U | Ordinal data |
| Multiple methods | ANOVA + post-hoc | Normality |
| Multiple methods, unknown | Kruskal-Wallis | Ordinal data |
| Paired comparisons | Wilcoxon signed-rank | Same test instances |

**Avoid:**
- p-hacking (running until significant)
- Multiple comparison problems (Bonferroni correct)
- Reporting only favorable metrics

### Step 7: Compute Budget

Before running, estimate:

| Component | Estimate | Notes |
|-----------|----------|-------|
| Single training run | X GPU-hours | [Details] |
| Hyperparameter search | Y runs × X hours | [Search strategy] |
| Baselines | Z runs × W hours | [Which baselines] |
| Ablations | N variants × X hours | [Which ablations] |
| Seeds | M seeds × above | [How many seeds] |
| **Total** | **T GPU-hours** | Buffer: 1.5-2x |

**Go/No-Go Decision:** Is this feasible with available resources?

### Step 8: Pre-Registration (Optional but Recommended)

Write down BEFORE running:
- Exact hypotheses
- Primary metrics (not chosen post-hoc)
- Analysis plan
- What would constitute "success"

This prevents unconscious goal-post moving.

## Output: Experiment Design Document

```markdown
# Experiment Design: [Title]

## Hypothesis
[Precise statement]

## Variables
### Independent
[Table]

### Dependent
[Table]

### Controls
[Table]

## Baselines
1. [Baseline 1]: [Source, details]
2. [Baseline 2]: [Source, details]

## Ablations
[Table]

## Confound Mitigation
[Table]

## Statistical Plan
- Seeds: [N]
- Tests: [Which tests for which comparisons]
- Significance threshold: [α level]

## Compute Budget
[Table with total estimate]

## Success Criteria
- Primary: [What must be true]
- Secondary: [Nice to have]

## Timeline
- Phase 1: [What, when]
- Phase 2: [What, when]

## Known Risks
1. [Risk 1]: [Mitigation]
2. [Risk 2]: [Mitigation]
```

## Red Flags in Experiment Design

🚩 "We'll figure out the metrics later"
🚩 "One run should be enough"
🚩 "We don't need baselines, it's obviously better"
🚩 "Let's just see what happens"
🚩 "We can always run more if it's not significant"
🚩 No compute estimate before starting
🚩 Vague success criteria
