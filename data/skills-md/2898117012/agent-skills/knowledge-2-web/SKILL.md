---
name: knowledge-2-web
description: 将知识文章内容转换为精美的交互式网页，自动生成配图，适用于历史、科学、文化等各类知识主题。
---

# Knowledge to Web - 知识文章网页生成器

将知识文章内容转换为精美的交互式网页，自动生成配图，适用于历史、科学、文化等各类知识主题。

## 使用场景

- 教学辅助材料制作
- 知识科普文章可视化
- 历史事件深度解析
- 科学概念图解说明
- 文化知识卡片展示

## 使用方法

### 方式一：提供JSON文件

```bash
python scripts/knowledge-to-web.py <content.json> [api_key] [--images N] [--style STYLE]
```

参数说明：
- `content.json`: 文章内容的JSON文件（参考 assets/example-industrial-revolution.json）
- `api_key`: Google API key（可选，如果已设置环境变量 GOOGLE_API_KEY）
- `--images N`: 生成图片数量（默认：5）
- `--style STYLE`: 图片风格（historical/scientific/cultural/nature，默认：historical）
- `--no-images`: 跳过图片生成，仅生成HTML

### 方式二：通过Skill调用

```
/knowledge-2-web 工业革命 包括背景、发展阶段、技术创新、社会影响等内容
```

## JSON内容格式

```json
{
  "title": "文章标题",
  "subtitle": "副标题",
  "coreThesis": "核心命题",
  "primaryColor": "#8B2B24",
  "accentColor": "#B58D59",
  "causes": [
    {
      "title": "原因标题",
      "description": "原因描述"
    }
  ],
  "timeline": [
    {
      "time": "时间点",
      "title": "事件标题",
      "description": "事件描述"
    }
  ],
  "impacts": [
    {
      "title": "影响标题",
      "description": "影响描述"
    }
  ],
  "perspectives": [
    {
      "title": "视角标题",
      "quote": "引用内容"
    }
  ],
  "misconceptions": [
    {
      "misconception": "常见误区",
      "fact": "正确事实"
    }
  ]
}
```

完整示例请参考：`assets/example-industrial-revolution.json`

## 图片生成

使用 Gemini Image API 自动生成配图：

### 图片风格

- **historical**: 传统中国画风格，适合历史主题
- **scientific**: 科学插图风格，适合科学概念
- **cultural**: 文化艺术风格，适合文化主题
- **nature**: 自然摄影风格，适合自然主题

### API配置

需要配置 Google API Key：

```bash
# 方式1：环境变量
export GOOGLE_API_KEY="your-api-key"

# 方式2：命令行参数
python scripts/knowledge-to-web.py content.json your-api-key
```

### 图片生成示例代码

```python
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client(api_key="your-api-key")

prompt = "A historical scene of the Industrial Revolution, traditional painting style"
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="16:9")
    )
)

for part in response.candidates[0].content.parts:
    if part.inline_data:
        image = Image.open(io.BytesIO(part.inline_data.data))
        image.save("generated_image.png")
```

## 输出

生成一个完整的HTML文件，包含：
- 响应式设计，适配移动端和桌面端
- 精美的卡片式布局
- AI生成的配图
- 时间线可视化
- 图标和视觉元素
- 易错点提示
- 可直接在浏览器中打开查看

输出目录：`output/knowledge-web/`

## 设计风格

- 使用Tailwind CSS框架
- 中文优化字体（Noto Sans SC / Noto Serif SC）
- 自定义配色方案
- 卡片悬停效果
- 滚动时间线
- 响应式网格布局
- 图片与文字完美融合

## 脚本说明

### knowledge-to-web.py
主脚本，完整的知识文章生成器，包含图片生成和HTML生成功能。

### generate-illustrations.py
独立的插图生成器，可单独使用为知识文章生成配图。

### generate-template.js
JavaScript模板生成器，用于前端动态生成HTML。

## 示例

```bash
# 生成工业革命知识网页（含5张插图）
python scripts/knowledge-to-web.py assets/example-industrial-revolution.json --images 5 --style historical

# 仅生成HTML，不生成图片
python scripts/knowledge-to-web.py assets/example-industrial-revolution.json --no-images

# 使用科学风格生成3张插图
python scripts/knowledge-to-web.py content.json --images 3 --style scientific
```
