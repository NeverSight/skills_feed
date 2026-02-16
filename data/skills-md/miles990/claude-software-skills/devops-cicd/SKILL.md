---
name: devops-cicd
description: CI/CD pipelines, infrastructure as code, and deployment strategies
domain: software-engineering
version: 1.0.0
tags: [ci, cd, github-actions, kubernetes, docker, terraform, gitops]
triggers:
  keywords:
    primary: [devops, ci, cd, cicd, pipeline, github actions, deployment, docker]
    secondary: [kubernetes, k8s, terraform, ansible, jenkins, gitlab ci, argocd, helm]
  context_boost: [automation, infrastructure, deploy, release]
  context_penalty: [frontend, design, ux]
  priority: high
---

# DevOps & CI/CD

## Overview

Practices for automating build, test, and deployment pipelines.

---

## CI/CD Pipeline

### Pipeline Stages

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Commit  │ → │  Build   │ → │   Test   │ → │  Deploy  │ → │ Release  │
│          │   │          │   │          │   │ Staging  │   │   Prod   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │              │              │
     │         ┌────┴────┐    ┌────┴────┐        │              │
     │         │ Compile │    │  Unit   │        │              │
     │         │  Lint   │    │  Integ  │        │              │
     │         │  Type   │    │   E2E   │        │              │
     │         └─────────┘    └─────────┘        │              │
     │                                           │              │
   Trigger                                    Manual?       Approval?
```

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Test
        run: npm run test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3

      - name: Build
        run: npm run build

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - name: Download build artifact
        uses: actions/download-artifact@v4
        with:
          name: build
          path: dist/

      - name: Deploy to staging
        run: |
          # Deploy script here
          echo "Deploying to staging..."

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com

    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
```

### Matrix Builds

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20, 22]
        exclude:
          - os: windows-latest
            node: 18

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
```

---

## Deployment Strategies

### Blue-Green Deployment

```
Before:
┌─────────────────────────────────────────┐
│           Load Balancer                  │
└─────────────────┬───────────────────────┘
                  │
          ┌───────┴───────┐
          ↓               ↓
    ┌───────────┐   ┌───────────┐
    │  Blue     │   │  Green    │
    │  (v1.0)   │   │  (idle)   │
    │  ACTIVE   │   │           │
    └───────────┘   └───────────┘

Deploy v1.1 to Green:
    ┌───────────┐   ┌───────────┐
    │  Blue     │   │  Green    │
    │  (v1.0)   │   │  (v1.1)   │
    │  ACTIVE   │   │  testing  │
    └───────────┘   └───────────┘

Switch traffic:
          ┌───────────────┐
          ↓               ↓
    ┌───────────┐   ┌───────────┐
    │  Blue     │   │  Green    │
    │  (v1.0)   │   │  (v1.1)   │
    │  standby  │   │  ACTIVE   │
    └───────────┘   └───────────┘
```

### Canary Deployment

```yaml
# Kubernetes canary with Argo Rollouts
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    canary:
      steps:
        - setWeight: 10        # 10% traffic to new version
        - pause: { duration: 5m }
        - setWeight: 30
        - pause: { duration: 5m }
        - setWeight: 50
        - pause: { duration: 10m }
        - setWeight: 100
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 2        # Start analysis at 30%
        args:
          - name: service-name
            value: my-app
```

### Rolling Update

```yaml
# Kubernetes rolling update
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Can exceed replicas by 1
      maxUnavailable: 0  # All must be available during update
  template:
    spec:
      containers:
        - name: app
          image: my-app:v1.1
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
```

---

## Infrastructure as Code

### Terraform

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

# Variables
variable "environment" {
  type    = string
  default = "production"
}

variable "instance_count" {
  type    = number
  default = 2
}

# Resources
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name        = "main-vpc"
    Environment = var.environment
  }
}

resource "aws_instance" "web" {
  count         = var.instance_count
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  vpc_security_group_ids = [aws_security_group.web.id]

  tags = {
    Name = "web-${count.index}"
  }
}

# Outputs
output "instance_ips" {
  value = aws_instance.web[*].public_ip
}
```

### Terraform Modules

```hcl
# modules/vpc/main.tf
variable "cidr_block" {
  type = string
}

variable "environment" {
  type = string
}

resource "aws_vpc" "this" {
  cidr_block = var.cidr_block
  tags = {
    Environment = var.environment
  }
}

output "vpc_id" {
  value = aws_vpc.this.id
}

# Using the module
module "vpc" {
  source      = "./modules/vpc"
  cidr_block  = "10.0.0.0/16"
  environment = "production"
}

resource "aws_subnet" "main" {
  vpc_id = module.vpc.vpc_id
  # ...
}
```

---

## Docker

### Dockerfile Best Practices

```dockerfile
# Use specific version tags
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy dependency files first (layer caching)
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage - smaller final image
FROM node:20-alpine AS production

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy from builder
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules

# Use non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1

# Run application
CMD ["node", "dist/index.js"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://postgres:password@db:5432/myapp
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## Kubernetes

### Basic Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: my-app:v1.0.0
          ports:
            - containerPort: 3000
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health/live
              port: 3000
            initialDelaySeconds: 3
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
---
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
```

### ConfigMaps and Secrets

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"

---
# secret.yaml (base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  database-url: cG9zdGdyZXM6Ly91c2VyOnBhc3NAaG9zdDo1NDMyL2Ri
```

---

## GitOps

### ArgoCD Application

```yaml
# application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/k8s-manifests.git
    targetRevision: HEAD
    path: apps/my-app/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

---

## Feature Flags

```typescript
// Using LaunchDarkly / Unleash pattern
interface FeatureFlags {
  newCheckoutFlow: boolean;
  betaFeatures: boolean;
  maxUploadSize: number;
}

class FeatureFlagService {
  constructor(private client: FeatureFlagClient) {}

  async isEnabled(flag: keyof FeatureFlags, user?: User): Promise<boolean> {
    return this.client.getBooleanValue(flag, false, {
      userId: user?.id,
      email: user?.email,
      groups: user?.groups
    });
  }
}

// Usage
if (await featureFlags.isEnabled('newCheckoutFlow', user)) {
  return <NewCheckoutFlow />;
} else {
  return <LegacyCheckout />;
}
```

---

## Related Skills

- [[testing-strategies]] - CI test integration
- [[reliability-engineering]] - Deployment reliability
- [[monitoring-observability]] - Deployment monitoring
