---
name: stellar-skills
description: Stellar blockchain and Soroban smart contract development. SDKs, wallets, DeFi protocols, and ecosystem tools. Use when building dApps on Stellar, writing Soroban contracts, integrating wallets, or working with Horizon/Soroban RPC.
---

# Stellar & Soroban Development

## Quick Reference

### Networks

| Network | Horizon | Soroban RPC | Explorer |
|---------|---------|-------------|----------|
| **Mainnet** | `horizon.stellar.org` | `soroban-rpc.mainnet.stellar.gateway.fm` | stellar.expert |
| **Testnet** | `horizon-testnet.stellar.org` | `soroban-testnet.stellar.org` | stellar.expert/explorer/testnet |
| **Futurenet** | `horizon-futurenet.stellar.org` | `rpc-futurenet.stellar.org` | stellarchain.io |

### Faucet (Testnet)

```bash
curl "https://friendbot.stellar.org?addr=YOUR_PUBLIC_KEY"
```

---

## CLIs & Scaffolds

| Tool | Use |
|------|-----|
| **stellar CLI** | Build, deploy, invoke contracts, generate TS bindings |
| **Scaffold Stellar** | Full project (Soroban + frontend + local network) → scaffoldstellar.org |
| **Stellar Lab** | Web tool for network experiments → lab.stellar.org |

---

## SDKs

| Library | Purpose |
|---------|---------|
| `@stellar/stellar-sdk` | Official JS/TS SDK (classic + Soroban) |
| `soroban-sdk` (Rust) | Write Soroban smart contracts |
| `@stellar/freighter-api` | Direct Freighter wallet integration |
| `@creit.tech/stellar-wallets-kit` | Multi-wallet abstraction → stellarwalletskit.dev |

---

## Workflows

### Workflow 1: Connect Wallet (Stellar Wallets Kit)

```typescript
import { StellarWalletsKit, WalletNetwork, allowAllModules } from '@creit.tech/stellar-wallets-kit';

const kit = new StellarWalletsKit({
  network: WalletNetwork.TESTNET,
  selectedWalletId: 'freighter',
  modules: allowAllModules(),
});

// Open modal to select wallet
await kit.openModal({
  onWalletSelected: async (option) => {
    kit.setWallet(option.id);
    const { address } = await kit.getAddress();
    console.log('Connected:', address);
  }
});
```

### Workflow 2: Deploy Contract (stellar CLI)

```bash
# Build contract
stellar contract build

# Deploy to testnet
stellar contract deploy \
  --wasm target/wasm32-unknown-unknown/release/my_contract.wasm \
  --source alice \
  --network testnet

# Generate TypeScript bindings
stellar contract bindings typescript \
  --contract-id CXXXXX... \
  --output-dir ./src/contracts/my-contract \
  --network testnet
```

### Workflow 3: Invoke Contract

```typescript
import * as StellarSdk from '@stellar/stellar-sdk';

const server = new StellarSdk.SorobanRpc.Server('https://soroban-testnet.stellar.org');
const contract = new StellarSdk.Contract('CXXXXX...');

// Build transaction
const tx = new StellarSdk.TransactionBuilder(account, { fee: '100' })
  .addOperation(contract.call('method_name', ...args))
  .setTimeout(30)
  .build();

// Simulate
const simulated = await server.simulateTransaction(tx);

// Sign with wallet kit
const { signedTxXdr } = await kit.signTransaction(tx.toXDR());

// Submit
const result = await server.sendTransaction(
  StellarSdk.TransactionBuilder.fromXDR(signedTxXdr, StellarSdk.Networks.TESTNET)
);
```

### Workflow 4: Sign & Submit with Wallet Kit

