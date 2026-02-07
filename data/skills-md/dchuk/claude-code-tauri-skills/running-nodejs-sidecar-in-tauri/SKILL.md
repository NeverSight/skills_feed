---
name: running-nodejs-sidecar-in-tauri
description: Guides users through running Node.js as a sidecar process in Tauri applications, enabling JavaScript backend functionality without requiring end-user Node.js installations.
---

# Running Node.js as a Sidecar in Tauri

Package and run Node.js applications as sidecar processes in Tauri desktop applications, leveraging the Node.js ecosystem without requiring users to install Node.js.

## Why Use a Node.js Sidecar

- Bundle existing Node.js tools and libraries with your Tauri application
- No external Node.js runtime dependency for end users
- Leverage npm packages that have no Rust equivalent
- Isolate Node.js logic from the main Tauri process
- Cross-platform support (Windows, macOS, Linux)

## Prerequisites

1. Existing Tauri v2 application
2. Shell plugin installed and configured
3. Node.js and npm on the development machine
4. Rust toolchain (1.84.0+ recommended)

### Install the Shell Plugin

```bash
npm install @tauri-apps/plugin-shell
cargo add tauri-plugin-shell --manifest-path src-tauri/Cargo.toml
```

Register in `src-tauri/src/lib.rs`:

```rust
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Project Structure

```
my-tauri-app/
├── package.json
├── src-tauri/
│   ├── binaries/
│   │   └── my-sidecar-<target-triple>[.exe]
│   ├── capabilities/default.json
│   ├── tauri.conf.json
│   └── src/lib.rs
├── sidecar/
│   ├── package.json
│   ├── index.js
│   └── rename.js
└── src/
```

## Step-by-Step Setup

### 1. Create the Sidecar Directory

```bash
mkdir sidecar && cd sidecar
npm init -y
npm add @yao-pkg/pkg --save-dev
```

### 2. Write Sidecar Logic

Create `sidecar/index.js`:

```javascript
const command = process.argv[2];
const args = process.argv.slice(3);

switch (command) {
  case 'hello':
    console.log(`Hello ${args[0] || 'World'}!`);
    break;
  case 'add':
    const [a, b] = args.map(Number);
    if (isNaN(a) || isNaN(b)) {
      console.error('Error: Both arguments must be numbers');
      process.exit(1);
    }
    console.log(JSON.stringify({ result: a + b }));
    break;
  default:
    console.error(`Unknown command: ${command}`);
    process.exit(1);
}
```

### 3. Create the Rename Script

Create `sidecar/rename.js`:

```javascript
import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const ext = process.platform === 'win32' ? '.exe' : '';

let targetTriple;
try {
  targetTriple = execSync('rustc --print host-tuple').toString().trim();
} catch {
  const rustInfo = execSync('rustc -vV').toString();
  const match = rustInfo.match(/host: (.+)/);
  targetTriple = match ? match[1] : null;
  if (!targetTriple) {
    console.error('Could not determine Rust target triple');
    process.exit(1);
  }
}

const destDir = path.join('..', 'src-tauri', 'binaries');
if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });

fs.renameSync(`my-sidecar${ext}`, path.join(destDir, `my-sidecar-${targetTriple}${ext}`));
```

### 4. Configure Build Scripts

Update `sidecar/package.json`:

```json
{
  "name": "my-sidecar",
  "type": "module",
  "scripts": {
    "build": "pkg index.js --output my-sidecar --targets node18",
    "postbuild": "node rename.js"
  },
  "devDependencies": {
    "@yao-pkg/pkg": "^5.0.0"
  }
}
```

### 5. Configure Tauri

Add to `src-tauri/tauri.conf.json`:

```json
{
  "bundle": {
    "externalBin": ["binaries/my-sidecar"]
  }
}
```

### 6. Configure Permissions

Update `src-tauri/capabilities/default.json`:

```json
{
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:default",
    {
      "identifier": "shell:allow-execute",
      "allow": [{
        "args": true,
        "name": "binaries/my-sidecar",
        "sidecar": true
      }]
    }
  ]
}
```

**Restrict arguments for security:**

```json
{
  "identifier": "shell:allow-execute",
  "allow": [
    {
      "args": ["hello", { "validator": "\\w+" }],
      "name": "binaries/my-sidecar",
      "sidecar": true
    }
  ]
}
```

## Communication Patterns

### Frontend to Sidecar (TypeScript)

```typescript
import { Command } from '@tauri-apps/plugin-shell';

async function sayHello(name: string): Promise<string> {
  const command = Command.sidecar('binaries/my-sidecar', ['hello', name]);
  const output = await command.execute();
  if (output.code !== 0) throw new Error(output.stderr);
  return output.stdout.trim();
}

