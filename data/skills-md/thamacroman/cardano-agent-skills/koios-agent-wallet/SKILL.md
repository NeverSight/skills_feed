---
name: koios-agent-wallet
description: "Quick setup of key-based Cardano agent wallets with MeshJS (MeshWallet) and KoiosProvider: generate wallet (no mnemonic), register stake address, and stake to a pool. Use when users ask to generate a wallet, register it, stake it, send transactions, or query wallet state via Koios."
---

# koios-agent-wallet

## Operating rules (must follow)

- Default to mainnet unless the user explicitly requests preprod/preview/guild.
- Confirm target network (mainnet, preprod, preview, guild) before giving endpoints if unclear.
- Use KoiosProvider for read + submit; do not suggest it for key generation.
- Never request seed phrases or private keys; keep examples with placeholder addresses only.
- Agent runtime must not use mnemonic phrases for signing/staking; use `cli` keys or `root` key mode only.
- Use the correct Koios base URL per network and confirm with the user if unsure.
- Staking requires a stake signing key; if only a payment key is available, staking cannot be signed.

## Quickstart workflow

1. Confirm key-based setup and environment

   - Ask: CLI-generated signing keys or root private key?
   - If user only has a mnemonic, instruct them to derive/export keys offline first; do not use mnemonic directly in agent runtime.
   - Ask: Node.js or browser? TypeScript or JavaScript?

2. Provide key-based wallet creation path

   - **When the user wants a new wallet:** run `scripts/generate-key-based-wallet.js` from the skill directory. It creates payment + stake keypairs and prints base address, stake address, and `PAYMENT_SKEY_CBOR_HEX` / `STAKE_SKEY_CBOR_HEX`. Optionally set `WALLET_DIR=./wallet` to write `addresses.json`, `payment.skey`, `stake.skey`, and (if `@noble/ed25519` is installed) `payment.vkey`, `stake.vkey`. Use those CBOR hex values with `agent-wallet.js` for send/stake.
   - Use MeshWallet for key-based wallets (CLI keys or root key).
   - For staking, require both payment.skey and stake.skey (or a root key).
   - If CLI keys are needed and the user does not have them, use `scripts/generate-key-based-wallet.js` (MeshJS + Koios only; no cardano-cli).
   - If mnemonic is provided to the agent, fail fast with a clear error and request CLI/root key input.

3. Provide Koios base URL for the network

   - Mainnet: `https://api.koios.rest`
   - Preprod: `https://preprod.koios.rest`
   - Preview: `https://preview.koios.rest`
   - Guild: `https://guild.koios.rest`
   - Use the OpenAPI docs at the base URL to confirm endpoint paths.

4. Verify funding with Koios

   - Use `KoiosProvider.fetchAddressUTxOs` or `provider.get(...)` with an OpenAPI endpoint.
   - If the wallet is unfunded on a testnet, direct the user to a faucet before retrying.

5. Core actions (must support)
   - Send ADA transactions with MeshTxBuilder.
   - Register and delegate stake with MeshTxBuilder + `deserializePoolId`.
   - Confirm staking status with `provider.fetchAccountInfo`.

## MeshJS key-based wallet (MeshWallet)

### Koios provider (recommended for agent read-only queries)

```typescript
import { KoiosProvider } from "@meshsdk/core";

const provider = new KoiosProvider("api", "<KOIOS_API_KEY>"); // api=mainnet
```

Network values: `api` (mainnet), `preview`, `preprod`, `guild`.

### Load from Cardano CLI keys (recommended for agents)

```typescript
import { MeshWallet } from "@meshsdk/core";

const wallet = new MeshWallet({
  networkId: 1, // 1 = mainnet
  fetcher: provider,
  submitter: provider,
  key: {
    type: "cli",
    payment: "<PAYMENT_SKEY_CBOR_HEX>",
    stake: "<STAKE_SKEY_CBOR_HEX>", // required for staking
  },
});

await wallet.init();
const address = await wallet.getChangeAddress();
console.log(address);
```

