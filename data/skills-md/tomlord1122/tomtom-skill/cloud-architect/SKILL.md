---
name: cloud-architect
description: Cloud architecture expert for Kubernetes, Helm, Terraform, and AWS EKS. Use when designing cloud infrastructure, writing K8s manifests, creating Helm charts, or building Terraform modules.
---

# Cloud Architecture Expert

Expert assistant for Kubernetes deployments, Helm chart design, Terraform infrastructure as code, and AWS EKS configuration.

## How It Works

1. Analyzes infrastructure requirements
2. Designs according to cloud-native best practices
3. Provides deployable YAML/HCL code
4. Includes security and cost considerations
5. Generates validation commands

## Usage

### Validate Helm Chart

```bash
bash /mnt/skills/user/cloud-architect/scripts/validate-helm.sh [chart-path] [values-file] [kube-version]
```

**Arguments:**
- `chart-path` - Path to Helm chart directory (default: current directory)
- `values-file` - Custom values file for validation (optional)
- `kube-version` - Kubernetes version to validate against (default: 1.28.0)

**Examples:**
```bash
bash /mnt/skills/user/cloud-architect/scripts/validate-helm.sh ./my-chart
bash /mnt/skills/user/cloud-architect/scripts/validate-helm.sh ./my-chart values-prod.yaml 1.29.0
```

### Validate Terraform

```bash
bash /mnt/skills/user/cloud-architect/scripts/validate-terraform.sh [tf-dir] [check-format]
```

**Arguments:**
- `tf-dir` - Path to Terraform directory (default: current directory)
- `check-format` - Check formatting: true/false (default: true)

**Examples:**
```bash
bash /mnt/skills/user/cloud-architect/scripts/validate-terraform.sh
bash /mnt/skills/user/cloud-architect/scripts/validate-terraform.sh ./infrastructure false
```

## Documentation Resources

**Official Documentation:**
- Kubernetes: `https://kubernetes.io/docs/`
- Helm: `https://helm.sh/docs/`
- Terraform: `https://developer.hashicorp.com/terraform/docs`
- AWS EKS: `https://docs.aws.amazon.com/eks/`

## Architecture Principles

1. **Infrastructure as Code** - All resources trackable and reproducible
2. **GitOps** - Use ArgoCD/Flux for continuous deployment
3. **Least Privilege** - Minimal IAM permissions
4. **Multi-AZ** - High availability design
5. **Observability** - Logging, metrics, tracing from day one

## Kubernetes Patterns

### Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:v1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
```

## Helm Chart Structure

```
my-chart/
├── Chart.yaml
├── values.yaml
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   └── secrets.yaml
└── charts/
```

### values.yaml Pattern

```yaml
replicaCount: 3

image:
  repository: myapp
  tag: "v1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

## Terraform Module Structure

```
modules/
├── eks-cluster/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── versions.tf
├── networking/
│   ├── vpc.tf
│   ├── subnets.tf
│   └── security-groups.tf
└── iam/
    └── roles.tf
```

### EKS Module Example

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    default = {
      min_size     = 2
      max_size     = 10
      desired_size = 3
      instance_types = ["t3.medium"]
    }
  }
}
```

## Security Best Practices

- [ ] Use IRSA (IAM Roles for Service Accounts)
- [ ] Enable pod security standards
- [ ] Encrypt secrets with KMS
- [ ] Implement network policies
- [ ] Regular security scanning

## Present Results to User

When providing cloud architecture solutions:
- Provide complete, deployable code
- Include security configurations
- Estimate cost implications
- Provide validation commands
- Note version-specific features

## Troubleshooting

**"Pod stuck in Pending"**
- Check resource quotas: `kubectl describe node`
- Verify PVC availability
- Check node selectors/taints

**"Helm install fails"**
- Validate chart: `helm lint`
- Check values: `helm template . -f values.yaml`
- Verify RBAC permissions

**"Terraform state conflict"**
- Use remote state with locking
- Run `terraform init -reconfigure`
- Check for concurrent operations
