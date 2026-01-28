---
name: symmetry-validation-suite
description: Use when you need to empirically test whether hypothesized symmetries actually hold in your data or model. Invoke when user mentions testing invariance, validating equivariance, checking if symmetry assumptions are correct, debugging symmetry-related model failures, or needs data-driven validation before committing to equivariant architecture. Provides test protocols and metrics.
---

# Symmetry Validation Suite

## What Is It?

This skill provides **empirical tests to validate symmetry hypotheses**. Before committing to an equivariant architecture, you should verify that your claimed symmetries actually hold. This skill gives you concrete testing protocols and metrics.

**Why validate?** Wrong symmetry assumptions hurt model performance. Too much symmetry over-constrains; missing symmetry wastes capacity.

## Workflow

Copy this checklist and track your progress:

```
Symmetry Validation Progress:
- [ ] Step 1: List symmetry hypotheses to test
- [ ] Step 2: Design transformation test sets
- [ ] Step 3: Run invariance/equivariance tests
- [ ] Step 4: Verify group structure
- [ ] Step 5: Analyze data distribution under transforms
- [ ] Step 6: Document validation results
```

**Step 1: List symmetry hypotheses to test**

Gather candidate symmetries from previous discovery work. For each, document: the transformation type, whether invariance or equivariance is expected, and confidence level. Prioritize testing low-confidence hypotheses. If no hypotheses exist, work with user through domain analysis to identify candidate symmetries first.

**Step 2: Design transformation test sets**

