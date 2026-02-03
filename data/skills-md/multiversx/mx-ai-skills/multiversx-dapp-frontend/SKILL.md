---
name: multiversx-dapp-frontend
description: Adapt React applications to MultiversX blockchain with wallet connection, transactions, and smart contract interactions. Use when app needs Web3, blockchain, wallet login, crypto payments, NFTs, tokens, or smart contract calls.
---

# MultiversX dApp Frontend Integration

Transform React applications into MultiversX blockchain dApps with wallet authentication, transaction signing, and smart contract interactions.

## Prerequisites

The starter project already includes MultiversX SDK packages:
- `@multiversx/sdk-core` - Core blockchain primitives
- `@multiversx/sdk-dapp` - React hooks and providers
- `@multiversx/sdk-dapp-core-ui` - Pre-built UI components
- `@multiversx/sdk-dapp-utils` - Utility functions

## App Initialization

**CRITICAL:** Call `initApp()` BEFORE rendering the React application.

Modify `src/main.tsx`:

```typescript
import { createRoot } from 'react-dom/client';
import { initApp } from '@multiversx/sdk-dapp/out/methods/initApp/initApp';
import { EnvironmentsEnum } from '@multiversx/sdk-dapp/out/types/enums.types';
import App from './App';
import './index.css';

const config = {
  storage: {
    getStorageCallback: () => sessionStorage
  },
  dAppConfig: {
    environment: EnvironmentsEnum.devnet, // Change to testnet or mainnet
    nativeAuth: {
      expirySeconds: 86400, // 24 hours
      tokenExpirationToastWarningSeconds: 300 // 5 min warning
    }
  }
};

initApp(config).then(() => {
  const root = createRoot(document.getElementById('root')!);
  root.render(<App />);
});
```

### Environment Options

| Environment | Value | Use Case |
|-------------|-------|----------|
| `EnvironmentsEnum.devnet` | Development | Testing with free tokens |
| `EnvironmentsEnum.testnet` | Staging | Pre-production testing |
| `EnvironmentsEnum.mainnet` | Production | Real transactions |

## Wallet Connection with UnlockPanelManager

UnlockPanelManager provides a pre-built UI supporting ALL wallet providers.

### Setup Unlock Panel

```typescript
import { UnlockPanelManager } from '@multiversx/sdk-dapp/out/managers/UnlockPanelManager';
import { useNavigate } from 'react-router-dom';

function ConnectWalletButton() {
  const navigate = useNavigate();

  const handleConnect = () => {
    const unlockPanelManager = UnlockPanelManager.init({
      loginHandler: () => {
        navigate('/dashboard'); // Redirect after successful login
      },
      onClose: () => {
        // Optional: handle panel close without login
      }
    });

    unlockPanelManager.openUnlockPanel();
  };

  return (
    <button onClick={handleConnect}>
      Connect Wallet
    </button>
  );
}
```

### Supported Wallet Providers

UnlockPanelManager automatically shows all available providers:
- **xPortal App** - Mobile wallet via QR code
- **xPortal Hub** - Browser-based xPortal
- **MultiversX DeFi Wallet** - Browser extension
- **Web Wallet** - MultiversX web wallet
- **Ledger** - Hardware wallet
- **WalletConnect** - WalletConnect v2 protocol
- **Passkey** - WebAuthn/FIDO2 authentication

### Logout

```typescript
import { getAccountProvider } from '@multiversx/sdk-dapp/out/providers/accountProvider';

async function handleLogout() {
  const provider = getAccountProvider();
  await provider.logout();
  navigate('/'); // Redirect to home
}
```

## Authentication State Hooks

### Check Login Status

```typescript
import { useGetIsLoggedIn } from '@multiversx/sdk-dapp/out/hooks/account/useGetIsLoggedIn';

function AuthStatus() {
  const isLoggedIn = useGetIsLoggedIn();

  return isLoggedIn ? <Dashboard /> : <LoginPrompt />;
}
```

### Get Account Data

```typescript
import { useGetAccount } from '@multiversx/sdk-dapp/out/hooks/account/useGetAccount';

function AccountInfo() {
  const { address, balance, nonce } = useGetAccount();

  return (
    <div>
      <p>Address: {address}</p>
      <p>Balance: {balance} EGLD</p>
    </div>
  );
}
```

### Get Address Only

```typescript
import { useGetAddress } from '@multiversx/sdk-dapp/out/hooks/account/useGetAddress';

function AddressDisplay() {
  const address = useGetAddress();
  return <span>{address}</span>;
}
```

### Get Network Configuration

```typescript
import { useGetNetworkConfig } from '@multiversx/sdk-dapp/out/hooks/useGetNetworkConfig';

function NetworkInfo() {
  const { network } = useGetNetworkConfig();

  return (
    <div>
      <p>Chain ID: {network.chainId}</p>
      <p>Label: {network.egldLabel}</p>
    </div>
  );
}
```

