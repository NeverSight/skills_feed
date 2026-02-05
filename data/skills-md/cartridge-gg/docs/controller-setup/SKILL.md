---
name: controller-setup
description: Integrate Cartridge Controller wallet into Starknet applications. Use when setting up Controller for the first time, installing packages, configuring chains/RPC endpoints, or troubleshooting basic integration issues. Covers installation, Controller instantiation, ControllerConnector vs SessionConnector choice, chain configuration, and package compatibility.
---

# Controller Setup

Cartridge Controller is a gaming-focused smart contract wallet for Starknet with session keys, passkeys, and paymaster support.

## Installation

```bash
# Basic Controller usage
pnpm add @cartridge/controller starknet

# With framework connectors (React, native apps)
pnpm add @cartridge/controller @cartridge/connector starknet
```

## Quick Start

```typescript
import Controller from "@cartridge/controller";

const controller = new Controller();
const account = await controller.connect();
// Ready to execute transactions
```

## When to Use Policies

Policies are **optional**. Choose based on your needs:

- **Use policies**: Games needing frequent, seamless transactions with gasless execution via Paymaster
- **Skip policies**: Simple apps where manual approval per transaction is acceptable

## Choosing a Connector

| Use Case | Connector | Key Difference |
|----------|-----------|----------------|
| Web apps with starknet-react | `ControllerConnector` | Keys managed via browser cookies & localStorage |
| Native/mobile apps | `SessionConnector` | App generates local keypair, authenticates via browser redirect |

### ControllerConnector (Web)

```typescript
import { ControllerConnector } from "@cartridge/connector";

const connector = new ControllerConnector({
  policies,              // Optional session policies
  signupOptions,         // Optional auth methods to show
});
```

### SessionConnector (Native/Mobile)

```typescript
import { SessionConnector } from "@cartridge/connector";
import { constants } from "starknet";

const connector = new SessionConnector({
  policies,
  rpc: "https://api.cartridge.gg/x/starknet/mainnet",
  chainId: constants.StarknetChainId.SN_MAIN,
  redirectUrl: "myapp://auth-callback",
  disconnectRedirectUrl: "myapp://logout",  // Optional logout redirect
  signupOptions: ["webauthn", "google"],    // Optional auth methods
});
```

**Session flow**: App generates keypair → User authenticates in browser → Browser redirects back → App signs transactions locally.

## Chain Configuration

Default RPC endpoints are provided. Override with custom chains:

```typescript
import { constants } from "starknet";

const controller = new Controller({
  chains: [
    { rpcUrl: "https://api.cartridge.gg/x/starknet/mainnet" },
    { rpcUrl: "https://api.cartridge.gg/x/starknet/sepolia" },
    { rpcUrl: "http://localhost:5050" }, // Local Katana
  ],
  defaultChainId: constants.StarknetChainId.SN_MAIN,
});
```

## Performance: Lazy Loading

Defer iframe mounting until `connect()` is called:

```typescript
const controller = new Controller({
  lazyload: true,
});
```

## ControllerOptions Reference

```typescript
type ControllerOptions = {
  chains?: Chain[];                    // Custom RPC endpoints
  defaultChainId?: string;             // Default chain (hex encoded)
  policies?: SessionPolicies;          // Session policies
  propagateSessionErrors?: boolean;    // Return errors to caller
  errorDisplayMode?: "modal" | "notification" | "silent";
  lazyload?: boolean;                  // Defer iframe mount
  preset?: string;                     // Theme preset name
  signupOptions?: AuthOptions;         // Auth methods to show
};
```

## Package Compatibility

```json
{
  "@cartridge/connector": "0.11.3-alpha.1",
  "@cartridge/controller": "0.11.3-alpha.1",
  "@starknet-react/core": "^5.0.1",
  "@starknet-react/chains": "^5.0.1",
  "starknet": "^8.1.2"
}
```

## Common Issues

**Cookies required**: Controller sets essential cookies for initialization.

**HTTPS required in dev**: Use `vite-plugin-mkcert` for local HTTPS.

**Connector outside components**: Create `ControllerConnector` outside React components to avoid recreation on re-render.
