---
name: pencil-ui-design
description: 使用 Pencil MCP 创建工业级 UI 设计的完整工作流和组件库
---

# Pencil MCP 工业级 UI 设计 Skills

本 Skills 提供了一套工业级标准的 UI 设计规范，用于 Pencil MCP 设计工作。

## 快速开始

### 1. 初始化设计系统变量
在开始设计前，先设置设计系统变量：

```javascript
mcp_pencil_set_variables({
  filePath: "<your-file.pen>",
  variables: {
    // 参考 design-tokens.json 中的完整变量定义
  }
})
```

### 2. 创建可复用组件
使用 `reusable: true` 创建组件，通过 `ref` 复用：

```javascript
// 创建组件
buttonPrimary=I(document, {type: "frame", reusable: true, name: "Button/Primary", ...})

// 使用组件
btn1=I(someParent, {type: "ref", ref: "buttonPrimary"})
```

---

## 设计系统规范

### 颜色系统 (Color Tokens)

| 变量名 | Light Mode | Dark Mode | 用途 |
|--------|------------|-----------|------|
| `--background` | `#FAFAFA` | `#09090B` | 页面背景 |
| `--foreground` | `#18181B` | `#FAFAFA` | 主文本 |
| `--card` | `#FFFFFF` | `#18181B` | 卡片背景 |
| `--card-foreground` | `#18181B` | `#FAFAFA` | 卡片文本 |
| `--muted` | `#F4F4F5` | `#27272A` | 次要背景 |
| `--muted-foreground` | `#71717A` | `#A1A1AA` | 次要文本 |
| `--border` | `#E4E4E7` | `#27272A` | 边框 |
| `--primary` | `#18181B` | `#FAFAFA` | 主按钮 |
| `--primary-foreground` | `#FAFAFA` | `#18181B` | 主按钮文本 |
| `--secondary` | `#F4F4F5` | `#27272A` | 次按钮 |
| `--accent` | `#FCD34D` | `#FCD34D` | 强调色 |
| `--destructive` | `#EF4444` | `#EF4444` | 危险操作 |
| `--ring` | `#18181B` | `#D4D4D8` | Focus ring |

### 字体层级 (Typography Scale)

| 层级 | 大小 | 字重 | 行高 | 用途 |
|------|------|------|------|------|
| Display | 36px | 700 | 1.2 | 大标题 |
| H1 | 24px | 600 | 1.3 | 页面标题 |
| H2 | 20px | 600 | 1.4 | 区块标题 |
| H3 | 18px | 600 | 1.4 | 卡片标题 |
| Body | 14px | 400 | 1.5 | 正文 |
| Small | 12px | 400 | 1.4 | 辅助文本 |
| Caption | 10px | 500 | 1.3 | 标签 |

**推荐字体**: `Inter` (英文), `Noto Sans SC` (中文)

### 间距系统 (Spacing)

基于 4px 网格：
- `xs`: 4px
- `sm`: 8px  
- `md`: 12px
- `lg`: 16px
- `xl`: 24px
- `2xl`: 32px
- `3xl`: 48px

### 圆角规范 (Border Radius)

| 变量 | 值 | 用途 |
|------|-----|------|
| `radius-sm` | 6px | 小元素 (Badge, Chip) |
| `radius-md` | 8px | 按钮、输入框 |
| `radius-lg` | 12px | 卡片、弹窗 |
| `radius-xl` | 16px | 大卡片 |
| `radius-full` | 9999px | 圆形头像 |

### 阴影系统 (Shadows)

```json
{
  "shadow-sm": {
    "type": "shadow",
    "shadowType": "outer",
    "color": "#0000000D",
    "blur": 2,
    "offset": {"x": 0, "y": 1}
  },
  "shadow-md": {
    "type": "shadow",
    "shadowType": "outer",
    "color": "#0000000A",
    "blur": 6,
    "offset": {"x": 0, "y": 4}
  },
  "shadow-lg": {
    "type": "shadow",
    "shadowType": "outer",
    "color": "#00000014",
    "blur": 15,
    "offset": {"x": 0, "y": 8}
  }
}
```

---

## 组件规范

### Button 按钮

#### Primary Button
```json
{
  "type": "frame",
  "name": "Button/Primary",
  "reusable": true,
  "height": 40,
  "layout": "horizontal",
  "padding": [16, 10],
  "gap": 8,
  "alignItems": "center",
  "justifyContent": "center",
  "fill": "#18181B",
  "cornerRadius": 8,
  "effect": {
    "type": "shadow",
    "shadowType": "outer",
    "color": "#0000001A",
    "blur": 2,
    "offset": {"x": 0, "y": 1}
  }
}
// 文本: fill="#FFFFFF", fontFamily="Inter", fontSize=14, fontWeight=500
```

