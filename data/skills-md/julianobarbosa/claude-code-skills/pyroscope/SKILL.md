---
name: pyroscope
description: >-
  Guide for Grafana Pyroscope continuous profiling. Use for Kubernetes Helm
  deployment, Go/Java/Python/.NET/Ruby/Node.js profiling, storage backends,
  trace-to-profile linking, and troubleshooting.
---

# Grafana Pyroscope Skill

Comprehensive guide for Grafana Pyroscope - the open-source continuous
profiling platform for analyzing application performance at the code level.

## What is Pyroscope?

Pyroscope is a **horizontally-scalable, highly-available, multi-tenant
continuous profiling system** that:

- **Collects profiling data continuously** with minimal overhead (~2-5% CPU)
- **Provides code-level visibility** with source-line granularity
- **Stores compressed profiles** in object storage (S3, GCS, Azure Blob)
- **Integrates with Grafana** for correlating profiles with metrics, logs, and traces
- **Supports multiple languages** - Go, Java, Python, .NET, Ruby, Node.js, Rust

## Architecture Overview

### Core Components

| Component | Purpose |
|-----------|---------|
| **Distributor** | Validates and routes incoming profiles to ingesters |
| **Ingester** | Buffers profiles in memory, compresses and writes to storage |
| **Querier** | Retrieves and processes profile data for analysis |
| **Query Frontend** | Handles query requests, caching, and scheduling |
| **Query Scheduler** | Manages per-tenant query queues |
| **Store Gateway** | Provides access to long-term profile storage |
| **Compactor** | Merges blocks, manages retention, handles deletion |

### Data Flow

**Write Path:**

```text
SDK/Alloy → Distributor → Ingester → Object Storage
                                   ↓
                             Blocks + Indexes
```

**Read Path:**

```text
Query → Query Frontend → Query Scheduler → Querier
                                             ↓
                                    Ingesters + Store Gateway
```

## Deployment Modes

### 1. Monolithic Mode (`-target=all`)

- All components in single process
- Best for: Development, small-scale deployments
- Query URL: `http://pyroscope:4040/`

### 2. Microservices Mode (Production)

- Each component runs independently
- Horizontally scalable
- Query URL: `http://pyroscope-querier:4040/`

```yaml
# Microservices deployment
architecture:
  microservices:
    enabled: true

querier:
  replicas: 3
distributor:
  replicas: 2
ingester:
  replicas: 3
compactor:
  replicas: 3
storeGateway:
  replicas: 3
```

## Quick Start - Kubernetes Helm

### Add Repository

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

### Install Single Binary

```bash
kubectl create namespace pyroscope
helm install pyroscope grafana/pyroscope -n pyroscope
```

### Install Microservices Mode

```bash
curl -Lo values-micro-services.yaml \
  https://raw.githubusercontent.com/grafana/pyroscope/main/operations/pyroscope/helm/pyroscope/values-micro-services.yaml

helm install pyroscope grafana/pyroscope \
  -n pyroscope \
  --values values-micro-services.yaml
```

## Profile Types

| Type | Description | Languages |
|------|-------------|-----------|
| **CPU** | Wall/CPU time consumption | All |
| **Memory** | Allocation objects/space, heap | Go, Java, .NET |
| **Goroutine** | Concurrent goroutines | Go |
| **Mutex** | Lock contention (count/duration) | Go, Java, .NET |
| **Block** | Thread blocking/delays | Go |
| **Exceptions** | Exception tracking | Python |

## Client Configuration Methods

### Method 1: SDK Instrumentation (Push Mode)

**Go SDK:**

```go
import "github.com/grafana/pyroscope-go"

pyroscope.Start(pyroscope.Config{
    ApplicationName: "my-app",
    ServerAddress:   "http://pyroscope:4040",
    ProfileTypes: []pyroscope.ProfileType{
        pyroscope.ProfileCPU,
        pyroscope.ProfileAllocObjects,
        pyroscope.ProfileAllocSpace,
        pyroscope.ProfileInuseObjects,
        pyroscope.ProfileInuseSpace,
        pyroscope.ProfileGoroutines,
        pyroscope.ProfileMutexCount,
        pyroscope.ProfileMutexDuration,
        pyroscope.ProfileBlockCount,
        pyroscope.ProfileBlockDuration,
    },
    Tags: map[string]string{
        "env": "production",
    },
})
```

