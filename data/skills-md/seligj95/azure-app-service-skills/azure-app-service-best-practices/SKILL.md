---
name: azure-app-service-best-practices
description: Best practices for Azure App Service web app development, configuration, and operations. Use when reviewing/optimizing App Service configs, implementing security patterns (Managed Identity, Key Vault), optimizing performance (cold starts, scaling), setting up production deployments (slots, CI/CD, health checks), cost optimization, or troubleshooting. Triggers on "best practices", "recommendations", "patterns", "how should I configure".
---

## When to Apply

Reference these guidelines when:

- Deploying new App Service web apps to production
- Reviewing existing configurations for optimization
- Setting up CI/CD pipelines and deployment strategies
- Implementing security and authentication
- Troubleshooting performance issues
- Planning cost optimization
- Migrating to App Service from other platforms

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Security | CRITICAL | `security-` |
| 2 | Reliability | CRITICAL | `reliability-` |
| 3 | Performance | HIGH | `perf-` |
| 4 | Deployment | HIGH | `deploy-` |
| 5 | Configuration | MEDIUM | `config-` |
| 6 | Cost Optimization | MEDIUM | `cost-` |
| 7 | Monitoring | MEDIUM | `monitor-` |

## Quick Reference

### 1. Security (CRITICAL)

| Rule | Description |
|------|-------------|
| `security-managed-identity` | Use Managed Identity instead of credentials in app settings |
| `security-https-only` | Enforce HTTPS-only connections |
| `security-keyvault-refs` | Store secrets in Key Vault with app setting references |
| `security-min-tls` | Require TLS 1.2 minimum |
| `security-disable-ftp` | Disable FTP/FTPS deployments |
| `security-auth-provider` | Use built-in authentication (Easy Auth) when applicable |
| `security-vnet-integration` | Use VNet integration for backend service access |
| `security-private-endpoints` | Use private endpoints for sensitive workloads |

### 2. Reliability (CRITICAL)

| Rule | Description |
|------|-------------|
| `reliability-always-on` | Enable Always On (Basic+ tier) to prevent cold starts |
| `reliability-health-check` | Configure health check endpoint for load balancer probing |
| `reliability-deployment-slots` | Use staging slots for zero-downtime deployments |
| `reliability-auto-heal` | Enable auto-heal rules for automatic recovery |
| `reliability-zone-redundancy` | Enable zone redundancy for production (Premium v3, Premium v4, Isolated v2) |
| `reliability-backup` | Configure automated backups for stateful apps |
| `reliability-multi-region` | Use Traffic Manager or Front Door for multi-region HA |

### 3. Performance (HIGH)

