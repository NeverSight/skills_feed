---
name: solidity-coding
description: "[AUTO-INVOKE] MUST be invoked BEFORE writing or modifying any Solidity contract (.sol files). Covers pragma version, naming conventions, project layout, OpenZeppelin library selection standards, Chainlink integration, and anti-patterns. Trigger: any task involving creating, editing, or reviewing .sol source files."
---

# Solidity Coding Standards

## Language Rule

- **Always respond in the same language the user is using.** If the user asks in Chinese, respond in Chinese. If in English, respond in English.

## Coding Principles

- **Pragma**: Use `pragma solidity ^0.8.20;` — keep consistent across all files in the project
- **Dependencies**: OpenZeppelin Contracts 4.9.x, manage imports via `remappings.txt`
- **Error Handling**: Prefer custom errors over `require` strings — saves gas and is more expressive
  - Define: `error InsufficientBalance(uint256 available, uint256 required);`
  - Use: `if (balance < amount) revert InsufficientBalance(balance, amount);`
- **Documentation**: All `public` / `external` functions must have NatSpec (`@notice`, `@param`, `@return`)
- **Event Indexing**: Only add `indexed` to `address` type parameters — add comment if indexing other types
- **Special Keywords**: `immutable` / `constant` / `unchecked` / `assembly` must have inline comment explaining why

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Contract / Library | PascalCase | `MyToken`, `StakingPool` |
| Interface | `I` + PascalCase | `IMyToken`, `IStakingPool` |
| State variable / Function | lowerCamelCase | `totalSupply`, `claimDividend` |
| Constant / Immutable | UPPER_SNAKE_CASE | `MAX_SUPPLY`, `ROUTER_ADDRESS` |
| Event | PascalCase (past tense) | `TokenTransferred`, `PoolCreated` |
| Custom Error | PascalCase | `InsufficientBalance`, `Unauthorized` |
| Function parameter | prefix `_` for setter | `function setFee(uint256 _fee)` |

- **Forbidden**: Pinyin names, single-letter variables (except `i/j/k` in loops), excessive abbreviations

## Code Organization Rules

| Situation | Rule |
|-----------|------|
| Cross-contract constants | Place in `src/common/Const.sol` |
| Interface definitions | Place in `src/interfaces/I<Name>.sol`, separate from implementation |
| Simple on-chain queries | Use `cast call` or `cast send` |
| Complex multi-step operations | Use `forge script` |
| Import style | Use named imports: `import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";` |

## Project Directory Structure

```
src/              — Contract source code
  interfaces/     — Interface definitions (I*.sol)
  common/         — Shared constants, types, errors (Const.sol, Types.sol)
test/             — Test files (*.t.sol)
script/           — Deployment & interaction scripts (*.s.sol)
config/           — Network config, parameters (*.json)
deployments/      — Deployment records (latest.env)
docs/             — Documentation, changelogs
lib/              — Dependencies (managed by forge install)
```

## Configuration Management

- `config/*.json` — network RPC URLs, contract addresses, business parameters
- `deployments/latest.env` — latest deployed contract addresses, must update after each deployment
- `foundry.toml` — compiler version, optimizer settings, remappings
- Important config changes must be documented in the PR description

## OpenZeppelin Library Selection Standards

When writing Solidity contracts, prioritize using battle-tested OpenZeppelin libraries over custom implementations. Select the appropriate library based on the scenario:

### Access Control

| Scenario | Library | Import Path |
|----------|---------|-------------|
| Single owner management | `Ownable` | `@openzeppelin/contracts/access/Ownable.sol` |
| Owner transfer needs safety | `Ownable2Step` | `@openzeppelin/contracts/access/Ownable2Step.sol` |
| Multi-role permission (admin/operator/minter) | `AccessControl` | `@openzeppelin/contracts/access/AccessControl.sol` |
| Need to enumerate role members | `AccessControlEnumerable` | `@openzeppelin/contracts/access/AccessControlEnumerable.sol` |
| Governance with timelock delay | `TimelockController` | `@openzeppelin/contracts/governance/TimelockController.sol` |

**Rule**: Single owner → `Ownable2Step`; 2+ roles → `AccessControl`; governance/DAO → `TimelockController`

### Security Protection

