---
name: flash
description: Complete knowledge of the runpod-flash framework - SDK, CLI, architecture, deployment, and codebase. Use when working with runpod-flash code, writing @remote functions, configuring resources, debugging deployments, or understanding the framework internals. Triggers on "flash", "runpod-flash", "@remote", "serverless", "deploy", "LiveServerless", "LoadBalancer", "GpuGroup".
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# Runpod Flash

**runpod-flash** (v1.0.0) is a Python SDK for distributed execution of AI workloads on RunPod's serverless infrastructure. Write Python functions locally, decorate with `@remote`, and Flash handles GPU/CPU provisioning, dependency management, and data transfer.

- **Package**: `pip install runpod-flash`
- **Import**: `from runpod_flash import remote, LiveServerless, GpuGroup, ...`
- **CLI**: `flash`
- **Python**: >=3.10, <3.15

## Getting Started

### 1. Install Flash

```bash
pip install runpod-flash
```

### 2. Set your RunPod API key

Get a key from [RunPod account settings](https://docs.runpod.io/get-started/api-keys), then either export it:

```bash
export RUNPOD_API_KEY=your_api_key_here
```

Or save in a `.env` file in your project directory (Flash auto-loads via `python-dotenv`):

```bash
echo "RUNPOD_API_KEY=your_api_key_here" > .env
```

### 3. Write and run a remote function

```python
import asyncio
from runpod_flash import remote, LiveServerless

gpu_config = LiveServerless(name="my-first-worker")

@remote(resource_config=gpu_config, dependencies=["torch"])
async def gpu_task(data):
    import torch
    tensor = torch.tensor(data, device="cuda")
    return {"sum": tensor.sum().item(), "gpu": torch.cuda.get_device_name(0)}

async def main():
    result = await gpu_task([1, 2, 3, 4, 5])
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

First run takes ~1 minute (endpoint provisioning). Subsequent runs take ~1 second.

### 4. Or create a Flash API project

```bash
flash init my_project
cd my_project
pip install -r requirements.txt
# Edit .env and add your RUNPOD_API_KEY
flash run                    # Start local FastAPI server at localhost:8888
flash run --auto-provision   # Pre-deploy all endpoints (faster testing)
```

API explorer available at `http://localhost:8888/docs`.

### 5. Build and deploy to production

```bash
flash build                              # Scan @remote functions, package artifact
flash build --exclude torch,torchvision  # Exclude packages in base image (500MB limit)
flash deploy new production              # Create deployment environment
flash deploy send production             # Upload and deploy
flash deploy list                        # List environments
flash deploy info production             # Show details
flash deploy delete production           # Tear down
```

## Core Concept: The @remote Decorator

The `@remote` decorator marks functions for remote execution on RunPod infrastructure. Code inside runs remotely; code outside runs locally.

```python
from runpod_flash import remote, LiveServerless

config = LiveServerless(name="my-worker")

@remote(resource_config=config, dependencies=["torch", "numpy"])
async def gpu_compute(data):
    import torch  # MUST import inside function
    tensor = torch.tensor(data, device="cuda")
    return {"result": tensor.sum().item()}

result = await gpu_compute([1, 2, 3])
```

### @remote Signature

```python
def remote(
    resource_config: ServerlessResource,  # Required: GPU/CPU config
    dependencies: list[str] = None,       # pip packages
    system_dependencies: list[str] = None,# apt-get packages
    accelerate_downloads: bool = True,    # CDN acceleration
    local: bool = False,                  # Execute locally (testing)
    method: str = None,                   # HTTP method (LoadBalancer only)
    path: str = None,                     # HTTP path (LoadBalancer only)
)
```

### CRITICAL: Cloudpickle Scoping Rules

Functions decorated with `@remote` are serialized with cloudpickle. They can ONLY access:
- Function parameters
- Local variables defined inside the function
- Imports done inside the function
- Built-in Python functions

They CANNOT access: module-level imports, global variables, external functions/classes.

```python
# WRONG - external references
import torch
@remote(resource_config=config)
async def bad(data):
    return torch.tensor(data)  # torch not accessible

# CORRECT - everything inside
@remote(resource_config=config, dependencies=["torch"])
async def good(data):
    import torch
    return torch.tensor(data)
```

### Return Behavior

- Decorated function is always awaitable (`await my_func(...)`)
- Queue-based resources return `JobOutput` with `.output`, `.error`, `.status`
- Load-balanced resources return your dict directly

## Resource Configuration Classes

Choose based on execution model and environment:

| Class | Queue | HTTP | Environment | Use Case |
|-------|-------|------|-------------|----------|
| `LiveServerless` | Yes | No | Dev | GPU with retries, remote code exec |
| `CpuLiveServerless` | Yes | No | Dev | CPU with retries, remote code exec |
| `ServerlessEndpoint` | Yes | No | Prod | GPU, custom Docker images |
| `CpuServerlessEndpoint` | Yes | No | Prod | CPU, custom Docker images |
| `LiveLoadBalancer` | No | Yes | Dev | GPU low-latency HTTP APIs |
| `CpuLiveLoadBalancer` | No | Yes | Dev | CPU low-latency HTTP APIs |
| `LoadBalancerSlsResource` | No | Yes | Prod | GPU production HTTP |
| `CpuLoadBalancerSlsResource` | No | Yes | Prod | CPU production HTTP |

**Queue-based**: Best for batch, long-running tasks, automatic retries.
**Load-balanced**: Best for real-time APIs, low-latency, direct HTTP routing.

**Live\* classes**: Fixed optimized Docker image, full remote code execution.
**Non-Live classes**: Custom Docker images, dictionary payload only.

### Common Parameters

```python
LiveServerless(
    name="worker-name",              # Required, unique
    gpus=[GpuGroup.AMPERE_80],       # GPU type(s)
    workersMin=0,                     # Min workers
    workersMax=3,                     # Max workers
    idleTimeout=300,                  # Seconds before scale-down
    networkVolumeId="vol_abc123",     # Persistent storage
    env={"KEY": "value"},             # Environment variables
    template=PodTemplate(containerDiskInGb=100),
)
```

### GPU Groups (GpuGroup enum)

- `GpuGroup.ANY` - Any available (not for production)
- `GpuGroup.AMPERE_16` - RTX A4000, 16GB
- `GpuGroup.AMPERE_24` - RTX A5000, 24GB
- `GpuGroup.AMPERE_48` - A40/RTX A6000, 48GB
- `GpuGroup.AMPERE_80` - A100, 80GB
- `GpuGroup.ADA_24` - RTX 4090, 24GB
- `GpuGroup.ADA_32_PRO` - RTX 5090, 32GB
- `GpuGroup.ADA_48_PRO` - RTX 6000 Ada, 48GB
- `GpuGroup.ADA_80_PRO` - H100, 80GB
- `GpuGroup.HOPPER_141` - H200, 141GB

### CPU Instance Types (CpuInstanceType enum)

Format: `CPU{generation}{type}_{vcpu}_{memory_gb}`

| Instance Type | Gen | Type | vCPU | RAM |
|--------------|-----|------|------|-----|
| `CPU3G_1_4` | 3rd | General | 1 | 4GB |
| `CPU3G_2_8` | 3rd | General | 2 | 8GB |
| `CPU3G_4_16` | 3rd | General | 4 | 16GB |
| `CPU3G_8_32` | 3rd | General | 8 | 32GB |
| `CPU3C_1_2` | 3rd | Compute | 1 | 2GB |
| `CPU3C_2_4` | 3rd | Compute | 2 | 4GB |
| `CPU3C_4_8` | 3rd | Compute | 4 | 8GB |
| `CPU3C_8_16` | 3rd | Compute | 8 | 16GB |
| `CPU5C_1_2` | 5th | Compute | 1 | 2GB |
| `CPU5C_2_4` | 5th | Compute | 2 | 4GB |
| `CPU5C_4_8` | 5th | Compute | 4 | 8GB |
| `CPU5C_8_16` | 5th | Compute | 8 | 16GB |

Use with `instanceIds` parameter:

```python
config = LiveServerless(
    name="cpu-worker",
    instanceIds=[CpuInstanceType.CPU5C_4_8],
    workersMax=5,
)
```

Or use explicit CPU classes:

```python
from runpod_flash import CpuLiveServerless
config = CpuLiveServerless(name="cpu-worker", workersMax=5)
```

### PodTemplate

Override pod-level settings:

```python
from runpod_flash import PodTemplate

template = PodTemplate(
    containerDiskInGb=100,
    env=[{"key": "PYTHONPATH", "value": "/workspace"}],
)

config = LiveServerless(name="worker", template=template)
```

### NetworkVolume

```python
from runpod_flash import NetworkVolume, DataCenter

volume = NetworkVolume(
    name="model-storage",
    size=100,  # GB
    dataCenterId=DataCenter.EU_RO_1,
)
```

### LoadBalancer Resources

When using `LoadBalancerSlsResource` or `LiveLoadBalancer`:
- `method` and `path` are **required** on `@remote`
- `path` must start with "/"
- `method` must be one of: GET, POST, PUT, DELETE, PATCH

```python
from runpod_flash import remote, LiveLoadBalancer

api = LiveLoadBalancer(name="api-service")

@remote(api, method="POST", path="/api/process")
async def process(x: int, y: int):
    return {"result": x + y}

@remote(api, method="GET", path="/api/health")
def health():
    return {"status": "ok"}
```

Key differences from queue-based:
- Direct HTTP routing (no queue), lower latency
- Returns dict directly (no JobOutput wrapper)
- No automatic retries

## Error Handling

### Queue-Based Resources

```python
job_output = await my_function(data)
if job_output.error:
    print(f"Failed: {job_output.error}")
else:
    result = job_output.output
```

`JobOutput` fields: `id`, `status`, `output`, `error`, `started_at`, `ended_at`

### Load-Balanced Resources

```python
try:
    result = await my_function(data)  # Returns dict directly
except Exception as e:
    print(f"Error: {e}")
```

### Runtime Exceptions

```
FlashRuntimeError (base)
  RemoteExecutionError      # Remote function failed
  SerializationError        # cloudpickle serialization failed
  GraphQLError              # GraphQL base error
    GraphQLMutationError    # Mutation failed
    GraphQLQueryError       # Query failed
  ManifestError             # Invalid/missing manifest
  ManifestServiceUnavailableError  # State Manager unreachable
```

## Common Patterns

### Hybrid GPU/CPU Pipeline

```python
from runpod_flash import remote, LiveServerless, CpuInstanceType

cpu_config = LiveServerless(name="preprocessor", instanceIds=[CpuInstanceType.CPU5C_4_8])
gpu_config = LiveServerless(name="inference", gpus=[GpuGroup.AMPERE_80])

@remote(resource_config=cpu_config, dependencies=["pandas"])
async def preprocess(data):
    import pandas as pd
    return pd.DataFrame(data).to_dict('records')

@remote(resource_config=gpu_config, dependencies=["torch"])
async def inference(data):
    import torch
    tensor = torch.tensor(data, device="cuda")
    return {"result": tensor.sum().item()}

async def pipeline(raw_data):
    clean = await preprocess(raw_data)
    return await inference(clean)
```

### Parallel Execution

```python
results = await asyncio.gather(
    process_item(item1),
    process_item(item2),
    process_item(item3),
)
```

### Local Testing

```python
@remote(resource_config=config, local=True)
async def my_function(data):
    return {"status": "ok"}  # Runs locally, skips remote
```

### Cost Optimization

- Use `workersMin=0` to scale from zero
- Use `idleTimeout=600` to reduce churn
- Use smaller GPUs if they fit your model
- Use `Live*` classes for spot pricing in dev
- Pass URLs/paths instead of large data objects

## CLI Commands

### flash init

```bash
flash init [project_name]
```

Creates a project template:

```
project_name/
├── main.py                # FastAPI entry point
├── workers/
│   ├── gpu/__init__.py    # GPU router
│   │   └── endpoint.py    # GPU @remote function
│   └── cpu/__init__.py    # CPU router
│       └── endpoint.py    # CPU @remote function
├── .env                   # API key template
├── .gitignore
├── .flashignore           # Deployment ignore patterns
├── requirements.txt
└── README.md
```

### flash run

```bash
flash run [--auto-provision] [--host HOST] [--port PORT]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--auto-provision` | off | Pre-deploy all endpoints before serving |
| `--host` | `localhost` | Server host (or `FLASH_HOST` env) |
| `--port` | `8888` | Server port (or `FLASH_PORT` env) |

### flash build

```bash
flash build [--exclude PACKAGES] [--keep-build] [--preview]
```

| Option | Description |
|--------|-------------|
| `--exclude pkg1,pkg2` | Skip packages already in base Docker image |
| `--keep-build` | Don't delete `.flash/.build/` after packaging |
| `--preview` | Build then run in local Docker containers |

Build steps: scan `@remote` decorators, group by resource config, create `flash_manifest.json`, install dependencies for Linux x86_64, package into `.flash/artifact.tar.gz`.

**500MB deployment limit** - use `--exclude` for packages in base image:

```bash
flash build --exclude torch,torchvision,torchaudio
```

**`--preview` mode**: Creates Docker containers per resource config, starts mothership on `localhost:8000`, enables end-to-end local testing.

### flash deploy

```bash
flash deploy new <env_name> [--app-name NAME]   # Create environment
flash deploy send <env_name> [--app-name NAME]   # Deploy archive
flash deploy list [--app-name NAME]               # List environments
flash deploy info <env_name> [--app-name NAME]    # Show details
flash deploy delete <env_name> [--app-name NAME]  # Delete (double confirmation)
```

`flash deploy send` requires `flash build` to have been run first.

### flash undeploy

```bash
flash undeploy list          # List all deployed resources
flash undeploy <name>        # Undeploy specific resource
```

### flash env / flash app

```bash
flash env list|create|info|delete <name>   # Environment management
flash app list|get <name>                  # App management
```

## Architecture Overview

### Deployment Architecture

**Mothership Pattern**: Coordinator endpoint + distributed child endpoints.

1. `flash build` scans code, creates manifest + archive
2. `flash deploy send` uploads archive, provisions resources
3. Mothership boots, reconciles desired vs current state
4. Child endpoints query State Manager GraphQL for service discovery (peer-to-peer)
5. Functions route locally or remotely based on manifest

### Cross-Endpoint Routing

Functions on different endpoints can call each other transparently:
1. `ProductionWrapper` intercepts calls
2. `ServiceRegistry` looks up function in manifest
3. Local function? Execute directly
4. Remote function? Serialize args (cloudpickle), POST to remote endpoint

**Serialization**: cloudpickle + base64, max 10MB payload.

## Common Gotchas

1. **External scope in @remote functions** - Most common error. Everything must be inside.
2. **Forgetting `await`** - All remote functions must be awaited.
3. **Undeclared dependencies** - Must be in `dependencies=[]` parameter.
4. **Queue vs LB confusion** - Queue returns `JobOutput`, LB returns dict directly.
5. **Large serialization** - Pass URLs/paths, not large data objects.
6. **Imports at module level** - Import inside `@remote` functions, not at top of file.
7. **LoadBalancer requires method+path** - `@remote(config, method="POST", path="/api/x")`
8. **Bundle too large (>500MB)** - Use `--exclude` for packages in base Docker image.
9. **Endpoints accumulate** - Clean up with `flash undeploy list` / `flash undeploy <name>`.
