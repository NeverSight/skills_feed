---
name: codify-design-to-code
description: >-
  将 Figma/MasterGo 设计转换为前端组件代码。通过 API 获取设计数据和截图，
  精准提取样式属性，生成高质量、可维护的任意框架组件代码。
  适用于需要将设计稿转换为可用代码的场景。
---

# Codify Dev - 设计还原

## 核心原则

> **截图看布局，骨架定边界，JSON 取样式。三者协同，缺一不可。**
> 严格遵守代码生产规范 [codegen-rules.md](references/codegen-rules.md)

---

## 理解三种数据源

| 数据源 | 告诉你什么 | 不告诉你什么 |
|--------|-----------|-------------|
| **截图** | 视觉效果、颜色感知、间距比例、整体氛围 | 精确数值、层级结构、节点 ID |
| **骨架** | 组件边界、布局方向、重复模式、节点层级 | 具体样式、颜色、字体大小 |
| **JSON** | 精确 CSS 值、节点属性、资源 ID | 视觉上下文、设计意图 |

**协同使用**：
- 截图 + 骨架 → **理解设计意图，规划组件拆分**
- 骨架 + JSON → **精确实现，确保不遗漏节点**
- 截图 + JSON → **验证还原效果**

---

## 工作流程

### Step 1. 建立视觉认知（如有截图）

用户上传截图时：
- 识别主要区域和层级关系
- 观察视觉模式（重复元素、对齐方式）
- 注意装饰细节（阴影、圆角、渐变）

> 无截图时跳过此步，直接进入 Step 2。

### Step 2. 获取结构骨架

```bash
curl -s -X POST http://127.0.0.1:13580/get_design \
  -H "Content-Type: application/json" \
  -d '{"node_id": "节点ID", "mode": "skeleton"}'
```

**骨架标记速查**：
- `[H]`/`[V]` → flex 水平/垂直布局
- `×N` → 重复 N 次，只实现模板
- `ID` → 关键节点，可单独获取
- `:` → 简单子节点，合并显示
- `ICON` → 需要下载 SVG 的图标节点
- `TEXT "..."` → 文本节点及内容预览

### Step 3. 复杂度判断 + 实现追踪（强制检查点）

**获取骨架后，必须输出以下内容：**

```markdown
## 实现追踪

**复杂度**：简单 / 复杂（层级 X，区域 N 个）
**路径**：A（整体实现）/ B（分步实现）

| # | 区域 | 节点 ID | 子节点顺序（按骨架） | 状态 |
|---|------|---------|---------------------|------|
| 1 | 区域 A | 1 | 1-1 → 1-2 → 1-3 | [ ] |
| 2 | 区域 B | 2 | 2-1 → 2-2 | [ ] |
```

**判定规则**：

| 条件 | 路径 |
|------|------|
| 层级 ≤3 且 区域 ≤2 | A：Step 4 整体实现 |
| 层级 >3 或 区域 >2 | B：**必须阅读文档并执行** [phased-workflow.md](references/phased-workflow.md) |

**路径 B 约束**：
- 禁止：判断为复杂后一次性生成所有代码
- 必须：阅读文档并执行 [phased-workflow.md](references/phased-workflow.md) 逐个组件实现，每完成一个更新状态为 [✓]

**完成条件**：所有区域状态为 [✓] 才算实现完成。

---

### Step 4. 路径 A：整体实现（仅限简单设计）

> 如果Step 3 判断为复杂，则跳过此步骤，阅读并按照[phased-workflow.md](references/phased-workflow.md)执行复杂设计。

```bash
curl -s -X POST http://127.0.0.1:13580/get_design \
  -H "Content-Type: application/json" \
  -d '{"node_id": "节点ID"}'
```

获取 JSON 后，遵循 [codegen-rules.md](references/codegen-rules.md) 生成代码。

---

### Step 5. 下载资源

> **禁止跳过此步骤**。禁止用 emoji/占位符/纯色代替图标和图片。

**资源识别**：

| 类型 | 识别方式 | 格式 |
|-----|---------|-----|
| 图标 | `type: "ICON"` | SVG |
| 图片背景 | `customStyle` 含 `url(<path-to-image>)` | PNG |
| 图片占位符 | `RECTANGLE` + `object-fit: cover`（无 url） | PNG |

**强制要求**：
- 必须下载组件代码中使用到的图标和图片背景等资源
- 对于 RECTANGLE + object-fit: cover 的隐式图片，用节点 ID 下载 PNG

**下载命令**：

```bash
node skill/scripts/download-assets.cjs --nodes '[
  {"nodeId":"123:456","outputPath":"/path/to/icon.svg","format":"svg"},
  {"nodeId":"789:012","outputPath":"/path/to/bg.png","format":"png"}
]'
```

---

### Step 6. 终态验证（强制）

> **禁止跳过**。禁止在此步骤前宣布"实现完成"。

**必须输出**：

1. **追踪表最终状态**（更新 Step 3 的表格）
2. **完成检查**：

| 检查项 | 适用路径 |
|--------|---------|
| 追踪表所有状态为 [✓] | A + B |
| 骨架关键节点均已实现（无遗漏） | A + B |
| 所有 `type: "ICON"` 已下载 | A + B |
| 所有 `url(<path-to-image>)` 已下载 | A + B |
| RECTANGLE + object-fit: cover 图片已下载 | A + B |
| 代码引用实际文件路径（无占位符） | A + B |
| 重复结构（×N）使用循环 | A + B |
| 已输出骨架理解 | 仅 B |
| 已创建实现计划 | 仅 B |
| 每个组件实现前有实现描述 | 仅 B |

3. **未完成说明**（如有 [ ]）：列出原因，询问是否继续

**验证规则**：
- 禁止：存在 [ ] 时输出"已完成"或"完成总结"
- 必须：明确告知未完成项，询问用户是否继续

---

## 参考文档

| 文档                                                | 何时读取             |
| --------------------------------------------------- | -------------------- |
| [codegen-rules.md](references/codegen-rules.md)     | **生成代码前必读**   |
| [design-schema.md](references/design-schema.md)     | 理解 JSON 结构       |
| [phased-workflow.md](references/phased-workflow.md) | **复杂设计必须先读** |
| [api.md](references/api.md)                         | API 详细参数         |

## 错误处理

| 错误码 | 处理 |
|-------|------|
| `NOT_CONNECTED` | 提示启用 Codify Dev 扩展 |
| `NO_SELECTION` | 提示选择节点 |
| `TIMEOUT` | 重试（最多 3 次） |