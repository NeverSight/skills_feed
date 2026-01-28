---
name: repository-structure
description: リポジトリ構造定義書を作成するスキル
---

# Repository Structure Skill

## 目的

プロジェクトのリポジトリ構造とディレクトリ構成を定義します。

## 入力

- `docs/product-requirements.md`
- `docs/functional-design.md`
- `docs/architecture.md`

## 出力

`docs/repository-structure.md` - リポジトリ構造定義書

## 実行手順

1. 既存のドキュメントを読み込む
2. アーキテクチャパターンに基づいてディレクトリ構造を設計する
3. [template.md](./template.md)を参照してリポジトリ構造定義書を作成する
4. 命名規則とファイル配置ルールを定義する
5. パス設定とインポートルールを定義する
6. Git管理ルールを定義する

## 参照ファイル

- [template.md](./template.md) - リポジトリ構造定義書のテンプレート
- [guide.md](./guide.md) - リポジトリ構造設計時のベストプラクティス

## 使い方

このスキルを使用する際は、以下の流れで作業します:

1. **テンプレートの確認**: [template.md](./template.md)でドキュメント構造を把握
2. **ガイドラインの理解**: [guide.md](./guide.md)で作成時の注意点を確認
3. **ドキュメント作成**: テンプレートに従って`docs/repository-structure.md`を作成
4. **品質チェック**: ガイドラインに沿って内容を検証