| Rule | Description |
|------|-------------|
| `perf-right-size-sku` | Choose appropriate SKU for workload (don't over/under provision) |
| `perf-linux-plans` | Prefer Linux plans for better performance and lower cost |
| `perf-local-cache` | Enable local cache for read-heavy file access |
| `perf-http2` | Enable HTTP/2 for multiplexed connections |
| `perf-arr-affinity` | Disable ARR affinity for stateless apps |
| `perf-connection-pooling` | Use connection pooling for database connections |
| `perf-async-patterns` | Use async patterns to maximize throughput |
| `perf-cdn-static` | Use CDN for static content delivery |

### 4. Deployment (HIGH)

| Rule | Description |
|------|-------------|
| `deploy-slots-swap` | Deploy to staging slot, then swap to production |
| `deploy-ci-cd` | Use GitHub Actions or Azure Pipelines for automated deployments |
| `deploy-run-from-package` | Use Run From Package for faster, atomic deployments |
| `deploy-warm-up` | Configure slot warm-up rules before swap |
| `deploy-rollback-plan` | Maintain ability to swap back for quick rollbacks |
| `deploy-slot-settings` | Mark slot-specific settings (connection strings, feature flags) |

### 5. Configuration (MEDIUM)

| Rule | Description |
|------|-------------|
| `config-startup-command` | Set explicit startup command for Linux apps |
| `config-64bit` | Use 64-bit platform for memory-intensive workloads |
| `config-timezone` | Set WEBSITE_TIME_ZONE for scheduled tasks |
| `config-env-separation` | Use slot settings to separate dev/staging/prod configs |
| `config-cors` | Configure CORS explicitly (avoid wildcard in production) |
| `config-websockets` | Enable WebSockets only if needed |

### 6. Cost Optimization (MEDIUM)

| Rule | Description |
|------|-------------|
| `cost-reserved-instances` | Use reserved instances for predictable workloads (1-3 year) |
| `cost-dev-test-pricing` | Use Dev/Test pricing for non-production |
| `cost-right-tier` | Start with lower SKU, scale up based on metrics |
| `cost-shared-plan` | Share App Service plans across low-traffic apps |
| `cost-auto-scale` | Configure autoscale instead of over-provisioning |
| `cost-stop-dev` | Stop/deallocate dev apps when not in use |

### 7. Monitoring (MEDIUM)

| Rule | Description |
|------|-------------|
| `monitor-app-insights` | Enable Application Insights for APM |
| `monitor-diagnostic-settings` | Configure diagnostic settings to Log Analytics |
| `monitor-alerts` | Set up alerts for HTTP errors, response time, CPU |
| `monitor-availability` | Configure availability tests for uptime monitoring |
| `monitor-log-streaming` | Enable application logging for troubleshooting |

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Storing secrets in app settings | Credentials exposed in portal/APIs | Use Key Vault references |
| Deploying directly to production | Downtime risk, no rollback | Use deployment slots |
| Using Free/Shared for production | No SLA, shared resources | Use Basic+ with Always On |
| Polling-based scaling | Slow reaction, resource waste | Use metric-based autoscale |
| Synchronous blocking calls | Thread starvation | Use async/await patterns |
| Large app packages | Slow cold starts | Optimize dependencies, use Run From Package |
| Hardcoded connection strings | Difficult rotation, env coupling | Use app settings + Key Vault |
| Ignoring health checks | Bad instances receive traffic | Configure health check path |

## Implementation Examples

### Enable Security Essentials

```bash
# Managed Identity
az webapp identity assign --name <app> --resource-group <rg>

# HTTPS Only + TLS 1.2
az webapp update --name <app> --resource-group <rg> --https-only true
az webapp config set --name <app> --resource-group <rg> --min-tls-version 1.2

# Disable FTP
az webapp config set --name <app> --resource-group <rg> --ftps-state Disabled
```

### Enable Reliability Essentials

```bash
# Always On
az webapp config set --name <app> --resource-group <rg> --always-on true

# Health Check
az webapp config set --name <app> --resource-group <rg> \
  --generic-configurations '{"healthCheckPath": "/health"}'

# Create staging slot
az webapp deployment slot create --name <app> --resource-group <rg> --slot staging
```

### Enable Performance Essentials

```bash
# HTTP/2
az webapp config set --name <app> --resource-group <rg> --http20-enabled true

# Disable ARR affinity (stateless apps)
az webapp update --name <app> --resource-group <rg> --client-affinity-enabled false

# Run From Package
az webapp config appsettings set --name <app> --resource-group <rg> \
  --settings WEBSITE_RUN_FROM_PACKAGE=1
```

### Configure Autoscaling

```bash
az monitor autoscale create \
  --resource-group <rg> \
  --resource <plan-name> \
  --resource-type Microsoft.Web/serverfarms \
  --min-count 2 --max-count 10 --count 2

az monitor autoscale rule create \
  --resource-group <rg> \
  --autoscale-name <rule-name> \
  --condition "CpuPercentage > 70 avg 5m" \
  --scale out 1
```

## SKU Selection Guide

| Workload | Recommended SKU | Why |
|----------|-----------------|-----|
| Dev/Test | F1, B1 | Low cost, sufficient for testing |
| Low-traffic production | B1, S1 | Always On, custom domains, SLA |
| Standard production | S1-S3 | Autoscale, slots, backups |
| Production (preferred) | P0V4-P3V4 | Latest generation, ARM64 support, best perf/cost |
| Production (fallback) | P0V3-P3V3 | Use if P*V4 not available in region |
| Memory-optimized (preferred) | P1MV4-P5MV4 | ARM64 with higher memory-to-core ratio |
| Memory-optimized (fallback) | P1MV3-P5MV3 | Use if P*MV4 not available in region |
| Isolated/Dedicated | I1V2-I6V2 | App Service Environment, single-tenant |
| Isolated memory-optimized | I1MV2-I5MV2 | ASE with higher memory-to-core ratio |

> **Note**: P*V2 SKUs are legacy. Always prefer P*V4 (or P*V3 if V4 unavailable).

## References

- **Security Rules**: See [references/rules/security.md](references/rules/security.md) for detailed security rule explanations
- **CLI Reference**: See [references/cli-reference.md](references/cli-reference.md) for command documentation
- **Troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md) for diagnostics

## Scripts

- `scripts/audit.sh` - Audit App Service configuration against best practices
- `scripts/health-check.sh` - App health check and diagnostics

## Related Skills

Install complementary App Service skills for specialized guidance:

```bash
# Install all App Service skills
npx skills add seligj95/azure-app-service-skills
```

| Skill | Focus |
|-------|-------|
| `azure-app-service-deployment` | GitHub Actions CI/CD, deployment slots, Run From Package |
| `azure-app-service-monitoring` | Application Insights, KQL queries, alerts, availability tests |
| `azure-app-service-security` | Managed Identity, Key Vault integration, Easy Auth, access restrictions |
| `azure-app-service-networking` | VNet integration, private endpoints, Front Door, Traffic Manager |
| `azure-app-service-environment` | App Service Environment v3 for isolated, dedicated deployments |
| `azure-app-service-managed-instance` | Legacy Windows apps requiring COM, registry, MSI (Pv4/Pmv4 preview) |
| `azure-app-service-troubleshooting` | HTTP error diagnosis, startup failures, Kudu tools, auto-heal |
