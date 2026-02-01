---
name: mixseek-model-list
description: MixSeek-Coreで利用可能なLLMモデルの一覧を表示します。「使えるモデル」「モデル一覧」「どのモデルがある」「モデルを取得」「APIからモデル」といった依頼で使用してください。API経由でプロバイダー別のモデル情報を動的取得し、推奨設定、互換性情報を提供します。
license: Apache-2.0
compatibility: Requires mixseek-core or mixseek-plus. Python 3.13+, uv recommended.
metadata:
  author: mixseek
  version: "1.0.0"
---

# MixSeek モデル一覧

## 概要

MixSeek-Coreで利用可能なLLMモデルの一覧を提供します。API経由で最新のモデル情報を動的に取得し、プロバイダー別のモデル情報、用途別の推奨設定、agent_typeとの互換性情報を確認できます。

**FR-008準拠**: Google Gemini、Anthropic Claude、OpenAI、Grokの各プロバイダーからAPI経由でモデル一覧を取得。

**Article 6準拠**: APIキー未設定やAPI失敗時は明示的にエラーを報告します（暗黙的フォールバックなし）。

## 前提条件

### 環境変数（API取得に必要）

APIからモデル一覧を取得する場合、対応する環境変数を設定:

| プロバイダー | 環境変数 | 備考 |
|-------------|---------|------|
| Google | `GOOGLE_API_KEY` | |
| Anthropic | `ANTHROPIC_API_KEY` | |
| OpenAI | `OPENAI_API_KEY` | |
| Grok | `GROK_API_KEY` | |
| Groq | `GROQ_API_KEY` | `gsk_` で始まる（mixseek-plus拡張） |
| Tavily | `TAVILY_API_KEY` | `tvly-` で始まる。web_search系で必要（オプション） |
| ClaudeCode | - | CLI認証のため環境変数不要（mixseek-plus拡張） |

**注意**: 環境変数が未設定の場合、該当プロバイダーは明示的にエラーを報告します。

## 使用方法

### Step 1: 環境変数の確認

APIキーが設定されているか確認:

```bash
# 設定状況を確認
echo "GOOGLE_API_KEY: ${GOOGLE_API_KEY:+設定済み}"
echo "ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:+設定済み}"
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:+設定済み}"
echo "GROK_API_KEY: ${GROK_API_KEY:+設定済み}"
```

### Step 2: 要件の確認

ユーザーの用途を確認:

1. **全モデル一覧**: すべてのプロバイダーのモデルを表示
2. **プロバイダー指定**: 特定プロバイダーのモデルのみ表示
3. **用途別推奨**: Leader/Member/Evaluator等の用途に適したモデル
4. **API経由取得**: 最新のモデル情報をAPIから取得

### Step 3: モデル情報の取得

**スクリプトによるAPI取得（推奨）:**

```bash
# 全プロバイダーからモデル取得（MixSeek形式）
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-model-list/scripts/fetch-models.py

# 特定プロバイダーのみ
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-model-list/scripts/fetch-models.py --provider google

# JSON形式で出力
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-model-list/scripts/fetch-models.py --json

# 詳細出力（エラー情報も表示）
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-model-list/scripts/fetch-models.py --verbose --format text
```

## CLIコマンドリファレンス

```
fetch-models.py [OPTIONS]

OPTIONS:
  --provider TEXT    プロバイダー指定: google, anthropic, openai, grok, all
                     (default: all)
  --format TEXT      出力形式: text, json, csv, mixseek
                     (default: mixseek)
  --json             --format json のショートカット
  --verbose, -v      詳細出力（エラー情報も表示）
```

### 出力形式

| 形式 | 説明 | 用途 |
|------|------|------|
| `mixseek` | `provider:model-id` 形式（1行1モデル） | チーム設定への直接コピー |
| `json` | JSON形式（メタデータ含む） | プログラム連携 |
| `text` | プロバイダー別の詳細表示 | 人間が読む用 |
| `csv` | CSV形式 | スプレッドシート等 |

## モデル形式

MixSeek-Coreでは以下の形式でモデルを指定します:

```
provider:model-name
```

