---
name: tempo
description: Guide for implementing Grafana Tempo - a high-scale distributed tracing backend for OpenTelemetry traces. Use when configuring Tempo deployments, setting up storage backends (S3, Azure Blob, GCS), writing TraceQL queries, deploying via Helm, understanding trace structure, or troubleshooting Tempo issues on Kubernetes.
---

# Grafana Tempo Skill

Comprehensive guide for Grafana Tempo - the cost-effective, high-scale distributed tracing backend designed for OpenTelemetry.

## What is Tempo?

Tempo is a **high-scale distributed tracing backend** that:

- **Trace-ID lookup model** - No indexing of every attribute, keeps ingestion fast and storage costs low
- **OpenTelemetry native** - First-class support for OTLP protocol
- **Object storage backed** - Stores traces in affordable S3, GCS, or Azure Blob Storage
- **TraceQL query language** - Powerful query language inspired by PromQL and LogQL
- **Apache Parquet format** - 5-10x less data pulled per query vs legacy formats
- **Multi-tenant by default** - Built-in tenant isolation via `X-Scope-OrgID` header

## Architecture Overview

### Core Components

| Component | Purpose |
|-----------|---------|
| **Distributor** | Entry point for trace data, routes to ingesters via consistent hash ring |
| **Ingester** | Buffers traces in memory, creates Parquet blocks, flushes to storage |
| **Query Frontend** | Query orchestration, shards blockID space, coordinates queriers |
| **Querier** | Locates traces in ingesters or storage using bloom filters |
| **Compactor** | Compresses blocks, deduplicates data, manages retention |
| **Metrics Generator** | Optional: derives metrics from traces |

### Data Flow

**Write Path:**

```
Applications → Collector → Distributor → Ingester → Object Storage
                                  ↓
                           Consistent Hash Ring
                           (routes by traceID)
```

**Read Path:**

```
Query Request → Query Frontend → Queriers → Ingesters (recent data)
                      ↓                            ↓
                 Block Sharding          Object Storage (historical data)
                      ↓                            ↓
              Parallel Querier Work      Bloom Filters + Indexes
```

## Deployment Modes

### 1. Monolithic Mode (`-target=all`)

- All components in single process
- Best for: Local testing, small-scale deployments
- **Cannot horizontally scale** component count
- Scale by increasing replicas

### 2. Scalable Monolithic (`-target=scalable-single-binary`)

- All components in one process with horizontal scaling
- Each instance runs all components
- Good for development with scaling needs

### 3. Microservices Mode (Distributed) - Recommended for Production

```yaml
# Using tempo-distributed Helm chart
distributor:
  replicas: 3

ingester:
  replicas: 3

querier:
  replicas: 2

queryFrontend:
  replicas: 2

compactor:
  replicas: 1
```

## Helm Deployment

### Add Repository

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### Install Distributed Tempo

```bash
helm install tempo grafana/tempo-distributed \
  --namespace monitoring \
  --values values.yaml
```

### Production Values Example

```yaml
# Storage configuration
storage:
  trace:
    backend: azure  # or s3, gcs
    azure:
      container_name: tempo-traces
      storage_account_name: mystorageaccount
      use_federated_token: true  # Workload Identity

# Distributor
distributor:
  replicas: 3
  resources:
    requests:
      cpu: 500m
      memory: 2Gi
    limits:
      memory: 4Gi

# Ingester
ingester:
  replicas: 3
  resources:
    requests:
      cpu: 1000m
      memory: 2Gi
    limits:
      memory: 8Gi  # Spikes to 8GB periodically
  persistence:
    enabled: true
    size: 20Gi

# Querier
querier:
  replicas: 2
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      memory: 4Gi

# Query Frontend
queryFrontend:
  replicas: 2
  resources:
    requests:
      cpu: 100m
      memory: 100Mi
    limits:
      memory: 2Gi

# Compactor
compactor:
  replicas: 1
  resources:
    requests:
      cpu: 500m
      memory: 2Gi
    limits:
      memory: 6Gi

# Block retention
compactor:
  compaction:
    block_retention: 336h  # 14 days

# Gateway for external access
gateway:
  enabled: true
  replicas: 1

# Metrics Generator (optional)
metricsGenerator:
  enabled: false
```

