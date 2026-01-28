---
name: web-audio-api
description: Web Audio API for JARVIS audio feedback and voice processing
model: sonnet
risk_level: LOW
version: 1.0.0
---

# Web Audio API Skill

## 1. Overview

This skill provides Web Audio API expertise for creating audio feedback, voice processing, and sound effects in the JARVIS AI Assistant.

**Risk Level**: LOW - Audio processing with minimal security surface

**Primary Use Cases**:
- HUD audio feedback (beeps, alerts)
- Voice input processing
- Spatial audio for 3D HUD elements
- Real-time audio visualization
- Text-to-speech integration

## 2. Core Responsibilities

### 2.1 Fundamental Principles

1. **TDD First**: Write tests before implementation for all audio components
2. **Performance Aware**: Optimize for 60fps with minimal audio latency
3. **User Gesture Required**: Audio context must be started after user interaction
4. **Resource Cleanup**: Close audio contexts and disconnect nodes on unmount
5. **AudioWorklet for Processing**: Use AudioWorklet for heavy DSP operations
6. **Accessibility**: Provide visual alternatives to audio feedback
7. **Volume Control**: Respect system and user volume preferences
8. **Error Handling**: Gracefully handle audio permission denials

## 3. Technology Stack & Versions

### 3.1 Browser Support

| Browser | AudioContext | AudioWorklet |
|---------|--------------|--------------|
| Chrome | 35+ | 66+ |
| Firefox | 25+ | 76+ |
| Safari | 14.1+ | 14.1+ |

### 3.2 TypeScript Types

```typescript
// types/audio.ts
interface AudioFeedbackOptions {
  frequency: number
  duration: number
  type: OscillatorType
  volume: number
}

interface SpatialAudioPosition {
  x: number
  y: number
  z: number
}
```

## 4. Implementation Patterns

### 4.1 Audio Context Management

```typescript
// composables/useAudioContext.ts
export function useAudioContext() {
  const audioContext = ref<AudioContext | null>(null)
  const isInitialized = ref(false)

  async function initialize() {
    if (audioContext.value) return
    audioContext.value = new AudioContext()
    if (audioContext.value.state === 'suspended') await audioContext.value.resume()
    isInitialized.value = true
  }

  onUnmounted(() => {
    audioContext.value?.close()
    audioContext.value = null
  })

  return { audioContext: readonly(audioContext), isInitialized: readonly(isInitialized), initialize }
}
```

### 4.2 HUD Beep Feedback

```typescript
// composables/useHUDSounds.ts
export function useHUDSounds() {
  const { audioContext, initialize } = useAudioContext()

  async function playBeep(options: Partial<AudioFeedbackOptions> = {}) {
    await initialize()
    const ctx = audioContext.value
    if (!ctx) return

    const { frequency = 440, duration = 0.1, type = 'sine', volume = 0.3 } = options
    const safeVolume = Math.max(0, Math.min(1, volume))

    const oscillator = ctx.createOscillator()
    const gainNode = ctx.createGain()
    oscillator.type = type
    oscillator.frequency.value = frequency
    gainNode.gain.value = safeVolume
    gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration)

    oscillator.connect(gainNode).connect(ctx.destination)
    oscillator.start()
    oscillator.stop(ctx.currentTime + duration)
  }

  const sounds = {
    confirm: () => playBeep({ frequency: 880, duration: 0.1, volume: 0.2 }),
    alert: () => playBeep({ frequency: 440, duration: 0.3, type: 'square', volume: 0.4 }),
    error: () => playBeep({ frequency: 220, duration: 0.5, type: 'sawtooth', volume: 0.3 }),
    click: () => playBeep({ frequency: 1000, duration: 0.05, volume: 0.1 })
  }
  return { playBeep, sounds }
}
```

### 4.3 Audio Visualization

```typescript
// composables/useAudioVisualization.ts
export function useAudioVisualization() {
  const { audioContext, initialize } = useAudioContext()
  let analyser: AnalyserNode | null = null
  let dataArray: Uint8Array | null = null

  async function setupAnalyser(source: AudioNode) {
    await initialize()
    const ctx = audioContext.value
    if (!ctx) return
    analyser = ctx.createAnalyser()
    analyser.fftSize = 256
    dataArray = new Uint8Array(analyser.frequencyBinCount)
    source.connect(analyser)
  }

  function getFrequencyData(): Uint8Array | null {
    if (!analyser || !dataArray) return null
    analyser.getByteFrequencyData(dataArray)
    return dataArray
  }

  return { setupAnalyser, getFrequencyData }
}
```

### 4.4 Spatial Audio for 3D HUD

