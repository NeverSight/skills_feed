---
name: tailscale
description: Troubleshoot Tailscale connectivity or access internal services via Tailscale hostnames.
---

# Tailscale

## Overview

Use Tailscale for access to internal services such as Temporal or OpenWebUI. Confirm network health before deeper debugging.

## Quick checks

```bash
tailscale status
tailscale netcheck
tailscale ping temporal-grpc.ide-newton.ts.net
```

## Access examples

- Temporal gRPC: `temporal-grpc.ide-newton.ts.net:7233`
- OpenWebUI: `http://openwebui`

## Resources

- Reference: `references/tailscale-troubleshooting.md`
- Diagnostic script: `scripts/tailscale-diag.sh`
- Checklist: `assets/tailscale-checklist.md`
