---
name: eclair
description: Run and interact with eclair Lightning Network daemon in Docker. Use for Lightning development, testing payment channels on regtest, managing eclair containers, and calling eclair API endpoints (getinfo, connect, open/close channels, pay/receive).
---

# Eclair Lightning Network Skill

Eclair is a Scala implementation of the Lightning Network. This skill helps you run eclair in Docker for development and testing, primarily on regtest.

## Prerequisites

- Docker and Docker Compose installed
- (Optional) Bitcoin Core if not using the bundled docker-compose

## Quick Start

Start the full regtest stack (Bitcoin Core + Eclair):

```bash
cd ~/.claude/skills/eclair/templates
docker-compose up -d --build   # First time: builds eclair from source (~5-10 min)
docker-compose up -d           # Subsequent runs: uses cached image
```

This starts:
- `bitcoind`: Bitcoin Core 30 in regtest mode with ZMQ
- `eclair`: Eclair 0.14.0-SNAPSHOT (built from local source)

**Notes**:
- Eclair is built from source at `/Users/roasbeef/codez/eclair` because Docker Hub images have a "kill switch" for older versions
- Eclair 0.14+ requires Bitcoin Core 29+, so we use `lightninglabs/bitcoin-core:30`
- First build takes ~5-10 minutes to compile Scala code

Check status:
```bash
docker exec eclair eclair-cli -p devpassword getinfo
```

## Docker Management

### Build Image (from eclair source)

```bash
~/.claude/skills/eclair/scripts/docker-build.sh [--source /path/to/eclair]
```

Or pull pre-built image:
```bash
docker pull acinq/eclair:latest
```

### Start Containers

Using docker-compose (recommended for regtest):
```bash
cd ~/.claude/skills/eclair/templates
docker-compose up -d
```

Using a custom image (e.g., from PR build):
```bash
cd ~/.claude/skills/eclair/templates
ECLAIR_IMAGE=eclair:pr-3144 docker-compose up -d
```

Single eclair container (requires external bitcoind):
```bash
~/.claude/skills/eclair/scripts/docker-start.sh --network regtest
```

### Stop Containers

```bash
cd ~/.claude/skills/eclair/templates
docker-compose down

# To also remove volumes:
docker-compose down -v
```

### View Logs

```bash
docker logs -f eclair
docker logs -f bitcoind
```

### Execute Commands

```bash
docker exec eclair eclair-cli -p devpassword <command>
docker exec bitcoind bitcoin-cli -regtest <command>
```

## Essential API Operations

All commands use the eclair REST API. Default password in regtest: `devpassword`

### Node Information

```bash
# Get node info (nodeId, alias, blockHeight, etc.)
docker exec eclair eclair-cli -p devpassword getinfo

# List connected peers
docker exec eclair eclair-cli -p devpassword peers
```

### Connect to Peers

```bash
# Connect by URI
docker exec eclair eclair-cli -p devpassword connect --uri=<nodeId>@<host>:<port>

# Connect by nodeId (requires DNS or known address)
docker exec eclair eclair-cli -p devpassword connect --nodeId=<nodeId>

# Disconnect
docker exec eclair eclair-cli -p devpassword disconnect --nodeId=<nodeId>
```

### Channel Management

```bash
# Open channel (amount in satoshis)
docker exec eclair eclair-cli -p devpassword open \
  --nodeId=<pubkey> \
  --fundingSatoshis=1000000

# List all channels
docker exec eclair eclair-cli -p devpassword channels

# List channels (short format)
docker exec eclair eclair-cli -p devpassword -s channels

# Get specific channel
docker exec eclair eclair-cli -p devpassword channel --channelId=<id>

# Get channel balances
docker exec eclair eclair-cli -p devpassword channelbalances

# Close channel gracefully
docker exec eclair eclair-cli -p devpassword close --channelId=<id>

# Force close channel
docker exec eclair eclair-cli -p devpassword forceclose --channelId=<id>
```

