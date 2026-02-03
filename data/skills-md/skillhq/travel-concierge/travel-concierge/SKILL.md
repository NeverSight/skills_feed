---
name: travel-concierge
description: Find accommodation contact details and run AI-assisted booking calls
version: 1.3.1
triggers:
  - find contact
  - hotel contact
  - accommodation contact
  - property contact
  - airbnb contact
  - booking contact
  - vrbo contact
  - expedia contact
  - direct booking
  - property email
  - property phone
  - call hotel
  - call property
  - direct booking call
---

# Travel Concierge

Find contact details (phone, email, WhatsApp, Instagram, etc.) for accommodation listings and place AI booking calls.

## Capabilities

### 1) Find contact details from a listing URL

```bash
travel-concierge find-contact "<url>"
```

### 2) Place an autonomous phone call

```bash
travel-concierge call "+1-555-123-4567" \
  --goal "Book a room for March 12-14" \
  --name "Derek Rein" \
  --email "alexanderderekrein@gmail.com" \
  --customer-phone "+1-555-000-1111" \
  --context "Prefer direct booking if rate beats Booking.com"
```

The `call` command now auto-manages infra by default: if local server is down, it starts `ngrok` + call server automatically and stops both when the call ends.

## Supported listing platforms

- **Airbnb**: `airbnb.com/rooms/...`
- **Booking.com**: `booking.com/hotel/...`
- **VRBO**: `vrbo.com/...`
- **Expedia**: `expedia.com/...Hotel...`

## Examples

### Find contacts for an Airbnb listing
Run:
```bash
travel-concierge find-contact "https://www.airbnb.com/rooms/12345"
```

### Start a call and control turns manually
Run:
```bash
travel-concierge call "+1-555-123-4567" \
  --goal "Negotiate a direct booking rate" \
  --name "Derek Rein" \
  --email "alexanderderekrein@gmail.com" \
  --customer-phone "+1-555-000-1111" \
  --interactive
```

### JSON output for scripting (contact lookup)
```bash
travel-concierge find-contact --json "https://..."
```

### Verbose output
```bash
travel-concierge --verbose find-contact "https://..."
```

## Configuration

The CLI stores configuration in:

`~/.config/travel-concierge/config.json5`

### Optional for contact lookup

```bash
travel-concierge config set googlePlacesApiKey "your-key"
```

### Required for AI phone calls

```bash
travel-concierge config set twilioAccountSid "<sid>"
travel-concierge config set twilioAuthToken "<token>"
travel-concierge config set twilioPhoneNumber "+14155551234"
travel-concierge config set deepgramApiKey "<key>"
travel-concierge config set elevenLabsApiKey "<key>"
travel-concierge config set elevenLabsVoiceId "EXAVITQu4vr4xnSDxMaL"
travel-concierge config set anthropicApiKey "<key>"

# Optional for auto ngrok auth
travel-concierge config set ngrokAuthToken "<token>"
```

Check values:

```bash
travel-concierge config show
```

## Notes

- Contact extraction uses publicly available information.
- `call` validates local dependencies before dialing (`ffmpeg` with MP3 decode support, and `ngrok` when auto-infra is needed).
- `call` runs preflight checks for Twilio, Deepgram, and ElevenLabs quota before dialing.
- When auto infra is used, server/ngrok logs are written under `~/.config/travel-concierge/call-runs/<run-id>/`.
