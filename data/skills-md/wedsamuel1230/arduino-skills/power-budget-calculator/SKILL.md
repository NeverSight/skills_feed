---
name: power-budget-calculator
description: Calculates total power consumption and battery life for Arduino/ESP32/RP2040 projects. Use when user asks about battery life, power requirements, current draw, or needs to estimate runtime. Includes sleep mode analysis, power optimization tips, and battery sizing recommendations. Run scripts/calculate_power.py for accurate calculations.
---

# Power Budget Calculator

Estimates power consumption and battery life for embedded projects.

## Resources

- **scripts/calculate_power.py** - Python calculator with component database, duty cycle support, battery life estimation
- **references/component-database.md** - Comprehensive current draw reference from datasheets  
- **assets/example-project.json** - Sample project configuration

## Quick Start

Run the calculator interactively:
```bash
uv run --no-project scripts/calculate_power.py --interactive
```

Or calculate for a single component:
```bash
uv run --no-project scripts/calculate_power.py --component ESP32 --mode deep_sleep --duty 95
```

Load a project configuration:
```bash
uv run --no-project scripts/calculate_power.py --json assets/example-project.json --output report.md
```

List all components in database:
```bash
uv run --no-project scripts/calculate_power.py --list
```

## When to Use
- "How long will my battery last?"
- "What size battery do I need?"
- "How much current does my project draw?"
- Planning battery-powered projects
- Optimizing for low power

## Workflow

### Step 1: Gather Component List

Ask user for:
1. Microcontroller (model and operating mode)
2. All sensors and modules
3. Displays
4. Actuators (motors, LEDs, relays)
5. Communication (WiFi, Bluetooth, LoRa)
6. Operating profile (always on vs. duty cycle)

### Step 2: Calculate Power Budget

Run `scripts/calculate_power.py --interactive` for guided calculation, or use this template:

```markdown
# Power Budget: [Project Name]

## Operating Conditions
- Supply Voltage: [V]
- Operating Modes: [Active/Sleep cycles]
- Duty Cycle: [X% active, Y% sleep]

## Component Current Draw

### Always-On Components
| Component | Voltage | Current | Power | Notes |
|-----------|---------|---------|-------|-------|
| [name] | [V] | [mA] | [mW] | [conditions] |
| ... | ... | ... | ... | ... |
| **Subtotal** | - | **[mA]** | **[mW]** | - |

### Active Mode Only
| Component | Voltage | Current | Power | Duty % |
|-----------|---------|---------|-------|--------|
| [name] | [V] | [mA] | [mW] | [%] |
| ... | ... | ... | ... | ... |
| **Subtotal** | - | **[mA]** | **[mW]** | - |

### Peak Current Events
| Event | Current | Duration | Frequency |
|-------|---------|----------|-----------|
| [WiFi TX] | [mA] | [ms] | [per hour] |
| ... | ... | ... | ... |

## Power Calculations

### Average Current
```
I_avg = (I_active × t_active + I_sleep × t_sleep) / t_total
I_avg = ([X]mA × [Y]s + [Z]mA × [W]s) / [T]s
I_avg = [result] mA
```

### Battery Life Estimate
```
Capacity: [X] mAh
Efficiency factor: 0.8 (80% usable)
Effective capacity: [X × 0.8] mAh

Runtime = Effective capacity / I_avg
Runtime = [X] mAh / [Y] mA
Runtime = [Z] hours ([days] days)
```

## Recommendations
- [Power optimization suggestions]
- [Battery type recommendation]
- [Sleep mode configuration]
```

## Current Draw Database

### Microcontrollers

#### Arduino (ATmega328P @ 5V)
| Mode | Current | Notes |
|------|---------|-------|
| Active (16MHz) | 15-20mA | No peripherals |
| Idle | 6mA | CPU stopped, peripherals on |
| Power-down | 0.1µA | Only WDT/external interrupt |
| With USB-Serial | +50mA | CH340/FTDI chip always on |

