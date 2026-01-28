---
name: slidev-ppt
description: 使用 Slidev 快速创建专业演示文稿的技能。支持多种预设主题（商务、技术、创意、极简）、自动生成大纲、启动开发服务器预览、导出 PDF/PPTX。当用户需要：1) 创建 PPT 演示文稿；2) 使用 Markdown 制作幻灯片；3) 技术分享或产品发布；4) 导出演示文稿为 PDF 或其他格式时使用此技能。
---

# Slidev PPT 制作技能

## Overview

此技能帮助用户使用 Slidev（基于 Markdown 的演示文稿工具）快速创建专业的 PPT。Slidev 使用 Markdown 语法，支持代码高亮、图表、Vue 组件等强大功能，特别适合技术分享、产品发布和商务演示。

## 快速开始

### 步骤 1: 确定需求和选择主题

询问用户以下问题以确定最佳方案：

1. **演示目的**: 技术分享、产品发布、商务报告、创意展示？
2. **目标受众**: 开发者、管理层、客户、大众？
3. **内容类型**: 代码演示、数据展示、图文结合？
4. **输出需求**: 仅预览、导出 PDF、导出 PPTX、全部？

根据用户回答选择合适的预设主题：
- **business-theme** (`assets/business-theme/`): 产品发布、商业报告、季度总结
- **tech-theme** (`assets/tech-theme/`): 技术分享、架构设计、代码演示
- **creative-theme** (`assets/creative-theme/`): 设计展示、作品集、创意提案
- **minimal-theme** (`assets/minimal-theme/`): 简洁演示、快速原型

### 步骤 2: 收集内容信息

收集创建演示文稿所需的关键信息：

**必需信息**:
- 标题 (title)
- 副标题 (subtitle)
- 演讲者 (presenter)
- 日期 (date)

**主题相关**:
- **商务主题**: 公司、职位、关键点、成果、下一步计划
- **技术主题**: 技术栈、问题背景、技术方案、代码示例、性能指标
- **创意主题**: 灵感来源、设计理念、视觉元素、作品图片
- **极简主题**: 章节标题、内容要点、关键概念

### 步骤 3: 创建演示文稿

使用 `scripts/create_presentation.py` 从模板创建：

```bash
python scripts/create_presentation.py <主题名称> <输出目录> [变量...]
```

示例：
```bash
python scripts/create_presentation.py business-theme ./presentation \\
  title="2024 Q4 产品发布会" \\
  subtitle="全新功能升级" \\
  presenter="张三" \\
  position="产品经理" \\
  company="ABC 科技" \\
  date="2024-12-15"
```

### 步骤 4: 启动开发服务器（自动预览）

使用 `scripts/start_dev_server.sh` 启动实时预览：

```bash
cd <输出目录>
bash /path/to/slidev-ppt/scripts/start_dev_server.sh slides.md
```

或直接使用命令：
```bash
npx slidev slides.md --open
```

浏览器会自动打开 http://localhost:3030

**开发服务器特性**:
- 实时预览：编辑 `slides.md` 后自动刷新
- 幻灯片导航：空格键、箭头键、点击翻页
- 绘图模式：按 `D` 进入，可在幻灯片上绘制
- 演讲者模式：按 `G` 查看演讲者备注和下一页预览
- 全屏模式：按 `F` 全屏演示

### 步骤 5: 导出演示文稿

用户可选择以下方式导出：

**导出为 PDF**（推荐用于分享和打印）:
```bash
bash /path/to/slidev-ppt/scripts/export_pdf.sh slides.md dist
```

**导出为 PPTX**（推荐用于进一步编辑）:
```bash
bash /path/to/slidev-ppt/scripts/export_pptx.sh slides.md dist
```

**导出为 PNG**（推荐用于制作图片）:
```bash
npx slidev export slides.md --format png --output dist
```

**导出特定页面范围**:
```bash
npx slidev export slides.md --range 1,3-5,8 --output dist
```

## 工作流程决策树

