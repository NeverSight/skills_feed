---
name: network-security
description: VPN access and firewall rules. Headscale VPN on bastion for admin access to private services.
---

# Network Security

Headscale v0.27.1 VPN and firewall for secure admin access. (Updated: January 2026). All scripts are **idempotent** - check state before applying changes.

## Responsibility

| This Skill | Other Skills |
|------------|-------------|
| Headscale VPN setup | Servers → hetzner-infra |
| VPN user management | DNS → hetzner-infra |
| Firewall rules | TLS → k8s-cluster-management |
| Bastion hardening | LB → hetzner-infra |

## Architecture

```
INTERNET
    │
    ├─ PUBLIC (via LB) ───▶ app, api, s3, registry
    │
    └─ ADMIN (via VPN) ──▶ gitlab, argocd, grafana, vault, k8s
                │
                └──▶ Bastion + Headscale
```

## Setup

Run on bastion server. See reference files for detailed commands:
- VPN server: [references/headscale.md](references/headscale.md)
- User management: [references/users.md](references/users.md)
- Firewall rules: [references/firewall.md](references/firewall.md)

## VPN Client Access

Connect from any server or sandboxed environment:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up --login-server https://vpn.example.com --authkey <KEY>
```

## Reference Files

- [references/headscale.md](references/headscale.md) - VPN server
- [references/netbird.md](references/netbird.md) - NetBird alternative
- [references/users.md](references/users.md) - User management
- [references/firewall.md](references/firewall.md) - Firewall rules
- [references/bastion.md](references/bastion.md) - Bastion hardening
- [references/architecture.md](references/architecture.md) - Network architecture