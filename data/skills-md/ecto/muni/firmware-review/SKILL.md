---
name: firmware-review
description: Reviews Rust firmware code for the BVR (Base Vectoring Rover) with focus on safety-critical systems, CAN bus protocol compliance, motor control logic, state machine correctness, and embedded testing patterns. Use when reviewing BVR firmware changes, debugging actuator control, testing motor communication, validating safety mechanisms, checking async patterns, or evaluating control system modifications. Covers watchdog implementation, e-stop handling, rate limiting, VESC motor controller integration, and Tokio async runtime patterns.
allowed-tools: Read, Grep, Glob, Bash(cargo:test), Bash(cargo:check), Bash(cargo:build)
---

# BVR Firmware Code Review Skill

This skill provides comprehensive code review for the BVR (Base Vectoring Rover) firmware, focusing on safety-critical systems, real-time control, and CAN bus communication.

## Overview

The BVR firmware runs on a Jetson Orin NX and controls a four-wheel differential drive rover using VESC motor controllers over CAN bus. The system is safety-critical with multiple layers of protection including watchdogs, e-stop mechanisms, and rate limiting.

**Key Architecture:**
- **Platform**: Jetson Orin NX (aarch64-unknown-linux-gnu)
- **Language**: Rust Edition 2021
- **Runtime**: Tokio async multi-threaded
- **Communication**: SocketCAN (can0 interface at 500kHz)
- **Workspace**: 18 crates in `bvr/firmware/`
- **Main daemon**: bvrd (1191 lines in `bins/bvrd/src/main.rs`)

**Critical Files:**
- State machine: `crates/state/src/lib.rs` (130 lines)
- Control logic: `crates/control/src/lib.rs` (243 lines)
- CAN abstraction: `crates/can/src/lib.rs`
- VESC protocol: `crates/can/src/vesc.rs`
- LED control: `crates/can/src/leds.rs`
- Main daemon: `bins/bvrd/src/main.rs` (1191 lines)
- Configuration: `config/bvr.toml` (152 lines)

## Safety-Critical Review Checklist

### 1. Watchdog Implementation

**Purpose**: Detect communication timeouts and transition to safe state (Idle) when commands stop arriving.

**Location**: `bvr/firmware/crates/control/src/lib.rs:162-193`

**Key Points to Review:**
- [ ] Watchdog initialized with appropriate timeout (default: 500ms)
- [ ] `feed()` called on every valid command reception
- [ ] `is_timed_out()` checked in main control loop
- [ ] Timeout triggers `Event::CommandTimeout` in state machine
- [ ] Watchdog reset on e-stop or mode transitions

**Example Pattern:**
```rust
// Good: Watchdog properly integrated
let mut watchdog = Watchdog::new(Duration::from_millis(500));
loop {
    if let Some(cmd) = recv_command() {
        watchdog.feed();  // Reset timer on command
    }
    if watchdog.is_timed_out() {
        state_machine.handle(Event::CommandTimeout);
        // Motors automatically stop in Idle mode
    }
}
```

**Red Flags:**
- Watchdog created but never checked
- Timeout value too long (>1 second for teleop)
- `feed()` called unconditionally (bypasses timeout detection)
- No transition to safe state on timeout

**See**: [safety-checklist.md](safety-checklist.md) for detailed verification steps.

### 2. E-Stop State Machine

**Purpose**: Immediate safety override from any operational mode, requiring explicit release to resume.

**Location**: `bvr/firmware/crates/state/src/lib.rs:7-130`

**State Machine Modes:**
1. `Disabled` - Initial state, motors off
2. `Idle` - Ready state, motors enabled but no movement
3. `Teleop` - Human control via gamepad/keyboard
4. `Autonomous` - Autonomous navigation
5. `EStop` - Emergency stop, requires release
6. `Fault` - Error state, requires fault clear

**Valid E-Stop Transitions:**
- ANY mode → `EStop` (via `Event::EStop`)
- `EStop` → `Idle` (via `Event::EStopRelease` only)

**Key Points to Review:**
- [ ] `Event::EStop` handled from all active modes (Idle, Teleop, Autonomous)
- [ ] Cannot exit e-stop without explicit `Event::EStopRelease`
- [ ] `force_estop()` method available for critical overrides
- [ ] LED feedback tied to e-stop state (red pulsing at 200ms)
- [ ] Motor commands blocked in e-stop mode
- [ ] State logged at each transition with old/new mode

