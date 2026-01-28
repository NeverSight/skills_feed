---
name: k8s-autoscaling
description: KEDA event-driven autoscaling for Kubernetes. Use when installing KEDA, configuring scalers (Prometheus, RabbitMQ, Kafka, etc.), setting up HPA, or implementing autoscaling best practices.
---

# K8s Autoscaling

KEDA v2.18.x (70+ built-in scalers). (Updated: January 2026). All scripts are **idempotent** - uses `helm upgrade --install`.

## Important Changes in v2.18

| Change | Details |
|--------|---------|
| Pod Identity removed | Use workload identity instead (v2.15+) |
| GCP Pub/Sub `subscriptionSize` | DEPRECATED - use `mode` and `value` instead (removed in v2.20) |
| Huawei `minMetricValue` | DEPRECATED - use `activationTargetMetricValue` (removed in v2.20) |

## Installation

See [references/keda.md](references/keda.md) for KEDA installation via Helm.

## Reference Files

- [references/keda.md](references/keda.md) - KEDA installation
- [references/keda-scalers.md](references/keda-scalers.md) - KEDA scalers
- [references/hpa.md](references/hpa.md) - Horizontal Pod Autoscaler
- [references/best-practices.md](references/best-practices.md) - Best practices