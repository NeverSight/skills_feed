---
name: creative-orchestrator
description: Master coordinator for all creative skills. Use this skill to orchestrate asset generation, manage workflows, and automate creative production. Integrates with nanobanana pro automation system.
---

# Creative Orchestrator Skill

## Overview

The Creative Orchestrator is the master coordinator for all creative skills. It tells Claude Code exactly how to generate assets using the automation system, manage workflows, and orchestrate creative production.

**Keywords**: orchestration, workflow, automation, asset generation, creative production, Claude Code integration

## What This Skill Does

The Creative Orchestrator:

1. **Coordinates all creative skills** — Tells Claude which skills to use in which order
2. **Manages Claude Code integration** — Shows Claude how to run Python code to generate assets
3. **Automates workflows** — Chains multiple generation tasks together
4. **Handles file organization** — Manages asset storage and organization
5. **Provides templates** — Pre-built workflows for common scenarios

## How Claude Code Uses This Skill

When you ask Claude to generate creative assets, the Orchestrator tells Claude Code:

1. **Where the automation system is** — File paths and imports
2. **How to set up the environment** — API keys, dependencies
3. **What Python code to run** — Exact function calls
4. **How to chain operations** — Multiple assets in sequence
5. **Where to save results** — Organized folder structure

### Automatic Skill Invocation

After understanding the user's creative needs, **ask if they want you to automatically invoke the relevant creative skills**. For example:

```
"For your product launch, I recommend these skills:
1. creative-strategist (define visual direction)
2. product-photography (hero shots)
3. social-graphics (platform assets)

Would you like me to run these skills now? I'll invoke each one to guide your asset creation."
```

If the user agrees, **invoke each skill using the /skill-name command** (e.g., `/creative-strategist`, `/product-photography`). Work through them in the recommended order.

## Setup: Enable Automation System

### Step 1: Extract Automation System

Copy and Extract `vibe-creative-automation.zip` to your project and add it in gitignore (it is located in the root where this file is):

```
your-project/
├── vibe-creative-automation/
│   ├── fal_api.py
│   ├── creative_cli.py
│   ├── claude_integration.py
│   └── requirements.txt
└── assets/  (will be created automatically)
```

### Step 2: Install Dependencies

```bash
pip install requests
```

### Step 3: Set API Key

```bash
export FAL_API_KEY="c42f7c6b-0ada-4a38-8a6e-604330d64156:bc3dc6a72347cbb32e4a8d3ea53ef335"
```

Or set in your environment:

```bash
export FAL_KEY="c42f7c6b-0ada-4a38-8a6e-604330d64156:bc3dc6a72347cbb32e4a8d3ea53ef335"
```

### Step 4: Test Connection

Ask Claude to test the API:

```
Test my nanobanana pro API connection by generating a simple test image.
```

Claude will run:

```python
from fal_api import NanobananProClient

client = NanobananProClient()
result = client.generate_image(
    prompt="A red cube on a white background, minimalist, professional quality, 4K",
    num_images=1,
    resolution="2K"
)
print(f"✅ Generated: {result['images'][0]['url']}")
```

## Claude Code Integration Patterns

### Pattern 1: Single Asset Generation

```python
from claude_integration import generate_product

result = generate_product(
    product_name="Luxury Watch",
    description="A luxury leather watch with gold accents",
    style="professional product photography",
    num_variations=3
)

for img in result['images']:
    print(f"Generated: {img}")
```

### Pattern 2: Social Campaign

```python
from claude_integration import generate_social

platforms = ["instagram", "linkedin", "twitter"]
for platform in platforms:
    result = generate_social(
        platform=platform,
        topic="Product Launch",
        description="Eye-catching post for product launch",
        num_variations=1
    )
    print(f"{platform}: {result['images']}")
```

### Pattern 3: Brand Identity

```python
from claude_integration import generate_brand

assets = ["logo", "icon", "pattern"]
for asset_type in assets:
    result = generate_brand(
        brand_name="TechCorp",
        element_type=asset_type,
        description=f"Modern {asset_type} for tech company",
        num_variations=1
    )
    print(f"{asset_type}: {result['images']}")
```

