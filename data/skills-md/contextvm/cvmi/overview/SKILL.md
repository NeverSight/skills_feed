---
name: overview
description: Understand ContextVM protocol fundamentals, architecture, and core concepts. Use when users need to learn about ContextVM basics, how it bridges MCP with Nostr, protocol design principles, event kinds, or the relationship between MCP and Nostr in decentralized communication.
---

# ContextVM Overview

ContextVM (Context Virtual Machine) is a protocol that bridges the Model Context Protocol (MCP) with the Nostr network, enabling decentralized communication between MCP servers and clients.

## Core Concept

ContextVM operates as a **transport layer** for MCP, using Nostr's relay network as the communication mechanism while preserving MCP's JSON-RPC semantics.

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Application Layer                     │
│         (Tools, Resources, Prompts, Sampling)               │
├─────────────────────────────────────────────────────────────┤
│                 ContextVM Transport Layer                    │
│    (Nostr events, Encryption, Public Key Cryptography)      │
├─────────────────────────────────────────────────────────────┤
│                     Nostr Relay Network                      │
│              (wss://relay.contextvm.org, etc.)              │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

- **Decentralized Communication**: No central servers required; use Nostr's distributed relay network
- **Security First**: Leverages Nostr's cryptographic primitives for verification and authorization
- **Public Key Identity**: Servers and clients identified by Nostr public keys
- **Optional Encryption**: End-to-end encryption via NIP-44 gift wrapping
- **Server Discovery**: Public server announcements via replaceable events

## Protocol Architecture

### Three-Layer Design

1. **Transport Layer**: Nostr events and relays
2. **Message Layer**: JSON-RPC MCP messages embedded in event content
3. **Metadata Layer**: Nostr event tags for addressing and correlation

### Main Actors

| Actor       | Role                        | Identification      |
| ----------- | --------------------------- | ------------------- |
| **Servers** | Expose MCP capabilities     | Public key + relays |
| **Clients** | Consume server capabilities | Public key          |
| **Relays**  | Propagate messages          | URL (wss://...)     |

## Event Kinds

ContextVM uses these Nostr event kinds:

| Kind    | Purpose                            | Persistence          |
| ------- | ---------------------------------- | -------------------- |
| `25910` | All ContextVM messages (ephemeral) | Not stored by relays |
| `11316` | Server announcement                | Replaceable          |
| `11317` | Tools list                         | Replaceable          |
| `11318` | Resources list                     | Replaceable          |
| `11319` | Resource templates list            | Replaceable          |
| `11320` | Prompts list                       | Replaceable          |
| `1059`  | Gift wrap (encrypted messages)     | Ephemeral            |

## Message Flow

### Connection Process

1. **Discovery**: Client discovers server via public key or relay queries
2. **Initialization**: Standard MCP handshake over Nostr
3. **Operation**: Client calls tools/lists resources via kind 25910 events
4. **Termination**: Connection closes when either party disconnects

### Event Structure

```json
{
  "kind": 25910,
  "pubkey": "<sender-public-key>",
  "content": "{\"jsonrpc\":\"2.0\",...}",
  "tags": [
    ["p", "<recipient-public-key>"],
    ["e", "<correlation-event-id>"]
  ]
}
```

## Security Model

### Public Key Cryptography

- All messages cryptographically signed
- Server identity = public key (portable across relays)
- Client authorization via public key whitelisting

### Encryption (CEP-4)

- Optional NIP-44 encryption via gift wrap (kind 1059)
- Negotiated during initialization
- Servers advertise support via `support_encryption` tag

## The Nostr Way

ContextVM follows the same core pattern as other Nostr-based RPC systems (like DVMs): publish a signed request event, listen for a correlated response. The difference is in the message structure—CVM uses JSON-RPC via MCP rather than provider-specific payloads.

To understand this foundation:

- Read [`references/nostr-way-without-sdks.md`](../client-dev/references/nostr-way-without-sdks.md) — The Nostr primitives behind CVM (for non-SDK implementations)

## Reference Materials

For detailed specifications, see:

- [`references/protocol-spec.md`](references/protocol-spec.md) - Full protocol specification
- [`references/ceps.md`](references/ceps.md) - ContextVM Enhancement Proposals
- [`references/mcp-integration.md`](references/mcp-integration.md) - MCP protocol integration details

## Ecosystem Navigation (what to use when)

Use this decision table to jump to the right component / skill:

| Goal                                               | Recommended path                     | Skill                                                                                                            |
| -------------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| Learn the protocol and message kinds               | Read spec + CEPs                     | [`SKILL.md`](SKILL.md) + [`references/protocol-spec.md`](references/protocol-spec.md)                            |
| Understand core concepts, architecture, FAQs       | Concepts and architectural overview  | [`../concepts/SKILL.md`](../concepts/SKILL.md)                                               |
| Build a new ContextVM-native server                | `McpServer` + `NostrServerTransport` | [`../server-dev/SKILL.md`](../server-dev/SKILL.md)                                           |
| Build a new ContextVM-native client                | `Client` + `NostrClientTransport`    | [`../client-dev/SKILL.md`](../client-dev/SKILL.md)                                           |
| Bridge an existing MCP server to Nostr             | Gateway pattern (`NostrMCPGateway`)  | [`../server-dev/references/gateway-pattern.md`](../server-dev/references/gateway-pattern.md) |
| Bridge an existing MCP client to Nostr             | Proxy pattern (`NostrMCPProxy`)      | [`../client-dev/references/proxy-pattern.md`](../client-dev/references/proxy-pattern.md)     |
| SDK-level details (interfaces, constants, logging)   | `@contextvm/sdk` reference           | [`../typescript-sdk/SKILL.md`](../typescript-sdk/SKILL.md)                                   |
| Add payments to capabilities (CEP-8)                 | Payments middleware + processors     | [`../payments/SKILL.md`](../payments/SKILL.md)                                               |
| Production operations (keys, Docker, monitoring)     | Deployment checklist                 | [`../deployment/SKILL.md`](../deployment/SKILL.md)                                           |
| Diagnose connection issues, errors, failures       | Troubleshooting guide                | [`../troubleshooting/SKILL.md`](../troubleshooting/SKILL.md)                                 |

Useful public entry points:

- ContextVM docs: https://docs.contextvm.org
- ContextVM org: https://contextvm.org
