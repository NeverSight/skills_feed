---
name: development-guidelines
description: 開発ガイドラインを作成するスキル
---

# Development Guidelines Skill

## 目的

チーム全体で一貫した開発を行うための基準を定義します。

## 前提条件

このスキルを実行する前に、以下のスキルが完了している必要があります:
- **architecture-design**: `docs/architecture.md` が作成されていること
- **repository-structure**: `docs/repository-structure.md` が作成されていること

## 入力

- `docs/architecture.md`
- `docs/repository-structure.md`

## 出力

`docs/development-guidelines.md` - 開発ガイドライン

## 実行手順

1. アーキテクチャとリポジトリ構造を読み込む
2. 技術スタックに合わせたコーディング規約を定義する
3. [template.md](./template.md)を参照してドキュメントを作成する
4. Good/Bad例を豊富に含める
5. 自動化ツールの設定も含める

## 参照ファイル

- [template.md](./template.md) - 開発ガイドラインのテンプレート
- [guide.md](./guide.md) - 作成時のガイドライン（具体例の書き方や実行可能性）

## 使い方

このスキルを使用する際は、以下の流れで作業します:

1. **テンプレートの確認**: [template.md](./template.md)でドキュメント構造を把握
2. **ガイドラインの理解**: [guide.md](./guide.md)で作成時の注意点を確認
3. **ドキュメント作成**: テンプレートに従って`docs/development-guidelines.md`を作成
4. **品質チェック**: 以下の項目を確認
   - [ ] ルールが自動化可能か(ESLint, Prettierで強制できるか)
   - [ ] チームの生産性を阻害しないか(過度に厳格でないか)
   - [ ] 例外ケースへの対応が柔軟か
   - [ ] Good/Bad例が豊富に含まれているか
   - [ ] ツール設定ファイル(.eslintrc, .prettierrcなど)が含まれているか
   - [ ] ガイドラインの各項目に具体的な理由が記載されているか
