---
name: multiversx-crypto-verification
description: Cryptographic operations in MultiversX smart contracts. Use when hashing data (SHA256, Keccak256, RIPEMD160), verifying signatures (Ed25519, secp256k1, secp256r1, BLS), or encoding signatures in on-chain logic.
---

# MultiversX Crypto Verification — `self.crypto()` API Reference

Complete reference for hashing and signature verification in MultiversX smart contracts (SDK v0.64+).

## Hashing Functions

All hashing functions take `&ManagedBuffer` (or anything that borrows as `ManagedBuffer`) and return a fixed-size `ManagedByteArray`.

| Method | Return Type | Output Size | Use Case |
|--------|------------|-------------|----------|
| `.sha256(data)` | `ManagedByteArray<A, 32>` | 32 bytes | General purpose hashing, Merkle trees |
| `.keccak256(data)` | `ManagedByteArray<A, 32>` | 32 bytes | Ethereum compatibility, EIP-712 |
| `.ripemd160(data)` | `ManagedByteArray<A, 20>` | 20 bytes | Bitcoin address derivation (rare) |

```rust
// Hash a message
let message = ManagedBuffer::from("data to hash");
let hash: ManagedByteArray<Self::Api, 32> = self.crypto().sha256(&message);

// Hash for Ethereum compatibility
let eth_hash = self.crypto().keccak256(&abi_encoded_data);
```

## Signature Verification

### Critical Distinction: Panic vs Bool

**Panic-based** — Transaction fails immediately on invalid signature. No error handling possible. Use when invalid signature = unauthorized action.

**Bool-based** — Returns `true`/`false`. Contract continues execution. Use when you need graceful error handling or multiple verification attempts.

| Method | Returns | On Invalid Signature |
|--------|---------|---------------------|
| `verify_ed25519(key, message, signature)` | `()` | **Panics** — tx fails with "invalid signature" |
| `verify_bls(key, message, signature)` | `()` | **Panics** |
| `verify_secp256r1(key, message, signature)` | `()` | **Panics** |
| `verify_bls_signature_share(key, message, signature)` | `()` | **Panics** |
| `verify_bls_aggregated_signature(keys, message, signature)` | `()` | **Panics** |
| `verify_secp256k1(key, message, signature)` | `bool` | **Returns false** |
| `verify_custom_secp256k1(key, message, signature, hash_type)` | `bool` | **Returns false** |

### Method Signatures

```rust
// Panic-based (no return value)
fn verify_ed25519(
    &self,
    key: &ManagedBuffer<A>,       // 32-byte public key
    message: &ManagedBuffer<A>,   // arbitrary message
    signature: &ManagedBuffer<A>, // 64-byte signature
)

fn verify_bls(
    &self,
    key: &ManagedBuffer<A>,       // 96-byte BLS public key
    message: &ManagedBuffer<A>,
    signature: &ManagedBuffer<A>, // 48-byte BLS signature
)

fn verify_secp256r1(
    &self,
    key: &ManagedBuffer<A>,       // 33 or 65-byte public key
    message: &ManagedBuffer<A>,
    signature: &ManagedBuffer<A>,
)

fn verify_bls_signature_share(
    &self,
    key: &ManagedBuffer<A>,
    message: &ManagedBuffer<A>,
    signature: &ManagedBuffer<A>,
)

fn verify_bls_aggregated_signature(
    &self,
    keys: &ManagedVec<A, ManagedBuffer<A>>,  // list of BLS public keys
    message: &ManagedBuffer<A>,
    signature: &ManagedBuffer<A>,             // aggregated signature
)

// Bool-based
fn verify_secp256k1(
    &self,
    key: &ManagedBuffer<A>,
    message: &ManagedBuffer<A>,
    signature: &ManagedBuffer<A>,  // DER-encoded or raw (min 2 bytes)
) -> bool

fn verify_custom_secp256k1(
    &self,
    key: &ManagedBuffer<A>,
    message: &ManagedBuffer<A>,
    signature: &ManagedBuffer<A>,
    hash_type: MessageHashType,    // how the message was hashed
) -> bool
```

### MessageHashType Enum

Used with `verify_custom_secp256k1` to specify how the message was pre-hashed:

```rust
pub enum MessageHashType {
    ECDSAPlainMsg,      // Message is not hashed (raw)
    ECDSASha256,        // Message was SHA-256 hashed
    ECDSADoubleSha256,  // Message was double SHA-256 hashed (Bitcoin)
    ECDSAKeccak256,     // Message was Keccak-256 hashed (Ethereum)
    ECDSARipemd160,     // Message was RIPEMD-160 hashed
    ECDSABlake2b,       // Message was Blake2b hashed
}
```

