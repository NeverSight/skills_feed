---
name: oxi-e16
description: OXI E16 MIDI controller scene configuration. Use when creating, editing, or analyzing .oxie16 scene files for the OXI E16 controller. Handles MIDI CC, NRPN, and 14-bit mappings for synthesizers and other MIDI gear.
---

# OXI E16 Scene Configuration

Create and edit `.oxie16` scene files for the OXI E16 MIDI controller.

## File Format

Scene files are JSON with this structure.

### Title Length Limit

Scene titles truncate to ~7 characters on the E16 display. Use common abbreviations:

| Device | Abbreviation |
|--------|--------------|
| Digitone II | DN2 |
| Digitakt II | DT2 |
| Syntakt | SYN |
| Analog Four | A4 |
| Analog Rytm | AR |
| Octatrack | OT |
| Model:Cycles | MC |
| Model:Samples | MS |

### Elektron MIDI Channels

Elektron devices have special MIDI channels (configurable in device settings):

| Channel | Default | Purpose |
|---------|---------|---------|
| Auto Channel | 10 | Controls the currently selected/active track |
| FX Control | 9 | Controls global FX parameters (Delay, Reverb, Chorus) |
| Tracks 1-8 | 1-8 | Individual track control |

**Auto Channel** is useful for E16 scenes - instead of hardcoding track 1, use the auto channel so the controller follows your track selection on the device.

**FX Control Channel** controls the master FX block (delay/reverb parameters, not per-track sends). Per-track sends use the track's channel.

### Icon Format

Icons are 16×16 1-bit bitmaps stored as **exactly 32 bytes** (2 bytes per row):
- Byte 0 = pixels 0-7, Byte 1 = pixels 8-15
- Bit 7 = leftmost pixel in each byte (MSB = left)
- Row 0 at bytes 0-1, Row 1 at bytes 2-3, etc.

**CRITICAL:** Icon must be exactly 32 bytes or the scene will fail to load silently.

#### Designing Icons

Study the reference icons in `references/icons/` (Nikoichu 1-bit Pixel Icons, CC0 licensed).

**Key principles for 16×16 1-bit icons:**

1. **Thin strokes (1-2px)** — Use 1-2 pixel stroke widths consistently. Avoid chunky 4px blocks.
2. **Outline over fill** — Prefer outlines with internal details over solid fills. ~90% of good icons are outline-dominant.
3. **Diagonal stepping** — 45° diagonals step 1:1 (one right, one down). Shallower angles use 2:1. This creates optical smoothness.
4. **Single-pixel endpoints** — Arrows, points, lightning, and tapered shapes terminate in single pixels.
5. **Fill the space** — Use 12-14 of the 16 rows; leave 1-2 rows margin on each side.
6. **Center if not filling** — If the icon doesn't fill the full 16×16, center it both vertically and horizontally.
7. **Negative space is design** — Empty areas define shapes as much as filled pixels. Don't over-fill.
8. **Minimal detail** — Include only features that aid recognition. Suggest complexity through pattern, not detail.
9. **Clear silhouette** — The icon should be recognizable even if filled solid.
10. **Symbolic over text** — Abstract symbols read better than tiny text at this size.

**Design process:**
1. Study similar icons in `references/icons/Sprites/` for technique
2. Sketch on 16×16 grid, starting with essential silhouette
3. Use 1-2px outlines, not solid fills
4. Apply diagonal stepping for angled lines
5. Taper points to single pixels
6. Remove any detail that doesn't improve recognition

**Previewing icons in terminal:**

Use double-width characters for better terminal rendering:

```
██ = on pixel (two full blocks)
░░ = off pixel (two light shade blocks)
```

Example (vinyl disc icon):
```
░░░░░░░░░░░░░░██████░░░░░░░░░░░░
░░░░░░░░░░██████████████░░░░░░░░
░░░░░░░░████████████████░░░░░░░░
░░░░░░██████████████████████░░░░
░░░░████████░░░░░░░░████████░░░░
░░░░██████░░░░░░░░░░░░██████░░░░
░░░░████████░░░░████░░████████░░
░░░░██████░░████████░░░░██████░░
░░░░██████░░████████░░░░██████░░
░░░░████████░░░░████░░████████░░
░░░░██████░░░░░░░░░░░░░░██████░░
░░░░████████░░░░░░░░████████░░░░
░░░░░░██████████████████████░░░░
░░░░░░░░████████████████░░░░░░░░
░░░░░░░░░░██████████████░░░░░░░░
░░░░░░░░░░░░░░██████░░░░░░░░░░░░
```

