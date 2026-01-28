---
name: speech-generator
description: "Generate speech audio from text using ElevenLabs TTS. Use when user asks to 'send voice', 'send audio message', 'create voice', 'generate speech', 'say something', 'voice message', 'send me audio', or needs TTS/narration."
version: "1.0.0"
author: aviz85
tags:
  - tts
  - speech
  - audio
  - elevenlabs
  - voice
setup: "./SETUP.md"
---

# Speech Generator

Generate speech audio using ElevenLabs TTS.

## Voice ID

Configure your voice ID from ElevenLabs:

```
YOUR_VOICE_ID
```

> Get voice IDs from [ElevenLabs](https://elevenlabs.io/) - you can use built-in voices or clone your own.

## Prompt Guidelines (Hebrew)

Write prompts as natural spoken Hebrew. Use square brackets `[...]` for speech directions.

### Direction Examples

```
[נשימה עמוקה] אוקיי, אז בואו נדבר על זה...
[צחוק קל] זה ממש מצחיק שאתה אומר את זה
[בהתלהבות] וואו! זה בדיוק מה שחיכיתי לו!
[ברצינות] עכשיו, תקשיבו טוב...
[בעצב] אני לא יודע מה להגיד...
[בשקט] זה סוד, אבל...
[מהר] צריך לרוץ עכשיו, אין זמן!
[לאט ובבירור] חשוב. מאוד. להקשיב.
[שאלה] אתה בטוח שזה מה שאתה רוצה?
[הפתעה] רגע, מה?!
```

### Natural Speech Patterns

Add filler words and pauses for natural flow:
- `אממ...`
- `אהה...`
- `כאילו...`
- `נו...`
- `יאללה...`
- `בקיצור...`
- `...` (pause)

### Example Prompt

```
[בהתלהבות] היי! מה קורה?
אממ... אז רציתי לספר לכם משהו מטורף שקרה לי היום.
[נשימה] אז הלכתי לקפה, וואלה, פתאום רואה את... [בשקט] אתה לא תאמין למי.
[צחוק] כן, בדיוק מי שחשבת!
```

## Commands

```bash
cd ~/.claude/skills/speech-generator/scripts

# Generate speech
npx ts-node generate_speech.ts \
  -t "[בהתלהבות] היי! מה קורה?" \
  -o /path/to/output.mp3

# From file
npx ts-node generate_speech.ts \
  -f /path/to/script.txt \
  -o /path/to/output.mp3

# List voices
npx ts-node generate_speech.ts --list-voices
```

## Options

| Option | Short | Default |
|--------|-------|---------|
| `--text` | `-t` | Text to speak |
| `--file` | `-f` | Read from file |
| `--output` | `-o` | Output path (required) |
| `--voice` | `-v` | Voice ID |
| `--speed` | | 1.0 |
| `--stability` | | 0.5 |
| `--similarity` | | 0.75 |
