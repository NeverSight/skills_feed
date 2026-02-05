---
name: sglang
description: |
  SGLang - High-performance serving framework for large language and multimodal models.
  Use when deploying LLMs at scale, building inference servers, working with OpenAI-compatible APIs, optimizing model performance, or integrating structured outputs.
  Keywords: sglang, llm-serving, inference-engine, openai-api, multimodal, batch-inference, structured-outputs, quantization, speculative-decoding, kv-cache, tensor-parallelism, vllm-alternative.
compatibility: Python 3.10+, CUDA 12.x+, NVIDIA GPUs (A100/H100/B300), AMD GPUs (MI300), TPU, Ascend NPU
metadata:
  source: https://docs.sglang.io/
  total_docs: 169
  generated: 2026-02-04
---

# SGLang

> SGLang is a high-performance serving framework designed for low-latency and high-throughput inference of large language and multimodal models across various hardware setups, from single GPUs to large distributed clusters.

## Quick Start

```python
# Launch server (in terminal)
# python3 -m sglang.launch_server --model-path meta-llama/Llama-3.1-8B-Instruct --host 0.0.0.0 --port 30000

# Use with OpenAI client
import openai

client = openai.Client(base_url="http://127.0.0.1:30000/v1", api_key="None")

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    temperature=0,
    max_tokens=64,
)
print(response.choices[0].message.content)
```

```python
# Offline batch inference (no HTTP server)
import sglang as sgl

llm = sgl.Engine(model_path="meta-llama/Llama-3.1-8B-Instruct")

prompts = ["Hello, my name is", "The capital of France is"]
outputs = llm.generate(prompts, {"temperature": 0.8, "top_p": 0.95})

for prompt, output in zip(prompts, outputs):
    print(f"Prompt: {prompt}\nGenerated: {output['text']}\n")
```

## Installation

```bash
# Method 1: pip/uv (recommended)
pip install --upgrade pip
pip install uv
uv pip install "sglang"

# Method 2: Docker
docker run --gpus all \
    --shm-size 32g \
    -p 30000:30000 \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HF_TOKEN=<your-token>" \
    --ipc=host \
    lmsysorg/sglang:latest \
    python3 -m sglang.launch_server --model-path meta-llama/Llama-3.1-8B-Instruct --host 0.0.0.0 --port 30000
```

## Documentation

Full documentation in `docs/`. See `docs/000-index.md` for detailed navigation.

### By Topic

| Topic | Files | Description |
|-------|-------|-------------|
| **Getting Started** | 001-003 | Introduction, installation, basic setup |
| **OpenAI API** | 005-010 | OpenAI-compatible endpoints (completions, embeddings, vision) |
| **Popular Models** | 011-037 | DeepSeek, GPT-OSS, GLM, Llama, Qwen, MiniMax usage guides |
| **Model Support** | 038-061 | Supported architectures, adding new models |
| **Structured Outputs** | 060-063 | JSON schemas, regex, EBNF, reasoning models |
| **Performance Optimization** | 064-082 | Quantization, LoRA, speculative decoding, HiCache, PD disaggregation |
| **Hardware Platforms** | 106-128 | NVIDIA, AMD, Intel, TPU, Ascend NPU guides |
| **Distributed Inference** | 129-137 | Multi-node deployment, Kubernetes, LWS, RBG |
| **Production Operations** | 138-147 | Metrics, monitoring, troubleshooting, environment variables |
| **Frontend Language** | 148-151 | SGLang DSL, choices methods |
| **Developer Guide** | 152-163 | Contribution, benchmarking, testing |

### By Keyword

