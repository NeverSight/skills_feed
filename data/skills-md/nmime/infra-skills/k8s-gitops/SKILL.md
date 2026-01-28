---
name: k8s-gitops
description: ArgoCD GitOps continuous delivery for Kubernetes. Use when installing ArgoCD, configuring ApplicationSets, setting up GitLab CI integration, or managing GitOps repository structure.
---

# K8s GitOps

ArgoCD v3.2.5. (Updated: January 2026). All scripts are **idempotent** - uses `kubectl apply` for convergent state.

## Version Support

| Version | Status |
|---------|--------|
| v3.2.x | Current (latest v3.2.5) |
| v3.1.x | Supported (latest v3.1.11) |
| v2.14.x | Supported until v3.2 release |
| < v2.13 | End of Life |

> ArgoCD releases every 3 months. Only 3 most recent minor versions receive patches.

## Installation

See [references/argocd.md](references/argocd.md) for tier-based installation.

## Reference Files

- [references/argocd.md](references/argocd.md) - ArgoCD installation
- [references/applicationsets.md](references/applicationsets.md) - ApplicationSets
- [references/gitlab-ci.md](references/gitlab-ci.md) - GitLab CI integration
- [references/repo-structure.md](references/repo-structure.md) - Repository structure