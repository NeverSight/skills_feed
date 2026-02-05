---
name: opnet-development
description: Build on OPNet - Bitcoin L1 consensus layer for trustless smart contracts. Use when building AssemblyScript smart contracts, TypeScript libraries, React frontends, or Node plugins for OPNet. Triggers on Bitcoin smart contract development, OP20 tokens, OP721 NFTs, WebAssembly contracts, verify-dont-custody patterns, epoch mining, and OPNet architecture questions.
---

# OPNet Development Skill

A comprehensive skill for building on OPNet - Bitcoin's L1 consensus layer for trustless smart contracts.

---

# STOP - MANDATORY READING BEFORE ANY CODE

**IF YOU WRITE CODE WITHOUT READING THE REQUIRED DOCS, YOU WILL CREATE BROKEN, EXPLOITABLE CODE.**

---

## CRITICAL RULES FOR AI AGENTS

### DO NOT:
- Read a few files and then say "I have enough context"
- Read random skills or guidelines not listed for your project type
- Start writing code after skimming 2-3 files
- Assume you know OPNet patterns from other frameworks
- Skip files because they "seem similar" to ones you read
- Create zip files or deliverables WITHOUT running `npm run lint` and `npm run typecheck`
- Say "run npm run lint to verify" instead of ACTUALLY running it

### YOU MUST:
- Read **EVERY SINGLE FILE** listed for your project type below
- Read them **IN ORDER** - later files depend on earlier ones
- Read the **COMPLETE FILE**, not just the first few sections
- **ONLY** read files listed in this skill - no random exploration
- Confirm you read all files before writing ANY code
- **ACTUALLY RUN** `npm install`, `npm run lint`, `npm run typecheck`, `npm run build`
- **FIX ALL ERRORS** before creating any deliverable (zip, PR, etc.)

---

## WHY THIS MATTERS

OPNet development has:
- **Beta package versions** that change frequently - guessing versions = build failures
- **Strict TypeScript rules** - violations = security vulnerabilities
- **Platform-specific patterns** - wrong patterns = exploits, gas attacks, data loss

**Guidelines are SUMMARIES. The `docs/` folder contains the ACTUAL implementation patterns.**

**Reading 3-4 files is NOT enough. You MUST read ALL files for your project type.**

---

## MANDATORY READING ORDER BY PROJECT TYPE

### For ALL Projects (Read First, Every Time)

| Order | File | Why |
|-------|------|-----|
| 1 | `docs/core-typescript-law-CompleteLaw.md` | **THE LAW** - Type system rules, forbidden constructs, required patterns |
| 2 | `guidelines/setup-guidelines.md` | Package versions, tsconfig, ESLint configs |

---

### For Smart Contracts (AssemblyScript)

**Read ALL of these BEFORE writing contract code:**

| Order | File | Contains |
|-------|------|----------|
| 1 | `docs/core-typescript-law-CompleteLaw.md` | Type rules (applies to AS too) |
| 2 | `guidelines/setup-guidelines.md` | Package versions, asconfig.json |
| 3 | `guidelines/contracts-guidelines.md` | Summary of contract patterns |
| 4 | `docs/contracts-btc-runtime-README.md` | Runtime overview |
| 5 | `docs/contracts-btc-runtime-getting-started-installation.md` | Setup |
| 6 | `docs/contracts-btc-runtime-getting-started-first-contract.md` | Entry point, factory pattern |
| 7 | `docs/contracts-btc-runtime-getting-started-project-structure.md` | Directory layout |
| 8 | `docs/contracts-btc-runtime-core-concepts-storage-system.md` | Storage types, pointers |
| 9 | `docs/contracts-btc-runtime-core-concepts-pointers.md` | Pointer allocation |
| 10 | `docs/contracts-btc-runtime-api-reference-safe-math.md` | SafeMath (MANDATORY for u256) |
| 11 | `docs/contracts-btc-runtime-gas-optimization.md` | Gas patterns, forbidden loops |
| 12 | `docs/contracts-btc-runtime-core-concepts-security.md` | Security checklist |

**For OP20 tokens, also read:**
- `docs/contracts-btc-runtime-api-reference-op20.md`
- `docs/contracts-btc-runtime-contracts-op20-token.md`

**For OP721 NFTs, also read:**
- `docs/contracts-btc-runtime-api-reference-op721.md`
- `docs/contracts-btc-runtime-contracts-op721-nft.md`

---

### For Frontend (React/Vite)

**Read ALL of these BEFORE writing frontend code:**

| Order | File | Contains |
|-------|------|----------|
| 1 | `docs/core-typescript-law-CompleteLaw.md` | Type rules, forbidden constructs |
| 2 | `guidelines/setup-guidelines.md` | Package versions, vite config |
| 3 | `guidelines/frontend-guidelines.md` | Summary of frontend patterns |
| 4 | `docs/core-opnet-README.md` | Client library overview |
| 5 | `docs/core-opnet-getting-started-installation.md` | Installation |
| 6 | `docs/core-opnet-getting-started-quick-start.md` | Quick start |
| 7 | `docs/core-opnet-providers-json-rpc-provider.md` | Provider setup |
| 8 | `docs/core-opnet-providers-internal-caching.md` | Caching (MANDATORY) |
| 9 | `docs/core-opnet-contracts-instantiating-contracts.md` | Contract instances |
| 10 | `docs/core-opnet-contracts-simulating-calls.md` | Read operations |
| 11 | `docs/core-opnet-contracts-sending-transactions.md` | Write operations |
| 12 | `docs/clients-walletconnect-README.md` | Wallet connection |
| 13 | `docs/frontend-motoswap-ui-README.md` | **THE STANDARD** - Reference implementation |

---

### For Backend/API (Node.js)

**Read ALL of these BEFORE writing backend code:**

| Order | File | Contains |
|-------|------|----------|
| 1 | `docs/core-typescript-law-CompleteLaw.md` | Type rules, forbidden constructs |
| 2 | `guidelines/setup-guidelines.md` | Package versions |
| 3 | `guidelines/backend-guidelines.md` | Summary of backend patterns |
| 4 | `docs/core-opnet-backend-api.md` | **REQUIRED FRAMEWORKS** - hyper-express, uWebSockets.js |
| 5 | `docs/core-opnet-providers-json-rpc-provider.md` | Provider setup |
| 6 | `docs/core-opnet-providers-threaded-http.md` | Threading (MANDATORY) |
| 7 | `docs/core-opnet-providers-internal-caching.md` | Caching (MANDATORY) |
| 8 | `docs/core-opnet-contracts-instantiating-contracts.md` | Contract instances |

**FORBIDDEN FRAMEWORKS:** Express, Fastify, Koa, Hapi, Socket.io - use hyper-express and uWebSockets.js only.

---

### For Plugins (OPNet Node)

**Read ALL of these BEFORE writing plugin code:**

| Order | File | Contains |
|-------|------|----------|
| 1 | `docs/core-typescript-law-CompleteLaw.md` | Type rules, forbidden constructs |
| 2 | `guidelines/setup-guidelines.md` | Package versions |
| 3 | `guidelines/plugin-guidelines.md` | Summary of plugin patterns |
| 4 | `docs/core-OIP-OIP-0003.md` | **PLUGIN SPECIFICATION** - Full spec |
| 5 | `docs/plugins-plugin-sdk-README.md` | SDK reference |
| 6 | `docs/plugins-opnet-node-README.md` | Node integration |

**CRITICAL:** You MUST implement `onReorg()` to handle chain reorganizations or your data will be inconsistent.

---

### For Unit Tests (TypeScript)

**Read ALL of these BEFORE writing test code:**

| Order | File | Contains |
|-------|------|----------|
| 1 | `docs/core-typescript-law-CompleteLaw.md` | Type rules |
| 2 | `guidelines/setup-guidelines.md` | Package versions |
| 3 | `guidelines/unit-testing-guidelines.md` | Summary of test patterns |
| 4 | `docs/testing-unit-test-framework-README.md` | Framework overview |
| 5 | `docs/testing-opnet-unit-test-README.md` | Test setup |
| 6 | `docs/testing-opnet-unit-test-docs-Blockchain.md` | Blockchain mocking |
| 7 | `docs/testing-opnet-unit-test-docs-ContractRuntime.md` | Contract runtime |

