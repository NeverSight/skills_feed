---
name: gitlab-selfhosted
description: GitLab CE self-hosted deployment on Kubernetes. Use when installing, configuring, upgrading, or managing GitLab instances including runners, container registry, backups, and external database integration.
---

# GitLab Self-Hosted

GitLab CE v18.7.1 with tier-based resources. (Updated: January 2026)

## Maintenance Policy

| Version | Status |
|---------|--------|
| 18.7.x | **Current** - Active development |
| 18.6.x | Security fixes only |
| 18.5.x | Security fixes only |
| < 18.5 | End of Life |

> GitLab releases monthly (3rd Thursday). Only latest + 2 previous minor versions receive security fixes.

## Modes

| Tier | Mode | Memory |
|------|------|--------|
| minimal/small | light | 2-4GB |
| medium/production | full | 6-12GB |

## Installation

See [references/gitlab-helm.md](references/gitlab-helm.md) for Helm-based installation.

## Reference Files

- [references/gitlab-light.md](references/gitlab-light.md) - Light mode setup
- [references/gitlab-full.md](references/gitlab-full.md) - Full mode setup
- [references/gitlab-helm.md](references/gitlab-helm.md) - Helm installation
- [references/gitlab-runner.md](references/gitlab-runner.md) - GitLab Runner
- [references/registry.md](references/registry.md) - Container registry
- [references/storage.md](references/storage.md) - Storage configuration
- [references/backup.md](references/backup.md) - Backup procedures
- [references/cleanup.md](references/cleanup.md) - Cleanup operations
- [references/external-db.md](references/external-db.md) - External database