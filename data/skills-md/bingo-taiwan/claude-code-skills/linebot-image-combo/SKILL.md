---
name: linebot-image-combo
description: LINE Bot 題庫與筆記圖片製作的 Gemini + matplotlib 連續技。整合 AI 生成高品質底圖與程式化中文標籤，產出符合 LINE Bot 規格的圖片（< 300KB、手機可讀）。
---

# LINE Bot 圖片製作連續技

## 概述

結合 **Gemini AI** 生成高品質底圖 + **matplotlib** 加上正確中文標籤的連續技，專為 LINE Bot 題庫與筆記設計。

**為什麼需要連續技？**

| 方法 | 優點 | 缺點 |
|------|------|------|
| 純 matplotlib | 中文標籤正確 | 圖形簡陋、不夠精緻 |
| 純 Gemini | 圖片品質高 | 中文常出錯（亂碼） |
| **連續技** | 品質高 + 中文正確 | 需要兩步驟 |

---

## LINE Bot 圖片規格（重要！）

### 硬性限制

| 項目 | 限制 | 說明 |
|------|------|------|
| **檔案大小** | **< 300KB** | 超過會載入緩慢或失敗 |
| 圖片格式 | JPEG, PNG | 不支援 GIF 動圖 |
| 圖片來源 | HTTPS | 必須是安全連線 |
| Hero 比例 | 4:3 或 16:9 | Flex Message 推薦 |

### 手機閱讀限制

**LINE Bot 圖片在手機上無法放大！** 必須確保：

- 字體夠大（手機上直接可讀）
- 圖片不要太寬（手機螢幕約 360-400px）
- 重要資訊不要太密集

---

## 優化後的圖片規格

### 尺寸標準（針對 LINE Bot 優化）

| 用途 | figsize | DPI | 輸出尺寸 | 檔案大小 |
|------|---------|-----|----------|----------|
| **題庫圖片** | (8, 6) | 120 | ~960×720px | < 150KB |
| **筆記圖片** | (8, 8) | 120 | ~960×960px | < 200KB |
| **橫向圖表** | (10, 6) | 120 | ~1200×720px | < 180KB |
| 大型圖（需壓縮） | (10, 8) | 100 | ~1000×800px | < 250KB |

### 字體大小標準（手機可讀）

```python
# LINE Bot 專用字體大小（比一般用途更大）
FONT_TITLE = 24      # 圖片標題
FONT_LABEL = 18      # 標籤文字（主要內容）
FONT_SUBLABEL = 14   # 次要標籤
FONT_NOTE = 12       # 註解（最小值，謹慎使用）
```

**對比原本的設定**：

| 項目 | 原設定 | LINE Bot 優化 | 原因 |
|------|--------|---------------|------|
| figsize | (14, 12) | (8, 6) | 原本太大，檔案超過 300KB |
| DPI | 150 | 120 | 降低以控制檔案大小 |
| 標籤字體 | 11-12 | 16-18 | 原本在手機上太小 |

---

## 連續技流程

### Step 1：Gemini 生成無標籤底圖

```bash
cd ~/.claude/skills/fanpage-article-writer/scripts

# 生成無標籤的高品質圖片
python generate_image.py "圖片描述，WITHOUT any text labels" \
    --output "底圖.png" \
    --model gemini
```

**Prompt 技巧**：

```
✅ 正確：
"A detailed anatomical diagram of [主題].
Clean medical illustration style WITHOUT any text labels or annotations.
High quality educational diagram, white background."

❌ 錯誤：
"心臟解剖圖，標示中文說明"  # 中文標籤會出錯
```

### Step 2：matplotlib 加中文標籤

