---
name: macro-agent
description: "Desktop macro control with image recognition. Commands: find, search, click-on, click, move-to, write, press, hotkey, scroll, drag, screenshot, region-capture, seq-create/add/run/list/delete. ALWAYS uses template matching (image search), NEVER fixed coordinates. Use 'region-capture' to capture new elements."
---

# Macro Agent

Desktop automation and UI control skill with **image recognition**.

## 🚨 CRITICAL: How to Handle User Requests

**BEFORE doing ANY action, ALWAYS check if a sequence exists for it:**

1. **FIRST** run `seq-list` to see available sequences
2. **LOOK** for sequences that match the user's intent (e.g., `whatsapp_send_marco` for "send message to Marco")
3. **IF sequence exists**: Use `seq-run <sequence_name>` then add your custom actions (write message, press enter)
4. **IF NO sequence exists**: Then use individual commands

### Common Workflow: Send Message to Contact

When user says "send message to X" or "envía mensaje a X":

```
1. seq-list                          # Check available sequences
2. seq-run whatsapp_send_<contact>   # Run the messaging sequence  
3. write "<message>"                 # Type the message
4. press enter                       # Send it
```

**NEVER** use `hotkey super` or manual navigation when a sequence exists!

### Available Sequences (check with seq-list)

The user has pre-configured sequences for common tasks. Always check them first!
- `whatsapp_send_ross` - Opens WhatsApp and selects Ross contact
- `whatsapp_send_marco` - Opens WhatsApp and selects Marco contact
- Other sequences may exist - always run `seq-list` first!

## 🎯 How Element Detection Works

When using `click-on` or `move-to`, the agent **ALWAYS** uses image recognition:
1. Searches for element image on screen (template matching)
2. If not found → **FAILS** (no fallback to coordinates)

This ensures elements are found dynamically based on their actual position.

**Output includes `method` field:**
- `image` = Found by template matching ✅
- `not_found` = Image not visible on screen ❌

**If element not found:** You need to capture it first with `region-capture`.

## ⚠️ Important

**NO "navigate" command exists**. To navigate:
1. `find <name>` - Search for element info
2. `click-on <name>` - Click using image recognition (ALWAYS)

## Usage

```bash
python ~/.copilot/skills/macro-agent/macro_agent.py <command> [args]
```

## Commands Reference

| Action | Command | Example |
|--------|---------|---------|
| Search element | `find <name>` | `find brave` |
| Search text | `search <text>` | `search save` |
| Click element | `click-on <name>` | `click-on brave` |
| Click coords | `click X Y` | `click 500 300` |
| Move to element | `move-to <name>` | `move-to button` |
| Move to coords | `move X Y` | `move 500 300` |
| Write text | `write <text>` | `write "hello"` |
| Press key | `press <key>` | `press enter` |
| Hotkey | `hotkey <keys>` | `hotkey ctrl c` |
| Scroll | `scroll N` | `scroll -3` |
| Screenshot | `screenshot <name>` | `screenshot test` |
| Region capture | `region-capture` | `region-capture` |

## Sequence Commands

| Command | Description |
|---------|-------------|
| `seq-create <name>` | Create new sequence |
| `seq-add <name> "<action>"` | Add action to sequence |
| `seq-show <name>` | View sequence |
| `seq-run <name>` | Execute sequence |
| `seq-list` | List all sequences |
| `seq-delete <name>` | Delete sequence |

## Output

JSON with:
- `success`: true/false
- `action`: Command executed
- `target`: Element name (if applicable)
- `coordinates`: {x, y} position
- `message`: Result description

## Data Locations

- **Elements**: `~/.copilot/skills/macro-agent/data/elements.json` (elemento definitions)
- **Captures**: `~/.copilot/skills/macro-agent/data/captures/` (template images)
- **Sequences**: `~/.copilot/skills/macro-agent/data/sequences/` (action sequences)

## Examples

### Find and Click App
```bash
python ~/.copilot/skills/macro-agent/macro_agent.py find chrome
python ~/.copilot/skills/macro-agent/macro_agent.py click-on chrome
```

### Type and Submit
```bash
python ~/.copilot/skills/macro-agent/macro_agent.py write "search query"
python ~/.copilot/skills/macro-agent/macro_agent.py press enter
```

### Keyboard Shortcut
```bash
python ~/.copilot/skills/macro-agent/macro_agent.py hotkey ctrl shift s
```

### Create and Run Sequence
```bash
python ~/.copilot/skills/macro-agent/macro_agent.py seq-create my_macro
python ~/.copilot/skills/macro-agent/macro_agent.py seq-add my_macro "click-on file_menu"
python ~/.copilot/skills/macro-agent/macro_agent.py seq-add my_macro "wait 0.5"
python ~/.copilot/skills/macro-agent/macro_agent.py seq-add my_macro "click-on save_option"
python ~/.copilot/skills/macro-agent/macro_agent.py seq-run my_macro
```

## Capture New Elements

```bash
python ~/.copilot/skills/macro-agent/macro_agent.py region-capture
```

Keys: `f`=freeze, `c`/`Space`=capture, `+/-`=resize, `q`/`ESC`=quit

## 📱 Example: Send WhatsApp Message

User says: "Envía mensaje a Marco diciendo hola"

**CORRECT approach:**
```bash
# 1. First check sequences
seq-list

# 2. Found whatsapp_send_marco! Run it
seq-run whatsapp_send_marco

# 3. Type and send
write "hola"
press enter
```

**WRONG approach (NEVER do this):**
```bash
# ❌ WRONG - Don't manually navigate!
hotkey super
wait 500
# This is stupid, use sequences!
```

## 🔄 Decision Flow

```
User Request
    ↓
Run seq-list
    ↓
Sequence exists? ──YES──→ seq-run <name> → Additional actions (write, press)
    ↓ NO
Use individual commands (click-on, write, press, etc.)
```
