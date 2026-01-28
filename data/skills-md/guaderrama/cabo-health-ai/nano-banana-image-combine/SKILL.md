---
name: nano-banana-image-combine
description: Combine multiple images using Gemini 2.5 Flash (Nano Banana) via OpenRouter. Use when merging 2-8 images with AI-guided composition.
license: MIT
---

# Nano Banana Image Combination

## Purpose
Combine, merge, and compose multiple images using Google's Gemini 2.5 Flash (codename "Nano Banana") via OpenRouter. Perfect for creating composite images, replacing backgrounds, face swapping, and AI-guided photo manipulation.

## When to Use
- Combining 2+ images into single composition
- Face swapping or identity replacement
- Background replacement
- Creating thumbnails from multiple sources
- AI-guided photo collages
- Portrait + background composition

## Architecture Pattern

### Project Structure
```
backend/
├── services/
│   ├── image_combiner_service.py    # Main combination logic
│   └── openrouter_service.py        # OpenRouter client
├── models/
│   └── combine_models.py            # Pydantic models
├── utils/
│   ├── image_encoding.py            # Base64 encoding
│   └── image_download.py            # Fetch from URLs
└── config/
    └── openrouter_config.py         # Configuration
```

### Installation
```bash
pip install httpx python-dotenv pydantic pillow base64
```

### Environment Setup
```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-...
FRONTEND_URL=http://localhost:3000
NANO_BANANA_MODEL=google/gemini-2.5-flash-image-preview
```

## Quick Start

### Basic Image Combination
```python
import httpx
import base64
from typing import List

async def combine_images(
    image_urls: List[str],
    prompt: str
) -> str:
    """Combine multiple images using Nano Banana"""

    # Encode images to base64
    encoded_images = []
    async with httpx.AsyncClient() as client:
        for url in image_urls:
            response = await client.get(url)
            b64 = base64.b64encode(response.content).decode('utf-8')
            encoded_images.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{b64}"
                }
            })

    # Call OpenRouter
    response = await client.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "HTTP-Referer": os.getenv('FRONTEND_URL')
        },
        json={
            "model": "google/gemini-2.5-flash-image-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *encoded_images
                    ]
                }
            ]
        }
    )

    result = response.json()
    return result["choices"][0]["message"]["content"]
```

## Complete Implementation

### Image Encoding Utility
```python
import httpx
import base64
from PIL import Image
from io import BytesIO
from typing import Tuple

class ImageEncoder:
    @staticmethod
    async def download_image(url: str) -> bytes:
        """Download image from URL"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content

    @staticmethod
    def resize_image(image_bytes: bytes, max_size: Tuple[int, int] = (1024, 1024)) -> bytes:
        """Resize image to reduce API costs"""
        img = Image.open(BytesIO(image_bytes))

        # Calculate new size maintaining aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Convert to RGB if RGBA
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Save to bytes
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        return buffer.getvalue()

    @staticmethod
    def encode_base64(image_bytes: bytes) -> str:
        """Encode image to base64"""
        return base64.b64encode(image_bytes).decode('utf-8')

    @classmethod
    async def prepare_image(cls, url: str, resize: bool = True) -> str:
        """Download, optionally resize, and encode image"""
        image_bytes = await cls.download_image(url)

        if resize:
            image_bytes = cls.resize_image(image_bytes)

        return cls.encode_base64(image_bytes)
```

### Pydantic Models
```python
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Literal

class CombineImagesInput(BaseModel):
    image_urls: List[HttpUrl] = Field(
        min_length=2,
        max_length=8,
        description="URLs of images to combine (2-8 images)"
    )
    prompt: str = Field(
        description="Instructions for how to combine the images",
        examples=[
            "Combine these images into a professional YouTube thumbnail",
            "Replace the background of the person in image 1 with image 2",
            "Create a face swap using the face from image 1 on the body in image 2"
        ]
    )
    style: Literal["natural", "artistic", "professional", "creative"] = "natural"
    output_format: Literal["url", "base64"] = "url"
    resize_inputs: bool = Field(
        default=True,
        description="Resize inputs to 1024x1024 to save costs"
    )

class CombineImagesOutput(BaseModel):
    success: bool
    result_url: str | None = None
    result_base64: str | None = None
    prompt_used: str
    images_processed: int
    error: str | None = None
```

