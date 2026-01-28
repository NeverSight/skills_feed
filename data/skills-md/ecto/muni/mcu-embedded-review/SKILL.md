---
name: mcu-embedded-review
description: Reviews embedded Rust firmware for RP2350 (Raspberry Pi Pico 2 W) and ESP32-S3 (Heltec) microcontrollers with focus on Embassy async runtime, memory constraints, LED control, CAN attachment protocols, and SLCAN bridging. Use when reviewing MCU firmware changes, debugging LED controller issues, evaluating Embassy async patterns, checking static memory allocation, validating SLCAN implementations, or assessing hardware-specific code for WS2812 LEDs, CAN peripherals, and tool attachments. Covers no_std environments, PIO state machines, RMT peripherals, and USB CDC serial communication.
allowed-tools: Read, Grep, Glob, Bash(cargo:build)
---

# MCU Embedded Firmware Code Review Skill

This skill provides comprehensive code review for embedded Rust firmware targeting RP2350 and ESP32-S3 microcontrollers used in the BVR rover system.

## Overview

The BVR uses two MCU platforms for peripheral control:
1. **RP2350 (Pico 2 W)**: LED controllers, USB peripherals
2. **ESP32-S3 (Heltec)**: Tool attachments, LoRa communication, OLED display

Both run Rust in `no_std` environments with hardware-specific runtimes and memory constraints.

**Architecture:**
```
mcu/
├── bins/
│   ├── rp2350/         # Pico 2 W binaries (LED controller, etc.)
│   │   └── src/main.rs
│   └── esp32s3/        # Heltec binaries (attachments, SLCAN)
│       └── src/main.rs
├── crates/
│   ├── mcu-core/       # Shared protocol and types
│   ├── mcu-leds/       # LED controller library
│   └── ...
```

**Key Differences:**

| Feature           | RP2350 (Pico 2 W)               | ESP32-S3 (Heltec)              |
|-------------------|---------------------------------|--------------------------------|
| **Runtime**       | Embassy async (`#[embassy_executor::main]`) | Polling loop (`#[main]`)       |
| **Memory**        | 520 KB SRAM, static allocation  | 512 KB SRAM, heap allocation   |
| **Edition**       | Rust 2021                       | Rust 2024                      |
| **LED Control**   | PIO state machine (WS2812)      | RMT peripheral (WS2811/WS2812) |
| **USB**           | USB CDC serial (device mode)    | USB serial (via UART bridge)   |
| **Display**       | None                            | OLED SSD1306 (I2C)             |
| **Wireless**      | WiFi (Pico W chip)              | WiFi, BLE, LoRa                |
| **CAN**           | External MCP2515 (SPI)          | Built-in TWAI (CAN 2.0)        |

## RP2350 (Pico 2 W) Patterns

### Embassy Async Runtime

**Location**: `mcu/bins/rp2350/src/main.rs`

**Key Points to Review:**
- [ ] `#[embassy_executor::main]` on main function
- [ ] Async main signature: `async fn main(spawner: Spawner)`
- [ ] Tasks spawned with `spawner.spawn(task_name()).unwrap()`
- [ ] All peripherals initialized before spawning tasks
- [ ] Interrupt bindings with `bind_interrupts!` macro

**Example Pattern:**
```rust
// Good: Embassy async main
#[embassy_executor::main]
async fn main(spawner: Spawner) {
    // 1. Initialize peripherals
    let p = embassy_rp::init(Default::default());

    // 2. Bind interrupts
    bind_interrupts!(struct Irqs {
        USBCTRL_IRQ => InterruptHandler<USB>;
    });

    // 3. Create drivers
    let driver = Driver::new(p.USB, Irqs);

    // 4. Spawn tasks
    spawner.spawn(usb_task(driver)).unwrap();
    spawner.spawn(led_controller_task(p.PIO0)).unwrap();

    // 5. Main loop (or empty if all work in tasks)
    loop {
        Timer::after_millis(1000).await;
    }
}
```

**Red Flags:**
- Blocking calls in async context (`std::thread::sleep`)
- Missing `.await` on async operations
- Unwrapping spawner (should handle spawn errors)
- Peripherals not moved into tasks (ownership violation)

### Embassy Tasks