```typescript
// For Soroban transactions that need simulation
const signedTx = await kit.signTransaction(tx.toXDR(), {
  networkPassphrase: StellarSdk.Networks.TESTNET,
});

// Submit and poll for result
const sendResponse = await server.sendTransaction(
  StellarSdk.TransactionBuilder.fromXDR(signedTx.signedTxXdr, StellarSdk.Networks.TESTNET)
);

if (sendResponse.status === 'PENDING') {
  let result = await server.getTransaction(sendResponse.hash);
  while (result.status === 'NOT_FOUND') {
    await new Promise(r => setTimeout(r, 1000));
    result = await server.getTransaction(sendResponse.hash);
  }
}
```

---

## OpenZeppelin Contracts (Soroban)

Audited contracts. **Check before writing custom logic.**

| Category | Includes |
|----------|----------|
| **Tokens** | Fungible, NFT, RWAs, Stablecoin, Vault (SEP-56) |
| **Access** | Ownable, Role-Based Access Control |
| **Utils** | Pausable, Upgradeable, Merkle Distributor |

Wizard: https://wizard.openzeppelin.com
Docs: https://docs.openzeppelin.com/stellar-contracts

---

## Security

| Tool | Use |
|------|-----|
| **Scout Audit** | Static analysis for Soroban → github.com/CoinFabrik/scout-soroban |
| **scout-actions** | GitHub Action for PR checks |

```bash
# Run Scout locally
cargo install scout-audit
scout-audit --path ./contracts
```

---

## Ecosystem

### DeFi & Protocols

| Project | What |
|---------|------|
| **Soroswap** | AMM/DEX → soroswap.finance |
| **Defindex** | Yield aggregator → defindex.io |
| **Allbridge** | Cross-chain bridge → allbridge.io |
| **Reflector** | Oracles (SEP-40) → reflector.network |

### Infrastructure & Services

| Project | What |
|---------|------|
| **Trustless Work** | Programmable escrows → trustlesswork.com |
| **Mercury** | Custom indexer (Retroshades, Zephyr) → mercurydata.app |
| **Horizon API** | Official API for network queries |
| **Anchor Platform** | On/off-ramps (SEP-10, SEP-24, SEP-31) |
| **Stellar Disbursement Platform** | Mass payouts infrastructure |
| **MoneyGram Ramps** | USDC on/off-ramp at retail locations |

### Block Explorers

| Explorer | Networks |
|----------|----------|
| **StellarExpert** | Mainnet, Testnet → stellar.expert |
| **StellarChain** | Mainnet, Testnet, Futurenet → stellarchain.io |
| **Stellar Explorer** | All networks |

### RPC Providers

| Provider | Notes |
|----------|-------|
| SDF (public) | Default, rate limited |
| Validation Cloud | Free + premium |
| Ankr | Horizon + Soroban RPC |
| QuickNode | Performance tiers |

---

## SEPs (Stellar Ecosystem Proposals)

| SEP | Purpose |
|-----|---------|
| **SEP-10** | Web Authentication |
| **SEP-24** | Interactive deposits/withdrawals |
| **SEP-41** | Soroban token interface |
| **SEP-56** | Tokenized Vault Standard |

All SEPs: github.com/stellar/stellar-protocol/tree/master/ecosystem

---

## Decision Framework

```
What are you building?
│
├─ **Smart Contract** (Soroban)
│  ├─ Token? → Check OpenZeppelin first
│  ├─ DeFi? → Integrate with Soroswap/Defindex
│  └─ Custom logic → Use soroban-sdk + Scout audit
│
├─ **Frontend dApp**
│  ├─ Wallet connection → Stellar Wallets Kit
│  ├─ Contract interaction → @stellar/stellar-sdk
│  └─ Full scaffold → Scaffold Stellar
│
├─ **Backend/Indexing**
│  ├─ Simple queries → Horizon API
│  ├─ Custom indexing → Mercury
│  └─ Real-time → Soroban RPC subscriptions
│
└─ **Payments/Ramps**
   ├─ On/off-ramp → Anchor Platform
   └─ Mass payouts → Stellar Disbursement Platform
```

---

## Docs

- https://developers.stellar.org
- https://soroban.stellar.org/docs
- https://stellarwalletskit.dev

**Principle**: Check for existing tools/protocols before writing custom code.