## Storage Configuration

### Azure Blob Storage (Recommended for Azure)

```yaml
storage:
  trace:
    backend: azure
    azure:
      container_name: tempo-traces
      storage_account_name: <storage-account-name>
      # Option 1: Workload Identity (Recommended)
      use_federated_token: true
      # Option 2: User-Assigned Managed Identity
      use_managed_identity: true
      user_assigned_id: <identity-client-id>
      # Option 3: Account Key (Dev only)
      # storage_account_key: <account-key>
      endpoint_suffix: blob.core.windows.net
      hedge_requests_at: 400ms
      hedge_requests_up_to: 2
```

### AWS S3

```yaml
storage:
  trace:
    backend: s3
    s3:
      bucket: my-tempo-bucket
      region: us-east-1
      endpoint: s3.us-east-1.amazonaws.com
      # Use IAM roles or access keys
      access_key: <access-key>
      secret_key: <secret-key>
```

### Google Cloud Storage

```yaml
storage:
  trace:
    backend: gcs
    gcs:
      bucket_name: my-tempo-bucket
      # Uses Workload Identity or service account
```

## TraceQL Query Language

### Basic Queries

```traceql
# Simplest query - all spans
{ }

# Filter by service
{ resource.service.name = "frontend" }

# Filter by operation
{ span:name = "GET /api/orders" }

# Filter by status
{ span:status = error }

# Filter by duration
{ span:duration > 500ms }

# Multiple conditions
{ resource.service.name = "api" && span:status = error }
```

### Structural Operators

```traceql
# Direct parent-child relationship
{ resource.service.name = "frontend" } > { resource.service.name = "api" }

# Ancestor-descendant relationship
{ span:name = "GET /api/products" } >> { span.db.system = "postgresql" }

# Sibling relationship
{ span:name = "span-a" } ~ { span:name = "span-b" }
```

### Aggregation Functions

```traceql
# Count spans
{ } | count() > 10

# Average duration
{ } | avg(span:duration) > 20ms

# Max duration
{ span:status = error } | max(span:duration)
```

### Metrics Functions

```traceql
# Rate of errors
{ span:status = error } | rate()

# Count over time
{ span:name = "GET /:endpoint" } | count_over_time()

# Percentile latency
{ span:name = "GET /:endpoint" } | quantile_over_time(span:duration, .99)

# Group by service
{ span:status = error } | rate() by(resource.service.name)

# Top 10 by error rate
{ span:status = error } | rate() by(resource.service.name) | topk(10)
```

## Trace Structure

### Intrinsic Fields (colon separator)

| Field | Description |
|-------|-------------|
| `span:name` | Operation name |
| `span:duration` | Elapsed time (e.g., "10ms", "1.5s") |
| `span:status` | `ok`, `error`, or `unset` |
| `span:kind` | `server`, `client`, `producer`, `consumer`, `internal` |
| `trace:duration` | Total trace duration |
| `trace:rootName` | Root span name |
| `trace:rootService` | Root span service |

### Attribute Scopes (period separator)

| Scope | Example | Description |
|-------|---------|-------------|
| `span.` | `span.http.method` | Span-level attributes |
| `resource.` | `resource.service.name` | Resource attributes |
| `event.` | `event.exception.message` | Event attributes |
| `link.` | `link.traceID` | Link attributes |

## Receiver Endpoints

| Protocol | Port | Endpoint |
|----------|------|----------|
| **OTLP gRPC** | 4317 | `/v1/traces` |
| **OTLP HTTP** | 4318 | `/v1/traces` |
| **Jaeger gRPC** | 14250 | - |
| **Jaeger Thrift HTTP** | 14268 | `/api/traces` |
| **Jaeger Thrift Compact** | 6831 | UDP |
| **Jaeger Thrift Binary** | 6832 | UDP |
| **Zipkin** | 9411 | `/api/v2/spans` |

