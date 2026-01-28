---
name: brand-guidelines
description: "将 Anthropic 官方品牌颜色与排版应用于任何可能受益于 Anthropic 外观与感觉的工件。当品牌颜色或样式指南、视觉格式或公司设计标准适用时使用。"
license: MIT
---

# Anthropic 品牌样式

访问 Anthropic 官方品牌身份与样式资源。

**关键词**：branding、corporate identity、visual identity、post-processing、styling、brand colors、typography、Anthropic brand、visual formatting、visual design

## 品牌指南

### 颜色

**主色**：
- 深色：`#141413` — 主文本与深色背景
- 浅色：`#faf9f5` — 浅色背景与深色上的文本
- 中灰：`#b0aea5` — 次要元素
- 浅灰：`#e8e6dc` — 微妙背景

**强调色**：
- 橙色：`#d97757` — 主强调
- 蓝色：`#6a9bcc` — 次强调
- 绿色：`#788c5d` — 第三强调

### 排版

- **标题**：Poppins（带 Arial 后备）
- **正文**：Lora（带 Georgia 后备）
- **注意**：字体应在环境中预安装以获得最佳效果

## 功能

### 智能字体应用

- 将 Poppins 字体应用于标题（24pt 及以上）
- 将 Lora 字体应用于正文
- 如自定义字体不可用自动后备到 Arial/Georgia
- 在所有系统上保持可读性

### 文本样式

- 标题（24pt+）：Poppins 字体
- 正文：Lora 字体
- 基于背景的智能颜色选择
- 保持文本层级与格式

### 形状与强调颜色

- 非文本形状使用强调颜色
- 循环使用橙色、蓝色与绿色强调
- 在保持品牌的同时保持视觉趣味

## 技术细节

### 字体管理

- 使用系统安装的 Poppins 与 Lora 字体（如可用）
- 提供自动后备到 Arial（标题）与 Georgia（正文）
- 无需字体安装—与现有系统字体工作
- 为获得最佳效果，在环境中预安装 Poppins 与 Lora 字体

### 颜色应用

- 使用 RGB 颜色值进行精确品牌匹配
- 通过 python-pptx 的 RGBColor 类应用
- 在不同系统上保持颜色保真度
