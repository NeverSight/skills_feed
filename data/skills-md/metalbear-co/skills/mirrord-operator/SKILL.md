---
name: mirrord-operator
description: Help users install and configure the mirrord operator for team environments. Use when users ask about operator setup, Helm installation, licensing, or multi-user mirrord deployments.
metadata:
  author: MetalBear
  version: "1.0"
---

# Mirrord Operator Skill

## Purpose

Help users set up mirrord operator for team/enterprise use:
- **Install** operator via Helm
- **Configure** licensing and settings
- **Manage** multi-user access
- **Troubleshoot** operator issues

## When to Use This Skill

Trigger on questions like:
- "How do I install mirrord operator?"
- "Set up mirrord for my team"
- "Configure mirrord licensing"
- "Operator not working"

## References

Read troubleshooting guidance from this skill's `references/` directory:
- `references/troubleshooting.md` - Common operator issues and solutions

## Prerequisites

Before operator setup, verify:
```bash
# Kubernetes cluster access
kubectl cluster-info

# Helm installed
helm version

# User has cluster-admin or sufficient RBAC
kubectl auth can-i create deployments --namespace mirrord
```

## Installation

### Step 1: Add Helm repository

```bash
helm repo add metalbear https://metalbear-co.github.io/charts
helm repo update
```

### Step 2: Install operator

**Trial/evaluation (no license):**
```bash
helm install mirrord-operator metalbear/mirrord-operator \
  --namespace mirrord --create-namespace
```

**Production (with license):**
```bash
helm install mirrord-operator metalbear/mirrord-operator \
  --namespace mirrord --create-namespace \
  --set license.key=<LICENSE_KEY>
```

### Step 3: Verify installation

```bash
# Check operator pod is running
kubectl get pods -n mirrord

# Check operator logs
kubectl logs -n mirrord -l app=mirrord-operator
```

## Configuration Options

### Common Helm values

```yaml
# values.yaml
license:
  key: "your-license-key"      # or use keyRef for secrets

# Namespaces where mirrord can run
roleNamespaces: []              # empty = all namespaces

operator:
  port: 443                     # can use 3000 or 8443 if 443 is restricted
  resources:
    limits:
      cpu: 200m
      memory: 200Mi             # enough for ~200 concurrent sessions

# Feature flags
sqsSplitting: false             # SQS queue splitting
kafkaSplitting: false           # Kafka queue splitting

# Agent settings
agent:
  tls: false                    # secure agent connections (requires agent 3.97.0+)
```

Install with custom values:
```bash
helm install mirrord-operator metalbear/mirrord-operator \
  --namespace mirrord --create-namespace \
  -f values.yaml
```

## User Configuration

Once operator is installed, users need to enable operator mode in their mirrord config:

```json
{
  "operator": true,
  "target": "pod/my-app"
}
```

Or via CLI:
```bash
mirrord exec --operator --target pod/my-app -- node app.js
```

## Common Issues

| Issue | Solution |
|-------|----------|
| "Operator not found" | Check operator pod is running: `kubectl get pods -n mirrord` |
| "License invalid" | Verify license key, check expiration |
| "Permission denied" | User needs RBAC permissions for mirrord CRDs |
| "Namespace not allowed" | Check namespaceSelector in Helm values |

## RBAC Setup

For multi-user access, create appropriate roles:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: mirrord-user
rules:
- apiGroups: ["mirrord.metalbear.co"]
  resources: ["targets", "sessions"]
  verbs: ["get", "list", "create", "delete"]
```

## Upgrade Operator

```bash
helm repo update
helm upgrade mirrord-operator metalbear/mirrord-operator \
  --namespace mirrord \
  -f values.yaml
```

## Uninstall

```bash
helm uninstall mirrord-operator --namespace mirrord
kubectl delete namespace mirrord
```

## Response Guidelines

1. **Check prerequisites first** — kubectl, helm, cluster access
2. **Ask about licensing** — do they have a license key?
3. **Verify installation** — always check pods are running
4. **Help with RBAC** — multi-user setups need proper permissions

## Learn More

- [Operator Documentation](https://metalbear.com/mirrord/docs/overview/teams/)
- [Helm Chart](https://github.com/metalbear-co/charts/tree/main/mirrord-operator)
- [Licensing](https://metalbear.com/pricing/)
