---
name: building-tauri-with-github-actions
description: Guides users through setting up Tauri GitHub Actions CI/CD pipelines and workflows for automated building, testing, and releasing cross-platform desktop applications.
---

# Building Tauri Apps with GitHub Actions

This skill covers CI/CD pipeline configuration for Tauri applications using GitHub Actions and the official `tauri-apps/tauri-action`.

## Overview

GitHub Actions enables automated building, testing, and releasing of Tauri applications across Windows, macOS, and Linux platforms. The `tauri-action` handles the complexity of cross-platform builds and release management.

## Workflow Triggers

### Push to Release Branch

```yaml
name: 'publish'
on:
  workflow_dispatch:
  push:
    branches:
      - release
```

### Tag-Based Releases

```yaml
name: 'publish'
on:
  push:
    tags:
      - 'app-v*'
```

## Platform Matrix Configuration

### Standard Multi-Platform Matrix

```yaml
jobs:
  publish-tauri:
    permissions:
      contents: write
    strategy:
      fail-fast: false
      matrix:
        include:
          - platform: 'macos-latest'
            args: '--target aarch64-apple-darwin'
          - platform: 'macos-latest'
            args: '--target x86_64-apple-darwin'
          - platform: 'ubuntu-22.04'
            args: ''
          - platform: 'windows-latest'
            args: ''

    runs-on: ${{ matrix.platform }}
```

### With ARM Linux Support (Public Repos Only)

Add `ubuntu-22.04-arm` to the matrix for native ARM64 Linux builds (public repositories only).

## Complete Workflow Example

```yaml
name: 'publish'

on:
  workflow_dispatch:
  push:
    branches:
      - release

jobs:
  publish-tauri:
    permissions:
      contents: write
    strategy:
      fail-fast: false
      matrix:
        include:
          - platform: 'macos-latest'
            args: '--target aarch64-apple-darwin'
          - platform: 'macos-latest'
            args: '--target x86_64-apple-darwin'
          - platform: 'ubuntu-22.04'
            args: ''
          - platform: 'windows-latest'
            args: ''

    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies (Ubuntu only)
        if: matrix.platform == 'ubuntu-22.04'
        run: |
          sudo apt-get update
          sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: lts/*
          cache: 'npm'

      - name: Setup Rust toolchain
        uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.platform == 'macos-latest' && 'aarch64-apple-darwin,x86_64-apple-darwin' || '' }}

      - name: Rust cache
        uses: swatinem/rust-cache@v2
        with:
          workspaces: './src-tauri -> target'

      - name: Install frontend dependencies
        run: npm ci

      - name: Build and release
        uses: tauri-apps/tauri-action@v0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tagName: app-v__VERSION__
          releaseName: 'App v__VERSION__'
          releaseBody: 'See the assets to download this version and install.'
          releaseDraft: true
          prerelease: false
          args: ${{ matrix.args }}
```

## Package Manager Variants

### pnpm

```yaml
- name: Setup pnpm
  uses: pnpm/action-setup@v4
  with:
    version: latest

- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: lts/*
    cache: 'pnpm'

- name: Install frontend dependencies
  run: pnpm install
```

