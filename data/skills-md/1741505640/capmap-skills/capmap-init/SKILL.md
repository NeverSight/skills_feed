---
name: capmap-init
description: >-
  初始化或对齐仓库文档根目录（docs_root 名任意）：选定并写入 .agents/skills/capmap-system/capmap.yaml，
  创建文档首页、主题能力底图、规范/运维/归档索引、gitignore、可选 Obsidian（含 graph.json 状态颜色组）。
  适用于「初始化 docs」「整理文档目录」「按能力底图体系建文档」「对齐文档结构」时使用。
---

# capmap-init — 初始化 / 对齐

原则：[capmap-system](../capmap-system/SKILL.md)  
契约：[directory-contract](../capmap-system/reference/directory-contract.md)  
配置：[project-config](../capmap-system/reference/project-config.md)  
模板：[templates](../capmap-system/reference/templates.md) · Tag：[status-tags](../capmap-system/reference/status-tags.md)

## 第一件事：统一 docs_root

目录叫什么**无所谓**，但**一个仓库只能有一个**，且必须持久化：

1. 询问用户：文档根目录相对仓库根叫什么？（例：`docs` / `doc` / `handbook` / `aigc-maop-server`）
2. 若已存在 `.agents/skills/capmap-system/capmap.yaml` → 读取并确认是否沿用
3. 若磁盘上已有文档树但无配置 → 探测候选目录（含 `文档首页.md` 或 `方案/能力底图-*`），请用户确认后写入配置
4. **写入/更新** `.agents/skills/capmap-system/capmap.yaml` 的 `docs_root`（及其他字段）
5. 之后本 Skill 与其它 capmap-* **只使用该路径**

不要默认「一定叫 docs」。

## 模式

| 模式 | 条件 | 行为 |
|------|------|------|
| **新建** | docs_root 不存在或为空 | 创建完整骨架 + 写配置 |
| **对齐检查** | 已有体系 + 已有配置 | 对照契约列缺口，只补缺失 |

## 执行前确认的参数

| 参数 | 说明 |
|------|------|
| `docs_root` | **必填**，任意合法目录名 |
| `themes[]` | 可空；有则生成对应能力底图空壳 |
| `main_branch` | 默认 `develop` |
| `obsidian` | 默认 true |
| gitignore | 是否按 docs_root 放开知识文档、只忽略产物 |

## Obsidian（`obsidian: true` 时必做）

模板在本 Skill 目录：[`assets/obsidian/graph.json`](assets/obsidian/graph.json)（图谱颜色组按状态 Tag / 文档类型着色）。

1. 确保目录 `<docs_root>/.obsidian/` 存在  
2. **写入 / 对齐** `<docs_root>/.obsidian/graph.json`：  
   - **新建**：整文件复制自 `assets/obsidian/graph.json`  
   - **对齐**：若已有 `graph.json`，合并补齐缺失的 `colorGroups` 项（按 `query` 去重）；**不要**清空用户已调的力学 / 缩放参数  
3. 写 `Obsidian使用说明.md`（说明 Vault=`docs_root`、状态 Tag、图谱颜色组已预置）

颜色组与 [status-tags](../capmap-system/reference/status-tags.md) 一致：方案主状态、测试轨、`能力底图` / `规范` / 各类索引等。

## Checklist

```
- [ ] 1. 选定 docs_root（询问 / 探测 / 确认）
- [ ] 2. 写入 .agents/skills/capmap-system/capmap.yaml
- [ ] 3. 创建 <docs_root>/ 下：方案/<主题>、测试/<主题>、规范、交付、运维、_archive/方案
- [ ] 4. 写 文档首页.md（须含 `## Inbox · 未立项` **开干指令**空表，见 templates）、能力总览.md、方案/测试/规范等 *索引.md；对齐时若首页缺该节则补空表，不覆盖已有行
- [ ] 5. 每主题 能力底图-<可读名>.md；文件名唯一；禁止 README 当底图；空壳文首 `tags: [能力底图]`（无 §1 行则暂不写 `状态/*`）
- [ ] 6. 若 obsidian=true：复制 assets/obsidian/graph.json → <docs_root>/.obsidian/graph.json（对齐则合并 colorGroups）；写 Obsidian使用说明.md
- [ ] 7. gitignore：针对 <docs_root>
- [ ] 8. 验收：配置可解析；闭环目录（方案/测试/规范/归档）齐全；obsidian 时 graph.json 含状态颜色组
- [ ] 9. 若对齐已有文档：方案文首回链底图；底图 §0/文首用唯一文件名挂方案；无 Obsidian 孤儿
```

## 不负责

- 不根据已有方案正文**推断并填满**底图 §1 / `状态/*`（存量补全用 capmap-backfill / capmap-scheme）
- 方案 / 开发标识 / 测试 / 规范 / 反补 / 归档 → 见 capmap-scheme、capmap-dev、capmap-test、capmap-norm、capmap-backfill、capmap-archive

## 对齐检查输出格式

```markdown
## 文档根对齐结果
- docs_root（配置）：…
- 已存在：…
- 缺失（将创建）：…
- Obsidian graph.json：已写入 / 已合并 colorGroups / 跳过
- 违规：如 方案/xx/README.md 当作底图
- 跳过（不覆盖）：…
```