Each row is 32 characters wide (16 pixels × 2 chars each).

To convert ASCII art to bytes:
```
Row: ##....## ........
     ││    ││ ││││││││
     Byte 0   Byte 1

##....## = 11000011 = 195 (0xC3)
........ = 00000000 = 0   (0x00)
→ [195, 0]
```

#### Icon Ideas (Symbolic)

| Device Type | Icon Concept |
|-------------|--------------|
| Sampler/Drum machine | Waveform with playhead, sample slice, drum pad grid |
| Synth (mono/poly) | Oscillator waveform, filter sweep, VCO symbol |
| Sequencer | Step grid, play arrow, clock/metronome |
| Effects unit | Delay taps, reverb waves, modulation wave |
| Groovebox | Combined waveform + grid, pattern indicator |
| Sample mangler | Broken/glitched waveform, disc/vinyl, spiral |

**Avoid text** — Device abbreviations like "DT2" don't read well at 16×16. Use symbolic representations instead.

#### Waveform & Synth Icon Techniques

See reference icons in `references/icons/Sprites/`:
- `Media_Audio_Visualizer_VU_Meters.png` — Fader/level meter technique
- `Software_Options_Settings_Sliders_Knobs_Audio.png` — Knob/slider technique
- `Software_Power_Electricity_Battery_Thunder_Lightning_Bolt_Zap.png` — Thin 1-2px lightning

**Waveforms**: Use 1px strokes. Saw = diagonal ramp + vertical drop. Square = horizontal/vertical steps. Triangle = symmetric diagonals.

**Knobs**: Circle outline (1px) with position indicator inside.

**Faders**: Vertical 1px tracks with small handle rectangles at varying heights.

**Lightning**: Sharp 45° diagonals, sudden angle changes, 1-2px strokes, single-pixel tip.

#### Example: Sine Wave
```
[0,0,8,0,20,0,34,0,0,0,65,0,0,0,128,128,0,0,0,65,0,0,0,34,0,20,0,8,0,0,0,0]
```

#### Example: Device Face (Digitone II style)
```
[255,255,192,3,222,171,222,3,222,171,192,3,255,255,192,3,219,219,219,219,192,3,219,219,219,219,192,3,255,255,0,0]
```

```json
{
  "title": "Scene Name",
  "icon": [32 bytes],
  "selectedPreset": 0,
  "code": {"code": ""},
  "pages": [12 pages]
}
```

### Page Structure

```json
{
  "title": "Page Name",
  "output": 0,
  "channel": 1,
  "encoders": [16 encoders]
}
```

- `channel`: Default MIDI channel for the page (1-16)
- `output`: MIDI output (0 = default)

### Encoder Structure

```json
{
  "name": "Display Name (8 char max)",
  "abbr": "Abbr (4 char)",
  "color": 0,
  "push_action": {...},
  "turn_actions": [{primary}, {secondary}],
  "bipolar": false
}
```

**CRITICAL:** Field order matters! The `bipolar` field must come AFTER `turn_actions`, not before.

#### Color Values

10x10 palette (0-99), indexed left-to-right, top-to-bottom:
- Row 0 (0-9): Purple → Deep Blue → Blue → Periwinkle
- Row 1 (10-19): Dark Blue → Blue → Purple-Blue → Lavender
- Row 2 (20-29): Blue-Gray → Slate → Purple-Gray → Light Lavender
- Row 3 (30-39): Olive/Brown → Rust → Orange-Brown → Khaki
- Row 4 (40-49): Olive → Brown → Orange → Salmon → Yellow
- Row 5 (50-59): Red → Crimson → Magenta-Red → Pink → Orange-Red
- Row 6 (60-69): Dark Red → Crimson → Magenta → Purple-Pink → Red
- Row 7 (70-79): Dark Purple → Magenta → Pink-Magenta → Blue-Purple → Cyan
- Row 8 (80-89): Dark Teal → Teal → Cyan → Green-Cyan → Blue-Cyan
- Row 9 (90-99): Dark Green → Green → Lime → Light Green

#### Color Schemes

**IMPORTANT: Ask the user about their color preferences before assigning colors.** Different users have different organizational preferences.

**Common color coding strategies:**

