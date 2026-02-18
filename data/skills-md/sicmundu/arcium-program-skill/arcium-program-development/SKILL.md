---
name: arcium-program-development
description: Build, refactor, and debug Arcium MXE program code across Arcis circuits (`encrypted-ixs`) and Anchor programs (`programs/*`). Use when implementing confidential instructions, wiring `init_comp_def`/`queue_computation`/callbacks, deriving Arcium PDAs and callback accounts, handling encrypted I/O and offsets, parsing generated callback output structs, building permission-gated flows, integrating offchain circuit sources, testing with `@arcium-hq/client`, deploying MXEs, or migrating Arcium versions.
---

# Arcium Program Development

Use this skill to implement and debug Arcium computations end-to-end with strict contracts across Arcis circuits, Anchor program wiring, callback verification, and client/test encryption flow.

## Decision Tree (Task Classification)

Classify the request before editing code:

1. **Stateless computation** (e.g., Coinflip)
- No persistent encrypted state account update.
- Usually one encrypted input and one revealed/encrypted output.
- Read first: `references/implementation-playbook.md`, `references/callback-output-shapes.md`.

2. **Stateful encrypted account flow** (e.g., Voting, Sealed Bid, Blackjack)
- Requires `.account(pubkey, offset, len)` with exact byte layout.
- Usually callback writes ciphertext + nonce to account state.
- Read first: `references/account-layout-offsets.md`, `references/implementation-playbook.md`.

3. **Permission-gated flow** (e.g., Encrypted DNA matching)
- Constraints and status transitions determine whether queueing is allowed.
- Read first: `references/permission-and-state-machines.md`, `references/examples-patterns.md`.

4. **Offchain circuit source flow**
- `init_comp_def` uses `CircuitSource::OffChain` and `circuit_hash!`.
- Read first: `references/docs-and-migrations.md`, `references/troubleshooting-matrix.md`.

5. **Migration or compatibility update**
- Update Rust/TypeScript dependencies and API call signatures first.
- Read first: `references/docs-and-migrations.md`, `references/anti-patterns.md`.

6. **Debugging request**
- Triaged by stage: encryption -> queue -> callback verify -> finalization.
- Read first: `references/troubleshooting-matrix.md`, `references/test-client-patterns.md`.

## Mandatory Build Contract

Keep these invariants aligned in every implementation:

1. Circuit function name (`#[instruction]`) must match `comp_def_offset("...")` identifier.
2. Program callback macro must match instruction name:
- `#[arcium_callback(encrypted_ix = "<ix_name>")]`
3. Callback output type must match generated type:
- `SignedComputationOutputs<<IxName>Output>`
4. Queue and callback contexts must reference the same comp-def account and cluster derivation.
5. Every callback must call `verify_output(&cluster_account, &computation_account)` before consuming output.
6. `init_*_comp_def` must exist for every queued encrypted instruction.

## ArgBuilder Contract (Strict Ordering)

### `Enc<Shared, T>` input contract

Order is strict and must be preserved:
1. `x25519_pubkey(<client_pubkey>)`
2. `plaintext_u128(<nonce>)`
3. encrypted fields in exact circuit argument order (`encrypted_u8/u16/u32/u64/u128/bool/...`)

### `Enc<Mxe, T>` input contract

Order is strict and must be preserved:
1. `plaintext_u128(<mxe_nonce>)`
2. encrypted fields in exact circuit argument order

### Account-backed encrypted state contract

Use:
- `.account(<state_account>, <byte_offset>, <byte_len>)`

Rules:
1. Offset must start after Anchor discriminator (`8`) plus preceding fixed fields.
2. Length must match ciphertext field count times `32` bytes (or packed struct contract).
3. Add inline comments documenting offset derivation.

See detailed formulas and examples in `references/account-layout-offsets.md`.

## Callback Output Parsing Contract

Two common shapes are generated:

1. **Simple shape**
```rust
Ok(MyIxOutput { field_0 }) => field_0
```
Used for single output structs/values.

2. **Nested shape**
```rust
Ok(MyIxOutput {
    field_0: MyIxOutputStruct0 {
        field_0: a,
        field_1: b,
        field_2: c,
    },
}) => (a, b, c)
```
Used when return type is a tuple or multi-field struct.

