---
name: remotion
description: 动画逻辑图工厂。用户描述想要的动画（ASCII 草图或文字），自动生成 Remotion 代码并渲染为 GIF。当用户提到动画、逻辑图、GIF、Remotion 时触发。
---

# Remotion 动画逻辑图 Skill

## 核心工作流

```
检测环境 → 用户描述 → 匹配现有模板 → 适配/新建 → 注册 → 渲染 GIF → 导出
```

**核心原则：优先复用现有模板，不要从零新建。**

用户不需要搭环境、不需要懂代码。Skill 自带完整运行环境。

## 目录结构

```
skills/remotion/
├── SKILL.md              # 本文件
├── package.json           # 依赖配置（已安装）
├── tsconfig.json          # TypeScript 配置
├── node_modules/          # 依赖（已安装）
├── src/
│   └── index.tsx          # 入口文件（注册所有 Composition）
├── 案例库/                 # 现有模板（可直接渲染）
│   ├── 循环流程图/
│   ├── 莫兰迪卡片网格/
│   ├── 可爱流程图/
│   ├── 对比流程图/
│   ├── 技能流程图/
│   ├── 终端流程图/
│   ├── 人物卡片/
│   ├── 时间线/
│   ├── 代码展示/
│   └── 饼图/
├── 脚本库/
│   ├── check-env.sh       # 环境自检
│   └── init-project.sh    # 初始化（已废弃，环境已内置）
└── 设计规范/
    └── 动画设计规范.md
```

## 执行步骤

当用户要求生成动画逻辑图时，按以下步骤执行：

### 第 1 步：检测 Remotion 环境

检查 `skills/remotion/` 目录是否存在：

- **不存在** → 自动克隆仓库到 skills 目录下，然后 `npm install`
- **存在但无 node_modules** → 自动 `npm install`
- **一切就绪** → 进入下一步

```bash
# 检查目录是否存在
ls skills/remotion/package.json

# 如果不存在，克隆仓库
git clone https://github.com/Ceeon/remotion-skill.git skills/remotion
cd skills/remotion && npm install

# 如果存在但无 node_modules
cd skills/remotion && npm install

# 一切就绪，检查环境
bash 脚本库/check-env.sh
```

### 第 2 步：理解用户需求

用户会提供以下任意一种输入：

- **ASCII 草图**：用文字画出大概的布局和逻辑
- **文字描述**：自然语言描述想要的动画
- **参考案例**：指定案例库中的某个模板

### 第 3 步：匹配现有模板（优先）

**先看案例库，不要直接新建。**

1. 浏览 `案例库/` 下所有子目录，读取每个模板的 `.tsx` 文件
2. 找到与用户需求最接近的模板
3. 判断匹配度：
   - **高匹配**（类型相同，只需改文字/颜色）→ 复制模板，修改内容
   - **中匹配**（类型相近，需调整布局/动画）→ 基于模板改造
   - **无匹配**（案例库没有类似的）→ 才从零新建

```
案例库现有模板：
├── 循环流程图/     → 循环关系、闭环流程
├── 莫兰迪卡片网格/ → 多卡片并列展示
├── 可爱流程图/     → 轻松风格的步骤图
├── 对比流程图/     → A vs B 对比
├── 技能流程图/     → 技能/能力展示
├── 终端流程图/     → 代码/终端风格
├── 人物卡片/       → 人物介绍
├── 时间线/         → 时间轴
├── 代码展示/       → 代码演示
└── 饼图/           → 数据可视化
```

### 第 4 步：生成/适配组件代码

基于模板适配或从零新建，在 `案例库/` 下创建新目录，写入 `.tsx` 组件文件。

**代码规范：**
- 画布尺寸：800×600（默认）
- fps：30
- 使用 `frame % totalFrames` 实现循环
- 动画使用 `spring()` 弹性效果
- 动画结尾留 60 帧静止缓冲（防闪烁）
- 字体：`PingFang SC, Microsoft YaHei, sans-serif`
- 入场动画：依次弹入，每个元素间隔 30-40 帧

**必须导入：**
```tsx
import { useCurrentFrame, useVideoConfig, interpolate, AbsoluteFill, spring } from 'remotion';
```

### 第 5 步：注册 Composition

将新组件添加到 `src/index.tsx`：

```tsx
import { NewComponent } from '../案例库/新组件/NewComponent';

// 在 Root 组件的 <> 内添加：
<Composition
  id="new-component"
  durationInFrames={240}
  fps={30}
  width={800}
  height={600}
  component={NewComponent}
/>
```

### 第 6 步：渲染 GIF

```bash
cd /path/to/skills/remotion
npx remotion render src/index.tsx <composition-id> "/目标路径/文件名.gif" --codec=gif --every-nth-frame=2
```

- `--every-nth-frame=2` 相当于 15fps，体积和流畅度的最佳平衡
- 输出路径由用户指定（通常是文章所在目录）

## 渲染已有模板

案例库中的模板可以直接渲染，无需额外操作：

```bash
# 查看可用 composition
grep 'id="' src/index.tsx

# 渲染指定模板
npx remotion render src/index.tsx cycle-flowchart /输出路径/循环流程图.gif --codec=gif --every-nth-frame=2
npx remotion render src/index.tsx morandi-grid /输出路径/莫兰迪卡片网格.gif --codec=gif --every-nth-frame=2
npx remotion render src/index.tsx cute-flowchart /输出路径/可爱流程图.gif --codec=gif --every-nth-frame=2
```

## 设计规范速查

| 项目 | 默认值 |
|------|--------|
| 画布 | 800×600 |
| fps | 30 |
| 背景 | `#fff` 或 `#f5f0eb`（莫兰迪） |
| 入场间隔 | 30-40 帧/元素 |
| 静止缓冲 | 尾部 60 帧 |
| 弹性动画 | `spring({ damping: 8-12 })` |
| 字体 | PingFang SC |
| 节点圆角 | 50%（圆）或 20px（卡片） |

## 触发条件

当用户提到以下内容时触发此 skill：
- 动画逻辑图、动态配图、GIF 配图
- Remotion 渲染
- 把 ASCII 变成动画
- 渲染模板、导出 GIF