#### ESP32 (WROOM-32)
| Mode | Current | Notes |
|------|---------|-------|
| Active (WiFi TX) | 160-260mA | Peak during transmission |
| Active (WiFi RX) | 95-100mA | Listening |
| Active (no WiFi) | 20-68mA | CPU only |
| Modem-sleep | 20mA | WiFi off, CPU on |
| Light-sleep | 0.8mA | CPU paused |
| Deep-sleep | 10µA | RTC only |
| Hibernation | 5µA | RTC off |

#### ESP32-C3
| Mode | Current | Notes |
|------|---------|-------|
| Active (WiFi TX) | 320mA peak | Brief spikes |
| Active (BLE) | 50-100mA | During advertising |
| Active (no radio) | 25-35mA | CPU at 160MHz |
| Light-sleep | 130µA | Auto wake |
| Deep-sleep | 5µA | RTC on |

#### RP2040 (Pico)
| Mode | Current | Notes |
|------|---------|-------|
| Active (both cores) | 25-50mA | Depends on clock |
| Single core | 15-25mA | One core dormant |
| Dormant | 0.18mA | Wake on GPIO/RTC |
| Sleep | 1.3mA | |

#### RP2040 (Pico W)
| Mode | Current | Notes |
|------|---------|-------|
| WiFi active | 50-150mA | During TX |
| WiFi idle | 30-40mA | Connected, listening |
| WiFi off | 25-50mA | Radio disabled |

### Sensors

| Sensor | Active | Sleep | Notes |
|--------|--------|-------|-------|
| DHT22 | 1.5mA | 50µA | During read |
| BME280 | 0.35mA | 0.1µA | Forced mode |
| BMP280 | 0.27mA | 0.1µA | |
| MPU6050 | 3.8mA | 5µA | All axes |
| DS18B20 | 1.5mA | 1µA | During conversion |
| HC-SR04 | 15mA | 2mA | No true sleep |
| VL53L0X | 19mA | 5µA | During ranging |
| MAX30102 | 600µA | 0.7µA | Low power mode |
| BH1750 | 120µA | 1µA | Power down mode |
| GPS (NEO-6M) | 45mA | 11mA | Backup mode |

### Displays

| Display | Active | Off/Sleep | Notes |
|---------|--------|-----------|-------|
| 16x2 LCD (backlight) | 80-120mA | 1mA | Backlight dominates |
| 16x2 LCD (no backlight) | 1-2mA | 1mA | |
| SSD1306 OLED 128x64 | 8-20mA | 10µA | Depends on content |
| SSD1306 OLED 128x32 | 5-15mA | 10µA | |
| ST7735 TFT | 20-40mA | 20mA | Backlight always on |
| ILI9341 TFT | 50-80mA | 50mA | |
| E-Paper 2.9" | 8mA | 0µA | Only during refresh |

### Communication Modules

| Module | TX Peak | RX/Idle | Sleep | Notes |
|--------|---------|---------|-------|-------|
| ESP8266 (module) | 170mA | 70mA | 20µA | Deep sleep |
| NRF24L01 | 11.3mA | 13.5mA | 0.9µA | |
| HC-05 Bluetooth | 40mA | 8mA | 2mA | |
| RFM95 LoRa | 120mA | 10mA | 0.2µA | |
| SIM800L GSM | 2A peak | 15mA | 1mA | Needs big cap! |

### Actuators

| Component | Current | Notes |
|-----------|---------|-------|
| LED (typical) | 10-20mA | Through resistor |
| RGB LED (each color) | 20mA | Per channel |
| WS2812B NeoPixel | 60mA max | Full white |
| SG90 Servo (idle) | 10mA | No load |
| SG90 Servo (moving) | 200-500mA | Under load |
| MG996R Servo | 500-900mA | Under load |
| Small DC motor | 100-500mA | Varies with load |
| 5V Relay module | 70-100mA | Coil energized |
| Buzzer (passive) | 30mA | |

