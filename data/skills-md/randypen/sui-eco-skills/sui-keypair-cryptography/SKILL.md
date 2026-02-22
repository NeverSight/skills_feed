---
name: sui-keypair-cryptography
description: "Helps Claude Code understand Sui blockchain keypair and cryptography operations, providing guidelines and examples for key generation, signing, verification, address derivation, and multi-signature scheme support. Use when working with cryptography in Sui development or when the user mentions keypairs, cryptography, signing, or verification."
---

# Keypair and Cryptography Skill

## Overview

The keypair and cryptography module provides secure cryptographic operations for the Sui blockchain ecosystem, including key generation, signing, verification, and address derivation. It supports multiple signature schemes and provides a unified interface for cryptographic operations.

## Quick Start

### Installation and Import

```typescript
// Import Ed25519 keypair
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';

// Import other signature schemes
import { Secp256k1Keypair } from '@mysten/sui/keypairs/secp256k1';
import { Secp256r1Keypair } from '@mysten/sui/keypairs/secp256r1';

// Import common utilities
import { mnemonicToSeed } from '@mysten/sui/cryptography';
// Note: generateMnemonic needs to be imported from @scure/bip39: import { generateMnemonic } from '@scure/bip39';
```

### Basic Examples

```typescript
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { Transaction } from '@mysten/sui/transactions';

// Generate new keypair
const keypair = new Ed25519Keypair();

// Get address
const address = keypair.toSuiAddress();
console.log('Address:', address);

// Sign transaction
const tx = new Transaction();
// ... build transaction
const bytes = await tx.build({ client });
const { signature } = await keypair.signTransaction(bytes);

// Verify signature
const isValid = await keypair.getPublicKey().verifyTransaction(bytes, signature);
console.log('Signature valid:', isValid);
```

## Core Components

### Signer Abstract Class

**Location**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/cryptography/keypair.ts`

`Signer` is the abstract base class for all signing operations, providing:
- Message signing with intent scope
- Transaction signing and execution
- Personal message signing
- Address derivation from public key

### Keypair Abstract Class

**Location**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/cryptography/keypair.ts`

`Keypair` extends `Signer`, adding secret key management:
- Secret key serialization/deserialization
- Bech32 encoding for private keys
- Multiple signature scheme support

### PublicKey Abstract Class

**Location**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/cryptography/publickey.ts`

`PublicKey` is the base class for public key operations, providing:
- Address derivation and verification
- Signature verification
- Multiple encoding formats
- Intent-based verification

## Supported Signature Schemes

For detailed information about supported signature schemes including Ed25519, Secp256k1, Secp256r1, and Passkey, see [Signature Schemes](reference/signature-schemes.md).

## Key Features

For detailed information about key features including intent-based signing, address derivation, and private key management, see [Key Features](reference/key-features.md).

## Usage Patterns

For detailed information about usage patterns including key generation, signing, verification, and serialization, see [Usage Patterns](reference/usage-patterns.md).

## Architecture Notes

For detailed information about architecture notes including security design, intent system, and address generation, see [Architecture Notes](reference/architecture-notes.md).

## Integration Points

For detailed information about integration points including transaction integration, wallet integration, and blockchain operations, see [Integration Points](reference/integration-points.md).

## Advanced Features

For detailed information about advanced features including multi-signature support, hardware security, and key rotation, see [Advanced Features](reference/advanced-features.md).

## Security Considerations

For detailed information about security considerations including key protection, signature security, and best practices, see [Security Considerations](reference/security-considerations.md).

## Workflows

For detailed information about workflows including secure key generation, transaction signing, and key recovery, see [Workflows](reference/workflows.md).

## Best Practices

For detailed information about best practices including key management, signing practices, and address handling, see [Best Practices](reference/best-practices.md).

## Related Skills

- [sui-transaction-building](./../sui-transaction-building/SKILL.md): Understand the application of keypairs in transaction signing
- [sui-bcs](./../sui-bcs/SKILL.md): Understand BCS serialization of public keys and signatures
- [sui-client](./../sui-client/SKILL.md): Understand integration with SuiClient

## References

- **Source Code**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/cryptography/` and `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/keypairs/`
- **Test Cases**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/cryptography/__tests__/`
- **TypeScript Type Definitions**: `https://github.com/MystenLabs/ts-sdks/tree/main/packages/typescript/src/cryptography/types.ts`
- **Security Guidelines**: Sui official security best practices documentation

---

*This skill helps Claude Code understand Sui keypair and cryptography operations, providing practical code examples and usage guidelines. When users need to handle key management, signing, and verification for the Sui blockchain, referring to this skill can provide accurate TypeScript code and best practices.*