### OpenRouter Service
```python
import httpx
import os
from typing import List, Dict, Any

class OpenRouterService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

    async def chat_with_images(
        self,
        prompt: str,
        images: List[str],  # Base64 encoded
        model: str = "google/gemini-2.5-flash-image-preview",
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """Send chat request with multiple images"""

        # Build content array
        content = [{"type": "text", "text": prompt}]

        # Add images
        for img_b64 in images:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_b64}"
                }
            })

        # Make request
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": self.frontend_url,
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": content
                        }
                    ],
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                }
            )

            response.raise_for_status()
            return response.json()
```

### Complete Combination Service
```python
import asyncio
from typing import List
import os

class ImageCombinationService:
    def __init__(self):
        self.openrouter = OpenRouterService()
        self.encoder = ImageEncoder()

    async def combine_images(
        self,
        input: CombineImagesInput
    ) -> CombineImagesOutput:
        """Main method to combine images"""

        try:
            # Step 1: Download and encode images
            encoded_images = await self._prepare_images(
                input.image_urls,
                resize=input.resize_inputs
            )

            # Step 2: Build prompt
            prompt = self._build_combination_prompt(
                input.prompt,
                input.style,
                len(input.image_urls)
            )

            # Step 3: Call OpenRouter
            response = await self.openrouter.chat_with_images(
                prompt=prompt,
                images=encoded_images
            )

            # Step 4: Extract result
            result = self._extract_result(response, input.output_format)

            return CombineImagesOutput(
                success=True,
                result_url=result if input.output_format == "url" else None,
                result_base64=result if input.output_format == "base64" else None,
                prompt_used=prompt,
                images_processed=len(input.image_urls)
            )

        except Exception as e:
            return CombineImagesOutput(
                success=False,
                prompt_used=input.prompt,
                images_processed=0,
                error=str(e)
            )

    async def _prepare_images(
        self,
        urls: List[str],
        resize: bool
    ) -> List[str]:
        """Download and encode all images concurrently"""
        tasks = [
            self.encoder.prepare_image(str(url), resize=resize)
            for url in urls
        ]
        return await asyncio.gather(*tasks)

    def _build_combination_prompt(
        self,
        user_prompt: str,
        style: str,
        num_images: int
    ) -> str:
        """Build enhanced prompt for better results"""

        style_instructions = {
            "natural": "Create a natural, realistic combination that looks like a single photo.",
            "artistic": "Combine with artistic flair, creative composition, and visual interest.",
            "professional": "Create a clean, professional composition suitable for business use.",
            "creative": "Be bold and creative with the combination, prioritize visual impact."
        }

        return f"""You are an expert image compositor. You have {num_images} images to work with.

USER REQUEST: {user_prompt}

STYLE GUIDELINE: {style_instructions[style]}

REQUIREMENTS:
- Seamlessly blend the images
- Maintain consistent lighting and color balance
- Ensure natural transitions between elements
- Preserve important details from all source images
- Output high-quality composition

Generate the combined image now."""

    def _extract_result(self, response: Dict[str, Any], format: str) -> str:
        """Extract URL or base64 from response"""
        content = response["choices"][0]["message"]["content"]

        # Nano Banana returns image URL in content
        if format == "url":
            # Extract URL from markdown or plain text
            import re
            url_match = re.search(r'https?://[^\s]+', content)
            if url_match:
                return url_match.group(0)
            return content

        return content
```

## Advanced Use Cases

### Face Swap
```python
async def face_swap(
    face_image_url: str,
    body_image_url: str
) -> str:
    """Swap face from one image onto body in another"""

    input = CombineImagesInput(
        image_urls=[face_image_url, body_image_url],
        prompt="""Take the face from image 1 and naturally place it on the person in image 2.
        Ensure:
        - Face matches body's angle and lighting
        - Natural skin tone blending
        - Consistent shadows and highlights
        - No visible seams""",
        style="natural"
    )

    service = ImageCombinationService()
    result = await service.combine_images(input)
    return result.result_url
```

### Background Replacement
```python
async def replace_background(
    subject_url: str,
    background_url: str,
    depth_of_field: bool = True
) -> str:
    """Replace background while preserving subject"""

    dof_instruction = "Apply subtle depth of field blur to background" if depth_of_field else ""

    input = CombineImagesInput(
        image_urls=[subject_url, background_url],
        prompt=f"""Extract the main subject from image 1 and place it naturally on the background from image 2.

        Requirements:
        - Clean subject extraction with natural edges
        - Match lighting conditions between subject and background
        - Natural shadows under subject
        {dof_instruction}
        - Professional composition""",
        style="professional"
    )

    service = ImageCombinationService()
    result = await service.combine_images(input)
    return result.result_url
```

