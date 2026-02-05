---
name: power-analysis
description: "Calculate statistical power and required sample sizes for research studies. Use when: (1) Designing experiments to determine sample size, (2) Justifying sample size for grant proposals or protocols, (3) Evaluating adequacy of existing studies, (4) Meeting NIH rigor standards for pre-registration, (5) Conducting retrospective power analysis to interpret null results."
allowed-tools: Read, Write
version: 1.0.0
---

# Statistical Power Analysis Skill

## Purpose

Calculate statistical power and determine required sample sizes for research studies. Essential for experimental design, grant writing, and meeting NIH rigor and reproducibility standards.

## Core Concepts

### Statistical Power
**Definition:** Probability of detecting a true effect when it exists (1 - β)

**Standard:** Power ≥ 0.80 (80%) is typically required for NIH grants and pre-registration

### Key Parameters
1. **Effect Size (d, r, η²)** - Magnitude of the phenomenon
2. **Alpha (α)** - Type I error rate (typically 0.05)
3. **Power (1-β)** - Probability of detecting effect (typically 0.80)
4. **Sample Size (N)** - Number of participants/observations needed

### The Relationship
```
Power = f(Effect Size, Sample Size, Alpha, Test Type)

For given effect size and alpha:
↑ Sample Size → ↑ Power
↑ Effect Size → ↓ Sample Size needed
```

## When to Use This Skill

### Pre-Study (Prospective Power Analysis)
1. **Grant Proposals** - Justify requested sample size
2. **Study Design** - Determine recruitment needs
3. **Pre-Registration** - Document planned sample size with justification
4. **Resource Planning** - Estimate time and cost requirements
5. **Ethical Review** - Minimize participants while maintaining power

### Post-Study (Retrospective/Sensitivity Analysis)
1. **Null Results** - Was study adequately powered?
2. **Publication** - Report achieved power
3. **Meta-Analysis** - Assess individual study adequacy
4. **Study Critique** - Evaluate power of published work

## Common Study Designs

### 1. Independent Samples T-Test
**Use:** Compare two independent groups

**Formula:**
```
N per group = 2 * (z_α/2 + z_β)² * σ² / d²

Where:
- d = effect size (Cohen's d)
- α = significance level (typ. 0.05)
- β = Type II error (1 - power)
- σ² = pooled variance
```

**Example:**
```
Research Question: Does intervention improve test scores vs. control?
Effect Size: d = 0.5 (medium effect)
Alpha: 0.05
Power: 0.80

Result: N = 64 per group (128 total)
```