**Java SDK:**

```java
PyroscopeAgent.start(
    new Config.Builder()
        .setApplicationName("my-app")
        .setServerAddress("http://pyroscope:4040")
        .setProfilingEvent(EventType.ITIMER)
        .setFormat(Format.JFR)
        .build()
);
```

**Python SDK:**

```python
import pyroscope

pyroscope.configure(
    application_name="my-app",
    server_address="http://pyroscope:4040",
    tags={"env": "production"},
)
```

### Method 2: Grafana Alloy (Pull Mode)

**Auto-instrumentation via Annotations:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    metadata:
      annotations:
        profiles.grafana.com/cpu.scrape: "true"
        profiles.grafana.com/cpu.port: "8080"
        profiles.grafana.com/memory.scrape: "true"
        profiles.grafana.com/memory.port: "8080"
        profiles.grafana.com/goroutine.scrape: "true"
        profiles.grafana.com/goroutine.port: "8080"
```

**Alloy Configuration:**

```river
pyroscope.scrape "default" {
  targets = discovery.kubernetes.pods.targets
  forward_to = [pyroscope.write.default.receiver]

  profiling_config {
    profile.process_cpu { enabled = true }
    profile.memory { enabled = true }
    profile.goroutine { enabled = true }
  }
}

pyroscope.write "default" {
  endpoint {
    url = "http://pyroscope:4040"
  }
}
```

### Method 3: eBPF Profiling (Linux)

**For compiled languages (C/C++, Go, Rust):**

```river
pyroscope.ebpf "default" {
  forward_to = [pyroscope.write.default.receiver]
  targets = discovery.kubernetes.pods.targets
}
```

## Storage Configuration

### Azure Blob Storage

```yaml
pyroscope:
  config:
    storage:
      backend: azure
      azure:
        container_name: pyroscope-data
        account_name: mystorageaccount
        account_key: ${AZURE_ACCOUNT_KEY}
```

### AWS S3

```yaml
pyroscope:
  config:
    storage:
      backend: s3
      s3:
        bucket_name: pyroscope-data
        region: us-east-1
        endpoint: s3.us-east-1.amazonaws.com
        access_key_id: ${AWS_ACCESS_KEY_ID}
        secret_access_key: ${AWS_SECRET_ACCESS_KEY}
```

### Google Cloud Storage

```yaml
pyroscope:
  config:
    storage:
      backend: gcs
      gcs:
        bucket_name: pyroscope-data
        # Uses GOOGLE_APPLICATION_CREDENTIALS
```

## Grafana Integration

### Data Source Configuration

```yaml
apiVersion: 1
datasources:
  - name: Pyroscope
    type: grafana-pyroscope-datasource
    access: proxy
    url: http://pyroscope-querier:4040
    isDefault: false
    editable: true
```

### Trace-to-Profile Linking

Enable span profiles to correlate traces with profiles:

**Go with OpenTelemetry:**

```go
import (
    "github.com/grafana/pyroscope-go"
    otelpyroscope "github.com/grafana/otel-profiling-go"
)

tp := trace.NewTracerProvider(
    trace.WithSpanProcessor(otelpyroscope.NewSpanProcessor()),
)
```

**Requirements:**

- Minimum span duration: 20ms
- Supported: Go, Java, .NET, Python, Ruby

## Resource Requirements

### Single Binary (Development)

```yaml
resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 1
    memory: 2Gi
