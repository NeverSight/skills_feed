---
name: tailscale
description: Mesh VPN.
metadata:
  trit: 0
---

# tailscale

Mesh VPN.

## Connect

```bash
tailscale up
tailscale down
tailscale status
```

## SSH

```bash
tailscale ssh hostname
tailscale ssh user@hostname
```

## Serve

```bash
tailscale serve http://localhost:8080
tailscale serve https://localhost:443
tailscale serve status
tailscale serve reset
```

## Funnel

```bash
tailscale funnel 443
tailscale funnel status
tailscale funnel reset
```

## File

```bash
tailscale file cp file.txt hostname:
tailscale file get ~/Downloads/
```

## DNS

```bash
tailscale dns status
tailscale whois 100.x.y.z
```

## Exit

```bash
tailscale set --exit-node=hostname
tailscale set --exit-node=
```
