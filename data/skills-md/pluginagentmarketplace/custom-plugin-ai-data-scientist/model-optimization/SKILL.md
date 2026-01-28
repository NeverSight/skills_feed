---
name: model-optimization
description: Quantization, pruning, AutoML, hyperparameter tuning, and performance optimization. Use for improving model performance, reducing size, or automated ML.
sasmp_version: "1.3.0"
bonded_agent: 06-mlops-deployment
bond_type: SECONDARY_BOND
---

# Model Optimization

Optimize models for better performance, efficiency, and faster inference.

## Hyperparameter Tuning

### Grid Search
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
```

### Bayesian Optimization
```python
from skopt import BayesSearchCV

param_space = {
    'n_estimators': (100, 500),
    'max_depth': (5, 50),
    'learning_rate': (0.01, 0.3, 'log-uniform')
}

bayes_search = BayesSearchCV(
    xgb.XGBClassifier(),
    param_space,
    n_iter=50,
    cv=5,
    scoring='f1_weighted'
)

bayes_search.fit(X_train, y_train)
```

### Optuna
```python
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3)
    }

    model = xgb.XGBClassifier(**params)
    score = cross_val_score(model, X_train, y_train,
                           cv=5, scoring='f1').mean()
    return score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

print(f"Best params: {study.best_params}")
print(f"Best score: {study.best_value:.3f}")
```

## Model Compression

### Quantization (PyTorch)
```python
import torch

# Post-training dynamic quantization
model_fp32 = MyModel()
model_int8 = torch.quantization.quantize_dynamic(
    model_fp32,
    {torch.nn.Linear},
    dtype=torch.qint8
)

# 4x smaller model, 2-4x faster inference

# Quantization-aware training
model = MyModel()
model.qconfig = torch.quantization.get_default_qat_qconfig('fbgemm')
model_prepared = torch.quantization.prepare_qat(model)

# Train
for epoch in range(epochs):
    train(model_prepared)

model_quantized = torch.quantization.convert(model_prepared)
```

### Pruning
```python
import torch.nn.utils.prune as prune

# Global unstructured pruning
parameters_to_prune = [
    (module, 'weight') for module in model.modules()
    if isinstance(module, torch.nn.Linear)
]

prune.global_unstructured(
    parameters_to_prune,
    pruning_method=prune.L1Unstructured,
    amount=0.2  # Remove 20% of weights
)

# Remove pruning reparametrization
for module, _ in parameters_to_prune:
    prune.remove(module, 'weight')
```

### Knowledge Distillation
```python
import torch.nn.functional as F

def distillation_loss(student_logits, teacher_logits, labels, T=3.0, alpha=0.5):
    """
    Distillation loss: combination of soft targets from teacher
    and hard targets from ground truth
    """
    # Soft targets (knowledge from teacher)
    soft_targets = F.softmax(teacher_logits / T, dim=1)
    soft_prob = F.log_softmax(student_logits / T, dim=1)
    soft_loss = F.kl_div(soft_prob, soft_targets, reduction='batchmean') * (T ** 2)

    # Hard targets (ground truth)
    hard_loss = F.cross_entropy(student_logits, labels)

    # Combined loss
    return alpha * soft_loss + (1 - alpha) * hard_loss

# Train student model
teacher_model.eval()
student_model.train()

for images, labels in train_loader:
    with torch.no_grad():
        teacher_logits = teacher_model(images)

    student_logits = student_model(images)
    loss = distillation_loss(student_logits, teacher_logits, labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

## AutoML

### Auto-sklearn
```python
import autosklearn.classification

automl = autosklearn.classification.AutoSklearnClassifier(
    time_left_for_this_task=3600,  # 1 hour
    per_run_time_limit=300,
    memory_limit=3072
)

automl.fit(X_train, y_train)
predictions = automl.predict(X_test)

print(automl.leaderboard())
print(automl.show_models())
```

### H2O AutoML
```python
import h2o
from h2o.automl import H2OAutoML

h2o.init()

train = h2o.H2OFrame(pd.concat([X_train, y_train], axis=1))
test = h2o.H2OFrame(pd.concat([X_test, y_test], axis=1))

aml = H2OAutoML(max_runtime_secs=3600, max_models=20)
aml.train(x=X_train.columns.tolist(), y='target',
         training_frame=train)

# Leaderboard
lb = aml.leaderboard
print(lb)

# Best model
best_model = aml.leader
predictions = best_model.predict(test)
```

### TPOT
```python
from tpot import TPOTClassifier

tpot = TPOTClassifier(
    generations=5,
    population_size=50,
    verbosity=2,
    random_state=42,
    n_jobs=-1
)

tpot.fit(X_train, y_train)
print(f"Score: {tpot.score(X_test, y_test):.3f}")

# Export best pipeline
tpot.export('best_pipeline.py')
```

## Feature Selection

```python
from sklearn.feature_selection import (
    SelectKBest, f_classif, RFE, SelectFromModel
)

# Univariate selection
selector = SelectKBest(f_classif, k=10)
X_new = selector.fit_transform(X, y)

# Recursive Feature Elimination
estimator = RandomForestClassifier()
rfe = RFE(estimator, n_features_to_select=10)
X_new = rfe.fit_transform(X, y)

# Model-based selection
selector = SelectFromModel(RandomForestClassifier(), max_features=10)
X_new = selector.fit_transform(X, y)
```

## Performance Optimization

### Inference Optimization (ONNX)
```python
import torch.onnx

# Export PyTorch to ONNX
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    opset_version=11,
    input_names=['input'],
    output_names=['output']
)

# Run with ONNX Runtime
import onnxruntime as ort

session = ort.InferenceSession("model.onnx")
input_name = session.get_inputs()[0].name
output = session.run(None, {input_name: input_data})
```

### TensorRT (NVIDIA GPU)
```python
import tensorrt as trt

# Convert ONNX to TensorRT
logger = trt.Logger(trt.Logger.WARNING)
builder = trt.Builder(logger)
network = builder.create_network()
parser = trt.OnnxParser(network, logger)

with open('model.onnx', 'rb') as f:
    parser.parse(f.read())

config = builder.create_builder_config()
config.max_workspace_size = 1 << 30  # 1GB

engine = builder.build_engine(network, config)

# 10x faster inference on GPU
```

## Learning Rate Scheduling

```python
from torch.optim.lr_scheduler import StepLR, CosineAnnealingLR

# Step decay
scheduler = StepLR(optimizer, step_size=30, gamma=0.1)

# Cosine annealing
scheduler = CosineAnnealingLR(optimizer, T_max=100)

# Training loop
for epoch in range(epochs):
    train(model, optimizer)
    scheduler.step()
```

## Early Stopping

```python
class EarlyStopping:
    def __init__(self, patience=7, min_delta=0):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False

    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.counter = 0

# Usage
early_stopping = EarlyStopping(patience=10)

for epoch in range(epochs):
    train_loss = train(model)
    val_loss = validate(model)

    early_stopping(val_loss)
    if early_stopping.early_stop:
        print("Early stopping triggered")
        break
```

## Best Practices

1. **Start simple**: Baseline model first
2. **Profile before optimizing**: Find bottlenecks
3. **Measure everything**: Track metrics
4. **Trade-offs**: Accuracy vs speed vs size
5. **Validate improvements**: A/B testing
6. **Automate**: Use AutoML for initial exploration
