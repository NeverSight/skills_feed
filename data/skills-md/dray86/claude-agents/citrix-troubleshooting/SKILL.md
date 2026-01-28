---
name: citrix-troubleshooting
description: Systematic Citrix issue diagnosis and resolution. Use when troubleshooting VDA registration failures, session launch problems, application errors, performance issues, or connectivity problems. Provides structured troubleshooting workflows, log analysis techniques, and proven solutions for common Citrix issues.
---

# Citrix Troubleshooting

## Overview

This skill provides structured troubleshooting workflows for diagnosing and resolving Citrix infrastructure issues, including VDA problems, session failures, and performance degradation.

## Troubleshooting Methodology

### 1. Gather Information

**Initial questions to answer:**
- What is the exact error message or symptom?
- When did the issue start?
- How many users/machines are affected?
- What changed recently (updates, configs, infrastructure)?
- Is the issue reproducible?

### 2. Isolate the Problem

**Determine scope:**
- Single user vs. multiple users
- Single VDA vs. multiple VDAs
- Specific delivery group vs. entire site
- Network segment specific

## Common Issues and Resolutions

### VDA Registration Failures

**Symptoms**: VDAs showing "Unregistered" in Studio/Director

**Diagnostic steps:**
```powershell
# Check registration state and failure reason
Get-BrokerMachine -DNSName <VDAName> |
    Select RegistrationState, LastDeregistrationReason, LastDeregistrationTime

# Common reasons:
# - AgentShuttingDown
# - DesktopRestart
# - CommunicationFailure
# - BrokerError
```

**Common causes and fixes:**

1. **Time Synchronization**
   ```powershell
   # Check time on VDA
   w32tm /query /status
   # Resync
   w32tm /resync /force
   ```

2. **Firewall Issues**
   - Ports required: 80 (WCF), 443 (SSL), 1494 (ICA), 2598 (CGP)
   ```powershell
   # Test connectivity to controller
   Test-NetConnection -ComputerName <DDC> -Port 80
   ```

3. **DNS Resolution**
   ```powershell
   # Verify VDA can resolve controller FQDN
   Resolve-DnsName <DDC-FQDN>
   ```

4. **ListOfDDCs Registry**
   ```powershell
   # Check configured controllers
   Get-ItemProperty "HKLM:\SOFTWARE\Citrix\VirtualDesktopAgent" -Name ListOfDDCs
   ```

5. **Service Status**
   ```powershell
   # Check VDA services
   Get-Service -Name "BrokerAgent", "Citrix*" | Select Name, Status
   # Restart if needed
   Restart-Service BrokerAgent -Force
   ```

### Session Launch Failures

**Symptoms**: Users cannot launch desktops/apps, receive error messages

**Diagnostic steps:**
```powershell
# Check recent connection attempts
Get-BrokerConnectionLog -MaxRecordCount 50 |
    Where-Object {$_.UserName -like "*<username>*"} |
    Select BrokeringTime, MachineName, BrokeringResult, BrokeringResultDetails

# Check machine availability
Get-BrokerMachine -DNSName <VDAName> |
    Select PowerState, RegistrationState, InMaintenanceMode, SessionCount
```

**Common causes:**

1. **No Available Resources**
   - Check delivery group capacity
   - Verify machines are registered and not in maintenance

2. **User Assignment Issues**
   ```powershell
   # Check user's assigned machines (for static assignment)
   Get-BrokerUser -Name "DOMAIN\username" | Select AssociatedMachines
   ```

3. **Profile Issues**
   - Check Profile Management logs
   - Verify profile path accessibility
   - Check for corrupt profile

4. **Application Issues**
   ```powershell
   # Verify published app exists and is enabled
   Get-BrokerApplication -Name "*<appname>*" |
       Select Name, Enabled, AssociatedDesktopGroupNames
   ```

### Slow Session Performance

**Symptoms**: Laggy sessions, slow application response