| プロバイダー | プレフィックス | 環境変数 | 代表モデル |
|-------------|---------------|---------|-----------|
| Google | `google-gla` | `GOOGLE_API_KEY` | `gemini-2.5-pro`, `gemini-2.5-flash` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` | `claude-sonnet-4-5`, `claude-haiku-4-5` |
| OpenAI | `openai` | `OPENAI_API_KEY` | `gpt-4o`, `gpt-4o-mini` |
| Grok | `grok` | `GROK_API_KEY` | `grok-3`, `grok-3-mini` |
| Groq | `groq` | `GROQ_API_KEY` | `llama-3.3-70b-versatile`, `qwen/qwen3-32b` |
| ClaudeCode | `claudecode` | - （CLI認証） | `claude-sonnet-4-5`, `claude-haiku-4-5` |

**注意**: Groq と ClaudeCode は **mixseek-plus 拡張プロバイダー**です。mixseek-core単体では利用できません。

**利用可能なモデル一覧は `fetch-models.py` スクリプトで取得してください。**

## プロバイダー特性

| プロバイダー | 特徴 |
|-------------|------|
| Google | 高品質・安定。Leader Agent / Evaluator向け |
| Anthropic | `code_execution` agent_type に完全対応 |
| OpenAI | 安定・汎用性が高い |
| Grok | Web検索機能内蔵モデルあり |
| Groq | 低レイテンシ・高速推論。リアルタイム応答向け（mixseek-plus拡張） |
| ClaudeCode | 組み込みツール（Bash、ファイル操作、Web検索）統合。開発タスク向け（mixseek-plus拡張） |

## 用途別推奨

### Leader Agent

タスクの調整・指示を行うリーダー向け。高品質（`-pro`系）なモデルを推奨。

### Member Agent

タスク実行を担当するメンバー向け。高速・コスト効率（`-flash`、`-mini`系）を推奨。

### code_execution Agent

コード実行が必要な場合。**Anthropicモデルのみ対応**。

### Evaluator / Judgment

評価・判定向け。安定性・一貫性のある高品質モデルを推奨。

### リアルタイム応答（mixseek-plus拡張）

低レイテンシが必要な場合。**Groqモデル**を推奨。`groq:llama-3.3-70b-versatile` など。

### 開発タスク自動化（mixseek-plus拡張）

ファイル操作、コマンド実行、Web検索を組み合わせた開発タスク。**ClaudeCodeモデル**を推奨。組み込みツールにより複雑なワークフローを自動化。

## agent_type互換性

### mixseek-core標準タイプ

| agent_type | Google | Anthropic | OpenAI | Grok |
|------------|--------|-----------|--------|------|
| `plain` | ✓ | ✓ | ✓ | ✓ |
| `web_search` | ✓ | ✓ | ✓ | ✓ |
| `code_execution` | ✗ | ✓ | ✗ | ✗ |
| `web_fetch` | ✓ | ✓ | ✓ | ✓ |
| `custom` | ✓ | ✓ | ✓ | ✓ |

**注意**: `code_execution`はAnthropicモデルのみ対応

### mixseek-plus拡張タイプ

| agent_type | Groq | ClaudeCode | 説明 |
|------------|------|------------|------|
| `groq_plain` | ✓ | - | Groq基本エージェント。高速推論 |
| `groq_web_search` | ✓ | - | Groq + Tavily検索統合 |
| `tavily_search` | ✓ | ✓ | Tavily API検索特化 |
| `claudecode_plain` | - | ✓ | ClaudeCode基本エージェント |
| `claudecode_tavily_search` | - | ✓ | ClaudeCode + Tavily検索統合 |
| `custom` | ✓ | ✓ | カスタムツール統合 |

**注意**: 拡張タイプは **mixseek-plus** でのみ利用可能です。

## 例

### 全モデル一覧の取得

```bash
# スクリプトを実行してAPIから最新のモデル一覧を取得
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-model-list/scripts/fetch-models.py --format text
```

出力例:
```
[GOOGLE]
  Prefix: google-gla
  Models:
    - gemini-2.5-pro: Gemini 2.5 Pro
    - gemini-2.5-flash: Gemini 2.5 Flash
    ...

[ANTHROPIC]
  Prefix: anthropic
  Models:
    - claude-sonnet-4-5-...: Claude Sonnet 4.5 [code_exec]
    ...
