---
name: navi
description: Navi programming language expert. Use when writing Navi code, implementing features, handling errors, or working with Navi's type system, concurrency, and modules. Navi is a high-performance, statically-typed compiled language with modern optional types, no NULL pointer exceptions, and built-in concurrency support.
---

# Navi Language Skill

Navi (/ˈnævi/) is a high-performance, statically-typed compiled language designed for complex computing tasks. It offers script-like execution with compiled performance comparable to Go, Rust, and C.

## Core Characteristics

- **Statically typed** with type inference
- **No NULL pointer exceptions** - once compiled, code runs reliably
- **Modern optional types** (similar to Rust's Option)
- **Comprehensive error handling** with `throws`, `try`, `try?`, `try!`
- **Built-in concurrency** with `spawn` and channels (single-threaded concurrency)
- **Cross-platform**: Linux, Windows, macOS, WebAssembly

## Quick Reference

### Basic Syntax

```nv
// Entry point (main must have throws)
fn main() throws {
    let name = "World";
    let message = `Hello ${name}.`;  // String interpolation
    println(message);  // Auto-imported from std.io
}

// Functions
fn add(a: int, b: int): int {
    return a + b;
}

// Structs
struct User {
    name: string,
    email: string?,  // Optional field
    active: bool = true,  // Default value
}

impl User {
    fn new(name: string): User {
        return User { name, email: nil };
    }
}
```

### Key Syntax Rules

- Statements end with `;`
- Use 4 spaces for indentation
- `//` for single-line comments, `///` for doc comments
- String interpolation uses backticks: `` `value: ${x}` ``
- File extension: `.nv`

### Important Syntax Limitations

**If and Switch are STATEMENTS, not expressions:**
```nv
// ❌ WRONG - Cannot assign if/switch directly
let status = if (active) { "on" } else { "off" };
let day = switch (n) { case 1: "Mon"; default: "Other"; };

// ✅ CORRECT - Use statements, then assign
let status = "";
if (active) {
    status = "on";
} else {
    status = "off";
}
```

**Scientific notation requires explicit sign:**
```nv
// ❌ WRONG
let num = 1.5e10;

// ✅ CORRECT
let num = 1.5e+10;  // or 1.5e-10 for negative exponent
```

**Map access with `[]` vs `.get()`:**
```nv
let scores = {"Alice": 95, "Bob": 87};

// ❌ WRONG - scores["key"] returns non-optional, can't use ||
let score = scores["Eve"] || 0;

// ✅ CORRECT - Use .get() which returns optional type
let score = scores.get("Eve") || 0;

// ✅ Also correct - Direct access (but key must exist)
let alice_score = scores["Alice"];  // OK if key exists

// ✅ Also correct - Check before access
if (scores.get("Eve") != nil) {
    let score = scores["Eve"];
}
```

### Type System Essentials

```nv
// Primitives (all 64-bit)
let n: int = 100;
let f: float = 3.14;
let b: bool = true;
let s: string = "text";  // Immutable UTF-8
let c: char = '🎉';

// Optional types (key to NULL safety)
let value: string? = nil;
let result = value || "default";  // Unwrap or default
let length = value?.len();  // Safe chaining (returns nil if value is nil)
println(value!);  // Unwrap (panics if nil - use sparingly)

// Collections
let array = [1, 2, 3];
let map = {"key": "value"};
let empty: [int] = [];
```

### Error Handling Pattern

```nv
// Declare function can throw
fn divide(a: int, b: int): int throws {
    if (b == 0) {
        throw "Division by zero";
    }
    return a / b;
}

// Handle errors
let result = try? divide(10, 0);  // Returns int? (nil on error)
let result = try divide(10, 2);   // Propagate error up
let result = try! divide(10, 2);  // Panic on error

// Do-catch block
do {
    let r = try divide(10, 0);
} catch (e) {
    println(e.error());
}
```

### Control Flow Patterns

```nv
// If-let for optionals
if (let value = optional) {
    println(value);  // value is unwrapped here
}

// Let-else for early returns
let value = optional else {
    return;
};
// value is unwrapped here

// Switch with type matching
switch (let v = value.(type)) {
    case int:
        println("integer");
    case string:
        println("string");
    default:
        println("other");
}

// For loops
for (let i in 0..10) {  // Range
    println(`${i}`);
}

for (let item in array) {  // Array
    println(item);
}

for (let k, v in map) {  // Map
    println(`${k}: ${v}`);
}
```

### Concurrency Basics

```nv
use std.time;

fn main() throws {
    let ch = channel::<int>();

    // Spawn concurrent task (not parallel - single thread)
    spawn {
        time.sleep(0.1.seconds());
        try! ch.send(42);
    }

    let result = try ch.recv();
    println(`${result}`);
}
```

### Worker Pattern

```nv
use std.worker.Worker;

fn main() throws {
    // Create worker with closure
    let worker = try Worker.create(|worker| {
        let msg = try worker.recv::<string>()!;
        try worker.send(msg.to_uppercase());
    });

    try worker.send("hello");
    let response = try worker.recv::<string>();
    println(response);  // "HELLO"
}
```

### Navi Stream Integration

```nv
use nvs.macd;  // Import .nvs file as module

fn main() throws {
    // Create instance of NVS indicator
    let indicator = macd.new();

    // Execute with market data
    indicator.execute(
        time: 1234567890,
        open: 100.0,
        high: 105.0,
        low: 99.0,
        close: 103.0,
        volume: 1000.0,
        turnover: 100000.0
    );

    // Access exported variables
    println(`hist=${indicator.hist:?}`);
    println(`signal=${indicator.signal:?}`);
    println(`macd=${indicator.macd:?}`);
}
```

### Variadic Arguments

```nv
// Accept arbitrary number of arguments
fn sum(values: ..int): int {
    let total = 0;
    for (let n in values) {
        total += n;
    }
    return total;
}

sum(1, 2, 3);           // Call with multiple args
let nums = [2, 3, 4];
sum(..nums);            // Spread array
sum(1, ..nums, 5);      // Mix regular and spread

// With other parameters
fn format(prefix: string, parts: ..string): string {
    return prefix + parts.join(",");
}
```

## Common Patterns

### Safe Optional Handling

```nv
// Pattern 1: Unwrap or default
let name = user?.name || "Unknown";

// Pattern 2: If-let
if (let user = optional_user) {
    process(user);
}

// Pattern 3: Let-else (early return)
let user = optional_user else {
    return;
};
process(user);

// Pattern 4: Method chaining
let email = user?.profile?.email || "none";
```

### Resource Management

```nv
fn process_file(path: string) throws {
    let file = try open_file(path);

    defer {
        file.close();  // Always runs when function exits
    }

    try file.read();
    // defer executes here (LIFO if multiple defer blocks)
}
```

### Builder Pattern

```nv
impl Config {
    fn new(): Config {
        return Config { /* defaults */ };
    }

    fn with_port(self, port: int): Config {
        self.port = port;
        return self;
    }
}

let config = Config.new().with_port(8080);
```

## CLI Commands

```shell
navi run              # Run main.nv
navi run file.nv      # Run specific file
navi test             # Run all tests
navi test file.nv     # Run tests in file
navi test --doc       # Run doc tests
navi build            # Build project
navi compile          # Show bytecode
```

## Testing

````nv
test "addition" {
    let result = add(2, 3);
    assert result == 5;
    assert_eq result, 5;
    assert_ne result, 0;
}

/// Doc test example
/// ```nv
/// assert_eq add(1, 2), 3;
/// ```
fn add(a: int, b: int): int {
    return a + b;
}
````

## Best Practices

### Naming Conventions

- `snake_case`: variables, functions, fields (`user_name`, `get_user`)
- `CamelCase`: types, structs, enums (`User`, `HttpRequest`)
- `SCREAMING_SNAKE_CASE`: constants (`MAX_SIZE`)

### When to Use Each Error Handler

- `try` - When error should propagate up (most common)
- `try?` - When failure is acceptable, convert to optional
- `try!` - When failure is unexpected (use sparingly)
- `do-catch` - When you need custom error handling logic

### Optional Type Guidelines

- Use `||` for simple defaults
- Use `?.` for safe chaining
- Prefer `if let` for conditional logic
- Use `let else` for early returns

### Concurrency Notes

- `spawn` is **concurrent, not parallel** (single-threaded)
- Tasks interleave but don't run simultaneously
- Use channels for communication between tasks
- Blocking operations block entire runtime

## When to Load References

Load reference files when you need detailed information:

- **syntax.md** - Full syntax reference with all language constructs
- **types.md** - Complete type system including interfaces, unions, type aliases
- **error-handling.md** - Comprehensive error handling patterns and custom errors
- **concurrency.md** - Advanced concurrency patterns, channels, and spawn details
- **modules.md** - Module system, imports, visibility rules
- **testing.md** - Testing framework, annotations, doc tests
- **patterns.md** - Common idiomatic patterns and anti-patterns

Use `Read` tool to load these files from `~/.claude/skills/navi/references/` when needed.

## Resources

- **Official Site**: https://navi-lang.org
- **Standard Library**: https://navi-lang.org/stdlib/
- **GitHub**: https://github.com/navi-language/navi
- **Installation**: `curl -sSL https://navi-lang.org/install | sh`
