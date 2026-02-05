---
name: tuist
description: Best practices for Tuist projects. Use when working with Tuist manifests, generating projects, or building with xcodebuild in Tuist projects.
---

# Tuist

## Project Generation

Generate projects without opening Xcode:

```bash
tuist generate --no-open
```

## Target Declaration

Use `buildableFolders` when declaring targets to avoid regenerating projects on file changes:

```swift
let target = Target(
    name: "MyApp",
    destinations: [.iPhone],
    product: .app,
    bundleId: "com.example.app",
    buildableFolders: ["Sources/", "Resources/"]
)
```

## Building with xcodebuild

Pass these build settings to enable caching and improve build performance:

```bash
xcodebuild build \
  -scheme MyScheme \
  COMPILATION_CACHE_ENABLE_CACHING=YES \
  CLANG_ENABLE_COMPILE_CACHE=YES \
  SWIFT_ENABLE_EXPLICIT_MODULES=YES \
  SWIFT_USE_INTEGRATED_DRIVER=YES
```

## Disable Signing for CI/Agent Builds

When building through an agent or CI, disable code signing:

```bash
xcodebuild build \
  -scheme MyScheme \
  CODE_SIGN_IDENTITY=""
```
