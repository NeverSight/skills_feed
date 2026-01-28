---
name: voice-ux-pro
id: voice-ux-pro
version: 1.1.0
description: "Master of Voice-First Interfaces, specialized in sub-300ms Latency, Spatial Hearing AI, and Multimodal Voice-Haptic feedback."
last_updated: "2026-01-22"
---

# Skill: Voice UX Pro (Standard 2026)

**Role:** The Voice UX Pro is a specialized designer and engineer responsible for "Frictionless" conversational interfaces. In 2026, this role masters sub-300ms response times, Spatial Hearing AI (voice separation), and the integration of subtle haptic feedback to guide users through hands-free workflows.

## 🎯 Primary Objectives
1.  **Sub-300ms Responsiveness:** Achieving natural human-like interaction speeds using Streaming APIs and Edge Inference.
2.  **Spatial Clarity:** Implementing "Spatial Hearing AI" to isolate user voices from complex background noise.
3.  **Conversational Design:** Crafting non-linear, robust dialogues that handle interruptions and "Ums/Ahs" gracefully.
4.  **Multimodal Synergy:** Synchronizing Voice with Haptics and Visuals for a holistic, accessible experience.

---

## 🏗️ The 2026 Voice Stack

### 1. Speech Engines
- **Whisper v4 / Chirp v3:** For high-fidelity, multilingual transcription (STT).
- **Google Speech-to-Speech (S2S):** For near-instant, zero-latency response loops.
- **ElevenLabs v3:** For emotive, human-grade synthetic voices (TTS).

### 2. Interaction & Feedback
- **Native Haptics (iOS/Android):** Precise vibration patterns synchronized with speech phases.
- **Audio Shaders:** Real-time spatialization of AI voices using Shopify Skia or native audio APIs.

---

## 🛠️ Implementation Patterns

### 1. The "Listen-Ahead" Pattern (Sub-300ms)
Generating partial results while the user is still speaking to "Pre-warm" the LLM prompt.

```typescript
// 2026 Pattern: Streaming STT to LLM
const sttStream = await speechClient.createStreamingSTT();
const aiStream = await genAI.generateContentStream();

sttStream.on('partial', (text) => {
  // Pre-load context if 'intent' is detected early
  if (detectEarlyIntent(text)) aiStream.warmUp();
});
```

### 2. Voice-Haptic Synchronization
Providing "Micro-confirmation" via haptics when the AI starts/stops listening.

```tsx
import * as Haptics from 'expo-haptics';

function useVoiceInteraction() {
  const onStartListening = () => {
    // Light pulse to indicate "I am hearing you"
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };
  
  const onSuccess = () => {
    // Success sequence: Short, crisp double-tap
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
  };
}
```

### 3. Spatial Isolation Logic
Isolating the user's voice based on 3D coordinates.

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** force the user to wait for a full sentence to be transcribed before acting.
2.  **NEVER** use "Robotic" monotonically generated voices. Use emotive TTS with prosody control.
3.  **NEVER** trigger loud audio confirmations in public settings without a "Silent Mode" check.
4.  **NEVER** ignore background noise. Always implement a "Noise-Floor" calibration step.

---

## 🛠️ Troubleshooting & Latency Audit

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **"Uncanny Valley" Delay** | Round-trip latency > 500ms | Move STT/TTS to a Regional Edge Function. |
| **Cross-Talk Failure** | Ambiguous sound sources | Implement Spatial Hearing AI (3D Beamforming). |
| **Instruction Fatigue** | Too many verbal options | Use "Contextual Shortlisting" (Only suggest relevant next steps). |
| **Accidental Triggers** | Sensitive Wake-word detection | Use "Personalized Voice Fingerprinting" for activation. |

---

## 📚 Reference Library
- **[Low-Latency Voice Stack](./references/1-low-latency-voice-stack.md):** STT, TTS, and S2S.
- **[Conversational Design](./references/2-conversational-design.md):** Beyond simple commands.
- **[Haptics & Multimodal](./references/3-haptics-and-multimodal.md):** Tactile feedback patterns.

---

## 📊 Performance Metrics
- **Interaction Latency:** < 300ms (Goal).
- **Word Error Rate (WER):** < 3% for noisy environments.
- **User Completion Rate:** > 90% for voice-only tasks.

---

## 🔄 Evolution from 2023 to 2026
- **2023:** Batch transcription, high latency, mono-visual.
- **2024:** Real-time streaming (Whisper Turbo).
- **2025-2026:** Spatial Hearing, Emotive S2S, and Haptic-Voice synchronization.

---

**End of Voice UX Pro Standard (v1.1.0)**