```

### Microservices (Production)

| Component | CPU Request | Memory Request | Memory Limit |
|-----------|-------------|----------------|--------------|
| Distributor | 500m | 256Mi | 1Gi |
| Ingester | 1 | 8Gi | 16Gi |
| Querier | 100m | 256Mi | 1Gi |
| Query Frontend | 100m | 256Mi | 1Gi |
| Compactor | 1 | 8Gi | 16Gi |
| Store Gateway | 1 | 8Gi | 16Gi |

## Common Helm Values

```yaml
# Production values
architecture:
  microservices:
    enabled: true

pyroscope:
  persistence:
    enabled: true
    size: 50Gi

  config:
    storage:
      backend: s3
      s3:
        bucket_name: pyroscope-prod
        region: us-east-1

# High availability
ingester:
  replicas: 3
  terminationGracePeriodSeconds: 600

querier:
  replicas: 3

distributor:
  replicas: 2

compactor:
  replicas: 3
  terminationGracePeriodSeconds: 1200

storeGateway:
  replicas: 3

# Pod disruption budget
podDisruptionBudget:
  enabled: true
  maxUnavailable: 1

# Topology spread
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: DoNotSchedule

# Monitoring
serviceMonitor:
  enabled: true

# Alloy for profile collection
alloy:
  enabled: true
```

## API Endpoints

### Ingestion

```bash
# Push profiles (Connect API)
POST /push.v1.PusherService/Push

# Legacy HTTP (pprof, JFR formats)
POST /ingest
```

### Query

```bash
# Merged profile
POST /querier.v1.QuerierService/SelectMergeProfile

# Flame graph data
POST /querier.v1.QuerierService/SelectMergeStacktraces

# Available labels
POST /querier.v1.QuerierService/LabelNames

# Profile types
POST /querier.v1.QuerierService/ProfileTypes

# Legacy render
GET /pyroscope/render?query={}&from=now-1h&until=now
```

### System

```bash
# Readiness
GET /ready

# Configuration
GET /config

# Metrics
GET /metrics
```

## Troubleshooting

### Diagnostic Commands

```bash
# Check pod status
kubectl get pods -n pyroscope -l app.kubernetes.io/name=pyroscope

# View ingester logs
kubectl logs -n pyroscope -l app.kubernetes.io/component=ingester --tail=100

# Check ring status
kubectl exec -it pyroscope-0 -n pyroscope -- \
  curl http://localhost:4040/ingester/ring

# Verify readiness
kubectl exec -it pyroscope-0 -n pyroscope -- \
  curl http://localhost:4040/ready

# Check configuration
kubectl exec -it pyroscope-0 -n pyroscope -- \
  curl http://localhost:4040/config
```

### Common Issues

**1. Ingester OOM:**

```yaml
ingester:
  resources:
    limits:
      memory: 16Gi
```

**2. Storage Authentication Failed:**

```bash
# Azure - verify RBAC
az role assignment create \
  --role "Storage Blob Data Contributor" \
  --assignee-object-id <principal-id> \
  --scope <storage-scope>
```

**3. High Cardinality Labels:**

```yaml
# Limit label cardinality
pyroscope:
  config:
    validation:
      max_label_names_per_series: 25
```

**4. Query Timeout:**

```yaml
pyroscope:
  config:
    querier:
      query_timeout: 5m
      max_concurrent: 8
```

## Reference Documentation

For detailed configuration by topic:

- **[Helm Deployment](references/helm-deployment.md)**: Complete Helm values reference
- **[Architecture](references/architecture.md)**: Component details and scaling
- **[SDK Instrumentation](references/sdk-instrumentation.md)**: Language SDK guides
- **[Troubleshooting](references/troubleshooting.md)**: Common issues and diagnostics

## External Resources

- [Official Pyroscope Documentation](https://grafana.com/docs/pyroscope/latest/)
- [Pyroscope Helm Chart](https://github.com/grafana/pyroscope/tree/main/operations/pyroscope/helm/pyroscope)
- [Pyroscope GitHub Repository](https://github.com/grafana/pyroscope)
- [Grafana Profiles Drilldown](https://grafana.com/docs/grafana/latest/explore/simplified-exploration/profiles/)
