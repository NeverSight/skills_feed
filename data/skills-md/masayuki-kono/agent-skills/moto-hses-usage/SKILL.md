---
name: moto-hses-usage
description: "moto-hses Rust crate usage guide. USE WHEN: implementing HSES (High Speed Ethernet Server) communication with Yaskawa robot controllers."
---

# moto-hses usage guide

This skill provides guidance for using the `moto-hses` crate family to communicate with Yaskawa robot controllers via the High Speed Ethernet Server (HSES) protocol.

> **Note**: The `moto-hses` crate family is a Rust client implementation for the HSES protocol. For the underlying protocol specification (message structure, command IDs, error codes), see the **hses-protocol** skill.

## When to Use

- Implementing HSES communication with Yaskawa robot controllers in Rust
- Using `moto_hses_client`, `moto_hses_proto`, or `moto_hses_mock` crates
- Looking up API methods for robot control, status reading, variable access, file operations
- Writing tests with MockServer for HSES communication

## Crate Overview

| Crate | Purpose |
|-------|---------|
| `moto_hses_client` | HSES client for communicating with robot controllers |
| `moto_hses_proto` | Protocol types (Status, commands, etc.) |
| `moto_hses_mock` | Mock server for integration testing |

### Key Types

| Type | Description |
|------|-------------|
| `HsesClient` | Basic HSES client (single-task usage) |
| `SharedHsesClient` | Thread-safe wrapper for concurrent access from multiple tasks |
| `HsesClientOps` | Trait for client abstraction (implemented by both client types) |

## Client Connection

### Basic Usage

```rust
use moto_hses_client::{ClientConfig, HsesClient};
use moto_hses_proto::{ROBOT_CONTROL_PORT, FILE_CONTROL_PORT, TextEncoding};
use std::time::Duration;

// Create configuration
let config = ClientConfig {
    host: "192.168.1.100".to_string(),
    port: ROBOT_CONTROL_PORT,  // 10040 for robot control
    timeout: Duration::from_millis(3000),
    retry_count: 0,
    retry_delay: Duration::from_millis(200),
    buffer_size: 8192,
    text_encoding: TextEncoding::ShiftJis,
};

// Connect to controller
let client = HsesClient::new_with_config(config).await?;
```

### Port Constants

| Constant | Port | Usage |
|----------|------|-------|
| `ROBOT_CONTROL_PORT` | 10040 | Status, servo, job, variable, I/O, register operations |
| `FILE_CONTROL_PORT` | 10041 | File transfer operations (send/receive/delete) |

### Thread-Safe Client (SharedHsesClient)

For concurrent access from multiple tasks, wrap `HsesClient` with `SharedHsesClient`:

```rust
use moto_hses_client::{HsesClient, HsesClientOps, SharedHsesClient};

// Create HsesClient and wrap it for thread-safe access
let client = HsesClient::new_with_config(config).await?;
let shared_client = SharedHsesClient::new(client);

// Clone for each concurrent task
let client1 = shared_client.clone();
let client2 = shared_client.clone();

let handle1 = tokio::spawn(async move {
    client1.read_status().await
});

let handle2 = tokio::spawn(async move {
    client2.read_position(0).await
});

// Wait for all tasks
let (result1, result2) = tokio::try_join!(handle1, handle2)?;
```

### HsesClientOps Trait

Both `HsesClient` and `SharedHsesClient` implement the `HsesClientOps` trait, enabling abstraction:

```rust
use moto_hses_client::HsesClientOps;

/// Accepts any client type implementing HsesClientOps
async fn check_status(client: &impl HsesClientOps) -> Result<bool, ClientError> {
    let status = client.read_status().await?;
    Ok(status.is_running())
}

// Works with both client types
check_status(&client).await?;        // HsesClient
check_status(&shared_client).await?; // SharedHsesClient
```

## HsesClient API

### Status & Control

| Method | Description |
|--------|-------------|
| `read_status()` | Read complete status (Data 1 & Data 2) |
| `read_status_data1()` | Read status data 1 only |
| `read_status_data2()` | Read status data 2 only |
| `set_servo(bool)` | Turn servo ON/OFF |
| `set_hold(bool)` | Set/release hold state |
| `set_hlock(bool)` | Set/release HLOCK (interlock PP and I/O) |
| `set_cycle_mode(CycleMode)` | Set cycle mode (Step/OneCycle/Continuous) |

#### Status Convenience Methods

The `Status` struct returned by `read_status()` provides these helper methods:

| Method | Description |
|--------|-------------|
| `is_running()` | Check if robot is running |
| `is_servo_on()` | Check if servo is ON |
| `has_alarm()` | Check if alarm is active |
| `has_error()` | Check if error is active |
| `is_teach_mode()` | Check if in teach mode |
| `is_play_mode()` | Check if in play mode |
| `is_remote_mode()` | Check if in remote mode |

#### CycleMode Enum (`moto_hses_proto::CycleMode`)

| Variant | Description |
|---------|-------------|
| `CycleMode::Step` | Execute one instruction at a time |
| `CycleMode::OneCycle` | Execute job once and stop |
| `CycleMode::Continuous` | Execute job repeatedly |

### Job Control

| Method | Description |
|--------|-------------|
| `select_job(select_type, job_name, line_number)` | Select job for execution |
| `start_job()` | Start the selected job |
| `read_executing_job_info(task_type, attribute)` | Read executing job info |
| `read_executing_job_info_complete(task_type)` | Read all job info attributes |

#### JobSelectType Enum (`moto_hses_proto::commands::JobSelectType`)

| Variant | Description |
|---------|-------------|
| `JobSelectType::InExecution` | Select job for current task |
| `JobSelectType::MasterJob` | Select as master job |

> **Note**: Job name does not require `.JBI` extension.

### Position

| Method | Description |
|--------|-------------|
| `read_position(control_group)` | Read current position |

### Alarm

| Method | Description |
|--------|-------------|
| `read_alarm_data(instance, attribute)` | Read alarm data |
| `read_alarm_history(instance, attribute)` | Read alarm history |
| `reset_alarm()` | Reset active alarms |
| `cancel_error()` | Cancel current error |

#### AlarmAttribute Enum (`moto_hses_proto::AlarmAttribute`)

| Variant | Description |
|---------|-------------|
| `AlarmAttribute::All` | Read all alarm attributes |
| `AlarmAttribute::Code` | Read alarm code only |
| `AlarmAttribute::Data` | Read alarm data only |
| `AlarmAttribute::Type` | Read alarm type only |
| `AlarmAttribute::Time` | Read alarm time only |
| `AlarmAttribute::Name` | Read alarm name only |

#### Alarm Instance Ranges

| Range | Type |
|-------|------|
| 1-10 | Major failure alarm history |
| 1001-1010 | Monitor alarm history |

### Variable (Single)

| Method | Description |
|--------|-------------|
| `read_u8(index)` / `write_u8(index, value)` | B-type (8-bit unsigned) |
| `read_i16(index)` / `write_i16(index, value)` | I-type (16-bit signed) |
| `read_i32(index)` / `write_i32(index, value)` | D-type (32-bit signed) |
| `read_f32(index)` / `write_f32(index, value)` | R-type (32-bit float) |
| `read_string(index)` / `write_string(index, value)` | S-type (string, 16 bytes max) |

### Variable (Multiple)

| Method | Description |
|--------|-------------|
| `read_multiple_u8(start, count)` / `write_multiple_u8(start, values)` | B-type |
| `read_multiple_i16(start, count)` / `write_multiple_i16(start, values)` | I-type |
| `read_multiple_i32(start, count)` / `write_multiple_i32(start, values)` | D-type |
| `read_multiple_f32(start, count)` / `write_multiple_f32(start, values)` | R-type |
| `read_multiple_strings(start, count)` / `write_multiple_strings(start, values)` | S-type |

### I/O

| Method | Description |
|--------|-------------|
| `read_io(io_number)` / `write_io(io_number, value)` | Single I/O |
| `read_multiple_io(start, count)` / `write_multiple_io(start, data)` | Multiple I/O |

### Register

| Method | Description |
|--------|-------------|
| `read_register(number)` / `write_register(number, value)` | Single register |
| `read_multiple_registers(start, count)` / `write_multiple_registers(start, values)` | Multiple registers |

### File

> **Note**: File operations require connecting to `FILE_CONTROL_PORT` (10041), not `ROBOT_CONTROL_PORT`.

| Method | Description |
|--------|-------------|
| `read_file_list(pattern)` | Get file list (e.g., "*.JBI") |
| `send_file(filename, content)` | Send file to controller |
| `receive_file(filename)` | Receive file from controller |
| `delete_file(filename)` | Delete file from controller |

## Error Handling

All async methods return `Result<T, ClientError>`. Common error patterns:

```rust
use moto_hses_client::ClientError;

match client.read_status().await {
    Ok(status) => { /* handle success */ }
    Err(ClientError::TimeoutError(_)) => { /* connection timeout */ }
    Err(ClientError::ConnectionError(_)) => { /* I/O error */ }
    Err(ClientError::ConnectionFailed(retries)) => { /* connection failed after retries */ }
    Err(ClientError::ProtocolError(_)) => { /* protocol-level error */ }
    Err(ClientError::InvalidVariable(_)) => { /* invalid variable access */ }
    Err(ClientError::SystemError(_)) => { /* system error */ }
}
```

## Testing

### Unit Tests

Use the `HsesClientOps` trait (see [HsesClientOps Trait](#hsesclientops-trait) section) for dependency injection and mock implementations in unit tests.

```rust
use moto_hses_client::{ClientError, HsesClientOps};
use moto_hses_proto::Status;

// Create a mock implementation for unit testing
struct MockClient {
    status: Status,
}

#[async_trait::async_trait]
impl HsesClientOps for MockClient {
    async fn read_status(&self) -> Result<Status, ClientError> {
        Ok(self.status.clone())
    }
    // ... implement other methods as needed
}

// Use in tests
async fn handler(client: &impl HsesClientOps) -> Result<bool, ClientError> {
    let status = client.read_status().await?;
    Ok(status.is_running())
}
```

### Integration Tests with MockServer

Use `moto_hses_mock::MockServer` for integration testing with actual network communication.

```rust
use moto_hses_mock::{MockConfig, MockServer};

let config = MockConfig::new("127.0.0.1", 10040, 10041);
let server = Arc::new(MockServer::new(config).await?);

tokio::spawn({
    let server = Arc::clone(&server);
    async move { server.run().await.ok(); }
});
tokio::time::sleep(Duration::from_millis(200)).await;
```

#### State Access

```rust
// Get state reference
let state = server.state();

// Read state (async)
let guard = state.read().await;
assert!(guard.servo_on);
assert!(guard.get_running());

// Write state (async)
let mut guard = state.write().await;
guard.set_servo(true);
guard.set_hold(false);
guard.set_running(true);
```

#### MockState Methods

| Method | Description |
|--------|-------------|
| `set_servo(bool)` | Set servo ON/OFF state |
| `set_hold(bool)` | Set hold state |
| `set_running(bool)` | Set running state |
| `get_running()` | Get running state |
| `set_executing_job(Option<ExecutingJobInfo>)` | Set executing job info |
| `get_variable(index)` | Get variable value |
| `set_variable(index, value)` | Set variable value |
| `get_io_state(io_number)` | Get I/O state |
| `set_io_state(io_number, state)` | Set I/O state |

If a method for the desired state doesn't exist, you can directly access the public fields of `MockState` (e.g., `guard.status.data1.running`).

## Important Considerations

### Port Conflict Avoidance
- **Single-threaded Execution**: Configure with `RUST_TEST_THREADS = "1"`
- **Port Management**: MockServer uses fixed ports (10040, 10041)
- **Test Isolation**: Independent MockServer instances prevent state interference between tests

### Test Design Best Practices
1. **State Management**: Utilize MockServer's state modification interfaces
2. **Wait for Async**: Add small delays after server start and before assertions

## Reference Examples (in references/examples/)

The `references/examples/` directory contains sample code for various operations:

| Example | Description |
|---------|-------------|
| `read_status.rs` | Status reading and convenience methods |
| `hold_servo_control.rs` | Servo/Hold/Hlock control operations |
| `cycle_mode_control.rs` | Cycle mode setting |
| `job_select.rs` | Job selection |
| `job_start.rs` | Job execution |
| `position_operations.rs` | Robot position reading |
| `alarm_operations.rs` | Alarm data reading and reset |
| `byte_variable_operations.rs` | B-type variable (8-bit unsigned) |
| `integer_variable_operations.rs` | I-type variable (16-bit signed) |
| `double_variable_operations.rs` | D-type variable (32-bit signed) |
| `real_variable_operations.rs` | R-type variable (32-bit float) |
| `string_variable_operations.rs` | S-type variable (string) |
| `io_operations.rs` | I/O data reading and writing |
| `register_operations.rs` | Register data reading and writing |
| `file_operations.rs` | File transfer operations |
| `read_executing_job_info.rs` | Executing job information |
| `mock_basic_usage.rs` | MockServer setup and state configuration |
| `shared_client.rs` | Thread-safe SharedHsesClient for concurrent access |

> **Note**: For detailed API specifications, refer to the crate documentation on crates.io. The examples above focus on practical usage patterns.

## Protocol Reference

For a complete mapping of HSES protocol commands to API methods, see [Protocol Command Reference](references/protocol-commands.md).
