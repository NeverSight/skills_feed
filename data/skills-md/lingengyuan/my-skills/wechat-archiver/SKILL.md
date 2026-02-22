---
name: wechat-archiver
description: Archives WeChat Official Account articles to knowledge base with auto-generated structured notes. Use when users provide WeChat article URLs (mp.weixin.qq.com) or mention archiving/saving WeChat articles. Combines wechat2md scraper and note-creator for complete workflow.
allowed-tools:
  - Bash(python3:*, mkdir:*, cp:*, rm:*, cat:*)
  - Read
  - Write
  - Edit
  - Glob
  - Skill
---

# wechat-archiver (Wrapper Skill)

## Purpose
一键归档微信公众号文章到知识库，自动生成结构化笔记。

此 skill 是一个 **wrapper/orchestrator**，负责：
1. 调用 `wechat2md` 抓取原始文章
2. 统一路径管理、幂等性控制
3. 调用 `note-creator` 生成结构化笔记
4. 聚合所有产物到单一资产目录

**核心原则**：
- ✅ 幂等性：同一 URL 重复抓取不会产生混乱
- ✅ 可追溯：保留原文、图片、运行日志
- ✅ 单一资产目录：所有文件集中在同一目录便于 review
- ✅ 增量友好：支持批量重跑、更新

---

## Dependencies
此 skill MUST 依赖以下 skills：
- `wechat2md/SKILL.md` - 抓取微信文章并转换为 Markdown
- `note-creator/SKILL.md` - 生成结构化笔记

---

## Inputs

### 单篇模式
- `article_url` (必填): 微信公众号文章 URL (mp.weixin.qq.com)
- `target_folder` (可选): 目标文件夹，默认 `20-阅读笔记`
- `force` (可选, bool): 强制重新生成笔记，默认 false
- `canvas` (可选): canvas 生成策略，默认 `auto`
  - `auto`: 根据关键词规则自动判断
  - `on`: 总是生成
  - `off`: 不生成
- `base` (可选): base 生成策略，默认 `auto`
  - `auto`: 根据关键词规则自动判断
  - `on`: 总是生成
  - `off`: 不生成

### 批量模式
- `inbox_file` (必填): 包含微信文章链接的 markdown 文件路径
- `target_folder` (可选): 目标文件夹，默认 `20-阅读笔记`
- `dry_run` (可选, bool): 预览模式，不实际处理
- `force` (可选, bool): 强制重新处理已完成的 URL
- `mark_done` (可选, bool): 处理后标记源文件，默认 true

详见 `references/batch-processing.md`

---

## Output Contract

**CRITICAL: Output paths are relative to CURRENT WORKING DIRECTORY (CWD)**

所有输出 MUST 写入到：

```
outputs/<target_folder>/<slug>/
  ├── article.md              # 原始文章（从 wechat2md 复制/移动）
  ├── images/                 # 图片文件夹（从 wechat2md 复制/移动）
  ├── note.md                 # 结构化笔记（note-creator 生成）
  ├── diagram.canvas          # 可选：文章逻辑结构图
  ├── table.base              # 可选：文章要点/概念表
  ├── meta.json               # 统一元数据（merge wrapper + note-creator）
  └── run.jsonl               # 运行日志（每次运行追加一行）
```

其中：
- `<slug>` = `YYYYMMDD-<标题slug>-<asset_id前6位>`
  - 例：`20260111-understanding-async-a1b2c3`
- `<asset_id>` = `sha1(normalized_url)`
  - 用于幂等性判断的主键

---

## Algorithm (Strict Execution Checklist)

### 0) 前置检查
- 验证 `article_url` 是否为有效的微信公众号 URL
- 如果不是 `mp.weixin.qq.com` 域名，报错并退出

### 1) 调用 wechat2md 抓取文章

```bash
python3 .claude/skills/wechat2md/tools/wechat2md.py "<article_url>"
```

期望输出：
- `outputs/<title>/<title>.md` - 原始 Markdown
- `images/<title>/` - 图片文件夹

读取输出：
- 提取 `article_title`（从 MD 文件名或内容）
- 记录 `temp_md_path`、`temp_images_dir`

### 2) 生成 asset_id 和 slug