### Yarn

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: lts/*
    cache: 'yarn'

- name: Install frontend dependencies
  run: yarn install --frozen-lockfile
```

## Caching Strategies

### Rust Artifact Caching

```yaml
- name: Rust cache
  uses: swatinem/rust-cache@v2
  with:
    workspaces: './src-tauri -> target'
```

### Node.js Dependency Caching

Configure via the `cache` parameter in `actions/setup-node@v4`: `'npm'`, `'yarn'`, or `'pnpm'`.

## Linux Dependencies

Ubuntu requires WebKit and related libraries:

```yaml
- name: Install dependencies (Ubuntu only)
  if: matrix.platform == 'ubuntu-22.04'
  run: |
    sudo apt-get update
    sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf
```

## Release Automation

### tauri-action Configuration

```yaml
- uses: tauri-apps/tauri-action@v0
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    tagName: app-v__VERSION__
    releaseName: 'App v__VERSION__'
    releaseBody: 'See the assets to download this version and install.'
    releaseDraft: true
    prerelease: false
    args: ${{ matrix.args }}
```

### Version Placeholders

The action automatically replaces `__VERSION__` with the app version from `tauri.conf.json`.

### Release Options

| Option | Description |
|--------|-------------|
| `tagName` | Git tag for the release (supports `__VERSION__` placeholder) |
| `releaseName` | Display name for the release |
| `releaseBody` | Release notes content |
| `releaseDraft` | Create as draft release (`true`/`false`) |
| `prerelease` | Mark as prerelease (`true`/`false`) |

## Artifact Uploads

### Upload Build Artifacts Without Release

```yaml
- name: Build Tauri app
  uses: tauri-apps/tauri-action@v0
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  id: tauri

- name: Upload artifacts
  uses: actions/upload-artifact@v4
  with:
    name: tauri-build-${{ matrix.platform }}
    path: src-tauri/target/release/bundle/
```

## GitHub Token Configuration

The `GITHUB_TOKEN` requires write permissions for release creation.

### Repository Settings

1. Go to Settings > Actions > General
2. Under "Workflow permissions"
3. Select "Read and write permissions"
4. Save

### Workflow Permissions

```yaml
jobs:
  publish-tauri:
    permissions:
      contents: write
```

## Non-Root Project Configuration

For projects where Tauri is not at the repository root:

```yaml
- uses: tauri-apps/tauri-action@v0
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    projectPath: './apps/desktop'
    tagName: app-v__VERSION__
    releaseName: 'App v__VERSION__'
```

## ARM Build Emulation (Alternative)

For ARM builds in private repositories or when native ARM runners are unavailable:

```yaml
jobs:
  build-arm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build ARM64
        uses: pguyot/arm-runner-action@v2.6.5
        with:
          base_image: dietpi:rpi_armv8_bullseye
          commands: |
            apt-get update
            apt-get install -y curl build-essential libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf
            curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
            source $HOME/.cargo/env
            curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
            apt-get install -y nodejs
            npm ci
            npm run tauri build
```

Note: ARM emulation builds take approximately one hour for fresh projects.

## Code Signing Integration

### macOS Signing Environment Variables

```yaml
- uses: tauri-apps/tauri-action@v0
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
    APPLE_CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
    APPLE_SIGNING_IDENTITY: ${{ secrets.APPLE_SIGNING_IDENTITY }}
    APPLE_ID: ${{ secrets.APPLE_ID }}
    APPLE_PASSWORD: ${{ secrets.APPLE_PASSWORD }}
    APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
```

### Windows Signing Environment Variables

```yaml
- uses: tauri-apps/tauri-action@v0
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    TAURI_SIGNING_PRIVATE_KEY: ${{ secrets.TAURI_SIGNING_PRIVATE_KEY }}
    TAURI_SIGNING_PRIVATE_KEY_PASSWORD: ${{ secrets.TAURI_SIGNING_PRIVATE_KEY_PASSWORD }}
```

## CI-Only Workflow (No Release)

For pull request validation without creating releases:

```yaml
name: 'CI Build'

on:
  pull_request:
    branches:
      - main

jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        include:
          - platform: 'macos-latest'
            args: '--target aarch64-apple-darwin'
          - platform: 'ubuntu-22.04'
            args: ''
          - platform: 'windows-latest'
            args: ''

    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies (Ubuntu only)
        if: matrix.platform == 'ubuntu-22.04'
        run: |
          sudo apt-get update
          sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: lts/*
          cache: 'npm'

      - name: Setup Rust toolchain
        uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.platform == 'macos-latest' && 'aarch64-apple-darwin,x86_64-apple-darwin' || '' }}

      - name: Rust cache
        uses: swatinem/rust-cache@v2
        with:
          workspaces: './src-tauri -> target'

      - name: Install frontend dependencies
        run: npm ci

      - name: Build Tauri app
        run: npm run tauri build -- ${{ matrix.args }}
```

## Troubleshooting

### Permission Denied for Release Creation

Ensure workflow has write permissions and verify repository settings allow Actions to create releases:

```yaml
jobs:
  publish-tauri:
    permissions:
      contents: write
```

### Linux Build Failures

Verify all dependencies are installed with the Ubuntu dependency installation step.

### macOS Target Not Found

Ensure Rust targets are installed for cross-compilation:

```yaml
- uses: dtolnay/rust-toolchain@stable
  with:
    targets: 'aarch64-apple-darwin,x86_64-apple-darwin'
```

### Cache Not Working

Verify the workspace path matches your project structure:

```yaml
- uses: swatinem/rust-cache@v2
  with:
    workspaces: './src-tauri -> target'
```
