---
name: platform
description: Use this skill when working on infrastructure, DevOps, CI/CD, Kubernetes, cloud deployment, observability, or cost optimization. Activates on mentions of Kubernetes, Docker, Terraform, Pulumi, OpenTofu, GitOps, Argo CD, Flux, CI/CD, GitHub Actions, observability, OpenTelemetry, Prometheus, Grafana, AWS, GCP, Azure, infrastructure as code, platform engineering, FinOps, or cloud costs.
---

# Platform Engineering

Build reliable, observable, cost-efficient infrastructure.

## Quick Reference

### The 2026 Platform Stack

| Layer         | Tool                   | Purpose                   |
| ------------- | ---------------------- | ------------------------- |
| IaC           | OpenTofu / Pulumi      | Infrastructure definition |
| GitOps        | Argo CD / Flux         | Continuous deployment     |
| Control Plane | Crossplane             | Kubernetes-native infra   |
| Observability | OpenTelemetry          | Unified telemetry         |
| Service Mesh  | Istio Ambient / Cilium | mTLS, traffic management  |
| Cost          | FinOps Framework       | Cloud optimization        |

### Infrastructure as Code

**OpenTofu** (Terraform-compatible, open-source):

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  tags = {
    Name        = "web-server"
    Environment = "production"
  }
}
```

**Pulumi** (Real programming languages):

```typescript
import * as aws from "@pulumi/aws";

const server = new aws.ec2.Instance("web", {
  ami: "ami-0c55b159cbfafe1f0",
  instanceType: "t3.micro",
  tags: { Name: "web-server" },
});

export const publicIp = server.publicIp;
```

### GitOps with Argo CD

```yaml
# Application manifest
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo
    targetRevision: HEAD
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Kubernetes Patterns

**Gateway API** (replacing Ingress):

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-route
spec:
  parentRefs:
    - name: main-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: api-service
          port: 8080
```

**Istio Ambient Mode** (sidecar-less service mesh):

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    istio.io/dataplane-mode: ambient # Enable ambient mesh
```

### OpenTelemetry Setup

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Initialize
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://collector:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Use
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("my-operation"):
    do_work()
```

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

      - name: Update manifests
        run: |
          cd k8s/overlays/production
          kustomize edit set image app=ghcr.io/${{ github.repository }}:${{ github.sha }}
          git commit -am "Deploy ${{ github.sha }}"
          git push
```

### FinOps Framework

**Phase 1: INFORM** (visibility)

- Tag everything: `team`, `environment`, `cost-center`
- Use cloud cost explorers
- Target: 95%+ cost allocation accuracy

**Phase 2: OPTIMIZE** (action)

- Rightsize instances (most are overprovisioned)
- Use spot/preemptible for stateless workloads
- Reserved instances for baseline capacity
- Target: 20-30% cost reduction

**Phase 3: OPERATE** (governance)

- Budget alerts at 80% threshold
- Cost metrics in CI/CD gates
- Regular FinOps reviews

### Security Baseline

```yaml
# Tetragon policy (eBPF runtime enforcement)
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: block-shell
spec:
  kprobes:
    - call: "sys_execve"
      selectors:
        - matchBinaries:
            - operator: "In"
              values: ["/bin/sh", "/bin/bash"]
          matchNamespaces:
            - namespace: production
      action: Block
```

## Agents

- **platform-engineer** - GitOps, IaC, Kubernetes, observability
- **data-engineer** - Pipelines, ETL, data infrastructure
- **finops-engineer** - Cloud cost optimization, FinOps framework

## Deep Dives

- [references/gitops-patterns.md](references/gitops-patterns.md)
- [references/kubernetes-gateway.md](references/kubernetes-gateway.md)
- [references/opentelemetry.md](references/opentelemetry.md)
- [references/finops-framework.md](references/finops-framework.md)

## Examples

- [examples/argo-cd-setup/](examples/argo-cd-setup/)
- [examples/pulumi-aws/](examples/pulumi-aws/)
- [examples/otel-stack/](examples/otel-stack/)
