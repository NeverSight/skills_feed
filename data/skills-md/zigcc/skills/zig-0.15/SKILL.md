---
name: zig-0.15
description: This skill provides Zig 0.15.x API guidance and should be used when writing or reviewing Zig code. It ensures correct usage of Zig 0.15 APIs, preventing common mistakes from using outdated 0.11/0.12/0.13/0.14 patterns. Essential for ArrayList, std.Io.Writer/Reader (Writergate), HTTP client, Ed25519, JSON, and type introspection APIs.
license: MIT
compatibility:
  - opencode
  - claude-code
metadata:
  version: "0.15.2"
  language: "zig"
  category: "programming-language"
---

# Zig 0.15.x Programming Guide

> **Version Scope**: This skill is pinned to **Zig 0.15.x** (specifically 0.15.2).
> For master/nightly builds, APIs may differ. Always check official docs for your version.

This skill ensures correct Zig 0.15.x API usage. Many LLMs have outdated Zig knowledge (0.11-0.14), causing compilation errors.

**Official Documentation (0.15.2)**:
- Language Reference: https://ziglang.org/documentation/0.15.2/
- Standard Library: https://ziglang.org/documentation/0.15.2/std/
- Release Notes: https://ziglang.org/download/0.15.1/release-notes.html
- Build System Guide: https://ziglang.org/learn/build-system/

**Community Resources (0.15.x)**:
- Zig Cookbook: https://cookbook.ziglang.cc/ (practical recipes, tracks 0.15.x)
- Zig Cookbook Source: https://github.com/zigcc/zig-cookbook

**Production Zig Codebases** (learn from real-world projects):
- Bun: https://github.com/oven-sh/bun (JS runtime, ~200k+ lines of Zig)
- Tigerbeetle: https://github.com/tigerbeetle/tigerbeetle (financial database)
- Mach Engine: https://github.com/hexops/mach (game engine)

**Learning Resources** (All 0.15.x Compatible):
- Zig Algorithms: https://github.com/TheAlgorithms/Zig (data structures & algorithms)
- zig-clap: https://github.com/Hejsil/zig-clap (CLI argument parser, 1.4k stars)
- zig-bench: https://github.com/Hejsil/zig-bench (benchmarking library, 68 stars)
- libvaxis: https://github.com/rockorager/libvaxis (TUI framework, 1.5k stars, v0.15.2)
- ZLS: https://github.com/zigtools/zls (Language Server, 4.5k stars, v0.15.0)
- zig-protobuf: https://github.com/Arwalk/zig-protobuf (Protocol Buffers, 365 stars)
- libxev: https://github.com/mitchellh/libxev (event loop, 2k+ stars)
- zig-aio: https://github.com/Cloudef/zig-aio (async I/O library)
- zig-toml: https://github.com/sam701/zig-toml (TOML parser)
- zig-xml: https://github.com/nektro/zig-xml (XML parser)
- log.zig: https://github.com/karlseguin/log.zig (structured logging)
- http.zig: https://github.com/karlseguin/http.zig (HTTP server, 1.3k stars)
- cache.zig: https://github.com/karlseguin/cache.zig (thread-safe LRU cache, 79 stars)
- pretty: https://github.com/timfayz/pretty (pretty printer for debugging, 98 stars)
- tls.zig: https://github.com/ianic/tls.zig (TLS 1.2/1.3, client & server)
- zig-network: https://github.com/ikskuh/zig-network (TCP/UDP networking)
- zmath: https://github.com/zig-gamedev/zmath (SIMD math library)

**Mitchell Hashimoto's Zig Libraries** (Ghostty author, high quality):
- libxev: https://github.com/mitchellh/libxev (cross-platform event loop)
- zig-graph: https://github.com/mitchellh/zig-graph (directed graph data structure)
- zig-libxml2: https://github.com/mitchellh/zig-libxml2 (libxml2 bindings)

**Compiler/Toolchain**:
- llvm-zig: https://github.com/kassane/llvm-zig (LLVM/Clang bindings, 53 stars)

