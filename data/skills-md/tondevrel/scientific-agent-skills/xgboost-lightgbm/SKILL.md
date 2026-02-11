---
name: xgboost-lightgbm
description: Industry-standard gradient boosting libraries for tabular data and structured datasets. XGBoost and LightGBM excel at classification and regression tasks on tables, CSVs, and databases. Use when working with tabular machine learning, gradient boosting trees, Kaggle competitions, feature importance analysis, hyperparameter tuning, or when you need state-of-the-art performance on structured data.
version: xgboost-2.0.3, lightgbm-4.3.0
license: Apache-2.0
---

# XGBoost & LightGBM - Gradient Boosting for Tabular Data

XGBoost (eXtreme Gradient Boosting) and LightGBM (Light Gradient Boosting Machine) are the de facto standard libraries for machine learning on tabular/structured data. They consistently win Kaggle competitions and are widely used in industry for their speed, accuracy, and robustness.

## When to Use

- Classification or regression on tabular data (CSVs, databases, spreadsheets).
- Kaggle competitions or data science competitions on structured data.
- Feature importance analysis and feature selection.
- Handling missing values automatically (no need to impute).
- Working with imbalanced datasets (built-in class weighting).
- Need for fast training on large datasets (millions of rows).
- Hyperparameter tuning with cross-validation.
- Ranking tasks (learning-to-rank algorithms).
- When you need interpretable feature importances.
- Production ML systems requiring fast inference on tabular data.

## Reference Documentation

**XGBoost Official**: https://xgboost.readthedocs.io/  
**XGBoost GitHub**: https://github.com/dmlc/xgboost  
**LightGBM Official**: https://lightgbm.readthedocs.io/  
**LightGBM GitHub**: https://github.com/microsoft/LightGBM  
**Search patterns**: `xgboost.XGBClassifier`, `lightgbm.LGBMRegressor`, `xgboost.train`, `lightgbm.cv`

## Core Principles

### Gradient Boosting Trees
Both libraries build an ensemble of decision trees sequentially, where each new tree corrects errors from previous trees. This creates highly accurate models that capture complex non-linear patterns.

### Speed vs Accuracy Trade-offs
**XGBoost**: Slower but often slightly more accurate. Better for smaller datasets (<100k rows).  
**LightGBM**: Faster, especially on large datasets (millions of rows). Uses histogram-based learning.

### Regularization
Both include L1/L2 regularization (alpha, lambda parameters) to prevent overfitting. This is crucial when you have many features.

### Handling Categorical Features
LightGBM has native categorical feature support. XGBoost requires encoding (label encoding or one-hot).

## Quick Reference

### Installation

```bash
# Install both
pip install xgboost lightgbm

# For GPU support
pip install xgboost[gpu] lightgbm[gpu]
```

### Standard Imports

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

# XGBoost
import xgboost as xgb
from xgboost import XGBClassifier, XGBRegressor

# LightGBM
import lightgbm as lgb
from lightgbm import LGBMClassifier, LGBMRegressor
```

### Basic Pattern - Classification with XGBoost

```python
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# 1. Prepare data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Create and train model
model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    random_state=42
)
model.fit(X_train, y_train)

# 3. Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
```

### Basic Pattern - Regression with LightGBM

```python
from lightgbm import LGBMRegressor

# 1. Create model
model = LGBMRegressor(
    n_estimators=100,
    learning_rate=0.1,
    num_leaves=31,
    random_state=42
)

# 2. Train
model.fit(X_train, y_train)

