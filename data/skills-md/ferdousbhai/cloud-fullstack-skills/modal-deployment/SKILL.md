---
name: modal-deployment
description: Run Python code in the cloud with serverless containers, GPUs, and autoscaling. Use when deploying ML models, running batch jobs, scheduling tasks, serving APIs with GPU acceleration, or scaling compute-intensive workloads. Triggers on requests for serverless GPU infrastructure, LLM inference, model training/fine-tuning, parallel data processing, cron jobs in the cloud, or deploying Python web endpoints.
---

# Modal

Modal is a serverless platform for running Python in the cloud with zero configuration. Define everything in code—no YAML, Docker, or Kubernetes required.

## Quick Start

```python
import modal

app = modal.App("my-app")

@app.function()
def hello():
    return "Hello from Modal!"

@app.local_entrypoint()
def main():
    print(hello.remote())
```

Run: `modal run app.py`

## Core Concepts

### Functions
Decorate Python functions to run remotely:

```python
@app.function(gpu="H100", memory=32768, timeout=600)
def train_model(data):
    # Runs on H100 GPU with 32GB RAM, 10min timeout
    return model.fit(data)
```

### Images
Define container environments via method chaining:

```python
image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("ffmpeg", "libsndfile1")
    .uv_pip_install("torch", "transformers", "numpy")
    .env({"CUDA_VISIBLE_DEVICES": "0"})
)

app = modal.App("ml-app", image=image)
```

Key image methods:
- `.debian_slim()` / `.micromamba()` - Base images
- `.uv_pip_install()` / `.pip_install()` - Python packages
- `.apt_install()` - System packages
- `.run_commands()` - Shell commands
- `.add_local_python_source()` - Local modules
- `.env()` - Environment variables

### GPUs
Attach GPUs with a single parameter:

```python
@app.function(gpu="H100")      # Single H100
@app.function(gpu="A100-80GB") # 80GB A100
@app.function(gpu="H100:4")    # 4x H100
@app.function(gpu=["H100", "A100-40GB:2"])  # Fallback options
```

Available: B200, H200, H100, A100-80GB, A100-40GB, L40S, L4, A10G, T4

### Classes with Lifecycle Hooks
Load models once at container startup:

```python
@app.cls(gpu="L40S")
class Model:
    @modal.enter()
    def load(self):
        self.model = load_pretrained("model-name")
    
    @modal.method()
    def predict(self, x):
        return self.model(x)

# Usage
Model().predict.remote(data)
```

### Web Endpoints
Deploy APIs instantly:

```python
@app.function()
@modal.fastapi_endpoint()
def api(text: str):
    return {"result": process(text)}

# For complex apps
@app.function()
@modal.asgi_app()
def fastapi_app():
    from fastapi import FastAPI
    web = FastAPI()
    
    @web.get("/health")
    def health():
        return {"status": "ok"}
    
    return web
```

### Volumes (Persistent Storage)

```python
volume = modal.Volume.from_name("my-data", create_if_missing=True)

@app.function(volumes={"/data": volume})
def save_file(content: str):
    with open("/data/output.txt", "w") as f:
        f.write(content)
    volume.commit()  # Persist changes
```

### Secrets

```python
@app.function(secrets=[modal.Secret.from_name("my-api-key")])
def call_api():
    import os
    key = os.environ["API_KEY"]
```

Create secrets: Dashboard or `modal secret create my-secret KEY=value`

### Dicts (Distributed Key-Value Store)

```python
cache = modal.Dict.from_name("my-cache", create_if_missing=True)

@app.function()
def cached_compute(key: str):
    if key in cache:
        return cache[key]
    result = expensive_computation(key)
    cache[key] = result
    return result
```

### Queues (Distributed FIFO)

```python
queue = modal.Queue.from_name("task-queue", create_if_missing=True)

@app.function()
def producer():
    queue.put_many([{"task": i} for i in range(10)])

@app.function()
def consumer():
    while task := queue.get(timeout=60):
        process(task)
```

### Parallel Processing

