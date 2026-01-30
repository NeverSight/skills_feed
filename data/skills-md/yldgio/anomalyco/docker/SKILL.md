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

### Example Good Dockerfile Pattern
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Runtime stage
FROM node:20-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER appuser
EXPOSE 3000
HEALTHCHECK CMD wget -q --spider http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
```