# 3. Predict
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"RMSE: {rmse:.4f}")
```

## Critical Rules

### ✅ DO

- **Use Early Stopping** - Always use early stopping with a validation set to prevent overfitting and save training time.
- **Start with Defaults** - Both libraries have excellent default parameters. Start there before tuning.
- **Monitor Training** - Use `eval_set` parameter to track validation metrics during training.
- **Handle Imbalance** - For imbalanced classes, use `scale_pos_weight` (XGBoost) or `class_weight` (LightGBM).
- **Feature Engineering** - Create interaction features, polynomial features, aggregations - boosting excels with rich feature sets.
- **Use Native API for Advanced Control** - For complex tasks, use `xgb.train()` or `lgb.train()` instead of sklearn wrappers.
- **Save Models Properly** - Use `.save_model()` and `.load_model()` methods, not pickle (more robust).
- **Check Feature Importance** - Always examine feature importances to understand your model and detect data leakage.

### ❌ DON'T

- **Don't Forget to Normalize Target** - For regression, if target has wide range, consider log-transform or standardization.
- **Don't Ignore Tree Depth** - `max_depth` (XGBoost) or `num_leaves` (LightGBM) are critical. Too deep = overfit.
- **Don't Use Default Learning Rate for Large Datasets** - Reduce `learning_rate` to 0.01-0.05 for datasets >1M rows.
- **Don't Mix Up Parameters** - XGBoost uses `max_depth`, LightGBM uses `num_leaves`. They're different!
- **Don't One-Hot Encode for LightGBM** - Use categorical_feature parameter instead for better performance.
- **Don't Skip Cross-Validation** - Always CV before trusting a single train/test split.

## Anti-Patterns (NEVER)

```python
# ❌ BAD: Training without validation set or early stopping
model = XGBClassifier(n_estimators=1000)
model.fit(X_train, y_train)  # Will likely overfit

# ✅ GOOD: Use early stopping with validation
model = XGBClassifier(n_estimators=1000, early_stopping_rounds=10)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=False
)

# ❌ BAD: One-hot encoding categorical features for LightGBM
X_encoded = pd.get_dummies(X)  # Creates many sparse columns
model = LGBMClassifier()
model.fit(X_encoded, y)

# ✅ GOOD: Use categorical_feature parameter
model = LGBMClassifier()
model.fit(
    X, y,
    categorical_feature=['category_col1', 'category_col2']
)

# ❌ BAD: Ignoring class imbalance
model = XGBClassifier()
model.fit(X_train, y_train)  # Majority class dominates

# ✅ GOOD: Handle imbalance with scale_pos_weight
from sklearn.utils.class_weight import compute_sample_weight
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
model = XGBClassifier(scale_pos_weight=scale_pos_weight)
model.fit(X_train, y_train)
```

## XGBoost Fundamentals

### Scikit-learn Style API

```python
from xgboost import XGBClassifier
import numpy as np

# Binary classification
model = XGBClassifier(
    n_estimators=100,        # Number of trees
    max_depth=6,             # Maximum tree depth
    learning_rate=0.1,       # Step size shrinkage (eta)
    subsample=0.8,           # Row sampling ratio
    colsample_bytree=0.8,    # Column sampling ratio
    random_state=42
)

# Train with early stopping
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=10,
    verbose=True
)

# Get best iteration
print(f"Best iteration: {model.best_iteration}")
print(f"Best score: {model.best_score}")
```

### Native XGBoost API (More Control)

```python
import xgboost as xgb

# 1. Create DMatrix (XGBoost's internal data structure)
dtrain = xgb.DMatrix(X_train, label=y_train)
dval = xgb.DMatrix(X_val, label=y_val)

# 2. Set parameters
params = {
    'objective': 'binary:logistic',  # or 'reg:squarederror' for regression
    'max_depth': 6,
    'eta': 0.1,                      # learning_rate
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'eval_metric': 'auc',
    'seed': 42
}

# 3. Train with cross-validation monitoring
evals = [(dtrain, 'train'), (dval, 'val')]
model = xgb.train(
    params,
    dtrain,
    num_boost_round=1000,
    evals=evals,
    early_stopping_rounds=10,
    verbose_eval=50
)

# 4. Predict
dtest = xgb.DMatrix(X_test)
y_pred_proba = model.predict(dtest)
y_pred = (y_pred_proba > 0.5).astype(int)
```

### Cross-Validation

```python
import xgboost as xgb

# Prepare data
dtrain = xgb.DMatrix(X_train, label=y_train)

