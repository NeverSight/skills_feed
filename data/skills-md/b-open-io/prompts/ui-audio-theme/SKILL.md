---
version: 1.0.0
name: ui-audio-theme
description: Generate cohesive UI audio themes with subtle, minimal sound effects for applications. This skill should be used when users want to create a set of coordinated interface sounds for wallet apps, dashboards, or web applications - generating sounds mapped to UI interaction constants like button clicks, notifications, and navigation transitions using ElevenLabs API.
location: user
---

# UI Audio Theme Generator

Generate cohesive sets of subtle, minimal UI sound effects using ElevenLabs text-to-sound-effects API. Create "audio themes" - coordinated sets of sounds that share a common aesthetic and map to standard UI interaction constants.

## Prerequisites

```bash
# Verify ElevenLabs API key is configured
echo $ELEVENLABS_API_KEY

# If not set, get key from https://elevenlabs.io (Profile -> API Keys)
# Add to shell profile: export ELEVENLABS_API_KEY="your-key"
```

## Workflow

### Step 1: Discover the UI Vibe

Before generating sounds, understand the application's aesthetic:

**Application Context:**
- What type of app? (wallet, dashboard, social, productivity)
- Primary user emotion? (trust, delight, focus, calm)
- Professional or playful interface?

**Audio Direction:**
- Preferred tone? (warm/organic, clean/digital, retro/nostalgic, futuristic)
- Reference sounds? (Apple-like clicks, game bleeps, banking chimes)

### Step 2: Select a Vibe Preset

Available presets in `assets/vibe-presets.json`:

| Preset | Tone | Best For |
|--------|------|----------|
| `corporate-trust` | Warm, professional | Banking, finance |
| `crypto-modern` | Digital, clean | Wallet apps, trading |
| `playful-delight` | Bright, friendly | Social, consumer |
| `minimal-focus` | Ultra-subtle | Productivity, tools |
| `retro-digital` | 8-bit inspired | Games, nostalgic |
| `premium-luxury` | Rich, refined | High-end apps |

### Step 3: Generate the Audio Theme

```bash
# Using preset vibe
python scripts/generate_theme.py \
  --vibe "crypto-modern" \
  --output-dir "./audio-theme"

# Using custom vibe description
python scripts/generate_theme.py \
  --vibe-custom "warm organic subtle wooden interface sounds" \
  --output-dir "./audio-theme"

# Generate specific categories only
python scripts/generate_theme.py \
  --vibe "crypto-modern" \
  --categories buttons feedback transactions \
  --output-dir "./audio-theme"

# List available presets
python scripts/generate_theme.py --list-vibes

# List all sound names
python scripts/generate_theme.py --list-sounds
```

### Step 4: Regenerate Individual Sounds

```bash
python scripts/generate_theme.py \
  --regenerate "button-click-primary,notification-success" \
  --vibe "crypto-modern" \
  --output-dir "./audio-theme"
```

## Sound Categories

### Buttons
| Constant | Description |
|----------|-------------|
| `button-click-primary` | Main action buttons |
| `button-click-secondary` | Secondary/ghost buttons |
| `button-click-destructive` | Delete/cancel actions |

### Navigation
| Constant | Description |
|----------|-------------|
| `nav-tab-switch` | Tab navigation |
| `nav-back` | Back button/gesture |
| `nav-forward` | Forward navigation |
| `nav-menu-open` | Menu drawer open |
| `nav-menu-close` | Menu dismiss |

### Feedback
| Constant | Description |
|----------|-------------|
| `notification-success` | Success confirmation |
| `notification-error` | Error alert |
| `notification-warning` | Warning indicator |
| `notification-info` | Information notice |
| `notification-badge` | Badge/counter update |

### States
| Constant | Description |
|----------|-------------|
| `toggle-on` | Switch enabled |
| `toggle-off` | Switch disabled |
| `checkbox-check` | Checkbox selected |
| `checkbox-uncheck` | Checkbox deselected |
| `loading-start` | Loading initiated |
| `loading-complete` | Loading finished |

### Modals
| Constant | Description |
|----------|-------------|
| `modal-open` | Modal appearance |
| `modal-close` | Modal dismissal |
| `tooltip-show` | Tooltip reveal |
| `dropdown-open` | Dropdown expand |
| `dropdown-close` | Dropdown collapse |

### Transactions (Wallet-specific)
| Constant | Description |
|----------|-------------|
| `tx-sent` | Transaction sent |
| `tx-received` | Payment received |
| `tx-pending` | Transaction waiting |
| `tx-confirmed` | Confirmation success |

## Output Structure

```
audio-theme/
├── theme.json              # Theme manifest
├── constants.ts            # TypeScript constants
├── buttons/
│   ├── button-click-primary.mp3
│   ├── button-click-secondary.mp3
│   └── button-click-destructive.mp3
├── navigation/
├── feedback/
├── states/
├── modals/
└── transactions/
```

## Integration

### TypeScript Usage

The generated `constants.ts` exports ready-to-use constants:

```typescript
import { UI_SOUNDS } from './audio-theme/constants';

const audio = new Audio(UI_SOUNDS.BUTTON_CLICK_PRIMARY);
audio.volume = 0.3;
audio.play();
```

### React Hook

```typescript
import { useCallback, useEffect, useRef } from 'react';

export function useUISound(soundUrl: string, volume = 0.3) {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    audioRef.current = new Audio(soundUrl);
    audioRef.current.volume = volume;
    audioRef.current.preload = 'auto';
    return () => { audioRef.current = null; };
  }, [soundUrl, volume]);

  const play = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.currentTime = 0;
      audioRef.current.play().catch(() => {});
    }
  }, []);

  return play;
}

// Usage
function SendButton() {
  const playClick = useUISound(UI_SOUNDS.BUTTON_CLICK_PRIMARY);
  return <button onClick={() => { playClick(); sendTransaction(); }}>Send</button>;
}
```

### Howler.js

```typescript
import { Howl } from 'howler';

const sounds = {
  click: new Howl({ src: [UI_SOUNDS.BUTTON_CLICK_PRIMARY], volume: 0.3 }),
  success: new Howl({ src: [UI_SOUNDS.NOTIFICATION_SUCCESS], volume: 0.4 }),
};

// Play on interaction
sounds.click.play();
```

## Best Practices

### Volume Recommendations
UI sounds should be mixed at 20-40% to remain unobtrusive.

### Accessibility
- Never rely solely on audio for critical information
- Provide visual alternatives for all audio feedback
- Allow users to disable sounds in settings

### Subtlety Principle
The more frequently a sound occurs, the subtler it should be. Button clicks should be nearly imperceptible; transaction confirmations can be more noticeable.

## Script Options

```
--vibe NAME           Preset vibe name
--vibe-custom DESC    Custom vibe description
--output-dir PATH     Output directory (default: ./audio-theme)
--format FORMAT       mp3 or wav (default: mp3)
--categories CATS     Specific categories to generate
--regenerate SOUNDS   Comma-separated sounds to regenerate
--prompt-influence N  0-1, higher = stricter prompt adherence (default: 0.5)
--list-vibes          Show available presets
--list-sounds         Show all sound names
```

## Resources

- `scripts/generate_theme.py` - CLI tool for generating themes
- `references/sound-design-guide.md` - Detailed sound design best practices
- `assets/vibe-presets.json` - Predefined vibe configurations
- `assets/theme-template.json` - Example output manifest

## Content-Specialist Integration

For custom sound generation beyond standard categories, use the content-specialist agent which has full ElevenLabs API integration for sound effects, music, and voice generation.
