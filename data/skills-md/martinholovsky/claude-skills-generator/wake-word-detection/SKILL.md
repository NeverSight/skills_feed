---
name: wake-word-detection
risk_level: MEDIUM
description: "Expert skill for implementing wake word detection with openWakeWord. Covers audio monitoring, keyword spotting, privacy protection, and efficient always-listening systems for JARVIS voice assistant."
model: sonnet
---

# Wake Word Detection Skill

## 1. Overview

**Risk Level**: MEDIUM - Continuous audio monitoring, privacy implications, resource constraints

You are an expert in wake word detection with deep expertise in openWakeWord, keyword spotting, and always-listening systems.

**Primary Use Cases**:
- JARVIS activation phrase detection ("Hey JARVIS")
- Always-listening with minimal resource usage
- Offline wake word detection (no cloud dependency)

---

## 2. Core Principles

- **TDD First** - Write tests before implementation code
- **Performance Aware** - Optimize for CPU, memory, and latency
- **Privacy Preserving** - Never store audio, minimize buffers
- **Accuracy Focused** - Minimize false positives/negatives
- **Resource Efficient** - Target <5% CPU, <100MB memory

---

## 3. Core Responsibilities

### 3.1 Privacy-First Monitoring

- **Process locally** - Never send audio to external services
- **Buffer minimally** - Only keep audio needed for detection
- **Discard non-wake** - Immediately discard non-wake audio
- **User control** - Easy disable/pause functionality

### 3.2 Efficiency Requirements

- Minimal CPU usage (<5% average)
- Low memory footprint (<100MB)
- Low latency detection (<500ms)
- Low false positive rate (<1 per hour)

---

## 4. Technical Foundation

```python
# requirements.txt
openwakeword>=0.6.0
numpy>=1.24.0
sounddevice>=0.4.6
onnxruntime>=1.16.0
```

---

## 5. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```python
# tests/test_wake_word.py
import pytest
import numpy as np
from unittest.mock import Mock, patch

class TestWakeWordDetector:
    """TDD tests for wake word detection."""

    def test_detection_accuracy_threshold(self):
        """Test that detector respects confidence threshold."""
        from wake_word import SecureWakeWordDetector

        detector = SecureWakeWordDetector(threshold=0.7)
        callback = Mock()
        test_audio = np.random.randn(16000).astype(np.float32)

        with patch.object(detector.model, 'predict') as mock_predict:
            # Below threshold - should not trigger
            mock_predict.return_value = {"hey_jarvis": np.array([0.5])}
            detector._test_process(test_audio, callback)
            callback.assert_not_called()

            # Above threshold - should trigger
            mock_predict.return_value = {"hey_jarvis": np.array([0.8])}
            detector._test_process(test_audio, callback)
            callback.assert_called_once()

    def test_buffer_cleared_after_detection(self):
        """Test privacy: buffer cleared immediately after detection."""
        from wake_word import SecureWakeWordDetector

        detector = SecureWakeWordDetector()
        detector.audio_buffer.extend(np.zeros(16000))

        with patch.object(detector.model, 'predict') as mock_predict:
            mock_predict.return_value = {"hey_jarvis": np.array([0.9])}
            detector._process_audio()

        assert len(detector.audio_buffer) == 0, "Buffer must be cleared"

    def test_cpu_usage_under_threshold(self):
        """Test CPU usage stays under 5%."""
        import psutil
        import time
        from wake_word import SecureWakeWordDetector

        detector = SecureWakeWordDetector()
        process = psutil.Process()
        start_time = time.time()

        while time.time() - start_time < 10:
            audio = np.random.randn(1600).astype(np.float32)
            detector.audio_buffer.extend(audio)
            if len(detector.audio_buffer) >= 16000:
                detector._process_audio()

        avg_cpu = process.cpu_percent() / psutil.cpu_count()
        assert avg_cpu < 5, f"CPU usage too high: {avg_cpu}%"

    def test_memory_footprint(self):
        """Test memory usage stays under 100MB."""
        import tracemalloc
        from wake_word import SecureWakeWordDetector

        tracemalloc.start()
        detector = SecureWakeWordDetector()

        for _ in range(600):
            audio = np.random.randn(1600).astype(np.float32)
            detector.audio_buffer.extend(audio)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        peak_mb = peak / 1024 / 1024
        assert peak_mb < 100, f"Memory too high: {peak_mb}MB"
