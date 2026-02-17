---
name: ml-engineering
description: Use when "deploying ML models", "MLOps", "model serving", "feature stores", "model monitoring", or asking about "PyTorch deployment", "TensorFlow production", "RAG systems", "LLM integration", "ML infrastructure"
version: 1.0.0
---

<!-- Adapted from: claude-skills/engineering-team/senior-ml-engineer -->

# ML Engineering Guide

Production-grade ML/AI systems, MLOps, and model deployment.

## When to Use

- Deploying ML models to production
- Building ML platforms and infrastructure
- Implementing MLOps pipelines
- Integrating LLMs into production systems
- Setting up model monitoring and drift detection

## Tech Stack

| Category | Tools |
|----------|-------|
| ML Frameworks | PyTorch, TensorFlow, Scikit-learn, XGBoost |
| LLM Frameworks | LangChain, LlamaIndex, DSPy |
| Data Tools | Spark, Airflow, dbt, Kafka, Databricks |
| Deployment | Docker, Kubernetes, AWS/GCP/Azure |
| Monitoring | MLflow, Weights & Biases, Prometheus |
| Databases | PostgreSQL, BigQuery, Snowflake, Pinecone |

## Production Patterns

### Model Deployment Pipeline

```python
# Model serving with FastAPI
from fastapi import FastAPI
import torch

app = FastAPI()
model = torch.load("model.pth")

@app.post("/predict")
async def predict(data: dict):
    tensor = preprocess(data)
    with torch.no_grad():
        prediction = model(tensor)
    return {"prediction": prediction.tolist()}
```

### Feature Store Integration

```python
# Feast feature store
from feast import FeatureStore

store = FeatureStore(repo_path=".")
features = store.get_online_features(
    features=["user_features:age", "user_features:location"],
    entity_rows=[{"user_id": 123}]
).to_dict()
```

### Model Monitoring

```python
# Drift detection
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref_df, current_data=curr_df)
```

## MLOps Best Practices

### Development

- Test-driven development for ML pipelines
- Version control models and data
- Reproducible experiments with MLflow

### Production

- A/B testing infrastructure
- Canary deployments for models
- Automated retraining pipelines
- Model monitoring and drift detection

### Performance Targets

| Metric | Target |
|--------|--------|
| P50 Latency | < 50ms |
| P95 Latency | < 100ms |
| P99 Latency | < 200ms |
| Throughput | > 1000 RPS |
| Availability | 99.9% |

## LLM Integration Patterns

### RAG System

```python
# Basic RAG with LangChain
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

vectorstore = Pinecone.from_existing_index(
    index_name="docs",
    embedding=OpenAIEmbeddings()
)
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)
```

### Prompt Management

```python
# Structured prompts with DSPy
import dspy

class QA(dspy.Signature):
    """Answer questions based on context."""
    context = dspy.InputField()
    question = dspy.InputField()
    answer = dspy.OutputField()

qa = dspy.Predict(QA)
```

## Common Commands

```bash
# Development
python -m pytest tests/ -v --cov
python -m black src/
python -m pylint src/

# Training
python scripts/train.py --config prod.yaml
mlflow run . -P epochs=10

# Deployment
docker build -t model:v1 .
kubectl apply -f k8s/model-serving.yaml

# Monitoring
mlflow ui --port 5000
```

## Security & Compliance

- Authentication for model endpoints
- Data encryption (at rest & in transit)
- PII handling and anonymization
- GDPR/CCPA compliance
- Model access audit logging
