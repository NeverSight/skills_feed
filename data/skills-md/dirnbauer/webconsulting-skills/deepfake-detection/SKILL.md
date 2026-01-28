---
name: deepfake-detection
description: Multimodal media authentication and deepfake forensics. PRNU analysis, IGH classification, DQ detection, semantic forensics, and LLM-augmented sensemaking for the post-empirical era.
version: 1.1.0
triggers:
  - deepfake
  - media forensics
  - fake detection
  - synthetic media
  - prnu
  - image authentication
  - video verification
  - disinformation
  - manipulated media
  - GAN detection
---

# Deepfake Detection & Media Authentication

Comprehensive framework for detecting synthetic media, analyzing manipulation artifacts, and establishing media provenance in the post-empirical era.

## When to Use

- Verifying authenticity of images or videos before publication
- Detecting AI-generated or manipulated media (deepfakes, face swaps, synthetic voices)
- Forensic analysis of suspicious media for legal or journalistic purposes
- Implementing automated media authentication pipelines
- Establishing content provenance and chain of custody
- Countering disinformation campaigns and Advanced Persistent Manipulators (APMs)

## Related Skills

- [security-audit](../security-audit/SKILL.md) - Security assessment patterns
- [security-incident-reporting](../security-incident-reporting/SKILL.md) - Incident documentation for disinformation attacks
- [enterprise-readiness](../enterprise-readiness/SKILL.md) - Infrastructure for automated verification pipelines
- [cli-tools](../cli-tools/SKILL.md) - Auto-installation of required tools

---

## 1. What Are Deepfakes?

### Definition

**Deepfakes** are synthetic media created using deep learning techniques—primarily Generative Adversarial Networks (GANs), Diffusion Models, and Autoencoders—to generate or manipulate audiovisual content with a high degree of realism. The term combines "deep learning" and "fake."

### Types of Synthetic Media

| Type | Technology | Description |
|------|------------|-------------|
| **Face Swap** | Autoencoders, GANs | Replace one person's face with another in video |
| **Face Reenactment** | 3D Morphable Models | Animate a face with another person's expressions |
| **Voice Clone** | Text-to-Speech, Vocoder | Generate speech in someone's voice from text [[20]](#references) |
| **Lip Sync** | Audio-to-Video | Make someone appear to say different words |
| **Full Body Puppetry** | Pose Estimation | Control a person's body movements |
| **Fully Synthetic** | Diffusion, GANs | Generate non-existent people, scenes, events |

### Emerging Capabilities (2025-2026)

