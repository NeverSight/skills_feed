---
name: remotion-video
description: 从零创建 Remotion 视频（默认 16:9 横屏 1920x1080，可选竖屏 1080x1920），涵盖项目初始化、场景开发、Edge TTS 配音、时间轴编排到 MP4 导出的完整工作流。适用于产品宣传片、知识科普、品牌展示等场景。
metadata: {"clawdbot":{"requires":{"bins":["node","npm","ffprobe"],"env":[]}}}
---

# Remotion 视频生成技能

## 适用场景

- 产品宣传片（默认 16:9 横屏 1920x1080）
- 竖屏短视频（抖音/视频号 1080x1920，需用户明确指定）
- 知识科普动画
- 品牌展示片
- 任何需要 React 代码驱动的程序化视频

## 画面规格

| 规格 | 分辨率 | 适用场景 |
|------|--------|---------|
| **横屏（默认）** | 1920×1080 | 官网宣传、B站、YouTube、会议展示 |
| 竖屏 | 1080×1920 | 抖音、视频号、Instagram Reels |

默认使用横屏。仅当用户明确要求竖屏时才切换。

## 前置条件

本技能基于 Remotion 官方脚手架 + 官方 Skills（`remotion-best-practices`）。
官方 Skills 提供 API 层面的最佳实践（动画、音频、转场等 30 个规则文件），本技能提供**端到端工作流**（内容规划 → 配音 → 场景开发 → 导出）。两者互补使用。

## 工作流概览

```
阶段1: 项目初始化 → 阶段2: 内容规划 → 阶段3: 配音生成
     → 阶段4: 场景开发 → 阶段5: 时间轴集成 → 阶段6: 预览与导出
```

---

## 阶段 1: 项目初始化

### 检查清单
- [ ] 使用 `npx create-video@latest` 创建项目（选 Blank + TailwindCSS + Skills）
- [ ] 安装额外依赖（lucide-react 等）
- [ ] 创建 src/scenes/ 和 public/audio/ 目录
- [ ] 验证 Studio 启动

### 操作步骤

1. **使用官方 CLI 创建项目**（用户在终端执行，需交互选择）:
```bash
npx create-video@latest <project-name>
```
按提示选择:
- 模板 → **Blank**
- TailwindCSS → **Yes**
- Skills → **Yes**（自动安装 `remotion-best-practices` 官方技能）

2. **安装额外依赖**:
```bash
cd <project-name>
npm install lucide-react
```

3. **创建目录**:
```bash
mkdir -p src/scenes public/audio
```

4. **验证**: `npm run dev` 能启动 Remotion Studio 且无报错。

### 官方脚手架生成的关键文件
| 文件 | 说明 |
|------|------|
| `remotion.config.ts` | Webpack 配置 + `@remotion/tailwind-v4` |
| `src/Root.tsx` | Composition 注册（导出名 `RemotionRoot`）|
| `src/index.ts` | `registerRoot` 入口 |
| `src/index.css` | Tailwind CSS v4 样式 |
| `package.json` | 含 `@remotion/media`、`tailwindcss 4.x` |
| `.agents/skills/` | 官方 remotion-best-practices 技能 |

### 关键 API 差异（与旧版对比）
- **Audio**: 从 `@remotion/media` 导入（不是 `remotion`）
- **Tailwind**: v4 + `@remotion/tailwind-v4`（不是 v3 + `@remotion/tailwind`）
- **Sequence**: 推荐加 `premountFor={30}` 预加载
- **Root 导出名**: `RemotionRoot`（不是 `Root`）

---

## 阶段 2: 内容规划

### 检查清单
- [ ] 与用户确认视频主题和目标受众
- [ ] 确定场景数量和每个场景的核心信息
- [ ] 为每个场景编写配音文本
- [ ] 创建 voiceover.json 文件

### 操作步骤

1. **与用户讨论**，确认以下信息:
   - 视频主题和核心卖点
   - 目标平台（抖音/视频号/通用）
   - 场景数量（推荐 3-5 个，每个 8-12 秒）
   - 配音语言和风格

2. **创建 voiceover.json**:
```json
[
  {
    "id": "scene1",
    "text": "第一个场景的配音文本",
    "voice": "zh-CN-YunxiNeural",
    "rate": "+5%"
  },
  {
    "id": "scene2",
    "text": "第二个场景的配音文本",
    "voice": "zh-CN-YunxiNeural",
    "rate": "+5%"
  }
]
```

