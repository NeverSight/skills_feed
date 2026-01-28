---
name: mlops-deployment
description: Docker, Kubernetes, CI/CD, model monitoring, and cloud platforms. Use for deploying ML models to production, setting up pipelines, or infrastructure.
sasmp_version: "1.3.0"
bonded_agent: 06-mlops-deployment
bond_type: PRIMARY_BOND
---

# MLOps & Deployment

Deploy and maintain ML models in production with robust infrastructure.

## Quick Start

### Dockerize ML Model
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model and code
COPY model.pkl .
COPY app.py .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

# Run
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### FastAPI Model Serving
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load('model.pkl')

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: float
    probability: float

@app.post('/predict', response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        features = np.array(request.features).reshape(1, -1)
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].max()

        return {
            'prediction': float(prediction),
            'probability': float(probability)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/health')
async def health():
    return {'status': 'healthy'}
```

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      containers:
      - name: ml-model
        image: myregistry/ml-model:v1.0.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: ml-model-service
spec:
  selector:
    app: ml-model
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## CI/CD Pipeline (GitHub Actions)

```yaml
name: ML Pipeline

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest tests/ --cov=src

  train:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Train model
      run: python src/train.py

    - name: Evaluate model
      run: python src/evaluate.py

  deploy:
    needs: train
    runs-on: ubuntu-latest
    steps:
    - name: Build Docker image
      run: |
        docker build -t ${{ secrets.REGISTRY }}/ml-model:${{ github.sha }} .

    - name: Push to registry
      run: |
        docker push ${{ secrets.REGISTRY }}/ml-model:${{ github.sha }}

    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/ml-model \
          ml-model=${{ secrets.REGISTRY }}/ml-model:${{ github.sha }}
```

## Model Monitoring

```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Metrics
prediction_counter = Counter(
    'model_predictions_total',
    'Total predictions'
)

prediction_latency = Histogram(
    'model_prediction_latency_seconds',
    'Prediction latency'
)

@app.post('/predict')
async def predict(request: PredictionRequest):
    start_time = time.time()

    try:
        prediction = model.predict(request.features)
        prediction_counter.inc()

    finally:
        latency = time.time() - start_time
        prediction_latency.observe(latency)

    return {'prediction': prediction}

# Start metrics server
start_http_server(9090)
```

## Data Drift Detection

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Reference data (training)
reference = pd.read_csv('training_data.csv')

# Current production data
current = pd.read_csv('production_data.csv')

# Generate drift report
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference, current_data=current)

# Check drift
drift_detected = report.as_dict()['metrics'][0]['result']['dataset_drift']

if drift_detected:
    print("WARNING: Data drift detected!")
    trigger_retraining()
```

## MLflow Model Registry

```python
import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("http://localhost:5000")

with mlflow.start_run():
    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Log parameters
    mlflow.log_param("n_estimators", 100)

    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)

    # Log model
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="RandomForest"
    )

# Promote to production
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="RandomForest",
    version=1,
    stage="Production"
)
```

## A/B Testing

```python
@app.route('/predict', methods=['POST'])
def predict():
    user_id = request.json['user_id']
    features = request.json['features']

    # 10% traffic to model B
    if hash(user_id) % 100 < 10:
        model = model_b
        model_version = 'B'
    else:
        model = model_a
        model_version = 'A'

    prediction = model.predict([features])[0]

    # Log for analysis
    log_prediction(user_id, model_version, prediction)

    return {
        'prediction': prediction,
        'model_version': model_version
    }
```

## Cloud Deployment

### AWS SageMaker
```python
import sagemaker
from sagemaker.sklearn import SKLearn

estimator = SKLearn(
    entry_point='train.py',
    framework_version='1.0-1',
    instance_type='ml.m5.xlarge',
    role=sagemaker_role
)

estimator.fit({'training': 's3://bucket/data/train'})

# Deploy
predictor = estimator.deploy(
    initial_instance_count=2,
    instance_type='ml.m5.large'
)
```

### Google Cloud Vertex AI
```python
from google.cloud import aiplatform

aiplatform.init(project='my-project', location='us-central1')

model = aiplatform.Model.upload(
    display_name='sklearn-model',
    artifact_uri='gs://bucket/model',
    serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest'
)

endpoint = model.deploy(
    machine_type='n1-standard-2',
    min_replica_count=1,
    max_replica_count=3
)
```

## Best Practices

1. **Version everything**: Code, data, models
2. **Monitor continuously**: Performance, drift, errors
3. **Automate testing**: Unit, integration, performance
4. **Use feature flags**: Gradual rollouts
5. **Implement rollback**: Quick recovery from issues
6. **Scale horizontally**: Multiple replicas
7. **Log predictions**: For debugging and retraining