```python
# Map over inputs (auto-parallelized)
results = list(process.map(items))

# Spawn async jobs
calls = [process.spawn(item) for item in items]
results = [call.get() for call in calls]

# Batch processing (up to 1M inputs)
process.spawn_map(range(100_000))
```

### Scheduling

```python
@app.function(schedule=modal.Period(hours=1))
def hourly_job():
    pass

@app.function(schedule=modal.Cron("0 9 * * 1-5"))  # 9am weekdays
def daily_report():
    pass
```

## CLI Commands

```bash
modal run app.py          # Run locally-triggered function
modal serve app.py        # Hot-reload web endpoints
modal deploy app.py       # Deploy persistently
modal shell app.py        # Interactive shell in container
modal app list            # List deployed apps
modal app logs <name>     # Stream logs
modal volume list         # List volumes
modal secret list         # List secrets
```

## Common Patterns

### LLM Inference

```python
@app.cls(gpu="H100", image=image)
class LLM:
    @modal.enter()
    def load(self):
        from vllm import LLM
        self.llm = LLM("meta-llama/Llama-3-8B")
    
    @modal.method()
    def generate(self, prompt: str):
        return self.llm.generate(prompt)
```

### Download Models at Build Time

```python
def download_model():
    from huggingface_hub import snapshot_download
    snapshot_download("model-id", local_dir="/models")

image = (
    modal.Image.debian_slim()
    .pip_install("huggingface-hub")
    .run_function(download_model)
)
```

### Concurrency for I/O-bound Work

```python
@app.function()
@modal.concurrent(max_inputs=100)
async def fetch_urls(url: str):
    async with aiohttp.ClientSession() as session:
        return await session.get(url)
```

### Memory Snapshots (Faster Cold Starts)

```python
@app.cls(enable_memory_snapshot=True, gpu="A10G")
class FastModel:
    @modal.enter(snap=True)
    def load(self):
        self.model = load_model()  # Snapshot this state
```

## Autoscaling

```python
@app.function(
    min_containers=2,       # Always keep 2 warm
    max_containers=100,     # Scale up to 100
    buffer_containers=5,    # Extra buffer for bursts
    scaledown_window=300,   # Keep idle for 5 min
)
def serve():
    pass
```

## Best Practices

1. **Put imports inside functions** when packages aren't installed locally
2. **Use `@modal.enter()`** for expensive initialization (model loading)
3. **Pin dependency versions** for reproducible builds
4. **Use Volumes** for model weights and persistent data
5. **Use memory snapshots** for sub-second cold starts in production
6. **Set appropriate timeouts** for long-running tasks
7. **Use `min_containers=1`** for production APIs to keep containers warm
8. **Use absolute imports** with full package paths (not relative imports)

### Fast Image Builds with uv_sync

Use `.uv_sync()` instead of `.pip_install()` for faster dependency installation:

```python
# In pyproject.toml, define dependency groups:
# [dependency-groups]
# modal = ["fastapi", "pydantic-ai>=1.0.0", "logfire"]

image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_sync("agent", groups=["modal"], frozen=False)
    .add_local_python_source("agent.src")  # Use dot notation for packages
)
```

**Key points:**
- Deploy from project root: `modal deploy agent/src/api.py`
- Use dot notation in `.add_local_python_source("package.subpackage")`
- Imports must match: `from agent.src.config import ...` (not relative `from .config`)

### Logfire Observability

Add observability with Logfire (especially for pydantic-ai):

```python
@app.cls(image=image, secrets=[..., modal.Secret.from_name("logfire")], min_containers=1)
class Web:
    @modal.enter()
    def startup(self):
        import logfire
        logfire.configure(send_to_logfire="if-token-present", environment="production", service_name="my-agent")
        logfire.instrument_pydantic_ai()
        self.agent = create_agent()
```

## Reference Documentation

See `references/` for detailed guides on images, functions, GPUs, scaling, web endpoints, storage, dicts, queues, sandboxes, and networking.

Official docs: https://modal.com/docs
