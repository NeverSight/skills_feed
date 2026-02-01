---
name: detect-python-command
description: 現在の環境で適切なPythonコマンドを判別し、スクリプトを実行します。「Pythonコマンドを確認」「どのpythonを使う」「Python実行方法」といった依頼や、他のスキルからPythonスクリプトを実行する前に使用してください。
license: Apache-2.0
compatibility: Requires mixseek-core or mixseek-plus. Python 3.13+, uv recommended.
metadata:
  author: mixseek
  version: "1.0.0"
---

# Python コマンド判別・実行

## 概要

現在の環境で使用すべき適切なPythonコマンドを判別し、スクリプトを実行します。プロジェクトの設定（pyproject.toml、.venv、uv）を確認し、最適な方法で実行します。

## 前提条件

なし（環境を自動検出します）

## 使用方法

### 方法1: ラッパースクリプトで実行（推奨）

`run-python.sh` を使用して、Pythonスクリプトを直接実行します：

```bash
skills/detect-python-command/scripts/run-python.sh script.py [args...]
```

**例**:
```bash
# 設定ファイルの検証
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-config-validate/scripts/validate-config.py config.toml

# 引数付きで実行
skills/detect-python-command/scripts/run-python.sh script.py --verbose --output result.json
```

### 方法2: コマンドの確認のみ

使用されるPythonコマンドを確認したい場合：

```bash
# 標準モード（コマンド名のみ）
skills/detect-python-command/scripts/detect-python.sh

# 詳細モード（判別過程を表示）
skills/detect-python-command/scripts/detect-python.sh --verbose
```

## 判別ロジック

以下の優先順位で判別します：

| 優先度 | 条件 | 使用するコマンド |
|--------|------|-----------------|
| 1 | `pyproject.toml` が存在 かつ `uv` がインストール済み | `uv run python` |
| 2 | `.venv/bin/python` が存在 | `.venv/bin/python` |
| 3 | `python` コマンドが存在 | `python` |
| 4 | `python3` コマンドが存在 | `python3` |
| 5 | いずれも該当しない | エラー終了 |

## 例

### 他のスキルからの参照

```bash
# mixseek-config-validate からの使用例
skills/detect-python-command/scripts/run-python.sh \
    skills/mixseek-config-validate/scripts/validate-config.py config.toml --type team
```

### 環境情報の確認

```
User: このプロジェクトでどのPythonコマンドを使えばいい？

Agent: 判別スクリプトを実行します...

       $ skills/detect-python-command/scripts/detect-python.sh --verbose

       出力:
       Detecting Python command...
         pyproject.toml: found
         uv: installed (0.9.24)
         Result: uv run python

       このプロジェクトでは `uv run python` が使用されます。
       スクリプト実行時は run-python.sh を使用してください。
```

## スクリプト一覧

| スクリプト | 用途 |
|-----------|------|
| `run-python.sh` | Pythonスクリプトを適切なコマンドで実行（推奨） |
| `detect-python.sh` | 使用されるコマンドを確認（情報提供用） |

## トラブルシューティング

### Pythonが見つからない

```
Error: No Python interpreter found
```

**解決方法**:
1. Python をインストール
2. または `uv sync` を実行して仮想環境を作成

### スクリプトが見つからない

```
Error: Script not found: script.py
```

**解決方法**:
1. スクリプトのパスが正しいか確認
2. 相対パスの場合、カレントディレクトリを確認

### uv が見つからない

uv がインストールされていない場合、フォールバックとして `.venv/bin/python` または システムの `python3` を使用します。

uv のインストールが必要な場合は、**ユーザーに確認してから**公式ドキュメント（https://docs.astral.sh/uv/）を案内してください。

## 関連スキル

このスキルは以下のスキルから参照されます：

- `mixseek-config-validate` - 設定ファイルの検証
