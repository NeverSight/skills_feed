---
name: arweave
description: Upload files and websites to permanent storage on Arweave (permaweb), and manage ArNS domain records. Use when the user wants to publish content to Arweave, deploy a static site to the permaweb, or attach a transaction to an ArNS name (ar.io).
compatibility: Requires Node.js 18+, internet access, and an Arweave wallet (JWK format)
metadata:
  author: rakis
  version: "0.0.1"
---

# Arweave Upload & ArNS Skill

Upload files and websites to permanent storage on Arweave, and manage ArNS (Arweave Name System) domain records.

## Phrase Mappings

| User Request | Command |
|--------------|---------|
| "use arweave to upload `<file>`" | `upload` |
| "use arweave to upload `<dir>`" | `upload-site` |
| "use arweave to attach `<txId>` to `<name>`" | `attach` |
| "use arweave to query transactions" | `query` |

## Wallet Handling

**Important**: This skill requires an Arweave wallet file (JWK format).

- If the user has not provided a wallet path, **ask them for it** before proceeding
- Pass the wallet path via `--wallet <path>` argument
- **Never expose or log wallet contents**

## Commands

### Upload a Single File

```sh
node skills/arweave/index.mjs upload "<file>" --wallet "<path/to/wallet.json>"
```

### Upload a Website/Directory

```sh
node skills/arweave/index.mjs upload-site "<directory>" --index "index.html" --wallet "<path/to/wallet.json>"
```

- `--index` specifies the default file served at the root (defaults to `index.html`)
- The returned `txId` is the **manifest transaction** that serves the entire site

### Attach Transaction to ArNS Name

```sh
node skills/arweave/index.mjs attach "<txId>" "<name>" --wallet "<path/to/wallet.json>" --yes
```

**Options:**
- `--ttl <seconds>` - Time-to-live in seconds (default: 3600)
- `--network <mainnet|testnet>` - Network to use (default: mainnet)
- `--ario-process <id>` - Override network with specific ARIO process ID
- `--yes` - Skip confirmation prompts

**Propagation:** Updates usually appear within a few minutes, but can take up to ~30 minutes to reflect everywhere (gateway/operator caches and client TTLs).

## ArNS Name Format

- Names with underscore like `hello_rakis` mean **undername** `hello` on base name `rakis`
- Strip `.ar.io` suffix if present (e.g., `rakis.ar.io` becomes `rakis`)

Examples:
- `rakis` - base name (updates `@` record)
- `hello_rakis` - undername `hello` under base `rakis`
- `docs_myproject` - undername `docs` under base `myproject`

## Network Selection

By default, the skill uses **mainnet**. You can specify a different network:

```sh
# Use mainnet (default)
node skills/arweave/index.mjs attach "<txId>" "<name>" --network mainnet --wallet "..." --yes

# Use testnet
node skills/arweave/index.mjs attach "<txId>" "<name>" --network testnet --wallet "..." --yes

# Use specific ARIO process ID (overrides --network)
node skills/arweave/index.mjs attach "<txId>" "<name>" --ario-process "<processId>" --wallet "..." --yes
```

## Output Handling

After successful upload, report back:

1. **Transaction ID** (`txId`)
2. **Gateway URL**: `https://arweave.net/<txId>`

Example response to user:
```
Uploaded successfully!
- Transaction ID: abc123xyz...
- View at: https://arweave.net/abc123xyz...
```

For site uploads, clarify that the txId represents the manifest transaction serving the entire site.

### Query Transactions

```sh
node skills/arweave/index.mjs query [options]
```

Search and filter Arweave transactions using the GraphQL endpoint.

**Options:**

- `--tag <name:value>` - Filter by tag (can specify multiple, uses AND logic)
- `--owner <address>` - Filter by owner wallet address
- `--recipient <address>` - Filter by recipient wallet address
- `--ids <comma-separated>` - Query specific transaction IDs
- `--block-min <height>` - Minimum block height
- `--block-max <height>` - Maximum block height
- `--limit <number>` - Max results to return (default: 10, set to 0 for all)
- `--sort <HEIGHT_DESC|HEIGHT_ASC>` - Sort order (default: HEIGHT_DESC)