### Multi-Image Collage
```python
async def create_collage(
    image_urls: List[str],
    layout: Literal["grid", "creative", "storytelling"] = "grid",
    title: str | None = None
) -> str:
    """Create artistic collage from multiple images"""

    layout_prompts = {
        "grid": "Arrange images in a clean grid layout with equal spacing",
        "creative": "Create an artistic, overlapping composition with varied sizes",
        "storytelling": "Arrange images to tell a visual story, left to right"
    }

    title_text = f"Include the text '{title}' as a prominent title" if title else ""

    input = CombineImagesInput(
        image_urls=image_urls,
        prompt=f"""{layout_prompts[layout]}. {title_text}

        Create a cohesive collage that:
        - Maintains visual balance
        - Uses consistent color grading
        - Has professional spacing and alignment
        - Feels unified despite multiple sources""",
        style="artistic"
    )

    service = ImageCombinationService()
    result = await service.combine_images(input)
    return result.result_url
```

### YouTube Thumbnail Creator
```python
async def create_youtube_thumbnail(
    portrait_url: str,
    background_url: str,
    title_text: str,
    style: Literal["tech", "gaming", "vlog", "tutorial"] = "tech"
) -> str:
    """Create engaging YouTube thumbnail"""

    style_guides = {
        "tech": "Clean, modern, professional tech aesthetic with blue/purple tones",
        "gaming": "High energy, vibrant colors, action-oriented composition",
        "vlog": "Personal, inviting, warm tones, casual composition",
        "tutorial": "Clear, educational, step-by-step visual hierarchy"
    }

    input = CombineImagesInput(
        image_urls=[portrait_url, background_url],
        prompt=f"""Create a professional YouTube thumbnail combining these images.

        STYLE: {style_guides[style]}

        TEXT TO INCLUDE: "{title_text}"

        REQUIREMENTS:
        - 1280x720 resolution (16:9 aspect ratio)
        - Bold, readable text overlay
        - High contrast for thumbnail visibility
        - Portrait positioned prominently
        - Background provides context without distraction
        - Eye-catching composition that stops scrolling
        - Professional color grading""",
        style="professional",
        resize_inputs=False  # Keep original quality
    )

    service = ImageCombinationService()
    result = await service.combine_images(input)
    return result.result_url
```

## FastAPI Integration

### Complete API Endpoint
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import List

app = FastAPI()

# Global service instance
combiner_service = ImageCombinationService()

