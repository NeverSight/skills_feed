---
name: replicate-integration
description: Integrate Replicate API for AI model deployment. Use when generating images with Flux, SDXL, or custom LoRA models via Replicate.
license: MIT
---

# Replicate API Integration

## Purpose
Deploy and run AI models in production using Replicate's cloud platform. Specialized for image generation with Flux Dev, SDXL, custom LoRA fine-tuning, and prediction polling patterns.

## When to Use
- Generating images with Flux Dev, SDXL, or custom models
- Fine-tuning models with custom LoRA weights
- Running predictions with polling/webhook patterns
- Deploying custom models to production
- Managing long-running AI workloads

## Architecture Pattern

### Project Structure
```
backend/
├── services/
│   ├── replicate_service.py    # Main Replicate client
│   └── model_service.py        # Model-specific logic
├── models/
│   └── replicate_models.py     # Pydantic models
├── config/
│   └── replicate_config.py     # Configuration
└── utils/
    └── polling.py              # Polling utilities
```

### Installation
```bash
pip install replicate httpx python-dotenv pydantic
```

### Environment Setup
```bash
# .env
REPLICATE_API_TOKEN=r8_...
FRONTEND_URL=http://localhost:3000
DEFAULT_MODEL=black-forest-labs/flux-dev
LORA_MODEL_ID=your-username/your-model-id
```

## Quick Start

### Basic Image Generation
```python
import replicate
import os

client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

# Simple prediction
output = client.run(
    "black-forest-labs/flux-dev",
    input={
        "prompt": "A serene mountain landscape at sunset",
        "num_outputs": 1,
        "aspect_ratio": "16:9"
    }
)

print(f"Generated image: {output[0]}")
```

### Async Pattern with Polling
```python
import replicate
import asyncio
from typing import List

async def generate_images_async(
    prompt: str,
    num_images: int = 4
) -> List[str]:
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

    # Start prediction
    prediction = client.predictions.create(
        version="black-forest-labs/flux-dev",
        input={
            "prompt": prompt,
            "num_outputs": num_images,
            "guidance_scale": 3.5,
            "num_inference_steps": 28
        }
    )

    # Poll for completion
    while prediction.status not in ["succeeded", "failed", "canceled"]:
        await asyncio.sleep(1)
        prediction = client.predictions.get(prediction.id)

    if prediction.status == "succeeded":
        return prediction.output
    else:
        raise Exception(f"Prediction failed: {prediction.error}")
```

## Flux Dev Integration

### Complete Flux Dev Configuration
```python
from pydantic import BaseModel, Field
from typing import Literal

class FluxDevInput(BaseModel):
    prompt: str = Field(description="Text description of image to generate")
    aspect_ratio: Literal["1:1", "16:9", "21:9", "3:2", "2:3", "4:5", "5:4", "9:16", "9:21"] = "1:1"
    num_outputs: int = Field(ge=1, le=4, default=1)
    num_inference_steps: int = Field(ge=1, le=50, default=28)
    guidance_scale: float = Field(ge=0, le=10, default=3.5)
    output_format: Literal["webp", "jpg", "png"] = "webp"
    output_quality: int = Field(ge=0, le=100, default=80)
    seed: int | None = None
    disable_safety_checker: bool = False

async def generate_flux_images(input: FluxDevInput) -> List[str]:
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

    output = await client.async_run(
        "black-forest-labs/flux-dev",
        input=input.model_dump()
    )

    return output
```

### Flux Dev Best Practices
```python
# Optimal settings for portraits
PORTRAIT_CONFIG = {
    "aspect_ratio": "2:3",
    "num_inference_steps": 30,
    "guidance_scale": 4.0,
    "output_format": "webp",
    "output_quality": 90
}

# Optimal settings for landscapes
LANDSCAPE_CONFIG = {
    "aspect_ratio": "16:9",
    "num_inference_steps": 28,
    "guidance_scale": 3.5,
    "output_format": "webp",
    "output_quality": 85
}

# Batch generation pattern
async def batch_generate(prompts: List[str]) -> List[List[str]]:
    tasks = [generate_flux_images(FluxDevInput(prompt=p)) for p in prompts]
    return await asyncio.gather(*tasks)
```

## LoRA Fine-Tuning Integration

