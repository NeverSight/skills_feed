---
name: platform-abstraction
description: Use @effect/platform abstractions for cross-platform file I/O, process spawning, HTTP clients, and terminal operations. Apply this skill when writing code that interacts with the filesystem, spawns processes, makes HTTP requests, or performs console I/O to ensure portability across Node.js, Bun, and browser environments.
---

# Platform Abstraction with @effect/platform

## Overview

The `@effect/platform` library provides platform-independent abstractions that work seamlessly across Node.js, Bun, and browser environments. Instead of using runtime-specific APIs directly, you write code once using Effect Platform services and run it anywhere.

**When to use this skill:**
- Writing file system operations
- Spawning child processes or executing commands
- Making HTTP requests
- Reading CLI arguments or environment variables
- Performing console/terminal I/O
- Working with paths across different operating systems
- Building cross-platform applications or libraries

## Why Effect Platform?

### 1. Cross-Platform Compatibility

Write once, run anywhere:

```typescript
import { FileSystem } from "@effect/platform"
import { Effect } from "effect"

// Works on Node.js, Bun, and browsers
const readConfig = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  return yield* fs.readFileString("config.json")
})
```

### 2. Type-Safe Error Handling

All operations track errors in the Effect type signature:

```typescript
import { FileSystem } from "@effect/platform"
import { Effect } from "effect"

// Effect<string, PlatformError, FileSystem>
//        ↓           ↓              ↓
//                                   Required service
//                     Typed error channel
//          Success value
```

### 3. Resource Safety

Automatic cleanup with `Scope`:

```typescript
import { FileSystem } from "@effect/platform"
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  // Read entire file into memory
  return yield* fs.readFile("data.txt")
})
```

### 4. Testability

Easy to mock and stub services:

```typescript
import { FileSystem } from "@effect/platform"
import { Effect, Layer } from "effect"

declare const myProgram: Effect.Effect<void, never, FileSystem.FileSystem>

const TestFileSystem = Layer.succeed(
  FileSystem.FileSystem,
  FileSystem.make({
    readFile: () => Effect.succeed(new Uint8Array())
  })
)

const test = myProgram.pipe(Effect.provide(TestFileSystem))
```

### 5. Composability

Integrates naturally with Effect's service system:

```typescript
import { FileSystem, Path } from "@effect/platform"
import { Context, Effect, Layer } from "effect"

interface ConfigService {
  readonly load: (name: string) => Effect.Effect<string>
}

const ConfigService = Context.GenericTag<ConfigService>("ConfigService")

const ConfigServiceLive = Layer.effect(
  ConfigService,
  Effect.gen(function* () {
    const fs = yield* FileSystem.FileSystem
    const path = yield* Path.Path

    return {
      load: (name: string) =>
        Effect.gen(function* () {
          const configPath = path.join("configs", name)
          return yield* fs.readFileString(configPath)
        })
    }
  })
)
```

## Core Platform Modules

### FileSystem - File Operations

The `FileSystem` service provides comprehensive file and directory operations.

**Anti-Pattern - Direct Node/Bun APIs:**

```typescript
// ❌ WRONG - Platform-specific, not testable
import * as fs from "fs"
import { readFile } from "fs/promises"

const content = fs.readFileSync("file.txt", "utf-8")
const asyncContent = await readFile("file.txt", "utf-8")

// ❌ WRONG - Bun-specific
declare const Bun: {
  file: (path: string) => { text: () => Promise<string> }
}

const file = Bun.file("file.txt")
const content = await file.text()
```

**Correct Pattern - FileSystem Service:**

```typescript
import { FileSystem } from "@effect/platform"
import { Effect } from "effect"

// ✅ CORRECT - Cross-platform, type-safe, testable
const readFile = (path: string) =>
  Effect.gen(function* () {
    const fs = yield* FileSystem.FileSystem
    return yield* fs.readFileString(path)
  })

// Effect<string, PlatformError, FileSystem>
```

**Common Operations:**