```python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import io

# 中文字體設定（必須）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def add_labels_for_linebot(base_image_path, output_path, labels, title):
    """
    為 Gemini 底圖加上中文標籤（LINE Bot 優化版）

    Parameters:
    - base_image_path: Gemini 生成的底圖路徑
    - output_path: 輸出路徑
    - labels: 標籤列表 [(x%, y%, 文字, 箭頭x%, 箭頭y%), ...]
    - title: 圖片標題
    """
    img = mpimg.imread(base_image_path)

    # LINE Bot 優化尺寸
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(img)
    ax.axis('off')

    h, w = img.shape[:2]

    for lx, ly, text, ax_x, ax_y in labels:
        x = lx * w
        y = ly * h
        arrow_x = ax_x * w
        arrow_y = ax_y * h

        bbox_props = dict(
            boxstyle='round,pad=0.3',
            facecolor='white',
            edgecolor='#333333',
            alpha=0.92,
            linewidth=1.5
        )

        ax.annotate(
            text,
            xy=(arrow_x, arrow_y),
            xytext=(x, y),
            fontsize=16,  # LINE Bot 優化：字體加大
            fontweight='bold',
            ha='center',
            va='center',
            bbox=bbox_props,
            arrowprops=dict(
                arrowstyle='-|>',
                color='#333333',
                lw=1.5,
                connectionstyle='arc3,rad=0.1'
            )
        )

    ax.set_title(title, fontsize=20, fontweight='bold', pad=10)

    # 儲存為 LINE Bot 優化格式
    save_for_linebot(fig, output_path)
    plt.close()


def save_for_linebot(fig, output_path, max_size_kb=280):
    """
    儲存圖片並確保 < 300KB

    自動調整品質以符合 LINE Bot 限制
    """
    # 先儲存為 PNG
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                facecolor='white', pad_inches=0.05)
    buf.seek(0)

    # 檢查大小
    size_kb = len(buf.getvalue()) / 1024

    if size_kb <= max_size_kb:
        # 大小 OK，直接儲存
        with open(output_path, 'wb') as f:
            f.write(buf.getvalue())
        print(f"已儲存: {output_path} ({size_kb:.1f} KB)")
    else:
        # 太大，轉換為 JPEG 並壓縮
        img = Image.open(buf)
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # 嘗試不同品質
        for quality in [85, 75, 65, 55]:
            jpeg_buf = io.BytesIO()
            img.save(jpeg_buf, format='JPEG', quality=quality, optimize=True)
            jpeg_size = len(jpeg_buf.getvalue()) / 1024

            if jpeg_size <= max_size_kb:
                jpeg_path = output_path.rsplit('.', 1)[0] + '.jpg'
                with open(jpeg_path, 'wb') as f:
                    f.write(jpeg_buf.getvalue())
                print(f"已儲存: {jpeg_path} ({jpeg_size:.1f} KB, quality={quality})")
                return

        # 如果還是太大，縮小尺寸
        img.thumbnail((800, 800), Image.LANCZOS)
        jpeg_buf = io.BytesIO()
        img.save(jpeg_buf, format='JPEG', quality=70, optimize=True)
        jpeg_path = output_path.rsplit('.', 1)[0] + '.jpg'
        with open(jpeg_path, 'wb') as f:
            f.write(jpeg_buf.getvalue())
        print(f"已儲存（縮小）: {jpeg_path} ({len(jpeg_buf.getvalue())/1024:.1f} KB)")
```

---

## 完整範例：心臟解剖圖

### 1. 生成底圖

```bash
cd ~/.claude/skills/fanpage-article-writer/scripts

python generate_image.py \
    "A detailed anatomical cross-section of the human heart showing four chambers, septum, valves, and major blood vessels. Clean medical illustration style WITHOUT any text labels. Blue for right side, red for left side. White background." \
    --output "C:/Users/user/Documents/temp/heart_base.png" \
    --model gemini
```

### 2. 加標籤腳本

```python
# heart_linebot.py
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import io

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_heart_diagram():
    img = mpimg.imread('C:/Users/user/Documents/temp/heart_base.png')

    # LINE Bot 優化尺寸
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(img)
    ax.axis('off')

    h, w = img.shape[:2]

    # 標籤：(標籤x%, 標籤y%, 文字, 箭頭x%, 箭頭y%)
    labels = [
        (0.08, 0.15, '上腔靜脈', 0.22, 0.20),
        (0.50, 0.05, '主動脈', 0.42, 0.18),
        (0.85, 0.10, '肺動脈', 0.60, 0.18),
        (0.05, 0.40, '右心房', 0.25, 0.38),
        (0.92, 0.35, '左心房', 0.72, 0.35),
        (0.05, 0.65, '右心室', 0.35, 0.60),
        (0.92, 0.65, '左心室', 0.65, 0.60),
        (0.50, 0.90, '心室中隔', 0.50, 0.70),
    ]

    for lx, ly, text, ax_x, ax_y in labels:
        ax.annotate(
            text,
            xy=(ax_x * w, ax_y * h),
            xytext=(lx * w, ly * h),
            fontsize=16,
            fontweight='bold',
            ha='center',
            va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                     edgecolor='#333', alpha=0.9),
            arrowprops=dict(arrowstyle='-|>', color='#333', lw=1.5)
        )

    # 圖例
    ax.text(0.20 * w, 0.95 * h, '● 含氧血', fontsize=12, color='#C62828',
            fontweight='bold', bbox=dict(facecolor='white', alpha=0.9))
    ax.text(0.75 * w, 0.95 * h, '● 缺氧血', fontsize=12, color='#1565C0',
            fontweight='bold', bbox=dict(facecolor='white', alpha=0.9))

    ax.set_title('心臟結構解剖圖', fontsize=18, fontweight='bold', pad=8)

    # 儲存（自動壓縮）
    save_for_linebot(fig, 'heart_anatomy_linebot.png')
    plt.close()


def save_for_linebot(fig, output_path, max_kb=280):
    """儲存並壓縮到 LINE Bot 規格"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight',
                facecolor='white', pad_inches=0.03)
    buf.seek(0)
    size_kb = len(buf.getvalue()) / 1024

    if size_kb <= max_kb:
        with open(output_path, 'wb') as f:
            f.write(buf.getvalue())
        print(f"已儲存: {output_path} ({size_kb:.1f} KB)")
    else:
        # 轉 JPEG 壓縮
        img = Image.open(buf).convert('RGB')
        for q in [85, 75, 65]:
            jbuf = io.BytesIO()
            img.save(jbuf, 'JPEG', quality=q, optimize=True)
            if len(jbuf.getvalue())/1024 <= max_kb:
                jpg_path = output_path.replace('.png', '.jpg')
                with open(jpg_path, 'wb') as f:
                    f.write(jbuf.getvalue())
                print(f"已儲存: {jpg_path} ({len(jbuf.getvalue())/1024:.1f} KB)")
                return
        print("警告：無法壓縮到目標大小")


if __name__ == '__main__':
    create_heart_diagram()
```

