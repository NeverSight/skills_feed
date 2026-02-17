---
name: shap
description: Use when "SHAP", "Shapley values", "feature importance", "model explainability", or asking about "explain predictions", "interpretable ML", "feature attribution", "waterfall plot", "beeswarm plot", "model debugging"
version: 1.0.0
---

<!-- Adapted from: claude-scientific-skills/scientific-skills/shap -->

# SHAP Model Explainability

Explain ML predictions using Shapley values - feature importance and attribution.

## When to Use

- Explain why a model made specific predictions
- Calculate feature importance with attribution
- Debug model behavior and validate predictions
- Create interpretability plots (waterfall, beeswarm, bar)
- Analyze model fairness and bias

## Quick Start

```python
import shap
import xgboost as xgb

# Train model
model = xgb.XGBClassifier().fit(X_train, y_train)

# Create explainer
explainer = shap.TreeExplainer(model)

# Compute SHAP values
shap_values = explainer(X_test)

# Visualize
shap.plots.beeswarm(shap_values)
```

## Choose Explainer

```python
# Tree-based models (XGBoost, LightGBM, RF) - FAST
explainer = shap.TreeExplainer(model)

# Deep learning (TensorFlow, PyTorch)
explainer = shap.DeepExplainer(model, background_data)

# Linear models
explainer = shap.LinearExplainer(model, X_train)

# Any model (slower but universal)
explainer = shap.KernelExplainer(model.predict, X_train[:100])

# Auto-select best explainer
explainer = shap.Explainer(model)
```

## Compute SHAP Values

```python
# Compute for test set
shap_values = explainer(X_test)

# Access components
shap_values.values      # SHAP values (feature attributions)
shap_values.base_values # Expected model output (baseline)
shap_values.data        # Original feature values
```

## Visualizations

### Global Feature Importance

```python
# Beeswarm - shows distribution and importance
shap.plots.beeswarm(shap_values)

# Bar - clean summary
shap.plots.bar(shap_values)
```

### Individual Predictions

```python
# Waterfall - breakdown of single prediction
shap.plots.waterfall(shap_values[0])

# Force - additive visualization
shap.plots.force(shap_values[0])
```

### Feature Relationships

```python
# Scatter - feature vs SHAP value
shap.plots.scatter(shap_values[:, "feature_name"])

# With interaction coloring
shap.plots.scatter(shap_values[:, "Age"], color=shap_values[:, "Income"])
```

### Heatmap (Multiple Samples)

```python
shap.plots.heatmap(shap_values[:100])
```

## Common Patterns

### Complete Analysis

```python
import shap

# 1. Create explainer and compute
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

# 2. Global importance
shap.plots.beeswarm(shap_values)

# 3. Top feature relationships
shap.plots.scatter(shap_values[:, "top_feature"])

# 4. Individual explanation
shap.plots.waterfall(shap_values[0])
```

### Compare Groups

```python
# Compare feature importance across groups
group_a = X_test['category'] == 'A'
group_b = X_test['category'] == 'B'

shap.plots.bar({
    "Group A": shap_values[group_a],
    "Group B": shap_values[group_b]
})
```

### Debug Errors

```python
# Find misclassified samples
errors = model.predict(X_test) != y_test
error_idx = np.where(errors)[0]

# Explain why they failed
for idx in error_idx[:5]:
    shap.plots.waterfall(shap_values[idx])
```

## Interpret Values

- **Positive SHAP** → Feature pushes prediction higher
- **Negative SHAP** → Feature pushes prediction lower
- **Magnitude** → Strength of impact
- **Sum of SHAP values** = Prediction - Baseline

```
Baseline: 0.30
Age: +0.15
Income: +0.10
Education: -0.05
Prediction: 0.30 + 0.15 + 0.10 - 0.05 = 0.50
```

## Best Practices

1. **Use TreeExplainer** for tree models (fast, exact)
2. **Use 100-1000 background samples** for KernelExplainer
3. **Start global** (beeswarm) then go **local** (waterfall)
4. **Check model output type** (probability vs log-odds)
5. **Validate with domain knowledge**

## vs Alternatives

| Tool | Best For |
|------|----------|
| **SHAP** | Theoretically grounded, all model types |
| LIME | Quick local explanations |
| Feature Importance | Simple tree-based importance |

## Resources

- Docs: <https://shap.readthedocs.io/>
- Paper: Lundberg & Lee (2017) "A Unified Approach to Interpreting Model Predictions"
