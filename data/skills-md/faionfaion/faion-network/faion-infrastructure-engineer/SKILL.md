---
name: faion-infrastructure-engineer
description: "Infrastructure: Docker, Kubernetes, Terraform, AWS/GCP, IaC, containerization."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Infrastructure Engineer Sub-Skill

**Communication: User's language. Config/code: English.**

## Purpose

Manages infrastructure provisioning, containerization, orchestration, and cloud platforms. Covers Docker, Kubernetes, Terraform, AWS, GCP, and IaC patterns.

---

## Quick Decision Tree

| If you need... | Use | File |
|---------------|-----|------|
| **Containerization** |
| Single service Dockerfile | docker-containerization | docker-containerization.md |
| Multi-service local dev | docker-compose | docker-compose.md |
| Dockerfile patterns | dockerfile-patterns | dockerfile-patterns.md |
| **Kubernetes** |
| K8s basics | k8s-basics | k8s-basics.md |
| K8s resources | k8s-resources | k8s-resources.md |
| K8s deployment | kubernetes-deployment | kubernetes-deployment.md |
| Helm charts | helm-basics, helm-advanced | helm-basics.md |
| **Infrastructure as Code** |
| Terraform basics | terraform-basics | terraform-basics.md |
| Terraform modules | terraform-modules | terraform-modules.md |
| Terraform state | terraform-state | terraform-state.md |
| IaC patterns | iac-basics, iac-patterns | iac-basics.md |
| **AWS** |
| AWS foundations | aws-architecture-foundations | aws-architecture-foundations.md |
| AWS services | aws-architecture-services | aws-architecture-services.md |
| EC2/ECS | aws-ec2-ecs | aws-ec2-ecs.md |
| Lambda | aws-lambda | aws-lambda.md |
| S3/Storage | aws-s3-storage | aws-s3-storage.md |
| Networking | aws-networking | aws-networking.md |
| **GCP** |
| GCP basics | gcp-arch-basics | gcp-arch-basics.md |
| GCP patterns | gcp-arch-patterns | gcp-arch-patterns.md |
| Compute/GKE | gcp-compute | gcp-compute.md |
| Cloud Run | gcp-cloud-run | gcp-cloud-run.md |
| Storage | gcp-storage | gcp-storage.md |
| Networking | gcp-networking | gcp-networking.md |

---

## Methodologies (30)

### Docker (6)
- docker-basics
- docker-compose
- docker-containerization
- dockerfile-patterns
- docker (reference)

### Kubernetes (6)
- k8s-basics
- k8s-resources
- kubernetes-deployment
- helm-basics
- helm-advanced

### Terraform & IaC (6)
- terraform-basics
- terraform-modules
- terraform-state
- terraform (reference)
- iac-basics
- iac-patterns

### AWS (7)
- aws (reference)
- aws-architecture-foundations
- aws-architecture-services
- aws-ec2-ecs
- aws-lambda
- aws-s3-storage
- aws-networking

### GCP (6)
- gcp (reference)
- gcp-arch-basics
- gcp-arch-patterns
- gcp-compute
- gcp-cloud-run
- gcp-storage
- gcp-networking

---

## Common Workflows

### Container Deployment
```
1. Write Dockerfile
2. Build and test locally
3. Push to registry
4. Update K8s manifests
5. Apply to cluster
6. Verify deployment
```

### Infrastructure Provisioning
```
1. Create feature branch
2. Write Terraform code
3. Run terraform plan
4. Review plan output
5. Create PR
6. Apply after approval
7. Verify resources
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-devops-engineer | Parent skill |
| faion-cicd-engineer | Sibling (CI/CD and monitoring) |

---

*Infrastructure Engineer Sub-Skill v1.0*
*30 Methodologies | Docker, K8s, Terraform, AWS, GCP*
