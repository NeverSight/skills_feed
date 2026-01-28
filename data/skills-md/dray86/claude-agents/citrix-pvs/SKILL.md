---
name: citrix-pvs
description: Comprehensive Citrix Provisioning Services (PVS) expertise for infrastructure management, troubleshooting, and optimization. Use when working with PVS environments including vDisk management, target device provisioning, boot process troubleshooting, write cache configuration, version management, replication, performance optimization, or any PVS-specific administration tasks.
---

# Citrix Provisioning Services (PVS) Skill

This skill provides domain-specific knowledge for Citrix Provisioning Services, enabling efficient troubleshooting, configuration, and management of PVS infrastructure that streams OS images to target devices.

## Core Architecture

### Infrastructure Components

**PVS Farm** - Top-level container holding all components with shared SQL database storing configuration including:
- Site definitions and server assignments
- Device collections and target device configurations
- vDisk definitions and version chains
- Store locations and replication settings
- Boot configuration and authentication settings

**PVS Server** - Streams vDisks to target devices running critical services:
- **Stream Service** (UDP 6910-6930) - Primary vDisk streaming to targets
- **TFTP Service** (UDP 69) - Delivers bootstrap files for network boot
- **PXE Service** (UDP 67/68, 4011) - DHCP proxy for boot information
- **SOAP Server** (TCP 54321) - Console communication and management
- **Two-Stage Boot Service** (UDP 6969) - BDM bootstrap delivery

Sizing: Each server supports 1,000-5,000 targets depending on workload (task workers scale better than general users).

**vDisk** - Read-only disk image (.vhdx format, up to 2TB) with properties file (.pvp) containing:
- Access modes (Private, Standard, Maintenance)
- Cache type and size settings
- Write cache location configuration
- Active Directory integration settings
- License mode and authentication settings

**vDisk Versions** - Differential disks (.avhdx) chained from base allowing multiple versions:
- Maintenance version - being updated, no target assignment
- Test version - limited target testing before promotion
- Production version - assigned to production targets
- Override versions - temporary testing versions with expiration

**Device Collections** - Logical groupings of target devices for management simplification enabling batch operations on maintenance mode, vDisk assignments, boot settings, and write cache configuration. Each target belongs to exactly one collection.

**Target Devices** - Physical or virtual machines booting from network via:
- PXE network boot (BIOS or UEFI)
- Boot Device Manager (BDM) ISO or partition
- Virtual hard disk with bootstrap

**vDisk Stores** - Network locations holding vDisk files supporting:
- Local server storage (low latency, no shared access)
- SMB/CIFS shares (most common, moderate performance)
- NFS shares (Linux environments)
- SAN LUNs (high performance, complexity)

### Boot Process Flow

**Phase 1: IP Acquisition** - DHCP DORA process (Discover, Offer, Request, Acknowledge) providing IP address, subnet mask, default gateway, DNS servers, and optionally TFTP server (option 66) and boot file (option 67).

**Phase 2: Bootstrap Download** via three methods:
- **PXE Boot** - PXE service provides TFTP server location and bootstrap filename, target downloads ARDBP32.BIN (BIOS) or ARDBP64.BIN (UEFI) via TFTP (UDP 69)
- **DHCP Options 66/67** - DHCP directly provides TFTP server IP and filename, eliminating PXE service requirement
- **BDM (Boot Device Manager)** - Bootstrap embedded in ISO or partition eliminating DHCP/PXE/TFTP dependencies

Bootstrap file (ARDBP32.BIN) contains:
- PVS server IP addresses (up to 4 by default, expandable)
- Login port (default 6910)
- Streaming protocol preferences
- Verbose logging flags
- Advanced connection settings

**Phase 3: PVS Login Process** (UDP 6910):
1. Target contacts PVS login server requesting connection
2. PVS responds with streaming server IP and port assignment
3. Target identifies itself via MAC address
4. PVS validates against database, replies with disk, policy, and client info
5. Target requests vDisk assignment details
6. PVS grants I/O access and provides vDisk metadata including write cache location

**Phase 4: Single-Read Mode** - Target begins streaming vDisk using basic protocol before full OS loads.

**Phase 5: BNISTACK/MIO Mode** - After OS loads BNISTACK.SYS driver, Multiple I/O communication begins with full protocol stack including sequencing, fragmentation, acknowledgements, retry mechanisms, and heartbeat monitoring.

