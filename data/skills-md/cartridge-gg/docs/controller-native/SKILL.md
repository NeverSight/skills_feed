---
name: controller-native
description: Integrate Cartridge Controller into native mobile applications (iOS, Android, React Native) and web wrappers (Capacitor). Use when building mobile games or apps that need Controller wallet functionality with local keypair signing. Covers SessionConnector for native auth flows, Controller.c FFI bindings, passkey configuration with Apple App Site Association, and platform-specific setup.
---

# Controller Native Integration

Integrate Controller into native and mobile applications.

## Choosing an Approach

| Approach | Use When | Platforms |
|----------|----------|-----------|
| Native Bindings (Controller.c) | Performance-critical, native apps | iOS, Android, React Native, C/C++ |
| Web Wrapper (Capacitor) | Existing web app → app store | iOS, Android |

## Key Concepts

- **SessionConnector**: Web/Capacitor apps with browser-based auth
- **SessionAccount**: Native apps using Controller.c FFI bindings
- **ControllerAccount**: Headless/server-side with custom signing keys

## SessionConnector (Web/Capacitor)

For web apps wrapped with Capacitor:

```typescript
import { SessionConnector } from "@cartridge/connector";
import { constants } from "starknet";

const policies = {
  contracts: {
    "0x1234...": {
      methods: [{ name: "play", entrypoint: "play" }],
    },
  },
};

const connector = new SessionConnector({
  policies,
  rpc: "https://api.cartridge.gg/x/starknet/mainnet",
  chainId: constants.StarknetChainId.SN_MAIN,
  redirectUrl: "myapp://auth-callback",
  disconnectRedirectUrl: "myapp://logout",
});
```

### Authentication Flow

1. App generates local keypair
2. User authenticates in browser (deep link)
3. Browser redirects back with session credentials
4. App signs transactions locally

## React Native

**Prerequisites**: Node.js >= 20

Uses TurboModules with Controller.c bindings. The native module is generated locally:

```bash
pnpm install
pnpm exec expo prebuild
```

```typescript
import { SessionAccount, type SessionPolicy, type Call } from "./modules/controller/src";

// Create session from subscription flow
const session = SessionAccount.createFromSubscribe(
  privateKey,
  sessionPolicies,
  "https://api.cartridge.gg/x/starknet/mainnet",
  "https://api.cartridge.gg"
);

// Access session metadata
const address = session.address();
const username = session.username();

// Execute transactions
const calls: Call[] = [
  {
    contractAddress: "0x...",
    entrypoint: "transfer",
    calldata: ["0x...", "0x100", "0x0"],
  },
];
const txHash = session.executeFromOutside(calls);
```

## iOS (Swift)

**Prerequisites**: Xcode 15+

Uses UniFFI-generated Swift bindings.

```swift
import ControllerAccount

// Create owner from private key
let owner = try Owner.init(privateKey: "0x...")

// Create headless controller
let controller = try ControllerAccount.newHeadless(
    appId: "my_app",
    username: "player",
    classHash: ControllerAccount.getControllerClassHash(.latest),
    rpcUrl: "https://api.cartridge.gg/x/starknet/mainnet",
    owner: owner,
    chainId: "0x534e5f4d41494e"
)

// Execute transaction
let call = Call(
    contractAddress: "0x...",
    entrypoint: "transfer",
    calldata: ["0x...", "0x100", "0x0"]
)

do {
    let txHash = try await controller.execute([call])
    print("Transaction: \(txHash)")
} catch let error as ControllerError {
    print("Error: \(error.message)")
}
```

## Android (Kotlin)

**Prerequisites**: Rust toolchain for building native libraries

Uses UniFFI-generated Kotlin bindings.

```kotlin
import uniffi.controller.*

val owner = ownerInit("0x...")

val controller = controllerNewHeadless(
    appId = "my_app",
    username = "player",
    classHash = getControllerClassHash(Version.LATEST),
    rpcUrl = "https://api.cartridge.gg/x/starknet/mainnet",
    owner = owner,
    chainId = "0x534e5f4d41494e"
)

val call = Call(
    contractAddress = "0x...",
    entrypoint = "transfer",
    calldata = listOf("0x...", "0x100", "0x0")
)

try {
    val txHash = controller.execute(listOf(call))
    println("Transaction: $txHash")
} catch (e: ControllerException) {
    println("Error: ${e.message}")
}
```

## Capacitor (Web Wrapper)

### iOS Configuration

```typescript
// capacitor.config.ts
export default {
  appId: "com.mygame.app",
  plugins: {
    App: {
      launchUrl: "myapp://",
    },
  },
};
```

### Android Configuration

Add to `AndroidManifest.xml`:

```xml
<activity
    android:name=".MainActivity"
    android:launchMode="singleTask">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="myapp" />
    </intent-filter>
</activity>
```

### Handle Deep Links

```typescript
import { App } from "@capacitor/app";

App.addListener("appUrlOpen", (event) => {
  if (event.url.includes("auth-callback")) {
    sessionConnector.handleCallback(event.url);
  }
});
```

**Note**: WebAuthn has limited support on Android webviews.

## Passkey Configuration (AASA)

To enable passkey sign-in on native apps, configure Apple App Site Association in your preset.

Add to `@cartridge/presets`:

```json
{
  "apple-app-site-association": {
    "webcredentials": {
      "apps": ["TEAMID.com.mygame.app"]
    }
  }
}
```

Replace `TEAMID` with your Apple Developer Team ID.

## Platform Notes

- **OAuth limitation**: Social login may not work in webviews. Prefer passkeys for native.
- **EVM wallets**: Desktop only, auto-hidden on mobile browsers.
- **Passkeys**: Require AASA configuration for native iOS apps.
- **Android WebAuthn**: Limited support in Capacitor webviews.

## Security

> **Warning**: Never commit private keys. Use environment variables, secure storage APIs, or secret managers.
