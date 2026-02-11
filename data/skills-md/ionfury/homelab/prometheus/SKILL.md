---
name: prometheus
description: Query Prometheus API for cluster metrics, alerts, and observability data. Use when investigating cluster health, performance issues, resource utilization, or alert status. Triggers on questions like "what's the CPU usage", "show me firing alerts", "check memory pressure", "query prometheus for", or any PromQL-related requests.
---

# Prometheus Querying

## Setup

Prometheus is accessible via the internal ingress gateway over HTTPS. **Always use DNS-based access as the default approach.**

| Cluster | URL |
|---------|-----|
| live | `https://prometheus.internal.tomnowak.work` |
| integration | `https://prometheus.internal.integration.tomnowak.work` |
| dev | `https://prometheus.internal.dev.tomnowak.work` |

```bash
# Set URL to the appropriate cluster (live example)
export PROMETHEUS_URL=https://prometheus.internal.tomnowak.work
```

**Note:** The internal gateway uses a homelab CA certificate. Use `-k` with curl to skip TLS verification, or configure the CA trust. The `promql.sh` script uses `curl -f` internally, so set `CURL_INSECURE=true` or use the `--insecure` flag if needed.

### Fallback: Port-Forward Access

Use port-forwarding only when DNS-based access is unavailable:

```bash
KUBECONFIG=~/.kube/<cluster>.yaml kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090
export PROMETHEUS_URL=http://localhost:9090
```

## Quick Queries

Use the bundled script at `.claude/skills/prometheus/scripts/promql.sh`:

```bash
# Set URL (default uses internal gateway for live cluster)
export PROMETHEUS_URL=https://prometheus.internal.tomnowak.work

# Instant query
./scripts/promql.sh query 'up'

# Range query (last hour, 15s resolution)
./scripts/promql.sh range 'node_cpu_seconds_total' --start 1h --step 15s

# Firing alerts only
./scripts/promql.sh alerts --firing

# All alert rules
./scripts/promql.sh rules

# Find metrics by label
./scripts/promql.sh series '{job="node-exporter"}'

# Health check
./scripts/promql.sh health
```

## Common Operations

### Check Cluster Health

```bash
# CPU usage %
./scripts/promql.sh query 'avg(1 - rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100'

# Memory usage %
./scripts/promql.sh query '(1 - sum(node_memory_MemAvailable_bytes) / sum(node_memory_MemTotal_bytes)) * 100'

# Problem pods
./scripts/promql.sh query 'kube_pod_status_phase{phase!~"Running|Succeeded"} == 1'

# Container restarts (last hour)
./scripts/promql.sh query 'increase(kube_pod_container_status_restarts_total[1h]) > 0'
```

### Check Alerts

```bash
# All firing alerts
./scripts/promql.sh alerts --firing

# Full alert details
./scripts/promql.sh alerts --verbose
```

### Direct curl (alternative)

```bash
# Instant query (use -k for self-signed TLS)
curl -sk "https://prometheus.internal.tomnowak.work/api/v1/query?query=up" | jq '.data.result'

# Alerts
curl -sk "https://prometheus.internal.tomnowak.work/api/v1/alerts" | jq '.data.alerts'
```

## Reference

For homelab-specific PromQL queries (Longhorn, CloudNative-PG, Cilium, etc.), see [references/queries.md](references/queries.md).

## Prometheus Details

| Property | Value |
|----------|-------|
| Namespace | `monitoring` |
| Service | `prometheus-operated:9090` |
| Retention | 14 days / 50GB |
| External label | `prometheus_source: ${cluster_name}` |
