---
name: controller-react
description: Integrate Cartridge Controller into React applications using starknet-react. Use when building React/Next.js web apps with Controller, setting up StarknetConfig provider, using hooks like useConnect/useAccount, or implementing wallet connection components. Covers ControllerConnector setup, provider configuration, and transaction execution patterns.
---

# Controller React Integration

Integrate Cartridge Controller with React using `starknet-react`.

## Installation

```bash
pnpm add @cartridge/connector @cartridge/controller @starknet-react/core @starknet-react/chains starknet
pnpm add -D vite-plugin-mkcert
```

## Provider Setup

**Important**: Create connector outside React components.

```typescript
import { sepolia, mainnet, Chain } from "@starknet-react/chains";
import { StarknetConfig, jsonRpcProvider, cartridge } from "@starknet-react/core";
import { ControllerConnector } from "@cartridge/connector";
import { SessionPolicies } from "@cartridge/controller";

// Define contract addresses
const ETH_TOKEN_ADDRESS =
  "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7";

const policies: SessionPolicies = {
  contracts: {
    [ETH_TOKEN_ADDRESS]: {
      methods: [
        {
          name: "approve",
          entrypoint: "approve",
          description: "Approve spending of tokens",
        },
        { name: "transfer", entrypoint: "transfer" },
      ],
    },
  },
};

// Create OUTSIDE component
const connector = new ControllerConnector({ policies });

const provider = jsonRpcProvider({
  rpc: (chain: Chain) => {
    switch (chain) {
      case mainnet:
        return { nodeUrl: "https://api.cartridge.gg/x/starknet/mainnet" };
      case sepolia:
        return { nodeUrl: "https://api.cartridge.gg/x/starknet/sepolia" };
    }
  },
});

export function StarknetProvider({ children }: { children: React.ReactNode }) {
  return (
    <StarknetConfig
      autoConnect
      defaultChainId={mainnet.id}
      chains={[mainnet, sepolia]}
      provider={provider}
      connectors={[connector]}
      explorer={cartridge}
    >
      {children}
    </StarknetConfig>
  );
}
```

## Connect Wallet Component

```typescript
import { useAccount, useConnect, useDisconnect } from "@starknet-react/core";
import { ControllerConnector } from "@cartridge/connector";
import { useEffect, useState } from "react";

export function ConnectWallet() {
  const { connect, connectors } = useConnect();
  const { disconnect } = useDisconnect();
  const { address } = useAccount();
  const controller = connectors[0] as ControllerConnector;
  const [username, setUsername] = useState<string>();

  useEffect(() => {
    if (!address) return;
    controller.username()?.then(setUsername);
  }, [address, controller]);

  if (address) {
    return (
      <div>
        <p>Account: {address}</p>
        {username && <p>Username: {username}</p>}
        <button onClick={() => disconnect()}>Disconnect</button>
      </div>
    );
  }

  return (
    <div>
      <button onClick={() => connect({ connector: controller })}>
        Connect
      </button>
    </div>
  );
}
```

## Dynamic Auth Buttons

```typescript
const handleSpecificAuth = async (signupOptions: string[]) => {
  try {
    // Direct controller connection for specific auth options
    await controller.connect({ signupOptions });

    // Manually trigger starknet-react state update
    connect({ connector: controller });
  } catch (error) {
    console.error("Connection failed:", error);
  }
};

<button onClick={() => handleSpecificAuth(["phantom-evm"])}>
  Continue with Phantom
</button>
<button onClick={() => handleSpecificAuth(["google"])}>
  Continue with Google
</button>
```

## Execute Transactions

```typescript
import { useAccount, useExplorer } from "@starknet-react/core";
import { useCallback, useState } from "react";

const ETH = "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7";

export function TransferEth() {
  const [submitted, setSubmitted] = useState<boolean>(false);
  const { account } = useAccount();
  const explorer = useExplorer();
  const [txnHash, setTxnHash] = useState<string>();

  const execute = useCallback(
    async (amount: string) => {
      if (!account) return;
      setSubmitted(true);
      setTxnHash(undefined);

      try {
        const result = await account.execute([
          {
            contractAddress: ETH,
            entrypoint: "approve",
            calldata: [account.address, amount, "0x0"],
          },
          {
            contractAddress: ETH,
            entrypoint: "transfer",
            calldata: [account.address, amount, "0x0"],
          },
        ]);

        setTxnHash(result.transaction_hash);
      } catch (e) {
        console.error(e);
      } finally {
        setSubmitted(false);
      }
    },
    [account]
  );

  if (!account) return null;

  return (
    <div>
      <button onClick={() => execute("0x1C6BF52634000")} disabled={submitted}>
        Transfer 0.005 ETH
      </button>
      {txnHash && (
        <a href={explorer.transaction(txnHash)} target="_blank" rel="noreferrer">
          View Transaction
        </a>
      )}
    </div>
  );
}
```

## External Wallet Methods

```typescript
// Wait for transaction confirmation
const response = await controller.externalWaitForTransaction(
  "metamask",
  txHash,
  30000 // timeout ms
);

if (response.success) {
  console.log("Receipt:", response.result);
} else {
  console.error("Error:", response.error);
}

// Switch chains
const success = await controller.externalSwitchChain("metamask", chainId);
```

Supported wallet types: `metamask`, `rabby`, `phantom`, `argent`, `walletconnect`.

## Vite Configuration

Enable HTTPS for local development:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import mkcert from "vite-plugin-mkcert";

export default defineConfig({
  plugins: [react(), mkcert()],
});
```

## Development Modes

```bash
# Local development with local APIs
pnpm dev

# Testing with production APIs (hybrid mode)
pnpm dev:live
```

The `dev:live` mode runs keychain locally while connecting to production APIs.

## App Structure

```typescript
import { StarknetProvider } from "./StarknetProvider";
import { ConnectWallet } from "./ConnectWallet";
import { TransferEth } from "./TransferEth";

function App() {
  return (
    <StarknetProvider>
      <ConnectWallet />
      <TransferEth />
    </StarknetProvider>
  );
}
```
