---
name: mixseek-config-validate
description: MixSeekの設定ファイル（team.toml、orchestrator.toml、evaluator.toml、judgment.toml）を検証します。「設定を検証」「TOMLをチェック」「設定ファイルの確認」「バリデーション」「ワークスペースの検証」といった依頼で使用してください。TOML構文とMixSeekスキーマへの準拠を確認します。
license: Apache-2.0
compatibility: Requires mixseek-core or mixseek-plus. Python 3.13+, uv recommended.
metadata:
  author: mixseek
  version: "1.0.0"
---

# MixSeek 設定検証

## 概要

MixSeek-Coreの設定ファイルがTOML構文およびMixSeekスキーマに準拠しているかを検証します。TOML構文エラー、必須フィールドの欠落、値の範囲外エラーなどを検出し、修正方法を提案します。

## 前提条件

- MixSeek-Coreがインストールされていること
- 検証対象の設定ファイルが存在すること
- Pythonコマンドが利用可能であること（`detect-python-command` スキルで判別）

## 対応ファイルタイプ

| ファイルタイプ | 説明 | パス例 |
|---------------|------|--------|
| team | チーム設定 | `configs/agents/team-*.toml` |
| orchestrator | オーケストレーター設定 | `orchestrator.toml` |
| evaluator | 評価設定 | `configs/evaluators/evaluator.toml` |
| judgment | 判定設定 | `configs/judgment/judgment.toml` |

## 使用方法

### Step 1: 検証対象の確認

ユーザーにどのファイルを検証するか確認:

```
検証対象のファイルを指定してください:
- 特定ファイル: configs/agents/team-web-research.toml
- 全設定: すべての設定ファイル
```

### Step 2: 検証の実行

`detect-python-command` スキルの `run-python.sh` を使用して検証を実行します：

```bash
# 特定ファイルの検証
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-config-validate/scripts/validate-config.py <file-path>

# ファイルタイプを指定して検証
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-config-validate/scripts/validate-config.py <file-path> --type team
```

### Step 3: 結果の報告

検証結果をユーザーに報告:

- **成功時**: 検証項目と結果を表示
- **失敗時**: エラー内容と修正方法を提案

## 検証項目

### TOML構文検証

- 基本構文の正しさ
- 文字列のクォート
- 配列・テーブルの形式
- コメントの形式

### スキーマ検証

| 項目 | 説明 |
|------|------|
| 必須フィールド | 必要なフィールドが存在するか |
| フィールド型 | 値の型が正しいか |
| 値の範囲 | 数値が許容範囲内か |
| 形式 | モデル形式など特殊形式の検証 |
| 一意性 | agent_name等の一意性 |
| 整合性 | min_rounds <= max_rounds 等 |

## 例

### 単一ファイルの検証

```
User: team.tomlを検証して

Agent: configs/agents/team-web-research.toml を検証します...

       ✅ TOML構文: OK
       ✅ 必須フィールド: OK
         - team.team_id: "team-web-research"
         - team.team_name: "Web Research Team"
         - team.leader.model: "google-gla:gemini-2.5-pro"
       ✅ モデル形式: OK
       ✅ Member Agent数: 2/15
       ✅ agent_name一意性: OK

       検証成功: この設定ファイルは有効です。
```

### エラーがある場合

```
User: team.tomlを検証して

Agent: configs/agents/team-broken.toml を検証します...

       ❌ エラーが検出されました:

       1. 必須フィールド欠落
          - team.members[0].tool_description が未定義
          - 修正: tool_description = "エージェントの説明" を追加

       2. 値の範囲外
          - team.max_concurrent_members = 100 (範囲: 1-50)
          - 修正: 1〜50の値に変更

       3. モデル形式エラー
          - team.leader.model = "gemini-pro" (無効)
          - 修正: "google-gla:gemini-2.5-pro" 形式に変更
```

### 全ファイル検証

```
User: すべての設定ファイルを検証して

Agent: ワークスペース内の設定ファイルを検証します...

       configs/agents/team-web-research.toml
       ✅ 有効

       configs/agents/team-analysis.toml
       ❌ エラー: member[0].agent_type が無効な値 "search"
          → 有効な値: plain, web_search, code_execution, web_fetch, custom

       configs/evaluators/evaluator.toml
       ✅ 有効

       configs/judgment/judgment.toml
       ✅ 有効

       orchestrator.toml
       ✅ 有効

       結果: 4/5 ファイルが有効
```

## エラーメッセージと修正方法

### TOML構文エラー

```
Error: Invalid TOML at line 15
```

**原因**: TOML構文が無効
**修正**: 該当行の構文を確認（クォート、ブラケット等）

### 必須フィールド欠落

```
Error: Missing required field: team.leader.system_instruction
```

**修正**: 指定されたフィールドを追加

```toml
[team.leader]
system_instruction = "指示内容"
```

### 型エラー

```
Error: Field 'temperature' must be float, got string
```

**修正**: 値の型を修正

```toml
# 誤り
temperature = "0.7"

# 正しい
temperature = 0.7
```

### 範囲エラー

```
Error: Field 'max_rounds' must be 1-10, got 15
```

**修正**: 値を許容範囲内に変更

### モデル形式エラー

```
Error: Invalid model format: "gemini-pro"
Expected format: "provider:model-name"
```

**修正**: `provider:model-name` 形式に変更

```toml
# 誤り
model = "gemini-pro"

# 正しい
model = "google-gla:gemini-2.5-pro"
```

### 重み合計エラー

```
Error: Metric weights must sum to 1.0, got 0.8
```

**修正**: 重みの合計が1.0になるよう調整

## CLIコマンド（直接実行）

```bash
# 単一ファイル検証
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-config-validate/scripts/validate-config.py path/to/config.toml

# タイプ指定
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-config-validate/scripts/validate-config.py config.toml --type team

# JSON出力
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-config-validate/scripts/validate-config.py config.toml --json

# 詳細出力
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-config-validate/scripts/validate-config.py config.toml --verbose
```

## トラブルシューティング

### スクリプトが実行できない

```
Error: No module named 'mixseek'
```

**解決方法**:
1. MixSeek-Coreがインストールされているか確認
2. `uv sync` を実行して依存関係を更新

### ファイルが見つからない

```
Error: File not found
```

**解決方法**:
1. ファイルパスが正しいか確認
2. `$MIXSEEK_WORKSPACE`からの相対パスを使用

## 参照

- **Pythonコマンド判別**: `skills/detect-python-command/SKILL.md`
- チーム設定スキーマ: `skills/mixseek-team-config/references/TOML-SCHEMA.md`
- オーケストレーター設定スキーマ: `skills/mixseek-orchestrator-config/references/TOML-SCHEMA.md`
- 評価設定スキーマ: `skills/mixseek-evaluator-config/references/TOML-SCHEMA.md`
