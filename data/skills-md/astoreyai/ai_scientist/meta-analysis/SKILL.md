---
name: meta-analysis
description: "Conduct quantitative synthesis through meta-analysis. Use when: (1) Combining effect sizes across studies, (2) Systematic review synthesis, (3) Calculating summary effects, (4) Assessing heterogeneity."
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# Meta-Analysis Skill

## Purpose
Quantitatively synthesize results across multiple studies.

## Meta-Analysis Steps

**1. Extract Effect Sizes**
- Convert to common metric (d, OR, RR)
- Calculate standard errors

**2. Choose Model**
- Fixed-effect: Assumes single true effect
- Random-effects: Allows heterogeneity

**3. Pool Results**
- Weight studies (inverse variance)
- Calculate summary effect
- 95% confidence interval

**4. Assess Heterogeneity**
- I² statistic (0-100%)
  - 0-40%: Low heterogeneity
  - 40-75%: Moderate
  - 75-100%: High
- Q test (statistical significance)

**5. Investigate Heterogeneity**
- Subgroup analysis
- Meta-regression
- Sensitivity analysis

**6. Publication Bias**
- Funnel plot
- Egger's test
- Trim-and-fill

## Reporting

**Example:**
"Meta-analysis of 15 RCTs (N=1,234) showed a moderate effect, g=0.52, 95% CI[0.38, 0.66], p<.001. Heterogeneity was moderate, I²=58%, suggesting variability in effects."

---
**Version:** 1.0.0
