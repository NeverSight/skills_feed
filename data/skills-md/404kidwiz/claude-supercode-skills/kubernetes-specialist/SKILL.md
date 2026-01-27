---
name: kubernetes-specialist
description: "Expert Kubernetes Specialist with deep expertise in container orchestration, cluster management, and cloud-native applications. Proficient in Kubernetes architecture, Helm charts, operators, and multi-cluster management across EKS, AKS, GKE, and on-premises deployments."
---

# Kubernetes Specialist

## Purpose

Provides expert Kubernetes orchestration and cloud-native application expertise with deep knowledge of container orchestration, cluster management, and production-grade deployments. Specializes in Kubernetes architecture, Helm charts, operators, multi-cluster management, and GitOps workflows across EKS, AKS, GKE, and on-premises deployments.

## When to Use

- Designing Kubernetes cluster architecture for production workloads
- Implementing Helm charts, operators, or GitOps workflows (ArgoCD, Flux)
- Troubleshooting cluster issues (networking, storage, performance)
- Planning Kubernetes upgrades or multi-cluster strategies
- Optimizing resource utilization and cost in Kubernetes environments
- Setting up service mesh (Istio, Linkerd) and observability
- Implementing Kubernetes security and RBAC policies

## Quick Start

**Invoke this skill when:**
- Designing Kubernetes cluster architecture for production workloads
- Implementing Helm charts, operators, or GitOps workflows
- Troubleshooting cluster issues (networking, storage, performance)
- Planning Kubernetes upgrades or multi-cluster strategies
- Optimizing resource utilization and cost in Kubernetes environments

**Do NOT invoke when:**
- Simple Docker container needs (use docker commands directly)
- Cloud infrastructure provisioning (use cloud-architect instead)
- Application code debugging (use backend-developer/frontend-developer)
- Database-specific issues (use database-administrator instead)

## Decision Framework

### Deployment Strategy Selection

```
├─ Zero downtime required?
│   ├─ Instant rollback needed → Blue-Green Deployment
│   │   Pros: Instant switch, easy rollback
│   │   Cons: 2x resources during deployment
│   │
│   ├─ Gradual rollout → Canary Deployment
│   │   Pros: Test with subset of traffic
│   │   Cons: Complex routing setup
│   │
│   └─ Simple updates → Rolling Update (default)
│       Pros: Built-in, no extra resources
│       Cons: Rollback takes time
│
├─ Stateful application?
│   ├─ Database → StatefulSet + PVC
│   │   Pros: Stable network IDs, ordered deployment
│   │   Cons: Complex scaling
│   │
│   └─ Stateless → Deployment
│       Pros: Easy scaling, self-healing
│
└─ Batch processing?
    ├─ One-time → Job
    ├─ Scheduled → CronJob
    └─ Parallel processing → Job with parallelism
```

### Resource Configuration Matrix

| Workload Type | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------------|-------------|-----------|----------------|--------------|
| **Web API** | 100m-500m | 1000m | 256Mi-512Mi | 1Gi |
| **Worker** | 500m-1000m | 2000m | 512Mi-1Gi | 2Gi |
| **Database** | 1000m-2000m | 4000m | 2Gi-4Gi | 8Gi |
| **Cache** | 100m-250m | 500m | 1Gi-4Gi | 8Gi |
| **Batch Job** | 500m-2000m | 4000m | 1Gi-4Gi | 8Gi |

### Node Pool Strategy

| Use Case | Instance Type | Scaling | Cost |
|----------|--------------|---------|------|
| **System pods** | t3.large (3 nodes) | Fixed | Low |
| **Applications** | m5.xlarge | Auto 3-20 | Medium |
| **Batch/Spot** | m5.large-2xlarge | Auto 0-50 | Very Low |
| **GPU workloads** | p3.2xlarge | Manual | High |

### Red Flags → Escalate

**STOP and escalate if:**
- Cluster upgrade with breaking API changes (deprecated versions)
- Multi-region active-active requirements
- Compliance requirements (PCI-DSS, HIPAA) need validation
- Custom scheduler or controller development needed
- etcd corruption or cluster state issues

## Quality Checklist

### Cluster Configuration
- [ ] Multi-AZ deployment (nodes spread across availability zones)
- [ ] Node autoscaling configured (Cluster Autoscaler or Karpenter)
- [ ] System node pool with taints (separate critical addons from apps)
- [ ] Encryption enabled (secrets at rest with KMS)
- [ ] Audit logging enabled (API server logs)

### Security
- [ ] Pod Security Standards enforced (restricted or baseline)
- [ ] Network policies configured (default deny + explicit allow)
- [ ] RBAC configured (least privilege for all service accounts)
- [ ] Image scanning enabled (scan for vulnerabilities)
- [ ] Private container registry configured

### Resource Management
- [ ] All pods have resource requests and limits
- [ ] HorizontalPodAutoscalers configured for scalable workloads
- [ ] PodDisruptionBudgets defined (prevent too many pods down)
- [ ] ResourceQuotas set per namespace
- [ ] LimitRanges defined (default limits for pods)

### High Availability
- [ ] Deployments have ≥2 replicas
- [ ] Anti-affinity rules prevent pod co-location
- [ ] Readiness and liveness probes configured
- [ ] PodDisruptionBudgets allow for rolling updates
- [ ] Multi-region cluster (if global scale required)

### Observability
- [ ] Metrics server installed (kubectl top works)
- [ ] Prometheus monitoring application metrics
- [ ] Centralized logging (CloudWatch, Elasticsearch, Loki)
- [ ] Distributed tracing (Jaeger, Tempo)
- [ ] Dashboards for cluster and application health

### Disaster Recovery
- [ ] Velero installed for cluster backups
- [ ] Backup schedule configured (daily minimum)
- [ ] Restore tested (annual drill)
- [ ] etcd backups automated (cloud-managed clusters)

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
