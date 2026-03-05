---
name: ssh-hardening
description: Harden SSH configuration on VPS servers by disabling root login, enforcing SSH key authentication, and creating non-root sudo users to prevent unauthorized access.
license: MIT
compatibility: Ubuntu, Debian, CentOS, RHEL, and most Linux distributions
metadata:
  author: secure-server-skill
  version: "1.0"
  category: security
allowed-tools: Bash(adduser:*, usermod:*, ssh-keygen:*, ssh-copy-id:*, systemctl:*, nano:*, vim:*)
---

# SSH Hardening Skill

Secure SSH access to VPS servers by implementing industry-standard hardening practices.

## What This Skill Does

This skill helps AI agents harden SSH configuration on VPS servers. SSH is the primary entry point for server management, making it a critical attack vector. Proper SSH hardening prevents unauthorized access, brute-force attacks, and credential theft.

**Key capabilities:**

- Create non-root users with sudo privileges
- Generate and configure SSH key authentication
- Disable password-based authentication
- Disable root login over SSH
- Configure security settings in sshd_config
- Test configuration before applying

## When to Use

Use this skill when you need to:

- Set up a new VPS server with secure SSH access
- Replace password authentication with SSH keys
- Disable root login for security compliance
- Harden an existing server against brute-force attacks
- Fix security audit findings related to SSH
- Implement principle of least privilege

**Critical understanding:** Root can do anything. One typo, one compromised session, and your entire system is gone. Passwords can be guessed. SSH keys can't be brute-forced in any practical timeframe.

## Prerequisites

- Root or existing sudo user access to the server
- SSH access to the server (keep current session open!)
- SSH client on local machine (ssh, ssh-keygen, ssh-copy-id)
- Terminal access to local machine

## SSH Hardening Steps

### Step 1: Create Non-Root User

**CRITICAL:** Complete this step and test before disabling root login!

Create a new user for daily operations:

```bash
# Create user (replace 'deployer' with desired username)
sudo adduser deployer
```

Enter a strong password when prompted.

Add user to sudo group:

```bash
sudo usermod -aG sudo deployer
```

**Test sudo access** before proceeding:

```bash
# Switch to new user
su - deployer

# Test sudo
sudo whoami
# Should output: root

# Exit back to original user
exit
```

### Step 2: Generate SSH Key Pair (Local Machine)

On your **local machine** (not the server), generate an SSH key:

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

**Key type explained:**

- `ed25519` - Modern, secure, fast (recommended)
- Alternative: `rsa -b 4096` for older systems

**When prompted:**

- Press Enter to save to default location (`~/.ssh/id_ed25519`)
- Enter a strong passphrase (recommended) or leave empty

### Step 3: Copy SSH Key to Server

From your **local machine**, copy the public key to the server:

```bash
ssh-copy-id deployer@your-server-ip
```

Enter the user's password when prompted.

**Manual alternative** (if ssh-copy-id is unavailable):

```bash
# On local machine, display public key
cat ~/.ssh/id_ed25519.pub

# On server, as the new user
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
# Paste the public key, save and exit
chmod 600 ~/.ssh/authorized_keys
```

### Step 4: Test SSH Key Authentication

**CRITICAL:** Test in a NEW terminal window, keep existing session open!

```bash
ssh deployer@your-server-ip
```

You should connect without entering a password (or only your SSH key passphrase).

**If connection fails, DO NOT proceed to Step 5!** Debug the issue first.

### Step 5: Harden SSH Configuration

**WARNING:** Make these changes carefully. Test in a new terminal before closing existing sessions!

Edit SSH daemon configuration:

```bash
sudo nano /etc/ssh/sshd_config
```

Update or add these settings:

