---
name: dotnet-inspect
description: Query .NET APIs across NuGet packages, platform libraries, and local files. Search for types, list API surfaces, compare versions, find extension methods and implementors. Use whenever you need to answer questions about .NET library contents.
---

# dotnet-inspect

Query .NET library APIs — the same commands work across NuGet packages, platform libraries (System.*, Microsoft.AspNetCore.*), and local .dll/.nupkg files.

## Quick Decision Tree

- **Code broken?** → `diff --package Foo@old..new` first, then `member --oneline`
- **Need API surface?** → `member Type --package Foo --oneline` (token-efficient)
- **Need signatures?** → `member Type --package Foo -m Method` (default verbosity)
- **Need source/IL?** → `member Type --package Foo -m Method -v:d` (verbose, one overload at a time)
- **Need constructors?** → `member 'Type<T>' --package Foo -m .ctor` (use `<T>` not `<>`)
- **Need all overloads?** → `member Type --package Foo --select` (shows `Name:N` indices)

## When to Use This Skill

- **"What types are in this package?"** — `type` discovers types (terse), `find` searches by pattern
- **"What's the API surface?"** — `type` for discovery, `member` for detailed inspection (docs on)
- **"What changed between versions?"** — `diff` classifies breaking/additive changes
- **"This code uses an old API — fix it"** — `diff` the old..new version, then `member --oneline` to see the new API
- **"What extends this type?"** — `extensions` finds extension methods/properties
- **"What implements this interface?"** — `implements` finds concrete types
- **"What does this type depend on?"** — `depends` walks the type hierarchy upward
- **"What version/metadata does this have?"** — `package` and `library` inspect metadata
- **"Show me something cool"** — `demo` runs curated showcase queries

## Search Scope

Search commands (`find`, `extensions`, `implements`, `depends`) work across all of .NET:

```bash
dnx dotnet-inspect -y -- find "Chat*"                    # default scope (platform + curated)
dnx dotnet-inspect -y -- find "Chat*" --platform         # platform frameworks only
dnx dotnet-inspect -y -- find "Chat*" --extensions       # Microsoft.Extensions.* packages
dnx dotnet-inspect -y -- find "Chat*" --aspnetcore       # Microsoft.AspNetCore.* packages
dnx dotnet-inspect -y -- find "Chat*" --platform --extensions  # combine scopes
dnx dotnet-inspect -y -- find "Chat*" --package Foo      # specific NuGet package
dnx dotnet-inspect -y -- find "Chat*" --platform --package Foo  # platform + a specific package
```

Scope flags are combinable — use multiple flags to widen the search. `--package` works on all commands. `type`, `member`, `library`, `diff` also accept `--platform <name>` for a specific platform library.

## Examples by Task

### Discover types

```bash
dnx dotnet-inspect -y -- type --package System.Text.Json                   # all types in package
dnx dotnet-inspect -y -- type -t "*Serializer*" --package System.Text.Json # filter by glob
dnx dotnet-inspect -y -- type 'HashSet<T>' --platform System.Collections --shape  # type shape diagram
```

### Inspect members

```bash
dnx dotnet-inspect -y -- member JsonSerializer --package System.Text.Json --oneline    # scannable, token-efficient
dnx dotnet-inspect -y -- member JsonSerializer --package System.Text.Json              # members with docs
dnx dotnet-inspect -y -- member JsonSerializer --package System.Text.Json --no-docs    # suppress docs
dnx dotnet-inspect -y -- member JsonSerializer --package System.Text.Json -m Serialize # filter to member
dnx dotnet-inspect -y -- member -m JsonSerializer.Deserialize --package System.Text.Json  # dotted syntax
```

### Constructors and version pinning

```bash
dnx dotnet-inspect -y -- member 'Option<T>' --package System.CommandLine@2.0.2 -m .ctor   # generic type constructor
dnx dotnet-inspect -y -- member Command --package System.CommandLine@2.0.2 -m .ctor        # non-generic constructor
dnx dotnet-inspect -y -- member RootCommand --package System.CommandLine@2.0.2 -m .ctor    # derived type constructor
```

Pin versions with `@version` to get reproducible results: `--package System.CommandLine@2.0.2`

### Search for types

```bash
dnx dotnet-inspect -y -- find "*Handler*" --package System.CommandLine
dnx dotnet-inspect -y -- find "Option*,Argument*,Command*" --package System.CommandLine --oneline
dnx dotnet-inspect -y -- find "*Logger*"
```

### Compare versions (migrations)

