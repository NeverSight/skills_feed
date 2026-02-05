---
name: docker-best-practices
description: >-
  Docker containerization patterns for Python/React projects. Use when creating or
  modifying Dockerfiles, optimizing image size, setting up Docker Compose for local
  development, or hardening container security. Covers multi-stage builds for Python
  (python:3.12-slim) and React (node:20-alpine -> nginx:alpine), layer optimization,
  .dockerignore, non-root user, security scanning with Trivy, Docker Compose for
  dev (backend + frontend + PostgreSQL + Redis), and image tagging strategy.
  Does NOT cover deployment orchestration (use deployment-pipeline).
license: MIT
compatibility: 'Docker 24+, Docker Compose v2'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: deployment
allowed-tools: Read Edit Write Bash(docker:*)
context: fork
---

# Docker Best Practices

## When to Use

Activate this skill when:
- Creating a new Dockerfile for a Python backend or React frontend
- Optimizing existing Docker images for smaller size or faster builds
- Setting up Docker Compose for local development
- Configuring multi-stage builds to separate build and runtime dependencies
- Hardening container security (non-root user, minimal base images)
- Running security scans on Docker images with Trivy
- Designing an image tagging strategy for CI/CD pipelines
- Troubleshooting Docker build failures or runtime issues

Do NOT use this skill for:
- Deployment orchestration or CI/CD pipelines (use `deployment-pipeline`)
- Kubernetes configuration or Helm charts
- Cloud infrastructure provisioning (Terraform, CloudFormation)
- Application code patterns (use `python-backend-expert` or `react-frontend-expert`)

## Instructions

### Multi-Stage Build Strategy

Multi-stage builds keep final images small by separating build-time and runtime dependencies.

**Principle:** Build in a full image, run in a minimal image. Only copy what is needed for runtime.

```
┌──────────────────────────────────┐
│       Stage 1: Builder           │
│  Full SDK, build tools, deps     │
│  Compile, install, build         │
├──────────────────────────────────┤
│       Stage 2: Runtime           │
│  Minimal base image              │
│  COPY --from=builder artifacts   │
│  Non-root user, health check     │
└──────────────────────────────────┘
```

### Python Backend Dockerfile

See `references/python-dockerfile-template` for the complete template.

**Key decisions for Python:**

```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Why these choices:**
- `python:3.12-slim` instead of `alpine` -- avoids musl compatibility issues with binary wheels
- `--no-cache-dir` -- prevents pip cache from bloating the image
- `--prefix=/install` -- isolates installed packages for clean COPY
- `libpq5` at runtime, `libpq-dev` only at build -- minimizes runtime dependencies
- `curl` in runtime -- needed for HEALTHCHECK command

### React Frontend Dockerfile

See `references/react-dockerfile-template` for the complete template.

**Key decisions for React:**

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine AS runtime

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup && \
    chown -R appuser:appgroup /var/cache/nginx /var/log/nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && chown appuser:appgroup /var/run/nginx.pid

USER appuser
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -q --spider http://localhost:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

**Why these choices:**
- `node:20-alpine` for build -- smallest Node image, only needed at build time
- `nginx:alpine` for serving -- ~7MB base, production-grade static file server
- `npm ci` -- deterministic installs from lockfile, faster than `npm install`
- `--ignore-scripts` -- security measure, prevents running arbitrary scripts during install
- Final image has NO Node.js runtime -- only static files + Nginx

### Base Image Selection Guide

| Use Case | Base Image | Size | Notes |
|----------|-----------|------|-------|
| Python backend | `python:3.12-slim` | ~150MB | Best compatibility with binary wheels |
| Python backend (minimal) | `python:3.12-alpine` | ~50MB | May need musl workarounds for some packages |
| React build stage | `node:20-alpine` | ~130MB | Only used during build |
| React runtime | `nginx:alpine` | ~7MB | Production static file serving |
| Utility/scripts | `alpine:3.19` | ~5MB | For helper containers |

**Rules:**
1. Never use `latest` tag -- always pin major.minor version
2. Prefer `-slim` variants for Python (avoids musl issues)
3. Prefer `-alpine` variants for Node.js and Nginx (smaller images)
4. Update base images monthly for security patches

### Layer Optimization

Docker caches layers. Order instructions from least-changing to most-changing.

**Optimal layer order:**
```dockerfile
# 1. Base image (changes rarely)
FROM python:3.12-slim

# 2. System dependencies (changes monthly)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl && rm -rf /var/lib/apt/lists/*

# 3. Create user (changes never)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 4. Python dependencies (changes weekly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Application code (changes every commit)
COPY src/ ./src/

# 6. Runtime config (changes rarely)
USER appuser
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Common mistakes to avoid:**
```dockerfile
# BAD: Copying everything before installing dependencies (busts cache)
COPY . .
RUN pip install -r requirements.txt

# GOOD: Copy only requirements first, then install, then copy code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
```

**Minimize layers:**
```dockerfile
# BAD: Multiple RUN commands create multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# GOOD: Single RUN command, single layer, clean up in same layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*
```

### .dockerignore

Always include a `.dockerignore` to prevent unnecessary files from entering the build context.

