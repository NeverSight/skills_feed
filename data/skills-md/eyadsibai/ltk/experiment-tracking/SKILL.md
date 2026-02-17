---
name: experiment-tracking
description: Use when "experiment tracking", "MLflow", "Weights & Biases", "wandb", "model registry", "hyperparameter logging", "ML experiments", "training metrics"
version: 1.0.0
---

# Experiment Tracking

Track ML experiments, metrics, and models.

## Comparison

| Platform | Best For | Self-hosted | Visualization |
|----------|----------|-------------|---------------|
| **MLflow** | Open-source, model registry | Yes | Basic |
| **W&B** | Collaboration, sweeps | Limited | Excellent |
| **Neptune** | Team collaboration | No | Good |
| **ClearML** | Full MLOps | Yes | Good |

---

## MLflow

Open-source platform from Databricks.

**Core components:**

- **Tracking**: Log parameters, metrics, artifacts
- **Projects**: Reproducible runs (MLproject file)
- **Models**: Package and deploy models
- **Registry**: Model versioning and staging

**Strengths**: Self-hosted, open-source, model registry, framework integrations
**Limitations**: Basic visualization, less collaborative features

**Key concept**: Autologging for major frameworks - automatic metric capture with one line.

---

## Weights & Biases (W&B)

Cloud-first experiment tracking with excellent visualization.

**Core features:**

- **Experiment tracking**: Metrics, hyperparameters, system stats
- **Sweeps**: Hyperparameter search (grid, random, Bayesian)
- **Artifacts**: Dataset and model versioning
- **Reports**: Shareable documentation

**Strengths**: Beautiful visualizations, team collaboration, hyperparameter sweeps
**Limitations**: Cloud-dependent, limited self-hosting

**Key concept**: `wandb.init()` + `wandb.log()` - simple API, powerful features.

---

## What to Track

| Category | Examples |
|----------|----------|
| **Hyperparameters** | Learning rate, batch size, architecture |
| **Metrics** | Loss, accuracy, F1, per-epoch values |
| **Artifacts** | Model checkpoints, configs, datasets |
| **System** | GPU usage, memory, runtime |
| **Code** | Git commit, diff, requirements |

---

## Model Registry Concepts

| Stage | Purpose |
|-------|---------|
| **None** | Just logged, not registered |
| **Staging** | Testing, validation |
| **Production** | Serving live traffic |
| **Archived** | Deprecated, kept for reference |

---

## Decision Guide

| Scenario | Recommendation |
|----------|----------------|
| Self-hosted requirement | MLflow |
| Team collaboration | W&B |
| Model registry focus | MLflow |
| Hyperparameter sweeps | W&B |
| Beautiful dashboards | W&B |
| Full MLOps pipeline | MLflow + deployment tools |

## Resources

- MLflow: <https://mlflow.org/docs/latest/>
- W&B: <https://docs.wandb.ai/>
