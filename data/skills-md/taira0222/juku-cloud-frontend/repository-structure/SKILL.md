---
name: repository-structure
description: リポジトリ構造定義書を作成するスキル
---

# Repository Structure Skill

## 目的

開発チームが一貫性のあるファイル配置を行えるよう、リポジトリの構造を明確に定義します。

## 前提条件

このスキルを実行する前に、以下のスキルが完了している必要があります:
- **architecture-design**: `docs/architecture.md` が作成されていること

## 入力

- `docs/architecture.md`

## 出力

`docs/repository-structure.md` - リポジトリ構造定義書

## 実行手順

1. アーキテクチャ設計書を読み込む
2. 技術スタックに基づいたディレクトリ構造を設計する
3. [template.md](./template.md)を参照してドキュメントを作成する
4. 命名規則とパスエイリアスを定義する
5. 実例を含めて具体的に記述する

## 参照ファイル

- [template.md](./template.md) - リポジトリ構造定義書のテンプレート
- [guide.md](./guide.md) - 作成時のガイドライン（ディレクトリ設計や命名規則）

## 使い方

このスキルを使用する際は、以下の流れで作業します:

1. **テンプレートの確認**: [template.md](./template.md)でドキュメント構造を把握
2. **ガイドラインの理解**: [guide.md](./guide.md)で作成時の注意点を確認
3. **ドキュメント作成**: テンプレートに従って`docs/repository-structure.md`を作成
4. **品質チェック**: スケーラビリティと保守性を考慮して検証