```typescript
import { FileSystem } from "@effect/platform"
import { Effect } from "effect"

const fileOperations = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem

  // Read files
  const text = yield* fs.readFileString("data.txt")
  const bytes = yield* fs.readFile("binary.dat")

  // Write files
  yield* fs.writeFileString("output.txt", "Hello World")

  // Directory operations
  yield* fs.makeDirectory("new-dir", { recursive: true })
  const files = yield* fs.readDirectory("src")

  // File metadata
  const stats = yield* fs.stat("file.txt")
  const exists = yield* fs.exists("config.json")

  // Copy and move
  yield* fs.copy("source.txt", "dest.txt")
  yield* fs.rename("old.txt", "new.txt")

  // Remove files/directories
  yield* fs.remove("temp-file.txt")
  yield* fs.remove("temp-dir", { recursive: true })

  // Temporary files (auto-cleanup with Scope)
  const tempFile = yield* fs.makeTempFileScoped()
  yield* fs.writeFileString(tempFile, "temporary data")
  // File automatically deleted when scope closes
})
```

**Streaming Files:**

```typescript
import { FileSystem } from "@effect/platform"
import { Effect, Stream, Chunk } from "effect"

declare const processChunk: (chunk: Chunk.Chunk<Uint8Array>) => Effect.Effect<void>

// Stream large files efficiently
const processLargeFile = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem

  // Read as stream
  const stream = fs.stream("large-file.txt", { chunkSize: 64 * 1024 })

  // Process stream
  yield* stream.pipe(
    Stream.mapEffect((chunk) => processChunk(chunk)),
    Stream.run(fs.sink("output.txt"))
  )
})
```

### Path - Path Manipulation

The `Path` service provides cross-platform path operations.

**Anti-Pattern - Manual String Manipulation:**

```typescript
// ❌ WRONG - Breaks on Windows, brittle
import path from "path"

declare const process: { cwd: () => string }
declare const filename: string

const configPath = "./config/" + filename + ".json"
const absPath = process.cwd() + "/" + configPath

// ❌ WRONG - Node-specific
const joined = path.join("src", "components", "Button.tsx")
```

**Correct Pattern - Path Service:**

```typescript
import { Path } from "@effect/platform"
import { Effect } from "effect"

// ✅ CORRECT - Cross-platform path handling
const buildPath = (filename: string) =>
  Effect.gen(function* () {
    const path = yield* Path.Path

    // Join paths correctly for any OS
    const configPath = path.join("config", `${filename}.json`)

    // Resolve to absolute path
    const absolutePath = path.resolve(configPath)

    // Extract path components
    const dir = path.dirname(absolutePath)
    const base = path.basename(absolutePath)
    const ext = path.extname(absolutePath)

    // Parse path into components
    const parsed = path.parse(absolutePath)
    // { root, dir, base, ext, name }

    return absolutePath
  })
```

**Path Operations:**

```typescript
import { Path } from "@effect/platform"
import { Effect } from "effect"

const pathOps = Effect.gen(function* () {
  const path = yield* Path.Path

  // Platform-specific separator ("/" or "\")
  const sep = path.sep

  // Join multiple segments
  const filePath = path.join("src", "lib", "utils.ts")

  // Resolve relative paths
  const absolute = path.resolve("..", "config", "app.json")

  // Get relative path between two paths
  const rel = path.relative("/app/src", "/app/dist")

  // Check if path is absolute
  const isAbs = path.isAbsolute("/usr/local")

  // Normalize path (remove "..", ".", etc.)
  const normalized = path.normalize("src/../lib/./utils.ts")

  // Work with file URLs
  const url = yield* path.toFileUrl("/path/to/file")
  const fromUrl = yield* path.fromFileUrl(new URL("file:///path/to/file"))
})
```

### Command - Process Execution

The `Command` and `CommandExecutor` services enable safe process spawning.

**Anti-Pattern - Direct child_process:**

```typescript
// ❌ WRONG - Node-specific, no resource safety
import { spawn, exec } from "child_process"
import { promisify } from "util"

const execAsync = promisify(exec)
const { stdout } = await execAsync("ls -la")

// ❌ WRONG - Bun-specific
declare const Bun: {
  spawn: (cmd: string[]) => { stdout: ReadableStream }
}
declare const Response: { new(stream: ReadableStream): { text: () => Promise<string> } }

const proc = Bun.spawn(["ls", "-la"])
const output = await new Response(proc.stdout).text()
```

