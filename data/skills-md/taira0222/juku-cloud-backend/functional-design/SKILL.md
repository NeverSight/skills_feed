---
name: functional-design
description: 機能設計書を作成するスキル
---

# Functional Design Skill

## 目的

プロダクト要求定義書（PRD）を基に、詳細な機能設計書を作成します。

## 入力

- `docs/product-requirements.md`

## 出力

`docs/functional-design.md` - 機能設計書

## 実行手順

1. `docs/product-requirements.md`を読み込む
2. 各ユーザーストーリーを機能に分解する
3. [template.md](./template.md)を参照して機能設計書を作成する
4. 機能ごとに詳細設計を記述する
5. API設計とデータフローを定義する
6. セキュリティとエラーハンドリングを考慮する

## 参照ファイル

- [template.md](./template.md) - 機能設計書のテンプレート構造
- [guide.md](./guide.md) - 機能設計時のベストプラクティスとガイドライン

## 使い方

このスキルを使用する際は、以下の流れで作業します:

1. **テンプレートの確認**: [template.md](./template.md)でドキュメント構造を把握
2. **ガイドラインの理解**: [guide.md](./guide.md)で作成時の注意点を確認
3. **ドキュメント作成**: テンプレートに従って`docs/functional-design.md`を作成
4. **品質チェック**: ガイドラインに沿って内容を検証

