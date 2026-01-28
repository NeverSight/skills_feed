---
name: swift-package-manager
description: Swift Package Manager documentation - create packages, manage dependencies, build and test Swift code
---

# PackageManagerDocs

Organize, manage, and edit Swift packages.

## Documentation Structure

### Essentials

- **Getting Started** ([GettingStarted.md](GettingStarted.md)): Learn to create and use Swift packages.
- **Introducing Packages** ([IntroducingPackages.md](IntroducingPackages.md)): Learn to create and use a Swift package.
- **Package Security** ([PackageSecurity.md](PackageSecurity.md)): Learn about the security features that the package manager implements.

### Guides

- **Creating a Swift package** ([CreatingSwiftPackage.md](CreatingSwiftPackage.md)): Bundle executable or shareable code into a standalone Swift package.
- **Setting the Swift tools version** ([SettingSwiftToolsVersion.md](SettingSwiftToolsVersion.md)): Define the minimum version of the swift compiler required for your package.
- **Adding dependencies to a Swift package** ([AddingDependencies.md](AddingDependencies.md)): Use other Swift packages, system libraries, or binary dependencies in your package.
- **Resolving and updating dependencies** ([ResolvingPackageVersions.md](ResolvingPackageVersions.md)): Coordinate and constrain dependencies for your package.
- **Creating C language targets** ([CreatingCLanguageTargets.md](CreatingCLanguageTargets.md)): Include C language code as a target in your Swift package.
- **Using build configurations** ([UsingBuildConfigurations.md](UsingBuildConfigurations.md)): Control the build configuration for your app or package.
- **Packaging based on the version of Swift** ([SwiftVersionSpecificPackaging.md](SwiftVersionSpecificPackaging.md)): Provide a package manifest for a specific version of Swift.
- **Bundling resources with a Swift package** ([BundlingResources.md](BundlingResources.md)): Add resource files to your Swift package and access them in your code.
- **Releasing and publishing a Swift package** ([ReleasingPublishingAPackage.md](ReleasingPublishingAPackage.md)): Share a specific version of your package.
- **Continuous Integration Workflows** ([ContinuousIntegration.md](ContinuousIntegration.md)): Build Swift packages with an existing continuous integration setup and prepare apps that consume package dependencies within an existing CI pipeline.
- **Plugins** ([Plugins.md](Plugins.md)): Extend package manager functionality with build or command plugins.
- **Module Aliasing** ([ModuleAliasing.md](ModuleAliasing.md)): Create aliased names for modules to avoid collisions between targets in your package or its dependencies.
- **Using a package registry** ([UsingSwiftPackageRegistry.md](UsingSwiftPackageRegistry.md)): Configure and use a package registry for Swift Package Manager.
- **Package Collections** ([PackageCollections.md](PackageCollections.md)): Learn to create, publish and use Swift package collections.
- **Using shell completion scripts** ([UsingShellCompletion.md](UsingShellCompletion.md)): Customize your shell to automatically complete swift package commands.
- **Swift Package Manager as a library** ([SwiftPMAsALibrary.md](SwiftPMAsALibrary.md)): Include Swift Package Manager as a dependency in your Swift package.

### Swift Commands

- **swift build** ([SwiftBuild.md](SwiftBuild.md)): Build sources into binary products.
- **swift test** ([SwiftTest.md](SwiftTest.md)): Build and run tests.
- **swift package** ([SwiftPackageCommands.md](SwiftPackageCommands.md)): Subcommands to update and inspect your Swift package.
- **swift sdk** ([SwiftSDKCommands.md](SwiftSDKCommands.md)): Perform operations on Swift SDKs.
- **swift package-registry** ([SwiftPackageRegistryCommands.md](SwiftPackageRegistryCommands.md)): Interact with package registry and manage related configuration.
- **swift package-collection** ([SwiftPackageCollectionCommands.md](SwiftPackageCollectionCommands.md)): Interact with package collections.
- **swift run** ([SwiftRun.md](SwiftRun.md)): Build and run an executable product.

### Design

- **Swift Package Registry Service Specification** ([RegistryServerSpecification.md](RegistryServerSpecification.md)): Learn about the specification for SwiftPM's registry service.

## Usage Notes

- Documentation is organized progressively from getting started to advanced topics
- Start with the Introduction or Getting Started section
- Consult specific guides for detailed information

## License & Attribution

This skill contains content converted from DocC documentation format.