**Correct Pattern - Command Service:**

```typescript
import { Command, CommandExecutor } from "@effect/platform"
import { Effect, Stream } from "effect"

// ✅ CORRECT - Cross-platform command execution
const runCommand = Effect.gen(function* () {
  const executor = yield* CommandExecutor.CommandExecutor

  // Create command
  const cmd = Command.make("ls", "-la")

  // Execute and get output as string
  const output = yield* cmd.pipe(
    Command.stdout("string"),
    Effect.flatMap((proc) => proc.exitCode)
  )

  return output
})
```

**Advanced Command Usage:**

```typescript
import { Command, CommandExecutor } from "@effect/platform"
import { Effect, Stream, Chunk } from "effect"

const commandExamples = Effect.gen(function* () {
  const executor = yield* CommandExecutor.CommandExecutor

  // Simple command execution
  const ls = Command.make("ls", "-la")
  const exitCode = yield* Command.exitCode(ls)

  // Capture stdout as string
  const git = Command.make("git", "status")
  const stdout = yield* Command.string(git)

  // Capture stdout as lines
  const lines = yield* Command.lines(git)

  // Stream stdout
  const stream = Command.stdout(git)
  yield* stream.pipe(
    Stream.mapEffect((chunk: Chunk.Chunk<Uint8Array>) => Effect.log(chunk.toString())),
    Stream.runDrain
  )

  // Pipe commands together
  const pipeline = Command.make("cat", "file.txt").pipe(
    Command.pipeTo(Command.make("grep", "error")),
    Command.pipeTo(Command.make("wc", "-l"))
  )

  // Set environment variables
  const withEnv = Command.make("node", "script.js").pipe(
    Command.env({
      NODE_ENV: "production",
      API_KEY: "secret"
    })
  )

  // Set working directory
  const withCwd = Command.make("npm", "install").pipe(
    Command.workingDirectory("/path/to/project")
  )

  // Feed stdin
  const withInput = Command.make("base64").pipe(
    Command.feed("Hello World")
  )

  // Start process and interact
  const process = yield* executor.start(git)
  const code = yield* process.exitCode

  return code
})
```

### Terminal - Terminal I/O

The `Terminal` service provides interactive terminal capabilities.

**Anti-Pattern - Direct Console:**

```typescript
// ❌ WRONG - Uses global console, not testable
declare const console: {
  log: (msg: string) => void
  error: (msg: string) => void
}
declare const process: {
  stdout: { write: (msg: string) => void }
}
declare const prompt: (msg: string) => string | null

console.log("Hello World")
console.error("Error occurred")
process.stdout.write("Output\n")

// ❌ WRONG - Not trackable in Effect type
const input = prompt("Enter name:")
```

**Correct Pattern - Terminal Service:**

```typescript
import { Terminal } from "@effect/platform"
import { Effect } from "effect"

// ✅ CORRECT - Trackable, testable terminal I/O
const interactiveProgram = Effect.gen(function* () {
  const terminal = yield* Terminal.Terminal

  // Display output
  yield* terminal.display("Hello World\n")

  // Read user input
  const name = yield* terminal.readLine
  yield* terminal.display(`Welcome, ${name}!\n`)

  // Get terminal dimensions
  const cols = yield* terminal.columns
  yield* terminal.display(`Terminal width: ${cols}\n`)
})
```

**For Simple Logging - Use Console or Effect.log:**

```typescript
import { Console, Effect } from "effect"

// ✅ CORRECT - Console service (from effect)
const logging = Effect.gen(function* () {
  yield* Console.log("Info message")
  yield* Console.error("Error message")
  yield* Console.warn("Warning")
  yield* Console.debug("Debug info")
})

// ✅ CORRECT - Effect.log with structured logging
const structuredLog = Effect.gen(function* () {
  yield* Effect.log("Operation started")
  yield* Effect.logDebug("Debug details")
  yield* Effect.logError("Error occurred")

  // With annotations
  yield* Effect.log("User action").pipe(
    Effect.annotateLogs("userId", "123"),
    Effect.annotateLogs("action", "login")
  )
})
```

### HttpClient - HTTP Requests

The `HttpClient` service provides type-safe HTTP operations.

**Anti-Pattern - Direct fetch/axios:**

