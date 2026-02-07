---
name: using-crabnebula-cloud-with-tauri
description: Guides the user through distributing Tauri applications via CrabNebula Cloud, including pipeline setup, cloud configuration, auto-updates integration, and CI/CD workflows for seamless app distribution.
---

# CrabNebula Cloud with Tauri

CrabNebula is an official Tauri partner providing a platform for application distribution that seamlessly integrates with the Tauri updater. The platform offers global CDN distribution, release management, and built-in auto-update support.

## Overview

CrabNebula Cloud provides:

- **Global CDN**: Worldwide distribution of installers and updates
- **Release Channels**: Support for multiple release tracks (stable, beta, nightly)
- **Auto-Updates**: Built-in update server compatible with Tauri's updater plugin
- **Download Metrics**: Analytics for tracking application downloads
- **CI/CD Integration**: GitHub Actions support for automated releases

## Initial Setup

### 1. Create CrabNebula Cloud Account

1. Navigate to [CrabNebula Cloud](https://web.crabnebula.cloud/)
2. Sign in using GitHub or GitLab authentication
3. Create an organization with a unique slug
4. Create an application within your organization

### 2. Generate API Key

1. Navigate to API Keys section in CrabNebula Cloud
2. Generate a new key with Read/Write permissions
3. Save this key securely (displayed only once)
4. Add as `CN_API_KEY` repository secret in GitHub

**Important**: Use repository secrets, not environment secrets, as environment secrets may appear in logs.

## CLI Installation

Install the CrabNebula CLI to manage releases locally:

```bash
# macOS/Linux
curl -L https://cdn.crabnebula.app/install/cn | sh

# Or via cargo
cargo install cn-cli
```

## Release Workflow

The release process follows four steps: draft, upload, publish, fetch.

### Manual CLI Commands

```bash
# Create a release draft
cn release draft ORG_SLUG/APP_SLUG VERSION

# Upload assets with Tauri framework detection
cn release upload ORG_SLUG/APP_SLUG RELEASE_ID --framework tauri

# Publish the release
cn release publish ORG_SLUG/APP_SLUG RELEASE_ID

# Fetch latest release info
cn release latest ORG_SLUG/APP_SLUG
```

### Upload Command Options

```bash
cn release upload ORG_SLUG/APP_SLUG RELEASE_ID \
  --framework tauri \
  --channel stable \
  --update-platform linux-x86_64 \
  --file path/to/binary \
  --signature path/to/signature
```

| Flag | Description |
|------|-------------|
| `--framework` | Auto-detect bundles (`tauri` or `packager`) |
| `--channel` | Release channel (must match draft channel) |
| `--update-platform` | Platform identifier for updates |
| `--file` | Path to binary asset |
| `--signature` | Path to signature file (required with `--update-platform`) |

## GitHub Actions Workflow

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    branches:
      - main
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  CN_APPLICATION: "your-org/your-app"

jobs:
  draft:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.read-version.outputs.version }}
    steps:
      - uses: actions/checkout@v4

      - name: Read version from tauri.conf.json
        id: read-version
        run: |
          VERSION=$(jq -r '.version' src-tauri/tauri.conf.json)
          echo "version=$VERSION" >> $GITHUB_OUTPUT

      - name: Create draft release
        uses: crabnebula-dev/cloud-release@v0
        with:
          command: release draft ${{ env.CN_APPLICATION }} ${{ steps.read-version.outputs.version }} --framework tauri
          api-key: ${{ secrets.CN_API_KEY }}

  build:
    needs: draft
    strategy:
      fail-fast: false
      matrix:
        include:
          - platform: ubuntu-22.04
            args: ""
          - platform: macos-latest
            args: "--target aarch64-apple-darwin"
          - platform: macos-latest
            args: "--target x86_64-apple-darwin"
          - platform: windows-latest
            args: ""
    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: lts/*

      - name: Install Rust stable
        uses: dtolnay/rust-action@stable
        with:
          targets: ${{ matrix.platform == 'macos-latest' && 'aarch64-apple-darwin,x86_64-apple-darwin' || '' }}

      - name: Install Linux dependencies
        if: matrix.platform == 'ubuntu-22.04'
        run: |
          sudo apt-get update
          sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf

      - name: Install frontend dependencies
        run: npm ci

      - name: Build Tauri app
        uses: tauri-apps/tauri-action@v0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TAURI_SIGNING_PRIVATE_KEY: ${{ secrets.TAURI_SIGNING_PRIVATE_KEY }}
          TAURI_SIGNING_PRIVATE_KEY_PASSWORD: ${{ secrets.TAURI_SIGNING_PRIVATE_KEY_PASSWORD }}
        with:
          args: ${{ matrix.args }}

      - name: Upload assets to CrabNebula Cloud
        uses: crabnebula-dev/cloud-release@v0
        with:
          command: release upload ${{ env.CN_APPLICATION }} --framework tauri
          api-key: ${{ secrets.CN_API_KEY }}

  publish:
    needs: [draft, build]
    runs-on: ubuntu-latest
    steps:
      - name: Publish release
        uses: crabnebula-dev/cloud-release@v0
        with:
          command: release publish ${{ env.CN_APPLICATION }} ${{ needs.draft.outputs.version }}
          api-key: ${{ secrets.CN_API_KEY }}
```

## Auto-Updates Configuration

### 1. Generate Signing Keys

```bash
cargo tauri signer generate -w ~/.tauri/myapp.key
```

This creates:
- `~/.tauri/myapp.key` - Private key (keep secret)
- `~/.tauri/myapp.key.pub` - Public key (add to config)

Add to GitHub repository secrets:
- `TAURI_SIGNING_PRIVATE_KEY`: Contents of `myapp.key`
- `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`: Your password

### 2. Configure tauri.conf.json

```json
{
  "version": "0.1.0",
  "bundle": {
    "createUpdaterArtifacts": true
  },
  "plugins": {
    "updater": {
      "active": true,
      "endpoints": [
        "https://cdn.crabnebula.app/update/YOUR_ORG/YOUR_APP/{{target}}-{{arch}}/{{current_version}}"
      ],
      "dialog": true,
      "pubkey": "dW50cnVzdGVkIGNvbW1lbnQ6IG1pbmlzaWduIHB1YmxpYyBrZXk..."
    }
  }
}
```

**Important**: Keep the `{{target}}`, `{{arch}}`, and `{{current_version}}` placeholders unchanged. Tauri replaces these dynamically at runtime.

For migrations from Tauri v1, use `"createUpdaterArtifacts": "v1Compatible"`.

### 3. Configure Capabilities

Update `/src-tauri/capabilities/main.json`:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Main capability for the application",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "dialog:default",
    "updater:default",
    "process:default",
    "process:allow-restart"
  ]
}
```

### 4. Install Dependencies

Add to `src-tauri/Cargo.toml`:

```toml
[dependencies]
tauri-plugin-updater = "2"
tauri-plugin-dialog = "2"
tauri-plugin-process = "2"
```

Install frontend packages:

```bash
npm install @tauri-apps/plugin-updater @tauri-apps/plugin-dialog @tauri-apps/plugin-process
```

### 5. Register Plugins (Rust)

Update `src-tauri/src/lib.rs`:

```rust
use tauri::Manager;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_updater::Builder::new().build())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_process::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### 6. Implement Update Check (TypeScript)

Create `src/updater.ts`:

```typescript
import { check } from "@tauri-apps/plugin-updater";
import { ask } from "@tauri-apps/plugin-dialog";
import { relaunch } from "@tauri-apps/plugin-process";

export async function checkForAppUpdates(): Promise<void> {
  try {
    const update = await check();

    if (!update?.available) {
      console.log("No update available");
      return;
    }

    const proceed = await ask(
      `Version ${update.version} is available!\n\nRelease notes:\n${update.body}`,
      {
        title: "Update Available",
        kind: "info",
        okLabel: "Update Now",
        cancelLabel: "Later"
      }
    );

    if (proceed) {
      console.log("Downloading and installing update...");
      await update.downloadAndInstall();
      await relaunch();
    }
  } catch (error) {
    console.error("Update check failed:", error);
  }
}
```

Call early in your app lifecycle:

```typescript
// React example
import { useEffect } from "react";
import { checkForAppUpdates } from "./updater";

function App() {
  useEffect(() => {
    checkForAppUpdates();
  }, []);

  return <div>Your app content</div>;
}
```

## Release Channels

For multiple distribution channels (beta, stable, nightly):

### Option 1: Channel Argument

```bash
# Create draft with channel
cn release draft ORG/APP VERSION --channel beta

# Upload must specify same channel
cn release upload ORG/APP RELEASE_ID --framework tauri --channel beta
```

### Option 2: Separate Applications

Create separate applications in CrabNebula Cloud:
- `your-org/your-app` (stable)
- `your-org/your-app-beta` (beta)

Configure different update endpoints per channel in your app builds.

## Environment Variables Summary

| Variable | Location | Description |
|----------|----------|-------------|
| `CN_API_KEY` | GitHub Secrets | CrabNebula Cloud API key |
| `TAURI_SIGNING_PRIVATE_KEY` | GitHub Secrets | Contents of private signing key |
| `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` | GitHub Secrets | Password for signing key |
| `CN_APPLICATION` | Workflow env | Organization/application slug |

## Troubleshooting

### Update Check Fails

1. Verify endpoint URL matches your organization and app slugs
2. Ensure public key in config matches the generated key
3. Check that `createUpdaterArtifacts` is set to `true`
4. Verify capabilities include required permissions

### Build Fails on Upload

1. Ensure `CN_API_KEY` is set as repository secret (not environment secret)
2. Verify the draft was created successfully before upload
3. Check that signing keys are properly configured

### Signature Mismatch

1. Ensure `TAURI_SIGNING_PRIVATE_KEY` matches the public key in config
2. Verify the same key pair is used across all builds
3. For v1 migrations, use `"createUpdaterArtifacts": "v1Compatible"`

## Resources

- [CrabNebula Cloud Documentation](https://docs.crabnebula.dev/cloud/)
- [Tauri Updater Plugin](https://v2.tauri.app/plugin/updater/)
- [CrabNebula Cloud Release Action](https://github.com/crabnebula-dev/cloud-release)
- [Tauri Distribution Guide](https://v2.tauri.app/distribute/crabnebula-cloud/)
