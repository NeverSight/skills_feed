---
name: frontend
description: Expert MultiversX Frontend Development. Use for building dApps with React, Next.js, and sdk-dapp.
---

# MultiversX Frontend Expert

This skill guides the development of decentralized applications (dApps) on MultiversX, focusing on `sdk-dapp`, `sdk-js`, and React/Next.js integration.

## Core Capabilities

1.  **Wallet Connection**: Integration with Defi Wallet, xPortal, Ledger, and Web Wallet.
2.  **Transaction Signing**: Constructing, signing, and broadcasting transactions.
3.  **State Management**: Tracking account balance, network configuration, and ensuring synchronization.
4.  **UI Components**: Using MultiversX-specific UI patterns.

## 🛠️ Development Workflow

### 1. Setup & Configuration
*   **Library**: `@multiversx/sdk-dapp` is the standard.
*   **Provider**: Wrap your root application in `<DappProvider>`.
    ```tsx
    <DappProvider
        environment="devnet"
        customNetworkConfig={{ name: 'customConfig', apiTimeout: 6000 }}
    >
        <App />
    </DappProvider>
    ```

### 2. Authentication (Login)
*   **Hooks**: Use `useExtensionLogin`, `useWalletConnectV2Login`, `useWebWalletLogin`.
*   **Best Practice**: Abstract login logic into a dedicated component.
*   **Session**: Handle session expiry automatically with `sdk-dapp`.

### 3. Smart Contract Interaction
*   **Queries**: Use `SmartContract.query()` via a `ProxyNetworkProvider`.
*   **Transactions**:
    1.  Create transaction: `new Interaction(...)`
    2.  Sign: `useSignTransactions` hook or `refreshAccount()`.
    3.  Broadcast & Track: Use `useTrackTransactionStatus` for UI updates.
*   **ABI**: Always load the correct ABI (`.abi.json`) for type-safe interactions.

### 4. Security
*   **Validation**: Validate all inputs before creating transactions.
*   **Feedback**: Show clear success/fail messages using clear visual indicators (Toasts).
*   **Slippage**: Handle slippage calculation on the frontend for DeFi apps.

## 📚 Expert Resources (Deep Dive)
*   **Frontend Audit**: `skills/expert/multiversx-dapp-audit/SKILL.md`
*   **JS SDK Core**: `skills/expert/mvx_sdk_js_core/SKILL.md`
*   **Wallet Integration**: `skills/expert/mvx_sdk_js_wallets/SKILL.md`
*   **Token Management**: `skills/expert/mvx_sdk_js_tokens/SKILL.md`

## ⚡ Common Operations

### Reading Account State
```tsx
const { address, account, balance } = useGetAccountInfo();
```

### Sending a Transport
```tsx
const { sendTransactions } = useSendTransactions();

await sendTransactions({
    transactions: [tx],
    transactionsDisplayInfo: {
        processingMessage: 'Processing Transaction',
        errorMessage: 'An error has occurred',
        successMessage: 'Transaction successful'
    },
    redirectAfterSign: false
});
```


# Frontend Base

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


# Frontend Audit

---
name: multiversx-dapp-audit
description: Audit frontend dApp components for security vulnerabilities in wallet integration and transaction handling. Use when reviewing React/TypeScript dApps using sdk-dapp, or assessing client-side security.
---

# MultiversX dApp Auditor

Audit the frontend components of MultiversX applications built with `@multiversx/sdk-dapp`. This skill focuses on client-side security, transaction construction, and wallet integration vulnerabilities.

## When to Use

- Reviewing React/TypeScript dApp code
- Auditing wallet connection implementations
- Assessing transaction signing security
- Checking for XSS and data exposure vulnerabilities
- Validating frontend-backend security boundaries

## 1. Transaction Construction Security

### The Threat Model
The frontend constructs transaction payloads that users sign. Vulnerabilities here can trick users into signing malicious transactions.

### Payload Manipulation
```typescript
// VULNERABLE: User input directly in transaction data
const sendTransaction = async (userInput: string) => {
    const tx = new Transaction({
        receiver: Address.newFromBech32(recipientAddress),
        data: Buffer.from(userInput),  // Attacker controls data!
        // ...
    });
    await signAndSend(tx);
};

// SECURE: Validate and sanitize all inputs
const sendTransaction = async (functionName: string, args: string[]) => {
    // Whitelist allowed functions
    const allowedFunctions = ['stake', 'unstake', 'claim'];
    if (!allowedFunctions.includes(functionName)) {
        throw new Error('Invalid function');
    }

    // Validate arguments
    const sanitizedArgs = args.map(arg => validateArgument(arg));

    const tx = new Transaction({
        receiver: contractAddress,
        data: Buffer.from(`${functionName}@${sanitizedArgs.join('@')}`),
        // ...
    });
    await signAndSend(tx);
};
```