```typescript
// ❌ WRONG - No Effect integration, manual error handling
declare const fetch: (url: string) => Promise<{ json: () => Promise<unknown> }>

const response = await fetch("https://api.example.com/data")
const data = await response.json()

// ❌ WRONG - External dependency, not in Effect system
import axios from "axios"

declare const axios: {
  get: (url: string) => Promise<{ data: unknown }>
}

const result = await axios.get("https://api.example.com/data")
```

**Correct Pattern - HttpClient Service:**

```typescript
import { HttpClient, HttpClientRequest } from "@effect/platform"
import { Effect } from "effect"

// ✅ CORRECT - Integrated with Effect type system
const fetchData = Effect.gen(function* () {
  const client = yield* HttpClient.HttpClient

  // Simple GET request
  const response = yield* client.get("https://api.example.com/data")
  const data = yield* response.json

  return data
})
```

**Advanced HTTP Operations:**

```typescript
import {
  HttpClient,
  HttpClientRequest,
  HttpClientResponse
} from "@effect/platform"
import { Effect, Schema, Schedule } from "effect"

const User = Schema.Struct({
  id: Schema.Number,
  name: Schema.String,
  email: Schema.String
})

const httpExamples = Effect.gen(function* () {
  const client = yield* HttpClient.HttpClient

  // GET with query parameters
  const getUsers = client.get("https://api.example.com/users", {
    urlParams: { page: "1", limit: "10" }
  })

  // POST with JSON body
  const createUser = client.post("https://api.example.com/users", {
    body: HttpClientRequest.jsonBody({
      name: "John Doe",
      email: "john@example.com"
    })
  })

  // Custom headers
  const withAuth = client.get("https://api.example.com/protected").pipe(
    HttpClientRequest.setHeader("Authorization", "Bearer token")
  )

  // Parse response with Schema
  const users = yield* client.get("https://api.example.com/users").pipe(
    Effect.flatMap(HttpClientResponse.schemaBodyJson(Schema.Array(User)))
  )

  // Error handling
  const safeRequest = client.get("https://api.example.com/data").pipe(
    Effect.catchTag("RequestError", (error) =>
      Effect.succeed({ error: "Network error" })
    ),
    Effect.catchTag("ResponseError", (error) =>
      Effect.succeed({ error: `HTTP ${error.status}` })
    )
  )

  // Retries with backoff
  const withRetries = client.get("https://api.example.com/data").pipe(
    Effect.retry({
      times: 3,
      schedule: Schedule.exponential("100 millis")
    })
  )

  return users
})
```

### KeyValueStore - Key-Value Storage

The `KeyValueStore` service provides platform-independent key-value storage.

**Anti-Pattern - Direct localStorage/file-based storage:**

```typescript
// ❌ WRONG - Browser-specific
declare const localStorage: {
  setItem: (key: string, value: string) => void
  getItem: (key: string) => string | null
}

localStorage.setItem("key", "value")
const value = localStorage.getItem("key")

// ❌ WRONG - Node-specific, manual file handling
import fs from "fs"

declare const fs: {
  writeFileSync: (path: string, data: string) => void
  readFileSync: (path: string, encoding: string) => string
}

fs.writeFileSync(".cache/key", "value")
const value2 = fs.readFileSync(".cache/key", "utf-8")
```

**Correct Pattern - KeyValueStore Service:**

```typescript
import { KeyValueStore } from "@effect/platform"
import { Effect, Schema } from "effect"

// ✅ CORRECT - Works on all platforms
const cacheData = Effect.gen(function* () {
  const store = yield* KeyValueStore.KeyValueStore

  // Set value
  yield* store.set("user:123", "John Doe")

  // Get value
  const name = yield* store.get("user:123")

  // Check existence
  const hasUser = yield* store.has("user:123")

  // Remove value
  yield* store.remove("user:123")

  // Clear all
  yield* store.clear

  return name
})
```

**Schema-Based Store:**