**Example Pattern:**
```rust
// Good: Proper e-stop handling
match (self.mode, event) {
    (_, Event::EStop) => {
        info!(?self.mode, "E-stop triggered");
        self.mode = Mode::EStop;
        // Motors automatically stopped by is_driving() check
    }
    (Mode::EStop, Event::EStopRelease) => {
        info!("E-stop released, transitioning to Idle");
        self.mode = Mode::Idle;
    }
    (Mode::EStop, Event::Enable) => {
        warn!("Cannot enable directly from e-stop, must release first");
        // No state change - requires explicit release
    }
    // ...
}
```

**Red Flags:**
- Direct transition from e-stop to driving modes without release
- E-stop event not handled in all modes
- State machine allows bypassing e-stop
- Missing logging on e-stop transitions

**See**: [state-machine.md](state-machine.md) for complete transition diagram.

### 3. Rate Limiting and Acceleration Control

**Purpose**: Progressive acceleration/deceleration to prevent wheel slip, mechanical stress, and loss of control.

**Location**: `bvr/firmware/crates/control/src/lib.rs:101-160`

**Rate Limiter Configuration:**
- **Max acceleration**: 50.0 m/s² (effectively unlimited for teleop responsiveness)
- **Max deceleration**: 15.0 m/s² (higher for quicker stops)
- **Max linear velocity**: 5.0 m/s (from chassis config)
- **Max angular velocity**: 2.5 rad/s (from chassis config)

**Key Points to Review:**
- [ ] Rate limiter applied before motor commands sent
- [ ] Direction change detection (applies deceleration rate)
- [ ] Velocity clamped to absolute limits
- [ ] Rate limiter reset on e-stop or mode change
- [ ] Delta time (dt) used for rate calculations
- [ ] No divide-by-zero when dt is very small

**Example Pattern:**
```rust
// Good: Rate limiting with direction change detection
impl RateLimiter {
    pub fn limit(&mut self, target: Twist, dt: f32) -> Twist {
        // Detect direction change (requires deceleration)
        let accel = if self.prev.linear * target.linear < 0.0 {
            self.max_decel  // Braking
        } else {
            self.max_accel  // Accelerating
        };

        // Apply rate limit
        let delta = target.linear - self.prev.linear;
        let max_delta = accel * dt;
        let limited = self.prev.linear + delta.clamp(-max_delta, max_delta);

        // Clamp to absolute limits
        Twist {
            linear: limited.clamp(-self.max_linear, self.max_linear),
            angular: /* similar for angular */,
            boost: target.boost,
        }
    }
}
```

**Red Flags:**
- Raw target velocity sent directly to motors
- No rate limiting on angular velocity
- Acceleration limits too high (>100 m/s²)
- Rate limiter bypassed in autonomous mode
- Missing dt parameter or using fixed dt

**See**: [safety-checklist.md](safety-checklist.md) for validation tests.

### 4. State Machine Transitions

**Purpose**: Enforce valid operational mode transitions and prevent unsafe state combinations.

**Key Points to Review:**
- [ ] All state transitions explicitly defined
- [ ] Invalid transitions logged and rejected
- [ ] `is_driving()` check used to gate motor commands
- [ ] `is_safe()` check used for configuration changes
- [ ] Unit tests cover all transition paths
- [ ] Logging includes both old and new modes

**Critical Checks:**
```rust
// is_driving() - only Teleop and Autonomous should drive
pub fn is_driving(&self) -> bool {
    matches!(self.mode, Mode::Teleop | Mode::Autonomous)
}

// is_safe() - only allow config changes in safe modes
pub fn is_safe(&self) -> bool {
    matches!(self.mode, Mode::Disabled | Mode::Idle | Mode::EStop)
}
```

**Example Pattern:**
```rust
// Good: Explicit transition handling with logging
match (self.mode, event) {
    (Mode::Idle, Event::Enable) => {
        self.mode = Mode::Teleop;
        info!(old = ?Mode::Idle, new = ?Mode::Teleop, "Mode transition");
    }
    (Mode::Disabled, Event::Enable) => {
        warn!("Cannot enable from Disabled, transition to Idle first");
        // Reject transition
    }
    _ => {
        debug!(?self.mode, ?event, "Unhandled event");
    }
}
```

**See**: [state-machine.md](state-machine.md) for full transition table and unit tests.

## CAN Bus Protocol Review

### 1. VESC Motor Controller Communication

