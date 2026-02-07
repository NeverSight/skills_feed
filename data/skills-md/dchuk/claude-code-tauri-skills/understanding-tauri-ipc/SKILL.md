---
name: understanding-tauri-ipc
description: Teaches the assistant about Tauri IPC (Inter-Process Communication) patterns including brownfield and isolation approaches for secure message passing between frontend and Rust backend.
---

# Tauri Inter-Process Communication (IPC)

This skill covers Tauri's IPC system, including the brownfield and isolation patterns for secure communication between frontend and backend processes.

## Overview

Tauri implements Inter-Process Communication using **Asynchronous Message Passing**. This enables isolated processes to exchange serialized requests and responses securely.

**Why Message Passing?**
- Safer than shared memory or direct function access
- Recipients can reject or discard malicious requests
- Tauri Core validates all requests before execution
- Prevents unauthorized function invocation

## IPC Primitives

Tauri provides two IPC primitives:

### Events

- **Direction**: Bidirectional (Frontend <-> Tauri Core)
- **Type**: Fire-and-forget, one-way messaging
- **Best for**: Lifecycle events, state changes, notifications

**Rust (emit to frontend):**
```rust
use tauri::{AppHandle, Emitter};

fn emit_event(app: &AppHandle) {
    app.emit("backend-event", "payload data").unwrap();
}
```

**Frontend (listen):**
```typescript
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen('backend-event', (event) => {
  console.log('Received:', event.payload);
});

// Call unlisten() when done
```

**Frontend (emit to backend):**
```typescript
import { emit } from '@tauri-apps/api/event';

await emit('frontend-event', { data: 'value' });
```

### Commands

- **Direction**: Frontend -> Rust backend
- **Protocol**: JSON-RPC-based abstraction
- **API**: Similar to browser's `fetch()` API
- **Requirement**: Arguments and return data must be JSON-serializable

**Rust command definition:**
```rust
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Frontend invocation:**
```typescript
import { invoke } from '@tauri-apps/api/core';

const greeting = await invoke('greet', { name: 'World' });
console.log(greeting); // "Hello, World!"
```

**Async command with Result:**
```rust
#[tauri::command]
async fn read_file(path: String) -> Result<String, String> {
    std::fs::read_to_string(&path)
        .map_err(|e| e.to_string())
}
```

## IPC Patterns

Tauri provides two IPC security patterns: **Brownfield** (default) and **Isolation**.

---

## Brownfield Pattern

### What It Is

The brownfield pattern is Tauri's **default** IPC approach. It prioritizes compatibility with existing web frontend projects by requiring minimal modifications.

### When to Use

- Migrating existing web applications to desktop
- Rapid prototyping and development
- Applications with trusted frontend code
- Simple applications with limited IPC surface

### Why Use It

- Zero configuration required
- Minimal changes to existing web code
- Direct access to Tauri APIs
- Fastest development path

### Configuration

Brownfield is the default. Explicit configuration is optional:

```json
{
  "app": {
    "security": {
      "pattern": {
        "use": "brownfield"
      }
    }
  }
}
```

**Note:** There are no additional configuration options for brownfield.

### Code Example

**Rust backend:**
```rust
#[tauri::command]
fn process_data(input: String) -> Result<String, String> {
    // Direct processing without isolation layer
    Ok(format!("Processed: {}", input))
}
```

**Frontend:**
```typescript
import { invoke } from '@tauri-apps/api/core';

// Direct invocation - no isolation layer
const result = await invoke('process_data', { input: 'test' });
```

### Security Considerations

- Frontend code has direct access to all exposed commands
- No additional validation layer between frontend and backend
- Supply chain attacks in frontend dependencies could invoke commands
- Rely on command-level validation in Rust

---

## Isolation Pattern

### What It Is

The isolation pattern intercepts and modifies **all** Tauri API messages from the frontend using JavaScript before they reach Tauri Core. A secure JavaScript application (the Isolation application) runs in a sandboxed iframe to validate and encrypt all IPC communications.

### When to Use

- Applications with many frontend dependencies
- High-security requirements
- Handling sensitive data or operations
- Public-facing applications
- When supply chain attacks are a concern

### Why Use It

**Protection against Development Threats:**
- Validates all IPC calls before execution
- Catches malicious or unwanted frontend calls
- Mitigates supply chain attack risks
- Provides a checkpoint for all communications

**Tauri recommends using isolation whenever feasible.**

### How It Works

1. Tauri's IPC handler receives a message from frontend
2. Message routes to the Isolation application (sandboxed iframe)
3. Isolation hook validates and potentially modifies the message
4. Message encrypts using AES-GCM with runtime-generated keys
5. Encrypted message returns to IPC handler
6. Encrypted message passes to Tauri Core for decryption and execution

**Key Security Features:**
- New encryption keys generated on each application launch
- Sandboxed iframe prevents isolation code manipulation
- All IPC calls validated, including event-based APIs

### Configuration

**tauri.conf.json:**
```json
{
  "app": {
    "security": {
      "pattern": {
        "use": "isolation",
        "options": {
          "dir": "../dist-isolation"
        }
      }
    }
  }
}
```

### Code Example

**Directory structure:**
```
project/
  src/           # Main frontend
  src-tauri/     # Rust backend
  dist-isolation/
    index.html
    index.js
