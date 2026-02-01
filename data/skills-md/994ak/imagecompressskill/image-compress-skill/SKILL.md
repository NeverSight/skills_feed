---
name: image-compress-skill
description: A production-grade, Rust-powered image optimization engine for AI Agents. Smartly routes between PNG quantization and WebP compression.
---

# ImageCompressSkill

> The intelligent image optimization engine for AI Agents. Smart routing between PNG quantization and WebP compression.

## 1. Smart Strategy Overview

The optimal compression strategy depends on the input content type and the target use case.

| Content Type | Primary Strategy | Toolchain | Target Format |
| :--- | :--- | :--- | :--- |
| **Photographs** | **Lossy WebP** | `image` -> `libwebp` | `.webp` |
| **Graphics / Logos / UI** | **Optimized PNG** | `image` -> `imagequant` -> `oxipng` | `.png` |
| **Universal (Web)** | **WebP (High Compat)** | `image` -> `libwebp` | `.webp` |
| **Universal (Archive)** | **Optimized PNG** | `image` -> `oxipng` (Lossless) | `.png` |

**Decision Logic:**
1.  **Try WebP First (Default)**: For most web use cases, WebP offers the best size/quality ratio (30-90% reduction).
2.  **Fallback to PNG**: If the input is a simple graphic (low color count) OR if WebP results in a larger file (rare, but happens with simple shapes), use the Quantized PNG pipeline.
3.  **Strict Quality**: If the user demands "Lossless" or "No visual change", skip quantization and use only `oxipng` (PNG) or Lossless WebP.

## Setup

This skill requires the `image-compress-tool` binary.

If the tool is not found, the agent should run:
```bash
./scripts/install.sh
```

## Usage

### 1. Smart Compression (Auto)
**Best for**: Photos, complex gradients, web assets.
*   **Quality (`-q`)**:
    *   **80-85**: Sweet spot for web (visually indistinguishable). **Default**.
    *   **75**: Aggressive, might show slight artifacts on sharp edges.
    *   **90+**: Archival quality, diminishing returns.
*   **Method (`-m`)**:
    *   **4**: Default. Good balance.
    *   **6**: Slowest but best compression. Use for static assets (build time).
*   **Usage**:
    ```rust
    // Rust (using webp crate)
    let encoder = webp::Encoder::from_image(&img)?;
    let memory = encoder.encode(80.0); // Q=80
    ```

### B. Optimized PNG (via `imagequant` + `oxipng`)
**Best for**: Logos, icons, screenshots, line art, transparent assets.
*   **Step 1: Quantization (`imagequant`)**
    *   **Quality**: `min=0, max=80` (or `80-90` for high fidelity).
    *   **Speed**: `4` (Default). `1` (Slowest/Best).
    *   *Note*: This step converts 32-bit RGBA to 8-bit Indexed Color. It is "lossy" but visually excellent for graphics.
*   **Step 2: Optimization (`oxipng`)**
    *   **Level (`-o`)**:
        *   **2**: Default. Good balance.
        *   **4**: Recommended for production builds (slower but worth it).
        *   **6**: Max. Very slow.
    *   **Strip (`--strip safe`)**: Remove metadata.
    *   **Interlace (`-i 0`)**: Disable interlacing (saves ~20%).
*   **Usage**:
    ```rust
    // Pipeline
    let (palette, pixels) = imagequant_attributes.quantize(img)?; // Step 1
    let png_data = encode_png(palette, pixels);
    let optimized = oxipng::optimize_from_memory(&png_data, &options)?; // Step 2
    ```

## 3. Implementation Rules for Agents

When implementing image compression tools:

1.  **Dual Mode Support**: Always implement BOTH pipelines (WebP and PNG).
2.  **Smart Defaults**:
    *   Default Quality: **80** (for both WebP and ImageQuant).
    *   Default WebP Method: **4**.
    *   Default Oxipng Level: **2** (or 4 if speed isn't critical).
3.  **Output Logic**:
    *   If user asks for "compress this image" -> Output **WebP** (smallest).
    *   If user asks for "optimize this PNG" -> Output **Quantized PNG**.
    *   If input is small (< 10KB) simple shape -> Check if WebP > PNG, if so, prefer PNG.

## 4. Code Resources

### Dependency Setup
```toml
[dependencies]
image = "0.25"
imagequant = "4.4"
oxipng = "10.1"
webp = "0.3"
anyhow = "1.0"
clap = { version = "4.5", features = ["derive"] }
```

### Rust Implementation Snippet (The "Golden Path")
See `image-compress-tool/src/main.rs` in the current project for the reference implementation that handles:
1. CLI Argument Parsing
2. Image Loading
3. WebP Branch (using `webp` crate)
4. PNG Branch (using `imagequant` -> `png` encoding -> `oxipng`)

## 5. Verification
Always verify:
1.  **File Size**: Is output < input?
2.  **Format**: Is it a valid WebP/PNG?
3.  **Visual**: Open in browser/viewer.
