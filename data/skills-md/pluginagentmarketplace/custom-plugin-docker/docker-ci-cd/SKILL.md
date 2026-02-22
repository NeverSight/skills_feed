---
name: docker-ci-cd
description: Docker integration with CI/CD pipelines for automated builds, testing, and deployments
sasmp_version: "1.3.0"
bonded_agent: 07-docker-production
bond_type: SECONDARY_BOND
---

# Docker CI/CD Skill

Integrate Docker with CI/CD pipelines for automated image builds, security scanning, and deployments.

## Purpose

Set up automated Docker workflows with GitHub Actions, GitLab CI, and other CI/CD platforms.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| platform | enum | No | github | github/gitlab/jenkins |
| registry | string | No | ghcr.io | Container registry |
| scan | boolean | No | true | Include security scan |

## GitHub Actions

### Complete Workflow
```yaml
name: Docker Build and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Scan for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-${{ github.sha }}
          exit-code: '1'
          severity: 'CRITICAL,HIGH'
```

### Multi-Arch Build
```yaml
- name: Set up QEMU
  uses: docker/setup-qemu-action@v3

- name: Build multi-arch
  uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64,linux/arm64
    push: true
    tags: ${{ steps.meta.outputs.tags }}
```

## GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - build
  - scan
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

scan:
  stage: scan
  image:
    name: aquasec/trivy
    entrypoint: [""]
  script:
    - trivy image --exit-code 1 --severity CRITICAL $DOCKER_IMAGE

deploy:
  stage: deploy
  script:
    - ssh deploy@server "docker pull $DOCKER_IMAGE && docker compose up -d"
  only:
    - main
```

## Best Practices

### Caching
```yaml
# GitHub Actions BuildKit cache
cache-from: type=gha
cache-to: type=gha,mode=max

# GitLab cache
cache:
  key: docker-$CI_COMMIT_REF_SLUG
  paths:
    - .docker-cache
```

### Security
```yaml
# Scan before push
- name: Scan
  run: trivy image --exit-code 1 --severity CRITICAL $IMAGE

# Sign images (cosign)
- name: Sign
  run: cosign sign $IMAGE
```

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `unauthorized` | Bad credentials | Check registry login |
| `rate limit` | Docker Hub limits | Use authenticated pulls |
| `cache miss` | First build | Cache will populate |

### Fallback Strategy
1. Build without cache if cache corrupted
2. Use fallback registry if primary down
3. Deploy previous version on failure

## Troubleshooting

### Debug Checklist
- [ ] Registry credentials valid?
- [ ] Docker daemon running?
- [ ] Build context correct?
- [ ] Dockerfile present?

## Usage

```
Skill("docker-ci-cd")
```

## Assets
- `assets/github-actions-docker.yaml` - GitHub Actions template
- `scripts/build-and-push.sh` - Build script

## Related Skills
- docker-production
- docker-security