#### Secondary Button
```json
{
  "fill": "#F4F4F5",
  "stroke": "#E4E4E7",
  "strokeThickness": 1,
  "cornerRadius": 8
}
// 文本: fill="#18181B"
```

#### Ghost Button
```json
{
  "fill": "transparent",
  "cornerRadius": 8
}
// Hover: fill="#F4F4F5"
```

#### Destructive Button
```json
{
  "fill": "#EF4444",
  "cornerRadius": 8
}
// 文本: fill="#FFFFFF"
```

### Card 卡片

```json
{
  "type": "frame",
  "name": "Card",
  "reusable": true,
  "layout": "vertical",
  "padding": 16,
  "gap": 12,
  "fill": "#FFFFFF",
  "stroke": "#E4E4E7",
  "strokeThickness": 1,
  "cornerRadius": 12,
  "effect": {
    "type": "shadow",
    "shadowType": "outer",
    "color": "#0000000A",
    "blur": 4,
    "offset": {"x": 0, "y": 2}
  }
}
```

### Input 输入框

```json
{
  "type": "frame",
  "name": "Input",
  "reusable": true,
  "height": 40,
  "layout": "horizontal",
  "padding": [12, 10],
  "gap": 8,
  "alignItems": "center",
  "fill": "#FFFFFF",
  "stroke": "#E4E4E7",
  "strokeThickness": 1,
  "cornerRadius": 8
}
// Focus 状态: stroke="#18181B", strokeThickness=2
```

### Avatar 头像

```json
{
  "type": "frame",
  "name": "Avatar",
  "reusable": true,
  "width": 40,
  "height": 40,
  "cornerRadius": 9999,
  "fill": "#F4F4F5",
  "layout": "vertical",
  "alignItems": "center",
  "justifyContent": "center"
}
```

### Badge 徽章

```json
{
  "type": "frame",
  "name": "Badge",
  "reusable": true,
  "height": 22,
  "layout": "horizontal",
  "padding": [6, 8],
  "alignItems": "center",
  "justifyContent": "center",
  "fill": "#F4F4F5",
  "stroke": "#E4E4E7",
  "strokeThickness": 1,
  "cornerRadius": 6
}
// 文本: fontSize=10, fontWeight=500
```

---

## 图标规范

> ⚠️ **重要**: Pencil MCP 使用 `Material Symbols Rounded` 图标字体，不是 Lucide！

### 基本用法

```json
{
  "type": "icon_font",
  "iconFontFamily": "Material Symbols Rounded",
  "iconFontName": "home",
  "fontSize": 24,
  "width": 24,
  "height": 24,
  "fill": "#71717A"
}
```

> 注意: 必须同时设置 `fontSize`、`width` 和 `height` 属性，否则图标可能不显示！

### 常用图标速查表

| 类别 | 图标名称 | 用途 |
|------|----------|------|
| **导航** | `home`, `menu`, `arrow_back`, `arrow_forward`, `close` | 导航和菜单 |
| **操作** | `add`, `edit`, `delete`, `search`, `settings` | 常用操作 |
| **状态** | `check_circle`, `error`, `warning`, `info` | 状态提示 |
| **媒体** | `headphones`, `mic`, `volume_up`, `play_arrow`, `pause` | 音频视频 |
| **社交** | `person`, `group`, `share`, `favorite`, `star` | 社交功能 |
| **文件** | `folder`, `description`, `menu_book`, `article` | 文件文档 |
| **通信** | `mail`, `chat`, `notifications`, `send` | 消息通知 |
| **游戏** | `extension`, `sports_esports`, `military_tech` | 游戏奖励 |
| **学习** | `school`, `lightbulb`, `timer`, `assignment` | 教育学习 |

### 图标尺寸规范

| 尺寸 | 值 | 用途 |
|------|-----|------|
| XS | 16px | 辅助小图标、徽章内 |
| SM | 20px | 按钮内图标、列表图标 |
| MD | 24px | 标准图标、导航图标 |
| LG | 32px | 大按钮、空状态图标 |
| XL | 48px | 特殊强调、卡片主图标 |

### 完整示例

```javascript
// 创建一个带图标的按钮
iconBtn=I(parent, {
  type: "frame",
  width: 48,
  height: 48,
  layout: "vertical",
  alignItems: "center",
  justifyContent: "center",
  fill: "#1E2A2F",
  cornerRadius: 9999
})
icon=I(iconBtn, {
  type: "icon_font",
  iconFontFamily: "Material Symbols Rounded",
  iconFontName: "add",
  fontSize: 24,
  width: 24,
  height: 24,
  fill: "#FFFFFF"
})
```

