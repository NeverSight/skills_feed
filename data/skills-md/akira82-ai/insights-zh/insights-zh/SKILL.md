---
name: insights-zh
description: Check for existing insights report and translate it to Chinese
disable-model-invocation: true
allowed-tools: TaskCreate, TaskUpdate, TaskList, TaskGet, Bash, Read, Write
---

# Insights 中文报告生成器

本技能检查现有的 insights HTML 报告并将其翻译为中文。

## 工作流程

当用户调用 `/insights-zh` 时，你将创建 7 个独立的 task 并按依赖关系顺序执行。

## 步骤 1: 创建任务

首先，使用 TaskCreate 工具创建以下 7 个任务：

### 任务 1: 检查报告文件
- **subject**: "Check for insights HTML report"
- **description**: "检查 ~/.claude/usage-data/ 目录是否存在 report.html 文件。如果存在则继续，如果不存在则向用户报告错误并终止。"
- **activeForm**: "Checking for HTML report"

### 任务 2: 分析 HTML 文本块
- **subject**: "Analyze HTML text blocks"
- **description**: "调用 analyze_html.py 脚本分析 ~/.claude/usage-data/report.html 文件，计算文本块数量，并将文本块拆分为 8-10 个部分。生成分析结果到 /tmp/insights-analysis.json"
- **activeForm**: "Analyzing HTML text blocks"
- **addBlockedBy**: ["1"]

### 任务 3: 创建翻译子任务
- **subject**: "Create translation subtasks"
- **description**: "根据 /tmp/insights-analysis.json 的分析结果，创建 8-10 个翻译子任务。每个子任务负责翻译一部分文本块。更新子任务列表并准备翻译工作。"
- **activeForm**: "Creating translation subtasks"
- **addBlockedBy**: ["2"]

### 任务 4: 执行翻译
- **subject**: "Translate all text blocks"
- **description**: "串行执行所有翻译子任务。对于每个子任务：1) 读取对应的文本块 2) 使用大模型将英文翻译为中文 3) 保存翻译结果到 /tmp/insights-analysis.json 中的对应位置。翻译时保留所有 HTML 标签、CSS 样式、JavaScript 代码和属性，只翻译用户可见的文本内容。"
- **activeForm**: "Translating text blocks"
- **addBlockedBy**: ["3"]

### 任务 5: 整合翻译结果
- **subject**: "Merge translations into HTML"
- **description**: "调用 merge_translations.py 脚本，将原始 HTML 文件 ~/.claude/usage-data/report.html 和翻译结果 /tmp/insights-analysis.json 合并，生成完整的中文 HTML 文件 /tmp/report-zh.html。保持原有的布局、颜色、风格等所有视觉元素。"
- **activeForm**: "Merging translations into HTML"
- **addBlockedBy**: ["4"]

### 任务 6: 复制到当前目录
- **subject**: "Copy translated report to current directory"
- **description**: "将 /tmp/report-zh.html 复制到当前工作目录，命名为 report-zh.html。验证文件已成功复制。"
- **activeForm**: "Copying translated file"
- **addBlockedBy**: ["5"]

### 任务 7: 在浏览器中打开
- **subject**: "Open translated report in browser"
- **description**: "使用系统默认浏览器打开当前目录的 report-zh.html 文件。macOS 使用 open 命令，Linux 使用 xdg-open 命令。"
- **activeForm**: "Opening report in browser"
- **addBlockedBy**: ["6"]

## 步骤 2: 执行任务

创建任务后，按以下顺序执行：

### 执行任务 1: 检查报告文件

使用 Bash 工具检查 `~/.claude/usage-data/report.html` 是否存在：

```bash
ls -lh ~/.claude/usage-data/report.html
```

**如果文件不存在**：向用户报告错误："❌ 未找到 report.html 文件。请先运行 /insights 命令生成报告。"并将任务标记为失败。

**如果文件存在**：继续执行任务 2。

### 执行任务 2: 分析 HTML 文本块

1. 确认技能目录中的脚本可用。
2. 使用 Bash 工具执行分析脚本：

```bash
python3 ~/.claude/skills/insights-zh/analyze_html.py ~/.claude/usage-data/report.html /tmp/insights-analysis.json 8
```

3. 验证分析结果已生成：
```bash
ls -lh /tmp/insights-analysis.json
```

4. 使用 Read 工具读取分析结果，查看文本块数量和拆分方案。

