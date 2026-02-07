---
name: calling-rust-from-tauri-frontend
description: Guides the user through calling Rust backend functions from the Tauri frontend using the invoke function, defining commands with the #[tauri::command] attribute, passing arguments, returning values, handling errors, and implementing async IPC communication.
---

# Calling Rust from Tauri Frontend

This skill covers how to call Rust backend functions from your Tauri v2 frontend using the command system and invoke function.

## Overview

Tauri provides two IPC mechanisms:
- **Commands** (recommended): Type-safe function calls with serialized arguments/return values
- **Events**: Dynamic, one-way communication (not covered here)

## Basic Commands

### Defining a Command in Rust

Use the `#[tauri::command]` attribute macro:

```rust
// src-tauri/src/lib.rs
#[tauri::command]
fn greet(name: String) -> String {
    format!("Hello, {}!", name)
}
```

### Registering Commands

Commands must be registered with the invoke handler:

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, login, fetch_data])
        .run(tauri::generate_context!())
        .expect("error while running tauri application")
}
```

### Invoking from JavaScript/TypeScript

```typescript
import { invoke } from '@tauri-apps/api/core';

const greeting = await invoke('greet', { name: 'World' });
console.log(greeting); // "Hello, World!"
```

Or with the global Tauri object (when `app.withGlobalTauri` is enabled):

```javascript
const { invoke } = window.__TAURI__.core;
const greeting = await invoke('greet', { name: 'World' });
```

## Passing Arguments

### Argument Naming Convention

By default, Rust snake_case arguments map to JavaScript camelCase:

```rust
#[tauri::command]
fn create_user(user_name: String, user_age: u32) -> String {
    format!("{} is {} years old", user_name, user_age)
}
```

```typescript
await invoke('create_user', { userName: 'Alice', userAge: 30 });
```

Use `rename_all` to change the naming convention:

```rust
#[tauri::command(rename_all = "snake_case")]
fn create_user(user_name: String, user_age: u32) -> String {
    format!("{} is {} years old", user_name, user_age)
}
```

### Complex Arguments

Arguments must implement `serde::Deserialize`:

```rust
use serde::Deserialize;

#[derive(Deserialize)]
struct UserData {
    name: String,
    email: String,
    age: u32,
}

#[tauri::command]
fn register_user(user: UserData) -> String {
    format!("Registered {} ({}) age {}", user.name, user.email, user.age)
}
```

```typescript
await invoke('register_user', {
    user: { name: 'Alice', email: 'alice@example.com', age: 30 }
});
```

## Returning Values

### Simple Return Types

Return types must implement `serde::Serialize`:

```rust
#[tauri::command]
fn get_count() -> i32 { 42 }

#[tauri::command]
fn get_message() -> String { "Hello from Rust!".into() }
```

```typescript
const count: number = await invoke('get_count');
const message: string = await invoke('get_message');
```

### Returning Complex Types

```rust
use serde::Serialize;

#[derive(Serialize)]
struct AppConfig {
    theme: String,
    language: String,
    notifications_enabled: bool,
}

#[tauri::command]
fn get_config() -> AppConfig {
    AppConfig {
        theme: "dark".into(),
        language: "en".into(),
        notifications_enabled: true,
    }
}
```

```typescript
interface AppConfig {
    theme: string;
    language: string;
    notificationsEnabled: boolean;
}
const config: AppConfig = await invoke('get_config');
```

### Returning Binary Data

For large binary data, use `tauri::ipc::Response` to bypass JSON serialization:

```rust
use tauri::ipc::Response;

#[tauri::command]
fn read_file(path: String) -> Response {
    let data = std::fs::read(&path).unwrap();
    Response::new(data)
}
```

```typescript
const data: ArrayBuffer = await invoke('read_file', { path: '/path/to/file' });
```

## Error Handling

### Using Result Types

Return `Result<T, E>` where `E` implements `Serialize` or is a `String`:

```rust
#[tauri::command]
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Cannot divide by zero".into())
    } else {
        Ok(a / b)
    }
}
```

```typescript
try {
    const result = await invoke('divide', { a: 10, b: 0 });
} catch (error) {
    console.error('Error:', error); // "Cannot divide by zero"
}
```

### Custom Error Types with thiserror

```rust
use serde::Serialize;
use thiserror::Error;

#[derive(Debug, Error)]
enum AppError {
    #[error("File not found: {0}")]
    FileNotFound(String),
    #[error("Permission denied")]
    PermissionDenied,
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

impl Serialize for AppError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::ser::Serializer {
        serializer.serialize_str(self.to_string().as_ref())
    }
}

#[tauri::command]
fn open_file(path: String) -> Result<String, AppError> {
    if !std::path::Path::new(&path).exists() {
        return Err(AppError::FileNotFound(path));
    }
    let content = std::fs::read_to_string(&path)?;
    Ok(content)
}
```

### Structured Error Responses

```rust
use serde::Serialize;

#[derive(Debug, Serialize)]
struct ErrorResponse { code: String, message: String }

#[tauri::command]
fn validate_input(input: String) -> Result<String, ErrorResponse> {
    if input.is_empty() {
        return Err(ErrorResponse {
            code: "EMPTY_INPUT".into(),
            message: "Input cannot be empty".into(),
        });
    }
    Ok(input.to_uppercase())
}
```

```typescript
interface ErrorResponse { code: string; message: string; }

