---
name: mixseek-debug
description: MixSeek-Plusのデバッグ機能を有効化し、ログ出力を制御します。「デバッグモードを有効化」「verbose」「ログを出力」「ログレベル」「デバッグ設定」といった依頼で使用してください。
license: Apache-2.0
compatibility: Requires mixseek-core or mixseek-plus. Python 3.13+, uv recommended.
metadata:
  author: mixseek
  version: "1.0.0"
---

# MixSeek デバッグ機能

## 概要

MixSeek-Plusは複数のデバッグ用環境変数を提供しています。これらを使用して、エージェント実行時の詳細なログ出力を有効化し、問題の診断や動作確認を行うことができます。

## 環境変数一覧

| 環境変数 | 値 | 効果 | スコープ |
|---------|-----|------|---------|
| `MIXSEEK_VERBOSE` | `1` または `true` | 統合デバッグモード | MCPツールログ + `mixseek.member_agents`(DEBUG) + `claudecode_model`(DEBUG) |
| `CLAUDECODE_MODEL_LOG_LEVEL` | `DEBUG` | claudecode-model単体のログ | claudecode-modelパッケージのみ |
| `MIXSEEK_LOGFIRE` | `1` または `true` | Logfireインストルメンテーション | pydantic-ai トレース（要Logfire設定） |

### 推奨設定

**通常のデバッグには `MIXSEEK_VERBOSE=1` のみで十分です。**

`MIXSEEK_VERBOSE=1` を設定すると、以下のログが有効化されます：
- MCPツール呼び出しの開始/完了ログ
- `mixseek.member_agents` ロガーのDEBUGレベル出力
- `claudecode_model` ロガーのDEBUGレベル出力

## 使用方法

### Step 1: 環境変数の確認

現在の環境変数設定を確認するには、以下のスクリプトを実行してください：

```bash
bash skills/mixseek-debug/scripts/check-debug-env.sh
```

### Step 2: CLI実行時の使用

#### 方法A: 環境変数を設定してCLI実行

```bash
# 統合デバッグモード（推奨）
MIXSEEK_VERBOSE=1 uv run mskp team "タスク" --config configs/agents/team.toml

# claudecode-model単体のデバッグ
CLAUDECODE_MODEL_LOG_LEVEL=DEBUG uv run mskp team "タスク" --config configs/agents/team.toml

# 複数の環境変数を組み合わせ
MIXSEEK_VERBOSE=1 MIXSEEK_LOGFIRE=1 uv run mskp team "タスク" --config configs/agents/team.toml
```

#### 方法B: シェルセッション全体に設定

```bash
# 現在のセッションに設定
export MIXSEEK_VERBOSE=1

# 以降のコマンドはすべてverboseモードで実行される
uv run mskp team "タスク" --config configs/agents/team.toml

# 無効化
unset MIXSEEK_VERBOSE
```

### Step 3: Python APIでの使用

```python
import mixseek_plus

# 方法A: enable_verbose_mode()を使用（推奨）
mixseek_plus.enable_verbose_mode()
mixseek_plus.patch_core()

# これ以降のClaudeCodeエージェントはverboseログを出力
# コンソール出力例:
# [Tool Start] fetch_page: url=https://example.com
# [Tool Done] fetch_page: success in 1234ms

# ファイル出力先: $WORKSPACE/logs/member-agent-YYYY-MM-DD.log

# verboseモードを無効化
mixseek_plus.disable_verbose_mode()
```

```python
import os
import mixseek_plus

# 方法B: 環境変数を直接設定
os.environ["MIXSEEK_VERBOSE"] = "1"
mixseek_plus.patch_core()

# 方法C: 一時的に有効化（コンテキストマネージャは非提供、手動管理）
os.environ["MIXSEEK_VERBOSE"] = "1"
try:
    # デバッグしたい処理
    pass
finally:
    del os.environ["MIXSEEK_VERBOSE"]
```

## ログ出力先

### コンソール出力

`MIXSEEK_VERBOSE=1` 時、以下のフォーマットでコンソールに出力されます：

