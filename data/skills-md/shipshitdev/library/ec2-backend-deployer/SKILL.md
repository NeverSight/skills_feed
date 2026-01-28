---
name: ec2-backend-deployer
description: Expert in deploying backends to EC2 instances using CI/CD pipelines, Docker containers, and GitHub Actions
---

# EC2 Backend Deployer

Expert in deploying backend applications to EC2 instances using CI/CD pipelines, Docker containers, and GitHub Actions.

## When to Use This Skill

Use when you're:

- Setting up CI/CD for backend deployment to EC2
- Configuring Docker-based deployments
- Implementing automated deployment pipelines
- Deploying NestJS, Next.js, or Express backends
- Setting up container registries and image management
- Configuring secure EC2 access (Tailscale)

## Quick Workflow

1. **Dockerfile**: Multi-stage build (base → builder → production)
2. **Registry**: GitHub Container Registry (ghcr.io) recommended
3. **CI/CD**: GitHub Actions with Tailscale for secure SSH
4. **Deploy**: Docker Compose on EC2 with health checks
5. **Verify**: Health endpoint + deployment verification

## Key Components

### Docker

- Multi-stage builds for smaller images
- Non-root user for security
- HEALTHCHECK for container orchestration
- BuildKit secrets for sensitive data

### GitHub Actions

- `docker/build-push-action` for image building
- `tailscale/github-action` for secure access
- `appleboy/ssh-action` for deployment

### EC2

- Docker Compose v2 required
- Health check verification
- Rollback procedures

## References

- [Full guide: Dockerfile, CI/CD workflow, deployment, troubleshooting](references/full-guide.md)
