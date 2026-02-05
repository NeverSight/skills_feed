---
name: gemini
description: Control Gemini via MQTT WebSocket. Use when user says "gemini", needs to send messages to Gemini, or control the Gemini browser tab.
---

# /gemini - Smooth MQTT Control for Gemini

Direct control of Gemini browser tab via MQTT WebSocket. **Tab precision works!**

## Quick Start

```bash
/gemini chat "Hello Gemini!"              # Send to active Gemini tab
/gemini new "Your message"                # Create new tab + chat
/gemini transcribe <youtube-url>          # Transcribe YouTube video
/gemini research "topic"                  # Deep Research mode
/gemini model fast|thinking|pro           # Select model
/gemini canvas                            # Open Canvas mode
```

## The Smooth Flow

```
create_tab → tabId → inject_badge → chat → GEMINI RESPONDS!
```

## Requirements

1. **Gemini Proxy Extension** v2.8.8+ (green badge = connected)
2. **Mosquitto broker** with dual listeners:
   - TCP port 1883 (for CLI/Bun scripts)
   - WebSocket port 9001 (for browser extension)
3. **Extension sidebar open** (click extension icon)

## Scripts

Located in `src/skills/gemini/scripts/`:

| Script | Purpose |
|--------|---------|
| `status.ts` | Show extension status + all tabs (like debug console) |
| `list-tabs.ts` | List all Gemini tabs with IDs |
| `deep-research.ts` | Deep Research automation |
| `send-chat.ts` | Send single chat message |
| `full-smooth.ts` | Complete flow demo |
| `youtube-transcribe.ts` | Transcribe YouTube video |

**Note:** For YouTube learning, use `/watch` skill which includes Oracle integration.

### Run Scripts

```bash
cd src/skills/gemini/scripts
node --experimental-strip-types full-smooth.ts
node --experimental-strip-types send-chat.ts "Your message"
node --experimental-strip-types youtube-transcribe.ts "https://youtube.com/..."
```

## MQTT Topics

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `claude/browser/command` | → Extension | Send commands |
| `claude/browser/response` | ← Extension | Command results |
| `claude/browser/status` | ← Extension | Online/offline |

**IMPORTANT**: Topics are `claude/browser/*` NOT `claude-browser-proxy/*`!

## Commands

### Tab Management

```json
{"action": "create_tab"}
// → {tabId: 2127157543, success: true}

{"action": "list_tabs"}
// → {tabs: [...], count: 3}

{"action": "focus_tab", "tabId": 2127157543}
// → {success: true}

{"action": "inject_badge", "tabId": 2127157543, "text": "HELLO"}
// → {success: true, injected: true}
```

### Chat (with Tab Precision!)

```json
{
  "action": "chat",
  "tabId": 2127157543,
  "text": "Your message to Gemini"
}
```

### Get Data

```json
{"action": "get_url", "tabId": 123}     // {url, title}
{"action": "get_text", "tabId": 123}    // {text}
{"action": "get_state", "tabId": 123}   // {loading, responseCount, tool}
```

### Model Selection

```json
{"action": "select_model", "model": "thinking"}
// "fast", "pro", or "thinking"
```

## Example: Full Smooth Flow

```typescript
import mqtt from 'mqtt';

const client = mqtt.connect('mqtt://localhost:1883');

// Helper function
async function send(action, params = {}) {
  return new Promise((resolve) => {
    const id = `${action}_${Date.now()}`;
    client.subscribe('claude/browser/response');
    client.on('message', (topic, msg) => {
      const data = JSON.parse(msg.toString());
      if (data.id === id) resolve(data);
    });
    client.publish('claude/browser/command',
      JSON.stringify({ id, action, ...params }));
  });
}

// The Flow
const tab = await send('create_tab');           // 1. Create tab
await new Promise(r => setTimeout(r, 4000));    // 2. Wait for load
await send('inject_badge', {                    // 3. Verify targeting
  tabId: tab.tabId,
  text: 'SMOOTH!'
});
await send('chat', {                            // 4. Send chat
  tabId: tab.tabId,
  text: 'Hello from Claude!'
});
// → Gemini responds!
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Commands timeout | Check topic names: `claude/browser/*` |
| Chat doesn't type | Extension needs v2.8.8+ |
| Tab not found | Use `list_tabs` to see available tabs |
| Extension offline | Open extension sidebar |

## Extension Source

`github.com/laris-co/claude-browser-proxy` (v2.8.8+)
