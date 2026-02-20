---
name: isol8
description: Securely execute untrusted Python, Node.js, Bun, Deno, and Bash code in sandboxed Docker containers.
---

# Isol8 Skill

Isol8 is a secure execution engine for running untrusted code inside Docker containers with strict resource limits, network controls, and output sanitization. Use this skill when you need to execute code, scripts, or system commands in a safe, isolated environment.

> For full documentation, see the [isol8 docs](https://bingo-ccc81346.mintlify.app). This file is a quick-reference for AI agents — it covers the most common operations and links to detailed docs for everything else.

## Quick Reference

### CLI Commands

| Command | Purpose | Full Docs |
|:--------|:--------|:----------|
| `isol8 run [file]` | Execute code in an isolated container | [CLI: run](https://bingo-ccc81346.mintlify.app/cli/run) |
| `isol8 setup` | Build Docker images, optionally bake in packages | [CLI: setup](https://bingo-ccc81346.mintlify.app/cli/setup) |
| `isol8 cleanup` | Remove orphaned isol8 containers | [CLI: cleanup](https://bingo-ccc81346.mintlify.app/cli/cleanup) |
| `isol8 serve` | Start HTTP server for remote execution (downloads binary on first use) | [CLI: serve](https://bingo-ccc81346.mintlify.app/cli/serve) |
| `isol8 config` | Display resolved configuration | [CLI: config](https://bingo-ccc81346.mintlify.app/cli/config) |

### Input Resolution (`isol8 run`)

1. `--eval` flag (inline code, defaults to `python` runtime)
2. File argument (runtime auto-detected from extension, or forced with `--runtime`)
3. Stdin (defaults to `python` runtime)

**Extension mapping:** `.py` → python, `.js`/`.mjs`/`.cjs` → node, `.ts` → bun, `.mts` → deno, `.sh` → bash

### Most-Used Flags (`isol8 run`)

| Flag | Default | Description |
|:-----|:--------|:------------|
| `-e, --eval <code>` | — | Execute inline code |
| `-r, --runtime <name>` | auto-detect | Force: `python`, `node`, `bun`, `deno`, `bash` |
| `--no-stream` | `false` | Disable real-time output streaming |
| `--persistent` | `false` | Keep container alive between runs |
| `--persist` | `false` | Keep container after execution for debugging |
| `--debug` | `false` | Enable internal debug logging |
| `--install <package>` | — | Install package before execution (repeatable) |
| `--net <mode>` | `none` | Network: `none`, `host`, `filtered` |
| `--timeout <ms>` | `30000` | Execution timeout |
| `--memory <limit>` | `512m` | Memory limit |
| `--secret <KEY=VALUE>` | — | Secret env var, value masked in output (repeatable) |
| `--stdin <data>` | — | Pipe data to stdin |

For the complete flag reference (20 flags total), see [CLI: run](https://bingo-ccc81346.mintlify.app/cli/run).

## CLI Examples

```bash
# Python inline
isol8 run -e "print('Hello!')" --runtime python

# Run a file (runtime auto-detected)
isol8 run script.py

# With package installation
isol8 run -e "import numpy; print(numpy.__version__)" --runtime python --install numpy

# Pipe via stdin
echo "console.log(42)" | isol8 run --runtime node

# Secrets (masked as *** in output)
isol8 run -e "import os; print(os.environ['KEY'])" --runtime python --secret KEY=sk-1234

# Remote execution
isol8 run script.py --host http://server:3000 --key my-api-key

# Cleanup orphaned containers
isol8 cleanup               # Interactive (prompts for confirmation)
isol8 cleanup --force       # Skip confirmation
```

## Library API (Quick Reference)

For full library documentation, see [Library Overview](https://bingo-ccc81346.mintlify.app/library/overview).

### DockerIsol8

```typescript
import { DockerIsol8 } from "isol8";

const isol8 = new DockerIsol8({
  mode: "ephemeral",     // or "persistent"
  network: "none",       // or "host" or "filtered"
  memoryLimit: "512m",
  cpuLimit: 1.0,
  timeoutMs: 30000,
  secrets: {},           // values masked in output
  persist: false,        // keep container after execution for debugging
  debug: false,          // enable internal debug logging
});

await isol8.start();

const result = await isol8.execute({
  code: 'print("hello")',
  runtime: "python",
  installPackages: ["numpy"],  // optional
});

console.log(result.stdout);    // captured output
console.log(result.exitCode);  // 0 = success
console.log(result.durationMs);

await isol8.stop();
```

Full options reference: [Execution Options](https://bingo-ccc81346.mintlify.app/library/execution)

### RemoteIsol8

```typescript
import { RemoteIsol8 } from "isol8";

const isol8 = new RemoteIsol8(
  { host: "http://localhost:3000", apiKey: "secret" },
  { network: "none" }
);
await isol8.start();
const result = await isol8.execute({ code: "print(1)", runtime: "python" });
await isol8.stop();
```

### Streaming

```typescript
for await (const event of isol8.executeStream({
  code: 'for i in range(5): print(i)',
  runtime: "python",
})) {
  if (event.type === "stdout") process.stdout.write(event.data);
  if (event.type === "exit") console.log("Exit code:", event.data);
}
```

Full streaming docs: [Streaming](https://bingo-ccc81346.mintlify.app/library/streaming)

### File I/O (Persistent Mode)

```typescript
await isol8.putFile("/sandbox/data.csv", "col1,col2\n1,2");
const buf = await isol8.getFile("/sandbox/output.txt");
```

Full file I/O docs: [File I/O](https://bingo-ccc81346.mintlify.app/library/file-io)

## HTTP Server API

Full endpoint reference: [Server Endpoints](https://bingo-ccc81346.mintlify.app/server/endpoints)

| Method | Path | Auth | Description |
|:-------|:-----|:-----|:------------|
| `GET` | `/health` | No | Health check |
| `POST` | `/execute` | Yes | Execute code, return result |
| `POST` | `/execute/stream` | Yes | Execute code, SSE stream |
| `POST` | `/file` | Yes | Upload file (base64) |
| `GET` | `/file` | Yes | Download file (base64) |
| `DELETE` | `/session/:id` | Yes | Destroy persistent session |

## Configuration

Config is loaded from (first found): `./isol8.config.json` or `~/.isol8/config.json`. Partial configs are deep-merged with defaults.

Full configuration reference: [Configuration](https://bingo-ccc81346.mintlify.app/configuration)

## Security Defaults

| Layer | Default |
|:------|:--------|
| Filesystem | Read-only root, `/sandbox` tmpfs 512MB (exec allowed), `/tmp` tmpfs 256MB (noexec) |
| User isolation | Non-root `sandbox` user (uid 100), processes killed between pool reuses |
| Processes | PID limit 64, `no-new-privileges` |
| Resources | 1 CPU, 512MB memory, 30s timeout |
| Network | Disabled (`none`), iptables enforcement in `filtered` mode |
| Output | Truncated at 1MB, secrets masked |
| Seccomp | "safety" (blocks mount, swap, ptrace, etc.) |

**Container Filesystem:**
- `/sandbox` (512MB): Working directory, packages installed here, execution allowed for `.so` files
- `/tmp` (256MB): Temporary files, no execution allowed for security

Full security model: [Security](https://bingo-ccc81346.mintlify.app/security)

## Troubleshooting

- **"Docker not running"**: Run `isol8 setup` to check.
- **Timeouts**: Increase `--timeout`. Process is killed on timeout.
- **OOM Killed**: Increase `--memory`.
- **"No space left on device"**: Increase `--sandbox-size` (default 512MB) or `--tmp-size` (default 256MB).
- **"Operation not permitted" with numpy/packages**: Packages need `--sandbox-size` large enough for installation (512MB+ recommended).
- **`.ts` files running with Bun instead of Deno**: `.ts` defaults to Bun. Use `--runtime deno` or `.mts` extension.
- **Serve command failing**: Ensure the server binary can be downloaded from GitHub Releases. Use `isol8 serve --update` to force a fresh download. Use `isol8 serve --debug` to see detailed server logs. For listen port selection, precedence is `--port` > `ISOL8_PORT` > `PORT` > `3000`; if the port is busy, `serve` can prompt for another port or auto-pick an available one.