**CRITICAL:** Unit tests are TypeScript (NOT AssemblyScript). They have a SEPARATE package.json.

---

### For Generic Questions (Architecture, Concepts, Best Practices)

**Read:** `guidelines/generic-questions-guidelines.md`

For questions like:
- "How does OPNet work?"
- "Can OPNet survive 51% attacks?"
- "How does airdrop work on OPNet?"
- "What's the difference between OPNet and Runes/Ordinals?"
- "Why can't contracts hold BTC?"
- "What is transaction pinning?"

**See the full guideline for complete topic mappings and what docs to read for each question type.**

**IMPORTANT: For conceptual questions, read the relevant docs/sections BEFORE answering. Do not guess or make assumptions about how OPNet works.**

---

### For Security Auditing

---

# STOP - MANDATORY READING BEFORE ANY AUDIT

**IF YOU AUDIT CODE WITHOUT READING THE REQUIRED DOCS, YOU WILL MISS CRITICAL VULNERABILITIES.**

OPNet audits require understanding:
- **AssemblyScript runtime internals** - serialization, storage, cache coherence
- **Bitcoin-specific attack vectors** - transaction pinning, malleability, reorgs
- **Critical vulnerability patterns** - that standard audits miss completely

**You MUST read `guidelines/audit-guidelines.md` COMPLETELY before auditing ANY code.**

**Skipping the audit guidelines = missing vulnerabilities. There are no shortcuts.**

---

#### DISCLAIMER (MANDATORY IN EVERY REPORT)

```
IMPORTANT DISCLAIMER: This audit is AI-assisted and may contain errors,
false positives, or miss critical vulnerabilities. This is NOT a substitute
for a professional security audit by experienced human auditors.
Do NOT deploy to production based solely on this review.
Always engage professional auditors for contracts handling real value.
```

---

#### Mandatory Reading Order for Audits

**Read ALL of these IN ORDER before starting ANY audit:**

| Order | File | Why Required |
|-------|------|--------------|
| 1 | `docs/core-typescript-law-CompleteLaw.md` | Type rules that define secure code |
| 2 | `guidelines/audit-guidelines.md` | **COMPLETE AUDIT GUIDE** - vulnerability patterns, checklists, detection methods |

**Then read based on code type:**

| Code Type | Additional Required Reading |
|-----------|----------------------------|
| Smart Contracts | `docs/contracts-btc-runtime-core-concepts-security.md`, `docs/contracts-btc-runtime-gas-optimization.md`, `docs/contracts-btc-runtime-api-reference-safe-math.md`, `docs/contracts-btc-runtime-types-bytes-writer-reader.md` |
| DEX/Swap Code | This SKILL.md - CSV, NativeSwap, Slashing sections |
| Frontend | `guidelines/frontend-guidelines.md` |
| Backend | `guidelines/backend-guidelines.md` |
| Plugins | `guidelines/plugin-guidelines.md` - Reorg Handling section |

---

#### AUDIT VERIFICATION CHECKPOINT

**BEFORE writing ANY audit findings, confirm:**

- [ ] I have read `guidelines/audit-guidelines.md` completely
- [ ] I have read `docs/core-typescript-law-CompleteLaw.md` completely
- [ ] I have read ALL additional docs for this code type
- [ ] I understand the Critical Runtime Vulnerability Patterns section
- [ ] I understand serialization/deserialization consistency requirements
- [ ] I understand storage system cache coherence issues
- [ ] I understand Bitcoin-specific attack vectors (CSV, pinning, reorgs)

**If you cannot check ALL boxes, GO BACK AND READ THE DOCS.**

---

#### Smart Contract Audit Checklist (Summary)

**See `guidelines/audit-guidelines.md` for COMPLETE checklists with detection patterns.**

| Category | Check For |
|----------|-----------|
| **Arithmetic** | All u256 operations use SafeMath (no raw `+`, `-`, `*`, `/`) |
| **Overflow/Underflow** | SafeMath.add(), SafeMath.sub(), SafeMath.mul(), SafeMath.div() |
| **Access Control** | onlyOwner checks, authorization on sensitive methods |
| **Reentrancy** | State changes BEFORE external calls (checks-effects-interactions) |
| **Gas/Loops** | No `while` loops, all `for` loops bounded, no unbounded iterations |
| **Storage** | No iterating all map keys, stored aggregates for totals |
| **Input Validation** | All user inputs validated, bounds checked |
| **Integer Handling** | u256 created via fromString() for large values, not arithmetic |
| **Serialization** | Write/read type consistency, sizeof<T>() mapping correct |
| **Cache Coherence** | Setters load from storage before comparison |
| **Deletion Markers** | Storage deletion uses 32-byte EMPTY_BUFFER |
| **Bounds Checking** | `>=` not `>` for max index checks |

#### TypeScript/Frontend/Backend Audit Checklist (Summary)

| Category | Check For |
|----------|-----------|
| **Type Safety** | No `any`, no `!` assertions, no `@ts-ignore` |
| **Null Safety** | Explicit null checks, optional chaining used correctly |
| **BigInt** | All satoshi/token amounts use `bigint`, not `number` |
| **No Floats** | No floating point for financial calculations |
| **Caching** | Provider/contract instances cached, not recreated |
| **Input Validation** | Address validation, amount validation, bounds checking |
| **Error Handling** | Errors caught and handled, no silent failures |
| **Provider Type** | Use JSONRpcProvider (WebSocketProvider is experimental) |

#### Bitcoin-Specific Audit Checklist (Summary)

| Category | Check For |
|----------|-----------|
| **CSV Timelocks** | All swap recipient addresses use CSV (anti-pinning) |
| **UTXO Handling** | Proper UTXO selection, dust outputs avoided |
| **Transaction Malleability** | Signatures not assumed immutable before confirmation |
| **Fee Sniping** | Proper locktime handling |
| **Reorg Handling** | Data deleted/reverted for reorged blocks |
| **P2WPKH** | Only compressed pubkeys (33 bytes), reject uncompressed |
| **Witness Script Size** | Validate against 3,600 byte standard limit |

#### DEX/Swap Audit Checklist (Summary)

| Category | Check For |
|----------|-----------|
| **Reservation System** | Prices locked at reservation, not execution |
| **Slippage Protection** | Maximum slippage enforced |
| **Front-Running** | Reservation system prevents front-running |
| **Queue Manipulation** | Slashing penalties for queue abuse |
| **Partial Fills** | Atomic coordination of multi-provider payments |

#### Critical Runtime Vulnerability Patterns (Summary)

**See `guidelines/audit-guidelines.md` for COMPLETE patterns with code examples.**

| ID | Vulnerability | Impact |
|----|---------------|--------|
| C-07 | Serialization Mismatch (write u16, read u32) | Data corruption |
| C-08 | sizeof<T>() bytes treated as bits | Truncated data |
| C-09 | Signed/unsigned type confusion (i8 → u8) | Sign loss |
| C-10 | Cache coherence (setter compares to unloaded cache) | Silent state corruption |
| C-11 | Wrong deletion marker size | has() returns wrong result |
| C-12 | Generic integer truncation (only reading first byte) | Data loss |
| H-06 | Index out of bounds | Memory corruption |
| H-07 | Off-by-one (`>` instead of `>=`) | Buffer overflow |
| H-08 | Pointer collision (truncate without hash) | Storage overwrites |
| M-05 | Taylor series divergence | Incorrect math |

**ALWAYS end audit reports with the disclaimer. NEVER claim the audit is complete or guarantees security.**

---

## VERIFICATION CHECKPOINT

**BEFORE writing ANY code, you MUST be able to answer:**

1. **What project type am I building?** (Contract / Frontend / Backend / Plugin / Tests)

2. **Did I read EVERY file listed for this project type?**
   - List each file you read
   - If you cannot list them all, GO BACK AND READ

3. **What are the exact package versions?** (from `guidelines/setup-guidelines.md`)
   - If you don't know, GO BACK AND READ

4. **What constructs are FORBIDDEN?**
   - `any`, `!`, `while` loops in contracts, `number` for satoshis, etc.
   - If you can't list them, GO BACK AND READ

5. **What patterns are REQUIRED?**
   - Caching, SafeMath, threading, etc.
   - If you can't list them, GO BACK AND READ

---

### STOP - DO NOT PROCEED IF:

