---
name: esp32-rust-embedded
description: Expert embedded Rust development for ESP32 microcontrollers using no-std, Embassy async framework, and the ESP-RS ecosystem (esp-hal, esp-rtos, esp-radio). Use when building, debugging, flashing, or adding features to ESP32 projects. Covers sensor integration (ADC, GPIO, I2C, SPI), power management (deep sleep, RTC memory), WiFi networking, MQTT clients, display drivers, async task patterns, memory allocation, error handling, and dependency management. Ideal for LilyGO boards, Espressif chips (ESP32, ESP32-S3, ESP32-C3), and any no-std Xtensa/RISC-V embedded development.
compatibility: Requires ESP Rust toolchain (espup), cargo-espflash, and ESP32/ESP32-S3/ESP32-C3 hardware. Designed for Claude Code and similar AI coding assistants.
---

# ESP32 Embedded Rust Specialist

Expert guidance for no-std Rust development on ESP32 microcontrollers using the ESP-RS ecosystem and Embassy async framework.

## ESP-RS Ecosystem Stack

### Core Dependencies
```toml
esp-hal = { version = "1.0.0", features = ["esp32s3", "log-04", "unstable"] }
esp-rtos = { version = "0.2.0", features = ["embassy", "esp-alloc", "esp-radio", "esp32s3", "log-04"] }
esp-radio = { version = "0.17.0", features = ["esp-alloc", "esp32s3", "wifi", "smoltcp"] }
esp-bootloader-esp-idf = { version = "0.4.0", features = ["esp32s3", "log-04"] }
```

### Embassy Framework
```toml
embassy-executor = { version = "0.9.1", features = ["log"] }
embassy-time = { version = "0.5.0", features = ["log"] }
embassy-net = { version = "0.7.1", features = ["dhcpv4", "tcp", "udp", "dns"] }
embassy-sync = { version = "0.7.2" }
```

### Dependency Hierarchy
```
esp-radio (WiFi) -> esp-rtos (scheduler) -> esp-hal (HAL) -> esp-phy (PHY)
embassy-executor -> embassy-time -> embassy-sync -> embassy-net
```

## Build & Flash

### Environment Setup
```bash
# Install ESP toolchain (one-time)
espup install
source $HOME/export-esp.sh

# Configure credentials (.env file)
cp .env.dist .env
# Edit: WIFI_SSID, WIFI_PSK, MQTT_HOSTNAME, MQTT_USERNAME, MQTT_PASSWORD
```

### Build Commands
```bash
# Quick build and flash
./run.sh

# Manual release build (recommended)
cargo run --release

# Debug build (slower on device)
cargo run
```

### Cargo Profile Optimization
```toml
[profile.dev]
opt-level = "s"  # Rust debug too slow for ESP32

[profile.release]
lto = 'fat'
opt-level = 's'
codegen-units = 1
```

### Common Build Errors

**Linker error: undefined symbol `_stack_start`**
- Check `build.rs` has linkall.x configuration
- Verify esp-hal version compatibility

**undefined symbol: `esp_rtos_initialized`**
- Ensure esp-rtos is started with timer:
```rust
let timg0 = TimerGroup::new(peripherals.TIMG0);
esp_rtos::start(timg0.timer0);
```

**Environment variable errors**
- Variables are compile-time via `env!()` macro
- Changes require full rebuild

## No-Std Patterns

### Application Entry
```rust
#![no_std]
#![no_main]

use esp_rtos::main;

#[main]
async fn main(spawner: Spawner) {
    // Initialize logger
    init_logger(log::LevelFilter::Info);

    // Initialize HAL
    let peripherals = esp_hal::init(Config::default());

    // Setup heap allocator
    heap_allocator!(#[unsafe(link_section = ".dram2_uninit")] size: 73744);

    // Start RTOS scheduler
    let timg0 = TimerGroup::new(peripherals.TIMG0);
    esp_rtos::start(timg0.timer0);
}
```

### Memory Management
- Use `esp-alloc` for dynamic allocation
- Prefer `heapless` collections with compile-time capacity
- Use `static_cell::StaticCell` for 'static lifetime requirements

### String Handling
```rust
use alloc::string::String;      // Dynamic strings (heap)
use heapless::String;           // Bounded strings (stack)

let s: heapless::String<64> = heapless::String::new();
```
Avoid cloning when possible.

### StaticCell Pattern
```rust
static CHANNEL: StaticCell<Channel<NoopRawMutex, Data, 3>> = StaticCell::new();

// In async function
let channel: &'static mut _ = CHANNEL.init(Channel::new());
let (sender, receiver) = (channel.sender(), channel.receiver());
```

