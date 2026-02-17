---
name: solidity-deploy
description: "[AUTO-INVOKE] MUST be invoked BEFORE deploying contracts or writing deployment scripts (*.s.sol). Covers pre-flight checks, forge script commands, post-deployment validation, and verification. Trigger: any task involving forge script, contract deployment, or block explorer verification."
---

# Deployment Workflow

## Language Rule

- **Always respond in the same language the user is using.** If the user asks in Chinese, respond in Chinese. If in English, respond in English.

## Pre-deployment Checklist (all must pass)

| Step | Command / Action |
|------|-----------------|
| Format code | `forge fmt` |
| Run all tests | `forge test` — zero failures required |
| Check gas report | `forge test --gas-report` — review critical functions |
| Verify config | Manually check `config/*.json` parameters |
| Dry-run | `forge script <Script> --fork-url $RPC_URL -vvvv` (no `--broadcast`) |
| Check balance | `cast balance $DEPLOYER --rpc-url $RPC_URL` — sufficient gas? |
| Gas limit set | Deployment command must include `--gas-limit` |

## Deployment Decision Rules

| Situation | Rule |
|-----------|------|
| Default deployment | **No `--verify`** — contracts are not verified on block explorers by default |
| User requests verification | Add `--verify` and `--etherscan-api-key` to the command |
| Post-deploy verification | Use `forge verify-contract` as a separate step |
| Multi-chain deploy | Separate scripts per chain, never batch multiple chains in one script |
| Proxy deployment | Deploy implementation first, then proxy — verify both separately |

## Post-deployment Operations (all required)

1. Update addresses in `config/*.json` and `deployments/latest.env`
2. Test critical functions: `cast call` / `cast send` to verify on-chain behavior
3. Record changes in `docs/CHANGELOG.md`
4. Submit PR with deployment transaction hash link
5. If verification needed, run `forge verify-contract` separately

## Command Templates

```bash
# Load environment
source .env

# Standard deployment (no verification by default)
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --gas-limit 5000000 \
  -vvvv

# Deployment with verification (only when explicitly requested)
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --gas-limit 5000000 \
  -vvvv

# Verify existing contract separately
forge verify-contract <ADDRESS> <CONTRACT> \
  --chain-id <CHAIN_ID> \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --constructor-args $(cast abi-encode "constructor(address)" <ARG>)

# Quick on-chain function test after deployment
cast call <CONTRACT_ADDRESS> "functionName()" --rpc-url $RPC_URL
cast send <CONTRACT_ADDRESS> "functionName(uint256)" 100 \
  --rpc-url $RPC_URL --private-key $PRIVATE_KEY
```
