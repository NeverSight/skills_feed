---
name: debug:scikit-learn
description: Debug Scikit-learn issues systematically. Use when encountering model errors like NotFittedError, shape mismatches between train and test data, NaN/infinity value errors, pipeline configuration issues, convergence warnings from optimizers, cross-validation failures due to class imbalance, data leakage causing suspiciously high scores, or preprocessing errors with ColumnTransformer and feature alignment.
---

# Scikit-learn Debugging Guide

This guide provides a systematic approach to debugging Scikit-learn machine learning code. Follow these phases to identify and resolve issues efficiently.

## Common Error Patterns

### 1. ValueError: Shapes Not Aligned
```python
# Error: ValueError: shapes (100,5) and (4,) not aligned
# Cause: Feature count mismatch between train and test data

# Debug steps:
print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"Feature names train: {X_train.columns.tolist() if hasattr(X_train, 'columns') else 'N/A'}")
print(f"Feature names test: {X_test.columns.tolist() if hasattr(X_test, 'columns') else 'N/A'}")

# Common fixes:
# 1. Ensure same preprocessing on train and test
# 2. Use Pipeline to encapsulate all transformations
# 3. Check for columns dropped during one-hot encoding
```

### 2. NotFittedError
```python
# Error: NotFittedError: This StandardScaler instance is not fitted yet
# Cause: Calling transform() or predict() before fit()

from sklearn.utils.validation import check_is_fitted

# Check if model is fitted:
try:
    check_is_fitted(model)
    print("Model is fitted")
except Exception as e:
    print(f"Model not fitted: {e}")

# Debug fitted attributes:
print(f"Model attributes: {[a for a in dir(model) if a.endswith('_') and not a.startswith('_')]}")

# Common fixes:
# 1. Call fit() before transform() or predict()
# 2. Use fit_transform() for training data
# 3. Ensure Pipeline is fitted before prediction
```

### 3. NaN Values in Input
```python
# Error: ValueError: Input contains NaN, infinity or a value too large
# Cause: Missing or infinite values in data

import numpy as np
import pandas as pd

# Diagnose NaN issues:
def diagnose_nan_issues(X, name="X"):
    if isinstance(X, pd.DataFrame):
        nan_counts = X.isna().sum()
        print(f"{name} NaN counts per column:\n{nan_counts[nan_counts > 0]}")
        print(f"{name} total NaN: {X.isna().sum().sum()}")
    else:
        print(f"{name} contains NaN: {np.isnan(X).any()}")
        print(f"{name} contains inf: {np.isinf(X).any()}")
        print(f"{name} NaN count: {np.isnan(X).sum()}")

diagnose_nan_issues(X_train, "X_train")
diagnose_nan_issues(X_test, "X_test")

# Common fixes:
from sklearn.impute import SimpleImputer

# Option 1: Remove rows with NaN
X_clean = X[~np.isnan(X).any(axis=1)]

# Option 2: Impute missing values
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X_train)

# Option 3: Replace infinity
X_train = np.clip(X_train, -1e10, 1e10)
```

### 4. Feature Mismatch Train/Test
```python
# Error: ValueError: X has 10 features, but model expects 12 features
# Cause: Different preprocessing on train vs test

# Debug feature alignment:
def debug_feature_mismatch(X_train, X_test, model=None):
    print(f"Train features: {X_train.shape[1]}")
    print(f"Test features: {X_test.shape[1]}")

    if model and hasattr(model, 'n_features_in_'):
        print(f"Model expects: {model.n_features_in_} features")

    if hasattr(X_train, 'columns') and hasattr(X_test, 'columns'):
        train_cols = set(X_train.columns)
        test_cols = set(X_test.columns)
        print(f"In train but not test: {train_cols - test_cols}")
        print(f"In test but not train: {test_cols - train_cols}")

# Fix: Use ColumnTransformer with remainder='passthrough' or 'drop'
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='drop'  # Explicitly handle unknown columns
)
```

### 5. Cross-Validation Issues
```python
# Error: ValueError: Cannot have number of splits n_splits=5 greater than samples
# Cause: Too few samples for specified fold count

from sklearn.model_selection import cross_val_score, StratifiedKFold

# Debug cross-validation setup:
def debug_cv_setup(X, y, cv=5):
    print(f"Total samples: {len(X)}")
    print(f"CV folds requested: {cv}")
    print(f"Min samples per fold: {len(X) // cv}")

    if hasattr(y, 'value_counts'):
        print(f"Class distribution:\n{y.value_counts()}")
    else:
        unique, counts = np.unique(y, return_counts=True)
        print(f"Class distribution: {dict(zip(unique, counts))}")

# Fix: Use appropriate CV strategy
# For small datasets:
from sklearn.model_selection import LeaveOneOut, RepeatedStratifiedKFold

# For imbalanced data:
cv = StratifiedKFold(n_splits=min(5, y.value_counts().min()))

# For time series:
from sklearn.model_selection import TimeSeriesSplit
cv = TimeSeriesSplit(n_splits=5)
```

