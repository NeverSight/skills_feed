---
name: viem-siwe
description: Comprehensive guide and reference implementation for Sign-In with Ethereum (SIWE) using the viem v2 library. Use this skill when implementing authentication flows, verifying Ethereum addresses on a backend, parsing EIP-4361 messages, or managing SIWE sessions. It includes nonce generation, message creation, signature verification, and best practices for replay protection and session management.
---

# Viem SIWE

This skill provides expertise in implementing Sign-In with Ethereum (SIWE) adhering to EIP-4361 using `viem`.

## Reference Implementation

For a complete, copy-pasteable implementation of a SIWE auth module, refer to [references/implementation.md](references/implementation.md).

This implementation includes:

- `siwe.ts`: Core logic for nonce generation, message creation, parsing, and verification.
- `index.ts`: Public API for the auth module.

## API Documentation

For detailed API documentation of `viem`'s SIWE utilities (`createSiweMessage`, `verifySiweMessage`, etc.), refer to [references/api-docs.md](references/api-docs.md).

## Critical Implementation Details

### Nonce Management

- **Always** generate a unique nonce for every login attempt.
- Store nonces with an expiration (TTL) on the backend.
- Verify and consume the nonce upon signature validation to prevent replay attacks.

### Message Verification

- **Verify Domain**: Ensure the `domain` in the message matches the host to prevent phishing.
- **Verify Chain ID**: Ensure the `chainId` matches the expected network.
- **Check Expiration**: Respect `expirationTime` and `notBefore` fields.

### Smart Contract Wallets (ERC-1271)

When verifying signatures from smart contract wallets:

- Use a `PublicClient` instance in `verifySiweMessage`.
- Do not rely solely on `verifyMessage` which only works for EOAs.
