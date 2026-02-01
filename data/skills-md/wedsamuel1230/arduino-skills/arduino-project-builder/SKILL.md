---
name: arduino-project-builder
description: Build complete, production-ready Arduino projects (environmental monitors, robot controllers, IoT devices, automation systems). Assembles multi-component systems combining sensors, actuators, communication protocols, state machines, data logging, and power management. Supports Arduino UNO, ESP32, and Raspberry Pi Pico with board-specific optimizations. Use this skill when users request complete Arduino applications, not just code snippets.
---

# Arduino Project Builder

Assemble complete, working Arduino projects from requirements. This skill combines multiple patterns (sensors, actuators, state machines, logging, communication) into cohesive systems.

## Quick Start

**List available project types:**
```bash
uv run --no-project scripts/scaffold_project.py --list
```

**Create a complete project:**
```bash
uv run --no-project scripts/scaffold_project.py --type environmental --board esp32 --name "WeatherStation"
uv run --no-project scripts/scaffold_project.py --type robot --board uno --output ./my-robot
```

**Interactive mode:**
```bash
uv run --no-project scripts/scaffold_project.py --interactive
```

## Resources

- **examples/** - Complete project examples (environmental monitor, robot controller, IoT device)
- **scripts/scaffold_project.py** - CLI tool for project scaffolding (config.h, main.ino, platformio.ini, README)
- **assets/workflow.mmd** - Mermaid diagram of project assembly workflow

## Supported Project Types

### Environmental Monitors
Multi-sensor data loggers (temperature, humidity, light, air quality)

See [Environmental Monitor Example](examples/project-environmental-monitor.md)

### Robot Controllers
Motor control, sensor fusion, obstacle avoidance, state machines

See [Robot Controller Example](examples/project-robot-controller.md)

### IoT Devices
WiFi/MQTT data transmission, cloud integration, remote monitoring

See [IoT Device Example](examples/project-iot-device.md)

### Home Automation
Relay control, scheduled tasks, sensor-triggered actions

### Data Acquisition Systems
High-frequency sampling, SD card logging, real-time visualization

## Project Assembly Workflow

- [ ] **[Requirements Gathering](workflow/step1-requirements-gathering.md)** - Analyze user request and gather project specifications
- [ ] **[Architecture Design](workflow/step2-architecture-design.md)** - Design component connections, data flow, and state machines
- [ ] **[Code Assembly](workflow/step3-code-assembly.md)** - Combine patterns and customize for user hardware
- [ ] **[Testing & Validation](workflow/step4-testing-validation.md)** - Verify compilation, memory usage, and functionality
- [ ] **[Documentation](workflow/step5-documentation.md)** - Create wiring diagrams, usage instructions, and troubleshooting guides

## Quality Standards & Rules

- [ ] **[Quality Standards](rules/quality-standards.md)** - Hardware abstraction, non-blocking code, error handling, and memory safety requirements
- [ ] **[Integration Checklist](rules/integration-checklist.md)** - Pre-delivery verification for sensor validation, timing, and reliability
- [ ] **[Board Considerations](rules/board-considerations.md)** - UNO, ESP32, and RP2040 specific optimizations and constraints

## Project Output Template

- [ ] **[Output Template](templates/project-output-template.md)** - Standardized format for delivering complete Arduino projects

## Resources

- **examples/** - Complete project examples with full implementations
- **scripts/scaffold_project.py** - CLI tool for project scaffolding with config.h, main.ino, platformio.ini, README
- **assets/workflow.mmd** - Mermaid diagram of project assembly workflow
- **workflow/** - Step-by-step project assembly process
- **rules/** - Quality standards and board-specific optimizations
- **templates/** - Project output templates and documentation standards
