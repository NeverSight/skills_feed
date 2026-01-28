---
name: lnd
description: Run and interact with lnd Lightning Network daemon in Docker. Use for Lightning development, testing payment channels on regtest, managing lnd containers, and calling lnd RPC endpoints (getinfo, connect, open/close channels, pay/receive). Supports bitcoind, btcd, and neutrino backends.
---

# LND Lightning Network Skill

LND (Lightning Network Daemon) is a complete implementation of a Lightning Network node. This skill helps you run lnd in Docker for development and testing, with support for multiple backends.

## Prerequisites

- Docker and Docker Compose installed
- (Optional) `gh` CLI for building from GitHub PRs

## Quick Start

Start the full regtest stack (Bitcoin Core + LND):

```bash
cd ~/.claude/skills/lnd/templates
docker-compose up -d --build   # First time: builds lnd from source (~3-5 min)
docker-compose up -d           # Subsequent runs: uses cached image
```

This starts:
- `lnd-bitcoind`: Bitcoin Core 30 in regtest mode with ZMQ
- `lnd`: LND built from local source

**Notes**:
- LND is built from source at `/users/roasbeef/gocode/src/github.com/lightningnetwork/lnd`
- First build takes ~3-5 minutes to compile Go code
- Uses `--noseedbackup` for testing (no wallet seed required)

Check status:
```bash
~/.claude/skills/lnd/scripts/lncli.sh getinfo
```

## Backend Options

LND supports three backend options:

| Backend | Description | Best For |
|---------|-------------|----------|
| **bitcoind** | Bitcoin Core | Production, regtest development, interop testing |
| **btcd** | btcd (Go implementation) | Simnet testing, fast iteration |
| **neutrino** | Light client (BIP 157/158) | Testnet, mobile simulation |

### Standalone Mode (bitcoind backend - default)
```bash
cd ~/.claude/skills/lnd/templates
docker-compose up -d
```

### Shared Mode (interop with eclair)
```bash
# First start eclair's stack
cd ~/.claude/skills/eclair/templates
docker-compose up -d

# Then start lnd using eclair's bitcoind
cd ~/.claude/skills/lnd/templates
docker-compose -f docker-compose-shared.yml up -d
```

### btcd Mode (simnet)
```bash
cd ~/.claude/skills/lnd/templates
docker-compose -f docker-compose-btcd.yml up -d
```

### Neutrino Mode (light client)
```bash
cd ~/.claude/skills/lnd/templates
docker-compose -f docker-compose-neutrino.yml up -d

# Or with signet
NETWORK=signet docker-compose -f docker-compose-neutrino.yml up -d
```

## Docker Management

### Build Image (from lnd source)

```bash
# Build from current source
~/.claude/skills/lnd/scripts/docker-build.sh

# Build from a specific branch
~/.claude/skills/lnd/scripts/docker-build.sh --branch simple-taproot-chans

# Build from a GitHub PR
~/.claude/skills/lnd/scripts/docker-build.sh --pr 1234

# Build from a specific commit
~/.claude/skills/lnd/scripts/docker-build.sh --commit abc123

# Quick PR build (convenience wrapper)
~/.claude/skills/lnd/scripts/build-pr.sh 1234
```

### Start Containers

```bash
# Start standalone stack (bitcoind + lnd)
~/.claude/skills/lnd/scripts/docker-start.sh

# Start in shared mode (uses external bitcoind)
~/.claude/skills/lnd/scripts/docker-start.sh --shared

# Start with btcd backend
~/.claude/skills/lnd/scripts/docker-start.sh --btcd

# Start in neutrino mode
~/.claude/skills/lnd/scripts/docker-start.sh --neutrino

# Rebuild before starting
~/.claude/skills/lnd/scripts/docker-start.sh --build
```

### Stop Containers

```bash
# Stop containers (preserve data)
~/.claude/skills/lnd/scripts/docker-stop.sh

# Stop and remove volumes (clean state)
~/.claude/skills/lnd/scripts/docker-stop.sh --clean
```

