---
name: controller-backend
description: Integrate Cartridge Controller into backend services using Node.js, Rust, or headless mode. Use when building server-side applications, game backends, automated bots, or any non-browser environment that needs to execute Starknet transactions. Covers SessionProvider for Node.js, Rust SDK setup, and headless Controller with custom signing keys.
---

# Controller Backend Integration

Integrate Controller into server-side applications and automated systems.

Sessions enable pre-approved transactions without manual user approval, making them ideal for automated backends.

## Node.js

Uses `SessionProvider` with file-based session storage.

### Installation

```bash
pnpm add @cartridge/controller starknet
```

### Setup

```typescript
import SessionProvider, {
  ControllerError,
} from "@cartridge/controller/session/node";
import { constants } from "starknet";
import path from "path";

const ETH_CONTRACT =
  "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7";

async function main() {
  const storagePath =
    process.env.CARTRIDGE_STORAGE_PATH ||
    path.join(process.cwd(), ".cartridge");

  const provider = new SessionProvider({
    rpc: "https://api.cartridge.gg/x/starknet/mainnet",
    chainId: constants.StarknetChainId.SN_MAIN,
    policies: {
      contracts: {
        [ETH_CONTRACT]: {
          methods: [
            {
              name: "approve",
              entrypoint: "approve",
              spender: "0x1234567890abcdef1234567890abcdef12345678",
              amount: "0xffffffffffffffffffffffffffffffff",
              description: "Approve spending of tokens",
            },
            { name: "transfer", entrypoint: "transfer" },
          ],
        },
      },
    },
    basePath: storagePath,
  });

  try {
    const account = await provider.connect();

    if (account) {
      console.log("Account address:", account.address);

      // Example: Transfer ETH
      const amount = "0x0";
      const recipient = account.address; // Replace with actual recipient

      const result = await account.execute([
        {
          contractAddress: ETH_CONTRACT,
          entrypoint: "transfer",
          calldata: [recipient, amount, "0x0"],
        },
      ]);

      console.log("Transaction hash:", result.transaction_hash);
    } else {
      console.log("Please complete the session creation in your browser");
    }
  } catch (error: unknown) {
    const controllerError = error as ControllerError;
    if (controllerError.code) {
      console.error("Session error:", {
        code: controllerError.code,
        message: controllerError.message,
        data: controllerError.data,
      });
    } else {
      console.error("Session error:", error);
    }
  }
}

main().catch(console.error);
```

### Notes

- `basePath` specifies session storage directory (must be writable)
- First run requires browser-based session creation
- Session persists between runs

## Rust

Uses `account_sdk` crate for native Rust integration.

### Installation

```toml
[dependencies]
account_sdk = { git = "https://github.com/cartridge-gg/controller-rs.git", package = "account_sdk" }
starknet = "0.10"
tokio = { version = "1", features = ["full"] }
```

### Setup

```rust
use account_sdk::{controller::Controller, signers::Signer};
use starknet::{
    accounts::Account,
    providers::Provider,
    signers::SigningKey,
    core::types::FieldElement,
};
use std::env;

#[tokio::main]
async fn main() {
    // Load private key from environment
    let private_key = env::var("PRIVATE_KEY")
        .expect("PRIVATE_KEY must be set");

    let owner = Signer::Starknet(
        SigningKey::from_secret_scalar(
            FieldElement::from_hex_be(&private_key).unwrap()
        )
    );

    let rpc_url = "https://api.cartridge.gg/x/starknet/mainnet";
    let provider = Provider::try_from(rpc_url).unwrap();
    let chain_id = provider.chain_id().await.unwrap();

    let controller = Controller::new(
        "my_app".to_string(),
        "username".to_string(),
        FieldElement::from_hex_be("0xCLASS_HASH").unwrap(),
        rpc_url.parse().unwrap(),
        owner,
        FieldElement::from_hex_be("0xCONTROLLER_ADDRESS").unwrap(),
        chain_id,
    );

    // Deploy if needed
    controller.deploy().await.unwrap();

    // Execute transaction
    let call = starknet::core::types::FunctionCall {
        contract_address: FieldElement::from_hex_be("0xCONTRACT").unwrap(),
        entry_point_selector: starknet::core::utils::get_selector_from_name("transfer").unwrap(),
        calldata: vec![FieldElement::from(123)],
    };

    controller.execute(vec![call], None).await.unwrap();
}
```

## Headless Controller

For server-side execution with custom signing keys.

### Use Cases

- Single owner, multiple accounts
- Automated game backends (bots, NPCs)
- Custom key management requirements

### C++ Example

> **Warning**: Never commit private keys. Use environment variables or secret managers.

```cpp
#include "controller.hpp"
#include <cstdlib>

int main() {
    // Load from environment - NEVER hardcode!
    const char* pk = std::getenv("PRIVATE_KEY");
    if (!pk) {
        std::cerr << "PRIVATE_KEY not set" << std::endl;
        return 1;
    }
    std::string private_key(pk);

    auto owner = controller::Owner::init(private_key);

    auto ctrl = controller::Controller::new_headless(
        "my_app",
        "bot_account",
        controller::get_controller_class_hash(controller::Version::kLatest),
        "https://api.cartridge.gg/x/starknet/mainnet",
        owner,
        "0x534e5f4d41494e"  // SN_MAIN
    );

    // Register new account onchain
    ctrl->signup(
        controller::SignerType::kStarknet,
        std::nullopt,
        std::nullopt
    );

    // Execute transaction
    controller::Call call{
        "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7",
        "transfer",
        {"0xRECIPIENT", "0x100", "0x0"}
    };

    std::string tx_hash = ctrl->execute({call});
    std::cout << "Transaction: " << tx_hash << std::endl;

    return 0;
}
```

## Security Best Practices

**Never commit private keys**. Use:

- Environment variables
- Secret managers (AWS Secrets Manager, HashiCorp Vault)
- Hardware security modules (HSM)

```typescript
// Good
const privateKey = process.env.PRIVATE_KEY;

// Bad - NEVER do this
const privateKey = "0x1234...";
```

## Telegram Mini-Apps

Use `SessionConnector` with Telegram WebApp context.

### Integration Flow

1. Configure session policies
2. Set up SessionProvider with cloud storage
3. Handle authentication redirects
4. Execute transactions via session

### Setup

```typescript
import { SessionConnector } from "@cartridge/connector";
import { constants } from "starknet";

const policies = {
  contracts: {
    "0x...": {
      methods: [{ name: "action", entrypoint: "action" }],
    },
  },
};

const connector = new SessionConnector({
  policies,
  rpc: "https://api.cartridge.gg/x/starknet/mainnet",
  chainId: constants.StarknetChainId.SN_MAIN,
  redirectUrl: window.Telegram?.WebApp?.initData
    ? "https://t.me/MyBot/app"
    : "https://myapp.com/callback",
});
```

### Next.js WebAssembly Configuration

For Telegram mini-apps using Next.js:

```typescript
// next.config.js
module.exports = {
  webpack: (config) => {
    config.experiments = {
      ...config.experiments,
      asyncWebAssembly: true,
    };
    return config;
  },
};
```
