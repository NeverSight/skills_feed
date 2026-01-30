---
name: audio-dsp
description: Digital signal processing for audio applications including reverb, convolution, FFT, and real-time audio processing patterns.
---

# Audio DSP Skill

Expert knowledge for implementing audio digital signal processing in web applications.

## When to Use

- Implementing audio effects (reverb, delay, chorus)
- Real-time audio processing with Web Audio API
- FFT analysis and visualization
- Convolution-based effects
- Audio worklet development

## Web Audio API Patterns

### Basic Audio Context
```typescript
const audioContext = new AudioContext();
const analyser = audioContext.createAnalyser();
analyser.fftSize = 2048;
```

### Audio Worklet (Real-time Processing)
```typescript
// Register processor
await audioContext.audioWorklet.addModule('processor.js');
const node = new AudioWorkletNode(audioContext, 'my-processor');
```

## Common Algorithms

### Convolution Reverb
```typescript
const convolver = audioContext.createConvolver();
const response = await fetch('/impulse-response.wav');
convolver.buffer = await audioContext.decodeAudioData(await response.arrayBuffer());
```

### FFT Analysis
```typescript
const dataArray = new Float32Array(analyser.frequencyBinCount);
analyser.getFloatFrequencyData(dataArray);
```

## Knowledge Base Resources

Query for DSP algorithms:
```sql
SELECT * FROM algorithm WHERE tags CONTAINS 'audio' OR tags CONTAINS 'dsp';
SELECT * FROM paper WHERE abstract @@ 'convolution reverb impulse';
```

## Performance Guidelines

1. **Use AudioWorklet** for real-time processing
2. **Avoid main thread** blocking during audio
3. **Buffer sizes**: 128-512 for low latency
4. **Sample rate**: Match device (usually 44100 or 48000)
5. **Use SharedArrayBuffer** for worklet communication

## React Integration

```typescript
// Custom hook pattern
const useAudioAnalyser = (audioContext: AudioContext) => {
  const analyserRef = useRef<AnalyserNode>();
  
  useEffect(() => {
    analyserRef.current = audioContext.createAnalyser();
    return () => analyserRef.current?.disconnect();
  }, [audioContext]);
  
  return analyserRef;
};
```

## Related KB Queries

```sql
-- Find reverb implementations
SELECT * FROM knowledge WHERE content @@ 'reverb implementation';

-- Get validated algorithms
SELECT * FROM algorithm WHERE success_rate > 0.8;
```