try {
    const result = await invoke('validate_input', { input: '' });
} catch (error) {
    const err = error as ErrorResponse;
    console.error(`Error ${err.code}: ${err.message}`);
}
```

## Async Commands

### Defining Async Commands

Use the `async` keyword:

```rust
#[tauri::command]
async fn fetch_data(url: String) -> Result<String, String> {
    let response = reqwest::get(&url).await.map_err(|e| e.to_string())?;
    let body = response.text().await.map_err(|e| e.to_string())?;
    Ok(body)
}
```

### Async with Borrowed Types Limitation

Async commands cannot use borrowed types like `&str` directly:

```rust
// Will NOT compile:
// async fn bad_command(value: &str) -> String { ... }

// Use owned types instead:
#[tauri::command]
async fn good_command(value: String) -> String {
    some_async_operation(&value).await;
    value
}

// Or wrap in Result as workaround:
#[tauri::command]
async fn with_borrowed(value: &str) -> Result<String, ()> {
    some_async_operation(value).await;
    Ok(value.to_string())
}
```

### Frontend Invocation

Async commands work identically to sync since `invoke` returns a Promise:

```typescript
const result = await invoke('fetch_data', { url: 'https://api.example.com/data' });
```

## Accessing Tauri Internals

### WebviewWindow, AppHandle, and State

```rust
use std::sync::Mutex;

struct AppState { counter: Mutex<i32> }

#[tauri::command]
async fn get_window_label(window: tauri::WebviewWindow) -> String {
    window.label().to_string()
}

#[tauri::command]
async fn get_app_version(app: tauri::AppHandle) -> String {
    app.package_info().version.to_string()
}

#[tauri::command]
fn increment_counter(state: tauri::State<AppState>) -> i32 {
    let mut counter = state.counter.lock().unwrap();
    *counter += 1;
    *counter
}

pub fn run() {
    tauri::Builder::default()
        .manage(AppState { counter: Mutex::new(0) })
        .invoke_handler(tauri::generate_handler![
            get_window_label, get_app_version, increment_counter
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application")
}
```

## Advanced Features

### Raw Request Access

Access headers and raw body:

```rust
use tauri::ipc::{Request, InvokeBody};

#[tauri::command]
fn upload(request: Request) -> Result<String, String> {
    let InvokeBody::Raw(data) = request.body() else {
        return Err("Expected raw body".into());
    };
    let auth = request.headers()
        .get("Authorization")
        .and_then(|v| v.to_str().ok())
        .ok_or("Missing Authorization header")?;
    Ok(format!("Received {} bytes", data.len()))
}
```

```typescript
const data = new Uint8Array([1, 2, 3, 4, 5]);
await invoke('upload', data, { headers: { Authorization: 'Bearer token123' } });
```

### Channels for Streaming

```rust
use tauri::ipc::Channel;
use tokio::io::AsyncReadExt;

#[tauri::command]
async fn stream_file(path: String, channel: Channel<Vec<u8>>) -> Result<(), String> {
    let mut file = tokio::fs::File::open(&path).await.map_err(|e| e.to_string())?;
    let mut buffer = vec![0u8; 4096];
    loop {
        let len = file.read(&mut buffer).await.map_err(|e| e.to_string())?;
        if len == 0 { break; }
        channel.send(buffer[..len].to_vec()).map_err(|e| e.to_string())?;
    }
    Ok(())
}
```

```typescript
import { Channel } from '@tauri-apps/api/core';

const channel = new Channel<Uint8Array>();
channel.onmessage = (chunk) => console.log('Received:', chunk.length, 'bytes');
await invoke('stream_file', { path: '/path/to/file', channel });
```

## Organizing Commands in Modules

```rust
// src-tauri/src/commands/user.rs
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct CreateUserRequest { pub name: String, pub email: String }

#[derive(Serialize)]
pub struct User { pub id: u32, pub name: String, pub email: String }

#[tauri::command]
pub fn create_user(request: CreateUserRequest) -> User {
    User { id: 1, name: request.name, email: request.email }
}
```

```rust
// src-tauri/src/commands/mod.rs
pub mod user;
```

```rust
// src-tauri/src/lib.rs
mod commands;

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![commands::user::create_user])
        .run(tauri::generate_context!())
        .expect("error while running tauri application")
}
```

## TypeScript Type Safety

Create a typed wrapper:

```typescript
import { invoke } from '@tauri-apps/api/core';

export interface User { id: number; name: string; email: string; }
export interface CreateUserRequest { name: string; email: string; }

export const commands = {
    createUser: (request: CreateUserRequest): Promise<User> =>
        invoke('create_user', { request }),
    greet: (name: string): Promise<string> =>
        invoke('greet', { name }),
};

// Usage
const user = await commands.createUser({ name: 'Bob', email: 'bob@example.com' });
```

## Quick Reference

| Task | Rust | JavaScript |
|------|------|------------|
| Define command | `#[tauri::command] fn name() {}` | - |
| Register command | `tauri::generate_handler![name]` | - |
| Invoke command | - | `await invoke('name', { args })` |
| Return value | `-> T` where T: Serialize | `const result = await invoke(...)` |
| Return error | `-> Result<T, E>` | `try/catch` |
| Async command | `async fn name()` | Same as sync |
| Access window | `window: tauri::WebviewWindow` | - |
| Access app | `app: tauri::AppHandle` | - |
| Access state | `state: tauri::State<T>` | - |

## Key Constraints

1. **Command names must be unique** across the entire application
2. **Commands in `lib.rs` cannot be `pub`** (use modules for organization)
3. **All commands must be registered** in a single `generate_handler!` call
4. **Async commands cannot use borrowed types** like `&str` directly
5. **Arguments must implement `Deserialize`**, return types must implement `Serialize`
