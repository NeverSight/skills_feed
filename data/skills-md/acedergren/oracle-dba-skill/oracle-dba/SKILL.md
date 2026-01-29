---
name: oracle-dba
description: "Oracle DBA and DevOps expertise for Autonomous Database (ADB) on OCI. This skill should be used when managing Oracle Autonomous Databases, writing optimized SQL/PLSQL, configuring security (TDE, Database Vault, Data Safe), implementing HA/DR (Data Guard, PITR), using OCI CLI for database operations, or integrating with Oracle MCP servers for AI-assisted database management. Covers Oracle Database versions 19c, 21c, 23ai, and 26ai."
---

# Oracle DBA & DevOps Skill

Expert Oracle Database administration and DevOps engineering for Autonomous Database (ADB) on Oracle Cloud Infrastructure.

## Overview

This skill provides comprehensive guidance for:
- **Production DBA**: Performance tuning, backup/recovery, monitoring, patching
- **Security DBA**: TDE, Database Vault, Data Safe, unified auditing, SQL Firewall
- **Cloud DBA**: OCI operations, scaling, Data Guard, cost optimization

## When to Use This Skill

- Managing Oracle Autonomous Database (Shared/Dedicated/Free Tier)
- Writing optimized SQL queries and PLSQL procedures
- Configuring database security and compliance
- Implementing high availability and disaster recovery
- Using Oracle MCP servers for AI-assisted database operations
- Automating database tasks with OCI CLI
- Troubleshooting performance issues with AWR/ADDM

## Quick Reference

### Connect to ADB via SQLcl

```bash
# Using wallet
sql admin@charlstn_high?TNS_ADMIN=/path/to/wallet

# Using Cloud Shell (no wallet needed)
sql -cloudconfig wallet.zip admin@adb_name_high
```

### Common OCI CLI Commands

```bash
# List Autonomous Databases
oci db autonomous-database list --compartment-id $C

# Start/Stop ADB
oci db autonomous-database start --autonomous-database-id $ADB_ID
oci db autonomous-database stop --autonomous-database-id $ADB_ID

# Scale ECPU
oci db autonomous-database update --autonomous-database-id $ADB_ID \
  --compute-count 4

# Create manual backup
oci db autonomous-database-backup create \
  --autonomous-database-id $ADB_ID \
  --display-name "pre-upgrade-backup"
```

### SQL Best Practices

```sql
-- Always use bind variables
SELECT * FROM users WHERE id = :user_id;

-- Use FETCH FIRST (not LIMIT)
SELECT * FROM orders ORDER BY created_at DESC FETCH FIRST 10 ROWS ONLY;

-- Vector similarity search (26ai)
SELECT id, content, VECTOR_DISTANCE(embedding, :query_vec, COSINE) AS score
FROM documents
ORDER BY score
FETCH FIRST 5 ROWS ONLY;
```

## MCP Server Integration

This skill integrates with three Oracle MCP servers for AI-assisted database operations:

### 1. Oracle SQLcl MCP Server
Enables AI agents to execute SQL queries and manage database connections.

**Key Tools:**
| Tool | Purpose |
|------|---------|
| `list-connections` | List available database connections |
| `connect` | Connect to a database |
| `run-sql` | Execute SQL statements |
| `schema-information` | Get schema metadata |

**Usage Pattern:**
```
1. Call list-connections to see available connections
2. Call connect with connection name
3. Call run-sql to execute queries
4. Call disconnect when done
```

### 2. Oracle Database MCP Server (100+ Tools)
Comprehensive database management through MCP tools.

**Tool Categories:**
- **Schema Discovery**: list tables, columns, constraints, indexes
- **Query Execution**: run SQL, explain plans, execution stats
- **Performance**: AWR reports, session analysis, wait events
- **Security**: user management, privilege grants, audit settings
- **Backup/Recovery**: backup status, restore points, PITR

### 3. Oracle DB Documentation MCP Server
Search official Oracle documentation from within AI conversations.

**Tool:**
| Tool | Purpose |
|------|---------|
| `search_oracle_database_documentation` | Search Oracle docs by phrase |

## Workflow Decision Tree

```
Database Task Required
├── Performance Issue?
│   ├── Slow Query → references/sql-patterns.md (query optimization)
│   ├── High CPU/Wait → AWR/ADDM analysis via MCP tools
│   └── Scaling Needed → OCI CLI scale commands
├── Security Task?
│   ├── Encryption → references/adb-security.md (TDE)
│   ├── Access Control → Database Vault, Label Security
│   └── Auditing → Unified Audit, Data Safe
├── HA/DR Task?
│   ├── Standby Setup → references/adb-ha-dr.md (Autonomous Data Guard)
│   ├── Backup/Restore → Automatic backups, PITR (95 days)
│   └── Failover → Switchover/Failover procedures
└── Development Task?
    ├── SQL Query → references/sql-patterns.md
    ├── Vector Search → DBMS_VECTOR, AI Vector Search
    └── JSON Processing → JSON Relational Duality
```

