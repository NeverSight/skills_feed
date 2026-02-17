---
name: modal
description: Use when "Modal", "serverless GPU", "cloud GPU", "deploy ML model", or asking about "serverless containers", "GPU compute", "batch processing", "scheduled jobs", "autoscaling ML"
version: 1.0.0
---

<!-- Adapted from: claude-scientific-skills/scientific-skills/modal -->

# Modal Serverless Cloud Platform

Serverless Python execution with GPUs, autoscaling, and pay-per-use compute.

## When to Use

- Deploy and serve ML models (LLMs, image generation)
- Run GPU-accelerated computation
- Batch process large datasets in parallel
- Schedule compute-intensive jobs
- Build serverless APIs with autoscaling

## Quick Start

```bash
# Install
pip install modal

# Authenticate
modal token new
```

```python
import modal

app = modal.App("my-app")

@app.function()
def hello():
    return "Hello from Modal!"

# Run with: modal run script.py
```

## Container Images

```python
# Build image with dependencies
image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("torch", "transformers", "numpy")
)

app = modal.App("ml-app", image=image)
```

## GPU Functions

```python
@app.function(gpu="H100")
def train_model():
    import torch
    assert torch.cuda.is_available()
    # GPU code here

# Available GPUs: T4, L4, A10, A100, L40S, H100, H200, B200
# Multi-GPU: gpu="H100:8"
```

## Web Endpoints

```python
@app.function()
@modal.web_endpoint(method="POST")
def predict(data: dict):
    result = model.predict(data["input"])
    return {"prediction": result}

# Deploy: modal deploy script.py
```

## Scheduled Jobs

```python
@app.function(schedule=modal.Cron("0 2 * * *"))  # Daily at 2 AM
def daily_backup():
    pass

@app.function(schedule=modal.Period(hours=4))  # Every 4 hours
def refresh_cache():
    pass
```

## Autoscaling

```python
@app.function()
def process_item(item_id: int):
    return analyze(item_id)

@app.local_entrypoint()
def main():
    items = range(1000)
    # Automatically parallelized across containers
    results = list(process_item.map(items))
```

## Persistent Storage

```python
volume = modal.Volume.from_name("my-data", create_if_missing=True)

@app.function(volumes={"/data": volume})
def save_results(data):
    with open("/data/results.txt", "w") as f:
        f.write(data)
    volume.commit()  # Persist changes
```

## Secrets Management

```python
@app.function(secrets=[modal.Secret.from_name("huggingface")])
def download_model():
    import os
    token = os.environ["HF_TOKEN"]
```

## ML Model Serving

```python
@app.cls(gpu="L40S")
class Model:
    @modal.enter()
    def load_model(self):
        from transformers import pipeline
        self.pipe = pipeline("text-classification", device="cuda")

    @modal.method()
    def predict(self, text: str):
        return self.pipe(text)

@app.local_entrypoint()
def main():
    model = Model()
    result = model.predict.remote("Modal is great!")
```

## Resource Configuration

```python
@app.function(
    cpu=8.0,              # 8 CPU cores
    memory=32768,         # 32 GiB RAM
    ephemeral_disk=10240, # 10 GiB disk
    timeout=3600          # 1 hour timeout
)
def memory_intensive_task():
    pass
```

## Best Practices

1. **Pin dependencies** for reproducible builds
2. **Use appropriate GPU types** - L40S for inference, H100 for training
3. **Leverage caching** via Volumes for model weights
4. **Use `.map()` for parallel processing**
5. **Import packages inside functions** if not available locally
6. **Store secrets securely** - never hardcode API keys

## vs Alternatives

| Platform | Best For |
|----------|----------|
| **Modal** | Serverless GPUs, autoscaling, Python-native |
| RunPod | GPU rental, long-running jobs |
| AWS Lambda | CPU workloads, AWS ecosystem |
| Replicate | Model hosting, simple deployments |

## Resources

- Docs: <https://modal.com/docs>
- Examples: <https://github.com/modal-labs/modal-examples>
