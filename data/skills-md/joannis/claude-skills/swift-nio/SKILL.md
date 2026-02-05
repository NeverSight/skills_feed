---
name: swift-nio
description: 'Expert guidance on SwiftNIO best practices, patterns, and implementation. Use when developers mention: (1) SwiftNIO, NIO, ByteBuffer, Channel, ChannelPipeline, ChannelHandler, EventLoop, NIOAsyncChannel, or NIOFileSystem, (2) EventLoopFuture, ServerBootstrap, or DatagramBootstrap, (3) TCP/UDP server or client implementation, (4) ByteToMessageDecoder or wire protocol codecs, (5) binary protocol parsing or serialization, (6) blocking the event loop issues.'
---

# Swift NIO

## Overview

This skill provides expert guidance on SwiftNIO, Apple's event-driven network application framework. Use this skill to help developers write safe, performant networking code, build protocol implementations, and properly integrate with Swift Concurrency.

## Agent Behavior Contract (Follow These Rules)

1. Analyze the project's `Package.swift` to determine which SwiftNIO packages are used.
2. Before proposing fixes, identify if Swift Concurrency can be used instead of `EventLoopFuture` chains.
3. **Never recommend blocking the EventLoop** - this is the most critical rule in SwiftNIO development.
4. Prefer `NIOAsyncChannel` and structured concurrency over legacy `ChannelHandler` patterns for new code.
5. Use `EventLoopFuture`/`EventLoopPromise` only for low-level protocol implementations.
6. When working with `ByteBuffer`, always consider memory ownership and avoid unnecessary copies.

## Quick Decision Tree

When a developer needs SwiftNIO guidance, follow this decision tree:

1. **Building a TCP/UDP server or client?**
   - Read `references/Channels.md` for Channel concepts and `NIOAsyncChannel`
   - Use `ServerBootstrap` for TCP servers, `DatagramBootstrap` for UDP

2. **Understanding EventLoops?**
   - Read `references/EventLoops.md` for event loop concepts
   - Critical: Never block the EventLoop!

3. **Working with binary data?**
   - Read `references/ByteBuffer.md` for buffer operations
   - Prefer slice views over copies when possible

4. **Implementing a binary protocol?**
   - Read `references/ByteToMessageCodecs.md` for codec patterns
   - Use `ByteToMessageDecoder` and `MessageToByteEncoder`

5. **Migrating from EventLoopFuture to async/await?**
   - Use `.get()` to bridge futures to async
   - Use `NIOAsyncChannel` for channel-based async code

## Triage-First Playbook (Common Issues -> Solutions)

- **"Blocking the EventLoop"**
  - Offload CPU-intensive work to a dispatch queue or use `NIOThreadPool`
  - Never perform synchronous I/O on an EventLoop
  - See `references/EventLoops.md`

- **Type mismatch crash in ChannelPipeline**
  - Ensure `InboundOut` of handler N matches `InboundIn` of handler N+1
  - Ensure `OutboundOut` of handler N matches `OutboundIn` of handler N-1
  - See `references/Channels.md`

- **Implementing binary protocol serialization**
  - Use `ByteToMessageDecoder` for parsing bytes into messages
  - Use `MessageToByteEncoder` for serializing messages to bytes
  - Use `readLengthPrefixedSlice` and `writeLengthPrefixed` helpers
  - See `references/ByteToMessageCodecs.md`

- **Memory issues with ByteBuffer**
  - Use `readSlice` instead of `readBytes` when possible
  - Remember ByteBuffer uses copy-on-write semantics
  - See `references/ByteBuffer.md`

- **Deadlock when waiting for EventLoopFuture**
  - Never `.wait()` on a future from within the same EventLoop
  - Use `.get()` from async contexts or chain with `.flatMap`

## Core Patterns Reference

### Creating a TCP Server (Modern Approach)

```swift
let server = try await ServerBootstrap(group: MultiThreadedEventLoopGroup.singleton)
    .bind(host: "0.0.0.0", port: 8080) { channel in
        channel.eventLoop.makeCompletedFuture {
            try NIOAsyncChannel(
                wrappingChannelSynchronously: channel,
                configuration: .init(
                    inboundType: ByteBuffer.self,
                    outboundType: ByteBuffer.self
                )
            )
        }
    }

try await withThrowingDiscardingTaskGroup { group in
    try await server.executeThenClose { clients in
        for try await client in clients {
            group.addTask {
                try await handleClient(client)
            }
        }
    }
}
```

### EventLoopGroup Best Practice

```swift
// Preferred: Use the singleton
let group = MultiThreadedEventLoopGroup.singleton

// Get any EventLoop from the group
let eventLoop = group.any()
```

### Bridging EventLoopFuture to async/await

```swift
// From EventLoopFuture to async
let result = try await someFuture.get()

// From async to EventLoopFuture
let future = eventLoop.makeFutureWithTask {
    try await someAsyncOperation()
}
```

### ByteBuffer Operations

```swift
var buffer = ByteBufferAllocator().buffer(capacity: 1024)

// Writing
buffer.writeString("Hello")
buffer.writeInteger(UInt32(42))

// Reading
let string = buffer.readString(length: 5)
let number = buffer.readInteger(as: UInt32.self)
```

