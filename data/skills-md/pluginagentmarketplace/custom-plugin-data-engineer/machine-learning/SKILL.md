---
name: machine-learning
description: Supervised & unsupervised learning, scikit-learn, XGBoost, model evaluation, feature engineering for production ML
sasmp_version: "1.3.0"
bonded_agent: 04-data-scientist
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 150
prerequisites: [python-programming, statistics-math]
unlocks: [deep-learning, mlops, llms-generative-ai]
---

# Machine Learning

Production-grade machine learning with scikit-learn, XGBoost, and modern ML engineering practices.

## Quick Start

```python
# Production ML Pipeline with scikit-learn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# Load and split data
df = pd.read_csv("data/customers.csv")
X = df.drop("churn", axis=1)
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Define feature types
numeric_features = ["age", "tenure", "monthly_charges"]
categorical_features = ["contract_type", "payment_method"]

# Build preprocessing pipeline
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# Full pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train and evaluate
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")

# Save model
joblib.dump(model, "models/churn_model.joblib")
```

## Core Concepts

### 1. Feature Engineering Pipeline

```python
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import FunctionTransformer
import numpy as np

class DateFeatureExtractor(BaseEstimator, TransformerMixin):
    """Custom transformer for date features."""

    def __init__(self, date_column: str):
        self.date_column = date_column

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        dates = pd.to_datetime(X[self.date_column])
        X["day_of_week"] = dates.dt.dayofweek
        X["month"] = dates.dt.month
        X["is_weekend"] = (dates.dt.dayofweek >= 5).astype(int)
        X["days_since_epoch"] = (dates - pd.Timestamp("1970-01-01")).dt.days
        return X.drop(self.date_column, axis=1)

class OutlierClipper(BaseEstimator, TransformerMixin):
    """Clip outliers to percentile bounds."""

    def __init__(self, lower_percentile=1, upper_percentile=99):
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile
        self.bounds_ = {}

    def fit(self, X, y=None):
        for col in X.columns:
            self.bounds_[col] = (
                np.percentile(X[col], self.lower_percentile),
                np.percentile(X[col], self.upper_percentile)
            )
        return self

    def transform(self, X):
        X = X.copy()
        for col, (lower, upper) in self.bounds_.items():
            X[col] = X[col].clip(lower, upper)
        return X

# Log transform for skewed features
log_transformer = FunctionTransformer(
    func=lambda x: np.log1p(np.maximum(x, 0)),
    inverse_func=lambda x: np.expm1(x)
)
```

### 2. Cross-Validation Strategies

```python
from sklearn.model_selection import (
    StratifiedKFold, TimeSeriesSplit, GroupKFold,
    cross_val_score, cross_validate
)

# Stratified K-Fold (for imbalanced classification)
stratified_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(
    model, X, y,
    cv=stratified_cv,
    scoring="roc_auc",
    n_jobs=-1
)
print(f"ROC-AUC: {scores.mean():.4f} (+/- {scores.std()*2:.4f})")

# Time Series Split (for temporal data)
ts_cv = TimeSeriesSplit(n_splits=5, gap=7)  # 7-day gap

for train_idx, test_idx in ts_cv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    # Train and evaluate...

# Group K-Fold (prevent data leakage by user/entity)
group_cv = GroupKFold(n_splits=5)
groups = df["user_id"]  # Same user never in train and test

scores = cross_val_score(
    model, X, y,
    cv=group_cv,
    groups=groups,
    scoring="roc_auc"
)

# Multiple metrics at once
results = cross_validate(
    model, X, y,
    cv=stratified_cv,
    scoring=["accuracy", "precision", "recall", "f1", "roc_auc"],
    return_train_score=True
)
```

### 3. Hyperparameter Tuning

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform
import optuna

# RandomizedSearchCV (good baseline)
param_dist = {
    "classifier__n_estimators": randint(100, 500),
    "classifier__max_depth": randint(3, 15),
    "classifier__min_samples_split": randint(2, 20),
    "classifier__min_samples_leaf": randint(1, 10),
}

random_search = RandomizedSearchCV(
    model,
    param_distributions=param_dist,
    n_iter=50,
    cv=stratified_cv,
    scoring="roc_auc",
    n_jobs=-1,
    random_state=42,
    verbose=1
)
random_search.fit(X_train, y_train)
print(f"Best params: {random_search.best_params_}")
print(f"Best score: {random_search.best_score_:.4f}")

