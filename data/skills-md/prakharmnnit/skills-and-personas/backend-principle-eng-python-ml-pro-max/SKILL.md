---
name: backend-principle-eng-python-ml-pro-max
description: "Principal backend engineering intelligence for Python AI/ML systems. Actions: plan, design, build, implement, review, fix, optimize, refactor, debug, secure, scale ML services and pipelines. Focus: data quality, reproducibility, reliability, performance, security, observability, model evaluation, MLOps."
---

# Backend Principle Eng Python ML Pro Max

Principal-level guidance for Python AI/ML backends, training pipelines, and inference services. Emphasizes data integrity, reproducibility, and production reliability.

## When to Apply
- Designing or refactoring ML training or inference systems
- Reviewing ML code for data leakage, evaluation quality, and reliability
- Building feature pipelines, batch scoring, or real-time serving
- Incident response for model regressions or data drift

## Priority Model (highest to lowest)

| Priority | Category | Goal | Signals |
| --- | --- | --- | --- |
| 1 | Data Quality & Leakage | Trust the data | Clean splits, lineage, leakage checks |
| 2 | Correctness & Reproducibility | Same inputs, same outputs | Versioned data, pinned deps, deterministic runs |
| 3 | Reliability & Resilience | Stable training and serving | Timeouts, retries, graceful degradation |
| 4 | Model Evaluation & Safety | Real-world performance | Offline + online eval, bias checks |
| 5 | Performance & Cost | Efficient training/inference | GPU utilization, batching, cost budgets |
| 6 | Observability & Monitoring | Fast detection | Drift, latency, error budgets |
| 7 | Security & Privacy | Protect sensitive data | Access controls, data minimization |
| 8 | Operability & MLOps | Sustainable delivery | CI/CD, model registry, rollback |

## Quick Reference (Rules)

### 1. Data Quality & Leakage (CRITICAL)
- `lineage` - Track dataset provenance and transformations
- `leakage` - Strict train/val/test separation with time-based splits when needed
- `features` - Feature definitions are versioned and documented
- `validation` - Schema and distribution checks on every data ingest

### 2. Correctness & Reproducibility (CRITICAL)
- `versioning` - Data, code, and model versions are pinned
- `determinism` - Fixed seeds and deterministic ops where possible
- `config` - Single source of truth for hyperparameters
- `artifact` - Immutable model artifacts and metadata

### 3. Reliability & Resilience (CRITICAL)
- `timeouts` - Explicit timeouts for all external calls
- `retries` - Bounded retries with jitter
- `fallbacks` - Safe fallback models or rules when inference fails
- `idempotency` - Safe retries for batch scoring

### 4. Model Evaluation & Safety (HIGH)
- `offline-eval` - Metrics aligned to product goals
- `online-eval` - Shadow or canary before full rollout
- `bias` - Bias and fairness checks for sensitive domains
- `calibration` - Calibrate probabilities for decision thresholds

### 5. Performance & Cost (HIGH)
- `batching` - Batch inference to improve throughput
- `caching` - Cache features and embeddings when safe
- `profiling` - Profile training and inference hot spots
- `cost-budgets` - Define and enforce cost ceilings

### 6. Observability & Monitoring (HIGH)
- `drift` - Monitor data and concept drift
- `latency` - Track P95/P99 for inference
- `quality` - Monitor model quality against ground truth
- `alerts` - SLO-based alerts with runbooks

### 7. Security & Privacy (HIGH)
- `access` - Least privilege for data and model artifacts
- `pii` - Redact or tokenize sensitive fields
- `secrets` - Use vault/KMS; never in code or logs
- `compliance` - Retention and deletion policies

### 8. Operability & MLOps (MEDIUM)
- `registry` - Model registry with lineage and approvals
- `rollout` - Canary, blue/green, or shadow deployments
- `rollback` - Fast revert on regression
- `ci-cd` - Automated tests for data, training, and serving

## Execution Workflow
1. Define product goals, metrics, and safety constraints
2. Validate data sources and prevent leakage
3. Define features and versioned pipelines
4. Train with reproducible configs and tracked artifacts
5. Evaluate offline, then validate online via shadow or canary
6. Deploy with monitoring for drift, latency, and quality
7. Establish rollback and retraining triggers

## Language-Specific Guidance
See `references/python-ml-core.md` for stack defaults, MLOps patterns, and tooling.
