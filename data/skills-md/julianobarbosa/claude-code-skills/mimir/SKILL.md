---
name: mimir
description: Guide for implementing Grafana Mimir - a horizontally scalable, highly available, multi-tenant TSDB for long-term storage of Prometheus metrics. Use when configuring Mimir on Kubernetes, setting up Azure/S3/GCS storage backends, troubleshooting authentication issues, or optimizing performance.
---

# Grafana Mimir Skill

Comprehensive guide for Grafana Mimir - the horizontally scalable, highly available, multi-tenant time series database for long-term Prometheus metrics storage.

## What is Mimir?

Mimir is an **open-source, horizontally scalable, highly available, multi-tenant long-term storage solution** for Prometheus and OpenTelemetry metrics that:

- **Overcomes Prometheus limitations** - Scalability and long-term retention
- **Multi-tenant by default** - Built-in tenant isolation via `X-Scope-OrgID` header
- **Stores data in object storage** - S3, GCS, Azure Blob Storage, or Swift
- **100% Prometheus compatible** - PromQL queries, remote write protocol
- **Part of LGTM+ Stack** - Logs, Grafana, Traces, Metrics unified observability

## Architecture Overview

### Core Components

| Component | Purpose |
|-----------|---------|
| **Distributor** | Validates requests, routes incoming metrics to ingesters via hash ring |
| **Ingester** | Stores time-series data in memory, flushes to object storage |
| **Querier** | Executes PromQL queries from ingesters and store-gateways |
| **Query Frontend** | Caches query results, optimizes and splits queries |
| **Query Scheduler** | Manages per-tenant query queues for fairness |
| **Store-Gateway** | Provides access to historical metric blocks in object storage |
| **Compactor** | Consolidates and optimizes stored metric data blocks |
| **Ruler** | Evaluates recording and alerting rules (optional) |
| **Alertmanager** | Handles alert routing and deduplication (optional) |

### Data Flow

**Write Path:**

```
Prometheus/OTel → Distributor → Ingester → Object Storage
                       ↓
                 Hash Ring
                 (routes by series)
```

**Read Path:**

```
Query → Query Frontend → Query Scheduler → Querier
                                              ↓
                                    Ingesters (recent)
                                              ↓
                                    Store-Gateway (historical)
```

## Deployment Modes

### 1. Monolithic Mode (`-target=all`)

- All components in single process
- Best for: Development, testing, small-scale (~1M series)
- Horizontally scalable by deploying multiple instances
- **Not recommended** for large-scale (all components scale together)

### 2. Microservices Mode (Distributed) - Recommended for Production

```yaml
# Using mimir-distributed Helm chart
distributor:
  replicas: 3

ingester:
  replicas: 3
  zoneAwareReplication:
    enabled: true

querier:
  replicas: 3

queryFrontend:
  replicas: 2

queryScheduler:
  replicas: 2

storeGateway:
  replicas: 3

compactor:
  replicas: 1
```

## Helm Deployment

### Add Repository

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### Install Distributed Mimir

```bash
helm install mimir grafana/mimir-distributed \
  --namespace monitoring \
  --values values.yaml
```

### Pre-Built Values Files

| File | Purpose |
|------|---------|
| `values.yaml` | Non-production testing with MinIO |
| `small.yaml` | ~1 million series (single replicas, not HA) |
| `large.yaml` | Production (~10 million series) |

### Production Values Example

```yaml
# Deployment mode
mimir:
  structuredConfig:
    multitenancy_enabled: true

# Storage configuration
mimir:
  structuredConfig:
    common:
      storage:
        backend: azure  # or s3, gcs
        azure:
          account_name: ${AZURE_STORAGE_ACCOUNT}
          account_key: ${AZURE_STORAGE_KEY}
          endpoint_suffix: blob.core.windows.net

    blocks_storage:
      azure:
        container_name: mimir-blocks

    alertmanager_storage:
      azure:
        container_name: mimir-alertmanager

    ruler_storage:
      azure:
        container_name: mimir-ruler

# Distributor
distributor:
  replicas: 3
  resources:
    requests:
      cpu: 1
      memory: 2Gi
    limits:
      memory: 4Gi

# Ingester
ingester:
  replicas: 3
  zoneAwareReplication:
    enabled: true
  persistentVolume:
    enabled: true
    size: 50Gi
  resources:
    requests:
      cpu: 2
      memory: 8Gi
    limits:
      memory: 16Gi

# Querier
querier:
  replicas: 3
  resources:
    requests:
      cpu: 1
      memory: 2Gi
    limits:
      memory: 8Gi

# Query Frontend
query_frontend:
  replicas: 2
  resources:
    requests:
      cpu: 500m
      memory: 1Gi
    limits:
      memory: 2Gi

# Query Scheduler
query_scheduler:
  replicas: 2

# Store Gateway
store_gateway:
  replicas: 3
  persistentVolume:
    enabled: true
    size: 20Gi
  resources:
    requests:
      cpu: 500m
      memory: 2Gi
    limits:
      memory: 8Gi

# Compactor
compactor:
  replicas: 1
  persistentVolume:
    enabled: true
    size: 50Gi
  resources:
    requests:
      cpu: 1
      memory: 4Gi
    limits:
      memory: 8Gi

# Gateway for external access
gateway:
  enabledNonEnterprise: true
  replicas: 2

# Monitoring
metaMonitoring:
  serviceMonitor:
    enabled: true
```

