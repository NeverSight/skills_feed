---
name: database-administrator
description: "Senior Database Administrator with expertise in PostgreSQL, MySQL, MongoDB, and enterprise database systems. Specializes in high availability architectures, performance tuning, backup strategies, and database security for production environments."
---

# Database Administrator

## Purpose

Provides senior-level database administration expertise for production database systems including PostgreSQL, MySQL, MongoDB, and enterprise databases. Specializes in high availability architectures, performance tuning, backup strategies, disaster recovery, and database security for mission-critical environments.

## When to Use

- Setting up production databases with high availability and disaster recovery
- Optimizing database performance (slow queries, indexing, configuration tuning)
- Implementing backup and recovery strategies (PITR, cross-region backups)
- Migrating databases (PostgreSQL, MySQL, MongoDB) to cloud or between versions
- Hardening database security (encryption, access control, audit logging)
- Troubleshooting database issues (locks, replication lag, corruption)
- Designing database architectures for scalability and reliability

## Quick Start

**Invoke this skill when:**
- Setting up production databases with high availability and disaster recovery
- Optimizing database performance (slow queries, indexing, configuration tuning)
- Implementing backup and recovery strategies (PITR, cross-region backups)
- Migrating databases (PostgreSQL, MySQL, MongoDB) to cloud or between versions
- Hardening database security (encryption, access control, audit logging)
- Troubleshooting database issues (locks, replication lag, corruption)

**Do NOT invoke when:**
- Only application-level ORM queries need optimization (use backend-developer)
- Data pipeline development (use data-engineer for ETL/ELT)
- Data modeling and schema design for analytics (use data-engineer)
- Database selection for new projects (use cloud-architect for strategy)
- Simple SQL queries or data analysis (use data-analyst)

## Decision Framework

### Database Selection

| Use Case | Database | Why |
|----------|----------|-----|
| **Transactional (OLTP)** | PostgreSQL | ACID, extensions, JSON support |
| **High-read web apps** | MySQL/MariaDB | Fast reads, mature replication |
| **Flexible schema** | MongoDB | Document model, horizontal scale |
| **Key-value cache** | Redis | Sub-ms latency, data structures |
| **Time-series data** | TimescaleDB/InfluxDB | Optimized for time-based queries |
| **Analytics (OLAP)** | Snowflake/BigQuery | Columnar, massive scale |

### High Availability Architecture

```
├─ Single Region HA?
│   ├─ Managed service → RDS Multi-AZ / Cloud SQL HA
│   │   Pros: Automatic failover, managed backups
│   │   Cost: 2x compute (standby instance)
│   │
│   └─ Self-managed → Patroni + etcd (PostgreSQL)
│       Pros: Full control, no vendor lock-in
│       Cost: Operational overhead
│
├─ Multi-Region HA?
│   ├─ Active-Passive → Cross-region read replicas
│   │   Pros: Simple, low cost
│   │   Cons: Manual failover, data lag
│   │
│   └─ Active-Active → CockroachDB / Spanner
│       Pros: True global distribution
│       Cons: Complexity, cost
│
└─ Horizontal Scaling?
    ├─ Read scaling → Read replicas
    ├─ Write scaling → Sharding (MongoDB, Vitess)
    └─ Both → Distributed SQL (CockroachDB, TiDB)
```

### Backup Strategy Matrix

| RPO Requirement | Strategy | Implementation |
|-----------------|----------|----------------|
| **< 1 minute** | Synchronous replication | Patroni sync mode |
| **< 5 minutes** | Continuous WAL archiving | pg_basebackup + WAL-G |
| **< 1 hour** | Automated snapshots | RDS automated backups |
| **< 24 hours** | Daily backups | pg_dump + S3 |

### Performance Tuning Priorities

1. **Query optimization** (biggest impact, lowest cost)
2. **Indexing strategy** (moderate effort, high impact)
3. **Configuration tuning** (one-time, moderate impact)
4. **Hardware upgrades** (high cost, last resort)

## Quality Checklist

### Production Readiness
- [ ] High availability configured (multi-AZ or multi-region)
- [ ] Automated backups enabled (daily + continuous WAL)
- [ ] Backup restoration tested (monthly disaster recovery drill)
- [ ] Connection pooling configured (PgBouncer/ProxySQL)
- [ ] Monitoring and alerting active (slow queries, replication lag)

### Performance
- [ ] Indexes created for all query patterns
- [ ] Table statistics up-to-date (autovacuum tuned)
- [ ] Query plans reviewed (no full table scans on large tables)
- [ ] Connection pooling optimized (min/max pool size)
- [ ] Database configuration tuned (shared_buffers, work_mem)

### Security
- [ ] Encryption at rest enabled
- [ ] Encryption in transit (SSL/TLS) enforced
- [ ] Least privilege access (no superuser for applications)
- [ ] Audit logging enabled (failed logins, DDL changes)
- [ ] Regular security patching scheduled

### Disaster Recovery
- [ ] RTO/RPO documented and tested
- [ ] Cross-region backups enabled
- [ ] Failover procedure documented and tested
- [ ] Data retention policy enforced
- [ ] Point-in-time recovery validated

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
