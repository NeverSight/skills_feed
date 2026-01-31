---
name: solana-security
description: Guide for Solana/Sealevel security research and where to organize Solana-specific resources in README.md.
---

# Solana Security (Sealevel)

## Scope

Use this skill for:

- Solana program auditing (Anchor/native)
- Solana account model pitfalls
- Solana-focused fuzzing / tooling / security references

## Key Concepts

- Account model (mutable accounts, ownership, rent/exempt)
- Program Derived Addresses (PDA) and seeds
- Cross-Program Invocation (CPI) security
- Signer vs authority checks
- Serialization, discriminators, and account layout assumptions

## Common Bug Classes

- Missing signer/authority validation
- Incorrect PDA derivation or seed collisions
- CPI to untrusted programs
- Account confusion (wrong account passed, mismatched owner)
- Arithmetic / precision issues in token math

## Tooling

- Anchor framework and security patterns
- Fuzzers / harnesses (e.g., Trident)
- Program analyzers and disassemblers

## Where to Add Links in README

- Solana SDKs/tools: `Development → SDK` / `Development → Tools`
- Solana audit checklists: `Security`
- Solana learning guides: `Blockchain Guide`

## Rules

- Use English descriptions
- Avoid duplicates across categories

## Data Source

For detailed and up-to-date resources, fetch the full list from:
```
https://raw.githubusercontent.com/gmh5225/awesome-web3-security/refs/heads/main/README.md
```

