---
name: nostr-tools
description: This skill should be used when working with nostr-tools library for Nostr protocol operations, including event creation, signing, filtering, relay communication, and NIP implementations. Provides comprehensive knowledge of nostr-tools APIs and patterns.
---

# nostr-tools Skill

This skill provides comprehensive knowledge and patterns for working with nostr-tools, the most popular JavaScript/TypeScript library for Nostr protocol development.

## When to Use This Skill

Use this skill when:
- Building Nostr clients or applications
- Creating and signing Nostr events
- Connecting to Nostr relays
- Implementing NIP features
- Working with Nostr keys and cryptography
- Filtering and querying events
- Building relay pools or connections
- Implementing NIP-44/NIP-04 encryption

## Core Concepts

### nostr-tools Overview

nostr-tools provides:
- **Event handling** - Create, sign, verify events
- **Key management** - Generate, convert, encode keys
- **Relay communication** - Connect, subscribe, publish
- **NIP implementations** - NIP-04, NIP-05, NIP-19, NIP-44, etc.
- **Cryptographic operations** - Schnorr signatures, encryption
- **Filter building** - Query events by various criteria

### Installation

```bash
npm install nostr-tools
```

### Basic Imports

```javascript
// Core functionality
import {
  SimplePool,
  generateSecretKey,
  getPublicKey,
  finalizeEvent,
  verifyEvent
} from 'nostr-tools';

// NIP-specific imports
import { nip04, nip05, nip19, nip44 } from 'nostr-tools';

// Relay operations
import { Relay } from 'nostr-tools/relay';
```

## Key Management

### Generating Keys

```javascript
import { generateSecretKey, getPublicKey } from 'nostr-tools/pure';

// Generate new secret key (Uint8Array)
const secretKey = generateSecretKey();

// Derive public key
const publicKey = getPublicKey(secretKey);

console.log('Secret key:', bytesToHex(secretKey));
console.log('Public key:', publicKey); // hex string
```

### Key Encoding (NIP-19)

```javascript
import { nip19 } from 'nostr-tools';

// Encode to bech32
const nsec = nip19.nsecEncode(secretKey);
const npub = nip19.npubEncode(publicKey);
const note = nip19.noteEncode(eventId);

console.log(nsec); // nsec1...
console.log(npub); // npub1...
console.log(note); // note1...

// Decode from bech32
const { type, data } = nip19.decode(npub);
// type: 'npub', data: publicKey (hex)

// Encode profile reference (nprofile)
const nprofile = nip19.nprofileEncode({
  pubkey: publicKey,
  relays: ['wss://relay.example.com']
});

// Encode event reference (nevent)
const nevent = nip19.neventEncode({
  id: eventId,
  relays: ['wss://relay.example.com'],
  author: publicKey,
  kind: 1
});

// Encode address (naddr) for replaceable events
const naddr = nip19.naddrEncode({
  identifier: 'my-article',
  pubkey: publicKey,
  kind: 30023,
  relays: ['wss://relay.example.com']
});
```

## Event Operations

### Event Structure

```javascript
// Unsigned event template
const eventTemplate = {
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [],
  content: 'Hello Nostr!'
};

// Signed event (after finalizeEvent)
const signedEvent = {
  id: '...', // 32-byte sha256 hash as hex
  pubkey: '...', // 32-byte public key as hex
  created_at: 1234567890,
  kind: 1,
  tags: [],
  content: 'Hello Nostr!',
  sig: '...' // 64-byte Schnorr signature as hex
};
```

### Creating and Signing Events

```javascript
import { finalizeEvent, verifyEvent } from 'nostr-tools/pure';

// Create event template
const eventTemplate = {
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [
    ['p', publicKey], // Mention
    ['e', eventId, '', 'reply'], // Reply
    ['t', 'nostr'] // Hashtag
  ],
  content: 'Hello Nostr!'
};

// Sign event
const signedEvent = finalizeEvent(eventTemplate, secretKey);

// Verify event
const isValid = verifyEvent(signedEvent);
console.log('Event valid:', isValid);
```

### Event Kinds

