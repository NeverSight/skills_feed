---
name: nushell-usage
description: Essential patterns, idioms, and gotchas for writing Nushell code. Use when writing Nushell scripts, functions, or working with Nushell's type system, pipelines, and data structures. Complements plugin development knowledge with practical usage patterns.
version_target: "0.100+"
---

# Nushell Usage Patterns

## Critical Distinctions

### Pipeline Input vs Parameters

**CRITICAL**: Pipeline input (`$in`) is NOT interchangeable with function parameters!

```nu
# ❌ WRONG - treats $in as first parameter
def my-func [list: list, value: any] {
    $list | append $value
}

# ✅ CORRECT - declares pipeline signature
def my-func [value: any]: list -> list {
    $in | append $value
}

# Usage
[1 2 3] | my-func 4  # Works correctly
my-func [1 2 3] 4    # ERROR! my-func doesn't take positional params
```

**This applies to closures too.**

**Why this matters**:
- Pipeline input can be **lazily evaluated** (streaming)
- Parameters are **eagerly evaluated** (loaded into memory)
- Different calling conventions entirely

### Type Signatures

```nu
# No pipeline input
def func [x: int] { ... }                    # (x) -> output

# Pipeline input only
def func []: string -> int { ... }           # string | func -> int

# Both pipeline and parameters
def func [x: int]: string -> int { ... }     # string | func x -> int

# Generic pipeline
def func []: any -> any { ... }              # works with any input type
```

## Common Patterns

### Working with Lists

```nu
# Filter with index
$list | enumerate | where {|e| $e.index > 5 and $e.item.some-bool-field}

# Transform with previous state
$list | reduce --fold 0 {|item, acc| $acc + $item.value}
```

### Working with Records

```nu
# Create record
{name: "Alice", age: 30}

# Merge records (right-biased)
$rec1 | merge $rec2

# Merge many records (right-biased)
[$rec1 $rec2 $rec3 $rec4] | into record

# Update field
$rec | update name {|r| $"Dr. ($r.name)"}

# Insert field
$rec | insert active true

# Insert field based on existing fields
{x:1, y: 2} | insert z {|r| $r.x + $r.y}

# Upsert (update or insert)
$rec | upsert count {|r| ($r.count? | default 0) + 1}

# Reject fields
$rec | reject password secret_key

# Select fields
$rec | select name age email
```

### Working with Tables

```nu
# Tables are lists of records
let table = [
    {name: "Alice", age: 30}
    {name: "Bob", age: 25}
]

# Filter rows
$table | where age > 25

# Add column
$table | insert retired {|row| $row.age > 65}

# Rename column
$table | rename -c {age: years}

# Group by
$table | group-by status --to-table

# Transpose (rows ↔ columns)
$table | transpose name data
```

### Conditional Execution

```nu
# If expressions return values
let result = if $condition {
    "yes"
} else {
    "no"
}

# Match expressions
let result = match $value {
    0 => "zero"
    1..10 => "small"
    _ => "large"
}
```

### Null Safety

```nu
# Optional fields with ?
$record.field?                    # Returns null if missing
$record.field? | default "N/A"    # Provide fallback

# Check existence
if ($record.field? != null) { ... }
```

### Error Handling

```nu
# Try-catch
try {
    dangerous-operation
} catch {|err|
    print $"Error: ($err.msg)"
}

# Returning errors
def my-func [] {
    if $condition {
        error make {msg: "Something went wrong"}
    } else {
        "success"
    }
}

# Check command success
let result = try { fallible-command }
if ($result == null) {
    # Handle error
}

# Use complete for detailed error info for EXTERNAL commands (bins)
let result = (fallible-external-command | complete)
if $result.exit_code != 0 {
    print $"Error: ($result.stderr)"
}
```

### Closures and Scoping

```nu
# Closures capture environment
let multiplier = 10
let double_and_add = {|x| ($x * 2) + $multiplier}
5 | do $double_and_add  # Returns 20

# Outer mutable variables CANNOT be captured in closures
mut sum = 0
[1 2 3] | each {|x| $sum = $sum + $x}  # ❌ WON'T COMPILE

# Use reduce instead
let sum = [1 2 3] | reduce {|x, acc| $acc + $x}
```

### Iteration Patterns

```nu
# each: transform each element
$list | each {|item| $item * 2}

# each --flatten: stream outputs instead of collecting
# Turns list<list<T>> into list<T> by streaming items as they arrive
ls *.txt | each --flatten {|f| open $f.name | lines } | find "TODO"

# each --keep-empty: preserve null results
[1 2 3] | each --keep-empty {|e| if $e == 2 { "found" }}
# Result: ["" "found" ""]  (vs. without flag: ["found"])

# filter/where: select elements
# Row condition (field access auto-uses $it)
$table | where size > 100        # Implicit: $it.size > 100
$table | where type == "file"    # Implicit: $it.type == "file"

# Closure (must use $in or parameter)
$list | where {|x| $x > 10}
$list | where {$in > 10}         # Same as above

# reduce/fold: accumulate
$list | reduce --fold 0 {|item, acc| $acc + $item}

# Reduce without fold (first element is initial accumulator)
[1 2 3 4] | reduce {|it, acc| $acc - $it}  # ((1-2)-3)-4 = -8

# par-each: parallel processing
$large_list | par-each {|item| expensive-operation $item}

# for loop (imperative style)
for item in $list {
    print $item
}
```