```dockerignore
# Version control
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
.pytest_cache
.mypy_cache
.ruff_cache
*.egg-info
dist/
build/
.venv/
venv/

# Node
node_modules/
npm-debug.log*
.next/
coverage/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Docker
Dockerfile*
docker-compose*
.dockerignore

# Environment files
.env
.env.*
!.env.example

# Documentation
*.md
docs/
LICENSE

# CI/CD
.github/
.gitlab-ci.yml

# OS
.DS_Store
Thumbs.db
```

**Impact of .dockerignore:**
- Without it: Build context may be 500MB+ (node_modules, .git)
- With it: Build context typically 5-20MB
- Faster builds, no risk of leaking secrets from `.env` files

### Security Hardening

#### Non-Root User

Never run containers as root in production.

```dockerfile
# Create a dedicated user with no shell and no home directory
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /sbin/nologin appuser

# Set ownership of application files
COPY --chown=appuser:appuser src/ ./src/

# Switch to non-root user
USER appuser
```

#### Security Scanning with Trivy

Scan images for vulnerabilities before deployment.

```bash
# Install Trivy
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh

# Scan image for vulnerabilities
trivy image --severity HIGH,CRITICAL app-backend:latest

# Scan and fail if HIGH/CRITICAL vulnerabilities found
trivy image --exit-code 1 --severity HIGH,CRITICAL app-backend:latest

# Generate JSON report
trivy image --format json --output trivy-report.json app-backend:latest

# Scan Dockerfile for misconfigurations
trivy config Dockerfile
```

**Integrate into CI/CD:**
```yaml
- name: Trivy vulnerability scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'app-backend:${{ github.sha }}'
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'
```

#### Additional Security Measures

```dockerfile
# Read-only filesystem where possible
# (set at runtime with docker run --read-only)

# No new privileges
# (set at runtime with docker run --security-opt=no-new-privileges)

# Drop all capabilities, add only what is needed
# (set at runtime with docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE)

# Use COPY instead of ADD (ADD can auto-extract tarballs, security risk)
COPY requirements.txt .  # GOOD
# ADD requirements.txt .  # AVOID unless you need tar extraction
```

### Docker Compose for Local Development

See `references/docker-compose-template.yml` for the full template.

**Architecture:**
```
┌────────────┐    ┌────────────┐
│  Frontend  │    │  Backend   │
│ React:3000 │───>│ FastAPI:8000│
└────────────┘    └─────┬──────┘
                        │
                 ┌──────┴──────┐
                 │             │
            ┌────┴────┐  ┌────┴────┐
            │PostgreSQL│  │  Redis  │
            │  :5432   │  │  :6379  │
            └─────────┘  └─────────┘
```

**Key Compose features for development:**
```yaml
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
      target: builder  # Use builder stage for development (has dev tools)
    volumes:
      - ./src:/app/src  # Hot reload
    environment:
      - DEBUG=true
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app_dev
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8000:8000"

  frontend:
    build:
      context: ./frontend
      target: builder
    volumes:
      - ./frontend/src:/app/src  # Hot reload
    ports:
      - "3000:3000"

  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]

volumes:
  pgdata:
```

**Essential Compose patterns:**
- Use `depends_on` with `condition: service_healthy` for startup ordering
- Mount source code as volumes for hot reloading in development
- Use named volumes for database persistence
- Set `target: builder` to use the build stage with dev dependencies
- Define health checks for all infrastructure services

### Image Tagging Strategy

Use a consistent tagging strategy across all environments.

**Tag format:**
```
registry.example.com/app-backend:<tag>
```

**Tagging rules:**

| Tag | When | Example | Purpose |
|-----|------|---------|---------|
| `git-<sha>` | Every build | `git-a1b2c3d` | Immutable reference to exact code |
| `branch-<name>` | Every push | `branch-main` | Latest from branch (mutable) |
| `v<semver>` | Release | `v1.2.3` | Semantic version release |
| `latest` | Production deploy | `latest` | Current production (mutable) |
| `staging` | Staging deploy | `staging` | Current staging (mutable) |

**Implementation:**
```bash
# Build with git SHA tag (immutable)
GIT_SHA=$(git rev-parse --short HEAD)
docker build -t "app-backend:git-${GIT_SHA}" .

# Tag for the branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
docker tag "app-backend:git-${GIT_SHA}" "app-backend:branch-${BRANCH}"

# Tag for release
docker tag "app-backend:git-${GIT_SHA}" "app-backend:v1.2.3"

# Tag as latest for production
docker tag "app-backend:git-${GIT_SHA}" "app-backend:latest"
```

**Rules:**
1. Always tag with git SHA -- this is the immutable, traceable reference
2. Never deploy using `latest` tag -- always use the SHA tag
3. Use `latest` only as a convenience alias after a successful production deploy
4. Include build metadata in image labels

```dockerfile
# Add metadata labels
LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.revision="${GIT_SHA}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
```

### Quick Reference

```bash
# Build images
docker build -t app-backend:$(git rev-parse --short HEAD) -f Dockerfile.backend .
docker build -t app-frontend:$(git rev-parse --short HEAD) -f Dockerfile.frontend .

# Start local development
docker compose up -d && docker compose logs -f backend

# Scan for vulnerabilities
trivy image --severity HIGH,CRITICAL app-backend:latest

# Check image sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep app-

# Clean up
docker image prune -f
```
