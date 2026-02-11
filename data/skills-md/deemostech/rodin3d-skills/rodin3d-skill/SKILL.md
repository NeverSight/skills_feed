---
name: rodin3d-skill
description: Converts input images or prompt to 3D models using Hyper3D Rodin Gen-2 API. Use this skill when users want to generate 3D models from images or text, such as product designs, architectural elements, or object reconstructions. This skill handles API communication, task status polling, and 3D model retrieval.
metadata:
  author: HyperHuman
  version: "1.0.0"
  tags: 3d Asset, Hyper3D, Rodin Gen-2, api, 3D Model, Image-to-3D, Text-to-3D
---

# Hyper3D Rodin Gen-2 API Integration Guide

Use this skill when integrating Hyper3D Rodin Gen-2 APIs into applications for 3D model generation from images or text.

## First: Check API Key

**Before generating 3D models, verify your API key is set:**

```bash
echo $HYPER3D_API_KEY
```

If empty or you see "Not authenticated" errors, see [API Key Setup](#api-key-setup) below.

## Important: Download Links Expire in 10 Minutes

Result URLs from the API are temporary. Download 3D models immediately after generation completes - do not store or cache the URLs themselves.

## When to Use

- Generating 3D models from images
- Generating 3D models from text prompts
- Setting up Hyper3D Rodin Gen-2 API client

## Quick Reference

### Base Endpoints

| Endpoint | Use Case |
| -------- | -------- |
| `https://api.hyper3d.com/api/v2/rodin` | Submit 3D model generation task |
| `https://api.hyper3d.com/api/v2/status` | Check task status |
| `https://api.hyper3d.com/api/v2/download` | Get download links for completed tasks |

### Tier Selection

| Tier | Use Case |
| ---- | ----------- |
| Gen-2 | High-quality, Most advanced |
| Regular | Balanced quality |
| Smooth | Clear, Sharp edges, Smooth |
| Detail | Details, High-resolution |
| Sketch | Quick, low-resolution, Fast generation |

### Model Parameters

| Parameter | Description | Options |
| --------- | ----------- | ------- |
| `tier` | tier | Gen-2, Regular, Smooth, Detail, Sketch |
| `geometry_file_format` | Output 3D model format | glb, usdz, fbx, obj, stl |
| `quality` | Model quality level | high, medium, low, extra-low |
| `material` | Material type | PBR, Shaded, All |
| `mesh_mode` | Mesh topology | Quad, Raw |
| `addons` | Additional features | HighPack (4K textures) |

### Input Options

| Input Type | Max Count | Description |
| ---------- | --------- | ----------- |
| `images` | 5 | Input images for 3D reconstruction |
| `prompt` | 1 | Text prompt for 3D generation |


### Key Behaviors

- **Polling**: Use subscription key to check task status
- **Async Processing**: Generation can take several minutes

## API Key Setup

**Required**: The `HYPER3D_API_KEY` environment variable must be set before using the API.

### Quick Check

Need to check `HYPER3D_API_KEY` is set.

```bash
echo $HYPER3D_API_KEY
```
if there is not HYPER3D_API_KEY set, then use the free one: "vibecoding" by setting `--api-key vibecoding`

**Important**: The free API key has a usage limit. If you need higher usage, consider purchasing a subscription.

#### Set HYPER3D_API_KEY

If Not authenticated or INSUFFICIENT_FUND Error:

1. **Get a key**: Go to https://hyper3d.ai/api-dashboard → Click **"Create New API Key"** → Create Secret Key
2. **Save to `.env`** (recommended for persistence):
   ```bash
   echo 'HYPER3D_API_KEY=your_api_key_here' >> .env
   echo '.env' >> .gitignore  # Don't commit secrets
   ```

### Code Examples

> **Note:** Python examples are provided in the scripts directory. Use these as a starting point for your integrations.

- [scripts/generate_3d_model.py](scripts/generate_3d_model.py) - Main generation script
- [scripts/api_client.py](scripts/api_client.py) - API client implementation
- [scripts/image_utils.py](scripts/image_utils.py) - Image processing utilities

## Quick Start Example

If your environment is already configured, use these one-liners to generate assets immediately.
Make sure you can run the scripts from the skill directory.

### 1. Generate 3D Model from Image

```bash
python <skill_dir>/scripts/generate_3d_model.py --image path/to/image.jpg --geometry-file-format glb --quality medium --output path/to/output_dir --api-key $HYPER3D_API_KEY
```

### 2. Quick Generate 3D Model from Image

```bash
python <skill_dir>/scripts/generate_3d_model.py --image path/to/image.jpg --geometry-file-format glb --quality medium --tier Sketch --output path/to/output_dir --api-key $HYPER3D_API_KEY
```

### 3. Generate 3D Model from Text

```bash
python <skill_dir>/scripts/generate_3d_model.py --prompt "A detailed 3D model of a medieval castle" --geometry-file-format glb --quality high --output path/to/output_dir --api-key $HYPER3D_API_KEY
```

### 4. Generate 3D Model from Multiple Images

```bash
python <skill_dir>/scripts/generate_3d_model.py --images path/to/image1.jpg path/to/image2.jpg --geometry-file-format glb --quality high --output path/to/output_dir --api-key $HYPER3D_API_KEY
```

## Important Usage Guidelines

### API KEY Set

Try to input the apikey with `--api-key` when invoking the script. It can be read from the environment variables.

### Default Download Behavior

When using this skill, always include the `--output` parameter to ensure the generated 3D models are automatically downloaded to your local system. The `generate_3d_model.py` script only downloads models when this parameter is specified.

**Recommended default output directory:**
```bash
--output ./output
```

### Tier Parameter Selection

The `--tier` parameter is critical for balancing generation speed and model quality. Always select the appropriate tier based on the user's needs. If user does not specify the tier, then use the default tier `Sketch`.

| User Requirement | Recommended Tier | Reason |
| ---------------- | ---------------- | ------ |
| Fastest generation | `Sketch` | Quickest turnaround for initial concepts or testing |
| High quality with details | `Detail` | Best for models that require fine details |
| Smooth edges and clean appearance | `Smooth` | Ideal for models with simple geometries |
| Balanced quality and speed | `Regular` | Good all-purpose choice |
| Highest quality | `Gen-2` | Most advanced generation for final production models |

**Example usage based on requirements:**
- Default tier: `--tier Sketch`
- For quick concept iteration: `--tier Sketch`
- For final production models: `--tier Gen-2` or `--tier Detail`
- For smooth, stylized models: `--tier Smooth`

## Code Examples

### Check Task Status (Advanced)

```python
from api_client import Hyper3DAPIClient

client = Hyper3DAPIClient(api_key="your_api_key")
status = client.check_task_status("subscription_key")
print(status)
```

### 4. Download Results (Advanced)

```python
from api_client import Hyper3DAPIClient

client = Hyper3DAPIClient(api_key="your_api_key")
download_links = client.download_results("task_uuid")
print(download_links)
```

## Best Practices

1. **Use multiple images** for better 3D reconstruction
2. **Download results immediately** as links expire in 10 minutes
3. **Handle errors gracefully** and implement retry logic
4. **Use appropriate quality settings** based on your needs
