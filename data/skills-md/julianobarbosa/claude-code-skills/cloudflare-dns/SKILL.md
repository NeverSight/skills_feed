---
name: cloudflare-dns
description: Comprehensive guide for managing Cloudflare DNS with Azure integration. Use when configuring Cloudflare as authoritative DNS provider for Azure-hosted applications, managing DNS records via API, setting up API tokens, configuring proxy settings, troubleshooting DNS issues, implementing DNS security best practices, or integrating External-DNS with Cloudflare for Kubernetes workloads.
---

# Cloudflare DNS Skill

Complete Cloudflare DNS operations via REST API with focus on Azure integration.

## Overview

This skill covers Cloudflare DNS management for Azure-hosted workloads, including:

- API token configuration and security
- DNS record management (A, AAAA, CNAME, TXT, MX)
- Proxy settings (orange/gray cloud)
- External-DNS integration for Kubernetes
- Troubleshooting and monitoring

## Authentication

### API Token (Recommended)

Create scoped API tokens instead of using Global API Key:

**Required Permissions:**

| Permission | Access | Purpose |
|------------|--------|---------|
| Zone > Zone | Read | List zones |
| Zone > DNS | Edit | Manage DNS records |

**Create Token:**

1. Cloudflare Dashboard > My Profile > API Tokens
2. Create Token > Custom token
3. Add permissions above
4. Zone Resources: Specific zones only
5. (Optional) IP filtering for extra security

**Environment Setup:**

```bash
# Export for API calls
export CF_API_TOKEN="your-api-token"
export CF_ZONE_ID="your-zone-id"

# Get zone ID
curl -s -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer $CF_API_TOKEN" | jq '.result[] | {name, id}'
```

### Token Verification

```bash
# Verify token is valid
curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer $CF_API_TOKEN"
```

## Quick Reference

### List DNS Records

```bash
# All records
curl -s "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" | jq '.result[] | {name, type, content, proxied}'

# Filter by type
curl -s "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records?type=A" \
  -H "Authorization: Bearer $CF_API_TOKEN" | jq '.result[]'

# Search by name
curl -s "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records?name=app.example.com" \
  -H "Authorization: Bearer $CF_API_TOKEN" | jq '.result[]'
```

### Create DNS Records

```bash
# A Record (proxied)
curl -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "A",
    "name": "app",
    "content": "20.185.100.50",
    "ttl": 1,
    "proxied": true
  }'

# A Record (DNS-only)
curl -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "A",
    "name": "mail",
    "content": "20.185.100.51",
    "ttl": 3600,
    "proxied": false
  }'

# CNAME Record
curl -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "www",
    "content": "app.example.com",
    "ttl": 1,
    "proxied": true
  }'

# TXT Record
curl -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "TXT",
    "name": "_dmarc",
    "content": "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com",
    "ttl": 3600
  }'

# MX Record
curl -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "MX",
    "name": "@",
    "content": "mail.example.com",
    "priority": 10,
    "ttl": 3600
  }'
```

### Update DNS Records

```bash
# Get record ID first
RECORD_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records?name=app.example.com&type=A" \
  -H "Authorization: Bearer $CF_API_TOKEN" | jq -r '.result[0].id')

# Update record
curl -X PUT "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "A",
    "name": "app",
    "content": "20.185.100.60",
    "ttl": 1,
    "proxied": true
  }'

# Patch (partial update)
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"proxied": false}'
```

### Delete DNS Records

```bash
# Get record ID
RECORD_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records?name=old.example.com" \
  -H "Authorization: Bearer $CF_API_TOKEN" | jq -r '.result[0].id')

# Delete
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_API_TOKEN"
```

## Proxy Settings (Orange/Gray Cloud)

### When to Enable Proxy (Orange Cloud)

| Use Case | Proxy | Reason |
|----------|-------|--------|
| Web applications | Yes | CDN, DDoS protection |
| REST APIs | Yes | Performance, security |
| Static websites | Yes | Caching, optimization |
| WebSockets | Yes | Supported with config |

### When to Disable Proxy (Gray Cloud)

| Use Case | Proxy | Reason |
|----------|-------|--------|
| Mail servers (MX) | No | SMTP not supported |
| SSH access | No | Non-HTTP protocol |
| FTP servers | No | Non-HTTP protocol |
| Custom TCP/UDP | No | Only HTTP/HTTPS proxied |
| VPN endpoints | No | Direct connection needed |

### Toggle Proxy via API

```bash
# Enable proxy
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"proxied": true}'

# Disable proxy
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"proxied": false}'
```

## External-DNS Integration

### Kubernetes Secret

```bash
kubectl create namespace external-dns

kubectl create secret generic cloudflare-api-token \
  --namespace external-dns \
  --from-literal=cloudflare_api_token="$CF_API_TOKEN"
```

### Helm Values (kubernetes-sigs/external-dns)

