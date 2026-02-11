---
name: music-timbre
description: Analyze timbre — MFCC, spectral features, loudness, source separation
user_invocable: true
---

# /music-timbre — Timbre & Spectral Analysis

Extract timbral and spectral characteristics: MFCC coefficients, spectral centroid/bandwidth/rolloff, loudness (LUFS), dynamic range, brightness, warmth, and optionally separate audio sources.

## Usage

```
/music-timbre <audio_file_path>
```

## Steps

1. Validate the audio file path
2. Run timbre analysis:

```bash
python3 -m music_analyzer timbre "<audio_file_path>"
```

Add `--no-separation` to skip Demucs source separation.

3. Present results:
   - **Brightness**: Score 0-1 (higher = brighter timbre)
   - **Warmth**: Score 0-1 (higher = more low-frequency energy)
   - **Dynamic Range**: Estimated in dB
   - **Loudness**: LUFS (if pyloudnorm available)
   - **MFCC Summary**: 13-coefficient means
   - **Stems**: Paths to separated vocals/drums/bass/other (if demucs ran)

## Output Fields

| Field | Description |
|-------|-------------|
| `mfcc` | MFCC means and stds |
| `spectral` | Centroid, bandwidth, rolloff, ZCR |
| `loudness_lufs` | Integrated loudness in LUFS |
| `dynamic_range_db` | Dynamic range in dB |
| `brightness` | Brightness score 0-1 |
| `warmth` | Warmth score 0-1 |
| `stems` | Separated stem file paths (if available) |