```typescript
import { KeyValueStore } from "@effect/platform"
import { Effect, Schema } from "effect"

const User = Schema.Struct({
  id: Schema.Number,
  name: Schema.String,
  email: Schema.String
})

const typedStore = Effect.gen(function* () {
  const store = yield* KeyValueStore.KeyValueStore

  // Create schema-based store
  const userStore = store.forSchema(User)

  // Type-safe operations
  yield* userStore.set("user:123", {
    id: 123,
    name: "John Doe",
    email: "john@example.com"
  })

  const user = yield* userStore.get("user:123")
  // user: Option<{ id: number, name: string, email: string }>
})
```

### CLI Arguments - @effect/cli

For CLI applications, use `@effect/cli` instead of direct `process.argv`.

**Anti-Pattern - Direct process.argv:**

```typescript
// ❌ WRONG - Manual parsing, no validation
declare const process: { argv: string[] }

const args = process.argv.slice(2)
const input = args[0]
const verbose = args.includes("--verbose")

// ❌ WRONG - Third-party parser, not Effect-integrated
import yargs from "yargs"

declare const yargs: (args: string[]) => { argv: Record<string, unknown> }

const argv = yargs(process.argv.slice(2)).argv
```

**Correct Pattern - @effect/cli:**

```typescript
import { Args, Command as CliCommand, Options } from "@effect/cli"
import { NodeContext, NodeRuntime } from "@effect/platform-node"
import { Effect, Console } from "effect"

declare const process: { argv: string[] }
declare const someOperation: Effect.Effect<string>

// ✅ CORRECT - Type-safe CLI with full Effect integration
// Define arguments
const inputArg = Args.file({ name: "input", exists: "yes" })

// Define options
const verboseOpt = Options.boolean("verbose").pipe(
  Options.withAlias("v")
)

// Define command
const command = CliCommand.make("process", { input: inputArg, verbose: verboseOpt },
  ({ input, verbose }) =>
    Effect.gen(function* () {
      if (verbose) {
        yield* Console.log(`Processing file: ${input}`)
      }
      // Process the file
      yield* someOperation
    })
)

// Run CLI
const cli = CliCommand.run(command, {
  name: "File Processor",
  version: "1.0.0"
})

cli(process.argv).pipe(
  Effect.provide(NodeContext.layer),
  NodeRuntime.runMain
)
```

## Platform Module Reference

Complete reference table of platform abstractions:

| Need | Use | Instead of | Package |
|------|-----|------------|---------|
| **File I/O** | `FileSystem.FileSystem` | `fs`, `Bun.file` | `@effect/platform` |
| **Path Operations** | `Path.Path` | `path`, string concat | `@effect/platform` |
| **Process Spawning** | `Command` + `CommandExecutor` | `child_process`, `Bun.spawn` | `@effect/platform` |
| **Terminal I/O** | `Terminal.Terminal` | `process.stdin/stdout` | `@effect/platform` |
| **Console Logging** | `Console.log` or `Effect.log` | `console.log` | `effect` |
| **HTTP Client** | `HttpClient.HttpClient` | `fetch`, `axios` | `@effect/platform` |
| **HTTP Server** | `HttpServer.HttpServer` | `http.createServer` | `@effect/platform` |
| **Key-Value Store** | `KeyValueStore.KeyValueStore` | `localStorage`, manual files | `@effect/platform` |
| **CLI Arguments** | `@effect/cli` Args | `process.argv`, `yargs` | `@effect/cli` |
| **Environment Variables** | `Config` from effect | `process.env` | `effect` |
| **Workers** | `Worker.Worker` | `Worker`, `worker_threads` | `@effect/platform` |
| **Sockets** | `Socket.Socket` | `net.Socket`, `WebSocket` | `@effect/platform` |
| **Streams** | `Stream` | Node streams, ReadableStream | `effect` |

## Setting Up Platform-Specific Layers

To use platform services, provide the appropriate platform layer:

**Node.js:**

```typescript
import { NodeContext, NodeRuntime } from "@effect/platform-node"
import { FileSystem } from "@effect/platform"
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  return yield* fs.readFileString("file.txt")
})

program.pipe(
  Effect.provide(NodeContext.layer),
  NodeRuntime.runMain
)
```

**Bun:**

```typescript
import { BunContext, BunRuntime } from "@effect/platform-bun"
import { FileSystem } from "@effect/platform"
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  return yield* fs.readFileString("file.txt")
})

program.pipe(
  Effect.provide(BunContext.layer),
  BunRuntime.runMain
)
```