### 6. Pipeline Configuration Errors
```python
# Error: TypeError: All estimators should implement fit and transform
# Cause: Final estimator in Pipeline doesn't have transform method

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Debug pipeline structure:
def debug_pipeline(pipe):
    print("Pipeline steps:")
    for name, step in pipe.named_steps.items():
        has_fit = hasattr(step, 'fit')
        has_transform = hasattr(step, 'transform')
        has_predict = hasattr(step, 'predict')
        print(f"  {name}: fit={has_fit}, transform={has_transform}, predict={has_predict}")
        print(f"    Type: {type(step).__name__}")
        if hasattr(step, 'get_params'):
            params = step.get_params()
            print(f"    Params: {params}")

debug_pipeline(my_pipeline)

# Common fixes:
# 1. Only the last step can be a predictor (no transform)
# 2. Intermediate steps must have fit_transform or fit + transform
# 3. Use 'passthrough' for no-op steps
```

### 7. Convergence Warnings
```python
# Warning: ConvergenceWarning: lbfgs failed to converge
# Cause: Optimization didn't reach convergence criteria

from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import ConvergenceWarning
import warnings

# Capture and analyze warnings:
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    model.fit(X_train, y_train)

    for warning in w:
        if issubclass(warning.category, ConvergenceWarning):
            print(f"Convergence issue: {warning.message}")

# Common fixes:
# 1. Increase max_iter
model = LogisticRegression(max_iter=1000)

# 2. Scale features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Try different solver
model = LogisticRegression(solver='saga', max_iter=1000)

# 4. Adjust tolerance
model = LogisticRegression(tol=1e-3)
```

### 8. Data Leakage Detection
```python
# Symptom: Suspiciously high cross-validation scores (>0.99)
# Cause: Information from test set leaking into training

# Debug data leakage:
def check_for_leakage(X, y, model, cv=5):
    from sklearn.model_selection import cross_val_score

    scores = cross_val_score(model, X, y, cv=cv)
    print(f"CV scores: {scores}")
    print(f"Mean: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

    if scores.mean() > 0.99:
        print("WARNING: Suspiciously high scores - check for data leakage!")
        print("Common causes:")
        print("  - Target variable encoded in features")
        print("  - Future information in time series")
        print("  - Preprocessing before train-test split")

    return scores

# Fix: Use Pipeline to prevent leakage
from sklearn.pipeline import Pipeline

# WRONG - leakage:
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)  # Fitted on ALL data
# X_train, X_test = train_test_split(X_scaled, ...)

# CORRECT - no leakage:
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
# fit_transform only sees training data in each CV fold
scores = cross_val_score(pipe, X, y, cv=5)
```

## Debugging Tools

### Model Inspection
```python
# Get all model parameters
print(model.get_params())

# Get only non-default parameters
from sklearn.utils._pprint import _EstimatorPrettyPrinter
print(model)

# Check fitted attributes (attributes ending with _)
fitted_attrs = [a for a in dir(model) if a.endswith('_') and not a.startswith('__')]
for attr in fitted_attrs:
    val = getattr(model, attr)
    if hasattr(val, 'shape'):
        print(f"{attr}: shape={val.shape}")
    else:
        print(f"{attr}: {type(val).__name__}")
```

### Cross-Validation Diagnostics
```python
from sklearn.model_selection import cross_val_score, cross_validate

# Basic CV score
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"CV Accuracy: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

# Detailed CV with multiple metrics
cv_results = cross_validate(
    model, X, y, cv=5,
    scoring=['accuracy', 'precision', 'recall', 'f1'],
    return_train_score=True,
    return_estimator=True
)

for metric in ['accuracy', 'precision', 'recall', 'f1']:
    train_key = f'train_{metric}'
    test_key = f'test_{metric}'
    print(f"{metric}:")
    print(f"  Train: {cv_results[train_key].mean():.4f}")
    print(f"  Test:  {cv_results[test_key].mean():.4f}")
    print(f"  Gap:   {cv_results[train_key].mean() - cv_results[test_key].mean():.4f}")
```

### Learning Curve Analysis
```python
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

def plot_learning_curve(estimator, X, y, cv=5, train_sizes=None):
    if train_sizes is None:
        train_sizes = np.linspace(0.1, 1.0, 10)

    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, train_sizes=train_sizes,
        scoring='accuracy', n_jobs=-1
    )

    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    test_mean = test_scores.mean(axis=1)
    test_std = test_scores.std(axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, 'o-', label='Training score')
    plt.plot(train_sizes, test_mean, 'o-', label='Cross-validation score')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1)
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.1)
    plt.xlabel('Training Examples')
    plt.ylabel('Score')
    plt.title('Learning Curve')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

    # Diagnose from learning curve
    final_gap = train_mean[-1] - test_mean[-1]
    if final_gap > 0.1:
        print("DIAGNOSIS: High variance (overfitting)")
        print("  - Try regularization")
        print("  - Reduce model complexity")
        print("  - Get more training data")
    elif test_mean[-1] < 0.7:
        print("DIAGNOSIS: High bias (underfitting)")
        print("  - Increase model complexity")
        print("  - Add more features")
        print("  - Reduce regularization")
```