### Critical Checks
| Check | Risk | Mitigation |
|-------|------|------------|
| Receiver address validation | Funds sent to wrong address | Validate against known addresses |
| Data payload construction | Malicious function calls | Whitelist allowed operations |
| Amount validation | Incorrect value transfers | Confirm amounts with user |
| Gas limit manipulation | Transaction failures | Use appropriate limits |

## 2. Signing Security

### Blind Signing Risks
Users may sign transactions without understanding the content:

```typescript
// DANGEROUS: Signing opaque data
const signMessage = async (data: string) => {
    const hash = keccak256(data);
    return await wallet.signMessage(hash);  // User sees only hash!
};

// SECURE: Show clear message to user
const signMessage = async (message: string) => {
    // Display message to user before signing
    const confirmed = await showConfirmationDialog({
        title: 'Sign Message',
        content: `You are signing: "${message}"`,
        warning: 'Only sign messages you understand'
    });

    if (!confirmed) throw new Error('User rejected');
    return await wallet.signMessage(message);
};
```

### Transaction Preview Requirements
Before signing, users should see:
- Recipient address (with verification if known)
- Amount being transferred
- Token type (EGLD, ESDT, NFT)
- Function being called (if smart contract interaction)
- Gas cost estimate

## 3. Sensitive Data Handling

### Private Key Security

```typescript
// CRITICAL VULNERABILITY: Never do this
localStorage.setItem('privateKey', wallet.privateKey);
localStorage.setItem('mnemonic', wallet.mnemonic);
sessionStorage.setItem('seed', wallet.seed);

// Check for these patterns in code review:
// - Any storage of private keys, mnemonics, or seeds
// - Logging of sensitive data
// - Sending sensitive data to APIs
```

### Secure Patterns
```typescript
// CORRECT: Use sdk-dapp's secure session management
import { initApp } from '@multiversx/sdk-dapp/out/methods/initApp/initApp';

initApp({
    storage: {
        getStorageCallback: () => sessionStorage  // Session only, not persistent
    },
    dAppConfig: {
        nativeAuth: {
            expirySeconds: 3600  // Short-lived tokens
        }
    }
});
```

### Access Token Security
```typescript
// VULNERABLE: Token exposed in URL
window.location.href = `https://api.example.com?accessToken=${token}`;

// VULNERABLE: Token in console
console.log('Auth token:', accessToken);

// SECURE: Token in Authorization header, never logged
fetch(apiUrl, {
    headers: {
        'Authorization': `Bearer ${accessToken}`
    }
});
```

## 4. XSS Prevention

### User-Generated Content
```typescript
// VULNERABLE: Direct HTML injection
const UserProfile = ({ bio }: { bio: string }) => {
    return <div dangerouslySetInnerHTML={{ __html: bio }} />;  // XSS!
};

// SECURE: React's default escaping
const UserProfile = ({ bio }: { bio: string }) => {
    return <div>{bio}</div>;  // Automatically escaped
};

// If HTML is necessary, sanitize first
import DOMPurify from 'dompurify';

const UserProfile = ({ bio }: { bio: string }) => {
    const sanitized = DOMPurify.sanitize(bio);
    return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
};
```

### URL Handling
```typescript
// VULNERABLE: Unvalidated redirect
const handleCallback = () => {
    const returnUrl = new URLSearchParams(window.location.search).get('returnUrl');
    window.location.href = returnUrl!;  // Open redirect!
};

// SECURE: Validate redirect URL
const handleCallback = () => {
    const returnUrl = new URLSearchParams(window.location.search).get('returnUrl');
    const allowed = ['/', '/dashboard', '/profile'];
    if (allowed.includes(returnUrl || '')) {
        window.location.href = returnUrl!;
    } else {
        window.location.href = '/';  // Default safe redirect
    }
};
```

## 5. API Communication Security

### HTTPS Enforcement
```typescript
// VULNERABLE: HTTP connection
const API_URL = 'http://api.example.com';  // Insecure!

// SECURE: Always HTTPS
const API_URL = 'https://api.example.com';