**Tag Syntax:**

Tags use the format `name:value`. Multiple `--tag` flags apply AND logic (all conditions must match).

```sh
# Single tag
--tag "Content-Type:text/html"

# Multiple tags (both must match)
--tag "Content-Type:text/html" --tag "User-Agent:ArweaveAutoDPL/0.1"
```

**Pagination:**

- Default limit is 10 transactions
- Use `--limit 0` to fetch all matching results
- Large queries may take time; consider narrowing filters for faster results

**Examples:**

```sh
# Query last 10 recent transactions
node skills/arweave/index.mjs query --sort HEIGHT_DESC

# Find all HTML content (fetch all results)
node skills/arweave/index.mjs query --tag "Content-Type:text/html" --limit 0

# Query by owner with custom limit
node skills/arweave/index.mjs query --owner "M6w588ZkR8SVFdPkNXdBy4sqbMN0Y3F8ZJUWm2WCm8M" --limit 50

# Multiple tags (AND logic: both conditions must match)
node skills/arweave/index.mjs query \
  --tag "Content-Type:text/html" \
  --tag "User-Agent:ArweaveAutoDPL/0.1" \
  --limit 20

# Query block height range
node skills/arweave/index.mjs query --block-min 587540 --block-max 587550 --limit 100

# Combine filters: HTML in specific block range, oldest first
node skills/arweave/index.mjs query \
  --tag "Content-Type:text/html" \
  --block-min 587540 \
  --block-max 587550 \
  --sort HEIGHT_ASC

# Query specific transaction IDs
node skills/arweave/index.mjs query --ids "abc123,def456,ghi789"

# Find transactions from specific recipient
node skills/arweave/index.mjs query --recipient "M6w588ZkR8SVFdPkNXdBy4sqbMN0Y3F8ZJUWm2WCm8M" --limit 25
```

### GraphQL Endpoint Fallback

The `query` command automatically tries multiple GraphQL endpoints for reliability:

1. `https://arweave.net/graphql` (primary - official gateway)
2. `https://arweave-search.goldsky.com/graphql` (fallback - Goldsky indexer)
3. `https://g8way.io/graphql` (fallback - alternative gateway)

This happens **transparently** - the command uses whichever endpoint responds first. You don't need to do anything; it just works.

#### Custom Endpoint Override

To use a specific GraphQL endpoint (useful for testing or private gateways):

```sh
# Use a custom endpoint
node skills/arweave/index.mjs query --tag "Content-Type:text/html" --limit 5 \
  --graphql-endpoint "https://custom-gateway.com/graphql"

# Force use of a specific public endpoint
node skills/arweave/index.mjs query --owner <address> --limit 10 \
  --graphql-endpoint "https://g8way.io/graphql"
```

**Note**: When `--graphql-endpoint` is provided, the automatic fallback is disabled. Only the specified endpoint will be tried.

## Example Invocations

```sh
# Upload a single markdown file
node skills/arweave/index.mjs upload "foo.md" --wallet "/path/to/wallet.json"

# Upload a website directory
node skills/arweave/index.mjs upload-site "./mywebsite" --index "index.html" --wallet "/path/to/wallet.json"

# Attach a transaction to an ArNS undername (mainnet)
node skills/arweave/index.mjs attach "<txId>" "hello_rakis" --ttl 3600 --network mainnet --wallet "/path/to/wallet.json" --yes

# Attach to testnet
node skills/arweave/index.mjs attach "<txId>" "hello_rakis" --network testnet --wallet "/path/to/wallet.json" --yes

# Attach using specific ARIO process
node skills/arweave/index.mjs attach "<txId>" "hello_rakis" --ario-process testnet --wallet "/path/to/wallet.json" --yes
```
