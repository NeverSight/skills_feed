---
name: doc-mindmap
description: 文档智能整理助手 - 批量转换办公文档为 Markdown，本地模型生成摘要，三维度软链接分类
---

# Doc Mindmap - 文档智能整理助手 📚🧠

将散落的办公文档（PDF、PPT、Word、Excel 等）批量转换为 Markdown，通过本地 Ollama 模型生成摘要和三维度分类，用软链接同时呈现多种分类方案，零额外磁盘占用。

## When to Use

Use this skill when users:
- 想整理大量文档、分类归档
- 需要给一批文档生成摘要
- 想生成文档的思维导图 / mindmap
- 想把 PDF、PPT、Word 转成 Markdown
- 需要文档分类建议或目录结构方案
- 想快速了解一个文件夹里都有什么文档
- 需要检测重复文件

触发关键词: 文档整理, 文档分类, 思维导图, mindmap, 文档摘要, PDF 转 Markdown, 批量转换, 文档归档

## Features

- **🔄 批量转换** - PDF、PPT、Word、Excel 等一键转 Markdown
- **📋 CSV 索引** - 自动生成文档索引，含 MD5 和重复检测
- **🔍 重复检测** - MD5 比对发现重复文件，建议删除释放空间
- **📝 本地摘要** - Ollama 本地模型生成摘要，不消耗 Claude 上下文
- **🗂️ 三维度分类** - 按主题/用途/客户三种方案同时分类
- **🔗 软链接目录** - symlink 实现多分类共存，零额外磁盘占用
- **✏️ 智能重命名** - AI 根据内容建议更清晰的文件名，软链接可选用优化名称
- **🛡️ 安全机制** - 只读转换，不修改原始文件

## Supported Formats

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| 📄 PDF | .pdf | PDF 文档 |
| 📊 PPT | .pptx | PowerPoint 演示文稿 |
| 📝 Word | .docx | Word 文档 |
| 📈 Excel | .xlsx, .xls | 电子表格 |
| 📈 CSV | .csv | 逗号分隔值 |
| 🌐 HTML | .html, .htm | 网页 |
| 📚 EPUB | .epub | 电子书 |
| 📋 JSON | .json | JSON 数据 |
| 📋 XML | .xml | XML 数据 |

## Usage

### 预览文档列表（含重复检测）

```bash
python scripts/doc_converter.py ~/Documents/reports --preview
```

### 执行转换

```bash
python scripts/doc_converter.py ~/Documents/reports --convert --confirm
```

### 转换指定文件

```bash
python scripts/doc_converter.py file1.pdf file2.pptx --convert --confirm
```

### 生成摘要（需先转换）

```bash
python scripts/doc_converter.py ~/Documents/reports --summarize
python scripts/doc_converter.py ~/Documents/reports --summarize --model qwen3:8b
```

### 三维度分类 + 软链接（需先摘要）

```bash
python scripts/doc_converter.py ~/Documents/reports --organize
```

### 分类 + 使用 AI 建议的文件名

```bash
python scripts/doc_converter.py ~/Documents/reports --organize --rename
```

### 全流程一步完成

```bash
python scripts/doc_converter.py ~/Documents/reports --convert --confirm --summarize --organize
# 含优化文件名
python scripts/doc_converter.py ~/Documents/reports --convert --confirm --summarize --organize --rename
```

### JSON 格式输出

```bash
python scripts/doc_converter.py ~/Documents --preview --json
```

## Arguments

| 参数 | 说明 |
|------|------|
| `paths` | 文件或目录路径（支持多个） |
| `--preview` | 预览模式，列出文档 + 重复检测 |
| `--convert` | 执行批量转换（自动跳过重复文件） |
| `--summarize` | 使用 Ollama 本地模型生成摘要（需先 convert） |
| `--organize` | 三维度分类并生成软链接目录（需先 summarize） |
| `--rename` | 软链接使用 AI 建议的优化文件名（配合 --organize） |
| `--model MODEL` | Ollama 模型名称（默认: qwen2.5:3b） |
| `--confirm` | 确认执行（安全机制） |
| `--json` | JSON 格式输出 |

## Output Structure

