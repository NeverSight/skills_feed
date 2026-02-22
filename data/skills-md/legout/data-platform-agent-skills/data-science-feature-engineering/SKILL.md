---
name: data-science-feature-engineering
description: "Feature engineering for machine learning: encoding, scaling, transformations, datetime features, text features, and feature selection. Use when preparing data for modeling or improving model performance through better representations."
dependsOn: ["@data-science-eda", "@data-engineering-core"]
---

# Feature Engineering

Use this skill for creating, transforming, and selecting features that improve model performance.

## When to use this skill

- After EDA — convert insights into features
- Model underperforming — need better representations
- Handling different data types (numerical, categorical, text, datetime)
- Reducing dimensionality or selecting most predictive features

## Feature engineering workflow

1. **Numerical features**
   - Scaling (StandardScaler, MinMaxScaler, RobustScaler)
   - Transformations (log, sqrt, Box-Cox for skewness)
   - Binning (equal-width, quantile, custom)
   - Interaction features

2. **Categorical features**
   - One-hot encoding (low cardinality)
   - Target/Mean encoding (high cardinality)
   - Ordinal encoding (ordered categories)
   - Frequency/rare category handling

3. **Datetime features**
   - Extract components (year, month, day, hour, dayofweek)
   - Cyclical encoding (sin/cos for time cycles)
   - Time since/duration features

4. **Text features**
   - TF-IDF, CountVectorizer
   - Embeddings (sentence-transformers)
   - Basic text stats (length, word count)

5. **Feature selection**
   - Filter methods (correlation, mutual information)
   - Wrapper methods (recursive feature elimination)
   - Embedded methods (L1 regularization, tree importance)

## Quick tool selection

| Task | Default choice | Notes |
|---|---|---|
| sklearn pipelines | **sklearn.pipeline + ColumnTransformer** | Reproducible, cross-validation safe |
| Categorical encoding | **category_encoders** | Beyond sklearn's limited options |
| Feature selection | **sklearn.feature_selection** | Mutual info, RFE, SelectFromModel |
| Text embeddings | **sentence-transformers** | Pre-trained semantic embeddings |
| Auto feature engineering | **Feature-engine** | Comprehensive transformations |

## Core implementation rules

### 1) Use pipelines to prevent leakage

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
])

pipeline = Pipeline([
    ('prep', preprocessor),
    ('model', RandomForestClassifier())
])
```

### 2) Fit on train only, transform on all

```python
# Correct: fit_transform on train, transform on test
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)  # Only transform!
```

### 3) Handle unknown categories

```python
OneHotEncoder(handle_unknown='ignore')  # Unknown → all zeros
# OR
OneHotEncoder(handle_unknown='infrequent_if_exist')  # Group rare/unknown
```

### 4) Document feature importance

Track which features were created, why, and their expected impact.

## Common anti-patterns

- ❌ Fitting preprocessors on full dataset (leakage!)
- ❌ One-hot encoding high-cardinality features (dimension explosion)
- ❌ Ignoring feature scaling for distance-based models
- ❌ Creating features without domain reasoning
- ❌ Not validating feature distributions match between train/test

## Progressive disclosure

- `../references/categorical-encoding.md` — Comprehensive encoding guide
- `../references/datetime-features.md` — Time-based feature patterns
- `../references/text-features.md` — NLP feature engineering
- `../references/feature-selection.md` — Selection strategies and implementations

## Related skills

- `@data-science-eda` — Understand data before engineering
- `@data-science-model-evaluation` — Validate feature impact
- `@data-engineering-core` — Data processing fundamentals

## References

- [sklearn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
- [category_encoders](https://contrib.scikit-learn.org/category_encoders/)
- [Feature-engine Documentation](https://feature-engine.trainindata.com/)
- [Sentence Transformers](https://www.sbert.net/)