```
用户请求创建 PPT
    │
    ├─ 是否已有内容？
    │   ├─ 是 → 使用模板快速生成
    │   │         ├─ 商务内容 → business-theme
    │   │         ├─ 技术分享 → tech-theme
    │   │         ├─ 创意设计 → creative-theme
    │   │         └─ 简洁演示 → minimal-theme
    │   │
    │   └─ 否 → 从零开始
    │             1. 收集内容大纲
    │             2. 确定内容类型
    │             3. 推荐合适主题
    │             4. 生成演示文稿
    │
    ├─ 是否需要自定义？
    │   ├─ 否 → 使用预设主题
    │   └─ 是 → 参考主题定制指南（见下方）
    │
    └─ 导出需求？
        ├─ 仅预览 → 启动开发服务器
        ├─ PDF → 使用 export_pdf.sh
        ├─ PPTX → 使用 export_pptx.sh
        └─ 全部 → 先预览，再导出多种格式
```

## 主题选择指南

### Business Theme（商务主题）

**适用场景**:
- 产品发布会
- 商业计划书
- 季度/年度报告
- 项目进度汇报
- 商务提案

**设计特点**:
- 专业、正式
- 双栏布局（目录 + 详情）
- 支持数据图表
- 包含成果和计划总结

**必需变量**:
```python
title, subtitle, presenter, position, company, date
slide1_title, slide1_content, point1, point2
# ... 其他内容变量
```

**模板位置**: `assets/business-theme/slides.md`

### Tech Theme（技术主题）

**适用场景**:
- 技术分享会
- 代码演示
- 架构设计讲解
- 技术方案评审
- 开发经验总结

**设计特点**:
- 使用 Apple Basic 主题
- 代码高亮（shiki）
- 支持架构图（Mermaid）
- 技术栈展示
- 性能优化对比

**必需变量**:
```python
title, subtitle, presenter, position, date
tech_stack, current_situation, challenges, goals
code_title, code_example, code_explanation
# ... 其他技术变量
```

**模板位置**: `assets/tech-theme/slides.md`

### Creative Theme（创意主题）

**适用场景**:
- 设计作品展示
- 创意提案
- 视觉设计分享
- 品牌设计方案
- 艺术作品集

**设计特点**:
- 使用 Seriph 主题
- 优雅的 Serif 字体
- 图片展示布局
- 配色方案展示
- 思维导图支持

**必需变量**:
```python
title, subtitle, cover_image, presenter
inspiration_intro, core_concept, design_philosophy
color_scheme, font_choice, graphic_elements
work1_image, work1_description, work2_image, work2_description
# ... 其他创意变量
```

**模板位置**: `assets/creative-theme/slides.md`

### Minimal Theme（极简主题）

**适用场景**:
- 简洁的演示文稿
- 快速原型
- 讲座和教学
- 概念介绍
- 轻量级分享

**设计特点**:
- 极简设计
- 清晰的文本布局
- 基础列表展示
- 简单的图表支持

**必需变量**:
```python
title, subtitle, presenter, date
section1, section1_id, section1_content
section2, section2_id, section2_intro, key_concept
# ... 其他章节变量
```

**模板位置**: `assets/minimal-theme/slides.md`

## 高级定制

### 自定义样式

如果用户需要自定义样式，参考以下资源：

**参考文档**:
- `references/syntax.md` - Slidev 语法完整参考
- `references/themes.md` - 主题定制和配色方案
- `references/quickstart.md` - 快速入门指南

**自定义方法**:

1. **修改颜色方案**: 编辑 `slides.md` 的 frontmatter
```yaml
---
theme: default
primary: '#5c7cfa'
secondary: '#6666ff'
---
```

2. **创建自定义布局**: 在项目目录创建 `layouts/` 文件夹
```vue
<!-- layouts/custom.vue -->
<template>
  <div class="slide-custom-layout">
    <slot />
  </div>
</template>
```

3. **添加自定义组件**: 在项目目录创建 `components/` 文件夹
```vue
<!-- components/InfoCard.vue -->
<template>
  <div class="info-card border rounded-lg p-6">
    <h3>{{ title }}</h3>
    <p>{{ content }}</p>
  </div>
</template>
```

