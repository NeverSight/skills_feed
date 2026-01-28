---
name: citrix-storefront-deployment
description: StoreFront deployment planning, configuration, and security hardening. Use when planning StoreFront infrastructure, configuring stores and authentication, setting up server groups, implementing SSL/TLS, or troubleshooting StoreFront connectivity issues. Covers architecture patterns, high availability, and operational procedures.
---

# Citrix StoreFront Deployment

## Overview

This skill provides guidance for planning, deploying, and configuring Citrix StoreFront infrastructure, including store configuration, authentication setup, high availability, and security hardening.

## Architecture Considerations

### Deployment Models

**Single Server**
- Suitable for small environments (<500 users)
- No built-in redundancy
- Simple management

**Server Group**
- 2-5 servers recommended for HA
- Servers must be within 40ms latency
- Configuration synchronized automatically
- Load balanced via NetScaler or NLB

**Multi-Site**
- Separate server groups per location
- Optimal aggregation and roaming
- Global Server Load Balancing (GSLB)

### Sizing Guidelines

| Users | Servers | CPU | Memory |
|-------|---------|-----|--------|
| <500 | 1 | 4 vCPU | 4 GB |
| 500-2000 | 2 | 4 vCPU | 8 GB |
| 2000-5000 | 3 | 8 vCPU | 8 GB |
| 5000+ | 4-5 | 8 vCPU | 16 GB |

## Deployment Instructions

### Prerequisites

1. **Server Requirements**
   - Windows Server 2016/2019/2022
   - .NET Framework 4.7.2+
   - IIS with required role services
   - Domain joined (recommended)

2. **Network Requirements**
   - Static IP address
   - DNS records (A and optionally SRV)
   - Firewall rules for ports 80/443
   - Access to Delivery Controllers

3. **Certificates**
   - SSL certificate from trusted CA
   - Include all DNS names (SAN)
   - Proper certificate chain installed

### Installation Steps

1. **Install StoreFront**
   ```powershell
   # Mount Citrix ISO and run installer
   # Select StoreFront role
   # Default installation path: C:\Program Files\Citrix\Receiver StoreFront
   ```

2. **Initial Configuration**
   - Launch StoreFront Console
   - Create new deployment
   - Specify base URL (HTTPS recommended)
   - Configure store

3. **Add Delivery Controllers**
   ```powershell
   # PowerShell configuration
   $storeService = Get-STFStoreService -VirtualPath "/Citrix/Store"
   Add-STFStoreFarm -StoreService $storeService `
       -FarmName "Production" `
       -FarmType XenDesktop `
       -Servers @("DDC1.domain.com", "DDC2.domain.com") `
       -LoadBalance $true `
       -Port 443 `
       -TransportType HTTPS
   ```

### Store Configuration

```powershell
# Get store service
$store = Get-STFStoreService -VirtualPath "/Citrix/Store"

# Configure store settings
Set-STFStoreService -StoreService $store `
    -LockedDown $true `
    -AllowSessionReconnect $true

# Configure subscription store (favorites)
Enable-STFStorePna -StoreService $store `
    -AllowUserPasswordChange $true
```

### Authentication Configuration

```powershell
# Get authentication service
$auth = Get-STFAuthenticationService -VirtualPath "/Citrix/StoreAuth"

# Enable authentication methods
Enable-STFAuthenticationServiceProtocol -AuthenticationService $auth `
    -Name "ExplicitForms"

# For pass-through authentication
Enable-STFAuthenticationServiceProtocol -AuthenticationService $auth `
    -Name "IntegratedWindows"

# Configure two-factor (requires Gateway)
Enable-STFAuthenticationServiceProtocol -AuthenticationService $auth `
    -Name "CitrixAGBasic"
```

### Server Group Configuration

```powershell
# On primary server - get cluster configuration
$cluster = Get-STFClusterConfiguration

# On secondary server - join group
Start-STFServerGroupJoin -AuthorizerHostName "PRIMARY-SF.domain.com" `
    -Confirm:$false

# Verify group membership
Get-STFServerGroup

# Propagate configuration changes
Publish-STFServerGroupConfiguration -Confirm:$false
```

## High Availability

### Load Balancing Options

**NetScaler ADC (Recommended)**
- Layer 7 load balancing
- Health monitoring
- SSL offloading
- Session persistence

**Windows NLB**
- Built-in Windows feature
- Layer 4 load balancing
- Simpler setup
- Limited health checks

### NetScaler Configuration

```
# StoreFront Service Group
add serviceGroup sg_storefront SSL
bind serviceGroup sg_storefront SF1.domain.com 443
bind serviceGroup sg_storefront SF2.domain.com 443

# Monitor
add lb monitor mon_storefront STOREFRONT -storename "Store"
bind serviceGroup sg_storefront -monitorName mon_storefront

# Virtual Server
add lb vserver vs_storefront SSL 10.0.0.100 443
bind lb vserver vs_storefront sg_storefront
set lb vserver vs_storefront -persistenceType COOKIEINSERT
```

## Security Hardening

### SSL/TLS Configuration

```powershell
# Require HTTPS
Set-STFWebReceiverCommunication -WebReceiverService $receiver `
    -RequiredLaunchProtocol "HTTPS"

# Configure strong ciphers via IIS/Registry
# Disable TLS 1.0, 1.1
# Enable TLS 1.2, 1.3
```

### IIS Hardening

- Remove default IIS headers
- Configure custom error pages
- Enable request filtering
- Set appropriate timeouts
- Enable logging

### Access Control

```powershell
# Configure allowed access methods
Set-STFStoreService -StoreService $store `
    -LockedDown $true

# Restrict to specific user groups
# Configure via Delivery Controller
```

## Troubleshooting

### Common Issues

1. **Store not accessible**
   - Check IIS application pool running
   - Verify DNS resolution
   - Check SSL certificate binding
   - Review firewall rules

2. **Applications not enumerating**
   - Verify Delivery Controller connectivity
   - Check farm configuration
   - Review StoreFront event logs
   - Test XML service on controllers

3. **Authentication failures**
   - Verify AD connectivity
   - Check time synchronization
   - Review auth service configuration
   - Check event logs for errors

### Log Locations

- **Admin logs**: `C:\Program Files\Citrix\Receiver StoreFront\admin\Trace`
- **Store logs**: `C:\Program Files\Citrix\Receiver StoreFront\services\Trace`
- **Event Viewer**: Applications > Citrix Delivery Services

### Diagnostic Commands

```powershell
# Export configuration
Export-STFConfiguration -Path "C:\Backup\sf-config.zip"

# Test farm connectivity
Test-STFStoreFarm -StoreService $store

# Check service status
Get-STFDeployment | Format-List *
```

## Reference Materials

For detailed StoreFront information, see:
- `citrix-knowledge/domain-knowledge/comprehensive-citrix-knowledge.md`
- `citrix-knowledge/runbooks/` for operational procedures
