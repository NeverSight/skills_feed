---
name: proxmox-admin
description: Use when administering Proxmox VE hosts, creating and managing VMs with qm, managing LXC containers with pct, configuring storage, networking, clusters, and automating provisioning tasks via the Proxmox CLI.
license: MIT
metadata:
  author: github.com/bastos
  version: "1.0"
---

# Proxmox VE Administration

## Overview

Proxmox VE is a server virtualization platform built on Debian. It manages KVM virtual machines and LXC containers through a web UI or CLI tools. This skill covers CLI-based administration using `qm` (VMs), `pct` (containers), and supporting utilities.

## When to Use

- Creating, configuring, or managing KVM virtual machines
- Spawning and administering LXC containers
- Managing Proxmox storage, networking, or clustering
- Automating VM/container provisioning via scripts
- Troubleshooting Proxmox host or guest issues

**Not for:** Web UI-only workflows (use the CLI equivalents below).

## Quick Reference

| Tool | Purpose |
|------|---------|
| `qm` | Manage KVM virtual machines |
| `pct` | Manage LXC containers |
| `pvesm` | Manage storage |
| `pvecm` | Manage cluster |
| `pveam` | Manage appliance/template downloads |
| `pvesh` | Access the Proxmox API from the shell |
| `pveperf` | Benchmark host performance |

## VM Management with `qm`

### Creating a VM

```bash
# Create a VM with ID 100
qm create 100 --name my-vm --memory 2048 --cores 2 --sockets 1 \
  --net0 virtio,bridge=vmbr0 --ostype l26

# Create with SCSI disk on local-lvm storage (32GB)
qm create 100 --name my-vm --memory 4096 --cores 4 \
  --scsi0 local-lvm:32 --scsihw virtio-scsi-pci \
  --net0 virtio,bridge=vmbr0 --ostype l26

# Attach an ISO for installation
qm set 100 --cdrom local:iso/ubuntu-22.04-server.iso --boot order=ide2
```

### VM Lifecycle

| Command | Purpose |
|---------|---------|
| `qm start <vmid>` | Start a VM |
| `qm shutdown <vmid>` | Graceful ACPI shutdown |
| `qm stop <vmid>` | Force stop (like pulling power) |
| `qm reboot <vmid>` | Reboot a VM |
| `qm reset <vmid>` | Hard reset |
| `qm suspend <vmid>` | Suspend to RAM |
| `qm resume <vmid>` | Resume from suspend |
| `qm destroy <vmid>` | Delete VM and its disks |
| `qm destroy <vmid> --purge` | Delete VM, disks, and all related jobs |

### VM Configuration

```bash
# Show current config
qm config 100

# Modify hardware
qm set 100 --memory 8192
qm set 100 --cores 4
qm set 100 --balloon 2048          # dynamic memory (min)
qm set 100 --cpu cputype=host      # pass through host CPU features
qm set 100 --machine q35           # use Q35 chipset (for PCIe passthrough)

# Add/resize disks
qm set 100 --scsi1 local-lvm:50    # add 50GB disk
qm disk resize 100 scsi0 +20G      # grow existing disk by 20GB

# Networking
qm set 100 --net0 virtio,bridge=vmbr0,tag=10   # VLAN tagged
qm set 100 --net1 virtio,bridge=vmbr1           # second NIC

# Cloud-init (for automated provisioning)
qm set 100 --ide2 local-lvm:cloudinit
qm set 100 --ciuser admin --cipassword 'secret'
qm set 100 --ipconfig0 ip=10.0.0.50/24,gw=10.0.0.1
qm set 100 --sshkeys ~/.ssh/authorized_keys
qm set 100 --boot order=scsi0

# EFI / UEFI boot
qm set 100 --bios ovmf --efidisk0 local-lvm:1,efitype=4m,pre-enrolled-keys=1

# Serial console (headless)
qm set 100 --serial0 socket --vga serial0

# PCI passthrough (GPU, NIC, etc.)
qm set 100 --hostpci0 0000:01:00.0,pcie=1
```

### Snapshots and Cloning

