---
name: file-adapters
description: Image file processing utilities (圖像檔案處理工具). Use when working with image resizing (圖片縮放), format conversion (格式轉換), watermarks (浮水印), or processing pipelines (處理管道). Covers Sharp integration, Buffer/Stream handling (緩衝/串流處理), batch processing (批次處理), and NestJS integration (NestJS 整合).
---

# File Converter Adapters

This skill provides comprehensive guidance for using `@rytass/file-converter` packages to process images with resizing, format conversion, watermarking, and pipeline processing.

## Overview

All adapters implement the `FileConverter` interface from `@rytass/file-converter`, providing a unified API for image processing:

| Package | Function | Based On |
|---------|----------|----------|
| `@rytass/file-converter` | Core interfaces and pipeline manager (核心介面與管道管理器) | TypeScript interfaces |
| `@rytass/file-converter-adapter-image-resizer` | Image resizing (圖像縮放) | Sharp ^0.34.5 |
| `@rytass/file-converter-adapter-image-transcoder` | Format conversion (格式轉換) | Sharp ^0.34.5, file-type ^21.1.1 |
| `@rytass/file-converter-adapter-image-watermark` | Watermark overlay (浮水印疊加) | Sharp ^0.34.5 |

### Base Interface (@rytass/file-converter)

All adapters share these core concepts:

**FileConverter<O>** - Main interface for file conversion
```typescript
interface FileConverter<O = Record<string, unknown>> {
  convert<Buffer>(file: ConvertableFile): Promise<Buffer>;
  convert<Readable>(file: ConvertableFile): Promise<Readable>;
}
```

**ConvertableFile** - Supported input types
```typescript
type ConvertableFile = Readable | Buffer;
```

**ConverterManager** - Pipeline processor for chaining conversions
```typescript
class ConverterManager {
  constructor(converters: FileConverter[]);
  convert<Output>(file: ConvertableFile): Promise<Output>;
}
```

## Installation

```bash
# Install base package
npm install @rytass/file-converter

# Choose the adapters you need
npm install @rytass/file-converter-adapter-image-resizer
npm install @rytass/file-converter-adapter-image-transcoder
npm install @rytass/file-converter-adapter-image-watermark
```

## Quick Start

### ImageResizer (圖像縮放)

Resize images while maintaining or controlling aspect ratio:

```typescript
import { ImageResizer } from '@rytass/file-converter-adapter-image-resizer';
import { readFileSync, writeFileSync } from 'fs';

// Resize to max 800x600, maintaining aspect ratio
const resizer = new ImageResizer({
  maxWidth: 800,
  maxHeight: 600,
  keepAspectRatio: true,
  concurrency: 4, // Optional: parallel processing
});

const originalImage = readFileSync('photo.jpg');
const resizedImage = await resizer.convert<Buffer>(originalImage);
writeFileSync('photo-resized.jpg', resizedImage);
```

### ImageTranscoder (格式轉換)

Convert images between formats (JPEG, PNG, WebP, AVIF, etc.):

```typescript
import { ImageTranscoder } from '@rytass/file-converter-adapter-image-transcoder';

// Convert to WebP format
const transcoder = new ImageTranscoder({
  targetFormat: 'webp',
  quality: 85,
  effort: 4,
});

const jpegBuffer = readFileSync('photo.jpg');
const webpBuffer = await transcoder.convert<Buffer>(jpegBuffer);
writeFileSync('photo.webp', webpBuffer);
```

### ImageWatermark (浮水印)

Add watermarks to images:

```typescript
import { ImageWatermark } from '@rytass/file-converter-adapter-image-watermark';
import { gravity } from 'sharp';

// Add watermark at bottom-right corner
const watermarker = new ImageWatermark({
  watermarks: [
    {
      image: readFileSync('logo.png'), // Can be Buffer or file path
      gravity: gravity.southeast, // Position: bottom-right
    },
  ],
});

const originalImage = readFileSync('photo.jpg');
const watermarkedImage = await watermarker.convert<Buffer>(originalImage);
writeFileSync('photo-watermarked.jpg', watermarkedImage);
```

### ConverterManager (管道處理)

Chain multiple converters in a pipeline:

```typescript
import { ConverterManager } from '@rytass/file-converter';
import { ImageResizer } from '@rytass/file-converter-adapter-image-resizer';
import { ImageWatermark } from '@rytass/file-converter-adapter-image-watermark';
import { ImageTranscoder } from '@rytass/file-converter-adapter-image-transcoder';
import { gravity } from 'sharp';

// Create processing pipeline: Resize → Watermark → Convert to WebP
const pipeline = new ConverterManager([
  new ImageResizer({
    maxWidth: 1200,
    maxHeight: 800,
    keepAspectRatio: true,
  }),
  new ImageWatermark({
    watermarks: [
      {
        image: './logo.png',
        gravity: gravity.southeast,
      },
    ],
  }),
  new ImageTranscoder({
    targetFormat: 'webp',
    quality: 85,
    effort: 4,
  }),
]);

const originalImage = readFileSync('photo.jpg');
const processedImage = await pipeline.convert<Buffer>(originalImage);
writeFileSync('processed.webp', processedImage);
```

## Common Patterns

### Buffer vs Stream Processing

**Buffer** - Use for small files (小檔案), faster, uses more memory:
```typescript
const buffer = readFileSync('image.jpg');
const result = await converter.convert<Buffer>(buffer);
writeFileSync('output.jpg', result);
```

**Stream (Readable)** - Use for large files (大檔案), memory efficient:
```typescript
import { createReadStream, createWriteStream } from 'fs';
import { Readable } from 'stream';

const stream = createReadStream('large-image.jpg');
const resultStream = await converter.convert<Readable>(stream);

// Pipe to output
resultStream.pipe(createWriteStream('output.jpg'));
```

### Single Conversion

Process one image with one converter:

```typescript
// Resize only
const resizer = new ImageResizer({ maxWidth: 800 });
const resized = await resizer.convert<Buffer>(imageBuffer);

// Convert format only
const transcoder = new ImageTranscoder({ targetFormat: 'webp', quality: 90 });
const webp = await transcoder.convert<Buffer>(jpegBuffer);
```

### Pipeline Conversion

Chain multiple operations:

```typescript
// Three-step processing
const pipeline = new ConverterManager([
  new ImageResizer({ maxWidth: 1000, maxHeight: 750 }),
  new ImageWatermark({ watermarks: [{ image: 'logo.png' }] }),
  new ImageTranscoder({ targetFormat: 'webp', quality: 85 }),
]);

const result = await pipeline.convert<Buffer>(originalImage);
```

### Batch Processing

Process multiple images:

```typescript
import { glob } from 'glob';
import { basename } from 'path';

const pipeline = new ConverterManager([
  new ImageResizer({ maxWidth: 800 }),
  new ImageTranscoder({ targetFormat: 'webp', quality: 85 }),
]);

// Find all JPEG files
const images = await glob('photos/*.jpg');

// Process all images
await Promise.all(
  images.map(async (imagePath) => {
    const buffer = readFileSync(imagePath);
    const result = await pipeline.convert<Buffer>(buffer);
    const outputName = basename(imagePath, '.jpg') + '.webp';
    writeFileSync(`output/${outputName}`, result);
  })
);
```

## Feature Comparison

| Feature | ImageResizer | ImageTranscoder | ImageWatermark | ConverterManager |
|---------|:------------:|:---------------:|:--------------:|:----------------:|
| Resize Images (縮放圖片) | Yes | No | No | Via pipeline |
| Convert Formats (轉換格式) | No | Yes | No | Via pipeline |
| Add Watermarks (添加浮水印) | No | No | Yes | Via pipeline |
| Maintain Aspect Ratio (保持縱橫比) | Yes | N/A | N/A | N/A |
| Crop to Fit (裁剪適配) | Yes | No | No | N/A |
| Buffer Support (緩衝支援) | Yes | Yes | Yes | Yes |
| Stream Support (串流支援) | Yes | Yes | Yes | Yes |
| Concurrency Control (並發控制) | Yes | Yes | Yes | N/A |
| Multiple Watermarks (多浮水印) | No | No | Yes | N/A |
| Pipeline Chaining (管道串聯) | No | No | No | Yes |

### Supported Formats (ImageTranscoder)

| Input Formats | Output Formats |
|--------------|----------------|
| jpg, png, webp, gif, avif, tif, svg | jpg/jpeg, png, webp, avif, heif, gif, tif/tiff |

> **Note:** Input formats are detected by `file-type` library. JPEG uses 'jpg' internally.

**內部常數（未導出）：**
- `SupportSources` - 支援的輸入格式陣列：`['jpg', 'png', 'webp', 'gif', 'avif', 'tif', 'svg']`
- `UnsupportedSource` - 當輸入格式不支援時拋出的錯誤類別

### ImageTranscoderOptions Types

每種輸出格式都有對應的 Sharp options：