## Storage Configuration

### Critical Requirements

- **Must create buckets manually** - Mimir doesn't create them
- **Separate buckets required** - blocks_storage, alertmanager_storage, ruler_storage cannot share the same bucket+prefix
- **Azure**: Hierarchical namespace must be disabled

### Azure Blob Storage

```yaml
mimir:
  structuredConfig:
    common:
      storage:
        backend: azure
        azure:
          account_name: <storage-account-name>
          # Option 1: Account Key (via environment variable)
          account_key: ${AZURE_STORAGE_KEY}
          # Option 2: User-Assigned Managed Identity
          # user_assigned_id: <identity-client-id>
          endpoint_suffix: blob.core.windows.net

    blocks_storage:
      azure:
        container_name: mimir-blocks

    alertmanager_storage:
      azure:
        container_name: mimir-alertmanager

    ruler_storage:
      azure:
        container_name: mimir-ruler
```

### AWS S3

```yaml
mimir:
  structuredConfig:
    common:
      storage:
        backend: s3
        s3:
          endpoint: s3.us-east-1.amazonaws.com
          region: us-east-1
          access_key_id: ${AWS_ACCESS_KEY_ID}
          secret_access_key: ${AWS_SECRET_ACCESS_KEY}

    blocks_storage:
      s3:
        bucket_name: mimir-blocks

    alertmanager_storage:
      s3:
        bucket_name: mimir-alertmanager

    ruler_storage:
      s3:
        bucket_name: mimir-ruler
```

### Google Cloud Storage

```yaml
mimir:
  structuredConfig:
    common:
      storage:
        backend: gcs
        gcs:
          service_account: ${GCS_SERVICE_ACCOUNT_JSON}

    blocks_storage:
      gcs:
        bucket_name: mimir-blocks

    alertmanager_storage:
      gcs:
        bucket_name: mimir-alertmanager

    ruler_storage:
      gcs:
        bucket_name: mimir-ruler
```

## Limits Configuration

```yaml
mimir:
  structuredConfig:
    limits:
      # Ingestion limits
      ingestion_rate: 25000                    # Samples/sec per tenant
      ingestion_burst_size: 50000              # Burst size
      max_series_per_metric: 10000
      max_series_per_user: 1000000
      max_global_series_per_user: 1000000
      max_label_names_per_series: 30
      max_label_name_length: 1024
      max_label_value_length: 2048

      # Query limits
      max_fetched_series_per_query: 100000
      max_fetched_chunks_per_query: 2000000
      max_query_lookback: 0                    # No limit
      max_query_parallelism: 32

      # Retention
      compactor_blocks_retention_period: 365d  # 1 year

      # Out-of-order samples
      out_of_order_time_window: 5m
```

### Per-Tenant Overrides (Runtime Configuration)

```yaml
# runtime-config.yaml
overrides:
  tenant1:
    ingestion_rate: 50000
    max_series_per_user: 2000000
    compactor_blocks_retention_period: 730d    # 2 years
  tenant2:
    ingestion_rate: 75000
    max_global_series_per_user: 5000000
```

Enable runtime configuration:

```yaml
mimir:
  structuredConfig:
    runtime_config:
      file: /etc/mimir/runtime-config.yaml
      period: 10s
```

## High Availability Configuration

### HA Tracker for Prometheus Deduplication

```yaml
mimir:
  structuredConfig:
    distributor:
      ha_tracker:
        enable_ha_tracker: true
        kvstore:
          store: memberlist
        cluster_label: cluster
        replica_label: __replica__

    memberlist:
      join_members:
        - mimir-gossip-ring.monitoring.svc.cluster.local:7946
```