### Payments

```bash
# Create invoice (amount in millisatoshis)
docker exec eclair eclair-cli -p devpassword createinvoice \
  --description="test payment" \
  --amountMsat=100000000

# Parse invoice to see details
docker exec eclair eclair-cli -p devpassword parseinvoice --invoice=<bolt11>

# Pay invoice
docker exec eclair eclair-cli -p devpassword payinvoice --invoice=<bolt11>

# Check sent payment status
docker exec eclair eclair-cli -p devpassword getsentinfo --paymentHash=<hash>

# Check received payment status
docker exec eclair eclair-cli -p devpassword getreceivedinfo --paymentHash=<hash>
```

### On-Chain Wallet

```bash
# Get new address
docker exec eclair eclair-cli -p devpassword getnewaddress

# Get on-chain balance
docker exec eclair eclair-cli -p devpassword onchainbalance

# Get global balance (on-chain + channels)
docker exec eclair eclair-cli -p devpassword globalbalance

# Send on-chain
docker exec eclair eclair-cli -p devpassword sendonchain \
  --address=<btc_address> \
  --amountSatoshis=50000 \
  --confirmationTarget=6
```

### Usable Balances

```bash
# Check how much you can send across all channels
docker exec eclair eclair-cli -p devpassword usablebalances
```

## Regtest Development Workflow

### 1. Start the Stack

```bash
cd ~/.claude/skills/eclair/templates
docker-compose up -d
```

### 2. Fund the Eclair Wallet

```bash
# Generate blocks to have spendable coins
docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin generatetoaddress 101 $(docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin getnewaddress)

# Get eclair address
ECLAIR_ADDR=$(docker exec eclair eclair-cli -p devpassword getnewaddress)

# Send funds to eclair
docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin sendtoaddress $ECLAIR_ADDR 10

# Mine a block to confirm
docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin generatetoaddress 1 $(docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin getnewaddress)

# Verify eclair balance
docker exec eclair eclair-cli -p devpassword onchainbalance
```

### 3. Open a Channel (with second node)

To test channels, you'll need a second Lightning node. You can start another eclair instance or use a different implementation.

```bash
# Connect to peer
docker exec eclair eclair-cli -p devpassword connect --uri=<nodeId>@<host>:9735

# Open 1M sat channel
docker exec eclair eclair-cli -p devpassword open --nodeId=<nodeId> --fundingSatoshis=1000000

# Mine blocks to confirm channel
docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin generatetoaddress 6 $(docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin getnewaddress)

# Check channel status
docker exec eclair eclair-cli -p devpassword -s channels
```

### 4. Send a Payment

```bash
# On receiving node: create invoice
INVOICE=$(docker exec eclair2 eclair-cli -p devpassword createinvoice --amountMsat=50000000 --description="test" | jq -r .serialized)

# On sending node: pay invoice
docker exec eclair eclair-cli -p devpassword payinvoice --invoice=$INVOICE
```

## Using the Helper Scripts

### docker-build.sh
Build eclair Docker image from source (useful for ARM64/Apple Silicon):
```bash
~/.claude/skills/eclair/scripts/docker-build.sh --source /path/to/eclair
```

Build from a specific branch, commit, or GitHub PR (for interop testing):
```bash
# Build from a specific branch
~/.claude/skills/eclair/scripts/docker-build.sh --branch taproot-feature-bit

# Build from a GitHub PR (requires gh CLI)
~/.claude/skills/eclair/scripts/docker-build.sh --pr 3144

# Build from a specific commit
~/.claude/skills/eclair/scripts/docker-build.sh --commit ea9c4ca8dc1403bca6c6dcbe9bc4f3bd81d76513

# Combine with custom tag
~/.claude/skills/eclair/scripts/docker-build.sh --pr 3144 --tag eclair:taproot
```