**Effect Size Guidelines (Cohen's d):**
- Small: d = 0.2
- Medium: d = 0.5
- Large: d = 0.8

### 2. Paired Samples T-Test
**Use:** Pre-post comparisons, matched pairs

**Formula:**
```
N = (z_α/2 + z_β)² * 2(1-ρ) / d²

Where ρ = correlation between measures
```

**Example:**
```
Research Question: Does training improve performance (pre-post)?
Effect Size: d = 0.6
Correlation: ρ = 0.5 (moderate test-retest reliability)
Alpha: 0.05
Power: 0.80

Result: N = 24 participants
```

**Key Insight:** Higher correlation → fewer participants needed

### 3. One-Way ANOVA
**Use:** Compare 3+ independent groups

**Formula:**
```
N per group = (k * (z_α/2 + z_β)²) / f²

Where:
- k = number of groups
- f = effect size (Cohen's f)
```

**Example:**
```
Research Question: Compare 4 treatment conditions
Effect Size: f = 0.25 (medium)
Alpha: 0.05
Power: 0.80

Result: N = 45 per group (180 total)
```

**Effect Size Guidelines (Cohen's f):**
- Small: f = 0.10
- Medium: f = 0.25
- Large: f = 0.40

### 4. Chi-Square Test
**Use:** Association between categorical variables

**Formula:**
```
N = (z_α/2 + z_β)² / (w² * df)

Where:
- w = effect size (Cohen's w)
- df = degrees of freedom
```

**Example:**
```
Research Question: Is treatment success related to group (2x2 table)?
Effect Size: w = 0.3 (medium)
Alpha: 0.05
Power: 0.80
df = 1

Result: N = 88 total participants
```

**Effect Size Guidelines (Cohen's w):**
- Small: w = 0.10
- Medium: w = 0.30
- Large: w = 0.50

### 5. Correlation
**Use:** Relationship between continuous variables

**Formula:**
```
N = (z_α/2 + z_β)² / C(r)² + 3

Where C(r) = 0.5 * ln((1+r)/(1-r)) [Fisher's z]
```

**Example:**
```
Research Question: Correlation between anxiety and performance
Expected r: 0.30
Alpha: 0.05
Power: 0.80

Result: N = 84 participants
```

**Effect Size Guidelines (Pearson's r):**
- Small: r = 0.10
- Medium: r = 0.30
- Large: r = 0.50

### 6. Multiple Regression
**Use:** Predict outcome from multiple predictors

**Formula:**
```
N = (L / f²) + k + 1

Where:
- L = non-centrality parameter
- f² = effect size (Cohen's f²)
- k = number of predictors
```

**Example:**
```
Research Question: Predict depression from 5 variables
Effect Size: f² = 0.15 (medium)
Alpha: 0.05
Power: 0.80
Predictors: 5

Result: N = 92 participants
```

**Effect Size Guidelines (f²):**
- Small: f² = 0.02
- Medium: f² = 0.15
- Large: f² = 0.35

## Choosing Effect Sizes

### Method 1: Previous Literature
**Best Practice:** Use meta-analytic estimates

```
Example: Meta-analysis shows d = 0.45 for CBT vs. control
Use: d = 0.45 for power calculation
```

### Method 2: Pilot Study
```
Run small pilot (N = 20-30)
Calculate observed effect size
Adjust for uncertainty (use 80% of observed)
```

### Method 3: Minimum Meaningful Effect
```
Question: What's the smallest effect worth detecting?
Clinical: Minimum clinically important difference (MCID)
Practical: Cost-benefit threshold
```

### Method 4: Cohen's Conventions
**Use only when no better information available:**
- Small effects: Often require N > 300
- Medium effects: Typically N = 50-100 per group
- Large effects: May need only N = 20-30 per group

**Warning:** Cohen's conventions are rough guidelines, not universal truths!

## NIH Rigor Standards

### Required Elements for NIH Grants

1. **Justified Effect Size**
   - Cite source (literature, pilot, theory)
   - Explain why this effect size is reasonable
   - Consider range of plausible values

2. **Power Calculation**
   - Show formula or software used
   - Report all assumptions
   - Calculate required N

3. **Sensitivity Analysis**
   - Show power across range of effect sizes
   - Demonstrate study is adequately powered

4. **Accounting for Attrition**
   ```
   N_recruit = N_required / (1 - expected_attrition_rate)
   
   Example:
   N_required = 100
   Expected attrition = 20%
   N_recruit = 100 / 0.80 = 125
   ```

### Sample Power Analysis Section (Grant)

```
Sample Size Justification

We will recruit 140 participants (70 per group) to detect a medium 
effect (d = 0.50) with 80% power at α = 0.05 using an independent 
samples t-test. This effect size is based on our pilot study (N = 30) 
which showed d = 0.62, and is consistent with meta-analytic estimates 
for similar interventions (Smith et al., 2023; d = 0.48, 95% CI 
[0.35, 0.61]).

We calculated the required sample size using G*Power 3.1, assuming 
a two-tailed test. To account for anticipated 20% attrition based on 
previous studies in this population, we will recruit 175 participants 
(rounded to 180 for equal groups: 90 per condition).

Sensitivity analysis shows our design provides:
- 95% power to detect d = 0.60 (large effect)
- 80% power to detect d = 0.50 (medium effect)  
- 55% power to detect d = 0.40 (small-medium effect)

This ensures adequate power while minimizing participant burden and 
research costs.
```

## Tools and Software

### G*Power (Free)
- **Use:** Most common power analysis tool
- **Pros:** User-friendly, comprehensive test coverage
- **Cons:** Desktop only, manual calculations
- **Download:** https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower

### R (pwr package)
```R
library(pwr)

# Independent t-test
pwr.t.test(d = 0.5, power = 0.80, sig.level = 0.05, type = "two.sample")

# ANOVA
pwr.anova.test(k = 4, f = 0.25, power = 0.80, sig.level = 0.05)

# Correlation
pwr.r.test(r = 0.30, power = 0.80, sig.level = 0.05)
```

### Python (statsmodels)
```python
from statsmodels.stats.power import ttest_power

# Calculate power
power = ttest_power(effect_size=0.5, nobs=64, alpha=0.05)

# Calculate required N
from statsmodels.stats.power import tt_ind_solve_power
n = tt_ind_solve_power(effect_size=0.5, power=0.8, alpha=0.05)
```

### Online Calculators
- **PASS:** https://www.ncss.com/software/pass/
- **PS:** https://sph.umich.edu/biostat/power-and-sample-size.html

## Common Pitfalls

### Pitfall 1: Using Post-Hoc Power
❌ **Wrong:** Calculate power after null result using observed effect
**Problem:** Will always show low power for null results (circular reasoning)

✅ **Right:** Report sensitivity analysis (what effects were you powered to detect?)

### Pitfall 2: Underpowered Studies
❌ **Wrong:** "We had N=20, but it was a pilot study"
**Problem:** Even pilots should have defensible sample sizes

✅ **Right:** Use sequential design, specify stopping rules, or acknowledge limitation

### Pitfall 3: Overpowered Studies
❌ **Wrong:** N = 1000 to detect tiny effect (d = 0.1)
**Problem:** Wastes resources, detects trivial effects

✅ **Right:** Power for smallest meaningful effect, not just statistical significance

### Pitfall 4: Ignoring Multiple Comparisons
❌ **Wrong:** Power calculation for single test, but running 10 tests
**Problem:** Actual power much lower due to multiple testing correction

✅ **Right:** Adjust alpha or specify primary vs. secondary outcomes

### Pitfall 5: Wrong Test Type
❌ **Wrong:** Power for independent t-test, but actually paired
**Problem:** Wrong sample size (paired designs often need fewer)

✅ **Right:** Match power calculation to actual analysis plan

## Reporting Power Analysis

### In Pre-Registration
```
Sample Size Determination:
- Statistical test: Independent samples t-test (two-tailed)
- Effect size: d = 0.50 (based on [citation])
- Alpha: 0.05
- Power: 0.80
- Required N: 64 per group (128 total)
- Accounting for 15% attrition: 150 recruited (75 per group)
- Power analysis conducted using G*Power 3.1.9.7
```

### In Manuscript Methods
```
We determined our sample size a priori using power analysis. To detect 
a medium effect (Cohen's d = 0.50) with 80% power at α = 0.05 
(two-tailed), we required 64 participants per group (G*Power 3.1). 
Accounting for anticipated 15% attrition, we recruited 150 participants.
```

### In Results (for Null Findings)
```
Although we found no significant effect (p = .23), sensitivity analysis 
shows our study had 80% power to detect effects of d ≥ 0.50 and 55% 
power for d = 0.40. Our 95% CI for the effect size was d = -0.12 to 0.38, 
excluding large effects but not ruling out small-to-medium effects.
```

## Integration with Research Workflow

### With Experiment-Designer Agent
```
Agent uses power-analysis skill to:
1. Calculate required sample size
2. Justify N in protocol
3. Generate power analysis section for pre-registration
4. Create sensitivity analysis plots
```

### With NIH-Validator
```
Validator checks:
- Power ≥ 80%
- Effect size justified with citation
- Attrition accounted for
- Analysis plan matches power calculation
```

### With Statistical Analysis
```
After analysis:
1. Report achieved power or sensitivity analysis
2. Calculate confidence intervals around effect size
3. Interpret results in context of statistical power
```

## Examples

### Example 1: RCT Power Analysis
```
Design: Randomized controlled trial, two groups
Outcome: Depression scores (continuous)
Analysis: Independent samples t-test
Literature: Meta-analysis shows d = 0.55 for CBT vs. waitlist
Conservative estimate: d = 0.50
Alpha: 0.05 (two-tailed)
Power: 0.80

Calculation (G*Power):
Input: t-test, independent samples, d = 0.5, α = 0.05, power = 0.80
Output: N = 64 per group (128 total)

With 20% attrition: 160 recruited (80 per group)
```

### Example 2: Within-Subjects Design
```
Design: Pre-post intervention
Outcome: Anxiety scores
Analysis: Paired t-test
Pilot data: d = 0.70, r = 0.60
Alpha: 0.05
Power: 0.80

Calculation (considering correlation):
N = 19 participants

With 15% attrition: 23 recruited
```

### Example 3: Factorial ANOVA
```
Design: 2x3 factorial (Treatment x Time)
Analysis: Two-way ANOVA
Effect of interest: Interaction (Treatment × Time)
Effect size: f = 0.25 (medium)
Alpha: 0.05
Power: 0.80

Calculation:
N = 50 per cell (300 total for 6 cells)

With 10% attrition: 330 recruited (55 per cell)
```

---

**Last Updated:** 2025-11-09
**Version:** 1.0.0