**AI/ML**:
- ZML: https://github.com/zml/zml (high-performance AI inference, 3k stars)

**Blockchain/Ethereum**:
- Zeam: https://github.com/blockblaz/zeam (Ethereum client in Zig)
- ssz.zig: https://github.com/blockblaz/ssz.zig (SSZ serialization for Eth2, 30 stars, ⚠️ 0.14.x)

**Ecosystem Index**:
- awesome-zig: https://github.com/zigcc/awesome-zig (curated list, ⚠️ check version compatibility!)
- Zigistry: https://zigistry.dev/ (package registry with version info)

**For Other Versions**:
- Master (unstable): https://ziglang.org/documentation/master/
- Source Code: https://codeberg.org/ziglang/zig
- All Releases: https://ziglang.org/download/

## Critical API Changes in Zig 0.15

### ArrayList (BREAKING)

All mutating methods now require explicit `allocator` parameter:

```zig
// ❌ WRONG (0.13 and earlier)
var list = std.ArrayList(T).init(allocator);
try list.append(item);
try list.appendSlice(items);
_ = try list.addOne();
_ = try list.toOwnedSlice();

// ✅ CORRECT (0.15+)
var list = try std.ArrayList(T).initCapacity(allocator, 16);
defer list.deinit(allocator);
try list.append(allocator, item);
try list.appendSlice(allocator, items);
_ = try list.addOne(allocator);
_ = try list.toOwnedSlice(allocator);

// AssumeCapacity variants do NOT need allocator
list.appendAssumeCapacity(item);
```

| Method | 0.13 | 0.15+ |
|--------|------|-------|
| `append` | `try list.append(item)` | `try list.append(allocator, item)` |
| `appendSlice` | `try list.appendSlice(items)` | `try list.appendSlice(allocator, items)` |
| `addOne` | `try list.addOne()` | `try list.addOne(allocator)` |
| `ensureTotalCapacity` | `try list.ensureTotalCapacity(n)` | `try list.ensureTotalCapacity(allocator, n)` |
| `toOwnedSlice` | `try list.toOwnedSlice()` | `try list.toOwnedSlice(allocator)` |
| `deinit` | `list.deinit()` | `list.deinit(allocator)` |

### HashMap

**Managed** (stores allocator internally):
```zig
var map = std.StringHashMap(V).init(allocator);
defer map.deinit();
try map.put(key, value);  // No allocator needed
```

**Unmanaged** (requires allocator for each operation):
```zig
var map = std.StringHashMapUnmanaged(V){};
defer map.deinit(allocator);
try map.put(allocator, key, value);  // Allocator required
```

## Writergate: New std.Io.Writer and std.Io.Reader (MAJOR REWRITE)

Zig 0.15 introduces completely new I/O interfaces. All old `std.io` readers/writers are deprecated.

### Key Changes

1. **Non-generic**: New interfaces are concrete types, not `anytype`
2. **Buffer in interface**: User provides buffer, implementation decides minimum size
3. **Ring buffer based**: More efficient peek and streaming operations
4. **Precise error sets**: No more `anyerror` propagation

### New stdout Pattern

```zig
// ❌ WRONG (0.14 and earlier)
const stdout = std.io.getStdOut().writer();
try stdout.print("Hello\n", .{});

// ✅ CORRECT (0.15+)
var stdout_buffer: [1024]u8 = undefined;
var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
const stdout: *std.Io.Writer = &stdout_writer.interface;

try stdout.print("Hello\n", .{});
try stdout.flush();  // Don't forget to flush!
```

### Adapter for Migration

If you have old-style writers and need new interface:

```zig
fn useOldWriter(old_writer: anytype) !void {
    var adapter = old_writer.adaptToNewApi(&.{});
    const w: *std.Io.Writer = &adapter.new_interface;
    try w.print("{s}", .{"example"});
}
```

### New Reader API

```zig
// Reading lines with delimiter
while (reader.takeDelimiterExclusive('\n')) |line| {
    // process line
} else |err| switch (err) {
    error.EndOfStream => {},
    error.StreamTooLong => return err,
    error.ReadFailed => return err,
}
```

