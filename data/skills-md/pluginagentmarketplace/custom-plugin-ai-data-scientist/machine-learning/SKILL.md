---
name: machine-learning
description: Supervised/unsupervised learning, model selection, evaluation, and scikit-learn. Use for building classification, regression, or clustering models.
sasmp_version: "1.3.0"
bonded_agent: 04-machine-learning-ai
bond_type: PRIMARY_BOND
---

# Machine Learning with Scikit-Learn

Build, train, and evaluate ML models for classification, regression, and clustering.

## Quick Start

### Classification
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)

# Evaluate
print(classification_report(y_test, predictions))
```

### Regression
```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score

model = GradientBoostingRegressor(n_estimators=100)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(f"MAE: {mean_absolute_error(y_test, predictions):.2f}")
print(f"R²: {r2_score(y_test, predictions):.3f}")
```

### Clustering
```python
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Find optimal k (elbow method)
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X)
    inertias.append(km.inertia_)

plt.plot(range(1, 11), inertias, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()

# Train with optimal k
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(X)
```

## Model Selection Guide

**Classification:**
- **Logistic Regression**: Linear, interpretable, baseline
- **Random Forest**: Non-linear, feature importance, robust
- **XGBoost**: Best performance, handles missing data
- **SVM**: Small datasets, kernel trick

**Regression:**
- **Linear Regression**: Linear relationships, interpretable
- **Ridge/Lasso**: Regularization, feature selection
- **Random Forest**: Non-linear, robust to outliers
- **XGBoost**: Best performance, often wins competitions

**Clustering:**
- **K-Means**: Fast, spherical clusters
- **DBSCAN**: Arbitrary shapes, handles noise
- **Hierarchical**: Dendrogram, no k selection

## Evaluation Metrics

**Classification:**
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='weighted')
recall = recall_score(y_true, y_pred, average='weighted')
f1 = f1_score(y_true, y_pred, average='weighted')
roc_auc = roc_auc_score(y_true, y_pred_proba, multi_class='ovr')
```

**Regression:**
```python
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score
)

mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_true, y_pred)
```

## Cross-Validation

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring='f1_weighted')
print(f"CV F1: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

## Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='f1_weighted',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")

# Use best model
best_model = grid_search.best_estimator_
```

## Feature Engineering

```python
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Encoding
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Polynomial features
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
```

## Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

## Best Practices

1. Always split data before preprocessing
2. Use cross-validation for reliable estimates
3. Scale features for distance-based models
4. Handle class imbalance (SMOTE, class weights)
5. Check for overfitting (train vs test performance)
6. Save models with joblib or pickle