## vDisk Management

### Creating Master Images

**Preparation workflow**:
1. Create VM with desired configuration (CPU, RAM, storage)
2. Install clean OS and apply updates
3. Install PVS Target Device software selecting correct stream method
4. Configure OS optimization (disable defrag, hibernation, system restore)
5. Install applications and updates
6. Run imaging preparation wizard removing unique identifiers
7. Shutdown cleanly without running Sysprep

**Image optimization** using Citrix Optimizer:
- Disable Windows Search indexing
- Disable Superfetch/Prefetch services
- Disable scheduled tasks (defrag, Windows Updates)
- Configure antivirus exclusions for write cache
- Set high-performance power plan
- Disable visual effects
- Configure event log sizes

**Capturing vDisk**:
1. Boot target in Private Image mode
2. Make required changes
3. Configure versioning (manual or automatic merge)
4. Switch to Standard Image or Maintenance mode
5. Promote version to Test or Production

### Access Modes

**Private Image** - Target has exclusive read/write access to vDisk for:
- Initial vDisk creation from master target
- Major updates requiring testing isolation
- Troubleshooting without affecting other targets
- Not suitable for production (no sharing)

**Standard Image** - Multiple targets stream read-only vDisk with writes redirected to cache:
- Production mode for deployed targets
- Enables image sharing across hundreds/thousands of targets
- Requires write cache configuration
- Most common operational mode

**Maintenance** - Administrators perform vDisk updates while targets boot from current version:
- Updates handled through versioning system
- No target downtime during updates
- New version tested before production promotion
- Automatic or manual merge strategies

### Versioning Strategies

**Manual versioning** provides complete control:
1. Create maintenance version
2. Boot single target in Maintenance mode
3. Make changes (updates, software installation)
4. Test maintenance version with test targets
5. Promote to Test version for broader testing
6. Promote to Production when validated
7. Merge versions to reclaim storage (optional)

**Automatic versioning** schedules regular updates:
- Define maintenance window schedule
- PVS creates new maintenance version automatically
- Apply updates during window
- Automatically promote to production on schedule
- Merge old versions based on retention policy
- Reduces administrative overhead

**Best practices**:
- Keep 2-3 production versions for quick rollback
- Test versions with pilot group before production promotion
- Document changes in version notes
- Schedule merges during low-usage periods
- Maintain base gold image separately for disaster recovery

## Write Cache Configuration

### Cache Types

**Cache on Device Hard Drive** - Local disk write cache:
- Best performance (local I/O)
- No network traffic for writes
- Lost on reboot unless persistent
- Requires local disk space
- Common for VDI with local storage

**Cache on Device Hard Drive Persisted** - Survives reboots:
- Writes preserved between sessions
- Enables Windows updates without vDisk updates
- Requires significantly more disk space
- Increases provisioning complexity
- Best for semi-persistent desktops

**Cache in Device RAM** - Memory-based cache:
- Fastest performance (RAM speed)
- No local disk required
- Lost on reboot
- Limited by available RAM
- Good for task workers with small write footprint

**Cache on Device RAM with Overflow on Hard Disk** - Hybrid approach:
- Optimal performance (RAM) with safety (disk overflow)
- Most common configuration
- Requires both RAM and disk allocation
- Automatic spillover when RAM fills
- Typical: 256MB RAM, 10GB disk overflow

**Cache on Server** - Network-based cache:
- Eliminates local storage requirement
- Poor performance (network latency)
- High network bandwidth consumption
- Not recommended for production
- Only for specific edge cases

**Cache on Server Persisted** - Network cache surviving reboots:
- Same drawbacks as non-persistent server cache
- Additional management complexity
- Higher storage requirements on PVS server
- Rarely used in modern deployments

### Cache Sizing

**Formula**: (Write Volume per Hour) × (Hours in Session) + (Safety Buffer)

**Typical sizes by workload**:
- Task workers (data entry): 2-4GB total cache
- General office users: 4-8GB total cache
- Power users (development): 8-16GB total cache
- Graphics/CAD workloads: 16-32GB total cache

**RAM allocation** (for RAM+Disk configurations):
- 128MB-256MB for task workers
- 256MB-512MB for general users
- 512MB-1GB for power users

