---
name: latex-document-writer
description: LaTeX 论文写作助手，负责章节、段落、图表、代码块等正文内容的撰写与组织。不涉及模板格式调整。
---

# latex-document-writer


## 1. 核心限制 ⚠️
- **禁止**执行任何编译命令（`pdflatex`, `xelatex`, `latexmk` 等）
- 仅编辑 `.tex` 文件并保存即可。


## 2. 目录结构规范
| 路径 | 用途 |
|------|------|
| `latex/chapter[n]/n.tex` | 第 n 章内容（如 `latex/chapter1/1.tex`） |
| `figures/` | 图片资源 |
| `bib/` | 参考文献 |
| `main.tex` | 主文件（勿放内容） |
| `latex/config.tex` | 配置文件（严禁修改） |


## 3. 写作风格规范
### 3.1 层次结构与内容组织

**核心原则**：连贯段落优先，列表为辅。

**标题层级**：`\section` → `\subsection` → `\subsubsection` → `enumerate [label={(\arabic*)}]`（作为第四级）

**逐级决策**：

在任意层级下组织内容时，按以下顺序判断：

(1) **能否用连贯段落**？若内容有连贯的逻辑推导、因果关系或叙事性质 → 使用完整段落，到此结束。

(2) **需要细分但内容厚重**？各分支含长句、技术推导或需多段展开 → 使用下一级标题。

(3) **需要细分且内容轻量**？各项简短独立、天然并列 → 使用列表：
   - 有序枚举：`enumerate [label={(\arabic*)}]`
   - 无序快速列举：`itemize`

**硬性约束**：
- 禁止将连贯句子拆解为 `\item`
- 禁止连续两个列表分点之间无实质过渡段（至少一个完整段落）
- 第四级标题后不再允许使用 `enumerate [label={(\arabic*)}]` ，只准用
  pifont 宏包或 `itemize`
- 禁止 `\item` 开头加 `\textbf{}`（除非用户明确要求）

📁 示例 → `references/writing-style.md`


### 3.2 源码行宽

为提升源码可读性，段落文字每行建议控制在 **"30个汉字"或"60个字符（含空格）**左右后手动换行。

**例外**：LaTeX 命令行、`lstlisting` 代码块、表格、公式、长URL、文件路径这些必须在同一行的功能性代码除外。



## 4. 浮动体规范

### 代码块
使用 `lstlisting` 环境，必须指定 `language=`、`caption`、`label=lst:xxx`。
📁 模板 → `snippets/code-block.tex`



### 图形
**决策**：简单示意图 → TikZ | 复杂/外部图 → `includegraphics`

**TikZ 模板** 📁 `snippets/figure-tikz/`：
| 文件 | 适用场景 |
|------|----------|
| `_index.tex` | 基础模板 + 样式参考 |
| `flowchart.tex` | 流程图（条件、循环、步骤） |
| `block.tex` | 框图（架构、模块、布局） |
| `tree.tex` | 树状结构（二叉树、目录、组织） |
| `relation.tex` | 关系图（ER、拓扑、时序、状态机、类图） |
| `data-struct.tex` | 数据结构（内存、指针、链表、数组） |
| `chart.tex` | 图表（坐标系、韦恩图、饼图、柱状图） |

**外部图片** 📁 模板 → `snippets/figure-image.tex`

**约束**：
- 必须 `[H]` 固定位置
- `caption` 在图下方
- `label=fig:xxx`


### 表格
使用三线表（`toprule/midrule/bottomrule`），禁止 `\hline`。

**约束**：
- `caption` 在表上方
- `label=tab:xxx`
- 表头用 `\textbf{}`
- 代码用 `\texttt{}`

📁 模板 → `snippets/table.tex`


## 5. 术语与引用

### 术语格式
中英对照用 `中文 (English)` 格式。
📁 术语表 → `references/glossary.tex`

### 交叉引用
| 引用对象 | 格式 |
|---------|------|
| 章节 | `\ref{sec:xxx}` |
| 代码 | `\ref{lst:xxx}` |
| 图片 | `\ref{fig:xxx}` |
| 表格 | `\ref{tab:xxx}` |

**禁止**：引用不存在的标签。引用前必须确认标签已定义。