### DER Signature Encoding

Convert raw (r, s) components to DER format for secp256k1:

```rust
fn encode_secp256k1_der_signature(
    &self,
    r: &ManagedBuffer<A>,  // 32-byte r component
    s: &ManagedBuffer<A>,  // 32-byte s component
) -> ManagedBuffer<A>      // DER-encoded signature
```

## Algorithm Selection Guide

| Algorithm | When to Use |
|-----------|-------------|
| **Ed25519** | MultiversX native signatures. Verify user/SC signatures from the chain. Default choice. |
| **secp256k1** | Ethereum/Bitcoin compatibility. Bridge contracts, cross-chain verification. |
| **secp256r1** | NIST P-256 / WebAuthn / Apple Secure Enclave. Passkey-based auth. |
| **BLS** | Validator signatures, multi-sig aggregation, threshold schemes. |
| **BLS aggregated** | Verify a single aggregated signature from multiple validators. |

## Common Patterns

### Ed25519 Signature Gate (MultiversX Native)
```rust
#[endpoint(executeWithSignature)]
fn execute_with_signature(
    &self,
    data: ManagedBuffer,
    signature: ManagedBuffer,
) {
    let signer = self.trusted_signer().get();
    // Panics if invalid — tx reverts automatically
    self.crypto().verify_ed25519(
        &signer,
        &data,
        &signature,
    );
    // Only reached if signature is valid
    self.process_data(&data);
}
```

### Ethereum Signature Verification (Graceful)
```rust
#[endpoint(verifyEthSignature)]
fn verify_eth_signature(
    &self,
    key: ManagedBuffer,
    message: ManagedBuffer,
    signature: ManagedBuffer,
) -> bool {
    // Returns bool — handle failure gracefully
    let valid = self.crypto().verify_custom_secp256k1(
        &key,
        &message,
        &signature,
        MessageHashType::ECDSAKeccak256,
    );
    require!(valid, "Invalid Ethereum signature");
    valid
}
```

### Multi-Validator BLS Aggregated Check
```rust
#[endpoint(verifyValidators)]
fn verify_validators(
    &self,
    validator_keys: ManagedVec<ManagedBuffer>,
    message: ManagedBuffer,
    aggregated_sig: ManagedBuffer,
) {
    // Panics if aggregated signature is invalid
    self.crypto().verify_bls_aggregated_signature(
        &validator_keys,
        &message,
        &aggregated_sig,
    );
}
```

### Hash-Based Commit-Reveal
```rust
#[endpoint(commit)]
fn commit(&self, hash: ManagedByteArray<Self::Api, 32>) {
    let caller = self.blockchain().get_caller();
    self.commitments(&caller).set(hash);
}

#[endpoint(reveal)]
fn reveal(&self, value: ManagedBuffer) {
    let caller = self.blockchain().get_caller();
    let stored_hash = self.commitments(&caller).get();
    let computed_hash = self.crypto().sha256(&value);
    require!(stored_hash == computed_hash, "Hash mismatch");
    self.commitments(&caller).clear();
    self.process_reveal(&caller, &value);
}
```

### DER Encoding for secp256k1
```rust
// When you have raw r,s components (e.g., from an oracle)
let r = ManagedBuffer::from(&r_bytes[..]);
let s = ManagedBuffer::from(&s_bytes[..]);
let der_sig = self.crypto().encode_secp256k1_der_signature(&r, &s);

let valid = self.crypto().verify_secp256k1(&pubkey, &message, &der_sig);
```

## Anti-Patterns

```rust
// BAD: Trying to catch Ed25519 failure — it panics, there's nothing to catch
let result = self.crypto().verify_ed25519(&key, &msg, &sig);
// ← verify_ed25519 returns (), not Result. If invalid, tx is already dead.

// GOOD: Use Ed25519 as a gate (panic is the intended behavior)
self.crypto().verify_ed25519(&key, &msg, &sig);
// Execution continues only if valid

// BAD: Using verify_secp256k1 without checking the bool
self.crypto().verify_secp256k1(&key, &msg, &sig);
// ← Compiles fine but ignores the result! Signature not actually checked.

// GOOD: Always check the bool return
let valid = self.crypto().verify_secp256k1(&key, &msg, &sig);
require!(valid, "Invalid signature");

// BAD: Using wrong hash type for Ethereum signatures
self.crypto().verify_custom_secp256k1(&key, &msg, &sig, MessageHashType::ECDSASha256);
// ← Ethereum uses Keccak256, not SHA256

// GOOD: Match the hash type to the chain
self.crypto().verify_custom_secp256k1(&key, &msg, &sig, MessageHashType::ECDSAKeccak256);
```
