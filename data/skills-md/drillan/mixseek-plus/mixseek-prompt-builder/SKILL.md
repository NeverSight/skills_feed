---
name: mixseek-prompt-builder
description: MixSeekのプロンプトビルダー設定ファイル（prompt_builder.toml）を生成します。「プロンプトを設定」「プロンプトビルダーを作成」「ラウンド別プロンプト」といった依頼で使用してください。
license: Apache-2.0
compatibility: Requires mixseek-core or mixseek-plus. Python 3.13+, uv recommended.
metadata:
  author: mixseek
  version: "1.0.0"
---

# MixSeek プロンプトビルダー設定生成

## 概要

MixSeek-Coreのプロンプトビルダー設定ファイル（prompt_builder.toml）を生成します。3つのテンプレートを定義し、各コンポーネントへのプロンプト配信を制御します。

### テンプレートの役割

| テンプレート | 対象 | 用途 |
|-------------|------|------|
| `team_user_prompt` | Team (Leader Agent) | ラウンド別の指示、過去履歴の提示 |
| `evaluator_user_prompt` | Evaluator | 提出内容の評価指示 |
| `judgment_user_prompt` | Judgment Client | 継続・終了の判定指示 |

## 前提条件

- ワークスペースが初期化されていること（`mixseek-workspace-init`参照）
- 環境変数 `MIXSEEK_WORKSPACE` が設定されていること（推奨）
- orchestrator設定が存在すること（マルチラウンド機能を使用する場合）

## 生成ファイル

- パス: `$MIXSEEK_WORKSPACE/configs/prompt_builder.toml`

## 使用方法

### Step 1: 要件のヒアリング

ユーザーに以下を確認してください:

1. **用途**: どのようなタスクに使用するか（調査、分析、コード生成など）
2. **ラウンド戦略**: マルチラウンドで改善するか、単発実行か
3. **カスタム判定基準**: 終了条件に特別な基準があるか

### Step 2: テンプレートの選択

用途に応じてテンプレートを選択:

| テンプレート | 用途 | 特徴 |
|-------------|------|------|
| `default` | 一般的な競合形式 | リーダーボード参照、基本的なラウンド進行 |
| `deep-research` | Deep Research | ラウンド別検索キーワード改善、段階的深掘り |
| `single-round` | 単発実行 | シンプル構造、ラウンド変数の最小使用 |

### Step 3: カスタマイズ

必要に応じて以下をカスタマイズ:

- **Jinja2条件分岐**: `{% if round_number == 1 %}` などでラウンド別指示
- **変数の追加使用**: `{{ ranking_table }}` でリーダーボード表示
- **判定基準の調整**: judgment_user_promptの判定条件

### Step 4: ファイルの保存

生成した設定を以下のパスに保存:

```bash
$MIXSEEK_WORKSPACE/configs/prompt_builder.toml
```

### Step 5: 設定ファイルの検証

生成後は構文とプレースホルダーを確認:

```bash
# TOML構文の検証
uv run python -c "import tomllib; tomllib.load(open('configs/prompt_builder.toml', 'rb'))"

# Jinja2構文の検証（オプション）
uv run python -c "
from jinja2 import Environment
env = Environment()
import tomllib
config = tomllib.load(open('configs/prompt_builder.toml', 'rb'))
for key in ['team_user_prompt', 'evaluator_user_prompt', 'judgment_user_prompt']:
    env.parse(config['prompt_builder'][key])
print('OK')
"
```

## テンプレート種類

### default（デフォルト）

- 一般的なチーム競合形式
- リーダーボード参照あり
- 基本的なラウンド進行指示
- 用途: 汎用的なタスク

### deep-research

- Deep Research特化
- ラウンド1: 初期調査、広範な検索
- ラウンド2: キーワード改善、深掘り
- ラウンド3: 最終統合、検証
- 用途: 調査・リサーチタスク

### single-round

- 単発実行向け
- シンプルなプロンプト構造
- ラウンド変数の最小使用
- 用途: 一回きりのタスク

## 利用可能なJinja2変数

### Team / Judgment 共通変数

| 変数名 | 型 | 説明 |
|--------|-----|------|
| `user_prompt` | string | 元のユーザプロンプト |
| `round_number` | int | 現在のラウンド番号（1始まり） |
| `submission_history` | string | 過去のSubmission履歴（整形済み） |
| `ranking_table` | string | リーダーボード（整形済み） |
| `team_position_message` | string | チーム順位メッセージ |
| `current_datetime` | string | 現在日時（ISO 8601形式） |

### Evaluator専用変数

| 変数名 | 型 | 説明 |
|--------|-----|------|
| `user_prompt` | string | 元のユーザプロンプト |
| `submission` | string | 評価対象のエージェント提出内容 |
| `current_datetime` | string | 現在日時（ISO 8601形式） |

詳細は `references/JINJA2-VARIABLES.md` を参照してください。

## 例

### Deep Research設定例

```toml
[prompt_builder]
team_user_prompt = """
現在日時: {{ current_datetime }}

# タスク
{{ user_prompt }}

# ラウンド {{ round_number }}
{% if round_number == 1 %}
## 初期調査
- 広範な検索キーワードで情報収集
- 主要な情報源を特定
{% elif round_number == 2 %}
## 検索キーワード改善
- 前回の結果を分析し、より具体的なキーワードを使用
- 情報の空白を埋める
{% else %}
## 最終統合
- 情報を検証し、矛盾を解消
- 構造化された回答を作成
{% endif %}

# 過去の提出履歴
{{ submission_history }}
"""

evaluator_user_prompt = """
# 評価タスク
以下の提出内容を評価してください。

## ユーザタスク
{{ user_prompt }}

## 提出内容
{{ submission }}
"""

judgment_user_prompt = """
# 判定タスク
調査の継続が必要かどうかを判定してください。

## 判定基準
- 継続: 情報不足、重要な観点が欠落
- 終了: 十分な回答が可能

## ユーザタスク
{{ user_prompt }}

## 提出履歴
{{ submission_history }}

## リーダーボード
{{ ranking_table }}
"""
```

### カスタム判定基準例

```toml
judgment_user_prompt = """
# カスタム判定
以下の基準で継続・終了を判定してください。

## 終了条件（すべて満たす場合）
1. 3つ以上の情報源から確認が取れている
2. 数値データが含まれている
3. 最新情報（1年以内）が含まれている

## 継続条件（いずれかに該当）
1. 情報源が2つ以下
2. 推測や不確かな表現が多い
3. 重要な観点が欠落している

## ユーザタスク
{{ user_prompt }}

## 提出履歴
{{ submission_history }}
"""
```

## トラブルシューティング

Jinja2構文エラー、変数展開の問題、マルチラインTOML文字列については `references/JINJA2-VARIABLES.md` の「エラー回避」セクションを参照してください。

## 参照

- TOMLスキーマ詳細: `references/TOML-SCHEMA.md`
- Jinja2変数詳細: `references/JINJA2-VARIABLES.md`
- orchestrator設定: `skills/mixseek-orchestrator-config/SKILL.md`
- evaluator設定: `skills/mixseek-evaluator-config/SKILL.md`