```bash
dnx dotnet-inspect -y -- diff --package System.CommandLine@2.0.0-beta4.22272.1..2.0.2
dnx dotnet-inspect -y -- diff --package System.Text.Json@9.0.0..10.0.0 --breaking
dnx dotnet-inspect -y -- diff JsonSerializer --package System.Text.Json@9.0.0..10.0.0
```

### Fix broken code (API migration workflow)

When code doesn't compile due to API changes, use `diff` first to see all changes, then `member --oneline` to explore the new API:

```bash
# Step 1: See what changed between versions
dnx dotnet-inspect -y -- diff --package System.CommandLine@2.0.0-beta4.22272.1..2.0.2

# Step 2: Scan the new API surface (--oneline is token-efficient)
dnx dotnet-inspect -y -- member Command --package System.CommandLine@2.0.2 --oneline

# Step 3: Enumerate overloads (--select shows Name:N indices)
dnx dotnet-inspect -y -- member Command --package System.CommandLine@2.0.2 --select

# Step 4: Drill into a specific overload by index
dnx dotnet-inspect -y -- member Command --package System.CommandLine@2.0.2 -m SetAction:3
```

### Find extensions, implementors, and dependencies

```bash
dnx dotnet-inspect -y -- extensions HttpClient                   # what extends HttpClient?
dnx dotnet-inspect -y -- extensions IServiceCollection           # across default scope
dnx dotnet-inspect -y -- implements Stream                       # what extends Stream?
dnx dotnet-inspect -y -- implements IDisposable --platform       # across all platform frameworks
dnx dotnet-inspect -y -- depends 'INumber<TSelf>'                # type dependency hierarchy
```

### Explore with demo

```bash
dnx dotnet-inspect -y -- demo list                               # list curated demos
dnx dotnet-inspect -y -- demo 1                                # run a specific demo
dnx dotnet-inspect -y -- demo --feeling-lucky                    # random pick
```

### Inspect packages and libraries

```bash
dnx dotnet-inspect -y -- package System.Text.Json                # metadata, latest version
dnx dotnet-inspect -y -- package System.Text.Json --versions     # available versions
dnx dotnet-inspect -y -- package search "Azure.AI"               # search NuGet for packages
dnx dotnet-inspect -y -- library System.Text.Json                # library metadata, symbols
dnx dotnet-inspect -y -- library ./bin/MyLib.dll                 # local file
```

### Search with prefix scoping

```bash
dnx dotnet-inspect -y -- find "Chat*" --package-prefix Azure.AI  # search all Azure.AI.* packages
dnx dotnet-inspect -y -- extensions IChatClient --package-prefix Microsoft.Extensions.AI
```

## Command Reference

| Command | Purpose |
| ------- | ------- |
| `type` | **Discover types** — terse output, no docs, use `--shape` for hierarchy |
| `member` | **Inspect members** — docs on by default, supports dotted syntax (`-m Type.Member`) |
| `find` | Search for types by glob pattern across any scope |
| `diff` | Compare API surfaces between versions — breaking/additive classification |
| `extensions` | Find extension methods/properties for a type |
| `implements` | Find types implementing an interface or extending a base class |
| `depends` | Walk the type dependency hierarchy upward (interfaces, base classes) |
| `package` | Package metadata, files, versions, dependencies, `search` for NuGet discovery |
| `library` | Library metadata, symbols, references, dependencies |
| `demo` | Run curated showcase queries — list, invoke, or feeling-lucky |

## Key Syntax

- **Generic types** need quotes: `'Option<T>'`, `'IEnumerable<T>'`
- **Use `<T>` not `<>`** for generic types — `"Option<>"` resolves to the abstract base, `'Option<T>'` resolves to the concrete generic with constructors
- **`type` uses `-t`** for type filtering, **`member` uses `-m`** for member filtering (not `--filter`)
- **Dotted syntax** for `member`: `-m JsonSerializer.Deserialize`
- **Diff ranges** use `..`: `--package System.Text.Json@9.0.0..10.0.0`
- **Signatures** include `params` and default values from metadata
- **Derived types** only show their own members — query the base type too (e.g., `RootCommand` inherits `Add()` and `SetAction()` from `Command`)

## Installation

Use `dnx` (like `npx`). Always use `-y` and `--` to prevent interactive prompts:

```bash
dnx dotnet-inspect -y -- <command>
```

## Full Documentation

For comprehensive syntax, edge cases, and the flag compatibility matrix:

```bash
dnx dotnet-inspect -y -- llmstxt
```