**Monitoring considerations**:
- Track cache consumption via PVS Console Target Devices view
- Set alerts at 80% cache utilization
- Monitor cache overflow events
- Review Event Viewer System logs for cache warnings (Event ID 18, 19, 20)

## Troubleshooting Framework

### Boot Failure Diagnosis

**Symptom: Target doesn't receive IP address**
- Verify DHCP scope has available addresses
- Check DHCP server logs for DORA process
- Validate network connectivity to DHCP server
- Ensure network switch allows DHCP broadcast
- Verify VLAN configuration if applicable

**Symptom: Target gets IP but times out on TFTP**
- Verify PVS TFTP service running
- Test TFTP connectivity: `tftp <pvs-ip> GET ARDBP32.BIN`
- Check Windows Firewall allows UDP 69
- Verify bootstrap file exists in `\Provisioning Services\TFTP\` directory
- Review DHCP options 66/67 configuration

**Symptom: PXE error "No Bootstrap Found"**
- Verify PXE service running on PVS server
- Check DHCP options NOT conflicting with PXE (remove 66/67 if using PXE)
- Verify network supports PXE proxy DHCP (port 4011)
- Check BDM bootstrap exists if using Boot Device Manager
- Review PXE service log in Event Viewer

**Symptom: Target downloads bootstrap but fails PVS login**
- Verify PVS Stream Service running
- Check target exists in database with correct MAC address
- Validate UDP port 6910 not blocked by firewall
- Review bootstrap file PVS server IP addresses
- Test network connectivity to PVS streaming port: `Test-NetConnection -ComputerName <pvs-ip> -Port 6910`

**Symptom: Target connects but can't access vDisk**
- Verify vDisk assigned to device collection
- Check vDisk in Standard or Private mode (not Maintenance)
- Validate vDisk store accessible from PVS server
- Review vDisk replication status if using distributed stores
- Check vDisk not locked by another process

### Performance Issues

**Slow boot times (>2 minutes)**:
- Check network latency: Target to PVS <1ms preferred, <10ms acceptable
- Review storage latency: vDisk reads <10ms preferred, <20ms acceptable
- Verify network bandwidth: 100Mbps minimum, 1Gbps recommended
- Monitor PVS server CPU/RAM: CPU <70%, available RAM >2GB
- Check antivirus not scanning vDisk files or write cache
- Review Event Viewer for retransmit events (ID 20, 21)

**In-session performance degradation**:
- Monitor write cache utilization approaching capacity
- Check RAM cache overflow to disk
- Review network packet loss via perfmon counters
- Validate storage IOPS supporting workload
- Check for memory pressure on target device

**vDisk streaming bandwidth issues**:
- Calculate required bandwidth: (Targets × Average Throughput)
- Typical throughput: 500KB/s per target during boot, 50-100KB/s steady state
- Monitor network interface saturation on PVS server
- Check for network errors/collisions
- Consider additional PVS servers for load distribution

### Common Error Codes

**Error 1603** - vDisk file not found or inaccessible:
- Verify vDisk path in PVS Console
- Check SMB share permissions (PVS server computer account needs read)
- Validate vDisk files not corrupted
- Review store path reachability from PVS server

**Error 1605** - vDisk access denied:
- Check NTFS permissions on vDisk files
- Verify PVS Stream Service account has read access
- Review share permissions on vDisk store
- Validate no file locks on vDisk

**BSOD during boot** - Driver or hardware compatibility:
- Verify PVS Target Device software version matches server version
- Check hardware acceleration settings in vDisk properties
- Review driver compatibility with OS version
- Test with different target device hardware
- Enable verbose logging in bootstrap for detailed errors

**Connection timeout (Error 51)** - Network connectivity loss:
- Check physical network connections
- Review switch port configurations
- Validate no spanning tree issues causing delays
- Check for IP address conflicts
- Monitor for DHCP lease expiration during session

## Advanced Configuration

### High Availability

**Multiple PVS Servers**:
- Deploy minimum 2 PVS servers per site
- Configure all servers in bootstrap file (up to 4 default)
- Enable HA on vDisk stores (CIFS DFS, replicated SAN)
- Set optimal load balancing: Subnet, Fixed, or Best Effort
- Test failover by disabling one server

**Database Redundancy**:
- Use SQL Server AlwaysOn Availability Groups (preferred)
- Configure SQL Server mirroring (deprecated but supported)
- Implement SQL Server failover clustering
- Regular database backups before any vDisk changes
- Document database restore procedures

**Network Redundancy**:
- Configure NIC teaming on PVS servers
- Use multiple streaming NICs for bandwidth scaling
- Implement TFTP load balancing via NetScaler (optional)
- Separate management and streaming networks
- Monitor network utilization continuously

### Replication

**Automatic vDisk replication**:
- Configure replication trigger: immediate or scheduled
- Set replication bandwidth throttling
- Enable differential replication for efficiency
- Monitor replication status via console
- Alert on replication failures

**Manual replication**:
- Right-click vDisk, select "Replicate to servers"
- Choose target PVS servers
- Monitor progress in Audit Trail
- Verify vDisk hash matches across servers: `Get-PvsVdiskInfo`

**Best practices**:
- Replicate during off-hours to minimize impact
- Verify sufficient storage on target servers
- Monitor replication logs for errors
- Test failover after replication completes
- Document replication topology

### PowerShell Automation

**Common PVS cmdlets**:
```powershell
# Import PVS module
Add-PSSnapin Citrix.PVS.SnapIn

