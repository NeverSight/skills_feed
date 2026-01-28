---
name: minio-storage
description: MinIO S3-compatible object storage on Kubernetes. Use when deploying MinIO, configuring buckets, setting up integrations with GitLab/Loki/backups, or managing S3-compatible storage infrastructure.
---

# MinIO Storage

S3-compatible storage for platform services. (Updated: January 2026). All scripts are **idempotent** - uses `helm upgrade --install`.

## MinIO Image Source Change

As of October 2025, MinIO no longer provides official Docker images. Use one of these alternatives:

| Option | Image | Notes |
|--------|-------|-------|
| **Chainguard (Recommended)** | `cgr.dev/chainguard/minio` | Free tier, vulnerability-free |
| **Bitnami** | `bitnami/minio` | Community maintained |
| **Build from source** | Self-built | Requires Go 1.24+ |

## Modes

| Tier | Mode | Replicas |
|------|------|----------|
| minimal/small | standalone | 1 |
| medium/production | distributed | 4 |

## Installation

See [references/installation.md](references/installation.md) for deployment options:
- Standalone: Single replica for minimal/small tiers
- Distributed: 4 replicas for medium/production tiers

## Integrations

- GitLab (artifacts, uploads, LFS)
- Loki (log storage)
- Backups

## Reference Files

- [references/installation.md](references/installation.md) - Installation overview
- [references/standalone.md](references/standalone.md) - Standalone mode
- [references/distributed.md](references/distributed.md) - Distributed mode
- [references/buckets.md](references/buckets.md) - Bucket management
- [references/gitlab-integration.md](references/gitlab-integration.md) - GitLab integration
- [references/loki-integration.md](references/loki-integration.md) - Loki integration
- [references/backup-integration.md](references/backup-integration.md) - Backup integration
- [references/monitoring.md](references/monitoring.md) - Monitoring
- [references/operations.md](references/operations.md) - Day-to-day operations