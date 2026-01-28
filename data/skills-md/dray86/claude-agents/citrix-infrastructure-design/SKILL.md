---
name: citrix-infrastructure-design
description: Citrix infrastructure architecture and capacity planning. Use when designing Citrix environments, planning capacity, sizing components, configuring high availability, designing multi-site deployments, or planning disaster recovery. Covers architecture patterns, component sizing, redundancy design, and best practices.
---

# Citrix Infrastructure Design

## Overview

This skill provides guidance for designing and architecting Citrix infrastructure, including component sizing, high availability patterns, multi-site deployments, and disaster recovery planning.

## Architecture Patterns

### Single-Site Architecture

**Components:**
- 2+ Delivery Controllers (N+1 redundancy)
- SQL Server (AlwaysOn or mirroring)
- StoreFront server group (2-5 servers)
- NetScaler ADC HA pair
- Hypervisor cluster

**Use Cases:**
- Small to medium deployments
- Single geographic location
- Simpler management requirements

### Multi-Site Architecture

**Components per site:**
- Local Delivery Controllers
- Local StoreFront servers
- Local database replica
- Zone configuration in single site

**Cross-site components:**
- GSLB for user routing
- Database replication
- Image management strategy

**Use Cases:**
- Geographic distribution
- DR requirements
- Regional performance needs

### Citrix Cloud Hybrid

**Citrix Cloud (managed):**
- Delivery Controllers
- Site database
- Studio/Director
- Licensing
- Gateway Service

**Customer managed:**
- Cloud Connectors (2+ per location)
- VDAs and applications
- Hypervisor/cloud infrastructure
- Active Directory

**Benefits:**
- Reduced infrastructure
- Automatic updates
- Built-in redundancy

## Component Sizing

### Delivery Controllers

| VDAs | Controllers | vCPU | Memory | Notes |
|------|-------------|------|--------|-------|
| <500 | 2 | 4 | 8 GB | Minimum HA |
| 500-2500 | 2 | 4 | 8 GB | Standard |
| 2500-5000 | 3 | 8 | 16 GB | Medium |
| 5000-10000 | 4 | 8 | 16 GB | Large |
| 10000+ | 5+ | 8 | 16 GB | Enterprise |

**Placement:**
- Anti-affinity rules across hosts
- Different failure domains
- Separate from other workloads

### SQL Database

| VDAs | SQL Tier | IOPS | Notes |
|------|----------|------|-------|
| <1000 | Standard | 500 | SQL Express possible |
| 1000-3000 | Standard | 1000 | Dedicated SQL |
| 3000-5000 | Enterprise | 2000 | AlwaysOn |
| 5000+ | Enterprise | 3000+ | AlwaysOn AG |

**Database sizing:**
- Site DB: 500 MB - 2 GB
- Logging DB: Grows based on retention
- Monitoring DB: Grows based on retention

### VDA Sizing

**Single-Session (VDI):**

| Workload | vCPU | Memory | Storage IOPS |
|----------|------|--------|--------------|
| Task Worker | 2 | 4 GB | 20-30 |
| Knowledge Worker | 2-4 | 6-8 GB | 40-60 |
| Power User | 4-6 | 8-16 GB | 80-100 |

**Multi-Session (RDSH):**

| Users/Server | vCPU | Memory | Storage IOPS |
|--------------|------|--------|--------------|
| 10-15 | 8 | 32 GB | 100-150 |
| 15-25 | 12 | 48 GB | 150-200 |
| 25-40 | 16 | 64 GB | 200-300 |

### Storage Considerations

**MCS Requirements:**
- Identity disk: 16 MB per VM (fixed)
- Difference disk: 10-40 GB (grows with writes)
- Write cache: 10-20 GB SSD/NVMe recommended

**IOPS Guidelines:**
- Boot storm: 50-100 IOPS per VM (brief)
- Steady state: 5-30 IOPS per VM
- Use MCS I/O with RAM cache to reduce storage load

## High Availability Design

### Controller Redundancy

```powershell
# Local Host Cache provides outage protection
# Minimum 2 controllers per site
# Controllers share site database
# Automatic failover to LHC during outage
```

