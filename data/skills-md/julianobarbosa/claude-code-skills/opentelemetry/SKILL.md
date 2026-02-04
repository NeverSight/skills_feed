---
name: opentelemetry
description: Implement OpenTelemetry (OTEL) observability - Collector configuration, Kubernetes deployment, traces/metrics/logs pipelines, instrumentation, and troubleshooting. Use when working with OTEL Collector, telemetry pipelines, observability infrastructure, or Kubernetes monitoring.
---

# OpenTelemetry Implementation Guide

## Overview

OpenTelemetry (OTel) is a vendor-neutral observability framework for instrumenting, generating, collecting, and exporting telemetry data (traces, metrics, logs). This skill provides guidance for implementing OTEL in Kubernetes environments.

## Quick Start

### Deploy OTEL Collector on Kubernetes

```bash
# Add Helm repo
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update

# Install with basic config
helm install otel-collector open-telemetry/opentelemetry-collector \
  --namespace monitoring --create-namespace \
  --set mode=daemonset
```

### Send Test Data via OTLP

```bash
# gRPC endpoint: 4317, HTTP endpoint: 4318
curl -X POST http://otel-collector:4318/v1/traces \
  -H "Content-Type: application/json" \
  -d '{"resourceSpans":[]}'
```

## Core Concepts

**Signals**: Three types of telemetry data:

- **Traces**: Distributed request flows across services
- **Metrics**: Numerical measurements (counters, gauges, histograms)
- **Logs**: Event records with structured/unstructured data

**Collector Components**:

- **Receivers**: Accept data (OTLP, Prometheus, Jaeger, Zipkin)
- **Processors**: Transform data (batch, memory_limiter, k8sattributes)
- **Exporters**: Send data (prometheusremotewrite, loki, otlp)
- **Extensions**: Add capabilities (health_check, pprof, zpages)

## Collector Configuration

### Basic Pipeline Structure

```yaml
config:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: ${env:MY_POD_IP}:4317
        http:
          endpoint: ${env:MY_POD_IP}:4318

  processors:
    batch:
      timeout: 10s
      send_batch_size: 1024
    memory_limiter:
      check_interval: 5s
      limit_percentage: 80
      spike_limit_percentage: 25

  exporters:
    prometheusremotewrite:
      endpoint: "http://prometheus:9090/api/v1/write"
    loki:
      endpoint: "http://loki:3100/loki/api/v1/push"

  service:
    pipelines:
      metrics:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [prometheusremotewrite]
      logs:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [loki]
      traces:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [otlp/tempo]
```

### Kubernetes Attributes Enrichment

```yaml
processors:
  k8sattributes:
    auth_type: "serviceAccount"
    passthrough: false
    filter:
      node_from_env_var: ${env:K8S_NODE_NAME}
    extract:
      metadata:
        - k8s.pod.name
        - k8s.namespace.name
        - k8s.deployment.name
        - k8s.node.name
```

## Deployment Modes

| Mode | Use Case | Pros | Cons |
|------|----------|------|------|
| DaemonSet | Node-level collection | Full coverage, host metrics | Higher resource usage |
| Deployment | Centralized gateway | Scalable, easier management | Single point of failure |
| Sidecar | Per-pod collection | Isolated, fine-grained | Resource overhead per pod |

## Common Patterns

### Development Environment

- Enable debug exporter for visibility
- Lower resource limits (250m CPU, 512Mi memory)
- Include spot instance tolerations for cost savings

### Production Environment

- Implement sampling (10-50% for traces)
- Higher batch sizes (2048-4096)
- Enable autoscaling and PodDisruptionBudget
- Use TLS for all endpoints

## Detailed References

For in-depth guidance, see:

- **Collector Configuration**: [COLLECTOR.md](references/COLLECTOR.md)
- **Kubernetes Deployment**: [KUBERNETES.md](references/KUBERNETES.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)
- **Instrumentation**: [INSTRUMENTATION.md](references/INSTRUMENTATION.md)

## Validation Commands

```bash
# Check collector pods
kubectl get pods -n monitoring -l app.kubernetes.io/name=otel-collector

# View collector logs
kubectl logs -n monitoring -l app.kubernetes.io/name=otel-collector --tail=100

# Test OTLP endpoint
kubectl run test-otlp --image=curlimages/curl:latest --rm -it -- \
  curl -v http://otel-collector.monitoring:4318/v1/traces

# Validate config syntax
otelcol validate --config=config.yaml
```

## Key Helm Chart Values

```yaml
mode: "daemonset"  # or "deployment"
presets:
  logsCollection:
    enabled: true
  hostMetrics:
    enabled: true
  kubernetesAttributes:
    enabled: true
  kubeletMetrics:
    enabled: true
useGOMEMLIMIT: true
resources:
  limits:
    cpu: 500m
    memory: 1Gi
  requests:
    cpu: 100m
    memory: 256Mi
```
