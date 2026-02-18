---
name: superfluid
description: >
  Use this skill for ANY question or task involving the Superfluid Protocol —
  writing integration code, debugging, looking up contract ABIs, understanding
  architecture, or answering questions. Do NOT search the web for Superfluid
  information before invoking this skill.
---

# Superfluid Protocol Skill

Complete interface documentation for Superfluid Protocol smart contracts via
Rich ABI YAML references. Read `references/architecture.md` for the full
protocol architecture. This file maps use-cases to the right references and
explains how to read them.

## Architecture Summary

**Host** (`Superfluid.sol`) — central router. Agreement calls go through
`Host.callAgreement()` or `Host.batchCall()`. Manages the app registry,
governance, and SuperTokenFactory.

**Agreements** — stateless financial primitives that store data on the token:
CFA (1:1 streams), GDA (many-to-many via pools), IDA (deprecated, replaced by GDA).

**Super Token** — ERC-20/ERC-777/ERC-2612 with real-time balance. Three
variants: Wrapper (ERC-20 backed), Native Asset/SETH (ETH backed), Pure
(pre-minted).

**Forwarders** (CFAv1Forwarder, GDAv1Forwarder) — convenience wrappers. Each
call is a standalone transaction with readable wallet descriptions. Cannot be
batched — use `Host.batchCall` with raw agreement calls for atomicity.

**MacroForwarder** — extensible batch executor. Developers deploy custom
macro contracts (`IUserDefinedMacro`) and call `MacroForwarder.runMacro()`
to execute complex multi-step operations atomically. See
`references/guides/macro-forwarders.md`.

**Automation** (Vesting Scheduler, FlowScheduler, Auto-Wrap) — schedule
on-chain intent, require off-chain keepers to trigger execution.

## Use-Case → Reference Map

Read only the files needed for the task. Each Rich ABI YAML documents every
public function, event, and error for one contract.

### Streaming money (CFA)

| Intent | Read |
|--------|------|
| Create/update/delete a stream (simple) | `references/contracts/CFAv1Forwarder.abi.yaml` |
| ACL, operator permissions, flow metadata | also `references/contracts/ConstantFlowAgreementV1.abi.yaml` |
| Batch streams with other ops atomically | also `references/contracts/Superfluid.abi.yaml` (Host batch call) |

### Distributing to many recipients (GDA)

| Intent | Read |
|--------|------|
| Create pools, distribute, stream to pool | `references/contracts/GDAv1Forwarder.abi.yaml` |
| Pool member management, units, claims | also `references/contracts/SuperfluidPool.abi.yaml` |
| Low-level agreement details | also `references/contracts/GeneralDistributionAgreementV1.abi.yaml` |

### Token operations

| Intent | Read |
|--------|------|
| Wrap/unwrap, balances, ERC-20/777, permit | `references/contracts/SuperToken.abi.yaml` |
| Deploy a new Super Token | `references/contracts/SuperTokenFactory.abi.yaml` |

### Automation

| Intent | Read |
|--------|------|
| Vesting with cliffs and streams | `references/contracts/VestingSchedulerV3.abi.yaml` |
| Schedule future stream start/stop | `references/contracts/FlowScheduler.abi.yaml` |
| Auto-wrap when Super Token balance is low | `references/contracts/AutoWrapManager.abi.yaml` and `references/contracts/AutoWrapStrategy.abi.yaml` |

### Writing Solidity integrations (SuperTokenV1Library)

| Intent | Read |
|--------|------|
| Token-centric Solidity API (`using SuperTokenV1Library for ISuperToken`) | `references/libraries/SuperTokenV1Library.abi.yaml` |

The library wraps CFA and GDA agreement calls into ergonomic methods like
`token.flow(receiver, flowRate)`. Use it for any Solidity contract that
interacts with Superfluid — Super Apps, automation contracts, DeFi
integrations. Includes agreement-abstracted functions (`flowX`, `transferX`)
that auto-route to CFA or GDA, plus `WithCtx` variants for Super App
callbacks. See the YAML header and glossary for Foundry testing gotchas.

### Building Super Apps

| Intent | Read |
|--------|------|
| CFA callback hooks (simplified base) | `references/bases/CFASuperAppBase.abi.yaml` |
| Token-centric API for callback logic | also `references/libraries/SuperTokenV1Library.abi.yaml` (use `WithCtx` variants) |
| App registration, Host context, batch calls | `references/contracts/Superfluid.abi.yaml` |

