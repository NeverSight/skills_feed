---
name: synth-api
description: Use the Synth AI API end-to-end (SDK + HTTP) for eval + GEPA
---

# Synth API (SDK + HTTP, end-to-end)

This skill explains how to run Synth end-to-end with:
- a **Local API task app** exposed via **Cloudflare tunnel**
- **GEPA prompt optimization**
- **Eval jobs** on held-out seeds

Reference demo: `demos/gepa_banking77/gepa_banking77_prompt_optimization.ipynb`

## Required env

- `SYNTH_API_KEY`: your API key (or mint a demo key if using a demo workflow)
- `SYNTH_BACKEND_URL` (optional): backend base URL, default `https://api.usesynth.ai`

## Auth + API keys

Synth uses two keys:

- `SYNTH_API_KEY` authenticates your SDK/CLI calls to the Synth backend.
- `ENVIRONMENT_API_KEY` authenticates backend-to-task-app requests (sent as `X-API-Key` or `Authorization: Bearer ...`).

### Mint a demo Synth API key (optional)

Demo keys are short‑lived (default 4 hours) and are great for notebooks or quick starts.

```python
import os

from synth_ai.core.utils.env import mint_demo_api_key

SYNTH_API_BASE = os.environ.get("SYNTH_BACKEND_URL", "https://api.usesynth.ai")
SYNTH_API_KEY = os.environ.get("SYNTH_API_KEY") or mint_demo_api_key(SYNTH_API_BASE)
os.environ["SYNTH_API_KEY"] = SYNTH_API_KEY
```

### Mint + upload an Environment API key

Your task app should use the same `ENVIRONMENT_API_KEY` that the backend stores for your org.
The helper below generates a key locally and uploads it to the backend using your `SYNTH_API_KEY`.

```python
import os

from synth_ai.sdk.localapi.auth import mint_environment_api_key, setup_environment_api_key

SYNTH_API_BASE = os.environ.get("SYNTH_BACKEND_URL", "https://api.usesynth.ai")
SYNTH_API_KEY = os.environ["SYNTH_API_KEY"]

ENVIRONMENT_API_KEY = mint_environment_api_key()
os.environ["ENVIRONMENT_API_KEY"] = ENVIRONMENT_API_KEY

setup_environment_api_key(SYNTH_API_BASE, SYNTH_API_KEY, token=ENVIRONMENT_API_KEY)
```

## Core concepts

- **Local API**: Your task app runs locally and exposes `/rollout` + `/task_info`.
- **Tunnel**: Cloudflare Quick Tunnel makes the local app reachable by Synth.
- **GEPA**: Prompt optimizer that mutates prompts to maximize reward.
- **Eval jobs**: Formal evaluation on held‑out seeds after optimization.

## Quick SDK health check

```python
import os
import asyncio

from synth_ai.sdk.jobs import JobsClient


async def main() -> None:
    async with JobsClient(
        base_url=os.environ.get("SYNTH_BACKEND_URL", "https://api.usesynth.ai"),
        api_key=os.environ["SYNTH_API_KEY"],
    ) as client:
        files = await client.files.list(limit=5)
        print(files)


if __name__ == "__main__":
    asyncio.run(main())
```

## 1) Define a Local API task app

Minimum Local API shape:
- `provide_taskset_description()`
- `provide_task_instances(seeds)`
- `rollout(request) -> RolloutResponse`

```python
from synth_ai.sdk.localapi import LocalAPIConfig, create_local_api
from synth_ai.sdk.localapi._impl.contracts import RolloutMetrics, RolloutRequest, RolloutResponse, TaskInfo


def create_banking77_local_api(system_prompt: str):
    async def run_rollout(request: RolloutRequest, fastapi_request) -> RolloutResponse:
        # Use your own task logic here; return a reward in [0, 1].
        reward = 1.0
        return RolloutResponse(
            trace_correlation_id=request.trace_correlation_id,
            reward_info=RolloutMetrics(outcome_reward=reward),
            trace=None,
        )

    def provide_taskset_description():
        return {"splits": ["train", "test"], "sizes": {"train": 1000, "test": 1000}}

    def provide_task_instances(seeds):
        for seed in seeds:
            yield TaskInfo(
                task={"id": "banking77", "name": "Banking77 Intent Classification"},
                dataset={"id": "banking77", "split": "train", "index": seed},
                inference={"tool": "banking77_classify"},
                limits={"max_turns": 1},
                task_metadata={"seed": seed},
            )

    return create_local_api(
        LocalAPIConfig(
            app_id="banking77",
            name="Banking77 Intent Classification",
            description="Classify customer queries into intents.",
            provide_taskset_description=provide_taskset_description,
            provide_task_instances=provide_task_instances,
            rollout=run_rollout,
            cors_origins=["*"],
        )
    )
```