### HTTP Client (MAJOR REWRITE)

Zig 0.15.2 has both `fetch()` (high-level) and `request()` (low-level) APIs:

```zig
// ✅ CORRECT: High-level fetch() API (Zig 0.15.2)
var client: std.http.Client = .{ .allocator = allocator };
defer client.deinit();

const result = try client.fetch(.{
    .location = .{ .url = "https://example.com/api" },
    .method = .GET,
});
// result.status contains the HTTP status

// ✅ CORRECT: Low-level request/response API (Zig 0.15.2)
var client: std.http.Client = .{ .allocator = allocator };
defer client.deinit();

const uri = try std.Uri.parse("https://example.com/api");

// Create request with client.request() (NOT client.open!)
var req = try client.request(.POST, uri, .{
    .extra_headers = &.{
        .{ .name = "Content-Type", .value = "application/json" },
    },
});
defer req.deinit();

// Send body (use @constCast for const slices)
try req.sendBodyComplete(@constCast("{\"key\": \"value\"}"));

// Receive response
var redirect_buf: [4096]u8 = undefined;
var response = try req.receiveHead(&redirect_buf);

// Check status
const status = @intFromEnum(response.head.status);
if (status >= 200 and status < 300) {
    // Read response body using std.Io.Reader
    var body_reader = response.reader(&redirect_buf);
    const body = try body_reader.allocRemaining(allocator, std.Io.Limit.limited(1024 * 1024));
    defer allocator.free(body);
}
```

**Key API functions (verified in Zig 0.15.2)**:
- `client.request(method, uri, options)` → `Request`
- `client.fetch(options)` → `FetchResult`
- `req.sendBodyComplete(body)` - sends body and flushes
- `req.sendBodiless()` - for GET requests without body
- `req.receiveHead(buffer)` → `Response`
- `response.reader(buffer)` → `*std.Io.Reader`
- `reader.allocRemaining(allocator, limit)` → `[]u8`

### Base64 Encoding

```zig
// ❌ WRONG (0.13)
const encoder = std.base64.standard;
const encoded = encoder.encode(&buf, data);

// ✅ CORRECT (0.15+)
const encoder = std.base64.standard.Encoder;
const encoded = encoder.encode(&buf, data);
```

### Ed25519 Cryptography (MAJOR CHANGES)

Key types are now structs, not raw byte arrays:

```zig
const Ed25519 = std.crypto.sign.Ed25519;

// ❌ WRONG (0.13 - SecretKey was [32]u8)
const secret: [32]u8 = ...;
const kp = Ed25519.KeyPair.fromSecretKey(secret);

// ✅ CORRECT (0.15+ - SecretKey is struct with 64 bytes)
// From 32-byte seed (deterministic):
const seed: [32]u8 = ...;
const kp = try Ed25519.KeyPair.generateDeterministic(seed);

// From 64-byte secret key:
var secret_bytes: [64]u8 = ...;
const secret_key = try Ed25519.SecretKey.fromBytes(secret_bytes);
const kp = try Ed25519.KeyPair.fromSecretKey(secret_key);

// Get public key bytes:
const pubkey_bytes: [32]u8 = kp.public_key.toBytes();

// Get seed:
const seed: [32]u8 = kp.secret_key.seed();
```

Signature changes:
```zig
// ❌ WRONG (0.13 - fromBytes returned error union)
const sig = try Ed25519.Signature.fromBytes(bytes);

// ✅ CORRECT (0.15+ - fromBytes does NOT return error)
const sig = Ed25519.Signature.fromBytes(bytes);
```

### Type Introspection Enums (Case Change)

```zig
// ❌ WRONG (0.13 - PascalCase)
if (@typeInfo(T) == .Slice) { ... }
if (@typeInfo(T) == .Pointer) { ... }
if (@typeInfo(T) == .Struct) { ... }

// ✅ CORRECT (0.15+ - lowercase/escaped)
if (@typeInfo(T) == .slice) { ... }
if (@typeInfo(T) == .pointer) { ... }
if (@typeInfo(T) == .@"struct") { ... }
if (@typeInfo(T) == .@"enum") { ... }
if (@typeInfo(T) == .@"union") { ... }
if (@typeInfo(T) == .array) { ... }
if (@typeInfo(T) == .optional) { ... }
```