```
# Disable root login
PermitRootLogin no

# Disable password authentication
PasswordAuthentication no

# Disable empty passwords
PermitEmptyPasswords no

# Limit authentication attempts
MaxAuthTries 3

# Allow only specific users (optional but recommended)
AllowUsers deployer

# Use only SSH protocol 2
Protocol 2

# Disable X11 forwarding (unless needed)
X11Forwarding no

# Set login grace time
LoginGraceTime 60

# Disable host-based authentication
HostbasedAuthentication no
```

**Optional advanced settings:**

```
# Change default port (security through obscurity, optional)
# Port 2222

# Disable agent forwarding (unless needed)
# AllowAgentForwarding no

# Disable TCP forwarding (unless needed)
# AllowTcpForwarding no

# Set idle timeout
# ClientAliveInterval 300
# ClientAliveCountMax 2
```

### Step 6: Test Configuration

Test the configuration file for syntax errors:

```bash
sudo sshd -t
```

No output means the configuration is valid.

### Step 7: Restart SSH Service

**CRITICAL:** Test in a new terminal BEFORE restarting!

```bash
# Test connection in NEW terminal first
ssh deployer@your-server-ip

# If successful, restart SSH (in original terminal)
sudo systemctl restart sshd
```

**Verification:**

```bash
sudo systemctl status sshd
```

### Step 8: Verify Root Login is Disabled

Try to connect as root (should fail):

```bash
ssh root@your-server-ip
```

Expected result: `Permission denied (publickey)`

## Configuration Reference

### AllowUsers vs AllowGroups

Restrict SSH access to specific users or groups:

```
# Option 1: Specific users
AllowUsers deployer admin

# Option 2: Users in specific group
AllowGroups sshusers
```

### Port Changes

Changing the default SSH port (22) reduces noise from automated scanners:

```
Port 2222
```

**Remember to:**

1. Update firewall rules before restarting SSH
2. Use the new port when connecting: `ssh -p 2222 user@host`

### Key-Based Authentication Only

Ensure these settings work together:

```
PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication no
UsePAM yes
```

## Security Best Practices

1. **Always test before closing sessions** - Keep one session open until verified
2. **Use SSH key passphrases** - Adds another layer of security
3. **Limit user access** - Use AllowUsers or AllowGroups
4. **Monitor authentication logs** - Check `/var/log/auth.log` regularly
5. **Use fail2ban** - Add automated banning for repeated failed attempts
6. **Regular key rotation** - Periodically generate new keys
7. **Disable unused features** - X11Forwarding, TCP forwarding, etc.

## Troubleshooting

### Locked Out of Server

Prevention is key:

- Always keep one session open when making changes
- Test in a new terminal before closing existing sessions
- Have console access via hosting provider's control panel

Recovery:

- Use hosting provider's console/VNC access
- Revert changes to `/etc/ssh/sshd_config`
- Restart sshd service

### SSH Key Not Working

```bash
# Check file permissions on server
ls -la ~/.ssh/
# Should show:
# drwx------ .ssh/
# -rw------- authorized_keys

# Fix permissions if needed
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Check SSH logs
sudo tail -f /var/log/auth.log
```

### Connection Refused After Changes

```bash
# Check SSH service status
sudo systemctl status sshd

# View recent errors
sudo journalctl -u sshd -n 50

# Test configuration
sudo sshd -t
```

## Common Mistakes to Avoid

- ❌ Closing all SSH sessions before testing new configuration
- ❌ Disabling password auth before setting up SSH keys
- ❌ Not testing sudo access for new user
- ❌ Typos in sshd_config causing service failure
- ❌ Forgetting to restart sshd after changes
- ❌ Not updating firewall when changing SSH port

## Additional Resources

See [references/sshd-config.md](references/sshd-config.md) for complete sshd_config reference.

See [scripts/setup-ssh-hardening.sh](scripts/setup-ssh-hardening.sh) for automated setup script.

## Related Skills

- `firewall-configuration` - Restrict SSH port access
- `fail2ban-setup` - Auto-ban brute-force attempts
- `auto-updates` - Keep SSH patched against vulnerabilities