Super Apps that relay incoming flows via app credit cause the **sender's deposit
to roughly double** (or more for fan-out patterns), because outgoing stream
deposits are backed by the sender as owed deposit. See "App Credit & Deposit
Mechanics" in `references/architecture.md` for the full explanation.

### Macro forwarders (composable batch operations)

| Intent | Read |
|--------|------|
| Write a macro for complex batched operations | `references/guides/macro-forwarders.md` |
| MacroForwarder contract address and interface | also `references/guides/macro-forwarders.md` |
| Batch operation types and encoding rules | also `references/contracts/Superfluid.abi.yaml` (batch_operation_types) |
| EIP-712 signed macro patterns | `references/guides/macro-forwarders-eip712-example.md` |

### Sentinels and liquidation

| Intent | Read |
|--------|------|
| Batch liquidation of critical flows | `references/contracts/BatchLiquidator.abi.yaml` |
| PIC auction, bond management, exit rates | `references/contracts/TOGA.abi.yaml` |

### Querying indexed data (Subgraphs)

| Intent | Read |
|--------|------|
| Understand how The Graph generates query schemas from entity definitions | `references/subgraphs/query-patterns.md` |
| Query streams, pools, tokens, accounts, events | also `references/subgraphs/protocol-v1.graphql` |
| Query vesting schedules and execution history | also `references/subgraphs/vesting-scheduler.graphql` |
| Query scheduled flows and automation tasks | also `references/subgraphs/flow-scheduler.graphql` |
| Query auto-wrap schedules and execution history | also `references/subgraphs/auto-wrap.graphql` |

### Legacy

| Intent | Read |
|--------|------|
| Old IDA (instant distribution, deprecated) | `references/contracts/InstantDistributionAgreementV1.abi.yaml` |

### Ecosystem & tooling

| Intent | Read |
|--------|------|
| Which SDK or package for a project | See Ecosystem → SDKs & Packages below |
| Token prices, filtered token list, CoinGecko IDs | See Ecosystem → API Services (CMS) below |
| Stream accounting, per-day chunking | See Ecosystem → API Services (Accounting) below |
| Resolve ENS / Farcaster / Lens handles | See Ecosystem → API Services (Whois) below |
| Query protocol data via GraphQL | See Ecosystem → Subgraphs below |
| SUP token, governance, DAO | See Ecosystem → Foundation, DAO & SUP Token below |
| Token prices for Super Tokens (simple API) | See Ecosystem → API Services (Token Prices) below |
| Run a sentinel / liquidation bot | See Ecosystem → Sentinels below |
| Get a Super Token listed / enable automations | See Ecosystem → Processes below |

## Debugging Reverts

Error prefixes map to contracts:

| Prefix | Contract |
|--------|----------|
| `CFA_*` | ConstantFlowAgreementV1 |
| `CFA_FWD_*` | CFAv1Forwarder |
| `GDA_*` | GeneralDistributionAgreementV1 |
| `SUPERFLUID_POOL_*` | SuperfluidPool |
| `SF_TOKEN_*` | SuperfluidToken (base of SuperToken) |
| `SUPER_TOKEN_*` | SuperToken |
| `SUPER_TOKEN_FACTORY_*` | SuperTokenFactory |
| `HOST_*` | Superfluid (Host) |
| `IDA_*` | InstantDistributionAgreementV1 |
| `APP_RULE` | Superfluid (Host) — Super App callback violation |

Each YAML's `errors:` section is the complete error index for that contract,
with selector hashes and descriptions. Per-function `errors:` fields show
which errors a specific function can throw.

## Reading the Rich ABI YAMLs

Each YAML is a self-contained contract reference. Here's how to parse them.

### Root structure

```
# Header comment — contract name, description, key notes
meta:             # name, version, source, implements, inherits, deployments
# == Section ==   # Grouped functions (these are the core content)
events:           # All events the contract emits
errors:           # Complete error index
```

Three root keys are reserved: `meta`, `events`, `errors`. Every other
root-level key is a **function**.

### Function entries

