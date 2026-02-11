---
name: deepclaw-voice
description: Set up phone calling to OpenClaw using Deepgram Voice Agent API
requires:
  bins:
    - python3
    - ngrok
    - git
---

# deepclaw Voice Setup

Use this skill when the user wants to call you on the phone, set up voice calling, or talk to OpenClaw via phone.

## What This Sets Up

Phone calls to OpenClaw using:
- **Deepgram Voice Agent API** - STT, TTS, turn-taking, barge-in
- **Twilio** - Phone number routing
- **OpenClaw** - Your AI (via chat completions proxy)

## Setup Process

### Step 1: Clone the repo

```bash
git clone https://github.com/deepgram/deepclaw.git ~/deepclaw
cd ~/deepclaw
pip install -r requirements.txt
```

### Step 2: Get Deepgram API Key

1. Go to https://console.deepgram.com/
2. Sign up (free $200 credit)
3. **API Keys** → **Create API Key** → Name: "deepclaw", Full Access
4. Copy key immediately

Ask: "What's your Deepgram API key?"

### Step 3: Get Twilio Credentials

1. Go to https://www.twilio.com/ and sign up
2. Copy **Account SID** and **Auth Token** from dashboard
3. **Phone Numbers** → **Buy a number** with Voice (~$1/month)

Ask: "What's your Twilio phone number, Account SID, and Auth Token?"

### Step 4: Get OpenClaw Gateway Token

Run this to get the token from their OpenClaw config:
```bash
grep -A2 '"auth"' ~/.openclaw/openclaw.json | grep token
```

Or generate a new one:
```bash
openssl rand -hex 24
```

If generating new, tell them to add it to `~/.openclaw/openclaw.json` under `gateway.auth.token`.

### Step 5: Create .env file

Create `~/deepclaw/.env` with their values:
```
DEEPGRAM_API_KEY=<their_deepgram_key>
TWILIO_ACCOUNT_SID=<their_sid>
TWILIO_AUTH_TOKEN=<their_token>
OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789
OPENCLAW_GATEWAY_TOKEN=<their_gateway_token>
```

### Step 6: Ensure OpenClaw Gateway has chat completions enabled

Check their `~/.openclaw/openclaw.json` has:
```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": {
          "enabled": true
        }
      }
    }
  }
}
```

If not, add it and restart the gateway: `openclaw daemon restart`

### Step 7: Start ngrok

```bash
ngrok http 8000
```

Note the HTTPS URL (e.g., `https://abc123.ngrok-free.app`).

### Step 8: Configure Twilio Webhook

1. https://console.twilio.com/
2. **Phone Numbers** → **Active Numbers** → Click their number
3. **Voice Configuration**:
   - A Call Comes In: **Webhook**
   - URL: `https://<ngrok-url>/twilio/incoming`
   - Method: **POST**
4. Save

### Step 9: Start Server

```bash
cd ~/deepclaw
python -m deepclaw.voice_agent_server
```

### Step 10: Test

Tell them: "Call your Twilio number now!"

Watch the server logs for:
- "Connected to Deepgram Voice Agent API"
- "Agent settings applied"
- "LLM proxy request received"

---

## Customizing Voice

Edit `~/deepclaw/deepclaw/voice_agent_server.py`, find `get_agent_config()`, change the `model` in `speak`:

```python
"speak": {"provider": {"type": "deepgram", "model": "aura-2-orion-en"}},
```

### Voice Options

**English:** thalia (F, default), orion (M), apollo (M), athena (F), luna (F), zeus (M), draco (M, British), pandora (F, British), hyperion (M, Australian)

**Spanish:** estrella (F, Mexican), javier (M, Mexican), alvaro (M, Spain), celeste (F, Colombian)

**German:** fabian (M), aurelia (F), lara (F)

**French:** hector (M), agathe (F)

**Italian:** cesare (M), livia (F)

**Dutch:** lars (M), daphne (F)