// Verify in code: all API URLs must use https://
```

### Request/Response Validation
```typescript
// VULNERABLE: Trusting API response blindly
const balance = await fetch('/api/balance').then(r => r.json());
displayBalance(balance.amount);  // What if API is compromised?

// SECURE: Validate response structure
const response = await fetch('/api/balance').then(r => r.json());
if (typeof response.amount !== 'string' || !/^\d+$/.test(response.amount)) {
    throw new Error('Invalid balance response');
}
displayBalance(response.amount);
```

## 6. Audit Tools and Techniques

### Network Traffic Analysis
```bash
# Use browser DevTools Network tab to inspect:
# - All API requests and responses
# - Transaction data being sent
# - Headers (especially Authorization)
# - WebSocket messages

# Or use proxy tools:
# - Burp Suite
# - mitmproxy
# - Charles Proxy
```

### Code Review Patterns
```bash
# Search for dangerous patterns
grep -r "localStorage" src/
grep -r "dangerouslySetInnerHTML" src/
grep -r "eval(" src/
grep -r "privateKey\|mnemonic\|seed" src/
grep -r "console.log" src/  # Check for sensitive data logging
```

### Browser Security Headers Check
```
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
```

## 7. Authentication Flow Audit

### Wallet Connection
```typescript
// Verify wallet connection flow:
// 1. User initiates connection
// 2. Wallet provider prompts for approval
// 3. Only public address shared with dApp
// 4. No private data transmitted

// Check UnlockPanelManager usage
const unlockPanelManager = UnlockPanelManager.init({
    loginHandler: () => {
        // Verify: no sensitive data handling here
        navigate('/dashboard');
    }
});
```

### Session Management
```typescript
// Verify session security:
// - Token expiration enforced
// - Logout clears all session data
// - No persistent sensitive storage

const handleLogout = async () => {
    const provider = getAccountProvider();
    await provider.logout();
    // Verify: session storage cleared
    sessionStorage.clear();
    navigate('/');
};
```

## 8. Audit Checklist

### Transaction Security
- [ ] All transaction data validated before signing
- [ ] User shown clear transaction preview
- [ ] Recipient addresses validated
- [ ] Amount confirmations for large transfers
- [ ] Gas limits appropriate for operation

### Data Security
- [ ] No private keys in any storage
- [ ] No sensitive data in console logs
- [ ] Access tokens not exposed in URLs
- [ ] HTTPS enforced for all API calls

### XSS Prevention
- [ ] No `dangerouslySetInnerHTML` with user input
- [ ] No `eval()` with user input
- [ ] URL redirects validated
- [ ] Content-Security-Policy headers present

### Session Security
- [ ] Token expiration enforced
- [ ] Logout clears all session data
- [ ] Protected routes properly guarded
- [ ] Re-authentication for sensitive operations

## 9. Report Template

```markdown
# dApp Security Audit Report

## Scope
- Application: [name]
- Version: [version]
- Files reviewed: [count]

## Findings

### Critical
| ID | Description | Location | Recommendation |
|----|-------------|----------|----------------|
| C1 | ... | ... | ... |

### High
...

### Medium
...

### Informational
...

## Recommendations Summary
1. [Priority recommendation]
2. ...

## Conclusion
[Overall assessment]
```


# Frontend Audit (Expert)

---
name: mvx_dapp_audit
description: Auditing dApps and standard Frontend flows.
---

# MultiversX dApp Auditor

This skill helps you audit the frontend components of a MultiversX application (`sdk-dapp`).

## 1. Transaction Construction
- **Critical Logic**: The frontend constructs the payload.
- **Attack**: Can a malicious frontend user change the payload before signing?
    - Example: `func@args` -> `func@evil_args`.
- **Mitigation**: The Smart Contract MUST validate everything. Do not trust the frontend to validate inputs.

## 2. Signing Security
- **Blind Signing**: Does the dApp verify what it asks the user to sign?
- **Hash Signing**: Is the user signing a hash (opaque) or a clear message?

## 3. Sensitive Data
- **Local Storage**: Is the private key or mnemonic ever stored in `localStorage`? (Should NEVER be).
- **XSS**: Can an attacker extract the `accessToken`?

## 4. Tools
- **Burp Suite**: Proxy traffic to see what the dApp sends to the API or Blockchain Proxy.
- **Inspect Element**: Check network tab for `POST /transactions` payloads.


# SDK JS Core

---
name: mvx_sdk_js_core
description: Core SDK operations for MultiversX TypeScript/JavaScript - Entrypoints, Network Providers, and Transactions.
---

# MultiversX SDK-JS Core Operations

This skill covers the fundamental building blocks of the `@multiversx/sdk-core` v15 library.

## Entrypoints

Network-specific clients that simplify common operations:

| Entrypoint | Network | Default URL |
|------------|---------|-------------|
| `DevnetEntrypoint` | Devnet | `https://devnet-api.multiversx.com` |
| `TestnetEntrypoint` | Testnet | `https://testnet-api.multiversx.com` |
| `MainnetEntrypoint` | Mainnet | `https://api.multiversx.com` |
| `LocalnetEntrypoint` | Local | `http://localhost:7950` |

