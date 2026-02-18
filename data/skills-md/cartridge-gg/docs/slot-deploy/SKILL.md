---
name: slot-deploy
description: Create, update, and manage Slot deployments for Katana and Torii services.
---

# Slot Deploy

Manage the lifecycle of Slot deployments — Katana (execution layer) and Torii (indexer).

## Prerequisites

Install the Slot CLI:

```sh
curl -L https://slot.cartridge.sh | bash
```

Authenticate:

```sh
slot auth login
```

For CI/scripts, generate a token and set the `SLOT_AUTH` env var:

```sh
slot auth token
```

## Creating Deployments

### Katana

```sh
slot deployments create <Project Name> katana
```

### Torii

Torii requires a TOML configuration file:

```sh
slot deployments create <Project Name> torii --config <path/to/torii.toml>
```

Minimal `torii.toml`:

```toml
rpc = "https://api.cartridge.gg/x/starknet/mainnet"
world_address = "0x3fa481f41522b90b3684ecfab7650c259a76387fab9c380b7a959e3d4ac69f"
```

Extended config options:

```toml
[indexing]
allowed_origins = ["*"]
index_pending = true
index_transactions = false
polling_interval = 1000
contracts = [
  "erc20:<contract-address>",
  "erc721:<contract-address>"
]

[events]
raw = true
historical = ["namespace-EventName"]
```

When you create a service with a new project name, a team is automatically created.

## Updating Deployments

```sh
slot deployments update <Project Name> torii --version v1.0.0
slot deployments update <Project Name> torii --config <path/to/torii.toml>
slot deployments update <Project Name> torii --replicas 3
```

## Deleting Deployments

```sh
slot deployments delete <Project Name> <katana | torii>
```

## Inspecting Deployments

```sh
# List all deployments
slot deployments list

# View configuration
slot deployments describe <Project Name> <katana | torii>

# Read logs
slot deployments logs <Project Name> <katana | torii>

# View predeployed Katana accounts
slot deployments accounts <Project Name> katana
```

## Transferring Services

Transfer a service to another team:

```sh
slot d transfer <Project Name> <katana | torii> <To Team Name>
```

## Observability

Enable Prometheus and Grafana monitoring ($10/month per deployment).

### On creation

```sh
slot deployments create <Project Name> --observability katana
slot deployments create <Project Name> --observability torii --config <path/to/torii.toml>
```

### On existing deployment

```sh
slot deployments update <Project Name> --observability katana
slot deployments update <Project Name> --observability torii
```

### Accessing dashboards

- Prometheus: `https://<deployment-url>/prometheus`
- Grafana: `https://<deployment-url>/grafana`

Both are protected by username/password credentials provided when observability is enabled.
