---
name: frida-17
description: Frida 17 JavaScript API compatibility checker and fixer. Use when writing, reviewing, or fixing Frida scripts, especially when migrating from older Frida versions. Detects deprecated APIs removed in Frida 17 (May 2025) and provides correct replacements. Covers Module, Memory, Process APIs and common naming conflicts.
---

# Frida 17 Scripting Guide

This skill helps write and fix Frida scripts compatible with Frida 17.0.0 (released May 2025).

## Breaking Changes in Frida 17

### 1. Static Module Methods - REMOVED

```javascript
// OLD - No longer works in Frida 17
Module.findBaseAddress('libriver.so')
Module.getBaseAddress('libriver.so')
Module.findExportByName(null, 'open')
Module.findExportByName('libc.so', 'open')
Module.getExportByName(null, 'open')
Module.ensureInitialized('libc.so')
Module.enumerateExports('libc.so')
Module.enumerateSymbols('libc.so')

// NEW - Use Process and instance methods instead
var lib = Process.findModuleByName('libriver.so');  // returns Module or null
var lib = Process.getModuleByName('libriver.so');   // throws if not found
lib.base                                             // module base address
lib.findExportByName('open')                        // returns address or null
lib.getExportByName('open')                         // throws if not found
lib.enumerateExports()                              // returns array
lib.enumerateSymbols()                              // returns array
```

### 2. Static Memory Methods - REMOVED

```javascript
// OLD - No longer works
Memory.readU32(ptr)
Memory.writeU32(ptr, value)

// NEW - Use NativePointer instance methods
ptr.readU32()
ptr.writeU32(value)
```

### 3. Legacy Enumeration APIs - REMOVED

```javascript
// OLD - Callback style removed
Process.enumerateModules({ onMatch: fn, onComplete: fn })
Process.enumerateModulesSync()

// NEW - Returns array directly
Process.enumerateModules()
```

### 4. Reserved Function Names - DO NOT OVERRIDE

The following are built-in Frida functions. Defining custom functions with these names causes:
`TypeError: cannot define variable 'hexdump'`

**Reserved names:**
- `hexdump` - Use `dumpHex` instead for custom hex dump functions
- `ptr` - pointer constructor shorthand
- `NULL` - null pointer constant

```javascript
// BAD - conflicts with built-in
function hexdump(ptr, len) { ... }

// GOOD - use different name
function dumpHex(ptr, len) { ... }
```

## NativePointer Methods (Valid in Frida 17)

**Conversion:**
- `toInt32()` - cast to signed 32-bit integer
- `toNumber()` - convert to JavaScript number
- `toString([radix])` - convert to string

**NOT available:**
- `toUInt32()` - DOES NOT EXIST, use `toInt32()` for sizes < 2^31

**Memory reading:**
- `readU8()`, `readS8()`, `readU16()`, `readS16()`
- `readU32()`, `readS32()`, `readU64()`, `readS64()`
- `readByteArray(length)` - returns ArrayBuffer
- `readPointer()`, `readCString()`, `readUtf8String()`

**Memory writing:**
- `writeU8(value)`, `writeS8(value)`, etc.
- `writeByteArray(bytes)` - bytes must be ArrayBuffer or JS array
- `writePointer(ptr)`, `writeUtf8String(str)`

**Pointer arithmetic:**
- `add(rhs)`, `sub(rhs)`, `and(rhs)`, `or(rhs)`, `xor(rhs)`
- `shr(n)`, `shl(n)`, `not()`
- `isNull()`, `equals(rhs)`, `compare(rhs)`

## Java Bridge API (Unchanged in Frida 17)

```javascript
Java.perform(function() {
    var MyClass = Java.use('com.example.MyClass');

    // Hook with overload
    MyClass.myMethod.overload('int', 'java.lang.String').implementation = function(a, b) {
        console.log('Called with: ' + a + ', ' + b);
        // Call original
        return this.myMethod.overload('int', 'java.lang.String').call(this, a, b);
    };

    // Hook all overloads
    MyClass.myMethod.overloads.forEach(function(overload) {
        overload.implementation = function() {
            return overload.apply(this, arguments);
        };
    });
});
```

**Java byte[] handling:**
Java byte arrays cannot be passed directly to `Memory.alloc().writeByteArray()`.
Convert manually:

```javascript
// BAD - throws "expected a buffer-like object"
var hex = dumpHex(Memory.alloc(javaByteArray.length).writeByteArray(javaByteArray), len);

// GOOD - iterate and convert
var hex = "";
for (var i = 0; i < javaByteArray.length; i++) {
    hex += ("0" + (javaByteArray[i] & 0xff).toString(16)).slice(-2);
}
```

## Common Patterns for Frida 17

### Waiting for a library to load

```javascript
function waitForLibrary(libName, callback) {
    var lib = Process.findModuleByName(libName);
    if (lib) {
        callback(lib.base);
        return;
    }
    var pollInterval = setInterval(function() {
        var lib = Process.findModuleByName(libName);
        if (lib) {
            clearInterval(pollInterval);
            callback(lib.base);
        }
    }, 500);
}
```

### Hooking libc functions

```javascript
var libc = Process.findModuleByName('libc.so');
var open = libc ? libc.findExportByName('open') : null;
if (open) {
    Interceptor.attach(open, {
        onEnter: function(args) {
            console.log('open(' + args[0].readCString() + ')');
        }
    });
}
```

### Custom hex dump function

```javascript
function dumpHex(ptr, len) {
    if (!ptr || ptr.isNull()) return 'null';
    try {
        var bytes = ptr.readByteArray(len);
        if (!bytes) return 'null';
        var arr = new Uint8Array(bytes);
        var hex = '';
        for (var i = 0; i < arr.length; i++) {
            hex += ('0' + arr[i].toString(16)).slice(-2);
        }
        return hex;
    } catch (e) {
        return 'error: ' + e;
    }
}
```

## Checklist for Frida 17 Compatibility

When reviewing a Frida script, check for:

1. [ ] `Module.findBaseAddress()` -> `Process.findModuleByName().base`
2. [ ] `Module.getBaseAddress()` -> `Process.getModuleByName().base`
3. [ ] `Module.findExportByName(null, name)` -> `Process.findModuleByName('libc.so').findExportByName(name)`
4. [ ] `Module.findExportByName(lib, name)` -> `Process.findModuleByName(lib).findExportByName(name)`
5. [ ] `Module.enumerateExports(lib)` -> `Process.getModuleByName(lib).enumerateExports()`
6. [ ] `Module.enumerateSymbols(lib)` -> `Process.getModuleByName(lib).enumerateSymbols()`
7. [ ] `Memory.readU32(ptr)` -> `ptr.readU32()`
8. [ ] `toUInt32()` -> `toInt32()` (toUInt32 never existed)
9. [ ] `function hexdump()` -> `function dumpHex()` (name conflict)
10. [ ] Java byte[] with `writeByteArray()` -> manual hex conversion

## References

- [Frida 17.0.0 Release Notes](https://frida.re/news/2025/05/17/frida-17-0-0-released/)
- [Frida JavaScript API](https://frida.re/docs/javascript-api/)
- [Frida Android Examples](https://frida.re/docs/examples/android/)
