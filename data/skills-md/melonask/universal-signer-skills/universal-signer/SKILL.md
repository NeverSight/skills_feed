---
name: universal-signer
description: Guide for using @universal-signer/core to unified signing across AWS KMS, GCP KMS, Ledger, Trezor, Turnkey, and Local accounts with Viem v2. Use when implementing secure signing logic that needs to support hardware or cloud KMS providers.
---

# Universal Signer

## Overview

`@universal-signer/core` provides a unified, type-safe interface for various signing providers, all compatible with **Viem v2**. It allows you to write blockchain logic once and switch between AWS KMS, Google Cloud KMS, Ledger, Trezor, Turnkey, and local keys through configuration.

## Installation

```bash
npm install @universal-signer/core viem
```

Then install only the provider(s) you need:

| Provider    | Dependencies                                                       |
| ----------- | ------------------------------------------------------------------ |
| **AWS KMS** | `npm install @aws-sdk/client-kms`                                  |
| **GCP KMS** | `npm install @google-cloud/kms`                                    |
| **Ledger**  | `npm install @ledgerhq/hw-app-eth @ledgerhq/hw-transport-node-hid` |
| **Trezor**  | `npm install @trezor/connect`                                      |
| **Turnkey** | `npm install @turnkey/viem @turnkey/http @turnkey/api-key-stamper` |
| **Local**   | No additional dependencies                                         |

## Quick Start

```typescript
import { createUniversalClient, createAwsAccount } from "@universal-signer/core";
import { mainnet } from "viem/chains";
import { http } from "viem";

// 1. Create an account
const account = await createAwsAccount({
  keyId: "alias/my-key",
  region: "us-east-1"
});

// 2. Create a Viem-compatible client
const client = createUniversalClient(account, mainnet, http());

// 3. Sign transactions or messages normally
const hash = await client.sendTransaction({
  to: "0x...",
  value: 1000000000000000n
});
```

## Features & Configuration

For detailed setup and configuration for specific providers, see the following:

- **[Provider Configurations](references/providers.md)**: Details for AWS, GCP, Hardware Wallets, and Turnkey.
- **[Troubleshooting & Technical Details](references/troubleshooting.md)**: Common errors and signature normalization info.

## Key Capabilities

- **Unified API**: All providers return a standard Viem `LocalAccount`.
- **Full Support**: `signTransaction`, `signMessage`, and `signTypedData` (EIP-712).
- **KMS Normalization**: Automatic EIP-2 signature normalization and `v` recovery.
- **Hardware Ready**: Built-in HID management for Ledger and Trezor.
