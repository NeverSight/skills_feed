---
name: pikvm
description: Remote KVM control via PiKVM REST API. Use for controlling remote computers through PiKVM - taking screenshots, moving mouse, clicking, typing text, pressing keys, keyboard shortcuts, scrolling, or power management.
vm0_secrets:
  - PIKVM_AUTH
  - PIKVM_URL
---

# PiKVM Remote Control

Control remote computers via PiKVM REST API with mouse, keyboard, and power management.

## When to Use

- Take screenshots of remote machine
- Move mouse and click
- Type text or press keyboard keys
- Execute keyboard shortcuts (Cmd+Space, Ctrl+Alt+Del, etc.)
- Power control (on/off/reset)
- Automate remote desktop operations

## Prerequisites

```bash
export PIKVM_URL=https://pikvm.example.com
export PIKVM_AUTH=admin:admin
```

### Get Credentials

1. Access your PiKVM web interface
2. Default credentials: `admin:admin`

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.

## Coordinate System

**Mouse coordinates use screen center as origin (0,0)**:
- Negative X = left, Positive X = right
- Negative Y = up, Positive Y = down

For 1920x1080 screen:
- Top-left: `(-960, -540)`
- Center: `(0, 0)`
- Bottom-right: `(960, 540)`

---

## Usage

### Take Screenshot

```bash
bash -c 'curl -k -s -o /tmp/screenshot.jpg -u "$PIKVM_AUTH" "${PIKVM_URL}/api/streamer/snapshot"'
```

### Type Text

Text must be sent as raw body with `Content-Type: text/plain`:

```bash
bash -c 'curl -k -s -X POST \
  -H "Content-Type: text/plain" \
  -u "$PIKVM_AUTH" \
  -d "Hello World" \
  "${PIKVM_URL}/api/hid/print?limit=0"'
```

### Move Mouse

Move to absolute position (0,0 = screen center):

```bash
bash -c 'curl -k -s -X POST \
  -u "$PIKVM_AUTH" \
  "${PIKVM_URL}/api/hid/events/send_mouse_move?to_x=-500&to_y=-300"'
```

### Mouse Click

```bash
# Press
bash -c 'curl -k -s -X POST \
  -u "$PIKVM_AUTH" \
  "${PIKVM_URL}/api/hid/events/send_mouse_button?button=left&state=true"'

# Release
bash -c 'curl -k -s -X POST \
  -u "$PIKVM_AUTH" \
  "${PIKVM_URL}/api/hid/events/send_mouse_button?button=left&state=false"'
```

### Press Key

Press and release with `state=true` then `state=false`:

```bash
# Press Enter
bash -c 'curl -k -s -X POST \
  -u "$PIKVM_AUTH" \
  "${PIKVM_URL}/api/hid/events/send_key?key=Enter&state=true"'

bash -c 'curl -k -s -X POST \
  -u "$PIKVM_AUTH" \
  "${PIKVM_URL}/api/hid/events/send_key?key=Enter&state=false"'
```

### Key Combo (e.g., Cmd+Space for Spotlight)

Press all keys in order, then release in reverse:

```bash
# Press Cmd
bash -c 'curl -k -s -X POST -u "$PIKVM_AUTH" "${PIKVM_URL}/api/hid/events/send_key?key=MetaLeft&state=true"'

# Press Space
bash -c 'curl -k -s -X POST -u "$PIKVM_AUTH" "${PIKVM_URL}/api/hid/events/send_key?key=Space&state=true"'

# Release Space
bash -c 'curl -k -s -X POST -u "$PIKVM_AUTH" "${PIKVM_URL}/api/hid/events/send_key?key=Space&state=false"'

# Release Cmd
bash -c 'curl -k -s -X POST -u "$PIKVM_AUTH" "${PIKVM_URL}/api/hid/events/send_key?key=MetaLeft&state=false"'
```

### Mouse Scroll

```bash
bash -c 'curl -k -s -X POST \
  -u "$PIKVM_AUTH" \
  "${PIKVM_URL}/api/hid/events/send_mouse_wheel?delta_x=0&delta_y=-50"'
```

### Get Device Info

```bash
bash -c 'curl -k -s \
  -u "$PIKVM_AUTH" \
  "${PIKVM_URL}/api/info"' | jq .
```

### ATX Power Control

```bash
# Power on
bash -c 'curl -k -s -X POST \
  -u "$PIKVM_AUTH" \
  "${PIKVM_URL}/api/atx/power?action=on"'

# Power off
bash -c 'curl -k -s -X POST -u "$PIKVM_AUTH" "${PIKVM_URL}/api/atx/power?action=off"'

# Hard reset
bash -c 'curl -k -s -X POST -u "$PIKVM_AUTH" "${PIKVM_URL}/api/atx/power?action=reset_hard"'
```

---

## Common Key Names

```
MetaLeft (Cmd), ControlLeft, AltLeft, ShiftLeft
Enter, Space, Escape, Tab, Backspace, Delete
ArrowUp, ArrowDown, ArrowLeft, ArrowRight
KeyA-KeyZ, Digit0-Digit9, F1-F12
PageUp, PageDown, Home, End
Equal (+), Minus (-)
```

## API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/streamer/snapshot` | GET | Screenshot (JPEG) |
| `/api/hid/print` | POST | Type text (body: raw text) |
| `/api/hid/events/send_mouse_move` | POST | Move mouse (`to_x`, `to_y`) |
| `/api/hid/events/send_mouse_button` | POST | Click (`button`, `state`) |
| `/api/hid/events/send_mouse_wheel` | POST | Scroll (`delta_x`, `delta_y`) |
| `/api/hid/events/send_key` | POST | Key press (`key`, `state`) |
| `/api/atx/power` | POST | Power control (`action`) |
| `/api/info` | GET | Device info |
| `/api/atx` | GET | ATX status |

## API Reference

- Official docs: https://docs.pikvm.org/api/
