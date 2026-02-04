---
name: clickhouse-cloud-management
description: ClickHouse Cloud user and permission management. TRIGGERS - create ClickHouse user, ClickHouse permissions, ClickHouse Cloud credentials.
allowed-tools: Read, Bash
---

# ClickHouse Cloud Management

ADR: 2025-12-08-clickhouse-cloud-management-skill

## Overview

ClickHouse Cloud user and permission management via SQL commands over HTTP interface. This skill covers database user creation, permission grants, and credential management for ClickHouse Cloud instances.

## When to Use This Skill

Invoke this skill when:

- Creating database users for ClickHouse Cloud
- Managing user permissions (GRANT/REVOKE)
- Testing ClickHouse Cloud connectivity
- Troubleshooting authentication issues
- Understanding API key vs database user distinction

## Key Concepts

### Management Options

ClickHouse Cloud provides two management interfaces with different capabilities:

| Task                 | Via SQL (CLI/HTTP) | Via Cloud Console |
| -------------------- | ------------------ | ----------------- |
| Create database user | CREATE USER        | Supported         |
| Grant permissions    | GRANT              | Supported         |
| Delete user          | DROP USER          | Supported         |
| Create API key       | Not possible       | Only here         |

**Key distinction**: Database users (created via SQL) authenticate to ClickHouse itself. API keys (created via console) authenticate to the ClickHouse Cloud management API.

### Connection Details

ClickHouse Cloud exposes only HTTP interface publicly:

- **Port**: 443 (HTTPS)
- **Protocol**: HTTP (not native ClickHouse protocol)
- **Native protocol**: Requires AWS PrivateLink (not available without enterprise setup)

### Password Requirements

ClickHouse Cloud enforces strong password policy:

- Minimum 12 characters
- At least 1 uppercase letter
- At least 1 special character

Example compliant password: `StrongPass@2025!`

## Quick Reference

### Create Read-Only User

```bash
curl -s "https://default:PASSWORD@HOST:443/" --data-binary \
  "CREATE USER my_reader IDENTIFIED BY 'StrongPass@2025!' SETTINGS readonly = 1"
```

### Grant Database Access

```bash
curl -s "https://default:PASSWORD@HOST:443/" --data-binary \
  "GRANT SELECT ON deribit.* TO my_reader"
```

### Delete User

```bash
curl -s "https://default:PASSWORD@HOST:443/" --data-binary \
  "DROP USER my_reader"
```

For comprehensive SQL patterns and advanced permission scenarios, see [SQL Patterns Reference](./references/sql-patterns.md).

## Credential Sources

### 1Password Items (Engineering Vault)

| Item                                             | Purpose                                   |
| ------------------------------------------------ | ----------------------------------------- |
| ClickHouse Cloud - API Key (Admin)               | Cloud management API (console operations) |
| ClickHouse Cloud - API Key (Developer Read-only) | Cloud management API (read-only)          |
| gapless-deribit-clickhouse                       | Database `default` user credentials       |

### Retrieving Credentials

```bash
# Database credentials (for SQL commands)
op item get "gapless-deribit-clickhouse" --vault Engineering --reveal

# API key (for cloud management API)
op item get "ClickHouse Cloud - API Key (Admin)" --vault Engineering --reveal
```

## Common Workflows

### Workflow 1: Create Application User

1. Retrieve `default` user credentials from 1Password
2. Create new user with appropriate permissions:

```bash
HOST="your-instance.clickhouse.cloud"
PASSWORD="default-user-password"

# Create user
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "CREATE USER app_user IDENTIFIED BY 'AppPass@2025!'"

# Grant specific database access
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary \
  "GRANT SELECT, INSERT ON mydb.* TO app_user"
```

### Workflow 2: Verify User Exists

```bash
curl -s "https://default:$PASSWORD@$HOST:443/" --data-binary "SHOW USERS"
```

### Workflow 3: Test Connection

```bash
curl -s "https://user:password@HOST:443/" --data-binary "SELECT 1"
```

Expected output: `1` (single row with value 1)

## Troubleshooting

### Authentication Failed

- Verify password meets complexity requirements
- Check host URL includes port 443
- Ensure using HTTPS (not HTTP)

### Permission Denied

- Verify user has required GRANT statements
- Check database and table names are correct
- Confirm user was created with correct settings

### Connection Timeout

- ClickHouse Cloud only exposes port 443 publicly
- Native protocol (port 9440) requires PrivateLink
- Use HTTP interface with curl or clickhouse-client HTTP mode

## Next Steps After User Creation

<!-- ADR: 2025-12-10-clickhouse-skill-delegation -->

After creating a ClickHouse user, invoke **`devops-tools:clickhouse-pydantic-config`** to generate DBeaver configuration with the new credentials.

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques, consult:

- **[references/sql-patterns.md](./references/sql-patterns.md)** - Complete SQL syntax reference with examples

## Python Driver Policy

For Python application code connecting to ClickHouse Cloud, use `clickhouse-connect` (official HTTP driver). See [`clickhouse-architect`](../../../quality-tools/skills/clickhouse-architect/SKILL.md#python-driver-policy) for recommended code patterns and why to avoid `clickhouse-driver` (community).

## Related Skills

- `quality-tools:clickhouse-architect` - Schema design, compression codecs, Python driver policy
- `devops-tools:clickhouse-pydantic-config` - DBeaver configuration generation
- `devops-tools:doppler-secret-validation` - For storing credentials in Doppler
- `devops-tools:doppler-workflows` - For credential rotation workflows
