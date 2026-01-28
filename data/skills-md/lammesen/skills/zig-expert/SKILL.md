---
name: zig-expert
description: Comprehensive Zig 0.15.2 development expert. Use when writing Zig code, debugging memory issues, designing build systems, implementing comptime metaprogramming, handling errors, or cross-compiling. Automatically activated for any .zig file or build.zig work.
allowed-tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash
---

# Zig Expert Skill

You are an expert Zig developer specializing in Zig 0.15.2. Apply these patterns, idioms, and best practices when assisting with Zig development.

## Core Language Principles

### Memory Management Philosophy
Zig has **no hidden memory allocations**. All allocations are explicit via allocators passed as parameters. This enables:
- Testability (inject test allocators for leak detection)
- Flexibility (swap allocators based on context)
- Clarity (visible allocation points)

### Error Handling Philosophy
Errors are **values, not exceptions**. Error unions (`!T`) combine a payload with an error set. Use:
- `try` to propagate errors to caller
- `catch` to handle errors locally
- `errdefer` for cleanup on error paths

### Comptime Philosophy
Compile-time execution replaces macros and generics. The same code runs at compile-time and runtime, enabling:
- Generic data structures via `comptime T: type`
- Code generation via `@typeInfo` introspection
- Compile-time validation and assertions

---

## Allocator Selection Guide

| Allocator | Use Case | Thread-Safe |
|-----------|----------|-------------|
| `std.heap.GeneralPurposeAllocator` | Development/debugging, leak detection | Configurable |
| `std.heap.ArenaAllocator` | Batch operations, bulk deallocation | No |
| `std.heap.FixedBufferAllocator` | Stack-backed, embedded, no heap | No |
| `std.heap.page_allocator` | Simple backing allocator | Yes |
| `std.heap.c_allocator` | Performance-critical (requires libc) | Yes |
| `std.testing.allocator` | Unit tests (auto leak detection) | No |

### Standard Allocator Patterns

**Application Entry Point:**
```zig
pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer {
        const status = gpa.deinit();
        if (status == .leak) @panic("Memory leak detected!");
    }
    const allocator = gpa.allocator();

    try run(allocator);
}
```

**Arena for Batch Operations:**
```zig
var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
defer arena.deinit(); // Frees ALL allocations at once
const allocator = arena.allocator();

// No individual frees needed
_ = try allocator.alloc(u8, 100);
_ = try allocator.alloc(u8, 200);
```

**Testing with Leak Detection:**
```zig
test "memory safety" {
    var list = std.ArrayList(i32).init(std.testing.allocator);
    defer list.deinit();
    try list.append(42);
    try std.testing.expectEqual(@as(i32, 42), list.pop());
}
```

---

## Error Handling Patterns

### Error Union Basics
```zig
// Define specific error sets (preferred over anyerror)
const FileError = error{
    AccessDenied,
    FileNotFound,
    OutOfMemory,
};

// Inferred error set (use sparingly)
fn process() !void {
    // Error set inferred from all possible errors
}
```

### try/catch/orelse Idioms
```zig
// try: Propagate error to caller
const file = try std.fs.cwd().openFile("data.txt", .{});

// catch: Handle error locally
const value = getValue() catch |err| switch (err) {
    error.OutOfMemory => return error.OutOfMemory,
    error.FileNotFound => return default_value,
    else => unreachable,
};

// catch with default
const result = mayFail() catch default;

// orelse: For optionals
const unwrapped = optional_value orelse default_value;
```

### errdefer for Resource Cleanup (Critical Pattern)
```zig
fn initResource(allocator: Allocator) !*Resource {
    const resource = try allocator.create(Resource);
    errdefer allocator.destroy(resource); // Runs ONLY if error returned

    resource.buffer = try allocator.alloc(u8, 1024);
    errdefer allocator.free(resource.buffer);

    try resource.initialize(); // If this fails, both errdefers run
    return resource;
}
```

### defer/errdefer Execution Order
```zig
fn example() !void {
    const a = try allocate();
    defer free(a);           // Runs: 3rd (last defer, first to run)
    errdefer cleanup(a);     // Runs: only on error, before defers

    const b = try allocate();
    defer free(b);           // Runs: 2nd

    const c = try allocate();
    defer free(c);           // Runs: 1st

    // Normal exit: free(c), free(b), free(a)
    // Error exit: cleanup(a), then error propagates
}
```

---

## Comptime and Generics Patterns

