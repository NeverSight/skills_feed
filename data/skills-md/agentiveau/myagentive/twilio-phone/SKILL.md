---
name: twilio-phone
description: Make phone calls with natural AI voices (ElevenLabs) and send SMS using Twilio CLI. Use this skill when the user wants to make a phone call, send a text message, or use AI-generated voice for calls. Requires Twilio CLI authenticated and ElevenLabs API key.
---

# Twilio Phone Skill

Make phone calls with natural AI-generated voices (ElevenLabs) and send SMS using the official Twilio CLI.

## Quick Start - AI Voice Call

To make a call with a natural ElevenLabs voice, run the script:

```bash
./.claude/skills/twilio-phone/scripts/voice_call.py \
  --to "+61XXXXXXXXXX" \
  --message "Your message here"
```

## Available Phone Numbers

| Number | Region | Use For |
|--------|--------|---------|
| +61 3 4827 9516 | Australia | Australian calls/SMS |
| +1 978 878 5597 | USA | US calls/SMS |

## ElevenLabs Voices

| Voice ID | Name | Accent |
|----------|------|--------|
| IKne3meq5aSn9XLyUdCD | Charlie | Australian |
| JBFqnCBsd6RMkjVDRZzb | George | British |
| Xb7hH8MSUJpSbSDYk0k2 | Alice | British |
| EXAVITQu4vr4xnSDxMaL | Sarah | American |
| CwhRBWXzGAHq8TQ4Fs17 | Roger | American |

**Default:** Charlie (Australian) with `eleven_v3` model

## Manual Process (Step by Step)

### 1. Generate audio with ElevenLabs

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/IKne3meq5aSn9XLyUdCD?output_format=mp3_44100_128" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your message here",
    "model_id": "eleven_v3",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.75
    }
  }' \
  --output /tmp/call_audio.mp3
```

### 2. Upload audio to public URL

```bash
curl -s -X POST -F "file=@/tmp/call_audio.mp3" "https://tmpfiles.org/api/v1/upload"
# Returns: {"data":{"url":"http://tmpfiles.org/XXXXXX/call_audio.mp3"}}
# Convert to direct URL: https://tmpfiles.org/dl/XXXXXX/call_audio.mp3
```

### 3. Make call with Twilio

```bash
twilio api:core:calls:create \
  --from "+61348279516" \
  --to "+61XXXXXXXXXX" \
  --twiml "<Response><Play>https://tmpfiles.org/dl/XXXXXX/call_audio.mp3</Play></Response>"
```

## Basic Twilio TTS Call (No ElevenLabs)

```bash
twilio api:core:calls:create \
  --from "+61348279516" \
  --to "+61XXXXXXXXXX" \
  --twiml "<Response><Say voice=\"alice\" language=\"en-AU\">Your message here.</Say></Response>"
```

## Sending SMS

```bash
twilio api:core:messages:create \
  --from "+61348279516" \
  --to "+61XXXXXXXXXX" \
  --body "Your message here"
```

## TwiML Elements

### Play - Play audio file
```xml
<Response><Play>https://example.com/audio.mp3</Play></Response>
```

### Say - Text to speech (Twilio built-in)
```xml
<Response><Say voice="alice" language="en-AU">Text to speak</Say></Response>
```

### Pause - Add silence
```xml
<Pause length="2"/>
```

### Gather - Collect DTMF input
```xml
<Gather numDigits="1" action="https://example.com/handle-key">
  <Say>Press 1 for sales, 2 for support.</Say>
</Gather>
```

## Call Options

| Option | Description |
|--------|-------------|
| `--timeout 30` | Ring for 30 seconds before giving up |
| `--record` | Record the call |
| `--machine-detection Enable` | Detect answering machines |
| `--send-digits "W1234#"` | Dial extension after connecting |

## Check Status

```bash
# List recent calls
twilio api:core:calls:list --limit 10

# Get specific call details
twilio api:core:calls:fetch --sid CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# List recent SMS
twilio api:core:messages:list --limit 10
```

## Environment Variables

Required in `.env`:
```
ELEVENLABS_API_KEY=sk_xxxxx
```

Twilio CLI must be authenticated first. Run `twilio login` to configure.

## Important Notes

1. **Phone format**: Use E.164 format (+61 for Australia, +1 for US)
2. **Australian mobiles**: +614XXXXXXXX (drop leading 0)
3. **Audio hosting**: tmpfiles.org URLs expire after some time
4. **ElevenLabs model**: `eleven_v3` is the most natural sounding
5. **Default voice**: Charlie (Australian accent)