### Custom Format Functions

```zig
// ❌ WRONG (0.13 - used {} format specifier)
pub fn format(
    self: Self,
    comptime fmt: []const u8,
    options: std.fmt.FormatOptions,
    writer: anytype,
) !void {
    _ = fmt;
    _ = options;
    try writer.writeAll("...");
}
// Usage: std.fmt.bufPrint(&buf, "{}", .{value});

// ✅ CORRECT (0.15+ - use {f} format specifier)
pub fn format(self: Self, writer: anytype) !void {
    _ = self;
    try writer.writeAll("...");
}
// Usage: std.fmt.bufPrint(&buf, "{f}", .{value});
```

### JSON Parsing and Serialization

```zig
const MyStruct = struct {
    name: []const u8,
    value: u32,
};

// ✅ CORRECT: Parsing (0.15+)
const json_str =
    \\{"name": "test", "value": 42}
;
const parsed = try std.json.parseFromSlice(MyStruct, allocator, json_str, .{});
defer parsed.deinit();
const data = parsed.value;

// ✅ CORRECT: Serialization (0.15.2 - writer-based API)
// Note: There is NO stringifyAlloc in 0.15.2!

// Method 1: Using std.json.Stringify with Allocating writer
var out: std.Io.Writer.Allocating = .init(allocator);
defer out.deinit();
var stringify: std.json.Stringify = .{
    .writer = &out.writer,
    .options = .{},
};
try stringify.write(data);
const json_output = out.written();

// Method 2: Using std.fmt with json.fmt wrapper
const formatted = try std.fmt.allocPrint(allocator, "{f}", .{std.json.fmt(data, .{})});
defer allocator.free(formatted);

// Method 3: To fixed buffer
var buf: [1024]u8 = undefined;
var fbs = std.io.fixedBufferStream(&buf);
var writer = fbs.writer();
var stringify2: std.json.Stringify = .{
    .writer = &writer.adaptToNewApi(&.{}).new_interface,
    .options = .{},
};
try stringify2.write(data);
const output = fbs.getWritten();
```

### Memory/Formatting

```zig
// Allocating format
const formatted = try std.fmt.allocPrint(allocator, "value: {d}", .{42});
defer allocator.free(formatted);

// Non-allocating format
var buffer: [256]u8 = undefined;
const result = try std.fmt.bufPrint(&buffer, "value: {d}", .{42});
```

## Common Error Messages and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `expected 2 argument(s), found 1` | ArrayList method missing allocator | Add allocator as first argument |
| `no field or member function named 'encode'` | Using `std.base64.standard.encode` | Use `std.base64.standard.Encoder.encode` |
| `no field or member function named 'open'` | Using old HTTP API | Use `client.request()` or `client.fetch()` |
| `expected type 'SecretKey', found '[32]u8'` | Ed25519 SecretKey is now struct | Use `generateDeterministic(seed)` |
| `expected error union type, found 'Signature'` | Signature.fromBytes doesn't return error | Remove `try` |
| `enum has no member named 'Slice'` | @typeInfo enum case changed | Use lowercase `.slice` |
| `no field named 'root_source_file'` | Old build.zig API | Use `root_module = b.createModule(...)` |

## Verification Workflow

After writing Zig code:

1. Run `zig build` to check for compilation errors
2. If errors match patterns above, apply the 0.15 fix
3. Run `zig build test` to verify functionality
4. Use `zig build -Doptimize=ReleaseFast test` to catch UB

## Build System (build.zig) Changes (MAJOR REWRITE)

**Official Guide**: https://ziglang.org/learn/build-system/

### Executable Creation

```zig
// ❌ WRONG (0.14 and earlier)
const exe = b.addExecutable(.{
    .name = "hello",
    .root_source_file = .{ .path = "src/main.zig" },
    .target = target,
    .optimize = optimize,
});

// ✅ CORRECT (0.15+)
const exe = b.addExecutable(.{
    .name = "hello",
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    }),
});
```

