---
name: solidity-security
description: "[AUTO-INVOKE] MUST be invoked BEFORE writing or modifying any Solidity contract (.sol files). Covers private key handling, access control, reentrancy prevention, gas safety, and pre-audit checklists. Trigger: any task involving creating, editing, or reviewing .sol source files."
---

# Solidity Security Standards

## Language Rule

- **Always respond in the same language the user is using.** If the user asks in Chinese, respond in Chinese. If in English, respond in English.

## Private Key Protection

- Store private keys in `.env`, load via `source .env` — never pass keys as CLI arguments
- Never expose private keys in logs, screenshots, conversations, or commits
- Provide `.env.example` with placeholder values for team reference
- Add `.env` to `.gitignore` — verify with `git status` before every commit

## Security Decision Rules

When writing or reviewing Solidity code, apply these rules:

| Situation | Required Action |
|-----------|----------------|
| External ETH/token transfer | Use `ReentrancyGuard` + Checks-Effects-Interactions (CEI) pattern |
| ERC20 token interaction | Use `SafeERC20` — call `safeTransfer` / `safeTransferFrom`, never raw `transfer` / `transferFrom` |
| Owner-only function | Inherit `Ownable2Step` (preferred) or `Ownable` from OZ 4.9.x — `Ownable2Step` prevents accidental owner loss |
| Multi-role access | Use `AccessControl` from `@openzeppelin/contracts/access/AccessControl.sol` |
| Token approval | Use `safeIncreaseAllowance` / `safeDecreaseAllowance` from `SafeERC20` — never raw `approve` |
| Price data needed | Use Chainlink `AggregatorV3Interface` if feed exists; otherwise TWAP with min-liquidity check — never use spot pool price directly |
| Upgradeable contract | Prefer UUPS (`UUPSUpgradeable`) over TransparentProxy; always use `Initializable` |
| Solidity version < 0.8.0 | Must use `SafeMath` — but strongly prefer upgrading to 0.8.20+ |
| Emergency scenario | Inherit `Pausable`, add `whenNotPaused` to user-facing functions; keep admin/emergency functions unpaused |
| Whitelist / airdrop | Use `MerkleProof` for gas-efficient verification — never store full address lists on-chain |
| Signature-based auth | Use `ECDSA` + `EIP712` — never roll custom signature verification |
| Signature content | Signature must bind `chainId` + `nonce` + `msg.sender` + `deadline` — prevent replay and cross-chain reuse |
| Cross-chain bridge / third-party dependency | Audit all inherited third-party contract code — never assume dependencies are safe |
| Deprecated / legacy contracts | Permanently `pause` or `selfdestruct` deprecated contracts — never leave unused contracts callable on-chain |

## Reentrancy Protection

- All contracts with external calls: inherit `ReentrancyGuard`, add `nonReentrant` modifier
  - Import: `@openzeppelin/contracts/security/ReentrancyGuard.sol` (OZ 4.9.x)
- Always apply CEI pattern even with `ReentrancyGuard`:
  1. **Checks** — validate all conditions (`require`)
  2. **Effects** — update state variables
  3. **Interactions** — external calls last

## Input Validation

- Reject `address(0)` for all address parameters
- Reject zero amounts for fund transfers
- Validate array lengths match when processing paired arrays
- Bound numeric inputs to reasonable ranges (prevent dust attacks, gas griefing)

## Gas Control

- Deployment commands must include `--gas-limit` (recommended >= 3,000,000)
- Monitor gas with `forge test --gas-report` — review before every PR
- Configure optimizer in `foundry.toml`: `optimizer = true`, `optimizer_runs = 200`
- Avoid unbounded loops over dynamic arrays — use pagination or pull patterns

## Pre-Audit Checklist

Before submitting code for review or audit, verify:

**Access & Control:**
- [ ] All external/public functions have `nonReentrant` where applicable
- [ ] No `tx.origin` used for authentication (use `msg.sender`)
- [ ] No `delegatecall` to untrusted addresses
- [ ] Owner transfer uses `Ownable2Step` (not `Ownable`) to prevent accidental loss
- [ ] Contracts with user-facing functions inherit `Pausable` with `pause()` / `unpause()`

**Token & Fund Safety:**
- [ ] All ERC20 interactions use `SafeERC20` (`safeTransfer` / `safeTransferFrom`)
- [ ] No raw `token.transfer()` or `require(token.transfer())` patterns
- [ ] Token approvals use `safeIncreaseAllowance`, not raw `approve`
- [ ] All `external call` return values checked

**Code Quality:**
- [ ] Events emitted for every state change
- [ ] No hardcoded addresses — use config or constructor params
- [ ] `.env` is in `.gitignore`

**Oracle & Price (if applicable):**
- [ ] Price data sourced from Chainlink feed or TWAP — never raw spot price
- [ ] Oracle has minimum liquidity check — revert if pool reserves too low
- [ ] Price deviation circuit breaker in place

**Testing:**
- [ ] `forge test` passes with zero failures
- [ ] `forge coverage` shows adequate coverage on security-critical paths
- [ ] Fuzz tests cover arithmetic edge cases (zero, max uint, boundary values)

## Security Verification Commands

```bash
# Run all tests with gas report
forge test --gas-report

# Fuzz testing with higher runs for critical functions
forge test --fuzz-runs 10000

# Check test coverage
forge coverage

# Dry-run deployment to verify no runtime errors
forge script script/Deploy.s.sol --fork-url $RPC_URL -vvvv

# Static analysis (if slither installed)
slither src/
```
