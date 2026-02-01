---
name: runpod-serverless-builder
description: Build production-ready RunPod serverless endpoints with optimized cold start times. Use when creating or modifying RunPod serverless workers for (1) vLLM-based LLM inference, (2) ComfyUI image/video generation, or (3) custom Python inference. Supports both baked models (fastest cold starts) and dynamic loading (shared models). Generates complete projects including Dockerfiles, worker handlers, startup scripts, and configuration optimized for minimal cold start latency.
---

# RunPod Serverless Builder

Build end-to-end RunPod serverless endpoints optimized for extremely short cold start times.

## Capabilities

Create production-ready RunPod serverless workers for:

1. **vLLM** - High-performance LLM inference
2. **ComfyUI** - Image/video generation with workflow support
3. **Custom Inference** - User-provided Python inference code

**Loading Strategies:**
- **Baked Models**: Models embedded in Docker image for fastest cold starts (<5s)
- **Dynamic Loading**: Models loaded from network storage at runtime (shared across workers)

## Quick Start

Use the interactive project generator:

```python
python3 scripts/init_project.py
```

This generates a complete project with:
- Optimized Dockerfile
- RunPod handler (worker.py)
- Startup scripts (for dynamic loading)
- Configuration files
- Documentation

## Project Generation Workflow

### Step 1: Run the Generator

Execute the script and answer prompts:

```python
import subprocess
skill_dir = "/path/to/runpod-serverless-builder"
subprocess.run(["python3", f"{skill_dir}/scripts/init_project.py"])
```

The script prompts for:
1. **Project name** - e.g., "my-vllm-worker"
2. **Workload type** - vLLM, ComfyUI, or Custom
3. **Loading strategy** - Baked or Dynamic
4. **Model configuration** - Model name, quantization, etc.
5. **Output directory** - Where to generate files

### Step 2: Customize Generated Files

The generator creates a complete project structure:

```
my-runpod-worker/
├── Dockerfile          # Optimized for cold starts
├── worker.py           # RunPod handler function
├── startup.sh          # Dynamic loading (if applicable)
├── requirements.txt    # Python dependencies
├── .dockerignore       # Build optimization
├── .env.example        # Environment variables
└── README.md           # Project documentation
```

Review and customize:
- **worker.py**: Modify handler logic, add custom processing
- **Dockerfile**: Add custom dependencies, adjust configurations
- **startup.sh**: Add custom initialization steps
- **requirements.txt**: Add additional Python packages

### Step 3: Build and Deploy

```bash
# Build Docker image
docker build -t my-worker:latest .

# Push to registry
docker push registry/my-worker:latest

# Deploy to RunPod Dashboard
# 1. Create template with image
# 2. Set environment variables
# 3. Create endpoint
```

## Manual Implementation (Without Generator)

If you prefer manual implementation or need to understand the patterns:

### vLLM Worker

**Baked Model Approach:**

1. Copy Dockerfile template:
```python
shutil.copy("assets/dockerfiles/vllm_baked.dockerfile", "Dockerfile")
```

2. Copy worker template:
```python
shutil.copy("assets/workers/worker_vllm.py", "worker.py")
```

3. Build with model:
```bash
docker build -t my-vllm:latest \
  --build-arg MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct" \
  --build-arg BASE_PATH="/models" \
  .
```

**Dynamic Loading Approach:**

1. Copy Dockerfile and startup script:
```python
shutil.copy("assets/dockerfiles/vllm_dynamic.dockerfile", "Dockerfile")
shutil.copy("assets/startup_scripts/startup_vllm.sh", "startup.sh")
```

2. Set environment variables in RunPod:
```bash
MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
HF_TOKEN=hf_your_token
GPU_MEMORY_UTILIZATION=0.95
```

### ComfyUI Worker

**Baked Model Approach:**

1. Use ComfyUI baked template:
```python
shutil.copy("assets/dockerfiles/comfyui_baked.dockerfile", "Dockerfile")
shutil.copy("assets/workers/worker_comfyui.py", "worker.py")
```

2. Modify Dockerfile to download models:
```dockerfile
# Add model downloads
RUN aria2c -x 16 -s 16 https://huggingface.co/... \
    -d /ComfyUI/models/checkpoints
```

**Dynamic Loading Approach:**

1. Use dynamic template with startup script:
```python
shutil.copy("assets/dockerfiles/comfyui_dynamic.dockerfile", "Dockerfile")
shutil.copy("assets/startup_scripts/startup_comfyui.sh", "startup.sh")
shutil.copy("assets/config/extra_model_paths.yaml", "extra_model_paths.yaml")
```

2. Configure network storage paths in extra_model_paths.yaml

3. Set environment variables:
```bash
GITHUB_PAT=ghp_token  # For private repos
CUSTOM_NODES=https://github.com/org/node1.git,https://github.com/org/node2.git
```

### Custom Inference Worker

1. Use custom templates:
```python
shutil.copy("assets/dockerfiles/custom_inference.dockerfile", "Dockerfile")
shutil.copy("assets/workers/worker_custom.py", "worker.py")
```

