---
name: pdf-to-image-preview
description: 将PDF文件的每一页转换为图片文件；支持自定义图片格式（PNG/JPG）和分辨率；适用于文档处理、图片化存档等场景
dependency:
  python:
    - pymupdf>=1.23.0
---

# PDF转图片Skill

## 任务目标
- 本Skill用于：将PDF文件的每一页转换为独立的图片文件
- 能力包含：PDF文件解析、图片格式转换（PNG/JPG）、可调分辨率输出
- 触发条件：用户需要将PDF转换为图片、提取PDF页面、图片化PDF内容等场景

## 前置准备
- 依赖说明：scripts脚本所需的依赖包及版本
  ```
  pymupdf>=1.23.0
  ```

## 操作步骤
- 标准流程：
  1. **准备PDF文件**
     - 确认PDF文件路径（使用 `./` 表示当前工作目录）
     - 例如：`./document.pdf`

  2. **执行转换**
     - 调用脚本将PDF文件的每一页转换为图片
     - 命令示例：
       ```bash
       python scripts/convert_pdf_to_images.py \
         --input ./document.pdf \
         --output-dir ./images
       ```
     - 可选参数：
       - `--image-format`: 图片格式，支持 `png` 或 `jpg`，默认为 `png`
       - `--dpi`: 图片分辨率（DPI），默认为 `200`
       - `--zip`: 生成ZIP压缩包
       - `--zip-output`: ZIP压缩包输出路径（默认：images.zip）

  3. **查看输出**
     - 图片文件保存在指定的输出目录中
     - 文件命名格式：`page_001.png`、`page_002.png`...
     - 可选择是否生成ZIP压缩包

## 资源索引
- 必要脚本：见 [scripts/convert_pdf_to_images.py](scripts/convert_pdf_to_images.py)(用途与参数：PDF转图片脚本)

## 注意事项
- 输入PDF文件必须存在且可读
- 输出目录必须具有写入权限
- **PDF页数限制**：暂支持100页以内的PDF文件，超过100页请拆分后转换
- 大型PDF文件转换可能需要较长时间，请耐心等待

## 故障排查
- **脚本找不到错误**：确保在Skill目录下执行，或使用相对路径 `scripts/xxx.py`
- **Python版本问题**：确保使用Python 3.6或更高版本
- **依赖缺失**：执行 `pip install pymupdf>=1.23.0` 安装依赖
- **页数超限错误**：PDF文件超过100页，请使用PDF工具拆分为多个小文件

## 使用示例

### 示例1：基本转换（PNG格式）
```bash
python scripts/convert_pdf_to_images.py \
  --input ./report.pdf \
  --output-dir ./images
```

### 示例2：使用JPG格式
```bash
python scripts/convert_pdf_to_images.py \
  --input ./document.pdf \
  --output-dir ./images \
  --image-format jpg
```

### 示例3：高分辨率输出
```bash
python scripts/convert_pdf_to_images.py \
  --input ./document.pdf \
  --output-dir ./images \
  --dpi 300
```

### 示例4：生成ZIP压缩包
```bash
python scripts/convert_pdf_to_images.py \
  --input ./document.pdf \
  --output-dir ./images \
  --zip \
  --zip-output ./images.zip
```

### 示例5：完整配置
```bash
python scripts/convert_pdf_to_images.py \
  --input ./report.pdf \
  --output-dir ./images \
  --image-format jpg \
  --dpi 200 \
  --zip
```