For each symmetry, create test protocol: Sample representative inputs from data distribution. Define transformation sampling strategy (random rotations, all permutations, etc.). Determine appropriate sample sizes for statistical significance. Consider edge cases and boundary conditions. See [Transformation Sampling](#transformation-sampling) for guidance. For detailed methodology, consult [Methodology Details](./resources/methodology.md).

**Step 3: Run invariance/equivariance tests**

For invariance testing: Apply transformation T to input x, compute outputs f(x) and f(T(x)), measure error ||f(T(x)) - f(x)||. For equivariance testing: Compute f(T(x)) and T'(f(x)) where T' is the output transformation, measure error ||f(T(x)) - T'(f(x))||. Use [Testing Protocols](#testing-protocols) for implementation details. Aggregate across samples and compute statistics. For complete code examples, see [Test Implementation Examples](./resources/test-examples.md).

**Step 4: Verify group structure**

Check that claimed transformations form a valid group: Test closure (composition of two transforms is a transform). Test associativity. Verify identity element exists. Verify inverses exist. For Lie groups, check that generators close under commutator. See [Group Structure Tests](#group-structure-tests).

**Step 5: Analyze data distribution under transforms**

Check if transformed data stays in-distribution: Apply transforms to training data. Compare statistics of original vs transformed data. Check for distributional shift that might break assumptions. Identify transformation ranges that maintain validity. This catches "approximate symmetry" cases where symmetry holds only within bounds.

**Step 6: Document validation results**

Create validation report using [Output Template](#output-template). For each symmetry: state hypothesis, test methodology, quantitative results, pass/fail decision. Recommend whether to use hard equivariance constraint, soft constraint (regularization), data augmentation, or no symmetry at all. Quality criteria for this output are defined in [Quality Rubric](./resources/evaluators/rubric_validation.json).

## Testing Protocols

### Invariance Test Protocol

```python
def test_invariance(model, data_samples, transform_fn, n_transforms=100):
    """
    Test if model output is invariant to transformations.

    Returns:
        mean_error: Average ||f(T(x)) - f(x)||
        max_error: Maximum error observed
        pass_rate: Fraction with error < threshold
    """
    errors = []
    for x in data_samples:
        y_orig = model(x)
        for _ in range(n_transforms):
            x_transformed = transform_fn(x)
            y_transformed = model(x_transformed)
            error = norm(y_transformed - y_orig)
            errors.append(error)

    return {
        'mean_error': mean(errors),
        'max_error': max(errors),
        'std_error': std(errors),
        'pass_rate': sum(e < threshold for e in errors) / len(errors)
    }
```

### Equivariance Test Protocol

```python
def test_equivariance(model, data_samples, input_transform, output_transform):
    """
    Test if f(T(x)) = T'(f(x)) for equivariance.

    Returns:
        mean_error: Average ||f(T(x)) - T'(f(x))||
        relative_error: Error normalized by output magnitude
    """
    errors = []
    for x in data_samples:
        # Method 1: Transform then model
        x_T = input_transform(x)
        y1 = model(x_T)

        # Method 2: Model then transform
        y = model(x)
        y2 = output_transform(y)

        error = norm(y1 - y2)
        relative = error / (norm(y2) + eps)
        errors.append({'absolute': error, 'relative': relative})

    return aggregate_stats(errors)
```

### Statistical Significance

For reliable results:
- Use at least 100 data samples
- Test at least 50 random transformations per sample
- Report mean, std, and percentiles (95th, 99th)
- Set threshold based on numerical precision expectations
- Use hypothesis testing if comparing methods

## Transformation Sampling

### Continuous Groups

| Group | Sampling Strategy |
|-------|-------------------|
| SO(2) | Uniform random angles θ ∈ [0, 2π) |
| SO(3) | Uniform random quaternions or axis-angle |
| SE(3) | Combine SO(3) rotation + uniform translation |
| Translations | Uniform within expected data range |

### Discrete Groups

| Group | Sampling Strategy |
|-------|-------------------|
| Cₙ | All n rotations |
| Dₙ | All 2n elements (rotations + reflections) |
| Sₙ | Random permutations (full enumeration if n ≤ 6) |

## Group Structure Tests

### Closure Test

```
For random g₁, g₂ ∈ G:
  Compute g₃ = g₁ · g₂
  Verify g₃ ∈ G (within numerical tolerance)
```

### Associativity Test

```
For random g₁, g₂, g₃ ∈ G:
  Compute (g₁ · g₂) · g₃
  Compute g₁ · (g₂ · g₃)
  Verify equality (within tolerance)
```

### Identity and Inverse Test

```
For random g ∈ G:
  Verify g · e = e · g = g
  Find g⁻¹ and verify g · g⁻¹ = e
```

## Interpretation Guide

### Error Thresholds

| Error Level | Interpretation |
|-------------|----------------|
| < 1e-6 | Exact symmetry (numerical precision) |
| 1e-6 to 1e-3 | Strong approximate symmetry |
| 1e-3 to 0.01 | Weak approximate symmetry |
| > 0.01 | Symmetry likely doesn't hold |

### Decision Matrix

| Validation Result | Recommendation |
|-------------------|----------------|
| Exact symmetry confirmed | Use hard equivariant constraint |
| Strong approximate | Use equivariant architecture |
| Weak approximate | Consider soft constraint or augmentation |
| Symmetry broken | Don't enforce this symmetry |
| Partial symmetry | Use conditional/local equivariance |

## Output Template

```
SYMMETRY VALIDATION REPORT
==========================

Tested Symmetries:

1. [Transformation]: [Invariance/Equivariance]
   - Sample size: [N samples × M transforms]
   - Mean error: [value]
   - Max error: [value]
   - Pass rate: [%] at threshold [value]
   - RESULT: [PASS/FAIL/PARTIAL]
   - Recommendation: [Hard constraint/Soft/Augmentation/None]

2. [Transformation]: [Invariance/Equivariance]
   ...

Group Structure:
- Closure: [PASS/FAIL]
- Associativity: [PASS/FAIL]
- Identity/Inverse: [PASS/FAIL]

Distribution Analysis:
- Transform range where symmetry holds: [bounds]
- Detected breaking factors: [list]

SUMMARY:
- Confirmed symmetries: [list]
- Rejected symmetries: [list]
- Proceed to architecture design with: [group specification]
```
