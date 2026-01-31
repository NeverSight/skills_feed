---
name: video-upload-patterns
description: Video upload patterns for YouTube, TikTok, and Vimeo. Use when uploading videos to platforms, managing video metadata, scheduling video releases, or handling bulk video uploads.
---

# Video Upload Patterns

Best practices for uploading videos to major platforms.

## YouTube Upload

### Basic Upload

```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def upload_video_youtube(
    credentials: Credentials,
    file_path: str,
    title: str,
    description: str,
    tags: list[str],
    category_id: str = "22",  # People & Blogs
    privacy: str = "private"
) -> dict:
    """Upload video to YouTube."""
    youtube = build('youtube', 'v3', credentials=credentials)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        file_path,
        mimetype='video/*',
        resumable=True,
        chunksize=1024*1024  # 1MB chunks
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploading: {int(status.progress() * 100)}%")

    return response


def set_thumbnail(
    credentials: Credentials,
    video_id: str,
    thumbnail_path: str
):
    """Set custom thumbnail for video."""
    youtube = build('youtube', 'v3', credentials=credentials)

    media = MediaFileUpload(thumbnail_path, mimetype='image/jpeg')

    return youtube.thumbnails().set(
        videoId=video_id,
        media_body=media
    ).execute()


def schedule_video(
    credentials: Credentials,
    video_id: str,
    publish_at: str  # ISO 8601 format
):
    """Schedule video for future publication."""
    youtube = build('youtube', 'v3', credentials=credentials)

    return youtube.videos().update(
        part="status",
        body={
            "id": video_id,
            "status": {
                "privacyStatus": "private",
                "publishAt": publish_at
            }
        }
    ).execute()
```

### Resumable Upload with Progress

```python
import os
import time
from googleapiclient.errors import HttpError

class YouTubeUploader:
    MAX_RETRIES = 10
    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

    def __init__(self, credentials):
        self.youtube = build('youtube', 'v3', credentials=credentials)

    def upload_with_retry(
        self,
        file_path: str,
        metadata: dict,
        progress_callback=None
    ) -> dict:
        """Upload with automatic retry on failure."""
        file_size = os.path.getsize(file_path)

        media = MediaFileUpload(
            file_path,
            mimetype='video/*',
            resumable=True,
            chunksize=5 * 1024 * 1024  # 5MB chunks
        )

        request = self.youtube.videos().insert(
            part="snippet,status",
            body=metadata,
            media_body=media
        )

        response = None
        retry = 0

        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    progress = status.progress()
                    bytes_uploaded = int(file_size * progress)
                    if progress_callback:
                        progress_callback(progress, bytes_uploaded, file_size)

            except HttpError as e:
                if e.resp.status in self.RETRIABLE_STATUS_CODES:
                    retry += 1
                    if retry > self.MAX_RETRIES:
                        raise
                    sleep_seconds = 2 ** retry
                    print(f"Retry {retry}, sleeping {sleep_seconds}s")
                    time.sleep(sleep_seconds)
                else:
                    raise

        return response
```

## TikTok Upload

### Content Posting API

```python
import requests
from dataclasses import dataclass
from typing import Optional

@dataclass
class TikTokVideo:
    video_url: str  # URL to video file
    title: str
    privacy_level: str = "SELF_ONLY"  # SELF_ONLY, MUTUAL_FOLLOW_FRIENDS, FOLLOWER_OF_CREATOR, PUBLIC_TO_EVERYONE
    disable_duet: bool = False
    disable_comment: bool = False
    disable_stitch: bool = False


class TikTokUploader:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://open.tiktokapis.com/v2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def init_video_upload(self, video: TikTokVideo) -> dict:
        """Initialize video upload and get upload URL."""
        response = requests.post(
            f"{self.base_url}/post/publish/video/init/",
            headers=self.headers,
            json={
                "post_info": {
                    "title": video.title,
                    "privacy_level": video.privacy_level,
                    "disable_duet": video.disable_duet,
                    "disable_comment": video.disable_comment,
                    "disable_stitch": video.disable_stitch
                },
                "source_info": {
                    "source": "PULL_FROM_URL",
                    "video_url": video.video_url
                }
            }
        )
        return response.json()

    def check_publish_status(self, publish_id: str) -> dict:
        """Check status of video publishing."""
        response = requests.post(
            f"{self.base_url}/post/publish/status/fetch/",
            headers=self.headers,
            json={"publish_id": publish_id}
        )
        return response.json()

    def upload_from_file(self, file_path: str, video: TikTokVideo) -> dict:
        """Upload video from local file (requires file hosting)."""
        # TikTok requires video URL, so you need to host the file first
        # This is a placeholder for the workflow
        raise NotImplementedError(
            "TikTok requires video URL. Host file and use init_video_upload()"
        )
```

### Direct Upload (Chunk-based)