### 常用语法速查

| 功能 | 语法 | 示例 |
|------|------|------|
| 新幻灯片 | `---` | `---\n# 新页面` |
| 代码块 | <code>\`\`\`lang</code> | <code>\`\`\`typescript\nconsole.log()\n\`\`\`</code> |
| 高亮行 | <code>\`\`\`ts {1-2}</code> | 高亮第 1-2 行 |
| 双栏布局 | `layout: two-cols` | 见各主题模板 |
| 点击显示 | `<v-clicks>` | 逐项显示内容 |
| 图表 | <code>\`\`\`mermaid</code> | 流程图、时序图等 |
| LaTeX | `$formula$` | `$\sum_{i=1}^n x_i$` |
| 图标 | `<carbon:user />` | 使用 Carbon 图标 |
| 目录 | `<Toc />` | 自动生成目录 |

完整语法见 `references/syntax.md`

## 故障排除

### 问题: Slidev 未安装

**解决**:
```bash
npm init slidev
# 或
npm install @slidev/cli @slidev/theme-default
```

### 问题: 模板变量未替换

**原因**: 变量名不匹配或格式错误

**解决**: 确保变量格式为 `key=value`，且 key 与模板中的 `{{key}}` 匹配

```bash
# 正确
python create_presentation.py business-theme ./out title="标题"

# 错误
python create_presentation.py business-theme ./out 标题
```

### 问题: 导出 PDF 失败

**原因**: 可能是缺少依赖或权限问题

**解决**:
```bash
# 检查 Node.js 版本
node --version  # 应 >= 14.0

# 重新安装依赖
npm install

# 使用 sudo（Linux/Mac）
sudo npm install -g @slidev/cli
```

### 问题: 图片不显示

**解决**:
- 使用绝对路径或放在 `public/` 目录
- 检查文件路径大小写（Linux 区分大小写）
- 使用网络图片确保可访问

### 问题: 中文显示异常

**解决**:
```yaml
---
fonts:
  sans: 'Noto Sans SC'
  serif: 'Noto Serif SC'
webfontUrls:
  - 'https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap'
---
```

## 最佳实践

### 内容组织

1. **遵循"每页一观点"原则**: 每个幻灯片只讲一个核心观点
2. **使用渐进显示**: 用 `<v-clicks>` 控制信息流，避免一次性展示过多内容
3. **代码示例优化**:
   - 限制代码长度（< 20 行）
   - 使用高亮突出关键行
   - 添加注释说明

### 设计原则

1. **一致性**: 保持配色、字体、间距的一致性
2. **对比度**: 确保文本和背景有足够对比度
3. **留白**: 避免内容过于拥挤，适当留白
4. **对齐**: 保持元素对齐，使用网格布局

### 演示技巧

1. **排练**: 使用演讲者模式（按 `G`）进行排练
2. **时间控制**: 每页幻灯片约 2-3 分钟
3. **互动**: 使用绘图模式（按 `D`）进行标注
4. **备用**: 导出 PDF 作为备份，防止技术故障

## 示例场景

### 场景 1: 技术分享 - Vue3 最佳实践

```bash
# 使用技术主题
python scripts/create_presentation.py tech-theme ./vue3-talk \\
  title="Vue3 最佳实践" \\
  subtitle="提升开发效率和代码质量" \\
  presenter="张三" \\
  position="前端架构师" \\
  date="2024-12-20" \\
  tech_stack="Vue3, TypeScript, Vite" \\
  current_situation="项目迁移到 Vue3 后遇到的问题" \\
  challenges="性能优化、代码组织、类型安全" \\
  goals="建立统一的开发规范和最佳实践"

# 启动预览
cd vue3-talk
npx slidev slides.md --open