### Library Creation

```zig
// ❌ WRONG (0.14 - addSharedLibrary/addStaticLibrary)
const lib = b.addSharedLibrary(.{
    .name = "mylib",
    .root_source_file = .{ .path = "src/lib.zig" },
});

// ✅ CORRECT (0.15+ - unified addLibrary with linkage)
const lib = b.addLibrary(.{
    .name = "mylib",
    .linkage = .dynamic,  // or .static
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/lib.zig"),
        .target = target,
        .optimize = optimize,
    }),
});
```

### Path Handling

```zig
// ❌ WRONG (0.14 - .path field)
.root_source_file = .{ .path = "src/main.zig" },

// ✅ CORRECT (0.15+ - use b.path())
.root_source_file = b.path("src/main.zig"),
```

### Module Dependencies

```zig
// ❌ WRONG (0.14)
exe.addModule("sdk", sdk_module);

// ✅ CORRECT (0.15+)
exe.root_module.addImport("sdk", sdk_module);
```

### Target Options

```zig
// ❌ WRONG (0.14)
const target = b.standardTargetOptions(.{});
// then use target directly

// ✅ CORRECT (0.15+)
const target = b.standardTargetOptions(.{});
const optimize = b.standardOptimizeOption(.{});

const exe = b.addExecutable(.{
    .name = "app",
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,      // pass to createModule
        .optimize = optimize,  // pass to createModule
    }),
});
```

### Testing

```zig
// ✅ CORRECT (0.15+)
const unit_tests = b.addTest(.{
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/main.zig"),
        .target = b.graph.host,  // use b.graph.host for native target
    }),
});

const run_unit_tests = b.addRunArtifact(unit_tests);
const test_step = b.step("test", "Run unit tests");
test_step.dependOn(&run_unit_tests.step);
```

### Complete build.zig Example

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "hello",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });

    b.installArtifact(exe);

    const run_exe = b.addRunArtifact(exe);
    const run_step = b.step("run", "Run the application");
    run_step.dependOn(&run_exe.step);
}
```

## std.mem Patterns

### Memory Operations

```zig
// Copy memory
@memcpy(dest, src);  // Same as std.mem.copyForwards

// Set memory
@memset(buffer, 0);  // Zero-fill

// Compare memory
const equal = std.mem.eql(u8, slice1, slice2);

// Find in slice
const index = std.mem.indexOf(u8, haystack, needle);
```

### Alignment

```zig
// Check alignment
const is_aligned = std.mem.isAligned(@intFromPtr(ptr), @alignOf(T));

// Align pointer
const aligned = std.mem.alignPointer(ptr, @alignOf(T));
```

## std.io Patterns

### Fixed Buffer Stream

```zig
var buf: [1024]u8 = undefined;
var fbs = std.io.fixedBufferStream(&buf);
const writer = fbs.writer();

try writer.writeAll("Hello");
try writer.print(" {d}", .{42});

const written = fbs.getWritten();  // "Hello 42"
```

### Counting Writer

```zig
var counting = std.io.countingWriter(underlying_writer);
try counting.writer().writeAll("test");
const bytes_written = counting.bytes_written;  // 4
```

## Testing Patterns

### Testing Allocator (Detects Leaks)

```zig
test "no memory leaks" {
    const allocator = std.testing.allocator;  // Auto-detects leaks
    
    const data = try allocator.alloc(u8, 100);
    defer allocator.free(data);  // MUST free or test fails
    
    // ... test code ...
}
```

### Assertions

```zig
test "assertions" {
    try std.testing.expect(condition);              // Boolean
    try std.testing.expectEqual(expected, actual);  // Equality
    try std.testing.expectEqualSlices(u8, expected, actual);  // Slices
    try std.testing.expectError(error.SomeError, result);     // Error
    try std.testing.expectEqualStrings("hello", str);         // Strings
}
```

## Comptime Patterns

### Type Reflection

```zig
fn serialize(comptime T: type, value: T) ![]u8 {
    const info = @typeInfo(T);
    
    switch (info) {
        .int => |i| {
            // Handle integer
            const byte_count = @divExact(i.bits, 8);
            // ...
        },
        .@"struct" => |s| {
            // Handle struct
            inline for (s.fields) |field| {
                // Process each field
                const field_value = @field(value, field.name);
                // ...
            }
        },
        else => @compileError("Unsupported type"),
    }
}
```

### Optional Type Handling

```zig
fn getInner(comptime T: type) type {
    const info = @typeInfo(T);
    if (info == .optional) {
        return info.optional.child;
    }
    return T;
}
```

## Pointer and Slice Patterns

### Slice to Many-Item Pointer

```zig
const slice: []u8 = buffer[0..10];
const ptr: [*]u8 = slice.ptr;
```

### Creating Slices

```zig
// From array
const arr = [_]u8{ 1, 2, 3, 4, 5 };
const slice = arr[1..4];  // [2, 3, 4]

