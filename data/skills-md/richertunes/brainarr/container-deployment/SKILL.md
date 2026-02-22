---
name: container-deployment
description: Manage containerization and deployment automation using Docker, Kubernetes, and cloud platforms. Use when working with Docker images, container registries, orchestration, deployment pipelines, infrastructure as code, or environment management. Handles container builds, registry publishing, and deployment strategies.
---

# Container & Deployment Engineer

## Mission
Design and implement containerization and deployment automation for Brainarr, enabling easy distribution, deployment, and scaling across diverse environments.

## Expertise Areas

### 1. Docker Containerization
- Create optimized Dockerfiles for plugins
- Build multi-stage Docker images
- Implement layer caching strategies
- Manage container image sizes
- Handle .NET runtime containers

### 2. Container Registry Management
- Publish to GitHub Container Registry (GHCR)
- Manage Docker Hub repositories
- Implement image tagging strategies
- Handle multi-architecture images
- Manage registry authentication

### 3. Deployment Automation
- Create deployment pipelines
- Implement blue-green deployments
- Handle zero-downtime deployments
- Implement rollback strategies
- Manage environment-specific configs

### 4. Kubernetes Orchestration
- Create Kubernetes manifests
- Design Helm charts
- Implement service deployments
- Handle ConfigMaps and Secrets
- Manage persistent volumes

### 5. Infrastructure as Code
- Write Terraform configurations
- Create CloudFormation templates
- Implement Ansible playbooks
- Design docker-compose files
- Manage environment provisioning

## Current Project Context

### Brainarr Infrastructure Status
- **Containerization**: ❌ No Docker images published
- **Existing Docker Usage**: ✅ Uses Docker to extract Lidarr assemblies
- **Deployment**: ⚠️ Manual installation only
- **Orchestration**: ❌ No Kubernetes/Helm charts
- **IaC**: ⚠️ Examples exist in documentation but not CI-integrated

### Existing Docker References
- `.github/workflows/ci.yml` - Extracts from `ghcr.io/hotio/lidarr:pr-plugins-3.1.2.4913`
- `docs/deployment/` - Docker Compose examples (not automated)
- `docs/deployment/` - Dockerfile examples (not automated)

### Enhancement Opportunities
1. **Publish Pre-packaged Images**: Lidarr + Brainarr combined image
2. **Plugin-only Image**: Lightweight plugin distribution
3. **Multi-arch Support**: amd64, arm64, arm/v7
4. **Registry Publishing**: GHCR automated in release workflow
5. **Helm Chart**: Kubernetes deployment automation

## Best Practices

### Docker Image Design

#### Option 1: Pre-packaged Lidarr + Brainarr
```dockerfile
FROM ghcr.io/hotio/lidarr:pr-plugins-3.1.2.4913

LABEL org.opencontainers.image.source="https://github.com/RicherTunes/brainarr"
LABEL org.opencontainers.image.description="Lidarr with Brainarr AI plugin pre-installed"
LABEL org.opencontainers.image.licenses="MIT"

# Copy plugin files
COPY --chown=hotio:hotio artifacts/plugin/ /config/plugins/RicherTunes/Brainarr/

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8686/ping || exit 1

EXPOSE 8686

ENTRYPOINT ["/init"]
```

Benefits:
- One-command deployment
- No manual plugin installation
- Consistent versions
- Easy upgrades

#### Option 2: Plugin-only Sidecar
```dockerfile
FROM alpine:latest

LABEL org.opencontainers.image.source="https://github.com/RicherTunes/brainarr"
LABEL org.opencontainers.image.description="Brainarr plugin files for mounting into Lidarr"

# Create plugin directory structure
RUN mkdir -p /plugin/RicherTunes/Brainarr

# Copy plugin artifacts
COPY artifacts/plugin/ /plugin/RicherTunes/Brainarr/

# Create volume for mounting
VOLUME ["/plugin"]

# Use scratch base for minimal size
FROM scratch
COPY --from=0 /plugin /plugin
VOLUME ["/plugin"]
```

Benefits:
- Minimal image size
- Volume mount approach
- Independent updates
- Flexible deployment

### Multi-Architecture Builds
```yaml
# In .github/workflows/release.yml
- name: Build and push multi-arch image
  uses: docker/build-push-action@v5
  with:
    context: .
    platforms: linux/amd64,linux/arm64,linux/arm/v7
    push: true
    tags: |
      ghcr.io/richertunes/brainarr:${{ env.VERSION }}
      ghcr.io/richertunes/brainarr:latest
```

### Image Tagging Strategy
- `latest` - Latest stable release
- `v1.3.1` - Specific version
- `v1.3` - Minor version track
- `v1` - Major version track
- `develop` - Development branch
- `pr-123` - Pull request builds
- `sha-abc123` - Commit SHA builds

