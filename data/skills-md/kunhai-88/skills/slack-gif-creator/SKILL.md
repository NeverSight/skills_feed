---
name: slack-gif-creator
description: "创建针对 Slack 优化的动画 GIF 的知识与工具。提供约束、验证工具与动画概念。当用户请求为 Slack 创建动画 GIF 时使用，如「为 Slack 制作一个 X 做 Y 的 GIF」。"
license: MIT
---

# Slack GIF Creator

提供用于创建针对 Slack 优化的动画 GIF 的工具与知识。

## Slack 要求

**尺寸**：
- Emoji GIF：128x128（推荐）
- 消息 GIF：480x480

**参数**：
- FPS：10-30（更低=更小文件大小）
- 颜色：48-128（更少=更小文件大小）
- 时长：Emoji GIF 保持 3 秒以下

## 核心工作流程

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. 创建构建器
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. 生成帧
for i in range(12):
 frame = Image.new('RGB', (128, 128), (240, 248, 255))
 draw = ImageDraw.Draw(frame)
 # 使用 PIL 原语绘制动画
 builder.add_frame(frame)

# 3. 保存并优化
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## 绘制图形

**使用用户上传的图像**：如果用户上传图像，考虑他们想要：直接使用（如「动画这个」「将其拆分为帧」）或作为灵感（如「制作类似这个的东西」）。使用 PIL 加载与处理图像。

**从零绘制**：使用 PIL ImageDraw 原语：椭圆/圆形、星形/三角形/任何多边形、线条、矩形。  
**使图形看起来好**：使用更粗线条（始终设置 `width=2` 或更高）、添加视觉深度（渐变背景、多层形状）、使形状更有趣（不要只画普通圆圈—添加高光、环或图案）、注意颜色（使用鲜艳、互补颜色、添加对比度）、复杂形状（心形、雪花等）使用多边形与椭圆的组合。

## 可用工具

**GIFBuilder** (`core.gif_builder`)：组装帧并针对 Slack 优化。  
**验证器** (`core.validators`)：检查 GIF 是否满足 Slack 要求。  
**缓动函数** (`core.easing`)：平滑运动而非线性。  
**帧助手** (`core.frame_composer`)：常见需求的便利函数。

## 动画概念

**摇动/振动**：用振荡偏移对象位置。  
**脉冲/心跳**：有节奏地缩放对象大小。  
**弹跳**：对象落下并弹起。  
**旋转**：围绕中心旋转对象。  
**淡入/淡出**：逐渐出现或消失。  
**滑动**：从屏幕外移动到位置。  
**缩放**：缩放与定位以产生缩放效果。  
**爆炸/粒子爆发**：创建向外辐射的粒子。

## 优化策略

仅在要求使文件大小更小时，实现以下方法：
1. 更少帧 — 更低 FPS（10 而非 20）或更短时长
2. 更少颜色 — `num_colors=48` 而非 128
3. 更小尺寸 — 128x128 而非 480x480
4. 移除重复 — `remove_duplicates=True` 在 save()
5. Emoji 模式 — `optimize_for_emoji=True` 自动优化

## 依赖

```bash
pip install pillow imageio numpy
```