```bash
# Create a snapshot
qm snapshot 100 before-upgrade --description "Before kernel upgrade"

# List snapshots
qm listsnapshot 100

# Rollback to snapshot
qm rollback 100 before-upgrade

# Delete a snapshot
qm delsnapshot 100 before-upgrade

# Clone a VM (full copy)
qm clone 100 101 --name cloned-vm --full

# Clone as linked clone (shares base disk, faster)
qm clone 100 101 --name linked-vm
```

### Templates

```bash
# Convert VM to template (irreversible)
qm template 100

# Create VM from template (linked clone)
qm clone 100 200 --name from-template

# Create VM from template (full clone)
qm clone 100 200 --name from-template --full
```

### Migration

```bash
# Online migration to another node
qm migrate 100 node2 --online

# Offline migration
qm migrate 100 node2
```

### Monitoring

```bash
# VM status
qm status 100

# List all VMs
qm list

# Show running processes/agent info
qm agent 100 ping
qm agent 100 get-osinfo

# Monitor interface (QEMU monitor)
qm monitor 100
```

## Container Management with `pct`

### Creating a Container

```bash
# Download a template first
pveam update
pveam available --section system
pveam download local debian-12-standard_12.2-1_amd64.tar.zst

# Create container with ID 200
pct create 200 local:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst \
  --hostname my-ct --memory 1024 --cores 2 \
  --rootfs local-lvm:8 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --password 'secret' --unprivileged 1

# Create with static IP
pct create 201 local:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst \
  --hostname web-ct --memory 2048 --cores 2 \
  --rootfs local-lvm:16 \
  --net0 name=eth0,bridge=vmbr0,ip=10.0.0.51/24,gw=10.0.0.1 \
  --nameserver 1.1.1.1 --unprivileged 1
```

### Container Lifecycle

| Command | Purpose |
|---------|---------|
| `pct start <ctid>` | Start container |
| `pct shutdown <ctid>` | Graceful shutdown |
| `pct stop <ctid>` | Force stop |
| `pct reboot <ctid>` | Reboot container |
| `pct destroy <ctid>` | Delete container and its volumes |
| `pct enter <ctid>` | Open a shell inside the container |
| `pct exec <ctid> -- <cmd>` | Run a command inside the container |
| `pct console <ctid>` | Attach to container console |

### Container Configuration

```bash
# Show config
pct config 200

# Modify resources
pct set 200 --memory 4096
pct set 200 --cores 4
pct set 200 --swap 1024

# Add mount point (bind mount from host)
pct set 200 --mp0 /mnt/data,mp=/data

# Add additional storage volume
pct set 200 --mp1 local-lvm:50,mp=/var/lib/data

# Networking
pct set 200 --net0 name=eth0,bridge=vmbr0,ip=10.0.0.60/24,gw=10.0.0.1
pct set 200 --net1 name=eth1,bridge=vmbr1,ip=dhcp

# Features (nesting, FUSE, NFS)
pct set 200 --features nesting=1
pct set 200 --features nesting=1,fuse=1,mount=nfs

# DNS
pct set 200 --nameserver "1.1.1.1 8.8.8.8" --searchdomain example.com

# Start on boot
pct set 200 --onboot 1 --startup order=1,up=30
```

### Container Snapshots and Cloning

```bash
# Snapshot
pct snapshot 200 clean-install

# Rollback
pct rollback 200 clean-install

# Clone
pct clone 200 201 --hostname cloned-ct --full
```

## Storage Management

```bash
# List storage pools
pvesm status

# List content of a storage
pvesm list local
pvesm list local-lvm

# Add storage (examples)
pvesm add dir my-backup --path /mnt/backup --content backup
pvesm add nfs nfs-share --server 10.0.0.5 --export /exports/pve --content images,vztmpl
pvesm add lvm my-lvm --vgname my-vg --content rootdir,images
pvesm add zfspool my-zfs --pool rpool/data --content rootdir,images

# Remove storage
pvesm remove my-backup

# Download ISO
wget -P /var/lib/vz/template/iso/ https://example.com/image.iso
```

## Networking

```bash
# List network interfaces
cat /etc/network/interfaces

# Common bridge configuration (in /etc/network/interfaces)
# auto vmbr0
# iface vmbr0 inet static
#     address 10.0.0.1/24
#     bridge-ports eno1
#     bridge-stp off
#     bridge-fd 0

# Apply network changes
ifreload -a
```

## Cluster Management

