---
name: a2ui-embed
description: Write HTML visualizations to the A2UI panel or embed running apps
---

# A2UI Visualization Skill

Write custom HTML visualizations or embed running web apps in the TriClaude A2UI panel.

## Trigger Phrases

- "open in a2ui", "show in a2ui", "embed", "a2ui"
- "visualize", "show me", "display", "chart", "render"

## How A2UI Works

```
┌─────────────────────────────────────────────────────────────┐
│  Claude writes HTML     Sidecar watches      UI displays   │
│  to a2ui_input.log  →   log file and     →   via WebSocket │
│                         broadcasts                          │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
1. **Log file**: `runtime/terminals/<terminal_id>/a2ui_input.log`
2. **Sidecar**: Python WebSocket server that watches the log
3. **UI**: React connects to sidecar WebSocket, renders HTML in iframe

## Step 1: Get Terminal Info

The A2UI log path is in your terminal startup message:
```
A2UI VISUALIZATION: Write HTML to /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/<terminal_id>/a2ui_input.log
```

To find terminal config (including sidecarPort):
```bash
cat /home/yousuf/GoogleDrive/PROJECTS/.triclaude/projects.json | python3 -m json.tool
```

Look for your terminal ID and note the `sidecarPort`.

## Step 2: Ensure Sidecar is Running

**Check if sidecar is running:**
```bash
ss -tlnp | grep <sidecarPort>
```

**If NOT running, start it:**
```bash
python3 /home/yousuf/GoogleDrive/PROJECTS/APPS/TriClaude/scripts/a2ui_sidecar.py \
  --port <sidecarPort> \
  --log /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/<terminal_id>/a2ui_input.log &
```

Example:
```bash
python3 /home/yousuf/GoogleDrive/PROJECTS/APPS/TriClaude/scripts/a2ui_sidecar.py \
  --port 7867 \
  --log /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/term_1768665093_0ve1c1/a2ui_input.log &
```

## Step 3: Write HTML to A2UI

### Custom Visualization

```bash
cat << 'A2UI_EOF' >> $A2UI_LOG
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0f172a;
  color: #e2e8f0;
  font-family: system-ui;
  padding: 16px;
}
/* Your styles here */
</style>
</head>
<body>
<!-- Your content here -->
</body>
</html>
<!-- A2UI:END -->
A2UI_EOF
```

### Embed Running App (iframe)

```bash
cat << 'A2UI_EOF' >> $A2UI_LOG
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; width: 100%; overflow: hidden; background: #0f172a; }
iframe { width: 100%; height: 100%; border: none; display: block; }
</style>
</head>
<body>
<iframe src="http://localhost:3000" allow="*" sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals"></iframe>
</body>
</html>
<!-- A2UI:END -->
A2UI_EOF
```

## Critical Requirements

1. **Markers required**: `<!-- A2UI:START -->` and `<!-- A2UI:END -->`
2. **Append to log**: Use `>>` not `>`
3. **Sidecar must be running** on the terminal's sidecarPort
4. **A2UI panel must be open** in the UI (purple button)
5. **Terminal must be visible/selected** in UI

For iframes:
- `sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals"`
- `allow="*"`
- No padding/margin on html/body
- `overflow: hidden` on body

## Project Registry (for embedding apps)

| Project | Path | Port |
|---------|------|------|
| tesseract | `/home/yousuf/local_workspaces/tesseract` | 3000 |
| triclaude | `/home/yousuf/local_workspaces/triclaude` | 3001 |

## Troubleshooting

**Panel shows nothing:**
1. Check sidecar is running: `ss -tlnp | grep <sidecarPort>`
2. Start sidecar if not running (see Step 2)
3. Toggle A2UI panel off/on to force WebSocket reconnect
4. Check log file has content: `tail -20 $A2UI_LOG`

**Find terminal's sidecar port:**
```bash
cat /home/yousuf/GoogleDrive/PROJECTS/.triclaude/projects.json | grep -A5 "<terminal_id>"
```

**Quick diagnostic:**
```bash
# 1. Get terminal ID from startup message
# 2. Find sidecar port
cat /home/yousuf/GoogleDrive/PROJECTS/.triclaude/projects.json | python3 -m json.tool | grep -A10 "term_XXXXX"

# 3. Check if sidecar running
ss -tlnp | grep 786

# 4. Start sidecar if needed
python3 /path/to/a2ui_sidecar.py --port PORT --log /path/to/a2ui_input.log &
```

## Example: Full Flow

```bash
# 1. Note terminal ID from startup: term_1768665093_0ve1c1
# 2. Check config - sidecarPort is 7867
# 3. Check sidecar: ss -tlnp | grep 7867 → not running
# 4. Start sidecar:
python3 /home/yousuf/GoogleDrive/PROJECTS/APPS/TriClaude/scripts/a2ui_sidecar.py \
  --port 7867 \
  --log /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/term_1768665093_0ve1c1/a2ui_input.log &

# 5. Write visualization:
cat << 'A2UI_EOF' >> /home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/term_1768665093_0ve1c1/a2ui_input.log
<!-- A2UI:START -->
<html><body style="background:#0f172a;color:white;padding:20px;">
<h1>Hello A2UI!</h1>
</body></html>
<!-- A2UI:END -->
A2UI_EOF
```
