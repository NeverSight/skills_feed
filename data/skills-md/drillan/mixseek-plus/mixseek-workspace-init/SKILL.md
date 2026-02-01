---
name: mixseek-workspace-init
description: MixSeekワークスペースを初期化し、設定ファイル用ディレクトリ構造を作成します。「ワークスペースを初期化」「mixseekのセットアップ」「設定ディレクトリを作成」「新しいプロジェクトを始める」といった依頼で使用してください。
license: Apache-2.0
compatibility: Requires mixseek-core or mixseek-plus. Python 3.13+, uv recommended.
metadata:
  author: mixseek
  version: "1.0.0"
---

# MixSeek ワークスペース初期化

## 概要

MixSeek-Coreのワークスペースディレクトリ構造を初期化します。チーム設定、評価設定、ログなどを格納するディレクトリを作成し、環境変数の設定をガイドします。

## 前提条件

- 対象ディレクトリへの書き込み権限
- 環境変数 `MIXSEEK_WORKSPACE` が設定されている（推奨）

## 使用方法

### Step 1: ワークスペースパスの確認

ユーザーにワークスペースパスを確認してください:

1. 環境変数 `MIXSEEK_WORKSPACE` が設定されている場合はその値を使用
2. 設定されていない場合は、ユーザーに希望するパスを確認
3. パスが指定されない場合は、カレントディレクトリを提案

```bash
# 環境変数の確認
echo $MIXSEEK_WORKSPACE
```

### Step 2: ディレクトリ構造の作成

以下のスクリプトを実行してディレクトリ構造を作成します:

```bash
# スクリプトの実行
bash skills/mixseek-workspace-init/scripts/init-workspace.sh <workspace-path>
```

または、手動で以下のディレクトリを作成:

```bash
mkdir -p <workspace-path>/configs/agents
mkdir -p <workspace-path>/configs/evaluators
mkdir -p <workspace-path>/configs/judgment
mkdir -p <workspace-path>/configs/presets
mkdir -p <workspace-path>/logs
mkdir -p <workspace-path>/templates
```

### Step 3: 環境変数の設定案内

初期化完了後、ユーザーに環境変数の設定を案内してください:

```bash
# シェル設定ファイルに追加（bash/zsh）
export MIXSEEK_WORKSPACE=/path/to/workspace
```

## 作成されるディレクトリ構造

```
$MIXSEEK_WORKSPACE/
├── configs/
│   ├── agents/           # チーム・メンバーエージェント設定 (team-*.toml)
│   ├── evaluators/       # 評価者設定 (evaluator.toml)
│   ├── judgment/         # 判定設定 (judgment.toml)
│   └── presets/          # ツール設定プリセット (claudecode.toml)
├── logs/                 # 実行ログ
└── templates/            # 設定テンプレート（オプション）
```

## 例

### 新規ワークスペース作成

```
User: MixSeekのワークスペースを初期化して

Agent: ワークスペースパスを確認します。
       MIXSEEK_WORKSPACE環境変数が設定されていません。
       どのディレクトリをワークスペースにしますか？
       現在のディレクトリ（/home/user/projects/my-project）でよろしいですか？

User: はい

Agent: ワークスペースを初期化します...
       [スクリプト実行]

       以下のディレクトリ構造を作成しました:
       ✓ configs/agents/
       ✓ configs/evaluators/
       ✓ configs/judgment/
       ✓ configs/presets/
       ✓ configs/presets/claudecode.toml (プリセットコピー)
       ✓ logs/
       ✓ templates/

       環境変数の設定を推奨します:
       export MIXSEEK_WORKSPACE=/home/user/projects/my-project

       シェル設定ファイル（.bashrc/.zshrc）に追加することで永続化できます。
```

### 既存ディレクトリへの追加

```
User: このディレクトリをmixseekのワークスペースにして

Agent: 現在のディレクトリ（/path/to/dir）をワークスペースとして初期化します。
       既存のファイルは保持され、必要なディレクトリのみ作成されます。
       よろしいですか？

User: はい

Agent: [既存ファイルを保持しながら不足ディレクトリを作成]
       完了しました。
```

## トラブルシューティング

### 書き込み権限エラー

```
Error: Permission denied: /path/to/workspace
```

**解決方法**:
1. ディレクトリの所有者を確認: `ls -la /path/to/workspace`
2. 権限を変更: `chmod 755 /path/to/workspace`
3. または、書き込み権限のある別のディレクトリを選択

### 既存ファイルとの競合

このスキルは既存ファイルを上書きしません。ディレクトリが既に存在する場合はスキップされます。

### 環境変数が認識されない

シェルを再起動するか、設定ファイルを再読み込みしてください:

```bash
source ~/.bashrc  # bash
source ~/.zshrc   # zsh
```

## 次のステップ

ワークスペース初期化後、以下のスキルを使用して設定を作成できます:

1. **チーム設定**: `mixseek-team-config` - 「チームを作成して」
2. **オーケストレーター設定**: `mixseek-orchestrator-config` - 「オーケストレーターを設定して」
3. **評価設定**: `mixseek-evaluator-config` - 「評価設定を作成して」
