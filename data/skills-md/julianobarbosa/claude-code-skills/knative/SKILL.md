---
name: knative
description: Knative serverless platform for Kubernetes. Use when deploying serverless workloads, configuring autoscaling (scale-to-zero), event-driven architectures, traffic management (blue-green, canary), CloudEvents routing, Brokers/Triggers/Sources, or working with Knative Serving/Eventing/Functions. Covers installation, networking (Kourier/Istio/Contour), and troubleshooting.
---

# Knative Skill

## Overview

Knative is an open-source Kubernetes-based platform for deploying and managing serverless workloads. It provides three main components:

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **Serving** | HTTP-triggered autoscaling runtime | Scale-to-zero, traffic splitting, revisions |
| **Eventing** | Event-driven architectures | Brokers, Triggers, Sources, CloudEvents |
| **Functions** | Simplified function deployment | `func` CLI, multi-language support |

**Current Version**: v1.20.0 (as of late 2024)

## When to Use This Skill

Use this skill when the user:

- Wants to deploy serverless workloads on Kubernetes
- Needs scale-to-zero autoscaling capabilities
- Is implementing event-driven architectures
- Needs traffic management (blue-green, canary, gradual rollout)
- Works with CloudEvents or event routing
- Mentions Knative Serving, Eventing, or Functions
- Asks about Brokers, Triggers, Sources, or Sinks
- Needs to configure networking layers (Kourier, Istio, Contour)

## Quick Reference

### Knative Service (Serving)

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-service
  namespace: default
spec:
  template:
    metadata:
      annotations:
        # Autoscaling configuration
        autoscaling.knative.dev/class: kpa.autoscaling.knative.dev
        autoscaling.knative.dev/min-scale: "0"
        autoscaling.knative.dev/max-scale: "10"
        autoscaling.knative.dev/target: "100"  # concurrent requests
    spec:
      containers:
        - image: gcr.io/my-project/my-app:latest
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              memory: 128Mi  # Memory limit = request (required)
          # NO CPU limits (causes throttling)
```

### Traffic Splitting

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-service
spec:
  template:
    # ... container spec
  traffic:
    # Blue-green: 100% to new or old
    - revisionName: my-service-00001
      percent: 90
    - revisionName: my-service-00002
      percent: 10
    # Or use latestRevision
    - latestRevision: true
      percent: 100
```

### Tagged Revisions (Preview URLs)

```yaml
traffic:
  - revisionName: my-service-00002
    percent: 0
    tag: staging  # Accessible at staging-my-service.example.com
  - latestRevision: true
    percent: 100
    tag: production
```

### Broker and Trigger (Eventing)

```yaml
# Create a Broker
apiVersion: eventing.knative.dev/v1
kind: Broker
metadata:
  name: default
  namespace: default
---
# Create a Trigger to route events
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: my-trigger
  namespace: default
spec:
  broker: default
  filter:
    attributes:
      type: dev.knative.example
      source: /my/source
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: my-service
```

### Event Source Example (PingSource)

```yaml
apiVersion: sources.knative.dev/v1
kind: PingSource
metadata:
  name: cron-job
spec:
  schedule: "*/1 * * * *"  # Every minute
  contentType: application/json
  data: '{"message": "Hello from cron"}'
  sink:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-display
```

## Installation

### Prerequisites

- Kubernetes cluster v1.28+
- `kubectl` configured
- Cluster admin permissions

### Method 1: YAML Install (Recommended for GitOps)

```bash
# Install Knative Serving CRDs and Core
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.20.0/serving-core.yaml

# Install Networking Layer (choose one)
# Option A: Kourier (lightweight, recommended for most cases)
kubectl apply -f https://github.com/knative/net-kourier/releases/download/knative-v1.20.0/kourier.yaml
kubectl patch configmap/config-network \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'

# Option B: Istio (for service mesh requirements)
kubectl apply -f https://github.com/knative/net-istio/releases/download/knative-v1.20.0/net-istio.yaml

# Install Knative Eventing
kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.20.0/eventing-crds.yaml
kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.20.0/eventing-core.yaml

# Install In-Memory Channel (dev only) or Kafka Channel (production)
kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.20.0/in-memory-channel.yaml

# Install MT-Channel-Based Broker
kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.20.0/mt-channel-broker.yaml
```

### Method 2: Knative Operator

```yaml
# Install the Operator
kubectl apply -f https://github.com/knative/operator/releases/download/knative-v1.20.0/operator.yaml

# Deploy Knative Serving
apiVersion: operator.knative.dev/v1beta1
kind: KnativeServing
metadata:
  name: knative-serving
  namespace: knative-serving
spec:
  ingress:
    kourier:
      enabled: true
  config:
    network:
      ingress-class: kourier.ingress.networking.knative.dev

---
# Deploy Knative Eventing
apiVersion: operator.knative.dev/v1beta1
kind: KnativeEventing
metadata:
  name: knative-eventing
  namespace: knative-eventing
```

### Configure DNS

