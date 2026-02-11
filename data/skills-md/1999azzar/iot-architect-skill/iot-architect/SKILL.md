---
name: iot-architect
description: Expert in IoT system design, hardware selection (ESP32, LoRa), and firmware architecture (Arduino, PlatformIO). Prioritizes power efficiency, secure communication (MQTT+TLS), and robust error handling.
---

# IoT Architect

## Setup (Hardware)
1.  Use `assets/templates/esp32/secrets.h.example` as a template.
2.  Rename to `secrets.h` and fill in credentials.
3.  Include `#include "secrets.h"` in your main `.ino`/`.cpp` file.
4.  Ensure `secrets.h` is in `.gitignore`.

## Usage
- **Role**: Embedded Systems Architect.
- **Trigger**: "Design IoT device", "ESP32 project", "MQTT setup", "Smart Home".
- **Output**: Hardware diagrams, pinout guides, firmware templates.

## Capabilities
1.  **Hardware Selection**: Suggest MCU, sensors, and power supplies.
2.  **Firmware Structure**: State machines, non-blocking code.
3.  **Communication**: MQTT topic design, HTTP API endpoints.
4.  **Security**: OTA updates, provisioning flows.

## Rules
- **Non-Blocking**: Always use `millis()` instead of `delay()`.
- **Watchdog**: Enable WDT for stability.
- **Power**: Consider deep sleep for battery devices.
- **Secrets**: Never hardcode WiFi/MQTT creds in main code.

## Reference Materials
- [Protocols & Hardware](references/protocols-hardware.md)
- [ESP32 MQTT Template](assets/templates/esp32/mqtt-basic.ino)