```yaml
createFlow:
  # Description of what the function does.
  # GOTCHA: Non-obvious behavior or edge cases.
  mutability: nonpayable     # view | pure | nonpayable | payable
  access: sender | operator  # who can call (omitted for view/pure)
  inputs:
    - token: address
    - receiver: address
    - flowRate: int96        # inline comments for non-obvious params
    - ctx: bytes
  outputs:
    - newCtx: bytes
  emits: [FlowUpdated, FlowUpdatedExtension]   # ordered by emission sequence
  errors: [CFA_FLOW_ALREADY_EXISTS, CFA_INVALID_FLOW_RATE]  # ordered by check sequence
```

Fields appear in this order: description comment, `mutability`, `access`,
`inputs`, `outputs`, `emits`, `errors`. All are omitted when not applicable.

### Key conventions

- **`ctx: bytes` parameter** = function is called through the Host
  (`callAgreement` / `batchCall`), never directly.
- **`access` labels**: `anyone`, `host`, `self`, `admin`, `governance`,
  `sender`, `receiver`, `operator`, `manager`, `pic`, `agreement`,
  `trusted-forwarder`, `factory`, `super-app`. Combine with `|`. Conditional:
  `anyone(if-critical-or-jailed)`.
- **`emits` and `errors` ordering** carries meaning: matches execution flow,
  not alphabetical. First errors in the list are the most likely causes.
- **`# GOTCHA:`** prefix flags non-obvious behavior, common mistakes, or edge
  cases. Pay close attention to these.
- **`meta.source`** is an array of raw GitHub URLs to the Solidity source files
  (implementation, interface, base — filenames are self-documenting).
- **`meta.deployments`** has per-network addresses split into `mainnet` and
  `testnet` subgroups.

### Events section

```yaml
events:
  FlowUpdated:
    indexed:              # log topics (filterable)
      - token: address
      - sender: address
    data:                 # log payload
      - flowRate: int96
```

### Errors section

```yaml
errors:
  # -- Category --
  - SIMPLE_ERROR                    # 0xabcd1234 — description
  - PARAMETERIZED_ERROR:            # errors with diagnostic data
      inputs:
        - value: uint256
```

## Runtime Data (Scripts)

The Rich ABIs document **interfaces** (what to call and how). Scripts provide
**runtime data** (what to call it on) by wrapping canonical npm packages with
local caching for offline use. No npm install required — the scripts fetch
from CDN equivalents of the packages.

### ABI JSON — `@sfpro/sdk` package + `scripts/abi.mjs`