### Generic Data Structure Template
```zig
pub fn ArrayList(comptime T: type) type {
    return struct {
        items: []T,
        capacity: usize,
        allocator: std.mem.Allocator,

        const Self = @This();

        pub fn init(allocator: std.mem.Allocator) Self {
            return .{ .items = &.{}, .capacity = 0, .allocator = allocator };
        }

        pub fn deinit(self: *Self) void {
            if (self.capacity > 0) {
                self.allocator.free(self.items.ptr[0..self.capacity]);
            }
        }

        pub fn append(self: *Self, item: T) !void {
            if (self.items.len >= self.capacity) {
                try self.ensureCapacity(self.capacity * 2 + 1);
            }
            self.items.len += 1;
            self.items[self.items.len - 1] = item;
        }
    };
}
```

### Type Introspection Pattern
```zig
fn serialize(comptime T: type, value: T) ![]u8 {
    const info = @typeInfo(T);
    return switch (info) {
        .@"struct" => |s| {
            inline for (s.fields) |field| {
                const field_value = @field(value, field.name);
                // Process each field...
            }
        },
        .int => std.fmt.allocPrint(allocator, "{d}", .{value}),
        .float => std.fmt.allocPrint(allocator, "{d}", .{value}),
        else => @compileError("Unsupported type: " ++ @typeName(T)),
    };
}
```

### Compile-Time Validation
```zig
fn Vector(comptime size: usize) type {
    if (size == 0) @compileError("Vector size must be > 0");
    if (size > 1024) @compileError("Vector size too large");

    return struct {
        data: [size]f32,

        pub fn dot(self: @This(), other: @This()) f32 {
            var sum: f32 = 0;
            inline for (0..size) |i| {
                sum += self.data[i] * other.data[i];
            }
            return sum;
        }
    };
}
```

### anytype Duck Typing
```zig
fn print(writer: anytype, value: anytype) !void {
    const T = @TypeOf(value);
    if (@hasDecl(T, "format")) {
        try value.format(writer);
    } else {
        try writer.print("{any}", .{value});
    }
}
```

---

## Type System Patterns

### Tagged Union (Sum Type) Pattern
```zig
const JsonValue = union(enum) {
    null,
    bool: bool,
    number: f64,
    string: []const u8,
    array: []JsonValue,
    object: std.StringHashMap(JsonValue),

    pub fn isNull(self: JsonValue) bool {
        return self == .null;
    }
};

// Pattern matching with payload capture
fn processJson(value: JsonValue) void {
    switch (value) {
        .null => {},
        .bool => |b| std.debug.print("bool: {}\n", .{b}),
        .number => |n| std.debug.print("number: {d}\n", .{n}),
        .string => |s| std.debug.print("string: {s}\n", .{s}),
        .array => |arr| for (arr) |item| processJson(item),
        .object => |obj| {
            var it = obj.iterator();
            while (it.next()) |entry| {
                std.debug.print("{s}: ", .{entry.key_ptr.*});
                processJson(entry.value_ptr.*);
            }
        },
    }
}
```

### Packed Struct for Bit Fields
```zig
const Flags = packed struct(u8) {
    enabled: bool,      // bit 0
    priority: u3,       // bits 1-3
    mode: enum(u2) { normal, fast, slow, custom }, // bits 4-5
    reserved: u2 = 0,   // bits 6-7
};

// Bitcast to/from backing integer
const flags = Flags{ .enabled = true, .priority = 5, .mode = .fast };
const byte: u8 = @bitCast(flags);
const restored: Flags = @bitCast(byte);
```

### extern struct for C Interop
```zig
const CStruct = extern struct {
    x: c_int,
    y: c_long,
    data: [256]u8,
};

// Guaranteed C-compatible layout
comptime {
    std.debug.assert(@sizeOf(CStruct) == @sizeOf(c_int) + @sizeOf(c_long) + 256);
}
```

---

## Build System Patterns

### Standard Executable build.zig
```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });

    b.installArtifact(exe);

    // Run step
    const run_exe = b.addRunArtifact(exe);
    run_exe.step.dependOn(b.getInstallStep());
    if (b.args) |args| run_exe.addArgs(args);

    const run_step = b.step("run", "Run the application");
    run_step.dependOn(&run_exe.step);

    // Test step
    const unit_tests = b.addTest(.{
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });
    const run_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_tests.step);
}
```

### Library with C Integration
```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const lib = b.addStaticLibrary(.{
        .name = "mylib",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/lib.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });

    // Link system libraries
    lib.linkSystemLibrary("z");
    lib.linkLibC();

    // Add C source files
    lib.addCSourceFiles(.{
        .files = &.{ "src/c/helper.c" },
        .flags = &.{ "-std=c99", "-O2" },
    });

    lib.addIncludePath(b.path("include/"));
    b.installArtifact(lib);
}
```

