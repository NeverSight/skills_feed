---
name: ubuntu-desktop-control
description:
  Control Ubuntu desktop GUI with semantic element targeting using AT-SPI
  accessibility tree and OCR fallback. For wallet automation, browser extensions,
  and GUI tasks Playwright can't reach.
license: MIT
compatibility: Requires Ubuntu/Debian with X11, Python 3.6+, and system packages (xdotool, scrot, at-spi2-core, tesseract-ocr). Run install.sh for setup.
metadata:
  author: lommaj
  version: '2.0.0'
---

# Desktop Control Skill

Control the desktop GUI using semantic element targeting. Find and click UI elements by name instead of coordinates.

**Key Features:**
- **AT-SPI** - Primary method using accessibility tree (knows element roles, states, actions)
- **OCR Fallback** - Tesseract-based text finding when AT-SPI can't find the element
- **Wait Utilities** - Poll for elements to appear with exponential backoff
- **Click Verification** - Optional pre-click screenshot verification

## Prerequisites

Install dependencies:
```bash
bash install.sh
```

Or manually:
```bash
# System packages
sudo apt-get install -y xdotool scrot imagemagick \
    at-spi2-core libatk-adaptor python3-gi gir1.2-atspi-2.0 \
    tesseract-ocr tesseract-ocr-eng python3-pip

# Python packages
pip3 install -r requirements.txt
```

For headless Xvfb sessions:
```bash
export GTK_MODULES=gail:atk-bridge
export QT_LINUX_ACCESSIBILITY_ALWAYS_ON=1
/usr/lib/at-spi2-core/at-spi-bus-launcher &
```

## Commands

All commands use `DISPLAY=:10.0` by default. Override with `--display` flag.

---

### find-element

Find UI element via AT-SPI with OCR fallback.

```bash
python3 scripts/desktop.py find-element --name "Confirm" [--role button] [--app Firefox]
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--name`, `-n` | string | No | Element name/text to find |
| `--role`, `-r` | string | No | Element role (button, entry, etc.) |
| `--app`, `-a` | string | No | Application name filter |
| `--all` | flag | No | Find all matches |
| `--clickable` | flag | No | Only clickable elements |
| `--max-results` | int | No | Maximum results (default: 50) |

**Returns:**
```json
{
  "element": {
    "name": "Confirm",
    "bounds": { "x": 400, "y": 300, "width": 100, "height": 30 },
    "center": { "x": 450, "y": 315 },
    "role": "push button",
    "source": "atspi",
    "visible": true,
    "enabled": true,
    "clickable": true
  }
}
```

---

### find-text

Find text on screen via OCR only.