## Sleep Mode Configurations

### ESP32 Deep Sleep Template
```cpp
#include <esp_sleep.h>

#define uS_TO_S_FACTOR 1000000ULL
#define TIME_TO_SLEEP 60  // seconds

void setup() {
    // Do measurements here
    
    // Configure wake-up source
    esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
    
    // Enter deep sleep
    esp_deep_sleep_start();
}

void loop() {
    // Never reached
}
```

### Arduino Power-Down Template
```cpp
#include <avr/sleep.h>
#include <avr/wdt.h>

void enterSleep() {
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    sleep_enable();
    sleep_mode();  // Sleep here
    sleep_disable();
}

// Wake on watchdog or external interrupt
ISR(WDT_vect) {
    // Wake up
}
```

## Power Optimization Checklist

### Hardware
- [ ] Remove power LED (saves 5-10mA)
- [ ] Remove USB-Serial chip for battery operation
- [ ] Use LDO with low quiescent current (<10µA)
- [ ] Add MOSFET to power-gate high-current peripherals
- [ ] Use pull-downs on unused pins
- [ ] Disable ADC when not reading

### Software
- [ ] Use sleep modes between readings
- [ ] Reduce clock speed if possible
- [ ] Batch data and transmit less frequently
- [ ] Turn off WiFi/BLE when not needed
- [ ] Disable brown-out detector in deep sleep
- [ ] Use interrupts instead of polling

### Design Patterns

**Power Gating:**
```
       VCC
        │
    [P-MOSFET] ← GPIO (LOW = ON)
        │
    [Sensor/Module]
        │
       GND
```

**Duty Cycling Formula:**
```
I_average = (I_active × T_active + I_sleep × T_sleep) / T_total

Example: Sensor reads every 5 minutes
- Active: 50mA for 2 seconds
- Sleep: 10µA for 298 seconds

I_avg = (50mA × 2s + 0.01mA × 298s) / 300s
I_avg = (100 + 2.98) / 300
I_avg = 0.34mA

With 2000mAh battery:
Runtime = 2000mAh × 0.8 / 0.34mA = 4706 hours = 196 days
```

## Battery Reference

### Common Battery Types

| Type | Voltage | Typical Capacity | Notes |
|------|---------|------------------|-------|
| CR2032 | 3V | 220mAh | Very low current only |
| 2x AA Alkaline | 3V | 2500mAh | Good for low power |
| 3x AA Alkaline | 4.5V | 2500mAh | Direct to 5V systems |
| 4x AA Alkaline | 6V | 2500mAh | With LDO to 5V |
| 18650 Li-ion | 3.7V | 2000-3500mAh | Rechargeable, popular |
| LiPo 1S | 3.7V | Various | Flat, light |
| 9V Alkaline | 9V | 500mAh | Poor energy density |

### Voltage Over Discharge

**18650/LiPo Discharge Curve:**
```
Capacity%   Voltage
─────────────────────
100%        4.2V
80%         3.9V
50%         3.7V
20%         3.5V
0%          3.0V (cut-off!)

Never discharge below 3.0V - damages cell!
```

**Alkaline AA Discharge:**
```
Capacity%   Voltage (per cell)
─────────────────────────────
100%        1.5V
50%         1.2V
0%          0.9V

Many devices stop working below 1.1V/cell
```

## Quick Calculator

```
Enter your values:

Always-on current: ______ mA
Active current: ______ mA
Active time: ______ seconds
Sleep current: ______ mA  
Sleep time: ______ seconds
Battery capacity: ______ mAh

Average current = (Active_mA × Active_s + Sleep_mA × Sleep_s) / Total_s
                = (_____ × _____ + _____ × _____) / _____
                = _____ mA

Runtime = Capacity × 0.8 / Average_current
        = _____ × 0.8 / _____
        = _____ hours
        = _____ days
```
