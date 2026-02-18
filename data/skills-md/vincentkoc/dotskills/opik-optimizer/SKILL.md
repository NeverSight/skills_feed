---
name: opik-optimizer
description: Optimize LLM prompts, tools, and agents in Opik using standardized optimizer workflows (prompt optimization, tool optimization, and parameter tuning), dataset/metric wiring, and result interpretation.
metadata:
  internal: true
---

# Opik Optimizer

## Purpose

Design, run, and interpret Opik Optimizer workflows for prompts, tools, and model parameters with consistent dataset/metric wiring and reproducible evaluation.

## When to use

Use this skill when a user asks for:

- Choosing and configuring Opik Optimizer algorithms for prompt/agent optimization.
- Writing `ChatPrompt`-based optimization runs and custom metric functions.
- Optimizing with tools (function calling or MCP), selected prompt roles, or prompt segments.
- Tuning LLM call parameters with `optimize_parameter`.
- Comparing optimizer outputs and interpreting `OptimizationResult`.

## Workflow

1. Select optimizer strategy (`MetaPromptOptimizer`, `FewShotBayesianOptimizer`, `HRPO`, etc.) based on the target optimization goal.
2. Build prompt/dataset/metric wiring and validate placeholder-field alignment.
3. Run prompt, tool, or parameter optimization with explicit controls (`n_threads`, `n_samples`, `max_trials`, seed).
4. Inspect `OptimizationResult` and compare score deltas against initial baselines.
5. Summarize recommendations, risks, and next experiments.

## Inputs

- Target optimization objective (prompt/tool/parameter) and success metric.
- Dataset source and expected schema fields.
- Model/provider constraints and runtime limits.
- Optional scope constraints (`optimize_prompts` segments, tool fields, project names).

## Outputs

- Optimizer run configuration and rationale.
- Result interpretation (`score`, `initial_score`, history trends).
- Recommended next changes and follow-up experiment plan.

Use the reference files in this skill for details before implementing code:

- `references/algorithms.md`
- `references/prompt_agent_workflow.md`
- `references/example_patterns.md`

## Opik Optimizer quickstart

1. Install and import:

```bash
pip install opik-optimizer
```

```python
from opik_optimizer import ChatPrompt, MetaPromptOptimizer, HRPO, FewShotBayesianOptimizer
from opik_optimizer import datasets
```

2. Build a prompt and metric:

```python
from opik.evaluation.metrics import LevenshteinRatio

prompt = ChatPrompt(
    system="You are a concise answerer.",
    user="{question}",
)

def metric(dataset_item: dict, output: str) -> float:
    return LevenshteinRatio().score(
        reference=dataset_item["answer"],
        output=output,
    ).value
```

3. Load dataset and run:

```python
dataset = datasets.hotpot(count=30)

result = MetaPromptOptimizer(model="openai/gpt-5-nano").optimize_prompt(
    prompt=prompt,
    dataset=dataset,
    metric=metric,
    n_samples=20,
    max_trials=10,
)
result.display()
```

## Core workflow you should follow

1. Pick optimizer class:
   - Few-shot examples + Bayesian selection: `FewShotBayesianOptimizer`
   - LLM meta-reasoning: `MetaPromptOptimizer`
   - Genetic + MOO / LLM crossover: `EvolutionaryOptimizer`
   - Hierarchical reflective diagnostics: `HierarchicalReflectiveOptimizer` (`HRPO`)
   - Pareto-based genetic strategy: `GepaOptimizer`
   - Parameter tuning only: `ParameterOptimizer`
2. Define a single `ChatPrompt` (or dict of prompts for multi-prompt cases).
3. Provide a dataset from `opik_optimizer.datasets`.
4. Provide metric callable with signature `(dataset_item, llm_output) -> float` (or `ScoreResult`/list of `ScoreResult`).
5. Set optimizer controls (`n_threads`, `n_samples`, `max_trials`, seed, etc.).
6. Run one of:
   - `optimize_prompt(...)` for prompt/system behavior changes.
   - `optimize_parameter(...)` for model-call hyperparameters.
7. Inspect `OptimizationResult` (`score`, `initial_score`, `history`, `optimization_id`, `get_optimized_parameters`).

## Key execution details to enforce

- Prefer explicit `project_name` for Opik tracking if you are using org-level observability.
- Keep placeholders in prompts aligned with dataset fields (for example `{question}`).
- Start with `optimize_prompts="system"` or `"user"` when scope should be constrained.
- Keep `model` names in `MetaPrompt`/`reasoning` calls provider-compatible for your account.
- Validate multimodal input payloads by preserving non-empty content segments only.
- For small datasets, use `n_samples` and `n_samples_strategy` carefully; over-allocation auto-falls back to full set.

## Tooling and segment-based control

- Tools can be optimized with MCP/function schema fields, not only by changing prompt wording.
- For fine-grained text updates, use `optimize_prompts` values and helper functions from `prompt_segments`:
  - `extract_prompt_segments(ChatPrompt)` to inspect stable segment IDs.
  - `apply_segment_updates(ChatPrompt, updates)` for deterministic edits.
- Tool optimization is distinct from prompt optimization.

Runnable examples live upstream in the Opik repo:

- https://github.com/comet-ml/opik/tree/main/sdks/opik_optimizer/src/opik_optimizer

If you need local runnable scripts, vendor the upstream examples into a `scripts/` folder and keep references one level deep.

## Common mistakes to avoid

- Passing empty dataset or mismatched placeholder names.
- Mixing deprecated constructor arg `num_threads` with `n_threads`.
- Assuming tool optimization is the same as agent function-calling optimization.
- Running `ParameterOptimizer.optimize_prompt` (it raises and should not be used).

## Next actions

- For in-depth behavior and per-class parameter tables: `references/algorithms.md`
- For exact `optimize_prompt` signatures, prompts, tool constraints, and result usage: `references/prompt_agent_workflow.md`
- For pattern examples and source-backed workflows: `references/example_patterns.md`
