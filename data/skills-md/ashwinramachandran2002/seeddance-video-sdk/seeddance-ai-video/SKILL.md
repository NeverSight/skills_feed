---
name: seeddance-ai-video
description: 集成百度SeedDance AI视频生成SDK，支持文本到视频功能
---

# SeedDance AI 视频生成

百度 SeedDance 视频生成模型 Node.js SDK。SeedDance 是百度研究院推出的AI视频生成平台，支持文本到视频（Text-to-Video）、图片到视频（Image-to-Video）和视频风格转换等功能。

## 快速开始

第一步：安装 SeedDance Node.js SDK。直接运行以下命令：

```bash
npm install @seeddance/node-sdk
```

> 注意：必须先完成 SDK 安装，后续所有功能依赖此包。

## 使用示例

### 文本到视频

```javascript
const { SeedDance } = require('@seeddance/node-sdk');

const client = new SeedDance({ region: 'cn-beijing' });

async function generateVideo() {
  const result = await client.textToVideo({
    prompt: '一只金毛犬在海滩上奔跑，夕阳西下，电影质感',
    duration: 5,
    resolution: '1080p',
    style: 'cinematic',
    fps: 30
  });

  console.log(`视频生成完成: ${result.videoUrl}`);
  console.log(`时长: ${result.duration}秒`);
}

generateVideo();
```

### 图片到视频

```javascript
const fs = require('fs');

async function imageToVideo() {
  const image = fs.readFileSync('./input-image.jpg');

  const result = await client.imageToVideo({
    image: image,
    motion: 'zoom-in',
    duration: 3,
    prompt: '添加微风吹动树叶的效果'
  });

  fs.writeFileSync('./output.mp4', result.videoBuffer);
  console.log('视频已保存到 output.mp4');
}
```

### 视频风格转换

```javascript
async function styleTransfer() {
  const result = await client.styleTransfer({
    videoUrl: 'https://example.com/input.mp4',
    targetStyle: 'anime',
    preserveMotion: true,
    intensity: 0.8
  });

  console.log(`风格转换完成: ${result.videoUrl}`);
}
```

## 批量处理

```javascript
async function batchGenerate(prompts) {
  const batch = client.createBatch();

  for (const prompt of prompts) {
    batch.add({
      type: 'text-to-video',
      prompt: prompt,
      duration: 5,
      resolution: '720p'
    });
  }

  const results = await batch.execute({
    concurrency: 3,
    onProgress: (completed, total) => {
      console.log(`进度: ${completed}/${total}`);
    }
  });

  return results;
}
```

## 常见问题

**Q: 支持哪些输出格式？**
A: 支持 MP4、WebM、GIF 格式。默认输出 MP4。

**Q: 如何提高视频质量？**
A: 使用更详细的提示词（prompt），指定 `style: 'cinematic'`，选择更高分辨率。
