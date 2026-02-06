---
name: weave
description: 'Assists with managing Initia appchains (Interwoven Rollups) using the Weave CLI. This skill helps guide the user through the interactive setup process.'
---

# Weave Skill

This skill helps you scaffold and manage Initia appchains (Interwoven Rollups) by providing guidance on how to use the `weave` CLI.

## First-Time Setup: `weave init`

The most important step for any user is to run `weave init` interactively. This command will guide you through the entire setup process, including:

*   Installing necessary dependencies (`minitiad`, `jq`).
*   Setting up a Gas Station account.
*   Funding the Gas Station account.
*   Choosing the L1 network to connect to (e.g., `Testnet (initiation-2)`).
*   Launching your first rollup.

**As an AI assistant, you cannot run `weave init` for the user.** You must instruct the user to run this command in their terminal and follow the interactive prompts.

## Agent Instructions

When a user asks to "prepare the environment" or "launch an appchain" for the first time, your primary instruction should be:

**"Please run `weave init` in your terminal and follow the interactive prompts. This will guide you through the entire setup process."**

After the user has completed the interactive `weave init`, you can then assist them with other `weave` commands, such as:

*   `weave gas-station show`: To show the gas station address.
*   `weave rollup list`: To list the running rollups.
*   `weave rollup stop`: To stop a rollup.
*   `weave rollup start`: To start a rollup.
*   `weave rollup restart`: To restart a rollup.
*   `weave rollup log`: To view the logs of a rollup.

## Core Commands

### verify_appchain

Verifies that an appchain is running correctly.

**Usage:**

```bash
# Set environment variables for your specific appchain
export CHAIN_ID="your-chain-id"
export RPC_URL="http://localhost:26657" # Default for local rollups

# Configure minitiad to talk to your appchain
minitiad config set client chain-id "$CHAIN_ID"
minitiad config set client node "$RPC_URL"

# Check if blocks are being produced
minitiad status | jq -r '.SyncInfo.latest_block_height'

# Check the balance of a genesis account
# (replace 'mykey' with the key name you chose during `weave init`)
minitiad query bank balances $(minitiad keys show mykey -a)
```