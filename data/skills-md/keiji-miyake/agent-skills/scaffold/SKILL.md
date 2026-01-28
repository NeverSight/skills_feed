---
name: scaffold
description: AI駆動開発のためのプロジェクト初期構築スキル。AGENTS.mdの作成、基本指示の設定、およびコアスキルのインストールを自動化します。
license: MIT License
metadata:
  author: Agent Skills
  version: "1.0"
---

# Project Scaffold Skill

このスキルは、AI駆動開発（Agent Skills Ecosystem）に対応した新規プロジェクト環境を構築するための手順と知識を提供します。
エージェントがプロジェクトの初期化が必要だと判断した際に、専門的な知識セットとして使用されることを想定しています。

## 核となる原則

- **Standard Commands**: スキルのインストールには `npx skills add` を使用し、常に最新かつ適切なバージョンを取得します。
- **Documentation First**: コードよりも先に、プロジェクトの「ルール（AGENTS.md）」と「指示（instructions.md）」を確立します。
- **Modular Setup**: 必要な機能（スキル）を選択的に導入できる構造にします。

## ワークフロー

### 1. プロジェクト定義の確立 (`AGENTS.md`)

プロジェクトのルートに `AGENTS.md` を作成し、エージェントの役割とプロジェクト全体の指示（システムプロンプト）を定義します。

**Action:**
以下のテンプレートを使用して `AGENTS.md` を作成してください。

```markdown
# Agent Definitions & Instructions

このプロジェクトでは、以下の役割を持つAIエージェントが協調して開発を行います。

## Project Instructions (System Prompt)
このプロジェクトでは「ドキュメント駆動開発」と「Agent Skills」ワークフローを採用しています。
すべての変更は、実装の前にドキュメント（SPEC.md, DESIGN.mdなど）に反映される必要があります。
(その他、コーディング規約や振る舞いに関するルールをここに記述してください)

## Roles
(プロジェクトのニーズに合わせて役割を追加・削除してください)

### 1. [Role Name] (role description)
- **責任**: ...
- **スキル**: ...

### examples:

### Architect (設計)
- **責任**: 要件定義、システム設計、技術選定、ドキュメント管理。
- **スキル**: `architect` (recommended)

### Developer (実装)
- **責任**: コードの実装、リファクタリング、単体テスト作成。
- **スキル**: `developer` (recommended)
```

### 2. スキルのインストール

`AGENTS.md` で定義した役割に必要なスキルをインストールします。

**Action:**
ユーザーと相談し、必要なスキルを選択してインストールしてください。

```bash
# 構文: npx skills add [skill-name]
npx skills add [required-skill]
```

> [!TIP]
> 一般的なスキル: `dev-support`, `architect`, `developer`, `qa`, `devops` など。
> Tech Stack固有のスキルがある場合はそれらも提案してください。

### 4. ドキュメント構造の初期化

標準的なドキュメントディレクトリを作成します。

**Action:**
```bash
mkdir -p docs/dev
touch docs/dev/README.md
```

## 完了後のステップ

環境構築手順の完了後、次のアクションについてはプロジェクトの現在のフェーズやユーザーの指示に基づき、エージェントが判断して提案を行ってください。
特定のスキルへの自動的な移行指示は含めないでください。