```python
class TikTokDirectUploader:
    """Direct upload using chunk-based approach."""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://open.tiktokapis.com/v2"

    def init_upload(
        self,
        file_size: int,
        chunk_size: int = 10 * 1024 * 1024  # 10MB
    ) -> dict:
        """Initialize direct upload."""
        total_chunks = (file_size + chunk_size - 1) // chunk_size

        response = requests.post(
            f"{self.base_url}/post/publish/inbox/video/init/",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            },
            json={
                "source_info": {
                    "source": "FILE_UPLOAD",
                    "video_size": file_size,
                    "chunk_size": chunk_size,
                    "total_chunk_count": total_chunks
                }
            }
        )
        return response.json()

    def upload_chunk(
        self,
        upload_url: str,
        chunk_data: bytes,
        chunk_index: int,
        total_chunks: int
    ):
        """Upload a single chunk."""
        response = requests.put(
            upload_url,
            headers={
                "Content-Type": "video/mp4",
                "Content-Range": f"bytes {chunk_index * len(chunk_data)}-{(chunk_index + 1) * len(chunk_data) - 1}/{total_chunks * len(chunk_data)}"
            },
            data=chunk_data
        )
        return response

    def upload_file(self, file_path: str) -> dict:
        """Upload complete file in chunks."""
        import os

        file_size = os.path.getsize(file_path)
        chunk_size = 10 * 1024 * 1024  # 10MB

        # Initialize
        init_response = self.init_upload(file_size, chunk_size)
        upload_url = init_response['data']['upload_url']
        publish_id = init_response['data']['publish_id']

        # Upload chunks
        with open(file_path, 'rb') as f:
            chunk_index = 0
            total_chunks = (file_size + chunk_size - 1) // chunk_size

            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                self.upload_chunk(upload_url, chunk, chunk_index, total_chunks)
                chunk_index += 1
                print(f"Uploaded chunk {chunk_index}/{total_chunks}")

        return {"publish_id": publish_id}
```

## Vimeo Upload

```python
import vimeo

class VimeoUploader:
    def __init__(self, token: str, key: str, secret: str):
        self.client = vimeo.VimeoClient(
            token=token,
            key=key,
            secret=secret
        )

    def upload_video(
        self,
        file_path: str,
        name: str,
        description: str = "",
        privacy: str = "nobody"  # anybody, nobody, password, disable
    ) -> dict:
        """Upload video to Vimeo."""
        uri = self.client.upload(file_path, data={
            'name': name,
            'description': description,
            'privacy': {
                'view': privacy
            }
        })

        # Get video details
        response = self.client.get(uri)
        return response.json()

    def upload_with_progress(
        self,
        file_path: str,
        name: str,
        progress_callback=None
    ) -> dict:
        """Upload with progress tracking."""
        def progress_handler(uploaded, total):
            if progress_callback:
                progress_callback(uploaded / total, uploaded, total)

        uri = self.client.upload(
            file_path,
            data={'name': name},
            progress=progress_handler
        )

        return self.client.get(uri).json()

    def replace_video(self, video_id: str, file_path: str) -> dict:
        """Replace existing video file."""
        uri = f"/videos/{video_id}"
        return self.client.replace(uri, file_path)

    def set_thumbnail(self, video_id: str, time_code: float) -> dict:
        """Set thumbnail from video frame."""
        response = self.client.post(
            f"/videos/{video_id}/pictures",
            data={'time': time_code, 'active': True}
        )
        return response.json()

    def add_to_folder(self, video_id: str, folder_id: str):
        """Add video to folder/project."""
        self.client.put(f"/me/projects/{folder_id}/videos/{video_id}")
```

## Bulk Upload Manager

