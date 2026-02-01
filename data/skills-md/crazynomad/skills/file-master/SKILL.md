---
name: file-master
description: Mac 文件管理大师 - 将磁盘清理、文件整理、文档分析串成「清 → 理 → 知」三阶段工作流
---

# File Master - Mac 文件管理大师

将 disk-cleaner、file-organizer、doc-mindmap 三个技能串成「清 → 理 → 知」三阶段工作流，一次搞定 Mac 文件管理。

## When to Use

**仅当用户明确需要多阶段组合流程时使用此技能。** 如果用户只想做单一任务（只清理磁盘、只整理文件、只分析文档），请直接使用对应的子技能（disk-cleaner / file-organizer / doc-mindmap），不要使用 file-master。

Use this skill when users:
- 明确要求**组合操作**："先清理再整理"、"清理完帮我归类文件"
- 说"帮我**全面**整理一下电脑"、"来个文件**大扫除**"（强调全面/完整）
- 想**一次性**完成清理 + 整理 + 归档中的至少两个阶段
- 说"磁盘快满了**还有**一堆文件没整理"（多个诉求并存）

**不要使用此技能** 当用户只说：
- "清理磁盘" / "释放空间" → 使用 disk-cleaner
- "整理文件" / "整理下载文件夹" → 使用 file-organizer
- "分析文档" / "文档转换" → 使用 doc-mindmap

触发关键词: 全面整理电脑, 一站式整理, 文件大扫除, 先清理再整理, 完整文件管理流程

## Features

- **三阶段工作流** - 清(释放空间) → 理(归类文件) → 知(文档智能分析)
- **灵活选择** - 可执行全部三阶段，也可选择任意阶段组合
- **预览优先** - 每个阶段先预览再执行，用户完全掌控
- **阶段联动** - Phase 2 整理的路径自动传递给 Phase 3 分析
- **容错设计** - 某阶段失败或跳过不影响后续阶段
- **最终报告** - 汇总三阶段成果，一目了然

## Usage

自然语言触发即可，Claude 会引导完成整个流程：

```
帮我全面整理一下电脑          → 执行全部三阶段
帮我清理磁盘再整理文件        → Phase 1 + Phase 2
整理一下文件然后做个文档分析  → Phase 2 + Phase 3
只帮我做文档分析              → Phase 3
```

## Dependencies

三个子技能各自的依赖：

### Phase 1 - disk-cleaner
- macOS, Homebrew
- Mole (`brew install tw93/tap/mole`)
- Python: `pip install jinja2`

### Phase 2 - file-organizer
- macOS
- Python 3.8+

### Phase 3 - doc-mindmap
- Python 3.10+
- markitdown: `pip install 'markitdown[all]'`
- Ollama: `brew install ollama` + `ollama pull qwen2.5:3b`
- requests: `pip install requests`

## Claude Workflow

Claude 使用此技能时，严格按以下步骤执行。

### 第 0 步：欢迎 + 阶段选择

向用户展示三阶段概览，询问要执行哪些阶段：

```
Mac 文件管理大师 - 三阶段工作流

Phase 1 「清」 - 磁盘清理，释放硬盘空间 (disk-cleaner)
Phase 2 「理」 - 文件整理，归类下载文件夹 (file-organizer)
Phase 3 「知」 - 文档分析，批量转换 + 摘要 + 分类 (doc-mindmap)

请选择：
1. 全部执行（推荐）
2. 选择部分阶段
3. 只执行某个阶段
```

如果用户选择部分阶段，记录要执行的阶段列表，跳过未选中的阶段。

---

### Phase 1「清」- 磁盘清理

使用 disk-cleaner 技能释放硬盘空间。

#### 1.1 预览扫描

```bash
python disk-cleaner/scripts/mole_cleaner.py --check
python disk-cleaner/scripts/mole_cleaner.py --preview
```

向用户展示扫描结果，包括可清理空间大小和分类。

#### 1.2 选择清理档位