# 导出 PDF
npx slidev export slides.md --output dist
```

### 场景 2: 产品发布会 - 新功能介绍

```bash
# 使用商务主题
python scripts/create_presentation.py business-theme ./product-launch \\
  title="ABC 产品 v2.0 发布会" \\
  subtitle="全新功能，全新体验" \\
  presenter="李四" \\
  position="产品总监" \\
  company="ABC 科技" \\
  date="2024-12-25" \\
  point1="智能推荐系统上线" \\
  point2="性能提升 300%" \\
  achievement1="用户增长 150%" \\
  achievement2="收入增长 200%"

cd product-launch
npx slidev slides.md --open
```

### 场景 3: 设计作品集 - UI/UX 设计展示

```bash
# 使用创意主题
python scripts/create_presentation.py creative-theme ./design-portfolio \\
  title="2024 设计作品集" \\
  subtitle="UI/UX 设计案例精选" \\
  presenter="王五" \\
  cover_image="./public/cover.jpg" \\
  core_concept="简约而不简单" \\
  design_philosophy="用户至上，体验优先" \\
  color_scheme="主色: #5c7cfa, 辅色: #6666ff" \\
  work1_image="./public/work1.jpg" \\
  work1_description="电商 APP 改版设计" \\
  work2_image="./public/work2.jpg" \\
  work2_description="企业后台系统设计"

cd design-portfolio
npx slidev slides.md --open
```

## 资源

### scripts/

可执行脚本，用于创建、启动和导出演示文稿：

- **create_presentation.py** - 从模板创建新的演示文稿
  - 用法: `python create_presentation.py <主题> <目录> [变量...]`
  - 示例: 见上方示例场景

- **start_dev_server.sh** - 启动 Slidev 开发服务器
  - 用法: `bash start_dev_server.sh <slides.md>`
  - 功能: 实时预览、自动刷新

- **export_pdf.sh** - 导出为 PDF
  - 用法: `bash export_pdf.sh <slides.md> [输出目录]`
  - 功能: 生成高质量 PDF 文件

- **export_pptx.sh** - 导出为 PPTX
  - 用法: `bash export_pptx.sh <slides.md> [输出目录]`
  - 功能: 生成可编辑的 PowerPoint 文件

### assets/

预设主题模板，包含完整的 slides.md 文件：

- **business-theme/** - 商务风格模板
  - 适用于: 产品发布、商业报告、项目汇报
  - 特点: 专业、正式、数据图表支持

- **tech-theme/** - 技术分享模板
  - 适用于: 技术分享、代码演示、架构讲解
  - 特点: 代码高亮、架构图、技术栈展示

- **creative-theme/** - 创意设计模板
  - 适用于: 设计展示、作品集、创意提案
  - 特点: 优雅字体、图片展示、配色方案

- **minimal-theme/** - 极简风格模板
  - 适用于: 简洁演示、快速原型、教学讲座
  - 特点: 极简设计、清晰布局、基础图表

### references/

详细参考文档，供深入学习使用：

- **syntax.md** - Slidev 语法完整参考
  - 内容: 基本语法、布局系统、代码块、图表、交互元素
  - 使用: 需要了解详细语法时查阅

- **themes.md** - 主题定制和配色方案
  - 内容: 内置主题、颜色方案、字体定制、样式自定义
  - 使用: 需要自定义主题和样式时查阅

- **quickstart.md** - 快速入门指南
  - 内容: 安装、基本使用、文件结构、常见问题
  - 使用: 初次使用 Slidev 时阅读

**加载策略**: 当用户需要深入了解语法、主题定制或遇到问题时，按需加载对应的参考文档。

## 相关资源

**官方文档**:
- [Slidev 官方文档](https://cn.sli.dev/)
- [语法详解](https://cn.sli.dev/guide/syntax.html)
- [主题画廊](https://cn.sli.dev/themes/gallery.html)
- [导出功能](https://cn.sli.dev/guide/exporting.html)

**社区资源**:
- [GitHub 仓库](https://github.com/slidevjs/slidev)
- [示例集合](https://cn.sli.dev/showcases.html)
- [社区讨论](https://github.com/slidevjs/slidev/discussions)
