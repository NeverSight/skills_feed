---
name: powershell-module-architect
description: Use when user needs PowerShell module design, function structure, reusable libraries, profile optimization, or cross-version compatibility across PowerShell 5.1 and PowerShell 7+.
---

# PowerShell Module Architect

## Purpose

Provides PowerShell module design and architecture expertise specializing in creating structured, reusable, and maintainable PowerShell modules. Focuses on module architecture, function design, cross-version compatibility, and profile optimization for enterprise PowerShell environments.

## When to Use

- Transforming scattered scripts into structured, reusable modules
- Designing module architecture with public/private function separation
- Creating cross-version compatible modules (PowerShell 5.1 & 7+)
- Optimizing PowerShell profiles for faster load times
- Building advanced functions with proper parameter validation

## Quick Start

**Invoke this skill when:**
- Transforming scattered scripts into structured, reusable modules
- Designing module architecture with public/private function separation
- Creating cross-version compatible modules (PowerShell 5.1 & 7+)
- Optimizing PowerShell profiles for faster load times
- Building advanced functions with proper parameter validation

**Do NOT invoke when:**
- Simple one-off scripts that won't be reused (use powershell-5.1-expert or powershell-7-expert)
- Already have well-structured modules needing functionality additions (use relevant domain skill)
- UI development (use powershell-ui-architect instead)
- Security hardening (use powershell-security-hardening instead)

## Decision Framework

### When to Create a Module

| Scenario | Recommendation |
|----------|----------------|
| 3+ related functions | Create module |
| Cross-team sharing needed | Create module + manifest |
| Single-use automation | Keep as script |
| Complex parameter sets | Advanced function in module |
| Version compatibility needed | Module with compatibility layer |

### Module Structure Decision

```
Script Organization Need
│
├─ Few related functions (3-10)?
│  └─ Single .psm1 with inline functions
│
├─ Many functions (10+)?
│  └─ Dot-source pattern (Public/Private folders)
│
├─ Publishing to gallery?
│  └─ Full manifest + tests + docs
│
└─ Team collaboration?
   └─ Git repo + CI/CD + Pester tests
```

## Core Workflow: Transform Scripts into Module

**Use case:** Refactor 10-50 scattered .ps1 scripts into organized module

### Step 1: Analysis

```powershell
# Inventory existing scripts
$scripts = Get-ChildItem -Path ./scripts -Filter *.ps1 -Recurse

# Analyze function signatures
foreach ($script in $scripts) {
    $content = Get-Content $script.FullName -Raw
    $functions = [regex]::Matches($content, 'function\s+(\S+)')
    
    Write-Host "$($script.Name): $($functions.Count) functions"
}

# Expected output:
# AD-UserManagement.ps1: 12 functions
# AD-GroupManagement.ps1: 8 functions
# Common-Helpers.ps1: 15 functions (candidates for Private/)
```

### Step 2: Design Module Structure

```powershell
# Create module skeleton
$moduleName = "Organization.ActiveDirectory"
$modulePath = "./modules/$moduleName"

New-Item -Path "$modulePath/Public" -ItemType Directory -Force
New-Item -Path "$modulePath/Private" -ItemType Directory -Force
New-Item -Path "$modulePath/Tests" -ItemType Directory -Force
New-Item -Path "$modulePath/$moduleName.psm1" -ItemType File -Force
New-Item -Path "$modulePath/$moduleName.psd1" -ItemType File -Force
```

### Step 3: Categorize Functions

```
Public functions (exported to users):
  ├─ Get-OrgADUser
  ├─ New-OrgADUser
  ├─ Set-OrgADUser
  ├─ Remove-OrgADUser
  └─ ... (user-facing functions)

Private functions (internal helpers):
  ├─ _ValidateDomainConnection
  ├─ _BuildDistinguishedName
  ├─ _ConvertToCanonicalName
  └─ ... (utility functions)
```

### Step 4: Implement Module File

