---
name: web-design-studio
description: Create complete web pages with production-grade frontend design AND auto-generated images. Use this skill when the user asks to build websites, landing pages, dashboards, or any web interfaces that need images. This skill combines frontend design expertise with automatic AI image generation to create fully functional, visually stunning web pages with all images included. Generates creative, polished HTML/CSS/JS code with AI-generated images that match the aesthetic direction.
license: Complete terms in LICENSE.txt
---

This skill combines frontend design expertise with AI image generation to create complete, production-ready web pages with all visual elements included.

## When to Use This Skill

Use this skill when the user asks for:
- Complete websites or landing pages
- Web dashboards or applications
- Product pages or portfolios
- Marketing pages with banners/hero sections
- Blog or content layouts with featured images
- Any web interface that needs visual assets

## How This Skill Works

This skill performs a two-step process:

### Step 1: Frontend Design

Follow the frontend-design aesthetic principles to create a distinctive, production-grade interface:

**Design Thinking:**
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick a bold aesthetic direction (minimalist, maximalist, retro-futuristic, organic, luxury, playful, brutalist, etc.)
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this UNFORGETTABLE?

**Frontend Aesthetics:**
- **Typography**: Choose distinctive, beautiful fonts (avoid Inter, Roboto, Arial, system fonts)
- **Color & Theme**: Commit to a cohesive aesthetic with CSS variables
- **Motion**: Use animations for effects and micro-interactions
- **Spatial Composition**: Unexpected layouts, asymmetry, overlap, diagonal flow
- **Backgrounds & Visual Details**: Gradient meshes, noise textures, geometric patterns, dramatic shadows

### Step 2: Image Generation

Identify all images needed in the design and generate them using the image generation script:

> **Note:** The script paths below use `~/.claude/skills/` as the default installation location.
> If you installed this skill via `npx skills add`, the actual path may be different (e.g.,
> `~/.local/share/npx/skills/` or similar). Adjust the path according to your setup.

**Identify Image Needs:**
- Hero/banner images
- Product/portfolio images
- Illustrations or icons
- Background images
- Section dividers or decorative elements

**Generate Images:**
Run the image generation script for each image needed. Images are automatically saved to the project's `images/` directory for better organization:

```bash
uv run ~/.claude/skills/web-design-studio/scripts/generate_image.py \
  --prompt "detailed image description matching the design aesthetic" \
  --filename "yyyy-mm-dd-hh-mm-ss-descriptive-name.png" \
  --resolution 1K|2K|4K
```

**Resolution Guidelines:**
- **1K** (default) - ~1024px for small images, icons, thumbnails
- **2K** - ~2048px for standard images, product shots
- **4K** - ~4096px for hero banners, large backgrounds

**Filename Format:** `{timestamp}-{descriptive-name}.png`
- Timestamp: `yyyy-mm-dd-hh-mm-ss` (24-hour format)
- Name: lowercase descriptive text with hyphens

**Image Organization:**
- Images are automatically saved to the project's `images/` directory
- The script detects git repository roots and places images at the project level
- When referencing images in code, use: `images/filename.png`

### Step 3: Complete Implementation

After generating all needed images, create the final code with:

1. All generated images properly referenced using `images/filename.png`
2. Optimized image attributes (alt text, loading, sizes)
3. Responsive image handling
4. Complete styling matching the aesthetic vision

**IMPORTANT:** After creating the HTML file, you MUST verify that all images load correctly:

```bash
python ~/.claude/skills/web-design-studio/scripts/verify_images.py
```

This script checks:
- All image references in HTML files
- Whether the referenced image files exist
- Common path issues (missing `images/` prefix, etc.)

**Do not proceed to the next step until all images are verified successfully.**

### Step 4: Design Documentation (REQUIRED)

After image verification, you MUST generate a professional design specification document for client delivery. This is a mandatory final step.

**Basic Usage:**
```bash
python ~/.claude/skills/web-design-studio/scripts/generate_design_doc.py \
  --project-name "Coffee Shop Landing Page" \
  --output "design-doc-coffee-shop.html"
```

**Auto-Extraction from HTML (RECOMMENDED):**
```bash
python ~/.claude/skills/web-design-studio/scripts/generate_design_doc.py \
  --project-name "Coffee Shop Landing Page" \
  --output "design-doc-coffee-shop.html" \
  --html-file "index.html"
```

The `--html-file` parameter automatically extracts:
- Page sections with their actual content summaries
- Color scheme from CSS variables
- All images with filenames and resolutions
- CTA button count

This is the **recommended approach** as it saves time and ensures accuracy by analyzing the actual HTML code.

**Advanced Usage (Manual Parameters):**
```bash
python ~/.claude/skills/web-design-studio/scripts/generate_design_doc.py \
  --project-name "Coffee Shop Landing Page" \
  --output "design-doc-coffee-shop.html" \
  --design-concept "温暖有机的咖啡文化体验，采用大地色系和质朴风格" \
  --target-audience "咖啡爱好者、年轻职场人士、追求品质生活的消费者" \
  --primary-color "#8B4513" \
  --secondary-color "#A0522D" \
  --accent-color "#D4AF37" \
  --typography "标题：Playfair Display，正文：Lato" \
  --page-sections "Hero区,产品展示,品牌故事,客户评价,联系信息,页脚" \
  --cta-count "8" \
  --tech-stack "HTML5,CSS3,JavaScript,响应式设计" \
  --features "图片懒加载,平滑滚动,表单验证,移动优化" \
  --author "设计团队名称" \
  --project-type "landing-page" \
  --version "1.0"
```