**Browser:**

```typescript
import { BrowserContext, BrowserRuntime } from "@effect/platform-browser"
import { HttpClient } from "@effect/platform"
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const http = yield* HttpClient.HttpClient
  return yield* http.get("https://api.example.com/data")
})

program.pipe(
  Effect.provide(BrowserContext.layer),
  BrowserRuntime.runMain
)
```

## Complete Example: Cross-Platform File Processor

```typescript
import { FileSystem, Path, Command, CommandExecutor } from "@effect/platform"
import { NodeContext, NodeRuntime } from "@effect/platform-node"
import { BunContext, BunRuntime } from "@effect/platform-bun"
import { Effect, Console, Schema } from "effect"

const Config = Schema.Struct({
  inputDir: Schema.String,
  outputDir: Schema.String,
  compress: Schema.Boolean
})

const processFiles = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  const path = yield* Path.Path
  const executor = yield* CommandExecutor.CommandExecutor

  // Load configuration
  const configData = yield* fs.readFileString("config.json")
  const config = yield* Schema.decode(Config)(JSON.parse(configData))

  // Ensure output directory exists
  yield* fs.makeDirectory(config.outputDir, { recursive: true })

  // Read input files
  const files = yield* fs.readDirectory(config.inputDir)

  yield* Console.log(`Processing ${files.length} files...`)

  // Process each file
  yield* Effect.forEach(files, (file) =>
    Effect.gen(function* () {
      const inputPath = path.join(config.inputDir, file)
      const outputPath = path.join(config.outputDir, file)

      // Copy file
      yield* fs.copy(inputPath, outputPath)

      // Optionally compress
      if (config.compress) {
        const cmd = Command.make("gzip", outputPath)
        yield* Command.exitCode(cmd)
      }

      yield* Console.log(`Processed: ${file}`)
    }),
    { concurrency: 4 }
  )

  yield* Console.log("All files processed!")
})

// Run on Node.js
processFiles.pipe(
  Effect.provide(NodeContext.layer),
  NodeRuntime.runMain
)

// Or run on Bun - same code!
processFiles.pipe(
  Effect.provide(BunContext.layer),
  BunRuntime.runMain
)
```

## Testing with Platform Abstractions

One major benefit of platform abstractions is testability:

```typescript
import { FileSystem } from "@effect/platform"
import { Effect, Layer } from "effect"

declare const myFileProcessor: Effect.Effect<void, never, FileSystem.FileSystem>

// Create mock FileSystem using makeNoop for testing
const TestFileSystem = Layer.succeed(
  FileSystem.FileSystem,
  FileSystem.makeNoop({
    readFile: (path) => {
      if (path === "config.json") {
        const data = JSON.stringify({ key: "value" })
        return Effect.succeed(new TextEncoder().encode(data))
      }
      return Effect.fail(new Error("File not found"))
    },
    exists: (path) => Effect.succeed(true)
  })
)

// Test your code
const testProgram = myFileProcessor.pipe(
  Effect.provide(TestFileSystem)
)

Effect.runPromise(testProgram)
```

## Quality Checklist

Before completing code that uses platform operations:

- [ ] All file I/O uses `FileSystem.FileSystem` service
- [ ] All path operations use `Path.Path` service
- [ ] Process spawning uses `Command` + `CommandExecutor`
- [ ] Console output uses `Console.log` or `Effect.log` (not `console.log`)
- [ ] CLI arguments parsed with `@effect/cli` (not `process.argv`)
- [ ] HTTP requests use `HttpClient.HttpClient` (not `fetch`/`axios`)
- [ ] Platform services accessed through Effect type system
- [ ] Appropriate platform layer provided (`NodeContext.layer`, `BunContext.layer`, etc.)
- [ ] No direct imports from `fs`, `path`, `child_process`, `http`, etc.
- [ ] No Bun-specific APIs (`Bun.file`, `Bun.spawn`, etc.)
- [ ] No browser-specific APIs without platform abstraction
- [ ] Code is testable with mock platform services

## Common Mistakes to Avoid

### 1. Mixing Platform APIs

