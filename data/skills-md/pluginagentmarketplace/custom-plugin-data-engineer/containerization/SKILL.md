---
name: containerization
description: Docker, Kubernetes, container orchestration, and cloud-native deployment for data applications
sasmp_version: "1.3.0"
bonded_agent: 03-devops-engineer
bond_type: PRIMARY_BOND
skill_version: "2.0.0"
last_updated: "2025-01"
complexity: intermediate
estimated_mastery_hours: 120
prerequisites: [python-programming, cloud-platforms]
unlocks: [mlops, big-data]
---

# Containerization & Kubernetes

Production-grade container orchestration for data engineering workloads with Docker and Kubernetes.

## Quick Start

```dockerfile
# Dockerfile for PySpark data application
FROM python:3.12-slim

# Install Java for Spark
RUN apt-get update && apt-get install -y openjdk-17-jdk-headless && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

ENV PYTHONPATH=/app
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

ENTRYPOINT ["python", "-m", "src.main"]
```

## Core Concepts

### 1. Multi-Stage Builds

```dockerfile
# Build stage
FROM python:3.12 AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Runtime stage
FROM python:3.12-slim AS runtime

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY src/ /app/src/
WORKDIR /app

USER 1000
CMD ["python", "-m", "src.main"]
```

### 2. Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: etl-worker
  labels:
    app: etl-worker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: etl-worker
  template:
    metadata:
      labels:
        app: etl-worker
    spec:
      containers:
      - name: etl-worker
        image: company/etl-worker:v1.2.0
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: LOG_LEVEL
          value: "INFO"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: etl-worker
              topologyKey: kubernetes.io/hostname
```

### 3. Kubernetes CronJob for ETL

```yaml
# cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-etl
spec:
  schedule: "0 2 * * *"  # 2 AM daily
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      backoffLimit: 2
      activeDeadlineSeconds: 7200  # 2 hour timeout
      template:
        spec:
          restartPolicy: Never
          containers:
          - name: etl-job
            image: company/etl-pipeline:v1.0.0
            resources:
              requests:
                memory: "4Gi"
                cpu: "2000m"
              limits:
                memory: "8Gi"
                cpu: "4000m"
            env:
            - name: EXECUTION_DATE
              value: "{{ .Date }}"
            volumeMounts:
            - name: config
              mountPath: /app/config
              readOnly: true
          volumes:
          - name: config
            configMap:
              name: etl-config
```

### 4. Helm Chart Structure

```yaml
# Chart.yaml
apiVersion: v2
name: data-pipeline
version: 1.0.0
appVersion: "2.0.0"
description: Data pipeline Helm chart

# values.yaml
replicaCount: 3

image:
  repository: company/data-pipeline
  tag: "latest"
  pullPolicy: IfNotPresent

resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "4Gi"
    cpu: "2000m"

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

env:
  LOG_LEVEL: INFO
  BATCH_SIZE: "1000"

secrets:
  - name: DATABASE_URL
    secretName: db-credentials
    key: url
```

### 5. Docker Compose for Local Dev

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: datawarehouse
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  airflow-webserver:
    image: apache/airflow:2.8.0-python3.11
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    environment:
      AIRFLOW__CORE__EXECUTOR: CeleryExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://admin:${DB_PASSWORD}@postgres/datawarehouse
      AIRFLOW__CELERY__BROKER_URL: redis://redis:6379/0
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./plugins:/opt/airflow/plugins

volumes:
  postgres_data:
```

## Tools & Technologies

| Tool | Purpose | Version (2025) |
|------|---------|----------------|
| **Docker** | Containerization | 25+ |
| **Kubernetes** | Orchestration | 1.29+ |
| **Helm** | K8s package manager | 3.14+ |
| **ArgoCD** | GitOps deployment | 2.10+ |
| **Kustomize** | K8s config management | Built-in |
| **containerd** | Container runtime | 1.7+ |
| **Podman** | Docker alternative | 4.8+ |

## Troubleshooting Guide

| Issue | Symptoms | Root Cause | Fix |
|-------|----------|------------|-----|
| **OOMKilled** | Pod restarts, exit code 137 | Memory limit exceeded | Increase limits, optimize code |
| **CrashLoopBackOff** | Pod keeps restarting | App crash, bad config | Check logs: `kubectl logs pod` |
| **ImagePullBackOff** | Pod stuck in Pending | Image not found, auth | Check image name, pull secrets |
| **Pending Pod** | Pod won't schedule | No resources, node selector | Check resources, affinity rules |

### Debug Commands

```bash
# Check pod status and events
kubectl describe pod <pod-name>

# View container logs
kubectl logs <pod-name> -c <container-name> --previous

# Execute shell in container
kubectl exec -it <pod-name> -- /bin/sh

# Check resource usage
kubectl top pods

# Debug networking
kubectl run debug --image=busybox -it --rm -- sh
```

## Best Practices

```dockerfile
# ✅ DO: Use specific image tags
FROM python:3.12.1-slim

# ✅ DO: Use non-root user
USER 1000

# ✅ DO: Use multi-stage builds
# ✅ DO: Set resource limits
# ✅ DO: Use health checks

# ❌ DON'T: Run as root
# ❌ DON'T: Use latest tag
# ❌ DON'T: Store secrets in images
```

## Resources

- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [Helm Charts](https://helm.sh/docs/)

---

**Skill Certification Checklist:**
- [ ] Can write production Dockerfiles
- [ ] Can deploy applications to Kubernetes
- [ ] Can create Helm charts
- [ ] Can debug container issues
- [ ] Can implement health checks and probes