## Protected Routes

Create an auth guard component for protected pages:

```typescript
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useGetIsLoggedIn } from '@multiversx/sdk-dapp/out/hooks/account/useGetIsLoggedIn';

interface AuthGuardProps {
  children: React.ReactNode;
}

function AuthGuard({ children }: AuthGuardProps) {
  const isLoggedIn = useGetIsLoggedIn();
  const navigate = useNavigate();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    // Small delay to allow SDK to restore session
    const timer = setTimeout(() => {
      setIsChecking(false);
      if (!isLoggedIn) {
        navigate('/');
      }
    }, 100);

    return () => clearTimeout(timer);
  }, [isLoggedIn, navigate]);

  if (isChecking) {
    return <div>Loading...</div>;
  }

  return isLoggedIn ? <>{children}</> : null;
}

// Usage in routes
<Route path="/dashboard" element={
  <AuthGuard>
    <Dashboard />
  </AuthGuard>
} />
```

## Basic Transactions

### Send EGLD Transfer

```typescript
import { Transaction, Address } from '@multiversx/sdk-core';
import { getAccountProvider } from '@multiversx/sdk-dapp/out/providers/accountProvider';
import { refreshAccount } from '@multiversx/sdk-dapp/out/utils/account/refreshAccount';
import { TransactionManager } from '@multiversx/sdk-dapp/out/managers/TransactionManager';
import { useGetAccount } from '@multiversx/sdk-dapp/out/hooks/account/useGetAccount';
import { useGetNetworkConfig } from '@multiversx/sdk-dapp/out/hooks/useGetNetworkConfig';

function SendEgld() {
  const { address: senderAddress, nonce } = useGetAccount();
  const { network } = useGetNetworkConfig();

  const sendTransaction = async (receiverAddress: string, amount: string) => {
    // Refresh account to get latest nonce
    await refreshAccount();

    // Create transaction (amount in wei: 1 EGLD = 10^18)
    const transaction = new Transaction({
      value: BigInt(amount),
      receiver: Address.newFromBech32(receiverAddress),
      sender: Address.newFromBech32(senderAddress),
      gasLimit: BigInt(50000),
      chainID: network.chainId,
      nonce: BigInt(nonce)
    });

    // Sign transaction
    const provider = getAccountProvider();
    const signedTransactions = await provider.signTransactions([transaction]);

    // Send and track
    const txManager = TransactionManager.getInstance();
    const sentTransactions = await txManager.send(signedTransactions);

    // Track with toast notifications
    const sessionId = await txManager.track(sentTransactions, {
      transactionsDisplayInfo: {
        processingMessage: 'Sending EGLD...',
        successMessage: 'EGLD sent successfully!',
        errorMessage: 'Transaction failed'
      }
    });

    return sessionId;
  };

  return (
    <button onClick={() => sendTransaction('erd1...', '1000000000000000000')}>
      Send 1 EGLD
    </button>
  );
}
```

### Send ESDT Token Transfer

```typescript
import { Transaction, Address, TokenTransfer } from '@multiversx/sdk-core';
import { EsdtHelpers } from '@multiversx/sdk-dapp-utils';

async function sendToken(
  receiverAddress: string,
  tokenId: string,
  amount: string,
  decimals: number
) {
  await refreshAccount();
  const { address: senderAddress, nonce } = useGetAccount();
  const { network } = useGetNetworkConfig();

  // Build token transfer data
  const transfer = TokenTransfer.fungibleFromAmount(tokenId, amount, decimals);

  const transaction = new Transaction({
    value: BigInt(0),
    receiver: Address.newFromBech32(receiverAddress),
    sender: Address.newFromBech32(senderAddress),
    gasLimit: BigInt(500000),
    chainID: network.chainId,
    nonce: BigInt(nonce),
    data: Buffer.from(`ESDTTransfer@${Buffer.from(tokenId).toString('hex')}@${transfer.amountAsBigInteger.toString(16)}`)
  });

  const provider = getAccountProvider();
  const signedTransactions = await provider.signTransactions([transaction]);

  const txManager = TransactionManager.getInstance();
  await txManager.send(signedTransactions);
}
```

## Transaction Status Tracking

### Monitor Pending Transactions

```typescript
import { useGetPendingTransactions } from '@multiversx/sdk-dapp/out/hooks/transactions/useGetPendingTransactions';

function PendingTransactions() {
  const { pendingTransactions, hasPendingTransactions } = useGetPendingTransactions();

  if (!hasPendingTransactions) {
    return <p>No pending transactions</p>;
  }

  return (
    <ul>
      {pendingTransactions.map((tx) => (
        <li key={tx.hash}>Processing: {tx.hash}</li>
      ))}
    </ul>
  );
}
```