## ADB Feature Summary

### Automatic Features (No DBA Action Required)
- **Auto Indexing**: Automatic index creation based on workload
- **Auto Scaling**: CPU scales 1-3x based on demand (when enabled)
- **Auto Backup**: Daily incremental, weekly full (60 days retention)
- **Auto Patching**: Security and bug fixes applied automatically
- **Auto Tuning**: SQL Plan Baselines, Segment Advisor

### DBA-Managed Features
- **Manual Scaling**: Adjust base ECPU/storage via console or CLI
- **Autonomous Data Guard**: Enable cross-region standby
- **Backup-Based DR**: Cross-region backup replication
- **Point-in-Time Recovery**: Restore to any point (up to 95 days)
- **Refreshable Clones**: Read-only clones with auto-refresh

### Version-Specific Features

| Feature | 19c | 21c | 23ai | 26ai |
|---------|-----|-----|------|------|
| JSON Duality | - | - | ✓ | ✓ |
| AI Vector Search | - | - | ✓ | ✓ |
| JavaScript Stored Procs | - | - | - | ✓ |
| Select AI | - | - | ✓ | ✓ |
| Property Graphs | - | ✓ | ✓ | ✓ |
| True Cache | - | - | - | ✓ |

## Common Operations

### Performance Troubleshooting

```sql
-- Find top SQL by elapsed time (last hour)
SELECT sql_id, elapsed_time/1000000 AS elapsed_sec, executions,
       ROUND(elapsed_time/executions/1000,2) AS avg_ms
FROM v$sql
WHERE executions > 0 AND last_active_time > SYSDATE - 1/24
ORDER BY elapsed_time DESC
FETCH FIRST 10 ROWS ONLY;

-- Check session wait events
SELECT event, total_waits, time_waited_micro/1000000 AS wait_sec
FROM v$system_event
WHERE wait_class != 'Idle'
ORDER BY time_waited_micro DESC
FETCH FIRST 10 ROWS ONLY;

-- Generate AWR report (requires DBA privilege)
SELECT * FROM TABLE(DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_HTML(
  l_dbid => (SELECT dbid FROM v$database),
  l_inst_num => 1,
  l_bid => :begin_snap_id,
  l_eid => :end_snap_id
));
```

### Security Configuration

```sql
-- Enable TDE for tablespace (auto-enabled in ADB)
ALTER TABLESPACE users ENCRYPTION USING 'AES256' ENCRYPT;

-- Create read-only user
CREATE USER report_user IDENTIFIED BY :password;
GRANT CREATE SESSION TO report_user;
GRANT SELECT ON schema.table TO report_user;

-- Enable unified auditing for schema
CREATE AUDIT POLICY audit_sales_schema
  ACTIONS ALL ON sales.orders, ALL ON sales.customers;
AUDIT POLICY audit_sales_schema;
```

### Backup and Recovery

```bash
# Restore to point in time (OCI Console or CLI)
oci db autonomous-database restore \
  --autonomous-database-id $ADB_ID \
  --timestamp "2024-01-15T10:30:00Z"

# Create refreshable clone
oci db autonomous-database create-clone \
  --source-autonomous-database-id $SOURCE_ID \
  --compartment-id $C \
  --clone-type REFRESHABLE_CLONE \
  --db-name "dev_clone" \
  --display-name "Development Clone"
```

## Known Issues and Workarounds

### PDB Visibility Delay
- **Issue**: New PDBs don't appear in console for several hours
- **Workaround**: PDBs are operational via SQL; console sync is eventual

### TDE Wallet Migration (12c R1/R2)
- **Issue**: File-based to customer-managed key migration fails
- **Workaround**: Use `dbaascli --skip_patch_check true`

### Backup to Object Storage Failures
- **Issue**: SSL certificate changes cause RMAN backup failures
- **Workaround**: Update Oracle Database Cloud Backup Module

## Resources

For detailed reference information, see:

- `references/mcp-tools.md` - Complete MCP server tool catalog
- `references/oci-cli.md` - OCI CLI commands for Autonomous Database
- `references/adb-security.md` - Security configuration (TDE, Vault, Data Safe)
- `references/adb-ha-dr.md` - High availability and disaster recovery
- `references/sql-patterns.md` - SQL/PLSQL patterns optimized for ADB

## External Documentation

- [Oracle Database 26ai Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/26/)
- [Autonomous Database Documentation](https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/)
- [OCI CLI Reference](https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/)
- [Oracle MCP Servers](https://github.com/oracle-samples/oracle-mcp-servers)
- [SQLcl Documentation](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/)
