---
name: dreamina-batch-management
description: Dreamina 图片生成批次管理规范，包含文件夹组织和文档记录
---

# Dreamina 批次管理规范

## 操作原则

### 1. 直接执行
- 生成和下载图片的 curl 指令**直接执行**
- **无需用户确认**，提高效率
- 包括 API 调用、轮询查询、文件下载

### 2. 分批管理
- 每次生成任务创建独立文件夹
- 按时间和主题分组组织
- 避免文件混乱堆积

## 文件夹结构

### 命名规范
```
batch-YYYYMMDD-HHmm-描述/
├── README.md           # 批次说明文档
├── image1.png         # 生成的图片文件
├── image2.png
├── metadata.json      # 可选：生成参数记录
└── ...
```

### 示例
```
batch-20250106-1630-chinese-storyboard/
├── README.md
├── chinese-character-storyboard.png
├── chinese-emotion-storyboard.png
└── chinese-seasons-storyboard.png
```

## README.md 模板

每个批次文件夹必须包含 README.md：

```markdown
# 批次说明

**生成时间**: YYYY-MM-DD HH:mm  
**主题**: 描述生成主题  
**数量**: X 张图片  

## 生成参数

- **generate_type**: text2imageV2
- **model_key**: high_aes_general_v40
- **ratio**: 16:9
- **prompt**: 主要提示词

## 文件清单

1. filename1.png - 简要描述
2. filename2.png - 简要描述

## 用途说明

描述这批图片的预期用途和应用场景。
```

## 执行流程

1. **创建批次文件夹**
   ```bash
   mkdir "batch-$(date +%Y%m%d-%H%M)-主题描述"
   ```

2. **生成图片**
   - 直接执行 curl 生成命令
   - 轮询查询结果
   - 下载到批次文件夹

3. **创建文档**
   - 生成 README.md
   - 记录生成参数
   - 列出文件清单

## 最佳实践

- **及时下载**: URL 有时效性，立即下载
- **参数记录**: 保存 submit_id 和关键参数
- **分类明确**: 按用途、风格、主题分批
- **文档完整**: README.md 包含必要信息