### Using Custom LoRA Models
```python
class LoRAInput(BaseModel):
    prompt: str
    lora_scale: float = Field(ge=0, le=1, default=1.0, description="LoRA influence strength")
    trigger_word: str | None = Field(default=None, description="Special token for identity")
    num_outputs: int = Field(ge=1, le=10, default=1)

async def generate_with_lora(
    model_id: str,  # e.g., "daniel-carreon/danielcarrong"
    input: LoRAInput
) -> List[str]:
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

    # Ensure trigger word is in prompt
    prompt = input.prompt
    if input.trigger_word and input.trigger_word not in prompt:
        prompt = f"{input.trigger_word} {prompt}"

    output = await client.async_run(
        model_id,
        input={
            "prompt": prompt,
            "lora_scale": input.lora_scale,
            "num_outputs": input.num_outputs,
            "num_inference_steps": 28,
            "guidance_scale": 3.5
        }
    )

    return output
```

### Training Custom LoRA
```python
async def train_lora(
    images_zip_url: str,
    trigger_word: str,
    steps: int = 1000
) -> str:
    """Train custom LoRA model on Replicate"""
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

    training = client.trainings.create(
        version="ostris/flux-dev-lora-trainer",
        input={
            "input_images": images_zip_url,
            "trigger_word": trigger_word,
            "steps": steps,
            "lora_rank": 16,
            "optimizer": "adamw8bit",
            "batch_size": 1,
            "learning_rate": 4e-4,
            "caption_prefix": f"a photo of {trigger_word}"
        },
        destination=f"{os.getenv('REPLICATE_USERNAME')}/my-lora-model"
    )

    # Wait for training completion
    while training.status not in ["succeeded", "failed", "canceled"]:
        await asyncio.sleep(30)
        training = client.trainings.get(training.id)

    if training.status == "succeeded":
        return training.output  # Model URL
    else:
        raise Exception(f"Training failed: {training.error}")
```

## Polling Patterns

### Robust Polling with Retry
```python
import asyncio
from typing import Callable, Any

class PollConfig(BaseModel):
    max_wait: int = 300  # 5 minutes
    poll_interval: float = 1.0  # 1 second
    timeout_multiplier: float = 1.5  # Backoff factor

async def poll_prediction(
    prediction_id: str,
    on_progress: Callable[[float], None] | None = None
) -> Any:
    """Poll Replicate prediction with exponential backoff"""
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

    start_time = asyncio.get_event_loop().time()
    poll_interval = 1.0

    while True:
        prediction = client.predictions.get(prediction_id)

        # Report progress
        if on_progress and hasattr(prediction, 'logs'):
            progress = extract_progress(prediction.logs)
            on_progress(progress)

        # Check status
        if prediction.status == "succeeded":
            return prediction.output
        elif prediction.status in ["failed", "canceled"]:
            raise Exception(f"Prediction {prediction.status}: {prediction.error}")

        # Timeout check
        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed > 300:  # 5 minutes
            raise TimeoutError(f"Prediction timeout after {elapsed}s")

        # Exponential backoff
        await asyncio.sleep(poll_interval)
        poll_interval = min(poll_interval * 1.5, 5.0)

def extract_progress(logs: str) -> float:
    """Extract progress from logs (0.0 to 1.0)"""
    # Example: "Progress: 50%"
    import re
    match = re.search(r"Progress: (\d+)%", logs or "")
    return float(match.group(1)) / 100 if match else 0.0
```

### Webhook Pattern (Production)
```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhooks/replicate")
async def handle_webhook(request: Request):
    """Handle Replicate webhook callback"""
    payload = await request.json()

    prediction_id = payload["id"]
    status = payload["status"]

    if status == "succeeded":
        output = payload["output"]
        # Process completed prediction
        await save_results(prediction_id, output)
    elif status == "failed":
        error = payload["error"]
        # Handle error
        await log_error(prediction_id, error)

    return {"status": "received"}

# Start prediction with webhook
def create_prediction_with_webhook(prompt: str) -> str:
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

    prediction = client.predictions.create(
        version="black-forest-labs/flux-dev",
        input={"prompt": prompt},
        webhook=f"{os.getenv('BACKEND_URL')}/webhooks/replicate",
        webhook_events_filter=["completed"]
    )

    return prediction.id
```

## Error Handling

### Comprehensive Error Handling
```python
from enum import Enum

class ReplicateError(Exception):
    """Base Replicate error"""
    pass

class RateLimitError(ReplicateError):
    """Rate limit exceeded"""
    pass

class ModelNotFoundError(ReplicateError):
    """Model not found"""
    pass

async def safe_replicate_call(
    model: str,
    input: dict,
    max_retries: int = 3
) -> Any:
    """Call Replicate with retry logic"""
    client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

    for attempt in range(max_retries):
        try:
            output = await client.async_run(model, input=input)
            return output
        except replicate.exceptions.ModelError as e:
            if "not found" in str(e).lower():
                raise ModelNotFoundError(f"Model {model} not found")
            raise
        except replicate.exceptions.ReplicateError as e:
            if "rate limit" in str(e).lower():
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise RateLimitError("Rate limit exceeded")
            raise ReplicateError(f"Replicate error: {e}")
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                continue
            raise
```

