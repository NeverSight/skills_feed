---
name: sling
description: >
  Sling data integration platform overview and MCP tools reference.
  Use when asked about Sling in general, what it does, or how to use the MCP tools.
---

# Sling - Data Integration Platform

Move data between 40+ databases, file systems, and APIs with a single CLI.

## When to Use Sling

| Use Case | Solution |
|----------|----------|
| Move data between databases | Replication (DB-to-DB) |
| Load files into databases | Replication (file-to-DB) |
| Export data to files | Replication (DB-to-file) |
| Extract API data | Replication (API-to-DB/file) |
| Multi-step workflows | Pipelines |

## MCP Tools Reference

| Tool | Actions | Use Case |
|------|---------|----------|
| `connection` | list, test, discover, set | Manage connections |
| `database` | query, get_schemata | Inspect/query databases |
| `file_system` | list, copy, inspect | Browse/copy files |
| `replication` | parse, compile, run | Execute data replications |
| `pipeline` | parse, run | Execute multi-step workflows |
| `api_spec` | parse, test | Build API integrations |

## Quick Examples

### List connections
```json
{"action": "list", "input": {}}
```

### Test connection
```json
{"action": "test", "input": {"connection": "MY_CONN", "debug": true}}
```

### Run replication
```json
{"action": "run", "input": {"file_path": "/path/to/replication.yaml"}}
```

## CLI Quick Reference

```bash
sling conns list                    # List connections
sling conns test MY_CONN            # Test connection
sling conns discover MY_PG          # Discover tables
sling run -r replication.yaml       # Run replication
sling run -p pipeline.yaml          # Run pipeline
```

## Related Skills

- `sling-connections` - Connection management
- `sling-replications` - Data replication configs
- `sling-pipelines` - Multi-step workflows
- `sling-transforms` - Data transformation functions
- `sling-hooks` - Pre/post actions
- `sling-api-specs` - API specification building
- `sling-troubleshooting` - Debug issues

## Documentation

- **Official Docs**: https://docs.slingdata.io
- **GitHub**: https://github.com/slingdata-io/sling-cli
