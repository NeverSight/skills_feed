---
name: zig
description: >
  Zig best practices for system programming with memory safety.
  Trigger: When writing Zig code with memory safety.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with zig"

## When to Use

Use this skill when:
- Writing Zig systems code
- Managing memory manually but safely
- Using comptime features
- Interfacing with C libraries

---

## Critical Patterns

### Error Handling (REQUIRED)

```zig
// ✅ ALWAYS: Use error unions
fn readFile(path: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();
    return try file.readToEndAlloc(allocator, max_size);
}

// Usage with catch
const content = readFile("config.txt") catch |err| {
    std.log.err("Failed: {}", .{err});
    return err;
};
```

### Memory Management (REQUIRED)

```zig
// ✅ ALWAYS: Use allocators explicitly
const allocator = std.heap.page_allocator;

var list = std.ArrayList(u8).init(allocator);
defer list.deinit();

try list.append(42);
```

### Comptime (REQUIRED)

```zig
// ✅ Use comptime for compile-time computation
fn Vec(comptime T: type, comptime N: usize) type {
    return struct {
        data: [N]T,
        
        pub fn init() @This() {
            return .{ .data = undefined };
        }
    };
}

const Vec3f = Vec(f32, 3);
```

---

## Decision Tree

```
Need error handling?       → Use error unions with try/catch
Need cleanup?              → Use defer
Need compile-time?         → Use comptime
Need optional value?       → Use ?T (optional type)
Need C interop?            → Use @cImport
```

---

## Commands

```bash
zig build                  # Build project
zig run src/main.zig       # Build and run
zig test src/main.zig      # Run tests
zig fmt src/               # Format code
```

---

## Resources

- **Best Practices**: [best-practices.md](best-practices.md)
- **Comptime**: [comptime.md](comptime.md)
- **Memory**: [memory.md](memory.md)
