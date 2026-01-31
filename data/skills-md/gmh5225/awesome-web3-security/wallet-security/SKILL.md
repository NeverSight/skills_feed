---
name: wallet-security
description: "Guide for wallet security topics: MPC/TSS, key management, wallet UX security, phishing, and how to categorize related resources in README.md."
---

# Wallet Security

## Scope

Use this skill when working on:

- Wallet threat models and architecture
- MPC/TSS/threshold signing resources
- Key management, backups, and secret sharing
- Wallet phishing and transaction safety

## Topics Checklist

### Key Management

- Secure key generation
- Backup and recovery
- Shamir secret sharing vs threshold signing
- Hardware security modules and secure enclaves

### MPC / TSS

- Threshold ECDSA/EdDSA protocols
- Signer orchestration, liveness, and rotation
- Attack surfaces: malicious participants, key extraction, nonce misuse

### User Safety

- Phishing detection
- Malicious approvals / Permit signatures
- Transaction simulation, warnings, and policy enforcement

## Where to Add Links in README

- Wallet source code: `Wallet → Source Code`
- MPC/TSS resources: `Wallet → MPC`
- Anti-phishing utilities: `Development → Tools` or `Security`

## Rules

- English descriptions
- No duplicate URLs

## Data Source

For detailed and up-to-date resources, fetch the full list from:
```
https://raw.githubusercontent.com/gmh5225/awesome-web3-security/refs/heads/main/README.md
```

