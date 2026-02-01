---
name: remotion-best-practices-zh
description: Remotion 最佳实践（中文版）
metadata:
  tags: remotion, 视频, react, 动画, composition
---

## 何时使用

当你处理 Remotion 代码并需要领域特定知识时，请使用本技能（中文版）。

## 如何使用

阅读 `rules` 目录下的各个规则文件以查看详细说明和代码示例：

- `rules/3d.md` - 在 Remotion 中使用 Three.js 和 React Three Fiber 的 3D 内容
- `rules/animations.md` - Remotion 的动画基础
- `rules/assets.md` - 在 Remotion 中导入图片、视频、音频和字体
- `rules/audio.md` - 音频使用与处理：导入、裁剪、音量、速度、音高
- `rules/calculate-metadata.md` - 在渲染前动态设置 composition 的时长、尺寸和 props
- `rules/can-decode.md` - 使用 Mediabunny 检查视频是否可被浏览器解码
- `rules/charts.md` - 图表与数据可视化模式
- `rules/compositions.md` - 定义 Composition、静帧、文件夹、默认 props 和动态元数据
- `rules/display-captions.md` - 在 Remotion 中显示字幕（例如 TikTok 风格）并高亮单词
- `rules/extract-frames.md` - 使用 Mediabunny 在指定时间点提取视频帧
- `rules/fonts.md` - 在 Remotion 中加载 Google 字体或本地图标
- `rules/get-audio-duration.md` - 使用 Mediabunny 获取音频时长（秒）
- `rules/get-video-dimensions.md` - 使用 Mediabunny 获取视频宽高
- `rules/get-video-duration.md` - 使用 Mediabunny 获取视频时长（秒）
- `rules/gifs.md` - 在 Remotion 中同步显示 GIF
- `rules/images.md` - 在 Remotion 中嵌入图片（使用 `Img` 组件）
- `rules/import-srt-captions.md` - 使用 `@remotion/captions` 导入 `.srt` 字幕
- `rules/lottie.md` - 在 Remotion 中使用 Lottie 动画
- `rules/measuring-dom-nodes.md` - 测量 DOM 元素尺寸
- `rules/measuring-text.md` - 测量文本尺寸、适配文本与检查溢出
- `rules/sequencing.md` - 时间序列（Sequencing）模式：延迟、裁剪、限制时长
- `rules/tailwind.md` - 在 Remotion 中使用 TailwindCSS
- `rules/text-animations.md` - 文本动画模式
- `rules/timing.md` - 时间插值曲线：线性、缓动、弹簧
- `rules/transcribe-captions.md` - 将音频转录为字幕
- `rules/transitions.md` - 场景过渡模式
- `rules/trimming.md` - 剪辑/裁剪模式
- `rules/videos.md` - 嵌入视频的注意事项：裁剪、音量、速度、循环、音高
- `rules/parameters.md` - 使用 Zod schema 使视频可参数化
- `rules/maps.md` - 使用 Mapbox 添加并动画化地图

（以上为中文索引，代码示例保留原文以便直接复制）

## 默认视频尺寸（竖屏 9:16）

本技能集合默认针对竖屏视频（纵向 9:16）。推荐的默认分辨率为 **1080 x 1920**（宽 x 高）。

建议做法：
- 在 `src/Root.tsx` 或你项目的根 Remotion 配置中，统一将 `Composition` 的 `width` 设置为 `1080`，`height` 设置为 `1920`，以保证所有示例与组件默认使用竖屏尺寸。
- 将本规则文件的说明也放入 `rules/portrait.md`（已在本包中提供），便于团队成员查阅。

示例（在 `src/Root.tsx` 中）:

```tsx
import {Composition} from 'remotion';
import {MyComposition} from './MyComposition';

export const RemotionRoot = () => {
  return (
    <Composition
      id="MyComposition"
      component={MyComposition}
      durationInFrames={300}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
```