**Purpose**: Send velocity/duty commands to 4 VESC motor controllers (FL, FR, RL, RR) and receive status.

**Location**: `bvr/firmware/crates/can/src/vesc.rs`

**VESC CAN IDs:** 0, 1, 2, 3 (configured in `bvr.toml`)
- ID 0: Front Left (FL)
- ID 1: Front Right (FR)
- ID 2: Rear Left (RL)
- ID 3: Rear Right (RR)

**Command Frame Format (Extended CAN):**
- **Frame ID**: `(command_id << 8) | vesc_id`
- **Data Length**: 4 bytes (duty), 4 bytes (RPM), 4 bytes (current)
- **Byte Order**: Big-endian

**Command Types:**
- `SetDuty (0)`: Duty cycle control, -1.0 to 1.0 scaled to ±100,000
- `SetRpm (3)`: Electrical RPM (divide by pole pairs for mechanical)
- `SetCurrent (1)`: Current control in milliamps

**Key Points to Review:**
- [ ] VESC IDs match configuration (0-3 for 4 motors)
- [ ] Command ID correctly shifted to bits [8:15]
- [ ] Big-endian byte order used (VESC protocol requirement)
- [ ] Duty cycle clamped to ±1.0 before scaling
- [ ] Status parsing includes bounds checking (`data.len() >= 8`)
- [ ] Heartbeat timeout configured (100ms default)
- [ ] Status frames parsed correctly (STATUS1, STATUS4, STATUS5)

**Example Pattern:**
```rust
// Good: VESC command with proper encoding
pub fn set_duty(&mut self, duty: f32) -> Result<Frame, CanError> {
    let clamped_duty = duty.clamp(-1.0, 1.0);
    let duty_value = (clamped_duty * 100_000.0) as i32;

    let frame_id = (CMD_SET_DUTY << 8) | self.id;  // Extended ID
    let data = duty_value.to_be_bytes();  // Big-endian

    Frame::new(Id::Extended(frame_id), &data)
}

// Good: Safe status parsing with bounds check
fn parse_status1(&mut self, data: &[u8]) {
    if data.len() < 8 {
        warn!("STATUS1 frame too short");
        return;
    }
    self.state.status.erpm = i32::from_be_bytes([data[0], data[1], data[2], data[3]]);
    self.state.status.current = i16::from_be_bytes([data[4], data[5]]) as f32 / 10.0;
    self.state.status.duty = i16::from_be_bytes([data[6], data[7]]) as f32 / 1000.0;
}
```

**Red Flags:**
- Little-endian byte order used (VESC expects big-endian)
- No bounds checking on status frame parsing (array panic risk)
- Duty cycle not clamped (can send invalid values >1.0)
- VESC IDs hardcoded instead of using configuration
- Missing timeout detection for lost VESCs

**See**: [can-protocol.md](can-protocol.md) for complete VESC protocol reference.

### 2. MCU LED Peripheral Communication

**Purpose**: Send LED mode commands to RP2350/ESP32-S3 MCU for rover status indication.

**Location**: `bvr/firmware/crates/can/src/leds.rs`

**LED CAN ID Range:** 0x0B00-0x0BFF (extended IDs for peripherals)
- **LED_CMD**: 0x0B00 (Jetson → MCU)
- **LED_STATUS**: 0x0B01 (MCU → Jetson)

**LED Modes:**
- `StateLinked (0x10)`: MCU automatically sets color based on rover mode
- `Solid`: Fixed color
- `Pulse`: Breathing effect (configurable period)
- `Flash`: Strobe effect (configurable period)
- `Chase`: Moving pattern

**Rover State Colors:**
- Disabled: Red solid
- Idle: Blue solid
- Teleop: Green pulse (2s period)
- Autonomous: Cyan pulse (1.5s period)
- EStop: Red flash (200ms, full brightness)
- Fault: Orange flash (500ms)

**Key Points to Review:**
- [ ] LED commands use 0x0B00 base address
- [ ] StateLinked mode used for automatic state indication
- [ ] LED state synchronized with state machine transitions
- [ ] Color choices distinct and recognizable
- [ ] MCU communication timeout handled gracefully

**Example Pattern:**
```rust
// Good: State-linked LED control
pub fn update_leds(&mut self, mode: Mode) {
    let led_mode = match mode {
        Mode::Idle => LedMode::idle(),        // Blue solid
        Mode::Teleop => LedMode::teleop(),    // Green pulse 2s
        Mode::Autonomous => LedMode::autonomous(), // Cyan pulse 1.5s
        Mode::EStop => LedMode::estop(),      // Red flash 200ms
        Mode::Fault => LedMode::fault(),      // Orange flash 500ms
        _ => LedMode::off(),
    };
    self.send_led_command(led_mode)?;
}
```

