---
name: ml-engineer
description: Implement ML pipelines, model serving, and feature engineering. Use for ML model integration or production deployment.
---

# ML Engineering

Build production machine learning systems.

## When to use

- Model serving and deployment
- Feature engineering
- ML pipeline design
- Model monitoring

## Model serving

### FastAPI endpoint

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load("model.pkl")

class PredictRequest(BaseModel):
    features: list[float]

class PredictResponse(BaseModel):
    prediction: float
    confidence: float

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    try:
        X = np.array(request.features).reshape(1, -1)
        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0].max()
        return PredictResponse(prediction=pred, confidence=proba)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model_version": "1.0.0"}
```

### Batch inference

```python
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

def predict_batch(df: pd.DataFrame, batch_size: int = 1000):
    results = []

    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        predictions = model.predict(batch)
        results.extend(predictions)

    return results

# Parallel batch processing
def parallel_predict(df: pd.DataFrame, n_workers: int = 4):
    chunks = np.array_split(df, n_workers)

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(executor.map(predict_batch, chunks))

    return np.concatenate(results)
```

## Feature engineering

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

numeric_features = ['age', 'income', 'score']
categorical_features = ['category', 'region']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numeric_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ]), categorical_features)
    ]
)

# Full pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', model)
])
```

## Model monitoring

```python
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import DataDriftTable, DatasetSummaryMetric

def check_data_drift(reference_data, current_data):
    column_mapping = ColumnMapping(
        target='label',
        prediction='prediction',
        numerical_features=['feature1', 'feature2'],
        categorical_features=['category']
    )

    report = Report(metrics=[
        DatasetSummaryMetric(),
        DataDriftTable(),
    ])

    report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )

    return report.as_dict()
```

## A/B testing

```python
import hashlib

def get_model_variant(user_id: str, experiment: str) -> str:
    """Deterministic assignment based on user_id"""
    hash_input = f"{user_id}:{experiment}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    return "control" if hash_value % 100 < 50 else "treatment"

def predict_with_experiment(user_id: str, features):
    variant = get_model_variant(user_id, "model_v2_test")

    if variant == "treatment":
        prediction = model_v2.predict(features)
    else:
        prediction = model_v1.predict(features)

    log_prediction(user_id, variant, prediction)
    return prediction
```

## Examples

**Input:** "Deploy model as API"
**Action:** Create FastAPI endpoint, add health check, containerize

**Input:** "Set up model monitoring"
**Action:** Implement drift detection, prediction logging, alerting
