---
name: external-dns
description: Comprehensive guide for configuring, troubleshooting, and implementing External-DNS across Azure DNS, AWS Route53, Cloudflare, and Google Cloud DNS. Use when implementing automatic DNS management in Kubernetes, configuring provider-specific authentication (managed identities, IRSA, API tokens), troubleshooting DNS synchronization issues, setting up secure production-grade external-dns deployments, optimizing performance, avoiding rate limits, or implementing GitOps patterns with ArgoCD.
---

# External-DNS Skill

Complete External-DNS operations for automatic DNS management in Kubernetes clusters.

## Overview

External-DNS synchronizes exposed Kubernetes Services and Ingresses with DNS providers, eliminating manual DNS record management. This skill covers configuration, best practices, and troubleshooting across multiple DNS providers with emphasis on Azure and Cloudflare.

## Provider Quick Reference

| Provider | Auth Method | Status | Reference |
|----------|-------------|--------|-----------|
| **Azure DNS** | Workload Identity (recommended) or Service Principal | Stable | `references/azure-dns.md` |
| **Cloudflare** | API Token | Beta | `references/cloudflare.md` |
| **AWS Route53** | IRSA (recommended) or Access Keys | Stable | Below |
| **Google Cloud DNS** | Workload Identity | Stable | Below |

## Essential Helm Values Structure

```yaml
# kubernetes-sigs/external-dns chart (v1.18.0+)
fullnameOverride: external-dns

provider:
  name: <provider>  # azure, cloudflare, aws, google

# Sources to watch
sources:
  - service
  - ingress

# Domain restrictions
domainFilters:
  - example.com

# Policy: sync (creates/updates/deletes) or upsert-only (creates/updates only)
policy: upsert-only  # Recommended for production

# Sync interval
interval: "5m"

# TXT record ownership (MUST be unique per cluster)
txtOwnerId: "aks-cluster-name"
txtPrefix: "_externaldns."

# Logging
logLevel: info  # debug, info, warning, error
logFormat: json

# Resources
resources:
  requests:
    memory: "64Mi"
    cpu: "25m"
  limits:
    memory: "128Mi"
    # cpu: REMOVED per best practice (no CPU limits)

# Security context
securityContext:
  runAsNonRoot: true
  runAsUser: 65534
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]

# Prometheus metrics
serviceMonitor:
  enabled: true
  interval: 30s
```

## Azure DNS Configuration

### Workload Identity (Recommended)

```yaml
provider:
  name: azure

serviceAccount:
  labels:
    azure.workload.identity/use: "true"
  annotations:
    azure.workload.identity/client-id: "<MANAGED_IDENTITY_CLIENT_ID>"

podLabels:
  azure.workload.identity/use: "true"

env:
  - name: AZURE_TENANT_ID
    value: "<TENANT_ID>"
  - name: AZURE_SUBSCRIPTION_ID
    value: "<SUBSCRIPTION_ID>"
  - name: AZURE_RESOURCE_GROUP
    value: "<DNS_ZONE_RESOURCE_GROUP>"

domainFilters:
  - example.com

txtOwnerId: "aks-cluster-name"
policy: upsert-only
interval: "5m"
```

### Required Azure RBAC Permissions

```bash
# Assign DNS Zone Contributor role to the managed identity
az role assignment create \
  --role "DNS Zone Contributor" \
  --assignee "<MANAGED_IDENTITY_OBJECT_ID>" \
  --scope "/subscriptions/<SUB_ID>/resourceGroups/<RG>/providers/Microsoft.Network/dnszones/<ZONE>"

# For Private DNS Zones
az role assignment create \
  --role "Private DNS Zone Contributor" \
  --assignee "<MANAGED_IDENTITY_OBJECT_ID>" \
  --scope "/subscriptions/<SUB_ID>/resourceGroups/<RG>/providers/Microsoft.Network/privateDnsZones/<ZONE>"
```

### Service Principal Alternative

```yaml
provider:
  name: azure

env:
  - name: AZURE_TENANT_ID
    value: "<TENANT_ID>"
  - name: AZURE_SUBSCRIPTION_ID
    value: "<SUBSCRIPTION_ID>"
  - name: AZURE_RESOURCE_GROUP
    value: "<DNS_ZONE_RESOURCE_GROUP>"
  - name: AZURE_CLIENT_ID
    valueFrom:
      secretKeyRef:
        name: azure-credentials
        key: client-id
  - name: AZURE_CLIENT_SECRET
    valueFrom:
      secretKeyRef:
        name: azure-credentials
        key: client-secret
```

## Cloudflare Configuration

```yaml
provider:
  name: cloudflare

env:
  - name: CF_API_TOKEN
    valueFrom:
      secretKeyRef:
        name: cloudflare-api-token
        key: cloudflare_api_token

extraArgs:
  cloudflare-proxied: true  # Enable CDN/DDoS protection
  cloudflare-dns-records-per-page: 5000  # Optimize API calls

domainFilters:
  - example.com

txtOwnerId: "aks-cluster-name"
policy: upsert-only
```

### Cloudflare API Token Permissions

- **Zone:Read** - List zones
- **DNS:Edit** - Create/update/delete DNS records
- **Zone Resources**: All zones or specific zones