转换输出在源文件夹的 `.summaries/` 隐藏目录下：

```
{source}/
└── .summaries/
    ├── converted/              # markitdown 转换的 .md 文件
    │   ├── report.pdf.md
    │   ├── slides.pptx.md
    │   └── data.xlsx.md
    ├── briefs/                 # Ollama 生成的摘要
    │   ├── report.pdf.brief.md
    │   ├── slides.pptx.brief.md
    │   └── data.xlsx.brief.md
    ├── schemes/                # 软链接分类目录
    │   ├── by-topic/           # 按主题分类
    │   │   ├── AI技术/
    │   │   │   └── AI驱动产品管理指南.pptx -> ../../../../slides.pptx  # --rename
    │   │   └── 数据治理/
    │   │       └── C端数据治理规划.pdf -> ../../../../report.pdf       # --rename
    │   ├── by-usage/           # 按用途分类
    │   │   ├── 培训材料/
    │   │   └── 客户交付方案/
    │   └── by-client/          # 按客户分类
    │       ├── 沃尔沃/
    │       └── 通用方案/
    ├── mindmap.md              # Claude 生成的思维导图分类
    └── index.csv               # 转换索引（含 MD5、重复标记）
```

## Dependencies

- Python 3.10+
- markitdown: `pip install 'markitdown[all]'`
- Ollama（摘要 + 分类）: `brew install ollama` + `ollama pull qwen2.5:3b`
- requests: `pip install requests`

## Claude Workflow

Claude 使用此技能时，按以下步骤执行：

### 第 1 步：预览文档

运行预览命令，向用户展示文档列表和重复检测结果：

```bash
python doc-mindmap/scripts/doc_converter.py <路径> --preview
```

告知用户找到的文档数量、类型分布、总大小和重复文件情况，等待确认。

### 第 2 步：执行转换

用户确认后执行转换（重复文件自动跳过）：

```bash
python doc-mindmap/scripts/doc_converter.py <路径> --convert --confirm
```

### 第 3 步：生成摘要（Ollama 本地模型）

使用 Ollama 本地模型为每个文档生成摘要，不消耗 Claude 上下文窗口：

```bash
python doc-mindmap/scripts/doc_converter.py <路径> --summarize
```

也可以和 convert 一起执行：
```bash
python doc-mindmap/scripts/doc_converter.py <路径> --convert --confirm --summarize
```

### 第 4 步：三维度分类 + 软链接

使用 Ollama 对每个文档进行三维度分类（主题/用途/客户），同时为每个文档建议更清晰的文件名：

```bash
# 先不带 --rename 运行，展示分类结果和建议文件名
python doc-mindmap/scripts/doc_converter.py <路径> --organize
```

向用户展示分类结果和 AI 建议的文件名，询问是否使用优化文件名。如果用户同意：

```bash
python doc-mindmap/scripts/doc_converter.py <路径> --organize --rename
```

三套分类方案通过软链接同时存在于 `.summaries/schemes/` 下，零额外磁盘占用。`--rename` 仅影响软链接名称，不修改原始文件。

### 第 5 步：预览分类结果

询问用户是否要在 Finder 中预览分类目录。如果用户同意：

1. 将 schemes 目录复制到桌面（保留软链接）：
```bash
cp -a <.summaries/schemes> ~/Desktop/文档分类-$(date +%Y%m%d)
```

2. 用 Finder 打开：
```bash
open ~/Desktop/文档分类-$(date +%Y%m%d)
```

用户可以在 Finder 中直观浏览三种分类方案，双击软链接即可打开原始文件。

### 第 6 步：生成思维导图

读取 `.summaries/briefs/` 下的摘要文件，生成 `.summaries/mindmap.md` 思维导图分类文件。

### 第 7 步：展示结果

向用户展示：
1. 转换统计（成功/失败/跳过重复）
2. 重复文件列表及删除建议
3. 三维度分类概览
4. 思维导图分类预览

## Credits

- [markitdown](https://github.com/microsoft/markitdown) - Microsoft 出品的文档转 Markdown 工具
- [Ollama](https://ollama.com/) - 本地 LLM 运行框架
- 与 [file-organizer](../file-organizer/) 配合使用，先分类再整理
