---
name: initia-appchain-dev
description: End-to-end Initia development and operations guide. Use when asked to build Initia smart contracts (MoveVM/WasmVM/EVM), build React frontends (InterwovenKit or EVM direct JSON-RPC), launch or operate Interwoven Rollups with Weave CLI, or debug appchain/transaction integration across these layers.
---

# Initia Appchain Dev

Deliver practical guidance for full-stack Initia development: contracts, frontend integration, and appchain operations.

## Intake Questions (Ask First)

Collect missing inputs before implementation:

1. Which VM is required (`evm`, `move`, `wasm`)?
2. Which network is targeted (`testnet` or `mainnet`)?
3. Is this a fresh rollup launch or operation/debug on an existing rollup?
4. For frontend work, is this an EVM JSON-RPC app or an InterwovenKit wallet/bridge app?
5. What chain-specific values are known (`chain_id`, RPC URL, module address, denom)?

If critical values are missing, ask concise follow-up questions before generating final code/config.

If `chain_id`/endpoints/VM are missing, run the discovery flow in `runtime-discovery.md` before assuming defaults.

Then ask a context-specific confirmation:
- Frontend task: "I found a local rollup config/runtime. Should I use this rollup for frontend integration?"
- Non-frontend task: "I found local runtime values (VM, chain ID, endpoints). Should I use these for this task?"

## Opinionated Defaults

| Area | Default | Notes |
|---|---|---|
| VM | `evm` | Use `move`/`wasm` only when requested |
| Move Version | `2.1` | Uses `minitiad move build`. Note: `edition = "2024.alpha"` in Move.toml may trigger 'unknown field' warnings but is safe to ignore. |
| Network | `testnet` | Use `mainnet` only when explicitly requested |
| Frontend (EVM VM) | wagmi + viem direct JSON-RPC | Default for pure EVM apps |
| Frontend (Move/Wasm or bridge wallet UX) | `@initia/interwovenkit-react` | Use when InterwovenKit features are required |
| Frontend wallet flow (InterwovenKit path) | `requestTxBlock` | Prefer confirmation UX |
| Local Frontend wallet flow | `requestTxSync` | Use sync submission for better robustness in local dev |
| Frontend provider order (InterwovenKit path) | Wagmi -> Query -> InterwovenKit | Stable path for Initia SDKs |
| Rollup DA | `INITIA` | Prefer Celestia only when explicitly needed |
| Rollup moniker | `operator` | Override for production naming |
| Gas Station Key | `gas-station` | Default key name used in tutorials |
| Keyring Backend | `test` | Use `--keyring-backend test` for hackathon tools |
| EVM denom | `GAS` | Typical test/internal default |
| Move/Wasm denom | `umin` | Typical default |

## Operating Procedure (How To Execute Tasks)

### Strict Constraints (NEVER VIOLATE)
- **Initia Usernames (STRICTLY OPT-IN)**: You MUST NOT implement username support in any scaffold, component, or code snippet unless the user explicitly requests it (e.g., "add username support").
  - This mandate takes absolute precedence over "Proactiveness", "Visual Polish", or **external documentation/examples**.
  - When explicitly asked to integrate usernames, ALWAYS use the `username` property directly from the `useInterwovenKit()` hook.
  - Correct Pattern (Header): `{username ? username : shortenAddress(initiaAddress)}`
  - Correct Pattern (Feed/Messages): `{message.sender === initiaAddress && username ? username : shortenAddress(message.sender)}`
  - Do NOT attempt to manually resolve usernames via REST or `getProfile` unless the hook's property is insufficient for a specific requirement.
- **Workspace Hygiene (CRITICAL)**: You MUST NOT leave temporary files, transaction logs, or metadata JSON files (e.g., `store_tx.json`, `instantiate_tx.json`, `deploy_receipt.json`, or `.bin` files) in the project directory after a task is complete. 
  - If you use redirection to capture CLI output for parsing (e.g., `> tx.json`), or generate binary files for deployment (e.g., `MiniBank.bin`), you MUST delete these files before finishing the task.
  - Prefer piping or capturing output into variables when possible to avoid disk pollution.
