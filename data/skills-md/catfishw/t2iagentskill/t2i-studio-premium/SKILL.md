---
name: T2I-Studio-Premium
description: 🎨 Generate stunning, state-of-the-art AI images directly from your terminal or Agent. Powered by Z-Image-Turbo.
---

# 🎨 T2I Studio Premium

Experience the future of AI image generation. **T2I Studio Premium** brings high-performance, high-quality image synthesis to your command line and AI agents.

## ✨ Features

- 🚀 **Turbo Speed**: Optimized for fast generation using the latest Z-Image-Turbo models.
- 🖼️ **Stunning Quality**: Native support for 1024x1024+ resolutions with rich aesthetics.
- 🛠️ **Developer Friendly**: Clean CLI interface and JSON output for easy integration.
- 📦 **Agent Ready**: Designed as a first-class skill for AI agents (Claude, GPT, Manus).
- 🔒 **Secure**: Private distribution via authenticated registry.

## 🚀 Installation

Install globally using the GitHub repository:

```bash
npm install -g CatfishW/T2IAgentSkill
```

## 📖 Usage

### CLI Basics

Generate a simple image:
```bash
t2i "a futuristic city floating in the clouds, cyberpunk style, hyper-realistic"
```

Advanced options:
```bash
t2i "portrait of a cyberpunk warrior" --size 1024x1024 --steps 8 --batch 2
```

### Options

| Option | Description | Default |
| :--- | :--- | :--- |
| `prompt` | The core text prompt for the image | (Required) |
| `--size`, `-s` | Image dimensions (WxH) | `768x768` |
| `--steps` | Number of sampling steps | `4` |
| `--cfg` | CFG Scale (Guidance) | `1.0` |
| `--batch`, `-b` | Number of images to generate (1-4) | `1` |
| `--format` | Output format (png/jpeg) | `png` |
| `--json` | Return JSON with Base64 data | `false` |

## 🧪 Verification

Run the built-in health check:
```bash
t2i --help
```

---
*Created by Yanlai wu*
