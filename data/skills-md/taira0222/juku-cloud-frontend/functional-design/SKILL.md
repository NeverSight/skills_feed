---
name: functional-design
description: 機能設計書を作成するスキル
---

# Functional Design Skill

## 目的

PRDで定義された要求を、実装可能な機能仕様に落とし込みます。

## 前提条件

このスキルを実行する前に、以下のスキルが完了している必要があります:
- **prd-writing**: `docs/product-requirements.md` が作成されていること

## 入力

- `docs/product-requirements.md`

## 出力

`docs/functional-design.md` - 機能設計書

## 実行手順

1. PRDを読み込む
2. 機能を実装可能な単位に分解する
3. [template.md](./template.md)を参照してドキュメントを作成する
4. 画面仕様、API仕様、データ仕様を詳細化する
5. フロー図を作成して処理を可視化する

## 参照ファイル

- [template.md](./template.md) - 機能設計書のテンプレート構造
- [guide.md](./guide.md) - 作成時のガイドライン（画面仕様やAPI仕様の書き方）

## 使い方

このスキルを使用する際は、以下の流れで作業します:

1. **テンプレートの確認**: [template.md](./template.md)でドキュメント構造を把握
2. **ガイドラインの理解**: [guide.md](./guide.md)で作成時の注意点を確認
3. **ドキュメント作成**: テンプレートに従って`docs/functional-design.md`を作成
4. **品質チェック**: ガイドラインに沿って内容を検証
