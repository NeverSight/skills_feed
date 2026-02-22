---
name: docker-multi-stage
description: Multi-stage builds for optimized, minimal production images with build/runtime separation
sasmp_version: "1.3.0"
bonded_agent: 02-docker-images
bond_type: SECONDARY_BOND
---

# Docker Multi-Stage Builds Skill

Create optimized, minimal production images using multi-stage builds with language-specific patterns.

## Purpose

Reduce image size by 50-90% by separating build dependencies from runtime, following 2024-2025 best practices.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| language | enum | Yes | - | node/python/go/rust/java |
| target | string | No | runtime | Build target stage |
| base_runtime | string | No | - | Custom runtime base image |

## Multi-Stage Patterns

### Node.js (Alpine + Distroless)
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

# Runtime stage (distroless = minimal attack surface)
FROM gcr.io/distroless/nodejs20-debian12 AS runtime
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER nonroot
CMD ["dist/index.js"]
```

### Python (Slim + Virtual Environment)
```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . .
USER nobody
CMD ["python", "main.py"]
```

### Go (Scratch = Smallest Possible)
```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server

# Runtime stage (scratch = 0 base size)
FROM scratch AS runtime
COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 65534
ENTRYPOINT ["/server"]
```

### Rust (Musl for Static Linking)
```dockerfile
# Build stage
FROM rust:1.75-alpine AS builder
RUN apk add --no-cache musl-dev
WORKDIR /app
COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl

# Runtime stage
FROM scratch AS runtime
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/app /app
USER 65534
ENTRYPOINT ["/app"]
```

### Java (JRE Only Runtime)
```dockerfile
# Build stage
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY . .
RUN ./gradlew build --no-daemon

# Runtime stage (JRE only, not JDK)
FROM eclipse-temurin:21-jre-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar
USER nobody
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Size Comparison

| Language | Before | After | Reduction |
|----------|--------|-------|-----------|
| Node.js | 1.2GB | 150MB | 87% |
| Python | 900MB | 120MB | 87% |
| Go | 800MB | 10MB | 99% |
| Rust | 1.5GB | 5MB | 99.7% |
| Java | 600MB | 200MB | 67% |

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `COPY --from failed` | Stage not found | Check stage name |
| `not found` at runtime | Missing libs | Use alpine, not scratch |
| `permission denied` | Non-root user | COPY --chown |

### Fallback Strategy
1. Start with alpine instead of scratch/distroless
2. Add required libraries incrementally
3. Use `ldd` to identify missing dependencies

## Troubleshooting

### Debug Checklist
- [ ] All required files copied to runtime stage?
- [ ] SSL certificates included for HTTPS?
- [ ] User/group exists in runtime image?
- [ ] Build artifacts correctly located?

### Debug Commands
```bash
# Check final image size
docker images myapp:latest

# Inspect layers
docker history myapp:latest --no-trunc

# Compare with baseline
dive myapp:latest
```

## Usage

```
Skill("docker-multi-stage")
```

## Assets
- `assets/Dockerfile.node-multistage` - Node.js template
- `assets/Dockerfile.python-multistage` - Python template

## Related Skills
- docker-optimization
- dockerfile-basics
