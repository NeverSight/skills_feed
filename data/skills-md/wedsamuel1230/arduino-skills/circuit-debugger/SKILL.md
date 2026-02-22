---
name: circuit-debugger
description: |
  Systematic hardware debugging guide for Arduino/ESP32/RP2040 circuits. Use when user reports: circuit not working, components getting hot, no power, intermittent failures, unexpected behavior, sensor not responding, LED not lighting, motor not spinning. Guides through power checks, continuity testing, signal tracing, and component isolation using multimeter techniques.
---

# Circuit Debugger

Systematic approach to diagnosing hardware issues in maker projects.

## Resources

This skill includes bundled tools and references:

- **scripts/generate_debug_sketch.py** - Arduino sketch generator for I2C scanner, GPIO tester, ADC checker, PWM tester
- **references/measurement-procedures.md** - Comprehensive multimeter and oscilloscope guide

## Quick Start

**Generate I2C scanner:**
```bash
uv run --no-project scripts/generate_debug_sketch.py --i2c --output i2c_scanner.ino
```

**Generate GPIO tester:**
```bash
uv run --no-project scripts/generate_debug_sketch.py --gpio --pins 2,3,4,5 --output gpio_test.ino
```

**Generate all debug sketches:**
```bash
uv run --no-project scripts/generate_debug_sketch.py --all
```

**Interactive mode:**
```bash
uv run --no-project scripts/generate_debug_sketch.py --interactive
```

## Trigger Phrases
- "My circuit doesn't work"
- "Component is getting hot"
- "No power to the board"
- "Sensor not responding"
- "Intermittent/random failures"
- "Works sometimes, not others"

## Debugging Protocol

### Phase 1: Power System Check (Do First!)

**Visual Inspection (30 seconds)**
```
□ Check for smoke, burn marks, or melted plastic
□ Verify power LED on microcontroller is lit
□ Look for loose wires or cold solder joints
□ Confirm correct polarity on polarized components (LEDs, caps, diodes)
```

**Multimeter Tests (Set to DC Voltage)**
```
Test Point              | Expected Value  | If Wrong
------------------------|-----------------|------------------
VCC to GND on MCU       | 3.3V or 5V      | Check regulator, power source
Sensor VCC pin          | Match datasheet | Check wiring, broken trace
Motor driver VCC        | Logic + Motor V | Separate supplies needed?
Battery terminals       | Rated voltage   | Dead/discharged battery
```

**Common Power Issues:**
| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| No voltage anywhere | Disconnected power, blown fuse | Check continuity from source |
| Low voltage (< 4V when expecting 5V) | Overloaded supply, bad regulator | Reduce load, check current draw |
| Voltage drops under load | Undersized power supply | Calculate total current, upgrade PSU |
| Reverse polarity | Swapped wires | Check all connections, may have damaged components |

### Phase 2: Ground Continuity

**Critical Rule:** All grounds must be connected together.

```
Multimeter: Set to CONTINUITY (beep mode)

Test these pairs - ALL should beep:
□ Arduino GND ↔ Sensor GND
□ Arduino GND ↔ Motor driver GND  
□ Arduino GND ↔ Display GND
□ Arduino GND ↔ Power supply negative
□ All breadboard GND rails connected
```

**Ground Problems Cause:**
- Erratic sensor readings
- I2C/SPI communication failures
- Motors behaving randomly
- Displays showing garbage

### Phase 3: Signal Verification

**Digital Signals (Set multimeter to DC Voltage)**
```cpp
// Add this debug code to verify pin states
void debugPins() {
    Serial.println("=== Pin States ===");
    Serial.print("D2: "); Serial.println(digitalRead(2) ? "HIGH" : "LOW");
    Serial.print("D3: "); Serial.println(digitalRead(3) ? "HIGH" : "LOW");
    // Add more pins as needed
}
```

**Expected Readings:**
| Signal Type | HIGH | LOW | Floating (Bad!) |
|-------------|------|-----|-----------------|
| 5V Logic | 4.5-5.5V | 0-0.5V | 1-3V unstable |
| 3.3V Logic | 2.8-3.6V | 0-0.3V | 0.8-2V unstable |

**I2C Troubleshooting:**
```cpp
// Run this I2C scanner first
#include <Wire.h>

void setup() {
    Serial.begin(115200);
    Wire.begin();
    
    Serial.println("I2C Scanner");
    for (uint8_t addr = 1; addr < 127; addr++) {
        Wire.beginTransmission(addr);
        if (Wire.endTransmission() == 0) {
            Serial.print("Found device at 0x");
            Serial.println(addr, HEX);
        }
    }
}
void loop() {}
```

| I2C Problem | Check |
|-------------|-------|
| No devices found | SDA/SCL swapped? Pull-ups present? Correct address? |
| Address conflict | Two devices same address? Check AD0/AD1 pins |
| Intermittent | Weak pull-ups (try 4.7kΩ), long wires, noise |

### Phase 4: Component Isolation

**The Divide-and-Conquer Method:**
```
1. Disconnect ALL external components
2. Verify MCU works alone (blink LED)
3. Add ONE component at a time
4. Test after EACH addition
5. When failure occurs, problem is last added component
```

**Component-Specific Tests:**

**LEDs:**
```
□ Correct polarity? (long leg = anode = positive)
□ Current limiting resistor present? (330Ω-1kΩ typical)
□ Test LED alone with battery + resistor
□ PWM pin? Try digitalWrite first
```

**Motors/Servos:**
```
□ Never connect directly to MCU pin (use driver!)
□ Separate power supply for motors
□ Flyback diode on DC motors
□ Check stall current vs driver rating
```

**Sensors:**
```
□ Correct operating voltage (3.3V vs 5V!)
□ Level shifter needed for mixed voltage?
□ Decoupling capacitor (100nF) near VCC pin
□ Pull-up resistors for I2C (4.7kΩ typical)
```

### Phase 5: Software vs Hardware

**Quick Software Test:**
```cpp
// Minimal test - does the MCU even run?
void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.begin(115200);
    Serial.println("MCU is alive!");
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
    Serial.println("heartbeat");
}
```

| If This Works | If This Fails |
|---------------|---------------|
| Hardware likely OK, check your code | Check USB cable, bootloader, board selection |

## Quick Reference: Common Failures

| Symptom | First Check | Second Check | Third Check |
|---------|-------------|--------------|-------------|
| Nothing works | Power supply | USB cable | Board selection in IDE |
| Gets hot | Short circuit | Reversed polarity | Overcurrent |
| Works then stops | Power brownout | Overheating | Memory leak |
| Erratic behavior | Floating inputs | Missing grounds | Noise/interference |
| I2C fails | Pull-ups | Address | Wire length |
| Motor jerky | Power supply | PWM frequency | Driver current |

## Multimeter Quick Guide

```
Measurement    | Setting      | Probes
---------------|--------------|------------------
DC Voltage     | V⎓ (20V)     | Red=signal, Black=GND
Continuity     | ))) or Ω     | Either direction
Resistance     | Ω            | Component out of circuit!
Current        | A or mA      | IN SERIES (break circuit)
```

## When to Ask for Help

If after this protocol you still can't find the issue:
1. Take clear photos of your wiring
2. Draw a schematic (even hand-drawn)
3. List exact components with part numbers
4. Share your complete code
5. Describe what you expected vs what happened

## References
- See [references/multimeter-guide.md](references/multimeter-guide.md) for detailed measurement techniques
- See [references/common-mistakes.md](references/common-mistakes.md) for beginner pitfall gallery