---

## 图片素材处理

### 使用 G() 操作生成图片

Pencil MCP 提供 `G()` 操作来生成或获取图片，支持两种方式：

#### AI 生成图片 (推荐用于插画、头像、图标)

```javascript
// 先创建一个 frame 容器
avatar=I(parent, {type: "frame", width: 48, height: 48, cornerRadius: 9999})
// 使用 AI 生成图片填充
G(avatar, "ai", "cute cartoon boy avatar, friendly smile, warm colors, children illustration style")
```

#### Stock 图片 (推荐用于真实照片)

```javascript
// 获取 Unsplash 图片
heroImg=I(parent, {type: "frame", width: 400, height: 300})
G(heroImg, "stock", "modern office workspace laptop natural light")
```

### Prompt 编写技巧

| 类型 | 好的 Prompt | 不好的 Prompt |
|------|-------------|---------------|
| 头像 | "cute cartoon boy, round face, brown hair, warm yellow background, simple illustration" | "boy" |
| 图标 | "isometric cloud server icon, soft gradients, minimalist" | "server" |
| 背景 | "abstract gradient purple blue, soft blur, dreamy atmosphere" | "background" |

### 图片使用注意事项

1. **没有 image 节点类型** - 图片只能作为 frame/rectangle 的填充
2. **先创建容器** - 必须先用 `I()` 创建 frame，再用 `G()` 应用图片
3. **设置正确尺寸** - frame 的 width/height 决定显示尺寸
4. **圆角裁剪** - 设置 `cornerRadius: 9999` 可实现圆形图片

---

## 文本处理规范

### 防止文本溢出

当文本内容较长时，必须设置以下属性防止溢出：

```json
{
  "type": "text",
  "content": "这是一段很长的文本内容...",
  "width": "fill_container",
  "textGrowth": "fixed-width",
  "lineHeight": 1.5
}
```

### textGrowth 属性说明

| 值 | 说明 | 适用场景 |
|----|------|----------|
| `"auto"` | 文本根据内容自动调整宽度（默认） | 短文本、标签 |
| `"fixed-width"` | 固定宽度，超出自动换行 | 段落、描述文本 |
| `"truncate"` | 固定宽度，超出显示省略号 | 列表项标题 |

### 常见文本样式

```javascript
// 段落文本 (自动换行)
paragraph=I(parent, {
  type: "text",
  content: "这是一段较长的描述文本，需要自动换行显示。",
  width: "fill_container",
  textGrowth: "fixed-width",
  fontSize: 14,
  lineHeight: 1.5,
  fill: "#71717A"
})

// 标题文本 (单行)
title=I(parent, {
  type: "text",
  content: "标题文本",
  fontSize: 18,
  fontWeight: 600,
  fill: "#1E2A2F"
})
```


---

## 设计工作流

### 第一步：设置设计系统
1. 打开或创建 .pen 文件
2. 使用 `mcp_pencil_set_variables` 设置颜色变量
3. 创建可复用组件

### 第二步：创建页面结构
1. 创建页面 Frame (390x844 for iPhone)
2. 设置背景色 `#FAFAFA`
3. 使用垂直布局 `layout: "vertical"`

### 第三步：使用组件构建 UI
1. 通过 `ref` 引用可复用组件
2. 使用 `U()` 覆盖特定属性
3. 保持设计一致性

### 第四步：验证设计
1. 使用 `mcp_pencil_get_screenshot` 截图检查
2. 验证对齐、间距、颜色
3. 检查字体和图标一致性

### 第五步：迭代优化
1. 根据反馈调整细节
2. 确保无视觉错误
3. 输出最终设计稿

---

## 批量更新样式

使用 `mcp_pencil_replace_all_matching_properties` 批量替换属性：

```javascript
mcp_pencil_replace_all_matching_properties({
  filePath: "design.pen",
  parents: ["pageId1", "pageId2"],
  properties: {
    "fillColor": {"#FFF9F2": "#FAFAFA"},
    "fontFamily": {"Fredoka": "Inter"},
    "cornerRadius": {24: 12}
  }
})
```

---

## 质量检查清单

- [ ] 所有页面背景统一 (`#FAFAFA`)
- [ ] 所有卡片有边框 (`1px #E4E4E7`)
- [ ] 阴影效果一致 (blur 2-6px)
- [ ] 按钮圆角统一 (8px)
- [ ] 字体统一 (Inter)
- [ ] 图标库统一 (Lucide)
- [ ] 字体层级正确 (12/14/16/18/20/24px)
- [ ] 间距遵循 4px 网格
