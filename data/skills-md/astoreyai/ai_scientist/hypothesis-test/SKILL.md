---
name: hypothesis-test
description: "Guide selection and interpretation of statistical hypothesis tests. Use when: (1) Choosing appropriate test for research data, (2) Checking assumptions before analysis, (3) Interpreting test results correctly, (4) Reporting statistical findings, (5) Troubleshooting assumption violations."
allowed-tools: Read, Write
version: 1.0.0
---

# Hypothesis Testing Skill

## Purpose

Guide appropriate selection and interpretation of statistical hypothesis tests for research data analysis.

## Test Selection Decision Tree

### Step 1: How many variables?

**One variable:**
- Categorical → Chi-square goodness of fit
- Continuous → One-sample t-test

**Two variables:**
- Both categorical → Chi-square test of independence
- One categorical, one continuous → T-test or ANOVA
- Both continuous → Correlation or regression

**Three+ variables:**
- Multiple predictors → Multiple regression or ANOVA
- Complex designs → Mixed models or advanced methods

### Step 2: Check assumptions

**For t-tests:**
1. Independence of observations
2. Normality (especially for small N)
3. Homogeneity of variance

**Violations?**
- Non-normal → Mann-Whitney U (non-parametric)
- Unequal variance → Welch's t-test
- Dependent observations → Paired t-test or mixed models

**For ANOVA:**
1. Independence
2. Normality
3. Homogeneity of variance
4. No outliers

**Violations?**
- Non-normal → Kruskal-Wallis test
- Unequal variance → Welch's ANOVA
- Outliers → Robust methods or transformation

### Step 3: Interpret results

Always report:
1. **Test statistic** (t, F, χ²)
2. **Degrees of freedom**
3. **p-value**
4. **Effect size with CI**
5. **Descriptive statistics**

**Example:**
```
Independent samples t-test showed a significant difference between 
groups, t(98) = 3.45, p < .001, d = 0.69, 95% CI [0.29, 1.09]. 
The experimental group (M = 45.2, SD = 8.3) scored higher than 
control (M = 37.8, SD = 9.1).
```

## Common Tests Reference

| Research Question | Test | Assumptions |
|------------------|------|-------------|
| 2 groups, continuous outcome | Independent t-test | Normality, equal variance |
| 2 measurements, same people | Paired t-test | Normality of differences |
| 3+ groups, one factor | One-way ANOVA | Normality, homogeneity |
| 3+ groups, multiple factors | Factorial ANOVA | Normality, homogeneity |
| Relationship between variables | Pearson correlation | Linearity, normality |
| Predict continuous outcome | Linear regression | Linearity, normality of residuals |
| 2 categorical variables | Chi-square test | Expected frequencies ≥5 |
| Ordinal data, 2 groups | Mann-Whitney U | None (non-parametric) |
| Ordinal data, paired | Wilcoxon signed-rank | None (non-parametric) |

## Assumption Checking

### Normality
```
Visual: Q-Q plot, histogram
Statistical: Shapiro-Wilk test (N < 50), Kolmogorov-Smirnov (N ≥ 50)
Guideline: Robust to moderate violations if N ≥ 30
```

### Homogeneity of Variance
```
Visual: Box plots, residual plots
Statistical: Levene's test, Bartlett's test
Guideline: Ratio of largest/smallest variance < 4
```

### Independence
```
Check: Research design, data collection
Red flags: Time series, clustered data, repeated measures
Solution: Use appropriate model (mixed effects, GEE)
```

## Integration

Use with data-analyst agent for complete statistical analysis workflow and experiment-designer agent for planning appropriate analyses.

---

**Version:** 1.0.0