```typescript
// composables/useSpatialAudio.ts
export function useSpatialAudio() {
  const { audioContext, initialize } = useAudioContext()
  let panner: PannerNode | null = null

  async function createSpatialSource(position: SpatialAudioPosition) {
    await initialize()
    const ctx = audioContext.value
    if (!ctx) return null
    panner = ctx.createPanner()
    panner.panningModel = 'HRTF'
    panner.distanceModel = 'inverse'
    setPosition(position)
    return panner
  }

  function setPosition(pos: SpatialAudioPosition) {
    if (!panner) return
    panner.positionX.value = pos.x
    panner.positionY.value = pos.y
    panner.positionZ.value = pos.z
  }

  return { createSpatialSource, setPosition }
}
```

### 4.5 Microphone Input

```typescript
// composables/useMicrophone.ts
export function useMicrophone() {
  const { audioContext, initialize } = useAudioContext()
  const stream = ref<MediaStream | null>(null)
  const isListening = ref(false)
  const error = ref<string | null>(null)

  async function startListening() {
    try {
      await initialize()
      stream.value = await navigator.mediaDevices.getUserMedia({
        audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true }
      })
      isListening.value = true
      return stream.value
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Microphone access denied'
      return null
    }
  }

  function stopListening() {
    stream.value?.getTracks().forEach(track => track.stop())
    stream.value = null
    isListening.value = false
  }

  onUnmounted(() => stopListening())

  return { stream: readonly(stream), isListening: readonly(isListening), error: readonly(error), startListening, stopListening }
}
```

## 5. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```typescript
// tests/composables/useHUDSounds.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useHUDSounds } from '~/composables/useHUDSounds'

// Mock AudioContext nodes
const mockOscillator = { connect: vi.fn(), start: vi.fn(), stop: vi.fn(), frequency: { value: 440 } }
const mockGainNode = { connect: vi.fn(), gain: { value: 1, exponentialRampToValueAtTime: vi.fn() } }
const mockAudioContext = {
  state: 'running', currentTime: 0, destination: {},
  createOscillator: vi.fn(() => mockOscillator),
  createGain: vi.fn(() => mockGainNode),
  resume: vi.fn(), close: vi.fn()
}
vi.stubGlobal('AudioContext', vi.fn(() => mockAudioContext))

describe('useHUDSounds', () => {
  beforeEach(() => vi.clearAllMocks())

  it('creates oscillator with correct frequency', async () => {
    const { playBeep } = useHUDSounds()
    await playBeep({ frequency: 880 })
    expect(mockOscillator.frequency.value).toBe(880)
  })

  it('clamps volume to valid range', async () => {
    const { playBeep } = useHUDSounds()
    await playBeep({ volume: 2.5 })
    expect(mockGainNode.gain.value).toBeLessThanOrEqual(1)
  })

  it('connects nodes in correct order', async () => {
    const { playBeep } = useHUDSounds()
    await playBeep()
    expect(mockOscillator.connect).toHaveBeenCalledWith(mockGainNode)
    expect(mockGainNode.connect).toHaveBeenCalledWith(mockAudioContext.destination)
  })
})
```

### Step 2: Implement Minimum to Pass

```typescript
// composables/useHUDSounds.ts
export function useHUDSounds() {
  // Implementation from section 4.2
  // Only add features that tests require
}
```

### Step 3: Refactor Following Patterns

After tests pass, refactor to:
- Extract shared audio context logic
- Add proper TypeScript types
- Implement cleanup on unmount

### Step 4: Run Full Verification

```bash
# Run all audio-related tests
npm test -- --grep "audio|sound|HUD"

# Check types
npm run typecheck

# Verify no memory leaks in browser
npm run dev  # Test manually with DevTools Memory tab
```

## 6. Performance Patterns

### 6.1 AudioWorklet for Processing

```typescript
// ✅ Good: Use AudioWorklet for DSP (runs on audio thread)
class NoiseGateProcessor extends AudioWorkletProcessor {
  process(inputs: Float32Array[][], outputs: Float32Array[][]) {
    for (let ch = 0; ch < inputs[0].length; ch++) {
      for (let i = 0; i < inputs[0][ch].length; i++) {
        outputs[0][ch][i] = Math.abs(inputs[0][ch][i]) > 0.01 ? inputs[0][ch][i] : 0
      }
    }
    return true
  }
}
registerProcessor('noise-gate', NoiseGateProcessor)

// ❌ Bad: ScriptProcessorNode (deprecated, blocks main thread)
```

### 6.2 Buffer Pooling

```typescript
// ✅ Good: Reuse audio buffers
class AudioBufferPool {
  private pool: AudioBuffer[] = []
  constructor(ctx: AudioContext, size: number, length: number) {
    for (let i = 0; i < size; i++) {
      this.pool.push(ctx.createBuffer(2, length, ctx.sampleRate))
    }
  }
  acquire(): AudioBuffer | undefined { return this.pool.pop() }
  release(buffer: AudioBuffer) {
    for (let ch = 0; ch < buffer.numberOfChannels; ch++) {
      buffer.getChannelData(ch).fill(0)
    }
    this.pool.push(buffer)
  }
}