```bash
# Create a new cluster
pvecm create my-cluster

# Join an existing cluster
pvecm add 10.0.0.1

# Show cluster status
pvecm status

# List cluster nodes
pvecm nodes

# Remove a node (run from a remaining node)
pvecm delnode nodename

# Check quorum
pvecm expected 1    # force quorum (dangerous, single-node recovery only)
```

## Firewall

```bash
# Enable/disable firewall at datacenter level
pve-firewall start
pve-firewall stop
pve-firewall status

# Manage rules via config files
# Datacenter: /etc/pve/firewall/cluster.fw
# Node:       /etc/pve/nodes/<node>/host.fw
# VM/CT:      /etc/pve/firewall/<vmid>.fw
```

## Backup and Restore

```bash
# Backup a VM
vzdump 100 --storage local --mode snapshot --compress zstd

# Backup a container
vzdump 200 --storage local --mode stop --compress zstd

# Backup all guests
vzdump --all --storage local --mode snapshot --compress zstd --mailto admin@example.com

# Restore a VM
qmrestore /var/lib/vz/dump/vzdump-qemu-100-*.vma.zst 100

# Restore a container
pct restore 200 /var/lib/vz/dump/vzdump-lxc-200-*.tar.zst

# Restore to different storage
qmrestore /var/lib/vz/dump/vzdump-qemu-100-*.vma.zst 100 --storage local-lvm
```

## Common Provisioning Patterns

### Cloud-Init VM from Template

```bash
# 1. Create base VM and install OS, then convert to template
qm template 9000

# 2. Clone and customize with cloud-init
qm clone 9000 110 --name web-server --full
qm set 110 --ciuser deploy --sshkeys ~/.ssh/authorized_keys
qm set 110 --ipconfig0 ip=10.0.0.110/24,gw=10.0.0.1
qm set 110 --nameserver 1.1.1.1
qm start 110
```

### Batch Create Containers

```bash
for i in $(seq 1 5); do
  CTID=$((300 + i))
  pct create $CTID local:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst \
    --hostname "worker-${i}" --memory 1024 --cores 2 \
    --rootfs local-lvm:8 \
    --net0 name=eth0,bridge=vmbr0,ip=10.0.0.$((60 + i))/24,gw=10.0.0.1 \
    --unprivileged 1 --start 1
done
```

### Import Disk Image (e.g., cloud image)

```bash
# Download a cloud image
wget https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img

# Import to a VM
qm importdisk 100 jammy-server-cloudimg-amd64.img local-lvm

# Attach the imported disk
qm set 100 --scsi0 local-lvm:vm-100-disk-0
qm set 100 --boot order=scsi0
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| VM won't start | Check `qm config <vmid>`, verify storage exists with `pvesm status` |
| "TASK ERROR: can't lock file" | `rm /run/lock/qemu-server/lock-<vmid>.conf` (verify VM is not running first) |
| Container has no network | Check bridge exists: `brctl show`; verify firewall rules |
| Disk full on storage | `pvesm status` to check usage; `lvs` for LVM thin pools |
| Cluster quorum lost | `pvecm expected 1` on surviving node (single-node recovery only) |
| Migration fails | Ensure same CPU type or use `--online` with live migration; check network between nodes |
| Backup fails with lock error | `qm unlock <vmid>` or `pct unlock <ctid>` |
| Slow disk I/O in VM | Use `virtio-scsi-pci` controller with `iothread=1` and `discard=on` |
| Guest agent not responding | Install `qemu-guest-agent` in the VM and enable: `qm set <vmid> --agent 1` |

## Useful Paths

| Path | Contents |
|------|----------|
| `/etc/pve/` | Cluster-wide config (pmxcfs) |
| `/etc/pve/qemu-server/<vmid>.conf` | VM configuration files |
| `/etc/pve/lxc/<ctid>.conf` | Container configuration files |
| `/etc/pve/storage.cfg` | Storage definitions |
| `/etc/pve/nodes/` | Per-node configuration |
| `/var/lib/vz/` | Default local storage root |
| `/var/lib/vz/template/iso/` | ISO images |
| `/var/lib/vz/template/cache/` | Container templates |
| `/var/lib/vz/dump/` | Backup files |
| `/var/log/pve/tasks/` | Task logs |
