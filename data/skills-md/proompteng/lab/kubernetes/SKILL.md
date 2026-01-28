---
name: kubernetes
description: Use for kubectl, CNPG, and kustomize/helm operations in this repo, including rollouts and cluster debugging.
---

# Kubernetes

## Overview

Operate cluster resources with explicit namespaces and GitOps manifests. Use CNPG for Postgres access and Helm v3 for kustomize when required.

## Namespace discipline

Always specify `-n jangar` for the Jangar stack unless a different namespace is required.

## Common operations

```bash
kubectl get pods -n jangar
kubectl logs -n jangar deploy/bumba --tail=200
kubectl rollout status -n jangar deployment/bumba
```

## Exec and port-forward

```bash
kubectl exec -n jangar deploy/bumba -- env | rg TEMPORAL
kubectl -n jangar port-forward svc/open-webui 8080:80
```

## CNPG (Postgres)

```bash
kubectl cnpg psql -n jangar jangar-db -- -c 'select now();'
```

## Helm-enabled kustomize

```bash
mise exec helm@3 -- kustomize build --enable-helm argocd/applications/jangar | kubectl apply -n jangar -f -
```

## Resources

- Reference: `references/kubectl-runbook.md`
- Helper: `scripts/kubectl-ns.sh`
- Triage checklist: `assets/kubectl-triage.md`