**LHC Capabilities:**
- VDA registration
- Session brokering
- Power management
- Some policy application

**LHC Limitations:**
- No new configurations
- No monitoring data
- Limited reporting

### Database HA

**SQL AlwaysOn Availability Groups (Recommended):**
- Synchronous replication within site
- Automatic failover
- Multiple readable secondaries

**SQL Mirroring:**
- Simpler setup
- Single secondary
- Manual or automatic failover

**Connection String:**
```
Server=SQLListener.domain.com;Database=CitrixSite;
MultiSubnetFailover=True;Integrated Security=True
```

### StoreFront HA

- Server group with 2-5 members
- Sub-40ms latency required
- Configuration auto-synchronized
- Load balanced via NetScaler or NLB

### NetScaler HA

- Active/Passive or Active/Active
- Synchronous configuration
- Virtual MAC for seamless failover
- Health monitoring for backend services

## Network Design

### VLAN Segmentation

| VLAN | Purpose | Access |
|------|---------|--------|
| Management | Controllers, SQL, Admin | Restricted |
| VDA | Desktop/App servers | User access |
| DMZ | Gateway, StoreFront external | Internet |
| Storage | SAN/NAS traffic | Infrastructure |

### Firewall Requirements

**User to StoreFront:**
- 443/TCP (HTTPS)

**StoreFront to Controller:**
- 80/TCP (HTTP)
- 443/TCP (HTTPS)

**User to VDA (internal):**
- 1494/TCP (ICA)
- 2598/TCP (Session Reliability)
- 443/TCP (TLS)

**VDA to Controller:**
- 80/TCP (Registration)
- 443/TCP (Secure registration)

### Bandwidth Planning

| Session Type | Bandwidth |
|-------------|-----------|
| Task worker | 50-150 Kbps |
| Office apps | 150-250 Kbps |
| Web/email | 250-500 Kbps |
| Graphics | 1-3 Mbps |
| Video | 2-5 Mbps |

## Disaster Recovery

### RTO/RPO Objectives

| Tier | RTO | RPO | Strategy |
|------|-----|-----|----------|
| 1 | <1 hr | Near-zero | Active/Active |
| 2 | 1-4 hr | <1 hr | Warm standby |
| 3 | 4-24 hr | <4 hr | Cold standby |

### Active/Active Design

- Controllers at both sites
- GSLB routes users to nearest site
- Real-time database replication
- Both sites handle production load
- Automatic failover

### Active/Passive Design

- Secondary site in standby
- Asynchronous replication acceptable
- Manual or automated failover
- Lower cost than active/active
- Longer RTO

### DR Considerations

**Non-persistent VDI advantages:**
- No VM replication needed
- Rapid provisioning at DR site
- Only master images replicated
- Lower storage costs

**Key data to replicate:**
- Site database
- Master images
- User profiles (if persistent)
- Application data

## Design Best Practices

### Scalability

1. **Design for growth** - Size for 3-5 year projection
2. **Use zones** - Separate workloads by zone
3. **Catalog organization** - Group by OS, workload, location
4. **Delivery group strategy** - Align with user groups

### Performance

1. **MCS I/O** - Use RAM cache with disk overflow
2. **Storage tiering** - SSD for write cache, HDD for read
3. **Network optimization** - EDT, Multi-Stream ICA
4. **Profile optimization** - Streaming, exclusions

### Security

1. **Segmentation** - Isolate management plane
2. **Encryption** - TLS for all communications
3. **MFA** - Required for external access
4. **Least privilege** - RBAC for administration

### Operations

1. **Monitoring** - Director, SCOM, third-party
2. **Alerting** - Proactive threshold alerts
3. **Automation** - PowerShell for routine tasks
4. **Documentation** - Architecture, runbooks, DR

## Reference Materials

For detailed design guidance, see:
- `citrix-knowledge/domain-knowledge/comprehensive-citrix-knowledge.md`
- `citrix-knowledge/architecture/` for design patterns
- `citrix-knowledge/templates/` for documentation templates
