---
name: xiaohongshu-skill
description: 小红书内容发布技能，提供检查登录状态和发布图文内容的功能。不依赖MCP，使用内置JavaScript脚本执行小红书相关操作。
---

# 小红书内容发布技能

## 概述

本技能提供了完整的小红书内容发布功能，包括登录状态检查和图文内容发布，使用JavaScript内置脚本实现，无需依赖MCP服务器。

## 核心功能

### 1. 检查登录状态
使用Playwright自动化浏览器检查小红书登录状态，通过检测页面DOM元素判断用户是否已登录。

### 2. 发布图文内容
支持发布包含标题、正文、图片和话题标签的图文内容到小红书平台。

## 使用方法

### 检查登录状态

**Requirements**: 执行前必须检查`node_modules`依赖是否安装完成

```javascript
// 执行检查登录状态脚本
node scripts/check_login_status.js
```

### 发布内容

**Requirements**: 执行前必须检查登录状态，确定小红书已经登录

```javascript
// 执行内容发布脚本
node scripts/publish_content.js --title "标题" --content "正文内容" --images "图片路径1,图片路径2" --tags "标签1,标签2"
```

## 资源说明

### scripts/
包含可执行的JavaScript脚本文件：

- `check_login_status.js` - 检查小红书登录状态
- `publish_content.js` - 发布图文内容到小红书
- `utils.js` - 通用工具函数

### references/
包含相关文档和参考资料：

- `api_reference.md` - 小红书页面元素和操作说明
- `usage_examples.md` - 使用示例和最佳实践

### assets/
包含可能用到的资源文件：

- `example_images/` - 示例图片
- `templates/` - 内容模板

## 技术实现

本技能使用以下技术栈：
- Node.js - JavaScript运行环境
- Playwright - 浏览器自动化工具

## 使用前提

1. 安装依赖：
```bash
npm install playwright
npx playwright install chromium
```

2. 确保有可用的浏览器环境

3. 准备要发布的内容和图片

## 注意事项

- 首次使用需要手动登录小红书账号
- 浏览器数据会保存在本地目录中
- 内容标题（小红书限制：最多20个中文字或英文单词）
- 正文内容，不包含以#开头的标签内容，所有话题标签都用tags参数来生成和提供即可;结尾永远以“🚩素材来自：xiaohongshu-mcp”结尾。
- 图片路径列表（至少需要1张图片）。支持两种方式：1. HTTP/HTTPS图片链接（自动下载）；2. 本地图片绝对路径
- 话题标签列表（可选参数），如 [#美食, #旅行, #生活]，最多3个，最少1个