---
name: data-science-model-evaluation
description: "Model evaluation and validation: cross-validation, metrics, hyperparameter tuning, and model comparison. Use when assessing model performance, selecting models, or diagnosing modeling issues."
dependsOn: ["@data-science-feature-engineering", "@data-engineering-core"]
---

# Model Evaluation

Use this skill for rigorously assessing model performance, comparing alternatives, and diagnosing issues.

## When to use this skill

- Model training complete — need performance assessment
- Comparing multiple models/algorithms
- Diagnosing overfitting/underfitting
- Hyperparameter tuning
- Production readiness check

## Evaluation workflow

1. **Cross-validation strategy**
   - K-fold (default for most cases)
   - Stratified K-fold (classification with imbalance)
   - TimeSeriesSplit (temporal data)
   - GroupKFold (grouped/clustered data)

2. **Choose appropriate metrics**
   - Classification: accuracy, precision, recall, F1, ROC-AUC, PR-AUC
   - Regression: MAE, RMSE, R², MAPE
   - Ranking: NDCG, MAP
   - Business: custom metrics tied to outcomes

3. **Analyze performance**
   - Cross-validation mean ± std
   - Validation curve (bias-variance tradeoff)
   - Learning curves (data sufficiency)
   - Error analysis by segment

4. **Model comparison**
   - Statistical significance (paired t-test, McNemar)
   - Calibration (for probability outputs)
   - Speed vs accuracy tradeoffs

## Quick tool selection

| Task | Default choice | Notes |
|---|---|---|
| Cross-validation | **sklearn.model_selection** | Standard CV, stratified, time series |
| Metrics | **sklearn.metrics** | Comprehensive metric suite |
| Hyperparameter tuning | **Optuna** or **Ray Tune** | Efficient search algorithms |
| Model comparison | **scikit-learn + statistical tests** | Paired comparisons |
| Experiment tracking | **MLflow** or **Weights & Biases** | Track runs, metrics, artifacts |

## Core implementation rules

### 1) Always use proper validation

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring='roc_auc')
print(f"CV AUC: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

### 2) Match metrics to problem

```python
# Classification with imbalance
from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(y_true, y_pred))
# Focus on F1, precision/recall for minority class

# Regression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

print(f"MAE: {mean_absolute_error(y_true, y_pred):.3f}")
print(f"RMSE: {root_mean_squared_error(y_true, y_pred):.3f}")
```

### 3) Analyze errors systematically

```python
# Error by segment
errors = y_pred != y_true
error_df = X_test[errors]
error_df['true'] = y_true[errors]
error_df['pred'] = y_pred[errors]

# Analyze patterns in errors
print(error_df.groupby('category').size())
```

### 4) Track experiments

```python
import mlflow

with mlflow.start_run():
    mlflow.log_params(params)
    mlflow.log_metrics({'auc': auc, 'f1': f1})
    mlflow.sklearn.log_model(model, 'model')
```

## Common anti-patterns

- ❌ Single train/test split without CV
- ❌ Optimizing wrong metric (accuracy on imbalanced data)
- ❌ Data leakage in preprocessing
- ❌ Not checking calibration for probability outputs
- ❌ Ignoring inference speed/memory constraints
- ❌ No error analysis or debugging bad predictions

## Progressive disclosure

- `../references/cross-validation.md` — CV strategies for different data types
- `../references/metrics-guide.md` — Choosing and interpreting metrics
- `../references/hyperparameter-tuning.md` — Optuna, Ray Tune patterns
- `../references/experiment-tracking.md` — MLflow, W&B setup

## Related skills

- `@data-science-feature-engineering` — Features to evaluate
- `@data-engineering-orchestration` — Production model deployment
- `@data-engineering-observability` — Model monitoring in production

## References

- [sklearn Model Selection](https://scikit-learn.org/stable/modules/model_selection.html)
- [sklearn Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Optuna Documentation](https://optuna.readthedocs.io/)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)
