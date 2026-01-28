---
name: swift-spm
description: Master Swift Package Manager - dependencies, creating libraries, publishing, local packages
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 01-swift-fundamentals
bond_type: SECONDARY_BOND
---

# Swift Package Manager Skill

Dependency management, package creation, and distribution with Swift Package Manager.

## Prerequisites

- Swift 5.5+ toolchain
- Xcode 14+ or VS Code with Swift extension
- Git for version control

## Parameters

```yaml
parameters:
  swift_tools_version:
    type: string
    default: "5.9"
  platforms:
    type: array
    items: [iOS, macOS, watchOS, tvOS, visionOS, linux]
    default: [iOS, macOS]
  package_type:
    type: string
    enum: [library, executable, plugin]
    default: library
```

## Topics Covered

### Package.swift Structure
| Element | Purpose |
|---------|---------|
| `name` | Package name |
| `platforms` | Supported platforms/versions |
| `products` | Libraries/executables exposed |
| `dependencies` | External packages |
| `targets` | Build targets |

### Dependency Specification
| Format | Example |
|--------|---------|
| Version range | `.upToNextMajor(from: "1.0.0")` |
| Exact version | `.exact("1.2.3")` |
| Branch | `.branch("main")` |
| Commit | `.revision("abc123")` |
| Path | `.package(path: "../LocalPkg")` |

### Target Types
| Type | Purpose |
|------|---------|
| `.target` | Library code |
| `.executableTarget` | Command-line tool |
| `.testTarget` | Unit tests |
| `.plugin` | Build tool plugin |
| `.macro` | Swift macro |

## Code Examples

### Complete Package.swift
```swift
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "NetworkKit",
    platforms: [
        .iOS(.v15),
        .macOS(.v12),
        .watchOS(.v8),
        .tvOS(.v15)
    ],
    products: [
        .library(
            name: "NetworkKit",
            targets: ["NetworkKit"]
        ),
        .library(
            name: "NetworkKitMocks",
            targets: ["NetworkKitMocks"]
        )
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-log.git", from: "1.5.0"),
        .package(url: "https://github.com/apple/swift-collections.git", from: "1.0.0")
    ],
    targets: [
        .target(
            name: "NetworkKit",
            dependencies: [
                .product(name: "Logging", package: "swift-log"),
                .product(name: "OrderedCollections", package: "swift-collections")
            ],
            resources: [
                .process("Resources")
            ],
            swiftSettings: [
                .enableExperimentalFeature("StrictConcurrency")
            ]
        ),
        .target(
            name: "NetworkKitMocks",
            dependencies: ["NetworkKit"]
        ),
        .testTarget(
            name: "NetworkKitTests",
            dependencies: [
                "NetworkKit",
                "NetworkKitMocks"
            ],
            resources: [
                .copy("Fixtures")
            ]
        )
    ]
)
```

### Library with Multiple Targets
```swift
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "FeatureKit",
    platforms: [.iOS(.v16), .macOS(.v13)],
    products: [
        // Main library
        .library(name: "FeatureKit", targets: ["FeatureKit"]),
        // Individual features for selective import
        .library(name: "AuthFeature", targets: ["AuthFeature"]),
        .library(name: "ProfileFeature", targets: ["ProfileFeature"])
    ],
    dependencies: [
        .package(url: "https://github.com/pointfreeco/swift-composable-architecture", from: "1.0.0")
    ],
    targets: [
        // Core shared code
        .target(
            name: "Core",
            dependencies: []
        ),

        // Auth feature
        .target(
            name: "AuthFeature",
            dependencies: [
                "Core",
                .product(name: "ComposableArchitecture", package: "swift-composable-architecture")
            ]
        ),

        // Profile feature
        .target(
            name: "ProfileFeature",
            dependencies: [
                "Core",
                .product(name: "ComposableArchitecture", package: "swift-composable-architecture")
            ]
        ),

        // Umbrella target
        .target(
            name: "FeatureKit",
            dependencies: ["AuthFeature", "ProfileFeature"]
        ),

        // Tests
        .testTarget(
            name: "AuthFeatureTests",
            dependencies: ["AuthFeature"]
        ),
        .testTarget(
            name: "ProfileFeatureTests",
            dependencies: ["ProfileFeature"]
        )
    ]
)
```