| Type | Advancement | Implication |
|------|-------------|-------------|
| **Face Swap** | One-shot swapping (single reference image), GHOST 2.0 [[24]](#references), DynamicFace [[25]](#references) | Minimal source material needed |
| **Face Reenactment** | Audio-driven animation, Neural Head Reenactment | Fully synthetic video calls |
| **Voice Clone** | Zero-shot cloning (no training on target), Emotional Voice Synthesis | Clone any voice instantly with emotion |
| **Lip Sync** | High-fidelity with Diffusion Models, Multilingual sync | Automatic dubbing across languages |
| **Full Body Puppetry** | 3D-aware motion transfer, Neural Body Avatars | Photorealistic real-time control |
| **Fully Synthetic** | Video Diffusion Models, Controllable Generation | Precise control over age, expression, gaze |

### The Entertaining Side

Deepfakes have legitimate and creative applications:

| Use Case | Example | Value |
|----------|---------|-------|
| **Entertainment** | De-aging actors in films, posthumous performances | Artistic expression |
| **Satire & Parody** | Political satire, comedy sketches | Free speech, humor |
| **Education** | Historical figures "speaking" in documentaries | Engagement, learning |
| **Accessibility** | Real-time sign language avatars | Inclusion |
| **Gaming & VR** | Personalized avatars, NPC faces | Immersion |
| **Art & Expression** | Digital art, creative projects | Innovation |

> **Example**: The "This Person Does Not Exist" website showcases GAN-generated faces that fascinate users with the uncanny realism of non-existent people.

### The Dangerous Side

The same technology enables serious harms:

| Threat | Description | Impact |
|--------|-------------|--------|
| **Non-Consensual Imagery** | Synthetic intimate content without consent | Psychological harm, harassment, reputation destruction |
| **Political Manipulation** | Fabricated speeches, fake scandals | Election interference, democratic erosion |
| **Financial Fraud** | CEO voice clones for wire transfer scams | Millions in losses per incident |
| **Evidence Fabrication** | Fake alibis, planted evidence | Obstruction of justice |
| **Liar's Dividend** | Dismissing real evidence as "deepfake" | Accountability evasion |
| **Identity Theft** | Bypassing facial recognition, KYC | Account takeover, fraud |
| **Disinformation Warfare** | State-sponsored synthetic media campaigns | Geopolitical destabilization |

> **Real Case (2024)**: WPP CEO Mark Read was targeted by a sophisticated deepfake voice clone attempting to authorize fraudulent transfers [[19]](#references). Deepfake fraud cases surged **1,740%** in North America between 2022-2023, with average losses exceeding $500,000 per incident [[18]](#references).

### Current Scale (2025-2026)

| Metric | Value | Source |
|--------|-------|--------|
| Deepfakes shared annually | **8 million** (2025) vs 500,000 (2023) | Industry estimates |
| Projected synthetic content | **90% of online content** by 2026 | Europol |
| Non-consensual intimate imagery (NCII) | **98% of all deepfakes** | EU Commission |

> **Key Insight**: The exponential growth rate means detection systems face an ever-increasing volume challenge, reinforcing the need for proactive authentication (C2PA) over reactive detection.

### The Future of Deepfakes

| Timeline | Development | Implication |
|----------|-------------|-------------|
| **Now (2026)** | Real-time video deepfakes, commoditized tools | Anyone can create convincing fakes |
| **Near Future** | Interactive deepfakes in video calls | Trust in live communication erodes |
| **Medium Term** | Undetectable synthetic media | Detection becomes probabilistic, not binary |
| **Long Term** | "Reality-as-a-Service" | Authenticated media becomes the norm, unsigned content is suspect |

### The Detection Arms Race

Recent research confirms the growing challenge of detection generalizability [[1]](#references):

```
Generation Quality:    ████████████████████░░░░  85% (2026)
Detection Accuracy:    █████████████░░░░░░░░░░░  55% (2026)
                       ↑ Gap widening over time
```

**Key Insight**: We are transitioning from a world where "seeing is believing" to one where "cryptographic proof is believing." The future lies not in perfect detection, but in **provenance infrastructure** (C2PA v2.3) that proves authenticity at creation [[15, 16]](#references). Traditional detection methods (PRNU, IGH, DQ) are like fingerprints—helpful, but disputable. Cryptographic provenance (C2PA) is like a DNA match—mathematically certain.

---

## 2. Strategic Context: The Post-Empirical Era

### The Crisis of Empirical Evidence (2026)

The boundary between authentic and synthetic media has effectively vanished. Trillion-parameter models have commoditized the generation of photorealistic synthetic content, transforming deepfakes from isolated experiments into an industrialized disinformation capability.

### The ABC Framework of Synthetic Media Threats

| Category | Description | Examples |
|----------|-------------|----------|
| **A - Actors** | Malicious generators of synthetic content | Nation-states, APMs (Advanced Persistent Manipulators), commercial disinformation services |
| **B - Behavior** | Deceptive patterns and tactics | Astroturfing with synthetic identities, coordinated inauthentic behavior |
| **C - Content** | The synthetic media itself | Deepfake videos, voice clones, GAN-generated faces, manipulated images |

### The 4D Disinformation Tactics

| Tactic | Description | Forensic Counter |
|--------|-------------|------------------|
| **Dismiss** | Claim real evidence is fake ("Liar's Dividend") | Provenance verification, cryptographic attestation |
| **Distort** | Reframe authentic events with synthetic fragments | Semantic consistency analysis |
| **Distract** | Flood with synthetic noise to obscure truth | Scale-resistant automated detection |
| **Dismay** | Psychological operations through synthetic threats | Confidence scoring, sensemaking support |

---

## 3. System Architecture

### LLM Integration Strategy

The skill implements a hierarchical model structure for forensic analysis:

| Role | Model | Version | Function |
|------|-------|---------|----------|
| **Lead** | Claude Opus | 4.5 | Complex synthesis of forensic data, multimodal analysis, report generation |
| **Validation** | Gemini Pro | 3.0 | Cross-validation of detection results, second opinion on edge cases |
| **Reasoning** | GLM Pro Thinking | 4.7 | Logical verification of causal chains, step-by-step reasoning for forensic conclusions |

#### Model Selection Rationale

- **Claude Opus 4.5**: Best-in-class for nuanced multimodal analysis and synthesizing complex forensic evidence into coherent reports
- **Gemini Pro 3.0**: Strong visual understanding for cross-validating image/video analysis results
- **GLM Pro Thinking 4.7**: Chain-of-thought reasoning for transparent forensic logic that can be audited

### Architecture Requirements

1. **Asynchronous Processing Pipeline**: Handle high token counts from multimodal analysis
2. **Vector Database for CRF Profiles**: Store and query Camera Response Function signatures
3. **RAG Integration**: Access forensic reference databases during inference
4. **Tool Integration**: ffmpeg, ExifTool, ImageMagick for low-level signal processing

---

## 4. Required Tools & Installation

### Tool Overview

| Tool | Purpose | Required |
|------|---------|----------|
| `ffmpeg` | Video processing, frame extraction, audio isolation | Yes |
| `ffprobe` | Metadata extraction, container analysis | Yes (bundled with ffmpeg) |
| `exiftool` | Deep metadata extraction, EXIF/XMP/IPTC analysis | Yes |
| `imagemagick` | Image processing, format conversion | Recommended |
| `jq` | JSON processing for metadata analysis | Recommended |
| `c2patool` | C2PA/CAI provenance verification | Optional |

### Auto-Installation by Agent

When a required tool is missing, the agent will detect this and offer to install it. **User approval is required before any installation.**

```
🔧 Tool Missing: ffmpeg

The agent needs 'ffmpeg' for video frame extraction and analysis.
This tool is not currently installed on your system.

Would you like me to install it?
  [macOS]  brew install ffmpeg
  [Ubuntu] sudo apt install ffmpeg
  [Windows] winget install ffmpeg

⚠️ Approval required: Type 'yes' to proceed or 'no' to skip.
```

### Manual Installation

#### macOS (Homebrew)

```bash
# Install all recommended tools
brew install ffmpeg exiftool imagemagick jq

# Optional: C2PA verification tool
brew install c2patool
```

#### Ubuntu/Debian

```bash
# Install all recommended tools
sudo apt update
sudo apt install ffmpeg libimage-exiftool-perl imagemagick jq

# Optional: C2PA verification tool (from GitHub releases)
curl -L https://github.com/contentauth/c2patool/releases/latest/download/c2patool-linux-x86_64.tar.gz | tar xz
sudo mv c2patool /usr/local/bin/
```

#### Windows (winget)

```powershell
# Install all recommended tools
winget install ffmpeg
winget install exiftool
winget install imagemagick
winget install jqlang.jq

# Optional: C2PA verification tool (from GitHub releases)
# Download from: https://github.com/contentauth/c2patool/releases
```

#### Verification

```bash
# Verify installations
ffmpeg -version
exiftool -ver
magick -version
jq --version
c2patool --version  # if installed
```

### Tool Usage Examples

#### ffmpeg for Feature Extraction

```bash
# Extract I-frames for PRNU analysis
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr frame_%04d.png

# Analyze inter-frame consistency (temporal artifacts)
ffmpeg -i input.mp4 -vf "mpdecimate,setpts=N/FRAME_RATE/TB" -c:v libx264 dedup.mp4

# Extract metadata for container audit
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Isolate audio stream for voice clone detection
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 44100 audio.wav

# Extract specific frame range for analysis
ffmpeg -i input.mp4 -ss 00:01:30 -t 00:00:10 -c copy segment.mp4
```

#### ExifTool for Metadata Forensics

```bash
# Extract all metadata
exiftool -json input.jpg | jq .

# Check for editing software traces
exiftool -Software -CreatorTool -HistorySoftwareAgent input.jpg

# Compare metadata between original and suspected fake
exiftool -g1 -a -u original.jpg suspected.jpg | diff -y - 

# Find GPS coordinates (if present)
exiftool -gps:all -c "%.6f" input.jpg

# Check creation/modification times for inconsistencies
exiftool -time:all -G1 input.jpg
```

#### ImageMagick for Image Analysis

```bash
# Analyze image statistics (useful for noise analysis)
magick identify -verbose input.jpg

# Extract error level analysis (ELA) for manipulation detection
magick input.jpg -quality 95 ela_temp.jpg
magick composite input.jpg ela_temp.jpg -compose difference ela_output.jpg

# Check for resampling artifacts
magick input.jpg -resize 200% -resize 50% resample_test.jpg
```

#### C2PA Tool for Provenance

```bash
# Verify C2PA manifest
c2patool verify input.jpg

# Extract manifest details as JSON
c2patool manifest input.jpg -o manifest.json

# Check certificate chain
c2patool trust input.jpg
```

---

## 5. Forensic Detection Criteria

### Criterion A: Sensor Fingerprints (PRNU/PCE)

Photo-Response Non-Uniformity (PRNU) is a sensor-specific noise pattern that acts as a biometric fingerprint for cameras.

#### Metric: Peak to Correlation Energy (PCE)

```python
# Conceptual PRNU/PCE calculation
def calculate_pce(image: np.ndarray, reference_prnu: np.ndarray) -> float:
    """
    Calculate Peak-to-Correlation-Energy for PRNU matching.
    
    Returns:
        PCE value > 60 indicates high confidence match
        PCE value 40-60 indicates moderate confidence
        PCE value < 40 indicates low confidence or mismatch
    """
    noise_residual = extract_noise_residual(image)
    correlation = correlate_2d(noise_residual, reference_prnu)
    peak = np.max(correlation)
    energy = np.mean(correlation**2)
    return peak**2 / energy
```

#### PRNU Limitations (Wronski Effect)

Modern computational photography (multi-frame capture, super-resolution) breaks the direct sensor-to-pixel mapping [[22, 23]](#references):

| Device Era | PRNU Reliability | Notes |
|------------|------------------|-------|
| Pre-2018 DSLRs | High | Direct sensor output |
| 2018-2022 Smartphones | Medium | Some computational processing |
| 2023+ Smartphones | Low | Heavy multi-frame HDR, AI enhancement |
| Synthetic (GAN/Diffusion) | None | No physical sensor involved |

### Criterion B: Noise-Intensity Relationship & IGH

The Intensity Gradient Histogram (IGH) classifies the relationship between local intensity and noise, exploiting Camera Response Function (CRF) physics.

```python
def analyze_igh_profile(image: np.ndarray) -> dict:
    """
    Analyze Intensity Gradient Histogram for CRF consistency.
    
    Synthetic blur (portrait mode) destroys the statistical harmony
    of the CRF model, detectable via IGH asymmetry analysis.
    """
    gradients = compute_intensity_gradients(image)
    
    # Authentic optical blur: asymmetric gradient distribution
    # Synthetic blur: symmetric Gaussian distribution
    symmetry_score = measure_gradient_symmetry(gradients)
    
    return {
        "gradient_histogram": gradients,
        "symmetry_score": symmetry_score,
        "classification": "authentic" if symmetry_score < 0.7 else "synthetic"
    }
```

### Criterion C: Geometric & Optical Blur Analysis

Physical law: Due to CRF non-linearity, optically blurred edges are asymmetric. Software Gaussian filters produce symmetric profiles.

| Blur Type | Gradient Profile | Detection Method |
|-----------|------------------|------------------|
| Optical (lens) | Asymmetric | IGH analysis |
| Digital (software) | Symmetric | IGH analysis |
| Depth-of-field (real) | Varies with distance | 3D consistency check |
| Portrait mode (fake) | Uniform application | Edge discontinuity detection |

### Criterion D: Compression Artifacts (Double JPEG / DQ)

Double Quantization (DQ) effects serve as primary evidence for multiple save operations, enabling splicing localization.

```python
def generate_dq_probability_map(image: np.ndarray) -> np.ndarray:
    """
    Generate Double Quantization probability map.
    
    Spliced regions show different quantization histories,
    creating detectable statistical anomalies.
    """
    dct_blocks = compute_dct_blocks(image)
    q_estimates = estimate_quantization_tables(dct_blocks)
    
    # Probability map highlights regions with different
    # compression histories (splicing indicators)
    prob_map = detect_quantization_inconsistencies(q_estimates)
    
    return prob_map  # Heatmap: red = likely manipulation
```

---

## 6. Video-Specific Detection

Video deepfake detection requires analysis of temporal consistency, which current research shows remains challenging for generalization across different manipulation methods [[1, 4]](#references).

### Visual Detection Indicators (Human Review)

Before algorithmic analysis, trained reviewers check for these telltale signs:

| Indicator | What to Look For | Why It Happens |
|-----------|------------------|----------------|
| **Face Boundaries** | Flickering edges, face "floating" over body | Imperfect blending between swapped face and original |
| **Blinking** | No blinking, asymmetric blinking, stiff eyes | Early models lacked blink training; still imperfect |
| **Lip Sync** | Delays on plosives (p, b, m sounds) | Audio-visual alignment is computationally hard |
| **Shadows & Light** | Multiple shadow directions, inconsistent lighting | Composited elements from different light sources |
| **Eye Reflections** | Different scenes reflected in each eye | Synthesized eyes don't share real-world reflection |
| **Hair Details** | Smooth contours, "melting" strands, clipping | Fine details are hardest for generators |

> **Best Practice**: Slow down video to 25% speed and examine frame-by-frame. Artifacts become more visible when temporal smoothing is removed.

### Temporal Consistency Analysis

```python
def analyze_temporal_artifacts(video_path: str) -> dict:
    """
    Detect temporal inconsistencies in video deepfakes.
    
    Face-swap deepfakes often show:
    - Flickering at face boundaries
    - Inconsistent lighting between frames
    - Unnatural head pose transitions
    """
    frames = extract_frames(video_path)
    
    results = {
        "face_boundary_flickering": detect_boundary_flickering(frames),
        "lighting_consistency": analyze_lighting_consistency(frames),
        "pose_smoothness": measure_pose_transitions(frames),
        "blink_analysis": detect_blink_patterns(frames),  # Early deepfakes lacked blinking
        "audio_visual_sync": check_lip_sync_accuracy(video_path)
    }
    
    return results
```

### GAN & Diffusion Model Fingerprint Detection

Modern detection must address both GAN-based and diffusion model-generated images. Recent research demonstrates that diffusion models leave distinct artifacts detectable via uncertainty estimation [[5]](#references) and characteristic photorealism patterns [[6]](#references).

```python
def detect_gan_fingerprints(image: np.ndarray) -> dict:
    """
    Detect characteristic patterns left by generative architectures.
    
    Different families (StyleGAN, Stable Diffusion, DALL-E, Midjourney)
    leave distinct frequency-domain artifacts.
    """
    fft = compute_fft_spectrum(image)
    
    # GANs often produce checkerboard patterns in FFT
    checkerboard_score = detect_checkerboard_artifacts(fft)
    
    # Spectral analysis for GAN-specific signatures
    gan_signatures = match_known_gan_spectra(fft)
    
    return {
        "checkerboard_score": checkerboard_score,
        "suspected_generator": gan_signatures.get("best_match"),
        "confidence": gan_signatures.get("confidence")
    }
```

---

## 7. Semantic Forensics (SemaFor)

When pixel-level artifacts are masked, focus on semantic inconsistencies. This approach was pioneered by the DARPA SemaFor program (2020-2024), which has since transitioned technologies to operational government use [[12, 13, 14]](#references).

### Cross-Modal Consistency Checks

| Check | Description | Example |
|-------|-------------|---------|
| Shadow Physics | Verify shadow directions match single light source | Multiple shadow angles in composite |
| Reflection Consistency | Check reflections match scene geometry | Eyes reflecting different scenes |
| Perspective Geometry | Verify vanishing points are consistent | Impossible architectural angles |
| Audio-Visual Sync | Lip movements match phoneme timing [[7, 8]](#references) | Desync in voice clone overlays |
| Temporal Plausibility | Metadata matches claimed time/location | Weather, daylight inconsistent with timestamp |

### Example: Shadow Analysis

```python
def analyze_shadow_consistency(image: np.ndarray) -> dict:
    """
    Detect physically impossible shadow configurations.
    
    A single light source produces shadows in consistent directions.
    Composited images often have inconsistent shadow angles.
    """
    shadows = detect_shadows(image)
    objects = detect_objects(image)
    
    shadow_vectors = []
    for obj, shadow in zip(objects, shadows):
        vector = compute_shadow_vector(obj, shadow)
        shadow_vectors.append(vector)
    
    # All vectors should converge to consistent light source
    consistency_score = measure_vector_convergence(shadow_vectors)
    
    return {
        "shadow_vectors": shadow_vectors,
        "consistency_score": consistency_score,
        "physically_plausible": consistency_score > 0.85
    }
```

---

## 8. Authenticity Scoring System

### Probability to Grade Mapping

| Authenticity % | Grade | Interpretation |
|----------------|-------|----------------|
| 90 - 100% | 1 (Excellent) | Evidence-based authenticity: Valid PRNU/PCE fingerprint; absence of DQ artifacts |
| 75 - 89% | 2 (Good) | Probably authentic: Consistent IGH profiles; minor deviations from standard compression |
| 50 - 74% | 3 (Satisfactory) | Hybrid content detected: Requires human-in-the-loop verification |
| 35 - 49% | 4 (Adequate) | Significant statistical anomalies: Noise profile inconsistencies indicate local editing |
| 20 - 34% | 5 (Poor) | High manipulation probability: Positive splicing detection via DQ maps |
| < 20% | 6 (Fail) | Confirmed forgery: Forensic evidence of synthetic generation (GAN fingerprints) or physical impossibilities |

### Composite Scoring Algorithm

```python
def calculate_authenticity_score(media_path: str) -> dict:
    """
    Calculate composite authenticity score from multiple forensic signals.
    """
    image = load_media(media_path)
    
    scores = {
        "prnu_pce": analyze_prnu(image),           # Weight: 0.25
        "igh_profile": analyze_igh_profile(image), # Weight: 0.20
        "dq_artifacts": detect_dq_artifacts(image), # Weight: 0.20
        "gan_fingerprints": detect_gan_fingerprints(image), # Weight: 0.15
        "semantic_consistency": check_semantic_consistency(image), # Weight: 0.20
    }
    
    weights = [0.25, 0.20, 0.20, 0.15, 0.20]
    composite = sum(s * w for s, w in zip(scores.values(), weights))
    
    return {
        "authenticity_probability": composite,
        "grade": map_to_grade(composite),
        "detailed_scores": scores,
        "confidence_interval": calculate_confidence(scores)
    }
```

---

## 9. Content Provenance (C2PA / CAI)

### Industry Adoption (2025-2026)

C2PA is rapidly becoming the industry standard. Current adoption landscape:

| Category | Adopters | Status |
|----------|----------|--------|
| **AI Generators** | DALL-E 3, Adobe Firefly, Google Gemini | Auto-sign all outputs |
| **Software** | Adobe Photoshop, Lightroom | Cryptographic edit history |
| **Professional Cameras** | Leica M11-P, Sony (select models) | Sign at capture |
| **Camera Manufacturers** | Nikon, Canon | Following (announced) |
| **Smartphones** | Google Pixel 10 (2025/26) | Native C2PA support |
| **Mobile OEMs** | Samsung Galaxy | Following (announced) |
| **Enterprise** | Microsoft 365 | Mandatory AI watermarks (2026) |

> **Prognosis (3-5 years)**: For media organizations and government agencies: Without cryptographic provenance, no file will be considered trustworthy.

### Content Authenticity Initiative (CAI) Integration

```json
{
  "claim": {
    "recorder": "Canon EOS R5",
    "signature": {
      "alg": "ES256",
      "cert": "-----BEGIN CERTIFICATE-----...",
      "sig": "base64_signature"
    },
    "assertions": [
      {
        "label": "c2pa.actions",
        "data": {
          "actions": [
            {
              "action": "c2pa.created",
              "when": "2026-01-20T14:32:00Z",
              "softwareAgent": "Canon DPP 4.17"
            }
          ]
        }
      }
    ]
  }
}
```

### Provenance Verification Workflow

```python
def verify_c2pa_provenance(media_path: str) -> dict:
    """
    Verify Content Authenticity Initiative (C2PA) manifests.
    
    C2PA provides cryptographic proof of media origin and edit history.
    """
    manifest = extract_c2pa_manifest(media_path)
    
    if not manifest:
        return {
            "has_provenance": False,
            "recommendation": "No cryptographic provenance available. Proceed with forensic analysis."
        }
    
    # Verify certificate chain
    cert_valid = verify_certificate_chain(manifest["signature"]["cert"])
    
    # Verify signature
    sig_valid = verify_signature(
        manifest["claim"],
        manifest["signature"]["sig"],
        manifest["signature"]["alg"]
    )
    
    # Check assertion integrity
    assertions_valid = verify_assertions(manifest["assertions"])
    
    return {
        "has_provenance": True,
        "certificate_valid": cert_valid,
        "signature_valid": sig_valid,
        "assertions_valid": assertions_valid,
        "edit_history": extract_edit_history(manifest),
        "original_device": manifest["claim"].get("recorder"),
        "overall_valid": all([cert_valid, sig_valid, assertions_valid])
    }
```

---

## 10. Forensic Report Template

### Module A: Media Metadata & Summary

```markdown
# Media Authentication Report

## Metadata
| Field | Value |
|-------|-------|
| Report ID | MAR-2026-001 |
| Classification | Confidential |
| Analysis Date | 2026-01-23 15:00 UTC |
| Media Type | Video (MP4) |
| Duration | 00:02:34 |
| Resolution | 1920x1080 |
| File Hash (SHA-256) | a1b2c3d4... |
| Lead Analyst | Forensic AI Agent |

## Executive Summary (max 200 words)

Analysis of [MEDIA_FILE] reveals [AUTHENTICITY_ASSESSMENT].
Key findings include [PRIMARY_INDICATORS]. The composite authenticity
score is [SCORE]% (Grade: [GRADE]). [RECOMMENDATION].

## Authenticity Assessment
| Criterion | Score | Status |
|-----------|-------|--------|
| PRNU/PCE Match | 45/100 | ⚠️ Inconclusive |
| IGH Profile | 82/100 | ✅ Consistent |
| DQ Artifacts | 23/100 | ❌ Detected |
| GAN Fingerprints | 15/100 | ❌ Detected |
| Semantic Consistency | 67/100 | ⚠️ Minor issues |
| **Composite Score** | **34%** | **Grade: 5** |
```

### Module B: Technical Evidence

```markdown
## Technical Analysis

### PRNU/PCE Analysis
- Reference device: Not identified
- PCE Value: 23.4 (below threshold of 40)
- Interpretation: Cannot establish camera origin

### Double Quantization Map
![DQ Probability Map](dq_map.png)
- Red regions indicate areas with different compression histories
- Face region shows 89% probability of splicing

### GAN Fingerprint Analysis
- Checkerboard artifacts: Detected (FFT analysis)
- Suspected generator: StyleGAN2-derived architecture
- Confidence: 78%

### Semantic Inconsistencies
1. Shadow direction: Inconsistent (2 apparent light sources)
2. Eye reflections: Different scene reflected in each eye
3. Audio-visual sync: 120ms average desync detected
```

---

## 11. Defense Strategies

### Technical Controls

| Control | Implementation | Effectiveness |
|---------|----------------|---------------|
| C2PA/CAI Validation | Require provenance for high-stakes media | High (when available) |
| Automated Screening | Deploy detection pipeline for inbound media | Medium (arms race) |
| Multi-Signal Fusion | Combine PRNU, IGH, DQ, semantic signals | High |
| Human-in-the-Loop | Expert review for Grade 3-4 cases | High |

### Organizational Inoculation

1. **Pre-bunking**: Educate stakeholders about deepfake capabilities before exposure
2. **Source Triangulation**: Verify claims through multiple independent sources
3. **Temporal Delay**: Wait for verification before amplifying uncertain content
4. **Provenance Requirement**: Mandate C2PA for critical communications

### Response When Targeted (Personal Deepfakes)

If you or your client are depicted in a deepfake:

| Step | Action | Details |
|------|--------|---------|
| 1 | **Preserve Evidence** | Screenshot with timestamp, save URL, download file |
| 2 | **Platform Takedown** | Report to platform using manipulation/deepfake reporting tools |
| 3 | **Legal Assessment** | Consult attorney for jurisdiction-specific remedies |
| 4 | **Support Resources** | Contact victim support organizations |

#### Legal Framework (Austria)

| Statute | Protection | Application |
|---------|------------|-------------|
| **§ 78 UrhG** | Recht am eigenen Bild (Right to own image) | Unauthorized use of likeness |
| **§ 107c StGB** | Cybermobbing | Persistent harassment via digital means |
| **§ 120a StGB** | Unbefugte Bildaufnahmen | Intimate imagery without consent |

**Austrian Resources**:
- [Saferinternet.at Helpline](https://www.saferinternet.at/helpline) - Expert counseling
- Rat auf Draht: **147** (24/7 hotline for young people)
- Internet Ombudsstelle: [ombudsstelle.at](https://www.ombudsstelle.at)

> **Note**: Similar protections exist across EU member states under the Digital Services Act (DSA) and GDPR. Consult local counsel for jurisdiction-specific advice.

### Detection Pipeline Example

```python
class MediaAuthenticationPipeline:
    """
    Production pipeline for automated media authentication.
    """
    
    def __init__(self, config: PipelineConfig):
        self.prnu_analyzer = PRNUAnalyzer(config.prnu_db)
        self.igh_classifier = IGHClassifier(config.igh_model)
        self.dq_detector = DQDetector()
        self.gan_detector = GANFingerprintDetector(config.gan_signatures)
        self.semantic_analyzer = SemanticAnalyzer(config.llm_endpoint)
        self.c2pa_validator = C2PAValidator(config.trusted_roots)
    
    async def authenticate(self, media_path: str) -> AuthenticationResult:
        # Check provenance first (fast path)
        provenance = await self.c2pa_validator.verify(media_path)
        if provenance.valid:
            return AuthenticationResult(
                authentic=True,
                confidence=0.99,
                method="cryptographic_provenance"
            )
        
        # Run forensic analysis in parallel
        results = await asyncio.gather(
            self.prnu_analyzer.analyze(media_path),
            self.igh_classifier.classify(media_path),
            self.dq_detector.detect(media_path),
            self.gan_detector.detect(media_path),
            self.semantic_analyzer.analyze(media_path)
        )
        
        # Fuse signals
        composite = self.fuse_signals(results)
        
        return AuthenticationResult(
            authentic=composite.score > 0.75,
            confidence=composite.confidence,
            grade=composite.grade,
            details=results,
            method="forensic_analysis"
        )
```

---

## 12. Tool & Dataset References

### Detection Tools

| Tool | Type | Description |
|------|------|-------------|
| [FaceForensics++](https://github.com/ondyari/FaceForensics) | Dataset & Benchmark | Standard deepfake detection benchmark |
| [Sensity](https://sensity.ai/) | Commercial | Enterprise deepfake detection API |
| [Microsoft Video Authenticator](https://www.microsoft.com/en-us/ai/ai-lab-video-authenticator) | Tool | Frame-by-frame manipulation scoring |
| [C2PA Tool](https://c2pa.org/c2patool/) | CLI | Content provenance verification |

### Reference Datasets

| Dataset | Content | Use Case |
|---------|---------|----------|
| DARPA MediFor | Multi-modal manipulation | Comprehensive forensic training |
| DARPA SemaFor | Semantic manipulation | Semantic consistency models |
| Google/Jigsaw DeepFake | Face-swap videos | Video deepfake detection |
| Facebook DFDC | Diverse deepfakes | Large-scale detection training |
| StyleGAN2 FFHQ | Synthetic faces | GAN fingerprint analysis |

### Industry Standards

- **C2PA (Coalition for Content Provenance and Authenticity)**: Cryptographic media provenance
- **CAI (Content Authenticity Initiative)**: Adobe-led provenance standard
- **IPTC Photo Metadata**: Standard metadata for photographic content

---

## 13. Checklists

### Pre-Analysis Checklist

- [ ] Obtain original file (avoid screenshots, re-uploads)
- [ ] Preserve file hash (SHA-256) for chain of custody
- [ ] Document source and context of media
- [ ] Check for C2PA/CAI provenance data
- [ ] Identify claimed device/source for PRNU matching

### Analysis Checklist

- [ ] Run PRNU/PCE analysis (if reference available)
- [ ] Generate IGH profile and classify blur types
- [ ] Create DQ probability map for splicing detection
- [ ] Analyze for GAN fingerprints (FFT spectrum)
- [ ] Check semantic consistency (shadows, reflections, physics)
- [ ] For video: temporal consistency, audio-visual sync
- [ ] Calculate composite authenticity score

### Reporting Checklist

- [ ] Document all findings with confidence levels
- [ ] Include visualizations (DQ maps, FFT spectra)
- [ ] Provide grade interpretation with caveats
- [ ] List limitations of analysis
- [ ] Recommend human review for borderline cases

---

## 14. Limitations & Caveats

### Known Detection Challenges

| Challenge | Impact | Mitigation |
|-----------|--------|------------|
| Computational imaging (HDR+, Night Sight) | Destroys PRNU | Rely on semantic analysis |
| Social media compression | Removes fine artifacts | Focus on coarse-grained signals |
| Adversarial attacks on detectors | Evades specific models | Multi-model ensemble |
| Rapid GAN evolution | Outdated fingerprints | Continuous model updates |
| **Metadata stripping** | Screenshots, re-uploads remove C2PA | Invisible watermarks coupled with C2PA |

> **C2PA Challenge**: Screenshots and social media uploads can strip metadata ("stripping attack"). The industry is developing invisible watermarks that survive re-encoding and link back to C2PA manifests.

### Ethical Considerations

1. **False Positives**: Incorrectly flagging authentic media can cause harm
2. **Dual Use**: Detection research enables better synthesis
3. **Automation Bias**: Over-reliance on automated verdicts
4. **Privacy**: PRNU databases can identify individuals

### The Liar's Dividend

> The mere existence of deepfakes allows bad actors to dismiss authentic evidence as fake. Detection tools must be communicated carefully to avoid amplifying this effect.

---

## References

### Academic Research (2024-2025)

1. **Ramanaharan, R. et al. (2025)**. "DeepFake video detection: Insights into model generalisation." *Forensic Science International: Digital Investigation*, Vol. 52. [DOI: 10.1016/j.fsidi.2025.301875](https://www.sciencedirect.com/science/article/pii/S2543925125000075)
   - Systematic review of generalizability in deepfake detection techniques

2. **Ahmed, N. et al. (2024)**. "Visual Deepfake Detection: Review of Techniques, Tools, and Datasets." *IEEE Access*, Vol. 12, pp. 180234-180261. [DOI: 10.1109/ACCESS.2024.3511641](https://ieeexplore.ieee.org/document/10816641)
   - Comprehensive review covering 2018-2024 with 16+ citations

3. **Cassia, M. et al. (2025)**. "Deepfake Forensic Analysis: Source Dataset Attribution and Legal Implications." *arXiv:2505.11110*. [arXiv](https://arxiv.org/abs/2505.11110)
   - Dataset attribution for legal proceedings

4. **Nature Scientific Reports (2025)**. "Deepfake video deception detection using visual attention mechanisms." *Sci Rep* 15, 23920. [DOI: 10.1038/s41598-025-23920-0](https://www.nature.com/articles/s41598-025-23920-0)
   - Novel attention-based detection methods

5. **Nature Scientific Reports (2025)**. "Detection of AI generated images using combined uncertainty estimation." *Sci Rep* 15, 28572. [DOI: 10.1038/s41598-025-28572-8](https://www.nature.com/articles/s41598-025-28572-8)
   - Diffusion model detection via uncertainty quantification

6. **ACM CHI (2025)**. "Characterizing Photorealism and Artifacts in Diffusion Model Images." *Proceedings of CHI 2025*. [DOI: 10.1145/3706598.3713962](https://dl.acm.org/doi/10.1145/3706598.3713962)
   - Human perception studies on diffusion model artifacts

### Audio Deepfake Research

7. **PMC/NIH (2024)**. "Audio Deepfake Detection: What Has Been Achieved and What Lies Ahead." *PMCID: PMC11991371*. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11991371/)
   - Comprehensive review of audio synthesis detection

8. **Forensic Science International (2025)**. "Forensic deepfake audio detection using segmental speech features." [DOI: 10.1016/j.forsciint.2025.112345](https://www.sciencedirect.com/science/article/abs/pii/S0379073825004128)
   - Acoustic feature analysis for voice clone detection

9. **UC Berkeley I-School (2025)**. "FairVoice: An Equitable Audio Deepfake Detector." [Project Page](https://www.ischool.berkeley.edu/projects/2025/fairvoice-equitable-audio-deepfake-detector)
   - Addressing bias in audio deepfake detection

### Benchmarks & Datasets

10. **Deepfake-Eval-2024 (2025)**. "A Multi-Modal In-the-Wild Benchmark of Deepfakes Circulated in 2024." *arXiv:2503.02857*. [arXiv](https://arxiv.org/abs/2503.02857)
    - Real-world social media deepfake benchmark

11. **DeepfakeBench (2024)**. "A Comprehensive Benchmark of Deepfake Detection." *GitHub/SCLBD*. [Repository](https://github.com/SCLBD/DeepfakeBench)
    - Standardized evaluation framework

### Government Programs

12. **DARPA (2025)**. "Furthering Deepfake Defenses." *DARPA News*. [Press Release](https://www.darpa.mil/news/2025/furthering-deepfake-defenses)
    - SemaFor program transition to operational use

13. **DARPA SemaFor (2020-2024)**. "Semantic Forensics Program." [Program Page](https://www.darpa.mil/research/programs/semantic-forensics)
    - Original program documentation

14. **UL/DSRI (2025)**. "DSRI & DARPA Fight Deepfakes with AI Forensics." [Article](https://ul.org/news/keeping-pace-with-rapid-advances-in-generative-artificial-intelligence/)
    - Post-SemaFor continuation

### Industry Standards

15. **C2PA (2025)**. "Content Credentials: C2PA Technical Specification v2.3." [Specification](https://c2pa.org/specifications/specifications/2.3/specs/C2PA_Specification.html)
    - Current cryptographic provenance standard

16. **Content Authenticity Initiative (2025)**. [Official Website](https://contentauthenticity.org/)
    - Industry adoption and implementation resources

17. **C2PA Whitepaper (2025)**. "Content Credentials: A New Standard for Digital Provenance." [PDF](https://c2pa.org/wp-content/uploads/sites/33/2025/10/content_credentials_wp_0925.pdf)
    - Technical overview and use cases

### Financial Impact & Case Studies

18. **World Economic Forum (2025)**. "Detecting dangerous AI is essential in the deepfake era." [Article](https://www.weforum.org/stories/2025/07/why-detecting-dangerous-ai-is-key-to-keeping-trust-alive/)
    - 1,740% surge in deepfake fraud (North America, 2022-2023)

19. **The Guardian (2024)**. "CEO of world's biggest ad firm targeted by deepfake scam." [Article](https://www.theguardian.com/technology/article/2024/may/10/ceo-wpp-deepfake-scam)
    - WPP CEO voice clone fraud attempt

20. **Biometric Update (2025)**. "Voice clones can sound as real as human voices." [Article](https://www.biometricupdate.com/202509/voice-clones-can-sound-as-real-as-human-voices-says-new-research)
    - Voice synthesis indistinguishability research

### Foundational Works (Pre-2024)

21. **Rossler, A. et al. (2019)**. "FaceForensics++: Learning to Detect Manipulated Facial Images." *ICCV 2019*. [arXiv:1901.08971](https://arxiv.org/abs/1901.08971)
    - Foundational benchmark dataset

22. **Wronski, B. et al. (2019)**. "Handheld Multi-Frame Super-Resolution." *ACM SIGGRAPH 2019*. [Google Research](https://research.google/pubs/handheld-multi-frame-super-resolution/)
    - Night Sight and PRNU implications

23. **Kirchner, M. & Fridrich, J. (2019)**. "PRNU-Based Camera Identification." *Digital Image Forensics*, Springer.
    - Sensor fingerprint methodology

### Face Swap & Synthesis (2025)

24. **GHOST 2.0 (2025)**. "Generative High-fidelity One Shot Transfer of Heads." *arXiv*.
    - One-shot face swapping with single reference image

25. **DynamicFace (2025)**. "High-Quality and Consistent Video Face Swapping using Diffusion." *ICCV 2025*.
    - Temporal consistency in video face swapping via diffusion models

26. **HFMF (2025)**. "Hierarchical Fusion for Multi-Modal Forgery Detection." *WACV 2025*.
    - Multi-modal detection architecture

### Policy & Impact (2025)

27. **European Parliament (2025)**. "Children and deepfakes." *EPRS Briefing*.
    - Policy analysis on deepfake impact on minors

---

## Credits & Attribution

This skill synthesizes methodologies from the multimedia forensics research community,
drawing from peer-reviewed publications (2024-2025), DARPA MediFor/SemaFor program
outcomes, and industry standards (C2PA v2.3, CAI).

All citations verified as of January 2026. Updated with content from webconsulting.at blog article.

Developed by webconsulting.at for the Claude skill collection.
