---
name: tunneling
description: Create free SSH tunnels to expose local ports to the internet using tinyfi.sh. Use when you need to share a locally running app, test webhooks, demo a prototype, or get a public HTTPS URL for any local service — no signup or authentication required.
---

# TinyFish Tunneling Service (tinyfi.sh)

Creates instant public HTTPS URLs for locally running apps via SSH tunneling. Free, no account, no installation beyond SSH.

## Pre-flight Check (REQUIRED)

Verify SSH is available (it almost always is):

```bash
which ssh && echo "SSH available" || echo "SSH not found — install OpenSSH first"
```

## Quick Start

Expose a local port to the internet:

```bash
ssh -o StrictHostKeyChecking=accept-new -R 80:localhost:<PORT> tinyfi.sh
```

Replace `<PORT>` with the port your app is running on. The command will print a public `https://<random>.tinyfi.sh` URL.

## Custom Subdomain

Request a specific subdomain instead of a random one:

```bash
ssh -o StrictHostKeyChecking=accept-new -R myname:80:localhost:<PORT> tinyfi.sh
```

This gives you `https://myname.tinyfi.sh`.

## Keep-Alive (Stable Connections)

For long-running tunnels, add a keep-alive interval to prevent disconnection:

```bash
ssh -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=60 -R 80:localhost:<PORT> tinyfi.sh
```

## Usage Guidelines

When starting a tunnel for the user:

1. **Ask which port** to expose if not already specified
2. **Run the SSH command** in the background so the agent can continue working
3. **Report the public URL** back to the user once the tunnel is established
4. The tunnel stays open as long as the SSH connection is alive

## Common Ports

| Framework / Tool     | Default Port |
|----------------------|-------------|
| Next.js / React / Express | 3000   |
| Vite                 | 5173        |
| Django               | 8000        |
| Flask                | 5000        |
| Go (net/http)        | 8080        |
| Ruby on Rails        | 3000        |
| PHP (built-in)       | 8000        |

## Rate Limits

- 5 SSH connections per minute per IP
- 100 HTTP requests per minute per IP
- 50 concurrent connections max
- 48-hour idle timeout

