---
name: dockerfile-basics
description: Learn Dockerfile fundamentals and best practices for building production-ready container images
sasmp_version: "1.3.0"
bonded_agent: 01-docker-fundamentals
bond_type: PRIMARY_BOND
---

# Dockerfile Basics Skill

Master Dockerfile fundamentals and 2024-2025 best practices for building secure, optimized container images.

## Purpose

Provide comprehensive guidance on Dockerfile syntax, instruction ordering, layer optimization, and security best practices.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| base_image | string | No | - | Base image to use |
| language | string | No | - | Programming language (node/python/go/java) |
| optimize | boolean | No | true | Apply optimization recommendations |

## Core Instructions

### Instruction Reference
| Instruction | Purpose | Example |
|-------------|---------|---------|
| FROM | Base image | `FROM node:20-alpine` |
| WORKDIR | Set working directory | `WORKDIR /app` |
| COPY | Copy files | `COPY package*.json ./` |
| RUN | Execute command | `RUN npm ci` |
| ENV | Set environment | `ENV NODE_ENV=production` |
| EXPOSE | Document port | `EXPOSE 3000` |
| USER | Set user | `USER appuser` |
| CMD | Default command | `CMD ["node", "app.js"]` |
| ENTRYPOINT | Fixed command | `ENTRYPOINT ["./start.sh"]` |
| HEALTHCHECK | Health check | `HEALTHCHECK CMD curl -f http://localhost/` |

### Layer Optimization Order
```dockerfile
# 1. Base image (most stable)
FROM node:20-alpine

# 2. System dependencies
RUN apk add --no-cache curl

# 3. Create user (security)
RUN addgroup -g 1001 app && adduser -u 1001 -G app -D app

# 4. Set working directory
WORKDIR /app

# 5. Copy dependency files (cache layer)
COPY package*.json ./

# 6. Install dependencies
RUN npm ci --only=production

# 7. Copy application code (most volatile)
COPY --chown=app:app . .

# 8. Switch to non-root user
USER app

# 9. Health check
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:3000/health || exit 1

# 10. Default command
CMD ["node", "server.js"]
```

## Best Practices (2024-2025)

### Security Essentials
```dockerfile
# Always use specific version tags
FROM node:20.10-alpine  # Good
# FROM node:latest      # Bad

# Run as non-root user
USER nonroot

# Use multi-stage builds
FROM node:20 AS builder
# ... build steps ...
FROM node:20-alpine AS runtime
COPY --from=builder /app/dist ./
```

### Optimization Techniques
```dockerfile
# Combine RUN commands
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Use .dockerignore
# node_modules, .git, *.md, etc.

# Leverage BuildKit cache mounts
RUN --mount=type=cache,target=/root/.npm npm ci
```

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `COPY failed: file not found` | File outside context | Check .dockerignore |
| `returned non-zero code: 127` | Command not found | Install package first |
| `permission denied` | Running as non-root | Use COPY --chown |

### Validation Commands
```bash
# Lint Dockerfile
hadolint Dockerfile

# Build with no cache
docker build --no-cache -t app:test .

# Inspect layers
docker history app:test
```

## Troubleshooting

### Debug Checklist
- [ ] .dockerignore excludes unnecessary files?
- [ ] Base image tag is specific (not :latest)?
- [ ] Dependencies copied before source code?
- [ ] Non-root user configured?
- [ ] HEALTHCHECK defined?

### Common Issues
| Symptom | Cause | Fix |
|---------|-------|-----|
| Large image size | No multi-stage | Add build stage |
| Slow builds | Poor layer order | Move COPY after dependencies |
| Security warnings | Root user | Add USER instruction |

## Usage

```
Skill("dockerfile-basics")
```

## Related Skills
- docker-multi-stage
- docker-optimization
- docker-security
