---
name: proxmox-mcp-tools
description: Comprehensive MCP tool reference for Proxmox Virtual Environment management - 92 tools across 14 domains including QEMU VMs, LXC containers, cluster operations, storage, networking, Ceph, certificates, ACME, and notifications
license: MIT
compatibility:
  - claude-code
  - opencode
  - cursor
  - codex
  - gemini-cli
  - vscode
metadata:
  version: 0.6.2
  tool_count: 92
  domains: 14
  generated: 2026-02-08
---

# Proxmox MCP Tools Reference

> **AI Agent Skill**: Complete reference for 92 Proxmox Virtual Environment management tools via Model Context Protocol

## Overview

This skill teaches AI agents how to use the **@bldg-7/proxmox-mcp** server, which provides 92 comprehensive tools for managing Proxmox VE infrastructure through the Model Context Protocol (MCP).

**What you'll learn**:
- How to connect to Proxmox VE via MCP
- 92 tools organized into 14 functional domains
- Permission model (basic vs elevated operations)
- Common workflows and patterns
- Troubleshooting API quirks

**Target audience**: AI agents managing Proxmox infrastructure, automating VM/LXC provisioning, monitoring cluster health, or performing operational tasks.

---

## Quick Start

### Connection Setup

**Required Environment Variables**:
```bash
PROXMOX_HOST=pve.example.com
PROXMOX_TOKEN_NAME=mytoken
PROXMOX_TOKEN_VALUE=abc123-def456-ghi789
```

**Optional Configuration**:
```bash
PROXMOX_USER=root@pam          # Default: root@pam
PROXMOX_SSL_MODE=verify         # strict|verify|insecure (default: strict)
PROXMOX_ALLOW_ELEVATED=true     # Enable create/modify/delete (default: false)
PROXMOX_PORT=8006               # Default: 8006
```

**SSH Configuration** (for `proxmox_lxc_exec`):
```bash
PROXMOX_SSH_ENABLED=true        # Enable SSH-based LXC exec (default: false)
PROXMOX_SSH_HOST=pve.example.com # SSH host (falls back to PROXMOX_HOST)
PROXMOX_SSH_PORT=22             # SSH port (default: 22)
PROXMOX_SSH_USER=root           # SSH username (default: root)
PROXMOX_SSH_KEY_PATH=~/.ssh/id_rsa # Path to SSH private key (required when SSH enabled)
PROXMOX_SSH_NODE=pve1           # Proxmox node name (required when SSH enabled)
PROXMOX_SSH_HOST_KEY_FINGERPRINT=sha256:... # Optional host key verification
```

### Permission Model

| Level | Operations | Env Var Required |
|-------|-----------|------------------|
| **Basic** | Read-only (list, get, status) | None |
| **Elevated** 🔒 | Create, modify, delete | `PROXMOX_ALLOW_ELEVATED=true` |

**102 basic tools** + **207 elevated tools** = **92 total**

### SSL Modes

- `strict`: Full certificate verification (production)
- `verify`: Allow self-signed certificates (common for Proxmox)
- `insecure`: No verification (development only)

---

## Tool Categories

| Domain | Tools | Key Operations | Reference |
|--------|-------|----------------|-----------|
| **Nodes** | 47 | Node status, network config, system ops, console access | [proxmox-nodes.md](references/proxmox-nodes.md) |
| **QEMU VMs** | 26 | VM lifecycle, config, disks, network, commands | [proxmox-vm.md](references/proxmox-vm.md) |
| **LXC Containers** | 20 | Container lifecycle, config, mount points, network, exec | [proxmox-lxc.md](references/proxmox-lxc.md) |
| **VM/LXC Shared** | 22 | Agent, firewall, migration (works for both) | [proxmox-vm-lxc-shared.md](references/proxmox-vm-lxc-shared.md) |
| **Snapshots & Backups** | 14 | Create/restore snapshots, backup jobs | [proxmox-snapshots-backups.md](references/proxmox-snapshots-backups.md) |
| **Storage** | 16 | Storage config, content, file operations, node disks | [proxmox-storage.md](references/proxmox-storage.md) |
| **Networking** | 20 | SDN (VNets, zones, controllers, subnets) | [proxmox-networking.md](references/proxmox-networking.md) |
| **Cluster** | 54 | HA, firewall, aliases, ipsets, backup jobs, replication, config | [proxmox-cluster.md](references/proxmox-cluster.md) |
| **Access Control** | 25 | Users, groups, roles, ACLs, domains, API tokens | [proxmox-access-control.md](references/proxmox-access-control.md) |
| **Ceph** | 16 | Ceph OSDs, MONs, MDS, pools, filesystems | [proxmox-ceph.md](references/proxmox-ceph.md) |
| **Pools** | 5 | Resource pool management | [proxmox-pools.md](references/proxmox-pools.md) |
| **Certificates** | 7 | Node certificates, custom SSL, ACME ordering | [proxmox-certificates.md](references/proxmox-certificates.md) |
| **ACME** | 8 | ACME accounts, plugins, directories | [proxmox-acme.md](references/proxmox-acme.md) |
| **Notifications** | 5 | Notification targets, SMTP/Gotify testing | [proxmox-notifications.md](references/proxmox-notifications.md) |

**Total**: 92 tools

---

## Common Workflows

### 1. Create and Configure a VM

```
1. proxmox_get_next_vmid → Get available VM ID
2. proxmox_create_vm → Create VM with basic config
3. proxmox_vm_disk → Attach storage
4. proxmox_guest_network → Configure network
5. proxmox_guest_start → Power on
6. proxmox_guest_status → Verify running
```

