---
name: eksctl
description: This skill should be used when users need to manage AWS EKS clusters via eksctl CLI. It covers cluster creation, nodegroup management, addon operations, IAM integration, and cluster upgrades. Complements kubectl for cluster-level operations. Triggers on requests mentioning eksctl, EKS cluster management, nodegroups, EKS addons, or Kubernetes cluster infrastructure on AWS.
---

# eksctl Skill

This skill enables AWS EKS cluster management using the eksctl CLI tool.

## Environment

- **Region**: `us-east-1`
- **AWS Account**: 830101142436
- **eksctl Version**: 0.221.0

### Current Cluster

| Cluster | Region | Kubernetes Version |
|---------|--------|-------------------|
| `production` | us-east-1 | 1.34 |

## eksctl vs kubectl

| Tool | Purpose |
|------|---------|
| `eksctl` | Cluster infrastructure management (create/delete clusters, nodegroups, addons) |
| `kubectl` | Workload management (pods, deployments, services) |

Use eksctl for cluster-level operations; use kubectl for application-level operations.

## Common Operations

### Cluster Management

```bash
# List clusters
eksctl get cluster --region us-east-1

# Get cluster info
eksctl get cluster --name production --region us-east-1

# Update kubeconfig
eksctl utils write-kubeconfig --cluster production --region us-east-1

# Describe cluster stacks
eksctl utils describe-stacks --cluster production --region us-east-1
```

### Nodegroup Operations

```bash
# List nodegroups
eksctl get nodegroup --cluster production --region us-east-1

# Create nodegroup
eksctl create nodegroup \
  --cluster production \
  --region us-east-1 \
  --name <nodegroup-name> \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 4

# Scale nodegroup
eksctl scale nodegroup \
  --cluster production \
  --region us-east-1 \
  --name <nodegroup-name> \
  --nodes 3

# Delete nodegroup
eksctl delete nodegroup \
  --cluster production \
  --region us-east-1 \
  --name <nodegroup-name>

# Drain nodegroup (for upgrades)
eksctl drain nodegroup \
  --cluster production \
  --region us-east-1 \
  --name <nodegroup-name>
```

### Addon Management

```bash
# List addons
eksctl get addon --cluster production --region us-east-1

# Get addon details
eksctl get addon --cluster production --region us-east-1 --name <addon-name>

# Create addon
eksctl create addon \
  --cluster production \
  --region us-east-1 \
  --name <addon-name> \
  --version <version>

# Update addon
eksctl update addon \
  --cluster production \
  --region us-east-1 \
  --name <addon-name> \
  --version <new-version>

# Delete addon
eksctl delete addon \
  --cluster production \
  --region us-east-1 \
  --name <addon-name>
```

### Current Addons (production cluster)

| Addon | Version | Status |
|-------|---------|--------|
| adot | v0.141.0-eksbuild.1 | ACTIVE |
| amazon-cloudwatch-observability | v4.8.0-eksbuild.1 | ACTIVE |
| aws-efs-csi-driver | v2.1.15-eksbuild.1 | ACTIVE |
| aws-network-flow-monitoring-agent | v1.1.1-eksbuild.1 | ACTIVE |
| cert-manager | v1.19.2-eksbuild.1 | ACTIVE |
| eks-pod-identity-agent | v1.3.10-eksbuild.2 | ACTIVE |
| metrics-server | v0.8.0-eksbuild.6 | ACTIVE |

### IAM & OIDC

```bash
# Associate OIDC provider
eksctl utils associate-iam-oidc-provider \
  --cluster production \
  --region us-east-1 \
  --approve

# Create IAM service account
eksctl create iamserviceaccount \
  --cluster production \
  --region us-east-1 \
  --namespace <namespace> \
  --name <sa-name> \
  --attach-policy-arn <policy-arn> \
  --approve

# List IAM service accounts
eksctl get iamserviceaccount --cluster production --region us-east-1

# Delete IAM service account
eksctl delete iamserviceaccount \
  --cluster production \
  --region us-east-1 \
  --namespace <namespace> \
  --name <sa-name>
```

### Pod Identity Associations

```bash
# Create pod identity association
eksctl create podidentityassociation \
  --cluster production \
  --region us-east-1 \
  --namespace <namespace> \
  --service-account-name <sa-name> \
  --role-arn <role-arn>

# List pod identity associations
eksctl get podidentityassociation --cluster production --region us-east-1

# Delete pod identity association
eksctl delete podidentityassociation \
  --cluster production \
  --region us-east-1 \
  --namespace <namespace> \
  --service-account-name <sa-name>
```

### Cluster Upgrades

```bash
# Check available upgrades
eksctl upgrade cluster \
  --cluster production \
  --region us-east-1 \
  --dry-run

# Upgrade control plane
eksctl upgrade cluster \
  --cluster production \
  --region us-east-1 \
  --version <new-version> \
  --approve

# Upgrade nodegroup
eksctl upgrade nodegroup \
  --cluster production \
  --region us-east-1 \
  --name <nodegroup-name> \
  --kubernetes-version <new-version>
```

### Access Management

```bash
# Get access entries
eksctl get accessentry --cluster production --region us-east-1

# Create access entry
eksctl create accessentry \
  --cluster production \
  --region us-east-1 \
  --principal-arn <arn>

# Delete access entry
eksctl delete accessentry \
  --cluster production \
  --region us-east-1 \
  --principal-arn <arn>
```

### Fargate Profiles

```bash
# List Fargate profiles
eksctl get fargateprofile --cluster production --region us-east-1

# Create Fargate profile
eksctl create fargateprofile \
  --cluster production \
  --region us-east-1 \
  --name <profile-name> \
  --namespace <namespace>

# Delete Fargate profile
eksctl delete fargateprofile \
  --cluster production \
  --region us-east-1 \
  --name <profile-name>
```

## Cluster Creation (Reference)

For creating new clusters (typically done via Terraform in this project):

```bash
# Create cluster with config file
eksctl create cluster -f cluster-config.yaml

# Create cluster with CLI options
eksctl create cluster \
  --name <cluster-name> \
  --region us-east-1 \
  --version 1.34 \
  --nodegroup-name <ng-name> \
  --node-type t3.medium \
  --nodes 2 \
  --managed
```

## Output Formatting

```bash
# JSON output
eksctl get cluster --region us-east-1 -o json

# YAML output
eksctl get cluster --region us-east-1 -o yaml
```

## Troubleshooting

### Check CloudFormation Stacks

eksctl uses CloudFormation under the hood:

```bash
# Describe stacks
eksctl utils describe-stacks --cluster production --region us-east-1

# Check for stack issues
aws cloudformation describe-stack-events \
  --stack-name eksctl-production-cluster \
  --region us-east-1
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `No nodegroups found` | Nodegroups managed by Karpenter | Use `kubectl get nodepools` instead |
| `ResourceInUseException` | Resource being modified | Wait and retry |
| `AccessDenied` | Missing IAM permissions | Check IAM roles |

## Integration Notes

- **Karpenter**: This cluster uses Karpenter for node provisioning instead of managed nodegroups
- **kubectl**: Use kubectl skill for workload operations (k1 for production, k2 for staging)
- **ArgoCD/Kargo**: Use GitOps skills for application deployments
- **AWS CLI**: Use aws-cli skill for other AWS resource management