```typescript
import type { AvifOptions, GifOptions, HeifOptions, JpegOptions, PngOptions, TiffOptions, WebpOptions } from 'sharp';

type ImageTranscoderOptions =
  | { targetFormat: 'avif' } & AvifOptions
  | { targetFormat: 'heif' } & HeifOptions
  | { targetFormat: 'gif' } & GifOptions
  | { targetFormat: 'tif' | 'tiff' } & TiffOptions
  | { targetFormat: 'png' } & PngOptions
  | { targetFormat: 'webp' } & WebpOptions
  | { targetFormat: 'jpg' | 'jpeg' } & JpegOptions;

// Constructor 額外支援 concurrency 選項
new ImageTranscoder(options: ImageTranscoderOptions & { concurrency?: number });
```

### ImageResizerOptions

```typescript
interface ImageResizerOptions {
  maxWidth?: number;      // 最大寬度（至少需設定 maxWidth 或 maxHeight 其一）
  maxHeight?: number;     // 最大高度
  keepAspectRatio?: boolean;  // 保持縱橫比（預設 true，使用 'inside' fit）
  concurrency?: number;   // 並發數（預設 1）
}
```

> **Note:** 使用 `withoutEnlargement: true` 確保不會放大小於目標尺寸的圖片。當 `keepAspectRatio=false` 時使用 `fit: 'cover'` 裁剪適配。

### ImageWatermarkOptions

```typescript
interface Watermark {
  image: string | Buffer;  // 浮水印圖片（檔案路徑或 Buffer）
  gravity?: Gravity;       // 位置（預設 southeast）
}

interface ImageWatermarkOptions {
  watermarks: Watermark[];  // 浮水印陣列（支援多個浮水印）
  concurrency?: number;     // 並發數（預設 1）
}
```

### Watermark Positions (ImageWatermark)

| Position | Gravity Constant | Description |
|----------|-----------------|-------------|
| Top-Left (左上) | `gravity.northwest` | Northwest corner |
| Top-Center (上中) | `gravity.north` | Top center |
| Top-Right (右上) | `gravity.northeast` | Northeast corner |
| Middle-Left (中左) | `gravity.west` | Middle left |
| Center (中央) | `gravity.center` | Center |
| Middle-Right (中右) | `gravity.east` | Middle right |
| Bottom-Left (左下) | `gravity.southwest` | Southwest corner |
| Bottom-Center (下中) | `gravity.south` | Bottom center |
| Bottom-Right (右下) | `gravity.southeast` | Southeast corner (default) |

## Detailed Documentation

For complete API reference and advanced usage:

- [ImageResizer Complete Reference](IMAGE-RESIZER.md) - All options, methods, and use cases
- [ImageTranscoder Complete Reference](IMAGE-TRANSCODER.md) - Format-specific options, error handling
- [ImageWatermark Complete Reference](IMAGE-WATERMARK.md) - Watermark configuration, positioning

## Complete Examples

### E-commerce Product Images

Process product photos: resize for web, add branding watermark, convert to modern format:

```typescript
import { ConverterManager } from '@rytass/file-converter';
import { ImageResizer } from '@rytass/file-converter-adapter-image-resizer';
import { ImageWatermark } from '@rytass/file-converter-adapter-image-watermark';
import { ImageTranscoder } from '@rytass/file-converter-adapter-image-transcoder';
import { readFileSync, writeFileSync } from 'fs';
import { gravity } from 'sharp';

// Create product image processor
const productImageProcessor = new ConverterManager([
  // Step 1: Resize to 1200x1200 max
  new ImageResizer({
    maxWidth: 1200,
    maxHeight: 1200,
    keepAspectRatio: true,
    concurrency: 4,
  }),

  // Step 2: Add brand watermark at bottom-right
  new ImageWatermark({
    watermarks: [
      {
        image: readFileSync('brand-logo.png'),
        gravity: gravity.southeast,
      },
    ],
  }),

  // Step 3: Convert to WebP for smaller file size
  new ImageTranscoder({
    targetFormat: 'webp',
    quality: 85,
    effort: 4, // Higher effort = better compression
  }),
]);

// Process a product image
const originalPhoto = readFileSync('product-001-raw.jpg');
const processedPhoto = await productImageProcessor.convert<Buffer>(originalPhoto);
writeFileSync('product-001.webp', processedPhoto);
```

### Large File Stream Processing

Handle large files efficiently with streams to avoid memory issues:

