---
name: embedding-tauri-sidecars
description: Teaches the assistant how to embed and execute external binaries (sidecars) in Tauri applications, including configuration, cross-platform executable naming, and Rust/JavaScript APIs for spawning sidecar processes.
---

# Tauri Sidecars: Embedding External Binaries

This skill covers embedding and executing external binaries (sidecars) in Tauri applications, including configuration, cross-platform considerations, and execution from Rust and JavaScript.

## Overview

Sidecars are external binaries embedded within Tauri applications to extend functionality or eliminate the need for users to install dependencies. They can be executables written in any programming language.

**Common Use Cases:**
- Python CLI applications packaged with PyInstaller
- Go or Rust compiled binaries for specific tasks
- Node.js applications bundled as executables
- API servers or background services

## Plugin Dependency

Sidecars require the shell plugin:

**Cargo.toml:**
```toml
[dependencies]
tauri-plugin-shell = "2"
```

**Register in main.rs:**
```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Frontend package:**
```bash
npm install @tauri-apps/plugin-shell
```

## Configuration

### Registering Sidecars

Configure sidecars in `tauri.conf.json` under `bundle.externalBin`. Paths are relative to `src-tauri`:

```json
{
  "bundle": {
    "externalBin": [
      "binaries/my-sidecar",
      "../external/processor"
    ]
  }
}
```

**Important:** The path is a stem. Tauri appends the target triple suffix at build time.

### Cross-Platform Binary Naming

Each sidecar requires platform-specific variants with target triple suffixes:

| Platform | Architecture | Required Filename |
|----------|--------------|-------------------|
| Linux | x86_64 | `my-sidecar-x86_64-unknown-linux-gnu` |
| Linux | ARM64 | `my-sidecar-aarch64-unknown-linux-gnu` |
| macOS | Intel | `my-sidecar-x86_64-apple-darwin` |
| macOS | Apple Silicon | `my-sidecar-aarch64-apple-darwin` |
| Windows | x86_64 | `my-sidecar-x86_64-pc-windows-msvc.exe` |

**Determine your target triple:**
```bash
rustc --print host-tuple    # Rust 1.84.0+
rustc -Vv | grep host       # Older versions
```

### Directory Structure

```
src-tauri/
  binaries/
    my-sidecar-x86_64-unknown-linux-gnu
    my-sidecar-aarch64-apple-darwin
    my-sidecar-x86_64-apple-darwin
    my-sidecar-x86_64-pc-windows-msvc.exe
  tauri.conf.json
  src/main.rs
```

## Executing Sidecars from Rust

### Basic Execution

```rust
use tauri_plugin_shell::ShellExt;

#[tauri::command]
async fn run_sidecar(app: tauri::AppHandle) -> Result<String, String> {
    let output = app
        .shell()
        .sidecar("my-sidecar")
        .map_err(|e| e.to_string())?
        .output()
        .await
        .map_err(|e| e.to_string())?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}
```

**Note:** Pass only the filename to `sidecar()`, not the full path from configuration.

### With Arguments

```rust
#[tauri::command]
async fn process_file(app: tauri::AppHandle, file_path: String) -> Result<String, String> {
    let output = app
        .shell()
        .sidecar("processor")
        .map_err(|e| e.to_string())?
        .args(["--input", &file_path, "--format", "json"])
        .output()
        .await
        .map_err(|e| e.to_string())?;

    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}
```

### Spawning Long-Running Processes

For sidecars that run continuously (API servers, watchers):

```rust
use tauri_plugin_shell::{ShellExt, process::CommandEvent};

#[tauri::command]
async fn start_server(app: tauri::AppHandle) -> Result<u32, String> {
    let (mut rx, child) = app
        .shell()
        .sidecar("api-server")
        .map_err(|e| e.to_string())?
        .args(["--port", "8080"])
        .spawn()
        .map_err(|e| e.to_string())?;

    let pid = child.pid();

    tauri::async_runtime::spawn(async move {
        while let Some(event) = rx.recv().await {
            match event {
                CommandEvent::Stdout(line) => println!("{}", String::from_utf8_lossy(&line)),
                CommandEvent::Stderr(line) => eprintln!("{}", String::from_utf8_lossy(&line)),
                CommandEvent::Terminated(payload) => {
                    println!("Terminated: {:?}", payload.code);
                    break;
                }
                _ => {}
            }
        }
    });

    Ok(pid)
}
```

### Managing Sidecar Lifecycle

```rust
use std::sync::Mutex;
use tauri::State;
use tauri_plugin_shell::{ShellExt, process::CommandChild};

struct SidecarState {
    child: Mutex<Option<CommandChild>>,
}

#[tauri::command]
async fn start_sidecar(app: tauri::AppHandle, state: State<'_, SidecarState>) -> Result<(), String> {
    let (_, child) = app.shell().sidecar("service").map_err(|e| e.to_string())?
        .spawn().map_err(|e| e.to_string())?;
    *state.child.lock().unwrap() = Some(child);
    Ok(())
}