### Pattern 4: Batch Generation

```python
from claude_integration import batch_generate_assets

assets = [
    {
        "type": "product",
        "name": "Watch",
        "description": "Luxury leather watch with gold accents",
        "style": "professional product photography",
        "num_variations": 2
    },
    {
        "type": "social",
        "platform": "instagram",
        "topic": "Product Launch",
        "description": "Instagram post for launch",
        "num_variations": 1
    },
    {
        "type": "brand",
        "brand_name": "TechCorp",
        "element_type": "logo",
        "description": "Modern tech logo",
        "num_variations": 1
    }
]

results = batch_generate_assets(assets)
for result in results:
    print(f"{result['asset_name']}: {result['images']}")
```

### Pattern 5: Custom Asset with Web Search

```python
from claude_integration import generate_asset

result = generate_asset(
    category="infographics",
    name="tech-trends-2025",
    prompt="Create an infographic of top tech trends for 2025 based on current data",
    num_variations=1,
    enable_web_search=True
)

print(f"Generated: {result['images']}")
```

## Nanobanana Pro Parameters

### Resolution Options

```
1K   — Small, fast generation
2K   — Default, balanced quality
4K   — Large, maximum detail
```

### Aspect Ratios

```
21:9  — Ultra-wide
16:9  — Widescreen
3:2   — Standard
4:3   — Square-ish
5:4   — Square-ish
1:1   — Square (default)
4:5   — Portrait
3:4   — Portrait
2:3   — Portrait
9:16  — Mobile portrait
```

### Output Formats

```
png   — Lossless, best for graphics (default)
jpeg  — Compressed, smaller file size
webp  — Modern format, good compression
```

### Web Search Integration

Enable Google Search for real-time data:

```python
result = generate_asset(
    category="infographics",
    name="stock-trends",
    prompt="Visualize current stock market trends",
    enable_web_search=True
)
```

## Workflow Templates

### Workflow 1: E-Commerce Product Launch

```python
from claude_integration import batch_generate_assets

# Generate complete product launch assets
assets = [
    # Product photos
    {"type": "product", "name": "watch", "description": "Luxury watch", "num_variations": 4},
    {"type": "product", "name": "wallet", "description": "Premium wallet", "num_variations": 3},
    
    # Social graphics
    {"type": "social", "platform": "instagram", "topic": "launch", "description": "Instagram post", "num_variations": 2},
    {"type": "social", "platform": "linkedin", "topic": "launch", "description": "LinkedIn post", "num_variations": 1},
    {"type": "social", "platform": "twitter", "topic": "launch", "description": "Twitter post", "num_variations": 1},
    
    # Brand assets
    {"type": "brand", "brand_name": "MyBrand", "element_type": "logo", "description": "Brand logo", "num_variations": 2},
]

results = batch_generate_assets(assets)
print(f"Generated {len(results)} asset groups")
```

### Workflow 2: Content Creator Series

```python
from claude_integration import generate_social, generate_asset

# Generate content series for a week
topics = ["AI Trends", "Web3", "Blockchain", "NFTs", "Metaverse"]

for topic in topics:
    # Generate thumbnail
    thumbnail = generate_asset(
        category="thumbnails",
        name=f"video-{topic.lower()}",
        prompt=f"YouTube thumbnail for {topic} video, bold design, eye-catching",
        num_variations=1
    )
    
    # Generate social post
    post = generate_social(
        platform="twitter",
        topic=topic,
        description=f"Tweet about {topic}",
        num_variations=1
    )
    
    print(f"{topic}: thumbnail={thumbnail['images']}, post={post['images']}")
```

### Workflow 3: Brand Refresh

