---
name: file-manager
description: 文件管理技能。用于创建、移动、复制、删除文件和文件夹，整理目录结构。当用户需要管理文件、整理文件夹或批量处理文件时使用。
version: 1.0.0
author: Naga Team
tags:
  - file
  - folder
  - organize
enabled: true
---

# 文件管理技能

本技能提供文件和文件夹管理能力。

## 核心功能

### 1. 文件操作
- 创建文件
- 复制/移动文件
- 重命名文件
- 删除文件

### 2. 文件夹操作
- 创建文件夹
- 列出目录内容
- 删除文件夹（递归）
- 复制文件夹

### 3. 批量处理
- 按类型分类
- 批量重命名
- 查找重复文件
- 整理下载文件夹

## 安全规则

### 禁止操作
- 系统目录（/System, /usr, /bin 等）
- 其他用户的文件
- 没有明确确认的删除操作

### 需要确认
- 删除文件前列出将被删除的内容
- 覆盖已存在的文件前提醒
- 批量操作前显示预览

## 常用操作示例

### 整理下载文件夹
```bash
# 1. 创建分类目录
mkdir -p ~/Downloads/{Documents,Images,Videos,Archives,Others}

# 2. 按扩展名移动
mv ~/Downloads/*.pdf ~/Downloads/Documents/
mv ~/Downloads/*.{jpg,png,gif} ~/Downloads/Images/
mv ~/Downloads/*.{mp4,mov,avi} ~/Downloads/Videos/
mv ~/Downloads/*.{zip,rar,7z} ~/Downloads/Archives/
```

### 批量重命名
```python
import os
from pathlib import Path

def batch_rename(directory, pattern, replacement):
    for file in Path(directory).iterdir():
        if pattern in file.name:
            new_name = file.name.replace(pattern, replacement)
            file.rename(file.parent / new_name)
```

## 输出格式

操作前显示预览：
```
即将执行以下操作：
- 移动 15 个 PDF 文件到 Documents/
- 移动 23 个图片文件到 Images/
- 跳过 3 个未知类型文件

确认执行？
```

操作后显示结果：
```
✓ 操作完成
  - 移动: 38 个文件
  - 跳过: 3 个文件
  - 错误: 0 个
```