### build.zig.zon Dependencies
```zig
.{
    .name = "my_project",
    .version = "0.1.0",
    .dependencies = .{
        .zap = .{
            .url = "https://github.com/zigzap/zap/archive/refs/tags/v0.1.7.tar.gz",
            .hash = "1220002d24d73672fe8b1e39717c0671598acc8ec27b8af2e1caf623a4fd0ce0d1bd",
        },
        .local_lib = .{
            .path = "../lib",
        },
    },
    .paths = .{ "build.zig", "build.zig.zon", "src" },
}
```

---

## Cross-Compilation

### Command Line
```bash
zig build -Dtarget=x86_64-linux-gnu -Doptimize=ReleaseFast
zig build -Dtarget=aarch64-macos
zig build -Dtarget=x86_64-windows-gnu
zig build -Dtarget=wasm32-freestanding
```

### Multi-Target Build
```zig
const targets = [_]std.Target.Query{
    .{}, // native
    .{ .cpu_arch = .x86_64, .os_tag = .linux },
    .{ .cpu_arch = .x86_64, .os_tag = .windows },
    .{ .cpu_arch = .aarch64, .os_tag = .macos },
    .{ .cpu_arch = .wasm32, .os_tag = .freestanding },
};

pub fn build(b: *std.Build) void {
    for (targets) |t| {
        const exe = b.addExecutable(.{
            .name = "myapp",
            .root_module = b.createModule(.{
                .root_source_file = b.path("src/main.zig"),
                .target = b.resolveTargetQuery(t),
                .optimize = .ReleaseFast,
            }),
        });
        b.installArtifact(exe);
    }
}
```

---

## Testing Patterns

### Test Structure
```zig
const std = @import("std");
const expect = std.testing.expect;
const expectEqual = std.testing.expectEqual;
const expectError = std.testing.expectError;

test "basic functionality" {
    var list = std.ArrayList(i32).init(std.testing.allocator);
    defer list.deinit();

    try list.append(42);
    try expectEqual(@as(i32, 42), list.pop());
}

test "error handling" {
    const result = mayFail();
    try expectError(error.SomeError, result);
}

test "floating point comparison" {
    const value = calculatePi();
    try expect(@abs(value - 3.14159) < 0.00001);
}
```

### Running Tests
```bash
zig build test --summary all
zig test src/main.zig
```

---

## Common Standard Library Modules

| Module | Purpose |
|--------|---------|
| `std.mem` | Memory utilities, slices, allocator interface |
| `std.heap` | Allocator implementations |
| `std.fs` | File system operations |
| `std.net` | Networking (TCP/UDP, DNS) |
| `std.json` | JSON parsing/serialization |
| `std.fmt` | String formatting |
| `std.io` | I/O readers and writers |
| `std.ArrayList` | Dynamic arrays |
| `std.HashMap` | Hash maps |
| `std.Thread` | Threading primitives |
| `std.testing` | Unit testing utilities |
| `std.debug` | Debug printing, assertions |
| `std.log` | Structured logging |
| `std.crypto` | Cryptographic primitives |
| `std.process` | Process management |

---

## Style Conventions

| Item | Convention | Example |
|------|------------|---------|
| Types | PascalCase | `HttpClient`, `ArrayList` |
| Functions | camelCase | `getValue`, `processData` |
| Constants | snake_case | `max_size`, `default_port` |
| Files | snake_case.zig | `http_client.zig` |
| Test names | Descriptive strings | `"handles empty input"` |

---

## Common Pitfalls to Avoid

1. **Forgetting defer for cleanup**: Always pair `alloc` with `defer free`
2. **Using anyerror**: Define specific error sets for better error handling
3. **Ignoring error unions**: `_ = mayFail();` is compile error; use `_ = mayFail() catch {};`
4. **Missing errdefer**: When function can fail after allocation, use `errdefer`
5. **Expecting comptime side effects**: Comptime code cannot have runtime effects
6. **Integer overflow in Release**: Use `+%` (wrapping) or `+|` (saturating) when intended
7. **Forgetting sentinel for C strings**: Use `[*:0]const u8` for null-terminated strings

---

## When This Skill Activates

This skill automatically activates when:
- Working with `.zig` files
- Creating or modifying `build.zig` or `build.zig.zon`
- Discussing Zig memory management, error handling, or comptime
- Cross-compiling Zig projects
- Integrating C code with Zig
- Writing or debugging Zig tests
