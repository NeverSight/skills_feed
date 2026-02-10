---
name: docx-reader
description: Reads Microsoft Word (.docx) files and extracts text content. Use when needing to read .docx documents. Requires python-docx package.
---

# DOCX Reader

Microsoft Word (.docx) ファイルをテキスト形式で読み込むスキルです。

## クイックスタート

### 基本的な使い方

```bash
# WSL環境でPythonスクリプトを実行
wsl python3 scripts/read_docx.py "/mnt/c/path/to/file.docx"
```

### Markdown形式で保存

1. スクリプトでテキスト抽出
2. Write ツールで .md ファイルに保存

## 前提条件

python-docx パッケージが必要です：

```bash
wsl pip3 install python-docx
```

## 使用例

### 例1: .docx ファイルを読み込んで内容を表示

```
User: "C:\Users\keita\repos\file.docx を読み込んで"
Assistant:
1. Windowsパスを WSL パスに変換: /mnt/c/Users/keita/repos/file.docx
2. wsl python3 scripts/read_docx.py を実行
3. 抽出されたテキストを表示
```

### 例2: .docx を Markdown に変換して保存

```
User: "申請書.docx を Markdown に変換して保存"
Assistant:
1. scripts/read_docx.py でテキスト抽出
2. Markdown形式で整形
3. Write ツールで 申請書.md に保存
4. 保存完了を報告
```

## ワークフロー

### 単一ファイルの読み込み

1. ユーザーが .docx ファイルパスを指定
2. Windows パスを WSL パス形式に変換 (`C:\` → `/mnt/c/`)
3. `wsl python3 scripts/read_docx.py` を実行
4. 抽出されたテキストを表示または保存

### 複数ファイルの一括処理

1. Glob で .docx ファイルを検索
2. 各ファイルに対してスクリプトを実行
3. 結果をまとめて報告

## スクリプト詳細

Python スクリプトは `scripts/read_docx.py` に配置されています。

**主な機能:**
- 段落テキストの抽出
- テーブルデータの抽出
- エラーハンドリング

**使い方:**
```bash
python scripts/read_docx.py <file_path>
```

## 制限事項

- 画像は抽出されません
- 複雑なレイアウトは簡略化されます
- フォント情報、色などのスタイルは失われます
- 埋め込みオブジェクトは抽出されません

## トラブルシューティング

### python-docx がインストールされていない

```bash
wsl pip3 install python-docx
```

### "No module named 'docx'" エラー

```bash
wsl pip3 uninstall docx
wsl pip3 install python-docx
```

### ファイルが開けない

- ファイルパスが正しいか確認（Windows → WSL パス変換）
- ファイルが他のプログラムで開かれていないか確認
- ファイルのアクセス権限を確認

## パス変換

Windows パスから WSL パスへの変換：

- `C:\Users\...` → `/mnt/c/Users/...`
- `D:\Projects\...` → `/mnt/d/Projects/...`
- バックスラッシュ `\` をスラッシュ `/` に変換

## 関連ツール

- **pandoc**: より高度な変換が必要な場合
- **python-docx2txt**: 軽量な代替ライブラリ
- **mammoth**: HTML形式での変換

## バージョン履歴

- v1.0.0 (2026-01-06): 初期リリース
  - 基本的なテキスト抽出機能
  - テーブル抽出対応
  - WSL環境での動作