# Parameters
params = {
    'objective': 'binary:logistic',
    'max_depth': 6,
    'eta': 0.1,
    'eval_metric': 'auc'
}

# Run CV
cv_results = xgb.cv(
    params,
    dtrain,
    num_boost_round=1000,
    nfold=5,
    stratified=True,
    early_stopping_rounds=10,
    seed=42,
    verbose_eval=50
)

# Best iteration
print(f"Best iteration: {cv_results.shape[0]}")
print(f"Best score: {cv_results['test-auc-mean'].max():.4f}")
```

## LightGBM Fundamentals

### Scikit-learn Style API

```python
from lightgbm import LGBMClassifier

# Binary classification
model = LGBMClassifier(
    n_estimators=100,
    num_leaves=31,           # LightGBM uses leaves, not depth
    learning_rate=0.1,
    feature_fraction=0.8,    # Same as colsample_bytree
    bagging_fraction=0.8,    # Same as subsample
    bagging_freq=5,
    random_state=42
)

# Train with early stopping
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric='auc',
    callbacks=[lgb.early_stopping(stopping_rounds=10)]
)

print(f"Best iteration: {model.best_iteration_}")
print(f"Best score: {model.best_score_}")
```

### Native LightGBM API

```python
import lightgbm as lgb

# 1. Create Dataset
train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

# 2. Parameters
params = {
    'objective': 'binary',
    'metric': 'auc',
    'num_leaves': 31,
    'learning_rate': 0.1,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': -1
}

# 3. Train
model = lgb.train(
    params,
    train_data,
    num_boost_round=1000,
    valid_sets=[train_data, val_data],
    valid_names=['train', 'val'],
    callbacks=[lgb.early_stopping(stopping_rounds=10)]
)

# 4. Predict
y_pred_proba = model.predict(X_test)
y_pred = (y_pred_proba > 0.5).astype(int)
```

### Categorical Features (LightGBM's Superpower)

```python
import lightgbm as lgb
import pandas as pd

# Assume 'category' and 'group' are categorical columns
# DO NOT one-hot encode them!

# Method 1: Specify by name
model = lgb.LGBMClassifier()
model.fit(
    X_train, y_train,
    categorical_feature=['category', 'group']
)

# Method 2: Specify by index
model.fit(
    X_train, y_train,
    categorical_feature=[2, 5]  # Indices of categorical columns
)

# Method 3: Convert to category dtype (automatic detection)
X_train['category'] = X_train['category'].astype('category')
X_train['group'] = X_train['group'].astype('category')
model.fit(X_train, y_train)  # Automatically detects
```

## Hyperparameter Tuning

### Key Parameters to Tune

**Learning Rate (`learning_rate` or `eta`)**
- Lower = more accurate but slower
- Start: 0.1, then try 0.05, 0.01
- Lower learning_rate requires more n_estimators

**Tree Complexity**
- XGBoost: `max_depth` (3-10)
- LightGBM: `num_leaves` (20-100)
- Higher = more complex, risk of overfit

**Sampling Ratios**
- `subsample` / `bagging_fraction`: 0.5-1.0
- `colsample_bytree` / `feature_fraction`: 0.5-1.0
- Lower values add regularization

**Regularization**
- `reg_alpha` (L1): 0-10
- `reg_lambda` (L2): 0-10
- Higher values prevent overfit

### Grid Search with Cross-Validation

```python
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier

# Define parameter grid
param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [100, 200, 300],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

# Grid search
model = XGBClassifier(random_state=42)
grid_search = GridSearchCV(
    model,
    param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)
grid_search.fit(X_train, y_train)

# Best parameters
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.4f}")

# Use best model
best_model = grid_search.best_estimator_
```

### Optuna for Advanced Tuning

```python
import optuna
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score

def objective(trial):
    """Optuna objective function."""
    params = {
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'n_estimators': trial.suggest_int('n_estimators', 50, 300),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 10.0),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 10.0),
    }
    
    model = XGBClassifier(**params, random_state=42)
    score = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc').mean()
    return score