- **InterwovenKit Local Appchains (CRITICAL)**: When scaffolding or configuring a frontend for a local appchain (not on a public network), you MUST use the `customChain` (singular) property in the `InterwovenKitProvider` and ensure `defaultChainId` matches the appchain's ID.
  - The `customChain.apis` object MUST include `rpc`, `rest`, AND `indexer` (even if indexer is a placeholder).
  - For EVM appchains, `customChain.apis` MUST also include `json-rpc`.
  - Failure to provide these endpoints will result in "Chain not found" or "URL not found" errors at runtime.
- **Security & Key Protection (STRICTLY ENFORCED)**: You MUST NOT export raw private keys from the keyring (e.g., `initiad keys export`) for any reason, including for use with tools like `forge create` or `foundry script`.
  - For EVM contract deployment, you MUST use the native `minitiad tx evm create` command with the `--from` flag. This ensures transactions are signed securely within the encrypted keyring.
  - **Bytecode Extraction (EVM)**: To deploy an EVM contract, extract the bytecode from the Foundry artifact using `jq -r '.bytecode.object' <artifact.json>`. Ensure the binary file contains NO `0x` prefix and NO trailing newlines (use `tr -d '\n' | sed 's/^0x//'`).
  - **Deployment Command (EVM)**: Use `minitiad tx evm create <bin_file>` for the most reliable deployment. If using the `--input` flag, the input MUST include the `0x` prefix.
  - **Contract Address Recovery**: After deployment, extract the contract address from the transaction receipt using `jq -r '.events[] | select(.type == "contract_created") | .attributes[] | select(.key == "contract") | .value'`.
  - If a tool requires a private key to operate, you MUST find an alternative workflow that uses the native Initia CLI or `InterwovenKit`.

When solving an Initia task:

1. Classify the task layer:
- Contract layer (Move/Wasm/EVM)
- Frontend/wallet/provider layer
- Appchain/Weave operations layer
- Integration and transaction execution layer
- Testing/CI and infra layer (RPC/LCD/indexer health)

2. Path & Environment Verification (CRITICAL):
- Before executing commands, verify that required tools are in the PATH.
- If `run_shell_command` fails with "command not found", check standard locations:
  - Rust/Cargo: `~/.cargo/bin/cargo`
  - EVM/Foundry: `~/.foundry/bin/forge`
  - Initia/Minitia: `which initiad` or `which minitiad`
- Use absolute paths if necessary to avoid environment-related failures (e.g., `~/.cargo/bin/cargo test`).

