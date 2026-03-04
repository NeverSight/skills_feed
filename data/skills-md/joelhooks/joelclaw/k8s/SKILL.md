---
name: k8s
displayName: K8s
description: >-
  Operate the joelclaw Kubernetes cluster — Talos Linux on Colima (Mac Mini).
  Deploy services, check health, debug pods, recover from restarts, add ports,
  manage Helm releases, inspect logs, fix networking. Triggers on: 'kubectl',
  'pods', 'deploy to k8s', 'cluster health', 'restart pod', 'helm install',
  'talosctl', 'colima', 'nodeport', 'flannel', 'port mapping', 'k8s down',
  'cluster not working', 'add a port', 'PVC', 'storage', any k8s/Talos/Colima
  infrastructure task. Also triggers on service-specific deploy: 'deploy redis',
  'redeploy inngest', 'livekit helm', 'pds not responding'.
version: 1.0.0
author: Joel Hooks
tags: [joelclaw, kubernetes, talos, colima, infrastructure]
---

# k8s Cluster Operations — joelclaw on Talos

## Architecture

```
Mac Mini (localhost ports)
  └─ Lima SSH mux (~/.colima/_lima/colima/ssh.sock) ← NEVER KILL
      └─ Colima VM (4 CPU, 8 GiB, 60 GiB, VZ framework, aarch64)
          └─ Docker 29.x
              └─ Talos v1.12.4 container (joelclaw-controlplane-1)
                  └─ k8s v1.35.0 (single node, Flannel CNI)
                      └─ joelclaw namespace (privileged PSA)
```

**⚠️ Talos has NO shell.** No bash, no /bin/sh, nothing. You cannot `docker exec` into the Talos container. Use `talosctl` for node operations and the Colima VM (`ssh lima-colima`) for host-level operations like `modprobe`.

For port mappings, recovery procedures, and cluster recreation steps, read [references/operations.md](references/operations.md).

## Quick Health Check

```bash
kubectl get pods -n joelclaw                          # all pods
curl -s localhost:3111/api/inngest                     # system-bus-worker → 200
curl -s localhost:7880/                                # LiveKit → "OK"
curl -s localhost:8108/health                          # Typesense → {"ok":true}
curl -s localhost:8288/health                          # Inngest → {"status":200}
curl -s localhost:9627/xrpc/_health                    # PDS → {"version":"..."}
kubectl exec -n joelclaw redis-0 -- redis-cli ping     # → PONG
```

## Services

| Service | Type | Pod | Ports (Mac→NodePort) | Helm? |
|---------|------|-----|---------------------|-------|
| Redis | StatefulSet | redis-0 | 6379→6379 | No |
| Typesense | StatefulSet | typesense-0 | 8108→8108 | No |
| Inngest | StatefulSet | inngest-0 | 8288→8288, 8289→8289 | No |
| system-bus-worker | Deployment | system-bus-worker-* | 3111→3111 | No |
| LiveKit | Deployment | livekit-server-* | 7880→7880, 7881→7881 | Yes (livekit/livekit-server 1.9.0) |
| PDS | Deployment | bluesky-pds-* | 9627→**3000** | Yes (nerkho/bluesky-pds 0.4.2) |

**⚠️ PDS port trap**: Docker maps `9627→3000` (host→container). NodePort must be **3000** to match the container-side port. If set to 9627, traffic won't route.

**Rule**: NodePort value = Docker's container-side port, not host-side.

## Deploy Commands

```bash
# Manifests (redis, typesense, inngest)
kubectl apply -f ~/Code/joelhooks/joelclaw/k8s/

# system-bus worker (build + push GHCR + apply + rollout wait)
~/Code/joelhooks/joelclaw/k8s/publish-system-bus-worker.sh

# LiveKit (Helm + reconcile patches)
~/Code/joelhooks/joelclaw/k8s/reconcile-livekit.sh joelclaw

# PDS (Helm) — always patch NodePort to 3000
# (export current values first if the release already exists)
helm get values bluesky-pds -n joelclaw > /tmp/pds-values-live.yaml 2>/dev/null || true
helm upgrade --install bluesky-pds nerkho/bluesky-pds \
  -n joelclaw -f /tmp/pds-values-live.yaml
kubectl patch svc bluesky-pds -n joelclaw --type='json' \
  -p='[{"op":"replace","path":"/spec/ports/0/nodePort","value":3000}]'
```

## Auto Deploy (GitHub Actions)

- Workflow: `.github/workflows/system-bus-worker-deploy.yml`
- Trigger: push to `main` touching `packages/system-bus/**` or worker deploy files
- Behavior:
  - builds/pushes `ghcr.io/joelhooks/system-bus-worker:${GITHUB_SHA}` + `:latest`
  - runs deploy job on `self-hosted` runner
  - updates k8s deployment image + waits for rollout + probes worker health
- If deploy job is queued forever, check that a `self-hosted` runner is online on the Mac Mini.

### GHCR push 403 Forbidden

**Cause:** `GITHUB_TOKEN` (default Actions token) does not have `packages:write` scope for this repo. A dedicated PAT is required.