## Multi-Tenancy

```yaml
# Enable multi-tenancy
multitenancy_enabled: true

# All requests must include X-Scope-OrgID header
# Example:
# curl -H "X-Scope-OrgID: tenant-1" http://tempo:3200/api/traces/<traceID>
```

## Azure Identity Configuration

### Workload Identity Federation (Recommended)

**1. Enable Workload Identity on AKS:**

```bash
az aks update \
  --name <aks-cluster> \
  --resource-group <rg> \
  --enable-oidc-issuer \
  --enable-workload-identity
```

**2. Create User-Assigned Managed Identity:**

```bash
az identity create \
  --name tempo-identity \
  --resource-group <rg>

IDENTITY_CLIENT_ID=$(az identity show --name tempo-identity --resource-group <rg> --query clientId -o tsv)
```

**3. Assign Storage Permission:**

```bash
az role assignment create \
  --role "Storage Blob Data Contributor" \
  --assignee-object-id <principal-id> \
  --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage>
```

**4. Create Federated Credential:**

```bash
az identity federated-credential create \
  --name tempo-federated \
  --identity-name tempo-identity \
  --resource-group <rg> \
  --issuer <aks-oidc-issuer-url> \
  --subject system:serviceaccount:monitoring:tempo \
  --audiences api://AzureADTokenExchange
```

**5. Configure Helm Values:**

```yaml
serviceAccount:
  annotations:
    azure.workload.identity/client-id: <IDENTITY_CLIENT_ID>

podLabels:
  azure.workload.identity/use: "true"

storage:
  trace:
    azure:
      use_federated_token: true
```

## Troubleshooting

### Common Issues

**1. Container Not Found (Azure)**

```bash
az storage container create --name tempo-traces --account-name <storage>
```

**2. Authorization Failure (Azure)**

```bash
# Verify RBAC assignment
az role assignment list --scope <storage-scope>

# Assign if missing
az role assignment create \
  --role "Storage Blob Data Contributor" \
  --assignee-object-id <principal-id> \
  --scope <storage-scope>
```

**3. Ingester OOM**

```yaml
ingester:
  resources:
    limits:
      memory: 16Gi  # Increase from 8Gi
```

**4. Query Timeout**

```yaml
querier:
  query_timeout: 5m
  max_concurrent_queries: 20
```

### Diagnostic Commands

```bash
# Check pod status
kubectl get pods -n monitoring -l app.kubernetes.io/name=tempo

# Check distributor logs
kubectl logs -n monitoring -l app.kubernetes.io/component=distributor --tail=100

# Check ingester logs
kubectl logs -n monitoring -l app.kubernetes.io/component=ingester --tail=100

# Verify readiness
kubectl exec -it <tempo-pod> -n monitoring -- wget -qO- http://localhost:3200/ready

# Check ring status
kubectl port-forward svc/tempo-distributor 3200:3200 -n monitoring
curl http://localhost:3200/distributor/ring
```

## API Reference

### Trace Retrieval

```bash
# Get trace by ID
GET /api/traces/<traceID>

# Search traces (TraceQL)
GET /api/search?q={resource.service.name="api"}

# Search tags
GET /api/search/tags
GET /api/search/tag/<tag>/values
```

### Health

```bash
GET /ready
GET /metrics
```

## Reference Documentation

For detailed configuration by topic:

- **[Storage Configuration](references/storage.md)**: Object stores, retention, caching
- **[TraceQL Reference](references/traceql.md)**: Query syntax and examples
- **[Configuration Reference](references/configuration.md)**: Full configuration manifest

## External Resources

- [Official Tempo Documentation](https://grafana.com/docs/tempo/latest/)
- [Tempo Helm Chart](https://github.com/grafana/helm-charts/tree/main/charts/tempo-distributed)
- [TraceQL Documentation](https://grafana.com/docs/tempo/latest/traceql/)
- [Tempo GitHub Repository](https://github.com/grafana/tempo)