**Prometheus Configuration:**

```yaml
global:
  external_labels:
    cluster: prom-team1
    __replica__: replica1

remote_write:
  - url: http://mimir-gateway:8080/api/v1/push
    headers:
      X-Scope-OrgID: my-tenant
```

### Zone-Aware Replication

```yaml
ingester:
  zoneAwareReplication:
    enabled: true
    zones:
      - name: zone-a
        nodeSelector:
          topology.kubernetes.io/zone: us-east-1a
      - name: zone-b
        nodeSelector:
          topology.kubernetes.io/zone: us-east-1b
      - name: zone-c
        nodeSelector:
          topology.kubernetes.io/zone: us-east-1c

store_gateway:
  zoneAwareReplication:
    enabled: true
```

## Shuffle Sharding

Limits tenant data to a subset of instances for fault isolation:

```yaml
mimir:
  structuredConfig:
    limits:
      # Write path
      ingestion_tenant_shard_size: 3

      # Read path
      max_queriers_per_tenant: 5
      store_gateway_tenant_shard_size: 3
```

## OpenTelemetry Integration

### OTLP Metrics Ingestion

**OpenTelemetry Collector Config:**

```yaml
exporters:
  otlphttp:
    endpoint: http://mimir-gateway:8080/otlp
    headers:
      X-Scope-OrgID: "my-tenant"

service:
  pipelines:
    metrics:
      receivers: [otlp]
      exporters: [otlphttp]
```

### Exponential Histograms (Experimental)

```go
// Go SDK configuration
Aggregation: metric.AggregationBase2ExponentialHistogram{
    MaxSize:  160,      // Maximum buckets
    MaxScale: 20,       // Scale factor
}
```

**Key Benefits:**

- Explicit min/max values (no estimation needed)
- Better accuracy for extreme percentiles
- Native OTLP format preservation

## Multi-Tenancy

```yaml
mimir:
  structuredConfig:
    multitenancy_enabled: true
    no_auth_tenant: anonymous    # Used when multitenancy disabled
```

**Query with tenant header:**

```bash
curl -H "X-Scope-OrgID: tenant-a" \
  "http://mimir:8080/prometheus/api/v1/query?query=up"
```

**Tenant ID Constraints:**

- Max 150 characters
- Allowed: alphanumeric, `!` `-` `_` `.` `*` `'` `(` `)`
- Prohibited: `.` or `..` alone, `__mimir_cluster`, slashes

## API Reference

### Ingestion Endpoints

```bash
# Prometheus remote write
POST /api/v1/push

# OTLP metrics
POST /otlp/v1/metrics

# InfluxDB line protocol
POST /api/v1/push/influx/write
```

### Query Endpoints

```bash
# Instant query
GET,POST /prometheus/api/v1/query?query=<promql>&time=<timestamp>

# Range query
GET,POST /prometheus/api/v1/query_range?query=<promql>&start=<start>&end=<end>&step=<step>

# Labels
GET,POST /prometheus/api/v1/labels
GET /prometheus/api/v1/label/{name}/values

# Series
GET,POST /prometheus/api/v1/series

# Exemplars
GET,POST /prometheus/api/v1/query_exemplars

# Cardinality
GET,POST /prometheus/api/v1/cardinality/label_names
GET,POST /prometheus/api/v1/cardinality/active_series
```

### Administrative Endpoints

```bash
# Flush ingester data
GET,POST /ingester/flush

# Prepare shutdown
GET,POST,DELETE /ingester/prepare-shutdown

# Ring status
GET /ingester/ring
GET /distributor/ring
GET /store-gateway/ring
GET /compactor/ring

# Tenant stats
GET /distributor/all_user_stats
GET /api/v1/user_stats
GET /api/v1/user_limits
```

### Health & Config

```bash
GET /ready
GET /metrics
GET /config
GET /config?mode=diff
GET /runtime_config
```

## Azure Identity Configuration

### User-Assigned Managed Identity

**1. Create Identity:**

```bash
az identity create \
  --name mimir-identity \
  --resource-group <rg>

IDENTITY_CLIENT_ID=$(az identity show --name mimir-identity --resource-group <rg> --query clientId -o tsv)
IDENTITY_PRINCIPAL_ID=$(az identity show --name mimir-identity --resource-group <rg> --query principalId -o tsv)
```

**2. Assign to Node Pool:**

```bash
az vmss identity assign \
  --resource-group <aks-node-rg> \
  --name <vmss-name> \
  --identities /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/mimir-identity
```

