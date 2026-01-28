---
name: storyboard-generator
description: 根据用户的创意/故事想法，批量生成多张连贯的图片和视频，并以专业分镜表（Storyboard）的形式展示。支持单镜头重新生成、图生视频、首尾帧视频生成等高级功能。适用于短视频脚本、动画分镜、广告创意、故事可视化等场景。
---

# Storyboard Generator - 分镜图/视频生成器

基于用户的 idea 或故事描述，自动拆解为多个场景/镜头，批量生成对应图片和视频，并以分镜表形式呈现。

## 核心能力

### 1. 批量图片生成
- 根据故事拆解，一次性生成 4-12 张连贯的分镜图
- 保持系列图片风格一致性
- 支持不同宽高比适配不同镜头类型

### 2. 批量视频生成
- 基于分镜图批量生成视频片段
- 支持三种视频生成模式：
  - **文生视频**: 纯文字描述生成视频
  - **首帧图生视频**: 使用分镜图作为视频首帧
  - **首尾帧生视频**: 指定首帧和尾帧图片，生成过渡视频

### 3. 单镜头重新生成
- 对不满意的单个镜头重新生成图片或视频
- 保持与其他镜头的风格一致性
- 支持微调提示词后重新生成

## 工作流程

### Step 1: 理解用户创意
- 分析用户提供的 idea、故事、脚本或概念
- 确定整体风格基调（写实、卡通、赛博朋克、水彩等）
- 确定输出类型：纯图片分镜 / 图片+视频 / 纯视频

### Step 2: 拆解分镜
将创意拆解为 4-12 个镜头，每个镜头包含：

| 字段 | 说明 | 示例 |
|------|------|------|
| shot_id | 镜头编号 | Shot 01 |
| shot_type | 镜头类型 | 远景/全景/中景/近景/特写 |
| description | 场景描述 | 城市全景，黄昏时分 |
| prompt | 图片生成提示词 | cinematic shot, city skyline... |
| video_prompt | 视频生成提示词（可选） | camera slowly pushing in... |
| duration | 建议时长 | 3s |
| ratio | 宽高比 | 16:9 |
| camera_move | 运镜方式 | 缓慢推进/固定/摇镜 |
| transition | 转场效果 | 淡入/切/叠化 |
| notes | 备注 | 配合环境音乐 |

### Step 3: 批量生成图片
为每个镜头调用 `draw_one_image` 工具：

```python
draw_one_image(
    prompt="[风格前缀], [镜头类型], [场景描述], [风格后缀]",
    reference_image_ids=[],  # 可选参考图
    ratio="16:9"  # 根据镜头类型选择
)
```

**宽高比选择指南：**
| 镜头类型 | 推荐比例 | 适用场景 |
|---------|---------|---------|
| 远景/全景 | 16:9, 21:9 | 环境交代、大场面 |
| 中景 | 4:3, 3:2 | 人物互动、对话 |
| 近景/特写 | 1:1, 3:4 | 情绪表达、细节 |
| 竖版 | 9:16 | 手机/短视频 |

### Step 4: 批量生成视频（可选）
为需要动态效果的镜头调用 `draw_one_video` 工具：

```python
# 模式1: 文生视频
draw_one_video(
    prompt="视频描述，包含运镜和动作",
    reference_image_ids=[]
)

# 模式2: 首帧图生视频（推荐）
draw_one_video(
    prompt="视频描述",
    reference_image_ids=["首帧图片URL"]
)

# 模式3: 首尾帧生视频
draw_one_video(
    prompt="过渡描述",
    reference_image_ids=["首帧URL", "尾帧URL"]
)
```

### Step 5: 生成分镜表
使用 `template/storyboard.html` 模板展示结果。

## 单镜头重新生成

当用户对某个镜头不满意时：

1. **识别目标镜头**: 根据用户指定的镜头编号（如 "重新生成 Shot 03"）
2. **获取上下文**: 保持与前后镜头的风格一致性
3. **调整提示词**: 根据用户反馈微调
4. **重新生成**: 调用对应工具生成新内容
5. **更新分镜表**: 替换对应镜头的图片/视频

