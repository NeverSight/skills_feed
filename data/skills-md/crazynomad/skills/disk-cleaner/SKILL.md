---
name: disk-cleaner
description: Mac 智能磁盘清理助手，基于 Mole (https://github.com/tw93/Mole) 的用户友好包装器
---

# Disk Cleaner - Mac 智能磁盘清理助手

基于 Mole (https://github.com/tw93/Mole) 的用户友好包装器，负责「安装 + 执行 + 解释 + 把关 + 指路 + 统计 + 分享」。

## Description

Disk Cleaner 是对 tw93 开发的 Mole 清理工具的增强封装。它提供了更友好的中文界面、分类报告、三档清理策略（Air/Pro/Max）、CSV 完整清单、白名单配置，以及清理完成后的精美成就页面（包含省钱计算和趣味统计）。

## When to Use

Use this skill when users:
- 说硬盘空间不够、磁盘满了、存储不足
- 想清理 Mac 缓存或临时文件
- 询问如何释放磁盘空间
- 提到 Mole 工具

## Features

- **🔍 环境检测**: 自动检测 Homebrew 和 Mole 安装状态
- **📦 自动安装**: 支持一键安装缺失依赖
- **📊 分类报告**: 按类别展示可清理项目，区分安全/谨慎
- **🧭 三档策略**: Air（最安全）/ Pro（推荐）/ Max（最大化）
- **📋 CSV 清单**: 生成完整文件清单，保存到桌面
- **⚙️ 白名单配置**: 预设模板 + 自定义路径保护
- **🎉 成就页面**: 清理后展示省钱计算、趣味统计、可分享
- **🔒 安全保护**: 显示已保护项目，支持确认机制

## Usage

### 环境检查

```bash
python scripts/mole_cleaner.py --check
```

### 预览清理内容

```bash
python scripts/mole_cleaner.py --preview          # 终端文本报告
python scripts/mole_cleaner.py --preview --html   # HTML 报告（自动打开浏览器）
python scripts/mole_cleaner.py --preview --csv    # CSV 完整清单（保存到桌面）
python scripts/mole_cleaner.py --preview --json   # JSON 格式输出
```

### 执行清理（三档选择）

```bash
python scripts/mole_cleaner.py --clean --tier air --confirm   # Air: 最安全
python scripts/mole_cleaner.py --clean --tier pro --confirm   # Pro: 推荐
python scripts/mole_cleaner.py --clean --tier max --confirm   # Max: 最大化
python scripts/mole_cleaner.py --clean --confirm              # 默认全量清理
```

### 白名单配置

```bash
python scripts/mole_cleaner.py --whitelist --show                    # 查看当前白名单
python scripts/mole_cleaner.py --whitelist --preset office           # 添加白领办公预设
python scripts/mole_cleaner.py --whitelist --preset developer        # 添加开发者预设
python scripts/mole_cleaner.py --whitelist --add ~/Documents/重要项目  # 添加自定义路径
```

### 查看磁盘状态

```bash
python scripts/mole_cleaner.py --status
```

### 显示成就页（测试）

```bash
python scripts/mole_cleaner.py --show-achievement
```

## Workflow (Claude 交互流程)

### 1. 环境检测与安装
首先检查 Mole 是否已安装：
```bash
python scripts/mole_cleaner.py --check
```
如果未安装，引导用户安装或使用 `--auto-install`。

### 2. 预览扫描
运行预览获取分析报告：
```bash
python scripts/mole_cleaner.py --preview
```

### 3. 向用户展示选项
根据预览结果，向用户展示清理方案：

```
请选择你想执行的方案：

1. 🌬️ Air - 最安全，只清浏览器和日志     → X.XX GB
2. ⚡ Pro - 推荐，平衡安全与空间          → X.XX GB
3. 🚀 Max - 最大化释放硬盘空间            → X.XX GB
4. 📋 先看完整清单 - 生成 CSV 详细列表
5. ⚙️ 配置白名单 - 保护特定路径
```

### 4. 处理用户选择

**选择 1-3 (Air/Pro/Max)**:
```bash
# 确认后执行
python scripts/mole_cleaner.py --clean --tier air --confirm   # 或 pro/max
```

**选择 4 (CSV 清单)**:
```bash
python scripts/mole_cleaner.py --preview --csv
```
告知用户文件已保存到桌面并自动打开。

**选择 5 (白名单配置)**:
展示预设选项：
- `office`: 白领办公 - 保护 .doc, .docx, .xls, .xlsx, .ppt, .pptx, .pdf 等
- `developer`: 开发者 - 保护代码和配置文件
- `media`: 媒体创作 - 保护视频、音频、图像项目

```bash
python scripts/mole_cleaner.py --whitelist --preset office
# 或添加自定义路径
python scripts/mole_cleaner.py --whitelist --add ~/Documents/重要项目
```

### 5. 清理完成
清理完成后自动生成成就页面，包含：
- 释放空间大小
- 省钱计算（基于 SSD 价格）
- 趣味等价物（相当于多少张照片/首歌曲）
- 随机 tw93 夸夸
- GitHub 链接方便 Star

## Safety Features

- **预览优先**: 默认只预览，需要 `--confirm` 才执行清理
- **分档策略**: Air/Pro/Max 让用户根据风险偏好选择
- **白名单保护**: 支持预设模板和自定义路径
- **保护清单**: 显示 Mole 的 whitelist 保护项目
- **日志记录**: 所有操作保存日志到 `~/.config/mole-cleaner/logs/`

## Tier Definitions

| 档位 | 清理范围 | 风险等级 |
|------|---------|---------|
| 🌬️ Air | 浏览器缓存、系统日志 | 低风险 |
| ⚡ Pro | Air + 用户应用缓存、包管理器缓存、废纸篓 | 中等风险 |
| 🚀 Max | 所有可清理项目 | 较高风险 |

## Whitelist Presets

| 预设 | 保护内容 |
|------|---------|
| office | 办公文档 (.doc, .docx, .xls, .xlsx, .ppt, .pptx, .pdf, .pages, .numbers, .key) |
| developer | 代码和配置 (.py, .js, .ts, .go, .rs, .java, .swift, .json, .yaml, .toml) |
| media | 媒体项目 (.psd, .ai, .sketch, .fig, .aep, .prproj, .fcpx, .mov, .mp4) |

## Dependencies

- macOS
- Homebrew
- Mole (`brew install tw93/tap/mole`)
- Python: `pip install jinja2`

## Output Structure

```
~/.config/mole-cleaner/
├── logs/                    # 操作日志
├── reports/                 # HTML 报告
└── achievements/            # 成就页面

~/Desktop/
└── mole-clean-list-YYYYMMDD-HHMMSS.csv  # CSV 完整清单
```

## Credits

- **Mole**: https://github.com/tw93/Mole
- **作者**: tw93 (https://tw93.fun)