// ❌ Bad: Create new buffer each time
const buffer = ctx.createBuffer(2, 44100, 44100) // Allocates memory each call
```

### 6.3 Offline Rendering

```typescript
// ✅ Good: Pre-render complex sounds
async function prerenderSound(): Promise<AudioBuffer> {
  const offlineCtx = new OfflineAudioContext(2, 44100, 44100)
  const osc = offlineCtx.createOscillator()
  const gain = offlineCtx.createGain()
  osc.connect(gain).connect(offlineCtx.destination)
  gain.gain.setValueAtTime(0, 0)
  gain.gain.linearRampToValueAtTime(1, 0.01)
  gain.gain.exponentialRampToValueAtTime(0.001, 1)
  osc.start(); osc.stop(1)
  return offlineCtx.startRendering()
}

// ❌ Bad: Generate complex sounds in real-time (multiple oscillators computed live)
```

### 6.4 Node Graph Optimization

```typescript
// ✅ Good: Reuse master gain node
const masterGain = ctx.createGain()
masterGain.connect(ctx.destination)
function playSound(buffer: AudioBuffer) {
  const source = ctx.createBufferSource()
  source.buffer = buffer
  source.connect(masterGain)
  source.start()
}

// ❌ Bad: Create full chain for each sound (gain + compressor per play)
```

### 6.5 Memory Management

```typescript
// ✅ Good: Disconnect and cleanup nodes
function playOneShot(buffer: AudioBuffer) {
  const source = ctx.createBufferSource()
  source.buffer = buffer
  source.connect(masterGain)
  source.onended = () => source.disconnect()
  source.start()
}

// ✅ Good: Limit concurrent sounds (max 8)
class SoundManager {
  private activeSources = new Set<AudioBufferSourceNode>()
  play(buffer: AudioBuffer) {
    if (this.activeSources.size >= 8) this.activeSources.values().next().value?.stop()
    const source = ctx.createBufferSource()
    source.buffer = buffer
    source.connect(masterGain)
    source.onended = () => { source.disconnect(); this.activeSources.delete(source) }
    this.activeSources.add(source)
    source.start()
  }
}

// ❌ Bad: Never cleanup - nodes stay in memory after playback
const source = ctx.createBufferSource()
source.connect(ctx.destination)
source.start()
```

## 7. Quality Standards

```typescript
// ✅ Always require user gesture
button.addEventListener('click', async () => {
  await audioContext.resume()
  playSound()
})

// ✅ Respect user preferences
if (usePreferencesStore().preferences.soundEnabled) playBeep()

// ✅ Handle permission denial gracefully
try {
  await navigator.mediaDevices.getUserMedia({ audio: true })
} catch (err) {
  if (err.name === 'NotAllowedError') {
    showVisualFeedback('Microphone access required')
  }
}
```

## 8. Testing & Quality

```typescript
describe('HUD Sounds', () => {
  it('validates volume bounds', async () => {
    const { playBeep } = useHUDSounds()
    await playBeep({ volume: 2 })  // Clamped to 1
    await playBeep({ volume: -1 }) // Clamped to 0
  })
})
```

## 9. Common Mistakes & Anti-Patterns

### 9.1 Critical Anti-Patterns

```typescript
// ❌ Auto-play without user gesture - BLOCKED
onMounted(() => playSound())

// ✅ After user interaction
const handleClick = async () => { await audioContext.resume(); playSound() }

// ❌ Memory leak - no cleanup
const audioContext = new AudioContext()

// ✅ Proper cleanup
onUnmounted(() => audioContext.close())

// ❌ New context per sound - performance killer
function playSound() { const ctx = new AudioContext() }

// ✅ Reuse context
const ctx = new AudioContext()
function playSound() { /* reuse ctx */ }
```

## 10. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Tests written for audio node creation and connections
- [ ] Tests written for volume clamping and validation
- [ ] Performance requirements identified (latency, concurrent sounds)
- [ ] AudioWorklet needed for DSP? Worklet file created
- [ ] Buffer pool size calculated for expected usage

### Phase 2: During Implementation

- [ ] User gesture required for AudioContext initialization
- [ ] Audio context reused (not created per sound)
- [ ] Nodes disconnected in onended callbacks
- [ ] Volume bounds validated (0-1 range)
- [ ] Microphone permissions handled gracefully
- [ ] Error states provide visual feedback

### Phase 3: Before Committing

- [ ] All audio tests pass: `npm test -- --grep "audio"`
- [ ] Type checking passes: `npm run typecheck`
- [ ] No memory leaks (tested in DevTools Memory tab)
- [ ] Audio context closed on component unmount
- [ ] Visual alternatives provided for accessibility
- [ ] Sound can be disabled via user preferences
- [ ] Volume respects system preferences

## 11. Summary

Web Audio API for JARVIS: Initialize after user gesture, cleanup on unmount, handle permission denials, provide visual alternatives. See `references/advanced-patterns.md`
