---
name: integration-testing
description: Guides end-to-end testing, mocking, and simulation for the Muni codebase. Use when writing integration tests, setting up test environments, creating mock CAN bus, testing WebSocket protocols, validating database fixtures, or debugging test failures. Covers Rust test patterns (tokio::test, integration tests), TypeScript testing (Vitest), mock infrastructure (Docker Compose for tests), CAN bus simulation, WebSocket test clients, database seeding, and Rerun recording validation. Essential for ensuring components work together correctly.
allowed-tools: Read, Grep, Glob, Bash(cargo:test), Bash(cargo:nextest), Bash(npm:test), Bash(docker:compose), Bash(pytest)
---

# Integration Testing Skill

Comprehensive guide for testing integration points across the Muni system.

## Overview

Muni has complex integration points that require end-to-end testing:

**Integration Points**:
- **Rover ↔ Depot**: WebSocket (teleop, discovery, dispatch), UDP (metrics)
- **CAN Bus**: VESC motor controllers, MCU peripherals
- **Database**: PostgreSQL (dispatch service)
- **File System**: Session recording, sync, playback
- **External Services**: GPS/RTK, video streaming

**Testing Approaches**:
| Component | Test Type | Tools | Location |
|-----------|-----------|-------|----------|
| Rust firmware | Integration tests | `tokio::test`, mocks | `tests/` directory |
| TypeScript console | Component/E2E tests | Vitest, Testing Library | `src/**/*.test.tsx` |
| Depot services | Integration tests | `tokio::test`, Docker | `tests/` directory |
| Python workers | Unit/integration | pytest | `tests/` directory |
| System-wide | Manual/scripted | Docker Compose | `integration-tests/` |

## Rust Integration Testing

### Test Structure

**Unit tests** (in same file):
```rust
// src/lib.rs or src/main.rs
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_function() {
        assert_eq!(2 + 2, 4);
    }
}
```

**Integration tests** (separate directory):
```
crate/
├── src/
│   └── lib.rs
├── tests/
│   ├── common/
│   │   └── mod.rs      # Shared test utilities
│   ├── integration_test_1.rs
│   └── integration_test_2.rs
└── Cargo.toml
```

### Async Testing with Tokio

```rust
// tests/websocket_test.rs
use tokio::net::TcpListener;
use futures_util::{SinkExt, StreamExt};

#[tokio::test]
async fn test_websocket_echo() {
    // Start test server
    let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
    let addr = listener.local_addr().unwrap();

    tokio::spawn(async move {
        let (stream, _) = listener.accept().await.unwrap();
        // Handle WebSocket...
    });

    // Connect as client
    let (ws_stream, _) = tokio_tungstenite::connect_async(
        format!("ws://{}", addr)
    ).await.unwrap();

    let (mut write, mut read) = ws_stream.split();

    // Send message
    write.send(tungstenite::Message::Text("hello".into())).await.unwrap();

    // Receive response
    let msg = read.next().await.unwrap().unwrap();
    assert_eq!(msg, tungstenite::Message::Text("hello".into()));
}
```

### Test Fixtures and Setup

**Shared test utilities**:
```rust
// tests/common/mod.rs
use std::sync::Arc;
use tokio::sync::RwLock;

pub struct TestContext {
    pub state: Arc<AppState>,
    pub addr: SocketAddr,
}

impl TestContext {
    pub async fn new() -> Self {
        // Setup test state
        let state = Arc::new(AppState::new());

        // Start test server
        let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
        let addr = listener.local_addr().unwrap();

        tokio::spawn(async move {
            axum::serve(listener, create_router(state)).await.unwrap();
        });

        Self { state, addr }
    }

    pub fn url(&self, path: &str) -> String {
        format!("http://{}{}", self.addr, path)
    }
}
```

**Using in tests**:
```rust
// tests/api_test.rs
mod common;

#[tokio::test]
async fn test_health_endpoint() {
    let ctx = common::TestContext::new().await;

    let response = reqwest::get(&ctx.url("/health")).await.unwrap();
    assert_eq!(response.status(), 200);

    let body: serde_json::Value = response.json().await.unwrap();
    assert_eq!(body["status"], "ok");
}
```

