---
name: solidity-hardhat-development
description: Hardhat 3 development workflow for Solidity smart contracts. Use when building, testing, or deploying with Hardhat 3.x (hardhat, ignition, EDR). Covers ESM-first project setup, defineConfig, Solidity-native tests, TypeScript tests, multichain support, Hardhat Ignition deployment, and hook-based plugin system. Triggers on tasks involving hardhat init, hardhat build, hardhat test, hardhat ignition, or Hardhat-based Solidity development.
license: MIT
metadata:
  author: whackur
  version: "0.5.3"
---

# Hardhat 3 Development Guide

## When to Apply

- Starting new Hardhat 3 projects.
- Migrating from v2 to v3.
- Testing Solidity contracts with Foundry-compatible tests.
- Deploying with Hardhat Ignition.
- Building multichain applications.

## Project Setup

Run `npx hardhat --init` to start. Hardhat 3 requires ESM, so set `"type": "module"` in your package.json. You need Node.js v22.10 or newer. Use `defineConfig` from `hardhat/config` for your configuration file.

## Configuration

The `defineConfig` pattern organizes your setup with `solidity`, `networks`, and `plugins` keys. Networks use `type: "edr-simulated"` for local testing or `type: "http"` for remote connections. Specify `chainType` as `"l1"`, `"op"`, or `"generic"`. Use `configVariable("KEY")` for secrets to keep them out of your code. Build profiles allow different settings for production, like enabling the optimizer. Plugins must be explicitly listed in the `plugins` array.

```typescript
import { defineConfig, configVariable } from "hardhat/config";
import { hardhatIgnition } from "@nomicfoundation/hardhat-ignition";

export default defineConfig({
  solidity: "0.8.28",
  plugins: [hardhatIgnition],
  networks: {
    hardhat: { type: "edr-simulated" },
    mainnet: {
      type: "http",
      url: configVariable("MAINNET_RPC_URL"),
    },
  },
});
```

## Testing

Solidity tests use a Rust-powered runner and `.t.sol` files. These tests inherit from `forge-std/Test.sol` and support full `vm` cheatcodes like `vm.prank` and `vm.deal`. Fuzz testing works out of the box. TypeScript tests can use the Node.js test runner with Viem or Mocha with Ethers.js. Access network helpers through the `networkHelpers` property. Run `npx hardhat test` for all tests or `npx hardhat test solidity` for just Solidity. Built-in flags `--coverage` and `--gas-stats` provide extra data.

## Deployment

Hardhat Ignition is the primary framework for deployments. It uses declarative modules created with `buildModule`. Ignition handles transaction parallelization and resumes failed deployments automatically. Deploy using `npx hardhat ignition deploy ignition/modules/MyModule.ts --network <network>`. Verify contracts with the `@nomicfoundation/hardhat-verify` plugin.

## Multichain Support

Hardhat 3 simulates multiple chains at once. Connect to different networks using `const mainnet = await network.connect("mainnet")`. You can fork several chains concurrently for complex testing.

## Debugging

Use `console.log` from `hardhat/console.sol` in your contracts. Increase verbosity with flags on the test command. EDR provides detailed stack traces for failures.

## Plugin System

The new hook-based architecture requires an explicit `plugins` array in your config. Side-effect imports from v2 no longer work. You must use v3-specific versions of plugins. Essential plugins include `hardhat-verify`, `hardhat-ignition`, and `hardhat-keystore`.

## Migration from v2

Upgrade to Node.js v22.10+ and switch to ESM. Replace `module.exports` with `defineConfig`. Move side-effect imports to the `plugins` array. Update Ethers from v5 to v6 or consider switching to Viem. The single network object is now a multichain `NetworkManager`.

## Enhanced with MCP

- `compile_contract`: Build contracts and get artifacts.
- `run_tests`: Execute the test suite.
- `gas_snapshot`: Get gas reports.
- `dry_run_deploy`: Simulate deployments.
- `run_slither`, `run_aderyn`: Perform security analysis.

## References

See the [Hardhat 3 Cheatsheet](./references/hardhat-cheatsheet.md) for examples.
