---
name: magazine-layout
description: |
  将文本内容转换为精美的杂志风格HTML页面，支持专业排版和多种视觉风格。触发场景：(1) 用户想将文本/文章转换为杂志风格HTML，(2) 用户提到"杂志排版"、"杂志设计"、"文章排版"、"专业排版"、"文本美化"、"magazine layout"，(3) 用户需要优雅排版的HTML页面，(4) 用户需要将设计内容导出为PDF。支持12种独特视觉风格，使用Tailwind CSS。
---

# 杂志排版设计师

将纯文本转换为专业设计的杂志风格HTML页面，使用Tailwind CSS实现精美排版。

## 快速开始

1. 用户提供文本内容
2. **与用户讨论并选择合适的风格**
3. 根据选定风格生成完整HTML
4. 可选：导出为PDF

## 工作流程

### 第一步：分析内容结构

识别文本的结构元素：
- 标题和副标题
- 章节和小标题
- 重要引言或金句
- 列表和数据要点
- 作者/日期信息

### 第二步：风格选择（与用户协商）

**重要**：必须向用户展示风格选项，与用户讨论后再确定。使用 AskUserQuestion 工具让用户选择。

阅读 [references/styles.md](references/styles.md) 获取完整模板。

**可选风格一览：**

| 编号 | 风格名称 | 适用场景 | 视觉特点 |
|-----|---------|---------|---------|
| 1 | 经典优雅 (Classic Elegance) | 文学、散文、回忆录 | 衬线字体、暖色调、首字下沉、装饰性分隔线 |
| 2 | 现代极简 (Modern Minimalist) | 科技博客、现代文章 | 无衬线字体、大量留白、简洁线条 |
| 3 | 科技杂志 (Tech Magazine) | 编程、技术内容 | 渐变色彩、代码块样式、未来感设计 |
| 4 | 自然生活 (Nature & Lifestyle) | 生活方式、旅行、美食 | 自然绿色调、有机造型、手写风格点缀 |
| 5 | 大胆社论 (Bold Editorial) | 观点、评论文章 | 超大标题、高对比黑白、红色强调 |
| 6 | 复古怀旧 (Vintage Retro) | 历史、怀旧内容 | 复古边框、打字机字体、羊皮纸质感 |
| 7 | 商务专业 (Corporate Professional) | 商业报告、企业文档 | 海军蓝配色、清晰层级、专业严谨 |
| 8 | 创意艺术 (Creative Art) | 设计、艺术创作 | 不对称布局、色块装饰、手绘风格 |
| 9 | 学术期刊 (Academic Journal) | 学术论文、研究报告 | 双栏布局、摘要样式、引用格式 |
| 10 | 时尚奢华 (Fashion Luxe) | 时尚、奢侈品内容 | 金色点缀、优雅衬线、精致留白 |
| 11 | 新闻报道 (News & Report) | 新闻、新闻报道 | 报纸风格、多级标题、突发标签 |
| 12 | 暗黑科技 (Dark Mode Tech) | 开发者内容 | 深色背景、荧光配色、终端风格 |

**风格推荐逻辑：**
- 文学/散文类 → 推荐：经典优雅、复古怀旧
- 技术/编程类 → 推荐：科技杂志、暗黑科技、现代极简
- 商业/报告类 → 推荐：商务专业、新闻报道
- 生活/旅行类 → 推荐：自然生活、时尚奢华
- 观点/评论类 → 推荐：大胆社论、创意艺术
- 学术/研究类 → 推荐：学术期刊

**用户也可以：**
- 混合多种风格元素
- 自定义颜色、字体
- 调整页面尺寸和间距

### 第三步：生成HTML

从 [references/styles.md](references/styles.md) 读取选定风格的模板，生成完整HTML。

**生成规则：**
1. 严格使用选定风格的模板结构
2. **保留用户原文的全部内容** - 绝不删减或总结
3. 应用合适的排版组件：
   - 首段使用 `drop-cap` 首字下沉
   - 重要语句使用 `blockquote` 引言样式
   - 章节间使用风格专属的分隔线
   - 正确的标题层级 (h1 > h2 > h3)
4. **必须包含智能分页CSS**（见下方说明）
5. 内容必须适应页面尺寸
6. 包含所有CSS（内联或通过CDN引入Tailwind、Google Fonts）
7. 输出完整、自包含的HTML文件