### View Logs

```bash
docker logs -f lnd
docker logs -f lnd-bitcoind
```

## Essential lncli Operations

All commands use `lncli.sh` wrapper which auto-detects the lnd container.

### Node Information

```bash
# Get node info
~/.claude/skills/lnd/scripts/lncli.sh getinfo

# Get wallet balance (on-chain)
~/.claude/skills/lnd/scripts/lncli.sh walletbalance

# Get channel balance (Lightning)
~/.claude/skills/lnd/scripts/lncli.sh channelbalance
```

### Wallet & Addresses

```bash
# Get new address (native SegWit)
~/.claude/skills/lnd/scripts/lncli.sh newaddress p2wkh

# Get new address (nested SegWit)
~/.claude/skills/lnd/scripts/lncli.sh newaddress np2wkh

# Get new Taproot address
~/.claude/skills/lnd/scripts/lncli.sh newaddress p2tr

# Send on-chain
~/.claude/skills/lnd/scripts/lncli.sh sendcoins --addr=<address> --amt=<satoshis>
```

### Connect to Peers

```bash
# Connect by URI
~/.claude/skills/lnd/scripts/lncli.sh connect <pubkey>@<host>:9735

# List connected peers
~/.claude/skills/lnd/scripts/lncli.sh listpeers

# Disconnect
~/.claude/skills/lnd/scripts/lncli.sh disconnect <pubkey>
```

### Channel Management

```bash
# Open channel
~/.claude/skills/lnd/scripts/lncli.sh openchannel --node_key=<pubkey> --local_amt=1000000

# List channels
~/.claude/skills/lnd/scripts/lncli.sh listchannels

# Get channel balance
~/.claude/skills/lnd/scripts/lncli.sh channelbalance

# Close channel cooperatively
~/.claude/skills/lnd/scripts/lncli.sh closechannel --funding_txid=<txid> --output_index=<n>

# Force close channel
~/.claude/skills/lnd/scripts/lncli.sh closechannel --funding_txid=<txid> --output_index=<n> --force
```

### Payments

```bash
# Create invoice
~/.claude/skills/lnd/scripts/lncli.sh addinvoice --amt=<satoshis> --memo="test payment"

# Decode invoice
~/.claude/skills/lnd/scripts/lncli.sh decodepayreq <bolt11_invoice>

# Pay invoice
~/.claude/skills/lnd/scripts/lncli.sh sendpayment --pay_req=<bolt11_invoice>

# List payments
~/.claude/skills/lnd/scripts/lncli.sh listpayments

# List invoices
~/.claude/skills/lnd/scripts/lncli.sh listinvoices
```

## Regtest Development Workflow

### 1. Start the Stack

```bash
cd ~/.claude/skills/lnd/templates
docker-compose up -d
```

### 2. Initialize Regtest Environment

```bash
# Automated setup: mines blocks, funds lnd wallet
~/.claude/skills/lnd/scripts/regtest-setup.sh
```

Or manually:

```bash
# Mine blocks for coinbase maturity
~/.claude/skills/lnd/scripts/mine.sh 101

# Get lnd address
LND_ADDR=$(~/.claude/skills/lnd/scripts/lncli.sh newaddress p2wkh | jq -r '.address')

# Send funds to lnd
~/.claude/skills/lnd/scripts/bitcoin-cli.sh sendtoaddress $LND_ADDR 10

# Confirm transaction
~/.claude/skills/lnd/scripts/mine.sh 1

# Check balance
~/.claude/skills/lnd/scripts/lncli.sh walletbalance
```

### 3. Open a Channel (with second node)

```bash
# Connect to peer
~/.claude/skills/lnd/scripts/lncli.sh connect <nodeId>@<host>:9735

# Open 1M sat channel
~/.claude/skills/lnd/scripts/lncli.sh openchannel --node_key=<nodeId> --local_amt=1000000

# Mine blocks to confirm channel
~/.claude/skills/lnd/scripts/mine.sh 6

# Check channel status
~/.claude/skills/lnd/scripts/lncli.sh listchannels
```

