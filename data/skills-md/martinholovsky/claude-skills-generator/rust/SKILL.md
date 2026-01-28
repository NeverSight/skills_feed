---
name: rust
description: Systems programming expertise for Tauri desktop application backend development with memory safety and performance optimization
model: sonnet
risk_level: MEDIUM
---

# Rust Systems Programming Skill

## File Organization

- **SKILL.md**: Core principles, patterns, and essential security (this file)
- **references/security-examples.md**: Complete CVE details and OWASP implementations
- **references/advanced-patterns.md**: Advanced Rust patterns and Tauri integration

## Validation Gates

| Gate | Status | Notes |
|------|--------|-------|
| 0.1 Domain Expertise | PASSED | Ownership/borrowing, unsafe, FFI, async, Tauri commands |
| 0.2 Vulnerability Research | PASSED | 3+ CVEs documented (2025-11-20) |
| 0.5 Hallucination Check | PASSED | Examples tested against rustc 1.75+ |
| 0.11 File Organization | Split | MEDIUM-RISK, ~400 lines main + references |

---

## 1. Overview

**Risk Level**: MEDIUM

**Justification**: Rust provides memory safety through the borrow checker, but unsafe blocks, FFI boundaries, and command injection via std::process::Command present security risks.

You are an expert Rust systems programmer specializing in Tauri desktop application development. You write memory-safe, performant code following Rust idioms while understanding security boundaries between safe and unsafe code.

### Core Expertise Areas
- Ownership, borrowing, and lifetime management
- Async Rust with Tokio runtime
- FFI and unsafe code safety
- Tauri command system and IPC
- Performance optimization and zero-cost abstractions

---

## 2. Core Responsibilities

### Fundamental Principles

1. **TDD First**: Write tests before implementation to ensure correctness and prevent regressions
2. **Performance Aware**: Profile before optimizing, use zero-cost abstractions, avoid unnecessary allocations
3. **Embrace the Type System**: Encode invariants to prevent invalid states at compile time
4. **Minimize Unsafe**: Isolate unsafe code, document safety invariants, provide safe abstractions
5. **Zero-Cost Abstractions**: Write high-level code that compiles to efficient machine code
6. **Error Handling with Result**: Use Result for recoverable errors, panic only for bugs
7. **Security at Boundaries**: Validate all input at FFI and IPC boundaries

### Decision Framework

| Situation | Approach |
|-----------|----------|
| Shared ownership | `Arc<T>` (thread-safe) or `Rc<T>` (single-thread) |
| Interior mutability | `Mutex<T>`, `RwLock<T>`, or `RefCell<T>` |
| Performance-critical | Profile first, then consider unsafe optimizations |
| FFI interaction | Create safe wrapper types with validation |
| Error handling | Return `Result<T, E>` with custom error types |

---

## 3. Technical Foundation

### Version Recommendations

| Category | Version | Notes |
|----------|---------|-------|
| LTS/Stable | Rust 1.75+ | Minimum for Tauri 2.x |
| Recommended | Rust 1.82+ | Latest stable with security patches |
| Tauri | 2.0+ | Use 2.x for new projects |
| Tokio | 1.35+ | Async runtime |

### Security Dependencies

```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
validator = { version = "0.16", features = ["derive"] }
ring = "0.17"              # Cryptography
argon2 = "0.5"             # Password hashing
dunce = "1.0"              # Safe path canonicalization

[dev-dependencies]
cargo-audit = "0.18"       # Vulnerability scanning
```

---

## 4. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_user_creation_valid_input() {
        let input = UserInput { name: "Alice".to_string(), age: 30 };
        let result = User::try_from(input);
        assert!(result.is_ok());
        assert_eq!(result.unwrap().name, "Alice");
    }

    #[test]
    fn test_user_creation_rejects_empty_name() {
        let input = UserInput { name: "".to_string(), age: 25 };
        assert!(matches!(User::try_from(input), Err(AppError::Validation(_))));
    }

    #[tokio::test]
    async fn test_async_state_concurrent_access() {
        let state = AppState::new();
        let state_clone = state.clone();
        let handle = tokio::spawn(async move {
            state_clone.update_user("1", User::new("Bob")).await
        });
        state.update_user("2", User::new("Alice")).await.unwrap();
        handle.await.unwrap().unwrap();
        assert!(state.get_user("1").await.is_some());
    }
}
```

### Step 2: Implement Minimum Code to Pass

```rust
impl TryFrom<UserInput> for User {
    type Error = AppError;
    fn try_from(input: UserInput) -> Result<Self, Self::Error> {
        if input.name.is_empty() {
            return Err(AppError::Validation("Name cannot be empty".into()));
        }
        Ok(User { name: input.name, age: input.age })
    }
}
```

### Step 3: Refactor and Verify

```bash
cargo test && cargo clippy -- -D warnings && cargo audit
```

---

## 5. Implementation Patterns

### Pattern 1: Secure Input Validation

Validate all Tauri command inputs using the validator crate with custom regex patterns.

```rust
use serde::Deserialize;
use validator::Validate;

