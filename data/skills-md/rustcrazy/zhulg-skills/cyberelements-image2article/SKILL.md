---
name: cyberelements-image2article
description: "Generate articles from images by analyzing workspace elements and writing tech-focused content for college students, new employees, and office workers about workspace setup and decoration. Use when user wants to generate an article from an image of desk/workspace setup, create content about workspace decoration and productivity tips, write tech- and art-style articles about office equipment and accessories, or provide workspace setup advice for students or new employees"
license: MIT
metadata:
  author: Claude
  version: "1.0.0"
  tags:
    - image
    - article
    - workspace
    - desk-setup
    - technology
    - office
    - student
    - decor
    - productivity
  commands:
    - name: /cyberelements-image2article
      description: Generate an article from an image of workspace setup, analyzing elements like computer, monitor, desk, lamp, plants, etc.
      usage: /cyberelements-image2article [image|url] [path_or_url] [audience] [options]
      examples:
        - "/cyberelements-image2article image /path/to/desk-setup.jpg audience student"
        - "/cyberelements-image2article url https://example.com/desk-setup.jpg audience newbie style tech"
        - "/cyberelements-image2article image /path/to/workspace.jpg audience employee length long"
---

# Cyberelements Image to Article

Generate engaging articles from images by analyzing workspace elements and creating tech-focused, art-infused content for students, new employees, and office workers.

## Quick Start

```bash
# Generate article from local image
/cyberelements-image2article image /path/to/workspace.jpg

# Generate with specific audience
/cyberelements-image2article image /path/to/desk.jpg audience student

# Generate from URL with style options
/cyberelements-image2article url https://example.com/setup.jpg audience newbie style tech
```

## Image Input

Supports two input methods:

**Local image path:**
```bash
/cyberelements-image2article image /Users/username/Pictures/desk-setup.jpg
```

**Image URL:**
```bash
/cyberelements-image2article url https://example.com/workspace.jpg
```

## Target Audiences

| Audience | Description | Use Case |
|----------|-------------|----------|
| `student` | College students, budget-conscious, dorm/apartment setups | Shared living spaces, compact setups, student-specific needs |
| `newbie` | New employees, career-focused, aspirational | First job, professional growth, workplace identity |
| `employee` | Office workers, quality-focused, productivity-oriented | Professional environments, efficiency, career advancement |

## Writing Styles

| Style | Description | Keywords |
|-------|-------------|----------|
| `tech` | Hardcore, geeky, tech-forward | 硬核, 极客, 科技感, 智能, 高效 |
| `artistic` | Warm, healing, atmospheric | 文艺, 温馨, 治愈, 生活美学, 氛围感 |
| `balanced` | Mix of tech and aesthetics | 科技与美学兼得, 实用而不失格调 |

## Article Length

| Length | Word Count | Best For |
|--------|------------|----------|
| `short` | 500-600 words | Social media, quick posts |
| `medium` | 900-1200 words | Blog posts, articles |
| `long` | 1500-2000 words | Detailed guides, featured content |

## Detected Elements

The skill identifies and categorizes:

**Tech:** Display, computer, keyboard, mouse, speakers, headphones, dock, charger

**Furniture:** Desk, chair, ergonomic chair, organizer, shelf

**Lighting:** Desk lamp, floor lamp, LED strips, ambient lights

**Decor:** Plants, posters, photos, wall art, figurines

**Accessories:** Cup, pen holder, sticky notes, calendar, clock

## Writing Guidelines

### Content Focus

- **Practical value**: Share actual workspace improvement tips
- **Product resonance**: Highlight specific items readers might want
- **Community belonging**: Create connection through shared interests
- **Aspiration**: Inspire readers to upgrade their own spaces

### Style Characteristics

**Tech + Art blend:**
- Tech-forward language with artistic descriptions
- Focus on electronic products with aesthetic appreciation
- Appeals to young tech enthusiasts and "otaku" culture
- Emphasizes professional identity and social belonging

**Writing tone:**
- Engaging, relatable, not overly formal
- Use tech terminology appropriately
- Include product-specific details that spark interest
- Create "I want that too" moments for readers

### Article Structure

1. **Title**: Catchy, audience-specific, highlights key elements
2. **Introduction**: Set context, identify target audience, preview content
3. **Body**: Organized by element categories (tech, furniture, lighting, decor, accessories)
4. **Conclusion**: Inspiring call-to-action, encourage engagement

## Example Output

For a student audience with balanced style:

```markdown
# 宿舍神器：显示器搭配让效率提升的秘密

在这个数字化时代，作为一名年轻的学生，我深知一个学习效率良好的环境对提升专注的重要性。今天分享的这套搭配，围绕显示器、键盘展开，希望能给宿舍神器们一些灵感。

从技术角度看，科技装备部分是学习效率的关键。显示器是科技与美学兼得的选择，配合键盘的点缀，这样的组合不仅省空间，更体现了学生党必备。

值得一提的是，灯光氛围是学习环境的关键。台灯是恰到好处的选择，加上绿植的点缀，这样的组合不仅温馨，更体现了宿舍神器。

装饰点缀部分是宿舍环境的关键。绿植是实用的选择，配合照片的点缀，这样的组合不仅生活美学，更体现了学生党必备。

这就是我的宿舍神器分享。记住，科技与美学兼得的工位不仅仅是工具，更是工作幸福感的体现。希望这些搭配能给你带来灵感，打造属于自己的理想工位。
```

## Claude Integration - AI 原生创作流程

本 Skill 充分释放大模型的 **原生多模态能力**。不再拼接字符串，而是将识别出的真实物件作为创作养料，由 AI 实时生成高质量内容。

### 核心工作流

1. **视觉分析 (Visual Recognition)**
   - 使用 `view_file` 工具读取图片。
   - 提取工位元素：识别显示器型号、桌面材质（如胡桃木）、绿植种类、光影效果等。

2. **数据预处理 (Context Enrichment)**
   - 运行 `prepareAIData` 函数。它会根据 `audience` 和 `style` 参数，结合识别出的元素，封装成一个高质量的写作 Prompt。

3. **原生创作 (AI Writing)**
   - AI 接收到 Prompt 后，基于识别到的物品细节进行深度写作。
   - **注意**：AI 应避免罗列物品，而应描述它们构建的整体空间感和生产力价值。

---

## 示例操作案例

**输入指令：**
`/cyberelements-image2article image /path/to/desk.jpg audience employee style artistic`

**执行步骤：**
1. **看图**：识别出 `[27寸显示器, 机械键盘, 豆绿色文件架, 天堂鸟, 暖黄灯光]`。
2. **生成 Prompt**：`prepareAIData` 输出针对职场精英的艺术风写作指令。
3. **输出文章**：AI 生成一篇充满氛围感的职场工位美学分享。

---

## 维护者建议 (Maintainer Tips)

- **保持感知真实**：写作时应多描述识别到的具体材质和光影（如“磨砂金属”、“百叶窗透过的光”）。
- **人设统一**：确保文章语气与 `audience` 参数设定的人物背景高度吻合。
- **杜绝 AI 味**：避免使用“总之”、“综上所述”等明显的模板化词汇。