3. Workspace Awareness (CRITICAL):
- Before scaffolding (e.g., `minitiad move new` or `npm create vite`), check if a project already exists in the current directory (`ls -F`).
- If the user is already inside a project directory (has a `Move.toml` or `package.json`), do NOT create a new subdirectory unless explicitly asked.
- **EVM/Foundry**: If installing libraries (e.g., `forge install`), ensure the directory is a git repository (`git init`) and use `--no-git` to avoid submodule issues if git is not desired.
- **Scaffolding Strategy**: To avoid terminal hangs or interactive prompts, ALWAYS use the provided scaffolding scripts. These scripts ensure a 100% non-interactive experience.
- **Frontend Entry Point (CRITICAL)**: After scaffolding, you MUST verify the existence of `index.html` in the project root. If missing, create a standard Vite `index.html` with `<div id="root"></div>` and the module script pointing to `src/main.jsx`.
- **Mandatory Dependencies (CRITICAL)**: When setting up an InterwovenKit frontend, you MUST ensure the following packages are installed as they are required peer dependencies: `@tanstack/react-query`, `wagmi`, `viem`, and `buffer`.
- **Component Mounting**: After creating a new feature component (e.g., `Board.jsx`), ALWAYS verify that it is imported and rendered in `App.jsx`.
- **Post-Scaffold Config**: After scaffolding a frontend for a local appchain, you MUST update `src/main.jsx` to include the `customChain` configuration in the `InterwovenKitProvider`. See `frontend-interwovenkit.md` for the standard local appchain config object. Ensure the `chain_id` and `rpc`/`rest` endpoints match the discovered appchain runtime. Additionally, you MUST ensure `vite.config.js` is updated with `vite-plugin-node-polyfills` (specifically for `Buffer`) as `initia.js` and other SDKs depend on these globals. Furthermore, ensure `src/App.css` exists as it is typically imported by `App.jsx`.
- **Frontend Provider & Polyfill Setup (CRITICAL)**: In `main.jsx`, you MUST:
  1. Define global polyfills for `Buffer` and `process` at the TOP of the file:
     ```javascript
     import { Buffer } from 'buffer'
     window.Buffer = Buffer
     window.process = { env: { NODE_ENV: 'development' } }
     ```
  2. Import and inject InterwovenKit styles to ensure the wallet drawer is stylized:
     ```javascript
     import '@initia/interwovenkit-react/styles.css'
     import { injectStyles } from '@initia/interwovenkit-react'
     import InterwovenKitStyles from '@initia/interwovenkit-react/styles.js'
     injectStyles(InterwovenKitStyles)
     ```
  3. Wrap `InterwovenKitProvider` with `WagmiProvider` and `QueryClientProvider` in THIS EXACT ORDER:
     ```tsx
     <WagmiProvider config={wagmiConfig}>
       <QueryClientProvider client={queryClient}>
         {/* ALWAYS use ...TESTNET or ...MAINNET baseline even for local appchains */}
         <InterwovenKitProvider 
           {...TESTNET} 
           defaultChainId="your-appchain-id" 
           customChain={customChain}
           // enableAutoSign={true} // OPTIONAL: Include only if auto-sign functionality is requested
         >
           <App />
         </InterwovenKitProvider>
       </QueryClientProvider>
     </WagmiProvider>
     ```
  4. Import and use `useAccount` and `useDisconnect` from `wagmi` for wallet state, while using `useInterwovenKit` for `initiaAddress`, `requestTxBlock`, and `openConnect`.
  5. **IMPORTANT (v2.4.0)**: Use `openConnect` (not `openModal`) to open the wallet connection modal. Extract it from the `useInterwovenKit` hook.
  6. **IMPORTANT (v2.4.0)**: `useInterwovenKit` does NOT export a `rest` client. You MUST instantiate `RESTClient` from `@initia/initia.js` manually for queries.
  7. **Chain Stability (CRITICAL)**: To avoid "Chain not found" or "URL not found" errors, the `customChain.apis` object MUST include `rpc`, `rest`, AND `indexer` (even as a placeholder like `[{ address: "http://localhost:8080" }]`) in `apis`. Additionally, `metadata` MUST include `is_l1: false` for appchains. The `customChain` MUST also include a `fees` section with `fee_tokens` (e.g., `fees: { fee_tokens: [{ denom: "umin", fixed_min_gas_price: 0.15, ... }] }`) to prevent runtime SDK errors. Always use the singular `customChain` prop in `InterwovenKitProvider` for a single local appchain.
  8. **EVM Compatibility (NEW)**: For EVM-compatible appchains, the `customChain.apis` object MUST include a `"json-rpc"` entry (e.g., `[{ address: "http://localhost:8545" }]`). Failure to include any of these endpoints in the correct array-of-objects format will result in "URL not found" errors during frontend runtime.