```typescript
import { DevnetEntrypoint } from "@multiversx/sdk-core";

// Default API
const entrypoint = new DevnetEntrypoint();

// Custom API
const entrypoint = new DevnetEntrypoint({ url: "https://custom-api.com" });

// Proxy mode (gateway)
const entrypoint = new DevnetEntrypoint({ 
    url: "https://devnet-gateway.multiversx.com", 
    kind: "proxy" 
});
```

## Entrypoint Methods

| Method | Description |
|--------|-------------|
| `createAccount()` | Create a new account instance |
| `createNetworkProvider()` | Get underlying network provider |
| `recallAccountNonce(address)` | Fetch current nonce from network |
| `sendTransaction(tx)` | Broadcast single transaction |
| `sendTransactions(txs)` | Broadcast multiple transactions |
| `getTransaction(txHash)` | Fetch transaction by hash |
| `awaitCompletedTransaction(txHash)` | Wait for finality |

## Network Providers

Lower-level network access:

| Provider | Use Case |
|----------|----------|
| `ApiNetworkProvider` | Standard API queries (recommended) |
| `ProxyNetworkProvider` | Direct node interaction via gateway |

```typescript
const provider = entrypoint.createNetworkProvider();

// Or manual instantiation
import { ApiNetworkProvider } from "@multiversx/sdk-core";

const api = new ApiNetworkProvider("https://devnet-api.multiversx.com", {
    clientName: "my-app",
    requestsOptions: { timeout: 10000 }
});
```

## Provider Methods

| Method | Description |
|--------|-------------|
| `getNetworkConfig()` | Chain ID, gas settings, etc. |
| `getNetworkStatus()` | Current epoch, nonce, etc. |
| `getBlock(blockHash)` | Fetch block data |
| `getAccount(address)` | Account balance, nonce |
| `getAccountStorage(address)` | Contract storage |
| `getTransaction(txHash)` | Transaction details |
| `awaitTransactionCompletion(txHash)` | Wait for finality |
| `queryContract(query)` | VM query (read-only) |

## Transaction Lifecycle

```typescript
// 1. Create account and sync nonce
const account = await Account.newFromPem("wallet.pem");
account.nonce = await entrypoint.recallAccountNonce(account.address);

// 2. Create transaction (via controller)
const controller = entrypoint.createTransfersController();
const tx = await controller.createTransactionForTransfer(
    account, 
    account.getNonceThenIncrement(),
    { receiver, nativeAmount: 1000000000000000000n }
);

// 3. Send
const txHash = await entrypoint.sendTransaction(tx);

// 4. Wait for completion
const result = await entrypoint.awaitCompletedTransaction(txHash);
console.log("Status:", result.status);
```

## Best Practices

1. **Always sync nonce** before creating transactions
2. **Use `awaitCompletedTransaction`** for critical operations
3. **Handle errors** - network calls can fail
4. **Use appropriate timeouts** for long operations
5. **Batch transactions** when possible with `sendTransactions()`


# SDK JS Wallets

---
name: mvx_sdk_js_wallets
description: Wallet and key management for MultiversX TypeScript/JavaScript SDK.
---

# MultiversX SDK-JS Wallets & Signing

This skill covers account management, key derivation, and transaction signing.

## Account Creation

```typescript
import { Account, Address, Mnemonic, UserWallet, UserPem } from "@multiversx/sdk-core";

// From PEM file (testing only - not secure)
const account = await Account.newFromPem("wallet.pem");

// From keystore (production)
const account = await Account.newFromKeystore("wallet.json", "password");

// From entrypoint (generates new)
const account = entrypoint.createAccount();
```

## Mnemonic Operations

```typescript
// Generate new mnemonic (24 words)
const mnemonic = Mnemonic.generate();
const words = mnemonic.getWords();

// Derive keys
const secretKey = mnemonic.deriveKey(0);  // First account
const publicKey = secretKey.generatePublicKey();
const address = publicKey.toAddress();
```