| Scenario | Library | Usage |
|----------|---------|-------|
| External call / token transfer | `ReentrancyGuard` | Add `nonReentrant` modifier |
| Emergency pause needed | `Pausable` | Add `whenNotPaused` to user-facing functions; keep admin functions unpaused |
| ERC20 token interaction | `SafeERC20` | Use `safeTransfer` / `safeTransferFrom` / `safeApprove` instead of raw calls |

**Rule**: Any contract that transfers tokens or ETH MUST use `ReentrancyGuard` + `SafeERC20`

### Token Standards

| Scenario | Library | Notes |
|----------|---------|-------|
| Fungible token | `ERC20` | Base standard |
| Token with burn mechanism | `ERC20Burnable` | Adds `burn()` and `burnFrom()` |
| Token with max supply cap | `ERC20Capped` | Enforces `totalSupply <= cap` |
| Gasless approval (EIP-2612) | `ERC20Permit` | Saves users approve tx gas |
| Governance voting token | `ERC20Votes` | Snapshot-based voting power |
| NFT | `ERC721` | Base NFT standard |
| NFT with enumeration | `ERC721Enumerable` | Supports `tokenOfOwnerByIndex` queries |
| Multi-token (FT + NFT mixed) | `ERC1155` | Game items, batch operations |

### Utility Libraries

| Scenario | Library | Usage |
|----------|---------|-------|
| Whitelist / airdrop verification | `MerkleProof` | Gas-efficient Merkle tree verification |
| Signature verification | `ECDSA` + `EIP712` | Off-chain sign + on-chain verify |
| Auto-increment IDs | `Counters` | Token ID, order ID generation |
| Batch function calls | `Multicall` | Multiple operations in one tx |
| Address set / uint set | `EnumerableSet` | Iterable sets with O(1) add/remove/contains |
| Revenue sharing | `PaymentSplitter` | Split ETH/token payments by shares |
| Standardized yield vault | `ERC4626` | DeFi vault standard |

### Contract Upgrade

| Scenario | Library | Notes |
|----------|---------|-------|
| Upgradeable contract (gas efficient) | `UUPSUpgradeable` | Upgrade logic in implementation contract |
| Upgradeable contract (admin separated) | `TransparentUpgradeableProxy` | Upgrade logic in proxy, higher gas |
| Initializer (replace constructor) | `Initializable` | Use `initializer` modifier instead of constructor |

**Rule**: New projects prefer `UUPSUpgradeable`; always use `Initializable` for upgradeable contracts

### Chainlink Integration

| Scenario | Library | Notes |
|----------|---------|-------|
| Token price data | `AggregatorV3Interface` | Only for tokens with Chainlink feed; check [data.chain.link](https://data.chain.link) |
| Verifiable randomness (lottery/NFT) | `VRFConsumerBaseV2` | On-chain provably fair random numbers |
| Automated execution (cron jobs) | `AutomationCompatible` | Replace centralized keepers |
| Cross-chain messaging | `CCIP` | Cross-chain token/message transfer |

### Library Selection Decision Flow

```
Does contract handle user funds/tokens?
├── YES → Add ReentrancyGuard + SafeERC20
│         Does it need emergency stop?
│         ├── YES → Add Pausable
│         └── NO  → Skip
└── NO  → Skip

How many admin roles needed?
├── 1 role  → Ownable2Step
├── 2+ roles → AccessControl
└── DAO/governance → TimelockController

Does contract need price data?
├── Token has Chainlink feed → AggregatorV3Interface
├── No Chainlink feed → Custom TWAP with min-liquidity check
└── No price needed → Skip

Will contract need upgrades?
├── YES → UUPSUpgradeable + Initializable
└── NO  → Standard deployment (immutable)
```

### Anti-Patterns (Do NOT)

- **Do NOT** write custom `transfer` wrappers — use `SafeERC20`
- **Do NOT** write custom access control modifiers — use `Ownable` / `AccessControl`
- **Do NOT** write custom pause logic — use `Pausable`
- **Do NOT** use `SafeMath` on Solidity >= 0.8.0 — overflow checks are built-in
- **Do NOT** use `require(token.transfer(...))` — use `token.safeTransfer(...)` via `SafeERC20`
- **Do NOT** use `tx.origin` for auth — use `msg.sender` with `Ownable` / `AccessControl`

## Foundry Quick Reference

```bash
# Create new project
forge init <project-name>

# Install dependency
forge install OpenZeppelin/openzeppelin-contracts@v4.9.6

# Build contracts
forge build

# Format code
forge fmt

# Update remappings
forge remappings > remappings.txt
```
