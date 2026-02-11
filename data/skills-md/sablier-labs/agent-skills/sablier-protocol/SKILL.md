---
name: sablier-protocol
description: This skill should be used when the user asks "what is Sablier", "explain Sablier protocol", "how does Sablier work", "Sablier vesting", "Sablier airdrops", "Sablier payroll", mentions Sablier company/product/protocol, or needs context about the Sablier ecosystem.
---

# Sablier

Sablier is an onchain token distribution protocol. It powers token vesting, airdrop distributions, and onchain payroll
across 27+ EVM chains and Solana.

Organizations use Sablier to distribute tokens at scale—whether compensating contributors, vesting team allocations, or
airdropping to thousands of recipients. The protocol handles the complexity of time-based token releases, letting teams
focus on what they're building rather than manual distribution logistics.

## Core Use Cases

### Token Vesting

Lock tokens with customizable unlock schedules. Vesting configurations include:

- **Linear unlocks** — Constant rate from start to end
- **Cliff periods** — Initial waiting period before any tokens unlock
- **Tranched releases** — Discrete unlocks at specific intervals (monthly, quarterly, yearly)
- **Custom curves** — Exponential, logarithmic, or step-based unlock patterns

All vesting positions are represented as NFTs, enabling recipients to transfer or trade their allocations.

### Airdrop Distributions

Distribute tokens to thousands of recipients efficiently using Merkle trees:

- Gas-optimized claiming—recipients pay only their own claim gas
- Built-in vesting—tokens can stream after claim rather than unlocking immediately
- Clawback support—reclaim unclaimed allocations after expiration
- Flexible eligibility—custom claim conditions and allowlists

### Onchain Payroll

Compensate contributors with tokens that accrue continuously:

- Real-time access to earned compensation
- No waiting for pay dates—withdraw anytime
- Adjustable payment rates for changing arrangements
- Clean separation between sender funding and recipient access

## How It Works

Sablier uses **streaming** as the underlying mechanism for token distribution. Rather than transferring tokens in lump
sums, the protocol releases them continuously over time—by the second.

Recipients withdraw their tokens whenever convenient. No sender approval required, no claim windows to miss. The
protocol tracks exactly how much has vested at any moment, and recipients access their portion on demand.

Every distribution position mints an NFT to the recipient. This representation enables:

- Transferring ownership to another address
- Trading positions on NFT marketplaces
- Using vesting positions as collateral in DeFi

## Protocol Modules

Sablier comprises three modules, each optimized for different distribution patterns:

### Lockup

The core vesting module. Creators deposit tokens upfront and define an unlock schedule. Supports three stream shapes:

- **Linear** — Constant unlock rate, optional cliff
- **Dynamic** — Custom curves using configurable segments
- **Tranched** — Step-wise unlocks at defined timestamps

### Flow

A pay-as-you-go module for ongoing distributions. No upfront deposit required—senders top up as needed while recipients
withdraw accrued amounts. Ideal for:

- Salaries and recurring payments
- Open-ended contributor arrangements
- Situations where total distribution isn't known upfront

### Airdrops

Merkle-tree based distribution for large recipient sets. Create a single contract that serves claims for thousands of
addresses. Combines gas efficiency with optional vesting—recipients can receive streaming positions rather than
immediate lump sums.

## Key Features

### Stream Shapes

Configure unlock curves to match any distribution requirement:

| Shape    | Pattern         | Use Case                              |
| -------- | --------------- | ------------------------------------- |
| Linear   | Constant rate   | Standard vesting, salaries            |
| Dynamic  | Custom segments | Backloaded vesting, milestones        |
| Tranched | Discrete steps  | Quarterly unlocks, scheduled releases |

### NFT Representation

All Lockup positions mint ERC-721 tokens. Recipients hold NFTs representing their vesting allocations, enabling
secondary market liquidity and DeFi composability.

### Hooks System

Execute custom logic in response to stream events. Hooks enable:

- Automatic reinvestment of received tokens
- Notifications to external systems
- Custom access controls or conditions

### Batch Operations

Create hundreds of distributions in a single transaction. Essential for:

- Company-wide vesting setup
- Large contributor grants
- Airdrop campaigns

### Permissionless Infrastructure

Pure DeFi infrastructure with no gatekeepers. Anyone can create distributions, build on the protocol, or integrate it
into existing products.

## Platform Availability

Sablier smart contracts are deployed across **27+ EVM chains** including Ethereum, Arbitrum, Optimism, Base, Polygon,
Avalanche, and BSC.

Sablier programs are also deployed on **Solana**.

### User Interfaces

| Network    | Interface                                        |
| ---------- | ------------------------------------------------ |
| EVM chains | [app.sablier.com](https://app.sablier.com)       |
| Solana     | [solana.sablier.com](https://solana.sablier.com) |

Both interfaces provide full access to create, manage, and withdraw from distributions without writing code.

## Developer Integration

Integrate Sablier into applications using:

- **Smart contract calls** — Direct interaction with Lockup, Flow, or Airdrops contracts
- **Subgraph APIs** — Query distribution data via The Graph
- **SDK libraries** — TypeScript utilities for common operations
- **CSV imports** — Bulk distribution creation via the UI

Common integration patterns include token vesting platforms, payroll systems, DAO contributor management, and DeFi
reward distribution.

## Resources

### Documentation

- [Sablier Docs](https://docs.sablier.com) — Protocol documentation and guides

### Smart Contracts (Solidity)

| Module   | Repository                                                        | UI Product |
| -------- | ----------------------------------------------------------------- | ---------- |
| Lockup   | [sablier-labs/lockup](https://github.com/sablier-labs/lockup)     | Vesting    |
| Flow     | [sablier-labs/flow](https://github.com/sablier-labs/flow)         | Payments   |
| Airdrops | [sablier-labs/airdrops](https://github.com/sablier-labs/airdrops) | Airdrops   |

### Solana (Rust)

- [sablier-labs/solsab](https://github.com/sablier-labs/solsab) — Sablier programs for Solana

### Indexers

- [sablier-labs/indexers](https://github.com/sablier-labs/indexers) — Subgraph deployments for querying onchain data

### Examples & Sandboxes

- [sablier-labs/evm-examples](https://github.com/sablier-labs/evm-examples) — Solidity integration examples
- [sablier-labs/sandbox](https://github.com/sablier-labs/sandbox) — Generic frontend sandbox
- [sablier-labs/airdrop-sandbox](https://github.com/sablier-labs/airdrop-sandbox) — Custom airdrop development sandbox

### Branding

- [sablier-labs/branding](https://github.com/sablier-labs/branding) — Logos, colors, and brand assets
