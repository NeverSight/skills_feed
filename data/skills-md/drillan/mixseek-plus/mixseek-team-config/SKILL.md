---
name: mixseek-team-config
description: MixSeekのチーム設定ファイル（team.toml）を生成します。「チームを作成」「エージェント設定を生成」「Web検索チームを作って」「分析チームを設定」といった依頼で使用してください。Leader AgentとMember Agentの構成を定義します。
license: Apache-2.0
compatibility: Requires mixseek-core or mixseek-plus. Python 3.13+, uv recommended.
metadata:
  author: mixseek
  version: "1.0.0"
---

# MixSeek チーム設定生成

## 概要

MixSeek-Coreのチーム設定ファイル（team.toml）を生成します。Leader AgentとMember Agentの構成、使用するモデル、システム指示などを定義します。

## 前提条件

- ワークスペースが初期化されていること（`mixseek-workspace-init`参照）
- 環境変数 `MIXSEEK_WORKSPACE` が設定されていること（推奨）

## 使用方法

### Step 1: 要件のヒアリング

ユーザーに以下を確認してください:

1. **チームの目的**: 何を達成するチームか
2. **必要なMember Agent**: どのような役割のエージェントが必要か
3. **使用モデル**: デフォルト（Gemini）を使用するか、特定のモデルを希望するか

### Step 2: チーム構成の提案

ユーザーの要件に基づいて、以下を提案:

- **team_id**: 一意のID（kebab-case推奨）
- **team_name**: 表示名
- **Leader Agent**: 指示とモデル
- **Member Agents**: 各エージェントの役割、タイプ、モデル

### Step 3: 設定ファイルの生成

以下のテンプレートを基に設定ファイルを生成:

```toml
[team]
team_id = "team-id"
team_name = "チーム名"
max_concurrent_members = 15

[team.leader]
system_instruction = """
あなたはチームのリーダーです。

## ツール呼び出しルール
| ツール名 | 用途 |
|---------|------|
| do_task | [役割]を実行 |

do_taskツールを使用してタスクを実行してください。
"""
model = "google-gla:gemini-2.5-pro"
temperature = 0.7
timeout_seconds = 300

[[team.members]]
agent_name = "member-name"      # 内部識別子（DB記録用）
agent_type = "plain"
tool_name = "do_task"           # ★ Leaderが呼び出す名前（system_instructionで使用）
tool_description = "このエージェントは[役割]を担当します"
model = "google-gla:gemini-2.5-flash"
system_instruction = """
あなたは[役割]を担当するエージェントです。
[詳細な指示]
"""
temperature = 0.2
```

#### agent_name vs tool_name（重要）

- **agent_name**: 内部識別子（ログ、DB記録用）
- **tool_name**: **Leaderが呼び出すツール名**（system_instructionで使用）

**Leaderのsystem_instructionでは必ず`tool_name`を使用してください。**

### Step 4: ファイルの保存

生成した設定を以下のパスに保存:

```bash
$MIXSEEK_WORKSPACE/configs/agents/team-<team-id>.toml
```

### Step 5: 設定ファイルの検証（必須）

**生成後は必ず検証を実行してください。**

```bash
uv run python skills/mixseek-config-validate/scripts/validate-config.py \
    $MIXSEEK_WORKSPACE/configs/agents/team-<team-id>.toml --type team
```

検証が成功したら、ユーザーに結果を報告します。失敗した場合は、エラー内容を確認して設定を修正してください。

## Member Agentタイプ

| タイプ | 説明 | 用途 |
|-------|------|------|
| `plain` | 基本テキスト生成 | 一般的な分析、要約、生成タスク |
| `web_search` | Web検索機能付き | 最新情報の取得、リサーチタスク |
| `code_execution` | コード実行機能付き | 計算、データ処理、スクリプト実行 |
| `web_fetch` | Webフェッチ機能付き | 特定URLからのデータ取得 |
| `custom` | カスタムプラグイン | 独自ツールの統合 |