### 常用中文语音
| Voice ID | 特点 | 适用场景 |
|----------|------|----------|
| `zh-CN-YunxiNeural` | 男声，专业感 | 科技产品、商务 |
| `zh-CN-XiaoxiaoNeural` | 女声，亲和力 | 生活类、教育 |
| `zh-CN-YunjianNeural` | 男声，浑厚 | 纪录片、庄重 |

---

## 阶段 3: 配音生成

### 检查清单
- [ ] 确认 edge-tts 已安装（`pip3 install edge-tts`）
- [ ] 确认 ffprobe 可用（`ffprobe -version`）
- [ ] 为每个场景生成 mp3 音频
- [ ] 获取每段音频的时长并计算帧数
- [ ] 记录 SCENES 配置数据

### 操作步骤

**方式一：使用脚本**（推荐）
```bash
bash scripts/generate-voiceover.sh
```

**方式二：手动逐个生成**

对 voiceover.json 中的每个条目执行:
```bash
# 生成音频
edge-tts --voice zh-CN-YunxiNeural --rate="+5%" \
  --text "配音文本" \
  --write-media public/audio/scene1.mp3

# 获取时长
ffprobe -i public/audio/scene1.mp3 \
  -show_entries format=duration -v quiet -of csv="p=0"

# 计算帧数: ceil(时长秒数 * 30) + 10（余量）
```

### 帧数计算公式
```
帧数 = Math.ceil(音频秒数 * 30) + 10
```
额外 10 帧作为场景切换的缓冲余量。

---

## 阶段 4: 场景开发

### 检查清单
- [ ] 为每个场景创建 src/scenes/SceneXXX.tsx 文件
- [ ] 每个场景包含：淡入淡出包络、背景层、内容动画
- [ ] 淡出帧范围与场景 duration 对齐
- [ ] 在 Studio 中逐个预览场景

### 场景组件标准骨架

```tsx
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  spring, interpolate,
} from "remotion";

const DURATION = 340; // ← 必须与 SCENES 中的 duration 一致

export const SceneX: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 淡入（前 15 帧）
  const sceneIn = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });
  // 淡出（最后 20 帧）— 帧数必须匹配 DURATION
  const sceneOut = interpolate(frame, [DURATION - 20, DURATION], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ opacity: sceneIn * sceneOut }}>
      {/* 背景层 */}
      <AbsoluteFill
        style={{
          background: "radial-gradient(ellipse at center, #252525 0%, #1A1A1A 100%)",
        }}
      />

      {/* 背景网格（可选） */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255,107,0,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,107,0,0.03) 1px, transparent 1px)
          `,
          backgroundSize: "40px 40px",
        }}
      />

      {/* 标题 */}
      <div className="absolute top-24 left-1/2 -translate-x-1/2 text-center">
        <h1 className="text-4xl font-bold text-white">主标题</h1>
        <p className="text-2xl mt-2" style={{ color: "#FF6B00" }}>副标题</p>
      </div>

      {/* 内容区域 — 在此添加场景特有的动画和元素 */}

      {/* 底部装饰线（可选） */}
      <div
        className="absolute bottom-0 left-0 right-0 h-1"
        style={{
          background: "linear-gradient(90deg, transparent, #FF6B00, transparent)",
          opacity: 0.5,
        }}
      />
    </AbsoluteFill>
  );
};
```

### Remotion API 参考（来自官方 remotion-best-practices）

场景开发时查阅 `references/remotion-api/` 下的规则文件，获取各 API 的最佳实践：

| 文件 | 内容 |
|------|------|
| `animations.md` | 动画基础（必须用 `useCurrentFrame()`，禁止 CSS 动画）|
| `timing.md` | `interpolate`、`spring`、`Easing` 详解 + 常用配置 |
| `sequencing.md` | `<Sequence>`、`<Series>`、`premountFor`、嵌套时序 |
| `transitions.md` | `<TransitionSeries>` 场景转场（fade/slide/wipe/flip）|
| `audio.md` | `<Audio>` 导入/裁剪/音量/变速/循环（从 `@remotion/media`）|
| `images.md` | `<Img>` 组件（禁止用原生 `<img>`）|
| `fonts.md` | Google Fonts + 本地字体加载 |
| `tailwind.md` | TailwindCSS 集成注意事项 |
| `text-animations.md` | 打字机、文字高亮动画模式 |
| `compositions.md` | Composition 定义、defaultProps、calculateMetadata |
| `display-captions.md` | TikTok 风格字幕显示 |
| `transcribe-captions.md` | 语音转字幕 |
| `charts.md` | 数据可视化图表 |
| `3d.md` | Three.js + React Three Fiber 3D 内容 |
| `lottie.md` | Lottie 动画嵌入 |
| `maps.md` | Mapbox 地图动画 |
| `parameters.md` | Zod schema 参数化视频 |

完整列表见 `references/remotion-api/` 目录。

### 动画模式速查

参考 `references/animation-patterns.md` 获取可复用的动画代码片段，包括:
- 打字机效果 Hook
- 弹性入场（spring）
- 声波可视化
- 雷达扫描
- 浮动元素
- 计数动画
- LED 跑马灯

---

## 阶段 5: 时间轴集成

### 检查清单
- [ ] 在 Main.tsx 中导入所有场景组件
- [ ] 配置 SCENES 数组（id、component、duration、audio）
- [ ] 确认 duration 之和等于 Root.tsx 的 durationInFrames
- [ ] 每个 Audio 在对应 Sequence 内

### Main.tsx 模板

```tsx
import { AbsoluteFill, Sequence, staticFile } from "remotion";
import { Audio } from "@remotion/media";
import { Scene1XXX } from "./scenes/Scene1XXX";
import { Scene2XXX } from "./scenes/Scene2XXX";
// ... 导入所有场景