### Load from a root private key (alternative)

```typescript
import { MeshWallet } from "@meshsdk/core";

const wallet = new MeshWallet({
  networkId: 1, // 1 = mainnet
  fetcher: provider,
  submitter: provider,
  key: {
    type: "root",
    bech32: "xprv1...", // root private key (keep secure)
  },
});

await wallet.init();
const address = await wallet.getChangeAddress();
console.log(address);
```

### Read-only wallet (address only)

```typescript
import { MeshWallet } from "@meshsdk/core";

const wallet = new MeshWallet({
  networkId: 1, // 1 = mainnet
  fetcher: provider,
  key: {
    type: "address",
    address: "addr1...",
  },
});

await wallet.init();
const address = await wallet.getChangeAddress();
console.log(address);
```

## Minimal Koios check (UTxOs)

### TypeScript (KoiosProvider)

```typescript
import { KoiosProvider } from "@meshsdk/core";

const provider = new KoiosProvider("api", "<KOIOS_API_KEY>");
const address = "addr1...";

const utxos = await provider.fetchAddressUTxOs(address);
console.log(utxos);
```

## Funding + confirmation checklist

1. Funding

   - Check UTxOs: `provider.fetchAddressUTxOs(address)`
   - Ensure enough ADA for fees and (if first-time staking) the stake deposit.

2. Staking readiness

   - Get reward address: `const rewardAddress = (await wallet.getRewardAddresses())[0]`
   - Check registration/delegation: `provider.fetchAccountInfo(rewardAddress)`

3. Confirmation after submit
   - Use `provider.fetchTxInfo(txHash)` or poll until confirmed.

## Agent wallet dossier (output format)

```
=== Agent Wallet Dossier ===
Network: mainnet (api)
Payment Address: addr1...
Stake Address: stake1...
Koios Provider: api
Funding UTxOs: <count>
Stake Status: registered | unregistered
Delegated Pool: pool1... | none
Last Tx: <txHash> | none
```

## Send ADA (MeshTxBuilder)

```typescript
import { KoiosProvider, MeshTxBuilder } from "@meshsdk/core";

const provider = new KoiosProvider("api", "<KOIOS_API_KEY>");
const txBuilder = new MeshTxBuilder({ fetcher: provider });

const utxos = await wallet.getUtxos();
const changeAddress = await wallet.getChangeAddress();

const unsignedTx = await txBuilder
  .txOut("addr1...", [{ unit: "lovelace", quantity: "1000000" }])
  .changeAddress(changeAddress)
  .selectUtxosFrom(utxos)
  .complete();

const signedTx = await wallet.signTx(unsignedTx);
const txHash = await wallet.submitTx(signedTx);
console.log(txHash);
```

## Stake to a pool (register + delegate)

```typescript
import { KoiosProvider, MeshTxBuilder, deserializePoolId } from "@meshsdk/core";

const provider = new KoiosProvider("api", "<KOIOS_API_KEY>");
const txBuilder = new MeshTxBuilder({ fetcher: provider, verbose: true });

const utxos = await wallet.getUtxos();
const changeAddress = await wallet.getChangeAddress();
const rewardAddresses = await wallet.getRewardAddresses();
const rewardAddress = rewardAddresses[0]!;
const poolIdHash = deserializePoolId("pool1...");

const unsignedTx = await txBuilder
  .registerStakeCertificate(rewardAddress)
  .delegateStakeCertificate(rewardAddress, poolIdHash)
  .selectUtxosFrom(utxos)
  .changeAddress(changeAddress)
  .complete();

const signedTx = await wallet.signTx(unsignedTx);
const txHash = await wallet.submitTx(signedTx);
console.log(txHash);
```

## Agent workflow: generate → fund → register + stake

Use this sequence when the user wants a new wallet, then to register its stake address and delegate to a pool. All steps use key-based setup (no mnemonic in agent runtime). **Yes: the agent can register, then stake — both happen in one transaction** (Step 3).

