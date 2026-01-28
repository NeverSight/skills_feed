---
name: glossary-creation
description: 用語集を作成するスキル
---

# Glossary Creation Skill

## 目的

プロジェクト全体で使用される専門用語、ドメイン用語、技術用語を定義した用語集を作成します。

## 入力

- `docs/product-requirements.md`
- `docs/functional-design.md`
- `docs/architecture.md`
- `docs/repository-structure.md`
- `docs/development-guidelines.md`

## 出力

`docs/glossary.md` - 用語集

## 実行手順

1. すべての既存ドキュメントを読み込む
2. ドキュメント内で使用されている専門用語を抽出する
3. [template.md](./template.md)を参照して用語集を作成する
4. 各用語をカテゴリに分類する
5. 各用語に定義、使用例、関連用語を追加する
6. 略語一覧を作成する

## 参照ファイル

- [template.md](./template.md) - 用語集のテンプレート構造
- [guide.md](./guide.md) - 用語集作成時のベストプラクティス

## 使い方

このスキルを使用する際は、以下の流れで作業します:

1. **テンプレートの確認**: [template.md](./template.md)でドキュメント構造を把握
2. **ガイドラインの理解**: [guide.md](./guide.md)で作成時の注意点を確認
3. **ドキュメント作成**: テンプレートに従って`docs/glossary.md`を作成
4. **品質チェック**: ガイドラインに沿って内容を検証