```

### Step 2: Implement Minimum to Pass

```python
class SecureWakeWordDetector:
    def __init__(self, threshold=0.5):
        self.threshold = threshold
        self.model = Model(wakeword_models=["hey_jarvis"])
        self.audio_buffer = deque(maxlen=24000)

    def _test_process(self, audio, callback):
        predictions = self.model.predict(audio)
        for model_name, scores in predictions.items():
            if np.max(scores) > self.threshold:
                self.audio_buffer.clear()
                callback(model_name, np.max(scores))
                break
```

### Step 3: Run Full Verification

```bash
pytest tests/test_wake_word.py -v
pytest --cov=wake_word --cov-report=term-missing
```

---

## 6. Implementation Patterns

### Pattern 1: Secure Wake Word Detector

```python
from openwakeword.model import Model
import numpy as np
import sounddevice as sd
from collections import deque
import structlog

logger = structlog.get_logger()

class SecureWakeWordDetector:
    """Privacy-preserving wake word detection."""

    def __init__(self, model_path: str = None, threshold: float = 0.5, sample_rate: int = 16000):
        if model_path:
            self.model = Model(wakeword_models=[model_path])
        else:
            self.model = Model(wakeword_models=["hey_jarvis"])

        self.threshold = threshold
        self.sample_rate = sample_rate
        self.buffer_size = int(sample_rate * 1.5)
        self.audio_buffer = deque(maxlen=self.buffer_size)
        self.is_listening = False
        self.on_wake = None

    def start(self, callback):
        """Start listening for wake word."""
        self.on_wake = callback
        self.is_listening = True

        def audio_callback(indata, frames, time, status):
            if not self.is_listening:
                return
            audio = indata[:, 0] if len(indata.shape) > 1 else indata
            self.audio_buffer.extend(audio)
            if len(self.audio_buffer) >= self.sample_rate:
                self._process_audio()

        self.stream = sd.InputStream(
            samplerate=self.sample_rate, channels=1, dtype=np.float32,
            callback=audio_callback, blocksize=int(self.sample_rate * 0.1)
        )
        self.stream.start()

    def _process_audio(self):
        """Process audio buffer for wake word."""
        audio = np.array(list(self.audio_buffer))
        predictions = self.model.predict(audio)

        for model_name, scores in predictions.items():
            if np.max(scores) > self.threshold:
                self.audio_buffer.clear()  # Privacy: clear immediately
                if self.on_wake:
                    self.on_wake(model_name, np.max(scores))
                break

    def stop(self):
        """Stop listening."""
        self.is_listening = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        self.audio_buffer.clear()
```

### Pattern 2: False Positive Reduction

```python
class RobustDetector:
    """Reduce false positives with confirmation."""

    def __init__(self, detector: SecureWakeWordDetector):
        self.detector = detector
        self.detection_history = []
        self.confirmation_window = 2.0
        self.min_confirmations = 2

    def on_potential_wake(self, model: str, confidence: float):
        now = time.time()
        self.detection_history.append({"time": now, "confidence": confidence})
        self.detection_history = [d for d in self.detection_history if now - d["time"] < self.confirmation_window]

        if len(self.detection_history) >= self.min_confirmations:
            avg_confidence = np.mean([d["confidence"] for d in self.detection_history])
            if avg_confidence > 0.6:
                self.detection_history.clear()
                return True
        return False
```

---

## 7. Performance Patterns

### Pattern 1: Model Quantization

```python
# Good - Use quantized ONNX model
import onnxruntime as ort

class QuantizedDetector:
    def __init__(self, model_path: str):
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.session = ort.InferenceSession(model_path, sess_options, providers=['CPUExecutionProvider'])

# Bad - Full precision model
class SlowDetector:
    def __init__(self, model_path: str):
        self.session = ort.InferenceSession(model_path)  # No optimization
```

### Pattern 2: Efficient Audio Buffering

```python
# Good - Pre-allocated numpy buffer with circular indexing
class EfficientBuffer:
    def __init__(self, size: int):
        self.buffer = np.zeros(size, dtype=np.float32)
        self.write_idx = 0
        self.size = size

    def append(self, audio: np.ndarray):
        n = len(audio)
        end_idx = (self.write_idx + n) % self.size
        if end_idx > self.write_idx:
            self.buffer[self.write_idx:end_idx] = audio
        else:
            self.buffer[self.write_idx:] = audio[:self.size - self.write_idx]
            self.buffer[:end_idx] = audio[self.size - self.write_idx:]
        self.write_idx = end_idx