**Key Points to Review:**
- [ ] Task functions marked with `#[embassy_executor::task]`
- [ ] Async signature
- [ ] Infinite loop or explicit return
- [ ] Error handling (log errors, don't panic)

**Example Pattern:**
```rust
// Good: Embassy task
#[embassy_executor::task]
async fn led_controller_task(mut pio: PIO0) {
    loop {
        // Wait for command
        let cmd = LED_COMMAND_CHANNEL.receive().await;

        // Update LEDs
        match update_leds(&mut pio, cmd) {
            Ok(_) => {}
            Err(e) => error!("LED update failed: {:?}", e),
        }
    }
}
```

### Static Memory Allocation

**Purpose**: No heap allocator in RP2350, all memory must be static.

**Key Points to Review:**
- [ ] `StaticCell` used for static mut data
- [ ] Global statics wrapped in `static` with `StaticCell`
- [ ] No `Box`, `Vec`, `String` (heap types)
- [ ] Arrays with fixed sizes

**Example Pattern:**
```rust
use embassy_sync::blocking_mutex::raw::CriticalSectionRawMutex;
use embassy_sync::channel::{Channel, Sender, Receiver};
use static_cell::StaticCell;

// Good: Static channel for inter-task communication
static LED_CHANNEL: StaticCell<Channel<CriticalSectionRawMutex, LedCommand, 8>> = StaticCell::new();

fn init_channel() -> &'static Channel<CriticalSectionRawMutex, LedCommand, 8> {
    LED_CHANNEL.init(Channel::new())
}

// Good: Static USB buffers
static EP_MEMORY: StaticCell<[u8; 1024]> = StaticCell::new();
static CONFIG_DESC: StaticCell<[u8; 256]> = StaticCell::new();

// Bad: Heap allocation (won't compile in no_std without alloc)
// let vec = vec![1, 2, 3];  // ❌ No Vec
// let string = String::from("hello");  // ❌ No String
```

**Red Flags:**
- Heap types (`Vec`, `String`, `Box`)
- Missing `StaticCell` wrapper for static mut
- Unbounded buffers (use fixed-size arrays)

**See**: [rp2350-patterns.md](rp2350-patterns.md) for detailed patterns.

### PIO for WS2812 LEDs

**Purpose**: Programmable I/O state machine generates precise timing for WS2812 protocol.

**Key Points to Review:**
- [ ] PIO program loaded with `pio.load_program()`
- [ ] State machine configured with correct frequency
- [ ] DMA used for efficient data transfer
- [ ] Color data in GRB format (not RGB)

**WS2812 Protocol**:
- **Bit 0**: 400ns high, 850ns low
- **Bit 1**: 800ns high, 450ns low
- **Reset**: >50µs low

**Example Pattern:**
```rust
// Good: PIO-based WS2812 driver
use embassy_rp::pio::{Pio, Common, StateMachine};

async fn init_ws2812(pio: PIO0, pin: PIN_25) -> Ws2812<'static> {
    let Pio { mut common, sm0, .. } = Pio::new(pio);

    // Load PIO program (bit-bangs WS2812 protocol)
    let prg = pio_proc::pio_asm!(
        ".side_set 1 opt",
        ".wrap_target",
        "bitloop:",
        "  out x, 1       side 0 [1]",  // Shift out 1 bit
        "  jmp !x do_zero side 1 [2]",  // High if bit 1
        "do_one:",
        "  jmp bitloop    side 1 [4]",  // Stay high (800ns)
        "do_zero:",
        "  nop            side 0 [4]",  // Go low (400ns)
        ".wrap"
    );

    let program = common.load_program(&prg.program);

    // Configure state machine
    let mut cfg = Config::default();
    cfg.set_out_pins(&[&pin]);
    cfg.set_clock_divider(125);  // 800kHz for WS2812 timing

    let ws2812 = Ws2812::new(sm0, pin, program, cfg);
    ws2812
}

// Send color data (GRB format!)
async fn set_led_color(ws2812: &mut Ws2812<'_>, index: usize, r: u8, g: u8, b: u8) {
    let color = ((g as u32) << 16) | ((r as u32) << 8) | (b as u32);  // GRB
    ws2812.write(&[color]).await;
}
```

**Red Flags:**
- RGB byte order (should be GRB for WS2812)
- Incorrect clock divider (breaks timing)
- Blocking write (should use DMA + await)
- Missing reset delay (>50µs)

### USB CDC Serial

**Purpose**: USB serial for debugging and SLCAN bridge.

**Key Points to Review:**
- [ ] USB driver created with `Driver::new()`
- [ ] CDC-ACM class instantiated
- [ ] Read/write methods awaited
- [ ] Line coding handled (baud rate, etc.)

**Example Pattern:**
```rust
use embassy_usb::class::cdc_acm::{CdcAcmClass, State};

#[embassy_executor::task]
async fn usb_task(driver: Driver<'static, USB>) {
    let mut config = embassy_usb::Config::new(0x1234, 0x5678);
    config.manufacturer = Some("Muni Robotics");
    config.product = Some("BVR LED Controller");

    let mut builder = Builder::new(driver, config, /* ... */);

    // Create CDC-ACM class
    let mut state = State::new();
    let mut cdc = CdcAcmClass::new(&mut builder, &mut state, 64);

    let usb = builder.build();

    loop {
        // Read from USB
        let mut buf = [0u8; 64];
        let n = cdc.read_packet(&mut buf).await.unwrap();

        // Echo back (for testing)
        cdc.write_packet(&buf[..n]).await.unwrap();
    }
}
```

## ESP32-S3 (Heltec) Patterns

### Polling Loop (No Async)

**Location**: `mcu/bins/esp32s3/src/main.rs`

**Key Points to Review:**
- [ ] `#[main]` entry point (not `#[embassy_executor::main]`)
- [ ] Infinite loop with non-blocking checks
- [ ] `delay.delay_millis()` for timing
- [ ] UART `read_ready()` for non-blocking reads

**Example Pattern:**
```rust
// Good: Polling loop
#[main]
fn main() -> ! {
    // 1. Initialize peripherals
    let peripherals = Peripherals::take();
    let mut delay = Delay::new();

    // 2. Initialize UART
    let mut uart = Uart::new(peripherals.UART0, /* ... */);

    // 3. Main loop
    loop {
        // Non-blocking UART read
        if uart.read_ready() {
            let mut buf = [0u8; 64];
            if let Ok(n) = uart.read(&mut buf) {
                process_command(&buf[..n]);
            }
        }

        // Update LEDs
        update_leds();

        // Small delay (don't busy-wait)
        delay.delay_millis(1);
    }
}
```

**Red Flags:**
- Blocking reads (`uart.read()` without `read_ready()`)
- Busy-wait loop (no delay)
- Async/await syntax (ESP32 uses blocking)

**See**: [esp32s3-patterns.md](esp32s3-patterns.md) for detailed patterns.

### Heap Allocation (esp-alloc)

**Purpose**: ESP32-S3 has a heap allocator, allows `Vec`, `String`, etc.

**Key Points to Review:**
- [ ] `esp_alloc::heap_allocator!()` called in main
- [ ] Heap types used sparingly (still embedded)
- [ ] Fixed-size buffers preferred for critical paths
- [ ] No unbounded growth (memory leaks)

**Example Pattern:**
```rust
use esp_alloc as _;

#[main]
fn main() -> ! {
    // Initialize heap allocator
    esp_alloc::heap_allocator!();

    // Now can use heap types (use sparingly!)
    let mut buffer = Vec::with_capacity(256);  // Pre-allocate

    loop {
        // Heap allocation okay for non-critical paths
        let message = String::from("Status: OK");
        send_message(&message);

        buffer.clear();  // Reuse buffer (don't re-allocate)
    }
}
```

**Best Practice**: Use heap for initialization and infrequent operations, not in hot loops.

### RMT for WS2811/WS2812 LEDs

**Purpose**: Remote Control Transceiver generates precise pulse sequences.

**Key Points to Review:**
- [ ] RMT channel configured with correct clock
- [ ] Pulse sequences match WS2812 timing
- [ ] Blocking transmit or interrupt-driven
- [ ] Memory limits (8 RMT channels, 64 items each)

**Example Pattern:**
```rust
use esp_hal::rmt::{Rmt, TxChannel};

fn init_rmt_leds(rmt: RMT, pin: GPIO48) -> TxChannel<'static, 0> {
    let rmt = Rmt::new(rmt, 80u32.MHz()).unwrap();  // 80MHz clock

    let tx_config = TxChannelConfig {
        clk_divider: 1,
        idle_output_level: false,
        carrier_modulation: false,
        idle_output: true,
    };

    let mut channel = rmt.channel0.configure(pin, tx_config).unwrap();

    // WS2812 pulse timings (in RMT ticks)
    // Bit 0: 400ns high, 850ns low
    // Bit 1: 800ns high, 450ns low
    // Each tick = 12.5ns at 80MHz

    channel
}

fn send_pixel(channel: &mut TxChannel, r: u8, g: u8, b: u8) {
    let grb = ((g as u32) << 16) | ((r as u32) << 8) | (b as u32);  // GRB order

    for bit in (0..24).rev() {
        let is_one = (grb >> bit) & 1 == 1;
        let (high, low) = if is_one {
            (64, 32)  // 800ns, 400ns at 80MHz
        } else {
            (32, 64)  // 400ns, 800ns
        };

        channel.transmit(&[(high, true, low, false)]).unwrap();
    }
}
```

**Red Flags:**
- RGB byte order (should be GRB)
- Incorrect timing calculations
- RMT buffer overflow (>64 items)

### OLED Display (SSD1306)

**Purpose**: Status display for standalone operation.

**Key Points to Review:**
- [ ] I2C initialized with correct frequency
- [ ] SSD1306 driver initialized
- [ ] Display cleared on startup
- [ ] Updates not too frequent (I2C is slow)

**Example Pattern:**
```rust
use ssd1306::{Ssd1306, mode::BufferedGraphicsMode, prelude::*, I2CDisplayInterface};

fn init_display(i2c: I2C0, sda: GPIO17, scl: GPIO18) -> Ssd1306<I2CInterface<I2C0>, ...> {
    let i2c = I2c::new(i2c, sda, scl, 400u32.kHz()).unwrap();
    let interface = I2CDisplayInterface::new(i2c);

    let mut display = Ssd1306::new(interface, DisplaySize128x64, DisplayRotation::Rotate0)
        .into_buffered_graphics_mode();

    display.init().unwrap();
    display.clear();
    display.flush().unwrap();

    display
}

fn update_status(display: &mut Ssd1306<...>, status: &str) {
    display.clear();
    Text::new(status, Point::new(0, 0), MonoTextStyle::new(&FONT_6X10, BinaryColor::On))
        .draw(display)
        .unwrap();
    display.flush().unwrap();
}
```

## LED Controller Library

**Location**: `mcu/crates/mcu-leds/src/lib.rs`

### LED Mode State Machine

**Purpose**: Manage LED patterns for rover state indication.

**Key Points to Review:**
- [ ] `LedMode` enum with all patterns (Off, Solid, Pulse, Chase, Flash)
- [ ] State machine updates mode based on CAN messages
- [ ] Smooth transitions with wipe animation
- [ ] Convenience methods for rover states (`idle()`, `teleop()`, etc.)

**LED Modes:**
- `Off`: All LEDs off
- `Solid(r, g, b, brightness)`: Fixed color
- `Pulse(r, g, b, period_ms)`: Breathing effect (sine wave)
- `Flash(r, g, b, period_ms)`: On/off strobe
- `Chase(r, g, b, speed)`: Moving pattern

**Rover State Convenience Methods:**
```rust
impl LedMode {
    pub fn idle() -> Self {
        Self::Solid(0, 0, 255, 200)  // Blue solid
    }

    pub fn teleop() -> Self {
        Self::Pulse(0, 255, 0, 2000)  // Green pulse, 2s period
    }

    pub fn autonomous() -> Self {
        Self::Pulse(0, 255, 255, 1500)  // Cyan pulse, 1.5s period
    }

    pub fn estop() -> Self {
        Self::Flash(255, 0, 0, 200)  // Red flash, 200ms (urgent!)
    }

    pub fn fault() -> Self {
        Self::Flash(255, 165, 0, 500)  // Orange flash, 500ms
    }
}
```

**Key Points to Review:**
- [ ] E-stop flash is fast (200ms) for maximum visibility
- [ ] Pulse periods reasonable (1-3 seconds)
- [ ] Brightness clamped to [0, 255]
- [ ] Color values clamped to [0, 255]

### Animation System

**Purpose**: Smooth transitions and effects.

**Key Points to Review:**
- [ ] Wipe transition with soft edge (gradient blend)
- [ ] Pulse uses sine wave (smooth breathing)
- [ ] Chase wraps around LED strip
- [ ] Frame rate consistent (30-60 Hz)

**Pulse Animation:**
```rust
// Good: Sine wave pulse
fn pulse_brightness(base: u8, time_ms: u32, period_ms: u32) -> u8 {
    let phase = (time_ms % period_ms) as f32 / period_ms as f32;
    let sine = ((phase * 2.0 * PI).sin() + 1.0) / 2.0;  // 0.0 to 1.0
    let min_brightness = base / 2;
    let max_brightness = base;

    (min_brightness as f32 + (max_brightness - min_brightness) as f32 * sine) as u8
}
```

## CAN Attachment Protocol

**Location**: `mcu/crates/mcu-core/src/protocol.rs`

### ID Scheme

**CAN ID Range:** 0x200-0x2FF (16 attachment slots, 0x10 offset each)

**Per-Attachment Messages** (8 message types per attachment):
- `+0x00`: Heartbeat (A → H, periodic beacon)
- `+0x01`: Identify request (H → A, query identity)
- `+0x02`: Identity response (A → H, device info)
- `+0x03`: Command (H → A, control attachment)
- `+0x04`: Acknowledgment (A → H, command ACK)
- `+0x05`: Sensor data (A → H, periodic readings)
- `+0x06`: Configuration (H → A, set parameters)
- `+0x07`: Error report (A → H, fault indication)

**Example**: Attachment 0 (base 0x200)
- Heartbeat: 0x200
- Command: 0x203
- Sensor: 0x205

**Key Points to Review:**
- [ ] CAN IDs calculated as `BASE + SLOT * 0x10 + OFFSET`
- [ ] Extended CAN IDs used (29-bit)
- [ ] Heartbeat sent at 1 Hz
- [ ] Commands acknowledged within 100ms

**See**: Firmware skill [can-protocol.md](../firmware-review/can-protocol.md) for full protocol.

## SLCAN Protocol

**Purpose**: Serial Line CAN bridge for debugging via USB.

**Location**: `mcu/bins/esp32s3/src/slcan.rs`

### Frame Format

**Standard Frame**:
```
t<ID><LEN><DATA>\r
```

**Extended Frame**:
```
T<ID><LEN><DATA>\r
```

**Example**:
```
T00000B0010A\r       # Extended ID 0x0B00, length 1, data 0x0A
t10348AABBCCDD\r     # Standard ID 0x103, length 4, data 0xAABBCCDD
```

### Commands

| Command | Description                 | Response    |
|---------|-----------------------------|-------------|
| `O\r`   | Open CAN bus                | `\r` (OK)   |
| `C\r`   | Close CAN bus               | `\r`        |
| `S4\r`  | Set bitrate to 500kbps      | `\r`        |
| `V\r`   | Get version                 | `V1234\r`   |
| `N\r`   | Get serial number           | `NABCD\r`   |

**Key Points to Review:**
- [ ] Frame parsing validates ID length (3 or 8 hex digits)
- [ ] Data length checked (0-8 bytes)
- [ ] Invalid commands return error (e.g., `\x07`)
- [ ] Carriage return (`\r`) terminates every message

**Example Pattern:**
```rust
// Good: SLCAN command parsing
fn parse_slcan(cmd: &[u8]) -> Result<SlcanCommand, SlcanError> {
    if cmd.is_empty() || cmd[cmd.len() - 1] != b'\r' {
        return Err(SlcanError::MissingCR);
    }

    match cmd[0] {
        b'O' => Ok(SlcanCommand::Open),
        b'C' => Ok(SlcanCommand::Close),
        b'S' => {
            // Parse bitrate (S0-S8)
            let rate = cmd[1] - b'0';
            if rate > 8 {
                return Err(SlcanError::InvalidBitrate);
            }
            Ok(SlcanCommand::SetBitrate(rate))
        }
        b't' => parse_standard_frame(&cmd[1..]),
        b'T' => parse_extended_frame(&cmd[1..]),
        _ => Err(SlcanError::UnknownCommand),
    }
}
```

**See**: [esp32s3-patterns.md](esp32s3-patterns.md) for full SLCAN implementation.

## Memory Constraints

### RP2350 (Pico 2 W)

**SRAM**: 520 KB total
- Stack: ~16 KB
- Static data: ~50 KB (USB buffers, channels, etc.)
- Available: ~450 KB

**Flash**: 4 MB
- Program: ~100 KB
- Data: Plenty of space

**Key Points to Review:**
- [ ] Stack size reasonable (<16 KB)
- [ ] No large arrays on stack (use static)
- [ ] StaticCell used for static mut data
- [ ] No unbounded recursion

### ESP32-S3 (Heltec)

**SRAM**: 512 KB total
- Heap: ~400 KB (configurable)
- Stack: ~8 KB per task
- DMA: ~50 KB

**Flash**: 8 MB
- Program: ~500 KB
- SPIFFS/LittleFS: ~7 MB

**Key Points to Review:**
- [ ] Heap allocations tracked (no leaks)
- [ ] Large buffers allocated once (not per loop)
- [ ] Stack size per task reasonable

## Testing Embedded Code

### Unit Tests (no_std)

**Key Points to Review:**
- [ ] `#[cfg(test)]` module for unit tests
- [ ] Tests use `#[test]` attribute
- [ ] Mock hardware with traits
- [ ] No `std` imports in tests

**Example Pattern:**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_led_mode_pulse() {
        let mode = LedMode::Pulse(255, 0, 0, 1000);
        match mode {
            LedMode::Pulse(r, g, b, period) => {
                assert_eq!(r, 255);
                assert_eq!(period, 1000);
            }
            _ => panic!("Wrong mode"),
        }
    }
}
```

### Integration Tests (on-device)

**Pattern**: Use `defmt` logging and probe-rs for debugging.

```bash
# Flash and run with logging
cargo run --release
# or
probe-rs run --chip RP2350
```

## Common Mistakes

### ❌ Async on ESP32-S3
```rust
// WRONG: ESP32 doesn't use Embassy
#[embassy_executor::main]
async fn main(spawner: Spawner) {  // ❌ Won't compile
    // ...
}
```

### ✅ Correct ESP32-S3 Entry
```rust
// CORRECT: Blocking main
#[main]
fn main() -> ! {
    loop {
        // ...
    }
}
```

### ❌ Heap Types on RP2350
```rust
// WRONG: No heap allocator
let vec = vec![1, 2, 3];  // ❌ Won't compile (no alloc)
```

### ✅ Correct RP2350 Storage
```rust
// CORRECT: Static array
static DATA: StaticCell<[u8; 16]> = StaticCell::new();
```

### ❌ RGB Instead of GRB
```rust
// WRONG: WS2812 expects GRB
let color = (r as u32) << 16 | (g as u32) << 8 | b as u32;  // ❌ RGB
```

### ✅ Correct GRB Order
```rust
// CORRECT: GRB for WS2812
let color = (g as u32) << 16 | (r as u32) << 8 | b as u32;  // ✅ GRB
```

## References and Additional Resources

For more detailed information, see:
- [rp2350-patterns.md](rp2350-patterns.md) - Embassy async, StaticCell, PIO usage
- [esp32s3-patterns.md](esp32s3-patterns.md) - Polling loop, RMT, esp-alloc, SLCAN
- [CLAUDE.md](/Users/cam/Developer/muni/CLAUDE.md) - Project-wide conventions
- Firmware skill [can-protocol.md](../firmware-review/can-protocol.md) - CAN attachment protocol

## Quick Review Commands

```bash
# Build RP2350
cd mcu
cargo build --release -p rover-leds

# Build ESP32-S3
cd mcu/bins/esp32s3
cargo build --release

# Flash RP2350 (requires picotool)
picotool load target/thumbv8m.main-none-eabihf/release/rover-leds -t elf -f

# Flash ESP32-S3 (requires espflash)
espflash flash --monitor target/xtensa-esp32s3-none-elf/release/heltec-attachment
```