| Keyword | File |
|---------|------|
| openai-api | 005-basic-usage-openai-api-completions.md |
| chat-completions | 004-basic-usage-send-request.md |
| embeddings | 006-basic-usage-openai-api-embeddings.md |
| vision | 007-basic-usage-openai-api-vision.md |
| offline-engine | 020-basic-usage-offline-engine-api.md |
| batch-inference | 020-basic-usage-offline-engine-api.md |
| structured-outputs | 061-advanced-features-structured-outputs.md |
| json-schema | 061-advanced-features-structured-outputs.md |
| reasoning-models | 060-advanced-features-structured-outputs-for-reasoning-models.md |
| tool-parser | 063-advanced-features-tool-parser.md |
| quantization | 064-advanced-features-quantization.md |
| lora | 066-advanced-features-lora.md |
| speculative-decoding | 067-advanced-features-speculative-decoding.md |
| expert-parallelism | 068-advanced-features-expert-parallelism.md |
| kv-cache | 070-advanced-features-hicache-best-practices.md |
| hicache | 071-advanced-features-hicache-design.md |
| pd-disaggregation | 078-advanced-features-pd-disaggregation.md |
| pipeline-parallelism | 079-advanced-features-pipeline-parallelism.md |
| server-arguments | 091-advanced-features-server-arguments.md |
| hyperparameter-tuning | 088-advanced-features-hyperparameter-tuning.md |
| observability | 089-advanced-features-observability.md |
| deepseek-v3 | 012-basic-usage-deepseek-v3.md |
| deepseek-r1 | 012-basic-usage-deepseek-v3.md |
| llama-4 | 017-basic-usage-llama4.md |
| qwen3 | 023-basic-usage-qwen3.md |
| glm-4 | 014-basic-usage-glm45.md |
| amd-gpu | 106-platforms-amd-gpu.md |
| ascend-npu | 113-platforms-ascend-npu.md |
| tpu | 116-platforms-tpu.md |
| cpu-inference | 114-platforms-cpu-server.md |
| kubernetes | 130-references-multi-node-deployment-deploy-on-k8s.md |
| multi-node | 132-references-multi-node-deployment-multi-node.md |
| prometheus-metrics | 141-references-production-metrics.md |
| request-tracing | 142-references-production-request-trace.md |
| faq | 140-references-faq.md |
| environment-variables | 139-references-environment-variables.md |
| docker | 155-developer-guide-development-guide-using-docker.md |
| benchmarking | 152-developer-guide-bench-serving.md |

### Learning Path

1. **Foundation (001-003)**: Overview, installation
2. **Basic Usage (004-037)**: API fundamentals, model-specific guides
3. **Supported Models (038-059)**: Model architectures, extending support
4. **Advanced Features (060-105)**: Structured outputs, optimization, scaling
5. **Platform Guides (106-128)**: Hardware-specific deployment
6. **Distributed Deployment (129-137)**: Multi-node, Kubernetes
7. **Production (138-151)**: Monitoring, troubleshooting, frontend language
8. **Development (152-169)**: Contributing, benchmarking

## Common Tasks

### Launch a Server
-> `docs/004-basic-usage-send-request.md` (Quick start guide for server + requests)

### Use OpenAI-Compatible API
-> `docs/005-basic-usage-openai-api-completions.md` (Chat/text completions with OpenAI client)

### Batch Inference Without Server
-> `docs/020-basic-usage-offline-engine-api.md` (Offline engine for batch processing)

### Constrain Output with JSON Schema
-> `docs/061-advanced-features-structured-outputs.md` (JSON, regex, EBNF constraints)

### Deploy DeepSeek Models
-> `docs/012-basic-usage-deepseek-v3.md` (DeepSeek V3/V3.1/R1 configuration)

### Enable Quantization
-> `docs/064-advanced-features-quantization.md` (FP8/INT4/AWQ/GPTQ quantization)

### Serve Multiple LoRA Adapters
-> `docs/066-advanced-features-lora.md` (Multi-LoRA batching)

### Use Speculative Decoding
-> `docs/067-advanced-features-speculative-decoding.md` (EAGLE-based acceleration)

### Configure HiCache (KV Caching)
-> `docs/070-advanced-features-hicache-best-practices.md` (Hierarchical caching setup)

### Multi-Node Deployment
-> `docs/132-references-multi-node-deployment-multi-node.md` (Distributed inference)

### Deploy on Kubernetes
-> `docs/130-references-multi-node-deployment-deploy-on-k8s.md` (K8s deployment guide)

### Monitor with Prometheus
-> `docs/141-references-production-metrics.md` (Production metrics setup)

### Troubleshoot Common Issues
-> `docs/140-references-faq.md` (CUDA OOM, common errors)

### Tune Server Performance
-> `docs/088-advanced-features-hyperparameter-tuning.md` (Throughput optimization)

### Deploy on AMD GPUs
-> `docs/106-platforms-amd-gpu.md` (ROCm/MI300 setup)
