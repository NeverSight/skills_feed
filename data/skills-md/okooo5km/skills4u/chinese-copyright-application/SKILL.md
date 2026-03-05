---
name: chinese-copyright-application
description: 中国软件著作权申请材料生成工具，直接输出 LaTeX 源文件并编译为 PDF。自动分析项目代码，生成著作权登记申请表、源程序文档（前后各30页共60页）、用户手册、设计说明书四份材料，含页眉页脚、截图占位、信息一致性校验。适用于微信小程序、Web应用、移动App、桌面应用等各类软件项目。当用户提到软件著作权、软著申请、版权登记时必须使用此 Skill。当用户要为任何软件项目准备著作权材料、生成软著文档时也应使用。
---

# 中国软件著作权申请材料生成

## 核心原则

所有文档直接生成 `.tex` 文件，用 XeLaTeX 编译为 PDF。

## 快速开始

1. 环境检查与安装引导
2. 收集著作权人信息与关键参数
3. 分析项目结构和代码
4. 生成四份 LaTeX 文档 + 编译脚本
5. 生成截图清单
6. 运行一致性校验

## 工作流程

### 第零步：环境检查

在开始生成前，主动询问用户是否已安装 XeLaTeX 环境。执行 `xelatex --version` 检测。

**如已安装**：继续下一步。

**如未安装**：告知用户需要安装 LaTeX 环境才能将 .tex 编译为 PDF，询问是否立即安装。用户同意后按以下命令执行：

- macOS：`brew install --cask basictex && sudo tlmgr update --self && sudo tlmgr install ctex xecjk fancyhdr lastpage fancyvrb tabularx enumitem float xcolor longtable collection-fontsrecommended`
- Linux：`sudo apt install texlive-xetex texlive-lang-chinese texlive-latex-extra texlive-fonts-recommended`
- Windows：引导用户安装 TeX Live 完整版（https://www.tug.org/texlive/）

### 第一步：信息收集

分两轮收集信息。

#### 第一轮：著作权人信息

先检查项目根目录或用户工作目录下是否存在 `copyright-owner.json`。

**如已存在**：读取文件内容，向用户展示并确认是否有变更。用户确认无误则直接使用，跳到第二轮。

**如不存在**：首次使用，需引导用户提供信息并保存。先问著作权人是个人还是企业，然后收集对应信息。

个人需提供：姓名、身份证号、地址、邮编、联系人、电话、邮箱。

企业需提供完整工商信息（参考 [requirements.md](references/requirements.md)「著作权人信息」章节）：公司全称、统一社会信用代码、企业类型、法定代表人、注册资本、住所地址、登记机关、营业执照登记日期、联系人、电话、邮箱。

收集完成后将信息保存为 `copyright-owner.json`，格式如下：

```json
{
  "type": "企业",
  "name": "星辰科技（北京）有限公司",
  "credit_code": "91110108MA01EXAMPLE",
  "enterprise_type": "有限责任公司",
  "legal_representative": "张三",
  "registered_capital": "伍佰万元整",
  "address": "北京市海淀区中关村大街1号",
  "registration_authority": "北京市海淀区市场监督管理局",
  "license_date": "2022年6月15日",
  "contact": "",
  "phone": "",
  "email": ""
}
```

此文件后续申请时直接复用，著作权人信息只需填一次。

#### 第二轮：软件关键参数

自动分析项目后预填建议值，让用户确认：

| 参数 | 说明 |
|------|------|
| 软件全称 | **必须以"软件"二字结尾**（如"智慧记账软件"），有辨识度，所有文档中完全一致。用户提供的名称若未以"软件"结尾，自动补上 |
| 版本号 | V1.0（首次申请统一使用 V1.0） |
| 开发完成日期 | 软件实际完成开发的日期 |
| 首次发表日期 | 软件首次上线/发布的日期（≥ 开发完成日期） |
| 源程序量 | 项目实际总代码行数（可自动统计后让用户确认） |

**日期约束**：开发完成日期 ≤ 首次发表日期 < 申请日期。生成时自动校验，不合规则提醒用户修改。

### 第二步：项目分析与源程序生成

运行 `scripts/analyze_and_generate_source.py` 完成项目分析和源程序 .tex 生成：

```bash
python3 scripts/analyze_and_generate_source.py <项目路径> \
  --name "软件全称" \
  --version "V1.0" \
  --owner "著作权人名称" \
  --date "2025年4月30日" \
  --output copyright-materials/
```

脚本自动完成：
1. 检测项目类型（微信小程序/Web/Node.js 等）
2. 遍历代码文件，排除 node_modules 等无关目录
3. 统计有效代码行数（排除空行和纯注释行），输出按文件类型的行数分布
4. 按文件优先级排序，去除空行后提取前30页 + 后30页代码，生成源程序 .tex 文件
5. 输出 `project_analysis.json` 供后续文档生成参考