### Step 1: Generate wallet (agent runs the script)

- Run `scripts/generate-key-based-wallet.js` from the skill directory. Uses **MeshJS + Koios only** (no cardano-cli, no mnemonic).
- Env (optional): `NETWORK=mainnet` (default) or `preprod` / `preview`; `KOIOS_API_KEY` for Koios; `WALLET_DIR=./wallet` to write `addresses.json`, `payment.skey`, `stake.skey`, and (if `@noble/ed25519` is installed) `payment.vkey`, `stake.vkey`. Keys are also printed to stdout.
- Output: base address, stake address, and export lines for `PAYMENT_SKEY_CBOR_HEX` / `STAKE_SKEY_CBOR_HEX`. For `.vkey` files, install `@noble/ed25519` alongside `@meshsdk/core`.
- Requires `@meshsdk/core` and network access (Koios) for address derivation.

```bash
cd skills/koios-agent-wallet
NETWORK=mainnet node scripts/generate-key-based-wallet.js
# Optional: WALLET_DIR=./wallet to persist keys to disk
```

- From the script output, capture the **base address** (user funds this), and the two **CBOR hex** values for Step 3.

### Step 2: Fund the wallet

- User must send ADA to the **base address** (payment address) printed in the dossier.
- For first-time staking: wallet needs enough for **~2 ADA stake deposit plus fees** (e.g. 3+ ADA total). Check with `provider.fetchAddressUTxOs(baseAddress)` before Step 3.

### Step 3: Register stake address and delegate (one transaction)

- **Register and stake in a single tx:** run `scripts/agent-wallet.js` with `MODE=stake`, `REGISTER_STAKE=1`, and `POOL_ID=pool1...`. This registers the stake address and delegates to the pool; no separate "register only" step is needed.
- Env: `PAYMENT_SKEY_CBOR_HEX`, `STAKE_SKEY_CBOR_HEX` (from Step 1), `KOIOS_NETWORK=api` (mainnet) or `preprod` / `preview`, `POOL_ID`, `REGISTER_STAKE=1`.

```bash
KOIOS_NETWORK=api MODE=stake REGISTER_STAKE=1 POOL_ID=pool1... \
  PAYMENT_SKEY_CBOR_HEX=<from_step_1> STAKE_SKEY_CBOR_HEX=<from_step_1> \
  node scripts/agent-wallet.js
```

- Optional: `CONFIRM=1` to poll for tx confirmation.

### Staking gotchas (agent must respect)

- **Stake address not registered**: Always use `REGISTER_STAKE=1` for the first delegation (or the stake cert will fail). Omit or set to 0 when changing delegation only.
- **Insufficient funds for deposit**: Stake registration locks ~2 ADA. Ensure wallet has 2 ADA + fees before running Step 3.
- **Staking requires stake key**: Wallet must be loaded with `STAKE_SKEY_CBOR_HEX` (or root key); payment-only cannot sign stake certs.
- **Stake cert signing**: `MeshWallet.signTx()` only adds the payment key witness; stake registration/delegation certs require the **stake key witness** too. If you see `MissingVKeyWitnessesUTXOW` or `KeyHash {...}`, the missing witness is usually the stake key. The skill’s `agent-wallet.js` uses CSL to hash the tx body, create `make_vkey_witness` for both payment and stake keys, and rebuild `Transaction.new(body, witnessSet, auxiliaryData)` so auxiliary data is preserved (avoids `MissingTxMetadata`). For staking with CLI keys, install: `@meshsdk/core`, `@emurgo/cardano-serialization-lib-nodejs`, and (if using hex pool ID) `bech32`.
- **Pool ID format**: `deserializePoolId()` expects bech32 (`pool1...`). Many APIs return hex (56 hex chars). The script accepts both: pass `POOL_ID` as bech32 or hex; hex is auto-converted using the `bech32` package.
- MeshJS staking reference: <https://meshjs.dev/apis/txbuilder/staking#stake-address-not-registered-error>

