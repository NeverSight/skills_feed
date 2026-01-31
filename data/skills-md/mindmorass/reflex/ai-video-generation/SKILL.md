---
name: ai-video-generation
description: AI video generation patterns using Sora, Runway, Pika, and other AI video tools. Use when generating videos from text prompts, image-to-video conversion, AI video editing, or integrating AI video APIs.
---

# AI Video Generation Patterns

Best practices for generating videos with AI tools.

## Platform Overview

| Platform | Type | Strengths |
|----------|------|-----------|
| Sora | Text-to-Video | Photorealistic, long-form |
| Runway Gen-3 | Text/Image-to-Video | Fast, good motion |
| Pika Labs | Text/Image-to-Video | Stylized, accessible |
| Kling AI | Text-to-Video | Long duration, realistic |
| Luma Dream Machine | Text/Image-to-Video | Coherent motion |
| Stable Video Diffusion | Image-to-Video | Open source |

## Runway API Integration

```python
import requests
from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class GenerationRequest:
    prompt: str
    image_url: Optional[str] = None
    duration: int = 4  # seconds
    aspect_ratio: str = "16:9"
    motion_strength: int = 5  # 1-10

@dataclass
class GenerationResult:
    id: str
    status: str
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


class RunwayClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.runwayml.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate_video(self, request: GenerationRequest) -> GenerationResult:
        """Generate video from text or image prompt."""
        payload = {
            "model": "gen3a_turbo",
            "prompt": request.prompt,
            "duration": request.duration,
            "aspectRatio": request.aspect_ratio
        }

        if request.image_url:
            payload["imageUrl"] = request.image_url
            payload["mode"] = "image-to-video"
        else:
            payload["mode"] = "text-to-video"

        response = requests.post(
            f"{self.base_url}/generations",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        return GenerationResult(
            id=data["id"],
            status=data["status"]
        )

    def get_generation(self, generation_id: str) -> GenerationResult:
        """Check status of generation."""
        response = requests.get(
            f"{self.base_url}/generations/{generation_id}",
            headers=self.headers
        )
        response.raise_for_status()
        data = response.json()

        return GenerationResult(
            id=data["id"],
            status=data["status"],
            video_url=data.get("output", {}).get("videoUrl"),
            thumbnail_url=data.get("output", {}).get("thumbnailUrl")
        )

    def wait_for_completion(
        self,
        generation_id: str,
        poll_interval: float = 5.0,
        timeout: float = 300.0
    ) -> GenerationResult:
        """Poll until generation completes."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            result = self.get_generation(generation_id)

            if result.status == "SUCCEEDED":
                return result
            elif result.status == "FAILED":
                raise Exception(f"Generation failed: {generation_id}")

            time.sleep(poll_interval)

        raise TimeoutError(f"Generation timed out: {generation_id}")

    def generate_and_wait(self, request: GenerationRequest) -> GenerationResult:
        """Generate video and wait for completion."""
        initial = self.generate_video(request)
        return self.wait_for_completion(initial.id)
```

## Pika Labs Integration

```python
class PikaClient:
    """Pika Labs API client (when API available)."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pika.art/v1"

    def text_to_video(
        self,
        prompt: str,
        negative_prompt: str = "",
        style: str = "realistic",  # realistic, anime, 3d-animation
        duration: int = 3,
        fps: int = 24
    ) -> dict:
        """Generate video from text prompt."""
        response = requests.post(
            f"{self.base_url}/generate",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "prompt": prompt,
                "negativePrompt": negative_prompt,
                "style": style,
                "duration": duration,
                "fps": fps
            }
        )
        return response.json()

    def image_to_video(
        self,
        image_url: str,
        motion_prompt: str,
        motion_strength: float = 1.0
    ) -> dict:
        """Animate an image."""
        response = requests.post(
            f"{self.base_url}/animate",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "imageUrl": image_url,
                "motionPrompt": motion_prompt,
                "motionStrength": motion_strength
            }
        )
        return response.json()
```

## Stable Video Diffusion (Local)

