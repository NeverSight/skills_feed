---
name: web-artifacts-builder
description: "使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）创建复杂的多组件 claude.ai HTML 工件的工具套件。用于需要状态管理、路由或 shadcn/ui 组件的复杂工件—非简单单文件 HTML/JSX 工件。"
license: MIT
---

# Web Artifacts Builder

构建强大的前端 claude.ai 工件，遵循以下步骤：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码开发工件
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包为单个 HTML 文件
4. 向用户显示工件
5. （可选）测试工件

**技术栈**：React 18 + TypeScript + Vite + Parcel（打包）+ Tailwind CSS + shadcn/ui

## 设计与样式指南

**非常重要**：为避免常被称为「AI 垃圾」的内容，避免使用过度居中布局、紫色渐变、统一圆角与 Inter 字体。

## 快速开始

### 步骤 1：初始化项目

运行初始化脚本创建新 React 项目：
```bash
bash scripts/init-artifact.sh 
cd 
```

这创建完全配置的项目，包含：
- ✅ React + TypeScript（通过 Vite）
- ✅ Tailwind CSS 3.4.1 与 shadcn/ui 主题系统
- ✅ 路径别名（`@/`）配置
- ✅ 40+ shadcn/ui 组件预安装
- ✅ 所有 Radix UI 依赖包含
- ✅ Parcel 配置用于打包（通过 .parcelrc）
- ✅ Node 18+ 兼容性（自动检测并固定 Vite 版本）

### 步骤 2：开发工件

编辑生成的文件以构建工件。见下方「常见开发任务」获取指导。

### 步骤 3：打包为单个 HTML 文件

将 React 应用打包为单个 HTML 工件：
```bash
bash scripts/bundle-artifact.sh
```

这创建 `bundle.html` — 包含所有 JavaScript、CSS 与依赖内联的自包含工件。此文件可直接在 Claude 对话中作为工件分享。

**要求**：项目必须在根目录有 `index.html`。

**脚本作用**：
- 安装打包依赖（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建带路径别名支持的 `.parcelrc` 配置
- 使用 Parcel 构建（无源映射）
- 使用 html-inline 将所有资源内联到单个 HTML

### 步骤 4：与用户分享工件

最后，在对话中分享打包的 HTML 文件，以便他们可以将其作为工件查看。

### 步骤 5：测试/可视化工件（可选）

注意：这是完全可选步骤。仅在必要时或请求时执行。

要测试/可视化工件，使用可用工具（包括其他技能或内置工具如 Playwright 或 Puppeteer）。通常，避免提前测试工件，因为它在请求与可以看到完成工件之间增加延迟。如果请求或出现问题，在呈现工件后稍后测试。

## 参考

- **shadcn/ui 组件**：https://ui.shadcn.com/docs/components
