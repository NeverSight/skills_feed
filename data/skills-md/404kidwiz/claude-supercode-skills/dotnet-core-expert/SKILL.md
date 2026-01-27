---
name: dotnet-core-expert
description: .NET 8 cross-platform specialist with expertise in MAUI, EF Core, and modern C# development. Use when building cross-platform .NET apps, working with .NET MAUI, or developing applications for multiple operating systems.
---

# .NET Core Expert

## Purpose
Provides expertise in cross-platform .NET development, including .NET MAUI for mobile/desktop, cross-platform console applications, and cloud-native .NET services. Covers .NET 8 features and cross-platform deployment.

## When to Use
- Building cross-platform .NET applications
- Developing with .NET MAUI (mobile/desktop)
- Creating cross-platform console tools
- Deploying .NET to Linux containers
- Building cloud-native .NET services
- Cross-platform file and process handling
- Using .NET Native AOT compilation

## Quick Start
**Invoke this skill when:**
- Building cross-platform .NET applications
- Developing with .NET MAUI
- Creating cross-platform console tools
- Deploying .NET to Linux containers
- Using .NET Native AOT compilation

**Do NOT invoke when:**
- Windows-only WPF/WinForms (use windows-app-developer)
- Legacy .NET Framework (use dotnet-framework-4.8-expert)
- Web APIs specifically (use csharp-developer)
- Azure infrastructure (use azure-infra-engineer)

## Decision Framework
```
Cross-Platform UI:
├── Mobile + Desktop → .NET MAUI
├── Desktop only → Avalonia or MAUI
├── Web → Blazor
└── Console → Cross-platform console app

Deployment Target:
├── Linux containers → Self-contained, Alpine
├── Windows service → Worker service
├── macOS app → .NET MAUI or Avalonia
├── Single file → Publish single-file
└── Fast startup → Native AOT
```

## Core Workflows

### 1. .NET MAUI App Setup
1. Create MAUI project from template
2. Configure target platforms
3. Set up MVVM architecture
4. Implement platform-specific code
5. Add handlers for native features
6. Configure app lifecycle
7. Test on each platform

### 2. Cross-Platform Deployment
1. Configure RuntimeIdentifiers
2. Choose self-contained or framework-dependent
3. Set up trimming if needed
4. Handle platform-specific paths
5. Package for each platform
6. Test on target OS

### 3. Native AOT Compilation
1. Enable PublishAot in project
2. Review AOT compatibility
3. Handle reflection limitations
4. Test trimmed application
5. Verify startup performance
6. Deploy optimized binary

## Best Practices
- Use Path.Combine for cross-platform paths
- Check RuntimeInformation.IsOSPlatform
- Use conditional compilation sparingly
- Test on all target platforms
- Use cross-platform abstractions
- Handle line endings properly

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Windows paths | Breaks on Linux/Mac | Use Path.Combine |
| P/Invoke everywhere | Platform-specific | Use cross-platform APIs |
| Ignoring case sensitivity | Fails on Linux | Consistent casing |
| Untested on targets | Runtime failures | CI for each platform |
| Heavy reflection with AOT | Trimming breaks app | Use source generators |