**重新生成示例对话：**
```
用户: Shot 03 的人物表情不够坚定，重新生成一下
助手: 好的，我来重新生成 Shot 03，加强人物坚定的神情...
      [调用 draw_one_image，微调 prompt 强调表情]
```

## 提示词模板

### 风格一致性前缀（选择一种风格，全程使用）

**电影感:**
```
cinematic photography, 35mm film, anamorphic lens, warm color grading, 
dramatic lighting, shallow depth of field
```

**动画风格:**
```
anime style, studio ghibli inspired, soft colors, detailed background,
cel shading, beautiful lighting
```

**赛博朋克:**
```
cyberpunk aesthetic, neon lights, rain-soaked streets, holographic displays,
dark atmosphere, high contrast, blade runner style
```

**写实摄影:**
```
professional photography, natural lighting, realistic textures,
high detail, 8k resolution, photorealistic
```

### 提示词结构
```
[风格前缀], [镜头类型 shot], [主体描述], [动作/状态], 
[环境/背景], [光线/氛围], [风格后缀]
```

## 输出格式

生成完成后，输出结构化的分镜数据：

```json
{
  "project_title": "项目标题",
  "style": "电影感/写实",
  "total_shots": 6,
  "total_duration": "15s",
  "shots": [
    {
      "shot_id": "Shot 01",
      "shot_type": "远景",
      "description": "城市全景，黄昏时分",
      "image_url": "生成的图片URL",
      "video_url": "生成的视频URL（可选）",
      "duration": "3s",
      "ratio": "16:9",
      "camera_move": "缓慢推进",
      "transition": "淡入",
      "prompt": "使用的提示词",
      "notes": "开场镜头"
    }
  ]
}
```

## 使用场景

| 场景 | 推荐配置 |
|------|---------|
| 抖音/短视频 | 6-8镜头, 9:16竖版, 图+视频 |
| 广告创意 | 8-12镜头, 16:9横版, 图+视频 |
| 动画分镜 | 8-12镜头, 16:9, 纯图片 |
| 故事绘本 | 6-10镜头, 1:1或4:3, 纯图片 |
| 游戏CG | 6-8镜头, 21:9超宽, 图+视频 |
| 音乐MV | 10-15镜头, 16:9, 图+视频 |

## 注意事项

1. 单次建议不超过 12 个镜头，避免生成时间过长
2. 视频生成较慢（约30-60秒/个），可先生成全部图片再按需生成视频
3. 首尾帧生视频时，两帧图片风格和内容需要有合理的过渡关系
4. 重新生成时保持风格前缀一致，仅调整具体描述
5. 如需角色高度一致，建议用户提供参考图

## 常见问题与踩坑记录

### 1. HTML 模板中 JavaScript 字符串引号问题

**问题现象**: 分镜表 HTML 页面只显示标题，镜头卡片不渲染。

**原因**: 在 JavaScript 的 `storyboardData` 对象中，`description` 或 `dialogue` 字段包含中文双引号 `"..."` 时，会破坏 JS 字符串语法，导致整个脚本解析失败。

**错误示例**:
```javascript
{ description: "上面写着"发愿"。", ... }  // ❌ 中文引号破坏字符串
```

**正确做法**:
```javascript
{ description: "上面写着「发愿」。", ... }  // ✅ 使用中文书名括号
{ description: "上面写着'发愿'。", ... }   // ✅ 使用单引号
{ description: "上面写着\"发愿\"。", ... } // ✅ 转义双引号
```

**排查方法**:
```bash
# 使用 Node.js 检查 JS 语法
node -e "
const fs = require('fs');
const html = fs.readFileSync('storyboard.html', 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (scriptMatch) {
    try {
        new Function(scriptMatch[1]);
        console.log('JavaScript syntax OK');
    } catch(e) {
        console.log('JavaScript error:', e.message);
    }
}
"
```

### 2. 占位图片服务

当实际图片尚未生成时，可使用 `picsum.photos` 作为占位图：
```html
<img src="https://picsum.photos/seed/shot${shot_id}/640/360" alt="Shot">
```
- `seed/shot${shot_id}` 确保同一镜头每次显示相同的随机图片
- 可添加 `filter: grayscale(100%)` 使占位图呈现黑白效果，与未生成状态区分