## FastAPI Integration

### Complete Replicate Endpoint
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    num_images: int = 4
    use_lora: bool = False
    lora_model_id: str | None = None

class GenerateResponse(BaseModel):
    prediction_id: str
    status: str
    images: List[str] | None = None

@app.post("/generate", response_model=GenerateResponse)
async def generate_images(request: GenerateRequest):
    """Generate images using Replicate"""
    try:
        client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

        # Select model
        model = request.lora_model_id if request.use_lora else "black-forest-labs/flux-dev"

        # Create prediction
        prediction = client.predictions.create(
            version=model,
            input={
                "prompt": request.prompt,
                "num_outputs": request.num_images
            }
        )

        return GenerateResponse(
            prediction_id=prediction.id,
            status=prediction.status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions/{prediction_id}")
async def get_prediction(prediction_id: str):
    """Check prediction status"""
    try:
        client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
        prediction = client.predictions.get(prediction_id)

        return GenerateResponse(
            prediction_id=prediction.id,
            status=prediction.status,
            images=prediction.output if prediction.status == "succeeded" else None
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail="Prediction not found")
```

## Rate Limiting

### Rate Limit Management
```python
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int = 50, window: int = 60):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window)
        self.requests: deque[datetime] = deque()

    async def acquire(self):
        """Wait if rate limit reached"""
        now = datetime.now()

        # Remove old requests
        while self.requests and self.requests[0] < now - self.window:
            self.requests.popleft()

        # Check limit
        if len(self.requests) >= self.max_requests:
            wait_time = (self.requests[0] + self.window - now).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)

        self.requests.append(now)

# Usage
limiter = RateLimiter(max_requests=50, window=60)

async def generate_with_limit(prompt: str):
    await limiter.acquire()
    return await generate_flux_images(FluxDevInput(prompt=prompt))
```

## Best Practices

1. **Always use async/await** for non-blocking I/O
2. **Implement polling with backoff** to avoid rate limits
3. **Use webhooks in production** for long-running tasks
4. **Cache prediction results** to avoid redundant API calls
5. **Monitor costs** - log prediction IDs and metrics
6. **Handle errors gracefully** with retry logic
7. **Use typed inputs** with Pydantic models
8. **Set timeouts** for all predictions
9. **Validate outputs** before returning to users
10. **Store metadata** for debugging and analytics

## Common Pitfalls

❌ **Don't**: Poll too frequently (wastes API calls)
✅ **Do**: Use exponential backoff (1s → 1.5s → 2.25s → ...)

❌ **Don't**: Forget to handle prediction failures
✅ **Do**: Check status and handle errors

❌ **Don't**: Hardcode model versions
✅ **Do**: Use environment variables for flexibility

❌ **Don't**: Block on predictions in API endpoints
✅ **Do**: Return prediction ID immediately, poll separately

## Complete Example: Production Service

```python
from fastapi import FastAPI, BackgroundTasks
import replicate
from pydantic import BaseModel
from typing import List
import asyncio

app = FastAPI()

class ImageGenerationService:
    def __init__(self):
        self.client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))
        self.rate_limiter = RateLimiter(max_requests=50, window=60)

    async def generate(
        self,
        prompt: str,
        num_images: int = 4,
        model_id: str = "black-forest-labs/flux-dev"
    ) -> List[str]:
        """Generate images with rate limiting and error handling"""
        await self.rate_limiter.acquire()

        try:
            prediction = self.client.predictions.create(
                version=model_id,
                input={
                    "prompt": prompt,
                    "num_outputs": num_images,
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5
                }
            )

            # Poll for completion
            output = await poll_prediction(
                prediction.id,
                on_progress=lambda p: print(f"Progress: {p*100:.0f}%")
            )

            return output
        except Exception as e:
            print(f"Generation failed: {e}")
            raise

# Global service instance
service = ImageGenerationService()

@app.post("/api/generate")
async def generate_endpoint(request: GenerateRequest):
    try:
        images = await service.generate(
            prompt=request.prompt,
            num_images=request.num_images
        )
        return {"status": "success", "images": images}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

## Resources

- [Replicate Docs](https://replicate.com/docs)
- [Flux Dev Model](https://replicate.com/black-forest-labs/flux-dev)
- [LoRA Training Guide](https://replicate.com/docs/guides/fine-tune-a-language-model)
- [Python Client](https://github.com/replicate/replicate-python)
