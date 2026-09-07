---
name: capmap-lint
description: >-
  校验 docs_root 文档体系：断链、能力底图 §1↔状态 Tag、活跃方案变更记录、
  README 底图、活跃/归档同名冲突。适用于「文档 lint」「检查文档体系」「跑 capmap-lint」。
  主源仓库为 capmap-skills；脚本与 CI action 均在本 skill 目录。
---

# capmap-lint — 文档体系校验

原则：[capmap-system](../capmap-system/SKILL.md)  
配置：`capmap-system/capmap.yaml`（由 capmap-init 生成；示例见仓库 `examples/`）  
契约：[status-tags](../capmap-system/reference/status-tags.md) · [lifecycle](../capmap-system/reference/lifecycle.md)

## 本目录

| 文件 | 职责 |
|------|------|
| `capmap_lint.py` | 校验脚本 |
| `action.yml` | GitHub composite action（setup + `--strict`） |
| `SKILL.md` | 本说明 |

## 启动

1. 配置由脚本自动读取（`capmap-system/capmap.yaml`）
2. 在**仓库根**执行：

```bash
python .agents/skills/capmap-lint/capmap_lint.py
python .agents/skills/capmap-lint/capmap_lint.py --json
python .agents/skills/capmap-lint/capmap_lint.py --strict   # CI：warn 也失败
```

3. 先修 **error**，再处理 **warn**（CI `--strict` 两者都要清）
4. 修完后重跑直至通过

## CI

- **逻辑与命令**：本目录 `action.yml`
- **GitHub 入口**（平台强制路径，仅薄封装）：`.github/workflows/capmap-lint.yml` → `uses: ./.agents/skills/capmap-lint`

## 检查项（与 V2 契约一致）

| code | 级 | 含义 |
|------|----|------|
| docs_root / theme_map | error | 配置或主题底图缺失 |
| readme_map | error | 用 README.md 当底图 |
| wikilink / md_link | error | 活跃区断链（`_archive` 为 warn） |
| status_sync / status_tag | error | 底图 §1 ↔ YAML `状态/*` |
| change_log | error | 活跃方案缺 `## 变更记录` |
| active_archive_dupe | error | 活跃与归档同名双副本 |
| escaped_pipe / scheme_tag / scheme_status / test_status / wikilink_ambiguous | warn | 建议修 |
| status_tag / map_status_tag | error | 方案主状态合法；**底图禁止状态 Tag**；测试须 测试中\|已验证；归档须 已归档 |
| status_skip | error | 落地中/已落地跳过验证门（关联测试仍为测试中或未已验证且无免测） |

## 叙事（修状态时）

- **能力进度** → 只改能力底图 §1（并同步该底图 YAML `状态/*` 集合）
- **方案文档生命周期** → 只改该方案文首单个 `状态/*`
- 二者不必字面相同（见 status-tags / lifecycle）

## 不做

- 不代替 capmap-backfill 写 §4
- 不自动改文件（只报告）；修复由 Agent/人按报错改
