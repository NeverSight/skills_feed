---
name: esp32-serial-logging
description: Real-time serial log monitoring for ESP32 and microcontrollers. Capture device output to a file and monitor logs in real-time. Use when debugging embedded devices, investigating crashes, or monitoring device behavior.
compatibility: Requires access to serial port (macOS/Linux). Device must be connected via USB.
metadata:
  author: H1D
  version: "1.0"
---

# ESP32 Serial Log Monitoring

## Overview

Capture serial output from ESP32 (or any microcontroller) to a file for real-time monitoring and analysis.

## ESP32 Setup (Device Side)

### ESP-IDF Framework

```cpp
#include "esp_log.h"

static const char* TAG = "MyComponent";

void my_function() {
    ESP_LOGI(TAG, "Info message");
    ESP_LOGW(TAG, "Warning: value=%d", some_value);
    ESP_LOGE(TAG, "Error occurred");
    ESP_LOGD(TAG, "Debug details");
}
```

### Arduino Framework

```cpp
void setup() {
    Serial.begin(115200);
}

void loop() {
    Serial.println("Status: running");
    Serial.printf("Sensor: %d\n", analogRead(A0));
    delay(1000);
}
```

## Host Side - Capture Logs

```bash
# Find serial port
PORT=$(ls /dev/cu.usbmodem* /dev/ttyUSB* /dev/ttyACM* 2>/dev/null | head -1)
echo "Found port: $PORT"

# Configure and start capture
stty -f "$PORT" 115200 raw -echo 2>/dev/null || stty -F "$PORT" 115200 raw -echo
cat "$PORT" >> /tmp/device.log &
echo "Logging to /tmp/device.log (PID: $!)"
```

## Monitor Logs

```bash
# Real-time monitoring
tail -f /tmp/device.log

# Filter specific patterns
tail -f /tmp/device.log | grep -E "ERROR|WiFi|Button"
```

## Search for Errors

```bash
# Find crashes and errors
grep -E "ERROR|crash|overflow|panic|assert|Backtrace" /tmp/device.log

# Find reboots (look for boot messages or uptime resets)
grep -E "boot:|rst:|Uptime: [0-9] sec" /tmp/device.log
```

## Debug Workflow

1. Clear log before reproducing issue:
   ```bash
   > /tmp/device.log
   ```

2. Reproduce the issue

3. Analyze captured logs:
   ```bash
   cat /tmp/device.log
   ```

## Common Baud Rates

| Device | Baud Rate |
|--------|-----------|
| ESP32 (default) | 115200 |
| ESP32 (fast) | 460800 |
| Arduino | 9600 |
| STM32 | 115200 |

## Stop Logging

```bash
pkill -f "cat /dev/cu.usbmodem"
pkill -f "cat /dev/ttyUSB"
```

## Troubleshooting

- **Port not found**: Check USB connection, try `ls /dev/cu.* /dev/tty.*`
- **Permission denied**: Add user to `dialout` group (Linux)
- **Garbled output**: Wrong baud rate