**See**: [can-protocol.md](can-protocol.md) for LED protocol details.

### 3. CAN Bus Error Handling

**Key Points to Review:**
- [ ] Timeout handling for lost CAN frames (10ms read/write timeout)
- [ ] Invalid frame ID detection and rejection
- [ ] Proper use of `Result` types with `CanError`
- [ ] Mock CAN bus for non-Linux development builds
- [ ] Error logging includes context (frame ID, data length, timeout)

**Example Pattern:**
```rust
// Good: Comprehensive error handling
#[derive(Error, Debug)]
pub enum CanError {
    #[error("Socket error: {0}")]
    Socket(String),
    #[error("Invalid CAN ID: {0}")]
    InvalidId(u32),
    #[error("Timeout waiting for response")]
    Timeout,
    #[error("Invalid frame data")]
    InvalidFrame,
}

// Good: Non-blocking receive with timeout
match self.socket.read_frame_timeout(Duration::from_millis(10)) {
    Ok(frame) => { /* process */ }
    Err(e) if e.kind() == ErrorKind::WouldBlock => { /* no data */ }
    Err(e) => {
        error!(?e, "CAN socket read error");
        return Err(CanError::Socket(e.to_string()));
    }
}
```

## Code Pattern Review

### 1. Error Handling with thiserror

**Convention**: Use `thiserror` for library crates, `anyhow` for binary crates.

**Key Points to Review:**
- [ ] Library crates define custom error enums with `thiserror`
- [ ] Error variants include context with `#[error("...")]`
- [ ] `#[from]` attribute used for error conversion
- [ ] Binary crates use `anyhow::Result` and `.context()`
- [ ] Errors logged with `?e` (Debug) not `%e` (Display)

**Example Pattern:**
```rust
// Library crate (crates/teleop/src/lib.rs)
use thiserror::Error;

#[derive(Error, Debug)]
pub enum TeleopError {
    #[error("Network error: {0}")]
    Network(#[from] std::io::Error),
    #[error("Serialization error: {0}")]
    Serialization(String),
    #[error("Connection timeout")]
    Timeout,
}

// Binary crate (bins/bvrd/src/main.rs)
use anyhow::{Context, Result};

fn load_config() -> Result<Config> {
    let contents = fs::read_to_string("bvr.toml")
        .context("Failed to read bvr.toml")?;
    toml::from_str(&contents)
        .context("Failed to parse bvr.toml")
}
```

**Red Flags:**
- String-based errors in libraries (`Result<T, String>`)
- Missing error context in anyhow chains
- Panic on recoverable errors (`unwrap()`, `expect()` in libraries)
- Display format used in logs (should use Debug: `?e`)

### 2. Async/Tokio Patterns

**Runtime**: Multi-threaded Tokio (`#[tokio::main]`)