## Hardware Patterns

### GPIO Configuration
```rust
use esp_hal::gpio::{Level, Output, OutputConfig, Pull, DriveMode};

// Standard output
let pin = Output::new(peripherals.GPIO2, Level::Low, OutputConfig::default());

// Open-drain for sensors like DHT11
let pin = Output::new(
    peripherals.GPIO1,
    Level::High,
    OutputConfig::default()
        .with_drive_mode(DriveMode::OpenDrain)
        .with_pull(Pull::None),
).into_flex();
```

### ADC Reading with Calibration
```rust
use esp_hal::analog::adc::{Adc, AdcConfig, AdcCalCurve, Attenuation};

let mut adc_config = AdcConfig::new();
let pin = adc_config.enable_pin_with_cal::<_, AdcCalCurve<ADC2>>(
    peripherals.GPIO11,
    Attenuation::_11dB  // 0-3.3V range
);
let adc = Adc::new(peripherals.ADC2, adc_config);

// Read with nb::block!
let value = nb::block!(adc.read_oneshot(&mut pin))?;
```

### Peripheral Bundles Pattern
```rust
pub struct SensorPeripherals {
    pub dht11_pin: GPIO1<'static>,
    pub moisture_pin: GPIO11<'static>,
    pub power_pin: GPIO16<'static>,
    pub adc2: ADC2<'static>,
}
```

## Async Task Architecture

### Task Definition
```rust
#[embassy_executor::task]
pub async fn my_task(sender: Sender<'static, NoopRawMutex, Data, 3>) {
    loop {
        // Do work
        sender.send(data).await;
        Timer::after(Duration::from_secs(5)).await;
    }
}
```

### Task Spawning
```rust
spawner.spawn(sensor_task(sender, peripherals)).ok();
spawner.spawn(update_task(stack, display, receiver)).ok();
```

### Inter-Task Communication

**Channel (multiple values)**
```rust
use embassy_sync::{blocking_mutex::raw::NoopRawMutex, channel::Channel};

static CHANNEL: StaticCell<Channel<NoopRawMutex, Data, 3>> = StaticCell::new();
// sender.send(data).await / receiver.receive().await
```

**Signal (single notification)**
```rust
use embassy_sync::{blocking_mutex::raw::CriticalSectionRawMutex, signal::Signal};

static SIGNAL: Signal<CriticalSectionRawMutex, ()> = Signal::new();
// SIGNAL.signal(()) / SIGNAL.wait().await
```

### Reconnection Loop Pattern
```rust
'reconnect: loop {
    let mut client = initialize_client().await?;
    loop {
        match client.process().await {
            Ok(_) => { /* handle messages */ }
            Err(e) => {
                println!("Error: {:?}", e);
                continue 'reconnect;  // Reconnect on error
            }
        }
    }
}
```

## Power Management

### Deep Sleep Configuration
```rust
use esp_hal::rtc_cntl::{Rtc, sleep::{RtcSleepConfig, TimerWakeupSource, RtcioWakeupSource, WakeupLevel}};

pub fn enter_deep(wakeup_pin: &mut dyn RtcPin, rtc_cntl: LPWR, duration: Duration) -> ! {
    // GPIO wake source
    let wakeup_pins: &mut [(&mut dyn RtcPin, WakeupLevel)] = &mut [(wakeup_pin, WakeupLevel::Low)];
    let ext0 = RtcioWakeupSource::new(wakeup_pins);

    // Timer wake source
    let timer = TimerWakeupSource::new(duration.into());

    let mut rtc = Rtc::new(rtc_cntl);
    let mut config = RtcSleepConfig::deep();
    config.set_rtc_fastmem_pd_en(false);  // Keep RTC fast memory powered

    rtc.sleep(&config, &[&ext0, &timer]);
    unreachable!();
}
```

### RTC Fast Memory Persistence
```rust
use esp_hal::ram;

#[ram(unstable(rtc_fast))]
pub static BOOT_COUNT: RtcCell<u32> = RtcCell::new(0);

// Survives deep sleep - read/write with .get()/.set()
let count = BOOT_COUNT.get();
BOOT_COUNT.set(count + 1);
```

### Power Optimization
- Toggle sensor power pins only during reads
- Use power save mode on displays
- Gracefully disconnect WiFi before sleep
- Keep awake duration minimal

## WiFi Networking

### Connection Setup
```rust
use esp_radio::wifi::{self, ClientConfig, ModeConfig, WifiController};

let init = esp_radio::init().unwrap();
let (controller, interfaces) = wifi::new(&init, wifi_peripheral, Default::default()).unwrap();

let client_config = ModeConfig::Client(
    ClientConfig::default()
        .with_ssid(env!("WIFI_SSID").try_into().unwrap())
        .with_password(env!("WIFI_PSK").try_into().unwrap()),
);

controller.set_config(&client_config)?;
controller.start_async().await?;
controller.connect_async().await?;
```

