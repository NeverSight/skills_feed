---
name: abs-journal
description: Use when user asks to recommend academic journals for paper submission, update the ABS/AJG journal database, or mentions "推荐期刊", "投稿建议", "journal recommendation", "ABS评级", "AJG评级".
---

# abs-journal

## Core Rules

- 默认推荐 **只使用本地 AJG CSV**（`assets/data/ajg_<year>_journals_core_custom.csv`），不得自动联网更新。
- 只有当用户明确提出 **更新/重新抓取/刷新/更新数据库/更新ABS(AJG)数据** 时，才运行抓取脚本更新 `assets/data/`。
- 抓取登录凭据仅通过环境变量 `AJG_EMAIL` / `AJG_PASSWORD` 提供；不要在文件中写入明文密码。
- 命令行示例默认使用 **项目根相对路径**（数据仍在 `assets/data/`；推荐产出统一在 `reports/`），仅在用户明确要求时使用绝对路径并注明基准。
- 推荐流程为：脚本导出主题贴合候选池 → AI 仅在候选池内二次筛选 → 子集校验 → 三段固定列报告。

## 参数职责（避免混淆）

- `--field`：论文领域标签/关键词配置（默认 `ECON`）。**不控制候选期刊范围**。
- `--field_scope`：候选期刊 Field 白名单（AJG CSV 的 `Field` 列；逗号分隔；精确匹配）。为空则使用默认白名单：
  `ECON, FINANCE, PUB SEC, REGIONAL STUDIES, PLANNING AND ENVIRONMENT, SOC SCI`（共 5 个 Field；其中 `REGIONAL STUDIES, PLANNING AND ENVIRONMENT` 是一个整体 Field 名称）。

## Quick Start

### A) 校验 AI 输出并生成最终报告（固定列三段 Top10）

```bash
python3 scripts/abs_journal.py \
  recommend \
  --field_scope "ECON,FINANCE,PUB SEC,REGIONAL STUDIES, PLANNING AND ENVIRONMENT,SOC SCI" \
  --title "你的论文标题" \
  --abstract "你的摘要（可选）" \
  --mode medium \
  --topk 10 \
  --rating_filter ""  \
  --hybrid \
  --export_candidate_pool_json "candidate_pool.json" \
  --ai_output_json "ai_output.json" \
  --ai_report_md "ai_report.md" \
  --auto_ai
```

### B) 更新 AJG/ABS 数据库（仅在用户明确要求时）

```bash
export AJG_EMAIL="你的账号"
export AJG_PASSWORD="你的密码"

python3 scripts/ajg_fetch.py \
  --outdir "$(pwd)/assets/data"
```

## Workflow

1) 解析用户意图：
   - 若用户只说“推荐投稿期刊/帮我选期刊”，走 **混合推荐流程**（不更新）。
   - 若用户明确说“更新/重新抓取/刷新数据库”，走 **更新+（可选）推荐流程**。
2) 混合推荐流程：
   - 读取本地 AJG CSV → 先构造“主题贴合候选池”并导出 JSON（满足 field/星级过滤等约束）。
   - 候选期刊默认来自固定 Field 白名单：`ECON, FINANCE, PUB SEC, REGIONAL STUDIES, PLANNING AND ENVIRONMENT, SOC SCI`（可用 `--field_scope` 覆盖）。
   - `--field` 仅作为论文领域标签/关键词配置，不控制候选范围。
   - 星级过滤（重要）：`--rating_filter` **留空** 时，会按 mode 自动分层（easy=1,2；medium=2,3；hard=4,4*）；若 **显式传入** `--rating_filter`，则会覆盖默认分层，可能导致三段星级过滤一致（不符合 easy/medium/hard 分层预期）。
   - AI **只能在候选池内** 输出三类 TopK（easy/medium/hard），并为每条补充 `推荐理由`（解释性摘要）。三类默认各 10 本且不重叠。
   - 脚本做 **候选池子集校验**（禁止候选池外期刊）；通过后生成固定列 Markdown 报告：
     `序号 | 期刊名 | ABS星级 | Field | 推荐理由`。
     - `Field`: AJG CSV 的领域分类（如 ECON, FINANCE），用于快速定位期刊所属领域
     - `推荐理由`: AI 根据论文内容生成，说明该期刊与论文的匹配度
3) 更新流程：
   - 检查 `AJG_EMAIL/AJG_PASSWORD` 是否存在；缺失则给出可复制的 export 提示。
   - 运行抓取脚本写入 `assets/data/`。
   - （可选）运行离线校验脚本确认输出契约。

## References (Load Only If Needed)

- 抓取/更新 AJG 数据库（显式触发才运行）：`references/ajg_fetch.md`
- 投稿期刊推荐（默认本地数据）：`references/abs_journal_recommend.md`
- AJG 数据输出契约与离线校验：`references/ajg_data_contract.md`
- 常见失败排查（gate/验证码/环境变量）：`references/troubleshooting.md`
- 推荐输出示例：`assets/recommendation_example.md`
