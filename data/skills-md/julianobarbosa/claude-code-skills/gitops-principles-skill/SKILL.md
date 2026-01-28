---
name: gitops-principles-skill
description: Comprehensive GitOps methodology and principles skill for cloud-native operations. Use when (1) Designing GitOps architecture for Kubernetes deployments, (2) Implementing declarative infrastructure with Git as single source of truth, (3) Setting up continuous deployment pipelines with ArgoCD/Flux/Kargo, (4) Establishing branching strategies and repository structures, (5) Troubleshooting drift, sync failures, or reconciliation issues, (6) Evaluating GitOps tooling decisions, (7) Teaching or explaining GitOps concepts and best practices, (8) Deploying ArgoCD on Azure Arc-enabled Kubernetes or AKS with workload identity. Covers the 4 pillars of GitOps (OpenGitOps), patterns, anti-patterns, tooling ecosystem, Azure Arc integration, and operational guidance.
---

# GitOps Principles Skill

Complete guide for implementing GitOps methodology in Kubernetes environments - the operational framework where **Git is the single source of truth** for declarative infrastructure and applications.

## What is GitOps?

GitOps is a set of practices that uses Git repositories as the source of truth for defining the desired state of infrastructure and applications. An automated process ensures the production environment matches the state described in the repository.

### The OpenGitOps Definition (CNCF)

GitOps is defined by **four core principles** established by the OpenGitOps project (part of CNCF):

| Principle | Description |
|-----------|-------------|
| **1. Declarative** | The entire system must be described declaratively |
| **2. Versioned and Immutable** | Desired state is stored in a way that enforces immutability, versioning, and retention |
| **3. Pulled Automatically** | Software agents automatically pull desired state from the source |
| **4. Continuously Reconciled** | Agents continuously observe and attempt to apply desired state |

## Core Concepts Quick Reference

### Git as Single Source of Truth

```
┌─────────────────────────────────────────────────────────────────┐
│                        GIT REPOSITORY                           │
│  (Single Source of Truth for Desired State)                    │
├─────────────────────────────────────────────────────────────────┤
│  manifests/                                                     │
│  ├── base/                    # Base configurations             │
│  │   ├── deployment.yaml                                        │
│  │   ├── service.yaml                                           │
│  │   └── kustomization.yaml                                     │
│  └── overlays/                # Environment-specific            │
│      ├── dev/                                                   │
│      ├── staging/                                               │
│      └── production/                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ Pull (not Push)
┌─────────────────────────────────────────────────────────────────┐
│                      GITOPS CONTROLLER                          │
│  (ArgoCD / Flux / Kargo)                                       │
│  - Continuously watches Git repository                          │
│  - Compares desired state vs actual state                       │
│  - Reconciles differences automatically                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ Apply
┌─────────────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER                           │
│  (Actual State / Runtime Environment)                          │
└─────────────────────────────────────────────────────────────────┘
```

### Push vs Pull Model

| Push Model (Traditional CI/CD) | Pull Model (GitOps) |
|--------------------------------|---------------------|
| CI system pushes changes to cluster | Agent pulls changes from Git |
| Requires cluster credentials in CI | Credentials stay within cluster |
| Point-in-time deployment | Continuous reconciliation |
| Drift goes undetected | Drift automatically corrected |
| Manual rollback process | Rollback = `git revert` |

### Key GitOps Benefits

1. **Auditability**: Git history = deployment history
2. **Security**: No external access to cluster required
3. **Reliability**: Automated drift correction
4. **Speed**: Deploy via PR merge
5. **Rollback**: Simple `git revert`
6. **Disaster Recovery**: Redeploy entire cluster from Git

## Repository Strategies

### Monorepo vs Polyrepo

**Monorepo** (Single repository for all environments):

```
gitops-repo/
├── apps/
│   ├── app-a/
│   │   ├── base/
│   │   └── overlays/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── prod/
│   └── app-b/
└── infrastructure/
    ├── monitoring/
    └── networking/
```

