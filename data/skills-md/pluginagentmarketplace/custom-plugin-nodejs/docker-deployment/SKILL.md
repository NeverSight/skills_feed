---
name: docker-deployment
description: Containerize and deploy Node.js applications with Docker including multi-stage builds, Docker Compose, and production optimization
sasmp_version: "1.3.0"
bonded_agent: 01-nodejs-fundamentals
bond_type: PRIMARY_BOND
---

# Docker Deployment Skill

Master containerizing and deploying Node.js applications with Docker for consistent, portable deployments.

## Quick Start

Dockerize Node.js app in 3 steps:
1. **Create Dockerfile** - Define container image
2. **Build Image** - `docker build -t myapp .`
3. **Run Container** - `docker run -p 3000:3000 myapp`

## Core Concepts

### Basic Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "src/index.js"]
```

### Multi-Stage Build (Optimized)
```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

USER nodejs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD node healthcheck.js || exit 1

CMD ["node", "src/index.js"]
```

## Learning Path

### Beginner (1-2 weeks)
- ✅ Understand Docker basics
- ✅ Create simple Dockerfile
- ✅ Build and run containers
- ✅ Manage volumes and networks

### Intermediate (3-4 weeks)
- ✅ Multi-stage builds
- ✅ Docker Compose
- ✅ Environment variables
- ✅ Health checks

### Advanced (5-6 weeks)
- ✅ Image optimization
- ✅ Production best practices
- ✅ Container orchestration
- ✅ CI/CD integration

## Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=myapp
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app

volumes:
  postgres-data:
  redis-data:
```

### Docker Compose Commands
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild images
docker-compose up -d --build

# Scale services
docker-compose up -d --scale app=3
```

## .dockerignore
```
node_modules
npm-debug.log
.git
.gitignore
.env
.env.local
.vscode
*.md
tests
coverage
.github
Dockerfile
docker-compose.yml
```

## Docker Commands
```bash
# Build image
docker build -t myapp:latest .

# Run container
docker run -d -p 3000:3000 --name myapp myapp:latest

# View logs
docker logs -f myapp

# Enter container
docker exec -it myapp sh

# Stop container
docker stop myapp

# Remove container
docker rm myapp

# List images
docker images

# Remove image
docker rmi myapp:latest

# Prune unused resources
docker system prune -a
```

## Environment Variables
```dockerfile
# In Dockerfile
ENV NODE_ENV=production
ENV PORT=3000

# Or in docker-compose.yml
environment:
  - NODE_ENV=production
  - PORT=3000

# Or from .env file
env_file:
  - .env.production
```

## Volumes for Persistence
```yaml
services:
  app:
    volumes:
      - ./logs:/app/logs              # Bind mount
      - node_modules:/app/node_modules # Named volume

volumes:
  node_modules:
```

## Health Checks
```dockerfile
# In Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD node healthcheck.js || exit 1
```

```javascript
// healthcheck.js
const http = require('http');

const options = {
  host: 'localhost',
  port: 3000,
  path: '/health',
  timeout: 2000
};

const request = http.request(options, (res) => {
  console.log(`STATUS: ${res.statusCode}`);
  process.exit(res.statusCode === 200 ? 0 : 1);
});

request.on('error', (err) => {
  console.log('ERROR:', err);
  process.exit(1);
});

request.end();
```

## Image Optimization
```dockerfile
# Use Alpine (smaller base image)
FROM node:18-alpine  # 180MB vs node:18 (1GB)

# Multi-stage build (remove build dependencies)
# Use .dockerignore (exclude unnecessary files)
# npm ci instead of npm install (faster, deterministic)
# Only production dependencies
RUN npm ci --only=production

# Combine RUN commands (fewer layers)
RUN apk add --no-cache git && \
    npm ci && \
    apk del git
```

## Production Best Practices
```dockerfile
FROM node:18-alpine

# Don't run as root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

COPY --chown=nodejs:nodejs package*.json ./
RUN npm ci --only=production

COPY --chown=nodejs:nodejs . .

USER nodejs

# Health check
HEALTHCHECK CMD node healthcheck.js || exit 1

# Use node instead of npm start (better signal handling)
CMD ["node", "src/index.js"]
```

## Docker Hub Deployment
```bash
# Login
docker login

# Tag image
docker tag myapp:latest username/myapp:1.0.0
docker tag myapp:latest username/myapp:latest

# Push to Docker Hub
docker push username/myapp:1.0.0
docker push username/myapp:latest

# Pull from Docker Hub
docker pull username/myapp:latest
```

## CI/CD with GitHub Actions
```yaml
name: Docker Build & Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: docker/setup-buildx-action@v2

      - uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - uses: docker/build-push-action@v4
        with:
          push: true
          tags: username/myapp:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Common Issues & Solutions

### Node modules caching
```dockerfile
# Cache node_modules layer
COPY package*.json ./
RUN npm ci
COPY . .  # This doesn't rebuild node_modules
```

### Signal handling
```dockerfile
# Use node directly (not npm)
CMD ["node", "src/index.js"]

# In app: Handle SIGTERM
process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
});
```

## When to Use

Use Docker deployment when:
- Need consistent environments (dev, staging, prod)
- Deploying microservices
- Want easy scaling and orchestration
- Using cloud platforms (AWS, GCP, Azure)
- Implementing CI/CD pipelines

## Related Skills
- Express REST API (containerize APIs)
- Database Integration (multi-container setup)
- Testing & Debugging (test in containers)
- Performance Optimization (optimize images)

## Resources
- [Docker Documentation](https://docs.docker.com)
- [Docker Compose](https://docs.docker.com/compose/)
- [Node.js Docker Best Practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)