```python
import torch
from diffusers import StableVideoDiffusionPipeline
from PIL import Image

class StableVideoGenerator:
    def __init__(self, model_id: str = "stabilityai/stable-video-diffusion-img2vid-xt"):
        self.pipe = StableVideoDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            variant="fp16"
        )
        self.pipe.to("cuda")

    def generate(
        self,
        image_path: str,
        num_frames: int = 25,
        fps: int = 7,
        motion_bucket_id: int = 127,
        noise_aug_strength: float = 0.02,
        decode_chunk_size: int = 8
    ) -> list:
        """Generate video from image."""
        image = Image.open(image_path).resize((1024, 576))

        frames = self.pipe(
            image,
            num_frames=num_frames,
            motion_bucket_id=motion_bucket_id,
            noise_aug_strength=noise_aug_strength,
            decode_chunk_size=decode_chunk_size
        ).frames[0]

        return frames

    def save_video(self, frames: list, output_path: str, fps: int = 7):
        """Save frames as video."""
        from diffusers.utils import export_to_video
        export_to_video(frames, output_path, fps=fps)
```

## Prompt Engineering for Video

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class VideoPrompt:
    subject: str
    action: str
    setting: str
    style: Optional[str] = None
    camera: Optional[str] = None
    lighting: Optional[str] = None
    mood: Optional[str] = None

    def to_prompt(self) -> str:
        """Build optimized prompt string."""
        parts = [
            f"{self.subject} {self.action}",
            f"in {self.setting}" if self.setting else "",
        ]

        modifiers = []
        if self.style:
            modifiers.append(self.style)
        if self.camera:
            modifiers.append(f"{self.camera} shot")
        if self.lighting:
            modifiers.append(f"{self.lighting} lighting")
        if self.mood:
            modifiers.append(f"{self.mood} mood")

        if modifiers:
            parts.append(", ".join(modifiers))

        return ", ".join(filter(None, parts))


class PromptLibrary:
    """Common prompt patterns for video generation."""

    CAMERA_MOVEMENTS = [
        "slow zoom in",
        "slow zoom out",
        "dolly shot",
        "tracking shot",
        "pan left to right",
        "crane shot",
        "steady cam",
        "handheld",
        "aerial drone shot",
        "first person POV"
    ]

    STYLES = [
        "cinematic",
        "photorealistic",
        "anime style",
        "3D animation",
        "stop motion",
        "vintage film grain",
        "documentary style",
        "music video aesthetic",
        "noir",
        "cyberpunk"
    ]

    LIGHTING = [
        "golden hour",
        "blue hour",
        "dramatic shadows",
        "soft diffused",
        "neon lights",
        "natural sunlight",
        "studio lighting",
        "candlelight",
        "moonlight",
        "backlit silhouette"
    ]

    @staticmethod
    def build_cinematic_prompt(
        subject: str,
        action: str,
        setting: str
    ) -> str:
        """Build a cinematic video prompt."""
        prompt = VideoPrompt(
            subject=subject,
            action=action,
            setting=setting,
            style="cinematic, high production value",
            camera="slow tracking",
            lighting="dramatic",
            mood="epic"
        )
        return prompt.to_prompt()

    @staticmethod
    def build_product_prompt(product: str, features: List[str]) -> str:
        """Build product showcase prompt."""
        return f"{product} rotating on clean white background, {', '.join(features)}, professional product photography, soft studio lighting, 4K quality"

    @staticmethod
    def build_nature_prompt(scene: str, atmosphere: str) -> str:
        """Build nature/landscape prompt."""
        return f"beautiful {scene}, {atmosphere} atmosphere, cinematic wide shot, golden hour lighting, National Geographic style, 8K quality"
```

## Batch Generation

```python
import asyncio
from dataclasses import dataclass
from typing import List
from enum import Enum