- ❌ You read fewer than 5 docs files
- ❌ You skipped any file in the mandatory reading list
- ❌ You read files not listed for your project type
- ❌ You cannot list the exact package versions
- ❌ You're about to write "I have enough context" after reading 2-3 files

**GO BACK AND READ ALL THE REQUIRED FILES. NO SHORTCUTS.**

---

## CODE VERIFICATION ORDER (MANDATORY)

**You MUST actually RUN these commands, not just mention them.**

### Step 1: Install Dependencies
```bash
npm install
```
- Run this FIRST before any other commands
- If package.json was created or modified, this is REQUIRED
- Do NOT skip this step

### Step 2: Run Prettier
```bash
npm run format
```
- Formats all code consistently
- Run BEFORE linting to avoid formatting conflicts
- Do NOT skip this step

### Step 3: Run ESLint
```bash
npm run lint
```
- MUST pass with zero errors
- If errors exist, FIX THEM before proceeding
- Do NOT say "you should run lint" - actually RUN IT

### Step 4: Run TypeScript Check
```bash
npm run typecheck
```
- Or `npx tsc --noEmit` if no script exists
- MUST pass with zero errors
- Fix all type errors before proceeding

### Step 5: Build
```bash
npm run build
```
- Only run AFTER format, lint, and typecheck pass
- For contracts: verify .wasm file is generated

### Step 6: Run Tests
```bash
npm run test
```
- Or `npx ts-node --esm tests/*.test.ts` for unit tests
- All tests MUST pass
- If tests fail, FIX THE CODE

---

### STOP - YOU MUST ACTUALLY RUN THESE COMMANDS

- ❌ Do NOT just write "run npm run lint to verify"
- ❌ Do NOT skip steps because "it should work"
- ❌ Do NOT consider code complete without running ALL steps
- ✅ Actually execute each command
- ✅ Verify each command passes
- ✅ Fix any errors before proceeding to next step

**If you wrote code but didn't run these commands, YOUR TASK IS NOT COMPLETE.**

---

## TASK COMPLETION CHECKPOINT

**BEFORE considering ANY task complete, ask yourself these questions:**

1. **Have I performed all the steps required by the task?**
   - Did I address everything the user asked for?
   - Did I miss any requirements?

2. **Did I actually run the verification commands?**
   - Did I run `npm install`? (REQUIRED if package.json exists/changed)
   - Did I run `npm run format`? (REQUIRED - Prettier formatting)
   - Did I run `npm run lint`? (REQUIRED - must pass with zero errors)
   - Did I run `npm run typecheck` or `npx tsc --noEmit`? (REQUIRED)
   - Did I run `npm run build`? (REQUIRED for deployable code)
   - Did I run `npm run test`? (REQUIRED if tests exist)
   - **If ANY command failed, did I fix the errors?**
   - **"I should run lint" is NOT the same as actually running it**

3. **Did I review and reconsider my work?**
   - Re-read what I produced - is it correct?
   - Did I make any assumptions that could be wrong?
   - Are there edge cases I didn't consider?
   - Could my code/answer introduce bugs or vulnerabilities?
   - For smart contracts: SafeMath, bounds checking, access control, serialization
   - For TypeScript: type safety, null handling, caching patterns
   - For answers: Is the information accurate? Did I verify it?

4. **Did I write complete, production-ready code?**
   - **NEVER** add comments like "in a production environment, you would..."
   - **NEVER** add stubs, placeholders, or TODO comments
   - **NEVER** write partial implementations with "add your logic here"
   - If you can't implement something fully, explain why and ask the user
   - All code must be ready to use immediately, not a starting point

5. **Is it appropriate to adjust non-code files?**
   - Did I update documentation if behavior changed?
   - Did I update config files if dependencies changed?

6. **Should new tests be written?**
   - If I added new functionality, are there tests for it?
   - Do the tests cover security patterns from the guidelines?

7. **Is this just exploration/research?**
   - If yes, tests, linting, and auditing are not required
   - Focus on providing accurate information

**This self-reflection prevents incomplete work, missed requirements, and security vulnerabilities.**

---

## PROJECT DELIVERY

---

### STOP - BEFORE CREATING ANY ZIP OR DELIVERABLE

**You MUST run and PASS all verification commands BEFORE packaging:**

```bash
# 1. Install dependencies
npm install

# 2. Format code
npm run format

# 3. Lint (MUST PASS)
npm run lint

# 4. TypeScript check (MUST PASS)
npm run typecheck
# OR: npx tsc --noEmit

# 5. Build (MUST SUCCEED)
npm run build

# 6. Tests (MUST PASS)
npm run test
```

**If ANY command fails, DO NOT create the zip. Fix the errors first.**

❌ **FORBIDDEN:** Creating zip without running verification commands
❌ **FORBIDDEN:** Saying "run npm run lint to verify" instead of actually running it
❌ **FORBIDDEN:** Skipping typecheck because "it should work"

---

**When creating zip files for delivery:**

**NEVER include:**
- `node_modules/` - recipient runs `npm install`
- `build/` or `dist/` - recipient runs `npm run build`
- `.git/` - repository history
- `.env` - contains secrets

**Correct zip command (only AFTER all checks pass):**
```bash
zip -r project.zip . -x "node_modules/*" -x "build/*" -x "dist/*" -x ".git/*" -x "*.wasm" -x ".env"
```

---

## What is OPNet

OPNet is a **Bitcoin L1 consensus layer** enabling smart contracts directly on Bitcoin. It is:

- **NOT a metaprotocol** - It's a full consensus layer
- **Fully trustless** - No centralized components
- **Permissionless** - Anyone can participate
- **Decentralized** - Relies on Bitcoin PoW + OPNet epoch SHA1 mining

### Security Model

After 20 blocks, an epoch is buried deep enough that changing it requires rewriting Bitcoin history at **millions of dollars per hour**, making OPNet state **more final than Bitcoin's 6-confirmation security**.

The **checksum root** for each epoch is a cryptographic fingerprint of the entire state. If even one bit differs, the checksum changes completely and proof fails, making **silent state corruption impossible**.

### Key Principles

1. **Contracts are WebAssembly** (AssemblyScript) - Deterministic execution
2. **NON-CUSTODIAL** - Contracts NEVER hold BTC
3. **Verify-don't-custody** - Contracts verify L1 tx outputs, not hold funds
4. **Partial reverts** - Only consensus layer execution reverts; Bitcoin transfers are ALWAYS valid
5. **No gas token** - Uses Bitcoin directly
6. **CSV timelocks are MANDATORY** - All addresses receiving BTC in swaps MUST use CSV (CheckSequenceVerify) to prevent transaction pinning attacks

### Why OPNet Requires Consensus (Not Just Indexing)

OPNet is fundamentally different from indexer-based protocols like Runes, Ordinals/BRC-20, or Alkanes:

| Protocol | State Consistency | Can Different Nodes Disagree? |
|----------|-------------------|-------------------------------|
| Runes | Indexer-dependent | Yes - no consensus mechanism |
| BRC-20 | Indexer-dependent | Yes - no consensus mechanism |
| Alkanes | Indexer-dependent | Yes - WASM is deterministic but no consensus |
| **OPNet** | **Cryptographic consensus** | **No - proof-of-work + attestations enforce agreement** |

**Why this matters**: For applications requiring binding state consistency (like DEXs, escrows, or any multi-party coordination), indexer disagreement is catastrophic. When NativeSwap locks a reservation at a specific price, EVERY node must agree that reservation exists. OPNet's consensus layer guarantees this through cryptographic proofs.

---

## CSV: The Critical Anti-Pinning Mechanism (MANDATORY)

### What is Transaction Pinning?

Transaction pinning is a **catastrophic attack vector** that most Bitcoin protocols ignore. Here's how it works:

1. When you send Bitcoin to someone, they can immediately create a transaction spending that Bitcoin, **even before the first transaction is confirmed**
2. An attacker creates massive chains of unconfirmed transactions, all dependent on each other
3. This makes it **impossible for miners to include your legitimate transaction** in a block
4. Your transaction is stuck in mempool limbo while the attacker manipulates contract state

### Why Pinning Destroys DEXs Without Protection

**Attack scenario on an unprotected DEX:**

1. Attacker pins your swap transaction, preventing confirmation
2. Your reservation expires, but your BTC is stuck in mempool
3. Attacker cancels their sell orders or manipulates pool state
4. When your transaction finally confirms (if ever), no tokens remain
5. **Result**: Attacker gets free money, you lose everything

