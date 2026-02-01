---
name: docker
description: Dockerfile best practices, security hardening, multi-stage builds, and image optimization
---

## Docker Code Review Rules

### Base Images
- Pin base image to specific version (not `latest`)
- Use official images from trusted sources
- Prefer minimal images (`alpine`, `slim`, `distroless`)
- Regularly update base images for security patches

### Build Optimization
- Use multi-stage builds to reduce final image size
- Order instructions by change frequency (cache optimization)
- Combine `RUN` commands to reduce layers
- Use `.dockerignore` to exclude unnecessary files

### Security
- Run as non-root user (`USER` directive)
- Don't store secrets in image (use runtime injection)
- Don't use `--privileged` without justification
- Scan images for vulnerabilities
- Set `readonly` root filesystem where possible

### Health Checks
- Include `HEALTHCHECK` instruction
- Health check should verify app is actually working
- Set appropriate interval and timeout

### Instructions
- Use `COPY` instead of `ADD` (unless extracting archives)
- Set `WORKDIR` before `COPY`/`RUN`
- Use explicit `EXPOSE` for documentation
- Set meaningful `LABEL` metadata
- Validate `COPY`/`ADD` sources and use `.dockerignore` properly
- Use `.dockerignore` to exclude sensitive files and `node_modules`
- Explicitly set `SHELL` if bash/sh features are needed
- Set environment variables with `ENV` for configuration (not secrets)
- Clean up package manager caches after install (e.g., `apt-get clean`)
- Understand `ENTRYPOINT` vs `CMD`: use `ENTRYPOINT` for main command, `CMD` for default args
- Document container usage with OCI labels (`org.opencontainers.image.*`)

### Example Good Dockerfile Pattern
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Runtime stage
FROM node:20-alpine

# Add OCI labels for documentation
LABEL org.opencontainers.image.title="My App"
LABEL org.opencontainers.image.description="Production web application"
LABEL org.opencontainers.image.version="1.0.0"

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app

# Copy dependencies and app files
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Set environment variables (not secrets)
ENV NODE_ENV=production

USER appuser
EXPOSE 3000
HEALTHCHECK CMD wget -q --spider http://localhost:3000/health || exit 1

# Use ENTRYPOINT for main command, CMD for default args
ENTRYPOINT ["node"]
CMD ["server.js"]
```