const SCENES = [
  { id: "scene1", component: Scene1XXX, duration: 340, audio: "audio/scene1.mp3" },
  { id: "scene2", component: Scene2XXX, duration: 355, audio: "audio/scene2.mp3" },
  // ...
];

export const Main: React.FC = () => {
  let currentFrame = 0;

  return (
    <AbsoluteFill style={{ background: "#0A0A0A" }}>
      {SCENES.map((scene) => {
        const from = currentFrame;
        currentFrame += scene.duration;
        const Component = scene.component;

        return (
          <Sequence
            key={scene.id}
            from={from}
            durationInFrames={scene.duration}
            name={scene.id}
            premountFor={30}
          >
            <Component />
            <Audio src={staticFile(scene.audio)} volume={1} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
```

### 更新 Root.tsx

```tsx
// 注意：官方脚手架导出名是 RemotionRoot
durationInFrames: /* SCENES 所有 duration 之和 */,
width: 1920,   // 横屏默认
height: 1080,
fps: 30,
```

---

## 阶段 6: 预览与导出

### 检查清单
- [ ] Studio 预览：场景切换流畅、音画同步
- [ ] 检查淡入淡出无跳变
- [ ] 导出 MP4

### 命令

```bash
# 开发预览
npm run dev

# 导出 MP4
npx remotion render Main out/video.mp4

# 导出 GIF（可选）
npx remotion render Main out/video.gif
```

---

## 常见陷阱

### 1. 总帧数不匹配
**症状**: 视频末尾黑屏或被截断。
**原因**: Root.tsx 的 `durationInFrames` 与 SCENES 各场景 duration 之和不一致。
**修复**: 确保 `durationInFrames = SCENES.reduce((sum, s) => sum + s.duration, 0)`。

### 2. 淡出帧范围错误
**症状**: 场景结尾突然消失而非平滑淡出。
**原因**: 场景内 `sceneOut` 的 interpolate 帧范围与该场景的实际 duration 不匹配。
**修复**: `sceneOut` 的结束帧必须等于该场景在 SCENES 中的 duration 值。

### 3. lucide-react ESM 路径报错
**症状**: Webpack 编译报错，找不到 lucide-react 模块。
**原因**: 使用了旧版 lucide-react（如 0.263），其 ESM 导出路径有问题。
**修复**: 安装最新版 `npm install lucide-react@latest`。

### 4. Audio 放在 Sequence 外部
**症状**: 音频从视频开头就开始播放，不跟随场景时间。
**原因**: `<Audio>` 组件没有被包裹在对应的 `<Sequence>` 内。
**修复**: 每段 Audio 必须在其所属场景的 Sequence 内。

### 5. Audio 导入路径错误
**症状**: `Audio is not exported from 'remotion'`。
**原因**: Remotion 4.x 新项目中 Audio 已迁移到 `@remotion/media` 包。
**修复**: `import { Audio } from "@remotion/media";`（不是 `from "remotion"`）。

### 6. Tailwind v3 vs v4 混淆
**症状**: Tailwind 类名不生效或构建报错。
**原因**: `npx create-video` 生成的新项目使用 Tailwind v4 + `@remotion/tailwind-v4`，不兼容 v3 配置。
**修复**: 使用 `index.css` 中的 `@import "tailwindcss"` 语法，不再需要 `tailwind.config.js`。