// From pointer + length
const slice = ptr[0..len];
```

### Sentinel-Terminated Slices

```zig
// Null-terminated string
const str: [:0]const u8 = "hello";
const c_str: [*:0]const u8 = str.ptr;

// Get length without sentinel
const len = str.len;  // 5, not including null
```

## Language Changes

### usingnamespace Removed

The `usingnamespace` keyword has been completely removed in Zig 0.15.

```zig
// ❌ WRONG (removed in 0.15)
pub usingnamespace @import("other.zig");

// ✅ CORRECT - explicit re-exports
pub const foo = @import("other.zig").foo;
pub const bar = @import("other.zig").bar;

// ✅ CORRECT - namespace via field
pub const other = @import("other.zig");
// Usage: other.foo, other.bar
```

**Migration for mixins**: Use zero-bit fields with `@fieldParentPtr`:

```zig
// ❌ OLD mixin pattern
pub const Foo = struct {
    count: u32 = 0,
    pub usingnamespace CounterMixin(Foo);
};

// ✅ NEW mixin pattern (0.15+)
pub fn CounterMixin(comptime T: type) type {
    return struct {
        pub fn increment(m: *@This()) void {
            const x: *T = @alignCast(@fieldParentPtr("counter", m));
            x.count += 1;
        }
    };
}

pub const Foo = struct {
    count: u32 = 0,
    counter: CounterMixin(Foo) = .{},  // zero-bit field
};
// Usage: foo.counter.increment()
```

### async/await Keywords Removed

The `async`, `await`, and `@frameSize` have been removed. Async functionality will be provided via the standard library's new I/O interface.

```zig
// ❌ REMOVED - no async/await keywords
async fn fetchData() ![]u8 { ... }
const result = await fetchData();

// ✅ Use std.Io interfaces or threads instead
```

### Arithmetic on undefined

Operations on `undefined` that could trigger illegal behavior now cause compile errors:

```zig
const a: u32 = 0;
const b: u32 = undefined;

// ❌ COMPILE ERROR in 0.15+
_ = a + b;  // error: use of undefined value here causes illegal behavior
```

### Lossy Integer to Float Coercion

Compile error if integer cannot be precisely represented:

```zig
// ❌ COMPILE ERROR in 0.15+
const val: f32 = 123_456_789;  // error: cannot represent precisely

