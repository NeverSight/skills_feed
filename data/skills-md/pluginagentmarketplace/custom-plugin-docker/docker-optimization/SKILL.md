---
name: docker-optimization
description: Optimize Docker images and containers for size, build speed, and runtime performance
sasmp_version: "1.3.0"
bonded_agent: 02-docker-images
bond_type: PRIMARY_BOND
---

# Docker Optimization Skill

Comprehensive optimization techniques for Docker images and containers covering size reduction, build caching, and runtime performance.

## Purpose

Reduce image size, improve build times, and optimize container performance using 2024-2025 industry best practices.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| target | enum | No | all | size/build/runtime/all |
| base_image | string | No | - | Current base image |
| current_size | string | No | - | Current image size |

## Optimization Strategies

### 1. Image Size Reduction

#### Base Image Selection
| Base | Size | Use Case |
|------|------|----------|
| scratch | 0 | Static Go/Rust binaries |
| distroless | 2-20MB | Production containers |
| alpine | 5MB | General purpose |
| slim | 80-150MB | When apt packages needed |
| full | 500MB+ | Development only |

```dockerfile
# Before: 1.2GB
FROM node:20

# After: 150MB (88% smaller)
FROM node:20-alpine
```

#### Layer Optimization
```dockerfile
# Bad: 3 layers, 150MB
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good: 1 layer, 50MB
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

#### Remove Unnecessary Files
```dockerfile
# Clean package manager cache
RUN npm cache clean --force
RUN pip cache purge
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Use .dockerignore
# node_modules, .git, *.md, tests/, docs/
```

### 2. Build Speed Optimization

#### Layer Caching Strategy
```dockerfile
# Dependencies first (rarely change)
COPY package*.json ./
RUN npm ci

# Source code last (frequently changes)
COPY . .
RUN npm run build
```

#### BuildKit Cache Mounts
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine

# Cache npm packages
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Cache pip packages
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

#### Parallel Multi-Stage
```dockerfile
# Parallel stages (BuildKit)
FROM node:20-alpine AS deps
COPY package*.json ./
RUN npm ci

FROM deps AS builder
COPY . .
RUN npm run build

FROM deps AS linter
COPY . .
RUN npm run lint
```

### 3. Runtime Performance

#### Resource Limits
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

#### Container Tuning
```bash
# Set memory limits
docker run --memory=512m --memory-swap=512m app

# CPU limits
docker run --cpus=1.5 app

# I/O limits
docker run --device-read-bps=/dev/sda:1mb app
```

## Optimization Checklist

### Size Checklist
- [ ] Using smallest viable base image?
- [ ] Multi-stage build implemented?
- [ ] Package manager cache cleaned?
- [ ] Dev dependencies excluded?
- [ ] .dockerignore configured?

### Build Speed Checklist
- [ ] Dependencies copied before code?
- [ ] BuildKit enabled?
- [ ] Cache mounts used?
- [ ] Parallel stages where possible?

### Runtime Checklist
- [ ] Resource limits set?
- [ ] Health checks configured?
- [ ] Non-root user?
- [ ] Read-only filesystem where possible?

## Analysis Tools

```bash
# Image size analysis
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Layer analysis
docker history <image> --format "{{.Size}}\t{{.CreatedBy}}"

# Deep dive analysis
dive <image>

# Build time analysis
DOCKER_BUILDKIT=1 docker build --progress=plain .
```

## Error Handling

### Common Issues
| Issue | Cause | Solution |
|-------|-------|----------|
| Large image | No multi-stage | Implement multi-stage |
| Slow builds | Poor layer order | Dependencies before code |
| Cache not working | Context changes | Use .dockerignore |
| OOM at runtime | No limits | Set memory limits |

## Troubleshooting

### Debug Checklist
- [ ] BuildKit enabled? (`DOCKER_BUILDKIT=1`)
- [ ] Cache being used? (Check build output)
- [ ] .dockerignore working? (Check context size)
- [ ] Layers optimized? (Run `dive`)

## Usage

```
Skill("docker-optimization")
```

## Related Skills
- docker-multi-stage
- dockerfile-basics
- docker-production
