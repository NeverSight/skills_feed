---
name: swift_package_manager
description: Swift Package Manager (SPM) for dependency management, package creation, and modular code organization.
license: Proprietary
compatibility: Swift 4+
metadata:
  version: "1.0"
  author: SwiftZilla
  website: https://swiftzilla.dev
---

# Swift Package Manager

This skill covers Swift Package Manager for managing dependencies, creating reusable packages, and organizing code into modular components.

## Overview

Swift Package Manager (SPM) is Apple's official tool for distributing and managing Swift code. It handles dependency resolution, building, and packaging with a simple declarative format.

## Available References

- [Package Structure](./references/package_structure.md) - Package.swift, targets, products, and dependencies
- [Dependencies](./references/dependencies.md) - Version constraints, local packages, and resolution
- [Publishing](./references/publishing.md) - Publishing packages to GitHub and registries

## Quick Reference

### Basic Package.swift

```swift
// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "MyLibrary",
    platforms: [.iOS(.v15), .macOS(.v12)],
    products: [
        .library(
            name: "MyLibrary",
            targets: ["MyLibrary"]
        ),
    ],
    dependencies: [
        .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0"),
    ],
    targets: [
        .target(
            name: "MyLibrary",
            dependencies: [
                .product(name: "Alamofire", package: "Alamofire")
            ]
        ),
        .testTarget(
            name: "MyLibraryTests",
            dependencies: ["MyLibrary"]
        ),
    ]
)
```

### Adding Dependencies

```swift
// Version ranges
.package(url: "...", from: "1.0.0")           // >= 1.0.0, < 2.0.0
.package(url: "...", .upToNextMajor(from: "1.0.0"))
.package(url: "...", .upToNextMinor(from: "1.0.0"))
.package(url: "...", .exact("1.0.0"))
.package(url: "...", branch: "main")
.package(url: "...", revision: "abc123")

// Local packages
.package(path: "../LocalPackage")
```

### Command Line

```bash
# Initialize new package
swift package init --type library
swift package init --type executable

# Resolve dependencies
swift package resolve

# Update dependencies
swift package update

# Build
swift build

# Test
swift test

# Generate Xcode project
swift package generate-xcodeproj
```

## Package Structure

```
MyPackage/
├── Package.swift          # Package manifest
├── Sources/
│   └── MyLibrary/
│       └── MyLibrary.swift
├── Tests/
│   └── MyLibraryTests/
│       └── MyLibraryTests.swift
└── README.md
```

## Best Practices

1. **Use semantic versioning** - Follow SemVer for version tags
2. **Specify platform requirements** - Declare minimum OS versions
3. **Create explicit products** - Control what you expose
4. **Separate test targets** - Keep tests isolated
5. **Use resource bundles** - For non-code assets
6. **Commit Package.resolved** - For reproducible builds
7. **Document public API** - Use Swift documentation comments
8. **Add LICENSE file** - Essential for open source

## For More Information

Visit https://swiftzilla.dev for comprehensive Swift Package Manager documentation.
