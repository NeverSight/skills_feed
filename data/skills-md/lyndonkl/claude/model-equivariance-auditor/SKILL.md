---
name: model-equivariance-auditor
description: Use when you have implemented an equivariant model and need to verify it correctly respects the intended symmetries. Invoke when user mentions testing model equivariance, debugging symmetry bugs, verifying implementation correctness, checking if model is actually equivariant, or diagnosing why equivariant model isn't working. Provides verification tests and debugging guidance.
---

# Model Equivariance Auditor

## What Is It?

This skill helps you **verify that your implemented model correctly respects its intended symmetries**. Even with equivariant libraries, implementation bugs can break equivariance. This skill provides systematic verification tests and debugging strategies.

**Why audit?** A model that claims equivariance but isn't will train poorly and give inconsistent predictions. Catching these bugs early saves debugging time.

## Workflow

Copy this checklist and track your progress:

```
Equivariance Audit Progress:
- [ ] Step 1: Gather model and symmetry specification
- [ ] Step 2: Run numerical equivariance tests
- [ ] Step 3: Test individual layers
- [ ] Step 4: Check gradient equivariance
- [ ] Step 5: Identify and diagnose failures
- [ ] Step 6: Document audit results
```

**Step 1: Gather model and symmetry specification**

Collect: the implemented model, the intended symmetry group, whether each output should be invariant or equivariant, the transformation functions for input and output spaces. Review the architecture specification from design phase. Clarify ambiguities with user before testing.

**Step 2: Run numerical equivariance tests**

