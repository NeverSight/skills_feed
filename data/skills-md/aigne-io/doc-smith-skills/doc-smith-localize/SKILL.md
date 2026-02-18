---
name: doc-smith-localize
description: Translate Doc-Smith generated documentation into multiple languages. Use this skill when the user requests document translation, localization, or multi-language support. Supports batch translation of documents and images.
---

# Doc-Smith 文档翻译

将文档翻译成多种语言，支持批量翻译和术语一致性。

## 用法

```bash
/doc-smith-localize --lang en                    # 翻译所有文档到英文
/doc-smith-localize -l en -l ja                  # 翻译到多个语言
/doc-smith-localize -l en -p /overview           # 只翻译指定文档
/doc-smith-localize -l en --force                # 强制重新翻译
/doc-smith-localize -l en --skip-images          # 跳过图片翻译
```

## 选项

| 选项 | 别名 | 说明 |
|------|------|------|
| `--lang <code>` | `-l` | 目标语言代码（可多次使用） |
| `--path <docPath>` | `-p` | 指定文档路径（可多次使用） |
| `--force` | `-f` | 强制重新翻译，覆盖已有 |
| `--skip-images` | | 跳过图片翻译 |

## 约束

以下约束在任何操作中都必须满足。

### 1. Workspace 约束

- `.aigne/doc-smith/config.yaml` 和 `planning/document-structure.yaml` 必须存在
- 不存在时提示用户先使用 `/doc-smith` 生成文档

### 2. 参数验证约束

- 目标语言不能与源语言（config.yaml 的 locale）相同
- `--path` 指定的路径必须存在于 document-structure.yaml
- 过滤后无有效语言时报错

### 3. 增量翻译约束

- 基于源 HTML 的 SHA256 hash（sourceHash）判断是否需要翻译
- hash 未变化的文档自动跳过（除非 `--force`）
- 翻译失败时不覆盖已有翻译、不修改 .meta.yaml

### 4. Task 分发约束

- 每个文档到每种语言为一个独立翻译任务
- 通过 Task(references/translate-document.md) 分发，**所有翻译 Task 必须使用 `run_in_background: true`**，避免执行日志回流到主 agent 上下文
- 每批最多并行 5 个 Task，超过时分批执行
- 如有术语表（`.aigne/doc-smith/glossary.yaml` 或 `.md`），传递给每个 Task

信号文件机制：
- 每个 Task 完成时在 `.aigne/doc-smith/cache/task-status/` 写入 `{slug}.status` 文件
- slug 规则：docPath 去除 `/` 前缀后以 `-` 替换 `/`，再拼接 `-{targetLang}`（如 `/api/overview` → `en` = `api-overview-en`）
- 状态文件内容为 1 行摘要（如 `/overview → en: 成功 | hash: abc123`）
- 主 agent 通过轮询 `.status` 文件判断 Task 是否完成（见"批次执行流程"）

### 5. 图片翻译约束

- 未指定 `--skip-images` 时，扫描 assets 中的图片资源
- 跳过条件（满足任一）：`generation.shared: true`、目标语言已存在、源语言图片不存在
- 使用 `/doc-smith-images --update` 翻译图片文字
- 翻译后更新图片 .meta.yaml 的 languages 和 translations

### 6. Config 更新约束

- 翻译完成后，将目标语言添加到 config.yaml 的 `translateLanguages` 数组
- 避免重复添加已存在的语言
- 更新后验证 config.yaml 正确

### 7. nav.js 重建约束

- Config 更新后**必须**执行 nav.js 重建：
  ```bash
  node skills/doc-smith-build/scripts/build.mjs \
    --nav --workspace .aigne/doc-smith --output .aigne/doc-smith/dist
  ```
- 验证 `dist/assets/nav.js` 包含所有目标语言的 code
- **此步骤是语言切换功能生效的关键，绝不能跳过**

## HTML-to-HTML 翻译模型

翻译直接在 HTML 层面完成，不经过 MD 中间步骤：

```
源 HTML → 提取可翻译区域 → 翻译 → 组装目标 HTML → 保存
dist/{source}/docs/{path}.html → dist/{target}/docs/{path}.html
```

**可翻译区域**（4 个）：
- `<title>` 标签内文本
- `<meta name="description">` 的 content 属性
- `<main data-ds="content">` 标签内 HTML
- `<nav data-ds="toc">` 标签内 HTML