### Database Testing

**In-memory database** (SQLite):
```rust
use sqlx::SqlitePool;

async fn setup_test_db() -> SqlitePool {
    let pool = SqlitePool::connect(":memory:").await.unwrap();

    // Run migrations
    sqlx::migrate!("./migrations")
        .run(&pool)
        .await
        .unwrap();

    pool
}

#[tokio::test]
async fn test_database_query() {
    let pool = setup_test_db().await;

    // Insert test data
    sqlx::query("INSERT INTO zones (name) VALUES ($1)")
        .bind("Test Zone")
        .execute(&pool)
        .await
        .unwrap();

    // Query
    let zones: Vec<Zone> = sqlx::query_as("SELECT * FROM zones")
        .fetch_all(&pool)
        .await
        .unwrap();

    assert_eq!(zones.len(), 1);
    assert_eq!(zones[0].name, "Test Zone");
}
```

**Test database** (PostgreSQL via Docker):
```rust
// tests/common/mod.rs
use testcontainers::{clients::Cli, images::postgres::Postgres, Container};

pub struct TestDb<'a> {
    _container: Container<'a, Postgres>,
    pub pool: PgPool,
}

impl<'a> TestDb<'a> {
    pub async fn new(docker: &'a Cli) -> Self {
        let container = docker.run(Postgres::default());
        let port = container.get_host_port_ipv4(5432);

        let pool = PgPoolOptions::new()
            .connect(&format!("postgres://postgres:postgres@localhost:{}/postgres", port))
            .await
            .unwrap();

        // Run migrations
        sqlx::migrate!("./migrations").run(&pool).await.unwrap();

        Self {
            _container: container,
            pool,
        }
    }
}

#[tokio::test]
async fn test_with_postgres() {
    let docker = Cli::default();
    let db = TestDb::new(&docker).await;

    // Use db.pool for queries...
}
```

### Mocking CAN Bus

**Mock CAN interface**:
```rust
// tests/mock_can.rs
use std::sync::{Arc, Mutex};

#[derive(Clone)]
pub struct MockCan {
    sent_frames: Arc<Mutex<Vec<CanFrame>>>,
}

impl MockCan {
    pub fn new() -> Self {
        Self {
            sent_frames: Arc::new(Mutex::new(Vec::new())),
        }
    }

    pub fn send(&self, frame: CanFrame) {
        self.sent_frames.lock().unwrap().push(frame);
    }

    pub fn recv(&self) -> Option<CanFrame> {
        // Return pre-configured frames or generate on-demand
        Some(CanFrame::new(0x001, &[0x01, 0x02, 0x03]))
    }

    pub fn get_sent_frames(&self) -> Vec<CanFrame> {
        self.sent_frames.lock().unwrap().clone()
    }

    pub fn clear(&self) {
        self.sent_frames.lock().unwrap().clear();
    }
}

#[tokio::test]
async fn test_motor_command() {
    let can = MockCan::new();

    // Send motor command
    send_motor_command(&can, MotorId::FrontLeft, 100).await;

    // Verify frame was sent
    let frames = can.get_sent_frames();
    assert_eq!(frames.len(), 1);
    assert_eq!(frames[0].id(), 0x001);  // VESC ID
}
```

**Trait-based abstraction** (for real/mock CAN):
```rust
#[async_trait]
pub trait CanInterface: Send + Sync {
    async fn send(&self, frame: CanFrame) -> Result<()>;
    async fn recv(&self) -> Result<CanFrame>;
}

// Real implementation
pub struct RealCan {
    socket: CanSocket,
}

#[async_trait]
impl CanInterface for RealCan {
    async fn send(&self, frame: CanFrame) -> Result<()> {
        self.socket.write_frame(&frame).await
    }

    async fn recv(&self) -> Result<CanFrame> {
        self.socket.read_frame().await
    }
}

// Mock implementation
pub struct MockCan {
    // ... as above
}

#[async_trait]
impl CanInterface for MockCan {
    async fn send(&self, frame: CanFrame) -> Result<()> {
        self.sent_frames.lock().unwrap().push(frame);
        Ok(())
    }

    async fn recv(&self) -> Result<CanFrame> {
        Ok(CanFrame::new(0x001, &[0x01, 0x02, 0x03]))
    }
}

// Usage in tests
#[tokio::test]
async fn test_with_mock_can() {
    let can: Arc<dyn CanInterface> = Arc::new(MockCan::new());
    // Test code uses CanInterface trait...
}
```

