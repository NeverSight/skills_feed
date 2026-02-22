---
name: zig-memory
description: This skill provides Zig memory management guidance. It ensures proper use of defer/errdefer patterns, allocators, and leak detection. Essential for writing Zig code with dynamic allocation, fixing memory leaks, implementing resource cleanup, and working with allocators.
license: MIT
compatibility:
  - opencode
  - claude-code
metadata:
  version: "1.0.0"
  language: "zig"
  category: "memory-management"
  zig_version: "0.15.x"
---

# Zig Memory Management Guide

> **Core Principle**: Every allocation must have a corresponding deallocation.
> Use `defer` for normal cleanup, `errdefer` for error path cleanup.

This skill ensures safe memory management in Zig, preventing memory leaks and use-after-free bugs.

**Official Documentation**:
- Memory Allocators: https://ziglang.org/documentation/0.15.2/#Memory
- std.mem: https://ziglang.org/documentation/0.15.2/std/#std.mem

**Related Skills**:
- `zig-0.15`: API changes including ArrayList allocator parameter
- `solana-sdk-zig`: Solana-specific memory constraints (32KB heap)

## References

> Detailed allocator patterns and examples:

| Document | Path | Content |
|----------|------|---------|
| **Allocator Patterns** | `references/allocator-patterns.md` | GPA, Arena, FixedBuffer, Testing allocators, BPF allocator |

## Resource Cleanup Pattern (Critical)

### Always Use defer for Cleanup

```zig
// ❌ WRONG - No cleanup
fn process(allocator: Allocator) !void {
    const buffer = try allocator.alloc(u8, 1024);
    // ... use buffer ...
    // Memory leaked!
}

// ✅ CORRECT - Immediate defer
fn process(allocator: Allocator) !void {
    const buffer = try allocator.alloc(u8, 1024);
    defer allocator.free(buffer);  // Always freed
    // ... use buffer ...
}
```

### Use errdefer for Error Path Cleanup

```zig
// ❌ WRONG - Leak on error
fn createResource(allocator: Allocator) !*Resource {
    const res = try allocator.create(Resource);
    res.data = try allocator.alloc(u8, 100);  // If this fails, res leaks!
    try res.initialize();  // If this fails, both leak!
    return res;
}

// ✅ CORRECT - errdefer for each allocation
fn createResource(allocator: Allocator) !*Resource {
    const res = try allocator.create(Resource);
    errdefer allocator.destroy(res);  // Freed only on error

    res.data = try allocator.alloc(u8, 100);
    errdefer allocator.free(res.data);  // Freed only on error

    try res.initialize();  // If this fails, errdefers run
    return res;  // Success - errdefers don't run
}
```

## ArrayList Memory Management (Zig 0.15+)

**Critical**: In Zig 0.15, ArrayList methods require explicit allocator:

```zig
// ❌ WRONG (0.13/0.14 style)
var list = std.ArrayList(T).init(allocator);
defer list.deinit();
try list.append(item);

// ✅ CORRECT (0.15+ style)
var list = try std.ArrayList(T).initCapacity(allocator, 16);
defer list.deinit(allocator);  // Allocator required!
try list.append(allocator, item);  // Allocator required!
try list.appendSlice(allocator, items);
try list.ensureTotalCapacity(allocator, n);
const owned = try list.toOwnedSlice(allocator);
defer allocator.free(owned);  // Caller owns the slice
```

### ArrayList Method Reference (0.15+)

| Method | Allocator? | Notes |
|--------|------------|-------|
| `initCapacity(alloc, n)` | Yes | Preferred initialization |
| `deinit(alloc)` | Yes | **Changed in 0.15!** |
| `append(alloc, item)` | Yes | **Changed in 0.15!** |
| `appendSlice(alloc, items)` | Yes | **Changed in 0.15!** |
| `addOne(alloc)` | Yes | Returns pointer to new slot |
| `ensureTotalCapacity(alloc, n)` | Yes | Pre-allocate capacity |
| `toOwnedSlice(alloc)` | Yes | Caller must free result |
| `appendAssumeCapacity(item)` | No | Assumes capacity exists |
| `items` field | No | Read-only access |

## HashMap Memory Management

### Managed HashMap (Recommended)

```zig
// Managed - stores allocator internally
var map = std.StringHashMap(V).init(allocator);
defer map.deinit();  // No allocator needed
try map.put(key, value);  // No allocator needed
```

### Unmanaged HashMap

```zig
// Unmanaged - requires allocator for each operation
var umap = std.StringHashMapUnmanaged(V){};
defer umap.deinit(allocator);  // Allocator required
try umap.put(allocator, key, value);  // Allocator required
```

### Which to Use?

| Type | When to Use |
|------|-------------|
| Managed (`StringHashMap`) | General use, simpler API |
| Unmanaged (`StringHashMapUnmanaged`) | When allocator changes, performance-critical |

## Arena Allocator

Best for batch allocations freed together:

```zig
// Arena - single deallocation frees everything
var arena = std.heap.ArenaAllocator.init(backing_allocator);
defer arena.deinit();  // Frees ALL allocations

const temp = arena.allocator();
const str1 = try temp.alloc(u8, 100);  // No individual free needed
const str2 = try temp.alloc(u8, 200);  // No individual free needed
// arena.deinit() frees both
```

