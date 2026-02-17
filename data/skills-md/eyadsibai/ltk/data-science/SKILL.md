---
name: data-science
description: Use when "statistical modeling", "A/B testing", "experiment design", "causal inference", "predictive modeling", or asking about "hypothesis testing", "feature engineering", "data analysis", "pandas", "scikit-learn"
version: 1.0.0
---

<!-- Adapted from: claude-skills/engineering-team/senior-data-scientist -->

# Data Science Guide

Statistical modeling, experimentation, and advanced analytics.

## When to Use

- Designing A/B tests and experiments
- Building predictive models
- Performing causal analysis
- Feature engineering
- Statistical hypothesis testing

## Tech Stack

| Category | Tools |
|----------|-------|
| Languages | Python, SQL, R |
| Analysis | NumPy, Pandas, SciPy |
| ML | Scikit-learn, XGBoost, LightGBM |
| Visualization | Matplotlib, Seaborn, Plotly |
| Statistics | Statsmodels, PyMC |
| Notebooks | Jupyter, VS Code |

## Experiment Design

### A/B Test Framework

```python
import scipy.stats as stats
import numpy as np

def calculate_sample_size(baseline_rate, mde, alpha=0.05, power=0.8):
    """Calculate required sample size for A/B test."""
    effect_size = mde / np.sqrt(baseline_rate * (1 - baseline_rate))
    analysis = stats.TTestIndPower()
    return int(analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        alternative='two-sided'
    ))

# Example: 5% baseline, 10% relative lift
n = calculate_sample_size(0.05, 0.005)
print(f"Required sample size per group: {n}")
```

### Statistical Significance

```python
def analyze_ab_test(control, treatment):
    """Analyze A/B test results."""
    # Two-proportion z-test
    n1, n2 = len(control), len(treatment)
    p1, p2 = control.mean(), treatment.mean()
    p_pool = (control.sum() + treatment.sum()) / (n1 + n2)

    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return {
        'control_rate': p1,
        'treatment_rate': p2,
        'lift': (p2 - p1) / p1,
        'p_value': p_value,
        'significant': p_value < 0.05
    }
```

## Feature Engineering

### Common Patterns

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

def engineer_features(df):
    """Feature engineering pipeline."""
    # Temporal features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6])

    # Aggregations
    df['user_avg_spend'] = df.groupby('user_id')['amount'].transform('mean')
    df['user_transaction_count'] = df.groupby('user_id')['amount'].transform('count')

    # Ratios
    df['spend_vs_avg'] = df['amount'] / df['user_avg_spend']

    return df
```

### Feature Selection

```python
from sklearn.feature_selection import mutual_info_classif

def select_features(X, y, k=10):
    """Select top k features by mutual information."""
    mi_scores = mutual_info_classif(X, y)
    top_k = np.argsort(mi_scores)[-k:]
    return X.columns[top_k].tolist()
```

## Model Evaluation

### Cross-Validation

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

def evaluate_model(model, X, y):
    """Robust model evaluation."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    scores = {
        'accuracy': cross_val_score(model, X, y, cv=cv, scoring='accuracy'),
        'precision': cross_val_score(model, X, y, cv=cv, scoring='precision'),
        'recall': cross_val_score(model, X, y, cv=cv, scoring='recall'),
        'auc': cross_val_score(model, X, y, cv=cv, scoring='roc_auc')
    }

    return {k: f"{v.mean():.3f} (+/- {v.std()*2:.3f})" for k, v in scores.items()}
```

## Causal Inference

### Propensity Score Matching

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

def propensity_matching(df, treatment_col, features):
    """Match treatment and control using propensity scores."""
    # Estimate propensity scores
    ps_model = LogisticRegression()
    ps_model.fit(df[features], df[treatment_col])
    df['propensity'] = ps_model.predict_proba(df[features])[:, 1]

    # Match nearest neighbors
    treated = df[df[treatment_col] == 1]
    control = df[df[treatment_col] == 0]

    nn = NearestNeighbors(n_neighbors=1)
    nn.fit(control[['propensity']])
    distances, indices = nn.kneighbors(treated[['propensity']])

    return treated, control.iloc[indices.flatten()]
```

## Best Practices

### Analysis Workflow

1. Define hypothesis clearly
2. Calculate required sample size
3. Design experiment (randomization)
4. Collect data with quality checks
5. Analyze with appropriate tests
6. Report with confidence intervals

### Common Pitfalls

- Multiple comparisons without correction
- Peeking at results before sample size reached
- Simpson's paradox in aggregations
- Survivorship bias in cohort analysis
- Correlation vs causation confusion
