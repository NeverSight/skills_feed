---
name: kargo-cli
description: This skill should be used when users need to manage progressive delivery via Kargo CLI. It covers freight management, stage promotion, warehouse status, and deployment pipeline operations. Integrates with ArgoCD for GitOps sync. Triggers on requests mentioning Kargo, freight, stage promotion, progressive delivery, or deployment pipelines.
---

# Kargo CLI Skill

This skill enables progressive delivery management using Kargo CLI.

## Environment

### Connection

- **Server**: `http://192.168.10.117:31080`
- **Web UI**: `http://192.168.10.117:31080`
- **Credentials**: admin / admin

### Login Command

If token expires, re-authenticate:

```bash
kargo login http://192.168.10.117:31080 --admin --password admin --insecure-skip-tls-verify
```

### Project Overview

| Project | Description |
|---------|-------------|
| `kargo-simplex` | SimplexAI main deployment pipeline |

### Stages

| Stage | Environment | ArgoCD App | Auto-Promote |
|-------|-------------|------------|--------------|
| `local` | K3s Local | simplex-local | Yes |
| `local2` | K3s Local2 | simplex-local2 | Yes |
| `staging` | AWS EKS Staging | simplex-k2-staging | Yes |
| `prod` | AWS EKS Production | simplex-k1-prod | No (Manual) |

## Core Concepts

### Freight

A **Freight** represents a collection of artifacts (container images, git commits, Helm charts) that can be promoted through stages.

### Stage

A **Stage** represents an environment in the deployment pipeline. Freights are promoted from one stage to another.

### Warehouse

A **Warehouse** monitors artifact sources (ECR, git) for new versions and creates freights automatically.

## Common Operations

### Project Management

```bash
# List all projects
kargo get projects

# Get project details
kargo get project kargo-simplex
```

### Stage Operations

```bash
# List stages in project
kargo get stages -p kargo-simplex

# Get specific stage details
kargo get stage staging -p kargo-simplex

# Get stage in YAML format
kargo get stage staging -p kargo-simplex -o yaml
```

### Freight Management

```bash
# List all freights in project
kargo get freights -p kargo-simplex

# Get freight details
kargo get freight <freight-id> -p kargo-simplex

# List freights verified for a stage
kargo get freights -p kargo-simplex --verified-in staging

# List freights approved for a stage
kargo get freights -p kargo-simplex --approved-for prod
```

### Promotion Operations

```bash
# Promote freight to stage
kargo promote --stage staging -p kargo-simplex --freight <freight-id>

# Promote latest available freight
kargo promote --stage staging -p kargo-simplex

# Promote to production (manual approval required)
kargo promote --stage prod -p kargo-simplex --freight <freight-id>
```

### Warehouse Operations

```bash
# List warehouses
kargo get warehouses -p kargo-simplex

# Get warehouse details
kargo get warehouse <name> -p kargo-simplex

# Refresh warehouse (check for new artifacts)
kargo refresh warehouse <name> -p kargo-simplex
```

### Approval Operations

```bash
# Approve freight for stage
kargo approve --stage prod -p kargo-simplex --freight <freight-id>
```

## Deployment Pipeline Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Warehouse  │────▶│    local    │────▶│   staging   │────▶│    prod     │
│ (ECR Watch) │     │  (Auto)     │     │   (Auto)    │     │  (Manual)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
   New Image         K3s Local           AWS Staging         AWS Prod
   Detected          Deployed            Deployed            Deployed
```

### Typical Workflow

1. **New image pushed to ECR** → Warehouse detects
2. **Freight created** automatically
3. **Local stage** auto-promotes and deploys
4. **Staging stage** auto-promotes after local success
5. **Production stage** requires manual promotion

## Status Interpretation

### Stage Status

| Status | Meaning |
|--------|---------|
| `Healthy` | Stage has current freight and is healthy |
| `Progressing` | Freight is being promoted/verified |
| `Unhealthy` | Promotion failed or ArgoCD sync failed |

### Freight Status

| Field | Meaning |
|-------|---------|
| `verified` | Freight has been tested in a stage |
| `approved` | Freight is approved for promotion to next stage |

## Output Formatting

### Pipeline Status Summary

```
🚀 Kargo Pipeline Status (kargo-simplex)

┌──────────┬─────────────────────────┬───────────┬─────────────────┐
│ Stage    │ Current Freight         │ Health    │ Status          │
├──────────┼─────────────────────────┼───────────┼─────────────────┤
│ local    │ 719578f13844...         │ Healthy   │ Verified        │
│ staging  │ 719578f13844...         │ Healthy   │ Verified        │
│ prod     │ (pending)               │ -         │ Awaiting Promo  │
└──────────┴─────────────────────────┴───────────┴─────────────────┘
```

## Troubleshooting

### Freight Not Created

1. Check warehouse status: `kargo get warehouses -p kargo-simplex`
2. Refresh warehouse: `kargo refresh warehouse <name> -p kargo-simplex`
3. Verify ECR credentials are valid
4. Check warehouse subscriptions match ECR repositories

### Stage Not Promoting

1. Check stage status: `kargo get stage <name> -p kargo-simplex`
2. Check if freight is verified in previous stage
3. Check ArgoCD application sync status
4. For prod: verify freight is approved

### Authentication Expired

```bash
kargo login http://192.168.10.117:31080 --admin --password admin --insecure-skip-tls-verify
```

## Integration with ArgoCD

Kargo updates ArgoCD applications by:

1. Modifying `kustomization.yaml` image tags in git
2. Committing changes to the GitOps repository
3. ArgoCD detects changes and syncs

Key integration points:
- Warehouse watches same ECR as ArgoCD apps
- Stage promotion tasks update git overlays
- ArgoCD apps have `kargo.akuity.io/authorized-stage` annotation

For application sync and status, use the ArgoCD CLI skill.
