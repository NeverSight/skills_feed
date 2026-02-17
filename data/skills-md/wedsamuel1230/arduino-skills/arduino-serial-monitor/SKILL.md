---
name: arduino-serial-monitor
description: Tools for reading and analyzing Arduino serial monitor output for enhanced debugging. Provides real-time monitoring, data logging, filtering, and pattern matching to help troubleshoot Arduino sketches using arduino-cli or Arduino IDE.
category: arduino
---

# Arduino Serial Monitor

This skill provides advanced tools for reading and analyzing serial monitor data from Arduino boards, enhancing the debugging experience beyond the basic Arduino IDE serial monitor.

## Features

- **Real-time Serial Monitoring**: Connect to Arduino serial ports and display data in real-time
- **Data Logging**: Save serial output to files with timestamps for later analysis
- **Filtering & Pattern Matching**: Filter output by keywords, regex patterns, or data types
- **Error Detection**: Automatically highlight common error patterns and warnings
- **Multiple Format Support**: Handle different data formats (text, JSON, CSV, binary)
- **Cross-platform**: Works with Windows, macOS, and Linux serial ports

## Usage

### Basic Serial Monitoring

```bash
# Monitor serial port with default settings (9600 baud)
uv run --no-project scripts/monitor_serial.py --port COM3

# Specify baud rate and output file
uv run --no-project scripts/monitor_serial.py --port /dev/ttyACM0 --baud 115200 --output debug.log

# Filter for specific patterns
uv run --no-project scripts/monitor_serial.py --port COM3 --filter "ERROR|WARNING"
```

### Advanced Debugging

```bash
# Parse JSON data from serial
uv run --no-project scripts/monitor_serial.py --port COM3 --format json --pretty

# Monitor with timestamp and color coding
uv run --no-project scripts/monitor_serial.py --port COM3 --timestamp --color

# Detect common Arduino errors
uv run --no-project scripts/monitor_serial.py --port COM3 --detect-errors
```

## Script Options

- `--port`: Serial port (e.g., COM3, /dev/ttyACM0)
- `--baud`: Baud rate (default: 9600)
- `--output`: Output file for logging
- `--filter`: Regex pattern to filter lines
- `--format`: Data format (text, json, csv, binary)
- `--timestamp`: Add timestamps to output
- `--color`: Enable color-coded output
- `--detect-errors`: Highlight common error patterns
- `--timeout`: Connection timeout in seconds

## Common Arduino Debugging Scenarios

### Memory Issues
```
Filter for: "low memory|stack overflow|heap"
```

### Sensor Data Validation
```
Filter for: "sensor|reading|value"
Format as: json
```

### Timing Analysis
```
Enable: --timestamp
Filter for: "start|end|duration"
```

### Communication Errors
```
Filter for: "timeout|failed|error"
Enable: --detect-errors
```

## Integration with Arduino CLI

```bash
# Compile and upload, then monitor
arduino-cli compile --fqbn arduino:avr:uno sketch/
arduino-cli upload -p COM3 --fqbn arduino:avr:uno sketch/
uv run --no-project scripts/monitor_serial.py --port COM3
```

## Troubleshooting

### Port Not Found
- Check `arduino-cli board list` for available ports
- Ensure Arduino is connected and drivers are installed
- Try different port names (COM1-COM99 on Windows, /dev/ttyACM* on Linux)

### No Data Received
- Verify baud rate matches Arduino sketch (`Serial.begin(9600)`)
- Check USB cable connection
- Reset Arduino board while monitoring

### Permission Errors (Linux/macOS)
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER
# Logout and login again
```

## Dependencies

- Python 3.8+
- pyserial
- colorama (for colored output)
- Install via: `uv add pyserial colorama`

## Examples

### Basic Temperature Sensor Monitoring

```python
// Arduino sketch
void setup() {
  Serial.begin(9600);
}

void loop() {
  float temp = analogRead(A0) * 0.488;
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println(" C");
  delay(1000);
}
```

```bash
uv run --no-project scripts/monitor_serial.py --port COM3 --filter "Temperature" --timestamp
```

### JSON Data Parsing

```python
// Arduino sketch with JSON output
#include <ArduinoJson.h>

void setup() {
  Serial.begin(115200);
}

void loop() {
  StaticJsonDocument<200> doc;
  doc["temperature"] = analogRead(A0) * 0.488;
  doc["humidity"] = analogRead(A1) * 0.146;
  doc["timestamp"] = millis();
  serializeJson(doc, Serial);
  Serial.println();
  delay(2000);
}
```

```bash
uv run --no-project scripts/monitor_serial.py --port COM3 --format json --pretty
```