```typescript
import { FileSystem } from "@effect/platform"
import { Effect } from "effect"
import fs from "fs"

// ❌ WRONG - Mixing Effect Platform with direct APIs
const bad = Effect.gen(function* () {
  const filesystem = yield* FileSystem.FileSystem
  const content1 = yield* filesystem.readFileString("file1.txt")
  const content2 = fs.readFileSync("file2.txt", "utf-8") // Don't mix!
})

// ✅ CORRECT - Use platform abstractions consistently
const good = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  const content1 = yield* fs.readFileString("file1.txt")
  const content2 = yield* fs.readFileString("file2.txt")
})
```

### 2. Forgetting Platform Layer

```typescript
import { FileSystem } from "@effect/platform"
import { NodeContext, NodeRuntime } from "@effect/platform-node"
import { Effect } from "effect"

// ❌ WRONG - No platform layer provided
const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  return yield* fs.readFileString("file.txt")
})

Effect.runPromise(program) // Runtime error!

// ✅ CORRECT - Provide platform layer
program.pipe(
  Effect.provide(NodeContext.layer),
  NodeRuntime.runMain
)
```

### 3. Using console.log

```typescript
import { Console, Effect } from "effect"

declare const someOperation: () => Effect.Effect<string>

// ❌ WRONG - Direct console usage
const badProgram = Effect.gen(function* () {
  console.log("Starting...")
  const result = yield* someOperation()
  console.log("Done!")
  return result
})

// ✅ CORRECT - Use Console or Effect.log
const goodProgram = Effect.gen(function* () {
  yield* Console.log("Starting...")
  const result = yield* someOperation()
  yield* Console.log("Done!")
  return result
})
```

## Migration Guide

### From Node.js fs to FileSystem

```typescript
import { FileSystem } from "@effect/platform"
import { Effect } from "effect"
import fs from "fs/promises"

// Before (Node.js)
declare const fs: {
  readFile: (path: string, encoding: string) => Promise<string>
  writeFile: (path: string, data: string) => Promise<void>
  existsSync: (path: string) => boolean
}

const data = await fs.readFile("file.txt", "utf-8")
await fs.writeFile("output.txt", data)
const exists = fs.existsSync("config.json")

// After (Effect Platform)
const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem

  const data = yield* fs.readFileString("file.txt")
  yield* fs.writeFileString("output.txt", data)
  const exists = yield* fs.exists("config.json")
})
```

### From fetch to HttpClient

```typescript
import { HttpClient, HttpClientRequest } from "@effect/platform"
import { Effect } from "effect"

// Before (fetch)
declare const fetch: (url: string, options: {
  method: string
  headers: Record<string, string>
  body: string
}) => Promise<{ json: () => Promise<unknown> }>

const response = await fetch("https://api.example.com/data", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ key: "value" })
})
const data = await response.json()

// After (Effect HttpClient)
const program = Effect.gen(function* () {
  const client = yield* HttpClient.HttpClient

  const response = yield* client.post("https://api.example.com/data", {
    body: HttpClientRequest.jsonBody({ key: "value" })
  })
  const data = yield* response.json

  return data
})
```

### From child_process to Command

```typescript
import { Command } from "@effect/platform"
import { Effect } from "effect"
import { exec } from "child_process"
import { promisify } from "util"

// Before (child_process)
declare const exec: (cmd: string, callback: (error: Error | null, result: { stdout: string }) => void) => void
declare const promisify: <T>(fn: T) => (...args: any[]) => Promise<any>

const execAsync = promisify(exec)
const { stdout } = await execAsync("git status")

// After (Effect Command)
const program = Effect.gen(function* () {
  const cmd = Command.make("git", "status")
  const stdout = yield* Command.string(cmd)
  return stdout
})
```

## Summary

Effect Platform provides a complete abstraction layer over platform-specific APIs, enabling you to:

1. **Write once, run anywhere** - Same code works on Node.js, Bun, and browsers
2. **Type-safe operations** - All errors tracked in Effect type signatures
3. **Resource safety** - Automatic cleanup with Scope
4. **Easy testing** - Mock services without touching the filesystem
5. **Full Effect integration** - Compose with services, layers, and error handling

Always prefer Effect Platform abstractions over direct platform APIs for maximum portability, safety, and testability.