```javascript
// Common event kinds
const KINDS = {
  Metadata: 0,           // Profile metadata (NIP-01)
  Text: 1,               // Short text note (NIP-01)
  RecommendRelay: 2,     // Relay recommendation
  Contacts: 3,           // Contact list (NIP-02)
  EncryptedDM: 4,        // Encrypted DM (NIP-04)
  EventDeletion: 5,      // Delete events (NIP-09)
  Repost: 6,             // Repost (NIP-18)
  Reaction: 7,           // Reaction (NIP-25)
  ChannelCreation: 40,   // Channel (NIP-28)
  ChannelMessage: 42,    // Channel message
  Zap: 9735,             // Zap receipt (NIP-57)
  Report: 1984,          // Report (NIP-56)
  RelayList: 10002,      // Relay list (NIP-65)
  Article: 30023,        // Long-form content (NIP-23)
};
```

### Creating Specific Events

```javascript
// Profile metadata (kind 0)
const profileEvent = finalizeEvent({
  kind: 0,
  created_at: Math.floor(Date.now() / 1000),
  tags: [],
  content: JSON.stringify({
    name: 'Alice',
    about: 'Nostr enthusiast',
    picture: 'https://example.com/avatar.jpg',
    nip05: 'alice@example.com',
    lud16: 'alice@getalby.com'
  })
}, secretKey);

// Contact list (kind 3)
const contactsEvent = finalizeEvent({
  kind: 3,
  created_at: Math.floor(Date.now() / 1000),
  tags: [
    ['p', pubkey1, 'wss://relay1.com', 'alice'],
    ['p', pubkey2, 'wss://relay2.com', 'bob'],
    ['p', pubkey3, '', 'carol']
  ],
  content: '' // Or JSON relay preferences
}, secretKey);

// Reply to an event
const replyEvent = finalizeEvent({
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [
    ['e', rootEventId, '', 'root'],
    ['e', parentEventId, '', 'reply'],
    ['p', parentEventPubkey]
  ],
  content: 'This is a reply'
}, secretKey);

// Reaction (kind 7)
const reactionEvent = finalizeEvent({
  kind: 7,
  created_at: Math.floor(Date.now() / 1000),
  tags: [
    ['e', eventId],
    ['p', eventPubkey]
  ],
  content: '+' // or '-' or emoji
}, secretKey);

// Delete event (kind 5)
const deleteEvent = finalizeEvent({
  kind: 5,
  created_at: Math.floor(Date.now() / 1000),
  tags: [
    ['e', eventIdToDelete],
    ['e', anotherEventIdToDelete]
  ],
  content: 'Deletion reason'
}, secretKey);
```

## Relay Communication

### Using SimplePool

SimplePool is the recommended way to interact with multiple relays:

```javascript
import { SimplePool } from 'nostr-tools/pool';

const pool = new SimplePool();
const relays = [
  'wss://relay.damus.io',
  'wss://nos.lol',
  'wss://relay.nostr.band'
];

// Subscribe to events
const subscription = pool.subscribeMany(
  relays,
  [
    {
      kinds: [1],
      authors: [publicKey],
      limit: 10
    }
  ],
  {
    onevent(event) {
      console.log('Received event:', event);
    },
    oneose() {
      console.log('End of stored events');
    }
  }
);

// Close subscription when done
subscription.close();

// Publish event to all relays
const results = await Promise.allSettled(
  pool.publish(relays, signedEvent)
);

// Query events (returns Promise)
const events = await pool.querySync(relays, {
  kinds: [0],
  authors: [publicKey]
});

// Get single event
const event = await pool.get(relays, {
  ids: [eventId]
});

// Close pool when done
pool.close(relays);
```

### Direct Relay Connection

```javascript
import { Relay } from 'nostr-tools/relay';

const relay = await Relay.connect('wss://relay.damus.io');

console.log(`Connected to ${relay.url}`);

// Subscribe
const sub = relay.subscribe([
  {
    kinds: [1],
    limit: 100
  }
], {
  onevent(event) {
    console.log('Event:', event);
  },
  oneose() {
    console.log('EOSE');
    sub.close();
  }
});

// Publish
await relay.publish(signedEvent);

// Close
relay.close();
```

### Handling Connection States

```javascript
import { Relay } from 'nostr-tools/relay';

const relay = await Relay.connect('wss://relay.example.com');

// Listen for disconnect
relay.onclose = () => {
  console.log('Relay disconnected');
};

// Check connection status
console.log('Connected:', relay.connected);
```

## Filters

### Filter Structure