---

## API Key 管理

Gemini API Key 設定位置：

```
~/.claude/skills/fanpage-article-writer/scripts/api_keys.json
```

檢查 API Key 狀態：

```bash
cd ~/.claude/skills/fanpage-article-writer/scripts
python generate_image.py --status
```

---

## 圖片命名規範

### 題庫圖片

```
ch{章}-{節}-q{題號}-{描述}.png      # 題目圖
ch{章}-{節}-a{題號}-{描述}.png      # 答案解析圖
```

### 筆記圖片

```
{主題}_{內容}.png
例：heart_anatomy.png, heart_conduction.png
```

---

## 常見問題

### 圖片太大（> 300KB）

1. 降低 DPI：`dpi=100` 或 `dpi=80`
2. 縮小 figsize：`figsize=(6, 4)`
3. 轉 JPEG：`quality=75`
4. 縮小尺寸：`img.thumbnail((800, 800))`

### 字體太小

- 標籤字體至少 `fontsize=14`
- 標題字體至少 `fontsize=18`
- 避免密集標籤，必要時分多張圖

### Gemini 中文出錯

- Prompt 中加 `WITHOUT any text labels`
- 使用 matplotlib 後製所有文字

### LINE 圖片快取

更新圖片後加版本參數：

```
https://example.com/images/heart.png?v=2
```

---

## 相關 Skill

- `linebot-notebook-design`：Flex Message 設計規範
- `quiz-builder`：題庫系統專用指南
- `fanpage-article-writer`：Gemini API 腳本位置

---

## Noto Sans CJK TC 字體（罕見中文字支援）

### 問題

微軟正黑體不支援某些罕見中文字，例如超重元素 105-118 的名稱：

| 原子序 | 符號 | 中文名 | 微軟正黑體 |
|--------|------|--------|------------|
| 105 | Db | 𨧀 | ⬜ 顯示為方框 |
| 106 | Sg | 𨭎 | ⬜ 顯示為方框 |
| 107 | Bh | 𨨏 | ⬜ 顯示為方框 |
| 108 | Hs | 𨭆 | ⬜ 顯示為方框 |
| 117 | Ts | 鿬 | ⬜ 顯示為方框 |
| 118 | Og | 鿫 | ⬜ 顯示為方框 |

### 解決方案：使用 Noto Sans CJK TC

Google 的 Noto Sans CJK TC 字體完整支援所有 CJK 字符。

**下載字體**：

```bash
# npm 安裝方式
npm install @aspect-build/aspect-fonts-noto-sans-cjk-tc

# 或直接下載 OTF 檔
# https://github.com/googlefonts/noto-cjk/releases
```

**matplotlib 使用方式**：

```python
import matplotlib.font_manager as fm
import matplotlib.patheffects as path_effects

# 載入 Noto Sans CJK TC 字體
NOTO_FONT_PATH = "C:/Users/user/Documents/temp/NotoSansCJKtc-Regular.otf"
noto_font = fm.FontProperties(fname=NOTO_FONT_PATH)

# 使用 fontproperties 參數
ax.text(0.95, 0.08, "鿬",  # 罕見字
        fontsize=48, color='white', fontweight='bold',
        fontproperties=noto_font,  # 指定字體
        path_effects=[
            path_effects.withStroke(linewidth=3, foreground='black')  # 黑邊
        ])
```

