---
name: faion-cicd-engineer
description: "CI/CD: GitHub Actions, GitLab CI, Jenkins, ArgoCD, GitOps, monitoring."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# CI/CD Engineer Sub-Skill

**Communication: User's language. Config/code: English.**

## Purpose

Manages CI/CD pipelines, monitoring, observability, security, and operational excellence. Covers GitHub Actions, GitLab CI, Jenkins, ArgoCD, GitOps, Prometheus, Grafana, and modern DevOps practices.

---

## Quick Decision Tree

| If you need... | Use | File |
|---------------|-----|------|
| **CI/CD** |
| GitHub Actions | github-actions-basics, github-actions-workflows | github-actions-basics.md |
| GitLab CI | gitlab-cicd | gitlab-cicd.md |
| Jenkins | jenkins-basics, jenkins-pipeline-patterns | jenkins-basics.md |
| GitOps | gitops, argocd-gitops | argocd-gitops.md |
| **Monitoring & Observability** |
| Metrics | prometheus-monitoring | prometheus-monitoring.md |
| Dashboards | grafana-basics, grafana-setup | grafana-basics.md |
| Logs | elk-stack-logging | elk-stack-logging.md |
| AIOps | aiops | aiops.md |
| **Security & Operations** |
| Secrets | secrets-management | secrets-management.md |
| SSL/TLS | ssl-tls-setup | ssl-tls-setup.md |
| Security as Code | security-as-code | security-as-code.md |
| Nginx | nginx-configuration | nginx-configuration.md |
| Load balancing | load-balancing-concepts, load-balancing-implementation | load-balancing-concepts.md |
| **Backup & Cost** |
| Backups | backup-basics, backup-implementation | backup-basics.md |
| Cost optimization | finops, finops-cloud-cost-optimization | finops.md |
| **Modern Practices** |
| Platform Engineering | platform-engineering | platform-engineering.md |
| DORA metrics | dora-metrics | dora-metrics.md |
| **Azure** |
| Azure compute | azure-compute | azure-compute.md |
| Azure networking | azure-networking | azure-networking.md |
| **Optimization** |
| Docker optimization | docker-optimization | docker-optimization.md |
| Docker Compose ref | ref-docker-compose | ref-docker-compose.md |

---

## Methodologies (28)

### CI/CD & GitOps (7)
- github-actions-basics
- github-actions-workflows
- gitlab-cicd
- jenkins-basics
- jenkins-pipeline-patterns
- gitops
- argocd-gitops

### Monitoring & Observability (5)
- prometheus-monitoring
- grafana-basics
- grafana-setup
- elk-stack-logging
- aiops

### Security & Operations (5)
- secrets-management
- ssl-tls-setup
- security-as-code
- nginx-configuration
- load-balancing-concepts
- load-balancing-implementation

### Backup & Cost (4)
- backup-basics
- backup-implementation
- finops
- finops-cloud-cost-optimization

### Modern Practices (2)
- platform-engineering
- dora-metrics

### Azure (2)
- azure-compute
- azure-networking

### Optimization (3)
- docker-optimization
- ref-docker-compose

---

## Common Workflows

### CI/CD Pipeline Setup
```
1. Choose platform (GitHub/GitLab/Jenkins)
2. Define pipeline stages
3. Configure triggers
4. Add tests and quality gates
5. Setup deployments
6. Configure notifications
```

### Monitoring Stack
```
1. Deploy Prometheus
2. Configure exporters
3. Create Grafana dashboards
4. Setup alerting rules
5. Configure log aggregation
6. Test alert routing
```

### GitOps Deployment
```
1. Setup ArgoCD/Flux
2. Create Git repo structure
3. Define K8s manifests
4. Configure sync policies
5. Monitor deployments
6. Rollback if needed
```

---

## Observability Triad

| Pillar | Tools | Files |
|--------|-------|-------|
| Metrics | Prometheus, Grafana | prometheus-monitoring.md, grafana-*.md |
| Logs | ELK, Loki | elk-stack-logging.md |
| Traces | Jaeger, Tempo | (use with monitoring stack) |

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-devops-engineer | Parent skill |
| faion-infrastructure-engineer | Sibling (infrastructure and cloud) |

---

*CI/CD Engineer Sub-Skill v1.0*
*28 Methodologies | CI/CD, Monitoring, Security, GitOps*
