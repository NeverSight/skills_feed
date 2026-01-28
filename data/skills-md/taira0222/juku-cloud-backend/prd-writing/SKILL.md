---
name: prd-writing
description: プロダクト要求定義書（PRD）を作成するスキル
---

# PRD Writing Skill

## 目的

`.steering/ideas/` 内のアイデアファイルを基に、体系的なプロダクト要求定義書（Product Requirements Document）を作成します。

## 入力

- `.steering/ideas/` 内のマークダウンファイル
- ユーザーとの対話による追加情報

## 出力

`docs/product-requirements.md` - プロダクト要求定義書

## 実行手順

1. `.steering/ideas/` 内の全マークダウンファイルを読み込む
2. アイデアの内容を分析・整理する
3. [template.md](./template.md)を参照してPRDを作成する
4. ユーザーに確認を求める
5. フィードバックを反映して完成させる
6. 具体性と測定可能性を検証する

## 参照ファイル

- [template.md](./template.md) - PRDのテンプレート構造
- [guide.md](./guide.md) - PRD作成時のベストプラクティスとガイドライン

## 使い方

このスキルを使用する際は、以下の流れで作業します:

1. **テンプレートの確認**: [template.md](./template.md)でドキュメント構造を把握
2. **ガイドラインの理解**: [guide.md](./guide.md)で作成時の注意点を確認
3. **ドキュメント作成**: テンプレートに従って`docs/product-requirements.md`を作成
4. **品質チェック**: ガイドラインに沿って内容を検証