2. Implement your inference logic in worker.py:
```python
def initialize_model():
    # Load your model
    return your_model

def handler(job):
    model = initialize_model()
    # Your inference logic
    result = model.predict(job["input"])
    return {"result": result}
```

## Handler Patterns

### vLLM Handler

```python
from vllm import LLM, SamplingParams

llm = None

def initialize_model():
    global llm
    if llm is None:
        llm = LLM(model=MODEL_NAME, gpu_memory_utilization=0.95)
    return llm

def handler(job):
    model = initialize_model()
    messages = job["input"]["messages"]

    # Apply chat template
    tokenizer = model.get_tokenizer()
    prompt = tokenizer.apply_chat_template(messages, tokenize=False)

    # Generate
    outputs = model.generate([prompt], SamplingParams(...))
    return {"text": outputs[0].outputs[0].text}
```

### ComfyUI Handler

```python
def update_workflow(workflow, parameters):
    # Update prompt node
    workflow[parameters["prompt_node_id"]]["inputs"]["text"] = parameters["prompt"]
    # Update seed node
    workflow[parameters["seed_node_id"]]["inputs"]["seed"] = parameters.get("seed", 42)
    return workflow

def handler(job):
    # Load workflow JSON
    with open(job["input"]["workflow_path"]) as f:
        workflow = json.load(f)

    # Update with parameters
    workflow = update_workflow(workflow, job["input"])

    # Execute with ComfyUI API
    output = execute_comfyui_workflow(workflow)
    return {"image_base64": output}
```

## Cold Start Optimization

Key strategies (see `references/cold_start_optimization.md` for details):

### Baked Models Strategy
- Models embedded in image
- Target: <5 second cold starts
- Best for: Small-medium models, latency-critical workloads

### Dynamic Loading Strategy
- Models on network storage
- Target: <60 second cold starts
- Best for: Large models, shared across workers

### Dockerfile Optimization
```dockerfile
# Use BuildKit cache mounts
RUN --mount=type=cache,target=/root/.cache/pip pip install ...

# Order from least to most frequently changing
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY worker.py /

# Combine commands to reduce layers
RUN apt-get update && apt-get install -y pkg1 pkg2 && apt-get clean
```

### Worker Optimization
```python
# Module-level initialization (runs once per container)
MODEL = load_model()  # Cached across warm starts

def handler(job):
    # MODEL already loaded for warm starts
    return MODEL.predict(job["input"])
```

## Reference Documentation

Consult reference files for detailed guidance:

- **`references/cold_start_optimization.md`** - Comprehensive cold start optimization strategies
- **`references/vllm_guide.md`** - vLLM configuration, API patterns, troubleshooting
- **`references/comfyui_guide.md`** - ComfyUI workflow management, custom nodes, video workflows

Load references when needed:
```python
# For cold start optimization questions
with open("references/cold_start_optimization.md") as f:
    cold_start_guide = f.read()

# For vLLM-specific configuration
with open("references/vllm_guide.md") as f:
    vllm_guide = f.read()

# For ComfyUI workflow patterns
with open("references/comfyui_guide.md") as f:
    comfyui_guide = f.read()
```

## Common Scenarios

### Scenario 1: vLLM with Baked Model

**User request:** "Create a RunPod endpoint for Llama 3.1 8B with the fastest possible cold starts"

**Implementation:**
1. Run init_project.py or copy vllm_baked templates
2. Set MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct" in Dockerfile
3. Build with model baked in
4. Deploy to RunPod

### Scenario 2: ComfyUI with Dynamic Loading

**User request:** "Build a ComfyUI video generation endpoint that loads models from network storage"

**Implementation:**
1. Run init_project.py selecting ComfyUI + Dynamic
2. Configure extra_model_paths.yaml for network storage
3. Implement workflow update logic in worker.py
4. Deploy with CUSTOM_NODES environment variable

### Scenario 3: Custom Inference with User Code

**User request:** "I have a custom object detection model, help me deploy it to RunPod"

**Implementation:**
1. Run init_project.py selecting Custom
2. Copy user's model code to inference/ directory
3. Implement initialize_model() and handler() in worker.py
4. Add dependencies to requirements.txt
5. Build and deploy

## Troubleshooting

### Slow Cold Starts
1. Check if models are baked vs downloaded at runtime
2. Review Dockerfile layer caching
3. Minimize dependencies in requirements.txt
4. Consult `references/cold_start_optimization.md`

### Worker Errors
1. Check logs in RunPod dashboard
2. Test worker.py locally: `python3 worker.py`
3. Verify environment variables in .env.example
4. Check model loading in initialize_model()

### Build Failures
1. Verify base image compatibility
2. Check requirements.txt for conflicting versions
3. Test Dockerfile locally: `docker build .`

## Best Practices

1. **Always use the generator first** - It implements proven patterns
2. **Start with baked models** - Optimize for cold starts, then consider dynamic loading if needed
3. **Pin dependency versions** - Avoid "latest" tags and unpinned packages
4. **Profile cold starts** - Measure and optimize based on actual metrics
5. **Test locally before deploying** - Run worker.py and docker build locally
6. **Consult references** - Load reference docs for detailed guidance on specific topics
