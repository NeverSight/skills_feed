---
name: nostr
description: This skill should be used when working with the Nostr protocol, implementing Nostr clients or relays, handling Nostr events, or discussing Nostr Implementation Possibilities (NIPs). Provides comprehensive knowledge of Nostr's decentralized protocol, event structure, cryptographic operations, and all standard NIPs.
---

# Nostr Protocol Expert

## Purpose

This skill provides expert-level assistance with the Nostr protocol, a simple, open protocol for global, decentralized, and censorship-resistant social networks. The protocol is built on relays and cryptographic keys, enabling direct peer-to-peer communication without central servers.

## When to Use

Activate this skill when:
- Implementing Nostr clients or relays
- Working with Nostr events and messages
- Handling cryptographic signatures and keys (schnorr signatures on secp256k1)
- Implementing any Nostr Implementation Possibility (NIP)
- Building social networking features on Nostr
- Querying or filtering Nostr events
- Discussing Nostr protocol architecture
- Implementing WebSocket communication with relays

## Core Concepts

### The Protocol Foundation

Nostr operates on two main components:
1. **Clients** - Applications users run to read/write data
2. **Relays** - Servers that store and forward messages

Key principles:
- Everyone runs a client
- Anyone can run a relay
- Users identified by public keys
- Messages signed with private keys
- No central authority or trusted servers

### Events Structure

All data in Nostr is represented as events. An event is a JSON object with this structure:

```json
{
  "id": "<32-bytes lowercase hex-encoded sha256 of the serialized event data>",
  "pubkey": "<32-bytes lowercase hex-encoded public key of the event creator>",
  "created_at": "<unix timestamp in seconds>",
  "kind": "<integer identifying event type>",
  "tags": [
    ["<tag name>", "<tag value>", "<optional third param>", "..."]
  ],
  "content": "<arbitrary string>",
  "sig": "<64-bytes lowercase hex of the schnorr signature of the sha256 hash of the serialized event data>"
}
```

### Event Kinds

Standard event kinds (from various NIPs):
- `0` - Metadata (user profile)
- `1` - Text note (short post)
- `2` - Recommend relay
- `3` - Contacts (following list)
- `4` - Encrypted direct messages
- `5` - Event deletion
- `6` - Repost
- `7` - Reaction (like, emoji reaction)
- `40` - Channel creation
- `41` - Channel metadata
- `42` - Channel message
- `43` - Channel hide message
- `44` - Channel mute user
- `1000-9999` - Regular events
- `10000-19999` - Replaceable events
- `20000-29999` - Ephemeral events
- `30000-39999` - Parameterized replaceable events

### Tags

Common tag types:
- `["e", "<event-id>", "<relay-url>", "<marker>"]` - Reference to an event
- `["p", "<pubkey>", "<relay-url>"]` - Reference to a user
- `["a", "<kind>:<pubkey>:<d-tag>", "<relay-url>"]` - Reference to a replaceable event
- `["d", "<identifier>"]` - Identifier for parameterized replaceable events
- `["r", "<url>"]` - Reference/link to a web resource
- `["t", "<hashtag>"]` - Hashtag
- `["g", "<geohash>"]` - Geolocation
- `["nonce", "<number>", "<difficulty>"]` - Proof of work
- `["subject", "<subject>"]` - Subject/title
- `["client", "<client-name>"]` - Client application used

## Key NIPs Reference

For detailed specifications, refer to **references/nips-overview.md**.

### Core Protocol NIPs

#### NIP-01: Basic Protocol Flow
The foundation of Nostr. Defines:
- Event structure and validation
- Event ID calculation (SHA256 of serialized event)
- Signature verification (schnorr signatures)
- Client-relay communication via WebSocket
- Message types: EVENT, REQ, CLOSE, EOSE, OK, NOTICE

#### NIP-02: Contact List and Petnames
Event kind `3` for following lists:
- Each `p` tag represents a followed user
- Optional relay URL and petname in tag
- Replaceable event (latest overwrites)

#### NIP-04: Encrypted Direct Messages
Event kind `4` for private messages:
- Content encrypted with shared secret (ECDH)
- `p` tag for recipient pubkey
- Deprecated in favor of NIP-44

#### NIP-05: Mapping Nostr Keys to DNS
Internet identifier format: `name@domain.com`
- `.well-known/nostr.json` endpoint
- Maps names to pubkeys
- Optional relay list