### Monitor Successful Transactions

```typescript
import { useGetSuccessfulTransactions } from '@multiversx/sdk-dapp/out/hooks/transactions/useGetSuccessfulTransactions';

function SuccessfulTransactions() {
  const { successfulTransactions } = useGetSuccessfulTransactions();

  return (
    <ul>
      {successfulTransactions.map((tx) => (
        <li key={tx.hash}>Completed: {tx.hash}</li>
      ))}
    </ul>
  );
}
```

### Monitor Failed Transactions

```typescript
import { useGetFailedTransactions } from '@multiversx/sdk-dapp/out/hooks/transactions/useGetFailedTransactions';

function FailedTransactions() {
  const { failedTransactions } = useGetFailedTransactions();

  return (
    <ul>
      {failedTransactions.map((tx) => (
        <li key={tx.hash}>Failed: {tx.hash}</li>
      ))}
    </ul>
  );
}
```

## Advanced Smart Contract Interactions

### Loading ABI Files

Store ABI JSON files in `src/contracts/` and import them:

```typescript
// src/contracts/myContract.abi.json - place your ABI file here

import { AbiRegistry, SmartContract, Address } from '@multiversx/sdk-core';
import myContractAbi from '@/contracts/myContract.abi.json';

function createContract(contractAddress: string) {
  const abiRegistry = AbiRegistry.create(myContractAbi);

  return new SmartContract({
    address: Address.newFromBech32(contractAddress),
    abi: abiRegistry
  });
}
```

### Query Smart Contract (View Functions)

```typescript
import { ApiNetworkProvider } from '@multiversx/sdk-core';
import { SmartContract, Address, AbiRegistry, ResultsParser } from '@multiversx/sdk-core';

async function queryContract() {
  const networkProvider = new ApiNetworkProvider('https://devnet-api.multiversx.com');

  const contract = new SmartContract({
    address: Address.newFromBech32('erd1qqqqqqqqqqqqqq...'),
    abi: AbiRegistry.create(myContractAbi)
  });

  // Create query for a view function
  const query = contract.createQuery({
    func: 'getTokenPrice',
    args: [] // Add arguments if needed
  });

  // Execute query
  const queryResponse = await networkProvider.queryContract(query);

  // Parse result using ABI
  const resultsParser = new ResultsParser();
  const endpointDefinition = contract.getEndpoint('getTokenPrice');
  const parsed = resultsParser.parseQueryResponse(queryResponse, endpointDefinition);

  return parsed.values[0]; // First return value
}
```

### Call Smart Contract (State-Changing Functions)

```typescript
import { SmartContract, Address, AbiRegistry, TokenTransfer } from '@multiversx/sdk-core';
import { getAccountProvider } from '@multiversx/sdk-dapp/out/providers/accountProvider';
import { refreshAccount } from '@multiversx/sdk-dapp/out/utils/account/refreshAccount';
import { TransactionManager } from '@multiversx/sdk-dapp/out/managers/TransactionManager';

async function callContract(
  contractAddress: string,
  functionName: string,
  args: any[],
  egldValue?: string
) {
  await refreshAccount();

  const contract = new SmartContract({
    address: Address.newFromBech32(contractAddress),
    abi: AbiRegistry.create(myContractAbi)
  });

  // Build interaction
  const interaction = contract.methods[functionName](args);

  // Set gas limit
  interaction.withGasLimit(BigInt(10000000));

  // Add EGLD payment if needed
  if (egldValue) {
    interaction.withValue(BigInt(egldValue));
  }

  // Build transaction
  const transaction = interaction.buildTransaction();

  // Sign
  const provider = getAccountProvider();
  const signedTransactions = await provider.signTransactions([transaction]);

  // Send and track
  const txManager = TransactionManager.getInstance();
  const sent = await txManager.send(signedTransactions);

  await txManager.track(sent, {
    transactionsDisplayInfo: {
      processingMessage: `Calling ${functionName}...`,
      successMessage: 'Transaction successful!',
      errorMessage: 'Transaction failed'
    }
  });
}
```

### Batch/Multi-Call Transactions

Send multiple transactions in parallel:

```typescript
async function batchTransactions(transactions: Transaction[]) {
  const provider = getAccountProvider();
  const signedTransactions = await provider.signTransactions(transactions);

  const txManager = TransactionManager.getInstance();

  // Send all in parallel
  const sent = await txManager.send(signedTransactions);

  await txManager.track(sent, {
    transactionsDisplayInfo: {
      processingMessage: 'Processing batch...',
      successMessage: 'All transactions completed!',
      errorMessage: 'Some transactions failed'
    }
  });
}
```

Send transactions sequentially (wait for each to complete):