**Key Points to Review:**
- [ ] `#[tokio::main]` on main function
- [ ] Channels for inter-task communication (mpsc, watch)
- [ ] Tasks spawned with `tokio::spawn` for concurrent subsystems
- [ ] Proper error handling in spawned tasks (log errors, don't panic)
- [ ] Graceful shutdown with signal handling
- [ ] No blocking operations in async context

**Example Pattern:**
```rust
// Good: Async main with spawned tasks
#[tokio::main]
async fn main() -> Result<()> {
    let (cmd_tx, cmd_rx) = mpsc::channel::<Command>(100);
    let (telem_tx, telem_rx) = watch::channel(Telemetry::default());

    // Spawn teleop server task
    tokio::spawn(async move {
        if let Err(e) = teleop_server.run(cmd_tx, telem_rx).await {
            error!(?e, "Teleop server error");
        }
    });

    // Spawn metrics task
    tokio::spawn(async move {
        if let Err(e) = metrics.run(telem_rx).await {
            error!(?e, "Metrics task error");
        }
    });

    // Main control loop
    loop {
        tokio::select! {
            Some(cmd) = cmd_rx.recv() => { /* handle */ }
            _ = tokio::signal::ctrl_c() => {
                info!("Shutdown signal received");
                break;
            }
        }
    }

    Ok(())
}
```

**Red Flags:**
- Blocking calls (std::thread::sleep, blocking I/O) in async functions
- Missing error handling in spawned tasks
- Tasks not joined/awaited on shutdown (resource leaks)
- Unbounded channels (prefer bounded with capacity)

### 3. Module Documentation

**Convention**: Module-level `//!` docs at top of lib.rs files, function-level `///` docs.

**Key Points to Review:**
- [ ] `//!` module-level docs describe crate purpose
- [ ] `///` function docs include examples for public API
- [ ] Struct fields documented with `///`
- [ ] No missing_docs warnings in library crates

**Example Pattern:**
```rust
//! State machine and mode management for bvr.
//!
//! This crate implements the rover's operational modes and state
//! transitions, including safety mechanisms like e-stop handling.

/// Represents the rover's current operational mode.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Mode {
    /// Motors disabled, awaiting initialization
    Disabled,
    /// Ready state, motors enabled but stationary
    Idle,
    /// Under human control via teleop
    Teleop,
    // ...
}

/// Handles a state machine event and transitions to a new mode if valid.
///
/// # Example
/// ```
/// let mut sm = StateMachine::new();
/// sm.handle(Event::Enable);
/// assert_eq!(sm.mode(), Mode::Idle);
/// ```
pub fn handle(&mut self, event: Event) {
    // ...
}
```

### 4. Workspace Dependencies

**Convention**: Use `version.workspace = true` for shared dependencies.

**Key Points to Review:**
- [ ] Workspace dependencies defined in root `Cargo.toml`
- [ ] Crate `Cargo.toml` uses `version.workspace = true`
- [ ] Consistent versions across all crates (tokio, serde, etc.)
- [ ] Optional features documented

**Example Pattern:**
```toml
# Root bvr/firmware/Cargo.toml
[workspace.dependencies]
tokio = { version = "1.41", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
thiserror = "2.0"

# Crate Cargo.toml
[dependencies]
tokio = { workspace = true }
serde = { workspace = true }
thiserror = { workspace = true }
```

## Testing Requirements

### 1. Unit Tests

**Convention**: Tests in `#[cfg(test)] mod tests` block at bottom of file.

**Key Points to Review:**
- [ ] Safety-critical functions have unit tests
- [ ] State machine transitions tested
- [ ] Edge cases covered (zero dt, negative values, etc.)
- [ ] Test names describe behavior (`test_watchdog_timeout_triggers`)
- [ ] Use `assert!` with helpful messages

**Example Pattern:**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_watchdog_timeout_triggers() {
        let mut wd = Watchdog::new(Duration::from_millis(100));
        assert!(wd.is_timed_out(), "Watchdog should timeout initially");

        wd.feed();
        assert!(!wd.is_timed_out(), "Watchdog should not timeout after feed");

        std::thread::sleep(Duration::from_millis(150));
        assert!(wd.is_timed_out(), "Watchdog should timeout after duration");
    }

    #[test]
    fn test_estop_requires_explicit_release() {
        let mut sm = StateMachine::new();
        sm.handle(Event::Enable);
        assert_eq!(sm.mode(), Mode::Teleop);

        sm.handle(Event::EStop);
        assert_eq!(sm.mode(), Mode::EStop);

        sm.handle(Event::Enable);
        assert_eq!(sm.mode(), Mode::EStop, "Cannot enable directly from e-stop");

        sm.handle(Event::EStopRelease);
        assert_eq!(sm.mode(), Mode::Idle, "Release transitions to Idle");
    }
}
```

### 2. Integration Tests

**Key Points to Review:**
- [ ] CAN bus simulation/mocking for development
- [ ] Teleop protocol tests with mock clients
- [ ] Configuration loading tested with fixtures

**See**: Run tests with `cargo test` (native) or `cargo test --target aarch64-unknown-linux-gnu` (cross).

## References and Additional Resources

For more detailed information, see:
- [safety-checklist.md](safety-checklist.md) - Line-by-line safety verification
- [can-protocol.md](can-protocol.md) - Complete VESC and LED protocol reference
- [state-machine.md](state-machine.md) - State transition diagram and LED feedback
- [CLAUDE.md](/Users/cam/Developer/muni/CLAUDE.md) - Project-wide conventions and architecture

## Quick Review Commands

```bash
# Run all tests
cargo test

# Check compilation without building
cargo check

# Build for Jetson (requires cross)
cargo build --release --target aarch64-unknown-linux-gnu

# Deploy to rover
./deploy.sh <rover-hostname>
```