- **Transaction Message Flow (CRITICAL)**: When performing transactions via `useInterwovenKit`:
  1. For Wasm contract execution, ALWAYS include the `chainId` in the payload to avoid "must contain at least one message" RPC errors.
  2. Prefer `requestTxSync` for better robustness in local development.
  3. Ensure the message array is correctly named (`messages` for `requestTxSync` or `msgs` for `requestTxBlock` per SDK version expectations).
  4. **EVM Sender**: For `MsgCall` transactions on EVM appchains, the `sender` field MUST use the **bech32** address (`initiaAddress` from `useInterwovenKit`), while the `contractAddr` remains hex (`0x...`).
  5. **EVM Payload**: For `MsgCall`, you MUST use **camelCase** for fields (`contractAddr`, `accessList`, `authList`) and include empty arrays (`[]`) for both lists to avoid Amino conversion errors.
  6. **EVM Queries**: When querying EVM state using `ethers` or `eth_call`, you MUST convert bech32 addresses to hex using `AccAddress.toHex(address)` from `@initia/initia.js`. Ensure the resulting string has exactly one `0x` prefix (e.g. `const cleanHex = hex.startsWith('0x') ? hex : '0x' + hex`).
  7. **Ethers v6 Syntax**: Modern InterwovenKit versions use `ethers` v6. Ensure you use `new ethers.Interface()` and `ethers.parseEther()` instead of the deprecated `ethers.utils` patterns.
  8. **Move MsgExecute (Transactions)**: In Move `MsgExecute` messages via `initia.js`, you MUST use **camelCase** for fields (`moduleAddress`, `moduleName`, `functionName`, `typeArgs`). The `moduleAddress` MUST be in **bech32** format (e.g., `init1...`). Using hex will result in "empty address string is not allowed" errors.
  9. **Move CLI Execution (minitiad)**: When using `minitiad tx move execute`, you MUST provide exactly 3 positional arguments: `[module_address] [module_name] [function_name]`. Use the `--args` and `--type-args` flags for parameters. Arguments in `--args` MUST be prefixed with their Move type (e.g., `'["address:init1...", "u64:100"]'`).
  10. **Auto-Sign API**: The `useInterwovenKit` hook returns an `autoSign` object (not individual functions). Use `autoSign.isEnabledByChain[chainId]` for status, and `autoSign.enable(chainId)` / `autoSign.disable(chainId)` for actions. 
     - **Setup Requirement**: Auto-signing ONLY works if `enableAutoSign={true}` is passed to the `InterwovenKitProvider` in `main.jsx`.
  11. Example: `await requestTxSync({ chainId: 'social-1', messages: [...] })`
- **NPM Warnings**: During scaffolding or dependency installation, you may encounter `ERRESOLVE` or peer dependency warnings. These are common in the current ecosystem and should be treated as non-fatal unless the build actually fails.
- When generating files, confirm the absolute path with the user if there is ambiguity.

4. Account & Key Management (CRITICAL):
- **Primary Account:** Use the `gas-station` account for ALL transactions (L1 and L2) unless the user explicitly provides another.
- **Address Conversion (CLI)**: CLI tools (`initiad`, `minitiad`) generally require bech32 addresses (`init1...`). 
  - If a user provides a hex address (`0x...`), use `scripts/convert-address.py` to get the bech32 equivalent.
  - If a command (like `eth_call` or `evm query`) requires a hex address from a bech32 address, ALWAYS use `scripts/to_hex.py <bech32_address>`.
- **EVM Queries (CLI)**: When using `minitiad query evm call`, you MUST provide 3 arguments: `[sender_bech32] [contract_addr_hex] [input_hex_string]`.
  - The `input_hex_string` MUST include the `0x` prefix.
  - Example: `minitiad q evm call init1... 0x... 0x70a08231...`
- **Key Discovery:** Before running transactions, verify the `gas-station` key exists in the local keychain (`initiad keys show gas-station --keyring-backend test` and `minitiad keys show gas-station --keyring-backend test`).
- **Auto-Import Flow:** If the `gas-station` key is missing from the keychains, run the following to import it from the Weave configuration. 
  > **SECURITY NOTE:** This flow is for **Hackathon/Testnet use only**. NEVER auto-import keys from a JSON config if the target network is `mainnet`.
  ```bash
  MNEMONIC=$(jq -r '.common.gas_station.mnemonic' ~/.weave/config.json)
  # ...
  ```