```bash
# Get the External IP of the ingress
kubectl get svc kourier -n kourier-system

# Option A: Real DNS (production)
# Create A record: *.knative.example.com -> EXTERNAL-IP

# Option B: Magic DNS with sslip.io (development)
kubectl patch configmap/config-domain \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"<EXTERNAL-IP>.sslip.io":""}}'

# Option C: Default domain (internal only)
kubectl patch configmap/config-domain \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"example.com":""}}'
```

## Autoscaling

### Autoscaler Classes

| Class | Key | Scale to Zero | Metrics |
|-------|-----|---------------|---------|
| **KPA** (default) | `kpa.autoscaling.knative.dev` | Yes | Concurrency, RPS |
| **HPA** | `hpa.autoscaling.knative.dev` | No | CPU, Memory |

### Autoscaling Annotations

```yaml
metadata:
  annotations:
    # Autoscaler class
    autoscaling.knative.dev/class: kpa.autoscaling.knative.dev

    # Scale bounds
    autoscaling.knative.dev/min-scale: "1"    # Prevent scale-to-zero
    autoscaling.knative.dev/max-scale: "100"
    autoscaling.knative.dev/initial-scale: "3"

    # Scaling metric (KPA)
    autoscaling.knative.dev/metric: concurrency  # or rps
    autoscaling.knative.dev/target: "100"        # target per pod

    # Scale-down behavior
    autoscaling.knative.dev/scale-down-delay: "5m"
    autoscaling.knative.dev/scale-to-zero-pod-retention-period: "1m"

    # Window for averaging metrics
    autoscaling.knative.dev/window: "60s"
```

### Concurrency Limits

```yaml
spec:
  template:
    spec:
      containerConcurrency: 100  # Hard limit per pod (0 = unlimited)
```

## Networking

### Networking Layer Comparison

| Layer | Pros | Cons | Use Case |
|-------|------|------|----------|
| **Kourier** | Lightweight, fast, simple | Limited features | Most deployments |
| **Istio** | Full service mesh, mTLS | Heavy, complex | Enterprise, security-critical |
| **Contour** | Envoy-based, good performance | Medium complexity | High-traffic apps |

### TLS Configuration

```yaml
# Using cert-manager (recommended)
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-service
  annotations:
    # Auto-TLS with cert-manager
    networking.knative.dev/certificate-class: cert-manager
spec:
  # ... template spec
```

### Custom Domain Mapping

```yaml
apiVersion: serving.knative.dev/v1beta1
kind: DomainMapping
metadata:
  name: api.example.com
  namespace: default
spec:
  ref:
    kind: Service
    name: my-service
    apiVersion: serving.knative.dev/v1
```

## Eventing Patterns

### Event Source Types

| Source | Description | Use Case |
|--------|-------------|----------|
| **PingSource** | Cron-based events | Scheduled tasks |
| **ApiServerSource** | K8s API events | Cluster monitoring |
| **KafkaSource** | Kafka messages | Stream processing |
| **GitHubSource** | GitHub webhooks | CI/CD triggers |
| **ContainerSource** | Custom container | Any external system |

### Channel Types

| Channel | Persistence | Use Case |
|---------|-------------|----------|
| **InMemoryChannel** | No | Development only |
| **KafkaChannel** | Yes | Production |
| **NATSChannel** | Configurable | High throughput |

### Sequence (Chained Processing)

```yaml
apiVersion: flows.knative.dev/v1
kind: Sequence
metadata:
  name: my-sequence
spec:
  channelTemplate:
    apiVersion: messaging.knative.dev/v1
    kind: InMemoryChannel
  steps:
    - ref:
        apiVersion: serving.knative.dev/v1
        kind: Service
        name: step-1
    - ref:
        apiVersion: serving.knative.dev/v1
        kind: Service
        name: step-2
  reply:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: final-handler
```

### Parallel (Fan-out)

```yaml
apiVersion: flows.knative.dev/v1
kind: Parallel
metadata:
  name: my-parallel
spec:
  channelTemplate:
    apiVersion: messaging.knative.dev/v1
    kind: InMemoryChannel
  branches:
    - subscriber:
        ref:
          apiVersion: serving.knative.dev/v1
          kind: Service
          name: handler-a
    - subscriber:
        ref:
          apiVersion: serving.knative.dev/v1
          kind: Service
          name: handler-b
```

## Knative Functions

### CLI Installation

```bash
# macOS
brew install knative/client/func

# Linux
curl -sL https://github.com/knative/func/releases/latest/download/func_linux_amd64 -o func
chmod +x func && sudo mv func /usr/local/bin/
```

### Function Lifecycle

```bash
# Create a new function
func create -l python my-function
cd my-function

# Build the function
func build

# Deploy to cluster
func deploy

# Invoke locally
func invoke

# Invoke remote
func invoke --target=remote
```

### Supported Languages

| Language | Template | Runtime |
|----------|----------|---------|
| Go | `go` | Native binary |
| Node.js | `node` | Node.js 18+ |
| Python | `python` | Python 3.9+ |
| Quarkus | `quarkus` | GraalVM/JVM |
| Rust | `rust` | Native binary |
| TypeScript | `typescript` | Node.js |

### Function Configuration (func.yaml)