```typescript
async function sequentialTransactions(transactions: Transaction[]) {
  const provider = getAccountProvider();
  const signedTransactions = await provider.signTransactions(transactions);

  const txManager = TransactionManager.getInstance();

  // Send sequentially using nested arrays
  const sent = await txManager.send(signedTransactions.map(tx => [tx]));

  await txManager.track(sent);
}
```

### Smart Contract with Token Payment

```typescript
async function callWithTokenPayment(
  contractAddress: string,
  functionName: string,
  tokenId: string,
  amount: string,
  decimals: number
) {
  const contract = new SmartContract({
    address: Address.newFromBech32(contractAddress),
    abi: AbiRegistry.create(myContractAbi)
  });

  const payment = TokenTransfer.fungibleFromAmount(tokenId, amount, decimals);

  const interaction = contract.methods[functionName]([])
    .withSingleESDTTransfer(payment)
    .withGasLimit(BigInt(15000000));

  const transaction = interaction.buildTransaction();

  // Sign and send...
}
```

## UI Components

### Format Token Amounts

```typescript
import { MvxFormatAmount } from '@multiversx/sdk-dapp-core-ui';

function BalanceDisplay({ amount }: { amount: string }) {
  return (
    <MvxFormatAmount
      value={amount}
      decimals={18}
      egldLabel="EGLD"
      showLabel
    />
  );
}
```

### Display Transactions Table

```typescript
import { MvxTransactionsTable } from '@multiversx/sdk-dapp-core-ui';

function TransactionsPage() {
  return (
    <div>
      <h2>Your Transactions</h2>
      <MvxTransactionsTable />
    </div>
  );
}
```

## Critical Knowledge

### WRONG: Hardcoding chain ID

```typescript
// WRONG - Will break on different networks
const transaction = new Transaction({
  chainID: 'D' // Hardcoded devnet
});
```

### CORRECT: Use network config

```typescript
// CORRECT - Dynamic chain ID
const { network } = useGetNetworkConfig();
const transaction = new Transaction({
  chainID: network.chainId
});
```

### WRONG: Not refreshing account before transaction

```typescript
// WRONG - May use stale nonce
const { nonce } = useGetAccount();
const tx = new Transaction({ nonce: BigInt(nonce) });
```

### CORRECT: Always refresh account first

```typescript
// CORRECT - Fresh nonce
await refreshAccount();
const { nonce } = useGetAccount();
const tx = new Transaction({ nonce: BigInt(nonce) });
```

### WRONG: Insufficient gas limit

```typescript
// WRONG - 50000 gas is only for simple EGLD transfers
const tx = new Transaction({
  gasLimit: BigInt(50000),
  data: Buffer.from('ESDTTransfer@...') // Token transfer needs more gas!
});
```

### CORRECT: Appropriate gas limits

```typescript
// CORRECT gas limits by operation type:
// Simple EGLD transfer: 50,000
// ESDT token transfer: 500,000
// NFT transfer: 1,000,000
// Smart contract call: 5,000,000 - 60,000,000 (depends on complexity)

const tx = new Transaction({
  gasLimit: BigInt(500000) // For token transfer
});
```

### WRONG: Rendering before initApp completes

```typescript
// WRONG - SDK not initialized
createRoot(document.getElementById('root')!).render(<App />);
initApp(config); // Too late!
```

### CORRECT: Wait for initApp

```typescript
// CORRECT - SDK ready before render
initApp(config).then(() => {
  createRoot(document.getElementById('root')!).render(<App />);
});
```

## API Endpoints Reference

| Network | API URL |
|---------|---------|
| Devnet | `https://devnet-api.multiversx.com` |
| Testnet | `https://testnet-api.multiversx.com` |
| Mainnet | `https://api.multiversx.com` |

## SDK Documentation Links

- **SDK-dApp Documentation**: https://github.com/multiversx/mx-sdk-dapp
- **Template dApp (Reference Implementation)**: https://github.com/multiversx/mx-template-dapp
- **SDK-Core Documentation**: https://github.com/multiversx/mx-sdk-js-core
- **MultiversX Docs**: https://docs.multiversx.com

## Verification Checklist

Before completion, verify:

- [ ] `initApp()` called in main.tsx BEFORE `createRoot().render()`
- [ ] Environment set correctly (devnet/testnet/mainnet)
- [ ] Wallet connection works with UnlockPanelManager
- [ ] `useGetIsLoggedIn()` correctly detects auth state
- [ ] Protected routes redirect unauthenticated users
- [ ] `refreshAccount()` called before creating transactions
- [ ] Gas limits appropriate for transaction type
- [ ] Chain ID from `useGetNetworkConfig()`, not hardcoded
- [ ] Transaction tracking shows toast notifications
- [ ] Smart contract ABI loaded correctly (if using contracts)
