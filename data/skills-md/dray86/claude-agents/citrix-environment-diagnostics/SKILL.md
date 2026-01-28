---
name: citrix-environment-diagnostics
description: Comprehensive Citrix environment health assessment and diagnostics. Use when analyzing Citrix site health, checking VDA registration status, verifying Delivery Controller services, assessing StoreFront availability, or performing environment audits. Covers infrastructure health, database connectivity, resource utilization, and component status verification.
---

# Citrix Environment Diagnostics

## Overview

This skill provides guidance for comprehensive Citrix environment health assessments, including VDA status, Delivery Controller health, StoreFront availability, and overall infrastructure diagnostics.

## Instructions

When performing Citrix environment diagnostics:

### 1. Verify Connectivity and Access

```powershell
# Load Citrix PowerShell snap-ins
Add-PSSnapin Citrix.* -ErrorAction SilentlyContinue

# Test connection to Delivery Controller
Get-BrokerSite
```

- Confirm PowerShell access to Delivery Controllers
- Validate administrative permissions
- Check network connectivity to all components

### 2. Assess VDA Registration Status

```powershell
# Get overall VDA registration summary
Get-BrokerMachine -MaxRecordCount 10000 |
    Group-Object RegistrationState |
    Select Name, Count

# List unregistered VDAs with details
Get-BrokerMachine -RegistrationState Unregistered |
    Select DNSName, CatalogName, LastConnectionFailure, LastDeregistrationReason

# Check VDA load distribution
Get-BrokerMachine -RegistrationState Registered |
    Select DNSName, LoadIndex, SessionCount |
    Sort LoadIndex -Descending
```

**Key metrics to verify:**
- Registration rate should be >95%
- Load index should be <8000 for healthy VDAs
- Check for patterns in failed registrations

### 3. Verify Delivery Controller Health

```powershell
# Check controller status
Get-BrokerController | Select MachineName, State, DesktopsRegistered

# Verify site database connectivity
Get-BrokerSite | Select Name, ConfigurationLoggingDatabaseName

# Check broker service status
Get-BrokerServiceStatus
```

**Validate:**
- All controllers showing "Active" state
- Database connections established
- Services running on all controllers

### 4. Assess StoreFront Status

```powershell
# On StoreFront server - check store status
Get-STFDeployment
Get-STFStoreService | Select FriendlyName, VirtualPath

# Verify authentication methods
Get-STFAuthenticationService | Select FriendlyName, VirtualPath
```

**Check:**
- Store accessibility from client networks
- Authentication provider configuration
- SSL certificate validity

### 5. Review Session and Resource Utilization

```powershell
# Active session count
Get-BrokerSession -MaxRecordCount 10000 | Measure-Object

# Sessions by delivery group
Get-BrokerSession -MaxRecordCount 10000 |
    Group-Object DesktopGroupName |
    Select Name, Count |
    Sort Count -Descending

# Machine utilization by catalog
Get-BrokerMachine -MaxRecordCount 10000 |
    Group-Object CatalogName |
    ForEach-Object {
        [PSCustomObject]@{
            Catalog = $_.Name
            Total = $_.Count
            Registered = ($_.Group | Where-Object {$_.RegistrationState -eq 'Registered'}).Count
            InUse = ($_.Group | Where-Object {$_.SessionCount -gt 0}).Count
        }
    }
```

### 6. Check Licensing Status

```powershell
# Get license server information
Get-BrokerSite | Select LicenseServerName, LicenseServerPort

# Check license usage (requires License Server access)
Get-LicInventory -LicenseServerAddress <LicenseServer> -LicenseServerPort 27000
```

### 7. Document and Report Findings

After completing diagnostics:

1. **Summary**: Overall environment health status
2. **Issues Identified**: List any problems found
3. **Metrics**: Key performance indicators
4. **Recommendations**: Remediation steps for any issues
5. **Next Steps**: Follow-up actions required

## Health Check Thresholds

| Component | Healthy | Warning | Critical |
|-----------|---------|---------|----------|
| VDA Registration | >98% | 95-98% | <95% |
| Load Index | <5000 | 5000-8000 | >8000 |
| Controller State | All Active | 1 Inactive | Multiple Inactive |
| DB Response | <100ms | 100-500ms | >500ms |

## Common Issues to Check

- **VDA Registration Failures**: Time sync, firewall, DNS resolution
- **High Load Index**: Resource contention, runaway processes
- **Controller Issues**: Service failures, database connectivity
- **StoreFront Problems**: Certificate expiry, IIS configuration

## Reference Materials

For detailed information, refer to:
- `citrix-knowledge/domain-knowledge/comprehensive-citrix-knowledge.md`
- `citrix-knowledge/runbooks/` for step-by-step procedures
- `citrix-knowledge/troubleshooting/` for common issue resolutions