# Run optimization
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

print(f"Best value: {study.best_value:.4f}")
print(f"Best params: {study.best_params}")
```

## Feature Importance and Interpretability

### Feature Importance

```python
import matplotlib.pyplot as plt
from xgboost import XGBClassifier

# Train model
model = XGBClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Get feature importance
importance = model.feature_importances_
feature_names = X_train.columns

# Sort by importance
indices = importance.argsort()[::-1]

# Plot
plt.figure(figsize=(10, 6))
plt.bar(range(len(importance)), importance[indices])
plt.xticks(range(len(importance)), feature_names[indices], rotation=45, ha='right')
plt.xlabel('Features')
plt.ylabel('Importance')
plt.title('Feature Importance')
plt.tight_layout()
plt.show()

# Print top 10
print("Top 10 features:")
for i in range(min(10, len(importance))):
    print(f"{feature_names[indices[i]]}: {importance[indices[i]]:.4f}")
```

### SHAP Values (Advanced Interpretability)

```python
import shap
from xgboost import XGBClassifier

# Train model
model = XGBClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Create SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test, plot_type="bar")

# Force plot for single prediction
shap.force_plot(
    explainer.expected_value,
    shap_values[0],
    X_test.iloc[0]
)
```

## Practical Workflows

### 1. Kaggle-Style Competition Pipeline

```python
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def kaggle_pipeline(X, y, X_test):
    """Complete Kaggle competition pipeline."""
    
    # 1. Cross-validation setup
    n_folds = 5
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
    
    # 2. Store predictions
    oof_predictions = np.zeros(len(X))
    test_predictions = np.zeros(len(X_test))
    
    # 3. Train on each fold
    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        print(f"\nFold {fold + 1}/{n_folds}")
        
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        # Train model
        model = XGBClassifier(
            n_estimators=1000,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=50,
            verbose=False
        )
        
        # Predict validation set
        oof_predictions[val_idx] = model.predict_proba(X_val)[:, 1]
        
        # Predict test set
        test_predictions += model.predict_proba(X_test)[:, 1] / n_folds
    
    # 4. Calculate OOF score
    oof_score = roc_auc_score(y, oof_predictions)
    print(f"\nOOF AUC: {oof_score:.4f}")
    
    return oof_predictions, test_predictions

# Usage
# oof_preds, test_preds = kaggle_pipeline(X_train, y_train, X_test)
```

### 2. Imbalanced Classification

```python
from xgboost import XGBClassifier
from sklearn.utils.class_weight import compute_sample_weight

def train_imbalanced_classifier(X_train, y_train, X_val, y_val):
    """Handle imbalanced datasets."""
    
    # Calculate scale_pos_weight
    n_pos = (y_train == 1).sum()
    n_neg = (y_train == 0).sum()
    scale_pos_weight = n_neg / n_pos
    
    print(f"Class distribution: {n_neg} negative, {n_pos} positive")
    print(f"Scale pos weight: {scale_pos_weight:.2f}")
    
    # Method 1: scale_pos_weight parameter
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        scale_pos_weight=scale_pos_weight,
        random_state=42
    )
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        early_stopping_rounds=10,
        verbose=False
    )
    
    return model

# Alternative: sample_weight
sample_weights = compute_sample_weight('balanced', y_train)
model.fit(X_train, y_train, sample_weight=sample_weights)
```

### 3. Multi-Class Classification

```python
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report

def multiclass_pipeline(X_train, y_train, X_val, y_val):
    """Multi-class classification with LightGBM."""
    
    # Train model
    model = LGBMClassifier(
        n_estimators=200,
        num_leaves=31,
        learning_rate=0.05,
        random_state=42
    )
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        eval_metric='multi_logloss',
        callbacks=[lgb.early_stopping(stopping_rounds=20)]
    )
    
    # Predict
    y_pred = model.predict(X_val)
    y_pred_proba = model.predict_proba(X_val)
    
    # Evaluate
    print(classification_report(y_val, y_pred))
    
    return model, y_pred, y_pred_proba