### Embassy-Net Stack
```rust
use embassy_net::{Config, Stack, StackResources};

let config = Config::dhcpv4(DhcpConfig::default());
let (stack, runner) = embassy_net::new(wifi_interface, config, stack_resources, seed);

// Wait for link and IP
loop {
    if stack.is_link_up() { break; }
    Timer::after(Duration::from_millis(500)).await;
}

loop {
    if let Some(config) = stack.config_v4() {
        println!("IP: {}", config.address);
        break;
    }
    Timer::after(Duration::from_millis(500)).await;
}
```

### Graceful WiFi Shutdown
```rust
pub static STOP_WIFI_SIGNAL: Signal<CriticalSectionRawMutex, ()> = Signal::new();

// In connection task
STOP_WIFI_SIGNAL.wait().await;
controller.stop_async().await?;

// Before deep sleep
STOP_WIFI_SIGNAL.signal(());
```

## Sensor Patterns

### ADC Sampling with Warmup
```rust
async fn sample_adc_with_warmup<PIN, ADC>(
    adc: &mut Adc<ADC, Blocking>,
    pin: &mut AdcPin<PIN, ADC>,
    warmup_ms: u64,
) -> Option<u16> {
    Timer::after(Duration::from_millis(warmup_ms)).await;
    nb::block!(adc.read_oneshot(pin)).ok()
}
```

### Power-Controlled Sensor Read
```rust
async fn read_sensor(adc: &mut Adc, pin: &mut AdcPin, power: &mut Output) -> Option<u16> {
    power.set_high();
    let result = sample_adc_with_warmup(adc, pin, 50).await;
    power.set_low();
    result
}
```

### Outlier-Resistant Averaging
```rust
fn calculate_average<T: Copy + Ord + Into<u32>>(samples: &mut [T]) -> Option<T> {
    if samples.len() <= 2 { return None; }

    samples.sort_unstable();
    let trimmed = &samples[1..samples.len() - 1];  // Remove min/max

    let sum: u32 = trimmed.iter().map(|&x| x.into()).sum();
    (sum / trimmed.len() as u32).try_into().ok()
}
```

## Display Integration

### ST7789 Parallel Interface
```rust
use mipidsi::{Builder, options::ColorInversion};

let di = display_interface_parallel_gpio::Generic8BitBus::new(/*pins*/);
let mut display = Builder::new(ST7789, di)
    .display_size(320, 170)
    .invert_colors(ColorInversion::Inverted)
    .init(&mut delay)?;
```

### Power Save Mode
```rust
display.set_display_on(false)?;  // Enter power save
// Before deep sleep
power_pin.set_low();
```

## Error Handling

### Module Error Pattern
```rust
#[derive(Debug)]
pub enum Error {
    Wifi(WifiError),
    Display(display::Error),
    Mqtt(MqttError),
}

impl From<WifiError> for Error {
    fn from(e: WifiError) -> Self { Self::Wifi(e) }
}
```

### Fallible Main Pattern
```rust
#[main]
async fn main(spawner: Spawner) {
    if let Err(error) = main_fallible(spawner).await {
        println!("Error: {:?}", error);
        software_reset();
    }
}

async fn main_fallible(spawner: Spawner) -> Result<(), Error> {
    // Application logic with ? operator
}
```

## Dependency Updates

### Safe Update Process
```bash
cargo outdated
cargo update -p esp-hal
cargo build --release
cargo clippy -- -D warnings
```

### Breaking Change Patterns
- GPIO API changes frequently (OutputConfig)
- Timer initialization changes
- Feature flag renames
- Always check esp-hal release notes

### Version Alignment
Update Embassy crates together:
```bash
cargo update -p embassy-executor -p embassy-time -p embassy-sync -p embassy-net
```

## Debugging

### Serial Logging
```rust
use esp_println::println;
init_logger(log::LevelFilter::Info);
println!("Debug: value = {}", value);
```

### Common Runtime Issues
- **WiFi fails**: Check 2.4GHz network, signal strength
- **MQTT fails**: Verify DNS resolution, broker credentials
- **Sensors fail**: Check warmup delays, power pin toggling
- **Display blank**: Ensure GPIO15 is HIGH (power enable)
- **Sleep wake fails**: Verify RTC fast memory config

### Software Reset
```rust
use esp_hal::system::software_reset;
software_reset();  // Clean restart on unrecoverable error
```