**Diagnostic areas:**

1. **Network Latency**
   ```powershell
   # Check from client to VDA
   Test-Connection -ComputerName <VDA> -Count 10 | Measure-Object -Property ResponseTime -Average
   ```

2. **VDA Resource Utilization**
   ```powershell
   # Check load index
   Get-BrokerMachine -DNSName <VDAName> | Select LoadIndex, LoadIndexes

   # Check CPU/Memory on VDA
   Get-Counter '\Processor(_Total)\% Processor Time','\Memory\% Committed Bytes In Use'
   ```

3. **HDX Policy Settings**
   - Review visual quality settings
   - Check compression policies
   - Verify bandwidth limits

4. **Graphics Mode**
   - Check if hardware graphics needed
   - Review GPU assignment for HDX 3D Pro

### StoreFront Issues

**Symptoms**: Cannot enumerate apps, login failures, store unavailable

**Diagnostic steps:**

1. **IIS Status**
   ```powershell
   # Check IIS service
   Get-Service W3SVC | Select Status

   # Check application pools
   Get-WebAppPoolState
   ```

2. **Store Configuration**
   ```powershell
   # On StoreFront server
   Get-STFStoreService | Select VirtualPath, FarmName

   # Check farm configuration
   Get-STFStoreFarm -StoreService (Get-STFStoreService)
   ```

3. **Certificate Issues**
   - Verify SSL certificate validity
   - Check certificate binding in IIS
   - Ensure certificate chain is complete

4. **Authentication Problems**
   ```powershell
   # Check auth methods
   Get-STFAuthenticationService | Select FriendlyName, ClaimsFactoryNames
   ```

### Printing Issues

**Symptoms**: Printers not mapping, slow printing, print jobs failing

**Common resolutions:**

1. **Universal Print Driver**
   - Verify UPD is installed on VDA
   - Check auto-creation policies

2. **Client Printer Mapping**
   ```powershell
   # Check policy for printer mapping
   # Studio > Policies > User Settings > ICA > Printing
   ```

3. **Print Spooler**
   ```powershell
   # Restart spooler on VDA
   Restart-Service Spooler
   ```

## Log Analysis

### Key Log Locations

| Component | Log Location |
|-----------|-------------|
| VDA | `%PROGRAMDATA%\Citrix\VirtualDesktopAgent\Logs` |
| CDF Traces | `%PROGRAMDATA%\Citrix\CDF` |
| Broker | `C:\ProgramData\Citrix\DesktopServer\Log` |
| StoreFront | `C:\Program Files\Citrix\Receiver StoreFront\admin\Trace` |

### Enable Verbose Logging

```powershell
# Enable CDF tracing
# Use CDFControl utility or:
logman create trace CitrixTrace -p Citrix-DesktopService -o C:\Traces\citrix.etl
logman start CitrixTrace
# Reproduce issue
logman stop CitrixTrace
```

### Log Analysis Commands

```powershell
# Search for errors in event log
Get-WinEvent -LogName Application -MaxEvents 100 |
    Where-Object {$_.ProviderName -like "*Citrix*" -and $_.LevelDisplayName -eq "Error"}

# Parse broker log for errors
Select-String -Path "C:\ProgramData\Citrix\DesktopServer\Log\*.log" -Pattern "ERROR|Exception"
```

## Escalation Criteria

Escalate to Citrix Support when:
- Multiple controllers showing issues simultaneously
- Database corruption suspected
- Site-wide outage
- Issue persists after all standard troubleshooting
- Error messages reference internal/unexpected exceptions

## Reference Materials

For detailed troubleshooting procedures, see:
- `citrix-knowledge/troubleshooting/` for documented issue resolutions
- `citrix-knowledge/runbooks/` for step-by-step procedures
- `citrix-knowledge/domain-knowledge/comprehensive-citrix-knowledge.md` for product knowledge
