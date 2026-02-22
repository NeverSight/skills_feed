---
name: cypher-shell
description: "Neo4j Cypher Shell skill. Connect to instances, run Cypher queries, and retrieve full graph schemas via cypher-shell CLI."
disable-model-invocation: true
---

# cypher-shell

Neo4j Cypher Shell skill. Connect once, query fast, inspect schemas.

## Connection Config

`connect` writes `~/.neo4j-connection` (env vars) **and** injects a one-line loader into the user's shell profile (`~/.zshrc`, `~/.bashrc`, or `~/.profile`). After that, every new Bash invocation has credentials loaded automatically via native cypher-shell env vars:

| Env Var | cypher-shell flag |
|---------|------------------|
| `NEO4J_URI` | `-a, --address, --uri` |
| `NEO4J_USERNAME` | `-u, --username` |
| `NEO4J_PASSWORD` | `-p, --password` |
| `NEO4J_DATABASE` | `-d, --database` |

**Execution pattern** (after connect):

```bash
cypher-shell --format verbose "<QUERY>"
```

No `source`, no flags, no credentials. Just `cypher-shell` + query.

Pre-flight for every command (except `connect` and `install`): verify env var `NEO4J_URI` is set. If not:

```bash
if [ -z "$NEO4J_URI" ]; then echo "Not connected. Run /cypher-shell connect <uri>"; exit 1; fi
```

---

## Route $ARGUMENTS

Parse the **first word** of `$ARGUMENTS` to determine the action:

| First word | Action |
|-----------|--------|
| `connect` | Connect to instance |
| `query` | Run Cypher query |
| `schema` | Retrieve graph schema |
| `test` | Test current connection |
| `install` | Show install instructions |
| _(none)_ | Show usage help |

Everything after the first word becomes the sub-argument.

---

## connect [URI]

### With URI (contains `://`)

1. Ask user for username (default: `neo4j`) and password
2. Optionally ask for database name
3. Write credentials file:

```bash
cat > ~/.neo4j-connection << 'EOF'
export NEO4J_URI="<uri>"
export NEO4J_USERNAME="<user>"
export NEO4J_PASSWORD="<pass>"
export NEO4J_DATABASE="<db>"
EOF
chmod 600 ~/.neo4j-connection
```

4. **Inject loader into shell profile** so every future shell session auto-loads credentials. Detect the profile file and append the loader line **only if not already present**:

```bash
# Detect shell profile
if [ -f ~/.zshrc ]; then
  SHELL_PROFILE=~/.zshrc
elif [ -f ~/.bashrc ]; then
  SHELL_PROFILE=~/.bashrc
elif [ -f ~/.bash_profile ]; then
  SHELL_PROFILE=~/.bash_profile
else
  SHELL_PROFILE=~/.profile
fi

# Append loader only if not already there
LOADER='[ -f ~/.neo4j-connection ] && source ~/.neo4j-connection'
grep -qF "$LOADER" "$SHELL_PROFILE" 2>/dev/null || echo "$LOADER" >> "$SHELL_PROFILE"
```

5. **Load credentials into current session** (so this session works immediately without restart):

```bash
source ~/.neo4j-connection
```

6. Test connection: `cypher-shell "RETURN 'connected' AS status;"`
7. On success, fetch server info:

```bash
cypher-shell --format verbose \
  "CALL dbms.components() YIELD name, versions, edition RETURN name, versions[0] AS version, edition;"
```

```bash
cypher-shell --format verbose \
  "SHOW DATABASES YIELD name, currentStatus, default RETURN name, currentStatus, default ORDER BY name;"
```

Report: version, edition, databases, URI. Confirm that credentials are persisted and no flags needed going forward.

### Without URI

If `~/.neo4j-connection` exists, show current config (mask password). Otherwise ask for URI.

### Protocol schemes

| Scheme | Encryption | Routing |
|--------|-----------|---------|
| `neo4j://` | None | Yes (cluster) |
| `neo4j+s://` | TLS (CA-verified) | Yes |
| `neo4j+ssc://` | TLS (self-signed) | Yes |
| `bolt://` | None | No (single) |
| `bolt+s://` | TLS (CA-verified) | No |
| `bolt+ssc://` | TLS (self-signed) | No |