```

### code_execution対応モデルの確認

```bash
# JSON形式で取得し、code_exec_compatible を確認
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-model-list/scripts/fetch-models.py --provider anthropic --json
```

**ポイント**: `code_exec_compatible: true` のモデルが `code_execution` agent_type に対応

### チーム設定での使用例

```toml
[[team.members]]
agent_name = "coder"
agent_type = "code_execution"
model = "anthropic:<model-id>"  # fetch-models.py で取得したモデルIDを使用
```

## トラブルシューティング

### APIキーエラー（fetch-models.py）

```
Error [google]: Error: GOOGLE_API_KEY environment variable is not set.
```

**解決方法**:
対応する環境変数を設定:
```bash
export GOOGLE_API_KEY="your-api-key"
export ANTHROPIC_API_KEY="your-api-key"
export OPENAI_API_KEY="your-api-key"
export GROK_API_KEY="your-api-key"
```

### API接続エラー

```
Error [google]: <urlopen error ...>
```

**原因と解決方法**:
- ネットワーク接続を確認
- プロキシ設定を確認（企業環境の場合）
- APIキーの有効性を確認
- 他のプロバイダーが成功していれば、そのモデルのみ出力されます

### API認証エラー（401/403）

```
Warning: API fetch failed for openai: HTTP Error 401: Unauthorized
```

**解決方法**:
- APIキーが正しく設定されているか確認
- APIキーの有効期限を確認
- APIキーの権限（スコープ）を確認

### タイムアウトエラー

```
Error [anthropic]: timed out
```

**解決方法**:
- ネットワーク接続を確認
- 後で再試行
- 特定のプロバイダーのみ指定: `--provider openai`

### MixSeek設定時のAPIキーエラー

```
Error: API key not found for provider: google-gla
```

**解決方法**:
対応する環境変数を設定してからMixSeekを実行

### モデルが見つからない

```
Error: Unknown model: invalid-model
```

**解決方法**:
- `provider:model-name` 形式を確認
- 有効なモデル名を使用（このスキルで確認）

### code_execution非対応エラー

```
Error: code_execution not supported for model: google-gla:...
```

**解決方法**:
- Anthropicモデルに変更（`code_execution`はAnthropicのみ対応）
- `fetch-models.py --provider anthropic` で対応モデルを確認

## mixseek-plus拡張

このセクションは **mixseek-plus** 固有の機能について説明します。mixseek-core単体では利用できません。

### 拡張プロバイダー

| プロバイダー | 特徴 | 主なユースケース |
|-------------|------|-----------------|
| **Groq** | 低レイテンシ・高速推論。LPU（Language Processing Unit）による高速化 | リアルタイム応答、大量バッチ処理 |
| **ClaudeCode** | 組み込みツール統合。Bash実行、ファイル操作、Web検索を標準装備 | 開発タスク自動化、コードベース探索 |

### 拡張agent_type

| agent_type | プロバイダー | 説明 |
|------------|-------------|------|
| `groq_plain` | Groq | 基本的な対話。高速推論が必要な場合 |
| `groq_web_search` | Groq | Tavily APIを使用したWeb検索統合 |
| `tavily_search` | Groq / ClaudeCode | Tavily検索特化エージェント |
| `claudecode_plain` | ClaudeCode | 基本的な対話。組み込みツール使用可能 |
| `claudecode_tavily_search` | ClaudeCode | ClaudeCode + Tavily検索統合 |

### チーム設定例（mixseek-plus）

```toml
# Groqエージェント（高速応答）
[[team.members]]
agent_name = "fast_responder"
agent_type = "groq_plain"
model = "groq:llama-3.3-70b-versatile"

# ClaudeCodeエージェント（開発タスク）
[[team.members]]
agent_name = "developer"
agent_type = "claudecode_plain"
model = "claudecode:claude-sonnet-4-5"

# Tavily検索エージェント
[[team.members]]
agent_name = "researcher"
agent_type = "tavily_search"
model = "groq:llama-3.3-70b-versatile"
```

### 注意事項

- **mixseek-plusの依存関係**: これらの機能を使用するには `mixseek-plus` パッケージが必要です
- **環境変数**: Groqは `GROQ_API_KEY`、Tavilyは `TAVILY_API_KEY` が必要
- **ClaudeCode認証**: Claude CLI認証を使用。環境変数は不要ですが、`claude` コマンドが認証済みである必要があります
- **互換性**: mixseek-core標準のagent_typeとは互換性がありません。拡張タイプ専用のプロバイダーを使用してください

## 参照

- スクリプト: `scripts/fetch-models.py`
- チーム設定: `skills/mixseek-team-config/`
- 評価設定: `skills/mixseek-evaluator-config/`
