---
name: scikit-learn
description: Use when "scikit-learn", "sklearn", "machine learning", "classification", "regression", "clustering", or asking about "train test split", "cross validation", "hyperparameter tuning", "ML pipeline", "random forest", "SVM", "preprocessing"
version: 1.0.0
---

# Scikit-learn Machine Learning

Industry-standard Python library for classical machine learning.

## When to Use

- Classification or regression tasks
- Clustering or dimensionality reduction
- Preprocessing and feature engineering
- Model evaluation and cross-validation
- Hyperparameter tuning
- Building ML pipelines

---

## Algorithm Selection

### Classification

| Algorithm | Best For | Strengths |
|-----------|----------|-----------|
| **Logistic Regression** | Baseline, interpretable | Fast, probabilistic |
| **Random Forest** | General purpose | Handles non-linear, feature importance |
| **Gradient Boosting** | Best accuracy | State-of-art for tabular |
| **SVM** | High-dimensional data | Works well with few samples |
| **KNN** | Simple problems | No training, instance-based |

### Regression

| Algorithm | Best For | Notes |
|-----------|----------|-------|
| **Linear Regression** | Baseline | Interpretable coefficients |
| **Ridge/Lasso** | Regularization needed | L2 vs L1 penalty |
| **Random Forest** | Non-linear relationships | Robust to outliers |
| **Gradient Boosting** | Best accuracy | XGBoost, LightGBM wrappers |

### Clustering

| Algorithm | Best For | Key Parameter |
|-----------|----------|---------------|
| **KMeans** | Spherical clusters | n_clusters (must specify) |
| **DBSCAN** | Arbitrary shapes | eps (density) |
| **Agglomerative** | Hierarchical | n_clusters or distance threshold |
| **Gaussian Mixture** | Soft clustering | n_components |

### Dimensionality Reduction

| Method | Preserves | Use Case |
|--------|-----------|----------|
| **PCA** | Global variance | Feature reduction |
| **t-SNE** | Local structure | 2D/3D visualization |
| **UMAP** | Both local/global | Visualization + downstream |

---

## Pipeline Concepts

**Key concept**: Pipelines prevent data leakage by ensuring transformations are fit only on training data.

| Component | Purpose |
|-----------|---------|
| **Pipeline** | Sequential steps (transform → model) |
| **ColumnTransformer** | Apply different transforms to different columns |
| **FeatureUnion** | Combine multiple feature extraction methods |

**Common preprocessing flow**:

1. Impute missing values (SimpleImputer)
2. Scale numeric features (StandardScaler, MinMaxScaler)
3. Encode categoricals (OneHotEncoder, OrdinalEncoder)
4. Optional: feature selection or polynomial features

---

## Model Evaluation

### Cross-Validation Strategies

| Strategy | Use Case |
|----------|----------|
| **KFold** | General purpose |
| **StratifiedKFold** | Imbalanced classification |
| **TimeSeriesSplit** | Temporal data |
| **LeaveOneOut** | Very small datasets |

### Metrics

| Task | Metric | When to Use |
|------|--------|-------------|
| **Classification** | Accuracy | Balanced classes |
| | F1-score | Imbalanced classes |
| | ROC-AUC | Ranking, threshold tuning |
| | Precision/Recall | Domain-specific costs |
| **Regression** | RMSE | Penalize large errors |
| | MAE | Robust to outliers |
| | R² | Explained variance |

---

## Hyperparameter Tuning

| Method | Pros | Cons |
|--------|------|------|
| **GridSearchCV** | Exhaustive | Slow for many params |
| **RandomizedSearchCV** | Faster | May miss optimal |
| **HalvingGridSearchCV** | Efficient | Requires sklearn 0.24+ |

**Key concept**: Always tune on validation set, evaluate final model on held-out test set.

---

## Best Practices

| Practice | Why |
|----------|-----|
| Split data first | Prevent leakage |
| Use pipelines | Reproducible, no leakage |
| Scale for distance-based | KNN, SVM, PCA need scaled features |
| Stratify imbalanced | Preserve class distribution |
| Cross-validate | Reliable performance estimates |
| Check learning curves | Diagnose over/underfitting |

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Fitting scaler on all data | Use pipeline or fit only on train |
| Using accuracy for imbalanced | Use F1, ROC-AUC, or balanced accuracy |
| Too many hyperparameters | Start simple, add complexity |
| Ignoring feature importance | Use `feature_importances_` or permutation importance |

## Resources

- Docs: <https://scikit-learn.org/>
- User Guide: <https://scikit-learn.org/stable/user_guide.html>
- Algorithm Cheat Sheet: <https://scikit-learn.org/stable/tutorial/machine_learning_map/>