### 4. Send a Payment

```bash
# On receiving node: create invoice
INVOICE=$( lncli addinvoice --amt=50000 --memo="test" | jq -r '.payment_request')

# On sending node: pay invoice
~/.claude/skills/lnd/scripts/lncli.sh sendpayment --pay_req=$INVOICE
```

## Multi-Node Testing

Run multiple lnd nodes for peer-to-peer testing:

### Start Multi-Node Stack

```bash
# Start alice and bob nodes
~/.claude/skills/lnd/scripts/docker-start.sh --multi --build

# Or with docker-compose directly
cd ~/.claude/skills/lnd/templates
docker-compose -f docker-compose-multi.yml up -d --build
```

### Initialize Multi-Node Environment

```bash
# Full setup: fund wallets and open channel between alice and bob
~/.claude/skills/lnd/scripts/multi-node-setup.sh

# Or without channel
~/.claude/skills/lnd/scripts/multi-node-setup.sh --no-channel
```

### Multi-Node Commands

```bash
# Use --node flag to specify which node
~/.claude/skills/lnd/scripts/lncli.sh --node alice getinfo
~/.claude/skills/lnd/scripts/lncli.sh --node bob getinfo

# Get pubkeys
ALICE_PUBKEY=$(~/.claude/skills/lnd/scripts/lncli.sh --node alice getinfo | jq -r '.identity_pubkey')
BOB_PUBKEY=$(~/.claude/skills/lnd/scripts/lncli.sh --node bob getinfo | jq -r '.identity_pubkey')

# Connect nodes
~/.claude/skills/lnd/scripts/lncli.sh --node alice connect ${BOB_PUBKEY}@lnd-bob:9735

# Open channel
~/.claude/skills/lnd/scripts/lncli.sh --node alice openchannel --node_key=$BOB_PUBKEY --local_amt=1000000

# Send payment from alice to bob
INVOICE=$(~/.claude/skills/lnd/scripts/lncli.sh --node bob addinvoice --amt=10000 | jq -r '.payment_request')
~/.claude/skills/lnd/scripts/lncli.sh --node alice sendpayment --pay_req=$INVOICE
```

### Multi-Node Ports

| Node | P2P Port | gRPC Port | REST Port |
|------|----------|-----------|-----------|
| alice | 9735 | 10009 | 8080 |
| bob | 9736 | 10010 | 8081 |
| charlie | 9737 | 10011 | 8082 |

## Interop Testing with Eclair

Test channel operations between lnd and eclair:

```bash
# Terminal 1: Start eclair stack
cd ~/.claude/skills/eclair/templates
docker-compose up -d
~/.claude/skills/eclair/scripts/regtest-setup.sh

# Terminal 2: Start lnd with shared bitcoind
cd ~/.claude/skills/lnd/templates
docker-compose -f docker-compose-shared.yml up -d --build

# Wait for lnd to sync, then run setup
sleep 10
~/.claude/skills/lnd/scripts/regtest-setup.sh --quick

# Get eclair's pubkey
ECLAIR_PUBKEY=$(docker exec eclair eclair-cli -p devpassword getinfo | jq -r '.nodeId')
echo "Eclair pubkey: $ECLAIR_PUBKEY"

# Connect lnd to eclair
~/.claude/skills/lnd/scripts/lncli.sh connect ${ECLAIR_PUBKEY}@eclair:9735

# Open channel from lnd to eclair
~/.claude/skills/lnd/scripts/lncli.sh openchannel --node_key=$ECLAIR_PUBKEY --local_amt=1000000

# Mine to confirm
~/.claude/skills/eclair/scripts/mine.sh 6

# Check channels on both sides
~/.claude/skills/lnd/scripts/lncli.sh listchannels
docker exec eclair eclair-cli -p devpassword channels
```

## Custom Arguments and Profiles

Pass extra arguments to lnd via `LND_EXTRA_ARGS`:

```bash
# Enable REST API on different port
LND_EXTRA_ARGS="--restlisten=0.0.0.0:8081" docker-compose up -d

# Enable debug logging for specific subsystems
LND_EXTRA_ARGS="--debuglevel=HSWC=trace,PEER=debug" docker-compose up -d

# Multiple extra args
LND_EXTRA_ARGS="--protocol.wumbo-channels --maxchansize=500000000" docker-compose up -d
```

## Build Tags

LND supports various build tags for optional features:

| Tag | Description |
|-----|-------------|
| `signrpc` | Signing RPC service |
| `walletrpc` | Wallet RPC service |
| `chainrpc` | Chain RPC service |
| `invoicesrpc` | Invoices RPC service |
| `routerrpc` | Router RPC service |
| `peersrpc` | Peers RPC service |
| `neutrinorpc` | Neutrino RPC service |
| `watchtowerrpc` | Watchtower RPC service |
| `kvdb_sqlite` | SQLite database backend |
| `kvdb_postgres` | PostgreSQL database backend |
| `dev` | Development features |

Build with custom tags:
```bash
~/.claude/skills/lnd/scripts/docker-build.sh --tags "signrpc walletrpc routerrpc dev"
```

## Helper Scripts

| Script | Description |
|--------|-------------|
| `docker-build.sh` | Build lnd image with branch/PR/commit support |
| `docker-start.sh` | Start containers with mode selection |
| `docker-stop.sh` | Stop containers, optionally clean volumes |
| `lncli.sh` | Wrapper for lncli with container and node auto-detection |
| `bitcoin-cli.sh` | Wrapper for bitcoin-cli |
| `mine.sh` | Mine regtest blocks |
| `regtest-setup.sh` | Initialize regtest with funded wallet |
| `multi-node-setup.sh` | Initialize multi-node with funded wallets and channels |
| `build-pr.sh` | Quick PR build convenience wrapper |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LND_SOURCE` | Path to lnd source directory | /users/roasbeef/gocode/src/github.com/lightningnetwork/lnd |
| `LND_IMAGE` | Docker image tag | lnd:local |
| `LND_DEBUG` | Log level | debug |
| `LND_EXTRA_ARGS` | Additional lnd arguments | (empty) |
| `NETWORK` | Bitcoin network | regtest |
| `BACKEND` | Backend: bitcoind, btcd, neutrino | bitcoind |

## Ports

| Port | Service | Description |
|------|---------|-------------|
| 9735 | Lightning | Peer-to-peer Lightning protocol |
| 10009 | gRPC | LND RPC (for lncli) |
| 8080 | REST | REST API |
| 18443 | Bitcoin RPC | Bitcoin Core RPC (regtest) |
| 28332 | ZMQ | Block notifications |
| 28333 | ZMQ | Transaction notifications |

## Troubleshooting

### "transport: Error while dialing dial tcp: connection refused"
- LND is still starting up. Wait a few seconds and retry.
- Check logs: `docker logs lnd`

### "unable to find a path to destination"
- No route to the destination. Check channel balances.
- Run: `lncli.sh listchannels` to see local/remote balances

### Channel stuck in "pending open"
- Mine blocks to confirm: `~/.claude/skills/lnd/scripts/mine.sh 6`

### "insufficient funds available"
- Check wallet balance: `lncli.sh walletbalance`
- Fund wallet using regtest-setup.sh

### "rpc error: code = Unknown desc = chain backend is still syncing"
- LND is syncing with the blockchain. Wait for sync to complete.
- Check: `lncli.sh getinfo` and look at `synced_to_chain`

### Build fails with "go: module requires Go X.Y"
- Update Go version or use `--prod` flag for production Dockerfile

## Further Reading

- [API Reference](references/api-reference.md) - gRPC and REST API documentation
- [LND GitHub](https://github.com/lightningnetwork/lnd) - Official repository
- [LND Documentation](https://docs.lightning.engineering/) - Official docs
- [BOLT Specifications](https://github.com/lightning/bolts) - Lightning Network protocol specs
