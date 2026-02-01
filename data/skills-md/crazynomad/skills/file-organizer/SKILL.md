---
name: file-organizer
description: Mac 智能文件整理助手，专注整理下载文件夹中的办公文档，避免误移动代码文件
---

# File Organizer - Mac 智能文件整理助手

帮助用户整理下载文件夹中散落的办公文档，支持手动整理（智能文件夹）和自动整理两种模式，并与 disk-cleaner 配合保护重要文件。

## When to Use

Use this skill when users:
- 想整理电脑上的文件
- 下载文件夹太乱想整理
- 清理磁盘前想先把重要文件整理好
- 截图太多想归类
- 想找出占空间的大文件

## Features

- **📥 默认整理下载文件夹** - 避免误动其他目录
- **🖐️ 手动模式** - 创建 macOS 智能文件夹，用户自己整理
- **🤖 自动模式** - 自动扫描并分类文件
- **📸 截图整理** - 按月份归类截图
- **💾 大文件发现** - 只显示明确用途的文件（PDF、PPT、视频等）
- **🔒 白名单机制** - 排除代码目录，保护项目文件

## File Categories

专注办公文档，避免误移动代码文件：

| 分类 | 扩展名 |
|------|--------|
| 📊 演示文稿 | .ppt, .pptx, .key |
| 📝 文档 | .doc, .docx, .pages, .rtf |
| 📈 表格 | .xls, .xlsx, .numbers, .csv |
| 📄 PDF | .pdf |
| 🖼️ 图片 | .jpg, .png, .gif, .webp, .heic |
| 🎬 视频 | .mp4, .mov, .avi, .mkv |
| 🎵 音频 | .mp3, .wav, .flac, .m4a |
| 📦 压缩包 | .zip, .rar, .7z, .dmg |
| 📚 电子书 | .epub, .mobi, .azw3 |

## Excluded Directories

类似 Mole 的白名单机制，自动排除：

- 代码目录: `.git`, `node_modules`, `venv`, `__pycache__`
- 系统目录: `Library`, `.Trash`
- IDE 配置: `.idea`, `.vscode`
- 构建产物: `build`, `dist`, `DerivedData`

## Usage

### 手动模式（创建智能文件夹）

```bash
# 默认整理下载文件夹
python scripts/file_organizer.py --manual

# 整理文档文件夹
python scripts/file_organizer.py --manual --scope documents

# 整理整个用户目录
python scripts/file_organizer.py --manual --scope home
```

### 自动模式

```bash
# 自动整理下载文件夹
python scripts/file_organizer.py --auto

# 预览模式（不实际移动）
python scripts/file_organizer.py --auto --dry-run

# 只整理最近 30 天的文件
python scripts/file_organizer.py --auto --days 30
```

### 截图整理

```bash
# 查看截图
python scripts/file_organizer.py --screenshots

# 自动整理截图（按月份）
python scripts/file_organizer.py --screenshots --auto
```

### 大文件发现

```bash
# 查找大于 100MB 的文件
python scripts/file_organizer.py --large-files

# 查找大于 500MB 的文件
python scripts/file_organizer.py --large-files --min-size 500
```

### 查看状态

```bash
python scripts/file_organizer.py --status
```

## Output Structure

### 手动模式

```
~/Desktop/待整理/
├── 📊 演示文稿.savedSearch
├── 📝 文档.savedSearch
├── 📈 表格.savedSearch
├── 📄 PDF.savedSearch
├── 🖼️ 图片.savedSearch
├── 🎬 视频.savedSearch
├── 🎵 音频.savedSearch
├── 📦 压缩包.savedSearch
├── 📚 电子书.savedSearch
└── 💾 大文件 (>100MB).savedSearch
```

### 自动模式

```
~/Desktop/已整理文件-20240125/
├── 演示文稿/
├── 文档/
├── 表格/
├── PDF/
├── 图片/
├── 视频/
├── 音频/
├── 压缩包/
└── 电子书/
```

## Integration with disk-cleaner

自动模式整理后的文件夹路径会自动写入 `~/.config/mole/whitelist.txt`，确保这些文件不会被 disk-cleaner 清理。

## Dependencies

- macOS (使用 Spotlight 和智能文件夹功能)
- Python 3.8+

## Credits

- 与 [disk-cleaner](../disk-cleaner/) 配合使用
- 灵感来自 macOS 智能文件夹功能