```javascript
const filter = {
  // Event IDs
  ids: ['abc123...'],

  // Authors (pubkeys)
  authors: ['pubkey1', 'pubkey2'],

  // Event kinds
  kinds: [1, 6, 7],

  // Tags (single-letter keys)
  '#e': ['eventId1', 'eventId2'],
  '#p': ['pubkey1'],
  '#t': ['nostr', 'bitcoin'],
  '#d': ['article-identifier'],

  // Time range
  since: 1704067200, // Unix timestamp
  until: 1704153600,

  // Limit results
  limit: 100,

  // Search (NIP-50, if relay supports)
  search: 'nostr protocol'
};
```

### Common Filter Patterns

```javascript
// User's recent posts
const userPosts = {
  kinds: [1],
  authors: [userPubkey],
  limit: 50
};

// User's profile
const userProfile = {
  kinds: [0],
  authors: [userPubkey]
};

// User's contacts
const userContacts = {
  kinds: [3],
  authors: [userPubkey]
};

// Replies to an event
const replies = {
  kinds: [1],
  '#e': [eventId]
};

// Reactions to an event
const reactions = {
  kinds: [7],
  '#e': [eventId]
};

// Feed from followed users
const feed = {
  kinds: [1, 6],
  authors: followedPubkeys,
  limit: 100
};

// Events mentioning user
const mentions = {
  kinds: [1],
  '#p': [userPubkey],
  limit: 50
};

// Hashtag search
const hashtagEvents = {
  kinds: [1],
  '#t': ['bitcoin'],
  limit: 100
};

// Replaceable event by d-tag
const replaceableEvent = {
  kinds: [30023],
  authors: [authorPubkey],
  '#d': ['article-slug']
};
```

### Multiple Filters

```javascript
// Subscribe with multiple filters (OR logic)
const filters = [
  { kinds: [1], authors: [userPubkey], limit: 20 },
  { kinds: [1], '#p': [userPubkey], limit: 20 }
];

pool.subscribeMany(relays, filters, {
  onevent(event) {
    // Receives events matching ANY filter
  }
});
```

## Encryption

### NIP-04 (Legacy DMs)

```javascript
import { nip04 } from 'nostr-tools';

// Encrypt message
const ciphertext = await nip04.encrypt(
  secretKey,
  recipientPubkey,
  'Hello, this is secret!'
);

// Create encrypted DM event
const dmEvent = finalizeEvent({
  kind: 4,
  created_at: Math.floor(Date.now() / 1000),
  tags: [['p', recipientPubkey]],
  content: ciphertext
}, secretKey);

// Decrypt message
const plaintext = await nip04.decrypt(
  secretKey,
  senderPubkey,
  ciphertext
);
```

### NIP-44 (Modern Encryption)

```javascript
import { nip44 } from 'nostr-tools';

// Get conversation key (cache this for multiple messages)
const conversationKey = nip44.getConversationKey(
  secretKey,
  recipientPubkey
);

// Encrypt
const ciphertext = nip44.encrypt(
  'Hello with NIP-44!',
  conversationKey
);

// Decrypt
const plaintext = nip44.decrypt(
  ciphertext,
  conversationKey
);
```

## NIP Implementations

### NIP-05 (DNS Identifier)

```javascript
import { nip05 } from 'nostr-tools';

// Query NIP-05 identifier
const profile = await nip05.queryProfile('alice@example.com');

if (profile) {
  console.log('Pubkey:', profile.pubkey);
  console.log('Relays:', profile.relays);
}

// Verify NIP-05 for a pubkey
const isValid = await nip05.queryProfile('alice@example.com')
  .then(p => p?.pubkey === expectedPubkey);
```

### NIP-10 (Reply Threading)

```javascript
import { nip10 } from 'nostr-tools';

// Parse reply tags
const parsed = nip10.parse(event);

console.log('Root:', parsed.root);     // Original event
console.log('Reply:', parsed.reply);   // Direct parent
console.log('Mentions:', parsed.mentions); // Other mentions
console.log('Profiles:', parsed.profiles); // Mentioned pubkeys
```

### NIP-21 (nostr: URIs)

```javascript
// Parse nostr: URIs
const uri = 'nostr:npub1...';
const { type, data } = nip19.decode(uri.replace('nostr:', ''));
```

### NIP-27 (Content References)

```javascript
// Parse nostr:npub and nostr:note references in content
const content = 'Check out nostr:npub1abc... and nostr:note1xyz...';

const references = content.match(/nostr:(n[a-z]+1[a-z0-9]+)/g);
references?.forEach(ref => {
  const decoded = nip19.decode(ref.replace('nostr:', ''));
  console.log(decoded.type, decoded.data);
});
```