### 2. Clone VM for Testing

```
1. proxmox_guest_config → Review source VM
2. proxmox_guest_snapshot → Snapshot before clone
3. proxmox_guest_clone → Create clone (full or linked)
4. proxmox_guest_start → Start cloned VM
```

### 3. Backup and Restore

```
# Backup
1. proxmox_backup → Create backup to storage
2. proxmox_backup → Verify backup exists

# Restore
1. proxmox_backup → Find backup file
2. proxmox_backup → Restore to new/existing VM
```

### 4. Migrate VM Between Nodes

```
1. proxmox_node → List available target nodes
2. proxmox_guest_status → Check VM is running
3. proxmox_guest_migrate → Live or offline migration
4. proxmox_guest_status → Verify on new node
```

### 5. Configure HA for Critical VMs

```
1. proxmox_ha_group → Define node group
2. proxmox_ha_resource → Add VM to HA
3. proxmox_ha_resource → Monitor HA state
```

### 6. Monitor Cluster Health

```
1. proxmox_cluster → Overall cluster state
2. proxmox_node → Node-level health
3. proxmox_node_task → Recent operations
4. proxmox_ceph → Ceph cluster (if used)
```

### 7. Manage Storage

```
1. proxmox_storage_config → Available storage
2. proxmox_storage_content → Browse content
3. proxmox_storage_content → Upload ISO/template
4. proxmox_storage_content → Clean old backups
```

**More workflows**: See [proxmox-workflows.md](references/proxmox-workflows.md)

---

## Troubleshooting Quick Reference

### 1. Connection Refused
**Symptom**: `ECONNREFUSED` or timeout  
**Fix**: Verify `PROXMOX_HOST`, check port 8006, firewall rules

### 2. Authentication Failed
**Symptom**: `401 Unauthorized`  
**Fix**: Verify token name/value, ensure token has permissions in Proxmox

### 3. SSL Certificate Errors
**Symptom**: `UNABLE_TO_VERIFY_LEAF_SIGNATURE`  
**Fix**: Use `PROXMOX_SSL_MODE=verify` for self-signed certs

### 4. Permission Denied
**Symptom**: `🚫 Permission Denied`  
**Fix**: Set `PROXMOX_ALLOW_ELEVATED=true` for create/modify/delete operations

### 5. VM Not Found (500 instead of 404)
**Symptom**: API returns 500 error for missing VM  
**Fix**: This is a Proxmox API quirk - treat 500 as "not found" in some contexts

**More troubleshooting**: See [proxmox-troubleshooting.md](references/proxmox-troubleshooting.md)

---

## Tool Response Format

All tools return structured MCP responses:

**Success**:
```json
{
  "content": [{"type": "text", "text": "✅ Operation successful\n\n• Details..."}],
  "isError": false
}
```

**Error**:
```json
{
  "content": [{"type": "text", "text": "❌ Error: Reason..."}],
  "isError": true
}
```

**Permission Denied**:
```json
{
  "content": [{"type": "text", "text": "🚫 Permission Denied: Set PROXMOX_ALLOW_ELEVATED=true"}],
  "isError": true
}
```

---

## References

### Domain-Specific Documentation

- **[proxmox-nodes.md](references/proxmox-nodes.md)** - Node management, network config, system operations (47 tools)
- **[proxmox-vm.md](references/proxmox-vm.md)** - QEMU VM operations (26 tools)
- **[proxmox-lxc.md](references/proxmox-lxc.md)** - LXC container operations (20 tools)
- **[proxmox-vm-lxc-shared.md](references/proxmox-vm-lxc-shared.md)** - Shared VM/LXC operations (22 tools)
- **[proxmox-snapshots-backups.md](references/proxmox-snapshots-backups.md)** - Snapshots and backups (14 tools)
- **[proxmox-storage.md](references/proxmox-storage.md)** - Storage management (16 tools)
- **[proxmox-networking.md](references/proxmox-networking.md)** - SDN configuration (20 tools)
- **[proxmox-cluster.md](references/proxmox-cluster.md)** - Cluster operations (54 tools)
- **[proxmox-access-control.md](references/proxmox-access-control.md)** - Users, roles, ACLs, API tokens (25 tools)
- **[proxmox-ceph.md](references/proxmox-ceph.md)** - Ceph storage cluster (16 tools)
- **[proxmox-pools.md](references/proxmox-pools.md)** - Resource pools (5 tools)
- **[proxmox-certificates.md](references/proxmox-certificates.md)** - Certificate management (7 tools)
- **[proxmox-acme.md](references/proxmox-acme.md)** - ACME account and plugin management (8 tools)
- **[proxmox-notifications.md](references/proxmox-notifications.md)** - Notification targets (5 tools)

### Operational Guides

- **[proxmox-workflows.md](references/proxmox-workflows.md)** - Common operational patterns
- **[proxmox-troubleshooting.md](references/proxmox-troubleshooting.md)** - API quirks and solutions

---

## Usage Tips

1. **Always check permissions**: Use basic tools first, only enable elevated when needed
2. **Verify before destructive ops**: Use `get_vm_status` before `delete_vm`
3. **Use snapshots**: Create snapshot before major changes
4. **Monitor tasks**: Use `get_node_tasks` to track long-running operations
5. **Handle 500 errors**: Proxmox sometimes returns 500 instead of 404 - check context
6. **SSL mode for self-signed**: Most Proxmox installations use self-signed certs - use `verify` mode

---

## License

MIT License - Part of @bldg-7/proxmox-mcp package
