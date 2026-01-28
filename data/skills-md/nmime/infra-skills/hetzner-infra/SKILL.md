---
name: hetzner-infra
description: Hetzner cloud infrastructure provisioning for Kubernetes. Use when provisioning servers, networks, load balancers, firewalls, DNS zones, or storage on Hetzner Cloud via hcloud CLI.
---

# Cloud Infrastructure

**Infrastructure patterns for Kubernetes clusters.** Implementation via hcloud CLI. All scripts are **idempotent**.

## Core Components

| Component | Purpose | hcloud Command |
|-----------|---------|----------------|
| Compute | VM instances for nodes | `hcloud server` |
| Network | Private connectivity | `hcloud network` |
| Load Balancer | Traffic distribution | `hcloud load-balancer` |
| Firewall | Network security | `hcloud firewall` |
| DNS | Name resolution | `hcloud zone` |
| Storage | Block storage | `hcloud volume` |

## Server Type Selection

If a server type is unavailable in the preferred location, try other European locations:

```bash
# Check availability across EU locations
for loc in fsn1 nbg1 hel1; do
  echo "=== $loc ===" && hcloud server-type list --selector location=$loc
done
```

EU locations: `fsn1` (Falkenstein), `nbg1` (Nuremberg), `hel1` (Helsinki)

## Quick Start

```bash
# Install hcloud CLI
curl -sL https://github.com/hetznercloud/cli/releases/latest/download/hcloud-linux-amd64.tar.gz | tar xz
sudo mv hcloud /usr/local/bin/

# Set token
export HCLOUD_TOKEN="your-token"

# Verify
hcloud server list
```

## hcloud Reference

| Resource | Reference |
|----------|-----------|
| Servers | [hcloud-server.md](references/hcloud-server.md) |
| Networks | [hcloud-network.md](references/hcloud-network.md) |
| Load Balancers | [hcloud-load-balancer.md](references/hcloud-load-balancer.md) |
| Firewalls | [hcloud-firewall.md](references/hcloud-firewall.md) |
| Volumes | [hcloud-volume.md](references/hcloud-volume.md) |
| Floating IPs | [hcloud-floating-ip.md](references/hcloud-floating-ip.md) |
| Primary IPs | [hcloud-primary-ip.md](references/hcloud-primary-ip.md) |
| SSH Keys | [hcloud-ssh-key.md](references/hcloud-ssh-key.md) |
| Images | [hcloud-image.md](references/hcloud-image.md) |
| Certificates | [hcloud-certificate.md](references/hcloud-certificate.md) |
| Placement Groups | [hcloud-placement-group.md](references/hcloud-placement-group.md) |
| DNS Zones | [hcloud-zone.md](references/hcloud-zone.md) |
| Storage Boxes | [hcloud-storage-box.md](references/hcloud-storage-box.md) |
| Datacenters | [hcloud-datacenter.md](references/hcloud-datacenter.md) |
| Context | [hcloud-context.md](references/hcloud-context.md) |

## Provisioning

See [references/provisioning.md](references/provisioning.md) for step-by-step infrastructure setup.

## References

- [provisioning.md](references/provisioning.md) - Step-by-step setup
- [terraform.md](references/terraform.md) - Infrastructure as Code
- [naming.md](references/naming.md) - Naming conventions
- [cost-optimization.md](references/cost-optimization.md) - Cost strategies
- [scripts.md](references/scripts.md) - Automation scripts
- [cert-manager-hetzner.md](references/cert-manager-hetzner.md) - TLS certificates
