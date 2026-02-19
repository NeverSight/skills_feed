---
name: kubernetes
description: "Kubernetes operations playbook for deploying services: core objects, probes, resource sizing, safe rollouts, and fast kubectl debugging"
version: 1.0.0
category: universal
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Operate Kubernetes workloads with safe rollouts, health probes, resource sizing, and fast kubectl debugging"
    when_to_use: "When deploying services to Kubernetes, diagnosing cluster/runtime issues, or hardening workloads for production readiness"
    quick_start: "1. Inspect: kubectl get/describe 2. Check events/logs 3. Add probes + requests/limits 4. Roll out safely 5. Validate endpoints"
  token_estimate:
    entry: 150
    full: 9000
context_limit: 900
tags:
  - kubernetes
  - k8s
  - infrastructure
  - deployment
  - operations
  - reliability
requires_tools:
  - kubectl
---

# Kubernetes

## Quick Start (kubectl)

```bash
kubectl describe pod/<pod> -n <ns>
kubectl get events -n <ns> --sort-by=.lastTimestamp | tail -n 30
kubectl logs pod/<pod> -n <ns> --previous --tail=200
```

## Production Minimums

- Health: `readinessProbe` and `startupProbe` for safe rollouts
- Resources: set `requests`/`limits` to prevent noisy-neighbor failures
- Security: run as non-root and grant least privilege

## Load Next (References)

- `references/core-objects.md` — choose the right workload/controller and service type
- `references/rollouts-and-probes.md` — probes, rollouts, graceful shutdown, rollback
- `references/debugging-runbook.md` — common failure modes and a fast triage flow
- `references/security-hardening.md` — pod security, RBAC, network policy, supply chain