This vulnerability exists in **every Bitcoin protocol** that doesn't mandate CSV:
- Multisig bridges can be frozen entirely with one malicious unwrap request
- Ordinals marketplaces are vulnerable
- Runes trading platforms are vulnerable
- BRC-20 exchanges are vulnerable

### The CSV Solution

**CSV (CheckSequenceVerify, BIP 112)** completely eliminates pinning attacks:

```
Without CSV: Maximum unconfirmed chain length = UNLIMITED (attackers can pin forever)
With CSV:    Maximum unconfirmed chain length = ZERO (must wait for confirmation)
```

By requiring all seller addresses to have a **1-block CSV timelock**, once Bitcoin arrives at those addresses, it **cannot be spent again for at least one block**. This is mathematically provable and completely closes the attack vector.

### Implementation Requirement

**ALL addresses receiving BTC in OPNet swaps MUST use CSV timelocks.**

This is enforced at the protocol level in NativeSwap. If you're building any application that coordinates BTC transfers with smart contract state, you MUST implement CSV protection.

---

## The Two Address Systems (CRITICAL for Airdrops)

### Why OPNet Airdrops Work Differently Than Ethereum

On **Ethereum**, there's one address format. You can loop through addresses and call `transfer(to, amount)` because ERC20 contracts just decrement sender balance and increment recipient balance using the same address type.

On **OPNet**, contract balances are keyed by **ML-DSA public key hashes** (32-byte quantum-resistant addresses), but users are typically known externally by their **Bitcoin addresses** (Taproot P2TR, tweaked public keys). These are **completely different cryptographic systems** with no inherent link between them.

| Address System | Format | Used For |
|---------------|--------|----------|
| **Bitcoin Address** | Taproot P2TR (`bc1p...`) | External identity, what you have in your airdrop list |
| **OPNet Address** | ML-DSA public key hash (32 bytes) | Contract balances, internal state |

### WHY YOU CANNOT JUST LOOP AND TRANSFER

If you have a list of Bitcoin addresses from token holders or snapshot participants:

```typescript
// WRONG - THIS DOES NOT WORK
for (const btcAddress of airdropList) {
    await token.transfer(btcAddress, amount);  // IMPOSSIBLE
}
```

**The contract literally cannot credit tokens to a Bitcoin address directly.** The contract storage uses ML-DSA addresses, not Bitcoin addresses. The mapping between them only exists once a user explicitly proves ownership of both keys together.

### THE CORRECT SOLUTION: Claim-Based Airdrop Contract

Airdrops on OPNet are done via a **smart contract** with a claim pattern:

**1. Deploy an airdrop contract** that stores allocations keyed by tweaked public key:
```typescript
// Contract storage
mapping(tweakedPubKey => amount)  // Store: which Bitcoin addresses get how much
mapping(tweakedPubKey => claimed) // Track: has this allocation been claimed
```

**2. Users call `claim()`** providing a signature that proves they control that Bitcoin address:
```typescript
// User's frontend (browser) - OP_WALLET signs automatically
const message = `Claim airdrop for ${contractAddress}`;
const signed = await MessageSigner.tweakAndSignMessageAuto(message);

// Submit to contract with signature in calldata
await airdropContract.claim(signature, messageHash);
```

**3. Contract verifies and transfers:**
```typescript
// Contract logic
public claim(calldata: Calldata): BytesWriter {
    const signature = calldata.readBytes(64);
    const messageHash = calldata.readBytes(32);

    // Verify signature proves caller owns the tweaked public key
    if (!Blockchain.verifySignature(Blockchain.tx.origin, signature, messageHash, false)) {
        throw new Revert('Invalid signature');
    }

    // Get allocation for this tweaked public key
    const tweakedKey = Blockchain.tx.origin.tweakedPublicKey;
    const amount = this.allocations.get(tweakedKey);

    // Transfer to caller's ML-DSA address (now linked!)
    this._mint(Blockchain.tx.sender, amount);
    this.claimed.set(tweakedKey, true);
}
```

**This is the "unlock transaction"** - the moment where the user proves ownership of both identities (Bitcoin address AND ML-DSA address), allowing the contract to link them and credit the tokens.

### The Banana Locker Analogy

- You know 300 monkeys by their **face** (Bitcoin address)
- Lockers open with a **secret handshake** (ML-DSA key)
- You label lockers with faces and put bananas inside
- When a monkey shows up, they show face AND do handshake
- System learns: "this face = this handshake" and gives them their banana
- **The banana was always "theirs" but they couldn't access it until they linked face to handshake**

---

## NativeSwap: How to Build a Real DEX on Bitcoin

NativeSwap answers the biggest unanswered question in BitcoinFi: **How do you build an actual AMM that trades native BTC for tokens, trustlessly, without custody?**

### The Fundamental Problem

Traditional AMMs (like Uniswap) hold both assets in a pool and use math to set prices. **Bitcoin cannot do this** - you literally cannot have a smart contract hold and programmatically transfer BTC.

**Why common "solutions" fail:**
- **Multisig wallets**: Trusted parties can collude or disappear
- **Wrapped BTC**: Bridges become honeypots (billions stolen from bridges)
- **Pure order books**: Terrible liquidity without market makers holding inventory

### Virtual Reserves: The Solution

NativeSwap realizes that an AMM doesn't need to physically hold assets - it just needs to **track the economic effect of trades**. This is similar to:
- Banks updating ledger entries without moving physical cash
- Futures markets trading billions in commodities without touching a barrel of oil
- Clearinghouses settling trillions without holding underlying assets

**How it works:**
1. The contract maintains two numbers: `bitcoinReserve` and `tokenReserve`
2. When someone buys tokens with BTC, the system records that bitcoin reserve increased and token reserve decreased
3. The actual BTC goes **directly to sellers**, not to the contract
4. AMM pricing only depends on the **ratio** between reserves
5. The constant product formula (`bitcoinReserve × tokenReserve = k`) works identically whether reserves are physical or virtual

### Two-Phase Commit: Why Reservations Are Necessary

**Problem**: OPNet can revert smart contract execution, but it **cannot reverse Bitcoin transfers**. Once you send BTC, that transfer is governed by Bitcoin's consensus rules, not OPNet's.

**Catastrophic scenario without reservations:**
1. You see token price is 0.01 BTC/token
2. You create a transaction sending 1 BTC to buy 100 tokens
3. During 10-20 minute confirmation time, other trades push price to 0.02 BTC/token
4. On Ethereum, your transaction would revert and return your ETH
5. On Bitcoin, **your BTC transfer already happened** - the contract can't send it back
6. You lose your BTC and get zero tokens

**The reservation system (two-phase commit):**

| Phase | What Happens |
|-------|--------------|
| **Phase 1: Reserve** | Prove you control BTC (UTXOs as inputs, sent back to yourself), pay small fee, **price is locked in consensus state** |
| **Phase 2: Execute** | Send exact BTC amount to providers (up to 200 addresses atomically), guaranteed execution at locked price |

**Benefits:**
- **No slippage risk**: Price locked at reservation time
- **No front-running**: Once price is locked in OPNet state, no one can change it
- **Partial fills**: Automatically coordinate payments to up to 200 providers in single atomic transaction (impossible on any other Bitcoin protocol)

### Queue Impact: Accounting for Pending Sells

Sellers queue tokens at the prevailing AMM price. The Queue Impact mechanism adjusts effective token reserve using **logarithmic scaling**:

**Why logarithmic?**
- Markets process information multiplicatively
- Doubling queue from 100→200 tokens has same psychological impact as 1000→2000
- First sellers signal strong selling pressure; additional sellers have diminishing marginal impact
- Matches empirical observations from market microstructure research

### Slashing: Making Queue Manipulation Economically Irrational

Without penalties, Queue Impact would be worthless:
1. Attacker adds massive fake sell orders → crashes price via Queue Impact
2. Attacker buys cheap tokens
3. Attacker cancels their sells
4. Profit from manipulation

**The slashing mechanism:**
- **Immediate cancellation**: 50% penalty (exceeds any realistic manipulation profit)
- **Extended squatting**: Escalates to 90% penalty
- **Slashed tokens return to pool**: Attempted attacks actually improve liquidity

This makes manipulation economically irrational and ensures queue depth is a reliable market signal.