### Testing WebSocket Protocols

**WebSocket test client**:
```rust
use tokio_tungstenite::{connect_async, tungstenite::Message};

#[tokio::test]
async fn test_dispatch_protocol() {
    // Start service
    let ctx = TestContext::new().await;
    let ws_url = format!("ws://{}/ws", ctx.addr);

    // Connect
    let (ws_stream, _) = connect_async(&ws_url).await.unwrap();
    let (mut write, mut read) = ws_stream.split();

    // Send registration
    let register = serde_json::json!({
        "type": "register",
        "rover_id": "test-rover"
    });
    write.send(Message::Text(register.to_string().into())).await.unwrap();

    // Receive task assignment
    let msg = read.next().await.unwrap().unwrap();
    let task: TaskMessage = serde_json::from_str(&msg.to_text().unwrap()).unwrap();

    assert_eq!(task.r#type, "task");
    assert!(!task.waypoints.is_empty());

    // Send progress
    let progress = serde_json::json!({
        "type": "progress",
        "task_id": task.task_id,
        "progress": 50
    });
    write.send(Message::Text(progress.to_string().into())).await.unwrap();

    // Cleanup
    write.close().await.unwrap();
}
```

### Test Timeouts

```rust
use tokio::time::{timeout, Duration};

#[tokio::test]
async fn test_with_timeout() {
    let result = timeout(Duration::from_secs(5), async {
        // Test code that might hang
        expensive_operation().await
    }).await;

    assert!(result.is_ok(), "Test timed out");
}
```

### Parallel Test Execution

**cargo-nextest** (faster test runner):
```bash
# Install
cargo install cargo-nextest

# Run tests in parallel
cargo nextest run

# Run specific test
cargo nextest run test_name

# Show output
cargo nextest run --nocapture
```

**Test isolation**:
```rust
// Use unique ports for each test
use std::sync::atomic::{AtomicU16, Ordering};

static NEXT_PORT: AtomicU16 = AtomicU16::new(50000);

fn get_test_port() -> u16 {
    NEXT_PORT.fetch_add(1, Ordering::SeqCst)
}

#[tokio::test]
async fn test_parallel_1() {
    let port = get_test_port();
    let listener = TcpListener::bind(format!("127.0.0.1:{}", port)).await.unwrap();
    // ...
}

#[tokio::test]
async fn test_parallel_2() {
    let port = get_test_port();
    let listener = TcpListener::bind(format!("127.0.0.1:{}", port)).await.unwrap();
    // ...
}
```

## TypeScript/React Testing

### Test Setup (Vitest)

**vitest.config.ts**:
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true,
  },
});
```

**test/setup.ts**:
```typescript
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
});
```

### Component Testing

```typescript
// src/components/RoverCard.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { RoverCard } from './RoverCard';

describe('RoverCard', () => {
  it('renders rover information', () => {
    const rover = {
      id: 'rover-1',
      name: 'Frog Zero',
      online: true,
      batteryVoltage: 48.5,
    };

    render(<RoverCard rover={rover} />);

    expect(screen.getByText('Frog Zero')).toBeInTheDocument();
    expect(screen.getByText('Online')).toBeInTheDocument();
    expect(screen.getByText('48.5V')).toBeInTheDocument();
  });

  it('shows offline status when rover is offline', () => {
    const rover = {
      id: 'rover-1',
      name: 'Frog Zero',
      online: false,
      batteryVoltage: 0,
    };

    render(<RoverCard rover={rover} />);

    expect(screen.getByText('Offline')).toBeInTheDocument();
  });
});
```

### Testing Hooks

```typescript
// src/hooks/useWebSocket.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { useWebSocket } from './useWebSocket';
import WS from 'jest-websocket-mock';

