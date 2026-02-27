---
name: speak
description: Automatically announces plans, issues, and summaries out loud using TTS. Use this skill PROACTIVELY after completing major tasks like finalizing a plan, resolving an issue, or generating a summary. Each project gets a unique voice so users can identify which project is speaking from another room. Providers fallback in order (google, openai, elevenlabs, say) on rate limits.
---

# Speak

Announce plans, issues, and summaries aloud using project-specific voices. Triggered automatically after major milestones.

## When to Announce

Announce automatically after:
- **Planning complete** - When a plan/todo list is finalized
- **Issue resolved** - When a bug fix or error is resolved
- **Summary generated** - When completing a sprint or major task

## Configuration

Store config at `.claude/tts-config.json` in the project root:

```json
{
  "provider_order": ["google", "openai", "elevenlabs", "say"],
  "unavailable_providers": [],
  "voices": {
    "planning": { "provider": "google", "voice": "Kore", "style": "calm" },
    "issue": { "provider": "google", "voice": "Aoede", "style": "urgent" },
    "summary": { "provider": "google", "voice": "Charon", "style": "satisfied" }
  },
  "assigned_at": "2025-01-15T10:30:00Z"
}
```

On first use in a new project, auto-generate config by selecting unused voices from the voice pool (see `references/voice-pools.json`).

**Note:** `say` (macOS) requires no API key and should always work as final fallback.

## Workflow

1. **Detect message type** - planning, issue, or summary
2. **Load config** - Read `.claude/tts-config.json` or create if missing
3. **Select provider** - Use first provider from `provider_order` not in `unavailable_providers`
4. **Transform text** - Convert to speech-friendly format (see below)
5. **Speak** - Call appropriate TTS tool with configured voice
6. **Handle failures** - See error handling below

## Error Handling

When a TTS call fails, check the error type:

| Error Pattern | Action |
|---------------|--------|
| "API key", "unauthorized", "authentication", "GOOGLE_API_KEY", "OPENAI_API_KEY", "ELEVENLABS_API_KEY" | Add provider to `unavailable_providers`, save config, try next |
| "rate limit", "quota", "429" | Try next provider (temporary) |
| Other errors | Try next provider |

**Critical:** On auth/config errors, immediately update `.claude/tts-config.json` to add the provider to `unavailable_providers`. This persists across sessions and prevents wasted attempts.

Example after Google fails due to missing API key:
```json
{
  "provider_order": ["google", "openai", "elevenlabs", "say"],
  "unavailable_providers": ["google"],
  ...
}
```

The agent will now skip Google and start with OpenAI on next announcement.

## Text Transformation

Convert verbose output to conversational speech:

| Remove/Replace | With |
|----------------|------|
| URLs | "see the link" or omit |
| Code blocks | "see the code changes" or brief description |
| File paths | Just the filename (e.g., `/src/lib/foo.rs` -> "foo.rs") |
| Long hashes/IDs | "a commit hash" or omit |
| Long number lists | "several values" or count |
| Markdown formatting | Plain text |
| Technical jargon | Simpler alternatives when possible |

**Target length**: ~15-30 seconds of speech (roughly 50-100 words)

**Tone by type**:
- Planning: "Here's the plan..." (forward-looking, organized)
- Issue: "Found a problem..." (alert but calm)
- Summary: "All done..." (satisfied, accomplished)

## TTS Tools

### google_tts (preferred)
```
mcp__mcp-tts__google_tts
- text: string (required)
- voice: string (default: "Kore")
- model: string (default: "gemini-2.5-flash-preview-tts")
```

Voices: Achernar, Achird, Algenib, Algieba, Alnilam, Aoede, Autonoe, Callirrhoe, Charon, Despina, Enceladus, Erinome, Fenrir, Gacrux, Iapetus, Kore, Laomedeia, Leda, Orus, Puck, Pulcherrima, Rasalgethi, Sadachbia, Sadaltager, Schedar, Sulafat, Umbriel, Vindemiatrix, Zephyr, Zubenelgenubi

### openai_tts (fallback 1)
```
mcp__mcp-tts__openai_tts
- text: string (required)
- voice: string (default: "alloy") - alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer, verse
- model: string (default: "gpt-4o-mini-tts")
- speed: number (0.25-4.0, default: 1.0)
- instructions: string (voice modulation hints)
```

### elevenlabs_tts (fallback 2)
```
mcp__mcp-tts__elevenlabs_tts
- text: string (required)
```

### say_tts (fallback 3 - local/free)
```
mcp__mcp-tts__say_tts
- text: string (required)
- voice: string (OPTIONAL - prefer leaving unset to use system default voice which sounds more natural)
- rate: integer (RECOMMENDED: 200-250 for natural speech, max 300 unless user asks faster; default: 200)
```

**IMPORTANT for say_tts:**
- Do NOT set a voice unless the user explicitly requests one - the system default sounds most natural
- Keep rate between 200-250 for comfortable listening; only go up to 275-300 if user wants faster speech

## Auto-Assignment

When creating config for a new project:

1. Read `references/voice-pools.json` for available voices
2. Check `~/.claude/tts-unavailable.json` for globally unavailable providers (shared across projects)
3. Scan `~/.claude/tts-assignments.json` for voices already assigned to other projects
4. Select 3 unused voices (one per message type) from first available provider
5. If all voices used, cycle back with provider variation
6. Save assignment to both project config and global assignments file

When a provider is marked unavailable in any project, also update `~/.claude/tts-unavailable.json`:
```json
{
  "unavailable": ["google", "elevenlabs"],
  "updated_at": "2025-01-15T10:30:00Z"
}
```

This prevents new projects from attempting providers known to be unconfigured.

## Examples

**Planning** (after TodoWrite with multiple items):
> "Here's the plan for the authentication feature. First, I'll create the login component. Then add session management. Finally, write the tests. Three tasks total."

**Issue** (after fixing an error):
> "Found and fixed an issue. The rate limiter wasn't catching timeout errors. Added a try-catch block in the handler. Tests are passing now."

**Summary** (after completing a feature):
> "All done with the authentication system. Added login, logout, and session management. Created five new files and updated the main router. Ready for review."
