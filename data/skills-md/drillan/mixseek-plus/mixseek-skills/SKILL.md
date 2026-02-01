---
name: mixseek-skills
description: MixSeek Agent Skills collection for AI coding assistants. Provides workspace management, team configuration, evaluation setup, and debugging tools for MixSeek-Core.
license: Apache-2.0
compatibility: Requires mixseek-core or mixseek-plus. Python 3.13+, uv recommended.
metadata:
  author: mixseek
  version: "1.0.0"
---

# MixSeek Agent Skills

MixSeek-Core用のAgent Skillsコレクションです。

## 含まれるスキル

| スキル | 説明 |
|--------|------|
| `detect-python-command` | Pythonコマンド判別・実行 |
| `mixseek-workspace-init` | ワークスペース初期化 |
| `mixseek-team-config` | チーム設定生成 |
| `mixseek-orchestrator-config` | オーケストレーター設定 |
| `mixseek-evaluator-config` | 評価設定生成 |
| `mixseek-config-validate` | 設定検証 |
| `mixseek-model-list` | モデル一覧取得 |
| `mixseek-prompt-builder` | プロンプトビルダー設定 |
| `mixseek-debug` | デバッグ機能・ログ制御 |

## インストール

```bash
npx skills add drillan/mixseek-plus
```

## 詳細

各スキルの詳細は、サブディレクトリ内の `SKILL.md` を参照してください。
