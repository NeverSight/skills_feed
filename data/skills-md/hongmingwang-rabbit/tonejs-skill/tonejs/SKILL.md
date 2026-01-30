---
name: tonejs
description: Best practices for Tone.js - programmatic music and audio synthesis in the browser using the Web Audio API. Covers synths, effects, sequencing, timing, samples, signals, patterns, MIDI, visualization, browser audio, music emotion mapping, rhythm/beat construction, music theory utilities, generative/algorithmic composition, performance optimization, offline rendering/recording, and React/Next.js integration.
metadata:
  tags: tonejs, audio, music, synthesis, web-audio, sequencing, effects, midi, visualization, emotion, mood, rhythm, beat, theory, chords, scales, generative, markov, react, nextjs, performance, recording, offline
---

## When to use

Use this skill whenever you are dealing with Tone.js code to obtain domain-specific knowledge for browser-based music synthesis, audio processing, programmatic music generation, and emotionally-driven composition.

## How to use

Read individual rule files for detailed explanations and code examples:

### Core API
- [rules/synths.md](rules/synths.md) - All synth types, oscillator variants (fat, FM, AM, pulse, PWM, custom partials), envelopes, and portamento
- [rules/sequencing.md](rules/sequencing.md) - Transport, Loop, Sequence, Part, Pattern, humanization, probability, and look-ahead scheduling
- [rules/effects.md](rules/effects.md) - Effects chains: Reverb, Delay, Filter, Distortion, Chorus, Phaser, Tremolo, AutoWah, Vibrato, PitchShift, StereoWidener, Chebyshev
- [rules/timing.md](rules/timing.md) - Time notation ("4n", "8n", "1m"), tempo, BPM, TimeClass, transport position, and swing
- [rules/samples.md](rules/samples.md) - Sample playback with Player, Players, Sampler, GrainPlayer, and Buffer
- [rules/signals.md](rules/signals.md) - Signal routing, automation, rampTo, LFO modulation, and signal math
- [rules/midi.md](rules/midi.md) - MIDI integration with WebMidi API, @tonejs/midi file parsing
- [rules/visualization.md](rules/visualization.md) - Audio analysis with FFT, Waveform, Meter, DCMeter, and Follower
- [rules/browser-audio.md](rules/browser-audio.md) - AudioContext, Tone.start(), user interaction requirements, React patterns

### Music Composition
- [rules/emotion.md](rules/emotion.md) - **Music emotion engine**: map feelings (happy, sad, tense, calm, epic, dreamy, etc.) to concrete Tone.js parameters — tempo, mode, timbre, dynamics, effects, articulation. Includes complete mood preset table and generator function.
- [rules/rhythm.md](rules/rhythm.md) - **Beat timing and groove**: drum patterns by genre, swing values, humanization, polyrhythm, Euclidean rhythms, time signatures, quantization, and emotion-driven rhythm construction.
- [rules/music-theory.md](rules/music-theory.md) - **Music theory utilities**: scale/chord/progression builders, all modes and scales with interval formulas, Roman numeral progressions, transposition, inversions, voice leading, and optional Tonal.js integration.
- [rules/patterns.md](rules/patterns.md) - Complete working examples: chord progression player, arpeggiator, drum machine, algorithmic melody generator, ambient music, and Remotion integration.
- [rules/generative.md](rules/generative.md) - **Generative/algorithmic music**: Markov chains, constrained random, probability-based rhythm, cellular automata, L-systems, evolving pieces, data sonification, and Magenta.js AI integration.

### Production & Integration
- [rules/performance.md](rules/performance.md) - **Performance and production**: context configuration, latency, Tone.Draw for visual sync, memory management, disposal, mobile audio, cross-browser issues, polyphony limits, and when NOT to use Tone.js.
- [rules/offline-recording.md](rules/offline-recording.md) - **Offline rendering and recording**: Tone.Offline for WAV export, Tone.Recorder, MediaRecorder, Remotion integration with audioBufferToDataUrl, and professional bus routing/mixing patterns.
- [rules/react-integration.md](rules/react-integration.md) - **React/Next.js integration**: useRef for audio nodes, SSR safety, dynamic imports, effect chain hooks, Transport-synced components, Reactronica declarative API, and cleanup patterns.