# Optuna (modern, efficient)
def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 15),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
    }

    model = XGBClassifier(**params, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc")
    return scores.mean()

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=100, n_jobs=-1)
print(f"Best params: {study.best_params}")
```

### 4. XGBoost Production Pattern

```python
import xgboost as xgb
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

# Prepare DMatrix for efficiency
dtrain = xgb.DMatrix(X_train, label=y_train, enable_categorical=True)
dtest = xgb.DMatrix(X_test, label=y_test, enable_categorical=True)

params = {
    "objective": "binary:logistic",
    "eval_metric": ["logloss", "auc"],
    "max_depth": 6,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 1,
    "tree_method": "hist",  # Fast histogram-based
    "device": "cuda",  # GPU if available
    "random_state": 42,
}

# Train with early stopping
evals = [(dtrain, "train"), (dtest, "eval")]
model = xgb.train(
    params,
    dtrain,
    num_boost_round=1000,
    evals=evals,
    early_stopping_rounds=50,
    verbose_eval=100
)

# Feature importance
importance = model.get_score(importance_type="gain")
sorted_importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))

# SHAP values for interpretability
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, plot_type="bar")
```

### 5. Handling Imbalanced Data

```python
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.utils.class_weight import compute_class_weight

# Option 1: Class weights
class_weights = compute_class_weight("balanced", classes=np.unique(y_train), y=y_train)
weight_dict = dict(zip(np.unique(y_train), class_weights))

model = RandomForestClassifier(class_weight=weight_dict)

# Option 2: SMOTE oversampling
smote = SMOTE(random_state=42, sampling_strategy=0.5)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Option 3: Combined pipeline (recommended)
resampling_pipeline = ImbPipeline([
    ("preprocessor", preprocessor),
    ("smote", SMOTE(random_state=42)),
    ("classifier", RandomForestClassifier())
])

# Option 4: Threshold tuning
from sklearn.metrics import precision_recall_curve

y_prob = model.predict_proba(X_test)[:, 1]
precisions, recalls, thresholds = precision_recall_curve(y_test, y_prob)

# Find threshold for target recall
target_recall = 0.8
idx = np.argmin(np.abs(recalls - target_recall))
optimal_threshold = thresholds[idx]

y_pred_adjusted = (y_prob >= optimal_threshold).astype(int)
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **scikit-learn** | Core ML library | 1.4+ |
| **XGBoost** | Gradient boosting | 2.0+ |
| **LightGBM** | Fast gradient boosting | 4.2+ |
| **CatBoost** | Categorical boosting | 1.2+ |
| **imbalanced-learn** | Sampling strategies | 0.12+ |
| **SHAP** | Model interpretability | 0.44+ |
| **Optuna** | Hyperparameter tuning | 3.5+ |
| **MLflow** | Experiment tracking | 2.10+ |

## Learning Path

### Phase 1: Foundations (Weeks 1-4)
```
Week 1: Supervised learning concepts, bias-variance
Week 2: Linear/logistic regression, evaluation metrics
Week 3: Decision trees, ensemble methods
Week 4: Cross-validation, train/test methodology
```

### Phase 2: Intermediate (Weeks 5-8)
```
Week 5: Feature engineering, preprocessing
Week 6: Gradient boosting (XGBoost, LightGBM)
Week 7: Hyperparameter tuning strategies
Week 8: Handling imbalanced data
```

### Phase 3: Advanced (Weeks 9-12)
```
Week 9: Unsupervised learning (clustering, PCA)
Week 10: Model interpretability (SHAP, LIME)
Week 11: Time series forecasting
Week 12: Anomaly detection
```

### Phase 4: Production (Weeks 13-16)
```
Week 13: ML pipelines with scikit-learn
Week 14: Model serialization, versioning
Week 15: A/B testing for ML models
Week 16: Monitoring and retraining
```

## Troubleshooting Guide