---

## test

1. Verify `NEO4J_URI` env var is set (if not, tell user to run `/cypher-shell connect <uri>`)
2. `cypher-shell "RETURN 'ok' AS status;"`
3. Show: URI, user, database, version

### Troubleshooting (if test fails)

1. `which cypher-shell` — not found? -> `install`
2. `java -version` — need 21+
3. `nc -z -w3 <host> <port>` — port not open? Neo4j not running
4. Auth error — reset at http://localhost:7474 or `cypher-shell --change-password`
5. TLS error — try `neo4j+ssc://` or `bolt://`

---

## install

Print install instructions for the user (do NOT run them):

- **macOS**: `brew install cypher-shell`
- **Debian/Ubuntu**: `curl -fsSL https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/neo4j.gpg && echo 'deb [signed-by=/usr/share/keyrings/neo4j.gpg] https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list && sudo apt-get update && sudo apt-get install -y cypher-shell`
- **Docker**: `docker run --rm -it --network host neo4j/neo4j:latest cypher-shell`

Requires **Java 21+**.

---

## query [CYPHER or shortcut]

### Full Cypher

If sub-argument contains Cypher keywords (`MATCH`, `CREATE`, `MERGE`, `CALL`, `SHOW`, `RETURN`, `WITH`, `UNWIND`, `LOAD`, `DROP`, `DELETE`, `EXPLAIN`, `PROFILE`, `FILTER`, `LET`, `SEARCH`, `FINISH`), run directly:

```bash
cypher-shell --format verbose "<sub-argument>"
```

### Shortcuts

| Shortcut | Query |
|----------|-------|
| `count` | `MATCH (n) RETURN labels(n) AS label, count(n) AS count ORDER BY count DESC;` then `MATCH ()-[r]->() RETURN type(r) AS type, count(r) AS count ORDER BY count DESC;` |
| `orphans` | `MATCH (n) WHERE NOT (n)--() RETURN labels(n) AS label, n.name AS name, count(*) AS count ORDER BY count DESC;` |
| `indexes` | `SHOW INDEXES YIELD name, type, labelsOrTypes, properties, state RETURN name, type, labelsOrTypes, properties, state;` |
| `constraints` | `SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties RETURN name, type, labelsOrTypes, properties;` |
| `wipe` | **WARN + ASK CONFIRMATION** then `CALL { MATCH (n) WITH n LIMIT 10000 DETACH DELETE n } IN TRANSACTIONS OF 10000 ROWS;` then verify `MATCH (n) RETURN count(n) AS remaining;` |

### No sub-argument -> show shortcuts list.

---

## schema [Label]

### Full schema (no label argument)

Run ALL and present formatted summary:

```cypher
MATCH (n) RETURN labels(n) AS label, count(n) AS count ORDER BY count DESC;
```
```cypher
MATCH ()-[r]->() RETURN type(r) AS type, count(r) AS count ORDER BY count DESC;
```
```cypher
MATCH (a)-[r]->(b) RETURN DISTINCT labels(a) AS from_label, type(r) AS relationship, labels(b) AS to_label ORDER BY from_label, relationship, to_label;
```
```cypher
MATCH (n) WITH labels(n) AS lbls, keys(n) AS props RETURN DISTINCT lbls AS label, props AS properties ORDER BY lbls;
```
```cypher
MATCH ()-[r]->() WITH type(r) AS rel, keys(r) AS props WHERE size(props) > 0 RETURN DISTINCT rel AS relationship, props AS properties ORDER BY rel;
```
```cypher
SHOW INDEXES YIELD name, type, labelsOrTypes, properties, state RETURN name, type, labelsOrTypes, properties, state ORDER BY name;
```
```cypher
SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties RETURN name, type, labelsOrTypes, properties ORDER BY name;
```

Present as ASCII schema map:

```
Graph Schema
============
Nodes: X total across Y labels
Rels: Z total across W types

[File] (145)  props: name, path, language
  --[:CONTAINS]--> [Function]
  --[:IMPORTS]--> [File]

[Function] (312)  props: name, file, line
  --[:CALLS]--> [Function]

Indexes: idx_file_path RANGE :File(path) ONLINE
Constraints: uniq_file_id UNIQUENESS :File(id)
```

