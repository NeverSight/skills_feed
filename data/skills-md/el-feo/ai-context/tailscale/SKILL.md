---
name: tailscale
description: Comprehensive Tailscale VPN setup, configuration, and management for mesh networking, secure access, and zero-trust infrastructure. Covers installation, CLI commands, subnet routers, exit nodes, Tailscale SSH, ACL/grants configuration, MagicDNS, Tailscale Serve/Funnel, API automation, and production deployment best practices.
---

# Tailscale Network Management

> **Trigger Keywords**: tailscale, tailnet, wireguard vpn, mesh vpn, tailscale ssh, exit node, subnet router, tailscale acl, magicDNS, tailscale serve, tailscale funnel

**What is Tailscale?** A mesh VPN service built on WireGuard that creates secure, encrypted peer-to-peer connections between devices without complex configuration. Unlike traditional VPNs with central gateways, Tailscale creates direct connections between devices (or uses relay servers when needed).

**Key Benefits:**
- **Zero-config networking**: Works seamlessly across NAT and firewalls
- **Direct connections**: Peer-to-peer mesh reduces latency vs traditional hub-and-spoke VPNs
- **WireGuard encryption**: State-of-the-art cryptographic security
- **Identity-based access**: Integrates with SSO providers (Google, Okta, GitHub, etc.)
- **Cross-platform**: Works on Linux, macOS, Windows, iOS, Android, and more

## Quick Start

### Installation

**Linux (one-liner):**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

**macOS:**
```bash
brew install tailscale
```

**Windows/Other platforms:**
Download from https://tailscale.com/download

### Initial Setup

```bash
# Start Tailscale and authenticate
sudo tailscale up

# Check status
tailscale status

# Get your Tailscale IP
tailscale ip -4

# Connect via MagicDNS hostname
ssh user@machine-name
```

## Common Operations

### Basic Connection Management

```bash
# Connect to your tailnet
tailscale up

# Disconnect but keep daemon running
tailscale down

# Check connection status and peers
tailscale status

# View detailed network map
tailscale status --json | jq

# Ping another tailnet device (TSMP ping)
tailscale ping machine-name

# Test connectivity including ACLs (ICMP ping)
tailscale ping --icmp machine-name
```

### Subnet Router Setup

**What it does**: Allows devices without Tailscale to be accessible via a gateway device that does have Tailscale installed.

**On the router device:**
```bash
# Enable IP forwarding (Linux)
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf

# Advertise routes to your local network
sudo tailscale up --advertise-routes=192.168.1.0/24,10.0.0.0/24
```

**In the admin console:**
1. Go to Machines → find your subnet router
2. Click menu → "Edit route settings"
3. Enable the advertised routes

**On client devices:**
```bash
# Linux needs explicit flag to accept routes
sudo tailscale up --accept-routes

# Other platforms accept routes automatically
```

### Exit Node Configuration

**What it does**: Routes ALL internet traffic through a specific device on your tailnet (like a traditional VPN).

**Setup exit node:**
```bash
# Enable IP forwarding (same as subnet router)
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf

# Advertise as exit node
sudo tailscale up --advertise-exit-node
```

**In admin console:**
1. Go to Machines → find exit node
2. Click menu → "Edit route settings"  
3. Enable "Use as exit node"

**Use exit node from another device:**
```bash
# Use specific exit node
tailscale set --exit-node=exit-node-name

# Use suggested exit node (auto-selects best)
tailscale set --exit-node=auto:any

# Allow LAN access while using exit node
tailscale set --exit-node=exit-node-name --exit-node-allow-lan-access

# Stop using exit node
tailscale set --exit-node=
```

### Tailscale SSH Setup

**What it does**: SSH without managing keys, using your Tailscale identity for authentication.

**Enable SSH on server:**
```bash
# Enable Tailscale SSH server
sudo tailscale set --ssh
```

**Configure access in admin console:**
Go to Access Controls and add to the policy file:

```json
{
  "grants": [
    {
      "src": ["user@example.com"],
      "dst": ["tag:servers"],
      "ip": ["22"]
    }
  ],
  "ssh": [
    {
      "action": "accept",
      "src": ["user@example.com"],
      "dst": ["tag:servers"],
      "users": ["root", "ubuntu", "autogroup:nonroot"]
    }
  ]
}
```

**Connect from client:**
```bash
# No special setup needed on client!
ssh machine-name

# Or use specific user
ssh ubuntu@machine-name

# Works with SCP and SFTP too
scp file.txt machine-name:/tmp/
```

**Check mode** (for high-security connections):
```json
{
  "ssh": [
    {
      "action": "check",  // Requires recent SSO re-auth
      "src": ["user@example.com"],
      "dst": ["tag:servers"],
      "users": ["root"]
    }
  ]
}
```

### Serve and Funnel

**Tailscale Serve** (share within your tailnet):
```bash
# Serve local web server to tailnet
tailscale serve 3000

# Serve specific path
tailscale serve --https=443 --set-path=/app 8080

# Serve static files
tailscale serve --https=443 /var/www/html

# Serve with TLS-terminated TCP
tailscale serve --tls-terminated-tcp=5432 localhost:5432

# Check status
tailscale serve status

# Turn off
tailscale serve off
```

**Tailscale Funnel** (expose to public internet):
```bash
# Share to entire internet (must be on ports 443, 8443, or 10000)
tailscale funnel 3000

# Turn off
tailscale funnel off
```

## Access Control Lists (ACLs)

**Default policy** (allows all):
```json
{
  "acls": [
    {
      "action": "accept",
      "src": ["*"],
      "dst": ["*:*"]
    }
  ]
}
```

