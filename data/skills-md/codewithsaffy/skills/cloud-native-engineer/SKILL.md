---
name: cloud-native-engineer
description: The definitive skill for building and deploying high-performance, distributed systems using Cloud Native standards (Dapr, Redis, Microservices). Use when a project requires professional-grade architecture, cross-service communication, elastic scaling, and sub-second agentic latency. Mandatory for flawless deployments on Kubernetes (Local or Cloud).
---

# Cloud Native Engineer (Master Skill)

This skill transforms Claude into an elite Cloud Native Architect capable of delivering production-ready distributed systems.

## Core Capabilities

1. **Strategic Domain Decomposition**: Logic for splitting any monolith into clear microservice boundaries.
2. **Standardized Dapr Infrastructure**: Reliable, ready-to-use configurations for Pub/Sub, State, and Jobs.
3. **Flawless K8s Orchestration**: Deterministic deployment workflows that avoid DNS, Auth, and Probe failures.
4. **Agentic Performance (Sub-Second)**: Engineering patterns for ultra-fast AI interactions.

## Workflows and Procedures

### 1. Architectural Planning
Analyze service boundaries and define the shared communication backbone.
- **Guidance**: [MICROSERVICES.md](references/microservices.md) (Domain splitting & Payload standards).

### 2. Infrastructure & Containerization
Build elite, secure, and lean images before rolling out the backbone.
- **Docker Best Practices**: [DOCKER_BEST_PRACTICES.md](references/docker_best_practices.md).
- **Backbone Setup**: [DAPR_CONFIG.md](references/dapr_config.md) (Redis-first Pub/Sub and State yaml).

### 3. Fail-Proof Deployment (Mandatory Sequence)
Follow the EXACT order of operations to ensure 100% success.
- **Deployment Guide**: [DEPLOYMENT_GUIDE.md](references/deployment_guide.md).
- **Manifest Standards**: [MANIFEST_STANDARDS.md](references/manifest_standards.md).

### 4. Automated Orchestration
Use the "Low Freedom" scripts to automate repetitive tasks.
- **Deploy Minikube**: [scripts/deploy_minikube.ps1](../scripts/deploy_minikube.ps1).
- **Verify Cluster**: [scripts/verify_cluster.ps1](../scripts/verify_cluster.ps1).

### 5. Diagnostic Excellence
Diagnose "Silent Failures" using the troubleshooting matrix.
- **Matrix**: [TROUBLESHOOTING.md](references/troubleshooting.md).

### 6. AI Acceleration (SaaS Specialty)
Implement the persistent MCP pattern for sub-second chatbot responses.
- **Reference**: [LATENCY_OPTIMIZATION.md](references/latency_optimization.md).

## Elite Checklist for Agents
- [ ] **Network-Parity**: Internal calls use K8s service names (`http://service:port`).
- [ ] **Probe-Resilience**: Liveness probes have enough delay for sidecar startup.
- [ ] **Cluster-Auth**: `JWKS_URL` points to the internal ingress/service.
- [ ] **Warm-Start**: AI Tools are pre-initialized in the application lifespan.