### Command-Line Tool
```swift
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "swift-format-tool",
    platforms: [.macOS(.v13)],
    products: [
        .executable(name: "swift-format-tool", targets: ["swift-format-tool"])
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-argument-parser", from: "1.2.0"),
        .package(url: "https://github.com/apple/swift-syntax", from: "509.0.0")
    ],
    targets: [
        .executableTarget(
            name: "swift-format-tool",
            dependencies: [
                .product(name: "ArgumentParser", package: "swift-argument-parser"),
                .product(name: "SwiftSyntax", package: "swift-syntax"),
                .product(name: "SwiftParser", package: "swift-syntax")
            ]
        )
    ]
)
```

### Local Development Package
```swift
// In your app's Package.swift or Xcode project
// Use local path during development

// Package.swift with local override
let package = Package(
    name: "MyApp",
    dependencies: [
        // Production: Use remote
        // .package(url: "https://github.com/company/SharedKit", from: "1.0.0")

        // Development: Use local
        .package(path: "../SharedKit")
    ],
    targets: [
        .target(name: "MyApp", dependencies: ["SharedKit"])
    ]
)
```

### Swift Macro Package
```swift
// swift-tools-version: 5.9
import PackageDescription
import CompilerPluginSupport

let package = Package(
    name: "MacroKit",
    platforms: [.macOS(.v10_15), .iOS(.v13)],
    products: [
        .library(name: "MacroKit", targets: ["MacroKit"])
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-syntax", from: "509.0.0")
    ],
    targets: [
        // Macro implementation
        .macro(
            name: "MacroKitMacros",
            dependencies: [
                .product(name: "SwiftSyntaxMacros", package: "swift-syntax"),
                .product(name: "SwiftCompilerPlugin", package: "swift-syntax")
            ]
        ),

        // Library that exposes the macro
        .target(
            name: "MacroKit",
            dependencies: ["MacroKitMacros"]
        ),

        // Tests for the macro
        .testTarget(
            name: "MacroKitTests",
            dependencies: [
                "MacroKitMacros",
                .product(name: "SwiftSyntaxMacrosTestSupport", package: "swift-syntax")
            ]
        )
    ]
)
```

## CLI Commands

```bash
# Create new package
swift package init --type library
swift package init --type executable
swift package init --type macro

# Build
swift build
swift build -c release

# Test
swift test
swift test --filter MyTests

# Update dependencies
swift package update
swift package update PackageName

# Resolve dependencies
swift package resolve

# Show dependencies
swift package show-dependencies
swift package show-dependencies --format json

# Generate Xcode project (deprecated but useful)
swift package generate-xcodeproj

# Clean
swift package clean
swift package reset

# Dump package description
swift package dump-package
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "No such module" | Missing dependency | Add to target dependencies |
| Version conflict | Incompatible requirements | Use version that satisfies all |
| Build fails on CI | Different Swift version | Pin swift-tools-version |
| Resources not found | Wrong resource rule | Use .process or .copy correctly |
| Xcode not seeing changes | Cache stale | Clean derived data |

### Debug Tips
```bash
# Verbose build
swift build -v

# Check resolved versions
cat Package.resolved

# Dependency tree
swift package show-dependencies --format dot | dot -Tpng -o deps.png

# Rebuild from scratch
rm -rf .build Package.resolved
swift package resolve
swift build
```

## Validation Rules

```yaml
validation:
  - rule: pin_versions
    severity: warning
    check: Use version ranges, not branch/revision in production
  - rule: semantic_versioning
    severity: error
    check: Follow semver for your packages
  - rule: platform_support
    severity: info
    check: Declare minimum platform versions
```

## Usage

```
Skill("swift-spm")
```

## Related Skills

- `swift-fundamentals` - Language basics
- `swift-testing` - Package testing
- `swift-architecture` - Package design