// ✅ CORRECT - opt-in to floating-point rounding
const val: f32 = 123_456_789.0;
```

## Extended References (This Skill)

> 详细的 API 参考和迁移指南请查阅以下文档：

| 文档 | 路径 | 内容 |
|------|------|------|
| **标准库 API 详解** | `references/stdlib-api-reference.md` | ArrayList、HashMap、HTTP Client、Ed25519、Base64、JSON、@typeInfo、std.fmt 等完整 API 参考 |
| **迁移模式指南** | `references/migration-patterns.md` | 从 0.13/0.14 迁移到 0.15 的详细对照，包括 Writergate、ArrayList、Build System 等 |
| **生产级代码库** | `references/production-codebases.md` | Sig（Solana）、ZML（AI）、Zeam（Ethereum）、Bun、Tigerbeetle 等项目学习指南，以及 0.15.x 兼容库列表 |
| **版本策略** | `VERSIONING.md` | 版本兼容性说明和更新策略 |

### 快速查阅建议

- **编写 HTTP 请求？** → 查看 `references/stdlib-api-reference.md` 的 `std.http.Client` 部分
- **ArrayList 报错？** → 查看 `references/migration-patterns.md` 的 `ArrayList Migration` 部分
- **学习最佳实践？** → 查看 `references/production-codebases.md` 中的 Sig 项目（Solana 验证器）
- **寻找第三方库？** → 查看 `references/production-codebases.md` 的 `Smaller Learning Projects` 表格

## References

**Official Documentation (0.15.2)**:
- Language Reference: https://ziglang.org/documentation/0.15.2/
- Standard Library Docs: https://ziglang.org/documentation/0.15.2/std/
- Release Notes (0.15.1): https://ziglang.org/download/0.15.1/release-notes.html
- Build System Guide: https://ziglang.org/learn/build-system/

**Community Resources (0.15.x)**:
- Zig Cookbook: https://cookbook.ziglang.cc/
- Zig Cookbook Source: https://github.com/zigcc/zig-cookbook

**Cookbook Recipe Categories** (all tested on 0.15.x):
- File System: read files, mmap, iterate directories
- Cryptography: SHA-256, PBKDF2, Argon2
- Network: TCP/UDP client/server
- Web: HTTP GET/POST, HTTP server
- Concurrency: threads, shared data, thread pools
- Encoding: JSON, ZON, base64
- Database: SQLite, PostgreSQL, MySQL

**Production Zig Codebases** (learn from real-world projects):
| Project | URL | Learn From |
|---------|-----|------------|
| **Sig** | https://github.com/Syndica/sig | **Solana validator in Zig** - most relevant for this SDK! |
| **Zeam** | https://github.com/blockblaz/zeam | **Ethereum client in Zig** - blockchain patterns |
| Bun | https://github.com/oven-sh/bun | JS runtime, async I/O, FFI, build system |
| Tigerbeetle | https://github.com/tigerbeetle/tigerbeetle | Financial DB, deterministic execution, testing |
| Mach | https://github.com/hexops/mach | Game engine, graphics, memory management |
| Ghostty | https://github.com/ghostty-org/ghostty | Terminal emulator, cross-platform, GPU rendering |
| Zig Algorithms | https://github.com/TheAlgorithms/Zig | Data structures, algorithms, idiomatic Zig |

**Key Sections in Release Notes**:
- Writergate (I/O rewrite): https://ziglang.org/download/0.15.1/release-notes.html#Writergate
- ArrayList changes: https://ziglang.org/download/0.15.1/release-notes.html#ArrayList-make-unmanaged-the-default
- usingnamespace removal: https://ziglang.org/download/0.15.1/release-notes.html#usingnamespace-Removed
- Format method changes: https://ziglang.org/download/0.15.1/release-notes.html#f-Required-to-Call-format-Methods

**Source Code & Development**:
- Official Repository: https://codeberg.org/ziglang/zig
- Master Documentation: https://ziglang.org/documentation/master/
- Master Std Library: https://ziglang.org/documentation/master/std/

## Version Compatibility Notes

This skill targets **Zig 0.15.x**. If you're using a different version:

| Version | Documentation | Notes |
|---------|--------------|-------|
| 0.15.x | This skill | Current stable, solana-zig uses 0.15.2 |
| 0.14.x | https://ziglang.org/documentation/0.14.1/ | Old build.zig API, old std.io |
| 0.13.x | https://ziglang.org/documentation/0.13.0/ | ArrayList without allocator param |
| master | https://ziglang.org/documentation/master/ | Unstable, APIs may change daily |

**How to check your Zig version**:
```bash
zig version
# or for this project:
./solana-zig/zig version
```

**When APIs differ from this skill**:
1. Check your actual Zig version
2. Consult version-specific documentation
3. Use compiler errors as guidance - Zig has excellent error messages
