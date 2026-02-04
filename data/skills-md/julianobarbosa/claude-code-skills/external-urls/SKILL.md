---
name: external-urls
description: Hypera infrastructure URLs and endpoints reference. Use when user asks about URLs, domains, ingress endpoints, cluster API servers, application URLs, Helm repositories, Git repositories, or needs to check connectivity to services. Provides quick lookup of all external URLs across all environments (hub, dev, prd) and clusters (cafehyna, loyalty, painelclientes, sonora).
---

# External URLs Skill

Quick reference for all external URLs and endpoints in Hypera's multi-cluster GitOps infrastructure.

## Quick URL Lookup

### Application URLs by Environment

**Hub (Shared Services)**

| Service | URL | Purpose |
|---------|-----|---------|
| ArgoCD | `https://argocd.cafehyna.com.br` | GitOps UI & API |
| Sentry | `https://sentry-hub.cafehyna.hypera.com.br` | Error tracking |
| SonarQube | `https://sonarqube-hub.cafehyna.com.br` | Code quality |
| phpMyAdmin | `https://dba.cafehyna.com.br` | MySQL admin |
| Adminer | `https://dba2.cafehyna.com.br` | Multi-DB admin |
| Mimir | `https://mimir-hub.cafehyna.com.br` | Metrics storage |

**Development**

| Service | URL | Purpose |
|---------|-----|---------|
| Sentry | `https://sentry.adocyl.com.br` | Error tracking |
| SonarQube | `https://sonarqube.hypera.com.br` | Code quality |
| Grafana OnCall | `https://oncall-dev.cafehyna.com` | On-call management |
| phpMyAdmin | `https://dev-dba.cafehyna.com.br` | MySQL admin |
| RabbitMQ | `https://rabbitmq-painelclientes-dev.cafehyna.com.br` | Message queue |

**Production**

| Service | URL | Purpose |
|---------|-----|---------|
| Sentry | `https://sentry.cafehyna.hypera.com.br` | Error tracking |

## Cluster API Endpoints

All clusters use Azure Private Link (VPN required):

| Cluster | API Server | Region |
|---------|------------|--------|
| cafehyna-hub | `https://aks-cafehyna-default-b2ie56p8.5bbf1042-d320-432c-bd11-cea99f009c29.privatelink.eastus.azmk8s.io:443` | East US |
| cafehyna-dev | `https://aks-cafehyna-dev-hlg-q3oga63c.30041054-9b14-4852-9bd5-114d2fac4590.privatelink.eastus.azmk8s.io:443` | East US |
| cafehyna-prd | `https://aks-cafehyna-prd-hsr83z2k.c7d864af-cbd7-481b-866b-8559e0d1c1ea.privatelink.eastus.azmk8s.io:443` | East US |
| painelclientes-dev | `https://akspainelclientedev-dns-vjs3nd48.hcp.eastus2.azmk8s.io:443` | East US 2 |
| painelclientes-prd | `https://akspainelclientesprd-dns-kezy4skd.hcp.eastus2.azmk8s.io:443` | East US 2 |
| loyalty-dev | `https://loyaltyaks-qas-dns-d330cafe.hcp.eastus.azmk8s.io:443` | East US |

## Repository URLs

### Git Repositories (Azure DevOps)

| Repository | URL |
|------------|-----|
| infra-team | `https://hypera@dev.azure.com/hypera/Cafehyna%20-%20Desenvolvimento%20Web/_git/infra-team` |
| argo-cd-helm-values | `https://hypera@dev.azure.com/hypera/Cafehyna%20-%20Desenvolvimento%20Web/_git/argo-cd-helm-values` |
| kubernetes-configuration | `https://hypera@dev.azure.com/hypera/Cafehyna%20-%20Desenvolvimento%20Web/_git/kubernetes-configuration` |

### Helm Repositories

| Repository | URL | Charts |
|------------|-----|--------|
| ingress-nginx | `https://kubernetes.github.io/ingress-nginx` | ingress-nginx |
| jetstack | `https://charts.jetstack.io` | cert-manager |
| bitnami | `https://charts.bitnami.com/bitnami` | external-dns, phpmyadmin, rabbitmq |
| prometheus-community | `https://prometheus-community.github.io/helm-charts` | kube-prometheus-stack |
| robusta | `https://robusta-charts.storage.googleapis.com` | robusta |
| cetic | `https://cetic.github.io/helm-charts` | adminer |
| defectdojo | `https://raw.githubusercontent.com/DefectDojo/django-DefectDojo/helm-charts` | defectdojo |

## Domain Reference

| Domain | Usage | Environment |
|--------|-------|-------------|
| `*.cafehyna.com.br` | Primary applications | All |
| `*.cafehyna.hypera.com.br` | Hypera-branded services | Hub/Prd |
| `*.adocyl.com.br` | Development services | Dev |
| `*.hypera.com.br` | Corporate services | All |

## Certificate & DNS

- **Certificate Issuer:** Let's Encrypt
- **DNS Provider:** Cloudflare
- **ClusterIssuers:** `letsencrypt-prod`, `letsencrypt-staging`
- **Contact:** `juliano.barbosa@hypera.com.br`

## SMTP Services

| Service | Host | Environment |
|---------|------|-------------|
| Office 365 | `smtp.office365.com` | Hub |
| SendGrid | `smtp.sendgrid.net` | Production |

## Quick Commands

### Check Application URL Health

```bash
# Check ArgoCD
curl -sI https://argocd.cafehyna.com.br | head -1

# Check all hub services
for url in argocd.cafehyna.com.br sentry-hub.cafehyna.hypera.com.br sonarqube-hub.cafehyna.com.br dba.cafehyna.com.br; do
  echo -n "$url: "; curl -sI "https://$url" -o /dev/null -w "%{http_code}\n" --connect-timeout 5 2>/dev/null || echo "FAILED"
done
```

### Check Cluster Connectivity

```bash
# Test cluster API (requires VPN)
curl -sk https://aks-cafehyna-default-b2ie56p8.5bbf1042-d320-432c-bd11-cea99f009c29.privatelink.eastus.azmk8s.io:443/healthz

# Using kubectl
kubectl --kubeconfig ~/.kube/aks-rg-hypera-cafehyna-hub-config cluster-info
```

### Check Helm Repository

```bash
# Add and update
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update ingress-nginx

# Search charts
helm search repo ingress-nginx
```

## Configuration File Locations

URLs are defined in these configuration files:

| Category | Path Pattern |
|----------|--------------|
| Application Ingress | `argo-cd-helm-values/kube-addons/<service>/<cluster>/values.yaml` |
| Cluster Endpoints | `infra-team/argocd-clusters/<cluster>.yaml` |
| Git Repositories | `infra-team/argocd-repos/base/git-repositories/*.yaml` |
| Helm Repositories | `infra-team/argocd-repos/base/helm-repositories/*.yaml` |

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Application URL not reachable | Check ingress-nginx pods, verify DNS in Cloudflare |
| Cluster API timeout | Verify VPN connection, check Azure AKS status |
| Certificate error | Verify cert-manager ClusterIssuer, check Let's Encrypt rate limits |
| DNS not resolving | Check external-dns logs, verify Cloudflare API token |

## Scripts

- `scripts/check-urls.sh` - Health check all application URLs
- `scripts/list-urls.sh` - List URLs by environment or category

## Detailed Reference

For complete URL inventory with source file locations:

- **[references/urls-detail.md](references/urls-detail.md)** - Complete URL reference
- **[docs/external-urls-reference.md](../../../docs/external-urls-reference.md)** - Full documentation