**核心排版组件：**

```html
<!-- 首字下沉段落 -->
<p class="drop-cap">首段文字内容...</p>

<!-- 引言/引用块 -->
<blockquote>
  <p>"重要引言内容"</p>
  <cite>— 来源</cite>
</blockquote>

<!-- 章节分隔线 -->
<div class="elegant-divider"><span>※</span></div>

<!-- 标题区域 -->
<header>
  <h1>主标题</h1>
  <p class="subtitle">副标题或导语</p>
</header>
```

**智能分页CSS（必须包含）：**

确保PDF导出时内容不会在元素中间被切断。每个模板已内置此CSS，生成HTML时必须保留：

```css
/* 打印/PDF模式 */
@media print {
  /* 标题后禁止分页 */
  h1, h2, h3, .chapter-number, .chapter-title {
    page-break-after: avoid; break-after: avoid;
  }
  /* 块级元素内部禁止分页 */
  blockquote, .highlight-box, .stage-item, .question-item,
  .code-block, .terminal, figure, img, table {
    page-break-inside: avoid; break-inside: avoid;
  }
  /* 列表保持完整 */
  ul, ol, .numbered-list, .stage-list {
    page-break-inside: avoid; break-inside: avoid;
  }
  /* 分隔线后禁止分页 */
  .elegant-divider, .divider, hr {
    page-break-after: avoid; break-after: avoid;
  }
  /* 段落孤行寡行控制 */
  p { orphans: 3; widows: 3; }
}
/* 非打印时也应用，确保PDF渲染一致 */
blockquote, .highlight-box, .code-block, .terminal, figure, img, table {
  page-break-inside: avoid; break-inside: avoid;
}
```

| CSS属性 | 效果 | 适用元素 |
|--------|------|---------|
| `page-break-inside: avoid` | 元素内部禁止分页 | 引言、卡片、列表 |
| `page-break-after: avoid` | 元素后禁止分页 | 标题、分隔线 |
| `orphans: 3` | 页底至少保留3行 | 段落 |
| `widows: 3` | 页顶至少保留3行 | 段落 |

### 第四步：PDF导出（可选）

使用 `scripts/html_to_pdf.py` 脚本：

```bash
# 检查可用引擎
python scripts/html_to_pdf.py --check

# 转换（自动检测最佳引擎）
python scripts/html_to_pdf.py magazine.html

# 指定输出文件名
python scripts/html_to_pdf.py magazine.html output.pdf

# 使用特定引擎
python scripts/html_to_pdf.py magazine.html --engine playwright
```

**引擎安装方法：**
- Playwright（推荐）: `pip install playwright && playwright install chromium`
- WeasyPrint: `pip install weasyprint`
- wkhtmltopdf: `brew install wkhtmltopdf` (macOS)

## 长文分页处理

**智能分页**：所有模板已内置分页控制CSS，PDF导出时自动避免在以下位置分页：
- 标题与正文之间
- 引用块、高亮框、列表内部
- 分隔线与下方内容之间

对于超长内容（需手动分割时）：
1. 在自然断点处分页（每页约800-1000字）
2. 生成独立HTML文件：`文章_第1页.html`、`文章_第2页.html`
3. 每页都是完整自包含的HTML（含完整CSS和分页控制）

## 输出格式

```markdown
## 您的杂志页面

将以下代码保存为 `文章.html`：

\`\`\`html
<!DOCTYPE html>
...完整HTML代码...
\`\`\`

**查看方式：** 用浏览器打开 `文章.html`
**导出PDF：** `python scripts/html_to_pdf.py 文章.html`
```

## 风格定制

用户可能要求修改：
- **颜色**：修改CSS变量或Tailwind类
- **字体**：更新Google Fonts导入
- **间距**：调整padding、margin、line-height
- **布局**：修改页面宽高尺寸

在保持整体风格协调的前提下应用修改。

## 资源文件

### scripts/
- `html_to_pdf.py` - HTML转PDF脚本，支持多种渲染引擎（Playwright/WeasyPrint/wkhtmltopdf）

### references/
- `styles.md` - 全部12种风格的完整模板，包含配色方案、字体设置、智能分页CSS和HTML模板代码