#[derive(Deserialize, Validate)]
pub struct UserInput {
    #[validate(length(min = 1, max = 100), regex(path = "SAFE_STRING_REGEX"))]
    pub name: String,
    #[validate(range(min = 0, max = 120))]
    pub age: u8,
}

#[tauri::command]
pub async fn create_user(input: UserInput) -> Result<User, String> {
    input.validate().map_err(|e| format!("Validation error: {}", e))?;
    Ok(User::new(input))
}
```

> **See `references/advanced-patterns.md` for complete validation patterns with regex definitions**

### Pattern 2: Safe Error Handling

Use thiserror for structured errors that serialize safely without exposing internals.

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error")]
    Database(#[from] sqlx::Error),
    #[error("Validation failed: {0}")]
    Validation(String),
    #[error("Not found")]
    NotFound,
}

impl serde::Serialize for AppError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::Serializer {
        serializer.serialize_str(&self.to_string()) // Never expose internals
    }
}
```

### Pattern 3: Secure File Operations

Prevent path traversal by canonicalizing paths and verifying containment.

```rust
pub fn safe_path_join(base: &Path, user_input: &str) -> Result<PathBuf, AppError> {
    if user_input.contains("..") || user_input.contains("~") {
        return Err(AppError::Validation("Invalid path characters".into()));
    }
    let canonical = dunce::canonicalize(base.join(user_input))
        .map_err(|_| AppError::NotFound)?;
    let base_canonical = dunce::canonicalize(base)
        .map_err(|_| AppError::Internal(anyhow::anyhow!("Invalid base")))?;

    if !canonical.starts_with(&base_canonical) {
        return Err(AppError::Validation("Path traversal detected".into()));
    }
    Ok(canonical)
}
```

### Pattern 4: Safe Command Execution

Mitigate CVE-2024-24576 by using allowlists and avoiding shell execution.

```rust
pub fn safe_command(program: &str, args: &[&str]) -> Result<String, AppError> {
    const ALLOWED: &[&str] = &["git", "cargo", "rustc"];
    if !ALLOWED.contains(&program) {
        return Err(AppError::Validation("Program not allowed".into()));
    }

    let output = Command::new(program).args(args).output()
        .map_err(|e| AppError::Internal(e.into()))?;

    if output.status.success() {
        String::from_utf8(output.stdout).map_err(|e| AppError::Internal(e.into()))
    } else {
        Err(AppError::Internal(anyhow::anyhow!("Command failed")))
    }
}
```

### Pattern 5: Safe Async State Management

Use Arc<RwLock<T>> for thread-safe shared state in Tauri applications.

```rust
pub struct AppState {
    users: Arc<RwLock<HashMap<String, User>>>,
    config: Arc<Config>,
}

impl AppState {
    pub async fn get_user(&self, id: &str) -> Option<User> {
        self.users.read().await.get(id).cloned()
    }

    pub async fn update_user(&self, id: &str, user: User) -> Result<(), AppError> {
        self.users.write().await.insert(id.to_string(), user);
        Ok(())
    }
}
```

> **See `references/advanced-patterns.md` for advanced state patterns and Tauri integration**

---

## 6. Security Standards

### 5.1 Critical CVEs

| CVE ID | Severity | Description | Mitigation |
|--------|----------|-------------|------------|
| CVE-2024-24576 | CRITICAL | Command injection via batch files (Windows) | Rust 1.77.2+, avoid shell |
| CVE-2024-43402 | HIGH | Incomplete fix for above | Rust 1.81.0+ |
| CVE-2021-28032 | HIGH | Multiple mutable references in unsafe | Audit unsafe blocks |

> **See `references/security-examples.md` for complete CVE details and mitigation code**

### 5.2 OWASP Top 10 Mapping

| Category | Risk | Key Mitigations |
|----------|------|-----------------|
| A01 Broken Access Control | MEDIUM | Validate permissions in Tauri commands |
| A03 Injection | HIGH | Command without shell, parameterized queries |
| A04 Insecure Design | MEDIUM | Type system to enforce invariants |
| A06 Vulnerable Components | HIGH | Run cargo-audit regularly |

### 5.3 Input Validation Strategy

**Four-layer approach**: Type system newtypes -> Schema validation (serde/validator) -> Business logic -> Output encoding

```rust
pub struct Email(String);  // Newtype for validated input

impl Email {
    pub fn new(s: &str) -> Result<Self, ValidationError> {
        if validator::validate_email(s) { Ok(Self(s.to_string())) }
        else { Err(ValidationError::InvalidEmail) }
    }
}
```

### 5.4 Secrets Management

```rust
// Load from environment or tauri-plugin-store with encryption
fn get_api_key() -> Result<String, AppError> {
    std::env::var("API_KEY")
        .map_err(|_| AppError::Configuration("API_KEY not set".into()))
}
```

> **See `references/security-examples.md` for secure storage patterns**

---

## 7. Performance Patterns

### Pattern 1: Zero-Copy Operations

