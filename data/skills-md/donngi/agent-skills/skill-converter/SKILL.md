---
name: skill-converter
description: スキルを各AI Agent固有のフォーマットに変換する。「スキルを変換」「convert skill」などと言われたときに使用する
---

# Skill Converter

どのAI Agentでも利用可能なように汎用的に設計されたスキルを特定のAI Agentツール固有のフォーマットに変換します。

## ワークフロー

### Step 1: 変換対象スキル、AI Agnet、変換結果の出力先のヒアリング

変換対象のskillのパス、変換対象のAI Agent名、変換結果の出力先ディレクトリをユーザーに質問し、取得する。
変換結果の出力先ディレクトリは、プロジェクトの構成を踏まえ、推奨値を提案する。

### Step 2: 各ツールの最新スキル仕様を調査

各種AI Agentの組み込み機能やインターネット検索を利用して、指定されたAI AgentのSkill機能の最新使用を取得する。

### Step 3: ツール固有の拡張を自動判断・提案

Step 2で調査した最新仕様に基づき、元のスキル内容を分析して

- 追加すべきプロパティ
- より具体的に書き換えが可能なステップ(例:`インターネット検索する`を`[変換対象のAI Agentの組み込み機能名]で調査する`に置き換え)

を自動判断し、ユーザーに提案する。

### Step 4: ユーザー確認

提案内容をユーザーに確認し、修正があれば反映する。

### Step 5: スキルの生成

1. 元のスキルを読み込む
2. 各ツール向けにYAMLフロントマター、本文を調整
3. 変換後のSkill.mdを出力 
4. 元のスキルにreferences/などの付随ファイルがあればコピー
5. 生成結果を表示

## フォーマットルール

**YAMLリストは縦書きで記述:**

```yaml
# Good
allowed-tools:
  - Read
  - Write
  - Bash(terraform:*)

# Bad
allowed-tools: Read, Write, Bash(terraform:*)
```

## 使用例

```
ユーザー: hello-worldスキルをkiro-cliに特化した形式に変換して
```

```
ユーザー: hello-worldスキルをClaude Code用に変換して
```
