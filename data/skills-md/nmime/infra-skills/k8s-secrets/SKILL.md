---
name: k8s-secrets
description: Vault + External Secrets Operator for secrets management.
---

# K8s Secrets

HashiCorp Vault v1.21.2 + ESO v1.2.1. (Updated: January 2026). All scripts are **idempotent** - uses `helm upgrade --install`.

## Components

| Component | Version |
|-----------|---------|
| Vault | v1.21.2 |
| ESO | v1.2.1 |

> **Note**: ESO minor version bumps may include breaking changes. Plan for testing during upgrades.

## Installation

See [references/vault.md](references/vault.md) for Vault setup and [references/eso.md](references/eso.md) for External Secrets Operator.

## Reference Files

- [references/vault.md](references/vault.md) - Vault installation
- [references/eso.md](references/eso.md) - External Secrets Operator
- [references/secret-stores.md](references/secret-stores.md) - Secret store configuration
- [references/best-practices.md](references/best-practices.md) - Best practices