```
请选择清理档位：
1. Air - 最安全，只清浏览器缓存和日志
2. Pro - 推荐，平衡安全与空间
3. Max - 最大化释放空间
4. 跳过此阶段
```

#### 1.3 执行清理

用户选择档位后执行：

```bash
python disk-cleaner/scripts/mole_cleaner.py --clean --tier <air|pro|max> --confirm
```

#### 1.4 Phase 1 小结

报告释放了多少空间，然后进入 Phase 2。

---

### Phase 2「理」- 文件整理

使用 file-organizer 技能归类文件。

#### 2.1 预览扫描

```bash
python file-organizer/scripts/file_organizer.py --status
```

向用户展示下载文件夹中的文件状况。

#### 2.2 选择整理模式

```
请选择整理模式：
1. 手动模式 - 创建智能文件夹，自己拖拽整理
2. 自动模式 - 自动按类型分类到桌面文件夹
3. 跳过此阶段
```

#### 2.3 执行整理

**手动模式**：
```bash
python file-organizer/scripts/file_organizer.py --manual
```

**自动模式**：
```bash
# 先预览
python file-organizer/scripts/file_organizer.py --auto --dry-run
# 用户确认后执行
python file-organizer/scripts/file_organizer.py --auto
```

自动模式执行后，整理路径会自动写入 disk-cleaner 白名单，保护已整理的文件。

#### 2.4 Phase 2 小结

报告整理了多少文件、分了哪些类别。**记录输出路径**（如 `~/Desktop/已整理文件-YYYYMMDD/`），供 Phase 3 使用。

---

### Phase 3「知」- 文档分析

使用 doc-mindmap 技能进行文档智能分析。

#### 3.0 确定目标目录

- 如果 Phase 2 已执行：自动使用 Phase 2 的输出路径
- 如果 Phase 2 跳过：询问用户要分析哪个目录

#### 3.1 预览文档

```bash
python doc-mindmap/scripts/doc_converter.py <目标路径> --preview
```

展示文档列表、类型分布、重复文件检测结果。

#### 3.2 执行转换

```bash
python doc-mindmap/scripts/doc_converter.py <目标路径> --convert --confirm
```

#### 3.3 生成摘要

```bash
python doc-mindmap/scripts/doc_converter.py <目标路径> --summarize
```

#### 3.4 三维度分类

```bash
# 先展示分类结果
python doc-mindmap/scripts/doc_converter.py <目标路径> --organize
```

询问用户是否使用 AI 建议的文件名。如果同意：

```bash
python doc-mindmap/scripts/doc_converter.py <目标路径> --organize --rename
```

#### 3.5 Finder 预览

询问用户是否在 Finder 中预览分类目录：

```bash
cp -a <.summaries/schemes> ~/Desktop/文档分类-$(date +%Y%m%d)
open ~/Desktop/文档分类-$(date +%Y%m%d)
```

#### 3.6 Phase 3 小结

报告转换了多少文档、生成了多少摘要、分类结果概览。

---

### 最终总结

汇总三阶段成果，向用户展示：

```
=== Mac 文件管理大师 - 完成报告 ===

Phase 1「清」: 释放了 X.XX GB 磁盘空间
Phase 2「理」: 整理了 N 个文件到 M 个分类
Phase 3「知」: 转换了 K 个文档，生成 K 份摘要，三维度分类完成

所有阶段执行完毕！
```

跳过的阶段标注"已跳过"，失败的阶段标注错误原因。

## Error Handling

- 某阶段依赖未安装时，提示用户安装命令，询问是否跳过该阶段继续
- 某阶段执行出错时，记录错误信息，询问用户是否继续下一阶段
- Phase 3 依赖 Ollama 本地模型，如果未安装则跳过摘要和分类步骤，只做转换

## Credits

- [disk-cleaner](../disk-cleaner/) - 磁盘清理
- [file-organizer](../file-organizer/) - 文件整理
- [doc-mindmap](../doc-mindmap/) - 文档智能分析
