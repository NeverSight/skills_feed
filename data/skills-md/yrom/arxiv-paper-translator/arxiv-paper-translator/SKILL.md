---
name: arxiv-paper-translator
description: Translate academic papers from arXiv to Chinese. Use when users want to (1) translate arXiv papers from English to Chinese, or (2) create technical reports summarizing academic papers. Works with arXiv paper IDs like "2206.04655".
license: MIT
---

# arXiv Paper Translator

Translate academic papers from arXiv by downloading LaTeX source, translating content while preserving structure, and generating translated PDFs with technical reports.

## Workflow Overview

1. **Download & Extract** - Get LaTeX source from arXiv
2. **Translate** - Convert English text to Chinese following LaTeX-specific rules
3. **Review** - Spawn reviewer subagent to check translation quality
4. **Chinese Support** - Add xeCJK, localize labels
5. **Compile** - Generate translated PDF using XeLaTeX
6. **Report** - Create technical summary document

## 环境检查

Check local xelatex installation:
```bash
xelatex --version
```
If not installed, make sure Docker is installed and available.

```bash
docker --version
```
This skill requires XeLaTeX to compile translated PDFs. If not installed locally, Docker will be used instead.

Recommend using [xu-cheng/latex-docker](https://github.com/xu-cheng/latex-docker) Docker images.

```sh
# e.g. Tex Live full distribution (only linux/amd64).
# NOTICE: ghcr.1ms.run is a mirror of ghcr.io.
docker pull ghcr.1ms.run/xu-cheng/texlive-debian:20260101 --platform linux/amd64
```

**If both local XeLaTeX and Docker are not installed, then STOP trying to run this skill.** And recommend user to install XeLaTeX or Docker.

## Step 1: Download LaTeX Source

Download and extract source code from arXiv:

All subsequent commands assume **working directory is `arXiv_${ARXIV_ID}`**.

```bash
# Download LaTeX source (replace ARXIV_ID with user-specified paper ID)
ARXIV_ID="2206.04655"
mkdir -p arXiv_${ARXIV_ID}
wget https://arxiv.org/e-print/${ARXIV_ID} -O arXiv_${ARXIV_ID}/paper_source.tar.gz
mkdir -p arXiv_${ARXIV_ID}/paper_source
tar -xzf arXiv_${ARXIV_ID}/paper_source.tar.gz -C arXiv_${ARXIV_ID}/paper_source
```

**Verify extraction:**
```bash
# List files to understand structure
ls -R arXiv_${ARXIV_ID}/paper_source
# Identify main .tex file (usually main.tex, paper.tex, or ms.tex)
find arXiv_${ARXIV_ID}/paper_source -name "*.tex"
```

## Step 2: Translate LaTeX Files

**IMPORTANT**: Before translating, read [references/translation_guidelines.md](references/translation_guidelines.md) for detailed rules.

### Translation Process

1. **Copy all non-.tex files** from `paper_source/` to `paper_cn/`:
   ```bash
   cd arXiv_${ARXIV_ID}
   mkdir -p paper_cn
   cp -rv paper_source/* paper_cn/ 2>/dev/null || true
   find ./paper_cn -name "*.tex" -type f -exec rm -f {} \;
   ```

2. **Find all .tex files** and translate content according to guidelines. **确保每个含可读文本的 .tex 文件都被翻译，不得遗漏。**

3. **Save translations** to `paper_cn/`. 纯命令/宏定义/引用的 .tex 文件（无需翻译）直接复制原文。

### Parallel Translation for Large Papers

If paper has many .tex files, dispatch translation tasks (subagents to translate) in parallel. Each Task should follow [references/translation_prompt.md](references/translation_prompt.md).

**IMPORTANT**: 派发每个翻译 subagent 前，你必须填入 prompt 模板中的所有 `[填入]` 字段：Paper Title、Abstract、Paper Structure（章节概述 + 当前文件属于哪个章节）、Key Terminologies。subagent 无法访问你的上下文，这些信息只有你能提供。

## Step 3: Review Translation

所有翻译 subagent 完成后，**你自己执行** [references/review_checklist.md](references/review_checklist.md) 中的检查步骤。逐条运行命令，分析输出，修复发现的问题。

## Step 4: Add Chinese Support

Follow [references/chinese_support.md](references/chinese_support.md) to configure.

**IMPORTANT**: Ask user for font preference (Fandol / 霞鹜文楷 / user provided font) before configuring.

## Step 5: Compile Translated PDF

### Option 1: Local XeLaTeX

```bash
# Basic compilation
xelatex main.tex

# If paper has bibliography (recommended approach)
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
# or
latexmk -xelatex main.tex
```

### Option 2: Docker with TeX Live

```bash
# change working directory to arXiv_${ARXIV_ID}
cd /path/to/arXiv_${ARXIV_ID}
docker run --rm \
  -v "$(pwd)/paper_cn":/workspace \
  -w /workspace \
  ghcr.1ms.run/xu-cheng/texlive-debian:20260101 \
  latexmk -xelatex main.tex
```

## Step 6: Generate Technical Report

Spawn a subagent following [references/summary_prompt.md](references/summary_prompt.md) to create a technical summary using [assets/report_template.md](assets/report_template.md).

**Save report**: `{arxiv_id}_technical_report.md`

## Final Deliverables

1. **Translated PDF**: `paper_cn/main.pdf`
2. **Technical report**: `{arxiv_id}_technical_report.md`
3. **Source**: `paper_cn/` directory with all translated LaTeX files

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Downloaded file is single .tex, not .tar.gz | `mv paper_source.tar.gz paper_source.tex` and create directory |
| Main file not named main.tex | `find . -name "*.tex" -exec grep -l "\\documentclass" {} \;` |
| Compilation fails with encoding error | `file *.tex` to check, `iconv -f ISO-8859-1 -t UTF-8` to convert |
| Command misspelling (e.g. `\footnotext`) | See review checklist step 2 — diff command sets to find typos |
| Undefined control sequence | xeCJK catcode issue — insert `{}` to separate custom macro from CJK text → `\xmax{}概率` |
| Custom .sty/.cls files | Copy to `paper_cn/`, check for hard-coded English text |
| `Missing $ inserted` in translated tables | 表格中原始数据（代码、traceback、AI 查询）不应翻译，中英混排导致 xeCJK 字体切换出错 |

## References

- **Translation rules**: [references/translation_guidelines.md](references/translation_guidelines.md)
- **Translation prompt**: [references/translation_prompt.md](references/translation_prompt.md)
- **Review checklist**: [references/review_checklist.md](references/review_checklist.md)
- **Chinese support**: [references/chinese_support.md](references/chinese_support.md)
- **Report template**: [assets/report_template.md](assets/report_template.md)
- **Makefile template (optional)**: [assets/Makefile.template](assets/Makefile.template)