@app.post("/api/combine-images", response_model=CombineImagesOutput)
async def combine_images_endpoint(request: CombineImagesInput):
    """Combine multiple images using Nano Banana"""
    try:
        result = await combiner_service.combine_images(request)

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/face-swap")
async def face_swap_endpoint(
    face_image_url: HttpUrl,
    body_image_url: HttpUrl
):
    """Face swap shortcut endpoint"""
    try:
        result_url = await face_swap(str(face_image_url), str(body_image_url))
        return {"result_url": result_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/replace-background")
async def replace_background_endpoint(
    subject_url: HttpUrl,
    background_url: HttpUrl,
    depth_of_field: bool = True
):
    """Background replacement endpoint"""
    try:
        result_url = await replace_background(
            str(subject_url),
            str(background_url),
            depth_of_field
        )
        return {"result_url": result_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Tool Calling Integration

### Agent Tool Definition
```python
from pydantic_ai import Agent, Tool

# Define tool for AI agent
combine_images_tool = Tool(
    name="combine_images",
    description="""Combine 2-8 images into a single composition using AI.

    Use cases:
    - Face swapping
    - Background replacement
    - Creating thumbnails
    - Photo collages
    - Portrait + scene composition

    Provide image URLs and clear instructions for combination.""",
    parameters=CombineImagesInput,
    execute=lambda args: ImageCombinationService().combine_images(args)
)

# Register with agent
agent = Agent(
    model='openrouter:openai/gpt-4o',
    tools=[combine_images_tool],
    system_prompt="""You are an AI assistant with image combination capabilities.

    When users select multiple images and ask to combine them, use the combine_images tool.

    Examples of combination requests:
    - "Combine these two"
    - "Put my face on that background"
    - "Create a thumbnail from these images"
    - "Swap faces between these photos"
    """
)
```

### Conversational Integration
```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    selected_images: List[str] = []  # URLs of selected images

@app.post("/api/chat")
async def chat_with_image_context(request: ChatRequest):
    """Chat endpoint with image selection context"""

    # Build system prompt with image context
    system_prompt = "You are a helpful assistant."

    if request.selected_images:
        system_prompt += f"""

        The user has selected {len(request.selected_images)} images:
        {', '.join(request.selected_images)}

        If they ask to combine/merge/blend images, use the combine_images tool."""

    # Agent processes message
    result = await agent.run(
        request.message,
        context={"selected_images": request.selected_images}
    )

    return {"response": result}
```

## Error Handling

### Comprehensive Error Handling
```python
from enum import Enum

class CombineError(Exception):
    """Base combination error"""
    pass

class InvalidImageError(CombineError):
    """Invalid or inaccessible image URL"""
    pass

class APIError(CombineError):
    """OpenRouter API error"""
    pass

async def safe_combine(
    input: CombineImagesInput,
    retry_count: int = 3
) -> CombineImagesOutput:
    """Combine with retry logic"""

    for attempt in range(retry_count):
        try:
            service = ImageCombinationService()
            result = await service.combine_images(input)

            if result.success:
                return result

            # If failed, retry
            if attempt < retry_count - 1:
                await asyncio.sleep(2 ** attempt)
                continue

            return result

        except httpx.HTTPError as e:
            if attempt < retry_count - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            raise APIError(f"OpenRouter API error: {e}")
        except Exception as e:
            raise CombineError(f"Combination failed: {e}")
```

## Best Practices

1. **Resize images before sending** - Reduces API costs and latency
2. **Validate URLs** before downloading - Avoid 404 errors
3. **Use async/await** for concurrent downloads
4. **Implement retry logic** for API failures
5. **Cache results** if same combination requested multiple times
6. **Set timeouts** on HTTP requests (30-60 seconds)
7. **Compress outputs** to WebP for storage efficiency
8. **Monitor costs** - Gemini charges per image token
9. **Provide clear prompts** for better results
10. **Handle rate limits** gracefully

## Cost Optimization

### Pricing (as of 2024)
- Input tokens: $0.30/M
- Output tokens: $2.50/M
- **Image tokens: $1.238/K images**

### Optimization Strategies
```python
# 1. Resize to minimum required dimensions
COST_OPTIMIZED_SIZE = (512, 512)  # Lower cost
BALANCED_SIZE = (1024, 1024)      # Good quality/cost ratio
HIGH_QUALITY_SIZE = (2048, 2048)  # Maximum quality

# 2. Use appropriate quality settings
def optimize_for_cost(img: Image) -> bytes:
    img.thumbnail((1024, 1024))
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=75)  # Lower quality = smaller size
    return buffer.getvalue()

# 3. Cache combinations
from functools import lru_cache

@lru_cache(maxsize=100)
async def cached_combine(image_urls_tuple: tuple, prompt: str):
    return await combine_images(list(image_urls_tuple), prompt)
```

## Common Pitfalls

❌ **Don't**: Send full-resolution images (wastes tokens)
✅ **Do**: Resize to 1024x1024 or smaller

❌ **Don't**: Use vague prompts like "combine these"
✅ **Do**: Provide specific instructions with desired outcome

❌ **Don't**: Forget to validate image URLs
✅ **Do**: Check URLs are accessible before processing

❌ **Don't**: Block API endpoints waiting for result
✅ **Do**: Return immediately, process async if needed

## Complete Production Example

```python
from fastapi import FastAPI
from typing import List
import asyncio

app = FastAPI()
service = ImageCombinationService()

@app.post("/api/tools/combine")
async def combine_tool(
    image_urls: List[HttpUrl],
    prompt: str,
    style: str = "natural"
):
    """Production-ready combination endpoint"""

    # Validate inputs
    if len(image_urls) < 2:
        return {"error": "Need at least 2 images"}

    if len(image_urls) > 8:
        return {"error": "Maximum 8 images allowed"}

    # Create input
    input = CombineImagesInput(
        image_urls=image_urls,
        prompt=prompt,
        style=style,
        resize_inputs=True  # Cost optimization
    )

    # Execute with timeout
    try:
        result = await asyncio.wait_for(
            service.combine_images(input),
            timeout=60.0
        )

        if result.success:
            return {
                "status": "success",
                "result_url": result.result_url,
                "images_processed": result.images_processed
            }
        else:
            return {
                "status": "error",
                "error": result.error
            }

    except asyncio.TimeoutError:
        return {"status": "error", "error": "Combination timeout"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
```

## Resources

- [OpenRouter Gemini Docs](https://openrouter.ai/models/google/gemini-2.5-flash-image-preview)
- [Gemini API Guide](https://ai.google.dev/docs)
- [Image Token Pricing](https://openrouter.ai/docs#pricing)
- [FastAPI Docs](https://fastapi.tiangolo.com)