### 执行任务 3: 创建翻译子任务

1. 使用 Read 工具读取 `/tmp/insights-analysis.json` 文件。
2. 根据 `chunks` 数组创建对应的翻译子任务记录。
3. 准备翻译工作列表，每个 chunk 作为一个独立的翻译单元。

### 执行任务 4: 执行翻译

对于每个翻译子任务，按顺序执行：

1. **读取文本块**：从分析结果中获取当前 chunk 的所有文本块。
2. **翻译文本**：使用大模型将英文文本翻译为中文。

**翻译规则**：

**必须保留不翻译的内容**:
- HTML 标签和属性名（如 `class`、`id`、`data-*`、`style`、`href` 等）
- HTML 属性值（如 `class="container"`、`id="header"` 等）
- CSS 类名和 ID
- 代码块中的技术术语和代码片段

**需要翻译的内容**:
- 所有用户可见的文本内容
- 页面标题、标题、段落文本
- 按钮文本、链接文本（href 保留，链接文本翻译）
- 表格内容、列表项文本

**翻译原则**:
- 保持 HTML 结构完全不变
- 保持所有标签和属性完整
- 保持缩进和格式
- 只翻译文本节点内容
- 确保翻译后的 HTML 语法正确
- 技术术语保持一致性

3. **保存翻译结果**：将翻译后的文本更新到 `/tmp/insights-analysis.json` 中对应 block 的 `translation` 字段。
4. 串行处理所有 chunk，确保每个翻译完成后再处理下一个。

### 执行任务 5: 整合翻译结果

1. 使用 Bash 工具执行合并脚本：

```bash
python3 ~/.claude/skills/insights-zh/merge_translations.py ~/.claude/usage-data/report.html /tmp/insights-analysis.json /tmp/report-zh.html
```

2. 验证合并后的文件已生成：
```bash
ls -lh /tmp/report-zh.html
```

3. 使用 Read 工具读取合并后的 HTML 文件的开头部分，验证格式正确。

### 执行任务 6: 复制到当前目录

使用 Bash 工具执行以下命令：

```bash
cp /tmp/report-zh.html ./report-zh.html
```

验证文件已成功复制到当前工作目录：

```bash
ls -lh ./report-zh.html
```

### 执行任务 7: 在浏览器中打开

根据操作系统使用相应的命令：

**macOS**:
```bash
open ./report-zh.html
```

**Linux**:
```bash
xdg-open ./report-zh.html
```

**Windows**:
```bash
start ./report-zh.html
```

## 完成提示

所有任务完成后，向用户显示以下信息：

```
✅ Insights 中文报告生成完成！

生成的文件：
- report-zh.html (当前目录)

原始报告：~/.claude/usage-data/report.html (未修改)

已在浏览器中打开翻译后的报告。
```

## 故障排除

### 如果找不到 HTML 文件

如果任务 1 报告找不到 `report.html` 文件，请：

1. 确认你已经运行过 `/insights` 命令
2. 检查 `~/.claude/usage-data/` 目录：

```bash
ls -la ~/.claude/usage-data/
```

3. 如果文件不存在，请先运行 `/insights` 命令生成报告

### 如果分析脚本执行失败

1. 确认 Python 3 已安装：
```bash
python3 --version
```

2. 确认脚本路径正确
3. 检查脚本权限：
```bash
chmod +x /path/to/analyze_html.py
```

### 如果翻译后 HTML 格式错误

确保：
- 所有 HTML 标签都完整保留
- `<style>` 和 `<script>` 标签内容未被翻译
- HTML 属性值未被修改
- 可以在浏览器中打开翻译后的 HTML 文件验证

### 如果浏览器无法打开

1. 确认文件已成功复制到当前目录
2. 手动在浏览器中打开 `./report-zh.html` 文件
3. 检查文件路径是否正确

## 技术说明

### 文本块分析策略

- 使用 HTMLParser 解析 HTML 结构
- 提取所有非 script/style 标签内的文本
- 记录每个文本块的上下文（所在标签层级）
- 按字符长度均衡分配到 8-10 个块中

### 翻译策略

- 串行执行确保上下文一致性
- 每个块独立翻译，避免长度限制
- 保留技术术语的原始形式
- 维护 HTML 结构完整性

### 合并策略

- 按文本长度降序替换，避免短文本被先替换
- 精确匹配原始文本
- 保留所有 HTML 标签和属性
- 只替换文本节点内容