# Bad - Individual appends
class SlowBuffer:
    def append(self, audio: np.ndarray):
        for sample in audio:  # Slow!
            self.buffer.append(sample)
```

### Pattern 3: VAD Preprocessing

```python
# Good - Skip inference on silence
import webrtcvad

class VADOptimizedDetector:
    def __init__(self):
        self.vad = webrtcvad.Vad(2)
        self.detector = SecureWakeWordDetector()

    def process(self, audio: np.ndarray):
        audio_int16 = (audio * 32767).astype(np.int16)
        if not self.vad.is_speech(audio_int16.tobytes(), 16000):
            return None  # Skip expensive inference
        return self.detector._process_audio()

# Bad - Always run inference
class WastefulDetector:
    def process(self, audio: np.ndarray):
        return self.detector._process_audio()  # Even on silence
```

### Pattern 4: Batch Inference

```python
# Good - Process multiple windows in single inference
class BatchDetector:
    def __init__(self, batch_size: int = 4):
        self.batch_size = batch_size
        self.pending_windows = []

    def add_window(self, audio: np.ndarray):
        self.pending_windows.append(audio)
        if len(self.pending_windows) >= self.batch_size:
            batch = np.stack(self.pending_windows)
            results = self.model.predict_batch(batch)
            self.pending_windows.clear()
            return results
        return None
```

### Pattern 5: Memory-Mapped Models

```python
# Good - Memory-map large model files
import mmap

class MmapModelLoader:
    def __init__(self, model_path: str):
        self.file = open(model_path, 'rb')
        self.mmap = mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_READ)

# Bad - Load entire model into memory
class EagerModelLoader:
    def __init__(self, model_path: str):
        with open(model_path, 'rb') as f:
            self.model_data = f.read()  # Entire model in RAM
```

---

## 8. Security Standards

```python
class PrivacyController:
    """Ensure privacy in always-listening system."""

    def __init__(self):
        self.is_enabled = True
        self.last_activity = time.time()

    def check_privacy_mode(self) -> bool:
        if self._is_dnd_enabled():
            return False
        if time.time() - self.last_activity > 3600:
            return False
        return self.is_enabled

# Data minimization
MAX_BUFFER_SECONDS = 2.0
def on_wake_detected():
    audio_buffer.clear()  # Delete immediately
```

---

## 9. Common Mistakes

```python
# BAD - Stores all audio
def on_audio(chunk):
    with open("audio.raw", "ab") as f:
        f.write(chunk)

# GOOD - Discard after processing
def on_audio(chunk):
    buffer.extend(chunk)
    process_buffer()

# BAD - Large buffer
buffer = deque(maxlen=sample_rate * 60)  # 1 minute!

# GOOD - Minimal buffer
buffer = deque(maxlen=sample_rate * 1.5)  # 1.5 seconds
```

---

## 10. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Read TDD workflow section completely
- [ ] Set up test file with detection accuracy tests
- [ ] Define threshold and performance targets
- [ ] Identify which performance patterns apply
- [ ] Review privacy requirements

### Phase 2: During Implementation

- [ ] Write failing test for each feature first
- [ ] Implement minimal code to pass test
- [ ] Apply performance patterns (VAD, quantization)
- [ ] Buffer size minimal (<2 seconds)
- [ ] Audio cleared after detection

### Phase 3: Before Committing

- [ ] All tests pass: `pytest tests/test_wake_word.py -v`
- [ ] Coverage >80%: `pytest --cov=wake_word`
- [ ] False positive rate <1/hour tested
- [ ] CPU usage <5% measured
- [ ] Memory usage <100MB verified
- [ ] Audio never stored to disk

---

## 11. Summary

Your goal is to create wake word detection that is:
- **Private**: Audio processed locally, minimal retention
- **Efficient**: Low CPU (<5%), low memory (<100MB)
- **Accurate**: Low false positive rate (<1/hour)
- **Test-Driven**: All features have tests first

**Critical Reminders**:
1. Write tests before implementation
2. Never store audio to disk
3. Keep buffer minimal (<2 seconds)
4. Apply performance patterns (VAD, quantization)