#### NIP-09: Event Deletion
Event kind `5` to request deletion:
- Contains `e` tags for events to delete
- Relays should delete referenced events
- Only works for own events

#### NIP-10: Text Note References (Threads)
Conventions for `e` and `p` tags in replies:
- Root event reference
- Reply event reference
- Mentions
- Marker types: "root", "reply", "mention"

#### NIP-11: Relay Information Document
HTTP endpoint for relay metadata:
- GET request to relay URL
- Returns JSON with relay information
- Supported NIPs, software, limitations

### Social Features NIPs

#### NIP-25: Reactions
Event kind `7` for reactions:
- Content usually "+" (like) or emoji
- `e` tag for reacted event
- `p` tag for event author

#### NIP-42: Authentication
Client authentication to relays:
- AUTH message from relay
- Client responds with event kind `22242`
- Proves key ownership

#### NIP-50: Search
Query filter extension for full-text search:
- `search` field in REQ filters
- Implementation-defined behavior

### Advanced NIPs

#### NIP-19: bech32-encoded Entities
Human-readable identifiers:
- `npub`: public key
- `nsec`: private key (sensitive!)
- `note`: note/event ID
- `nprofile`: profile with relay hints
- `nevent`: event with relay hints
- `naddr`: replaceable event coordinate

#### NIP-44: Encrypted Payloads
Improved encryption for direct messages:
- Versioned encryption scheme
- Better security than NIP-04
- ChaCha20-Poly1305 AEAD

#### NIP-65: Relay List Metadata
Event kind `10002` for relay lists:
- Read/write relay preferences
- Optimizes relay discovery
- Replaceable event

## Client-Relay Communication

### WebSocket Messages

#### From Client to Relay

**EVENT** - Publish an event:
```json
["EVENT", <event JSON>]
```

**REQ** - Request events (subscription):
```json
["REQ", <subscription_id>, <filters JSON>, <filters JSON>, ...]
```

**CLOSE** - Stop a subscription:
```json
["CLOSE", <subscription_id>]
```

**AUTH** - Respond to auth challenge:
```json
["AUTH", <signed event kind 22242>]
```

#### From Relay to Client

**EVENT** - Send event to client:
```json
["EVENT", <subscription_id>, <event JSON>]
```

**OK** - Acceptance/rejection notice:
```json
["OK", <event_id>, <true|false>, <message>]
```

**EOSE** - End of stored events:
```json
["EOSE", <subscription_id>]
```

**CLOSED** - Subscription closed:
```json
["CLOSED", <subscription_id>, <message>]
```

**NOTICE** - Human-readable message:
```json
["NOTICE", <message>]
```

**AUTH** - Authentication challenge:
```json
["AUTH", <challenge>]
```

### Filter Objects

Filters select events in REQ messages:

```json
{
  "ids": ["<event-id>", ...],
  "authors": ["<pubkey>", ...],
  "kinds": [<kind number>, ...],
  "#e": ["<event-id>", ...],
  "#p": ["<pubkey>", ...],
  "#a": ["<coordinate>", ...],
  "#t": ["<hashtag>", ...],
  "since": <unix timestamp>,
  "until": <unix timestamp>,
  "limit": <max number of events>
}
```

Filtering rules:
- Arrays are ORed together
- Different fields are ANDed
- Tag filters: `#<single-letter>` matches tag values
- Prefix matching allowed for `ids` and `authors`

## Cryptographic Operations

### Key Management

- **Private Key**: 32-byte random value, keep secure
- **Public Key**: Derived via secp256k1
- **Encoding**: Hex (lowercase) or bech32

### Event Signing (schnorr)

Steps to create a signed event:
1. Set all fields except `id` and `sig`
2. Serialize event data to JSON (specific order)
3. Calculate SHA256 hash → `id`
4. Sign `id` with schnorr signature → `sig`

Serialization format for ID calculation:
```json
[
  0,
  <pubkey>,
  <created_at>,
  <kind>,
  <tags>,
  <content>
]
```

### Event Verification

Steps to verify an event:
1. Verify ID matches SHA256 of serialized data
2. Verify signature is valid schnorr signature
3. Check created_at is reasonable (not far future)
4. Validate event structure and required fields

## Implementation Best Practices

### For Clients

