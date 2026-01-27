---
name: powershell-7-expert
description: Expert in modern, cross-platform PowerShell Core. Specializes in Linux/macOS automation, parallel processing, REST API integration, and modern scripting patterns. Use for cross-platform automation and modern PowerShell features. Triggers include "PowerShell 7", "PowerShell Core", "pwsh", "ForEach-Object -Parallel", "cross-platform PowerShell".
---

# PowerShell 7 Expert

## Purpose
Provides expertise in modern PowerShell 7+ (PowerShell Core) for cross-platform automation. Specializes in parallel processing, REST API integration, modern scripting patterns, and leveraging new language features.

## When to Use
- Cross-platform automation (Windows, Linux, macOS)
- Parallel processing with ForEach-Object -Parallel
- REST API integrations
- Modern PowerShell scripting patterns
- Pipeline chain operators (&& ||)
- Ternary expressions and null coalescing
- SSH-based remoting
- JSON/YAML data manipulation

## Quick Start
**Invoke this skill when:**
- Writing cross-platform PowerShell scripts
- Using PowerShell 7+ specific features
- Implementing parallel processing
- Building REST API integrations
- Modernizing scripts from 5.1

**Do NOT invoke when:**
- Legacy Windows-only systems → use `/powershell-5.1-expert`
- GUI development → use `/powershell-ui-architect`
- Security configuration → use `/powershell-security-hardening`
- Module design → use `/powershell-module-architect`

## Decision Framework
```
PowerShell 7 Feature Selection?
├── Parallel Processing
│   ├── Simple iteration → ForEach-Object -Parallel
│   └── Complex workflows → Start-ThreadJob
├── API Integration
│   └── Invoke-RestMethod with modern options
├── Null Handling
│   ├── Default value → ?? operator
│   └── Conditional access → ?. operator
└── Pipeline Control
    └── && and || chain operators
```

## Core Workflows

### 1. Parallel Processing
1. Identify parallelizable workload
2. Use ForEach-Object -Parallel
3. Set -ThrottleLimit appropriately
4. Handle thread-safe data access
5. Aggregate results
6. Handle errors from parallel runs

### 2. REST API Integration
1. Construct request parameters
2. Handle authentication (Bearer, OAuth)
3. Use Invoke-RestMethod
4. Parse JSON response
5. Implement pagination
6. Add retry logic for failures

### 3. Cross-Platform Script
1. Avoid Windows-specific paths
2. Use $PSVersionTable and $IsLinux/$IsWindows
3. Handle path separators correctly
4. Test on all target platforms
5. Use compatible modules
6. Document platform requirements

## Best Practices
- Use ternary operator for concise conditionals
- Leverage null-coalescing for defaults
- Use ForEach-Object -Parallel for CPU-bound tasks
- Prefer SSH remoting over WinRM for cross-platform
- Use Join-Path for cross-platform paths
- Test on all target operating systems

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Hardcoded backslashes | Breaks on Linux/macOS | Join-Path or / |
| Windows-only cmdlets | Cross-platform failure | Check availability |
| Over-parallelization | Thread overhead | Tune ThrottleLimit |
| Ignoring $Error | Silent failures | Proper error handling |
| Assuming WinRM | Not cross-platform | SSH remoting |