# Get all target devices
Get-PvsDevice

# Get device by name
Get-PvsDevice -Name "TARGET001"

# Get device status
Get-PvsDeviceStatus -DeviceName "TARGET001"

# Boot target device
Start-PvsDevice -DeviceName "TARGET001"

# Shutdown target device
Stop-PvsDevice -DeviceName "TARGET001"

# Set device to maintenance mode
Set-PvsDevice -DeviceName "TARGET001" -Enabled $false

# Get vDisk information
Get-PvsDiskInfo -DiskLocatorName "WIN10-v1"

# Create new maintenance version
New-PvsDiskVersion -DiskLocatorName "WIN10-v1" -Description "Monthly updates"

# Promote version to Test
Set-PvsDiskVersion -DiskLocatorName "WIN10-v1" -Version 2 -Access 2 # 2=Test

# Promote version to Production
Set-PvsDiskVersion -DiskLocatorName "WIN10-v1" -Version 2 -Access 0 # 0=Production

# Get server status
Get-PvsServer

# Get farm configuration
Get-PvsFarm

# Export farm configuration
Export-PvsFarm -Path "C:\PVS-Backup\farm-config.xml"

# Audit trail query
Get-PvsAuditTrail -BeginDate (Get-Date).AddDays(-7)
```

**Bulk operations**:
```powershell
# Restart all devices in collection
Get-PvsDevice -CollectionName "Accounting" | Restart-PvsDevice

# Check cache consumption across all targets
Get-PvsDevice | Get-PvsDeviceStatus | Select DeviceName, DiskCacheSize, DiskCacheUsed