# Usage
# model, preds, proba = multiclass_pipeline(X_train, y_train, X_val, y_val)
```

### 4. Time Series with Boosting

```python
import pandas as pd
from xgboost import XGBRegressor

def time_series_features(df, target_col, date_col):
    """Create time-based features."""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Time features
    df['year'] = df[date_col].dt.year
    df['month'] = df[date_col].dt.month
    df['day'] = df[date_col].dt.day
    df['dayofweek'] = df[date_col].dt.dayofweek
    df['quarter'] = df[date_col].dt.quarter
    
    # Lag features
    for lag in [1, 7, 30]:
        df[f'lag_{lag}'] = df[target_col].shift(lag)
    
    # Rolling statistics
    for window in [7, 30]:
        df[f'rolling_mean_{window}'] = df[target_col].rolling(window).mean()
        df[f'rolling_std_{window}'] = df[target_col].rolling(window).std()
    
    return df.dropna()

def train_time_series_model(df, target_col, feature_cols):
    """Train XGBoost on time series."""
    
    # Split by time (no shuffle!)
    split_idx = int(0.8 * len(df))
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]
    
    X_train = train[feature_cols]
    y_train = train[target_col]
    X_test = test[feature_cols]
    y_test = test[target_col]
    
    # Train
    model = XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        random_state=42
    )
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        early_stopping_rounds=20,
        verbose=False
    )
    
    # Predict
    y_pred = model.predict(X_test)
    
    return model, y_pred

# Usage
# df = time_series_features(df, 'sales', 'date')
# model, predictions = train_time_series_model(df, 'sales', feature_cols)
```

### 5. Model Stacking (Ensemble)

```python
from sklearn.model_selection import cross_val_predict
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression

def create_stacked_model(X_train, y_train, X_test):
    """Stack XGBoost and LightGBM with meta-learner."""
    
    # Base models
    xgb_model = XGBClassifier(n_estimators=100, random_state=42)
    lgb_model = LGBMClassifier(n_estimators=100, random_state=42)
    
    # Generate meta-features via cross-validation
    xgb_train_preds = cross_val_predict(
        xgb_model, X_train, y_train, cv=5, method='predict_proba'
    )[:, 1]
    
    lgb_train_preds = cross_val_predict(
        lgb_model, X_train, y_train, cv=5, method='predict_proba'
    )[:, 1]
    
    # Train base models on full training set
    xgb_model.fit(X_train, y_train)
    lgb_model.fit(X_train, y_train)
    
    # Get test predictions from base models
    xgb_test_preds = xgb_model.predict_proba(X_test)[:, 1]
    lgb_test_preds = lgb_model.predict_proba(X_test)[:, 1]
    
    # Create meta-features
    meta_X_train = np.column_stack([xgb_train_preds, lgb_train_preds])
    meta_X_test = np.column_stack([xgb_test_preds, lgb_test_preds])
    
    # Train meta-model
    meta_model = LogisticRegression()
    meta_model.fit(meta_X_train, y_train)
    
    # Final predictions
    final_preds = meta_model.predict_proba(meta_X_test)[:, 1]
    
    return final_preds

# Usage
# stacked_predictions = create_stacked_model(X_train, y_train, X_test)
```

## Performance Optimization

### GPU Acceleration

```python
# XGBoost with GPU
from xgboost import XGBClassifier

model = XGBClassifier(
    tree_method='gpu_hist',  # Use GPU
    gpu_id=0,
    n_estimators=100
)
model.fit(X_train, y_train)

# LightGBM with GPU
from lightgbm import LGBMClassifier

model = LGBMClassifier(
    device='gpu',
    gpu_platform_id=0,
    gpu_device_id=0,
    n_estimators=100
)
model.fit(X_train, y_train)
```

### Memory Optimization

```python
import lightgbm as lgb

# Use float32 instead of float64
X_train = X_train.astype('float32')

