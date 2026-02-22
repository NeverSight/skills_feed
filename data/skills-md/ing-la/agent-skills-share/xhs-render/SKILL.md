---
name: xhs-render
description: "Converts Xiaohongshu copywriting into publish-ready images via HTML templates and scripts. Integrates with skill-share. No AI image generation. Use when user mentions '文案转图片', '小红书配图', 'XHS copy to image', '渲染 skill-share 的文案', or needs script-based text-to-image for Little Red Book."
license: MIT
metadata:
  version: "1.0.0"
---

# xhs-render — 小红书文案转图 + 配套文案

用户提供需渲染的文案所在目录（或指定文档），Skill 完成：选模板 → 定位文档 → 创建工作目录 → LLM 设计 blocks.json 与 xhs-copy → 渲染成图并写入配套文案。

## 流程

1. **选模板（先与用户交互）**：列出可选模板，询问用户选择，待用户确认后再继续。
   - 可选：ing-minimal、ing-notion、ing-skillshare（Ing 品牌）；minimal、notion、skillshare（share 品牌）
   - 示例：「可选模板：ing-minimal（Ing 品牌简约，推荐）、ing-notion（Ing 井字格知识风）、ing-skillshare（Ing 技能分享风）；minimal、notion、skillshare 为 share 品牌同款。请问用哪个？」→ 用户回复后记下，后续用 `-t <所选>`

2. **定位文档**：
   - 用户指定文案目录（如 `Agent-skills-share/daily-posts/YYYY-MM-DD-<skill-name>`）或具体文件
   - **优先顺序**：用户指定哪个就读哪个；未指定则默认 `final.md`
   - 用户说「渲染 draft」→ 读 `draft.md`；说「渲染 final」或未指定 → 读 `final.md`；指定其他（如 `my-copy.md`）→ 读该文档

3. **创建工作目录**：
   - `python .cursor/skills/xhs-render/scripts/get_output_dir.py <文案目录> --source <source>`
   - source：用户指定 draft 时用 `draft`，指定其他自定义文档时用 `custom`，否则 `final`
   - 输出目录：`<文案目录>/xhs-render/from-{source}-v{N}/`（如 `from-final-v1`、`from-draft-v1`）

4. **LLM 设计 blocks.json 与 xhs-copy**（一次产出）：
   - 读取定位到的文档
   - **角色**：你是小红书配图设计专家，擅长把长文案重排成「有节奏、有冲击力」的视觉结构。**严禁照抄原文**——必须按屏上可读性重新提炼、缩写、造句。
   - **任务**：从文档中提炼核心信息，设计一套配图（blocks.json）及配套发帖文案（xhs-copy）
   - **blocks.json 刚性约束**：
     - **Cover**：text 不得超过 2 行（约 20 字），只放金句或主卖点；**主文案建议 6–12 字**为佳（如「AI 文案去味神器」），既能撑满版面又不会挤；**必须在 cover 块中显式添加 `"skill": "<技能名>"`**（如 `"skill": "humanizer-zh"`），封面会在主文案下方以「技能名」形式醒目展示；若未填则脚本会从目录名 `YYYY-MM-DD-<skill-name>` 自动解析
     - **每块 text**：建议 150–200 字，**每页可含多条要点**；多条要点之间**必须用双换行**（`\n\n`）分隔，否则会挤成一段、圆点无法分条；用短句、换行、关键词前置，让版面充实
     - **碎碎念块**：若有 Agent 碎碎念、评价类内容，字数可适当增多（60–100 字），表达更饱满
     - **ending 块**：放致谢开发者，格式：`宝藏开发者：owner/repo` + `传送门：https://skills.sh/...`，可加碎碎念；**不放安装命令**；安装命令写在 xhs-copy 文案中
     - **禁止**：将文档的【】小节 1:1 映射为 block；在 title 里直接复制小节名（可创新改写）；在图片里放安装命令
     - 分几张图、每块 title/text/emoji 由你专业判断；页数可多可少，设计好、必要内容都有即可。避免同一张图内 title 与 emoji 重复。**纯 hashtag 不生成图片**
   - **xhs-copy**：与配图配套的发帖文案，XHS-ready 纯文本——无 `##`、`**`、`` ` ``，可直接复制到小红书。链接用 `[文字](url)`。**必须包含安装命令**（npx skills add ...）。**不含 hashtag**（用户发布时自选）
   - **输出**：写入 `<输出目录>/blocks.json` 与 `<输出目录>/xhs-copy.md`

5. **渲染**：`python .cursor/skills/xhs-render/scripts/render_images.py <输出目录>/blocks.json -t <用户所选模板> -o <输出目录>`

## blocks.json Schema

```json
[
  {"index": 1, "total": N, "text": "...", "title": "...", "role": "cover", "skill": "humanizer-zh", "emoji": "✨"},
  {"index": i, "total": N, "text": "...", "title": "", "role": "content", "emoji": ""},
  {"index": N, "total": N, "text": "...", "title": "", "role": "ending", "emoji": "📌"}
]
```

- **role**: cover（仅第 1 块）| content | ending（若仅为 hashtag 则跳过渲染）
- **title、emoji**：均可为空，由你判断
- 脚本按 blocks.json 渲染，纯标签页自动跳过

**设计约束**（LLM 设计时需遵守）：Cover text ≤ 2 行且须体现 skill 名；多要点用 `\n\n` 分隔；ending 放致谢开发者、不放安装命令；页数可多可少

## xhs-copy 规范

- 纯文本格式，存为 `xhs-copy.md`，内容无 markdown 语法
- 与配图内容一致，可直接复制到小红书作为发帖正文
- 不含 hashtag（用户发布时自选）

## 依赖

- `html2image`（`pip install html2image`）
- Chrome 或 Edge 浏览器

## 模板

| 名称 | 说明 |
|------|------|
| ing-minimal | Ing 品牌简约，页眉「线—Ing—线」，支持 LaTeX 数学公式（推荐） |
| ing-notion | Ing 井字格背景，知识卡片风，内容直接显示在网格上 |
| ing-skillshare | Ing 技能分享风，点阵背景、&lt; skills share 标签、Ing 水印、带圆点排版 |
| minimal | share 品牌，与 ing-minimal 同款，水印为 share |
| notion | share 品牌，与 ing-notion 同款，水印为 share |
| skillshare | share 品牌，与 ing-skillshare 同款，水印为 share |

纯标签页自动跳过，无页码。

## 异常与处理

渲染失败时根据错误信息处理：缺 Python → 提示安装；缺 html2image → **询问用户是否安装**，同意后 `pip install html2image` 再重试；pip 安装失败 → 提示可能版本冲突；其他 → 根据报错说明。不做预检查。

脚本、模板、参考文档均在本目录内。
