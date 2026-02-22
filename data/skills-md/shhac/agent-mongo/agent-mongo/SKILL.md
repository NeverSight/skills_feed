---
name: agent-mongo
description: |
  Read-only MongoDB CLI for AI agents. Use when:
  - Exploring MongoDB databases, collections, schemas, or indexes
  - Querying documents (find, get by ID, count, sample, distinct, aggregate)
  - Managing MongoDB connections or credentials
  - Checking database or collection statistics
  Triggers: "mongodb", "mongo query", "mongo find", "mongo schema", "mongo collection", "mongo database", "mongo connection", "mongo aggregate", "query mongodb", "mongo stats"
---

# MongoDB exploration with `agent-mongo`

`agent-mongo` is a read-only CLI binary on `$PATH`. All output is JSON to stdout. Errors go to stderr as `{ "error": "..." }` with non-zero exit.

## Quick start (connections)

Set up a connection:

```bash
agent-mongo connection add local "mongodb://localhost:27017/myapp" --default
agent-mongo connection test
```

For authenticated connections, store credentials separately:

```bash
agent-mongo credential add acme --username deploy --password secret
agent-mongo connection add prod "mongodb+srv://cluster.example.net/myapp" --credential acme --default
```

## Exploring a database

```bash
agent-mongo database list                                # all databases with sizes
agent-mongo collection list myapp                        # all collections in myapp
agent-mongo collection schema myapp users                # infer schema from samples
agent-mongo collection schema myapp users --depth 2      # limit nesting depth
agent-mongo collection schema myapp events --limit 50    # paginate large schemas
agent-mongo collection schema myapp events --limit 50 --skip 50  # next page
agent-mongo collection indexes myapp users               # index key patterns
agent-mongo collection stats myapp orders                # document count, sizes
agent-mongo database stats myapp                         # database-level statistics
```

## Querying documents

```bash
agent-mongo query find myapp users --filter '{"age":{"$gte":21}}' --limit 10
agent-mongo query find myapp orders --sort '{"createdAt":-1}' --projection '{"status":1,"total":1}'
agent-mongo query get myapp users 665a1b2c3d4e5f6a7b8c9d0e      # by _id (auto-detects ObjectId)
agent-mongo query get myapp users 665a1b2c3d4e5f6a7b8c9d0e --projection '{"name":1,"email":1}'
agent-mongo query count myapp orders --filter '{"status":"pending"}'
agent-mongo query sample myapp users --size 10                    # random documents
agent-mongo query sample myapp users --size 10 --filter '{"status":"active"}'  # filtered sample
agent-mongo query distinct myapp orders status                    # unique values
```

## Aggregation

```bash
agent-mongo query aggregate myapp orders '[{"$group":{"_id":"$status","count":{"$sum":1}}}]'
agent-mongo query aggregate myapp orders --pipeline '[{"$group":{"_id":"$status","count":{"$sum":1}}}]'
agent-mongo query aggregate myapp events '[{"$match":{"type":"purchase"}},{"$group":{"_id":"$userId","total":{"$sum":"$amount"}}}]'
```

Pipeline can be passed as a positional argument, via `--pipeline` flag, or piped via stdin.

Write stages (`$out`, `$merge`) are rejected — the CLI is strictly read-only.

## Connection management

```bash
agent-mongo connection list                              # saved connections + defaults
agent-mongo connection add staging "mongodb://..." --credential acme
agent-mongo connection update prod --credential new-cred
agent-mongo connection set-default staging
agent-mongo connection remove old-conn
agent-mongo connection test -c prod                      # verify connectivity
```

Connection resolution: `-c` flag > `AGENT_MONGO_CONNECTION` env > config default > error listing available connections.

## Credential management

```bash
agent-mongo credential add acme --username deploy --password secret
agent-mongo credential list                              # passwords always redacted
agent-mongo credential remove acme --force               # even if connections reference it
```

Credentials are stored separately from connections. When you rotate a password, just re-add the credential — all connections referencing it pick up the new auth automatically.

## Truncation

Any string field exceeding `truncation.maxLength` (default 200) gets truncated with `…` and a companion `{field}Length` key showing original length.

```bash
agent-mongo --full query find myapp posts                # expand all fields
agent-mongo --expand description query find myapp posts  # expand specific field
```

These are global flags — place them before or after the command.

## Configuration

```bash
agent-mongo config list-keys                             # all keys with defaults/ranges
agent-mongo config set defaults.limit 50
agent-mongo config get query.timeout
agent-mongo config reset                                 # restore defaults
```

Key settings: `defaults.limit` (20), `defaults.sampleSize` (5), `defaults.schemaSampleSize` (100), `query.timeout` (30000ms), `query.maxDocuments` (100), `truncation.maxLength` (200).

## Safety

- **Read-only**: No write operations exist
- **Aggregation**: `$out` and `$merge` stages rejected
- **Result cap**: `query.maxDocuments` (default 100)
- **Timeout**: `query.timeout` (default 30s)

## Per-command usage docs

Every command group has a `usage` subcommand with detailed, LLM-optimized docs:

```bash
agent-mongo usage                  # top-level overview
agent-mongo connection usage       # connection + credential commands
agent-mongo credential usage       # credential management
agent-mongo database usage          # database commands
agent-mongo collection usage       # collection commands
agent-mongo query usage            # all query commands
agent-mongo config usage           # settings keys, defaults, validation
```

Use `agent-mongo <command> usage` when you need deep detail on a specific domain before acting.

## References

- [references/commands.md](references/commands.md): full command map + all flags
- [references/output.md](references/output.md): JSON output shapes + field details