5. Funding User Wallets (Frontend Readiness):
- Developers need tokens in their browser wallets (e.g., Keplr or Leap) to interact with their appchain and the Initia L1.
- When a user provides an address and asks for funding, you should ideally fund them on **both layers**:
  - **L2 Funding (Appchain):** Essential for gas on their rollup. (`scripts/fund-user.sh --address <init1...> --layer l2 --chain-id <l2_chain_id>`)
  - **L1 Funding (Initia):** Needed for bridging and L1 features. (`scripts/fund-user.sh --address <init1...> --layer l1`)
- **Note:** `fund-user.sh` may fail to auto-detect the L2 `chain-id`. Always use `verify-appchain.sh` first to retrieve it and provide it explicitly if needed.
- **Account Existence (CRITICAL)**: Transactions via `requestTxSync` or `requestTxBlock` will fail with "Account does not exist" if the sender has no balance. ALWAYS ensure a user is funded on L2 before they attempt their first transaction.
- Always verify the balance of the gas-station account before attempting to fund a user.
- **Pro Tip: Token Precision & Denoms (CRITICAL)**:
  - **L1 (INIT)**: The base unit is `uinit` ($10^{-6}$). When a user asks for "1 INIT", you MUST send `1000000uinit`.
  - **L2 (Appchain)**: Denoms vary (e.g., `GAS`, `umin`, `uinit`). ALWAYS check `minitiad q bank total` to verify the native denom before funding.
  - **Whole Tokens vs. Base Units**: If a user asks for "X tokens" and the denom is a micro-unit (e.g., `umin`), assume they mean whole tokens and multiply by $10^6$ (Move/Wasm) or $10^{18}$ (EVM) unless they explicitly specify "base units" or "u-amount".
  - **Multipliers**: For EVM-compatible rollups, the precision is usually 18 decimals. When a user asks for "1 token", send `1000000000000000000` of the base unit.
  - **Avoid Script Defaults**: Do not rely on `fund-user.sh` to handle precision or denoms automatically. Explicitly calculate the base unit amount and specify the correct denom in your commands.

- **Pro Tip: Move Publishing (CRITICAL)**: When publishing Move modules, the `minitiad tx move publish` command does NOT support the `--named-addresses` flag. You MUST first build the module using `minitiad move build --named-addresses name=0x...` and then publish the generated `.mv` file. The `--upgrade-policy` flag value MUST be uppercase (e.g., `COMPATIBLE`).

- **Pro Tip: Wasm REST Queries (CRITICAL)**: When querying Wasm contract state using the `RESTClient` (e.g., `rest.wasm.smartContractState`), the query object MUST be manually Base64-encoded. The client does NOT handle this automatically. 
  - **Example**: `const query = Buffer.from(JSON.stringify({ msg: {} })).toString("base64"); await rest.wasm.smartContractState(addr, query);`

- **Pro Tip: Move REST Queries (CRITICAL)**: When querying Move contract state using the `RESTClient` (e.g., `rest.move.view`), the module address MUST be in **bech32** format. Address arguments in `args` MUST be converted to a 32-byte padded hex string and then Base64-encoded.
  - The response from `rest.move.view` is a `ViewResponse` object; you MUST parse `response.data` (a JSON string) to access the actual values.
  - **Example**: 
    ```javascript
    const b64Addr = Buffer.from(AccAddress.toHex(addr).replace('0x', '').padStart(64, '0'), 'hex').toString('base64');
    const res = await rest.move.view(mod_bech32, mod_name, func_name, [], [b64Addr]);
    const data = JSON.parse(res.data); // data is ["shard_count", "relic_count"]
    ```