describe('useWebSocket', () => {
  it('connects to WebSocket server', async () => {
    const server = new WS('ws://localhost:1234');

    const { result } = renderHook(() =>
      useWebSocket('ws://localhost:1234')
    );

    await waitFor(() => {
      expect(result.current.status).toBe('connected');
    });

    server.close();
  });

  it('receives messages', async () => {
    const server = new WS('ws://localhost:1234');
    const onMessage = vi.fn();

    renderHook(() =>
      useWebSocket('ws://localhost:1234', { onMessage })
    );

    server.send({ type: 'update', data: 'test' });

    await waitFor(() => {
      expect(onMessage).toHaveBeenCalledWith({ type: 'update', data: 'test' });
    });

    server.close();
  });
});
```

### Mocking Zustand Store

```typescript
// src/test/mocks/store.ts
import { create } from 'zustand';
import { AppState } from '@/store';

export const createMockStore = (initialState?: Partial<AppState>) => {
  return create<AppState>(() => ({
    rovers: [],
    selectedRover: null,
    teleopActive: false,
    ...initialState,
    // Actions
    setRovers: vi.fn(),
    selectRover: vi.fn(),
    startTeleop: vi.fn(),
  }));
};

// In tests
import { createMockStore } from '@/test/mocks/store';

it('displays selected rover', () => {
  const mockStore = createMockStore({
    selectedRover: {
      id: 'rover-1',
      name: 'Frog Zero',
      online: true,
    },
  });

  render(
    <StoreProvider store={mockStore}>
      <RoverDetails />
    </StoreProvider>
  );

  expect(screen.getByText('Frog Zero')).toBeInTheDocument();
});
```

### E2E Testing with Playwright

**playwright.config.ts**:
```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: {
    baseURL: 'http://localhost:5173',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  webServer: {
    command: 'npm run dev',
    port: 5173,
    reuseExistingServer: !process.env.CI,
  },
});
```

**e2e/teleop.spec.ts**:
```typescript
import { test, expect } from '@playwright/test';

test('teleop flow', async ({ page }) => {
  await page.goto('/');

  // Select rover
  await page.click('[data-testid="rover-card-rover-1"]');
  await expect(page).toHaveURL(/\/rover\/rover-1/);

  // Start teleop
  await page.click('[data-testid="start-teleop-button"]');
  await expect(page.locator('[data-testid="teleop-active"]')).toBeVisible();

  // Send command (keyboard)
  await page.keyboard.press('KeyW');
  await page.waitForTimeout(100);

  // Stop teleop
  await page.click('[data-testid="stop-teleop-button"]');
  await expect(page.locator('[data-testid="teleop-active"]')).not.toBeVisible();
});
```

## Docker Test Environments

### Test Compose File

**docker-compose.test.yml**:
```yaml
version: '3.8'

services:
  postgres-test:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: test
      POSTGRES_DB: test_db
    ports:
      - "5433:5432"
    tmpfs:
      - /var/lib/postgresql/data  # In-memory (fast, ephemeral)

  redis-test:
    image: redis:7
    ports:
      - "6380:6379"

  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    depends_on:
      - postgres-test
      - redis-test
    environment:
      DATABASE_URL: postgres://postgres:test@postgres-test:5432/test_db
      REDIS_URL: redis://redis-test:6379
    command: cargo test
```

**Running tests**:
```bash
# Run tests in Docker
docker compose -f docker-compose.test.yml up --abort-on-container-exit

# Cleanup
docker compose -f docker-compose.test.yml down -v
```

### Test Fixtures with Docker

```rust
// tests/common/docker.rs
use testcontainers::{clients::Cli, Container, RunnableImage};
use testcontainers::images::postgres::Postgres;

pub struct TestEnv<'a> {
    pub postgres: Container<'a, Postgres>,
    pub pool: PgPool,
}

impl<'a> TestEnv<'a> {
    pub async fn new(docker: &'a Cli) -> Self {
        let postgres = docker.run(Postgres::default());
        let port = postgres.get_host_port_ipv4(5432);

        let pool = PgPoolOptions::new()
            .connect(&format!("postgres://postgres:postgres@localhost:{}/postgres", port))
            .await
            .unwrap();

        sqlx::migrate!("./migrations").run(&pool).await.unwrap();

        Self { postgres, pool }
    }