**With Image List:**
```bash
python ~/.claude/skills/web-design-studio/scripts/generate_design_doc.py \
  --project-name "Coffee Shop" \
  --output "design-doc.html" \
  --image-list "2026-01-26-10-30-01-hero.png|4K|Banner区背景,2026-01-26-10-30-02-product.png|2K|产品展示" \
  --primary-color "#0a2540" \
  --secondary-color "#1e3a5f" \
  --accent-color "#ff6b2c"
```

**Document Contents (6 Major Sections):**
- 01 设计概述 - 核心理念、设计目标、目标受众
- 02 视觉设计策略 - 色彩系统、字体设计、图片策略
- 03 页面结构设计 - 完整页面布局和区块说明
- 04 用户体验设计 - 交互设计、响应式设计、性能优化
- 05 技术实现 - 技术栈、代码特点、浏览器兼容
- 06 交付清单 - 已交付内容、图片清单、建议后续工作

**Output:** A professionally formatted HTML document with sticky navigation, comprehensive sections, and beautiful styling - perfect for client presentations and design handoffs.

**Key Parameters:**
- `--html-file`: (RECOMMENDED) Auto-extract sections, colors, images, CTAs from HTML
- `--design-concept`, `--target-audience`: Project description
- `--primary-color`, `--secondary-color`, `--accent-color`, `--bg-color`: Custom color scheme
- `--page-sections`: Comma-separated section list
- `--image-list`: Format: `filename1|resolution1|purpose1,filename2|resolution2|purpose2`
- `--cta-count`: Number of CTA buttons
- `--author`: Design team/author name
- `--project-type`: landing-page, website, dashboard, etc.
- `--version`: Document version number

## Complete Workflow Example

**User Request:** "Create a landing page for a coffee shop"

**Process:**

1. **Design Phase:** Choose a warm, organic aesthetic with earth tones, rustic typography
2. **Image Planning:** Identify needs for:
   - Hero banner with coffee atmosphere
   - Product shots for coffee cups
   - Background textures for sections
3. **Generate Images:**
   ```bash
   # Hero banner (auto-saved to images/)
   uv run ~/.claude/skills/web-design-studio/scripts/generate_image.py \
     --prompt "warm rustic coffee shop interior, golden hour lighting" \
     --filename "2026-01-24-10-30-15-coffee-shop-hero.png" \
     --resolution 4K
   
   # Product shot (auto-saved to images/)
   uv run ~/.claude/skills/web-design-studio/scripts/generate_image.py \
     --prompt "artisan coffee cup on wooden table, latte art, top view" \
     --filename "2026-01-24-10-32-45-coffee-cup-product.png" \
     --resolution 2K
   
   # Background texture (auto-saved to images/)
   uv run ~/.claude/skills/web-design-studio/scripts/generate_image.py \
     --prompt "subtle coffee bean pattern texture, warm brown gradient" \
     --filename "2026-01-24-10-35-20-coffee-texture-bg.png" \
     --resolution 2K
   ```

4. **Create Code:** Build complete HTML/CSS with all images integrated using `images/filename.png`

5. **Verify Images:** (CRITICAL STEP)
   ```bash
   python ~/.claude/skills/web-design-studio/scripts/verify_images.py
   ```

   This ensures all image paths are correct and files exist. Fix any issues before proceeding.

6. **Generate Design Doc:** (REQUIRED FINAL STEP)
   ```bash
   python ~/.claude/skills/web-design-studio/scripts/generate_design_doc.py \
     --project-name "Coffee Shop Landing Page" \
     --output "design-doc-coffee-shop.html" \
     --html-file "index.html"
   ```

   The script will automatically extract:
   - Page sections with content summaries
   - Color scheme from CSS
   - All images and their resolutions
   - CTA button count

   Optional: Add custom parameters for more control:
   ```bash
   python ~/.claude/skills/web-design-studio/scripts/generate_design_doc.py \
     --project-name "Coffee Shop Landing Page" \
     --output "design-doc-coffee-shop.html" \
     --html-file "index.html" \
     --design-concept "温暖有机的咖啡文化体验，采用大地色系和质朴风格" \
     --target-audience "咖啡爱好者、年轻职场人士" \
     --author "设计团队"
   ```

## API Key

The script requires a Gemini API key:
- Pass via `--api-key` argument if user provides one
- Otherwise uses `GEMINI_API_KEY` environment variable

## Best Practices

1. **Design First, Images Second**: Plan the complete design before generating images
2. **Match Aesthetics**: Ensure generated images match the chosen design aesthetic
3. **Optimize Resolution**: Use appropriate resolution for each image's purpose
4. **Descriptive Prompts**: Write detailed, aesthetic-specific prompts for better results
5. **Organize Filenames**: Use clear, descriptive filenames matching the design context
6. **Verify Images**: ALWAYS run the verification script after creating HTML to catch path issues early
7. **Generate Documentation**: Design documentation is MANDATORY - never skip this final step

## Output

This skill produces the following complete deliverables:

1. **Complete HTML/CSS/JS Code**: Production-ready, responsive, fully functional
2. **Generated Images**: All images saved to `images/` directory with proper naming
3. **Verified Image References**: All image paths validated and working (via verify_images.py)
4. **Design Documentation**: MANDATORY professional spec document (design-doc-{project}.html)
5. **Clean Project Structure**: Organized files ready for deployment

**Verification Checklist Before Completion:**
- [ ] All images generated and in `images/` directory
- [ ] HTML file created with image references as `images/filename.png`
- [ ] Verification script passes: `python verify_images.py`
- [ ] Design documentation generated: `python generate_design_doc.py`
- [ ] All deliverables are present and accessible

Remember: The goal is to create COMPLETE web experiences where every visual element is thoughtfully designed and generated - no placeholder images, no "image goes here" sections. Real, finished work.
