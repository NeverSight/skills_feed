---
name: docker-security
description: Secure Docker containers and images with hardening, scanning, and secrets management
sasmp_version: "1.3.0"
bonded_agent: 06-docker-security
bond_type: PRIMARY_BOND
---

# Docker Security Skill

Master container security hardening, vulnerability scanning, and secrets management following CIS Docker Benchmark.

## Purpose

Implement security best practices for Docker containers and images including non-root users, capability dropping, and vulnerability scanning.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| image | string | No | - | Image to scan |
| severity | enum | No | HIGH | CRITICAL/HIGH/MEDIUM/LOW |
| compliance | string | No | CIS | CIS/NIST/SOC2 |

## Security Hardening

### Non-Root User (MANDATORY)
```dockerfile
# Create non-root user
RUN addgroup -g 1001 app && \
    adduser -u 1001 -G app -D app

# Set ownership
COPY --chown=app:app . /app

# Switch user
USER app
```

### Read-Only Filesystem
```bash
docker run --read-only \
  --tmpfs /tmp:rw,noexec,nosuid \
  myapp:latest
```

### Drop Capabilities
```bash
docker run \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  myapp:latest
```

### Complete Hardened Run
```bash
docker run \
  --security-opt no-new-privileges:true \
  --cap-drop ALL \
  --read-only \
  --user 1001:1001 \
  --pids-limit 100 \
  --memory 512m \
  myapp:latest
```

## Vulnerability Scanning

### Trivy
```bash
# Basic scan
trivy image myapp:latest

# Filter by severity
trivy image --severity CRITICAL,HIGH myapp:latest

# CI/CD integration (fail on critical)
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# JSON output
trivy image --format json --output report.json myapp:latest
```

### Docker Scout
```bash
# Quick scan
docker scout cves myapp:latest

# Detailed report
docker scout cves --format markdown myapp:latest
```

## Secrets Management

### Docker Compose Secrets
```yaml
services:
  database:
    image: postgres:16-alpine
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### BuildKit Secrets
```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm install
```

```bash
docker build --secret id=npmrc,src=.npmrc .
```

## Secure Dockerfile
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER nonroot
CMD ["dist/index.js"]
```

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `permission denied` | Non-root user | Fix file ownership |
| `read-only filesystem` | Read-only mode | Use tmpfs mounts |
| `operation not permitted` | Missing capability | Add specific cap |

### Fallback Strategy
1. Start without restrictions
2. Add security options incrementally
3. Test each restriction

## Troubleshooting

### Debug Checklist
- [ ] Running as non-root? `docker exec <c> id`
- [ ] Scanned for vulnerabilities?
- [ ] Capabilities dropped?
- [ ] Secrets not in env vars?

### CIS Benchmark
```bash
docker run --rm --net host --pid host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docker/docker-bench-security
```

## Usage

```
Skill("docker-security")
```

## Related Skills
- dockerfile-basics
- docker-production