### Summary: Why Each Component Is Necessary

| Component | Constraint It Addresses |
|-----------|------------------------|
| Virtual reserves | Smart contracts can't custody BTC on Bitcoin |
| Reservations (two-phase commit) | OPNet controls contract state, not Bitcoin transfers |
| Queue Impact | Pending orders affect market psychology and pricing |
| Slashing | Queue Impact would be manipulable without penalties |
| CSV timelocks | UTXO chains are vulnerable to transaction pinning |
| OPNet consensus | Indexers can't provide binding state consistency |

**Remove any component and the system either becomes exploitable or stops functioning as an AMM.**

---

## ENFORCEMENT RULES (NON-NEGOTIABLE)

### Before Writing ANY Code

**YOU MUST:**

1. **READ `docs/core-typescript-law-CompleteLaw.md` COMPLETELY** - These are strict TypeScript rules
2. **VERIFY project configuration matches standards** in `docs/` config files

### Configuration Files (in `docs/`)

| File | Purpose |
|------|---------|
| `eslint-contract.json` | ESLint for AssemblyScript contracts |
| `eslint-generic.json` | ESLint for TypeScript libraries |
| `eslint-react.json` | ESLint for React/Next.js frontends |
| `tsconfig-generic.json` | TypeScript config (NOT for contracts) |
| `asconfig.json` | AssemblyScript compiler config |

### TypeScript is MANDATORY

**JavaScript is NOT allowed. All code MUST be TypeScript.**

- ❌ No `.js` files (except config files like `eslint.config.js`)
- ❌ No `// @ts-check` in JS files - use real TypeScript
- ❌ No `allowJs: true` in tsconfig
- ✅ All source files must be `.ts` or `.tsx`
- ✅ Strict mode enabled in tsconfig
- ✅ All types explicitly defined

---

### Full Project Setup is MANDATORY

**Before writing ANY code, the project MUST have:**

```
project/
├── package.json          # With correct OPNet package versions
├── tsconfig.json         # Matching docs/tsconfig-generic.json
├── eslint.config.js      # Using appropriate config from docs/
├── .prettierrc           # Prettier configuration
├── .prettierignore       # Prettier ignore file
├── src/                  # Source code directory
│   └── index.ts          # Entry point
└── tests/                # Test directory (if applicable)
    └── *.test.ts
```

### Prettier Configuration (MANDATORY)

**.prettierrc:**
```json
{
    "semi": true,
    "singleQuote": true,
    "tabWidth": 4,
    "trailingComma": "all",
    "printWidth": 100,
    "bracketSpacing": true,
    "arrowParens": "always"
}
```

**.prettierignore:**
```
node_modules/
build/
dist/
*.wasm
coverage/
```

**Package.json scripts (add these):**
```json
{
    "scripts": {
        "format": "prettier --write \"src/**/*.{ts,tsx}\"",
        "format:check": "prettier --check \"src/**/*.{ts,tsx}\""
    }
}
```

**Run Prettier before committing:**
```bash
npm run format
```

**For Frontend (React/Vite), also include:**
```
├── vite.config.ts        # Vite configuration
├── index.html            # Entry HTML
└── src/
    ├── App.tsx
    ├── main.tsx
    └── styles/           # CSS files (NO inline CSS)
        └── variables.css
```

**For Contracts (AssemblyScript), also include:**
```
├── asconfig.json         # AssemblyScript config
└── assembly/
    ├── index.ts          # Contract entry point
    └── contracts/
        └── MyContract.ts
```

**You MUST create these files BEFORE writing application code.**

---

### Configuration Verification Checklist

- [ ] `package.json` exists with correct OPNet package versions
- [ ] `tsconfig.json` matches `docs/tsconfig-generic.json` (or strict ESNext for contracts)
- [ ] `eslint.config.js` uses appropriate config from `docs/`
- [ ] `.prettierrc` exists with correct configuration
- [ ] **NO `any` type anywhere** - This is FORBIDDEN
- [ ] **NO inline CSS** - Use CSS modules, Tailwind, or external stylesheets
- [ ] **NO JavaScript files** - TypeScript only
- [ ] Code is formatted with Prettier (`npm run format`)
- [ ] ESNext compliant
- [ ] Unit tests exist and pass

### IF ANY CHECK FAILS → REFUSE TO CODE UNTIL FIXED

Misconfigured projects lead to **exploits and critical vulnerabilities**.

---

## TypeScript Law (CRITICAL)

From `docs/core-typescript-law-CompleteLaw.md`:

### FORBIDDEN Constructs

| Construct | Why Forbidden |
|-----------|---------------|
| `any` | Runtime bug waiting to happen. No exceptions. |
| `unknown` | Only at system boundaries (JSON parsing, external APIs) |
| `object` (lowercase) | Use specific interfaces or `Record<string, T>` |
| `Function` (uppercase) | Use specific signatures |
| `{}` | Means "any non-nullish value". Use `Record<string, never>` |
| Non-null assertion (the ! operator) | Use explicit null checks or optional chaining |
| Dead/duplicate code | Design is broken if present |
| ESLint bypasses | Never |
| Section separator comments | See below |
| **Inline CSS** | Use CSS modules, styled-components, or external stylesheets. No `style={{ }}` props. |

### FORBIDDEN: Section Separator Comments

**NEVER** write comments like:

```typescript
// ==================== PRIVATE METHODS ====================
// ---------------------- HELPERS ----------------------
// ************* CONSTANTS *************
// ####### INITIALIZATION #######
```

These are **lazy, unprofessional, and useless**. They add noise without value.

**INSTEAD**: Use proper TSDoc for EVERY class, method, property, and function:

```typescript
/**
 * Transfers tokens from sender to recipient.
 *
 * @param to - The recipient address
 * @param amount - The amount to transfer in base units
 * @returns True if transfer succeeded
 * @throws {InsufficientBalanceError} If sender has insufficient balance
 * @throws {InvalidAddressError} If recipient address is invalid
 *
 * @example
 * ```typescript
 * const success = await token.transfer(recipientAddress, 1000n);
 * ```
 */
public async transfer(to: Address, amount: bigint): Promise<boolean> {
    // ...
}
```

**TSDoc Requirements:**

- `@param` for every parameter
- `@returns` for non-void returns
- `@throws` for possible exceptions
- `@example` for non-trivial methods
- Description of what the method does, not how

**Code organization comes from proper class design, not ASCII art.**

### Numeric Types

- **`number`**: Array lengths, loop counters, small flags, ports, pixels
- **`bigint`**: Satoshi amounts, block heights, timestamps, database IDs, file sizes, cumulative totals
- **Floats for financial values**: **FORBIDDEN** - Use fixed-point `bigint` with explicit scale

### Common API Pitfalls

**`Address.fromString()` requires TWO parameters:**

```typescript
// WRONG - will fail
const addr = Address.fromString(addressString);

// CORRECT - always provide both params
const addr = Address.fromString(mldsaPublicKey, tweakedPublicKey);
```

The first parameter is the ML-DSA public key (quantum-resistant), the second is the tweaked public key (legacy Bitcoin). Always provide both.

### Required tsconfig.json Settings

```json
{
    "compilerOptions": {
        "strict": true,
        "noImplicitAny": true,
        "strictNullChecks": true,
        "noUnusedLocals": true,
        "noUnusedParameters": true,
        "exactOptionalPropertyTypes": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true,
        "noUncheckedIndexedAccess": true,
        "noImplicitOverride": true,
        "moduleResolution": "bundler",
        "module": "ESNext",
        "target": "ESNext",
        "lib": ["ESNext"],
        "isolatedModules": true,
        "verbatimModuleSyntax": true
    }
}
```

---

## Performance Rules

### THREADING IS MANDATORY

- **Sequential processing = unacceptable performance**
- Use Worker threads for CPU-bound work
- Use async with proper concurrency for I/O
- Batch operations where possible
- Use connection pooling

### Caching (ALWAYS)

- **Reuse contract instances** - Never create new instances for same contract
- **Reuse providers** - Single provider instance per network
- **Cache locally** - Browser localStorage/IndexedDB for user data
- **Cache on API** - Server-side caching for blockchain state
- **Invalidate on block change** - Clear stale data when new block confirmed

### RPC Call Optimization

**Use `.metadata()` instead of multiple calls:**