### Arena Use Cases

| Use Case | Why Arena |
|----------|-----------|
| Temporary computations | Free all at once |
| Request handling | Allocate per request, free at end |
| Parsing | Allocate AST nodes, free when done |
| Building strings | Accumulate, then transfer ownership |

## Testing Allocator (Leak Detection)

`std.testing.allocator` automatically detects memory leaks:

```zig
test "no memory leak" {
    const allocator = std.testing.allocator;

    // If you forget to free, test FAILS with:
    // "memory address 0x... was never freed"
    const buffer = try allocator.alloc(u8, 100);
    defer allocator.free(buffer);  // MUST have this

    // Test code...
}
```

### Common Test Memory Issues

```zig
// ❌ WRONG - Memory leak
test "leaky test" {
    const allocator = std.testing.allocator;
    const data = try allocator.alloc(u8, 100);
    // Forgot free → test fails: "memory leak detected"
}

// ✅ CORRECT - Proper cleanup
test "clean test" {
    const allocator = std.testing.allocator;
    const data = try allocator.alloc(u8, 100);
    defer allocator.free(data);
    // Test code...
}

// ❌ WRONG - ArrayList leak
test "leaky arraylist" {
    const allocator = std.testing.allocator;
    var list = try std.ArrayList(u8).initCapacity(allocator, 16);
    // Forgot deinit → memory leak
}

// ✅ CORRECT - ArrayList cleanup
test "clean arraylist" {
    const allocator = std.testing.allocator;
    var list = try std.ArrayList(u8).initCapacity(allocator, 16);
    defer list.deinit(allocator);
    // Test code...
}
```

## Segfault Prevention

### Null Pointer Dereference

```zig
// ❌ DANGEROUS - Segfault
var ptr: ?*u8 = null;
_ = ptr.?.*;  // Dereference null → crash

// ✅ SAFE - Check null
var ptr: ?*u8 = null;
if (ptr) |p| {
    _ = p.*;
}
```

### Array Bounds

```zig
// ❌ DANGEROUS - Out of bounds
const arr = [_]u8{ 1, 2, 3 };
_ = arr[5];  // Index 5 > len 3 → undefined behavior

// ✅ SAFE - Bounds check
const arr = [_]u8{ 1, 2, 3 };
if (5 < arr.len) {
    _ = arr[5];
}
```

### Use After Free

```zig
// ❌ DANGEROUS - Use after free
const data = try allocator.alloc(u8, 100);
allocator.free(data);
data[0] = 42;  // Use after free → undefined behavior

// ✅ SAFE - Set to undefined after free
const data = try allocator.alloc(u8, 100);
allocator.free(data);
// Don't use data after this point
```

## String Ownership

### Borrowed (Read-Only)

```zig
// Borrowed - caller keeps ownership
fn process(borrowed: []const u8) void {
    // Read-only, cannot modify, cannot free
    std.debug.print("{s}\n", .{borrowed});
}
```

### Owned (Caller Must Free)

```zig
// Owned - caller takes ownership and must free
fn createMessage(allocator: Allocator, name: []const u8) ![]u8 {
    return try std.fmt.allocPrint(allocator, "Hello, {s}!", .{name});
}

// Usage
const msg = try createMessage(allocator, "World");
defer allocator.free(msg);  // Caller frees
```

## Solana BPF Allocator

In Solana programs, use the BPF bump allocator:

```zig
const allocator = @import("solana_program_sdk").allocator.bpf_allocator;

// Limited to 32KB heap
const data = try allocator.alloc(u8, 1024);
// Note: BPF allocator does NOT support free()!
```

### BPF Memory Constraints

| Constraint | Value |
|------------|-------|
| Total heap | 32KB |
| Free support | ❌ None |
| Stack size | 64KB (with 4KB frame limit) |

### BPF Memory Tips

- Pre-calculate sizes when possible
- Use stack for small/fixed allocations
- Reuse buffers instead of reallocating
- Use `extern struct` for zero-copy parsing

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `memory leak detected` | Forgot to free | Add `defer allocator.free(...)` |
| `expected 2 arguments, found 1` | ArrayList missing allocator | Add allocator to `append`, `deinit` |
| `use of undefined value` | Use after free | Don't use data after freeing |
| `index out of bounds` | Array access past length | Check bounds before access |

## Pre-commit Checklist

- [ ] Every `alloc` has corresponding `defer free`
- [ ] Every `create` has corresponding `defer destroy`
- [ ] ArrayList uses `deinit(allocator)` (0.15+)
- [ ] `errdefer` used for error path cleanup
- [ ] Tests use `std.testing.allocator`
- [ ] No "memory leak detected" in test output
- [ ] No segfaults or crashes
- [ ] Solana programs respect 32KB limit

## Quick Reference

| Pattern | When to Use |
|---------|-------------|
| `defer allocator.free(x)` | Single allocation cleanup |
| `errdefer allocator.free(x)` | Cleanup only on error |
| `defer list.deinit(allocator)` | ArrayList cleanup (0.15+) |
| `defer map.deinit()` | Managed HashMap cleanup |
| `defer umap.deinit(allocator)` | Unmanaged HashMap cleanup |
| `Arena + defer arena.deinit()` | Many temporary allocations |
| `std.testing.allocator` | Test memory leak detection |