```yaml
specVersion: 0.36.0
name: my-function
runtime: python
registry: docker.io/myuser
image: docker.io/myuser/my-function:latest
build:
  builder: pack
  buildpacks:
    - paketo-buildpacks/python
deploy:
  namespace: default
  annotations:
    autoscaling.knative.dev/min-scale: "1"
  env:
    - name: MY_VAR
      value: my-value
  volumes:
    - secret: my-secret
      path: /secrets
```

## Best Practices

### Resource Configuration

| Resource | Requirement | Notes |
|----------|-------------|-------|
| CPU requests | Required | Set based on actual usage |
| CPU limits | **FORBIDDEN** | Causes throttling |
| Memory requests | Required | Match your app needs |
| Memory limits | Required | Must equal requests |

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    memory: 128Mi  # Same as request
    # NO cpu limit!
```

### Probes Configuration

```yaml
spec:
  containers:
    - image: my-app
      readinessProbe:
        httpGet:
          path: /health
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 10
      # Liveness probe optional for serverless
      # (Knative handles pod lifecycle)
```

### Cold Start Optimization

1. **Keep minimum replicas**: Set `min-scale: "1"` for latency-critical services
2. **Optimize container image**: Use distroless/alpine base images
3. **Lazy initialization**: Defer heavy initialization until first request
4. **Connection pooling**: Pre-warm database connections

### Production Checklist

- [ ] Use KafkaChannel instead of InMemoryChannel
- [ ] Configure proper resource requests/limits
- [ ] Set up TLS with cert-manager
- [ ] Configure custom domain
- [ ] Set appropriate min/max scale values
- [ ] Enable dead letter sink for Triggers
- [ ] Configure monitoring (Prometheus metrics)
- [ ] Set up proper RBAC

## Troubleshooting

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Service not accessible | DNS not configured | Configure domain mapping or use sslip.io |
| Pods not scaling up | Activator overloaded | Increase activator replicas |
| Slow cold starts | Large image or slow init | Optimize image, use `min-scale: "1"` |
| Events not delivered | Broker misconfigured | Check Broker/Trigger status |
| 503 errors | Service scaling | Check activator logs, increase scale |
| Certificate errors | cert-manager issue | Check ClusterIssuer and Certificate status |

### Diagnostic Commands

```bash
# Check Knative Serving status
kubectl get ksvc -A
kubectl describe ksvc <service-name>

# Check revisions
kubectl get revisions -A
kubectl describe revision <revision-name>

# Check routes
kubectl get routes -A

# Check Knative Eventing status
kubectl get brokers -A
kubectl get triggers -A
kubectl get sources -A

# Check event delivery
kubectl get subscriptions -A

# View activator logs
kubectl logs -n knative-serving -l app=activator -c activator

# View controller logs
kubectl logs -n knative-serving -l app=controller

# Check networking layer (Kourier)
kubectl logs -n kourier-system -l app=3scale-kourier-gateway
```

### Debug Event Flow

```bash
# Deploy event-display service for debugging
kubectl apply -f - <<EOF
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: event-display
spec:
  template:
    spec:
      containers:
        - image: gcr.io/knative-releases/knative.dev/eventing/cmd/event_display
EOF

# Create a trigger to route all events
kubectl apply -f - <<EOF
apiVersion: eventing.knative.dev/v1
kind: Trigger
metadata:
  name: debug-trigger
spec:
  broker: default
  subscriber:
    ref:
      apiVersion: serving.knative.dev/v1
      kind: Service
      name: event-display
EOF

# Watch events
kubectl logs -l serving.knative.dev/service=event-display -c user-container -f
```

## Integration with ArgoCD

### ApplicationSet for Knative Services

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: knative-services
spec:
  generators:
    - git:
        repoURL: https://github.com/org/repo.git
        revision: HEAD
        directories:
          - path: knative-services/*
  template:
    metadata:
      name: '{{path.basename}}'
      annotations:
        # Disable SSA if using Jobs
        argocd.argoproj.io/compare-options: ServerSideDiff=false
    spec:
      project: default
      source:
        repoURL: https://github.com/org/repo.git
        targetRevision: HEAD
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: default
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### Health Checks for Knative Resources

ArgoCD automatically recognizes Knative resources. Custom health checks:

```yaml
# In argocd-cm ConfigMap
data:
  resource.customizations.health.serving.knative.dev_Service: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.conditions ~= nil then
        for _, condition in ipairs(obj.status.conditions) do
          if condition.type == "Ready" and condition.status == "True" then
            hs.status = "Healthy"
            hs.message = "Service is ready"
            return hs
          end
        end
      end
    end
    hs.status = "Progressing"
    hs.message = "Waiting for service to be ready"
    return hs
```

## References

- [Official Documentation](https://knative.dev/docs/)
- [Knative Serving API](https://knative.dev/docs/serving/spec/)
- [Knative Eventing API](https://knative.dev/docs/eventing/)
- [Knative Functions](https://knative.dev/docs/functions/)
- [GitHub Repository](https://github.com/knative)
- [Detailed Reference](references/knative-detail.md)