**Polyrepo** (Separate repositories):

```
# Repository per concern
app-a-config/          # App A manifests
app-b-config/          # App B manifests
infrastructure/        # Shared infrastructure
cluster-bootstrap/     # Cluster setup
```

### Multi-Repository Pattern (This Project)

Separates **infrastructure** from **values** for security boundaries:

```
infra-team/                    # Base configurations, ApplicationSets
├── applications/              # ArgoCD Application definitions
└── helm-base-values/          # Default Helm values

argo-cd-helm-values/           # Environment-specific overrides
├── dev/                       # Development values
├── stg/                       # Staging values
└── prd/                       # Production values
```

**Benefits**:

- Different access controls per repo
- Separation of concerns
- Environment-specific secrets isolated

## Branching Strategies

### Environment Branches

```
main ────────────────────────────────────► Production
  │
  └──► staging ──────────────────────────► Staging cluster
         │
         └──► develop ───────────────────► Development cluster
```

### Trunk-Based with Overlays (Recommended)

```
main ────────────────────────────────────► All environments
  │
  ├── overlays/dev/       → Dev cluster
  ├── overlays/staging/   → Staging cluster
  └── overlays/prod/      → Prod cluster
```

### Release Branches

```
main
  │
  ├── release/v1.0 ──────► Production (v1.0)
  ├── release/v1.1 ──────► Production (v1.1)
  └── release/v2.0 ──────► Production (v2.0)
```

## Sync Policies and Strategies

### Automated Sync

```yaml
syncPolicy:
  automated:
    prune: true       # Delete resources not in Git
    selfHeal: true    # Revert manual changes
```

### Manual Sync (Production Recommended)

```yaml
syncPolicy:
  automated: null     # Require explicit sync
```

### Sync Options

| Option | Use Case |
|--------|----------|
| `CreateNamespace=true` | Auto-create missing namespaces |
| `PruneLast=true` | Delete after successful sync |
| `ServerSideApply=true` | Handle large CRDs |
| `ApplyOutOfSyncOnly=true` | Performance optimization |
| `Replace=true` | Force resource replacement |

## Declarative Configuration Patterns

### Kustomize Pattern

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml

# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
patchesStrategicMerge:
  - replica-patch.yaml
images:
  - name: myapp
    newTag: v1.2.3
```

### Helm Pattern

```yaml
# Application pointing to Helm chart
spec:
  source:
    repoURL: https://charts.example.com
    chart: my-app
    targetRevision: 1.2.3
    helm:
      releaseName: my-app
      valueFiles:
        - values.yaml
        - values-prod.yaml
```

### Multi-Source Pattern

```yaml
spec:
  sources:
    - repoURL: https://charts.bitnami.com/bitnami
      chart: nginx
      targetRevision: 15.0.0
      helm:
        valueFiles:
          - $values/nginx/values-prod.yaml
    - repoURL: https://github.com/org/values.git
      targetRevision: main
      ref: values
```

## Progressive Delivery Integration

GitOps enables progressive delivery patterns:

### Blue-Green Deployments

```yaml
# Two applications, traffic shift via Ingress/Service
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-blue
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-green
```

### Canary with Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: {duration: 5m}
        - setWeight: 50
        - pause: {duration: 10m}
```

### Environment Promotion (Kargo)

```
Warehouse → Dev Stage → Staging Stage → Production Stage
    │           │              │               │
    └── Freight promotion through environments ───┘
```

## Cloud Provider Integration

### Azure Arc-enabled Kubernetes & AKS

Azure provides a managed ArgoCD experience through the **Microsoft.ArgoCD** cluster extension:

```bash
# Simple installation (single node)
az k8s-extension create \
  --resource-group <rg> --cluster-name <cluster> \
  --cluster-type managedClusters \
  --name argocd \
  --extension-type Microsoft.ArgoCD \
  --release-train preview \
  --config deployWithHighAvailability=false

# Production with workload identity (recommended)
# Use Bicep template - see references/azure-arc-integration.md
```

