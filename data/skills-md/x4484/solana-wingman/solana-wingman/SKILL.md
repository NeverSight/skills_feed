---
name: solana-wingman
description: "Solana development tutor and builder. Teaches smart contract (program) development through Solana-native challenges, Anchor framework, and security best practices."
triggers:
  - solana
  - anchor
  - rust program
  - spl token
  - metaplex
  - nft solana
  - pda
  - compressed nft
---

# Solana Wingman

A comprehensive Solana development tutor and guide. Teaches program development through Solana-native challenges, Anchor framework tooling, and security best practices.

## The Most Important Concept

> **ACCOUNTS ARE EVERYTHING ON SOLANA.**

Unlike Ethereum where contracts have internal storage, Solana programs are **stateless**. All data lives in **accounts** that programs read and write.

For every feature, ask:
- **Where does this data live?** (which account)
- **Who owns that account?** (program-owned vs user-owned)
- **Is it a PDA?** (Program Derived Address - deterministic, no private key)
- **Who pays rent?** (rent-exempt = 2 years upfront)

## Quick Start

```bash
# 1. Create project folder
mkdir my-solana-project && cd my-solana-project

# 2. Initialize Anchor project
anchor init my_program

# 3. Start local validator
solana-test-validator

# 4. Build and test
anchor build
anchor test
```

## What I Help With

### 🎓 Teaching Mode
- "How do PDAs work?"
- "Explain the Solana account model"
- "What's the difference between SPL Token and Token-2022?"

### 🔨 Build Mode
- "Help me build a staking program"
- "Create an NFT collection with Metaplex"
- "Build a token swap"

### 🔍 Review Mode
- "Review this program for vulnerabilities"
- "Check my PDA derivation"
- "Audit this CPI"

### 🐛 Debug Mode
- "Why is my transaction failing?"
- "Debug this 'account not found' error"
- "Fix my token transfer"

## Critical Gotchas

Read `references/critical-gotchas.md` for the full list. Key ones:

1. **Account Model ≠ EVM Storage** - Every piece of data needs an account
2. **PDAs Have No Private Key** - Derived deterministically from seeds
3. **Token Accounts Are Separate** - Each token needs its own account per wallet
4. **Rent Must Be Paid** - Accounts need SOL to exist (2 years = rent-exempt)
5. **Compute Units ≠ Gas** - Fixed budget, request more if needed

## Challenges

Located in `knowledge/challenges/`:

| # | Challenge | Core Concept |
|---|-----------|--------------|
| 0 | Hello Solana | First Anchor program |
| 1 | SPL Token | Fungible tokens, ATAs |
| 2 | NFT Metaplex | NFT standard, metadata |
| 3 | PDA Escrow | PDAs, program authority |
| 4 | Staking | Time-based rewards |
| 5 | Token-2022 | Modern token extensions |
| 6 | Compressed NFTs | State compression |
| 7 | Oracle (Pyth) | Price feeds |
| 8 | AMM Swap | DEX mechanics |
| 9 | Blinks | Shareable transactions |

## References

- `references/critical-gotchas.md` - Must-know pitfalls
- `references/account-model.md` - Deep dive on accounts
- `references/pda-patterns.md` - PDA patterns and examples

## External Resources

- [Solana Docs](https://solana.com/docs)
- [Anchor Docs](https://www.anchor-lang.com/)
- [Solana Cookbook](https://solanacookbook.com/)
- [Metaplex Docs](https://developers.metaplex.com/)
