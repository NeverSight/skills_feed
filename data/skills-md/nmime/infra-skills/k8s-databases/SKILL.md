---
name: k8s-databases
description: PostgreSQL and MongoDB on Kubernetes via Percona Operators. Use when deploying databases, configuring HA clusters, setting up backups, monitoring, or performing database operations.
---

# K8s Databases

Percona Operators for PostgreSQL and MongoDB. (Updated: January 2026). All deployments are **idempotent** - operators reconcile to desired state.

## Percona Operators

| Operator | Version | Database |
|----------|---------|----------|
| Percona PostgreSQL | v2.8.2 | PostgreSQL 18.x |
| Percona Server MongoDB | v1.21.2 | MongoDB 8.0.x |

> Always use latest versions. Operators include built-in backup, monitoring, and HA management.

## Deployment Tiers

| Tier | PostgreSQL | MongoDB | HA |
|------|------------|---------|-----|
| minimal/small | 1 replica | 1 replica | No |
| medium/production | 3 replicas + PgBouncer | 3 replicas (ReplicaSet) | Yes |

## Installation

See [references/postgresql.md](references/postgresql.md) and [references/mongodb.md](references/mongodb.md) for deployment.

## Get Connections

```bash
# PostgreSQL
kubectl get secret myapp-pg-pguser-myapp -n databases \
  -o jsonpath='{.data.uri}' | base64 -d

# MongoDB
kubectl get secret myapp-mongo-secrets -n databases \
  -o jsonpath='{.data.MONGODB_DATABASE_ADMIN_URI}' | base64 -d
```

## Reference Files

- [references/postgresql.md](references/postgresql.md) - PostgreSQL HA cluster
- [references/postgresql-single.md](references/postgresql-single.md) - PostgreSQL single instance
- [references/mongodb.md](references/mongodb.md) - MongoDB ReplicaSet
- [references/backups.md](references/backups.md) - Backup with MinIO
- [references/monitoring.md](references/monitoring.md) - Metrics and alerting