async function addNumbers(a: number, b: number): Promise<number> {
  const command = Command.sidecar('binaries/my-sidecar', ['add', String(a), String(b)]);
  const output = await command.execute();
  if (output.code !== 0) throw new Error(output.stderr);
  return JSON.parse(output.stdout).result;
}
```

### Backend to Sidecar (Rust)

```rust
use tauri_plugin_shell::ShellExt;

#[tauri::command]
async fn call_sidecar(
    app: tauri::AppHandle,
    command: String,
    args: Vec<String>,
) -> Result<String, String> {
    let mut sidecar = app.shell().sidecar("my-sidecar").map_err(|e| e.to_string())?;
    sidecar = sidecar.arg(&command);
    for arg in args {
        sidecar = sidecar.arg(&arg);
    }
    let output = sidecar.output().await.map_err(|e| e.to_string())?;
    if output.status.success() {
        String::from_utf8(output.stdout).map_err(|e| e.to_string())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}
```

Register the command:

```rust
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![call_sidecar])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Streaming Output

```typescript
import { Command } from '@tauri-apps/plugin-shell';

async function runWithStreaming(args: string[]): Promise<void> {
  const command = Command.sidecar('binaries/my-sidecar', args);
  command.on('close', (data) => console.log(`Finished: ${data.code}`));
  command.on('error', (error) => console.error(`Error: ${error}`));
  command.stdout.on('data', (line) => console.log(`stdout: ${line}`));
  command.stderr.on('data', (line) => console.error(`stderr: ${line}`));
  await command.spawn();
}
```

## Long-Running HTTP Sidecar

For persistent processes, use HTTP:

`sidecar/index.js`:

```javascript
import http from 'http';

const PORT = process.env.SIDECAR_PORT || 3333;

const server = http.createServer((req, res) => {
  let body = '';
  req.on('data', (chunk) => (body += chunk));
  req.on('end', () => {
    res.setHeader('Content-Type', 'application/json');
    try {
      const data = body ? JSON.parse(body) : {};
      if (req.url === '/hello') {
        res.end(JSON.stringify({ message: `Hello ${data.name || 'World'}!` }));
      } else if (req.url === '/health') {
        res.end(JSON.stringify({ status: 'ok' }));
      } else {
        res.statusCode = 404;
        res.end(JSON.stringify({ error: 'Not found' }));
      }
    } catch (err) {
      res.statusCode = 400;
      res.end(JSON.stringify({ error: err.message }));
    }
  });
});

server.listen(PORT, '127.0.0.1', () => console.log(`Listening on ${PORT}`));
process.on('SIGTERM', () => server.close(() => process.exit(0)));
```

Frontend communication:

```typescript
import { Command } from '@tauri-apps/plugin-shell';
import { fetch } from '@tauri-apps/plugin-http';

let sidecarProcess: any = null;
const PORT = 3333;

async function startSidecar(): Promise<void> {
  if (sidecarProcess) return;
  const command = Command.sidecar('binaries/my-sidecar', [], {
    env: { SIDECAR_PORT: String(PORT) },
  });
  sidecarProcess = await command.spawn();
  for (let i = 0; i < 10; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${PORT}/health`);
      if (res.ok) return;
    } catch {
      await new Promise((r) => setTimeout(r, 100));
    }
  }
  throw new Error('Sidecar failed to start');
}

async function callSidecar(endpoint: string, data?: object): Promise<any> {
  const res = await fetch(`http://127.0.0.1:${PORT}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: data ? JSON.stringify(data) : undefined,
  });
  return res.json();
}

async function stopSidecar(): Promise<void> {
  if (sidecarProcess) {
    await sidecarProcess.kill();
    sidecarProcess = null;
  }
}
```

## Building for Production

Update root `package.json`:

```json
{
  "scripts": {
    "build:sidecar": "cd sidecar && npm run build",
    "dev": "npm run build:sidecar && tauri dev",
    "build": "npm run build:sidecar && tauri build"
  }
}
```

Cross-platform targets:

| Platform | pkg Target | Rust Triple |
|----------|------------|-------------|
| Windows x64 | `node18-win-x64` | `x86_64-pc-windows-msvc` |
| macOS x64 | `node18-macos-x64` | `x86_64-apple-darwin` |
| macOS ARM | `node18-macos-arm64` | `aarch64-apple-darwin` |
| Linux x64 | `node18-linux-x64` | `x86_64-unknown-linux-gnu` |

## Security

1. Use validators instead of `"args": true`
2. Bind HTTP servers to `127.0.0.1` only
3. Validate input in both Tauri and sidecar
4. Ensure sidecars terminate when the app closes

## Troubleshooting

**Binary not found:** Check target triple matches:
```bash
ls -la src-tauri/binaries/
rustc --print host-tuple
```

**Permission denied (Unix):**
```bash
chmod +x src-tauri/binaries/my-sidecar-*
```

**Silent crashes:** Check stderr:
```typescript
const output = await command.execute();
if (output.code !== 0) console.error(output.stderr);
```