**Japanese:** ebisu (M), izanami (F)

Format: `aura-2-<name>-<lang>` (e.g., `aura-2-estrella-es`)

---

## Troubleshooting

When something goes wrong, check the server logs first. Here's how to diagnose common issues:

### No server logs when calling

**Symptom:** You call, phone hangs up, but no logs appear in the server terminal.

**Cause:** Twilio webhook URL doesn't match your ngrok URL.

**Fix:**
1. Check your current ngrok URL in the ngrok terminal
2. Go to Twilio Console → Phone Numbers → Your Number → Voice Configuration
3. Make sure the webhook URL matches exactly: `https://<your-ngrok-url>/twilio/incoming`
4. Save and try again

### "Check your think provider settings" error

**Symptom:** Call connects, you hear the greeting, then Deepgram says "Check your think provider settings" and hangs up.

**Cause:** Deepgram can't reach the LLM proxy endpoint, or it's returning an error.

**Fix:**
1. Test the proxy endpoint directly:
   ```bash
   curl -X POST https://<your-ngrok-url>/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"gpt-4","messages":[{"role":"user","content":"hi"}]}'
   ```
2. If you get `401 Unauthorized`, the auth is blocking requests. This shouldn't happen with the latest code.
3. If you get connection refused, the server isn't running or ngrok isn't forwarding.
4. Check that OpenClaw gateway is running: `curl http://127.0.0.1:18789/health`

### Call works once then hangs up

**Symptom:** First exchange works (greeting + one response), then call drops with "FAILED_TO_THINK" in logs.

**Cause:** SSE stream formatting issue—usually fixed in latest code.

**Fix:**
1. Make sure you have the latest code: `cd ~/deepclaw && git pull`
2. Restart the server

### Words running together in speech

**Symptom:** TTS says "Whydo you want" instead of "Why do you want"

**Cause:** Markdown stripping was removing spaces between streaming chunks.

**Fix:**
1. Update to latest code: `cd ~/deepclaw && git pull`
2. Restart the server

### Inbound calls don't work, but everything else does

**Symptom:** Server responds to curl, ngrok works, but calling from your phone gets immediate disconnect with no logs.

**Cause:** Your carrier may be blocking calls to the Twilio number, or you're dialing wrong.

**Fix:**
1. Verify you're dialing the exact Twilio number (with country code if needed)
2. Try calling from a different phone
3. Test with an outbound call from Twilio to you:
   ```python
   # Run this in Python with your .env loaded
   import requests
   requests.post(
       f'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Calls.json',
       auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
       data={
           'To': '+1YOURNUMBER',
           'From': '+1TWILIONUMBER',
           'Url': 'https://<your-ngrok-url>/twilio/incoming'
       }
   )
   ```
   If this works, the issue is your carrier blocking outbound calls to Twilio.

### OpenClaw returns errors

**Symptom:** Logs show errors from OpenClaw like "No API key found for provider"

**Fix:**
1. Make sure OpenClaw is configured with your Anthropic API key
2. Run `openclaw configure --section model` to set it up
3. Restart OpenClaw gateway: `openclaw daemon restart`

### ngrok URL keeps changing

**Symptom:** Every time you restart ngrok, you get a new URL and have to update Twilio.

**Fix:** Use a fixed ngrok domain (requires ngrok account):
```bash
ngrok http 8000 --domain=your-chosen-name.ngrok-free.app
```

### Still stuck?

1. Check the server logs carefully—they usually tell you what's wrong
2. Test each component individually:
   - Server health: `curl http://localhost:8000/health`
   - ngrok forwarding: `curl https://<ngrok-url>/health`
   - OpenClaw gateway: `curl http://127.0.0.1:18789/health`
   - LLM proxy: `curl -X POST https://<ngrok-url>/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"gpt-4","messages":[{"role":"user","content":"test"}]}'`
3. Open an issue at https://github.com/deepgram/deepclaw/issues