```yaml
fullnameOverride: external-dns

provider:
  name: cloudflare

env:
  - name: CF_API_TOKEN
    valueFrom:
      secretKeyRef:
        name: cloudflare-api-token
        key: cloudflare_api_token

extraArgs:
  cloudflare-proxied: true
  cloudflare-dns-records-per-page: 5000

sources:
  - service
  - ingress

domainFilters:
  - example.com

txtOwnerId: "aks-cluster-name"  # MUST be unique per cluster
txtPrefix: "_externaldns."
policy: upsert-only  # Production: NEVER use sync
interval: "5m"

logLevel: info
logFormat: json

resources:
  requests:
    memory: "64Mi"
    cpu: "25m"
  limits:
    memory: "128Mi"

serviceMonitor:
  enabled: true
  interval: 30s
```

### Ingress Annotations

```yaml
metadata:
  annotations:
    # Hostname for External-DNS
    external-dns.alpha.kubernetes.io/hostname: "app.example.com"

    # Custom TTL
    external-dns.alpha.kubernetes.io/ttl: "300"

    # Override proxy setting
    external-dns.alpha.kubernetes.io/cloudflare-proxied: "true"

    # Multiple hostnames
    external-dns.alpha.kubernetes.io/hostname: "app.example.com,www.example.com"
```

## Zone Management

### List Zones

```bash
curl -s "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer $CF_API_TOKEN" | jq '.result[] | {name, id, status, plan: .plan.name}'
```

### Get Zone Details

```bash
curl -s "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID" \
  -H "Authorization: Bearer $CF_API_TOKEN" | jq '.result'
```

### Zone Settings

```bash
# Get all settings
curl -s "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/settings" \
  -H "Authorization: Bearer $CF_API_TOKEN" | jq '.result[] | {id, value}'

# Get specific setting
curl -s "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/settings/ssl" \
  -H "Authorization: Bearer $CF_API_TOKEN" | jq '.result'

# Update SSL mode
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/settings/ssl" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value": "full"}'
```

## Export/Import DNS Records

### Export (BIND Format)

```bash
curl -s "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/export" \
  -H "Authorization: Bearer $CF_API_TOKEN" > dns-backup-$(date +%Y%m%d).txt
```

### Import (BIND Format)

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records/import" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -F "file=@dns-backup.txt"
```

## Troubleshooting

### DNS Verification

```bash
# Query Cloudflare DNS (1.1.1.1)
dig @1.1.1.1 app.example.com A
dig @1.1.1.1 app.example.com AAAA

# Check if proxied (returns Cloudflare IP)
dig +short app.example.com
# Proxied: 104.x.x.x or 172.64.x.x
# DNS-only: Your actual IP

# Check TXT records (External-DNS ownership)
dig @1.1.1.1 TXT _externaldns.app.example.com

# Full trace
dig +trace app.example.com

# Check nameservers
dig NS example.com +short
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Regenerate API token |
| 403 Forbidden | Insufficient permissions | Add Zone:Read, DNS:Edit |
| 429 Rate Limited | Too many requests | Increase interval, use pagination |
| Record exists | Duplicate | Delete or update existing record |

### External-DNS Logs

```bash
# Watch logs
kubectl logs -n external-dns deployment/external-dns -f

# Check for Cloudflare errors
kubectl logs -n external-dns deployment/external-dns | grep -i cloudflare

# Check sync status
kubectl logs -n external-dns deployment/external-dns | grep -i "All records are already up to date"
```

## Security Best Practices

### API Token Security

1. **Scope tokens** - Use specific zones, not "All zones"
2. **IP filtering** - Restrict to known IPs when possible
3. **Rotate regularly** - Every 90 days for production
4. **Store securely** - Kubernetes Secrets or Azure Key Vault
5. **Audit usage** - Check Cloudflare audit logs

### Token Rotation

```bash
# 1. Create new token in Cloudflare dashboard

# 2. Update Kubernetes secret
kubectl create secret generic cloudflare-api-token \
  --namespace external-dns \
  --from-literal=cloudflare_api_token="NEW_TOKEN" \
  --dry-run=client -o yaml | kubectl apply -f -

# 3. Restart External-DNS
kubectl rollout restart deployment external-dns -n external-dns

# 4. Verify
kubectl logs -n external-dns deployment/external-dns | head -20

# 5. Revoke old token in Cloudflare dashboard
```

## Rate Limits

**Cloudflare API Limits:**

- 1,200 requests per 5 minutes (per account)
- 100 requests per 5 minutes (per zone, for some endpoints)

**Mitigation:**

```yaml
# External-DNS optimizations
extraArgs:
  cloudflare-dns-records-per-page: 5000  # Max pagination
  zone-id-filter: "specific-zone-id"     # Reduce API calls

interval: "10m"  # Less frequent polling
```

## Azure Integration

### cert-manager with Cloudflare DNS-01

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-cloudflare
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-cloudflare-key
    solvers:
      - dns01:
          cloudflare:
            apiTokenSecretRef:
              name: cloudflare-api-token
              key: api-token
        selector:
          dnsZones:
            - example.com
```

### AKS Ingress Configuration

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-cloudflare
    external-dns.alpha.kubernetes.io/cloudflare-proxied: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 80
```

## References

- `references/api-reference.md` - Complete Cloudflare DNS API documentation
- `references/azure-integration.md` - Azure-specific patterns and configurations
- `scripts/cloudflare-dns.sh` - Helper script for common operations
- [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
- [External-DNS Cloudflare Tutorial](https://kubernetes-sigs.github.io/external-dns/latest/tutorials/cloudflare/)