**3. Grant Storage Permission:**

```bash
az role assignment create \
  --role "Storage Blob Data Contributor" \
  --assignee-object-id $IDENTITY_PRINCIPAL_ID \
  --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage>
```

**4. Configure Mimir:**

```yaml
mimir:
  structuredConfig:
    common:
      storage:
        azure:
          user_assigned_id: <IDENTITY_CLIENT_ID>
```

### Workload Identity Federation

**1. Create Federated Credential:**

```bash
az identity federated-credential create \
  --name mimir-federated \
  --identity-name mimir-identity \
  --resource-group <rg> \
  --issuer <aks-oidc-issuer-url> \
  --subject system:serviceaccount:monitoring:mimir \
  --audiences api://AzureADTokenExchange
```

**2. Configure Helm Values:**

```yaml
serviceAccount:
  annotations:
    azure.workload.identity/client-id: <IDENTITY_CLIENT_ID>

podLabels:
  azure.workload.identity/use: "true"
```

## Troubleshooting

### Common Issues

**1. Container Not Found (Azure)**

```bash
# Create required containers
az storage container create --name mimir-blocks --account-name <storage>
az storage container create --name mimir-alertmanager --account-name <storage>
az storage container create --name mimir-ruler --account-name <storage>
```

**2. Authorization Failure (Azure)**

```bash
# Verify RBAC assignment
az role assignment list --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage>

# Assign if missing
az role assignment create \
  --role "Storage Blob Data Contributor" \
  --assignee-object-id <principal-id> \
  --scope <storage-scope>

# Restart pod to refresh token
kubectl delete pod -n monitoring <ingester-pod>
```

**3. Ingester OOM**

```yaml
ingester:
  resources:
    limits:
      memory: 16Gi  # Increase memory
```

**4. Query Timeout**

```yaml
mimir:
  structuredConfig:
    querier:
      timeout: 5m
      max_concurrent: 20
```

**5. High Cardinality**

```yaml
mimir:
  structuredConfig:
    limits:
      max_series_per_user: 5000000
      max_series_per_metric: 50000
```

### Diagnostic Commands

```bash
# Check pod status
kubectl get pods -n monitoring -l app.kubernetes.io/name=mimir

# Check ingester logs
kubectl logs -n monitoring -l app.kubernetes.io/component=ingester --tail=100

# Check distributor logs
kubectl logs -n monitoring -l app.kubernetes.io/component=distributor --tail=100

# Verify readiness
kubectl exec -it <mimir-pod> -n monitoring -- wget -qO- http://localhost:8080/ready

# Check ring status
kubectl port-forward svc/mimir-distributor 8080:8080 -n monitoring
curl http://localhost:8080/distributor/ring

# Check configuration
kubectl exec -it <mimir-pod> -n monitoring -- cat /etc/mimir/mimir.yaml

# Validate configuration before deployment
mimir -modules -config.file <path-to-config-file>
```

### Key Metrics to Monitor

```promql
# Ingestion rate per tenant
sum by (user) (rate(cortex_distributor_received_samples_total[5m]))

# Series count per tenant
sum by (user) (cortex_ingester_memory_series)

# Query latency
histogram_quantile(0.99, sum by (le) (rate(cortex_request_duration_seconds_bucket{route=~"/api/prom/api/v1/query.*"}[5m])))

# Compactor status
cortex_compactor_runs_completed_total
cortex_compactor_runs_failed_total

# Store-gateway block sync
cortex_bucket_store_blocks_loaded
```

## Circuit Breakers (Ingester)

```yaml
mimir:
  structuredConfig:
    ingester:
      push_circuit_breaker:
        enabled: true
        request_timeout: 2s
        failure_threshold_percentage: 10
        cooldown_period: 10s
      read_circuit_breaker:
        enabled: true
        request_timeout: 30s
```

**States:**

1. **Closed** - Normal operation
2. **Open** - Stops forwarding to failing instances
3. **Half-open** - Limited trial requests after cooldown

## External Resources

- [Official Mimir Documentation](https://grafana.com/docs/mimir/latest/)
- [Mimir Helm Chart](https://github.com/grafana/mimir/tree/main/operations/helm/charts/mimir-distributed)
- [Configuration Reference](https://grafana.com/docs/mimir/latest/configure/configuration-parameters/)
- [HTTP API Reference](https://grafana.com/docs/mimir/latest/references/http-api/)
- [Mimir GitHub Repository](https://github.com/grafana/mimir)
