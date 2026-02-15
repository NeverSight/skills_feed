---
name: argocd-cli
description: This skill should be used when users need to manage GitOps deployments via ArgoCD CLI. It covers application sync, rollback, status checking, refresh, and deployment history. Integrates with Kargo for progressive delivery. Triggers on requests mentioning ArgoCD, GitOps, application sync, deployment status, or rollback operations.
---

# ArgoCD CLI Skill

This skill enables GitOps deployment management using ArgoCD CLI.

## Environment

### Connection

- **Server**: `192.168.10.117:31006`
- **Web UI**: `http://192.168.10.117:31006`
- **Credentials**: admin / CpfsoneT7ogVKWOh

### Login Command

If token expires, re-authenticate:

```bash
yes | argocd login 192.168.10.117:31006 --username admin --password CpfsoneT7ogVKWOh --insecure
```

### Applications Overview

| Application | Cluster | Namespace | Environment |
|-------------|---------|-----------|-------------|
| `simplex-k1-prod` | AWS EKS | production | 生产环境 |
| `simplex-k2-staging` | AWS EKS | staging | 预发布环境 |
| `simplex-local` | K3s | simplex | 本地开发 |
| `simplex-local-infra` | K3s | common | 本地基础设施 |

## Common Operations

### Application Status

```bash
# List all applications
argocd app list

# Get specific application status
argocd app get argocd/simplex-k1-prod
argocd app get argocd/simplex-k2-staging
argocd app get argocd/simplex-local

# Get application in JSON format
argocd app get argocd/simplex-k1-prod -o json

# Get application in YAML format
argocd app get argocd/simplex-k1-prod -o yaml
```

### Sync Operations

```bash
# Sync application (deploy latest from git)
argocd app sync argocd/simplex-k1-prod

# Sync with prune (remove resources not in git)
argocd app sync argocd/simplex-k1-prod --prune

# Sync specific resources only
argocd app sync argocd/simplex-k1-prod --resource apps:Deployment:simplex-api

# Sync with force (replace resources)
argocd app sync argocd/simplex-k1-prod --force

# Sync and wait for completion
argocd app sync argocd/simplex-k1-prod --timeout 300

# Dry run sync (preview changes)
argocd app sync argocd/simplex-k1-prod --dry-run
```

### Refresh

```bash
# Refresh application (re-read from git)
argocd app get argocd/simplex-k1-prod --refresh

# Hard refresh (clear cache and re-read)
argocd app get argocd/simplex-k1-prod --hard-refresh
```

### Rollback

```bash
# View deployment history
argocd app history argocd/simplex-k1-prod

# Rollback to specific revision
argocd app rollback argocd/simplex-k1-prod <revision-id>

# Example: rollback to revision 5
argocd app rollback argocd/simplex-k1-prod 5
```

### Diff and Comparison

```bash
# Show diff between live and desired state
argocd app diff argocd/simplex-k1-prod

# Show diff with local manifests
argocd app diff argocd/simplex-k1-prod --local /path/to/manifests
```

### Resource Management

```bash
# List application resources
argocd app resources argocd/simplex-k1-prod

# Get logs from application pods
argocd app logs argocd/simplex-k1-prod

# Follow logs
argocd app logs argocd/simplex-k1-prod --follow

# Logs from specific container
argocd app logs argocd/simplex-k1-prod --container simplex-api

# Delete specific resource
argocd app delete-resource argocd/simplex-k1-prod --kind Deployment --resource-name simplex-api
```

### Application Management

```bash
# Create new application
argocd app create <name> \
  --repo ssh://git@192.168.10.117:2222/simplexai/infra/simplex-gitops.git \
  --path kubernetes/overlays/<env> \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace <namespace>

# Delete application
argocd app delete argocd/<app-name>

# Set application parameters
argocd app set argocd/simplex-k1-prod --parameter key=value
```

### Project Management

```bash
# List projects
argocd proj list

# Get project details
argocd proj get simplex

# List project roles
argocd proj role list simplex
```

## Status Interpretation

### Sync Status

| Status | Meaning |
|--------|---------|
| `Synced` | Live state matches desired state in git |
| `OutOfSync` | Live state differs from git |
| `Unknown` | Unable to determine sync status |

### Health Status

| Status | Meaning |
|--------|---------|
| `Healthy` | All resources are healthy |
| `Progressing` | Resources are being updated |
| `Degraded` | One or more resources are unhealthy |
| `Suspended` | Resources are suspended |
| `Missing` | Resources don't exist |
| `Unknown` | Health status unknown |

## Output Formatting

### Status Summary

```
📊 ArgoCD Application Status

┌─────────────────────┬──────────┬───────────┬─────────────────┐
│ Application         │ Sync     │ Health    │ Last Sync       │
├─────────────────────┼──────────┼───────────┼─────────────────┤
│ simplex-k1-prod     │ Synced   │ Healthy   │ 2h ago          │
│ simplex-k2-staging  │ Synced   │ Healthy   │ 1h ago          │
│ simplex-local       │ OutOfSync│ Degraded  │ 30m ago         │
└─────────────────────┴──────────┴───────────┴─────────────────┘
```

## Troubleshooting

### Application Not Syncing

1. Check sync status: `argocd app get argocd/<app>`
2. Check for sync errors in conditions
3. Hard refresh: `argocd app get argocd/<app> --hard-refresh`
4. Check git repository access

### ComparisonError

Usually indicates:
- Git repository access issues
- Invalid manifests in git
- Kustomize/Helm rendering errors

Resolution:
```bash
# Hard refresh to clear cache
argocd app get argocd/<app> --hard-refresh

# Check app details for error message
argocd app get argocd/<app>
```

### Authentication Expired

```bash
# Re-login
yes | argocd login 192.168.10.117:31006 --username admin --password CpfsoneT7ogVKWOh --insecure
```

## Integration with Kargo

ArgoCD applications are managed by Kargo for progressive delivery:

- **Kargo Warehouse** detects new images in ECR
- **Kargo Stages** promote freights through environments
- **ArgoCD** syncs the changes to clusters

Kargo-managed applications have annotation:
```yaml
kargo.akuity.io/authorized-stage: kargo-simplex:prod
```

For progressive delivery operations, use the Kargo CLI skill.