**不翻译**：head 资源引用、script、header/footer/sidebar、HTML 属性、代码块中的代码

## 翻译质量要求

- 术语一致性：使用术语表保持专业术语统一
- HTML 结构保持：标签原样保留，只翻译文本内容
- 上下文理解：根据技术文档语境选择合适译法
- 自然流畅：翻译结果符合目标语言习惯

## 关键流程

### 并行翻译文档

每个翻译任务使用单独的 Task tool 生成（≤ 5 个并行，> 5 个分批）。**必须使用 `run_in_background: true` 分发 Task**。必须使用以下模板构造 Task prompt：

```
你是文档翻译代理。请先用 Read 工具读取 {TRANSLATE_DOC_MD_PATH} 作为你的完整工作流程，然后严格按照其中的步骤执行。

你的翻译任务参数如下：
- docPath：{DOC_PATH}
- targetLanguage：{TARGET_LANG}
- sourceLanguage：{SOURCE_LANG}
- force：{FORCE}
- glossary：{GLOSSARY}
- 状态文件路径：{STATUS_FILE_PATH}

完成检查清单（必须在写入状态文件前逐项确认）：
□ 步骤 2 增量检查：已验证是否需要翻译
□ 步骤 3 提取：已提取 4 个可翻译区域
□ 步骤 4 翻译：已完成翻译并保持 HTML 结构
□ 步骤 5 组装：已保存目标语言 HTML
□ 步骤 6 Meta：已更新 .meta.yaml
□ 状态文件：已将 1 行摘要写入 {STATUS_FILE_PATH}
```

**模板变量说明**：
- `{TRANSLATE_DOC_MD_PATH}`：`references/translate-document.md` 的绝对路径
- `{DOC_PATH}`：文档路径，如 `/overview`
- `{TARGET_LANG}`：目标语言代码，如 `en`
- `{SOURCE_LANG}`：源语言代码，如 `zh`
- `{FORCE}`：是否强制翻译
- `{GLOSSARY}`：术语表内容（如有）
- `{STATUS_FILE_PATH}`：`.aigne/doc-smith/cache/task-status/{slug}.status`

### 批次执行流程

#### 准备阶段

分发第一个 Task 前：
1. `mkdir -p .aigne/doc-smith/cache/task-status`
2. `rm -f .aigne/doc-smith/cache/task-status/*.status`（清空旧状态）

#### 分发阶段

每个 Task 使用 `run_in_background: true` 分发。批次内所有 Task 同时启动。

#### 等待阶段

每 15 秒检查 `.status` 文件数量：

```bash
ls .aigne/doc-smith/cache/task-status/*.status 2>/dev/null | wc -l
```

- 文件数 = 当前批次任务数 → 该批次完成
- 超时：单批最多等待 10 分钟，超时后报告缺失文档
- **不要读取后台 Task 的 output_file**（可能 300K+），只读 `.status` 文件

#### 收集结果

```bash
cat .aigne/doc-smith/cache/task-status/*.status
```

每个文件 1 行，所有翻译摘要汇总后通常不超过 20 行。

#### 失败处理

- `.status` 内容以"失败"开头 → 记录失败原因，不阻塞后续批次
- 超时未产生 `.status` → 标记为超时，在最终报告中提示用户重试

### 翻译图片

```bash
/doc-smith-images "将图片中的文字从 {source} 翻译成 {target}，保持布局和风格不变" \
  --update .aigne/doc-smith/assets/{key}/images/{source}.png \
  --savePath .aigne/doc-smith/assets/{key}/images/{target}.png \
  --locale {target}
```

### 更新图片引用

翻译后 HTML 中的图片路径需更新语言后缀：
- 匹配 `images/{source}.png` → 替换为 `images/{target}.png`（仅当目标语言图片存在时）

### AI 巡检

翻译和 nav.js 重建完成后，读取 `dist/` 中生成的 HTML 文件（每种语言各抽查 1-2 个页面），检查输出是否符合预期。如有问题直接修改 HTML 文件修复。

### 翻译报告

返回翻译结果摘要，包含文档和图片的翻译/跳过/失败统计。

## 错误处理

- Workspace 不存在：提示先使用 `/doc-smith` 生成文档
- 目标语言与源语言相同：提示指定不同的语言
- 文档路径无效：列出有效路径供用户参考
- 翻译部分失败：报告失败文档，建议使用 `--path` 单独重试