# Update all devices to new vDisk version
Get-PvsDevice -CollectionName "Engineering" | Set-PvsDevice -DiskLocatorName "WIN10-v2"
```

## Operational Procedures

### Monthly Patching Workflow

1. Create new maintenance version: Version 2 created automatically or manually
2. Boot single target in Maintenance mode for version 2
3. Apply Windows updates and reboot as needed
4. Install application updates
5. Test functionality thoroughly
6. Promote to Test version
7. Assign pilot device collection to Test version
8. Monitor pilot users for 24-48 hours
9. Promote to Production when validated
10. Update all device collections to new version
11. Merge old versions after 30-day retention

### Disaster Recovery

**Backup requirements**:
- SQL database daily full backup
- vDisk base images (.vhdx) after each update
- Farm configuration export weekly: `Export-PvsFarm`
- Bootstrap files backup
- Document server configurations

**Recovery procedures**:
1. Restore SQL database from backup
2. Reinstall PVS server software
3. Import farm configuration: `Import-PvsFarm`
4. Copy vDisk files to stores
5. Regenerate bootstrap files
6. Test single target boot
7. Gradually bring collections online

### Capacity Planning

**Per-server metrics**:
- vCPU: 2-4 vCPU per 1,000 targets
- RAM: 8-16GB base + (500MB per 1,000 targets)
- Network: 1Gbps per 500-1,000 targets
- Storage IOPS: 100 IOPS per vDisk

**Scaling indicators**:
- CPU consistently >70%: Add PVS servers or reduce target count
- Network utilization >60%: Add streaming NICs or servers
- Storage latency >20ms: Optimize storage or distribute vDisks
- Boot times increasing: Review optimization and capacity

## Key Files and Logs

**Configuration files**:
- Bootstrap: `\Provisioning Services\TFTP\ARDBP32.BIN` (BIOS) or `ARDBP64.BIN` (UEFI)
- vDisk: `<StorePath>\<DiskName>.vhdx` base image
- vDisk properties: `<StorePath>\<DiskName>.pvp` configuration
- Version chain: `<StorePath>\<DiskName>v<N>.avhdx` differentials

**Log locations**:
- Stream Service: Event Viewer > Applications and Services Logs > Citrix > Provisioning Services
- Database: `C:\Program Files\Citrix\Provisioning Services\Logs\`
- SOAP Server: `C:\Program Files\Citrix\Provisioning Services\Logs\SoapServer.log`
- PXE Service: Event Viewer > System log (Source: CitrixPXE)

**Critical Event IDs**:
- 18: Write cache disk full warning (80% capacity)
- 19: Write cache disk full critical (90% capacity)
- 20: Write cache disk overflow started
- 51: Target device lost connection to PVS server
- 1603: vDisk file not found or access denied
- 1605: vDisk access denied (permissions)

**Diagnostic commands**:
```cmd
# Test TFTP connectivity
tftp <pvs-server-ip> GET ARDBP32.BIN

# Test streaming port
Test-NetConnection -ComputerName <pvs-server> -Port 6910

# Check PVS services
Get-Service Citrix* | Select Name, Status

# View bootstrap configuration
StreamProcess.exe -boot ARDBP32.BIN

# Verbose target boot logging
# Modify bootstrap: Add /v parameter for verbose logging
```

## Integration with CVAD

**XenDesktop Setup Wizard** automates:
- Master target VM creation in hypervisor
- vDisk creation from master image
- BDM partition creation and attachment
- Device collection creation
- Delivery Group integration
- Automatic provisioning of target VMs

**Machine Catalog integration**:
- PVS-provisioned catalog type in Studio
- Targets automatically registered with VDA
- Power management through CVAD
- Director monitoring of PVS targets
- Automatic target cleanup on catalog deletion

**MCS vs PVS decision factors**:
- Use MCS for: Simpler management, cloud environments, smaller deployments (<500 VMs)
- Use PVS for: Maximum scale (>1,000 VMs), network bandwidth available, existing PVS investment, complex versioning requirements

## Security Considerations

**Network security**:
- Isolate PVS streaming network from production
- Implement IPsec for vDisk streaming (optional)
- Use secure communication for SOAP (HTTPS)
- Firewall rules limiting console access
- Monitor unauthorized bootstrap downloads

**vDisk security**:
- NTFS permissions restricting vDisk file access
- SMB signing on vDisk stores
- Encryption at rest for vDisk files
- Regular security updates to vDisk images
- Audit trail monitoring for vDisk modifications

**Authentication**:
- Active Directory authentication for console access
- Role-based access control (Farm/Site/Collection Admin)
- Service account least privilege principle
- Regular password rotation for service accounts
- Multi-factor authentication for administrative access (optional)

## Performance Optimization

**Storage optimization**:
- Place vDisk base images on fastest storage tier
- Use local SSD for single-server deployments
- Implement SAN read caching
- Optimize antivirus exclusions: exclude .vhdx, .avhdx, .pvp files
- Monitor storage queue depth

**Network optimization**:
- Enable jumbo frames (MTU 9000) if infrastructure supports
- Configure RSS (Receive Side Scaling) on NICs
- Use dedicated streaming NICs separate from management
- Implement QoS for PVS traffic prioritization
- Monitor for packet fragmentation

**vDisk optimization**:
- Merge versions regularly to reduce I/O
- Compact vDisk files after merges
- Remove unused applications from master image
- Implement thin provisioning on storage
- Schedule defragmentation on vDisk stores (not vDisk itself)

**Target device optimization**:
- Adequate RAM allocation (4GB minimum, 8GB recommended)
- CPU allocation matching workload
- Write cache on local storage when possible
- Disable unnecessary Windows services
- Configure appropriate page file size