1. **Connect to Multiple Relays**: Don't rely on single relay
2. **Cache Events**: Reduce redundant relay queries
3. **Verify Signatures**: Always verify event signatures
4. **Handle Replaceable Events**: Keep only latest version
5. **Respect User Privacy**: Careful with sensitive data
6. **Implement NIP-65**: Use user's preferred relays
7. **Proper Error Handling**: Handle relay disconnections
8. **Pagination**: Use `limit`, `since`, `until` for queries

### For Relays

1. **Validate Events**: Check signatures, IDs, structure
2. **Rate Limiting**: Prevent spam and abuse
3. **Storage Management**: Ephemeral events, retention policies
4. **Implement NIP-11**: Provide relay information
5. **WebSocket Optimization**: Handle many connections
6. **Filter Optimization**: Efficient event querying
7. **Consider NIP-42**: Authentication for write access
8. **Performance**: Index by pubkey, kind, tags, timestamp

### Security Considerations

1. **Never Expose Private Keys**: Handle nsec carefully
2. **Validate All Input**: Prevent injection attacks
3. **Use NIP-44**: For encrypted messages (not NIP-04)
4. **Check Event Timestamps**: Reject far-future events
5. **Implement Proof of Work**: NIP-13 for spam prevention
6. **Sanitize Content**: XSS prevention in displayed content
7. **Relay Trust**: Don't trust single relay for critical data

## Common Patterns

### Publishing a Note

```javascript
const event = {
  pubkey: userPublicKey,
  created_at: Math.floor(Date.now() / 1000),
  kind: 1,
  tags: [],
  content: "Hello Nostr!",
}
// Calculate ID and sign
event.id = calculateId(event)
event.sig = signEvent(event, privateKey)
// Publish to relay
ws.send(JSON.stringify(["EVENT", event]))
```

### Subscribing to Notes

```javascript
const filter = {
  kinds: [1],
  authors: [followedPubkey1, followedPubkey2],
  limit: 50
}
ws.send(JSON.stringify(["REQ", "my-sub", filter]))
```

### Replying to a Note

```javascript
const reply = {
  kind: 1,
  tags: [
    ["e", originalEventId, relayUrl, "root"],
    ["p", originalAuthorPubkey]
  ],
  content: "Great post!",
  // ... other fields
}
```

### Reacting to a Note

```javascript
const reaction = {
  kind: 7,
  tags: [
    ["e", eventId],
    ["p", eventAuthorPubkey]
  ],
  content: "+", // or emoji
  // ... other fields
}
```

## Development Resources

### Essential NIPs for Beginners

Start with these NIPs in order:
1. **NIP-01** - Basic protocol (MUST read)
2. **NIP-19** - Bech32 identifiers
3. **NIP-02** - Following lists
4. **NIP-10** - Threaded conversations
5. **NIP-25** - Reactions
6. **NIP-65** - Relay lists

### Testing and Development

- **Relay Implementations**: nostream, strfry, relay.py
- **Test Relays**: wss://relay.damus.io, wss://nos.lol
- **Libraries**: nostr-tools (JS), rust-nostr (Rust), python-nostr (Python)
- **Development Tools**: NostrDebug, Nostr Army Knife, nostril
- **Reference Clients**: Damus (iOS), Amethyst (Android), Snort (Web)

### Key Repositories

- **NIPs Repository**: https://github.com/nostr-protocol/nips
- **Awesome Nostr**: https://github.com/aljazceru/awesome-nostr
- **Nostr Resources**: https://nostr.how

## Reference Files

For comprehensive NIP details, see:
- **references/nips-overview.md** - Detailed descriptions of all standard NIPs
- **references/event-kinds.md** - Complete event kinds reference
- **references/common-mistakes.md** - Pitfalls and how to avoid them

## Quick Checklist

When implementing Nostr:
- [ ] Events have all required fields (id, pubkey, created_at, kind, tags, content, sig)
- [ ] Event IDs calculated correctly (SHA256 of serialization)
- [ ] Signatures verified (schnorr on secp256k1)
- [ ] WebSocket messages properly formatted
- [ ] Filter queries optimized with appropriate limits
- [ ] Handling replaceable events correctly
- [ ] Connected to multiple relays for redundancy
- [ ] Following relevant NIPs for features implemented
- [ ] Private keys never exposed or transmitted
- [ ] Event timestamps validated

## Official Resources

- **NIPs Repository**: https://github.com/nostr-protocol/nips
- **Nostr Website**: https://nostr.com
- **Nostr Documentation**: https://nostr.how
- **NIP Status**: https://nostr-nips.com