# For very large datasets, use LightGBM's Dataset
train_data = lgb.Dataset(
    X_train,
    label=y_train,
    free_raw_data=False  # Keep data in memory if you'll reuse it
)

# Use histogram-based approach (LightGBM is already optimized for this)
params = {
    'max_bin': 255,  # Reduce for less memory, increase for more accuracy
    'num_leaves': 31,
    'learning_rate': 0.05
}
```

### Parallel Training

```python
from xgboost import XGBClassifier

# Use all CPU cores
model = XGBClassifier(
    n_estimators=100,
    n_jobs=-1,  # Use all cores
    random_state=42
)
model.fit(X_train, y_train)

# Control number of threads
model = XGBClassifier(
    n_estimators=100,
    n_jobs=4,  # Use 4 cores
    random_state=42
)
```

## Common Pitfalls and Solutions

### The "Overfitting on Validation Set" Problem

When you tune hyperparameters based on validation performance, you're indirectly overfitting to the validation set.

```python
# ❌ Problem: Tuning on same validation set repeatedly
# This leads to overly optimistic performance estimates

# ✅ Solution: Use nested cross-validation
from sklearn.model_selection import cross_val_score, GridSearchCV

# Outer loop: performance estimation
# Inner loop: hyperparameter tuning
param_grid = {'max_depth': [3, 5, 7], 'learning_rate': [0.01, 0.1]}
model = XGBClassifier()
grid_search = GridSearchCV(model, param_grid, cv=3)  # Inner CV
outer_scores = cross_val_score(grid_search, X, y, cv=5)  # Outer CV
print(f"Unbiased performance: {outer_scores.mean():.4f}")
```

### The "Categorical Encoding" Dilemma

XGBoost doesn't handle categorical features natively (but LightGBM does).

```python
# For XGBoost: use label encoding, NOT one-hot
from sklearn.preprocessing import LabelEncoder

# ❌ BAD for XGBoost: One-hot encoding creates too many sparse features
X_encoded = pd.get_dummies(X, columns=['category'])

# ✅ GOOD for XGBoost: Label encoding
le = LabelEncoder()
X['category_encoded'] = le.fit_transform(X['category'])

# ✅ BEST: Use LightGBM with native categorical support
model = lgb.LGBMClassifier()
model.fit(X, y, categorical_feature=['category'])
```

### The "Learning Rate vs Trees" Trade-off

Lower learning rate needs more trees but gives better results.

```python
# ❌ Problem: Too few trees with low learning rate
model = XGBClassifier(n_estimators=100, learning_rate=0.01)
# Model won't converge

# ✅ Solution: Use early stopping to find optimal number
model = XGBClassifier(n_estimators=5000, learning_rate=0.01)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=50
)
# Will stop when validation score stops improving
```

### The "max_depth vs num_leaves" Confusion

XGBoost uses `max_depth`, LightGBM uses `num_leaves`. They're related but different!

```python
# XGBoost: max_depth controls tree depth
model_xgb = XGBClassifier(max_depth=6)  # Tree can have 2^6 = 64 leaves

# LightGBM: num_leaves controls number of leaves directly
model_lgb = LGBMClassifier(num_leaves=31)  # Exactly 31 leaves

# ⚠️ Relationship: num_leaves ≈ 2^max_depth - 1
# But LightGBM grows trees leaf-wise (faster, more accurate)
# XGBoost grows trees level-wise (more conservative)
```

### The "Data Leakage" Detection

Feature importance can reveal data leakage.

```python
# ✅ Always check feature importance
model.fit(X_train, y_train)
importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(importance.head(10))

# 🚨 Red flags for data leakage:
# 1. One feature has >>90% importance (suspicious)
# 2. ID columns have high importance (leakage!)
# 3. Target-derived features (leakage!)
# 4. Future information in time series (leakage!)
```

XGBoost and LightGBM have revolutionized machine learning on tabular data. Their combination of speed, accuracy, and interpretability makes them the go-to choice for structured data problems. Master these libraries, and you'll have a powerful tool for the vast majority of real-world ML tasks.
