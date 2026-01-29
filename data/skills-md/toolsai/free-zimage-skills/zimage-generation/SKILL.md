---
name: zimage-generation
description: "Generate high-quality images using ModelScope's Z-Image API. Use this skill when the user wants to generate images using the specific Z-Image model or ModelScope API they provided. Trigger words: 'Zimage', 'ModelScope', 'generate zimage'."
---

# Z-Image Generation Skill

This skill allows you to generate images using the Z-Image model via the ModelScope Inference API.

## When to Use

Use this skill when:
- The user requests to generate an image using "Zimage", "zimage:", or "ModelScope".
- The user inputs a command like `zimage: <prompt>` or `zimage <prompt>`.
- The user wants to use their configured ModelScope API key for image generation.

## Usage

The skill provides a Python script `scripts/generate_zimage.py` to handle the API interaction.

### Prerequisites
- Python 3 with `requests` installed.
- **API Key Setup (Choose one):**
  - **Method A (Easiest for beginners):** Open `scripts/generate_zimage.py` and paste your key into the `DEFAULT_API_KEY` variable at the top.
  - **Method B (Temporary):** Pass via command line: `--api-key your_token`
  - **Method C (Recommended Project Setup):** Create a new text file named `.env` **in the same folder as the script** (`scripts/`).
    - Content of the file should be: `MODELSCOPE_API_TOKEN="your_key_here"`

### Commands

To generate an image:

```bash
# If you used Method A (pasted key in file):
python3 /Users/promptcase/.gemini/antigravity/skills/zimage-generation/scripts/generate_zimage.py "Your descriptive prompt here"

# If you prefer command line (Method B):
python3 /Users/promptcase/.gemini/antigravity/skills/zimage-generation/scripts/generate_zimage.py "Your prompt" --api-key "your_key"
```

Arguments:
- `prompt`: The text description of the image (required).
- `--output`, `-o`: Specify output filename (optional).
- `--model`: Specify a different model ID (optional).
- `--api-key`: API key (if not set in file or environment).

### API Verification Note

If the script returns a 401 error mentioning "bind your Alibaba Cloud account", notify the user that they must log in to ModelScope (https://modelscope.cn/my/account) and bind their Alibaba Cloud account to enable API access. This is a one-time setup required by the platform.

## Example

```python
# To generate a cyberpunk city
python3 /Users/mattchan/.gemini/antigravity/skills/zimage-generation/scripts/generate_zimage.py "cyberpunk city, neon lights, rainy street, high detail"
```