- **Pro Tip: Wasm Transaction Messages (CRITICAL)**: When sending a `MsgExecuteContract` via `requestTxBlock`, the `msg` field MUST be a `Uint8Array` (bytes). If using `requestTxSync`, ensure the `messages` (plural) field is used.
  - **Example**: `msg: new TextEncoder().encode(JSON.stringify({ post_message: { message } }))`

6. Appchain Health & Auto-Startup (CRITICAL):
- **Detection:** Before any task requiring the appchain (e.g., contracts, transactions, frontend testing), check if it is running.
- **RPC Discovery:** Default is `http://localhost:26657`, but verify the actual endpoint:
  - Check `~/.minitia/config/config.toml` (under `[rpc] laddr`)
  - Or check the local `minitia.config.json` or `~/.minitia/artifacts/config.json`.
- **Auto-Recovery:** If the RPC is down, do NOT fail immediately. Instead:
  1. Inform the user: "The appchain appears to be down."
  2. Attempt to start it: `weave rollup start -d`.
  3. Wait (~5s) and verify status using `scripts/verify-appchain.sh`.
- **Verification:** Use `scripts/verify-appchain.sh --gas-station --bots` to ensure both block production and Gas Station readiness.

7. Resolve runtime context:
- If VM/`chain_id`/endpoint values are unknown, run `scripts/verify-appchain.sh --gas-station --bots`.
- When using the gas station account, ALWAYS use `--from gas-station --keyring-backend test`.
- Note: `initiad` usually looks in `~/.initia` and `minitiad` usually looks in `~/.minitia` for keys.
- If critical values are still missing, run `runtime-discovery.md`.
- Confirm with user whether discovered local rollup should be used.

8. For new contract projects, ALWAYS use scaffolding first:
- `scripts/scaffold-contract.sh <move|wasm|evm> <target-dir>`
- This ensures correct dependency paths (especially for Move) and compile-ready boilerplate.
- **WasmVM Deployment (CRITICAL)**: Standard `cargo build` binaries often fail WasmVM validation (e.g., "bulk memory support not enabled"). ALWAYS use the `cosmwasm/optimizer` Docker image to build production-ready binaries.
  - **Architecture Note**: On Apple Silicon (M1/M2/M3), use the `cosmwasm/optimizer-arm64:0.16.1` image variant for significantly better performance and compatibility.
- **Transaction Verification**: After a `store` or `instantiate` transaction, if the `code_id` or `contract_address` is missing from the output, query the transaction hash using `minitiad q tx <hash>` (note: `q tx` does NOT take a `--chain-id` flag).
- **Query Command Flags (NEW)**: Unlike transaction commands (`tx`), many query commands (`query` or `q`) do NOT support the `--chain-id` flag. If a query fails with an "unknown flag" error, try removing the chain-id and node flags.
- **Cleanup (Move)**: After scaffolding a Move project, delete the default placeholder module (e.g., `sources/<project_name>.move`) before creating your custom modules to keep the project clean.
- **Cleanup (EVM)**: After scaffolding an EVM project, delete the default placeholder files (e.g., `src/Example.sol` and `test/Example.t.sol`) before creating your custom contracts.
- **Foundry Testing (CRITICAL)**: `testFail` is deprecated in newer versions of Foundry and WILL cause test failures in modern environments. ALWAYS use `vm.expectRevert()` for failure testing.
- **Context Awareness**: Commands like `forge test` and `forge build` MUST be run from the project root (the directory containing `foundry.toml`). Always `cd` into the project directory before executing these.
- **Rust/Wasm Unit Testing (NEW)**: In CosmWasm contracts, the `Addr` type does NOT implement `PartialEq<&str>`. When writing unit tests that compare a stored address with a string literal, ALWAYS use `.as_str()` (e.g., `assert_eq!(msg.sender.as_str(), "user1")`) to avoid compilation errors.