### Summary

| Step | Action                        | Script / API                                            |
| ---- | ----------------------------- | ------------------------------------------------------- |
| 1    | Generate wallet (no mnemonic) | `generate-key-based-wallet.js`                          |
| 2    | Fund base address             | User sends ADA; verify with `fetchAddressUTxOs`         |
| 3    | Register + delegate           | `agent-wallet.js` MODE=stake, REGISTER_STAKE=1, POOL_ID |

## Response checklist (agent wallet setup)

- Network and Koios base URL
- Wallet address used for funding
- Koios query used (endpoint + payload)
- Transaction intent (send or stake), tx hash, and confirmation method

## Notes

- Koios provides OpenAPI docs at each network base URL; use them to confirm endpoints and payloads.
- KoiosProvider expects a `network` string and optional `apiKey`; it can submit transactions.
- MeshTxBuilder staking flows are documented in MeshJS staking transactions.

## Scripts

- `scripts/agent-wallet.js` — end-to-end template (wallet init, send ADA, stake, confirm). **Staking with CLI keys:** uses CSL to hash tx body, create vkey witnesses for both payment and stake keys, and rebuild the transaction with auxiliary data preserved (MeshWallet.signTx only signs with payment key; stake certs need both). **Pool ID:** accepts bech32 (`pool1...`) or hex (56 chars); hex is converted to bech32 via `bech32`. Deps: `@meshsdk/core`, `@emurgo/cardano-serialization-lib-nodejs`; for hex `POOL_ID`, also `bech32`.
- `scripts/generate-key-based-wallet.js` — generate new key-based wallet (no mnemonic, no cardano-cli); uses MeshJS + Koios only; creates payment + stake keys and outputs CBOR hex for use with agent-wallet (staking-ready).

### Generate new wallet (key-based, stakable)

```bash
# Optional: NETWORK=mainnet (default) | preprod | preview; KOIOS_API_KEY=...; WALLET_DIR=./my-wallet (writes addresses.json only)
node scripts/generate-key-based-wallet.js
```

Outputs: base + stake addresses and `PAYMENT_SKEY_CBOR_HEX` / `STAKE_SKEY_CBOR_HEX` export lines. If `WALLET_DIR` is set, writes `addresses.json`, `payment.skey`, `stake.skey`, and (if `@noble/ed25519` is installed) `payment.vkey`, `stake.vkey`. No cardano-cli required. Requires `@meshsdk/core` and Koios (network). For staking with `agent-wallet.js` (CLI keys), also install `@emurgo/cardano-serialization-lib-nodejs`; if you pass a hex `POOL_ID`, install `bech32`.

### Script usage examples

```bash
# Status (read-only)
KOIOS_NETWORK=api MODE=status ADDRESS_ONLY=addr1... \\
  node scripts/agent-wallet.js

# Send ADA (CLI keys)
KOIOS_NETWORK=api MODE=send PAYMENT_SKEY_CBOR_HEX=<...> \\
  RECIPIENT_ADDR=addr1... SEND_LOVELACE=1000000 \\
  node scripts/agent-wallet.js

# Register + delegate (POOL_ID can be pool1... or 56-char hex)
KOIOS_NETWORK=api MODE=stake PAYMENT_SKEY_CBOR_HEX=<...> \\
  STAKE_SKEY_CBOR_HEX=<...> POOL_ID=pool1... REGISTER_STAKE=1 \\
  node scripts/agent-wallet.js
```

## References

- `shared/PRINCIPLES.md`
- Koios API base: `https://api.koios.rest/`
- Koios API guide: `https://koios.rest/guide/`
- MeshJS Koios provider: `https://meshjs.dev/providers/koios`
- MeshJS MeshWallet: `https://meshjs.dev/apis/wallets/meshwallet`
- MeshJS MeshTxBuilder basics: `https://meshjs.dev/apis/txbuilder/basics`
- MeshJS staking transactions: `https://meshjs.dev/apis/txbuilder/staking`