### Common Failure Modes

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Overfitting** | Train >> Test score | Model too complex | Regularization, cross-validation |
| **Underfitting** | Both scores low | Model too simple | More features, complex model |
| **Data Leakage** | Perfect CV, bad prod | Future info in features | Check feature timing |
| **Class Imbalance** | Low minority recall | Skewed class distribution | SMOTE, class weights, threshold |
| **Covariate Shift** | Model degrades over time | Data distribution changed | Monitor, retrain regularly |

### Debug Checklist

```python
# 1. Check data distribution
print(y.value_counts(normalize=True))

# 2. Verify no data leakage
# - Features computed before target event
# - No future information
# - No target encoding on full data

# 3. Learning curves
from sklearn.model_selection import learning_curve

train_sizes, train_scores, test_scores = learning_curve(
    model, X, y, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring="roc_auc"
)

# 4. Feature importance analysis
importances = model.feature_importances_
sorted_idx = np.argsort(importances)[::-1]

# 5. Error analysis
errors = X_test[y_test != y_pred]
# Analyze patterns in misclassifications
```

## Unit Test Template

```python
import pytest
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from your_module import create_pipeline, train_model

@pytest.fixture
def sample_data():
    X, y = make_classification(
        n_samples=1000, n_features=20, n_informative=10,
        n_redundant=5, random_state=42
    )
    return train_test_split(X, y, test_size=0.2, random_state=42)

class TestMLPipeline:

    def test_pipeline_trains_successfully(self, sample_data):
        X_train, X_test, y_train, y_test = sample_data
        model = create_pipeline()
        model.fit(X_train, y_train)
        assert hasattr(model, "predict")

    def test_predictions_valid_range(self, sample_data):
        X_train, X_test, y_train, y_test = sample_data
        model = create_pipeline()
        model.fit(X_train, y_train)
        predictions = model.predict_proba(X_test)[:, 1]

        assert np.all(predictions >= 0)
        assert np.all(predictions <= 1)

    def test_model_better_than_random(self, sample_data):
        X_train, X_test, y_train, y_test = sample_data
        model = create_pipeline()
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)

        assert score > 0.5  # Better than random

    def test_handles_missing_values(self):
        X = np.array([[1, 2], [np.nan, 3], [4, np.nan]])
        y = np.array([0, 1, 0])

        model = create_pipeline()
        model.fit(X, y)
        predictions = model.predict(X)

        assert len(predictions) == len(y)
```

## Best Practices

### Model Development
```python
# ✅ DO: Use pipelines for reproducibility
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

# ✅ DO: Stratify splits for classification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, random_state=42
)

# ✅ DO: Use appropriate metrics
# Classification: ROC-AUC, PR-AUC, F1
# Regression: RMSE, MAE, R²

# ❌ DON'T: Tune on test set
# ❌ DON'T: Feature engineer on full data
# ❌ DON'T: Ignore class imbalance
```

### Production Readiness
```python
# ✅ DO: Version your models
import mlflow

mlflow.sklearn.log_model(model, "model")
mlflow.log_params(params)
mlflow.log_metrics({"auc": auc_score})

# ✅ DO: Monitor predictions
def monitor_predictions(predictions, reference_dist):
    from scipy.stats import ks_2samp
    stat, p_value = ks_2samp(predictions, reference_dist)
    if p_value < 0.05:
        alert("Distribution shift detected")
```

## Resources

### Official Documentation
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [SHAP Documentation](https://shap.readthedocs.io/)

### Courses
- [Fast.ai Practical ML](https://www.fast.ai/)
- [Coursera ML Specialization](https://www.coursera.org/specializations/machine-learning)
- [Kaggle Learn](https://www.kaggle.com/learn)

### Books
- "Hands-On Machine Learning" by Aurélien Géron
- "The Elements of Statistical Learning"
- "Feature Engineering for ML" by Alice Zheng

## Next Skills

After mastering Machine Learning:
- → `deep-learning` - Neural networks with PyTorch
- → `mlops` - Production ML systems
- → `llms-generative-ai` - Large language models
- → `statistics-math` - Deeper mathematical foundations

---

**Skill Certification Checklist:**
- [ ] Can build end-to-end ML pipelines with scikit-learn
- [ ] Can tune hyperparameters with cross-validation
- [ ] Can handle imbalanced datasets appropriately
- [ ] Can interpret models with SHAP values
- [ ] Can deploy models with proper versioning
