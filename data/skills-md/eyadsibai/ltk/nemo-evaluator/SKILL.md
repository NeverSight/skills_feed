---
name: nemo-evaluator
description: Use when evaluating LLMs, running benchmarks like MMLU/HumanEval/GSM8K, setting up evaluation pipelines, or asking about "NeMo Evaluator", "LLM benchmarking", "model evaluation", "MMLU", "HumanEval", "GSM8K", "benchmark harnesses"
version: 1.0.0
---

# NeMo Evaluator SDK - Enterprise LLM Benchmarking

## Quick Start

NeMo Evaluator SDK evaluates LLMs across 100+ benchmarks from 18+ harnesses using containerized, reproducible evaluation with multi-backend execution (local Docker, Slurm HPC, Lepton cloud).

**Installation**:

```bash
pip install nemo-evaluator-launcher
```

**Basic evaluation**:

```bash
export NGC_API_KEY=nvapi-your-key-here

cat > config.yaml << 'EOF'
defaults:
  - execution: local
  - deployment: none
  - _self_

execution:
  output_dir: ./results

target:
  api_endpoint:
    model_id: meta/llama-3.1-8b-instruct
    url: https://integrate.api.nvidia.com/v1/chat/completions
    api_key_name: NGC_API_KEY

evaluation:
  tasks:
    - name: ifeval
EOF

nemo-evaluator-launcher run --config-dir . --config-name config
```

## Common Workflows

### Workflow 1: Standard Model Evaluation

**Checklist**:

```
- [ ] Configure API endpoint (NVIDIA Build or self-hosted)
- [ ] Select benchmarks (MMLU, GSM8K, IFEval, HumanEval)
- [ ] Run evaluation
- [ ] Check results
```

**Step 1: Configure endpoint**

For NVIDIA Build:

```yaml
target:
  api_endpoint:
    model_id: meta/llama-3.1-8b-instruct
    url: https://integrate.api.nvidia.com/v1/chat/completions
    api_key_name: NGC_API_KEY
```

For self-hosted (vLLM, TRT-LLM):

```yaml
target:
  api_endpoint:
    model_id: my-model
    url: http://localhost:8000/v1/chat/completions
    api_key_name: ""
```

**Step 2: Select benchmarks**

```yaml
evaluation:
  tasks:
    - name: ifeval           # Instruction following
    - name: gpqa_diamond     # Graduate-level QA
      env_vars:
        HF_TOKEN: HF_TOKEN
    - name: gsm8k_cot_instruct  # Math reasoning
    - name: humaneval        # Code generation
```

**Step 3: Run and check results**

```bash
nemo-evaluator-launcher run --config-dir . --config-name config
nemo-evaluator-launcher status <invocation_id>
cat results/<invocation_id>/<task>/artifacts/results.yml
```

### Workflow 2: Slurm HPC Evaluation

```yaml
defaults:
  - execution: slurm
  - deployment: vllm
  - _self_

execution:
  hostname: cluster.example.com
  account: my_slurm_account
  partition: gpu
  output_dir: /shared/results
  walltime: "04:00:00"
  nodes: 1
  gpus_per_node: 8

deployment:
  checkpoint_path: /shared/models/llama-3.1-8b
  tensor_parallel_size: 2
  data_parallel_size: 4
```

### Workflow 3: Model Comparison

```bash
# Same config, different models
nemo-evaluator-launcher run --config-dir . --config-name base_eval \
  -o target.api_endpoint.model_id=meta/llama-3.1-8b-instruct

nemo-evaluator-launcher run --config-dir . --config-name base_eval \
  -o target.api_endpoint.model_id=mistralai/mistral-7b-instruct-v0.3

# Export results
nemo-evaluator-launcher export <id> --dest mlflow
nemo-evaluator-launcher export <id> --dest wandb
```

## Supported Harnesses

| Harness | Tasks | Categories |
|---------|-------|------------|
| lm-evaluation-harness | 60+ | MMLU, GSM8K, HellaSwag, ARC |
| simple-evals | 20+ | GPQA, MATH, AIME |
| bigcode-evaluation-harness | 25+ | HumanEval, MBPP, MultiPL-E |
| safety-harness | 3 | Aegis, WildGuard |
| vlmevalkit | 6+ | OCRBench, ChartQA, MMMU |
| bfcl | 6 | Function calling v2/v3 |

## CLI Reference

| Command | Description |
|---------|-------------|
| `run` | Execute evaluation with config |
| `status <id>` | Check job status |
| `ls tasks` | List available benchmarks |
| `ls runs` | List all invocations |
| `export <id>` | Export results (mlflow/wandb/local) |
| `kill <id>` | Terminate running job |

## When to Use vs Alternatives

**Use NeMo Evaluator when:**

- Need 100+ benchmarks from 18+ harnesses
- Running on Slurm HPC clusters
- Requiring reproducible containerized evaluation
- Evaluating against OpenAI-compatible APIs

**Use alternatives instead:**

- **lm-evaluation-harness**: Simpler local evaluation
- **bigcode-evaluation-harness**: Code-only benchmarks
- **HELM**: Broader evaluation (fairness, efficiency)

## Common Issues

**Container pull fails**: Configure NGC credentials

```bash
docker login nvcr.io -u '$oauthtoken' -p $NGC_API_KEY
```

**Task requires env var**: Add to task config

```yaml
tasks:
  - name: gpqa_diamond
    env_vars:
      HF_TOKEN: HF_TOKEN
```

**Increase parallelism**:

```bash
-o +evaluation.nemo_evaluator_config.config.params.parallelism=8
-o +evaluation.nemo_evaluator_config.config.params.limit_samples=100
```

## Requirements

- Python 3.10-3.13
- Docker (for local execution)
- NGC API Key (for NVIDIA Build)
- HF_TOKEN (for some benchmarks)