詳細は `references/MEMBER-TYPES.md` を参照してください。

## 推奨モデル

| 用途 | モデル | 理由 |
|------|--------|------|
| Leader Agent | `google-gla:gemini-2.5-pro` | 高品質な指示理解と調整 |
| Member Agent（標準） | `google-gla:gemini-2.5-flash` | 高速レスポンス |
| Member Agent（高品質） | `google-gla:gemini-2.5-pro` | 複雑なタスク向け |
| コード実行 | `anthropic:claude-sonnet-4-5-20250929` | code_execution対応 |

## 例

### Web検索チームの作成

```
User: Web検索と分析ができるチームを作って

Agent: チーム設定を提案します:

       チームID: team-web-research
       チーム名: Web Research Team

       構成:
       - Leader Agent: gemini-2.5-pro（チーム調整）
       - web_researcher (web_search): Web検索担当
       - analyst (plain): 情報分析担当

       この構成でよろしいですか？

User: はい

Agent: 設定ファイルを生成しました:
       configs/agents/team-web-research.toml

       検証を実行します...
       ✅ 検証成功: 設定ファイルは有効です。

       実行コマンド:
       mixseek team "調べたいこと" --config configs/agents/team-web-research.toml
```

### 生成される設定ファイル例

```toml
[team]
team_id = "team-web-research"
team_name = "Web Research Team"
max_concurrent_members = 15

[team.leader]
system_instruction = """
あなたはWeb調査チームのリーダーです。

ユーザーからの質問に対して、以下の手順で調査を進めてください:
1. search_webツールで関連情報のWeb検索を実行
2. 取得した情報をanalyze_dataツールで分析
3. 分析結果を統合して、ユーザーに回答を提供

## ツール呼び出しルール
| ツール名 | 用途 |
|---------|------|
| search_web | Web検索を実行 |
| analyze_data | 情報を分析 |

各ツールを適切に使い分けてください。
"""
model = "google-gla:gemini-2.5-pro"
temperature = 0.7
timeout_seconds = 300

[[team.members]]
agent_name = "web_researcher"   # 内部識別子
agent_type = "web_search"
tool_name = "search_web"        # ★ Leaderが呼び出す名前
tool_description = "Web検索を実行し、最新の情報を取得します"
model = "google-gla:gemini-2.5-flash"
system_instruction = """
あなたはWeb検索の専門家です。
与えられたトピックについて、信頼性の高い情報源からの最新情報を検索してください。
検索結果には出典URLを含めてください。
"""
temperature = 0.2

[[team.members]]
agent_name = "analyst"          # 内部識別子
agent_type = "plain"
tool_name = "analyze_data"      # ★ Leaderが呼び出す名前
tool_description = "収集した情報を分析し、洞察を提供します"
model = "google-gla:gemini-2.5-flash"
system_instruction = """
あなたは情報分析の専門家です。
提供された情報を分析し、以下を含むレポートを作成してください:
- 主要なポイントの要約
- 情報の信頼性評価
- 結論と推奨事項
"""
temperature = 0.2
```

## トラブルシューティング

### チーム実行時にエラーが発生

1. **設定ファイルの検証**: `mixseek-config-validate`スキルで検証
2. **APIキーの確認**: 使用モデルに対応するAPIキーが設定されているか確認
3. **ワークスペースパス**: `MIXSEEK_WORKSPACE`が正しく設定されているか確認

### Member Agent数の制限

`max_concurrent_members`の範囲は1-50です。デフォルトは15です。
多数のエージェントを使用する場合は、この値を調整してください。

## 参照

- TOMLスキーマ詳細: `references/TOML-SCHEMA.md`
- Member Agentタイプ: `references/MEMBER-TYPES.md`
- 利用可能モデル: `skills/mixseek-model-list/references/VALID-MODELS.md`