### Classification Metrics
```python
from sklearn.metrics import (
    confusion_matrix, classification_report,
    precision_recall_curve, roc_curve, roc_auc_score
)

# Comprehensive classification report
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Visualize confusion matrix
import seaborn as sns
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Debug class imbalance
print("\nClass Distribution:")
print(f"Train: {np.bincount(y_train)}")
print(f"Test:  {np.bincount(y_test)}")
```

### Pandas Output Configuration
```python
# Enable pandas output for transformers (sklearn 1.2+)
from sklearn import set_config

set_config(transform_output="pandas")

# Now transformers return DataFrames with column names
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)  # Returns DataFrame!
print(X_scaled.head())
print(X_scaled.columns.tolist())

# Reset to default
set_config(transform_output="default")
```

## The Four Phases (Sklearn-specific)

### Phase 1: Data Validation
```python
def validate_data(X, y, name="Dataset"):
    """Comprehensive data validation before training."""
    print(f"=== {name} Validation ===")

    # Shape check
    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape if hasattr(y, 'shape') else len(y)}")

    # Type check
    print(f"X dtype: {X.dtype if hasattr(X, 'dtype') else type(X)}")
    print(f"y dtype: {y.dtype if hasattr(y, 'dtype') else type(y)}")

    # NaN/Inf check
    X_arr = np.asarray(X)
    print(f"X contains NaN: {np.isnan(X_arr).any()}")
    print(f"X contains Inf: {np.isinf(X_arr).any()}")

    # Value range
    print(f"X value range: [{X_arr.min():.4f}, {X_arr.max():.4f}]")

    # Target distribution
    if len(np.unique(y)) <= 20:  # Classification
        unique, counts = np.unique(y, return_counts=True)
        print(f"Class distribution: {dict(zip(unique, counts))}")

        # Check for class imbalance
        ratio = max(counts) / min(counts)
        if ratio > 10:
            print(f"WARNING: Severe class imbalance (ratio: {ratio:.1f})")
    else:  # Regression
        print(f"y range: [{y.min():.4f}, {y.max():.4f}]")
        print(f"y mean: {y.mean():.4f}, std: {y.std():.4f}")

    return True
```

### Phase 2: Model Configuration Validation
```python
def validate_model_config(model, X, y):
    """Validate model configuration before fitting."""
    print("=== Model Configuration Validation ===")

    params = model.get_params()
    print(f"Model: {type(model).__name__}")
    print(f"Parameters: {params}")

    # Check for common misconfigurations
    issues = []

    # Classification-specific checks
    n_classes = len(np.unique(y))
    if n_classes == 2:
        # Binary classification
        if hasattr(model, 'multi_class') and params.get('multi_class') == 'multinomial':
            issues.append("Using multinomial for binary classification")

    # Regularization checks
    if hasattr(model, 'C'):
        if params.get('C', 1.0) > 1000:
            issues.append("Very weak regularization (high C)")
        if params.get('C', 1.0) < 0.001:
            issues.append("Very strong regularization (low C)")

    # n_estimators check for ensemble methods
    if hasattr(model, 'n_estimators'):
        n_est = params.get('n_estimators', 100)
        if n_est < 10:
            issues.append(f"Low n_estimators ({n_est})")

    # max_depth check
    if hasattr(model, 'max_depth'):
        max_depth = params.get('max_depth')
        if max_depth is not None and max_depth > 50:
            issues.append(f"Deep tree (max_depth={max_depth}) - potential overfitting")

    if issues:
        print("Potential issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("No obvious configuration issues found")

    return len(issues) == 0
```

### Phase 3: Training Diagnostics
```python
def train_with_diagnostics(model, X_train, y_train, X_test, y_test):
    """Train model with comprehensive diagnostics."""
    import time
    from sklearn.exceptions import ConvergenceWarning
    import warnings

    print("=== Training Diagnostics ===")

    # Capture warnings
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")

        start_time = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - start_time

    print(f"Training time: {train_time:.2f}s")

    # Report warnings
    if caught_warnings:
        print("\nWarnings during training:")
        for w in caught_warnings:
            print(f"  - {w.category.__name__}: {w.message}")

    # Training vs test scores
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"\nTraining score: {train_score:.4f}")
    print(f"Test score: {test_score:.4f}")
    print(f"Gap: {train_score - test_score:.4f}")

    # Diagnose
    if train_score - test_score > 0.2:
        print("\nDIAGNOSIS: Significant overfitting detected")
    elif test_score < 0.6:
        print("\nDIAGNOSIS: Model may be underfitting")
    elif train_score > 0.99:
        print("\nDIAGNOSIS: Perfect training score - possible data leakage")

    return model
```

