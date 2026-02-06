---
name: hoosat-dev
description: "Comprehensive Hoosat blockchain development toolkit for building transactions, integrating wallets, creating dApps, and interacting with the Hoosat network (a Kaspa fork using Blake3 and Hoohash). Use when working with Hoosat blockchain development including: (1) Building and broadcasting HTN transactions, (2) Generating addresses with hoosat: prefix, (3) Creating dApps using hoosat-sdk or hoosat-sdk-web, (4) Integrating Hoosat wallets, (5) Using Hoosat SDKs (Node.js hoosat-sdk, Browser hoosat-sdk-web, Motoko hoosat-mo for IC), (6) Using the Hoosat REST API at proxy.hoosat.net, (7) Working with HRC20 tokens. Supports JavaScript/TypeScript (Node.js and Browser), Go, and Motoko (Internet Computer) development."
---

# Hoosat Development

## Overview

This skill provides comprehensive support for Hoosat blockchain development. Hoosat is a Kaspa fork that uses BLAKE3 and Hoohash consensus algorithms with HTN as its native token.

**Key Characteristics:**
- **Ticker**: HTN
- **Address Prefix**: `hoosat:` (mainnet), `hoosattest:` (testnet)
- **Consensus**: BLAKE3 and Hoohash (not kHash like Kaspa)
- **SDKs**: hoosat-sdk (Node.js), hoosat-sdk-web (Browser), hoosat-mo (Motoko/IC)
- **API**: https://proxy.hoosat.net/api/v1 (no auth required)
- **Token Standard**: HRC20 (KRC20 equivalent, in progress)

**GitHub Repositories:**
- https://github.com/hoosatnetwork
- https://github.com/Namp88

## Quick Start

### Check Network Status