### build-pr.sh
Quick convenience wrapper for building from a GitHub PR:
```bash
~/.claude/skills/eclair/scripts/build-pr.sh 3144   # Builds and tags as eclair:pr-3144
```

### docker-start.sh
Start eclair with custom configuration:
```bash
~/.claude/skills/eclair/scripts/docker-start.sh \
  --network regtest \
  --api-password mypassword \
  --data-dir /tmp/eclair-data
```

### docker-stop.sh
Stop and optionally clean up:
```bash
~/.claude/skills/eclair/scripts/docker-stop.sh
~/.claude/skills/eclair/scripts/docker-stop.sh --clean  # Also removes volumes
```

### eclair-cli.sh
Convenient wrapper for eclair API:
```bash
~/.claude/skills/eclair/scripts/eclair-cli.sh getinfo
~/.claude/skills/eclair/scripts/eclair-cli.sh channels
~/.claude/skills/eclair/scripts/eclair-cli.sh createinvoice --amountMsat=100000000 --description="test"
```

### regtest-setup.sh
Initialize regtest environment with funded wallet:
```bash
~/.claude/skills/eclair/scripts/regtest-setup.sh
```

### mine.sh
Mine blocks in regtest:
```bash
~/.claude/skills/eclair/scripts/mine.sh        # Mine 1 block
~/.claude/skills/eclair/scripts/mine.sh 6      # Mine 6 blocks (confirm channel)
~/.claude/skills/eclair/scripts/mine.sh 100    # Mine 100 blocks (coinbase maturity)
```

### bitcoin-cli.sh
Wrapper for Bitcoin Core commands:
```bash
~/.claude/skills/eclair/scripts/bitcoin-cli.sh getblockchaininfo
~/.claude/skills/eclair/scripts/bitcoin-cli.sh getbalance
~/.claude/skills/eclair/scripts/bitcoin-cli.sh sendtoaddress <address> <amount>
```

## Bitcoin Core Control

The bitcoind container is fully accessible for controlling the regtest blockchain.

### Mining Blocks

```bash
# Using the helper script
~/.claude/skills/eclair/scripts/mine.sh 6

# Or directly
docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin \
  generatetoaddress 6 $(docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin getnewaddress)
```

### Blockchain Info

```bash
~/.claude/skills/eclair/scripts/bitcoin-cli.sh getblockchaininfo
~/.claude/skills/eclair/scripts/bitcoin-cli.sh getmempoolinfo
~/.claude/skills/eclair/scripts/bitcoin-cli.sh getblockcount
```

### Wallet Operations

```bash
# Get balance
~/.claude/skills/eclair/scripts/bitcoin-cli.sh getbalance

# Generate address
~/.claude/skills/eclair/scripts/bitcoin-cli.sh getnewaddress

# Send funds
~/.claude/skills/eclair/scripts/bitcoin-cli.sh sendtoaddress <address> 1.0
```

### Connecting Other Lightning Nodes (lnd, c-lightning)

The bitcoind container exposes all ports to the host, allowing other Lightning implementations to connect:

| Port | Protocol | Usage |
|------|----------|-------|
| 18443 | RPC | Bitcoin Core RPC (regtest) |
| 18444 | P2P | Bitcoin Core P2P (regtest) |
| 28332 | ZMQ | Block notifications |
| 28333 | ZMQ | Transaction notifications |

Example lnd configuration to connect to the shared bitcoind:
```ini
[Bitcoin]
bitcoin.active=1
bitcoin.regtest=1
bitcoin.node=bitcoind

[Bitcoind]
bitcoind.rpchost=localhost:18443
bitcoind.rpcuser=bitcoin
bitcoind.rpcpass=bitcoin
bitcoind.zmqpubrawblock=tcp://localhost:28332
bitcoind.zmqpubrawtx=tcp://localhost:28333
```

