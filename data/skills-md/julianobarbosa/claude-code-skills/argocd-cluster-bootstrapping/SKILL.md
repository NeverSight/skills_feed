---
name: argocd-cluster-bootstrapping
description: Complete ArgoCD cluster bootstrapping skill for multi-repository GitOps environments. Use when provisioning new Kubernetes clusters, registering clusters with ArgoCD, configuring ApplicationSets, setting up cluster secrets, or troubleshooting cluster connectivity issues.
---

# ArgoCD Cluster Bootstrapping Skill

Complete guide for bootstrapping new Kubernetes clusters into a multi-repository GitOps environment managed by ArgoCD.

## When to Use This Skill

- Provisioning a new AKS/EKS/GKE cluster and integrating it with ArgoCD
- Registering an existing cluster with the ArgoCD hub
- Creating cluster secrets with proper labels for ApplicationSet targeting
- Setting up ArgoCD Projects for new business units
- Configuring multi-source ApplicationSets for new clusters
- Troubleshooting cluster connectivity or sync issues
- Understanding the multi-repository GitOps architecture

## Quick Start

### 1. Pre-Flight Checklist
```bash
# Verify ArgoCD CLI is installed
argocd version --client

# Verify kubectl access to hub cluster
kubectl config use-context aks-cafehyna-default
kubectl get nodes

# Verify access to target cluster
kubectl config use-context <new-cluster-context>
kubectl get nodes
```

### 2. Register Cluster (3 Steps)
```bash
# Step 1: Add cluster to ArgoCD
argocd cluster add <cluster-context> --name <developer-friendly-name>

# Step 2: Create cluster secret with labels (GitOps)
# See templates/cluster-secret.yaml

# Step 3: Create ArgoCD Project (GitOps)
# See templates/argocd-project.yaml
```

### 3. Deploy First Application
```bash
# Sync the master ApplicationSet to pick up new cluster
argocd app sync applicationset-master --resource-filter kind=ApplicationSet
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HUB CLUSTER                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    ArgoCD Server                             │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│   │
│  │  │ApplicationSet│ │  Projects   │ │    Cluster Secrets     ││   │
│  │  │  Controller  │ │  (RBAC)     │ │  (Labels for targeting)││   │
│  │  └─────────────┘ └─────────────┘ └─────────────────────────┘│   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ DEV Cluster │      │ HLG Cluster │      │ PRD Cluster │
│  (Spot OK)  │      │  (Staging)  │      │ (HA Config) │
└─────────────┘      └─────────────┘      └─────────────┘
```

## Repository Structure

```
infra-team/                          # Infrastructure repository
├── applicationset/                  # ApplicationSet definitions
│   ├── kube-addons/                # Add-on ApplicationSets
│   └── applications/               # Business app ApplicationSets
├── argocd-clusters/                # Cluster registration secrets
├── argocd-projects/                # Project definitions (RBAC)
└── applicationset-templates/       # Reusable templates

argo-cd-helm-values/                # Values repository (separate security)
└── kube-addons/
    └── <component>/
        └── <cluster-name>/
            └── values.yaml         # Per-cluster overrides
```

## Key Concepts

### Naming Convention (Critical)
| Context | Developer Name | Azure AKS Name |
|---------|---------------|----------------|
| ArgoCD | `cafehyna-dev` | `aks-cafehyna-dev` |
| Secrets | Uses developer name | - |
| Labels | Uses developer name | - |

### Cluster Labels (Required)
```yaml
labels:
  argocd.argoproj.io/secret-type: cluster
  environment: dev|hlg|prd|hub
  region: brazilsouth|eastus2
  cluster-name: <developer-friendly-name>
  node-type: spot|standard|mixed
  connection-type: internal|external
  tier: platform|application
```

### Environment Characteristics
| Environment | Sync Policy | Replicas | Node Type | Prune |
|-------------|-------------|----------|-----------|-------|
| dev | Automated | 1 | Spot OK | Yes |
| hlg | Manual | 2 | Mixed | Yes |
| prd | Manual | 3 | Standard | No |

## Reference Documentation

- [Complete Workflow](references/workflow.md) - Step-by-step bootstrapping process
- [Templates](references/templates/) - Ready-to-use YAML templates
- [Tools & Commands](references/tools.md) - CLI reference and scripts
- [Best Practices](references/guidance.md) - Security, troubleshooting, patterns
- [Architecture Details](references/architecture.md) - Deep dive into the system

## Common Tasks

### Add New Dev Cluster
```bash
# Use the bootstrap script
./scripts/bootstrap-cluster.sh \
  --name cafehyna-dev-02 \
  --environment dev \
  --region brazilsouth \
  --node-type spot
```

### Troubleshoot Connectivity
```bash
# Check cluster health
argocd cluster get <cluster-name>

# Verify secret labels
kubectl get secret -n argocd -l argocd.argoproj.io/secret-type=cluster

# Test ApplicationSet targeting
argocd appset get <appset-name> --show-params
```

## Safety Rules

1. **Never use `kubectl apply` on managed clusters** - All changes via Git
2. **Always validate before commit** - Run `pre-commit run --all-files`
3. **Test in dev first** - Promote through hlg before prd
4. **Preserve existing labels** - They control ApplicationSet targeting
5. **Use secrets for credentials** - Never hardcode in values files
