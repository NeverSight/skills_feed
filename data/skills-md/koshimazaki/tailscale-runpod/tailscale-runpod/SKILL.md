---
name: tailscale-runpod
description: Setup Tailscale for SSH access to RunPod, Vast.ai, or any cloud GPU instance. Use when user asks to "setup Tailscale", "SSH to RunPod", "connect to cloud GPU", or needs VPN/mesh networking.
version: 1.1.0
author: koshimazaki
---

# Tailscale for Cloud GPU (RunPod/Vast.ai)

Connect to your cloud GPU instances via SSH using Tailscale mesh VPN.

## Why Tailscale?

- **Direct SSH** - No port forwarding or exposed services
- **Persistent IP** - Same IP even after pod restarts
- **Secure** - End-to-end encrypted, no public exposure
- **Works anywhere** - Bypasses NAT and firewalls

## Quick Setup (Cloud Instance)

**Run in JupyterLab terminal or RunPod SSH:**

```bash
curl -fsSL https://tailscale.com/install.sh | bash; /usr/sbin/tailscaled --tun=userspace-networking --state=/workspace/tailscale.state & sleep 5; tailscale up --ssh
```

Click the auth URL to login. Then SSH from your local machine via Tailscale IP.

### Platform Paths

| Platform | Persistent Storage | Default User |
|----------|-------------------|--------------|
| RunPod | `/workspace/` | `root` |
| Vast.ai | `/workspace/` | `root` |
| Lambda Labs | `/home/ubuntu/` | `ubuntu` |
| Paperspace | `/storage/` | `paperspace` |

**For non-RunPod platforms**, adjust the state path:
```bash
# Lambda Labs
/usr/sbin/tailscaled --tun=userspace-networking --state=/home/ubuntu/tailscale.state &

# Paperspace
/usr/sbin/tailscaled --tun=userspace-networking --state=/storage/tailscale.state &
```

## SSH from Local Machine

Once connected:

```bash
ssh root@<TAILSCALE_IP>
```

Find the IP with `tailscale status` on either machine.

---

## Detailed Setup

### Cloud Instance (RunPod/Vast.ai)

#### 1. Install Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | bash
```

#### 2. Start daemon (container mode)

```bash
/usr/sbin/tailscaled --tun=userspace-networking --state=/workspace/tailscale.state &
sleep 5
```

| Flag | Purpose |
|------|---------|
| `--tun=userspace-networking` | Required for containers (no kernel TUN device) |
| `--state=/workspace/` | Persist auth across restarts |
| `&` | Run in background |

#### 3. Connect with SSH enabled

```bash
tailscale up --ssh
```

**The `--ssh` flag is critical** - it enables Tailscale's built-in SSH server, required for SSH to work in containers.

Click the auth URL to login via browser.

#### 4. Get your Tailscale IP

```bash
tailscale ip -4
```

### Local Machine (macOS)

```bash
brew install --cask tailscale
open -a Tailscale
```

Or download from: https://tailscale.com/download

### Local Machine (Linux)

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

### Local Machine (Windows)

Download from: https://tailscale.com/download/windows

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `tailscale status` | Show all connected devices |
| `tailscale ip -4` | Get your Tailscale IPv4 |
| `tailscale up --ssh` | Connect with SSH enabled |
| `tailscale down` | Disconnect |
| `tailscale ping <ip>` | Test connectivity to peer |
| `tailscale netcheck` | Network diagnostics |
| `tailscale logout` | Sign out completely |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **SSH connection timeout** | Ensure you used `--ssh` flag: `tailscale up --ssh` |
| **"tailscaled not running"** | Start daemon: `/usr/sbin/tailscaled --tun=userspace-networking &` |
| **Peer shows "offline"** | Run `tailscale up --ssh` on that machine |
| **Slow connection (relay)** | Wait for direct connection, or check `tailscale netcheck` |
| **Auth expired** | Run `tailscale up --ssh` again |
| **Version mismatch warning** | Usually harmless, update if issues persist |

### Full Reset

```bash
pkill tailscaled; sleep 1; /usr/sbin/tailscaled --tun=userspace-networking --state=/workspace/tailscale.state & sleep 5 && tailscale up --ssh
```

---

## Example Workflow

```bash
# On RunPod (first time)
curl -fsSL https://tailscale.com/install.sh | bash
/usr/sbin/tailscaled --tun=userspace-networking --state=/workspace/tailscale.state &
sleep 5
tailscale up --ssh
# Click the URL, login, note the IP (e.g., 100.x.x.x)

# On your Mac
tailscale status  # Verify pod is online
ssh root@100.x.x.x  # Connect!
```

---

## File Transfer

### Download from RunPod (to versioned folder)

Creates `~/Downloads/runpod_1_01-30-2026/` (version_MM-DD-YYYY):

```bash
# Set your RunPod IP and version
RUNPOD=100.x.x.x
V=1

# Create versioned folder and download
mkdir -p ~/Downloads/runpod_${V}_$(date +%m-%d-%Y) && rsync -avz --progress --partial root@$RUNPOD:/workspace/ComfyUI/output/ ~/Downloads/runpod_${V}_$(date +%m-%d-%Y)/
```

Increment `V=2`, `V=3` for multiple sessions/pods.

### Upload to RunPod

```bash
# Single file
scp ~/file.png root@$RUNPOD:/workspace/ComfyUI/input/

# Folder with progress (chunked, resumable)
rsync -avz --progress --partial ~/models/ root@$RUNPOD:/workspace/ComfyUI/models/
```

### Large Files (chunked transfer)

For reliability on large files, use rsync with block checksum:

```bash
# Download large files in ~1MB chunks, resumable
rsync -avz --progress --partial --block-size=1048576 root@$RUNPOD:/workspace/outputs/ ~/Downloads/runpod_$(date +%Y-%m-%d)/

# Upload with same settings
rsync -avz --progress --partial --block-size=1048576 ~/large_model.safetensors root@$RUNPOD:/workspace/ComfyUI/models/
```

### Quick Aliases

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Set your default RunPod IP
export RUNPOD_IP="100.x.x.x"

# Download outputs to dated folder
alias rpget='mkdir -p ~/Downloads/runpod_$(date +%Y-%m-%d) && rsync -avz --progress --partial root@$RUNPOD_IP:/workspace/ComfyUI/output/ ~/Downloads/runpod_$(date +%Y-%m-%d)/'

# Upload to inputs
alias rpput='rsync -avz --progress --partial'

# SSH shortcut
alias rpssh='ssh root@$RUNPOD_IP'
```

Usage:
```bash
rpget                           # Download all outputs
rpput file.png root@$RUNPOD_IP:/workspace/ComfyUI/input/
rpssh                           # SSH in
```

---

## Security Notes

- Tailscale IPs are only accessible within your tailnet
- Traffic is end-to-end encrypted (WireGuard)
- No ports exposed to public internet

## Important Notes

- **Browser auth required** - You must click the auth URL each time. Authkey in startup commands doesn't work reliably for SSH in unprivileged containers.
- **Userspace networking** - Required for containers without TUN device access
- **`--ssh` flag** - Enables Tailscale's built-in SSH server, which is the only way SSH works in userspace mode
