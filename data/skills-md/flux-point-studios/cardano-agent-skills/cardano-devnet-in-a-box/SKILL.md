---
name: cardano-devnet-in-a-box
description: "One-command local rehearsal stack: cardano-node + hydra + ogmios + kupo. Docker-based, deterministic green/red testing."
metadata: {"openclaw":{"emoji":"\ud83d\udce6","requires":{"bins":["docker","docker-compose","git"]},"install":[{"id":"brew","kind":"brew","formula":"colima docker docker-compose curl git","bins":["colima","docker","docker-compose","curl","git"],"label":"Install Docker runtime (Colima) + Docker CLI + Compose + curl + git (brew)","os":["darwin","linux"]}]}}
---

# Cardano Devnet-in-a-Box (cardano-node + hydra + ogmios + kupo)

## What this skill is for

You are setting up a **local, end-to-end rehearsal environment** so we can:

- build/sign/submit real transactions (cardano-cli)
- run dApp infra (Ogmios + Kupo)
- open/close a Hydra Head and push L2 txs

…all **locally** before anyone even thinks about mainnet.

This skill uses **Hydra’s official demo devnet** as the base (because it’s the most “known-good” path), then bolts on **Ogmios + Kupo** as extra services.

Hydra’s docs describe this demo setup: a single fast local devnet + 3 Hydra nodes (Alice/Bob/Carol) + hydra-tui.

Kupo’s Docker image docs show the minimal container flags we reuse (`--node-socket`, `--node-config`, `--host`, `--workdir`).

Hydra publishes official Docker images at `ghcr.io/cardano-scaling/hydra-node`.

---

## Assumptions

- Docker is installed and running.
- `git` is available.
- Ports available on host:
  - 1337 (ogmios)
  - 1442 (kupo)
  - 4001-4003 (hydra API)
  - 3000 (grafana, optional)

---

## The canonical setup

### If the repo already has `devnet-in-a-box/`

Run:

```bash
cd devnet-in-a-box
chmod +x run.sh
./run.sh up
```

This will:

1. Clone `cardano-scaling/hydra` into `devnet-in-a-box/.vendor/hydra`
2. Copy our `docker-compose.override.yml` into `hydra/demo/`
3. Run the upstream demo scripts:
   - `./prepare-devnet.sh` (creates the `devnet/` folder + fresh genesis start time)
   - `./seed-devnet.sh` (publishes Hydra scripts + funds parties)
4. Start:
   - `cardano-node`
   - `hydra-node-1..3`
   - `ogmios`
   - `kupo`

### If the repo does NOT have `devnet-in-a-box/`

Create it by copying these exact files from the skill repo:

- `devnet-in-a-box/run.sh`
- `devnet-in-a-box/docker-compose.override.yml`
- `devnet-in-a-box/README.md`

(They’re designed to be dropped into any project.)

---

## Endpoints

- Ogmios (WebSocket): `ws://localhost:1337`
- Kupo (HTTP): `http://localhost:1442`
- Hydra API:
  - Alice: `http://localhost:4001`
  - Bob: `http://localhost:4002`
  - Carol: `http://localhost:4003`

---

## How to use it (agent playbook)

### 1) Bring the stack up

```bash
./devnet-in-a-box/run.sh up
```

### 2) Open a head (fastest path = TUI)

In 3 terminals:

```bash
./devnet-in-a-box/run.sh tui 1
./devnet-in-a-box/run.sh tui 2
./devnet-in-a-box/run.sh tui 3
```

Then inside the TUI:

- `[i]` init
- `[c]` commit
- once all parties commit, the head opens automatically

Hydra’s docs walk through this flow.

### 3) Validate the L1 + infra are alive

From the demo directory (the script handles paths for you), you can query the chain tip:

```bash
./devnet-in-a-box/run.sh logs cardano-node
```

Or directly:

```bash
cd devnet-in-a-box/.vendor/hydra/demo
docker compose exec -T cardano-node cardano-cli query tip --testnet-magic 42 --socket-path /devnet/node.socket
```

### 4) Use Ogmios + Kupo for app-level rehearsal

Typical dApp stack:

- **Kupo** for UTxO lookup / index queries
- **Ogmios** for chain sync + tx submission

This is the pair most “realistic” apps use for local integration tests.

---


### Deterministic rehearsal (green / red)

For a **no-vibes end-to-end check**, run:

```bash
cd devnet-in-a-box
./run.sh rehearsal
```

It will:

- run a smoke test (cardano-node + hydra APIs + optional kupo health)
- create a tiny **always-true Plutus script UTxO** on L1 (inline datum = 42, 10 ADA)
- initialize a Hydra Head
- commit: Alice (script UTxO + collateral) + Bob + Carol
- submit one L2 transaction that **spends the script UTxO inside the head**
- close → wait contestation → fanout

If everything works you get **GREEN**. Otherwise you get **RED** and the failing step.

Lightweight health check:

```bash
./run.sh smoke
```

## Troubleshooting (quick hits)

### `TraceNoLedgerView` in cardano-node logs

That’s almost always a **genesis start time** drift.

Fix: rerun prepare + restart the node.

```bash
cd devnet-in-a-box/.vendor/hydra/demo
./prepare-devnet.sh
docker compose up -d --force-recreate cardano-node
```

Hydra docs explicitly warn about waiting too long after `prepare-devnet.sh`.

### Ogmios/Kupo can’t open the node socket

Usually permissions on `devnet/node.socket`.

The `run.sh` tries to `chmod a+w` the socket from inside the container.

If it still fails:

```bash
cd devnet-in-a-box/.vendor/hydra/demo
docker compose exec -u root cardano-node chmod a+w /devnet/node.socket
```

### Kupo is “running” but returns nothing

Make sure we’re indexing something.

We default to `--match "*"` for devnet so it indexes everything.

If you change it, you can accidentally index zero addresses.

---

## Hard rule

This devnet harness is for **rehearsals**:

- never treat the demo keys as production keys
- never assume devnet settings ≈ mainnet settings
- always re-check protocol params, cost models, and script budgets when moving to preprod/mainnet

