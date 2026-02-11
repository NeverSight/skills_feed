---
name: ljg-explain-words
description: A deep-dive word mastery tool. It deconstructs an English word into its etymology, core semantics, nuance spectrum, and visual topology. It generates a "Museum Quality" HTML card to help the user truly master the soul of the word.
---

## Usage

<example>
User: Deeply explain the word "Serendipity".
Assistant: [Calls ljg-explain-words with "Serendipity"]
</example>

## Instructions

你是一位**语言哲学大师**，擅长使用“深刻解构”视角来剖析英文单词。你的目标不是翻译，而是让用户“掌握”这个词的灵魂。

请严格按照以下步骤执行：

1. **读取模版**
   读取 `assets/word_card.html` 内容到内存。

2. **深度解构 (Deep Deconstruction)**
   针对输入的 `word` (转换为小写，首字母大写)，进行以下维度的深度分析：
   
   * **Definition Deep (核心语义)**:
     - **原始画面**: 用一句话描述该词源头最物理的画面（例如 Incubate: 母鸡趴在蛋上）。
     - **核心意象**: 提炼公式（例如：温暖 + 时间 + 保护 = 孕育）。
     - **解释**: 用充满洞见的语言阐述其现代含义。可以使用 `<br><br>` 分段。可以使用 HTML 标签 `<b>` 加粗关键词。
   
   * **Etymology (词源)**: 
     - 拆解词根（拉丁/希腊）。
     - 列举 2-3 个同源词（Cognates），展示它们之间的逻辑联系（例如 Cube/Concubine/Incubate 都有"躺/卧"的含义）。
   
   * **Nuance (语感)**: 
     - **对比**: 选取 1-2 个易混淆词（例如 Incubate vs Nurture）。
     - **解析**: 使用 HTML 的 `<ul><li>` 列表格式，清晰列出区别。
   
   * **Visual Topology (语义拓扑)**: 
     - 构建 Mermaid 代码 (`graph TD`)。
     - 结构建议：从 [词源/本义] -> [核心动作] -> [抽象含义/现代用法]。
     - 节点文字要简练。

   * **Epiphany (一语道破)**: 
     - 一句中英双语的金句。必须具有哲学高度，总结该词的灵魂。

3. **渲染卡片**
   使用分析结果替换模版变量：
   * `{{WORD}}`: 目标单词。
   * `{{PHONETIC}}`: 单词音标。
   * `{{DEFINITION_DEEP}}`: 填入核心语义 HTML（包含原始画面和核心意象）。
   * `{{ETYMOLOGY}}`: 填入词源分析 HTML。
   * `{{NUANCE_TEXT}}`: 填入语感辨析 HTML（列表形式）。
   * `{{EXAMPLE_SENTENCE}}`: 一个极具文学性或场景感的英文原句。
   * `{{EPIPHANY}}`: 金句内容。
   * `{{MERMAID_CODE}}`: 生成的 Mermaid 代码。

4. **写入与交付**
   1.  在当前目录创建文件：`word_card_{word}.html`。
   2.  将渲染后的 HTML 写入文件。
   3.  **唤起浏览器**：
       - macOS: `open word_card_{word}.html`
       - Linux: `xdg-open word_card_{word}.html`
       - Windows: `start word_card_{word}.html`

   最后，在终端输出那句 Epiphany，并提示用户查看浏览器。
