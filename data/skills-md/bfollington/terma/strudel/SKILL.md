---
name: strudel
description: This skill should be used when working with Strudel.cc, a live-coding music environment. Use when creating musical patterns, drum sequences, melodies, basslines, or generative compositions. The user will always want to run Strudel code in the browser, either by copy-pasting or by providing a clickable URL with the code encoded in base64.
---

# Strudel

## Overview

Strudel is a browser-based live-coding environment that ports TidalCycles' pattern language to JavaScript. It uses pure functional programming to create musical patterns that can include drums, melodies, synthesis, and effects. Patterns are immutable query functions that transform time spans into event streams, supporting mini-notation DSL, Euclidean rhythms, and extensive audio processing.

## When to Use This Skill

Use this skill when:
- Creating drum patterns, melodies, basslines, or full compositions
- Generating algorithmic or generative music
- Applying effects like filters, reverb, delay, or distortion
- Debugging Strudel code or explaining pattern behavior
- Encoding Strudel code into shareable URLs

## Core Workflow

### 1. Understanding the User's Musical Intent

When a user requests a pattern, clarify:
- **Genre/style** (techno, ambient, jazz, etc.)
- **Artist references** (Lorn, Clams Casino, Aphex Twin, etc.)
- **Tempo** (BPM or cycles per minute)
- **Elements needed** (drums only, drums + bass, full arrangement)
- **Complexity level** (simple loop vs. generative/evolving)

**For genre/artist-specific techniques**, consult `references/genre-styles.md` which provides:
- Sonic characteristics for common genres and artists
- Strudel implementation patterns
- Concrete code examples for each style
- Typical tempo ranges, effects, and structural elements

### 2. Writing the Pattern

Build patterns using Strudel's functional, compositional approach:

**Basic structure:**
```javascript
// Simple drum pattern
s("bd hh sd hh")

// With tempo
s("bd hh sd hh").cpm(120)

// Layered with stack
stack(
  s("bd(3,8)"),           // Kick drum
  s("hh*8"),              // Hi-hats
  s("~ sd ~ sd")          // Snare on backbeat
).cpm(120)
```

**Key patterns:**
- Use mini-notation (`"bd hh sd"`) for concise rhythm specification
- Use `stack()` to layer multiple patterns
- Use `.cpm()` for tempo in cycles per minute
- Use Euclidean rhythms `(pulses, steps)` for interesting distributions
- Use lambda functions for transformations: `.off(1/8, x => x.add(7))`

### 3. Providing Output to the User

The user always wants to run the code in their browser. Provide both:

1. **The raw code** - for copy-pasting into https://strudel.cc/
2. **An encoded URL** - using `scripts/strudel_url.py` for immediate playback

**When to encode URLs:**
- **Initial creation**: Always provide encoded URL when creating a new pattern from scratch
- **Iterations/refinements**: Skip encoding unless user requests it
- **Final version**: Offer to encode when work is complete

**Encoding a URL:**
```bash
python3 scripts/strudel_url.py encode 's("bd hh sd hh").cpm(120)'
```

This produces a clickable link like:
```
https://strudel.cc/#cygiYmQgaGggc2QgaGgiKS5jcG0oMTIwKQ%3D%3D
```

Present the URL as a clickable link the user can immediately open.

### 4. Iteration and Refinement

After the user tests the pattern, they may request modifications:
- Adjust tempo: `.cpm(130)` or `.slow(2)` or `.fast(2)`
- Add effects: `.room(.5)`, `.lpf(1000)`, `.delay(.25)`
- Add variation: `.sometimes(x => x.speed(2))`, `.every(4, rev)`
- Change sounds: Replace sample names or add synthesis parameters

Provide the updated code for copy-pasting. Skip URL encoding during iterations unless requested.

## Common Pattern Templates

Use templates from `assets/patterns/` as starting points:

- **techno-drums.js** - 4/4 techno with Euclidean patterns
- **acid-bass.js** - TB-303 style bassline with filter sweeps
- **ambient-pad.js** - Lush pad with slow chord progression
- **generative-melody.js** - Algorithmic melody with scale and Euclidean rhythms
- **breakbeat.js** - Amen break slicing and manipulation
- **polyrhythm.js** - Multiple time signatures layered

Reference these when users request similar styles.

## Key Syntax Quick Reference