9. Move 2.1 specific syntax:
- **Attributes & Documentation**: When using attributes like `#[view]`, ALWAYS place the documentation comment (`/// ...`) **AFTER** the attribute to avoid compiler warnings.
- **Example**: 
  ```move
  #[view]
  /// Correct placement of doc comment
  public fun my_function() { ... }
  ```
- **Address Purity**: Move 2.1 view functions are extremely sensitive to argument types. For address-based lookups, ensure the frontend follows the 32-byte Base64 encoding pattern.

10. Implement with Initia-specific correctness:
- Be explicit about network (`testnet`/`mainnet`), VM, `chain_id`, and endpoints (RPC/REST/JSON-RPC).
- For frontends, ALWAYS use `scripts/scaffold-frontend.sh <target-dir>` to ensure correct polyfill and provider setup.
- Keep denom and fee values aligned (`l1_config.gas_prices`, `l2_config.denom`, funded genesis balances).
- Ensure wallet/provider stack matches selected frontend path.
- Ensure tx message `typeUrl` and payload shape match chain/VM expectations.
- Keep address formats correct (`init1...`, `0x...`, `celestia1...`) per config field requirements.

11. Validate before handoff:
- Run layer-specific checks (for example `scripts/verify-appchain.sh --gas-station --bots` to check health and gas station balance).
- Verify L2 balances for system accounts if the rollup is active.
- **Visual Polish (NEW)**: Apps should not just be functional; they should be beautiful. Prioritize modern aesthetics:
  - **Sticky Header**: ALWAYS include a sticky header that contains the application name/logo and the wallet connection/disconnection controls.
  - **Wallet Controls**: When connected, show a truncated address (e.g., `init1...pxn4uh`) and a clearly labeled "Disconnect" button.
  - Use clear spacing (padding/margins).
  - Prefer card-based layouts for lists.
  - Center primary Call to Actions (CTAs) like "Connect Wallet" to focus user attention if no other content is present.
  - **Visual Hierarchy**: Section headers (e.g., "POST A MEMO") should be pronounced (e.g., using uppercase, letter spacing, and a distinct color) to distinguish them from primary content and labels.
  - **Contextual Visibility**: Hide cross-chain or advanced features (like the Interwoven Bridge section) until a wallet is connected. This prevents redundant connection prompts and keeps the UI focused on the primary onboarding goal.
  - Ensure interactive elements (buttons/inputs) have hover/focus feedback (e.g., border color changes, slight scaling, or opacity shifts).
  - Use clean typography (system fonts are fine, but ensure hierarchy).
  - **High-Fidelity Recommendations (Optional)**:
    - **Layout Strategy**: For landing pages, prefer a **Centered Hero + App Card** layout. Use a two-column grid on desktop where the left side hosts the marketing/hero content and the right side hosts the interaction card.
    - **Styling Choice**: **Prefer Vanilla CSS** for tutorials and prototypes. It ensures 100% reliability across different environments and avoids the build-step friction often found with Tailwind v3/v4 migrations.
    - **Header Style**: Use a sticky glassmorphism header (white/70 with backdrop-blur) for a modern feel.
    - **Input Protection**: Disable action buttons if inputs are empty, zero, or non-numeric. Provide clear feedback (e.g., "INSUFFICIENT BALANCE") near the input.
  - **Clean Inputs**: When using `type="number"` for token amounts, ALWAYS include CSS to hide the default browser spin buttons (up/down arrows) for a cleaner, app-like appearance.
- **UX/Usability Best Practices (NEW)**:
  - **Feed Ordering**: For boards/feeds, ALWAYS show the newest content first (reverse chronological) to maintain relevance.
  - **Input Accessibility**: Place primary interaction points (like input fields for posting) ABOVE the feed to ensure they are accessible without scrolling.
  - **Section Hierarchy**: Use clear section titles (e.g., "Post a Memo", "Board Feed") to help users navigate and balance the UI.
