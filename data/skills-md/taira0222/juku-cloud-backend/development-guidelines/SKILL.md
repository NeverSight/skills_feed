---
name: development-guidelines
description: 開発ガイドラインを作成するスキル
---

# Development Guidelines Skill

## 目的

開発チーム全体で遵守すべき開発ガイドラインを定義します。

## 入力

- `docs/product-requirements.md`
- `docs/architecture.md`
- `docs/repository-structure.md`

## 出力

`docs/development-guidelines.md` - 開発ガイドライン

## 実行手順

1. 既存のドキュメントを読み込む
2. プロジェクトの技術スタックに基づいて規約を定義する
3. [template.md](./template.md)を参照して開発ガイドラインを作成する
4. チームの開発フローを考慮する
5. セキュリティとパフォーマンスのベストプラクティスを含める
6. 具体的な例を示す

## 参照ファイル

- [template.md](./template.md) - 開発ガイドラインのテンプレート
- [guide.md](./guide.md) - ガイドライン作成時のベストプラクティス

## 使い方

このスキルを使用する際は、以下の流れで作業します:

1. **テンプレートの確認**: [template.md](./template.md)でドキュメント構造を把握
2. **ガイドラインの理解**: [guide.md](./guide.md)で作成時の注意点を確認
3. **ドキュメント作成**: テンプレートに従って`docs/development-guidelines.md`を作成
4. **品質チェック**: ガイドラインに沿って内容を検証