**排版经验值**（10pt + `\small` Verbatim + 上下2cm左右1.5cm边距，基于实测校准）：

| 参数 | 值 | 说明 |
|------|------|------|
| 标准页容量 | 50行/页 | 满页代码行数 |
| 首页容量 | 40行 | 标题区域占约10行空间 |
| 后30页首页 | 48行 | 分隔标题占约2行空间 |
| 前30页目标 | 1490行 | 40 + 29×50 |
| 后30页目标 | 1498行 | 48 + 29×50 |
| 总目标 | 2988行 | 去除空行后的代码行数 |

代码量不足2988行时，脚本使用全部代码，不强凑60页。

脚本输出的 `total_lines_effective` 即为申请表中的「源程序量」。

### 第三步：生成四份文档

所有文档的 LaTeX 编写规范见 [references/requirements.md](references/requirements.md)。每份文档的模板见 references 目录下对应的 `.tex` 模板文件。

#### 输出文件夹与命名

输出目录：`copyright-materials/`

生成文档前先创建目录结构：
```bash
mkdir -p copyright-materials/images
```

文件命名规范为「软件全称 + 文档类型」，举例：

- `智慧记账软件著作权登记申请表.tex` / `.pdf`
- `智慧记账软件源程序.tex` / `.pdf`
- `智慧记账软件用户手册.tex` / `.pdf`
- `智慧记账软件设计说明书.tex` / `.pdf`
- `build_all.sh`
- `images/`（图片目录，用户后续在此放入截图）

#### 3.1 著作权登记申请表

模板：[application-form-template.tex](references/application-form-template.tex)

格式要求：
- documentclass: `a4paper,12pt,article`
- 表格使用 `tabularx` 环境
- 分为：基本信息、著作权人信息、开发者信息、软硬件环境信息、软件基础信息、软件技术特点、软件功能简介、备注
- 申请表字段有严格字数限制（详见 requirements.md「字数限制」章节），生成后必须校验

**字数限制速查**：
- 硬件环境/操作系统/开发工具/运行平台/支撑环境：各 ≤50 字符
- 开发目的/面向领域：各 ≤50 字
- 主要功能：≤200 字
- 技术特点：≤100 字

#### 3.2 源程序

由第二步的脚本自动生成，无需手动编写。生成规则详见 [requirements.md](references/requirements.md)「源程序文档要求」。

#### 3.3 用户手册

模板：[user-manual-template.tex](references/user-manual-template.tex)

内容结构：
1. 软件简介（概述 + 主要特点）
2. 功能概述（功能列表 + 适用场景）
3. 安装与使用说明（系统要求 + 进入方式 + 登录说明）
4. 主要功能说明（每个功能的操作步骤，配截图）
5. 注意事项
6. 技术支持

**截图要求**：
- 定义 `\screenshot{文件名}{标题}` 宏，宽度 0.35\textwidth
- 对尚未提供的截图，LaTeX 中仍放置 `\screenshot` 调用
- 同时输出截图清单（见第四步）

#### 3.4 设计说明书

模板：[design-doc-template.tex](references/design-doc-template.tex)

内容结构：
1. 软件概述（简介 + 开发背景 + 设计目标）
2. 需求分析（功能/性能/安全需求）
3. 总体设计（系统架构 + 模块划分 + 技术选型 + 运行环境）
4. 详细设计（各模块功能、处理流程，配截图）
5. 数据结构设计
6. 接口设计（内部接口 + 外部 API 列表）
7. 界面设计（配截图）
8. 安全设计
9. 测试设计

### 第四步：截图管理

分析项目代码（页面文件、弹窗组件、模态框等），生成截图清单 `screenshot-list.md`：

```
| 编号 | 文件名 | 描述 | 触发方式 | 使用位置 |
|------|--------|------|----------|----------|
| 01 | 图1-首页空状态.png | 首页空状态 | 首次进入首页 | 用户手册§3、设计说明书§4.1 |
| 02 | 图2-搜索结果列表.png | 搜索结果 | 输入关键词搜索 | 用户手册§4.1、设计说明书§4.1 |
```

LaTeX 文档中 `\screenshot{文件名}{标题}` 宏已内置 `images/` 路径前缀，用户只需将截图放到 `images/` 目录，文件名与清单中一致即可，编译时自动找到。

#### 交付截图任务给用户

文档初版生成完毕后，**暂停自动流程**，向用户输出以下操作指引（将 `<输出目录>` 替换为实际路径）：

---

文档初版已全部生成完毕，接下来需要你手动截取软件界面截图。

截图保存路径：`<输出目录>/images/`

请按照上方截图清单，逐一截取对应的软件界面截图，保存到该目录。文件名与清单中的「文件名」列保持一致（如 `图1-首页.png`）。

