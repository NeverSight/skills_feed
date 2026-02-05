---
name: banana-watermark-remove-skill
description: Remove Gemini Nano Banana / Pro watermarks from images using GeminiWatermarkTool. Use when users want to (1) remove visible watermarks from AI-generated images, (2) batch process multiple images to remove watermarks, (3) clean up Gemini watermarks from screenshots or documents. Supports Windows, macOS, and Linux platforms.
---

# Banana Watermark Remove Skill

Remove Gemini Nano Banana / Pro visible watermarks from images using reverse alpha blending.

## Tool Location

The GeminiWatermarkTool executables are bundled within this skill at `tools/`:

- **Windows**: `tools/GeminiWatermarkTool.exe`
- **macOS**: `tools/GeminiWatermarkTool-macOS`
- **Linux**: `tools/GeminiWatermarkTool-Linux`

All binaries are standalone with zero dependencies.

## Workflow

1. **Determine the operating system** and select the correct executable:
   - Windows → `GeminiWatermarkTool.exe`
   - macOS → `GeminiWatermarkTool-macOS`
   - Linux → `GeminiWatermarkTool-Linux`

2. **Execute the command** based on input type:
   - **Single file**: `GeminiWatermarkTool -i watermarked.jpg -o clean.jpg`
   - **Directory (batch)**: `GeminiWatermarkTool -i ./input_folder/ -o ./output_folder/`

3. **Verify output**

## Usage Examples

```bash
# Windows - Single file
.\GeminiWatermarkTool.exe -i watermarked.jpg -o clean.jpg

# Windows - Directory batch
.\GeminiWatermarkTool.exe -i ./input_folder/ -o ./output_folder/

# macOS - Single file
./GeminiWatermarkTool-macOS -i watermarked.jpg -o clean.jpg

# macOS - Directory batch
./GeminiWatermarkTool-macOS -i ./input_folder/ -o ./output_folder/

# Linux - Single file
./GeminiWatermarkTool-Linux -i watermarked.jpg -o clean.jpg

# Linux - Directory batch
./GeminiWatermarkTool-Linux -i ./input_folder/ -o ./output_folder/
```

## Command Line Options

| Option            | Short | Description              |
| ----------------- | ----- | ------------------------ |
| `--input <path>`  | `-i`  | Input file or directory  |
| `--output <path>` | `-o`  | Output file or directory |
| `--verbose`       | `-v`  | Enable verbose output    |
| `--quiet`         | `-q`  | Suppress output          |
| `--version`       | `-V`  | Show version             |
| `--help`          | `-h`  | Show help                |

Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`

## Limitations

- **Visible watermarks only**: Does NOT remove SynthID (invisible watermarks)
- **Gemini watermarks only**: Designed specifically for Gemini Nano Banana / Pro watermarks
- Auto-detects 48×48 or 96×96 watermark size based on image dimensions