## Reference Files

Load these files as needed for specific topics:

- **`EventLoops.md`** - EventLoop concepts, nonblocking I/O, why blocking is bad
- **`Channels.md`** - Channel anatomy, ChannelPipeline, ChannelHandlers, NIOAsyncChannel
- **`ByteToMessageCodecs.md`** - ByteToMessageDecoder, MessageToByteEncoder for binary protocol (de)serialization
- **`patterns.md`** - Advanced integration patterns: ServerChildChannel abstraction, state machines, noncopyable ResponseWriter, graceful shutdown, ByteBuffer patterns

## Best Practices Summary

1. **Never block the EventLoop** - Offload heavy work to thread pools
2. **Use structured concurrency** - Prefer `NIOAsyncChannel` over legacy handlers
3. **Use the singleton EventLoopGroup** - `MultiThreadedEventLoopGroup.singleton`
4. **Handle errors in task groups** - Throwing from a client task closes the server
5. **Mind the types in pipelines** - Type mismatches crash at runtime
6. **Use ByteBuffer efficiently** - Prefer slices over copies

### Use ByteBuffer for Binary Protocol Handling

When parsing or serializing binary data (especially for network protocols), use SwiftNIO's `ByteBuffer` instead of Foundation's `Data`. ByteBuffer provides:
- Efficient read/write operations with built-in endianness handling
- Zero-copy slicing with reader/writer index tracking
- Integration with NIO ecosystem

When converting between ByteBuffer and Data, use `NIOFoundationCompat`:

```swift
import NIOFoundationCompat

// ByteBuffer to Data
let data = Data(buffer: byteBuffer)

// Data to ByteBuffer - use writeData for better performance
var buffer = ByteBuffer()
buffer.writeData(data)  // Faster than writeBytes(data)
```

**Bad - Using Data with manual byte manipulation:**
```swift
var buffer = Data()
var messageLength: UInt32?

for try await message in inbound {
    buffer.append(message)

    if messageLength == nil && buffer.count >= 4 {
        messageLength = UInt32(buffer[0]) << 24
            | UInt32(buffer[1]) << 16
            | UInt32(buffer[2]) << 8
            | UInt32(buffer[3])
        buffer = Data(buffer.dropFirst(4))  // Copies data!
    }
}
```

**Good - Using ByteBuffer:**

```swift
var buffer = ByteBuffer()

for try await message in inbound {
    buffer.writeBytes(message)

    if buffer.readableBytes >= 4 {
        let readerIndex = buffer.readerIndex
        guard let messageLength = buffer.readInteger(endianness: .big, as: UInt32.self) else {
            continue
        }

        if buffer.readableBytes >= messageLength {
            guard let bytes = buffer.readBytes(length: Int(messageLength)) else { continue }
            // Process bytes...
        } else {
            // Not enough data yet, reset reader index
            buffer.moveReaderIndex(to: readerIndex)
        }
    }
}
```

### Binary Data Types Comparison

There are several "bag of bytes" data structures in Swift:

| Type | Source | Platform | Notes |
|------|--------|----------|-------|
| `Array<UInt8>` | stdlib | All | Safe, growable, good for Embedded Swift |
| `InlineArray<N, UInt8>` | stdlib (6.1+) | All | Fixed-size, stack-allocated, no heap allocation |
| `Data` | Foundation | All (large binary) | Not always contiguous on Apple platforms |
| `ByteBuffer` | SwiftNIO | All (requires NIO) | Best for network protocols, not Embedded |
| `Span<UInt8>` | stdlib (6.2+) | All | Zero-copy view, requires Swift 6.2+ |
| `UnsafeBufferPointer<UInt8>` | stdlib | All | Unsafe, manual memory management |

**Recommendations:**
- For iOS/macOS-only projects: `Data` is fine due to framework integration
- For SwiftNIO-based projects: `ByteBuffer` is required for I/O operations
- For Embedded Swift: `[UInt8]` and `InlineArray`
- For cross-platform APIs: `Span<UInt8>` (Swift 6.2+) allows any backing type

### NIO Channel Pattern with executeThenClose

Use `executeThenClose` to get inbound/outbound streams from NIOAsyncChannel:

```swift
return try await channel.executeThenClose { inbound, outbound in
    let socket = Client(inbound: inbound, outbound: outbound, channel: channel.channel)
    return try await perform(client)
}
```

### Public API with Internal NIO Types

When exposing async sequences that wrap NIO types:
1. Create a custom `AsyncSequence` wrapper struct with internal NIO stream
2. The wrapper's `AsyncIterator` transforms NIO types to public types
3. This avoids exposing internal NIO imports in public API

### SwiftNIO UDP Notes

- Use `DatagramBootstrap` for UDP sockets
- Messages use `AddressedEnvelope<ByteBuffer>` containing remote address and data
- Multicast requires casting channel to `MulticastChannel` protocol
- Socket options use `SocketOptionValue` (Int32) type
- `so_reuseport` is only available on Linux