**重點**：
- 使用 `fontproperties=` 參數，不是 `fontfamily=`
- `path_effects.withStroke()` 可加黑邊讓白字更清晰
- 字體檔約 16MB，不要放進 Git repo

---

## Breaking Bad 風格元素圖片生成

使用 Gemini API 直接生成 Breaking Bad 風格的元素週期表 hero 圖片。

### API 直接呼叫方式

```python
from google import genai
from google.genai import types

# 初始化 client
client = genai.Client(api_key=API_KEY)

# 生成圖片
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['image', 'text']  # 重要！
    )
)

# 取得圖片資料
for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        image_data = part.inline_data.data
        with open(output_path, 'wb') as f:
            f.write(image_data)
```

### Breaking Bad 風格 Prompt 範例

```python
def generate_prompt(element, color_hex):
    symbol = element['symbol']  # e.g., "H"
    rest_name = "ydrogen"       # 去掉符號後的名稱
    atomic_num = 1
    atomic_mass = "1.008"

    return f"""Create a Breaking Bad TV series style periodic table element card.

CRITICAL REQUIREMENTS:
1. BACKGROUND: Dark navy blue (#1a1a2e) with {color_hex} colored smoke/vapor filling the ENTIRE image background.

2. ELEMENT BOX (center-left):
   - Green square box (#00A300) with white border (3px)
   - Large white letter '{symbol}' in the center (bold, sans-serif)
   - Small white number '{atomic_num}' in top-right corner of the box

3. TEXT (to the right of the box):
   - '{rest_name}' in white, same baseline as the symbol
   - Below that: '{atomic_mass}' in smaller white text

4. LAYOUT:
   - Design should be centered and fit a 2:1 aspect ratio (wide format)
   - NO solid colored panels blocking the smoke background

5. STYLE:
   - Cinematic, dramatic lighting
   - Similar to Breaking Bad title card aesthetic

DO NOT add any other text, watermarks, or decorations."""
```

### 後處理：裁切 + 中文標籤 + 壓縮

```python
def post_process_image(input_path, output_path, element, target_width=1200):
    """後處理：裁切成 2:1、加中文標籤、壓縮到 < 300KB"""
    from PIL import Image
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as path_effects
    import matplotlib.font_manager as fm

    # 載入 Noto 字體
    noto_font = fm.FontProperties(fname=NOTO_FONT_PATH)

    # 開啟圖片
    img = Image.open(input_path)
    width, height = img.size

    # 裁切成 2:1 比例（從中心裁切）
    target_height = width // 2
    if height > target_height:
        top = (height - target_height) // 2
        img = img.crop((0, top, width, top + target_height))

    # 調整大小
    target_height = target_width // 2
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # 轉換為 RGB
    if img.mode != 'RGB':
        background = Image.new('RGB', img.size, (26, 26, 46))
        if img.mode == 'RGBA':
            background.paste(img, mask=img.split()[3])
        else:
            background.paste(img)
        img = background

    # 用 matplotlib 加中文標籤
    fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
    ax.imshow(img)
    ax.axis('off')

    # 加上中文名稱（右下角）
    ax.text(0.95, 0.08, element['name_zh'],
            transform=ax.transAxes,
            fontsize=48, color='white', fontweight='bold',
            ha='right', va='bottom',
            fontproperties=noto_font,
            path_effects=[
                path_effects.withStroke(linewidth=3, foreground='black')
            ])

    # 儲存並壓縮
    plt.tight_layout(pad=0)
    plt.savefig(output_path, dpi=100, bbox_inches='tight', pad_inches=0,
                format='jpeg', quality=85)
    plt.close()
```

### 生成結果

- 輸出尺寸：1200×600px（2:1 比例）
- 檔案大小：~80-150KB（符合 LINE Bot 限制）
- 風格：Breaking Bad 電視劇風格，深藍背景 + 彩色煙霧

---

## Windows Console 編碼問題

在 Windows 上執行 Python 腳本時，若遇到 `UnicodeEncodeError`，在程式開頭加入：

```python
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
```

---

## 變更記錄

| 日期 | 版本 | 變更內容 |
|------|------|----------|
| 2026-01-18 | 1.0 | 初版制定，整合 Gemini + matplotlib 連續技 |
| 2026-01-20 | 1.1 | 新增 Noto Sans CJK TC 字體、Breaking Bad 風格生成、Windows 編碼修正 |
