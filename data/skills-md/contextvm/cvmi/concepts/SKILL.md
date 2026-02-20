---
name: concepts
description: Understand ContextVM core concepts, architecture decisions, and frequently asked questions. Use when users need clarification on what ContextVM is, why it uses Nostr, decentralization benefits, public vs private servers, network topology, or comparisons with traditional MCP.
---

# ContextVM Concepts

Core concepts, architectural decisions, and common questions about ContextVM.

## What is ContextVM?

ContextVM is a protocol that liberates the Model Context Protocol (MCP) by running it over Nostr—a simple, open communication network built on cryptographic, censorship-resistant, and permissionless foundations.

Rather than relying on centralized infrastructure like domains, OAuth, or cloud hosting, ContextVM allows anyone to run or access services using only Nostr and an internet-connected device.

**Key Insight**: ContextVM operates at the **transport layer**, meaning existing MCP servers and clients can be used without code changes through the Gateway and Proxy tools.

## Why Run MCP Over Nostr?

Running MCP over Nostr eliminates traditional infrastructure barriers:

| Traditional Requirement | Nostr Solution |
|------------------------|----------------|
| Domain name + DNS | Not needed |
| Static IP address | Not needed |
| OAuth/API keys | Built-in public key cryptography |
| Public hosting | Any device with internet |
| Port forwarding | Outbound-only relay connections |

Nostr provides:
- **Identity** via public/private key cryptography
- **Discovery** through service announcements on relays
- **Transport** via signed and encrypted events
- **Payments** (optional) using Bitcoin and Lightning Network

## Decentralization Model

ContextVM uses Nostr relays as a **distributed message bus**:

```
Client ⇄ Nostr Relay(s) ⇄ Server
```

- No central directory or gatekeeper
- Anyone can run a server and announce it (or keep it private)
- Servers can connect to multiple relays for redundancy
- Services can go offline and come back online without breaking references

## The Dual API Advantage

ContextVM presents a unique dual API that lets you write your server once and make it accessible to both humans and machines:

**For Developers**: Build web apps, desktop applications, or CLI tools that interact with ContextVM servers directly using standard MCP patterns.

**For AI Agents**: LLMs operate the same service naturally through MCP's self-documenting capabilities (tools/list, schemas, etc.).

**Build Once, Deploy Everywhere**: Your service becomes a reusable component accessible through code, web interfaces, or AI agents.

## Public vs Private Servers

| Feature | Public Server | Private Server |
|---------|---------------|----------------|
| **Announcements** | Published to relays | Not published |
| **Discovery** | Via relay queries | Known public key only |
| **Access Control** | Open or whitelisted | Whitelisted |
| **Encryption** | E2E encrypted | E2E encrypted |
| **Payments** | Optional | Optional |

**Use Private Servers For**: Personal tools, team infrastructure, sensitive operations, development/testing.

## Network Topology

Communication flows through three actors:

1. **Client**: MCP client using ContextVM Proxy or SDK
2. **Relay(s)**: WebSocket servers routing encrypted events
3. **Server**: Service using ContextVM Gateway or SDK

**Flow**:
1. Server optionally publishes announcement to relays
2. Client discovers service (public) or uses known pubkey (private)
3. Client sends encrypted request via relays
4. Server receives, decrypts, processes, responds

All messages are signed and end-to-end encrypted (NIP-44).

## ContextVM vs Traditional Remote MCP

| Requirement | Traditional MCP (HTTP/SSE) | ContextVM |
|-------------|---------------------------|-----------|
| Domain name | Required | Not needed |
| DNS configuration | Required | Not needed |
| Static IP | Required | Not needed |
| Port forwarding | Required | Not needed |
| TLS certificate | Required | Implicit via encryption |
| Authentication | OAuth/API keys | Built-in pubkey crypto |
| Hosting | Cloud VM/VPS | Any device |
| Discovery | Centralized directories | Decentralized relays |
| Censorship resistance | Low | High |

## Authentication

Authentication is built into Nostr's public key cryptography:

- Every request is **signed** by the client's private key
- Servers verify signatures to confirm identity
- Server operators can:
  - Allow all signed requests (open access)
  - Whitelist specific public keys (private access)
  - Require payment before processing

No OAuth, passwords, or API keys needed.

## Security

All client-server communication is **end-to-end encrypted** using NIP-44:

- Messages encrypted to recipient's public key
- Only intended party can decrypt
- Compromised relays cannot read content or impersonate parties
- Ensures confidentiality, integrity, and non-repudiation

## MCP Possibilities Beyond AI

MCP is a protocol for invoking remote functions—any computational task, not just AI:

- **SSH Access Portal**: Secure remote machine access
- **Encryption as a Service**: GPG operations in sandboxed environment
- **Data Processing**: Validate, transform, analyze data on demand
- **Code Sandbox**: Execute untrusted code safely
- **IoT Command Hub**: Trigger physical actions remotely
- **Math & Simulation**: Complex calculations or symbolic math

## Getting Started

### Deploy a Server (Gateway)
```bash
gateway-cli --private-key "your-key" \
  --relays "wss://relay.nostr.org" \
  --server "python my-mcp-server.py" \
  --public  # omit for private server
```

### Connect a Client (Proxy)
```bash
proxy-cli --private-key "your-key" \
  --relays "wss://relay.nostr.org" \
  --server-pubkey "npub1..."
```

### Build Native (SDK)
Use `@contextvm/sdk` for TypeScript applications with `NostrServerTransport` and `NostrClientTransport`.

## References

- [`../overview/SKILL.md`](../overview/SKILL.md) — Protocol overview
- [`../server-dev/references/gateway-pattern.md`](../server-dev/references/gateway-pattern.md) — Gateway usage
- [ContextVM Docs](https://docs.contextvm.org)
- [GitHub](https://github.com/contextvm)