```typescript
// ❌ BAD - 4 RPC calls (slow)
const [name, symbol, decimals, totalSupply] = await Promise.all([
    contract.name(),
    contract.symbol(),
    contract.decimals(),
    contract.totalSupply()
]);

// ✅ GOOD - 1 RPC call (fast)
const { name, symbol, decimals, totalSupply } = (await contract.metadata()).decoded;
```

**`.metadata()` returns name, symbol, decimals, totalSupply, owner, and more in ONE call.**

### Backend/API Frameworks

**MANDATORY**: Use OPNet's high-performance libraries:

| Package | Purpose |
|---------|---------|
| `@btc-vision/uwebsocket.js` | WebSocket server (fastest) |
| `@btc-vision/hyper-express` | HTTP server (fastest) |

**FORBIDDEN**: Express, Fastify, Koa, Hapi, or any other HTTP framework. They are significantly slower.

```typescript
// CORRECT - Use hyper-express with threading
import HyperExpress from '@btc-vision/hyper-express';
import { Worker } from 'worker_threads';

const app = new HyperExpress.Server();
// Use classes, not functions
// Delegate CPU work to workers
```

---

## Contract Gas Optimization (CRITICAL)

### FORBIDDEN Patterns in Contracts

| Pattern | Why Forbidden | Alternative |
|---------|---------------|-------------|
| `while` loops | Unbounded gas consumption | Use bounded `for` loops |
| Infinite loops | Contract halts, wastes gas | Always have exit condition |
| Iterating all map keys | O(n) grows exponentially | Use indexed lookups, pagination |
| Iterating all array elements | O(n) cost explosion | Store aggregates, use pagination |
| Unbounded arrays | Grows forever | Cap size, use cleanup |

### Gas-Efficient Patterns

```typescript
// WRONG - Iterating all holders (O(n) disaster)
let total: u256 = u256.Zero;
for (let i = 0; i < holders.length; i++) {
    total = SafeMath.add(total, balances.get(holders[i]));
}

// CORRECT - Store running total
const totalSupply: StoredU256 = new StoredU256(TOTAL_SUPPLY_POINTER);
// Update on mint/burn, read in O(1)
```

---

## Security Audit Checklist

### All Code Must Be Checked For:

#### Cryptographic

- [ ] Key generation entropy
- [ ] Nonce reuse
- [ ] Signature malleability
- [ ] Timing attacks
- [ ] Replay attacks

#### Smart Contract

- [ ] Reentrancy
- [ ] Integer overflow/underflow
- [ ] Access control bypass
- [ ] Authorization flaws
- [ ] State manipulation
- [ ] Race conditions

#### Bitcoin-specific

- [ ] Transaction malleability
- [ ] UTXO selection vulnerabilities
- [ ] Fee sniping
- [ ] Dust attacks
- [ ] **Transaction pinning attacks** - MUST use CSV timelocks
- [ ] **Unconfirmed transaction chains** - Verify CSV enforcement

#### DEX/Swap-specific

- [ ] Front-running / MEV attacks
- [ ] Price manipulation via queue flooding
- [ ] Reservation expiry edge cases
- [ ] Partial fill coordination
- [ ] Slashing mechanism bypass attempts

---

## Quick Start

| Task | Template |
|------|----------|
| New OP20 token | `templates/contracts/OP20Token.ts` |
| New OP721 NFT | `templates/contracts/OP721NFT.ts` |
| Generic contract | `templates/contracts/MyContract.ts` |
| Contract tests | `templates/tests/` |
| Frontend dApp | `templates/frontend/` |
| Node plugin (indexer) | `templates/plugins/OP20Indexer.ts` |
| Node plugin (generic) | `templates/plugins/MyPlugin.ts` |

---

## Complete File Index

### Configuration Files (`docs/`)

| File | Description |
|------|-------------|
| `docs/asconfig.json` | AssemblyScript compiler config |
| `docs/eslint-contract.json` | ESLint for AssemblyScript contracts |
| `docs/eslint-generic.json` | ESLint for TypeScript libraries |
| `docs/eslint-react.json` | ESLint for React frontends |
| `docs/tsconfig-generic.json` | TypeScript config (not contracts) |
| `docs/setup-README.md` | Setup instructions |

### TypeScript Law

| File | Description |
|------|-------------|
| `docs/core-typescript-law-readme.md` | Overview |
| `docs/core-typescript-law-CompleteLaw.md` | **COMPLETE RULES - READ FIRST** |

### OPNet Client Library

| File | Description |
|------|-------------|
| `docs/core-opnet-README.md` | Library overview |
| `docs/core-opnet-backend-api.md` | Backend API with hyper-express |
| `docs/core-opnet-getting-started-installation.md` | Installation |
| `docs/core-opnet-getting-started-overview.md` | Architecture overview |
| `docs/core-opnet-getting-started-quick-start.md` | Quick start guide |
| `docs/core-opnet-providers-json-rpc-provider.md` | JSON-RPC provider |
| `docs/core-opnet-providers-websocket-provider.md` | WebSocket provider |
| `docs/core-opnet-providers-understanding-providers.md` | Provider concepts |
| `docs/core-opnet-providers-advanced-configuration.md` | Advanced config |
| `docs/core-opnet-providers-internal-caching.md` | Caching system |
| `docs/core-opnet-providers-threaded-http.md` | Threading |
| `docs/core-opnet-contracts-overview.md` | Contract interaction overview |
| `docs/core-opnet-contracts-instantiating-contracts.md` | Creating contract instances |
| `docs/core-opnet-contracts-simulating-calls.md` | Simulating calls |
| `docs/core-opnet-contracts-sending-transactions.md` | Sending transactions |
| `docs/core-opnet-contracts-gas-estimation.md` | Gas estimation |
| `docs/core-opnet-contracts-offline-signing.md` | Offline signing |
| `docs/core-opnet-contracts-transaction-configuration.md` | TX config |
| `docs/core-opnet-contracts-contract-code.md` | Contract code retrieval |
| `docs/core-opnet-abi-reference-abi-overview.md` | ABI overview |
| `docs/core-opnet-abi-reference-data-types.md` | ABI data types |
| `docs/core-opnet-abi-reference-op20-abi.md` | OP20 ABI |
| `docs/core-opnet-abi-reference-op20s-abi.md` | OP20S ABI (signatures) |
| `docs/core-opnet-abi-reference-op721-abi.md` | OP721 ABI |
| `docs/core-opnet-abi-reference-motoswap-abis.md` | MotoSwap ABIs |
| `docs/core-opnet-abi-reference-factory-abis.md` | Factory ABIs |
| `docs/core-opnet-abi-reference-stablecoin-abis.md` | Stablecoin ABIs |
| `docs/core-opnet-abi-reference-custom-abis.md` | Custom ABI creation |
| `docs/core-opnet-api-reference-provider-api.md` | Provider API |
| `docs/core-opnet-api-reference-contract-api.md` | Contract API |
| `docs/core-opnet-api-reference-epoch-api.md` | Epoch API |
| `docs/core-opnet-api-reference-utxo-manager-api.md` | UTXO Manager API |
| `docs/core-opnet-api-reference-types-interfaces.md` | Types & interfaces |
| `docs/core-opnet-bitcoin-utxos.md` | UTXO handling |
| `docs/core-opnet-bitcoin-utxo-optimization.md` | UTXO optimization |
| `docs/core-opnet-bitcoin-balances.md` | Balance queries |
| `docs/core-opnet-bitcoin-sending-bitcoin.md` | Sending BTC |
| `docs/core-opnet-blocks-block-operations.md` | Block operations |
| `docs/core-opnet-blocks-block-witnesses.md` | Block witnesses |
| `docs/core-opnet-blocks-gas-parameters.md` | Gas parameters |
| `docs/core-opnet-blocks-reorg-detection.md` | Reorg detection |
| `docs/core-opnet-epochs-overview.md` | Epochs overview |
| `docs/core-opnet-epochs-epoch-operations.md` | Epoch operations |
| `docs/core-opnet-epochs-mining-template.md` | Mining template |
| `docs/core-opnet-epochs-submitting-epochs.md` | Submitting epochs |
| `docs/core-opnet-transactions-broadcasting.md` | Broadcasting TXs |
| `docs/core-opnet-transactions-fetching-transactions.md` | Fetching TXs |
| `docs/core-opnet-transactions-transaction-receipts.md` | TX receipts |
| `docs/core-opnet-transactions-challenges.md` | TX challenges |
| `docs/core-opnet-storage-storage-operations.md` | Storage operations |
| `docs/core-opnet-public-keys-public-key-operations.md` | Public key ops |
| `docs/core-opnet-utils-bitcoin-utils.md` | Bitcoin utilities |
| `docs/core-opnet-utils-binary-serialization.md` | Binary serialization |
| `docs/core-opnet-utils-revert-decoder.md` | Revert decoder |
| `docs/core-opnet-examples-op20-examples.md` | OP20 examples |
| `docs/core-opnet-examples-op721-examples.md` | OP721 examples |
| `docs/core-opnet-examples-deployment-examples.md` | Deployment examples |
| `docs/core-opnet-examples-advanced-swaps.md` | Swap examples |