```python
import hashlib

# Normalize URL (移除追踪参数等)
normalized_url = normalize_url(article_url)
asset_id = hashlib.sha1(normalized_url.encode()).hexdigest()

# Generate slug
date_prefix = datetime.now().strftime("%Y%m%d")
title_slug = sanitize_title(article_title, max_len=50)
asset_id_short = asset_id[:6]
slug = f"{date_prefix}-{title_slug}-{asset_id_short}"
```

### 3) 创建统一资产目录

```bash
asset_dir = "<cwd>/outputs/<target_folder>/<slug>/"
mkdir -p "${asset_dir}"
```

### 4) 统一文件到资产目录

```bash
# 复制原始文章
cp "${temp_md_path}" "${asset_dir}/article.md"

# 复制图片文件夹
cp -r "${temp_images_dir}" "${asset_dir}/images/"

# CRITICAL: Fix image paths in article.md
# wechat2md generates images with ./images/ prefix (portable relative path)
# After copying images to same directory as article.md, links work correctly
# No path replacement needed!

# 清理临时目录
rm -rf "outputs/<title>/"  # wechat2md 的临时输出
```

### 5) 计算哈希并判断幂等性

```python
# 计算 article.md 内容哈希
with open(f"{asset_dir}/article.md", "r", encoding="utf-8") as f:
    content = f.read()
hash_content = hashlib.sha1(content.encode()).hexdigest()

# 检查是否存在历史 meta.json
meta_path = f"{asset_dir}/meta.json"
if os.path.exists(meta_path) and not force:
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    if meta.get("hash_content") == hash_content:
        # 内容未变化，跳过 note-creator
        log_run("skipped", "content unchanged")
        return success(asset_dir, "skipped")
```

### 6) 调用 note-creator 生成结构化笔记

如果需要生成笔记（首次运行或内容变化或 force=true）：

**Step 6.1: 决定 artifact_plan**

```python
# 读取 article.md 内容
article_content = read_file(f"{asset_dir}/article.md")

# 决定 canvas
if canvas == "on":
    canvas_enabled = True
elif canvas == "off":
    canvas_enabled = False
else:  # auto
    canvas_keywords = ["流程", "步骤", "架构", "原理", "时序", "sequence", "flow", "architecture"]
    canvas_enabled = any(kw in article_content for kw in canvas_keywords)

# 决定 base
if base == "on":
    base_enabled = True
elif base == "off":
    base_enabled = False
else:  # auto
    base_keywords = ["对比", "比较", "清单", "要点", "总结", "术语", "vs", "对比表"]
    base_enabled = any(kw in article_content for kw in base_keywords)

# 构建 artifact_plan
artifact_plan = ["md"]
if canvas_enabled:
    artifact_plan.append("canvas")
if base_enabled:
    artifact_plan.append("base")
```

**Step 6.2: 调用 note-creator**

通过 `Skill(note-creator)` 调用，传入：
- `user_prompt`: 基于 article.md 内容生成的摘要提示词
- `optional_context_files`: [`article.md`]
- 额外上下文：
  - `title`: `article_title`
  - `folder`: `target_folder`
  - `artifact_plan`: `artifact_plan`
  - `target_slug`: `slug`
  - `output_to_same_dir`: true  # 告知 note-creator 输出到同一目录

**注意**: note-creator 会生成 `note.md`、`diagram.canvas`、`table.base`、`meta.json` 到同一资产目录。

### 7) 合并 meta.json

```python
# 读取 note-creator 生成的 meta.json
note_meta = read_json(f"{asset_dir}/meta.json")

# 构建统一的 meta.json
unified_meta = {
    # Article metadata
    "asset_id": asset_id,
    "url": article_url,
    "title": article_title,
    "published_at": extract_date(article_content),  # 尝试从文章提取
    "ingested_at": datetime.now().isoformat(),
    "hash_content": hash_content,

    # Note-creator metadata (merge)
    "category": note_meta.get("category", "article"),
    "tags": note_meta.get("tags", []),
    "properties": note_meta.get("properties", {}),

    # Artifact plan
    "artifact_plan": artifact_plan,

    # Run info
    "last_run_at": datetime.now().isoformat(),
    "last_run_status": "success",
}

write_json(f"{asset_dir}/meta.json", unified_meta)
```

### 8) 记录运行日志

```jsonl
{"timestamp": "2026-01-11T10:30:00", "action": "ingest", "asset_id": "a1b2c3...", "status": "success", "hash_content": "...", "artifact_plan": ["md", "canvas"]}
{"timestamp": "2026-01-11T11:00:00", "action": "update", "asset_id": "a1b2c3...", "status": "skipped", "reason": "content unchanged"}
```