**截图添加完成后回复我一声，我会重新编译所有文档生成最终 PDF。**

---

等用户确认截图完成后，再继续执行第五步（编译）和第六步（校验）。

### 第五步：编译脚本

生成 `build_all.sh`，模板见 [references/build-script-template.sh](references/build-script-template.sh)。

脚本要点：
- 设置 PATH 包含 TeX 路径
- 每个 .tex 文件编译两遍（确保页码引用正确）
- 清理 .aux/.log/.out 等临时文件
- 输出每个 PDF 的文件大小

### 第六步：一致性校验

生成完所有文档后，自动校验以下内容并输出校验报告：

| 校验项 | 校验位置 |
|--------|----------|
| 软件全称 | 申请表、源程序页眉和首页、用户手册标题/页眉、设计说明书标题/页眉 |
| 版本号 | 所有文档的页眉和正文中 |
| 源程序量 | 申请表中的数字 = 源程序文档首页标注的数字 |
| 著作权人名称 | 每个文档首页 |
| 日期 | 各文档中引用的日期一致 |
| 字数限制 | 申请表各字段不超限 |

校验通过则输出"✓ 一致性校验通过"，否则列出不一致项。

## 统一 LaTeX 排版规范

以下规范适用于申请表、用户手册、设计说明书（源程序文档例外，有专门规范）：

### 页面设置
```latex
\documentclass[a4paper,12pt]{article}
\usepackage[UTF8,heading=true]{ctex}
\usepackage[top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm]{geometry}
```

### 页眉页脚
```latex
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{软件全称V1.0\quad 文档类型}
\fancyfoot[C]{第 \thepage\ 页\quad 共 \pageref{LastPage} 页}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}
\fancypagestyle{plain}{\pagestyle{fancy}}
```

页眉格式：`软件全称V版本号  文档类型`（如：智慧记账软件V1.0 用户手册）
页脚格式：`第 X 页  共 XX 页`
页眉页脚均有分隔线（0.5pt）

### 中文排版
```latex
\setlength{\parindent}{2em}          % 段首缩进 2 字符
\setlength{\parskip}{0.3em}
\renewcommand{\baselinestretch}{1.3}  % 1.3 倍行距
```

### 列表
```latex
\begin{itemize}[leftmargin=2em]
\begin{enumerate}[leftmargin=2em]
```

### 截图宏

在文档 preamble 中设置图片搜索路径，并定义截图宏：
```latex
\graphicspath{{images/}}

\newcommand{\screenshot}[2]{%
  \begin{figure}[H]
    \centering
    \includegraphics[width=0.35\textwidth]{#1}
    \caption{#2}
  \end{figure}
}
```
调用时只需 `\screenshot{图1-首页.png}{首页}`，LaTeX 会自动在 `images/` 目录下查找图片文件。

### 文档首页结构

每份文档首页统一格式：
```latex
\begin{center}
  {\LARGE\bfseries 软件全称\quad 文档类型}
  \vspace{0.8em}
  {\large 著作权人：公司全称}
  \vspace{0.3em}
  软件版本：V1.0\qquad 发布日期：YYYY年M月D日
\end{center}
```

## 特殊项目类型处理

### 微信小程序

- 软件分类：移动应用软件——小程序
- 运行平台：iOS、Android、Windows、macOS、HarmonyOS（微信客户端）
- 运行支撑环境：微信客户端（支持小程序的任意版本）
- 技术特点类型选择：小程序

### Web 应用

- 软件分类：应用软件——Web应用
- 运行平台：Windows、macOS、Linux（浏览器）
- 运行支撑环境：Chrome/Firefox/Safari 等浏览器

### 移动 App

- 软件分类：移动应用软件——App
- 运行平台：根据实际支持列出（iOS/Android/HarmonyOS 等）

### 跨平台项目

- Electron 应用：Windows、macOS、Linux
- Flutter/React Native：iOS、Android（如支持桌面端则加上 Windows、macOS、Linux）

## LaTeX 环境依赖

环境检查与安装流程见「第零步」。

**必需宏包**：ctex、xecjk、fancyhdr、lastpage、fancyvrb、tabularx、enumitem、float、xcolor、longtable、graphicx、hyperref、array、geometry

**编译命令**：`xelatex -interaction=nonstopmode 文件名.tex`（运行两遍）

## 参考文档

- [申请要求详细说明](references/requirements.md)
- [申请表 LaTeX 模板](references/application-form-template.tex)
- [源程序 LaTeX 模板](references/source-code-template.tex)
- [用户手册 LaTeX 模板](references/user-manual-template.tex)
- [设计说明书 LaTeX 模板](references/design-doc-template.tex)
- [编译脚本模板](references/build-script-template.sh)