**Role-based access example:**
```json
{
  "groups": {
    "group:engineering": ["user1@example.com", "user2@example.com"],
    "group:ops": ["ops@example.com"]
  },
  "tagOwners": {
    "tag:dev": ["group:engineering"],
    "tag:prod": ["group:ops"]
  },
  "acls": [
    {
      "action": "accept",
      "src": ["group:engineering"],
      "dst": ["tag:dev:*"]
    },
    {
      "action": "accept",
      "src": ["group:ops"],
      "dst": ["tag:prod:*"]
    }
  ]
}
```

**Modern Grants syntax** (recommended):
```json
{
  "grants": [
    {
      "src": ["group:engineering"],
      "dst": ["tag:dev"],
      "ip": ["*"]
    },
    {
      "src": ["group:ops"],
      "dst": ["tag:prod"],
      "ip": ["22", "443", "80"]
    }
  ]
}
```

## Common Scenarios

### Home Lab Access
```bash
# On home server
sudo tailscale up --advertise-routes=192.168.1.0/24

# From anywhere
ssh homeserver
# Access 192.168.1.* devices through homeserver
```

### Secure Travel
```bash
# Set home device as exit node before trip
tailscale set --exit-node=home-server

# All traffic now routes through home
```

### Multi-Site Connectivity
```bash
# Site A router
sudo tailscale up --advertise-routes=10.0.0.0/24

# Site B router  
sudo tailscale up --advertise-routes=10.1.0.0/24 --accept-routes

# Now Site B can reach Site A's 10.0.0.0/24 network
```

## Troubleshooting

### Connection Issues

```bash
# Check if devices can establish connection (ignores ACLs)
tailscale ping --tsmp peer-name

# Check end-to-end including ACLs
tailscale ping --icmp peer-name

# View network map and connection details
tailscale netcheck

# Debug daemon logs
tailscale debug daemon-logs

# Check DERP relay status
tailscale netcheck
```

**If TSMP succeeds but ICMP fails**: ACL policy is blocking the connection.

**If both fail**: Network connectivity issue (firewall, NAT, routing problem).

### ACL Testing

```bash
# Preview rules for specific user (in admin console)
# Access Controls → Preview rules → select user

# Test ACL in policy file
# Add to policy:
"tests": [
  {
    "src": "user@example.com",
    "accept": ["tag:server:22"],
    "deny": ["tag:prod:*"]
  }
]
```

### Subnet Router Not Working

```bash
# Verify IP forwarding enabled
cat /proc/sys/net/ipv4/ip_forward  # Should be 1

# Check firewall isn't blocking
sudo iptables -L -v -n
sudo iptables -t nat -L -v -n

# Verify routes advertised
tailscale status | grep "subnet router"

# On client, ensure routes accepted
tailscale status | grep "routes accepted"
```

### MagicDNS Not Resolving

```bash
# Check MagicDNS enabled
tailscale status | grep MagicDNS

# In admin console: DNS → Enable MagicDNS

# Flush DNS cache
# macOS
sudo dscacheutil -flushcache

# Linux (systemd-resolved)
sudo systemd-resolve --flush-caches
```

## Best Practices

### Security

✅ **Use tags for servers**: Never share with personal accounts
```bash
sudo tailscale up --advertise-tags=tag:server
```

✅ **Disable key expiry for servers**:
- Admin console → Machines → menu → "Disable key expiry"
- Or use `--auth-key` with reusable key

✅ **Use check mode for root access**: Requires recent SSO re-authentication

✅ **Principle of least privilege**: Grant only necessary ports in ACLs
```json
{
  "grants": [{
    "src": ["group:devs"],
    "dst": ["tag:dev"],
    "ip": ["22", "80", "443"]  // Only SSH and HTTP(S)
  }]
}
```

✅ **Enable Tailnet Lock** (enterprise): Cryptographically prevent unauthorized device additions

### Operations

✅ **Use auth keys for automation**:
```bash
# Generate in admin console → Settings → Keys
sudo tailscale up --auth-key=tskey-auth-...
```

✅ **Tag infrastructure servers**: Enables service accounts instead of personal ownership

✅ **Set up high-availability**:
```bash
# Multiple subnet routers with same routes = automatic failover
# Router 1
sudo tailscale up --advertise-routes=10.0.0.0/24

# Router 2  
sudo tailscale up --advertise-routes=10.0.0.0/24
```

✅ **Use GitOps for ACLs**: Version control your policy file with GitHub/GitLab

✅ **Monitor with logging**: Enable network flow logs (Enterprise feature)

### Performance

✅ **Enable UDP GRO forwarding** (Linux subnet routers):
```bash
NETDEV=$(ip -o route get 8.8.8.8 | cut -f 5 -d " ")
sudo ethtool -K $NETDEV rx-udp-gro-forwarding on rx-gro-list off
```

✅ **Prefer direct connections**: Check with `tailscale status` - look for "direct"

✅ **Use appropriate MTU**: Usually auto-detected correctly, but can tune if needed

## Reference Files

- `references/cli-reference.md` - Complete CLI command reference with all flags
- `references/acl-examples.md` - Detailed ACL and grants configuration examples
- `references/api-usage.md` - Tailscale API integration and automation
- `references/troubleshooting.md` - Comprehensive troubleshooting guide
- `references/production-setup.md` - Best practices for production deployments
- `scripts/setup_subnet_router.sh` - Automated subnet router setup script
- `scripts/setup_exit_node.sh` - Automated exit node setup script