```python
import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional
from pathlib import Path

class UploadPlatform(Enum):
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    VIMEO = "vimeo"

class UploadStatus(Enum):
    PENDING = "pending"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"

@dataclass
class VideoUploadJob:
    file_path: Path
    title: str
    description: str
    tags: list[str]
    platforms: list[UploadPlatform]
    thumbnail_path: Optional[Path] = None
    scheduled_time: Optional[str] = None
    status: UploadStatus = UploadStatus.PENDING
    results: dict = None

    def __post_init__(self):
        self.results = {}


class BulkUploadManager:
    def __init__(
        self,
        youtube_creds=None,
        tiktok_token=None,
        vimeo_client=None
    ):
        self.youtube_creds = youtube_creds
        self.tiktok_token = tiktok_token
        self.vimeo_client = vimeo_client
        self.jobs: list[VideoUploadJob] = []

    def add_job(self, job: VideoUploadJob):
        """Add upload job to queue."""
        self.jobs.append(job)

    async def process_job(self, job: VideoUploadJob):
        """Process single upload job."""
        job.status = UploadStatus.UPLOADING

        for platform in job.platforms:
            try:
                if platform == UploadPlatform.YOUTUBE and self.youtube_creds:
                    result = upload_video_youtube(
                        self.youtube_creds,
                        str(job.file_path),
                        job.title,
                        job.description,
                        job.tags
                    )
                    job.results['youtube'] = result

                elif platform == UploadPlatform.VIMEO and self.vimeo_client:
                    result = self.vimeo_client.upload_video(
                        str(job.file_path),
                        job.title,
                        job.description
                    )
                    job.results['vimeo'] = result

            except Exception as e:
                job.results[platform.value] = {"error": str(e)}

        job.status = UploadStatus.COMPLETE

    async def process_all(self, concurrent_limit: int = 3):
        """Process all jobs with concurrency limit."""
        semaphore = asyncio.Semaphore(concurrent_limit)

        async def process_with_limit(job):
            async with semaphore:
                await self.process_job(job)

        await asyncio.gather(
            *[process_with_limit(job) for job in self.jobs]
        )

    def get_status_report(self) -> dict:
        """Get status of all jobs."""
        return {
            "total": len(self.jobs),
            "pending": sum(1 for j in self.jobs if j.status == UploadStatus.PENDING),
            "uploading": sum(1 for j in self.jobs if j.status == UploadStatus.UPLOADING),
            "complete": sum(1 for j in self.jobs if j.status == UploadStatus.COMPLETE),
            "failed": sum(1 for j in self.jobs if j.status == UploadStatus.FAILED),
            "jobs": [
                {
                    "file": str(j.file_path),
                    "status": j.status.value,
                    "results": j.results
                }
                for j in self.jobs
            ]
        }
```

## Metadata Templates

```python
from dataclasses import dataclass
from typing import Optional
from string import Template

@dataclass
class VideoMetadataTemplate:
    title_template: str
    description_template: str
    tags: list[str]
    category: str

    def render(self, **kwargs) -> dict:
        """Render template with variables."""
        return {
            "title": Template(self.title_template).safe_substitute(**kwargs),
            "description": Template(self.description_template).safe_substitute(**kwargs),
            "tags": self.tags,
            "category": self.category
        }


# Example templates
GAMING_TEMPLATE = VideoMetadataTemplate(
    title_template="$game_name - $episode_title | Episode $episode_num",
    description_template="""
$episode_title

Welcome back to $game_name! In this episode, we $episode_summary.

Timestamps:
$timestamps

Subscribe for more $game_name content!

#$game_tag #gaming #letsplay
    """.strip(),
    tags=["gaming", "letsplay", "gameplay"],
    category="20"  # Gaming
)

TUTORIAL_TEMPLATE = VideoMetadataTemplate(
    title_template="$topic Tutorial - $subtitle | $series_name",
    description_template="""
Learn $topic in this comprehensive tutorial!

In this video:
$outline

Resources:
$resources

Don't forget to like and subscribe!
    """.strip(),
    tags=["tutorial", "howto", "learn"],
    category="27"  # Education
)
```

## Upload Validation

```python
import subprocess
import os
from dataclasses import dataclass

@dataclass
class VideoValidation:
    is_valid: bool
    duration: float
    resolution: str
    codec: str
    file_size: int
    errors: list[str]

def validate_video(file_path: str, platform: str = "youtube") -> VideoValidation:
    """Validate video meets platform requirements."""
    errors = []

    # Get video info
    probe = subprocess.run([
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        file_path
    ], capture_output=True, text=True)

    import json
    info = json.loads(probe.stdout)
    video_stream = next(s for s in info['streams'] if s['codec_type'] == 'video')

    duration = float(info['format']['duration'])
    file_size = int(info['format']['size'])
    resolution = f"{video_stream['width']}x{video_stream['height']}"
    codec = video_stream['codec_name']

    # Platform-specific validation
    if platform == "youtube":
        if duration > 12 * 3600:  # 12 hours
            errors.append("Video exceeds 12 hour limit")
        if file_size > 256 * 1024 * 1024 * 1024:  # 256GB
            errors.append("File exceeds 256GB limit")

    elif platform == "tiktok":
        if duration > 10 * 60:  # 10 minutes
            errors.append("Video exceeds 10 minute limit")
        if file_size > 4 * 1024 * 1024 * 1024:  # 4GB
            errors.append("File exceeds 4GB limit")

    elif platform == "vimeo":
        if duration > 12 * 3600:
            errors.append("Video exceeds 12 hour limit")

    return VideoValidation(
        is_valid=len(errors) == 0,
        duration=duration,
        resolution=resolution,
        codec=codec,
        file_size=file_size,
        errors=errors
    )
```

## References

- [YouTube Data API](https://developers.google.com/youtube/v3)
- [TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started)
- [Vimeo API](https://developer.vimeo.com/api)
- [FFprobe Documentation](https://ffmpeg.org/ffprobe.html)
