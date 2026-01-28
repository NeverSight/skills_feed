---
name: programming-swift-embedded
description: Provides the complete Embedded Swift documentation for developing on microcontrollers, embedded systems, and baremetal applications.
---

# Embedded Swift

Embedded Swift is a compilation and language mode that enables development of baremetal, embedded and standalone software in Swift

## Documentation Structure

### Getting Started

- **Introduction to Embedded Swift** ([GettingStarted/Introduction.md](GettingStarted/Introduction.md)): Write Swift code for microcontrollers, embedded systems, and bare-metal applications
- **Language subset** ([GettingStarted/LanguageSubset.md](GettingStarted/LanguageSubset.md)): Details of the Embedded Swift language subset compared to full Swift
- **Install Embedded Swift** ([GettingStarted/InstallEmbeddedSwift.md](GettingStarted/InstallEmbeddedSwift.md)): Get the tools needed to use Embedded Swift

### Guided Examples

- **Getting started with Embedded Swift** ([GettingStarted/WaysToGetStarted.md](GettingStarted/WaysToGetStarted.md)): Possible directions to explore to start using Embedded Swift
- **Try out Embedded Swift on macOS** ([GuidedExamples/macOSGuide.md](GuidedExamples/macOSGuide.md)): Tutorial for building a simple program for your host OS with Embedded Swift
- **Raspberry Pi Pico Blink (Pico SDK)** ([GuidedExamples/PicoGuide.md](GuidedExamples/PicoGuide.md)): Tutorial for targetting a Raspberry Pi Pico as an embedded device that runs a simple Swift program
- **Baremetal Setup for STM32 with Embedded Swift** ([GuidedExamples/STM32BaremetalGuide.md](GuidedExamples/STM32BaremetalGuide.md)): Program a STM32 microcontroller directly with low-level Swift code

### Using Embedded Swift

- **Basics of using Embedded Swift** ([UsingEmbeddedSwift/Basics.md](UsingEmbeddedSwift/Basics.md)): Basic information for using Embedded Swift in typical embedded projects
- **Strings** ([UsingEmbeddedSwift/Strings.md](UsingEmbeddedSwift/Strings.md)): How to enable full Unicode-compliant string support in Embedded Swift
- **Conditionalizing compilation for Embedded Swift** ([UsingEmbeddedSwift/ConditionalCompilation.md](UsingEmbeddedSwift/ConditionalCompilation.md)): How to share code between Embedded Swift and full Swift using conditional compilation
- **Libraries and modules in Embedded Swift** ([UsingEmbeddedSwift/Libraries.md](UsingEmbeddedSwift/Libraries.md)): Understand the library setup and linkage model of Embedded Swift
- **External dependencies** ([UsingEmbeddedSwift/ExternalDependencies.md](UsingEmbeddedSwift/ExternalDependencies.md)): What external system dependencies should you expect from Embedded Swift compilations
- **Existentials** ([UsingEmbeddedSwift/Existentials.md](UsingEmbeddedSwift/Existentials.md)): Restrictions on existentials ("any" types) that apply in Embedded Swift
- **Non-final generic methods** ([UsingEmbeddedSwift/NonFinalGenericMethods.md](UsingEmbeddedSwift/NonFinalGenericMethods.md)): Restrictions on unbound generic methods that apply in Embedded Swift

### Build System Support

- **Integrate with Bazel** ([BuildSystemSupport/IntegrateWithBazel.md-wip](BuildSystemSupport/IntegrateWithBazel.md-wip)): *(Work in Progress)*
- **Integrate with CMake** ([BuildSystemSupport/IntegrateWithCMake.md-wip](BuildSystemSupport/IntegrateWithCMake.md-wip)): *(Work in Progress)*
- **Integrate with Make** ([BuildSystemSupport/IntegrateWithMake.md-wip](BuildSystemSupport/IntegrateWithMake.md-wip)): *(Work in Progress)*
- **Integrate with SwiftPM** ([BuildSystemSupport/IntegrateWithSwiftPM.md-wip](BuildSystemSupport/IntegrateWithSwiftPM.md-wip)): *(Work in Progress)*
- **Integrate with Xcode** ([BuildSystemSupport/IntegrateWithXcode.md-wip](BuildSystemSupport/IntegrateWithXcode.md-wip)): *(Work in Progress)*

### SDK Support

- **Integrating with embedded platforms** ([SDKSupport/IntegratingWithPlatforms.md](SDKSupport/IntegratingWithPlatforms.md)): Understand the common patterns and approaches for integrating Swift with existing embedded systems
- **Baremetal use of Embedded Swift** ([SDKSupport/Baremetal.md](SDKSupport/Baremetal.md)): Programming without an SDK for maximum control and minimal size
- **ESP IDF** ([SDKSupport/IntegrateWithESP.md-wip](SDKSupport/IntegrateWithESP.md-wip)): *(Work in Progress)*
- **Raspberry Pi Pico SDK** ([SDKSupport/IntegrateWithPico.md](SDKSupport/IntegrateWithPico.md)): Setting up a project that can seamlessly use C APIs from the Pico SDK.
- **Zephyr RTOS SDK** ([SDKSupport/IntegrateWithZephyr.md](SDKSupport/IntegrateWithZephyr.md)): Integrating Swift with Zephyr RTOS for embedded systems development

### Compiler Development and Details

- **ABI of Embedded Swift** ([CompilerDetails/ABI.md](CompilerDetails/ABI.md)): Understanding the different ABI (Application Binary Interface) for Embedded Swift
- **Implementation Status** ([CompilerDetails/Status.md](CompilerDetails/Status.md)): Implementation status of compiler and language features in Embedded Swift, comparison to standard Swift

## Usage Notes

- Documentation is organized progressively from getting started to advanced topics
- Start with the Introduction or Getting Started section
- Consult specific guides for detailed information

## License & Attribution

This skill contains content converted from DocC documentation format.