### Docker Compose for Development
```yaml
version: '3.9'

services:
  lidarr:
    image: ghcr.io/richertunes/lidarr-brainarr:latest
    container_name: lidarr-brainarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - BRAINARR_API_KEY=${BRAINARR_API_KEY}
    volumes:
      - ./config:/config
      - ./music:/music
      - ./downloads:/downloads
    ports:
      - "8686:8686"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8686/ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lidarr-brainarr
  labels:
    app: lidarr
    plugin: brainarr
spec:
  replicas: 1
  selector:
    matchLabels:
      app: lidarr
  template:
    metadata:
      labels:
        app: lidarr
    spec:
      containers:
      - name: lidarr
        image: ghcr.io/richertunes/lidarr-brainarr:v1.3.1
        ports:
        - containerPort: 8686
        env:
        - name: PUID
          value: "1000"
        - name: PGID
          value: "1000"
        volumeMounts:
        - name: config
          mountPath: /config
        - name: music
          mountPath: /music
        livenessProbe:
          httpGet:
            path: /ping
            port: 8686
          initialDelaySeconds: 60
          periodSeconds: 30
      volumes:
      - name: config
        persistentVolumeClaim:
          claimName: lidarr-config
      - name: music
        persistentVolumeClaim:
          claimName: music-library
```

### Helm Chart Structure
```
helm/brainarr/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   └── secret.yaml
└── README.md
```

## Deployment Strategies

### Blue-Green Deployment
1. Deploy new version (green) alongside current (blue)
2. Run health checks on green
3. Switch traffic from blue to green
4. Keep blue running for quick rollback
5. Decommission blue after validation period

### Canary Deployment
1. Deploy new version to subset of instances (10%)
2. Monitor metrics and error rates
3. Gradually increase traffic (25%, 50%, 100%)
4. Rollback if issues detected
5. Full rollout when stable

### Rolling Deployment
1. Update instances one at a time
2. Health check before proceeding to next
3. Maintain service availability throughout
4. Automatic rollback on failures

## CI/CD Integration

### GitHub Actions Container Workflow
```yaml
name: Container Build and Publish

on:
  push:
    tags:
      - 'v*.*.*'
  workflow_dispatch:

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ghcr.io/richertunes/brainarr:${{ steps.version.outputs.VERSION }}
            ghcr.io/richertunes/brainarr:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Troubleshooting

### Image Size Too Large
**Problem**: Docker image is 500MB+
**Solutions**:
- Use multi-stage builds
- Clean up package caches
- Avoid installing dev dependencies
- Use .dockerignore

### Slow Container Builds
**Problem**: Build takes 10+ minutes
**Solutions**:
- Enable Docker layer caching
- Use GitHub Actions cache
- Parallelize builds
- Optimize layer order

### Permission Issues
**Problem**: Plugin files not readable in container
**Solutions**:
- Set correct PUID/PGID
- Use COPY --chown in Dockerfile
- Check volume mount permissions

### Health Check Failures
**Problem**: Container marked unhealthy
**Solutions**:
- Increase start-period
- Verify health check endpoint
- Check Lidarr startup time
- Review container logs

## Implementation Roadmap

### Phase 1: Basic Containerization
1. Create Dockerfile for Lidarr + Brainarr image
2. Add .dockerignore file
3. Test local builds
4. Document manual build process

### Phase 2: CI/CD Integration
5. Add container-build.yml workflow
6. Configure GHCR authentication
7. Implement image tagging strategy
8. Test automated builds on tags

### Phase 3: Multi-Architecture
9. Set up Docker Buildx
10. Add ARM support (arm64, arm/v7)
11. Test on different platforms
12. Document supported architectures

### Phase 4: Orchestration
13. Create Helm chart
14. Add Kubernetes manifests
15. Document deployment options
16. Provide example configurations

## Related Skills
- `release-automation` - Integrate container builds in releases
- `artifact-manager` - Manage container images as artifacts
- `observability` - Add monitoring to deployed containers

## Examples

### Example 1: Create Docker Image
**User**: "Create a Docker image that includes Lidarr and Brainarr"
**Action**:
1. Create Dockerfile with multi-stage build
2. Base on ghcr.io/hotio/lidarr:pr-plugins
3. Copy Brainarr plugin files
4. Add health check
5. Test local build
6. Document usage

### Example 2: Publish to GHCR
**User**: "Automatically publish Docker images on release"
**Action**:
1. Create .github/workflows/container-build.yml
2. Configure GHCR authentication
3. Add multi-arch build support
4. Implement version tagging from git tags
5. Test on release tag
6. Document image usage in README

### Example 3: Create Helm Chart
**User**: "Create a Helm chart for Kubernetes deployment"
**Action**:
1. Create helm/brainarr/ directory structure
2. Write Chart.yaml with metadata
3. Create deployment, service, ingress templates
4. Add values.yaml with sensible defaults
5. Document installation: `helm install brainarr ./helm/brainarr`
