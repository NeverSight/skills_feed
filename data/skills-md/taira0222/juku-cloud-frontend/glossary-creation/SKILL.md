---
name: glossary-creation
description: プロジェクトの用語集を作成するスキル
---

# Glossary Creation Skill

## 目的

チームメンバー間の共通理解を促進し、用語の認識齟齬を防ぎます。

## 前提条件

このスキルを実行する前に、以下のスキルが完了している必要があります:
- **prd-writing**: `docs/product-requirements.md` が作成されていること
- **functional-design**: `docs/functional-design.md` が作成されていること
- **architecture-design**: `docs/architecture.md` が作成されていること

## 入力

- `docs/product-requirements.md`
- `docs/functional-design.md`
- `docs/architecture.md`

## 出力

`docs/glossary.md` - 用語集

## 実行手順

1. 既存のドキュメントを全て読み込む
2. プロジェクト固有の用語を抽出する
3. [template.md](./template.md)を参照してドキュメントを作成する
4. カテゴリ別に整理し、定義を明確に記述する
5. 関連用語や使用例を含める

## 参照ファイル

- [template.md](./template.md) - 用語集のテンプレート構造
- [guide.md](./guide.md) - 作成時のガイドライン（用語選定や定義の書き方）

## 使い方

このスキルを使用する際は、以下の流れで作業します:

1. **テンプレートの確認**: [template.md](./template.md)でドキュメント構造を把握
2. **ガイドラインの理解**: [guide.md](./guide.md)で作成時の注意点を確認
3. **ドキュメント作成**: テンプレートに従って`docs/glossary.md`を作成
4. **品質チェック**: 定義の明確性と他ドキュメントとの整合性を確認