### Label deep-dive (argument matches a label)

```cypher
MATCH (n:<LABEL>) RETURN n LIMIT 5;
```
```cypher
MATCH (n:<LABEL>) WITH n LIMIT 100 UNWIND keys(n) AS key
RETURN DISTINCT key AS property, head(collect(DISTINCT valueType(n[key]))) AS type, count(*) AS present_in ORDER BY present_in DESC;
```
```cypher
MATCH (n:<LABEL>)-[r]->(m) RETURN type(r) AS rel, labels(m) AS target, count(*) AS count ORDER BY count DESC;
```
```cypher
MATCH (n:<LABEL>)<-[r]-(m) RETURN type(r) AS rel, labels(m) AS source, count(*) AS count ORDER BY count DESC;
```
```cypher
MATCH (n:<LABEL>) RETURN count(n) AS total;
```
```cypher
MATCH (n:<LABEL>) WHERE NOT (n)--() RETURN count(n) AS orphans;
```

---

## cypher-shell CLI Reference

### Key flags

| Flag | Description | Default |
|------|-------------|---------|
| `-a, --address, --uri` | Connection URI | `neo4j://localhost:7687` |
| `-u, --username` | Username | env `NEO4J_USERNAME` |
| `-p, --password` | Password | env `NEO4J_PASSWORD` |
| `-d, --database` | Database | env `NEO4J_DATABASE` |
| `-f, --file FILE` | Execute .cypher file | — |
| `-P, --param` | Set params: `-P '{a: 1}'` | `[]` |
| `--format {auto,verbose,plain}` | Output format | `auto` |
| `--access-mode {read,write}` | Access mode | `write` |
| `--non-interactive` | Force non-interactive | `false` |
| `--fail-fast / --fail-at-end` | Error handling for files | `fail-fast` |
| `--sample-rows N` | Rows for table width | `1000` |
| `--wrap {true,false}` | Wrap long columns | `true` |
| `--transaction-timeout` | e.g. `10m`, `1h30m` | `disable` |
| `--error-format {gql,legacy,stacktrace}` | Error display | `gql` |
| `--encryption {true,false,default}` | Encryption | `default` |
| `--impersonate USER` | Run as user | — |
| `--change-password` | Change password | — |
| `--enable-autocompletions` | Tab-complete (5+) | `false` |
| `--notifications` | Query notifications | `false` |
| `--idle-timeout` | Auto-exit | `disable` |
| `--log [FILE]` | Debug log | — |
| `-v, --version` | Version | — |

### Shell commands (interactive)

`:help` `:exit` `:use <db>` `:source <file>` `:param {k:v}` `:param k => expr` `:param` (list) `:param clear` `:begin` `:commit` `:rollback` `:history` `:connect` `:disconnect` `:sysinfo` `:impersonate` `:access-mode [read|write]`

### Cypher quick patterns

```cypher
MATCH (n:Label {prop: "val"}) RETURN n;
MATCH (a)-[:REL]->(b) RETURN a.name, b.name;
MATCH path = (a)-[*1..3]->(b) WHERE a.name = "x" RETURN path;
MATCH path = shortestPath((a {name:"x"})-[*]-(b {name:"y"})) RETURN path;
MATCH (n:Label) RETURN n.prop, count(n) ORDER BY count(n) DESC;
MERGE (n:Label {id: "x"}) ON CREATE SET n.created = timestamp() ON MATCH SET n.updated = timestamp();
CALL { MATCH (n:Label) WITH n LIMIT 10000 DETACH DELETE n } IN TRANSACTIONS OF 10000 ROWS;
LOAD CSV WITH HEADERS FROM 'file:///data.csv' AS row CREATE (:Label {name: row.name});
EXPLAIN MATCH (n)-[r]->(m) RETURN n, r, m;
PROFILE MATCH (n)-[r]->(m) RETURN n, r, m;
```

Cypher 25 (Neo4j 2025.06+): `FILTER`, `LET`, `FINISH`, `WHEN`, `NEXT`, `SEARCH` (vector), `coll.distinct/flatten/indexOf/insert/max/min/remove/sort`.