class GenerationStatus(Enum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class BatchJob:
    id: str
    prompt: str
    status: GenerationStatus = GenerationStatus.PENDING
    result_url: Optional[str] = None
    error: Optional[str] = None


class BatchGenerator:
    def __init__(self, runway_client: RunwayClient):
        self.client = runway_client
        self.jobs: List[BatchJob] = []

    def add_job(self, prompt: str) -> str:
        """Add generation job to batch."""
        import uuid
        job_id = str(uuid.uuid4())
        job = BatchJob(id=job_id, prompt=prompt)
        self.jobs.append(job)
        return job_id

    async def process_job(self, job: BatchJob, semaphore: asyncio.Semaphore):
        """Process single job with concurrency control."""
        async with semaphore:
            job.status = GenerationStatus.GENERATING
            try:
                request = GenerationRequest(prompt=job.prompt)
                result = await asyncio.to_thread(
                    self.client.generate_and_wait, request
                )
                job.status = GenerationStatus.COMPLETED
                job.result_url = result.video_url
            except Exception as e:
                job.status = GenerationStatus.FAILED
                job.error = str(e)

    async def process_all(self, max_concurrent: int = 3):
        """Process all jobs with concurrency limit."""
        semaphore = asyncio.Semaphore(max_concurrent)

        tasks = [
            self.process_job(job, semaphore)
            for job in self.jobs
        ]

        await asyncio.gather(*tasks)

    def get_results(self) -> dict:
        """Get summary of all jobs."""
        return {
            "total": len(self.jobs),
            "completed": sum(1 for j in self.jobs if j.status == GenerationStatus.COMPLETED),
            "failed": sum(1 for j in self.jobs if j.status == GenerationStatus.FAILED),
            "jobs": [
                {
                    "id": j.id,
                    "prompt": j.prompt[:50] + "...",
                    "status": j.status.value,
                    "url": j.result_url,
                    "error": j.error
                }
                for j in self.jobs
            ]
        }
```

## Video Enhancement

```python
class VideoEnhancer:
    """Post-process AI-generated videos."""

    def __init__(self):
        pass

    def upscale(
        self,
        input_path: str,
        output_path: str,
        scale: int = 2
    ):
        """Upscale video using AI."""
        import subprocess

        # Using Real-ESRGAN for upscaling
        subprocess.run([
            "realesrgan-ncnn-vulkan",
            "-i", input_path,
            "-o", output_path,
            "-s", str(scale),
            "-n", "realesrgan-x4plus"
        ])

    def interpolate_frames(
        self,
        input_path: str,
        output_path: str,
        target_fps: int = 60
    ):
        """Interpolate frames for smoother video."""
        import subprocess

        # Using RIFE for frame interpolation
        subprocess.run([
            "ffmpeg",
            "-i", input_path,
            "-vf", f"minterpolate=fps={target_fps}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            output_path
        ])

    def remove_artifacts(
        self,
        input_path: str,
        output_path: str
    ):
        """Remove common AI artifacts."""
        import subprocess

        subprocess.run([
            "ffmpeg",
            "-i", input_path,
            "-vf", "unsharp=5:5:0.8:3:3:0.4,hqdn3d=3:3:6:6",
            "-c:v", "libx264",
            "-crf", "18",
            output_path
        ])

    def add_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: str
    ):
        """Add audio track to silent AI video."""
        import subprocess

        subprocess.run([
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ])
```

## Storyboard to Video

```python
from dataclasses import dataclass
from typing import List

@dataclass
class StoryboardScene:
    description: str
    duration: int  # seconds
    transition: str = "cut"  # cut, fade, dissolve
    audio: Optional[str] = None

@dataclass
class Storyboard:
    title: str
    scenes: List[StoryboardScene]


class StoryboardRenderer:
    def __init__(self, video_client: RunwayClient):
        self.client = video_client

    async def render_storyboard(self, storyboard: Storyboard) -> List[str]:
        """Generate video for each scene."""
        video_paths = []

        for i, scene in enumerate(storyboard.scenes):
            print(f"Generating scene {i + 1}/{len(storyboard.scenes)}")

            request = GenerationRequest(
                prompt=scene.description,
                duration=scene.duration
            )

            result = self.client.generate_and_wait(request)

            # Download video
            output_path = f"scene_{i:03d}.mp4"
            self._download_video(result.video_url, output_path)
            video_paths.append(output_path)

        return video_paths

    def _download_video(self, url: str, output_path: str):
        """Download video from URL."""
        import requests

        response = requests.get(url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def concatenate_scenes(
        self,
        video_paths: List[str],
        output_path: str
    ):
        """Combine scenes into final video."""
        import subprocess

        # Create file list
        with open('scenes.txt', 'w') as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        subprocess.run([
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", "scenes.txt",
            "-c", "copy",
            output_path
        ])
```

## References

- [Runway API Documentation](https://docs.runwayml.com/)
- [Stable Video Diffusion](https://stability.ai/stable-video)
- [Pika Labs](https://pika.art/)
- [Luma Dream Machine](https://lumalabs.ai/)
- [Kling AI](https://klingai.com/)