### String Manipulation

```nu
# Interpolation
$"Hello ($name)!"
$"Sum: (1 + 2)"  # "Sum: 3"

# Split/join
"a,b,c" | split row ","        # ["a", "b", "c"]
["a", "b"] | str join ", "     # "a, b"

# Regex
"hello123" | parse --regex '(?P<word>\w+)(?P<num>\d+)'

# Multi-line strings
$"
Line 1
Line 2
"
```

### Glob Patterns (File Matching)

```nu
# Basic patterns
glob *.rs                         # All .rs files in current dir
glob **/*.rs                      # Recursive .rs files
glob **/*.{rs,toml}               # Multiple extensions
```

**Note**: Prefer `glob` over `find` or `ls` for file searches - it's more efficient and has better pattern support.

### Module System

```nu
# Define module
module my_module {
    export def public-func [] { ... }
    def private-func [] { ... }

    export const MY_CONST = 42
}

# Use module
use my_module *
use my_module [public-func MY_CONST]

# Import from file
use lib/helpers.nu *
```

## Row Conditions vs Closures

Many commands accept either a **row condition** or a **closure**:

### Row Conditions (Short-hand Syntax)

```nu
# Automatic $it expansion on left side
$table | where size > 100           # Expands to: $it.size > 100
$table | where name =~ "test"       # Expands to: $it.name =~ "test"

# Works with: where, filter (DEPRECATED, use where), find, skip while, take while, etc.
ls | where type == file             # Simple and readable
```

**Limitations**:
- Cannot be stored in variables
- Only field access on left side auto-expands
- Subexpressions need explicit `$it`:
  ```nu
  ls | where ($it.name | str downcase) =~ readme  # Need $it here
  ```

### Closures (Full Flexibility)

```nu
# Use $in or parameter name
$table | where {|row| $row.size > 100}
$table | where {$in.size > 100}

# Can be stored and reused
let big_files = {|row| $row.size > 1mb}
ls | where $big_files

# Works anywhere
$list | each {|x| $x * 2}
$list | where {$in > 10}
```

**When to use**:
- Row conditions: Simple field comparisons (cleaner syntax)
- Closures: Complex logic, reusable conditions, nested operations

## Common Pitfalls

### `each` on Single Records

```nu
# ❌ Don't pass single records to each
let record = {a: 1, b: 2}
$record | each {|field| print $field}  # Only runs once!

# ✅ Use items, values, or transpose instead
$record | items {|key, val| print $"($key): ($val)"}
$record | transpose key val | each {|row| ...}
```

### Pipe vs Call Ambiguity

```nu
# These are different!
$list | my-func arg1 arg2   # $list piped, arg1 & arg2 as params
my-func $list arg1 arg2     # All three as positional params (if signature allows)
```

### Optional Fields

```nu
# ❌ Error if field doesn't exist
$record.missing  # ERROR

# ✅ Use ?
$record.missing?  # null
$record.missing? | default "N/A"  # "N/A"
```

### Empty Collections

```nu
# Empty list/table checks
if ($list | is-empty) { ... }

# Default value if empty
$list | default -e $val_if_empty
```

## Advanced Topics

For advanced patterns and deeper dives, see:

- **[references/advanced-patterns.md](references/advanced-patterns.md)** - Performance optimization, lazy evaluation, streaming, closures, memory-efficient patterns
- **[references/type-system.md](references/type-system.md)** - Complete type system guide, conversions, generics, type guards

## Best Practices

1. **Use type signatures** - helps catch errors early
2. **Prefer pipelines** - more idiomatic and composable
3. **Document with comments** - `#` for inline, also `#` above declarations for doc comments
4. **Export selectively** - don't pollute namespace
5. **Use `default`** - handle null/missing gracefully
6. **Validate inputs** - check types/ranges at function start
7. **Return consistent types** - don't mix null and values unexpectedly
8. **Use modules** - organize related functions
9. **Test incrementally** - build complex pipelines step-by-step
10. **Prefix external commands with caret** - `^grep` instead of just `grep`. Makes it clear it's not a nushell command, avoids ambiguity. **Nushell commands always have precedence**, e.g. `find` is NOT usual Unix `find` tool: use `^find`.
11. **Use dedicated external commands when needed** - searching through lots of files is still faster with `grep` or `rg`, and large nested JSON structures will be processed much faster by `jq`

## Debugging Techniques

```nu
# Print intermediate values
$data | each {|x| print $x; $x}  # Prints and passes through

# Inspect type
$value | describe

# Debug point
debug           # Drops into debugger (if available)

# Timing
timeit { expensive-command }
```

## External Resources

- [Official Nushell Book](https://www.nushell.sh/book/)
- [Nushell Cookbook](https://www.nushell.sh/cookbook/)
- [Type Signatures Guide](https://www.nushell.sh/book/custom_commands.html#type-signatures)
- [Module System](https://www.nushell.sh/book/modules.html)