Mandatory checks:
1. Verify output before parsing.
2. Check ciphertext cardinality when business logic expects exact count.
3. Persist/emit only after successful verification and shape checks.

See `references/callback-output-shapes.md`.

## Account Offset Contract

Use this formula for encrypted payload start:

```text
offset = 8 (Anchor discriminator) + sum(size of preceding account fields)
```

Examples:
- Voting counters: `8 + 1` (discriminator + bump)
- Sealed auction encrypted state: `8 + 1 + 32 + 1 + 1 + 8 + 8 + 1 + 16`
- DNA markers block: `8 + 32 + 16 + 32`

When adding or reordering account fields, recompute offsets immediately.

## Failure Triage Tree

1. **Encryption stage failure**
- Symptoms: decrypt mismatch, invalid nonce usage, unusable ciphertext.
- Check x25519 keypair generation, nonce serialization (`deserializeLE`), shared secret pairing.
- Reference: `references/test-client-patterns.md`, `references/troubleshooting-matrix.md`.

2. **Queue stage failure**
- Symptoms: account not found, constraint errors, custom program errors.
- Check cluster offset, PDA derivation, comp-def account offset, account ordering, constraint seeds.
- Reference: `references/account-layout-offsets.md`, `references/permission-and-state-machines.md`.

3. **Callback verify failure**
- Symptoms: `AbortedComputation`, output parse mismatch.
- Check comp-def alignment, callback macro ix name, generated output shape assumptions.
- Reference: `references/callback-output-shapes.md`.

4. **Finalization stage failure**
- Symptoms: queue tx confirmed but no resolved result.
- Check `awaitComputationFinalization(...)` usage, computation offset mismatch, event listener sequencing.
- Reference: `references/test-client-patterns.md`, `references/troubleshooting-matrix.md`.

## Templates (Scaffolding)

Use templates in `assets/templates` to start implementations quickly:

- `assets/templates/new-computation/arcis-instruction.rs.tpl`
- `assets/templates/new-computation/program-flow.rs.tpl`
- `assets/templates/new-computation/callback.rs.tpl`
- `assets/templates/new-computation/init-comp-def.rs.tpl`
- `assets/templates/new-computation/e2e-test.ts.tpl`
- `assets/templates/offchain-circuit/init-comp-def-offchain.rs.tpl`
- `assets/templates/permissioned-flow/accounts-and-constraints.rs.tpl`

Replace placeholders such as `<IX_NAME>`, `<PROGRAM_ID>`, `<STATE_OFFSET>`, `<STATE_LEN>`.

## Task Routing

- End-to-end implementation workflow:
Read `references/implementation-playbook.md`.

- Pattern selection by example:
Read `references/examples-patterns.md`.

- Account layout and offset math:
Read `references/account-layout-offsets.md`.

- Callback output decoding:
Read `references/callback-output-shapes.md`.

- Permissions and state transitions:
Read `references/permission-and-state-machines.md`.

- Test/client orchestration:
Read `references/test-client-patterns.md`.

- Migrations and deployment:
Read `references/docs-and-migrations.md`.

- Failure triage:
Read `references/troubleshooting-matrix.md`.

- What to avoid:
Read `references/anti-patterns.md`.

## Definition of Done

Code changes are complete only when all checks pass:

1. Structural/build checks:
```bash
arcium build
cargo check --all
arcium test
```

2. Skill checks:
```bash
python3 /Users/grisahudozestvennyj/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/grisahudozestvennyj/Documents/projects/arcium/dna/skills/arcium-program-development
rg -n "[\p{Cyrillic}]" /Users/grisahudozestvennyj/Documents/projects/arcium/dna/skills/arcium-program-development || true
```

3. Functional acceptance checks:
- Circuit name, comp-def offset, callback macro, and callback output type are aligned.
- ArgBuilder order matches circuit input ownership contract.
- Offset constants match actual account layout and are documented.
- Callback verifies output before parsing/persisting.
- Tests wait for computation finalization and validate expected results.

## Delivery Standard

- Produce concrete code edits, not abstract guidance.
- Preserve existing seed derivation and PDA conventions unless migration requires changes.
- State assumptions explicitly when required inputs are missing.
- End with executed validation commands and any remaining risk notes.
