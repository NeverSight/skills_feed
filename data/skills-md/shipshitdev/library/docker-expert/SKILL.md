---
name: docker-expert
description: Expert in Docker, docker-compose, Dockerfile patterns, and container orchestration for NestJS and Next.js applications. Use this skill when users need Docker setup, containerization, or docker-compose configuration.
---

# Docker Expert

## Overview

This skill enables AI assistants to help with Docker containerization, docker-compose setups, and container orchestration for micro startup infrastructure.

## When to Use This Skill

This skill activates when users need:

- Dockerfile creation for NestJS/Next.js
- docker-compose configuration
- Container networking and volumes
- Multi-stage builds optimization
- Health checks and restart policies
- MongoDB/Redis container setup

## Dockerfile Best Practices

### NestJS Multi-Stage Build

```dockerfile
FROM node:20-alpine AS base
WORKDIR /app

FROM base AS deps
COPY package*.json ./
RUN npm ci

FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3001
CMD ["node", "dist/main.js"]
```

### Next.js Dockerfile

```dockerfile
FROM node:20-alpine AS base
WORKDIR /app

FROM base AS deps
COPY package*.json ./
RUN npm ci

FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
ENV NODE_ENV=production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
EXPOSE 3000
CMD ["npm", "start"]
```

## Docker Compose Patterns

### Development Setup

- Use volumes for live reload
- Mount source code
- Set restart: unless-stopped
- Configure networks

### Production Setup

- Use named volumes for persistence
- Set restart policies
- Configure health checks
- Use secrets management

### MongoDB with Docker Compose

```yaml
services:
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_ROOT_USERNAME}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
    volumes:
      - mongodb_data:/data/db
    networks:
      - app-network
    command: mongod --auth
```

## Health Checks

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3001/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Best Practices

- Use multi-stage builds to reduce image size
- Leverage layer caching
- Use .dockerignore
- Set appropriate restart policies
- Use health checks for containers
- Mount volumes for persistent data
- Use networks for service isolation
