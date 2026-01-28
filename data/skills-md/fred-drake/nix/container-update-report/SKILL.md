---
name: container-update-report
description: Update container digests and deploy affected hosts end-to-end. Use when the user wants to check for container updates, update container digests, or deploy container changes. Triggers on requests like "update containers", "check for container updates", "deploy container updates", or "run container-update-report".
---

# Container Update Report

Update container digests and deploy affected NixOS hosts end-to-end.

## Workflow

### 1. Update Container Digests

Run the update command to fetch latest container SHAs:

```bash
just update-container-digests
```

This updates `apps/fetcher/containers-sha.nix` with the latest digests from all registries.

### 2. Check What Changed

Check the diff to see which containers have updates:

```bash
git diff apps/fetcher/containers-sha.nix
```

Summarize changes in a table format:
- Registry (docker.io, ghcr.io, lscr.io, etc.)
- Container name and tag
- Note: If no changes, inform user that all containers are up to date

### 3. Map Containers to Hosts

Search for container usage in `.nix` files:

```bash
# Search for specific container
grep -r "container-name" --include="*.nix" .
```

Key locations:
- `apps/*.nix` - Application definitions
- `modules/nixos/host/*/` - Host-specific configurations

See [container-host-mapping.md](references/container-host-mapping.md) for known mappings.

### 4. Deploy Affected Hosts

Ask user which hosts to deploy, then deploy each:

```bash
just colmena <hostname>
```

Run deployments in parallel when hosts are independent. Verify success by checking output shows "Activation successful" and "All done!".

### 5. Report Summary

After deployment, provide a summary table:

| Container | Host | Status |
|-----------|------|--------|
| container:tag | hostname | ✓ |

## Common Container Locations

| Container | Typical Host |
|-----------|--------------|
| postgres | woodpecker, paperless, sonarqube, resume |
| redis | paperless |
| woodpecker-agent/server | woodpecker |
| n8n | n8n |
| calibre, sabnzbd, sonarr, radarr | larussa |
| lazylibrarian | larussa |
| paperless-ngx | paperless |

## Resources

See [references/container-host-mapping.md](references/container-host-mapping.md) for detailed container-to-host mappings.