To get current network information (block height, supply, hashrate, etc.), see the **Checking Network Status** section in [references/api-reference.md](references/api-reference.md#checking-network-status).

### Choose Your SDK

| Environment | Package | Install |
|------------|---------|---------|
| **Node.js** | `hoosat-sdk` | `npm install hoosat-sdk` |
| **Browser** | `hoosat-sdk-web` | `npm install hoosat-sdk-web` |
| **Motoko (IC)** | `hoosat-mo` | `mops install hoosat-mo` |

### Generate a Hoosat Address

**Node.js (hoosat-sdk):**
```javascript
import { HoosatCrypto } from 'hoosat-sdk';

const wallet = HoosatCrypto.generateKeyPair('mainnet');
console.log('Address:', wallet.address);
console.log('Private Key:', wallet.privateKey.toString('hex'));
```

**Browser (hoosat-sdk-web):**
```javascript
import { HoosatCrypto } from 'hoosat-sdk-web';

const wallet = HoosatCrypto.generateKeyPair('mainnet');
```

**Python:**
```python
python scripts/generate-address.py --network mainnet
```

### Check Balance

**Node.js:**
```javascript
import { HoosatClient, HoosatUtils } from 'hoosat-sdk';

const client = new HoosatClient({
  host: '54.38.176.95',
  port: 42420
});

const result = await client.getBalance('hoosat:qz7ulu8mmmul6hdcnssmjnt28h2xfer8dz9nfqamvvh86ngef4q8dvzxcjdqe');
if (result.ok) {
  const htn = HoosatUtils.sompiToAmount(result.result.balance);
  console.log(`Balance: ${htn} HTN`);
}
```

**Browser:**
```javascript
import { HoosatWebClient } from 'hoosat-sdk-web';

const client = new HoosatWebClient({
  baseUrl: 'https://proxy.hoosat.net/api/v1'
});

const balance = await client.getBalance(address);
```

**REST API:**
```bash
curl https://proxy.hoosat.net/api/v1/address/hoosat:qz7ulu8mmmul6hdcnssmjnt28h2xfer8dz9nfqamvvh86ngef4q8dvzxcjdqe/balance
```

### Send a Transaction

**Node.js:**
```javascript
import { HoosatClient, HoosatCrypto, HoosatTxBuilder, HoosatUtils } from 'hoosat-sdk';

const client = new HoosatClient({ host: '54.38.176.95', port: 42420 });
const wallet = HoosatCrypto.importKeyPair(process.env.WALLET_PRIVATE_KEY);

// Get UTXOs
const utxosResult = await client.getUtxosByAddresses([wallet.address]);
const utxos = utxosResult.result.utxos;

// Calculate minimum fee
const minFee = await client.calculateMinFee(wallet.address);

// Build transaction
const builder = new HoosatTxBuilder();
for (const utxo of utxos) {
  builder.addInput(utxo, wallet.privateKey);
}
builder
  .addOutput(recipientAddress, HoosatUtils.amountToSompi('1.0'))
  .setFee(minFee)
  .addChangeOutput(wallet.address);

const signedTx = builder.sign();

// Submit
const result = await client.submitTransaction(signedTx);
if (result.ok) {
  console.log('TX ID:', result.result.transactionId);
}
```

### Sign a Message

**Node.js:**
```javascript
import { HoosatSigner } from 'hoosat-sdk';

const signature = HoosatSigner.signMessage(message, wallet.privateKey);
const isValid = HoosatSigner.verifyMessage(message, signature, wallet.publicKey);
```

### Motoko (Internet Computer)

```motoko
import Wallet "mo:hoosat-mo/wallet";
import Address "mo:hoosat-mo/address";

let wallet = Wallet.createMainnetWallet("key", ?"hoosat");
let result = await wallet.sendTransaction(from, to, amount, null, null);
```

## SDK Modules Overview

### HoosatClient (Node.js)
Main client for gRPC connection to Hoosat nodes.

```javascript
const client = new HoosatClient({
  host: '54.38.176.95',
  port: 42420
});
```

**Key Methods:**
- `getBalance(address)` - Get address balance
- `getUtxosByAddresses(addresses)` - Get UTXOs
- `submitTransaction(tx)` - Submit signed transaction
- `calculateMinFee(address)` - Calculate minimum fee
- `events.subscribeToUtxoChanges(addresses)` - Real-time UTXO monitoring

### HoosatCrypto (Node.js & Browser)
Cryptographic operations with BLAKE3 hashing.

**Key Methods:**
- `generateKeyPair(network)` - Generate new wallet
- `importKeyPair(privateKey, network)` - Import existing wallet
- `signTransactionInput(tx, index, privateKey, utxo)` - Sign transaction input
- `blake3Hash(data)` - BLAKE3 hashing

### HoosatTxBuilder (Node.js & Browser)
Fluent transaction builder.

```javascript
const builder = new HoosatTxBuilder();
builder
  .addInput(utxo, privateKey)
  .addOutput(recipientAddress, amount)
  .setFee(fee)
  .addChangeOutput(changeAddress);
  
const signedTx = builder.sign();
```

### HoosatUtils (Node.js & Browser)
Utility functions for validation and conversion.

- `amountToSompi(htn)` - Convert HTN to sompi (1 HTN = 100M sompi)
- `sompiToAmount(sompi)` - Convert sompi to HTN
- `isValidAddress(address)` - Validate address
- `getAddressNetwork(address)` - Get network from address

### HoosatEventManager (Node.js)
Real-time event streaming.

```javascript
await client.events.subscribeToUtxoChanges([address]);
client.events.on(EventType.UtxoChange, (notification) => {
  console.log('Balance changed!');
});
```

### HoosatQR (Node.js & Browser)
QR code generation for payments.

```javascript
const qr = await HoosatQR.generatePaymentQR({
  address: merchantAddress,
  amount: HoosatUtils.amountToSompi('1.5'),
  label: 'My Store',
  message: 'Order #12345'
});
```

### HoosatSigner (Node.js & Browser)
Message signing for authentication.

```javascript
const signature = HoosatSigner.signMessage(message, privateKey);
const isValid = HoosatSigner.verifyMessage(message, signature, publicKey);
```

## Error Handling

All SDK methods use a consistent error handling pattern:

```typescript
interface BaseResult<T> {
  ok: boolean;
  result?: T;
  error?: string;
}

// Usage
const result = await client.getBalance(address);
if (result.ok) {
  console.log('Balance:', result.result.balance);
} else {
  console.error('Error:', result.error);
}
```

## Network Types

- **Mainnet**: Production network (prefix: `hoosat:`)
- **Testnet**: Testing network (prefix: `hoosattest:`)

## Address Formats

Hoosat uses Bech32 encoding:

- Mainnet: `hoosat:qz7ulu8mmmul6hdcnssmjnt28h2xfer8dz9nfqamvvh86ngef4q8dvzxcjdqe`
- Testnet: `hoosattest:qqkqkzjvr7zwxxmjxjkmxx`

## Unit Conversion

- 1 HTN = 100,000,000 sompi
- Dust threshold: 1,000 sompi minimum
- Use `HoosatUtils.amountToSompi()` and `HoosatUtils.sompiToAmount()` for conversions

## SDK References

For detailed SDK documentation:

- **Node.js SDK**: See [references/hoosat-sdk.md](references/hoosat-sdk.md)
- **Browser SDK**: See [references/hoosat-sdk-web.md](references/hoosat-sdk-web.md)
- **Motoko Package**: See [references/hoosat-mo.md](references/hoosat-mo.md)
- **REST API**: See [references/api-reference.md](references/api-reference.md)

## Integration Guides

### Wallet Integration

See [references/wallet-integration.md](references/wallet-integration.md) for:
- Wallet connection patterns
- Transaction signing flows
- Address management
- Network switching

### Node Operations

See [references/node-operations.md](references/node-operations.md) for:
- Docker deployment
- Binary installation
- Building from source
- RPC node setup

### dApp Development

When building a Hoosat dApp:

1. **Setup**: Use `hoosat-sdk-web` for browser compatibility
2. **Wallet Connection**: Implement wallet adapter using HoosatCrypto
3. **State Management**: Track balances, transactions, and UTXOs
4. **Transaction Building**: Use HoosatTxBuilder with UTXO selection
5. **Error Handling**: Handle BaseResult<T> pattern

Use the `dapp-template/` asset for a starter React/Next.js dApp.

### Block Explorer

To build a block explorer:

1. **Data Source**: Use Hoosat REST API or run your own node
2. **Indexing**: Index blocks, transactions, and addresses
3. **API Layer**: Build REST/GraphQL API using HoosatWebClient
4. **Frontend**: Display blocks, transactions, addresses

Use the `explorer-template/` asset for a starter block explorer.

## HRC20 Tokens

HRC20 is Hoosat's token standard (KRC20 equivalent). For token development:

See [references/hrc20-tokens.md](references/hrc20-tokens.md) for:
- Token contract structure
- Transfer and approval mechanisms
- Integration patterns

## Agent Wallet System

**PRIMARY:** Use `agent-wallet.py` for ALL wallet operations (create, manage, transact).

## Agent Wallet System

### Features

- **Encrypted Wallet Storage**: AES-256 encryption with PBKDF2 key derivation
- **Balance Queries**: Real-time balance checking via REST API
- **Transaction Execution**: Transfer HTN with auto-approve or confirmation
- **Address Book**: Save and label frequently used addresses
- **UTXO Consolidation**: Optimize wallet by combining small UTXOs

The agent wallet system enables AI agents to actively manage Hoosat wallets and execute transactions.

### Features

- **Encrypted Wallet Storage**: AES-256 encryption with PBKDF2 key derivation
- **Balance Queries**: Real-time balance checking via REST API
- **Transaction Execution**: Transfer HTN with auto-approve or confirmation
- **Address Book**: Save and label frequently used addresses
- **UTXO Consolidation**: Optimize wallet by combining small UTXOs

### Agent Execution Workflows

**IMPORTANT: When user gives natural language commands, EXECUTE these workflows using the agent-wallet.py script.**

#### Initialize Wallet System
**User says:** "Initialize hoosat wallet", "Set up wallet system", "Initialize agent wallets"

**Agent actions:**
1. Check if already initialized: `test -f ~/.hoosat-wallets/wallets.enc`
2. If not initialized:
   - Ask user for master password or generate one
   - Execute: `python3 {skill_path}/scripts/agent-wallet.py`
   - Call `manager.initialize(password)` 
   - Confirm: "Wallet system initialized at ~/.hoosat-wallets/"

#### Create Wallet
**User says:** "Create wallet [name] on [network]", "Make a [name] wallet", "Generate wallet for [purpose]", "Give me a wallet"

**Agent actions:**
1. Check if wallet system is initialized: `python3 scripts/agent-wallet.py list`
2. If not initialized: `python3 scripts/agent-wallet.py init`
3. Create wallet: `python3 scripts/agent-wallet.py create [name] --network [network]`
4. Show result to user

#### Check Balance
**User says:** "Check balance of [wallet]", "How much HTN in [wallet]?", "What's the balance?"

**Agent actions:**
1. Execute: `python3 {skill_path}/scripts/agent-transact.py`
2. Call: `executor.get_balance(wallet_name)`
3. Convert sompi to HTN and display
4. If error, explain (wallet not found, network issue, etc.)

#### Transfer Funds
**User says:** "Transfer [amount] HTN from [wallet] to [address]", "Send [amount] to [address]"

**Agent actions:**
1. Resolve recipient (check address book if label used)
2. Check if auto-approve is enabled for this wallet/amount
3. If confirmation needed, ask: "Send [amount] HTN to [recipient]?"
4. Execute: `python3 {skill_path}/scripts/agent-transact.py`
5. Call: `executor.transfer(from_wallet, to_address, amount)`
6. Display transaction result (success/failure, tx ID)

#### List Wallets
**User says:** "List my wallets", "Show wallets", "What wallets do I have?"

**Agent actions:**
1. Execute: `python3 {skill_path}/scripts/agent-wallet.py`
2. Call: `manager.list_wallets()`
3. Display names, addresses, networks

#### Add Address to Book
**User says:** "Save address [label] as [address]", "Add [label] to address book"

**Agent actions:**
1. Execute: `python3 {skill_path}/scripts/agent-wallet.py`
2. Call: `manager.add_address(label, address)`
3. Confirm: "Address saved"

#### Consolidate UTXOs
**User says:** "Consolidate UTXOs in [wallet]", "Compound UTXOs", "Optimize [wallet]"

**Agent actions:**
1. Check current UTXO count
2. If > 10 UTXOs, suggest consolidation
3. Ask for confirmation
4. Execute: `python3 {skill_path}/scripts/agent-transact.py`
5. Call: `executor.consolidate_utxos(wallet_name)`

### Quick Reference Commands

```
Initialize: "Initialize hoosat wallet system"
Create:     "Create wallet [name] on [network]"
Balance:    "Check balance of [wallet]"  
Transfer:   "Transfer [amount] HTN from [wallet] to [address]"
List:       "List my wallets"
Address:    "Save address [label] as [address]"
Consolidate:"Consolidate UTXOs in [wallet]"
```

### Security

- Master password required to unlock (stored in `HOOSAT_AGENT_PASSWORD` env var)
- Session timeout: 1 hour
- Auto-approve: Configurable per-wallet limits
- Dry-run mode: Test transactions without broadcasting

### Configuration

Located at: `~/.hoosat-wallets/config.json`

```json
{
  "autoApprove": {
    "enabled": false,
    "wallets": {
      "mining": {
        "enabled": true,
        "maxAmount": "1000000000"
      }
    }
  },
  "features": {
    "dryRun": true
  }
}
```

### Scripts

- `agent-wallet.py`: Main wallet management
- `agent-crypto.py`: Encryption/decryption utilities  
- `agent-transact.py`: Transaction execution

See [references/agent-wallet-guide.md](references/agent-wallet-guide.md) for complete documentation.

### Setup and Dependencies

**Recommended Installation (Pure Python - No Compilation):**
```bash
pip3 install ecdsa bech32 blake3 base58
```

**Alternative with secp256k1 (requires compilation):**
```bash
# Install pkg-config first (macOS)
brew install pkg-config

# Then install Python packages
pip3 install secp256k1 bech32 blake3 base58
```

**For Agent Wallet System (additional dependencies):**
```bash
pip3 install cryptography requests
```

**macOS Installation (if standard pip fails):**
```bash
# Option 1: Use --user flag
pip3 install --user ecdsa bech32 blake3 base58 cryptography requests

# Option 2: Use --break-system-packages (not recommended but works)
pip3 install --break-system-packages ecdsa bech32 blake3 base58 cryptography requests

# Option 3: Use Homebrew Python
brew install python
/opt/homebrew/bin/pip3 install ecdsa bech32 blake3 base58 cryptography requests
```

### State Management

The agent maintains wallet state across conversations:

1. **Persistent Storage**: `~/.hoosat-wallets/` directory
   - `wallets.enc` - Encrypted wallet data
   - `address-book.json` - Saved addresses
   - `config.json` - Agent configuration
   - `transactions.log` - Transaction history

2. **Session State**:
   - `HOOSAT_AGENT_PASSWORD` env var for current session
   - 1-hour timeout (auto-lock)
   - Re-authentication required after timeout

3. **Context Awareness**:
   - Agent remembers current wallet directory
   - Tracks which wallets are unlocked
   - Maintains address book mappings

### Error Handling

Common errors and responses:

**"Wallet system locked"**
- Ask for password: "Please provide wallet password to unlock"
- Set: `export HOOSAT_AGENT_PASSWORD=your_password`

**"No such file or directory" (dependencies)**
- Install: `pip3 install cryptography requests`

**"Insufficient balance"**
- Check balance first
- Verify network (mainnet vs testnet)

**"Invalid address"**
- Check format: must start with `hoosat:` or `hoosattest:`
- Verify no typos

**"Wallet already exists"**
- Use different name
- Or delete existing: "Delete wallet [name] first"

### Best Practices for Agents

1. **Always confirm high-value transactions** (> 1 HTN)
2. **Check dry-run mode** before real transactions
3. **Suggest testnet** for new users
4. **Remind about backups** after wallet creation
5. **Lock session** when user indicates they're done

## Resources

### References

- **api-reference.md**: Hoosat REST API documentation (proxy.hoosat.net)
- **hoosat-sdk.md**: Node.js SDK documentation
- **hoosat-sdk-web.md**: Browser SDK documentation
- **hoosat-mo.md**: Motoko (Internet Computer) documentation
- **wallet-integration.md**: Wallet integration patterns
- **node-operations.md**: Node operations guide
- **hrc20-tokens.md**: HRC20 token standard
- **agent-wallet-guide.md**: Agent wallet system documentation

### Assets

- **dapp-template/**: React/Next.js dApp starter using hoosat-sdk-web
- **explorer-template/**: Block explorer starter

## Best Practices

1. **Always validate addresses** before using them (check `hoosat:` or `hoosattest:` prefix)
2. **Handle UTXO selection** carefully to avoid dust outputs (min 1000 sompi)
3. **Implement proper error handling** using BaseResult<T> pattern
4. **Test on testnet** before mainnet deployment
5. **Use fee estimation** via `client.calculateMinFee()` for proper fees
6. **Secure private keys** - never expose them in client-side code
7. **Use BLAKE3 hashing** for any custom cryptographic operations
8. **Convert amounts properly** using HoosatUtils (1 HTN = 100M sompi)

## Getting Help

- **Developer Hub**: https://hub.hoosat.net/
- **REST API Docs**: https://proxy.hoosat.net/docs
- **GitHub (Network)**: https://github.com/hoosatnetwork
- **GitHub (Developer)**: https://github.com/Namp88
- **GitHub (Organization)**: https://github.com/Hoosat-Oy
- **Discord**: https://discord.gg/mFBfNpNA
- **Twitter**: https://x.com/HoosatNetwork
- **Telegram**: https://t.me/HoosatNetwork
- **Official Website**: https://network.hoosat.fi
- **Motoko Package**: https://mops.one/hoosat-mo