## 2) Expose the Local API with a Cloudflare tunnel

Use the built‑in tunnel helper to auto‑start the server and provision a URL.
The helper spins up your local server, creates a public `trycloudflare.com` URL,
and forwards requests from the public URL to your local port. Keep the process
running while Synth calls your task app.

```python
from synth_ai.core.tunnels import TunnelBackend, TunneledLocalAPI

app = create_banking77_local_api("baseline prompt")
baseline_tunnel = await TunneledLocalAPI.create_for_app(
    app=app,
    local_port=None,  # auto-select
    backend=TunnelBackend.CloudflareQuickTunnel,
    progress=True,
)
LOCAL_API_URL = baseline_tunnel.url
print("Local API URL:", LOCAL_API_URL)
```

## 3) Run GEPA (prompt optimization)

GEPA mutates prompt candidates and evaluates them via rollouts. Use a GEPA config body
or a config file. Example config body:

```python
from synth_ai.sdk.optimization.internal.prompt_learning import PromptLearningJob

config_body = {
    "prompt_learning": {
        "algorithm": "gepa",
        "task_app_url": LOCAL_API_URL,
        "env_name": "banking77",
        "initial_prompt": {
            "messages": [
                {"role": "system", "order": 0, "pattern": "Baseline system prompt"},
                {"role": "user", "order": 1, "pattern": "Customer Query: {query}\n\nAvailable Intents:\n{available_intents}"},
            ],
            "wildcards": {"query": "REQUIRED", "available_intents": "OPTIONAL"},
        },
        "policy": {
            "model": "gpt-4.1-nano",
            "provider": "openai",
            "inference_mode": "synth_hosted",
            "temperature": 0.0,
            "max_completion_tokens": 256,
        },
        "gepa": {
            "env_name": "banking77",
            "evaluation": {
                "seeds": list(range(50)),
                "validation_seeds": list(range(50, 60)),
            },
            "rollout": {"budget": 80, "max_concurrent": 8, "minibatch_size": 8},
            "mutation": {"rate": 0.3},
            "population": {"initial_size": 4, "num_generations": 3, "children_per_generation": 3},
            "archive": {"size": 5, "pareto_set_size": 10},
        },
    },
}

job = PromptLearningJob.from_dict(config_dict=config_body, skip_health_check=True)
job_id = job.submit()
result = job.poll_until_complete(timeout=3600.0, interval=3.0, progress=True)
print(result.status.value)
```

## 4) Run Eval jobs (held‑out seeds)

Eval jobs score a fixed set of held‑out seeds for a final report once optimization
finishes.

```python
from synth_ai.sdk.eval.job import EvalJob, EvalJobConfig

config = EvalJobConfig(
    local_api_url=LOCAL_API_URL,
    backend_url=os.environ.get("SYNTH_BACKEND_URL", "https://api.usesynth.ai"),
    api_key=os.environ["SYNTH_API_KEY"],
    env_name="banking77",
    seeds=list(range(100, 150)),
    policy_config={"model": "gpt-4.1-nano", "provider": "openai"},
    env_config={"split": "test"},
    concurrency=10,
)
job = EvalJob(config)
job.submit()
result = job.poll_until_complete(timeout=600.0, interval=2.0, progress=True)
print(result.status)
```

## 5) Retrieve optimized prompts

```python
from synth_ai.sdk.optimization.internal.learning.prompt_learning_client import PromptLearningClient

client = PromptLearningClient()
prompt_results = await client.get_prompts(job_id)
best_score = prompt_results.best_score
print("Best score:", best_score)
```

## HTTP example (raw)

```python
import os
import requests

base = os.environ.get("SYNTH_BACKEND_URL", "https://api.usesynth.ai")
resp = requests.get(
    f"{base}/api/health",
    headers={"Authorization": f"Bearer {os.environ['SYNTH_API_KEY']}"},
    timeout=30,
)
resp.raise_for_status()
print(resp.json())
```

## Troubleshooting checklist

- **Cloudflare tunnel**: Make sure `TunneledLocalAPI` returns a reachable URL; expect a `trycloudflare.com` URL.
- **Inference URL**: If using hosted inference, your model requests should point to `https://api.usesynth.ai/api/inference/v1`.
- **Auth**: Confirm `SYNTH_API_KEY` is set and valid.
- **Task app shape**: Ensure `/task_info` and `/rollout` return valid `RolloutResponse`.
- **Polling errors**: If a poll fails, re‑query `/api/prompt-learning/online/jobs/{job_id}` to confirm job status.
