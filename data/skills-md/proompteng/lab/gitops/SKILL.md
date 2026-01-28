---
name: gitops
description: "GitOps workflows for this repo: edit Argo CD/Kubernetes/infra manifests in version control, validate changes, and rely on Argo CD to sync. Use when tasks touch argocd/, kubernetes/, tofu/, ansible/, or deployment/runbook changes, or when asked to roll out services via GitOps."
---

# GitOps

## Overview

Use GitOps-first changes for infra and deployment workflows, then validate locally and let Argo CD reconcile. Only apply directly to the cluster when explicitly instructed or in an emergency.

## Workflow

1) **Locate the source of truth**
   - Argo CD apps and overlays: `argocd/`
   - Kubernetes manifests: `kubernetes/`
   - IaC: `tofu/`, `ansible/`
   - Service-specific instructions: nearest `README.md`

2) **Edit manifests in Git**
   - Prefer updating Argo CD apps/overlays instead of raw kubectl applies.
   - Keep environment-specific changes in overlays.

3) **Validate locally**
   - Argo lint: `scripts/argo-lint.sh`
   - Kubeconform: `scripts/kubeconform.sh argocd`
   - Terraform/tofu: `bun run tf:plan` (apply only when asked)
   - Ansible: `bun run ansible`

4) **Rollout discipline**
  - Note rollout/impact for changes in `argocd/`, `kubernetes/`, `tofu/`, `ansible/`.
  - For Helm charts with kustomize, use: `mise exec helm@3 -- kustomize build --enable-helm <path>`.

5) **Cluster access (exception-only)**
  - Use direct `kubectl apply` only when explicitly asked or in emergencies.
  - Always set namespace: `kubectl ... -n <ns>`.

6) **Deploy completion guardrail**
   - Only call a deploy "completed" after the Argo CD application is synced and healthy.

## Pointers

- Use `references/gitops-checklist.md` for quick commands and repo-specific notes.