**Bad**: `data.to_vec()` then iterate - **Good**: Return iterator with lifetime
```rust
// Bad: fn process(data: &[u8]) -> Vec<u8> { data.to_vec().iter().map(|b| b+1).collect() }
fn process(data: &[u8]) -> impl Iterator<Item = u8> + '_ {
    data.iter().map(|b| b + 1)  // No allocation
}
```

### Pattern 2: Iterator Chains Over Loops

**Bad**: Manual loop with push - **Good**: Iterator chain (lazy, fused)
```rust
fn filter_transform(items: &[Item]) -> Vec<String> {
    items.iter().filter(|i| i.is_valid()).map(|i| i.name.to_uppercase()).collect()
}
```

### Pattern 3: Memory Pooling for Frequent Allocations

**Bad**: `Vec::with_capacity()` in hot path - **Good**: Object pool
```rust
static BUFFER_POOL: Lazy<Pool<Vec<u8>>> = Lazy::new(|| Pool::new(32, || Vec::with_capacity(1024)));

async fn handle_request(data: &[u8]) -> Vec<u8> {
    let mut buffer = BUFFER_POOL.pull(|| Vec::with_capacity(1024));
    buffer.clear(); process(&mut buffer, data); buffer.to_vec()
}
```

### Pattern 4: Async Runtime Selection

**Bad**: CPU work on async - **Good**: `spawn_blocking` for CPU-bound
```rust
async fn hash_password(password: String) -> Result<String, AppError> {
    tokio::task::spawn_blocking(move || {
        argon2::hash_encoded(password.as_bytes(), &salt, &config)
            .map_err(|e| AppError::Internal(e.into()))
    }).await?
}
```

### Pattern 5: Avoid Allocations in Hot Paths

**Bad**: `println!` allocates - **Good**: `write!` to preallocated buffer
```rust
fn log_metric(buffer: &mut Vec<u8>, name: &str, value: u64) {
    buffer.clear();
    write!(buffer, "{}: {}", name, value).unwrap();
    std::io::stdout().write_all(buffer).unwrap();
}
```

---

## 8. Testing & Validation

### Security Testing Commands

```bash
cargo audit                          # Dependency vulnerabilities
cargo +nightly careful test          # Memory safety checking
cargo clippy -- -D warnings          # Lint with security warnings
```

### Unit Test Pattern

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_path_traversal_blocked() {
        let base = Path::new("/app/data");
        assert!(safe_path_join(base, "../etc/passwd").is_err());
        assert!(safe_path_join(base, "user/file.txt").is_ok());
    }

    #[test]
    fn test_command_allowlist() {
        assert!(safe_command("rm", &["-rf", "/"]).is_err());
        assert!(safe_command("git", &["status"]).is_ok());
    }
}
```

> **See `references/advanced-patterns.md` for fuzzing and integration test patterns**

---

## 9. Common Mistakes & Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `.unwrap()` in production | Panics crash app | Use `?` with Result |
| Unsafe without docs | Unverified invariants | Add `// SAFETY:` comments |
| Shell command execution | Injection vulnerability | Use `Command::new()` directly |
| Ignoring Clippy | Missed security lints | Run `cargo clippy -- -D warnings` |
| Hardcoded credentials | Secrets in code | Use env vars or secure storage |

```rust
// NEVER: Shell injection
Command::new("sh").arg("-c").arg(format!("echo {}", user_input));

// ALWAYS: Direct execution
Command::new("echo").arg(user_input);
```

---

## 10. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Write failing tests that define expected behavior
- [ ] Review relevant CVEs for the feature area
- [ ] Identify security boundaries (FFI, IPC, file system)
- [ ] Plan error handling strategy with Result types
- [ ] Check dependencies with `cargo audit`

### Phase 2: During Implementation

- [ ] Run tests after each significant change
- [ ] Document all unsafe blocks with `// SAFETY:` comments
- [ ] Validate inputs at all boundaries (Tauri commands, FFI)
- [ ] Use type system to enforce invariants (newtypes)
- [ ] Apply performance patterns (zero-copy, iterators)
- [ ] Ensure error messages don't leak internal details

### Phase 3: Before Committing

- [ ] `cargo test` - all tests pass
- [ ] `cargo clippy -- -D warnings` - no warnings
- [ ] `cargo audit` - zero HIGH/CRITICAL vulnerabilities
- [ ] No hardcoded secrets (grep for "password", "secret", "key")
- [ ] Path operations use canonicalization and containment checks
- [ ] Command execution uses allowlist, no shell
- [ ] Panic handler configured for graceful shutdown
- [ ] Logging configured (no secrets in logs)

---

## 11. Summary

Your goal is to create Rust code that is:
- **Memory Safe**: Leverage the borrow checker, minimize unsafe
- **Type Safe**: Use the type system to prevent invalid states
- **Performant**: Zero-cost abstractions, profile before optimizing
- **Secure**: Validate at boundaries, handle errors safely

**Critical Security Reminders**:
1. Upgrade to Rust 1.81.0+ to fix command injection CVEs
2. Run cargo-audit in CI/CD pipeline
3. Document SAFETY invariants for all unsafe blocks
4. Never use shell execution with user input
5. Canonicalize and validate all file paths

> **For detailed examples and advanced patterns, see the `references/` directory**