| Strategy | Description | Best For |
|----------|-------------|----------|
| **By parameter type** | Oscillators=blue, Filters=cyan, Envelopes=orange, Effects=purple, Levels=green | Learning a new synth |
| **By function** | All volumes same color, all pans same, all sends same | Quick visual scanning |
| **By page theme** | Each page has a distinct color palette | Multi-synth setups |
| **By behavior** | Bipolar=one color, levels=another, discrete=another | Understanding parameter ranges |
| **By importance** | Frequently-tweaked params bright, others muted | Live performance |
| **Uniform** | All same color (0), rely on display text | Minimal distraction |

**Suggested palette for "by parameter type":**

| Category | Color | Value |
|----------|-------|-------|
| Oscillators | Blue | 4-6 |
| Filters | Cyan/Teal | 83-85 |
| Filter Envelopes | Orange | 45-47 |
| Amp Envelopes | Salmon/Pink | 48-57 |
| LFOs/Modulation | Magenta | 73-75 |
| Effects (Delay/Reverb) | Purple | 0, 70-72 |
| Chorus | Light Purple | 17-19 |
| Levels/Volume | Green | 92-94 |
| Pan/Stereo | Lavender | 7-9 |
| Sends | Brown/Rust | 32-35 |
| Bit Crush/SRR | Red | 50-52 |
| Overdrive | Dark Red | 60-62 |

**When creating a scene, ask the user:**
1. "Do you want color-coded encoders? If so, which strategy?"
2. "Any specific colors for certain parameter types?"
3. "Should each page have a distinct color theme?"

### Turn Action (MIDI Mapping)

**CRITICAL:** All action objects (push_action, turn_actions[0], turn_actions[1]) must include ALL fields. Do NOT use shorthand like `{"type": 0}` — the app will fail to load the scene silently.

```json
{
  "instrument": 127,
  "parameter": 0,
  "type": 9,
  "display": 10,
  "mode": 3,
  "channel": 0,
  "lower": 0,
  "upper": 127,
  "defaultValue": 0,
  "nr1": 73,
  "nr2": 1,
  "output": 12
}
```

**Disabled action template** (use this instead of `{"type": 0}`):
```json
{
  "instrument": 127,
  "parameter": 0,
  "type": 0,
  "display": 0,
  "mode": 0,
  "channel": 0,
  "lower": 0,
  "upper": 127,
  "defaultValue": 0,
  "nr1": 0,
  "nr2": 0,
  "output": 12
}
```

#### Type Values

| Type | Mode |
|------|------|
| 0 | OFF (disabled) |
| 1 | CC Rel 1 (relative) |
| 2 | CC Rel 2 (relative) |
| 3 | CC Abs (absolute) |
| 4 | CC14 (14-bit high res) |
| 5 | PC (Program Change) |
| 6 | PB (Pitch Bend) |
| 7 | AT (Aftertouch) |
| 8 | NOTE |
| 9 | NRPN |
| 10 | SNAPSHOT |

#### NRPN Fields