```powershell
# Organization.ActiveDirectory.psm1

# Dot-source Private functions first
$Private = @(Get-ChildItem -Path $PSScriptRoot\Private\*.ps1 -ErrorAction SilentlyContinue)
foreach ($import in $Private) {
    try {
        . $import.FullName
    } catch {
        Write-Error "Failed to import private function $($import.FullName): $_"
    }
}

# Dot-source Public functions
$Public = @(Get-ChildItem -Path $PSScriptRoot\Public\*.ps1 -ErrorAction SilentlyContinue)
foreach ($import in $Public) {
    try {
        . $import.FullName
    } catch {
        Write-Error "Failed to import public function $($import.FullName): $_"
    }
}

# Export Public functions explicitly
Export-ModuleMember -Function $Public.BaseName
```

### Step 5: Create Module Manifest

```powershell
# Generate manifest
$manifestParams = @{
    Path              = "$modulePath/$moduleName.psd1"
    RootModule        = "$moduleName.psm1"
    ModuleVersion     = '1.0.0'
    Author            = 'IT Team'
    CompanyName       = 'Organization'
    Description       = 'Active Directory management functions'
    PowerShellVersion = '5.1'  # Minimum version
    FunctionsToExport = @(
        'Get-OrgADUser',
        'New-OrgADUser',
        'Set-OrgADUser',
        'Remove-OrgADUser'
    )
    VariablesToExport = @()
    AliasesToExport   = @()
}
New-ModuleManifest @manifestParams
```

### Step 6: Add Pester Tests

```powershell
# Tests/Module.Tests.ps1
BeforeAll {
    Import-Module "$PSScriptRoot/../Organization.ActiveDirectory.psd1" -Force
}

Describe "Organization.ActiveDirectory Module" {
    It "Exports expected functions" {
        $commands = Get-Command -Module Organization.ActiveDirectory
        $commands.Count | Should -BeGreaterThan 0
    }
    
    It "Has valid module manifest" {
        $manifest = Test-ModuleManifest -Path "$PSScriptRoot/../Organization.ActiveDirectory.psd1"
        $manifest.Version | Should -Be '1.0.0'
    }
}

Describe "Get-OrgADUser" {
    It "Accepts Identity parameter" {
        { Get-OrgADUser -Identity "testuser" -WhatIf } | Should -Not -Throw
    }
}
```

## Quick Reference: Advanced Function Template

```powershell
function Get-OrgUser {
    <#
    .SYNOPSIS
        Retrieves Active Directory user by name.
    
    .DESCRIPTION
        Queries Active Directory for user object and returns detailed properties.
    
    .PARAMETER Name
        The username or SamAccountName to search for.
    
    .EXAMPLE
        Get-OrgUser -Name "jdoe"
        
        Returns all properties for user jdoe.
    
    .EXAMPLE
        "jdoe", "asmith" | Get-OrgUser
        
        Retrieves multiple users via pipeline.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [ValidateNotNullOrEmpty()]
        [string]$Name
    )
    
    process {
        Get-ADUser -Identity $Name -Properties *
    }
}
```

## Integration Patterns

### powershell-5.1-expert
- **Handoff**: Module architecture designed → 5.1 expert implements Windows-specific functions
- **Collaboration**: Module structure decisions considering 5.1 compatibility

### powershell-7-expert
- **Handoff**: Module structure defined → 7 expert adds modern syntax optimizations
- **Collaboration**: Dual-mode functions using version detection

### windows-infra-admin
- **Handoff**: Module architecture → Windows admin implements domain-specific logic
- **Shared responsibility**: Active Directory, GPO, DNS module functions

### azure-infra-engineer
- **Handoff**: Module patterns → Azure engineer builds cloud automation modules
- **Integration**: Cross-cloud modules combining on-prem & Azure

## Red Flags - When to Escalate

| Observation | Action |
|-------------|--------|
| 100+ functions in single module | Consider splitting into sub-modules |
| Complex cross-version issues | Consult powershell-5.1 and 7 experts |
| Performance <1s profile load | Apply lazy loading patterns |
| Security-sensitive operations | Involve powershell-security-hardening |

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
  - Profile optimization workflow
  - Module manifest template
  - Dynamic parameters pattern
  
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
  - Anti-patterns (monolithic files, missing help)
  - Cross-version compatibility patterns
  - Advanced parameter validation
