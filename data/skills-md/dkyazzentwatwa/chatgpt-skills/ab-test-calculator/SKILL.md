---
name: ab-test-calculator
description: Calculate statistical significance for A/B tests. Sample size estimation, power analysis, and conversion rate comparisons with confidence intervals.
---

# A/B Test Calculator

Statistical significance testing for A/B experiments with power analysis and sample size estimation.

## Features

- **Significance Testing**: Chi-square, Z-test, T-test for conversions
- **Sample Size Estimation**: Calculate required samples for desired power
- **Power Analysis**: Determine test power given sample size
- **Confidence Intervals**: Calculate CIs for conversion rates
- **Multiple Variants**: Support A/B/n testing
- **Bayesian Analysis**: Probability to beat baseline

## Quick Start

```python
from ab_test_calc import ABTestCalculator

calc = ABTestCalculator()

# Test significance
result = calc.test_significance(
    control_visitors=10000,
    control_conversions=500,
    variant_visitors=10000,
    variant_conversions=550
)

print(f"Significant: {result['significant']}")
print(f"P-value: {result['p_value']:.4f}")
print(f"Lift: {result['lift']:.2%}")
```

## CLI Usage

```bash
# Test significance
python ab_test_calc.py --test 10000 500 10000 550

# Calculate sample size
python ab_test_calc.py --sample-size --baseline 0.05 --mde 0.10 --power 0.8

# Power analysis
python ab_test_calc.py --power-analysis --baseline 0.05 --mde 0.10 --samples 5000

# Bayesian analysis
python ab_test_calc.py --bayesian 10000 500 10000 550

# Multiple variants
python ab_test_calc.py --test-multi 10000 500 10000 550 10000 520
```

## API Reference

### ABTestCalculator Class

```python
class ABTestCalculator:
    def __init__(self, alpha: float = 0.05)

    # Significance testing
    def test_significance(self, control_visitors: int, control_conversions: int,
                         variant_visitors: int, variant_conversions: int,
                         test: str = "chi_square") -> dict

    # Sample size calculation
    def calculate_sample_size(self, baseline_rate: float,
                             minimum_detectable_effect: float,
                             power: float = 0.8,
                             alpha: float = 0.05) -> dict

    # Power analysis
    def calculate_power(self, baseline_rate: float,
                       minimum_detectable_effect: float,
                       sample_size: int,
                       alpha: float = 0.05) -> dict

    # Confidence interval
    def confidence_interval(self, visitors: int, conversions: int,
                           confidence: float = 0.95) -> dict

    # Bayesian analysis
    def bayesian_analysis(self, control_visitors: int, control_conversions: int,
                         variant_visitors: int, variant_conversions: int,
                         simulations: int = 100000) -> dict

    # Multiple variants
    def test_multiple_variants(self, control: tuple, variants: list,
                              correction: str = "bonferroni") -> dict

    # Duration estimation
    def estimate_duration(self, daily_visitors: int, baseline_rate: float,
                         minimum_detectable_effect: float,
                         power: float = 0.8) -> dict
```

## Test Methods

### Chi-Square Test (Default)
Best for comparing conversion rates between groups.

```python
result = calc.test_significance(
    control_visitors=10000,
    control_conversions=500,
    variant_visitors=10000,
    variant_conversions=550,
    test="chi_square"
)
```

### Z-Test for Proportions
Good for large sample sizes.

```python
result = calc.test_significance(
    control_visitors=10000,
    control_conversions=500,
    variant_visitors=10000,
    variant_conversions=550,
    test="z_test"
)
```

## Sample Size Estimation

Calculate the number of visitors needed per variant:

```python
result = calc.calculate_sample_size(
    baseline_rate=0.05,          # Current conversion rate (5%)
    minimum_detectable_effect=0.10,  # 10% relative improvement
    power=0.8,                   # 80% power
    alpha=0.05                   # 5% significance level
)

# Returns:
{
    "sample_size_per_variant": 31234,
    "total_sample_size": 62468,
    "baseline_rate": 0.05,
    "expected_variant_rate": 0.055,
    "minimum_detectable_effect": 0.10,
    "power": 0.8,
    "alpha": 0.05
}
```

## Power Analysis

Calculate the probability of detecting an effect:

```python
result = calc.calculate_power(
    baseline_rate=0.05,
    minimum_detectable_effect=0.10,
    sample_size=25000,
    alpha=0.05
)

# Returns:
{
    "power": 0.72,
    "interpretation": "72% chance of detecting the effect if it exists"
}
```

## Bayesian Analysis

Get probability that variant beats control:

```python
result = calc.bayesian_analysis(
    control_visitors=10000,
    control_conversions=500,
    variant_visitors=10000,
    variant_conversions=550
)

# Returns:
{
    "prob_variant_better": 0.9523,
    "prob_control_better": 0.0477,
    "expected_lift": 0.098,
    "credible_interval_95": [0.02, 0.18]
}
```

## Multiple Variant Testing

Test multiple variants with correction for multiple comparisons:

```python
result = calc.test_multiple_variants(
    control=(10000, 500),          # (visitors, conversions)
    variants=[
        (10000, 550),              # Variant A
        (10000, 520),              # Variant B
        (10000, 480)               # Variant C
    ],
    correction="bonferroni"        # or "holm", "none"
)

# Returns:
{
    "control": {"visitors": 10000, "conversions": 500, "rate": 0.05},
    "variants": [
        {"visitors": 10000, "conversions": 550, "rate": 0.055,
         "lift": 0.10, "p_value": 0.012, "significant": True},
        ...
    ],
    "winner": "Variant A",
    "correction_method": "bonferroni"
}
```

## Output Format

### Significance Test Result

```python
{
    "significant": True,
    "p_value": 0.0234,
    "control_rate": 0.05,
    "variant_rate": 0.055,
    "lift": 0.10,
    "lift_absolute": 0.005,
    "confidence_interval": {
        "lower": 0.02,
        "upper": 0.18
    },
    "test_method": "chi_square",
    "alpha": 0.05,
    "recommendation": "Variant shows significant improvement"
}
```

## Example Workflows

### Pre-Test Planning

```python
calc = ABTestCalculator()

# 1. Estimate required sample size
sample = calc.calculate_sample_size(
    baseline_rate=0.03,     # Current 3% conversion
    minimum_detectable_effect=0.15,  # Want to detect 15% lift
    power=0.8
)
print(f"Need {sample['sample_size_per_variant']} visitors per variant")

# 2. Estimate test duration
duration = calc.estimate_duration(
    daily_visitors=5000,
    baseline_rate=0.03,
    minimum_detectable_effect=0.15
)
print(f"Test will take ~{duration['days']} days")
```

### Post-Test Analysis

```python
calc = ABTestCalculator()

# 1. Test significance
result = calc.test_significance(
    control_visitors=15000,
    control_conversions=450,
    variant_visitors=15000,
    variant_conversions=525
)

# 2. Get Bayesian probability
bayes = calc.bayesian_analysis(15000, 450, 15000, 525)

print(f"P-value: {result['p_value']:.4f}")
print(f"Lift: {result['lift']:.2%}")
print(f"Probability variant wins: {bayes['prob_variant_better']:.1%}")
```

## Dependencies

- scipy>=1.10.0
- numpy>=1.24.0
- statsmodels>=0.14.0