## Wallet Storage

```typescript
// Save mnemonic to keystore
const wallet = UserWallet.fromMnemonic({
    mnemonic: mnemonic.toString(),
    password: "secure-password"
});
wallet.save("wallet.json");

// Save secret key to keystore
const wallet = UserWallet.fromSecretKey({
    secretKey: secretKey,
    password: "secure-password"
});
wallet.save("wallet.json");

// Save to PEM (testing only)
const pem = new UserPem(address.toBech32(), secretKey);
pem.save("wallet.pem");
```

## Transaction Signing

```typescript
// Controller-created transactions are auto-signed
const tx = await controller.createTransactionForTransfer(account, nonce, options);
// tx.signature is already set

// Factory-created transactions need manual signing
const tx = await factory.createTransactionForTransfer(sender, options);
tx.nonce = account.getNonceThenIncrement();
tx.signature = await account.signTransaction(tx);
```

## Message Signing

```typescript
// Sign arbitrary message
const message = new SignableMessage({ message: Buffer.from("Hello") });
const signature = await account.signMessage(message);

// Verify signature
import { MessageSigner } from "@multiversx/sdk-core";
const isValid = MessageSigner.verify(message, signature, publicKey);
```

## Ledger Device

```typescript
// Ledger requires MultiversX app installed
import { LedgerAccount } from "@multiversx/sdk-hw-provider";

const ledger = new LedgerAccount();
await ledger.init();
const address = await ledger.getAddress(0);
```

## Security Best Practices

| Practice | Reason |
|----------|--------|
| Use keystore files | Encrypted with password |
| Never commit PEM files | Plain text private keys |
| Use Ledger for mainnet | Hardware security |
| Validate addresses | Prevent typos |


# SDK JS Tokens

---
name: mvx_sdk_js_tokens
description: Token operations (ESDT/NFT/SFT) for MultiversX TypeScript/JavaScript SDK.
---

# MultiversX SDK-JS Token Operations

This skill covers ESDT (fungible), NFT, and SFT token operations.

## Token Transfers

### Native EGLD Transfer
```typescript
const controller = entrypoint.createTransfersController();

const tx = await controller.createTransactionForTransfer(account, nonce, {
    receiver: Address.newFromBech32("erd1..."),
    nativeAmount: 1000000000000000000n  // 1 EGLD (18 decimals)
});
```

### ESDT Token Transfer
```typescript
import { TokenTransfer } from "@multiversx/sdk-core";

const tx = await controller.createTransactionForTransfer(account, nonce, {
    receiver: receiverAddress,
    tokenTransfers: [
        TokenTransfer.fungibleFromBigInteger("TOKEN-abc123", 1000000n)
    ]
});
```

### NFT/SFT Transfer
```typescript
const tx = await controller.createTransactionForTransfer(account, nonce, {
    receiver: receiverAddress,
    tokenTransfers: [
        TokenTransfer.nftFromBigInteger("NFT-abc123", 1n, 1n)  // nonce=1, quantity=1
    ]
});
```

## Token Issuance

### Issue Fungible Token
```typescript
const controller = entrypoint.createTokenManagementController();

const tx = await controller.createTransactionForIssuingFungible(account, nonce, {
    tokenName: "MyToken",
    tokenTicker: "MTK",
    initialSupply: 1_000_000_000000n,  // With decimals
    numDecimals: 6n,
    canFreeze: false,
    canWipe: true,
    canPause: false,
    canChangeOwner: true,
    canUpgrade: true,
    canAddSpecialRoles: true
});

const txHash = await entrypoint.sendTransaction(tx);
const outcome = await controller.awaitCompletedIssueFungible(txHash);
const tokenIdentifier = outcome[0].tokenIdentifier;
```

### Issue Semi-Fungible Token
```typescript
const tx = await controller.createTransactionForIssuingSemiFungible(account, nonce, {
    tokenName: "MySFT",
    tokenTicker: "SFT",
    canFreeze: false,
    canWipe: true,
    canPause: false,
    canTransferNFTCreateRole: true,
    canChangeOwner: true,
    canUpgrade: true,
    canAddSpecialRoles: true
});
```

### Register and Set NFT Roles
```typescript
const tx = await controller.createTransactionForRegisteringAndSettingRoles(account, nonce, {
    tokenName: "MyNFT",
    tokenTicker: "MNFT",
    tokenType: "NonFungibleESDT"
});
```

## Token Role Management