### NIP-57 (Zaps)

```javascript
import { nip57 } from 'nostr-tools';

// Validate zap receipt
const zapReceipt = await pool.get(relays, {
  kinds: [9735],
  '#e': [eventId]
});

const validatedZap = await nip57.validateZapRequest(zapReceipt);
```

## Utilities

### Hex and Bytes Conversion

```javascript
import { bytesToHex, hexToBytes } from '@noble/hashes/utils';

// Convert secret key to hex
const secretKeyHex = bytesToHex(secretKey);

// Convert hex back to bytes
const secretKeyBytes = hexToBytes(secretKeyHex);
```

### Event ID Calculation

```javascript
import { getEventHash } from 'nostr-tools/pure';

// Calculate event ID without signing
const eventId = getEventHash(unsignedEvent);
```

### Signature Operations

```javascript
import {
  getSignature,
  verifyEvent
} from 'nostr-tools/pure';

// Sign event data
const signature = getSignature(unsignedEvent, secretKey);

// Verify complete event
const isValid = verifyEvent(signedEvent);
```

## Best Practices

### Connection Management

1. **Use SimplePool** - Manages connections efficiently
2. **Limit concurrent connections** - Don't connect to too many relays
3. **Handle disconnections** - Implement reconnection logic
4. **Close subscriptions** - Always close when done

### Event Handling

1. **Verify events** - Always verify signatures
2. **Deduplicate** - Events may come from multiple relays
3. **Handle replaceable events** - Latest by created_at wins
4. **Validate content** - Don't trust event content blindly

### Key Security

1. **Never expose secret keys** - Keep in secure storage
2. **Use NIP-07 in browsers** - Let extensions handle signing
3. **Validate input** - Check key formats before use

### Performance

1. **Cache events** - Avoid re-fetching
2. **Use filters wisely** - Be specific, use limits
3. **Batch operations** - Combine related queries
4. **Close idle connections** - Free up resources

## Common Patterns

### Building a Feed

```javascript
const pool = new SimplePool();
const relays = ['wss://relay.damus.io', 'wss://nos.lol'];

async function loadFeed(followedPubkeys) {
  const events = await pool.querySync(relays, {
    kinds: [1, 6],
    authors: followedPubkeys,
    limit: 100
  });

  // Sort by timestamp
  return events.sort((a, b) => b.created_at - a.created_at);
}
```

### Real-time Updates

```javascript
function subscribeToFeed(followedPubkeys, onEvent) {
  return pool.subscribeMany(
    relays,
    [{ kinds: [1, 6], authors: followedPubkeys }],
    {
      onevent: onEvent,
      oneose() {
        console.log('Caught up with stored events');
      }
    }
  );
}
```

### Profile Loading

```javascript
async function loadProfile(pubkey) {
  const [metadata] = await pool.querySync(relays, {
    kinds: [0],
    authors: [pubkey],
    limit: 1
  });

  if (metadata) {
    return JSON.parse(metadata.content);
  }
  return null;
}
```

### Event Deduplication

```javascript
const seenEvents = new Set();

function handleEvent(event) {
  if (seenEvents.has(event.id)) {
    return; // Skip duplicate
  }
  seenEvents.add(event.id);

  // Process event...
}
```

## Troubleshooting

### Common Issues

**Events not publishing:**
- Check relay is writable
- Verify event is properly signed
- Check relay's accepted kinds

**Subscription not receiving events:**
- Verify filter syntax
- Check relay has matching events
- Ensure subscription isn't closed

**Signature verification fails:**
- Check event structure is correct
- Verify keys are in correct format
- Ensure event hasn't been modified

**NIP-05 lookup fails:**
- Check CORS headers on server
- Verify .well-known path is correct
- Handle network timeouts

## References

- **nostr-tools GitHub**: https://github.com/nbd-wtf/nostr-tools
- **Nostr Protocol**: https://github.com/nostr-protocol/nostr
- **NIPs Repository**: https://github.com/nostr-protocol/nips
- **NIP-01 (Basic Protocol)**: https://github.com/nostr-protocol/nips/blob/master/01.md

## Related Skills

- **nostr** - Nostr protocol fundamentals
- **svelte** - Building Nostr UIs with Svelte
- **applesauce-core** - Higher-level Nostr client utilities
- **applesauce-signers** - Nostr signing abstractions
