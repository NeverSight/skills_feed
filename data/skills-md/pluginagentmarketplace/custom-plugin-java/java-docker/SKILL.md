---
name: java-docker
description: Containerize Java applications - Dockerfile optimization, JVM settings, security
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 08-java-devops
bond_type: PRIMARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# Parameter Validation
parameters:
  base_image:
    type: string
    enum: [temurin, distroless, alpine]
    description: Base image type
  java_version:
    type: string
    default: "21"
    description: Java version
---

# Java Docker Skill

Containerize Java applications with optimized Dockerfiles and JVM settings.

## Overview

This skill covers Docker best practices for Java including multi-stage builds, JVM container settings, security hardening, and layer optimization.

## When to Use This Skill

Use when you need to:
- Create optimized Java Dockerfiles
- Configure JVM for containers
- Implement security best practices
- Reduce image size
- Set up health checks

## Topics Covered

### Dockerfile Optimization
- Multi-stage builds
- Layer caching strategy
- Spring Boot layered JARs
- Dependency caching

### JVM Container Settings
- UseContainerSupport
- MaxRAMPercentage
- GC selection
- Exit on OOM

### Security
- Non-root users
- Read-only filesystem
- Vulnerability scanning
- Secrets handling

## Quick Reference

```dockerfile
# Multi-stage optimized Dockerfile
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

# Cache dependencies
COPY pom.xml .
COPY .mvn .mvn
RUN mvn dependency:go-offline -B

# Build and extract layers
COPY src ./src
RUN mvn package -DskipTests && \
    java -Djarmode=layertools -jar target/*.jar extract

# Runtime stage
FROM eclipse-temurin:21-jre-alpine

# Security: non-root user
RUN addgroup -S app && adduser -S app -G app
USER app

WORKDIR /app

# Copy layers in order of change frequency
COPY --from=builder /app/dependencies/ ./
COPY --from=builder /app/spring-boot-loader/ ./
COPY --from=builder /app/snapshot-dependencies/ ./
COPY --from=builder /app/application/ ./

# JVM container settings
ENV JAVA_OPTS="-XX:+UseContainerSupport \
    -XX:MaxRAMPercentage=75.0 \
    -XX:+ExitOnOutOfMemoryError \
    -XX:+UseG1GC"

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=30s \
    CMD wget -qO- http://localhost:8080/actuator/health/liveness || exit 1

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS org.springframework.boot.loader.launch.JarLauncher"]
```

## JVM Container Flags

```bash
# Recommended production settings
JAVA_OPTS="
  -XX:+UseContainerSupport
  -XX:MaxRAMPercentage=75.0
  -XX:InitialRAMPercentage=50.0
  -XX:+ExitOnOutOfMemoryError
  -XX:+HeapDumpOnOutOfMemoryError
  -XX:HeapDumpPath=/tmp/heapdump.hprof
  -XX:+UseG1GC
  -Djava.security.egd=file:/dev/./urandom
"
```

## Base Image Comparison

| Image | Size | Security | Use Case |
|-------|------|----------|----------|
| temurin:21-jre | ~200MB | Good | General use |
| temurin:21-jre-alpine | ~100MB | Good | Size-optimized |
| distroless/java21 | ~80MB | Best | Production |

## Security Best Practices

```dockerfile
# Non-root user
RUN addgroup -S app && adduser -S app -G app
USER app

# Read-only filesystem
# (Configure at runtime with --read-only)

# No shell access with distroless
FROM gcr.io/distroless/java21-debian12

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget -qO- localhost:8080/actuator/health || exit 1
```

## Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| OOMKilled | Heap > limit | Set MaxRAMPercentage |
| Slow startup | Large image | Multi-stage build |
| Permission denied | Root required | Fix file permissions |
| No memory info | Old JVM | Update to Java 11+ |

### Debug Checklist
```
□ Check container memory limits
□ Verify JVM sees container limits
□ Review health check configuration
□ Scan image for vulnerabilities
□ Test with resource constraints
```

## Usage

```
Skill("java-docker")
```

## Related Skills
- `java-maven-gradle` - Build integration
- `java-microservices` - K8s deployment