Execute end-to-end equivariance tests using [Test Implementation](#test-implementation). For invariance: verify ||f(T(x)) - f(x)|| < ε. For equivariance: verify ||f(T(x)) - T'(f(x))|| < ε. Use multiple random inputs and transformations. Record error statistics. See [Error Interpretation](#error-interpretation) for thresholds. For ready-to-use test code, see [Test Code Templates](./resources/test-templates.md).

**Step 3: Test individual layers**

If end-to-end test fails, isolate the problem by testing layers individually. For each layer: freeze other layers, test equivariance of that layer alone. This identifies which layer breaks equivariance. Use [Layer-wise Testing](#layer-wise-testing) protocol. Check nonlinearities, normalizations, and custom operations especially carefully.

**Step 4: Check gradient equivariance**

Verify that gradients also respect equivariance (important for training). Compute gradients at x and T(x). Check that gradients transform appropriately. Gradient bugs can cause training to "unlearn" equivariance. See [Gradient Testing](#gradient-testing).

**Step 5: Identify and diagnose failures**

If tests fail, use [Common Failure Modes](#common-failure-modes) to diagnose. Check: non-equivariant nonlinearities, batch normalization issues, incorrect output transformation, numerical precision problems, implementation bugs in custom layers. Provide specific fix recommendations. For step-by-step troubleshooting, consult [Debugging Guide](./resources/debugging.md).

**Step 6: Document audit results**

Create audit report using [Output Template](#output-template). Include: pass/fail for each test, error magnitudes, identified issues, and recommendations. Distinguish between: exact equivariance (numerical precision), approximate equivariance (acceptable error), and broken equivariance (needs fixing). For detailed audit methodology, see [Methodology Details](./resources/methodology.md). Quality criteria for this output are defined in [Quality Rubric](./resources/evaluators/rubric_audit.json).

## Test Implementation

### End-to-End Equivariance Test

```python
import torch

def test_model_equivariance(model, x, input_transform, output_transform,
                            n_tests=100, tol=1e-5):
    """
    Test if model is equivariant: f(T(x)) ≈ T'(f(x))

    Args:
        model: The neural network to test
        x: Sample input tensor
        input_transform: Function that transforms input
        output_transform: Function that transforms output
        n_tests: Number of random transformations to test
        tol: Error tolerance

    Returns:
        dict with test results
    """
    model.eval()
    errors = []

    with torch.no_grad():
        for _ in range(n_tests):
            # Generate random transformation
            T = sample_random_transform()

            # Method 1: Transform input, then apply model
            x_transformed = input_transform(x, T)
            y1 = model(x_transformed)

            # Method 2: Apply model, then transform output
            y = model(x)
            y2 = output_transform(y, T)

            # Compute error
            error = torch.norm(y1 - y2).item()
            relative_error = error / (torch.norm(y2).item() + 1e-8)
            errors.append({
                'absolute': error,
                'relative': relative_error
            })

    return {
        'mean_absolute': np.mean([e['absolute'] for e in errors]),
        'max_absolute': np.max([e['absolute'] for e in errors]),
        'mean_relative': np.mean([e['relative'] for e in errors]),
        'max_relative': np.max([e['relative'] for e in errors]),
        'pass': all(e['relative'] < tol for e in errors)
    }
```

### Invariance Test (Simpler Case)

```python
def test_model_invariance(model, x, transform, n_tests=100, tol=1e-5):
    """Test if model output is invariant to transformations."""
    model.eval()
    errors = []

    with torch.no_grad():
        y_original = model(x)

        for _ in range(n_tests):
            T = sample_random_transform()
            x_transformed = transform(x, T)
            y_transformed = model(x_transformed)

            error = torch.norm(y_transformed - y_original).item()
            errors.append(error)

    return {
        'mean_error': np.mean(errors),
        'max_error': np.max(errors),
        'pass': max(errors) < tol
    }
```

## Layer-wise Testing

### Protocol

```python
def test_layer_equivariance(layer, x, input_transform, output_transform):
    """Test a single layer for equivariance."""
    layer.eval()

    with torch.no_grad():
        T = sample_random_transform()

        # Transform then layer
        y1 = layer(input_transform(x, T))

        # Layer then transform
        y2 = output_transform(layer(x), T)

        error = torch.norm(y1 - y2).item()

    return {
        'layer': layer.__class__.__name__,
        'error': error,
        'pass': error < tolerance
    }

def audit_all_layers(model, x, transforms):
    """Test each layer individually."""
    results = []

    for name, layer in model.named_modules():
        if is_testable_layer(layer):
            result = test_layer_equivariance(layer, x, *transforms)
            result['name'] = name
            results.append(result)

    return results
```

### What to Test Per Layer

| Layer Type | What to Check |
|------------|---------------|
| Convolution | Kernel equivariance |
| Nonlinearity | Should preserve equivariance |
| Normalization | Often breaks equivariance |
| Pooling | Correct aggregation |
| Linear | Weight sharing patterns |
| Attention | Permutation equivariance |

## Gradient Testing

### Why Test Gradients?

Forward pass can be equivariant while backward pass is not. This causes:
- Training instability
- Model "unlearning" equivariance
- Inconsistent optimization

### Gradient Equivariance Test

```python
def test_gradient_equivariance(model, x, loss_fn, transform, tol=1e-4):
    """Test if gradients respect equivariance."""
    model.train()

    # Gradients at original input
    x1 = x.clone().requires_grad_(True)
    y1 = model(x1)
    loss1 = loss_fn(y1)
    loss1.backward()
    grad1 = x1.grad.clone()

    # Gradients at transformed input
    model.zero_grad()
    T = sample_random_transform()
    x2 = transform(x.clone(), T).requires_grad_(True)
    y2 = model(x2)
    loss2 = loss_fn(y2)
    loss2.backward()
    grad2 = x2.grad.clone()

    # Transform grad1 and compare to grad2
    grad1_transformed = transform_gradient(grad1, T)
    error = torch.norm(grad2 - grad1_transformed).item()

    return {'error': error, 'pass': error < tol}
```

## Error Interpretation

### Error Thresholds

| Error Level | Interpretation | Action |
|-------------|----------------|--------|
| < 1e-6 | Perfect (float32 precision) | Pass |
| 1e-6 to 1e-4 | Excellent (acceptable) | Pass |
| 1e-4 to 1e-2 | Approximate equivariance | Investigate |
| > 1e-2 | Broken equivariance | Fix required |

### Relative vs Absolute Error

- **Absolute error**: Raw difference magnitude
- **Relative error**: Normalized by output magnitude

Use relative error when output magnitudes vary. Use absolute when comparing to numerical precision.

## Common Failure Modes

### 1. Non-Equivariant Nonlinearity

**Symptom**: Error increases after nonlinearity layers
**Cause**: Using ReLU, sigmoid on equivariant features
**Fix**: Use gated nonlinearities, norm-based, or restrict to invariant features

### 2. Batch Normalization Breaking Equivariance

**Symptom**: Error varies with batch composition
**Cause**: BN computes different stats for different orientations
**Fix**: Use LayerNorm, GroupNorm, or equivariant batch norm

### 3. Incorrect Output Transformation

**Symptom**: Test fails even for identity transform
**Cause**: output_transform doesn't match model output type
**Fix**: Verify output transformation matches layer output representation

### 4. Numerical Precision Issues

**Symptom**: Small but non-zero error everywhere
**Cause**: Floating point accumulation, interpolation
**Fix**: Use float64 for testing, accept small tolerance

### 5. Custom Layer Bug

**Symptom**: Error isolated to specific layer
**Cause**: Implementation error in custom equivariant layer
**Fix**: Review layer implementation against equivariance constraints

### 6. Padding/Boundary Effects

**Symptom**: Error higher near edges
**Cause**: Padding doesn't respect symmetry
**Fix**: Use circular padding or handle boundaries explicitly

## Output Template

```
MODEL EQUIVARIANCE AUDIT REPORT
===============================

Model: [Model name/description]
Intended Symmetry: [Group]
Symmetry Type: [Invariant/Equivariant]

END-TO-END TESTS:
-----------------
Test samples: [N]
Transformations tested: [M]

Invariance/Equivariance Error:
- Mean absolute: [value]
- Max absolute: [value]
- Mean relative: [value]
- Max relative: [value]
- RESULT: [PASS/FAIL]

LAYER-WISE ANALYSIS:
--------------------
[For each layer]
- Layer: [name]
- Error: [value]
- Result: [PASS/FAIL]

GRADIENT TEST:
--------------
- Gradient equivariance error: [value]
- RESULT: [PASS/FAIL]

IDENTIFIED ISSUES:
------------------
1. [Issue description]
   - Location: [layer/component]
   - Severity: [High/Medium/Low]
   - Recommended fix: [description]

OVERALL VERDICT: [PASS/FAIL/NEEDS_ATTENTION]

Recommendations:
- [List of actions needed]
```