Example c-lightning/CLN configuration:
```ini
network=regtest
bitcoin-rpcconnect=localhost
bitcoin-rpcport=18443
bitcoin-rpcuser=bitcoin
bitcoin-rpcpassword=bitcoin
```

## Configuration

Key configuration options (set via environment variables or eclair.conf):

| Option | Description | Default |
|--------|-------------|---------|
| `eclair.chain` | Network: mainnet, testnet, signet, regtest | regtest |
| `eclair.api.enabled` | Enable REST API | true |
| `eclair.api.password` | API authentication password | (required) |
| `eclair.api.port` | API port | 8080 |
| `eclair.node-alias` | Node name visible on network | eclair |
| `eclair.bitcoind.host` | Bitcoin Core host | bitcoind |
| `eclair.bitcoind.rpcuser` | Bitcoin Core RPC user | bitcoin |
| `eclair.bitcoind.rpcpassword` | Bitcoin Core RPC password | bitcoin |

See [templates/eclair.conf.template](templates/eclair.conf.template) for full configuration.

## Ports

| Port | Service | Description |
|------|---------|-------------|
| 9735 | Lightning | Peer-to-peer Lightning protocol |
| 8080 | API | REST API and WebSocket |
| 18443 | Bitcoin RPC | Bitcoin Core RPC (regtest) |
| 28332 | Bitcoin ZMQ | Bitcoin Core ZMQ notifications |

## Troubleshooting

### "Connection refused" to API
- Ensure eclair container is running: `docker ps`
- Check logs: `docker logs eclair`
- Verify API is enabled in config

### "Unauthorized" API response
- Check password matches `eclair.api.password` in config
- Default regtest password: `devpassword`

### Channel stuck in "WAIT_FOR_FUNDING_CONFIRMED"
- Mine more blocks: `docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin generatetoaddress 6 $(docker exec bitcoind bitcoin-cli -regtest -rpcuser=bitcoin -rpcpassword=bitcoin getnewaddress)`

### "Insufficient funds"
- Check on-chain balance: `eclair-cli onchainbalance`
- Fund wallet from bitcoind (see regtest workflow above)

### Bitcoin Core connection failed
- Verify bitcoind is running: `docker ps`
- Check ZMQ is enabled and ports match
- Verify RPC credentials match between bitcoind and eclair config

### Building on Apple Silicon (ARM64)
Use the docker-build.sh script which handles ARM64 builds:
```bash
~/.claude/skills/eclair/scripts/docker-build.sh --source /path/to/eclair
```

## Interop Testing with Custom Branches/PRs

For testing in-development features across Lightning implementations:

### Testing a GitHub PR

```bash
# Build and tag from PR #3144 (taproot feature bit)
~/.claude/skills/eclair/scripts/build-pr.sh 3144

# Or manually with docker-build.sh
~/.claude/skills/eclair/scripts/docker-build.sh --pr 3144 --tag eclair:taproot

# Start the stack with the PR image
cd ~/.claude/skills/eclair/templates
ECLAIR_IMAGE=eclair:pr-3144 docker-compose up -d --build
```

### Testing a Feature Branch

```bash
# Build from taproot-feature-bit branch
~/.claude/skills/eclair/scripts/docker-build.sh --branch taproot-feature-bit --tag eclair:taproot

# Start the stack
cd ~/.claude/skills/eclair/templates
ECLAIR_IMAGE=eclair:taproot docker-compose up -d
```

### Environment Variables for docker-compose

| Variable | Description | Default |
|----------|-------------|---------|
| `ECLAIR_SOURCE` | Path to eclair source directory | /Users/roasbeef/codez/eclair |
| `ECLAIR_IMAGE` | Docker image tag to use | eclair:local |

## Further Reading

- [API Reference](references/api-reference.md) - Complete API endpoint documentation
- [Eclair GitHub](https://github.com/ACINQ/eclair) - Official repository
- [BOLT Specifications](https://github.com/lightning/bolts) - Lightning Network protocol specs
