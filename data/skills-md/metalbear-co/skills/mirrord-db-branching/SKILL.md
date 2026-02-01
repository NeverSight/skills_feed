---
name: mirrord-db-branching
description: Helps users configure mirrord.json for database branching, enabling isolated database copies for safe development and testing. Use when the user wants to set up MySQL or PostgreSQL branching, configure copy modes, IAM authentication, or manage database branches.
metadata:
  author: MetalBear
  version: "1.0"
---

# Mirrord DB Branching Skill

## Purpose

Generate and validate `mirrord.json` configurations for database branching:
- **Generate** valid db_branches configs from natural language descriptions
- **Explain** copy modes, IAM authentication, and branch management
- **Validate** user-provided configs against schema requirements
- **Troubleshoot** common DB branching issues

## References

For complete documentation, see:
- [DB Branching Overview](https://github.com/metalbear-co/docs/blob/main/docs/using-mirrord/db-branching.md)
- [Advanced Configuration](https://github.com/metalbear-co/docs/blob/main/docs/using-mirrord/db-branching-advanced-config.md)
- [Branch Management](https://github.com/metalbear-co/docs/blob/main/docs/using-mirrord/db-branch-management.md)

## Critical First Steps

**Step 0: Load References**
Read the reference files from this skill's `references/` directory:
- `references/db-branches-schema.json` - Authoritative JSON Schema for db_branches configuration
- `references/troubleshooting.md` - Common issues and solutions

The schema is derived from the official mirrord schema at:
https://raw.githubusercontent.com/metalbear-co/mirrord/main/mirrord-schema.json

If using absolute paths, search for the schema using patterns like `**/mirrord-db-branching/references/*`.

**Step 1: Verify Prerequisites**

For MySQL:
- Operator 3.129.0+, mirrord CLI 3.160.0+, Helm chart 1.37.0+
- Helm chart must have `operator.mysqlBranching: true`

For PostgreSQL:
- Operator 3.131.0+, mirrord CLI 3.175.0+, Helm chart 1.40.2+
- Helm chart must have `operator.pgBranching: true`

**Step 2: Identify Connection Environment Variable**
The application must use an environment variable for the database connection string. mirrord will override this variable with the branch connection URL.

**Step 3: Validate Configuration**
After generating any config, ALWAYS run:
```bash
mirrord verify-config /path/to/config.json
```

## Configuration Structure

### Basic DB Branch Configuration

```json
{
  "db_branches": [
    {
      "id": "unique-branch-identifier",
      "type": "mysql",
      "version": "8.0",
      "name": "database-name",
      "ttl_secs": 60,
      "creation_timeout_secs": 20,
      "connection": {
        "url": {
          "type": "env",
          "variable": "DB_CONNECTION_URL"
        }
      },
      "copy": {
        "mode": "empty"
      }
    }
  ]
}
```

### Supported Database Types

| Type | Value | Notes |
|------|-------|-------|
| MySQL | `"mysql"` | Requires operator.mysqlBranching: true |
| PostgreSQL | `"pg"` | Requires operator.pgBranching: true, supports IAM auth |
| MongoDB | `"mongodb"` | Uses collections instead of tables |
| Redis | `"redis"` | Can run locally or remotely |

### Configuration Fields (MySQL, PostgreSQL, MongoDB)

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | Database engine: `"mysql"`, `"pg"`, or `"mongodb"` |
| `connection` | Yes | Connection source configuration |
| `connection.url.type` | Yes | Must be `"env"` or `"env_from"` |
| `connection.url.variable` | Yes | Environment variable storing the connection string |
| `id` | No | Branch identifier for reuse; same ID reconnects to existing branch |
| `name` | No | Database name when not accessible from connection |
| `version` | No | Engine version (e.g., `"8.0"` for MySQL, `"16"` for PostgreSQL) |
| `ttl_secs` | No | Branch lifetime in seconds (max 900 / 15 minutes, default 300 / 5 minutes) |
| `creation_timeout_secs` | No | Setup timeout (default 60 seconds) |
| `copy.mode` | No | Cloning strategy (default `"empty"`) |
| `iam_auth` | No | Cloud IAM authentication (PostgreSQL only) |

### Configuration Fields (Redis)

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | Must be `"redis"` |
| `location` | No | `"local"` or `"remote"` (default: `"remote"`) |
| `connection` | No | Redis connection config (URL or host/port/password) |
| `id` | No | Branch identifier for reuse |
| `local` | No | Local Redis runtime config (when location is `"local"`) |

## Copy Modes

### Empty Database (Default)
Creates an empty database with no schema or data. Use when your application handles migrations on startup.

```json
{
  "copy": {
    "mode": "empty"
  }
}
```

### Schema Only
Replicates table structures without data. Good for testing schema modifications.

```json
{
  "copy": {
    "mode": "schema"
  }
}
```

### Complete Database
Copies schema and all data. **Use only for small databases** as this increases creation time significantly.

```json
{
  "copy": {
    "mode": "all"
  }
}
```

### Filtered Data Clone (MySQL/PostgreSQL)
Copy schema plus filtered rows from specific tables. Cannot be combined with `"mode": "all"`.

```json
{
  "copy": {
    "mode": "schema",
    "tables": {
      "users": {"filter": "name = 'alice' OR name = 'bob'"},
      "orders": {"filter": "created_at > 1759948761"}
    }
  }
}
```

### MongoDB Copy Modes

MongoDB uses `collections` instead of `tables`:

```json
{
  "copy": {
    "mode": "all",
    "collections": {
      "users": {"filter": "{\"name\": {\"$in\": [\"alice\", \"bob\"]}}"},
      "orders": {"filter": "{\"created_at\": {\"$gt\": 1759948761}}"}
    }
  }
}
```

## Redis Configuration

Redis branches can run locally or use the remote instance.

### Local Redis Branch
```json
{
  "db_branches": [
    {
      "type": "redis",
      "location": "local",
      "connection": {
        "url": {
          "type": "env",
          "variable": "REDIS_URL"
        }
      },
      "local": {
        "runtime": "container",
        "container_runtime": "docker",
        "port": 6379,
        "version": "7-alpine"
      }
    }
  ]
}
```

### Redis with Separated Connection
```json
{
  "db_branches": [
    {
      "type": "redis",
      "location": "local",
      "connection": {
        "host": {
          "type": "env",
          "variable": "REDIS_HOST"
        },
        "port": 6379,
        "password": {
          "type": "env",
          "variable": "REDIS_PASSWORD"
        }
      }
    }
  ]
}
```

## IAM Authentication

### AWS RDS
Uses credentials from the target pod's environment:

```json
{
  "iam_auth": {
    "type": "aws_rds"
  }
}
```

Default variables checked: `AWS_REGION`, `AWS_DEFAULT_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`

### GCP Cloud SQL
**Important:** Requires TLS - ensure connection URL includes `sslmode=require`

```json
{
  "iam_auth": {
    "type": "gcp_cloud_sql"
  }
}
```

Uses `GOOGLE_APPLICATION_CREDENTIALS` by default. Can override with:
- `credentials_json` - Inline JSON credentials
- `credentials_path` - Custom file path

## Branch Management Commands

### View Branch Status
```bash
mirrord db-branches [-n namespace] status [branch-names...]
mirrord db-branches --all-namespaces status
```

### Destroy Branches
```bash
mirrord db-branches [-n namespace] destroy branch-name
mirrord db-branches [-n namespace] destroy --all
mirrord db-branches --all-namespaces destroy --all
```

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Connection timeouts | Branch databases disable SSL by default; verify client isn't forcing SSL |
| GCP Cloud SQL fails | Ensure connection URL includes `sslmode=require` |
| Branch creation slow | Using `"mode": "all"` on large database; switch to `"schema"` or `"empty"` |
| Branch not reused | Ensure `id` field is set and matches; check TTL hasn't expired |
| Wrong database connected | Verify `connection.url.variable` matches your app's actual env var |

## What to Ask (only if critical)

If the request is under-specified, ask for ONE detail:
- Database type (MySQL or PostgreSQL)
- Environment variable name for connection string
- Copy mode preference (empty, schema, or all)
- Whether IAM authentication is needed (AWS RDS or GCP Cloud SQL)

Otherwise, provide safe defaults and note assumptions.

## Example Scenarios

### MySQL branch with schema copy
**User:** "I want to test migrations on my MySQL database without affecting production"

```json
{
  "db_branches": [
    {
      "id": "migration-test",
      "type": "mysql",
      "version": "8.0",
      "name": "myapp_production",
      "ttl_secs": 300,
      "connection": {
        "url": {
          "type": "env",
          "variable": "DATABASE_URL"
        }
      },
      "copy": {
        "mode": "schema"
      }
    }
  ]
}
```

### PostgreSQL with AWS RDS IAM
**User:** "Set up a Postgres branch using AWS IAM authentication"

```json
{
  "db_branches": [
    {
      "type": "pg",
      "version": "16",
      "name": "app_db",
      "connection": {
        "url": {
          "type": "env",
          "variable": "PG_CONNECTION_STRING"
        }
      },
      "copy": {
        "mode": "empty"
      },
      "iam_auth": {
        "type": "aws_rds"
      }
    }
  ]
}
```

### Filtered data for testing
**User:** "I need a branch with only test users from the users table"

```json
{
  "db_branches": [
    {
      "id": "test-data-branch",
      "type": "pg",
      "version": "15",
      "name": "production_db",
      "connection": {
        "url": {
          "type": "env",
          "variable": "DATABASE_URL"
        }
      },
      "copy": {
        "mode": "schema",
        "tables": {
          "users": {"filter": "email LIKE '%@test.com'"}
        }
      }
    }
  ]
}
```

### MongoDB branch
**User:** "Set up a MongoDB branch that copies specific users"

```json
{
  "db_branches": [
    {
      "type": "mongodb",
      "version": "7.0",
      "name": "app_database",
      "connection": {
        "url": {
          "type": "env",
          "variable": "MONGODB_URI"
        }
      },
      "copy": {
        "mode": "all",
        "collections": {
          "users": {"filter": "{\"role\": \"admin\"}"}
        }
      }
    }
  ]
}
```

### Local Redis for development
**User:** "I want a local Redis instance for my development session"

```json
{
  "db_branches": [
    {
      "type": "redis",
      "id": "dev-redis",
      "location": "local",
      "connection": {
        "url": {
          "type": "env",
          "variable": "REDIS_URL"
        }
      },
      "local": {
        "runtime": "container",
        "container_runtime": "docker",
        "version": "7-alpine"
      }
    }
  ]
}
```

## Quality Requirements

- **Valid JSON**: Always parseable, no comments or trailing commas
- **Minimal configs**: Only include fields the user actually needs
- **Correct types**: Use proper database types (`"mysql"` or `"pg"`)
- **Safe defaults**: Default to `"empty"` copy mode to avoid long creation times
- **Actionable feedback**: Explain what each field does when relevant
