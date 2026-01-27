---
name: powershell-security-hardening
description: Expert in Windows security hardening and PowerShell security configuration. Specializes in securing automation, enforcing least privilege, and aligning with enterprise security baselines. Use for securing PowerShell environments and Windows systems. Triggers include "PowerShell security", "constrained language mode", "JEA", "execution policy", "security baseline", "PowerShell logging".
---

# PowerShell Security Hardening

## Purpose
Provides expertise in Windows security hardening and PowerShell security configuration. Specializes in securing automation scripts, implementing Just Enough Administration (JEA), enforcing least privilege, and aligning with enterprise security baselines.

## When to Use
- Configuring PowerShell security policies
- Implementing Constrained Language Mode
- Setting up Just Enough Administration (JEA)
- Enabling PowerShell logging and auditing
- Securing automation credentials
- Applying CIS/STIG baselines
- Protecting against PowerShell attacks
- Implementing execution policies

## Quick Start
**Invoke this skill when:**
- Hardening PowerShell environments
- Implementing JEA or constrained language mode
- Configuring PowerShell logging
- Securing automation credentials
- Applying security baselines

**Do NOT invoke when:**
- General Windows administration → use `/windows-infra-admin`
- PowerShell development → use `/powershell-7-expert`
- Active Directory security → use `/ad-security-reviewer`
- Network security → use `/network-engineer`

## Decision Framework
```
Security Requirement?
├── Script Execution Control
│   ├── Basic → Execution Policy
│   └── Strict → AppLocker/WDAC
├── Language Restriction
│   └── Constrained Language Mode
├── Privilege Reduction
│   └── JEA (Just Enough Administration)
└── Auditing
    └── Script Block Logging + Transcription
```

## Core Workflows

### 1. PowerShell Logging Setup
1. Enable Script Block Logging via GPO
2. Enable Module Logging for key modules
3. Configure transcription to secure location
4. Set up protected event log forwarding
5. Create alerts for suspicious patterns
6. Test logging with sample scripts

### 2. JEA Configuration
1. Define role capabilities file
2. Specify allowed cmdlets and parameters
3. Create session configuration
4. Register JEA endpoint
5. Test with limited user account
6. Document role assignments

### 3. Constrained Language Mode
1. Assess application requirements
2. Create AppLocker/WDAC policy
3. Enable CLM for untrusted scripts
4. Whitelist required scripts
5. Test application functionality
6. Monitor for bypass attempts

## Best Practices
- Enable script block logging on all systems
- Use JEA instead of full admin rights
- Store credentials in secure vault (not scripts)
- Apply AMSI for malware detection
- Use signed scripts with AllSigned policy
- Regularly audit PowerShell usage logs

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Credentials in scripts | Exposure risk | SecretManagement vault |
| Disabled logging | No visibility | Enable all logging |
| Bypass execution policy | Security theater | AppLocker/WDAC |
| Full admin for automation | Over-privileged | JEA with minimal rights |
| Ignoring AMSI | Malware blind spot | Keep AMSI enabled |