```
[Tool Start] <tool_name>: <params>
[Tool Done] <tool_name>: <status> in <time>ms
[Tool Result Preview] <result_preview>
```

**例:**
```
[Tool Start] fetch_page: url=https://example.com/docs
[Tool Done] fetch_page: success in 2345ms
[Tool Result Preview] # Documentation\n\nWelcome to...
```

### ファイル出力

Member Agentのログは以下のファイルに出力されます：

```
$MIXSEEK_WORKSPACE/logs/member-agent-YYYY-MM-DD.log
```

**出力内容:**
- ツール呼び出しの詳細（パラメータ、実行時間、ステータス）
- エージェント実行のトレース情報
- エラーとスタックトレース

### claudecode_model ログ

`MIXSEEK_VERBOSE=1` 時、`claudecode_model` ロガーも自動的にDEBUGレベルに設定され、以下が出力されます：

```
claudecode_model - DEBUG - <message>
```

## 組み合わせ例

### 1. 基本的なデバッグ（最も一般的）

```bash
MIXSEEK_VERBOSE=1 uv run mskp team "Webページを取得して要約して" --config configs/agents/team.toml
```

### 2. Logfireトレースを追加

```bash
# 事前にLogfireの設定が必要
MIXSEEK_VERBOSE=1 MIXSEEK_LOGFIRE=1 uv run mskp team "タスク" --config configs/agents/team.toml
```

### 3. claudecode-model単体のデバッグ

他のログを抑制してclaudecode-modelのみをデバッグしたい場合：

```bash
CLAUDECODE_MODEL_LOG_LEVEL=DEBUG uv run mskp team "タスク" --config configs/agents/team.toml
```

## トラブルシューティング

### ログが出力されない

**原因1: 環境変数が正しく設定されていない**

```bash
# 確認
echo $MIXSEEK_VERBOSE

# 正しく設定
export MIXSEEK_VERBOSE=1
```

**原因2: patch_core()が呼び出されていない**

Python APIを使用する場合、`patch_core()` を呼び出す必要があります：

```python
import mixseek_plus
mixseek_plus.enable_verbose_mode()
mixseek_plus.patch_core()  # これを忘れないこと
```

**原因3: ログハンドラーが設定されていない**

Pythonのロギング設定を確認してください：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### ファイルログが見つからない

**原因: MIXSEEK_WORKSPACEが設定されていない**

```bash
# 確認
echo $MIXSEEK_WORKSPACE

# 設定
export MIXSEEK_WORKSPACE=/path/to/workspace

# ログファイルの場所
ls -la $MIXSEEK_WORKSPACE/logs/
```

### ログ出力が多すぎる

`MIXSEEK_VERBOSE=1` は多くのログを出力します。特定のコンポーネントのみをデバッグしたい場合：

```bash
# claudecode-model単体のみ
CLAUDECODE_MODEL_LOG_LEVEL=DEBUG uv run mskp team "タスク" --config configs/agents/team.toml
```

または、Pythonでロガーレベルを個別に制御：

```python
import logging

# 特定のロガーのみDEBUGに
logging.getLogger("claudecode_model").setLevel(logging.DEBUG)

# 他はINFOに抑制
logging.getLogger("mixseek.member_agents").setLevel(logging.INFO)
```

### Logfireトレースが表示されない

**原因: Logfireが設定されていない**

Logfireを使用するには、事前に設定が必要です：

```python
import logfire
logfire.configure()
```

詳細は [Logfire公式ドキュメント](https://logfire.dev/docs) を参照してください。

## 関連ドキュメント

- [MixSeek-Plus README](../../README.md)
- [ClaudeCode Provider](../../docs/providers/claudecode.md)
- [Member Agent ログ](../../docs/logging.md)

## 次のステップ

デバッグが完了したら、環境変数を削除または無効化してください：

```bash
unset MIXSEEK_VERBOSE
unset CLAUDECODE_MODEL_LOG_LEVEL
unset MIXSEEK_LOGFIRE
```

または、Python APIで：

```python
import mixseek_plus
mixseek_plus.disable_verbose_mode()
```
