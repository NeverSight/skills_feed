---
name: controller-sessions
description: Configure session keys and policies for Cartridge Controller to enable gasless, pre-approved transactions. Use when defining contract interaction policies, setting spending limits, configuring signed message policies, or implementing error handling for session-based transactions. Covers SessionPolicies type, policy definitions, verified sessions, and error display modes.
---

# Controller Sessions & Policies

Sessions enable pre-approved, gasless transactions without user prompts for each interaction.

## How Sessions Work

1. Define policies (which contracts/methods your app needs)
2. User approves policies once during connection
3. Controller creates session with approved permissions
4. Transactions execute seamlessly via Paymaster

## With vs Without Policies

| Feature | With Policies | Without Policies |
|---------|--------------|------------------|
| Transaction approval | Pre-approved | Manual each time |
| Gasless transactions | Yes (Paymaster) | No |
| Error handling | Configurable display modes | Standard modal |
| Best for | Games, frequent txs | Simple apps |

## Defining Policies

```typescript
import { SessionPolicies } from "@cartridge/controller";

const policies: SessionPolicies = {
  contracts: {
    "0x1234...": {
      name: "My Game",
      description: "Game contract interactions",
      methods: [
        {
          name: "Move Player",
          entrypoint: "move_player",
          description: "Move player on the map",
        },
        {
          name: "Attack",
          entrypoint: "attack",
        },
      ],
    },
  },
};

const controller = new Controller({ policies });
```

## Token Spending Limits

For `approve` methods, specify spending limits in hex format:

```typescript
const policies: SessionPolicies = {
  contracts: {
    // ETH contract
    "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7": {
      name: "Ethereum",
      methods: [
        {
          name: "approve",
          entrypoint: "approve",
          amount: "0x3", // Limit: 3 ETH (hex, accounts for decimals)
        },
      ],
    },
  },
};
```

- Use `0xffffffffffffffffffffffffffffffff` for unlimited (max uint128)
- Users see USD values alongside token amounts when price data is available

## Signed Message Policies

Pre-approve typed message signing:

```typescript
const policies: SessionPolicies = {
  messages: [
    {
      name: "Game Message",
      types: {
        StarknetDomain: [
          { name: "name", type: "shortstring" },
          { name: "version", type: "shortstring" },
          { name: "chainId", type: "shortstring" },
          { name: "revision", type: "shortstring" },
        ],
        GameMessage: [
          { name: "content", type: "string" },
          { name: "timestamp", type: "felt" },
        ],
      },
      primaryType: "GameMessage",
      domain: {
        name: "MyGame",
        version: "1",
        chainId: "SN_MAIN",
        revision: "1",
      },
    },
  ],
};
```

## Error Handling

### Error Display Modes

```typescript
const controller = new Controller({
  policies,
  errorDisplayMode: "notification", // "modal" | "notification" | "silent"
});
```

- **modal** (default): Full error modal, blocks interaction
- **notification**: Toast notification (clickable to open modal), non-blocking
- **silent**: Console only, custom handling required

### Error Handling Interaction

| `propagateSessionErrors` | `errorDisplayMode` | Behavior |
|--------------------------|-------------------|----------|
| `true` | Any | Errors rejected immediately, no UI shown |
| `false` (default) | `modal` | Opens controller modal |
| `false` | `notification` | Shows clickable toast |
| `false` | `silent` | No UI, logged to console |

### Error Propagation

Return errors to your app instead of showing keychain UI:

```typescript
import { Controller, ResponseCodes } from "@cartridge/controller";

const controller = new Controller({
  policies,
  propagateSessionErrors: true,
});

const result = await account.execute(calls);
if (result.code === ResponseCodes.SUCCESS) {
  console.log("Tx hash:", result.transaction_hash);
} else if (result.code === ResponseCodes.ERROR) {
  console.error(result.message, result.error);
}
```

**Note**: `SessionRefreshRequired` and `ManualExecutionRequired` always show modal regardless of settings.

## Disconnect Redirect

For mobile apps and cross-platform logout flows:

```typescript
const connector = new SessionConnector({
  policies,
  rpc: "https://api.cartridge.gg/x/starknet/mainnet",
  chainId: "SN_MAIN",
  redirectUrl: "myapp://callback",
  disconnectRedirectUrl: "myapp://logout", // Where to go after logout
});
```

## Verified Sessions

Verified policies display trust badges and streamlined approval flows.
Submit configs to [`@cartridge/presets`](https://github.com/cartridge-gg/presets/tree/main/configs) for verification.

## SessionOptions Type

```typescript
type SessionOptions = {
  rpc: string;                        // RPC endpoint URL
  chainId: string;                    // Chain ID
  policies: SessionPolicies;          // Approved transaction policies
  redirectUrl: string;                // URL to redirect after auth
  disconnectRedirectUrl?: string;     // URL to redirect after logout
  signupOptions?: AuthOptions;        // Auth methods to show
};
```