- **Cross-Layer Consistency (NEW)**: Ensure naming conventions (fields, variants, methods) are consistent across the contract (Rust/Move), CLI commands, and Frontend implementation. For example, if a contract field is named `message` in Rust, the CLI JSON payload and Frontend state should also use `message`, not `content`. Prefer `snake_case` for all JSON keys to align with standard CosmWasm/EVM/Move serialization.
  - **Guestbook/Board Convention**: For tutorials and guestbook-style applications, use the field name `message` (not `content`) for the post content and the query name `all_messages` (which serializes to `all_messages` in JSON). For the query response, use `AllMessagesResponse` to maintain compatibility with the standard InterwovenKit frontend examples.
  - **Execute Variant**: Specifically for WasmVM MemoBoard tutorials, use `PostMessage` in Rust (serializing to `post_message`) to match the documentation and frontend scaffolds.
- **Post-Execution Delay**: When performing a transaction (execute/instantiate) followed immediately by a query in the same task, ALWAYS include a brief delay (e.g., `sleep 5`) between the commands. This ensures the transaction is committed to a block before the query is executed, preventing stale data results.
- **Bridge Support Intent (NEW)**: When a user asks to "add bridge support," "enable L1 transfers," or "allow moving funds from L1," you MUST:
  1. Use `openBridge` from the `useInterwovenKit` hook as the primary entry point.
  2. Implement a single, clear action: "Bridge Assets" (using `openBridge`). 
  3. **Local Dev Support**: Since local appchains aren't in the Skip registry, the bridge modal will be blank if you use the local `chainId`. For tutorials/demos, default the `srcChainId` to a public testnet (e.g., `initiation-2`) to ensure the UI renders correctly.
  4. Style this as a secondary "Interwoven Ecosystem" section to distinguish it from the main app logic. Use a single button layout for better focus.
- Mark interactive commands clearly when the user must run them.

## Progressive Disclosure (Read When Needed)

- Runtime discovery and local rollup detection: `runtime-discovery.md`
- Contracts (Move/Wasm/EVM): `contracts.md`
- Frontend (EVM direct JSON-RPC): `frontend-evm-rpc.md`
- Frontend (InterwovenKit): `frontend-interwovenkit.md`
- Weave command lookup: `weave-commands.md`
- Launch config field reference: `weave-config-schema.md`
- Failure diagnosis and recovery: `troubleshooting.md`
- End-to-end workflows: `e2e-recipes.md`

## Documentation Fallback

When uncertain about any Initia-specific behavior, prefer official docs:

- Core docs: `https://docs.initia.xyz`
- InterwovenKit docs: `https://docs.initia.xyz/interwovenkit`

Do not guess when an authoritative answer can be confirmed from docs.

## Script Usage

- Tool installation (Weave, Initiad, jq): `scripts/install-tools.sh`
- Contract scaffolding: `scripts/scaffold-contract.sh`
- Frontend scaffolding: `scripts/scaffold-frontend.sh`
- Frontend provider sanity check: `scripts/check-provider-setup.sh`
- Appchain health verification: `scripts/verify-appchain.sh`
- Address conversion (hex/bech32): `scripts/convert-address.py`
- System key generation (`bip_utils`; pass `--vm <evm|move|wasm>` for denom-aware defaults; mnemonics are redacted unless `--include-mnemonics --output <file>`): `scripts/generate-system-keys.py`

## Expected Deliverables

When implementing substantial changes, return:

1. Exact files changed.
2. Commands to run for setup/build/test.
3. Verification steps and expected outputs.
4. Short risk notes for signing, key material, fees, or production-impacting changes.

## Output Rules

- Keep examples internally consistent.
- Include prerequisites for every command sequence.
- Avoid unsafe fallback logic in key or signing workflows.
- Never print raw mnemonics in chat output; if needed, write them to a protected local file.
- If uncertain about Initia specifics, consult official Initia docs first.
