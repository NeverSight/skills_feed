---
name: token-minter
description: Generate, build, and deploy custom ERC20 tokens on EVM networks. Use when users want to create and deploy their own ERC20 tokens with custom parameters like name, symbol, decimals, and initial supply. Supports deployment to various networks including Sepolia testnet and requires Foundry (forge/cast) for blockchain interactions.
---

# Token Minter

## Overview

This skill enables users to create custom ERC20 tokens by collecting parameters, generating Solidity code, setting up a Foundry project, building the contract, and deploying to a target EVM network.

## Workflow

### Step 1: Collect Information
Collect the following parameters from the user:
- Token name (e.g., "MyToken")
- Token symbol (e.g., "MTK")
- Decimals (default: 18)
- Initial supply (default: 1000000)
- Target network (default: sepolia)

### Step 2: Generate ERC20 Contract
Use the provided script to generate the ERC20 contract code based on user parameters.
- Run `python scripts/generate_contract.py <name> <symbol> <decimals> <initial_supply>` to generate the contract
- The generated contract uses OpenZeppelin ERC20 standard

### Step 3: Initialize Forge Project
- Create a temporary directory under `./tmp/`
- Initialize a new Foundry project: `forge init`
- Place the generated contract in `src/Contract.sol`

### Step 4: Build Contract
- Install dependencies: `forge install OpenZeppelin/openzeppelin-contracts`
- Build the contract: `forge build`

### Step 5: Deploy to Network
- Ensure a local cast wallet is created (prerequisite)
- Get RPC URL for target network from https://chainlist.org/rpcs.json
  - Find the network entry and use a reliable HTTPS RPC URL
  - For Sepolia: typically "https://ethereum-sepolia.publicnode.com" or similar
- Deploy using: `forge create --rpc-url <network_rpc> --account <account_name> src/Contract.sol:MyToken --constructor-args <initial_supply> --broadcast`
- Verify deployment on the target network

## Prerequisites
- Foundry installed (forge, cast commands available)
- Local cast wallet created with `cast wallet new`
- Sufficient funds on the deployment account for gas fees

## Resources

### scripts/
- `generate_contract.py`: Python script to generate ERC20 contract code with custom parameters

### references/
- `erc20_guide.md`: Overview of ERC20 standard, required functions, events, and deployment considerations

### assets/
- `ERC20Template.sol`: Template Solidity file for ERC20 contract generation