```python
from claude_integration import batch_generate_assets

# Complete brand refresh
assets = [
    # New brand identity
    {"type": "brand", "brand_name": "NewBrand", "element_type": "logo", "description": "Modern logo", "num_variations": 3},
    {"type": "brand", "brand_name": "NewBrand", "element_type": "icon", "description": "App icons", "num_variations": 1},
    {"type": "brand", "brand_name": "NewBrand", "element_type": "pattern", "description": "Brand pattern", "num_variations": 1},
    
    # Marketing graphics
    {"type": "social", "platform": "instagram", "topic": "rebrand", "description": "Rebrand announcement", "num_variations": 2},
    {"type": "social", "platform": "linkedin", "topic": "rebrand", "description": "LinkedIn announcement", "num_variations": 1},
]

results = batch_generate_assets(assets)
print(f"Brand refresh complete: {len(results)} assets generated")
```

## Common Prompting Patterns

### Product Photography

```
A luxury leather watch with gold accents on white background, 
professional product photography, studio lighting with rim light, 
centered composition, sharp focus, 4K, highly detailed
```

### Viral Thumbnail

```
Design a viral video thumbnail with bold colors, eye-catching text overlay, 
high contrast, professional quality, 4K, trending design
```

### Infographic

```
Create a clean, modern infographic summarizing key information. 
Include charts, icons, and legible text. 
Professional quality, 4K, suitable for presentation
```

### Brand Logo

```
Modern tech company logo, geometric style, blue and white colors, 
minimalist design, scalable, professional, clean lines, 
suitable for all media
```

### Social Media Graphic

```
Instagram post graphic for product launch, vibrant colors, 
eye-catching composition, modern design, professional quality, 
trending aesthetic
```

## Troubleshooting

### Problem: API Key Not Found

**Error**: `FAL_API_KEY or FAL_KEY not found`

**Solution**:
```bash
export FAL_API_KEY="your_key_here"
```

Or ask Claude to set it:
```
Set my FAL_API_KEY environment variable to [your_key]
```

### Problem: No Images Generated

**Solution**:
- Check API key is valid
- Verify internet connection
- Try a simpler prompt
- Check nanobanana pro is available

### Problem: Images Don't Match Style

**Solution**:
- Add more specific style descriptors
- Reference your Creative Strategist guide
- Generate multiple variations
- Use conversational editing

### Problem: Generation Too Slow

**Solution**:
- Reduce resolution from 4K to 2K
- Reduce num_images to 1
- Use simpler prompts

## Integration with Creative Skills

The Orchestrator works with all creative skills:

- **Creative Strategist** — Defines your visual direction
- **Image Generation** — Teaches prompting techniques
- **Product Photography** — Creates product shots
- **Social Graphics** — Generates social content
- **Brand Asset** — Creates brand elements
- **Product Video** — Plans video content
- **Talking Head** — Plans presenter videos

## Asset Organization

Generated assets are automatically organized:

```
assets/
├── product-photography/
│   ├── luxury-watch/
│   └── premium-wallet/
├── social-graphics/
│   ├── instagram/
│   ├── linkedin/
│   └── twitter/
├── brand-assets/
│   └── techcorp/
│       ├── logo/
│       ├── icon/
│       └── pattern/
└── thumbnails/
    └── video-1/
```

## Next Steps

1. **Extract automation system** to your project
2. **Install dependencies**: `pip install requests`
3. **Set API key**: `export FAL_API_KEY="your_key"`
4. **Test connection**: Ask Claude to test the API
5. **Choose your workflow**: Pick a template above
6. **Generate assets**: Start creating!

## Quick Commands

**Generate product photo:**
```
Generate 3 product photos for my luxury watch using nanobanana pro
```

**Generate social campaign:**
```
Generate Instagram, LinkedIn, and Twitter posts for my product launch
```

**Generate brand identity:**
```
Generate a complete brand identity including logo, icons, and patterns
```

**Batch generate:**
```
Generate 10 assets for my e-commerce store including product photos and social graphics
```

**Test API:**
```
Test my nanobanana pro API connection
```

---

**You now have complete automation for creative asset generation with nanobanana pro. Start creating! 🚀**
