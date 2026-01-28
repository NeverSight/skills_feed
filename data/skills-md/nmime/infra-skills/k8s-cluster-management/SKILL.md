---
name: k8s-cluster-management
description: Kubernetes cluster installation via Kubespray. Always use Kubespray for cluster provisioning. Includes core addons (Cilium, Gateway API, cert-manager, LoadBalancer). Multi-cloud support.
---

# K8s Cluster Management

**Always use Kubespray for Kubernetes cluster installation.** Kubespray playbooks are idempotent and converge to desired state.

## Components (January 2026)

| Component | Version | Purpose |
|-----------|---------|--------|
| Kubernetes | v1.34.3 | Cluster |
| Kubespray | v2.29.1 | Installer |
| etcd | v3.5.26 | Key-value store |
| containerd | v2.2.1 | Container runtime |
| Cilium | v1.18.6 | CNI + Gateway |
| Gateway API | v1.4.0 | Ingress |
| cert-manager | v1.19.2 | TLS automation |
| MetalLB | v0.14.9 | Bare metal LB |

> **Note**: For K8s v1.35.0, wait for Kubespray v2.30+.

## Installation

Run from bastion server. See reference files for detailed commands:
- Kubernetes cluster: [references/kubespray.md](references/kubespray.md)
- CNI: [references/cilium.md](references/cilium.md)
- Ingress: [references/gateway-api.md](references/gateway-api.md)
- TLS: [references/cert-manager.md](references/cert-manager.md)

## kubectl Access

After installation, kubectl works directly from bastion:

```bash
# On bastion
kubectl get nodes
kubectl get pods -A
```

Or via VPN from any connected server:

```bash
# Connect to VPN first
tailscale up --login-server https://vpn.example.com --authkey <KEY>

# Then kubectl works
kubectl get nodes
```

## Reference Files

- [references/kubespray.md](references/kubespray.md) - Installation
- [references/cilium.md](references/cilium.md) - CNI
- [references/gateway-api.md](references/gateway-api.md) - Ingress
- [references/cert-manager.md](references/cert-manager.md) - TLS
- [references/upgrades.md](references/upgrades.md) - Cluster upgrades
- [references/essential-components.md](references/essential-components.md) - Essential components
- [references/troubleshooting.md](references/troubleshooting.md) - Troubleshooting