---
name: architecture-design
description: アーキテクチャ設計書を作成するスキル
---

# Architecture Design Skill

## 目的

システム全体のアーキテクチャ設計書を作成します。

## 入力

- `docs/product-requirements.md`
- `docs/functional-design.md`

## 出力

`docs/architecture.md` - アーキテクチャ設計書

## 実行手順

1. PRDと機能設計書を読み込む
2. システムの要件を分析する
3. 適切なアーキテクチャパターンを選定する
4. [template.md](./template.md)を参照してドキュメントを作成する
5. レイヤー構造とアーキテクチャパターンが適切か検証する
6. セキュリティとスケーラビリティを考慮する

## 参照ファイル

- [template.md](./template.md) - アーキテクチャ設計書のテンプレート構造
- [guide.md](./guide.md) - 実装時のコード例集（設計書作成後、実装時に参照）

## 使い方

このスキルを使用する際は、以下の流れで作業します:

1. **テンプレートの確認**: [template.md](./template.md)でドキュメント構造を把握
2. **ガイドラインの理解**: [guide.md](./guide.md)で作成時の注意点を確認
3. **ドキュメント作成**: テンプレートに従って`docs/architecture.md`を作成
4. **品質チェック**: ガイドラインに沿って内容を検証