```bash
python3 scripts/desktop.py find-text "I have an existing wallet" [--exact] [--all]
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | Text to find |
| `--exact` | flag | No | Require exact match |
| `--case-sensitive` | flag | No | Case-sensitive matching |
| `--all` | flag | No | Find all occurrences |
| `--max-results` | int | No | Maximum results (default: 50) |

**Returns:**
```json
{
  "match": {
    "name": "I have an existing wallet",
    "bounds": { "x": 200, "y": 400, "width": 180, "height": 20 },
    "center": { "x": 290, "y": 410 },
    "source": "ocr",
    "confidence": 95.2
  }
}
```

---

### click-element

Click element by name/role (finds element first, then clicks at center).

```bash
python3 scripts/desktop.py click-element --name "Next" [--role button] [--verify]
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--name`, `-n` | string | No | Element name/text |
| `--role`, `-r` | string | No | Element role |
| `--app`, `-a` | string | No | Application name filter |
| `--right` | flag | No | Right click |
| `--double` | flag | No | Double click |
| `--verify` | flag | No | OCR verify before click |

`click-element` requires at least one selector: `--name` or `--role`.
When `--verify` is used, OCR must be available and text must be provided (typically via `--name`).

**Returns:**
```json
{
  "clicked": {
    "element": { "name": "Next", "..." },
    "x": 450,
    "y": 315,
    "button": "left",
    "double": false
  }
}
```

---

### wait-for

Wait for element or text to appear (with timeout and exponential backoff).

```bash
python3 scripts/desktop.py wait-for --name "Success" --timeout 30
python3 scripts/desktop.py wait-for --text "Transaction complete" --timeout 60
python3 scripts/desktop.py wait-for --name "Loading" --gone --timeout 30
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--name`, `-n` | string | No | Element name (AT-SPI + OCR) |
| `--role`, `-r` | string | No | Element role (AT-SPI only) |
| `--app`, `-a` | string | No | Application filter |
| `--text`, `-t` | string | No | Text to find (OCR only) |
| `--exact` | flag | No | Exact text match |
| `--gone` | flag | No | Wait until disappears |
| `--timeout` | float | No | Timeout in seconds (default: 30) |

Use either `--text` or element selectors (`--name`, `--role`, `--app`) for a single call, not both.
For element waits (with or without `--gone`), provide at least one of `--name` or `--role`.

**Returns:**
```json
{ "found": { "name": "Success", "..." } }
// or
{ "gone": true, "name": "Loading" }
// or
{ "error": "Element not found within 30s", "timeout": true }
```

---

### list-elements

List all interactive elements (buttons, inputs, links, etc.)

```bash
python3 scripts/desktop.py list-elements [--app Firefox] [--role button]
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--app`, `-a` | string | No | Application name filter |
| `--role`, `-r` | string | No | Filter by role |
| `--include-hidden` | flag | No | Include hidden elements |
| `--max-results` | int | No | Maximum results (default: 100) |

**Returns:**
```json
{
  "elements": [
    { "name": "Sign In", "role": "push button", "..." },
    { "name": "Email", "role": "entry", "..." }
  ],
  "count": 2
}
```

---

### status

Check AT-SPI and OCR availability.

```bash
python3 scripts/desktop.py status
```

**Returns:**
```json
{
  "atspi": {
    "available": true,
    "applications": ["Firefox", "gnome-calculator"]
  },
  "ocr": { "available": true },
  "display": ":10.0"
}
```

---

## Original Commands

These coordinate-based commands are still available:

| Command | Description |
|---------|-------------|
| `screenshot [--output PATH]` | Take screenshot |
| `click X Y [--right] [--double]` | Click at coordinates |
| `type "TEXT" [--type-delay MS]` | Type text |
| `key "KEYS"` | Press key combination |
| `move X Y` | Move mouse |
| `active` | Get active window info |
| `find-window "NAME"` | Find windows by name |
| `focus "NAME"` | Focus window by name |
| `position` | Get mouse position |
| `windows` | List all windows |

---

## Example Workflows

### MetaMask Transaction (Semantic)

```bash
# Wait for and click Confirm button
python3 scripts/desktop.py wait-for --name "Confirm" --role button --timeout 30
python3 scripts/desktop.py click-element --name "Confirm" --role button

# Wait for success message
python3 scripts/desktop.py wait-for --text "Transaction submitted" --timeout 60
```

### Phantom Wallet Import (Semantic)

```bash
# Click "I have an existing wallet"
python3 scripts/desktop.py click-element --name "I already have a wallet"

# Wait for seed phrase input
python3 scripts/desktop.py wait-for --role entry --timeout 10

# Type seed phrase
python3 scripts/desktop.py type "word1 word2 word3..."

# Click Import
python3 scripts/desktop.py click-element --name "Import"
```

### Hybrid Approach (Semantic + Coordinates)

```bash
# Use semantic for known buttons
python3 scripts/desktop.py click-element --name "Settings"

# Fall back to coordinates for unlabeled icons
python3 scripts/desktop.py screenshot --output /tmp/screen.png
# (analyze screenshot to get coordinates)
python3 scripts/desktop.py click 850 120
```

---

## Tips

1. **Prefer semantic commands** - `click-element` and `wait-for` are more robust than coordinates
2. **Check status first** - Run `status` to verify AT-SPI and OCR are available
3. **Use --role for precision** - Distinguish between buttons and text with same name
4. **Fall back to OCR** - If AT-SPI doesn't expose an element, `find-text` uses OCR
5. **Wait instead of sleep** - `wait-for` is more reliable than fixed delays
6. **Use --verify for critical clicks** - Adds OCR verification before clicking