### 9) 清理临时文件

```bash
# 删除 wechat2md 的临时输出（如果还残留）
rm -rf "outputs/<title>/"
```

### 10) 输出执行摘要

返回给用户：
- 资产目录路径
- 生成的文件列表
- 运行状态（success/skipped/updated）
- 如果生成了 canvas/base，提示用户

---

## File Writing Rules (CRITICAL)

- 每个步骤的文件 MUST 实际写入到磁盘
- 使用绝对路径或确保在 CWD 下使用正确的相对路径
- 不允许只输出内容不写文件
- `run.jsonl` 每次运行追加一行，不覆盖历史

---

## Hard Constraints

### 幂等性
- 相同 URL 必须生成相同的 `asset_id`
- 相同内容（`hash_content`）默认跳过 `note-creator`
- `force=true` 时跳过幂等检查

### 目录结构
- 所有文件 MUST 在同一个 `<slug>` 目录下
- 不允许分散存放
- `article.md` MUST 保留（不可删除）

### Meta.json
- MUST 包含 `asset_id`、`hash_content`、`url`
- MUST merge note-creator 的元数据
- 更新时保留历史字段（如 `first_ingested_at`）

### Artifact Plan
- `note.md` MUST 始终生成
- `canvas`/`base` 默认 `auto`，根据关键词规则判断
- 规则定义在 `rules/classification.md`

---

## Error Handling

### wechat2md 失败
- 记录错误到 `run.jsonl`
- 不创建资产目录
- 向用户返回错误信息

### note-creator 失败
- 保留 `article.md` 和 `images/`
- 记录错误到 `run.jsonl`
- `meta.json` 中标记 `last_run_status: "failed"`
- 向用户返回部分成功状态

### 文件冲突
- 如果资产目录已存在但 `meta.json` 缺失或损坏：
  - 警告用户
  - 询问是否覆盖或跳过

---

## Examples

### Example 1: 首次抓取
```bash
User: "抓取这个微信文章：https://mp.weixin.qq.com/s/xxx"
Action:
  1. 调用 wechat2md → 获得 "Understanding Async.md"
  2. 生成 slug: "20260111-understanding-async-a1b2c3"
  3. 创建 "outputs/20-阅读笔记/20260111-understanding-async-a1b2c3/"
  4. 复制 article.md + images/
  5. 检测到 "async" 关键词 → canvas=on
  6. 调用 note-creator → 生成 note.md + diagram.canvas
  7. 写入 meta.json + run.jsonl
Output: "✅ 归档成功：outputs/20-阅读笔记/20260111-understanding-async-a1b2c3/"
```

### Example 2: 重复抓取（幂等）
```bash
User: "再次抓取同一个 URL"
Action:
  1. 生成相同的 asset_id
  2. 发现资产目录已存在
  3. 计算 hash_content = 历史记录中的 hash
  4. 跳过 note-creator
  5. 追加运行日志到 run.jsonl
Output: "⏭️ 内容未变化，跳过生成笔记"
```

### Example 3: 强制更新
```bash
User: "强制重新生成笔记"
Action:
  1. 忽略 hash_content 检查
  2. 重新调用 note-creator
  3. 覆盖 note.md / diagram.canvas / table.base
  4. 更新 meta.json
Output: "🔄 已更新笔记"
```

### Example 4: 批量处理 inbox.md
```bash
User: "把 inbox.md 里的微信文章都归档一下"
Action:
  1. 读取 inbox.md，提取所有 mp.weixin.qq.com 链接
  2. 去重并过滤已处理的 URL
  3. 逐个调用 wechat_archiver 处理
  4. 更新 inbox.md 标记已完成项
Output: "✅ 批量归档完成：处理 5 篇，跳过 2 篇，失败 0 篇"
```

**批量处理命令**：
```bash
# 预览
python3 .claude/skills/wechat-archiver/tools/batch_archiver.py --inbox inbox.md --dry-run

# 执行
python3 .claude/skills/wechat-archiver/tools/batch_archiver.py --inbox inbox.md
```

---

## Templates

See `templates/` directory:
- `execution-flow.md` - 执行流程模板
- `meta-merge.md` - meta.json 合并规则
- `classification-rules.md` - canvas/base 自动判断规则
