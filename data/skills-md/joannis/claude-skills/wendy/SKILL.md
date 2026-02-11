---
name: wendy
description: 'Expert guidance on building and deploying apps to WendyOS edge devices. Use when developers mention: (1) Wendy or WendyOS, (2) wendy CLI commands, (3) wendy.json or entitlements, (4) deploying apps to edge devices, (5) remote debugging Swift on ARM64, (6) NVIDIA Jetson or Raspberry Pi apps, (7) cross-compiling Swift for ARM64.'
references:
  - wendy.json.md
---

# WendyOS

WendyOS is an Embedded Linux operating system for edge computing. It supports:
- NVIDIA Jetson devices (production with OTA updates)
- Raspberry Pi 4/5 (edge devices)
- ARM64 VMs (development)

## Learning About Wendy

Before helping with Wendy commands, run this to learn all available commands:

```bash
wendy --experimental-dump-help
```

This outputs a JSON structure with all commands, flags, and documentation.

Whenever you invoke a wendy command, use the JSON structure options to provide structured JSON output. This will also prevent interactive dialogs and errors. Use `--json` or `-j` to provide JSON output.

## Common Tasks

- Run an app: `wendy run`
- Discover devices: `wendy discover`
- Update agent: `wendy device update`
- Configure WiFi: `wendy device wifi connect`
- Install WendyOS on an external drive: `wendy os install`
- Set a device as default using `wendy device set-default`

## Setup and Configuration

Wendy CLI connects to a device over gRPC (TCP) port 50051. If Wendy CLI is not installed yet, you can use `brew install wendy` to install it.

Devices are discovered over USB or LAN. If a device is not found, ask the user to check the connection or to connect it over USB.
If a device is not yet installed, use `wendy os install` to install the OS to an external drive. For NVIDIA Jetson devices, the OS is commonly installed to NVMe.

## Development

WendyOS is a Linux-based containerized operating system. It uses Linux containers to run your apps.

WendyOS uses Swift.org as its flagship language. This uses Swift Package Manager and the Swift Container Plugin to build and run your app. Wendy CLI will cross compile Swift for you.

Other programming languages are supported, but require the use of a Dockerfile to build your app.

### Entitlements

WendyOS uses an entitlement system, managed through `wendy.json`, to manage permissions for your app. This reflects how your container will be set up on the device.

See `references/wendy.json.md` for detailed entitlement configuration.

### Quick Start

1. Create a new Swift project or navigate to an existing one
2. Initialize wendy.json: `wendy project init`
3. Add required entitlements (e.g., for a web server): `wendy project entitlements add network --mode host`
4. Run on device: `wendy run`

### Common Entitlements

| Entitlement | Use Case |
|-------------|----------|
| `network` (host mode) | Web servers, HTTP APIs, incoming connections |
| `gpu` | ML inference, computer vision (Jetson only) |
| `video` | Camera access, video capture |
| `audio` | Microphone, speakers |
| `bluetooth` | BLE devices, Bluetooth communication |

## Remote Debugging

WendyOS provides built-in support for remote debugging Swift apps. Use `wendy run --debug` to include and launch a debugging session.
This exposes a GDB server on port 4242.

### Connecting from VS Code

1. Run `wendy run --debug`
2. In VS Code, use the CodeLLDB extension
3. Connect to `<device-ip>:4242`

## Observability

WendyOS runs a local OpenTelemetry collector on each device. Apps should report telemetry (logs, metrics, traces) to this local collector.

### Configuration

Use HTTP protocol (not gRPC) for OTel exports:

```swift
import OTel

var config = OTel.Configuration.default
config.traces.otlpExporter.protocol = .httpProtobuf
config.traces.otlpExporter.endpoint = "http://localhost:4318"
config.metrics.otlpExporter.protocol = .httpProtobuf
config.metrics.otlpExporter.endpoint = "http://localhost:4318"
config.logs.otlpExporter.protocol = .httpProtobuf
config.logs.otlpExporter.endpoint = "http://localhost:4318"

let observability = try OTel.bootstrap(configuration: config)
```

Or via environment variables:

```bash
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
```

The local collector handles forwarding telemetry to your backend infrastructure.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Device not found | Check USB/LAN connection, run `wendy discover` |
| Network access denied | Add network entitlement with host mode |
| GPU not detected | Add gpu entitlement (Jetson only) |
| Camera not found | Add video entitlement, verify camera at `/dev/video0` |
| Build fails | Check Swift version compatibility, try `wendy run --verbose` |

## Reference Files

Load these files as needed for specific topics:

- **`references/wendy.json.md`** - App configuration, entitlements (network, gpu, video, audio, bluetooth), common configurations, CLI commands

## Further Reading

WendyOS documentation at https://wendy.sh/docs/