### Transaction Library

| File | Description |
|------|-------------|
| `docs/core-transaction-README.md` | Library overview |
| `docs/core-transaction-transaction-building.md` | Building transactions |
| `docs/core-transaction-offline-transaction-signing.md` | Offline signing |
| `docs/core-transaction-addresses-P2OP.md` | P2OP address format |
| `docs/core-transaction-quantum-support-README.md` | Quantum overview |
| `docs/core-transaction-quantum-support-01-introduction.md` | Quantum intro |
| `docs/core-transaction-quantum-support-02-mnemonic-and-wallet.md` | Quantum wallet |
| `docs/core-transaction-quantum-support-03-address-generation.md` | Quantum addresses |
| `docs/core-transaction-quantum-support-04-message-signing.md` | Quantum signing |
| `docs/core-transaction-quantum-support-05-address-verification.md` | Quantum verification |

### Address Systems & Airdrops (CRITICAL)

| File | Description |
|------|-------------|
| `docs/core-opnet-address-systems-airdrop-pattern.md` | **Two address systems, airdrop pattern (MUST READ)** |

### OIP Specifications

| File | Description |
|------|-------------|
| `docs/core-OIP-README.md` | OIP overview |
| `docs/core-OIP-OIP-0001.md` | OIP process |
| `docs/core-OIP-OIP-0002.md` | Contract standards |
| `docs/core-OIP-OIP-0003.md` | **Plugin system spec** |
| `docs/core-OIP-OIP-0004.md` | Epoch system |
| `docs/core-OIP-OIP-0020.md` | OP20 token standard |
| `docs/core-OIP-OIP-0721.md` | OP721 NFT standard |

### Contract Runtime (btc-runtime)

| File | Description |
|------|-------------|
| `docs/contracts-btc-runtime-README.md` | Runtime overview |
| `docs/contracts-btc-runtime-gas-optimization.md` | **Gas optimization (CRITICAL)** |
| `docs/contracts-btc-runtime-getting-started-installation.md` | Installation |
| `docs/contracts-btc-runtime-getting-started-first-contract.md` | First contract |
| `docs/contracts-btc-runtime-getting-started-project-structure.md` | Project structure |
| `docs/contracts-btc-runtime-core-concepts-blockchain-environment.md` | Blockchain env |
| `docs/contracts-btc-runtime-core-concepts-storage-system.md` | Storage system |
| `docs/contracts-btc-runtime-core-concepts-pointers.md` | Storage pointers |
| `docs/contracts-btc-runtime-core-concepts-events.md` | Events |
| `docs/contracts-btc-runtime-core-concepts-decorators.md` | Decorators |
| `docs/contracts-btc-runtime-core-concepts-security.md` | Security |
| `docs/contracts-btc-runtime-api-reference-blockchain.md` | Blockchain API |
| `docs/contracts-btc-runtime-api-reference-storage.md` | Storage API |
| `docs/contracts-btc-runtime-api-reference-events.md` | Events API |
| `docs/contracts-btc-runtime-api-reference-op20.md` | OP20 API |
| `docs/contracts-btc-runtime-api-reference-op721.md` | OP721 API |
| `docs/contracts-btc-runtime-api-reference-safe-math.md` | SafeMath API |
| `docs/contracts-btc-runtime-contracts-op-net-base.md` | OP_NET base class |
| `docs/contracts-btc-runtime-contracts-op20-token.md` | OP20 implementation |
| `docs/contracts-btc-runtime-contracts-op20s-signatures.md` | OP20S signatures |
| `docs/contracts-btc-runtime-contracts-op721-nft.md` | OP721 implementation |
| `docs/contracts-btc-runtime-contracts-reentrancy-guard.md` | Reentrancy guard |
| `docs/contracts-btc-runtime-contracts-upgradeable.md` | Upgradeable contracts |
| `docs/contracts-btc-runtime-storage-stored-primitives.md` | Stored primitives |
| `docs/contracts-btc-runtime-storage-stored-maps.md` | Stored maps |
| `docs/contracts-btc-runtime-storage-stored-arrays.md` | Stored arrays |
| `docs/contracts-btc-runtime-storage-memory-maps.md` | Memory maps |
| `docs/contracts-btc-runtime-types-address.md` | Address type |
| `docs/contracts-btc-runtime-types-calldata.md` | Calldata type |
| `docs/contracts-btc-runtime-types-bytes-writer-reader.md` | BytesWriter/Reader |
| `docs/contracts-btc-runtime-types-safe-math.md` | SafeMath type |
| `docs/contracts-btc-runtime-advanced-cross-contract-calls.md` | Cross-contract calls |
| `docs/contracts-btc-runtime-advanced-signature-verification.md` | Signature verification |
| `docs/contracts-btc-runtime-advanced-quantum-resistance.md` | Quantum resistance |
| `docs/contracts-btc-runtime-advanced-bitcoin-scripts.md` | Bitcoin scripts |
| `docs/contracts-btc-runtime-advanced-contract-upgrades.md` | Contract upgrades |
| `docs/contracts-btc-runtime-advanced-plugins.md` | Contract plugins |
| `docs/contracts-btc-runtime-examples-basic-token.md` | Basic token example |
| `docs/contracts-btc-runtime-examples-stablecoin.md` | Stablecoin example |
| `docs/contracts-btc-runtime-examples-nft-with-reservations.md` | NFT example |
| `docs/contracts-btc-runtime-examples-oracle-integration.md` | Oracle example |

### Other Contract Docs

| File | Description |
|------|-------------|
| `docs/contracts-as-bignum-README.md` | BigNum library (u256, u128) |
| `docs/contracts-opnet-transform-README.md` | Transform decorators |
| `docs/contracts-opnet-transform-std-README.md` | Standard library |
| `docs/contracts-example-tokens-README.md` | Example tokens |
| `docs/contracts-example-tokens-docs-OP_20.md` | OP20 example |

### Client Libraries

| File | Description |
|------|-------------|
| `docs/clients-bitcoin-README.md` | Bitcoin library overview |
| `docs/clients-bitcoin-psbt.md` | PSBT class, signing, finalization |
| `docs/clients-bitcoin-payments.md` | Payment types (P2TR, P2WPKH, P2WSH, P2SH, P2OP) |
| `docs/clients-bitcoin-script.md` | Script building, opcodes |
| `docs/clients-bitcoin-address.md` | Address encoding/decoding |
| `docs/clients-bitcoin-transaction.md` | Transaction class |
| `docs/clients-bip32-README.md` | BIP32 HD derivation |
| `docs/clients-bip32-QUANTUM.md` | Quantum support |
| `docs/clients-ecpair-README.md` | EC key pairs |
| `docs/clients-walletconnect-README.md` | WalletConnect |
| `docs/clients-walletconnect-wallet-integration.md` | Wallet integration |

### Testing

| File | Description |
|------|-------------|
| `docs/testing-unit-test-framework-README.md` | Test framework |
| `docs/testing-opnet-unit-test-README.md` | Unit testing |
| `docs/testing-opnet-unit-test-docs-README.md` | Test docs |
| `docs/testing-opnet-unit-test-docs-Blockchain.md` | Blockchain mocking |
| `docs/testing-opnet-unit-test-docs-ContractRuntime.md` | Contract runtime |

### Frontend

| File | Description |
|------|-------------|
| `docs/frontend-motoswap-ui-README.md` | **Frontend guide (THE STANDARD)** |

### Plugins