```typescript
// Set special role
const tx = await controller.createTransactionForSettingSpecialRole(account, nonce, {
    tokenIdentifier: "TOKEN-abc123",
    user: userAddress,
    addRoleLocalMint: true,
    addRoleLocalBurn: true
});
```

## Token Queries

```typescript
const provider = entrypoint.createNetworkProvider();

// Get specific token
const token = await provider.getTokenOfAccount(address, "TOKEN-abc123");

// Get all fungible tokens
const tokens = await provider.getFungibleTokensOfAccount(address);

// Get all NFTs
const nfts = await provider.getNonFungibleTokensOfAccount(address);
```

## Best Practices

1. **Decimals**: EGLD has 18 decimals, custom tokens vary
2. **Token identifiers**: Format is `TICKER-hexhash` (e.g., `USDC-a1b2c3`)
3. **NFT nonces**: Start at 1, increment per mint
4. **Gas**: Token operations need ~60,000,000+ gas


# SDK JS Contracts

---
name: mvx_sdk_js_contracts
description: Smart contract operations for MultiversX TypeScript/JavaScript SDK.
---

# MultiversX SDK-JS Smart Contract Operations

This skill covers ABI loading, deployments, calls, queries, and parsing.

## ABI Loading

```typescript
import { Abi } from "@multiversx/sdk-core";
import { promises } from "fs";

// From file
const abiJson = await promises.readFile("contract.abi.json", "utf8");
const abi = Abi.create(JSON.parse(abiJson));

// From URL
const response = await axios.get("https://example.com/contract.abi.json");
const abi = Abi.create(response.data);

// Manual construction
const abi = Abi.create({
    endpoints: [{
        name: "add",
        inputs: [{ type: "BigUint" }],
        outputs: [{ type: "BigUint" }]
    }]
});
```

## Smart Contract Controller

```typescript
const controller = entrypoint.createSmartContractController(abi);
```

## Deployment

```typescript
const bytecode = await promises.readFile("contract.wasm");

const tx = await controller.createTransactionForDeploy(account, nonce, {
    bytecode: bytecode,
    gasLimit: 60_000_000n,
    arguments: [42]  // Constructor args (plain values with ABI)
});

const txHash = await entrypoint.sendTransaction(tx);
const outcome = await controller.awaitCompletedDeploy(txHash);
const contractAddress = outcome[0].contractAddress;
```

## Contract Calls

```typescript
// With ABI - use plain values
const tx = await controller.createTransactionForExecute(account, nonce, {
    contract: contractAddress,
    function: "add",
    arguments: [42],
    gasLimit: 5_000_000n
});

// Without ABI - use TypedValue
import { U32Value, BigUintValue } from "@multiversx/sdk-core";
const tx = await controller.createTransactionForExecute(account, nonce, {
    contract: contractAddress,
    function: "add",
    arguments: [new U32Value(42)],
    gasLimit: 5_000_000n
});
```

## Transfer & Execute (Send tokens to SC)

```typescript
const tx = await controller.createTransactionForExecute(account, nonce, {
    contract: contractAddress,
    function: "deposit",
    arguments: [],
    gasLimit: 10_000_000n,
    nativeTransferAmount: 1_000_000_000_000_000_000n,  // 1 EGLD
    tokenTransfers: [
        TokenTransfer.fungibleFromBigInteger("TOKEN-abc123", 1000n)
    ]
});
```

## VM Queries (Read-Only)

```typescript
const controller = entrypoint.createSmartContractController(abi);

const result = await controller.queryContract({
    contract: contractAddress,
    function: "getSum",
    arguments: []
});

// Parsed output (with ABI)
const sum = result[0];  // Automatically typed
```

## Upgrades

```typescript
const newBytecode = await promises.readFile("contract_v2.wasm");

const tx = await controller.createTransactionForUpgrade(account, nonce, {
    contract: contractAddress,
    bytecode: newBytecode,
    gasLimit: 60_000_000n,
    arguments: []
});
```

## RelayedV3 Contract Calls

```typescript
const tx = await controller.createTransactionForExecute(account, nonce, {
    contract: contractAddress,
    function: "endpoint",
    arguments: [],
    gasLimit: 5_050_000n,  // +50,000 for relayed
    relayer: relayerAddress
});

tx.relayerSignature = await relayer.signTransaction(tx);
```

## Best Practices

1. **Always use ABI** when available for type safety
2. **Gas estimation**: Start high, optimize later
3. **Simulate first**: Use `simulateTransaction()` before real calls
4. **Parse outcomes**: Use `awaitCompletedExecute()` for return values
