---
name: checkpointing
description: |
  Save session context to agent configuration files or create full checkpoint files.
  Supports three modes: session history (default), full checkpoint (--full),
  and skill analysis (--full --analyze) for extracting reusable patterns.
metadata:
  short-description: Checkpoint session context with skill extraction support
---

# Checkpointing — セッションコンテキストの永続化

**セッション中の作業履歴を保存し、再利用可能なスキルパターンを発見します。**

## モード

### Mode 1: Session History（デフォルト）

CLI相談履歴を各エージェントの設定ファイルに追記。

```
┌─────────────────────────────────────────────────────────────┐
│  .claude/logs/cli-tools.jsonl                               │
│                      ↓                                      │
│  /checkpointing                                             │
│                      ↓                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │  CLAUDE.md   │ │ AGENTS.md    │ │ GEMINI.md            │ │
│  │ ## Session   │ │ ## Session   │ │ ## Session           │ │
│  │ History      │ │ History      │ │ History              │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Mode 2: Full Checkpoint（--full）

作業全体の包括的なスナップショットを作成。

```
┌─────────────────────────────────────────────────────────────┐
│  Data Sources:                                              │
│  ├─ git log (commits)                                       │
│  ├─ git diff (file changes)                                 │
│  └─ cli-tools.jsonl (Codex/Gemini logs)                     │
│                      ↓                                      │
│  /checkpointing --full                                      │
│                      ↓                                      │
│  .claude/checkpoints/2026-01-28-153000.md                   │
│  ├─ Summary (commits, files, consultations)                 │
│  ├─ Git History (commits list)                              │
│  ├─ File Changes (created, modified, deleted)               │
│  └─ CLI Consultations (Codex/Gemini)                        │
└─────────────────────────────────────────────────────────────┘
```

### Mode 3: Skill Analysis（--full --analyze）

チェックポイントからスキル化できるパターンを発見。

```
┌─────────────────────────────────────────────────────────────┐
│  /checkpointing --full --analyze                            │
│                      ↓                                      │
│  1. Full Checkpoint を生成                                   │
│  2. 分析用プロンプトを生成                                    │
│     → .claude/checkpoints/YYYY-MM-DD-HHMMSS.analyze-prompt.md│
│                      ↓                                      │
│  3. サブエージェントでAI分析を実行                            │
│     → 作業パターンを発見                                      │
│     → スキル候補を提案                                        │
│                      ↓                                      │
│  4. 新スキルを .claude/skills/ に追加                         │
└─────────────────────────────────────────────────────────────┘
```

**発見するパターン例:**
- テスト→実装の繰り返し（TDDワークフロー）
- リサーチ→設計→実装の流れ
- 特定ファイルセットの同時変更
- CLI相談→コード変更のシーケンス

## 使い方

```bash
# Session History モード（デフォルト）
/checkpointing

# Full Checkpoint モード
/checkpointing --full

# Skill Analysis モード（推奨）
/checkpointing --full --analyze

# 期間指定
/checkpointing --since "2026-01-26"
/checkpointing --full --analyze --since "2026-01-26"
```

### Skill Analysis の実行フロー

```bash
# Step 1: チェックポイント + 分析プロンプト生成
python checkpoint.py --full --analyze

# Step 2: サブエージェントで分析（Claudeが自動実行）
# → 分析プロンプトを読み込み
# → スキル候補を提案
# → ユーザーが承認したらスキルを生成
```

## 処理内容

### Session History モード

1. `.claude/logs/cli-tools.jsonl` を解析
2. Codex/Geminiへの相談内容を日付ごとに整理
3. 各エージェント設定ファイルに `## Session History` を追記

### Full Checkpoint モード

1. **Git情報を収集**
   - `git log` でコミット履歴
   - `git diff --name-status` でファイル変更
   - `git diff --numstat` で行数変更

2. **CLI相談ログを解析**
   - Codex相談内容とステータス
   - Gemini調査内容とステータス

3. **チェックポイントファイルを生成**
   - `.claude/checkpoints/YYYY-MM-DD-HHMMSS.md`

## Full Checkpoint フォーマット

```markdown
# Checkpoint: 2026-01-28 15:30:00 UTC

## Summary
- **Commits**: 5
- **Files changed**: 12 (8 modified, 3 created, 1 deleted)
- **Codex consultations**: 3
- **Gemini researches**: 2

## Git History

### Commits
- `abc1234` Add checkpointing enhancement
- `def5678` Update documentation

### File Changes

**Created:**
- `new_feature.py` (+120)

**Modified:**
- `checkpoint.py` (+80, -20)
- `SKILL.md` (+45, -10)

**Deleted:**
- `old_script.py`

## CLI Tool Consultations

### Codex (3 consultations)
- ✓ 設計: チェックポイント拡張アーキテクチャ
- ✓ デバッグ: Git log parsing issue

### Gemini (2 researches)
- ✓ 調査: Git integration best practices
```

## Session History フォーマット

```markdown
## Session History

### 2026-01-26

**Codex相談:**
- ✓ サブエージェントパターンでCodex/Gemini呼び出しを推奨...

**Gemini調査:**
- ✓ MCP vs CLI比較調査...
```

## 実行タイミング

| タイミング | 推奨モード |
|-----------|-----------|
| セッション終了前 | `--full --analyze` |
| 重要な設計決定後 | `--full` |
| 大きな機能実装完了後 | `--full --analyze` |
| 長時間作業の区切り | `--full` |
| 繰り返しパターンを感じた時 | `--full --analyze` |
| 日次の軽い記録 | デフォルト |

## 注意事項

- ログが空の場合は何も追記されません
- 既存の `## Session History` セクションは上書きされます
- ログファイル自体は変更されません（読み取りのみ）
- Full Checkpoint は `.claude/checkpoints/` に蓄積されます
- Git未初期化プロジェクトでもCLIログ部分は動作します
- `--analyze` で生成されたスキル提案は人間がレビューしてから採用すること
- スキル分析はパターンを固定せず、AIが自由に発見する設計