**Fix already applied:** Workflow uses `secrets.GHCR_PAT` (not `secrets.GITHUB_TOKEN`) for the GHCR login step. The PAT is stored in:
- GitHub repo secrets as `GHCR_PAT` (set via GitHub UI)
- agent-secrets as `ghcr_pat` (`secrets lease ghcr_pat`)

**If this breaks again:** PAT may have expired. Regenerate at github.com → Settings → Developer settings → PATs, update both stores.

**Local fallback (bypass GHA entirely):**
```bash
DOCKER_CONFIG_DIR=$(mktemp -d)
echo '{"credsStore":""}' > "$DOCKER_CONFIG_DIR/config.json"
export DOCKER_CONFIG="$DOCKER_CONFIG_DIR"
secrets lease ghcr_pat | docker login ghcr.io -u joelhooks --password-stdin
~/Code/joelhooks/joelclaw/k8s/publish-system-bus-worker.sh
```
Note: `publish-system-bus-worker.sh` uses `gh auth token` internally — if `gh auth` is stale, use the Docker login above before running the script, or patch it to use `secrets lease ghcr_pat` directly.

## Resilience Rules (ADR-0148)

1. **NEVER use `kubectl port-forward` for persistent services.** All services MUST use NodePort + Docker port mappings. Port-forwards silently die on idle/restart/pod changes.
2. **All workloads MUST have liveness + readiness + startup probes.** Missing probes = silent hangs that never recover.
3. **After any Docker/Colima/node restart**: remove control-plane taint, **uncordon node**, verify flannel, check all pods reach Running.
4. **PVC reclaimPolicy is Delete** — deleting a PVC = permanent data loss. Never delete PVCs without backup.
5. **Colima VM disk is limited (19GB).** Monitor with `colima ssh -- df -h /`. Alert at >80%.
6. **All launchd plists MUST set PATH including `/opt/homebrew/bin`.** Colima shells to `limactl`, kubectl/talosctl live in homebrew. launchd's default PATH is `/usr/bin:/bin:/usr/sbin:/sbin` — no homebrew. The canonical PATH for infra plists is: `/opt/homebrew/bin:/Users/joel/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`. Discovered Feb 2026: missing PATH caused 6 days of silent recovery failures.
7. **Shell scripts run by launchd MUST export PATH at the top.** Even if the plist sets EnvironmentVariables, belt-and-suspenders — add `export PATH="/opt/homebrew/bin:..."` to the script itself.

### Current Probe Gaps (fix when touching these services)
- Typesense: missing liveness probe (hangs won't be detected)
- Bluesky PDS: missing readiness and startup probes
- system-bus-worker: missing startup probe

## Danger Zones

1. **Never kill Lima SSH mux** — it handles ALL tunnels. Killing anything on the SSH socket kills all port access.
2. **Adding Docker port mappings** — can be hot-added without cluster recreation via `hostconfig.json` edit. See [references/operations.md](references/operations.md) for the procedure.
3. **Inngest legacy host alias in manifests** — old container-host alias may still appear in legacy configs. Worker uses connect mode, so it usually still works, but prefer explicit Talos/Colima hostnames.
4. **Colima zombie state** — `colima status` reports "Running" but docker socket / SSH tunnels are dead. All k8s ports unresponsive. `colima start` is a no-op. Only `colima restart` recovers. Detect with: `ssh -F ~/.colima/_lima/colima/ssh.config lima-colima "docker info"` — if that fails while `colima status` passes, it's a zombie. The heal script handles this automatically.
5. **Talos container has NO shell** — No bash, no /bin/sh. Cannot `docker exec` into it. Kernel modules like `br_netfilter` must be loaded at the Colima VM level: `ssh lima-colima "sudo modprobe br_netfilter"`.

## Key Files

| Path | What |
|------|------|
| `~/Code/joelhooks/joelclaw/k8s/*.yaml` | Service manifests |
| `~/Code/joelhooks/joelclaw/k8s/livekit-values.yaml` | LiveKit Helm values (source controlled) |
| `~/Code/joelhooks/joelclaw/k8s/reconcile-livekit.sh` | LiveKit Helm deploy + post-upgrade reconcile |
| `~/Code/joelhooks/joelclaw/k8s/publish-system-bus-worker.sh` | Build/push/deploy system-bus worker to k8s |
| `~/Code/joelhooks/joelclaw/infra/k8s-reboot-heal.sh` | Reboot auto-heal script for Colima/Talos/taint/flannel |
| `~/Code/joelhooks/joelclaw/infra/launchd/com.joel.k8s-reboot-heal.plist` | launchd timer for reboot auto-heal |
| `~/Code/joelhooks/joelclaw/skills/k8s/references/operations.md` | Cluster operations + recovery notes |
| `~/.talos/config` | Talos client config |
| `~/.kube/config` | Kubeconfig (context: `admin@joelclaw-1`) |
| `~/.colima/default/colima.yaml` | Colima VM config |
| `~/.local/caddy/Caddyfile` | Caddy HTTPS proxy (Tailscale) |

## Troubleshooting

Read [references/operations.md](references/operations.md) for:
- Recovery after Colima restart
- Recovery after Mac reboot
- Flannel br_netfilter crash fix
- Full cluster recreation (nuclear option)
- Caddy/Tailscale HTTPS proxy details
- All port mapping details with explanation
