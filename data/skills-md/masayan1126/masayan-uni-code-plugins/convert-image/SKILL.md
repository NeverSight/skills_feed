---
name: convert-image
description: PNG/JPG/JPEG画像をWebP、ICO、SVG形式に変換。「画像を変換して」「webpに変換」などで使用。
---

# Image Converter

PNG/JPG/JPEG画像をWebP、ICO、SVG形式に変換する。

## 使用方法

詳細は `scripts/convert_image.py --help` を参照。

```bash
# WebPに変換
python3 scripts/convert_image.py input.png --format webp

# ICOに変換（複数サイズ対応）
python3 scripts/convert_image.py input.png --format ico --sizes 16,32,48,256

# SVGに変換（画像埋め込み形式）
python3 scripts/convert_image.py input.png --format svg

# 出力先を指定
python3 scripts/convert_image.py input.jpg --format webp -o output.webp
```

## 依存関係

```bash
pip install Pillow
```