- `nr1`: **LSB** (CC#98 value)
- `nr2`: **MSB** (CC#99 value)

Example: NRPN MSB 1, LSB 73 → `nr1: 73, nr2: 1`

#### CC Fields

- `nr1`: CC number (0-127)
- `nr2`: 0 (unused)

#### Other Fields

| Field | Value | Meaning |
|-------|-------|---------|
| `channel` | 0 | Use page channel |
| `channel` | 1-16 | Override to specific channel |
| `lower` | 0 | Minimum value |
| `upper` | 127 | Maximum value (7-bit) |
| `upper` | 16383 | Maximum value (14-bit) |
| `display` | 10 | Standard display |
| `mode` | 3-7 | Acc0-Acc4 (acceleration modes) |
| `output` | 12 | Page (inherit from page) |
| `instrument` | 127 | Generic/custom |

#### Output Values

| Output | Value |
|--------|-------|
| ALL | 0 |
| TRS1 | 1 |
| TRS2 | 2 (likely) |
| USB1 | 3 (likely) |
| USB2 | 4 (likely) |
| USB3 | 5 |
| BLE | 6 |
| Page | 12 |
| ALL -BLE | 13 |
| ALL -USB | 14 |

#### Display Values

| Display | Value |
|---------|-------|
| OFF | 0 |
| 127 | 1 |
| 100 | 2 (likely) |
| 1000 | 3 |
| B63 | 4 |
| 9999 | 8 |
| Standard | 10 |
| High Res | 11 |

### Push Action (Encoder Press)

Same structure as turn_action but different type values. Note: push_action does NOT have `defaultValue` field.

**Disabled push_action template:**
```json
{
  "instrument": 127,
  "parameter": 0,
  "type": 0,
  "display": 0,
  "mode": 0,
  "channel": 0,
  "lower": 0,
  "upper": 127,
  "nr1": 0,
  "nr2": 0,
  "output": 12
}
```

| Type | Push Action |
|------|-------------|
| 0 | Off |
| 1 | Note |
| 2 | CC |
| 3 | PC (Program Change) |
| 4 | Set to Default |
| 5 | AT (Aftertouch) |
| 6 | Page |
| 7 | Record |
| 8 | Play/Pause Rec |

## Creating a Scene

1. Start with the base structure (12 pages, 16 encoders each)
2. Set page titles and channels
3. Configure each encoder's turn_actions[0] for primary mapping
4. For unused actions, use the full disabled action template (type: 0 with all fields)
5. Ensure field order in encoders: name, abbr, color, push_action, turn_actions, bipolar
6. Save as minified single-line JSON with `.oxie16` extension

**Common mistakes that cause silent load failures:**
- Using shorthand `{"type": 0}` instead of full action objects
- Wrong field order in encoder objects
- Missing required fields in any action object

## Scene Generator

Use `generate-scene.js` to create valid `.oxie16` files from compact input:

```bash
node generate-scene.js input.json output.oxie16
```

### Input Format

Encoders use object format:

```json
{"abbr": "FREQ", "name": "Flt Freq", "cc": 16}
{"abbr": "PAN", "name": "Pan", "cc": 89, "default": 64}
{"abbr": "TUNE", "name": "Tune", "cc": 40, "default": 64}
{"abbr": "DELT", "name": "Del Time", "cc": 21, "channel": 9}
{"abbr": "MUL1", "name": "LF1 Mult", "cc": 103, "upper": 23}
{"abbr": "ALGO", "name": "Algorith", "cc": 40, "upper": 7}
{"abbr": "VOL", "name": "Volume", "cc": 89, "default": 100}
```

**Encoder fields:**
- `abbr` - 4-char abbreviation (required)
- `name` - Display name, max 8 chars (required)
- `cc` - CC number for CC mode
- `msb`, `lsb` - NRPN address for NRPN mode
- `channel` - Override page channel (optional)
- `default` - Reset value when pressed (optional, default 0)
- `lower`, `upper` - Value range (optional, default 0-127)

### Default Values

The `default` field sets the value sent when the encoder is pressed (via "Set to Default" push action). Use this for:

**Bipolar parameters** (center = neutral): `"default": 64`
- Tune/Pitch (64 = 0 semitones)
- Pan (64 = center)
- Filter Envelope depth (64 = 0)
- Oscillator Mix (64 = equal blend)
- Detune, Drift, Linear offset, Harmonics

**Level/Mix parameters**: Check device - not always 100 or 127!
- Volume, Track Level: often 100
- Mix parameters: may be 127 (full wet/blend)
- Some levels default to specific values (e.g., 80)

**Device-specific defaults**: Many parameters have non-obvious defaults
- Example: DN2 Swarmer Animation = 15, Noise Mod = 20
- Example: DN2 Waves = 80 (on 0-120 range)
- Always verify with the actual device when uncertain

**FX-specific defaults** (Elektron reverb example):
- Pre-delay: `"default": 16`
- Decay: `"default": 32`
- HPF: `"default": 32`
- Shelf Freq: `"default": 64`
- Shelf Gain: `"default": 50`

**Discrete parameters**: Usually no default needed (or `"default": 0`)

**Finding default values:** Check the instrument's .oxiindef file if available. Otherwise, look at the device itself - most synths show parameter values on screen when you initialize a patch or reset a parameter.

**IMPORTANT: Verify bipolar parameters before setting defaults.** Not all parameters with "center" behavior are bipolar. Before assuming a parameter should default to 64:

1. **Check the .oxiindef file** - look for `default_value` field
2. **Search the web** for the device's MIDI implementation or manual
3. **Ask the user** if you're uncertain - they can check their device directly

Common mistakes to avoid:
- Assuming all "offset" or "detune" parameters are bipolar (some start at 0)
- Assuming envelope depths are always bipolar (varies by device)
- Setting default=64 on parameters that are actually unipolar

When in doubt, **ask the user to check their device** - they can initialize a patch and see what value the parameter shows.

### Discrete Value Ranges

For parameters with discrete values (not continuous 0-127), set the `upper` field to limit the range:

```json
{"abbr": "OMOD", "name": "Osc Mod", "cc": 50, "upper": 3}
{"abbr": "ALGO", "name": "Algorith", "cc": 40, "upper": 7}
{"abbr": "WAV1", "name": "LF1 Wav", "cc": 106, "upper": 6}
```

**Common discrete parameters (Elektron):**

| Parameter | Values | Upper |
|-----------|--------|-------|
| Osc Mod | 4 (off, ring mod, ring mod fixed, hard sync) | 3 |
| Wave table select | 2 (prim, harm) | 1 |
| FM Algorithm | 8 | 7 |
| FM Drum Algorithm | 7 | 6 |
| Filter Type | 3 | 2 |
| LFO Waveform | 7 | 6 |
| LFO Multiplier | 24 | 23 |
| LFO Trig Mode | 5 | 4 |
| Play Mode | 4 | 3 |
| Amp Mode | 2 (on/off) | 1 |
| Env Reset | 2 (on/off) | 1 |
| Routing toggles | 2 (on/off) | 1 |
| PingPong | 2 (on/off) | 1 |

**Finding discrete ranges:** Check the .oxiindef file's `maximum` field for each parameter. If not available, refer to the device's MIDI implementation chart or count the options in the device's menu.

**Why this matters:** Without proper `upper` limits, turning the encoder past the last valid value has no effect - the parameter stays at its maximum. Setting `upper` correctly makes the encoder feel responsive across its full range

**Scene fields:**
- `instrument` - Path to `.oxiindef` file for parameter reference (used for verifying CCs, finding discrete value ranges, and default value lookup)

**Page fields:**
- `type` - `"cc"` or `"nrpn"` (default: cc)
- `channel` - MIDI channel 1-16

**Features:**
- **Push action**: All encoders use "Set to Default" (type 4) - press to reset
- **Instrument lookup**: If `instrument` specified, defaults are loaded from `.oxiindef`
- Empty encoders auto-padded to 16 per page, 12 pages total

## References

- `generate-scene.js` — Scene generator (compact JSON → .oxie16)
- `references/scene-schema.json` — Full JSON Schema for validation
- `references/scene-template.json` — Minimal starting template

## Finding MIDI Parameters

Use **[midi.guide](https://midi.guide)** to find CC and NRPN values for any device:

- [Elektron Digitone II](https://midi.guide/d/elektron/digitone-ii/)
- [Elektron Digitakt II](https://midi.guide/d/elektron/digitakt-ii/)
- [Elektron Syntakt](https://midi.guide/d/elektron/syntakt/)
- [Elektron Analog Four](https://midi.guide/d/elektron/analog-four-mkii/)

For each parameter, midi.guide lists:
- **CC MSB** — Use with `type: 3` (CC Abs) in the scene, set `nr1` to this value
- **NRPN MSB/LSB** — Use with `type: 9` (NRPN), set `nr2` = MSB, `nr1` = LSB

**GitHub CSV source:** https://github.com/pencilresearch/midi — Raw parameter data for many devices.

### Choosing CC vs NRPN

| Type | Resolution | When to Use |
|------|------------|-------------|
| CC (type 3) | 7-bit (0-127) | **Recommended.** Simple, reliable, widely compatible |
| NRPN (type 9) | 14-bit (0-16383) | High resolution, but may have issues (see below) |

**Recommendation: Start with CC mode.** Most Elektron parameters support both CC and NRPN. While NRPN provides finer control (16,384 steps vs 128), CC is more reliable.

#### Known NRPN Issues

NRPN requires a 4-message sequence (CC99 → CC98 → CC6 → CC38). This can cause problems:

| Symptom | Likely Cause |
|---------|--------------|
| Parameter jumps erratically | CC38 (Data Entry LSB) bug in Elektron firmware |
| Value snaps to minimum/maximum | Message timing or ordering issues |
| Wrong parameter changes | NRPN address corruption |
| Intermittent response | NRPN null sequence (127,127) mishandled |

**Elektron firmware bug:** There's a [confirmed bug](https://www.elektronauts.com/t/nrpn-to-delay-time-data-entry-lsb-not-functioning/168499) where CC38 (Data Entry LSB) doesn't function correctly on some Elektron devices, causing erratic behavior when using NRPN.

#### When CC Precision is Sufficient

7-bit CC (128 steps) is adequate for most parameters:
- ✓ Oscillator waveforms, algorithms
- ✓ Envelope times (attack, decay, release)
- ✓ Effect sends, levels, pan
- ✓ LFO speed, depth, waveform

Where you *might* notice stepping with CC:
- Filter frequency (long sweeps)
- Fine pitch/detune adjustments
- Very slow parameter automation

**If NRPN issues occur:** Switch to CC mode by adding `"type": "cc"` to your page definition.

## Elektron Abbreviation Conventions

Elektron devices use **UPPERCASE** 4-character abbreviations. Follow these conventions for consistency:

### Standard Parameters

| Parameter | Abbreviation |
|-----------|--------------|
| Tune | TUNE |
| Wave | WAV (or WAV1/WAV2) |
| Level | LEV (or LEV1/LEV2) |
| Frequency | FREQ |
| Resonance | RESO |
| Type | TYPE |
| Pan | PAN |
| Volume | VOL |
| Mix | MIX |

### Envelopes (ADSR/AHDR)

| Parameter | Filter | Amp |
|-----------|--------|-----|
| Attack | FATK | AATK |
| Decay | FDEC | ADEC |
| Sustain | FSUS | — |
| Hold | — | AHLD |
| Release | FREL | AREL |
| Env Depth | FENV | — |

### Effects

| Effect | Send | Time | Feedback | Mix | Other |
|--------|------|------|----------|-----|-------|
| Delay | DEL | DELT | DELF | DELM | — |
| Reverb | REV | — | — | REVM | REVP (PreDly), REVD (Decay) |
| Chorus | CHR | — | — | CHRM | CHRD (Depth), CHRS (Speed) |
| Overdrive | OVER | — | — | — | — |
| Bit Reduce | BR | — | — | — | — |
| Sample Rate | SRR | — | — | — | — |

### Numbered Parameters

Put numbers at the **end**, not the start:
- `TUN1`, `TUN2` (not `1TUN`)
- `WAV1`, `WAV2`
- `LEV1`, `LEV2`
- `LIN1`, `LIN2`
- `OFS1`, `OFS2` (offset)
- `TBL1`, `TBL2` (wavetable)

### LFO Parameters

| LFO 1 | LFO 2 | Parameter |
|-------|-------|-----------|
| SPD1 | SPD2 | Speed |
| MUL1 | MUL2 | Multiplier |
| FAD1 | FAD2 | Fade |
| DST1 | DST2 | Destination |
| WAV1 | WAV2 | Waveform |
| PHS1 | PHS2 | Phase |
| TRG1 | TRG2 | Trigger |
| DPT1 | DPT2 | Depth |

### Other Common

| Parameter | Abbreviation |
|-----------|--------------|
| Algorithm | ALGO |
| Harmonic | HARM |
| Detune | DETN |
| Feedback | FDBK |
| Drift | DRIF |
| Mode | MODE |
| Reset | RSET |
| Track Level | TLEV |
| Pattern Volume | PVOL |

## Example: Elektron Digitone II

Look up values at [midi.guide/d/elektron/digitone-ii](https://midi.guide/d/elektron/digitone-ii/) or the [GitHub CSV](https://github.com/pencilresearch/midi/blob/main/Elektron/Digitone%20II.csv).

**CC mode (recommended):**
- Use `"type": "cc"` on the page
- Array format: `[abbr, name, cc, channel?]`
- Example: `["TUN1", "Osc1 Tune", 40]`
- Reliable, no known issues

**NRPN mode (use with caution):**
- Use `"type": "nrpn"` on the page (or omit, it's the default)
- Array format: `[abbr, name, msb, lsb, channel?]`
- Example: `["TUN1", "Osc1 Tune", 1, 73]`
- May cause erratic behavior due to firmware bugs (see above)
- Not all parameters support NRPN — check midi.guide for availability
- Example: Osc1 Tune → `nr1: 40, nr2: 0`

**Channel setup:**
- Set page `channel` to auto channel (default 10) or specific track (1-8)
- Use `channel: 9` override for master FX parameters (delay/reverb/chorus)

Sample page layout for Wavetone engine:
```
TUN1  WAV1  PD1   LEV1
TUN2  WAV2  PD2   LEV2
LIN1  LIN2  OMOD  DRIF
NATK  NDEC  NLEV  NCHR
```