| File | Description |
|------|-------------|
| `docs/plugins-plugin-sdk-README.md` | Plugin SDK |
| `docs/plugins-opnet-node-README.md` | OPNet node |
| `docs/plugins-opnet-node-docker-README.md` | Docker setup |

### Templates

#### Contract Templates (`templates/contracts/`)

| File | Description |
|------|-------------|
| `templates/contracts/OP20Token.ts` | OP20 token implementation |
| `templates/contracts/OP721NFT.ts` | OP721 NFT implementation |
| `templates/contracts/MyContract.ts` | Generic contract template |
| `templates/contracts/index.ts` | Entry point / exports |

#### Frontend Templates (`templates/frontend/`)

| File | Description |
|------|-------------|
| `templates/frontend/App.tsx` | Main app component |
| `templates/frontend/OPNetProvider.tsx` | OPNet context provider |
| `templates/frontend/WalletConnect.tsx` | Wallet connection component |
| `templates/frontend/ContractInteraction.tsx` | Contract interaction component |
| `templates/frontend/useWallet.ts` | Wallet hook |
| `templates/frontend/useContract.ts` | Contract hook |
| `templates/frontend/vite.config.ts` | Vite configuration |
| `templates/frontend/package.json` | Package dependencies |

#### Plugin Templates (`templates/plugins/`)

| File | Description |
|------|-------------|
| `templates/plugins/MyPlugin.ts` | Generic plugin template |
| `templates/plugins/OP20Indexer.ts` | OP20 indexer plugin |
| `templates/plugins/types.ts` | Type definitions |
| `templates/plugins/index.ts` | Entry point |
| `templates/plugins/plugin.json` | Plugin manifest |

#### Test Templates (`templates/tests/`)

| File | Description |
|------|-------------|
| `templates/tests/OP20.test.ts` | OP20 test example |
| `templates/tests/setup.ts` | Test setup |
| `templates/tests/gulpfile.js` | Gulp build config |

---

## Contract Development

### Key Concepts

1. **Contracts use AssemblyScript** - Compiles to WebAssembly
2. **Constructor runs on EVERY interaction** - Use `onDeployment()` for initialization
3. **Contracts CANNOT hold BTC** - They are calculators, not custodians
4. **Verify-don't-custody pattern** - Check `Blockchain.tx.outputs` against internal state

### Decorator Reference

```typescript
// Mark method as callable
@method({ name: 'param1', type: ABIDataTypes.UINT256 })

// Specify return types
@returns({ name: 'result', type: ABIDataTypes.UINT256 })

// Declare emitted events
@emit('Transfer', 'Approval')
```

### Storage Types

| Type | Use Case |
|------|----------|
| `StoredU256` | Single u256 value |
| `StoredBoolean` | Boolean flag |
| `StoredString` | String value |
| `StoredMapU256` | Key-value map (u256 keys/values) |
| `AddressMemoryMap` | In-memory address map |

---

## Testing

### ALL CODE MUST HAVE TESTS

```typescript
import { opnet, OPNetUnit, Assert, Blockchain } from '@btc-vision/unit-test-framework';

await opnet('My Tests', async (vm: OPNetUnit) => {
    vm.beforeEach(async () => {
        Blockchain.dispose();
        await Blockchain.init();
    });

    await vm.it('should work correctly', async () => {
        const result = await contract.someMethod();
        Assert.expect(result).toEqual(expected);
    });
});
```

---

## Plugin Development

**OPNet nodes are like Minecraft servers - they support plugins!**

### Key Resources

- Read `docs/plugins-plugin-sdk-README.md`
- Read `docs/core-OIP-OIP-0003.md` for plugin specification
- Use `templates/plugins/OP20Indexer.ts` for indexers

### Plugin Lifecycle

| Hook | When Called | Blocking |
|------|-------------|----------|
| `onFirstInstall` | First installation | Yes |
| `onNetworkInit` | Every load | Yes |
| `onBlockChange` | New block confirmed | No |
| `onReorg` | Chain reorganization | Yes (CRITICAL) |

### Critical: Reorg Handling

You **MUST** implement `onReorg()` to revert state for reorged blocks. Failure to do so will cause data inconsistency.

---

## Frontend Development

### Configuration Standard

Frontend configs **MUST** use `docs/eslint-react.json` and `docs/tsconfig-generic.json`:

- Vite + React
- Vitest for testing
- ESLint with TypeScript strict mode
- ESNext target

### Caching (MANDATORY)

- **Reuse provider instances** - Singleton per network
- **Reuse contract instances** - Cache by address
- **Cache API responses** - Invalidate on block change

### Key Hooks

```typescript
// OPNet provider
const { provider, isConnected, network } = useOPNet();

// Contract interaction
const { contract, callMethod, loading } = useContract(address, abi);

// Wallet connection
const { address, connect, disconnect, signPsbt } = useWallet();
```

See `docs/frontend-motoswap-ui-README.md` for complete integration guide.

---

## Backend/API Development

### MANDATORY Frameworks

| Package | Purpose |
|---------|---------|
| `@btc-vision/hyper-express` | HTTP server (fastest) |
| `@btc-vision/uwebsocket.js` | WebSocket server (fastest) |

**FORBIDDEN**: Express, Fastify, Koa, Hapi - they are significantly slower.

See `docs/core-opnet-backend-api.md` for complete guide.

---

## Official Wallet: OP_WALLET

**OP_WALLET is the main and official wallet supporting OPNet.** It is developed by the OPNet team and provides the most complete feature set for interacting with the OPNet Bitcoin L1 smart contract ecosystem.

### Why OP_WALLET is Required for Full OPNet Support

| Feature | OP_WALLET | Other Wallets |
|---------|-----------|---------------|
| **Official Support** | Yes | No |
| **MLDSA Signatures** | Yes | No |
| **Quantum-Resistant Keys** | Yes | No |
| **Full OPNet Integration** | Yes | Partial |
| **First-Party Updates** | Yes | No |

### Key Capabilities

1. **MLDSA (ML-DSA) Signatures**: Only OP_WALLET supports quantum-resistant ML-DSA signatures, which are critical for future-proof security on OPNet
2. **Full Address System Support**: OP_WALLET properly handles both Bitcoin addresses (tweaked public keys) and OPNet addresses (ML-DSA public key hashes)
3. **Native OPNet Features**: Direct access to all OPNet features as they are released
4. **Optimized UX**: Built specifically for OPNet dApp interactions

### Integration via WalletConnect

Use `@btc-vision/walletconnect` to integrate OP_WALLET into your dApp:

```typescript
import { WalletConnectProvider, useWalletConnect, SupportedWallets } from '@btc-vision/walletconnect';

// Wrap your app
<WalletConnectProvider theme="dark">
  <App />
</WalletConnectProvider>

// In your component
const { connectToWallet, mldsaPublicKey, signMLDSAMessage } = useWalletConnect();

// Connect specifically to OP_WALLET for full feature support
connectToWallet(SupportedWallets.OP_WALLET);

// Use MLDSA signatures (OP_WALLET only)
if (mldsaPublicKey) {
  const signature = await signMLDSAMessage('Your message');
}
```

### Installation

Install OP_WALLET from the [Chrome Web Store](https://chromewebstore.google.com/search/OP_WALLET)

---

## Client Libraries

| Package | Doc | Description |
|---------|-----|-------------|
| `@btc-vision/bitcoin` | `docs/clients-bitcoin-README.md` | Bitcoin lib (709x faster PSBT) |
| `@btc-vision/bip32` | `docs/clients-bip32-README.md` | HD derivation + quantum |
| `@btc-vision/ecpair` | `docs/clients-ecpair-README.md` | EC key pairs |
| `@btc-vision/transaction` | `docs/core-transaction-README.md` | OPNet transactions |
| `opnet` | `docs/core-opnet-README.md` | Main client library |
| `@btc-vision/walletconnect` | `docs/clients-walletconnect-README.md` | Wallet connection (OP_WALLET + UniSat) |

---

## Version Requirements

| Tool | Minimum Version |
|------|-----------------|
| Node.js | >= 24.0.0 |
| TypeScript | >= 5.9.3 |
| AssemblyScript | >= 0.28.9 |

---

## Critical Reminders

1. **READ typescript-law FIRST** - Non-negotiable rules
2. **Verify project configuration** - Before writing any code
3. **NO `any` type** - Ever
4. **Test everything** - Unit tests required
5. **Handle