```typescript
import { createReadStream, createWriteStream } from 'fs';
import { ImageResizer } from '@rytass/file-converter-adapter-image-resizer';
import { Readable } from 'stream';

// Create resizer
const resizer = new ImageResizer({
  maxWidth: 1920,
  maxHeight: 1080,
  keepAspectRatio: true,
});

// Process large file using streams
const inputStream = createReadStream('large-photo.jpg');
const outputStream = await resizer.convert<Readable>(inputStream);

// Pipe to output file
outputStream.pipe(createWriteStream('large-photo-resized.jpg'));

// Wait for completion
await new Promise((resolve, reject) => {
  outputStream.on('finish', resolve);
  outputStream.on('error', reject);
});
```

### Batch Processing with Progress Tracking

Process multiple images with progress updates:

```typescript
import { glob } from 'glob';
import { basename } from 'path';
import { ConverterManager } from '@rytass/file-converter';
import { ImageResizer } from '@rytass/file-converter-adapter-image-resizer';
import { ImageTranscoder } from '@rytass/file-converter-adapter-image-transcoder';

// Create pipeline
const pipeline = new ConverterManager([
  new ImageResizer({ maxWidth: 800, maxHeight: 600, keepAspectRatio: true }),
  new ImageTranscoder({ targetFormat: 'webp', quality: 80 }),
]);

// Find all images
const images = await glob('input-photos/*.{jpg,png,jpeg}');
const total = images.length;
let processed = 0;

console.log(`Found ${total} images to process`);

// Process with progress tracking
for (const imagePath of images) {
  const buffer = readFileSync(imagePath);
  const result = await pipeline.convert<Buffer>(buffer);

  const outputName = basename(imagePath).replace(/\.(jpg|png|jpeg)$/, '.webp');
  writeFileSync(`output/${outputName}`, result);

  processed++;
  console.log(`Progress: ${processed}/${total} (${Math.round((processed / total) * 100)}%)`);
}

console.log('All images processed successfully!');
```

### Conditional Processing

Apply different processing based on image properties:

```typescript
import sharp from 'sharp';
import { ImageResizer } from '@rytass/file-converter-adapter-image-resizer';
import { ImageTranscoder } from '@rytass/file-converter-adapter-image-transcoder';
import { ConverterManager } from '@rytass/file-converter';

async function processImage(inputBuffer: Buffer): Promise<Buffer> {
  // Get image metadata
  const metadata = await sharp(inputBuffer).metadata();

  if (!metadata.width || !metadata.height) {
    throw new Error('Unable to read image dimensions');
  }

  // For large images: resize first
  if (metadata.width > 2000 || metadata.height > 2000) {
    console.log('Large image detected, resizing...');
    const pipeline = new ConverterManager([
      new ImageResizer({ maxWidth: 1600, maxHeight: 1600, keepAspectRatio: true }),
      new ImageTranscoder({ targetFormat: 'webp', quality: 85 }),
    ]);
    return pipeline.convert<Buffer>(inputBuffer);
  }

  // For small images: just convert format
  console.log('Small image detected, converting format only...');
  const transcoder = new ImageTranscoder({ targetFormat: 'webp', quality: 90 });
  return transcoder.convert<Buffer>(inputBuffer);
}

// Usage
const imageBuffer = readFileSync('photo.jpg');
const result = await processImage(imageBuffer);
writeFileSync('output.webp', result);
```

## Troubleshooting

### Common Issues

**Memory Errors with Large Images**
- Solution: Use Stream processing instead of Buffer

```typescript
// Instead of Buffer
const buffer = readFileSync('huge-image.jpg');
const result = await converter.convert<Buffer>(buffer);

// Use Stream
const stream = createReadStream('huge-image.jpg');
const resultStream = await converter.convert<Readable>(stream);
```

**Sharp Cache Issues**
- Sharp automatically disables cache in all adapters with `sharp.cache(false)`
- No action needed

**Concurrency Performance**
- Adjust `concurrency` option based on your CPU cores
- Default is 1 (single-threaded)
- Try 4-8 for multi-core systems

```typescript
const resizer = new ImageResizer({
  maxWidth: 800,
  concurrency: 8, // Adjust based on CPU cores
});
```

**Unsupported Format Errors (ImageTranscoder)**
- Check input format is supported: JPEG, PNG, WebP, GIF, AVIF, TIFF, SVG
- Error will throw `UnsupportedSource` exception (internal class, catch using `instanceof Error` and check `message === 'UnsupportedSource'`)

**Output Quality Issues**
- Increase `quality` parameter (0-100)
- For WebP/AVIF, increase `effort` (0-9) for better compression

```typescript
const transcoder = new ImageTranscoder({
  targetFormat: 'webp',
  quality: 95, // Higher quality
  effort: 6,   // More compression effort
});
```