**Key Benefits:**

| Feature | Description |
|---------|-------------|
| Managed Installation | Azure handles deployment and upgrades |
| Workload Identity | Azure AD authentication without secrets |
| Multi-Cluster | Consistent GitOps across hybrid environments |
| Azure Integration | Native ACR, Key Vault, Azure AD support |

**Prerequisites:**

- Azure Arc-connected cluster OR MSI-based AKS cluster
- `Microsoft.KubernetesConfiguration` provider registered
- `k8s-extension` CLI extension installed

See `references/azure-arc-integration.md` for complete setup guide.

---

## Security Considerations

### Secrets Management

**Never store secrets in Git!** Use:

| Approach | Tool |
|----------|------|
| External Secrets | External Secrets Operator |
| Sealed Secrets | Bitnami Sealed Secrets |
| SOPS | Mozilla SOPS encryption |
| Vault | HashiCorp Vault + CSI |
| Cloud KMS | AWS/Azure/GCP Key Management |

### RBAC Best Practices

```yaml
# Limit ArgoCD to specific namespaces
apiVersion: argoproj.io/v1alpha1
kind: AppProject
spec:
  destinations:
    - namespace: 'team-a-*'
      server: https://kubernetes.default.svc
  sourceRepos:
    - 'https://github.com/org/team-a-*'
```

### Network Policies

- GitOps controller should be only component with Git access
- Restrict egress from application namespaces
- Use network policies to isolate environments

## Observability and Debugging

### Health Status Interpretation

| Status | Meaning | Action |
|--------|---------|--------|
| Healthy | All resources running | None |
| Progressing | Deployment in progress | Wait |
| Degraded | Health check failed | Investigate |
| Suspended | Manually paused | Resume when ready |
| Missing | Resource not found | Check manifests |

### Common Issues Checklist

1. **Sync Failed**: Check YAML syntax, RBAC permissions
2. **OutOfSync**: Compare diff, check ignoreDifferences
3. **Degraded**: Check Pod logs, resource limits
4. **Missing**: Verify namespace, check pruning settings

### Drift Detection

```bash
# Check application diff
argocd app diff myapp

# Force refresh from Git
argocd app get myapp --refresh
```

## Quick Decision Guide

### When to Use GitOps

- Kubernetes-native workloads
- Multiple environments (dev/staging/prod)
- Need audit trail for deployments
- Team collaboration on infrastructure
- Disaster recovery requirements

### When GitOps May Not Fit

- Rapidly changing development environments
- Legacy systems without declarative configs
- Real-time configuration changes required
- Single developer, single environment

## References

For detailed information, see:

- `references/core-principles.md` - Deep dive into the 4 pillars
- `references/patterns-and-practices.md` - Branching and repo patterns
- `references/tooling-ecosystem.md` - ArgoCD vs Flux vs Kargo
- `references/anti-patterns.md` - Common mistakes to avoid
- `references/troubleshooting.md` - Debugging guide
- `references/azure-arc-integration.md` - Azure Arc & AKS GitOps setup

## Templates

Ready-to-use templates in `templates/`:

- `application.yaml` - ArgoCD Application example
- `applicationset.yaml` - Multi-cluster deployment
- `kustomization.yaml` - Kustomize overlay structure

## Scripts

Utility scripts in `scripts/`:

- `gitops-health-check.sh` - Validate GitOps setup

## External Resources

- [OpenGitOps Principles](https://opengitops.dev/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Flux Documentation](https://fluxcd.io/docs/)
- [Kargo Documentation](https://docs.kargo.io/)
- [GitOps Working Group](https://github.com/gitops-working-group/gitops-working-group)
- [Azure Arc GitOps with ArgoCD](https://learn.microsoft.com/en-us/azure/azure-arc/kubernetes/tutorial-use-gitops-argocd)
- [Azure Arc-enabled Kubernetes](https://learn.microsoft.com/en-us/azure/azure-arc/kubernetes/)