    pub async fn seed_data(&self) {
        sqlx::query("INSERT INTO zones (name) VALUES ('Test Zone')")
            .execute(&self.pool)
            .await
            .unwrap();
    }
}
```

## Python Testing (splat-worker)

### pytest Setup

**tests/conftest.py**:
```python
import pytest
import asyncio

@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def sample_point_cloud():
    """Load sample point cloud data."""
    import numpy as np
    points = np.random.rand(1000, 3)
    colors = np.random.rand(1000, 3)
    return points, colors
```

**tests/test_splat.py**:
```python
import pytest
from splat_worker import process_session

@pytest.mark.asyncio
async def test_process_session(sample_point_cloud):
    points, colors = sample_point_cloud

    result = await process_session(points, colors)

    assert result is not None
    assert result.splat_count > 0
    assert result.output_path.exists()
```

## Rerun Recording Validation

### Validate Recording Structure

```rust
// tests/recording_test.rs
use rerun::RecordingStream;

#[tokio::test]
async fn test_session_recording() {
    let rec = RecordingStream::new("test", rerun::default_store()).unwrap();

    // Log some data
    rec.log("world/robot/position", &rerun::Position3D::new(1.0, 2.0, 3.0)).unwrap();

    // Save recording
    rec.save("test.rrd").unwrap();

    // Validate file exists and is not empty
    let metadata = std::fs::metadata("test.rrd").unwrap();
    assert!(metadata.len() > 0);

    // Cleanup
    std::fs::remove_file("test.rrd").unwrap();
}
```

### Playback Validation

```bash
# Play back recording
rerun test.rrd

# Validate with Python
python -c "import rerun as rr; rr.load('test.rrd'); print('Valid')"
```

## CI/CD Integration

### GitHub Actions

**. github/workflows/test.yml**:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test-rust:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: actions-rs/toolchain@v1
        with:
          toolchain: stable

      - name: Run tests
        run: cargo test
        env:
          DATABASE_URL: postgres://postgres:test@localhost/postgres

  test-typescript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci
        working-directory: depot/console

      - name: Run tests
        run: npm test
        working-directory: depot/console
```

## Testing Checklist

### Before Committing

- [ ] All unit tests pass: `cargo test`
- [ ] Integration tests pass: `cargo test --test '*'`
- [ ] TypeScript tests pass: `npm test`
- [ ] Linting passes: `cargo clippy`, `npm run lint`
- [ ] Format is correct: `cargo fmt --check`

### Before Deploying

- [ ] All tests pass in CI
- [ ] Manual smoke tests completed
- [ ] Database migrations tested
- [ ] Rollback procedure verified
- [ ] Monitoring dashboards checked

### Test Coverage Goals

- **Critical paths**: 100% (safety systems, CAN communication)
- **Core functionality**: >80% (state machine, control logic)
- **Utilities**: >60% (helpers, converters)
- **UI components**: >50% (interactive elements)

## Common Testing Patterns

### Testing Error Handling

```rust
#[tokio::test]
async fn test_error_handling() {
    let result = function_that_fails().await;

    assert!(result.is_err());
    assert_eq!(
        result.unwrap_err().to_string(),
        "Expected error message"
    );
}
```

### Testing with Timeouts

```rust
use tokio::time::{timeout, Duration};

#[tokio::test]
async fn test_operation_completes_in_time() {
    let result = timeout(
        Duration::from_secs(5),
        slow_operation()
    ).await;

    assert!(result.is_ok(), "Operation timed out");
}
```

### Snapshot Testing

```rust
use insta::assert_debug_snapshot;

#[test]
fn test_serialization() {
    let data = ComplexStruct { /* ... */ };
    assert_debug_snapshot!(data);
}
```

## References

- [Tokio testing guide](https://tokio.rs/tokio/topics/testing)
- [SQLx testing](https://github.com/launchbadge/sqlx#testing)
- [Testing Library docs](https://testing-library.com/docs/react-testing-library/intro)
- [Vitest documentation](https://vitest.dev)
- [Playwright documentation](https://playwright.dev)
- [testcontainers-rs](https://github.com/testcontainers/testcontainers-rs)
