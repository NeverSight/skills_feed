---
name: devops
description: Provides comprehensive DevOps guidance including CI/CD pipeline design, infrastructure as code (Terraform, CloudFormation, Bicep), container orchestration (Docker, Kubernetes), deployment strategies (blue-green, canary, rolling), monitoring and observability, configuration management (Ansible, Chef, Puppet), and cloud platform automation (AWS, GCP, Azure). Produces deployment scripts, pipeline configurations, infrastructure code, and operational procedures. Use when designing CI/CD pipelines, automating infrastructure, containerizing applications, setting up monitoring, implementing deployment strategies, managing configurations, or when users mention DevOps, CI/CD, infrastructure automation, Kubernetes, Docker, Terraform, deployment, monitoring, or cloud operations.
---

# DevOps

## Core Capabilities

Provides expert guidance covering the entire software delivery lifecycle:

1. **CI/CD Pipeline Design** - Automated build, test, and deployment workflows
2. **Infrastructure as Code** - Cloud resource provisioning with Terraform, CloudFormation, Bicep
3. **Container Orchestration** - Docker and Kubernetes deployment patterns
4. **Deployment Strategies** - Blue-green, canary, and rolling deployments
5. **Monitoring & Observability** - Metrics, logging, alerting with Prometheus, Grafana, ELK
6. **Configuration Management** - Ansible, Chef, Puppet automation
7. **Security & Compliance** - DevSecOps practices and container security

## Best Practices

## CI/CD

- Keep pipelines fast (< 10 minutes for feedback)
- Fail fast with quick tests first
- Use pipeline as code (version controlled)
- Implement proper secret management
- Enable artifact caching and parallelize independent jobs

### Infrastructure as Code

- Use remote state with locking
- Create reusable modules and pin versions
- Always review plan before apply
- Implement proper tagging strategy
- Document resource dependencies

### Container Orchestration

- Set resource requests and limits
- Implement health checks (liveness/readiness probes)
- Use pod anti-affinity for high availability
- Enable horizontal pod autoscaling
- Implement proper logging and monitoring

### Deployment

- Use rolling updates with zero downtime
- Implement proper health checks and rollback capabilities
- Use canary/blue-green for critical applications
- Test thoroughly in staging environments
- Monitor post-deployment metrics

### Security

- Run containers as non-root with read-only root filesystems
- Scan images for vulnerabilities regularly
- Implement network policies and secrets management
- Enable pod security standards and least privilege access

### Monitoring

- Collect metrics using RED/USE methods
- Implement structured logging with meaningful alerts
- Create actionable dashboards and monitor SLIs/SLOs
- Set up distributed tracing for microservices

## Detailed References

Load reference files based on specific needs:

- **CI/CD Pipeline Design**: See [cicd-pipeline-design.md](references/cicd-pipeline-design.md) for:
  - GitHub Actions, GitLab CI, Jenkins pipeline examples
  - Automated build, test, deploy workflow patterns
  - Pipeline optimization and caching strategies

- **Infrastructure as Code**: See [infrastructure-as-code.md](references/infrastructure-as-code.md) for:
  - Terraform, CloudFormation, Bicep patterns
  - AWS, GCP, Azure resource provisioning
  - Module design and state management

- **Container Orchestration**: See [container-orchestration.md](references/container-orchestration.md) for:
  - Kubernetes manifests, Helm charts, Kustomize
  - Docker best practices and multi-stage builds
  - Service mesh and networking patterns

- **Deployment Strategies**: See [deployment-strategies.md](references/deployment-strategies.md) for:
  - Blue-green deployment implementation
  - Canary release patterns with traffic splitting
  - Rolling update strategies and rollback procedures

- **Monitoring & Observability**: See [monitoring-and-observability.md](references/monitoring-and-observability.md) for:
  - Prometheus, Grafana setup and configuration
  - ELK stack deployment and log aggregation
  - Alert rules, dashboards, and SLO definitions

- **Security Best Practices**: See [security-best-practices.md](references/security-best-practices.md) for:
  - DevSecOps pipeline integration
  - Container security scanning and hardening
  - Secret management and compliance validation

- **Configuration Management**: See [configuration-management.md](references/configuration-management.md) for:
  - Ansible playbooks, Chef recipes, Puppet manifests
  - Server configuration automation patterns
  - Infrastructure drift detection

- **Common Commands**: See [common-commands.md](references/common-commands.md) for:
  - Kubernetes kubectl command reference
  - Docker CLI operations
  - Terraform and cloud provider CLI commands

- **Troubleshooting**: See [troubleshooting-guide.md](references/troubleshooting-guide.md) for:
  - Common issues and resolution steps
  - Debugging techniques for containers and orchestration
  - Performance optimization strategies