### Phase 4: Prediction Validation
```python
def validate_predictions(model, X_test, y_test):
    """Validate model predictions."""
    print("=== Prediction Validation ===")

    y_pred = model.predict(X_test)

    # Basic checks
    print(f"Prediction shape: {y_pred.shape}")
    print(f"Unique predictions: {np.unique(y_pred)}")

    # Check for constant predictions
    if len(np.unique(y_pred)) == 1:
        print("WARNING: Model predicting only one class!")
        print(f"  Predicted class: {y_pred[0]}")
        print(f"  Actual class distribution: {np.bincount(y_test.astype(int))}")

    # Check prediction distribution matches training distribution
    pred_dist = np.bincount(y_pred.astype(int), minlength=len(np.unique(y_test)))
    actual_dist = np.bincount(y_test.astype(int))

    print(f"\nPrediction distribution: {pred_dist}")
    print(f"Actual distribution: {actual_dist}")

    # Probability calibration check (if available)
    if hasattr(model, 'predict_proba'):
        y_proba = model.predict_proba(X_test)
        print(f"\nProbability range: [{y_proba.min():.4f}, {y_proba.max():.4f}]")

        # Check for overconfident predictions
        max_proba = y_proba.max(axis=1)
        if (max_proba > 0.99).mean() > 0.5:
            print("WARNING: Many overconfident predictions (>99% probability)")
```

## Quick Reference Commands

### Data Inspection
```python
# Quick data summary
print(X.describe() if hasattr(X, 'describe') else f"Shape: {X.shape}, dtype: {X.dtype}")

# Check for issues
print(f"NaN: {np.isnan(X).sum()}, Inf: {np.isinf(X).sum()}")

# Feature statistics
print(f"Mean: {X.mean(axis=0)}")
print(f"Std: {X.std(axis=0)}")
```

### Model Debugging
```python
# Check if fitted
from sklearn.utils.validation import check_is_fitted
check_is_fitted(model)

# Get parameters
model.get_params()

# Get feature importances (tree-based models)
model.feature_importances_

# Get coefficients (linear models)
model.coef_, model.intercept_
```

### Pipeline Debugging
```python
# Inspect pipeline steps
pipe.named_steps

# Get intermediate results
pipe[:-1].transform(X)

# Debug specific step
pipe.named_steps['scaler'].mean_
```

### Quick Diagnostics
```python
# One-liner diagnostics
from sklearn.model_selection import cross_val_score
print(f"CV: {cross_val_score(model, X, y, cv=5).mean():.4f}")

# Quick classification report
from sklearn.metrics import classification_report
print(classification_report(y_test, model.predict(X_test)))

# Learning curve quick check
from sklearn.model_selection import learning_curve
sizes, train_scores, test_scores = learning_curve(model, X, y, cv=5)
print(f"Learning curve gap: {train_scores[:,-1].mean() - test_scores[:,-1].mean():.4f}")
```

### Memory and Performance
```python
# Check memory usage
import sys
print(f"X memory: {sys.getsizeof(X) / 1024**2:.2f} MB")

# Use sparse matrices for high-dimensional data
from scipy.sparse import csr_matrix
X_sparse = csr_matrix(X)

# Reduce precision
X_float32 = X.astype(np.float32)
```

### Debugging with Verbose Mode
```python
# Enable verbose output during training
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(verbose=1)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(verbose=2)

from sklearn.svm import SVC
model = SVC(verbose=True)
```

## Sources

This guide was compiled using information from:
- [Scikit-learn Common Pitfalls Documentation](https://scikit-learn.org/stable/common_pitfalls.html)
- [Scikit-learn Developer Tips for Debugging](https://scikit-learn.org/0.15/developers/debugging.html)
- [50+ Common Scikit-learn Mistakes and Solutions](https://baotramduong.medium.com/python-for-data-science-50-common-scikit-learn-mistakes-and-solutions-for-machine-learning-c150110e9ba7)
- [Sling Academy: Scikit-Learn Common Errors Series](https://www.slingacademy.com/series/scikit-learn-common-errors-and-how-to-fix-them/)
- [Best Practices in Scikit-learn](https://medium.com/@tommanzur/best-practices-in-scikit-learn-6b606b384ee1)
- [8 Mistakes I Made with Scikit-learn](https://medium.com/@connect.hashblock/8-mistakes-i-made-with-scikit-learn-and-what-fixed-them-08e6c78afafc)
