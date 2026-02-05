---
name: controller-signers
description: Configure authentication methods for Cartridge Controller including passkeys, social login, and external wallets. Use when implementing user authentication, adding multiple signers for account recovery, customizing signup options, or integrating external wallets like MetaMask or Phantom. Covers WebAuthn passkeys, Google/Discord/Twitter OAuth, wallet connections, and dynamic authentication flows.
---

# Controller Signers & Authentication

Controller supports multiple authentication methods (signers) for flexibility and security.

## Supported Signer Types

| Type | Description | Best For |
|------|-------------|----------|
| `webauthn` | Passkey (biometric/hardware key) | Primary auth, most secure |
| `google` | Google OAuth | Easy onboarding |
| `discord` | Discord OAuth | Gaming communities |
| `twitter` | Twitter/X OAuth | Social integration |
| `argent` | Argent wallet (Starknet) | Starknet native users |
| `braavos` | Braavos wallet (Starknet) | Starknet native users |
| `metamask` | MetaMask (desktop only) | EVM users |
| `phantom-evm` | Phantom EVM mode (desktop only) | Multi-chain users |
| `rabby` | Rabby wallet (desktop only) | Security-focused users |
| `walletconnect` | WalletConnect (desktop only) | Cross-device |
| `password` | Email/password | **Testing only** |

> **Warning**: Password authentication is non-recoverable. If users lose their password, they permanently lose account access. Do not use in production.

## Configuring Auth Options

```typescript
const controller = new Controller({
  signupOptions: [
    "webauthn",     // Passkeys
    "google",       // Google OAuth
    "discord",      // Discord OAuth
    "twitter",      // Twitter/X OAuth
    "argent",       // Argent wallet
    "braavos",      // Braavos wallet
    "metamask",     // MetaMask (desktop)
    "phantom-evm",  // Phantom (desktop)
    "rabby",        // Rabby (desktop)
    "walletconnect",// WalletConnect (desktop)
  ],
});
```

Order reflects UI order. With one option, branded buttons appear.

## Dynamic Authentication

Override auth options per connection:

```typescript
// Default options
const controller = new Controller({
  signupOptions: ["webauthn", "google", "discord"],
});

// Branded Phantom flow
await controller.connect(["phantom-evm"]);

// Branded Google flow
await controller.connect(["google"]);
```

### Branded Buttons

Single signer config shows branded styling:

```typescript
// Shows "sign up with Phantom" button with Phantom branding
const controller = new Controller({
  signupOptions: ["phantom-evm"],
});
```

## Passkey Authentication

Platform support: iOS (Face ID/Touch ID), Android, Windows Hello, password managers (Bitwarden, 1Password).

Passkeys are backed up via:
- Apple: iCloud Keychain
- Android: Google account
- Windows: Windows account

## Social Login

Uses Auth0 + Turnkey wallet infrastructure:

1. Popup OAuth flow (fallback to redirect if blocked)
2. OIDC token validation with nonce
3. Turnkey wallet creation linked to social account

**Native app limitation**: OAuth may not work in webviews. Use passkeys for native apps.

## External Wallets

### Starknet Wallets

- **Argent**: Advanced security features, account management
- **Braavos**: Built-in security features

### EVM Wallets (Desktop Only)

- **MetaMask**: Popular browser extension
- **Rabby**: Security-focused multi-chain
- **Phantom**: Multi-chain with EVM support

### Cross-Platform

- **WalletConnect**: QR code or deep link connection

**Note**: EVM wallets are automatically hidden on mobile browsers.

### Chain Switching

```typescript
const success = await controller.externalSwitchChain(
  "metamask",  // wallet type
  chainId      // target chain (hex)
);
```

Braavos does not support chain switching.

### Transaction Confirmation

```typescript
const response = await controller.externalWaitForTransaction(
  "metamask",
  txHash,
  30000 // timeout ms
);

if (response.success) {
  console.log("Receipt:", response.result);
} else {
  console.error("Error:", response.error);
}
```

## Multi-Signer Management

Add backup signers via Settings > Signer(s) > Add Signer (Mainnet only).

To remove a signer:
1. Navigate to Settings > Signer(s)
2. Find the signer to remove
3. Click Remove option

Best practices:
- Add 2-3 different signer types for recovery
- Test each auth method periodically
- Remove compromised signers promptly

## Account Synchronization

Argent and Braavos wallets auto-sync when user switches accounts in wallet.
Controller registers `accountsChanged` listener and updates state automatically.

**Note**: Account synchronization is currently only available for Starknet wallets (Argent and Braavos). Other external wallets maintain existing connection behavior.

## Platform-Specific Configuration

```typescript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

const authOptions = isMobile
  ? ["webauthn", "google", "discord", "argent", "braavos"]
  : ["webauthn", "google", "discord", "argent", "braavos", "metamask", "walletconnect"];

await controller.connect(authOptions);
```