**Mini-notation:**
- `"a b c"` - Sequence (evenly distributed)
- `"<a b c>"` - Slow cat (one per cycle)
- `"[a b]"` - Subdivision (faster)
- `"a,b,c"` - Parallel/chord
- `"a*4"` - Speed up (4x)
- `"a/2"` - Slow down (2x)
- `"a(3,8)"` - Euclidean rhythm (3 pulses in 8 steps)
- `"~"` - Rest/silence
- `"a?"` - 50% probability

**Common functions:**
- `s()` or `.sound()` - Sample selection
- `note()` or `.note()` - Pitch (note name or MIDI number)
- `.scale()` - Apply scale (e.g., `"C:minor"`)
- `stack()` - Layer patterns
- `.fast()` / `.slow()` - Speed control
- `.rev()` - Reverse
- `.sometimes()` - Apply transformation 50% of the time
- `.every(n, fn)` - Apply transformation every n cycles

**Effects:**
- `.lpf()` - Low-pass filter (cutoff frequency)
- `.hpf()` - High-pass filter
- `.room()` - Reverb (0-1)
- `.delay()` - Delay effect (0-1)
- `.gain()` - Volume
- `.pan()` - Stereo position (0=left, 1=right)

**For comprehensive syntax**, consult `references/strudel-reference.md` which contains:
- Complete mini-notation syntax
- All pattern transformations (Euclidean, temporal, stochastic)
- Audio effects and synthesis parameters
- Signal functions (sine, perlin, saw, etc.)
- Pattern alignment strategies
- Practical composition examples

Search this file with grep when needed:
```bash
grep -i "euclidean" references/strudel-reference.md
grep -i "filter" references/strudel-reference.md
grep -i "delay" references/strudel-reference.md
```

## Debugging Common Issues

**Pattern not playing:**
- Ensure the pattern ends with appropriate audio output (`.s()`, `.sound()`, or `.note()`)
- Check that samples are loaded (default samples work without loading)
- Verify syntax: balanced brackets, quotes, parentheses

**Timing issues:**
- Use `.cpm()` or `setcpm()` to set tempo explicitly
- Check for conflicting `.fast()` / `.slow()` calls
- Verify Euclidean rhythms have valid (pulses, steps) values

**Filter not working:**
- Ensure cutoff frequency is in valid range (20-20000 Hz)
- Check filter envelope parameters (`.lpa()`, `.lpd()`, `.lps()`, `.lpr()`)
- Use `.lpenv()` for filter envelope depth

**Code too complex:**
- Break into smaller patterns and test individually
- Use variables: `let drums = s("bd hh")`
- Stack tested patterns: `stack(drums, bass, melody)`

## Resources

### scripts/strudel_url.py
Python script for encoding/decoding Strudel URLs.

**Encode:**
```bash
python3 scripts/strudel_url.py encode '<strudel-code>'
```

**Decode:**
```bash
python3 scripts/strudel_url.py decode '<strudel-url>'
```

Always encode URLs after creating or modifying patterns to provide clickable links.

### references/strudel-reference.md
Comprehensive technical reference including:
- Complete mini-notation syntax
- All pattern operations and transformations
- Audio effects and synthesis
- Signals and continuous patterns
- Composition examples
- Best practices

Load this file when users need detailed syntax explanations or advanced techniques.

### references/genre-styles.md
Genre and artist style guide including:
- Dark Ambient Hip-Hop (Lorn, Clams Casino)
- Techno (General, Dub Techno)
- Drum & Bass / Jungle (Jungle, Liquid DnB)
- Trap / Hip-Hop (Trap, Boom Bap)
- Ambient / Experimental (Dark Ambient, IDM/Glitch)
- House (Deep House, Acid House)

Each entry provides sonic characteristics and Strudel implementation techniques. Load when users reference specific genres or artists.

Search this file when needed:
```bash
grep -i "lorn" references/genre-styles.md
grep -i "techno" references/genre-styles.md
grep -i "ambient" references/genre-styles.md
```

### assets/patterns/
Example pattern templates for common musical styles. Copy and adapt these as starting points:
- `techno-drums.js` - Electronic drum patterns
- `acid-bass.js` - Resonant basslines
- `ambient-pad.js` - Atmospheric textures
- `generative-melody.js` - Algorithmic melodies
- `breakbeat.js` - Sample manipulation
- `polyrhythm.js` - Complex rhythmic structures