```

**dist-isolation/index.html:**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Isolation Secure Script</title>
  </head>
  <body>
    <script src="index.js"></script>
  </body>
</html>
```

**dist-isolation/index.js:**
```javascript
window.__TAURI_ISOLATION_HOOK__ = (payload) => {
  // Log all IPC calls for debugging
  console.log('IPC call intercepted:', payload);

  // Return payload unchanged (passthrough)
  return payload;
};
```

**Validation example (index.js):**
```javascript
window.__TAURI_ISOLATION_HOOK__ = (payload) => {
  // Validate command calls
  if (payload.cmd === 'invoke') {
    const { __tauriModule, message } = payload;

    // Block unauthorized file system access
    if (message.cmd === 'readFile') {
      const path = message.path;
      if (!path.startsWith('/allowed/directory/')) {
        console.error('Blocked unauthorized file access:', path);
        return null; // Block the request
      }
    }

    // Validate specific commands
    if (message.cmd === 'deleteItem') {
      if (!confirm('Are you sure you want to delete this item?')) {
        return null; // User cancelled
      }
    }
  }

  return payload;
};
```

**Comprehensive validation example:**
```javascript
const ALLOWED_COMMANDS = ['greet', 'read_config', 'save_settings'];
const BLOCKED_PATHS = ['/etc/', '/usr/', '/System/'];

window.__TAURI_ISOLATION_HOOK__ = (payload) => {
  // Validate invoke commands
  if (payload.cmd === 'invoke') {
    const commandName = payload.message?.cmd;

    // Whitelist approach
    if (!ALLOWED_COMMANDS.includes(commandName)) {
      console.warn('Blocked unknown command:', commandName);
      return null;
    }

    // Validate path arguments
    const args = payload.message?.args || {};
    if (args.path) {
      for (const blocked of BLOCKED_PATHS) {
        if (args.path.startsWith(blocked)) {
          console.error('Blocked access to protected path:', args.path);
          return null;
        }
      }
    }
  }

  // Validate event emissions
  if (payload.cmd === 'emit') {
    const eventName = payload.event;
    // Add event validation as needed
  }

  return payload;
};
```

### Performance Considerations

- AES-GCM encryption overhead is minimal for most applications
- Comparable to TLS encryption used in HTTPS
- Key generation requires system entropy (handled seamlessly on modern systems)
- Performance-sensitive applications may notice slight impact

### Limitations

- ES Modules do not load in sandboxed iframes on Windows
- Scripts must be inlined during build time
- External files must be embedded rather than referenced
- Avoid bundlers for the isolation application

### Best Practices

1. **Keep it simple**: Minimize isolation application dependencies
2. **No bundlers**: Skip ES Modules and complex build processes
3. **Validate inputs**: Verify IPC calls match expected parameters
4. **Whitelist commands**: Only allow known, safe commands
5. **Log suspicious activity**: Monitor for potential attacks
6. **Apply to events**: Validate events that trigger Rust code

---

## Pattern Comparison

| Aspect | Brownfield | Isolation |
|--------|------------|-----------|
| Default | Yes | No |
| Configuration | None required | Requires isolation app |
| Security | Basic | Enhanced |
| Validation | Command-level only | All IPC calls |
| Encryption | None | AES-GCM |
| Performance | Fastest | Slight overhead |
| Complexity | Simple | Moderate |
| Best for | Trusted code, prototypes | Production, sensitive apps |

## Security Best Practices

### For Both Patterns

1. **Validate all inputs in Rust commands**
   ```rust
   #[tauri::command]
   fn process_file(path: String) -> Result<String, String> {
       // Always validate paths
       if path.contains("..") || path.starts_with("/etc") {
           return Err("Invalid path".into());
       }
       // Process file...
       Ok("Done".into())
   }
   ```

2. **Use typed arguments**
   ```rust
   #[derive(serde::Deserialize)]
   struct CreateUserArgs {
       name: String,
       email: String,
   }

   #[tauri::command]
   fn create_user(args: CreateUserArgs) -> Result<(), String> {
       // Type-safe argument handling
       Ok(())
   }
   ```

3. **Limit exposed commands**: Only expose necessary functionality

4. **Use capability-based permissions**: Configure permissions in `capabilities/`

### For Isolation Pattern

1. **Keep isolation code minimal**: Reduce attack surface
2. **Avoid external dependencies**: No npm packages in isolation app
3. **Use strict validation**: Whitelist over blacklist
4. **Test thoroughly**: Ensure validation catches edge cases

## Choosing a Pattern

**Use Brownfield when:**
- Building internal tools
- Prototyping rapidly
- Frontend code is fully trusted
- Minimal security requirements

**Use Isolation when:**
- Building public applications
- Handling sensitive user data
- Using many third-party frontend packages
- Security is a priority
- Compliance requirements exist

When in doubt, **prefer isolation** for production applications.
