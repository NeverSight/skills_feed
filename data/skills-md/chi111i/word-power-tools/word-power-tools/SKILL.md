---
name: word-power-tools
description: 处理 Microsoft Word 文档（.docx/.doc/.rtf）：转换（PDF/Markdown/HTML/TXT）、提取（文本/表格/图片）、批量替换、合并/拆分、统一排版/套模板、格式校验/报告。用户提到 Word、docx、doc、论文排版、格式检查、表格提取、导出 PDF 时使用。
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash(python:*)
  - Bash(python3:*)
  - Bash(pip:*)
  - Bash(pip3:*)
---

# Word Power Tools

本 Skill 的目标：让 Claude Code 在本地（Linux/macOS/Windows）把 Word 文档当作**可编程文档**来可靠处理。

## ⚠️ 核心原则

**必须优先使用本 Skill 提供的脚本 `scripts/word_tool.py`，最好不要自己编写临时脚本或一次性代码。**

所有文档操作都应通过 `word_tool.py` 的子命令完成，确保可复现性和稳定性。

## 适用场景（触发关键词）

- “把 docx/doc 转 pdf/markdown/html/txt”
- “从 Word 提取表格/图片/章节结构/正文文本”
- “论文排版、格式统一、目录、页码、页眉页脚”
- “批量替换、合并、拆分、套模板”
- “格式审查（页边距、字体、行距、标题层级）并输出报告”

## 原则（减少风险 + 提高可复现性）

1) **默认不覆盖原文件**：所有会改写的操作必须写到新输出文件（`-o/--output`）。
2) **先 lint 后 format**：排版类任务先生成报告，再应用修复（避免"修坏了但不知道改了什么"）。
3) **复杂任务用脚本输出**：脚本可"零上下文执行"，输出更稳定、可测试。

## Quickstart

依赖自检（推荐每个新环境先跑一次）：

```bash
python scripts/word_tool.py doctor
```

文档概览：

```bash
python scripts/word_tool.py info path/to/file.docx
python scripts/word_tool.py outline path/to/file.docx
```

提取：

```bash
python scripts/word_tool.py extract-text path/to/file.docx -o out.txt
python scripts/word_tool.py extract-tables path/to/file.docx -o tables/ --format xlsx
python scripts/word_tool.py extract-images path/to/file.docx -o images/
```

转换：

```bash
python scripts/word_tool.py convert input.doc  --to docx -o output.docx
python scripts/word_tool.py convert input.docx --to pdf  -o output.pdf
python scripts/word_tool.py convert input.docx --to md   -o output.md
```

批量替换（YAML 规则）：

```bash
python scripts/word_tool.py replace input.docx --rules templates/replace_rules.example.yaml -o replaced.docx
```

写入元数据（作者/标题等）：

```bash
python scripts/word_tool.py set-metadata input.docx --metadata templates/metadata.example.yaml -o meta.docx
```

插入目录（TOC 字段，需要在 Word 里“更新域”才能渲染）：

```bash
python scripts/word_tool.py toc input.docx --levels 1-3 -o with_toc.docx
```

排版校验 + 应用统一格式（YAML 配置）：

```bash
python scripts/word_tool.py lint   input.docx --config templates/format_thesis_qfnu_science.yaml -o report.md
python scripts/word_tool.py format input.docx --config templates/format_thesis_qfnu_science.yaml -o fixed.docx
```

合并/拆分：

```bash
python scripts/word_tool.py merge a.docx b.docx c.docx -o merged.docx
python scripts/word_tool.py split input.docx --by heading1 -o split_out/
```

生成新文档骨架（论文/报告模板化）：

```bash
python scripts/word_tool.py new --template templates/thesis_skeleton.example.yaml -o thesis.docx
```

## 参考文档（按需读取）

- 安装与环境：`docs/INSTALL.md`
- 使用手册（所有子命令）：`docs/USAGE.md`
- 排版规则配置：`docs/FORMAT_RULES.md`
- 常见问题：`docs/TROUBLESHOOTING.md`
- 安全注意事项：`docs/SECURITY.md`