The [`@sfpro/sdk`](https://sdk.superfluid.pro/docs) package provides typed JSON ABIs
for use with viem / wagmi / ethers. ABIs are split across sub-paths:

| Contract (YAML name) | Import path | Export name |
|---|---|---|
| CFAv1Forwarder | `@sfpro/sdk/abi` | `cfaForwarderAbi` |
| GDAv1Forwarder | `@sfpro/sdk/abi` | `gdaForwarderAbi` |
| SuperfluidPool | `@sfpro/sdk/abi` | `gdaPoolAbi` |
| SuperToken | `@sfpro/sdk/abi` | `superTokenAbi` |
| Superfluid (Host) | `@sfpro/sdk/abi/core` | `hostAbi` |
| ConstantFlowAgreementV1 | `@sfpro/sdk/abi/core` | `cfaAbi` |
| GeneralDistributionAgreementV1 | `@sfpro/sdk/abi/core` | `gdaAbi` |
| InstantDistributionAgreementV1 | `@sfpro/sdk/abi/core` | `idaAbi` |
| SuperTokenFactory | `@sfpro/sdk/abi/core` | `superTokenFactoryAbi` |
| BatchLiquidator | `@sfpro/sdk/abi/core` | `batchLiquidatorAbi` |
| TOGA | `@sfpro/sdk/abi/core` | `togaAbi` |
| AutoWrapManager | `@sfpro/sdk/abi/automation` | `autoWrapManagerAbi` |
| AutoWrapStrategy | `@sfpro/sdk/abi/automation` | `autoWrapStrategyAbi` |
| FlowScheduler | `@sfpro/sdk/abi/automation` | `flowSchedulerAbi` |
| VestingSchedulerV3 | `@sfpro/sdk/abi/automation` | `vestingSchedulerV3Abi` |

The SDK also exports chain-indexed address objects alongside each ABI:

| Import path | Address exports |
|---|---|
| `@sfpro/sdk/abi` | `cfaForwarderAddress`, `gdaForwarderAddress` |
| `@sfpro/sdk/abi/core` | `hostAddress`, `cfaAddress`, `gdaAddress`, `idaAddress`, `superTokenFactoryAddress`, `batchLiquidatorAddress`, `togaAddress` |
| `@sfpro/sdk/abi/automation` | `autoWrapManagerAddress`, `autoWrapStrategyAddress`, `flowSchedulerAddress`, `vestingSchedulerV3Address` |

Each export is an object keyed by chain ID:

```js
import { hostAbi, hostAddress } from "@sfpro/sdk/abi/core";
const host = hostAddress[8453]; // Base Mainnet
```

CFASuperAppBase and SuperTokenV1Library are not in the SDK (abstract base /
Solidity library).

When writing application code, ALWAYS import ABIs and addresses from
`@sfpro/sdk` — do NOT hand-craft ABI fragments (risk of phantom parameters)
or hardcode contract addresses (they vary per network). Use `scripts/abi.mjs`
to inspect or inline ABIs when the SDK is not a dependency:

```
node abi.mjs <contract>               Full JSON ABI
node abi.mjs <contract> <function>    Single fragment by name
node abi.mjs list                     All contracts with SDK import info
```

Accepts YAML names (`CFAv1Forwarder`) and short aliases (`cfa`, `host`,
`pool`, `token`, `vesting`, etc.).

### Token list — `scripts/tokenlist.mjs`

Source: `@superfluid-finance/tokenlist` npm package.
Resolves Super Token addresses, symbols, and types. Use when you need to find
a specific token address or determine a Super Token's type.

```
node tokenlist.mjs super-token <chain-id> <symbol-or-address>
node tokenlist.mjs by-chain <chain-id> --super
node tokenlist.mjs by-symbol <symbol> [--chain-id <id>]
node tokenlist.mjs by-address <address>
node tokenlist.mjs stats
```

The `superTokenInfo.type` field determines which ABI patterns apply:
- **Wrapper** → `upgrade`/`downgrade` work; `underlyingTokenAddress` is
  provided. Underlying ERC-20 approval uses underlying's native decimals;
  Super Token functions always use 18 decimals.
- **Native Asset** → use `upgradeByETH`/`downgradeToETH` instead.
- **Pure** → `upgrade`/`downgrade` revert; no wrapping.

### Super Token balance — `scripts/balance.mjs`

Source: [Super API](https://superapi.kazpi.com) (real-time on-chain query).
Retrieves the current Super Token balance, net flow rate, and underlying token
balance for any account. No caching — balances are fetched live.

```
node balance.mjs balance <chain-id> <token-symbol-or-address> <account>
```

The output includes:
- **connected/unconnected balance** — wei and human-readable formatted values.
  Connected = streaming balance; unconnected = pending pool distributions.
- **netFlow** — aggregate flow rate in wei/sec and tokens/month (30-day month).
- **maybeCriticalAt** — estimated time when connected balance hits zero.
- **underlyingToken** — the wrapped ERC-20 balance (for Wrapper Super Tokens).

### Network metadata — `scripts/metadata.mjs`

Source: `@superfluid-finance/metadata` npm package.
Resolves contract addresses, subgraph endpoints, and network info for any
Superfluid-supported chain. Use when `meta.deployments` in a YAML doesn't
cover the target chain, or when you need automation/subgraph endpoints.

```
node metadata.mjs contracts <chain-id-or-name>
node metadata.mjs contract <chain-id-or-name> <key>
node metadata.mjs automation <chain-id-or-name>
node metadata.mjs subgraph <chain-id-or-name>
node metadata.mjs networks [--mainnets|--testnets]
```

Contract keys match the field names in the metadata: `host`, `cfaV1`,
`cfaV1Forwarder`, `gdaV1`, `gdaV1Forwarder`, `superTokenFactory`, `toga`,
`vestingSchedulerV3`, `flowScheduler`, `autowrap`, `batchLiquidator`, etc.

### On-chain reads — `cast call`

[`cast`](https://www.getfoundry.sh/cast) performs read-only `eth_call` queries against
any contract. If `cast` is not installed locally, use `bunx @foundry-rs/cast` instead.

**Never use `cast send` or any write/transaction command — read calls only.**

```
cast call <address> "functionName(inputTypes)(returnTypes)" [args] --rpc-url <url>
```

The return types in the second set of parentheses tell cast how to decode the
output. Without them you get raw hex.

**RPC endpoint:** `https://rpc-endpoints.superfluid.dev/{network-name}` — network
names are the canonical Superfluid names from `node metadata.mjs networks`
(e.g. `optimism-mainnet`, `base-mainnet`, `eth-mainnet`).

**Examples:**

```bash
# Total supply of USDCx on Optimism
cast call 0x35adeb0638eb192755b6e52544650603fe65a006 \
  "totalSupply()(uint256)" \
  --rpc-url https://rpc-endpoints.superfluid.dev/optimism-mainnet

# Flow rate via CFAv1Forwarder (address from Common Contract Addresses below)
cast call 0xcfA132E353cB4E398080B9700609bb008eceB125 \
  "getAccountFlowrate(address,address)(int96)" \
  <superTokenAddress> <account> \
  --rpc-url https://rpc-endpoints.superfluid.dev/optimism-mainnet
```

Use `abi.mjs` to look up exact function signatures and `metadata.mjs` /
`tokenlist.mjs` for contract and token addresses.

## Common Contract Addresses

Do NOT hardcode or fabricate addresses. Get them from the SDK address exports
(see ABI section above) or from `node scripts/metadata.mjs contracts <chain>`.

Forwarder addresses are the exception — uniform across most networks:
- CFAv1Forwarder: `0xcfA132E353cB4E398080B9700609bb008eceB125`
- GDAv1Forwarder: `0x6DA13Bde224A05a288748d857b9e7DDEffd1dE08`

Host and agreement addresses vary per network.

## Ecosystem

### SDKs & Packages

**Active — recommended for new projects:**

| Package | Purpose |
|---------|---------|
| [`@sfpro/sdk`](https://www.npmjs.com/package/@sfpro/sdk) | Frontend/backend SDK — ABIs, wagmi hooks, actions |
| [`@superfluid-finance/ethereum-contracts`](https://www.npmjs.com/package/@superfluid-finance/ethereum-contracts) | Build-time ABI source for codegen |
| [`@superfluid-finance/metadata`](https://www.npmjs.com/package/@superfluid-finance/metadata) | Contract addresses, network info (zero deps) |
| [`@superfluid-finance/tokenlist`](https://www.npmjs.com/package/@superfluid-finance/tokenlist) | Listed Super Tokens + underlying tokens |

**When to use what:**

- **Frontend with wagmi/viem** — install `@sfpro/sdk`. Enhanced ABIs include
  downstream errors for type-safe error handling. Import paths documented in
  the ABI section above.
  [Docs](https://sdk.superfluid.pro/docs) ·
  [Repo](https://github.com/superfluid-org/superfluid.pro/tree/main/sdk)
- **Solidity integrations** — import ABIs from
  `@superfluid-finance/ethereum-contracts` at build time. Do NOT use as a
  runtime dependency — it pulls in heavy deps not suitable for client bundles.
  [Repo](https://github.com/superfluid-org/protocol-monorepo/tree/dev/packages/ethereum-contracts)
- **Resolving addresses/networks at runtime** —
  `@superfluid-finance/metadata` has zero dependencies, wrapped by
  `scripts/metadata.mjs`.
  [Repo](https://github.com/superfluid-org/protocol-monorepo/tree/dev/packages/metadata)
- **Finding token addresses** — `@superfluid-finance/tokenlist` based on
  `@uniswap/token-lists`, wrapped by `scripts/tokenlist.mjs`.
  [Repo](https://github.com/superfluid-org/tokenlist)

**Deprecated — do not recommend for new projects:**

| Package | Replaced by | Why deprecated |
|---------|-------------|----------------|
| [`@superfluid-finance/sdk-core`](https://www.npmjs.com/package/@superfluid-finance/sdk-core) | `@sfpro/sdk` | Over-abstracted, locked to ethers v5. [Docs](https://superfluid.gitbook.io/superfluid/developers/sdk-core) · [Repo](https://github.com/superfluid-org/protocol-monorepo/tree/dev/packages/sdk-core) |
| [`@superfluid-finance/sdk-redux`](https://www.npmjs.com/package/@superfluid-finance/sdk-redux) | wagmi + `@sfpro/sdk` | Pre-wagmi Redux hooks. [Repo](https://github.com/superfluid-org/protocol-monorepo/tree/dev/packages/sdk-redux) |
| [`@superfluid-finance/js-sdk`](https://www.npmjs.com/package/@superfluid-finance/js-sdk) | `@sfpro/sdk` | Oldest SDK, truffle-based. [Repo](https://github.com/superfluid-org/protocol-monorepo/tree/dev/packages/js-sdk) |
| [`@superfluid-finance/widget`](https://www.npmjs.com/package/@superfluid-finance/widget) | — | Subscription checkout widget, stuck on wagmi v1. [Repo](https://github.com/superfluid-finance/widget) · [Playground](https://checkout-builder.superfluid.finance/) |

### API Services

| API | Base URL | Purpose |
|-----|----------|---------|
| Super API | `https://superapi.kazpi.com` | Real-time on-chain Super Token balances |
| CMS | `https://cms.superfluid.pro` | Token prices, price history, filtered token list |
| Points | `https://cms.superfluid.pro/points` | SUP points campaigns |
| Accounting | `https://accounting.superfluid.dev/v1` | Stream accounting with per-day chunking |
| Allowlist | `https://allowlist.superfluid.dev` | Check automation allowlist status |
| Whois | `https://whois.superfluid.finance` | Resolve profiles (ENS, Farcaster, Lens, AF) |
| Token Prices | `https://token-prices-api.superfluid.dev/v1/{network}/{token}` | Super Token prices (CoinGecko-backed) |

- **Super API** — wrapped by `scripts/balance.mjs`. Use the script instead of
  calling the API directly.
- **CMS** — can return unlisted Super Tokens (not just those in the
  tokenlist). Can get CoinGecko IDs for price lookups.
  [Swagger](https://cms.superfluid.pro/api-docs) ·
  [OpenAPI](https://cms.superfluid.pro/openapi.json) ·
  [Repo](https://github.com/superfluid-org/superfluid.pro/tree/main/cms)
- **Points** — SUP points campaigns (Stack.so replacement). Same repo as CMS.
  [API docs](https://cms.superfluid.pro/points/api-docs) ·
  [OpenAPI](https://cms.superfluid.pro/points/openapi.json)
- **Accounting** — splits per-second streams into chunked granularity (e.g.
  streamed per day). Handles CFA and ERC-20 transfers only — **no GDA
  support**.
  [Swagger](https://accounting.superfluid.dev/v1/swagger) ·
  [Repo](https://github.com/superfluid-org/accounting-api)
- **Allowlist** — `GET /api/allowlist/{account}/{chainId}`. Check if an
  account is allowlisted for automations (vesting, flow scheduling, auto-wrap).
- **Whois** — Resolves across ENS, AF, Farcaster, Lens, etc.
  - `GET /api/resolve/{address}` — address → profile/name
  - `GET /api/reverse-resolve/{handle}` — name/handle → address
  GOTCHA: despite the names, `resolve` takes an address and `reverse-resolve`
  takes a name.
- **Token Prices** — simpler alternative to CMS for price lookups. Provides
  prices for all listed SuperTokens where the token (or underlying) is known to
  CoinGecko. Endpoint: `GET /v1/{canonical-network-name}/{token-address}`.
  [Repo](https://github.com/d10r/sf-token-prices-api/)

### Subgraphs

**Prefer RPC over subgraph for current state.** The subgraph only updates on
transactions, but Superfluid state changes continuously (streams flow every
second). Balances, flow rates, and distribution states on the subgraph are
always behind. This is especially true for GDA and IDA — their 1-to-many and
N-to-many primitives are built for scalability: a distribution to millions of
pool members updates only the Pool entity on-chain (one event), so individual
PoolMember records on the subgraph won't reflect the new state until each
member transacts. Use `cast call` or `scripts/balance.mjs` for real-time
reads. The subgraph is best for historical queries, event indexing, and
listing/filtering entities.

For entity schemas and query construction patterns, see the
"Querying indexed data" use-case section above.

Endpoint pattern: `https://subgraph-endpoints.superfluid.dev/{network-name}/{subgraph}`

| Subgraph | Path | Notes |
|----------|------|-------|
| Protocol | `protocol-v1` | Main protocol data (streams, tokens, accounts) |
| Vesting Scheduler | `vesting-scheduler` | All versions: v1, v2, v3 |
| Flow Scheduler | `flow-scheduler` | |
| Auto-Wrap | `auto-wrap` | |

Network names are canonical Superfluid names (`optimism-mainnet`,
`base-mainnet`, etc.). Use `node metadata.mjs subgraph <chain>` to get the
resolved URL for a specific chain.

### Apps

| App | URL | Purpose |
|-----|-----|---------|
| Dashboard | [app.superfluid.org](https://app.superfluid.org/) | Stream management for end-users |
| Explorer | [explorer.superfluid.org](https://explorer.superfluid.org/) | Block explorer for Superfluid Protocol |
| Claim | [claim.superfluid.org](https://claim.superfluid.org/) | SUP token, SUP points, reserves/lockers |
| TOGA | [toga.superfluid.finance](https://toga.superfluid.finance/) | View recent liquidations by token |

Repos:
[Dashboard](https://github.com/superfluid-org/superfluid-dashboard) ·
[Explorer](https://github.com/superfluid-org/superfluid-explorer) ·
[TOGA](https://github.com/superfluid-org/toga-suit)

### Sentinels

Sentinels monitor streams and liquidate senders whose Super Token balance
reaches zero, keeping the protocol solvent. Anyone can run one.

| Tool | Purpose |
|------|---------|
| [Graphinator](https://github.com/superfluid-org/graphinator) | Lightweight subgraph-based sentinel |

### Foundation, DAO & SUP Token

**Superfluid Foundation** — independent entity overseeing long-term protocol
stewardship. Provides governance facilitation, administrative, and legal
support.

**Superfluid DAO** — community-driven governance. Includes a Security Council
that handles routine protocol upgrades. Proposals discussed on the
[forum](https://forum.superfluid.org/), voted on via
[Snapshot](https://snapshot.box/#/s:superfluid.eth) (`superfluid.eth`).
Delegate SUP at
[claim.superfluid.org/governance](https://claim.superfluid.org/governance).

**SUP token** — a SuperToken on Base. Address:
`0xa69f80524381275a7ffdb3ae01c54150644c8792`. Total supply: 1,000,000,000.
Future inflation at DAO discretion.
[CoinGecko](https://www.coingecko.com/en/coins/superfluid)

Distribution:
- **60% community** — distributed via Streaming Programmatic Rewards (SPR)
  over at least 2 years in quarterly seasons. SPR streams token rewards
  continuously (alternative to one-off airdrops). Sub-split between DAO
  treasury and foundation funds.
- **25% development team** — 3-year lockup stream with 1-year cliff.
- **15% early backers** — same 3-year lockup with 1-year cliff.

**Locker / Reserve system** — on-chain staking mechanism (FluidLocker
contract). Holders lock SUP and choose unlock duration — longer lockup = bigger
bonus, early unlock incurs a tax. Terminology: "Locker" in contracts, "Reserve"
in the UI and marketing (e.g. the Claim app).

Links:
[Website](https://superfluid.org/) ·
[Blog](https://superfluid.org/blog) ·
[Forum](https://forum.superfluid.org/) ·
[Claim app](https://claim.superfluid.org/) ·
[Token launch announcement](https://x.com/Superfluid_HQ/status/1892236759771091346)

### Processes

**Token Listing** — a Super Token gets listed on the on-chain Resolver, which
the subgraph picks up (marks `isListed`). Once listed, it appears in the
Superfluid token list along with its underlying token (if any).

- Request: [listing form](https://airtable.com/appxGogNpt64ImOFH/shrzOcdK9eveDmRWV)
  → opens issue in [superfluid-org/assets](https://github.com/superfluid-org/assets/issues)

**Automation Allowlisting** — required for automations (vesting, flow
scheduling, auto-wrap) to appear in the Dashboard UI and for Superfluid
off-chain keepers to trigger the automation contracts. Without allowlisting,
automations won't be executed on time and are effectively useless.

- Request: [allowlisting form](https://airtable.com/appmq3TJDdQUrTQpx/shrWouN6ursCkOQ86)
- Check status: `GET https://allowlist.superfluid.dev/api/allowlist/{account}/{chainId}`
