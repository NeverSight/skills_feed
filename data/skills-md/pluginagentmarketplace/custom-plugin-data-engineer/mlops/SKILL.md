---
name: mlops
description: MLflow, model versioning, experiment tracking, model registry, and production ML systems
sasmp_version: "1.3.0"
bonded_agent: 06-ml-ai-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: advanced
estimated_mastery_hours: 150
prerequisites: [machine-learning, containerization, python-programming]
unlocks: [llms-generative-ai]
---

# MLOps

Production machine learning systems with MLflow, model versioning, and deployment pipelines.

## Quick Start

```python
import mlflow
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib

# Configure MLflow
mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("customer-churn-prediction")

# Training with experiment tracking
with mlflow.start_run(run_name="rf-baseline"):
    # Log parameters
    params = {"n_estimators": 100, "max_depth": 10, "random_state": 42}
    mlflow.log_params(params)

    # Train model
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)

    # Evaluate and log metrics
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred, average="weighted")
    }
    mlflow.log_metrics(metrics)

    # Log model to registry
    mlflow.sklearn.log_model(
        model, "model",
        registered_model_name="churn-classifier",
        signature=mlflow.models.infer_signature(X_train, y_pred)
    )

    print(f"Run ID: {mlflow.active_run().info.run_id}")
```

## Core Concepts

### 1. Model Registry & Versioning

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Promote model to production
client.transition_model_version_stage(
    name="churn-classifier",
    version=3,
    stage="Production"
)

# Archive old version
client.transition_model_version_stage(
    name="churn-classifier",
    version=2,
    stage="Archived"
)

# Load production model
model_uri = "models:/churn-classifier/Production"
model = mlflow.sklearn.load_model(model_uri)

# Model comparison
def compare_model_versions(model_name: str, versions: list[int]) -> dict:
    results = {}
    for version in versions:
        run_id = client.get_model_version(model_name, str(version)).run_id
        run = client.get_run(run_id)
        results[version] = run.data.metrics
    return results
```

### 2. Feature Store Pattern

```python
from feast import FeatureStore, Entity, Feature, FeatureView, FileSource
from datetime import timedelta

# Define feature store
store = FeatureStore(repo_path="feature_repo/")

# Get training features
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "customer_features:total_purchases",
        "customer_features:days_since_last_order",
        "customer_features:avg_order_value"
    ]
).to_df()

# Get online features for inference
feature_vector = store.get_online_features(
    features=[
        "customer_features:total_purchases",
        "customer_features:days_since_last_order"
    ],
    entity_rows=[{"customer_id": "12345"}]
).to_dict()
```

### 3. Model Serving with FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import numpy as np

app = FastAPI()

# Load model at startup
model = mlflow.sklearn.load_model("models:/churn-classifier/Production")

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        X = np.array(request.features).reshape(1, -1)
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0].max()

        return PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            model_version="v3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}
```

### 4. CI/CD for ML

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    paths:
      - 'src/**'
      - 'data/**'

jobs:
  train-and-evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest tests/

      - name: Train model
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URI }}
        run: python src/train.py

      - name: Evaluate model
        run: python src/evaluate.py --threshold 0.85

      - name: Register model
        if: success()
        run: python src/register_model.py

  deploy:
    needs: train-and-evaluate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/model-server \
            model-server=gcr.io/$PROJECT/model:${{ github.sha }}
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **MLflow** | Experiment tracking | 2.10+ |
| **Feast** | Feature store | 0.36+ |
| **BentoML** | Model serving | 1.2+ |
| **Seldon** | K8s model serving | 1.17+ |
| **DVC** | Data versioning | 3.40+ |
| **Weights & Biases** | Experiment tracking | Latest |
| **Evidently** | Model monitoring | 0.4+ |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **Model Drift** | Accuracy drops | Data distribution change | Monitor, retrain |
| **Slow Inference** | High latency | Large model, no optimization | Quantize, distill |
| **Version Mismatch** | Prediction errors | Wrong model version | Pin versions |
| **Feature Skew** | Train/serve mismatch | Different preprocessing | Use feature store |

## Best Practices

```python
# ✅ DO: Version everything
mlflow.log_artifact("data/train.csv")
mlflow.log_params({"data_version": "v2.3"})

# ✅ DO: Test model before deployment
def test_model_performance(model, threshold=0.85):
    score = evaluate_model(model)
    assert score >= threshold, f"Model score {score} below threshold"

# ✅ DO: Monitor in production
# ✅ DO: A/B test new models

# ❌ DON'T: Deploy without validation
# ❌ DON'T: Skip rollback strategy
```

## Resources

- [MLflow Docs](https://mlflow.org/docs/latest/)
- [Made With ML](https://madewithml.com/)
- [Google ML Best Practices](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

---

**Skill Certification Checklist:**
- [ ] Can track experiments with MLflow
- [ ] Can manage model registry
- [ ] Can deploy models with FastAPI/BentoML
- [ ] Can set up CI/CD for ML
- [ ] Can monitor models in production