#[tauri::command]
async fn stop_sidecar(state: State<'_, SidecarState>) -> Result<(), String> {
    if let Some(child) = state.child.lock().unwrap().take() {
        child.kill().map_err(|e| e.to_string())?;
    }
    Ok(())
}
```

## Executing Sidecars from JavaScript

### Permission Configuration

Grant shell execution permissions in `src-tauri/capabilities/default.json`:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:default",
    {
      "identifier": "shell:allow-execute",
      "allow": [{ "name": "binaries/my-sidecar", "sidecar": true }]
    }
  ]
}
```

### Basic Execution

```typescript
import { Command } from '@tauri-apps/plugin-shell';

async function runSidecar(): Promise<string> {
  const command = Command.sidecar('binaries/my-sidecar');
  const output = await command.execute();
  if (output.code === 0) return output.stdout;
  throw new Error(output.stderr);
}
```

### With Arguments

```typescript
async function processFile(filePath: string): Promise<string> {
  const command = Command.sidecar('binaries/processor', [
    '--input', filePath, '--format', 'json'
  ]);
  const output = await command.execute();
  return output.stdout;
}
```

### Handling Streaming Output

```typescript
import { Command, Child } from '@tauri-apps/plugin-shell';

async function runWithStreaming(): Promise<Child> {
  const command = Command.sidecar('binaries/long-task');

  command.on('close', (data) => console.log(`Finished: ${data.code}`));
  command.on('error', (error) => console.error(error));
  command.stdout.on('data', (line) => console.log(line));
  command.stderr.on('data', (line) => console.error(line));

  return await command.spawn();
}
```

### Managing Long-Running Processes

```typescript
let serverProcess: Child | null = null;

async function startServer(): Promise<number> {
  const command = Command.sidecar('binaries/api-server', ['--port', '8080']);
  command.stdout.on('data', console.log);
  serverProcess = await command.spawn();
  return serverProcess.pid;
}

async function stopServer(): Promise<void> {
  if (serverProcess) {
    await serverProcess.kill();
    serverProcess = null;
  }
}
```

## Argument Validation

Configure argument validation in capabilities:

```json
{
  "identifier": "shell:allow-execute",
  "allow": [{
    "name": "binaries/my-sidecar",
    "sidecar": true,
    "args": [
      "-o",
      "--verbose",
      { "validator": "\\S+" }
    ]
  }]
}
```

**Argument types:**
- **Static string**: Exact match required (`-o`, `--verbose`)
- **Validator object**: Regex pattern for dynamic values
- **`true`**: Allow any argument (use with caution)

## Cross-Platform Considerations

### Building Platform-Specific Binaries

**Rust sidecars:**
```bash
cargo build --release --target x86_64-unknown-linux-gnu
cp target/x86_64-unknown-linux-gnu/release/my-tool \
   src-tauri/binaries/my-tool-x86_64-unknown-linux-gnu
```

**Python with PyInstaller:**
```bash
pyinstaller --onefile my_script.py
mv dist/my_script dist/my_script-x86_64-unknown-linux-gnu
```

### Platform Notes

**Windows:**
- Executables must have `.exe` extension
- Handle line endings in text file processing

**macOS:**
- Use `lipo` for universal binaries (Intel + Apple Silicon)
- Code signing may be required for distribution
- Gatekeeper may block unsigned sidecars

**Linux:**
- Mark binaries as executable (`chmod +x`)
- Consider glibc version compatibility
- Static linking reduces dependency issues

## Complete Example

**tauri.conf.json:**
```json
{
  "productName": "My App",
  "version": "1.0.0",
  "identifier": "com.example.myapp",
  "bundle": {
    "externalBin": ["binaries/data-processor"]
  }
}
```

**capabilities/default.json:**
```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:default",
    {
      "identifier": "shell:allow-execute",
      "allow": [{
        "name": "binaries/data-processor",
        "sidecar": true,
        "args": [
          "--input", { "validator": "^[a-zA-Z0-9_\\-./]+$" },
          "--output", { "validator": "^[a-zA-Z0-9_\\-./]+$" }
        ]
      }]
    }
  ]
}
```

**src/main.rs:**
```rust
use tauri_plugin_shell::ShellExt;

#[tauri::command]
async fn process_data(app: tauri::AppHandle, input: String, output: String) -> Result<String, String> {
    let result = app.shell().sidecar("data-processor").map_err(|e| e.to_string())?
        .args(["--input", &input, "--output", &output])
        .output().await.map_err(|e| e.to_string())?;

    if result.status.success() {
        Ok(String::from_utf8_lossy(&result.stdout).to_string())
    } else {
        Err(String::from_utf8_lossy(&result.stderr).to_string())
    }
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![process_data])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Frontend (App.tsx):**
```tsx
import { invoke } from '@tauri-apps/api/core';

function App() {
  const handleProcess = async () => {
    try {
      const result = await invoke('process_data', {
        input: '/path/to/input.txt',
        output: '/path/to/output.txt'
      });
      console.log('Result:', result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return <button onClick={handleProcess}>Process Data</button>;
}
```

## Best Practices

1. **Validate all sidecar paths**: Never pass untrusted paths to sidecars
2. **Use argument validators**: Restrict allowed arguments in capabilities
3. **Handle errors gracefully**: Sidecars may fail or be missing
4. **Clean up processes**: Kill spawned processes on app exit
5. **Test on all platforms**: Binary naming and execution varies
6. **Consider binary size**: Sidecars increase bundle size significantly
