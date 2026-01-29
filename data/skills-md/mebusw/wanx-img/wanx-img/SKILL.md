---
name: wanx-img
description: Generate or edit images using WanX (Alibaba's text-to-image model)
allowed-tools: Read, Bash
---

## Overview

This skill provides commands for generating and editing images using the WanX model from Alibaba.

## Workflow

1. decide user's intent: whether to generate a new image, or edit given images
2. decide which version of visual LLM will be used, use the highest version by default, if it's not availiable or rejected by provider, then downgrade to other version
3. if user provides images urls/paths, you don't need to read the files but only pass them to scripts
4. if user specify size of image in pixel number, pass it to scripts, or if user specify aspect ratio, convert it to image size and then pass to scripts
5. run a proper script to generate or edit images with user input prompt, synchronously by default
6. output original prompts, extended actual prompts, size of image, and full urls of generated images (don't miss any parameters from the url for example Signature etc. )


## Conversion between ratio and image size
The total number of pixels must be between [1280*1280, 1440*1440] and the aspect ratio must be between [1:4, 4:1]. For example, 768*2700 meets the requirements. The default value is 1280*1280.

| aspect ratio | image size |
| --- | --- |
| 1:1 | 1280*1280 |
| 3:4 | 1104*1472 |
| 4:3 | 1472*1104 |
| 9:16 | 960*1696 |
| 16:9 | 1696*960 |


## Available Scripts

- `wanx2.6-text-to-image-v2-demo.py` - Generate images from text prompts, using WanX visual model version 2.6
- `wanx2.6-image-edit-demo.py` - Edit images with text prompts, optionally with reference/mask images, using WanX visual model version 2.6
- `wanx2.5-text-to-image-v2-demo.py` - Generate images from text prompts, using WanX visual model version 2.5
- `wanx2.5-image-edit-demo.py` - Edit images with text prompts, optionally with reference/mask images, using WanX visual model version 2.5
- `wanx2.2-text-to-image-v2-demo.py` - Generate images from text prompts, using WanX visual model version 2.2


## Setting Up
首次使用时，进入目录并安装依赖：
```bash
cd ~/.claude/skills/wanx-img
python3 -m venv py312-ai-rag
source py312-ai-rag/bin/activate
pip install dashscope python-dotenv argparse
cp .env.example .env
```

后续执行python脚本时，先执行`source py312-ai-rag/bin/activate`，然后再执行脚本。如果`python`或`python3`命令找不到合适的packages，则应用`~/.pyenv/versions/py312-ai-rag/bin/python`来替代作为执行器。

## Usage Examples

- **Use custom prompt to generate image**
```bash
~/.pyenv/versions/py312-ai-rag/bin/python "./scripts/wanx2.6-text-to-image-v2-demo.py" --prompt "一只可爱的猫咪在花园里玩耍. ar 3:4" --size "960*1280"
```

- **Use synchronous call with custom prompt and negative prompt to generate image**
```bash
~/.pyenv/versions/py312-ai-rag/bin/python "./scripts/wanx2.6-text-to-image-v2-demo.py" -p "美丽的日落风景" -n "人物" --sync
```

- **Use custom prompt and referencing images to edit image**
```bash
~/.pyenv/versions/py312-ai-rag/bin/python "./scripts/wanx2.6-image-edit-demo.py" --prompt "参考图1的风格和图2的背景，生成番茄炒蛋" --images http://1.img http://2.img -m http://3.img -b http://4.img
```

- **Use synchronous call with custom prompt to edit iamge**
```bash
~/.pyenv/versions/py312-ai-rag/bin/python "./scripts/wanx2.6-image-edit-demo.py" -p "参考图1的风格和图2的背景，生成番茄炒蛋" --sync
```


## Requirements

- Python 3.12+
- LLM API credentials configured in demo scripts
- DashScope Python SDK 1.25.8+

