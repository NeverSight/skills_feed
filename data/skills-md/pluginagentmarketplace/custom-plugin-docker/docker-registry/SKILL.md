---
name: docker-registry
description: Private registry setup, image management, and multi-registry operations
sasmp_version: "1.3.0"
bonded_agent: 02-docker-images
bond_type: PRIMARY_BOND
---

# Docker Registry Skill

Set up and manage private Docker registries for secure image distribution and management.

## Purpose

Deploy private registries, configure authentication, and manage images across multiple registries.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| registry_type | enum | No | docker | docker/ecr/gcr/acr |
| auth | boolean | No | true | Enable authentication |
| tls | boolean | No | true | Enable TLS |

## Registry Types

| Registry | Provider | Auth Method |
|----------|----------|-------------|
| Docker Hub | Docker | Username/token |
| GHCR | GitHub | GitHub token |
| ECR | AWS | IAM/CLI |
| GCR | Google | Service account |
| ACR | Azure | Service principal |

## Private Registry Setup

### Docker Compose
```yaml
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    volumes:
      - registry_data:/var/lib/registry
      - ./auth:/auth
      - ./certs:/certs
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
      REGISTRY_HTTP_TLS_CERTIFICATE: /certs/domain.crt
      REGISTRY_HTTP_TLS_KEY: /certs/domain.key
    restart: unless-stopped

volumes:
  registry_data:
```

### Create Auth File
```bash
# Create htpasswd file
docker run --rm --entrypoint htpasswd \
  httpd:alpine -Bbn admin password > auth/htpasswd
```

## Registry Operations

### Login
```bash
# Docker Hub
docker login

# GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# AWS ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com

# Private registry
docker login registry.example.com
```

### Push/Pull
```bash
# Tag for registry
docker tag myapp:latest registry.example.com/myapp:latest

# Push
docker push registry.example.com/myapp:latest

# Pull
docker pull registry.example.com/myapp:latest
```

### Image Management
```bash
# List images in registry (API)
curl -X GET https://registry.example.com/v2/_catalog

# List tags
curl -X GET https://registry.example.com/v2/myapp/tags/list

# Delete image (via API)
curl -X DELETE https://registry.example.com/v2/myapp/manifests/<digest>
```

## Multi-Registry Sync
```bash
# Copy between registries
skopeo copy \
  docker://source-registry/image:tag \
  docker://dest-registry/image:tag

# Sync all tags
skopeo sync --src docker --dest docker \
  source-registry/image dest-registry/
```

## Cloud Registry Setup

### AWS ECR
```bash
# Create repository
aws ecr create-repository --repository-name myapp

# Login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

# Push
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
```

### Google GCR
```bash
# Auth with service account
gcloud auth configure-docker

# Push
docker push gcr.io/project-id/myapp:latest
```

## Error Handling

### Common Errors
| Error | Cause | Solution |
|-------|-------|----------|
| `unauthorized` | Bad credentials | Re-login |
| `manifest unknown` | Image not found | Check name/tag |
| `denied: access` | No permission | Check IAM/roles |
| `TLS handshake` | Certificate issue | Add to trusted certs |

### Fallback Strategy
1. Verify credentials: `docker login`
2. Check image exists in registry
3. Verify network connectivity

## Troubleshooting

### Debug Checklist
- [ ] Logged in? `docker login`
- [ ] Image tagged correctly?
- [ ] Registry accessible? `curl https://registry/v2/`
- [ ] TLS configured? Check certificates

## Usage

```
Skill("docker-registry")
```

## Assets
- `assets/docker-compose-registry.yaml` - Registry setup
- `scripts/registry-setup.sh` - Setup script

## Related Skills
- docker-optimization
- docker-ci-cd
