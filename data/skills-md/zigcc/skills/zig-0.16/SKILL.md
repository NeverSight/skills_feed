---
name: zig-0.16
description: Notes for porting code to Zig 0.16-dev (std.Io era). Use this when fixing 0.15-era code that fails on 0.16 master/dev.
license: MIT
compatibility:
  - opencode
  - claude-code
metadata:
  version: "0.16-dev"
  language: "zig"
  category: "programming-language"
---

# Zig 0.16-dev Porting Notes

This skill captures gotchas hit when porting a 0.15 project to **Zig 0.16-dev** (std.Io world). APIs keep moving; always check the stdlib sources for your exact build.

## Std.Io replaces std.net / legacy std.posix wrappers
- `std.net` is gone. The new networking lives under **`std.Io.net`** (types: `IpAddress`, `Stream`, `Server`, `UnixAddress`, etc.).
- High-level functions like `tcpConnectToHost`, `Address.parseIp`, `Stream.connect`, `Stream.read/writeAll` no longer exist. You must use `Io` vtables (`io.vtable.netConnectIp`, `netRead`, `netWrite`, `netListenIp`, `netAccept`).
- If you need raw fds, call platform syscalls (`std.os.linux.socket`, `accept4`, `connect`, `bind`, `listen`, `write`, `writev`, `read`, `close`). Many helpers that were under `std.posix` are gone.
- `posix.socket`, `posix.bind`, `posix.accept`, `posix.shutdown`, `posix.writev`, `posix.listen`, `posix.pipe2`, `posix.getrandom`, `std.net.has_unix_sockets`, etc. are removed. Use `std.os.<platform>` syscalls and `posix.system.*` where available, or the Io vtable.
- Epoll: use `std.os.linux.epoll_create1/epoll_ctl/epoll_wait` directly; signatures include an explicit `count` param for writev/epoll_wait.

## Std.Io Readers/Writers
- New writer/reader interfaces live under `std.Io`. TLS expects `*std.Io.Reader` / `*std.Io.Writer` (struct fields `.interface`). Pass pointers to interfaces, not call `interface()` as a function.
- `std.time.sleep` removed; use `std.Io.sleep(io, Duration, Clock)`.

## Time / Random / Env / Exit
- `std.time.milliTimestamp` removed. Use `std.time.Timer` or `std.Io.Clock.now(clock, io)` and compare `Timestamp.nanoseconds`.
- Random secure bytes: `std.Io.randomSecure(io, buf)`; no `std.crypto.random` or `std.posix.getrandom` convenience.
- `std.process.getEnvVarOwned` is gone; use `std.c.getenv` and copy.
- `std.posix.exit` removed; use `std.process.exit`.

## TLS Client options
- `std.crypto.tls.Client.Options` now requires `entropy: *const [entropy_len]u8` and `realtime_now_seconds: i64`. Fill entropy with `std.Io.randomSecure`; compute seconds with `Io.Clock.now(.real, io)` / `ns_per_s`.

## MemoryPool API changes
- `std.heap.MemoryPool(T).initCapacity(allocator, n)` returns the pool; `create`/`destroy` now require allocator. No bare `init()` or zero-arg `deinit()`.

## Atomic order & Thread
- Atomic orders use `.monotonic` / `.seq_cst`; `.awake` removed.

## Format options
- `std.fmt.Options` replaces `FormatOptions`.
- `std.fmt.format` helper is gone; call `writer.print` directly (writers live in `std.Io.Writer`).

## Randomness / crypto changes
- `std.crypto.random` was removed. Use an `std.Io` instance: `const io = std.Io.Threaded.global_single_threaded.ioBasic(); io.random(&buf);`.
- `Ed25519.KeyPair.generate` now requires an `io: std.Io` argument: `Ed25519.KeyPair.generate(io);`.

## Enum conversion
- `std.meta.intToEnum` removed. Use `std.enums.fromInt(EnumType, value)` (returns `?EnumType`).

## Fixed-buffer writers in tests
- `std.io.fixedBufferStream` was removed. For in-memory writes use `var w = std.Io.Writer.fixed(buf);` and read bytes with `std.Io.Writer.buffered(&w)`.
- `std.ArrayList` no longer has `.init(allocator)` shorthand; use `.initBuffer(slice)` for stack buffers or managed variants.

## Stream/Conn helpers we added (compat pattern)
- Build a thin compat layer that wraps platform syscalls to reintroduce `Stream { read, writeAll, close, readAtLeast }` and address parsing/formatting, plus `tcpConnectToHost/Address` using raw sockets.
- For Unix sockets: build sockaddr manually and call `connect`.

## Testing adjustments
- For in-process client/server tests, use `socketpair(AF.UNIX, SOCK.STREAM|CLOEXEC, 0, &fds)` to avoid relying on Io vtable network (Threaded nets return `NetworkDown` if not wired).

## Error sets tightened
- Many functions return narrower error sets (e.g., Reader.fill no longer includes `WouldBlock`/`Timeout`). Remove unreachable branches accordingly.

## syscalls return types
- `std.os.linux.*` return `usize`; cast with `@as(isize, @bitCast(rc))` before checking `< 0`. For `writev/epoll_wait` include the `count` argument.

Use this skill when upgrading 0.15-era code to 0.16-dev to avoid common build-breakers.
