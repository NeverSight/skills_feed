---
name: sensitivity-analysis
description: "Conduct sensitivity analyses to test robustness of findings. Use when: (1) Testing assumption violations, (2) Meta-analysis robustness, (3) Handling missing data, (4) Examining outliers."
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# Sensitivity Analysis Skill

## Purpose
Test whether findings are robust to analytical decisions and assumptions.

## Types of Sensitivity Analyses

**1. Exclusion Analyses**
- Remove outliers
- Remove high risk-of-bias studies
- One-study-removed analysis

**2. Analytical Decisions**
- Different statistical tests
- Parametric vs non-parametric
- Different transformations

**3. Missing Data**
- Complete case analysis
- Best-case scenario
- Worst-case scenario
- Multiple imputation

**4. Measurement**
- Different outcome definitions
- Different time points
- Alternative scoring methods

## Interpretation

**Robust Findings:**
- Results consistent across analyses
- Conclusions unchanged
- High confidence

**Sensitive Findings:**
- Results vary by decision
- Interpret with caution
- Report uncertainty

## Example

"Results were robust to removal of the highest risk-of-bias study (d=0.48 vs d=0.52) and remained significant when using non-parametric tests (p=.002)."

---
**Version:** 1.0.0
