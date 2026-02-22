---
name: opentunnel-connect
description: Connect to remote servers behind NAT using reverse SSH tunnel with bore.
version: 5.0.0
---

# OpenTunnel Connect Skill

Connect to remote servers behind NAT using reverse SSH tunnel.

## Flow

### Step 1: Ask Options

Ask user:
- Username? (default: tunneluser)
- Minutes? (default: 60)

### Step 2: Execute Binary

```powershell
& "$env:USERPROFILE\.config\opencode\skills\opentunnel-connect\opentunnel.exe" --user USERNAME --minutes MINUTES
```

The binary will:
1. Read/create SSH key from `~/.ssh/id_ed25519.pub`
2. Output curl command for remote server
3. Wait for user to input tunnel info

### Step 3: User Runs Command

Give curl command to user to run on **remote server**.

Example:
```bash
curl -fsSL "https://raw.githubusercontent.com/julianponguta/opentunnel/main/connect.sh?v=$(date +%s)" | sudo bash -s -- 60 root "ssh-ed25519..."
```

### Step 4: Get Tunnel Info

User must provide: `bore.pub:PORT`

### Step 5: Connect with ezssh

```javascript
ezssh_ssh_execute({
  command: "hostname && uptime",
  hosts: ["bore.pub"],
  port: PORT,
  username: "USERNAME",
  privateKeyPath: process.env.USERPROFILE + "/.ssh/id_ed25519"
})
```

On Linux/macOS:
```javascript
privateKeyPath: process.env.HOME + "/.ssh/id_ed25519"
```

## Quick Install (for users)

Users can install on their servers:
```bash
echo 'ot() { curl -fsSL "https://raw.githubusercontent.com/julianponguta/opentunnel/main/connect.sh?v=$(date +%s)" | sudo bash -s -- "${@:-60}"; }' >> ~/.bashrc && source ~/.bashrc
```

Then just run: `ot 60 root`
