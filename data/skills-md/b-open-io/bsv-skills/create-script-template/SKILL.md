---
name: create-script-template
description: This skill should be used when the user asks to "create a script template", "add a new template to ts-templates", "create a BitCom template", "build an OP_RETURN template", or mentions creating templates for protocols like SIGMA, AIP, MAP, BAP, B. Guides creation of @bsv/sdk ScriptTemplate implementations.
---

# Create Script Template

Create script templates for the b-open-io/ts-templates repository following established patterns.

## When to Use

- Create a new BitCom protocol template (like AIP, MAP, SIGMA)
- Build an OP_RETURN data template
- Implement a ScriptTemplate for a new protocol
- Add a template to ts-templates repository

## Template Structure

Every template follows this pattern:

```typescript
import { ScriptTemplate, LockingScript, UnlockingScript, Script, Utils } from '@bsv/sdk'
import BitCom, { Protocol, BitComDecoded } from './BitCom.js'

export const PREFIX = 'PROTOCOL_ID'

export interface ProtocolData {
  bitcomIndex?: number
  // protocol-specific fields
  valid?: boolean
}

export default class Protocol implements ScriptTemplate {
  public readonly data: ProtocolData

  constructor(data: ProtocolData) {
    this.data = data
  }

  static decode(bitcom: BitComDecoded): Protocol[] { /* ... */ }
  static sign(/* params */): Promise<Protocol> { /* ... */ }
  lock(): LockingScript { /* ... */ }
  unlock(): { sign: Function, estimateLength: Function } { /* ... */ }
  verify(): boolean { /* ... */ }
}
```

## Creation Process

### Step 1: Understand the Protocol

Gather protocol specifications:
- Protocol prefix/identifier (Bitcoin address or literal string)
- Field order and data types
- Signing requirements (if any)
- Verification logic

### Step 2: Create Template File

Location: `src/template/bitcom/ProtocolName.ts`

Required exports:
- `PREFIX` constant
- `ProtocolData` interface
- Default class implementing `ScriptTemplate`

### Step 3: Implement Core Methods

**decode()** - Parse from BitComDecoded:
```typescript
static decode(bitcom: BitComDecoded): Protocol[] {
  const results: Protocol[] = []
  for (const protocol of bitcom.protocols) {
    if (protocol.protocol === PREFIX) {
      const script = Script.fromBinary(protocol.script)
      const chunks = script.chunks
      // Extract fields from chunks using Utils.toUTF8(chunk.data)
    }
  }
  return results
}
```

**lock()** - Generate locking script:
```typescript
lock(): LockingScript {
  const script = new Script()
  script.writeBin(Utils.toArray(field1, 'utf8'))
  script.writeBin(Utils.toArray(field2, 'utf8'))

  const protocols: Protocol[] = [{
    protocol: PREFIX,
    script: script.toBinary(),
    pos: 0
  }]

  return new BitCom(protocols).lock()
}
```

### Step 4: Add to mod.ts

Export the new template:
```typescript
export { default as Protocol, PREFIX } from './src/template/bitcom/Protocol.js'
export type { ProtocolData, ProtocolOptions } from './src/template/bitcom/Protocol.js'
```

### Step 5: Create Pull Request

1. Create feature branch: `git checkout -b feature/protocol-template`
2. Commit changes with descriptive message
3. Push and create PR to b-open-io/ts-templates

## Key Patterns

### Chunk-Based Parsing

Always use `script.chunks` directly, never string splitting:
```typescript
const script = Script.fromBinary(protocol.script)
const chunks = script.chunks

const field1 = Utils.toUTF8(chunks[0].data ?? [])
const field2 = Utils.toUTF8(chunks[1].data ?? [])
const signature = Array.from(chunks[2].data ?? [])
```

### Utils Over Buffer

Use @bsv/sdk Utils for all byte manipulation:
- `Utils.toArray(string, 'utf8')` - String to bytes
- `Utils.toUTF8(bytes)` - Bytes to string
- `Utils.toHex(bytes)` - Bytes to hex
- `Utils.toBase64(bytes)` - Bytes to base64

### Signature Verification

For protocols with signatures, use BSM recovery:
```typescript
for (let recovery = 0; recovery < 4; recovery++) {
  try {
    const publicKey = sig.RecoverPublicKey(
      recovery,
      new BigNumber(BSM.magicHash(message))
    )
    if (BSM.verify(message, sig, publicKey) &&
        publicKey.toAddress().toString() === address) {
      return true
    }
  } catch { /* try next */ }
}
```

## Additional Resources

### Reference Files

- **`references/template-anatomy.md`** - Detailed template structure
- **`references/pr-workflow.md`** - Contribution workflow for ts-templates

### Examples

- **`examples/OpReturn.ts`** - Minimal template (no external deps)

### More Examples

For complete production templates, see the ts-templates repository:
https://github.com/b-open-io/ts-templates/tree/master/src/template

Notable templates:
- `bitcom/Sigma.ts` - Transaction-bound signatures (uses sigma-protocol)
- `bitcom/AIP.ts` - Author Identity Protocol
- `bitcom/MAP.ts` - Magic Attribute Protocol
- `bitcom/BAP.ts` - Bitcoin Attestation Protocol
- `bitcom/B.ts` - B:// file storage
- `opreturn/OpReturn.ts` - Simple OP_RETURN