## AWS Route53 Configuration (IRSA)

```yaml
provider:
  name: aws

env:
  - name: AWS_DEFAULT_REGION
    value: "us-east-1"

serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: "arn:aws:iam::<ACCOUNT_ID>:role/external-dns"

extraArgs:
  aws-zone-type: public  # or private
  aws-batch-change-size: 4000

domainFilters:
  - example.com

txtOwnerId: "eks-cluster-name"
```

### Required AWS IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["route53:ChangeResourceRecordSets"],
      "Resource": ["arn:aws:route53:::hostedzone/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["route53:ListHostedZones", "route53:ListResourceRecordSets"],
      "Resource": ["*"]
    }
  ]
}
```

## Google Cloud DNS Configuration

```yaml
provider:
  name: google

env:
  - name: GOOGLE_PROJECT
    value: "<GCP_PROJECT_ID>"

serviceAccount:
  annotations:
    iam.gke.io/gcp-service-account: "external-dns@<PROJECT_ID>.iam.gserviceaccount.com"

domainFilters:
  - example.com

txtOwnerId: "gke-cluster-name"
```

## Kubernetes Resource Annotations

### Basic Usage

```yaml
# On Service or Ingress
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostname: "app.example.com"
    external-dns.alpha.kubernetes.io/ttl: "300"
```

### Multiple Hostnames

```yaml
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostname: "app1.example.com,app2.example.com"
```

### Provider-Specific Annotations

```yaml
# Cloudflare - disable proxy for specific record
external-dns.alpha.kubernetes.io/cloudflare-proxied: "false"

# AWS Route53 - create ALIAS record
external-dns.alpha.kubernetes.io/alias: "true"

# Custom TTL
external-dns.alpha.kubernetes.io/ttl: "60"
```

## Environment-Specific Best Practices

### Development

```yaml
policy: sync  # Auto-delete orphaned records
interval: "1m"  # Fast sync for rapid iteration
logLevel: info
resources:
  requests:
    memory: "50Mi"
    cpu: "10m"
  limits:
    memory: "50Mi"
```

### Production

```yaml
policy: upsert-only  # NEVER auto-delete
interval: "10m"  # Conservative to reduce API load
logLevel: error  # Minimal logging

# High Availability
replicaCount: 2

affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: app.kubernetes.io/name
              operator: In
              values: [external-dns]
        topologyKey: kubernetes.io/hostname

podDisruptionBudget:
  enabled: true
  minAvailable: 1

priorityClassName: high-priority
```

## Common Commands

```bash
# Check external-dns pods
kubectl get pods -n external-dns

# View logs
kubectl logs -n external-dns deployment/external-dns --tail=100 -f

# Check configuration
kubectl get deployment external-dns -n external-dns -o yaml | grep -A20 args

# Verify DNS records (Cloudflare)
dig @1.1.1.1 app.example.com

# Verify DNS records (Azure)
az network dns record-set list -g <RESOURCE_GROUP> -z example.com -o table

# Check TXT ownership records
dig TXT _externaldns.app.example.com

# Force restart
kubectl rollout restart deployment external-dns -n external-dns

# Dry-run mode (add to extraArgs)
extraArgs:
  dry-run: true
```

## Key Metrics

```promql
# Total endpoints managed
external_dns_registry_endpoints_total

# Sync errors
external_dns_controller_sync_errors_total

# Last sync timestamp
external_dns_controller_last_sync_timestamp_seconds

# DNS records by type
external_dns_registry_a_records
external_dns_registry_aaaa_records
external_dns_registry_cname_records
```

## ArgoCD ApplicationSet Pattern

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: external-dns
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - cluster: dev
            branch: main
          - cluster: prd
            branch: main
  template:
    metadata:
      name: 'external-dns-{{cluster}}'
    spec:
      project: infrastructure
      sources:
        - chart: external-dns
          repoURL: https://kubernetes-sigs.github.io/external-dns/
          targetRevision: "1.18.0"
          helm:
            releaseName: external-dns
            valueFiles:
              - $values/argo-cd-helm-values/kube-addons/external-dns/{{cluster}}/values.yaml
        - repoURL: https://your-repo.git
          targetRevision: "{{branch}}"
          ref: values
      destination:
        server: '{{url}}'
        namespace: external-dns
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

## Security Checklist

- [ ] Use Workload Identity/IRSA instead of static credentials
- [ ] Grant least privilege permissions to DNS zones
- [ ] Set `runAsNonRoot: true` and `readOnlyRootFilesystem: true`
- [ ] Use unique `txtOwnerId` per cluster
- [ ] Restrict `domainFilters` to necessary domains
- [ ] Store API tokens in Kubernetes Secrets
- [ ] Enable Pod Security Standards (restricted)
- [ ] Use `policy: upsert-only` in production

## References

- `references/azure-dns.md` - Complete Azure DNS configuration guide
- `references/cloudflare.md` - Complete Cloudflare configuration guide
- `references/troubleshooting.md` - Common issues and solutions
- Official docs: <https://kubernetes-sigs.github.io/external-dns/>
- Helm chart: <https://artifacthub.io/packages/helm/external-dns/external-dns>
