---
name: streaming-patterns
description: Live streaming patterns for YouTube, Twitch, and OBS. Use when setting up live streams, configuring stream keys, RTMP workflows, multi-platform streaming, or real-time broadcast automation.
---

# Live Streaming Patterns

Best practices for live streaming to YouTube, Twitch, and other platforms.

## Platform Configuration

### YouTube Live

```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def create_youtube_broadcast(
    credentials: Credentials,
    title: str,
    description: str,
    scheduled_start: str,
    privacy: str = "unlisted"
):
    """Create a YouTube live broadcast."""
    youtube = build('youtube', 'v3', credentials=credentials)

    # Create broadcast
    broadcast = youtube.liveBroadcasts().insert(
        part="snippet,status,contentDetails",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "scheduledStartTime": scheduled_start
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False
            },
            "contentDetails": {
                "enableAutoStart": True,
                "enableAutoStop": True,
                "enableDvr": True,
                "recordFromStart": True
            }
        }
    ).execute()

    # Create stream
    stream = youtube.liveStreams().insert(
        part="snippet,cdn",
        body={
            "snippet": {
                "title": f"Stream for {title}"
            },
            "cdn": {
                "frameRate": "60fps",
                "ingestionType": "rtmp",
                "resolution": "1080p"
            }
        }
    ).execute()

    # Bind stream to broadcast
    youtube.liveBroadcasts().bind(
        part="id,contentDetails",
        id=broadcast['id'],
        streamId=stream['id']
    ).execute()

    return {
        "broadcast_id": broadcast['id'],
        "stream_key": stream['cdn']['ingestionInfo']['streamName'],
        "rtmp_url": stream['cdn']['ingestionInfo']['ingestionAddress'],
        "watch_url": f"https://youtube.com/watch?v={broadcast['id']}"
    }


def transition_broadcast(credentials: Credentials, broadcast_id: str, status: str):
    """Transition broadcast status: testing, live, complete."""
    youtube = build('youtube', 'v3', credentials=credentials)

    return youtube.liveBroadcasts().transition(
        broadcastStatus=status,
        id=broadcast_id,
        part="status"
    ).execute()
```

### Twitch

```python
import requests

class TwitchAPI:
    def __init__(self, client_id: str, access_token: str):
        self.client_id = client_id
        self.access_token = access_token
        self.base_url = "https://api.twitch.tv/helix"
        self.headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {access_token}"
        }

    def get_stream_key(self, broadcaster_id: str) -> str:
        """Get stream key for broadcaster."""
        response = requests.get(
            f"{self.base_url}/streams/key",
            headers=self.headers,
            params={"broadcaster_id": broadcaster_id}
        )
        return response.json()['data'][0]['stream_key']

    def update_stream_info(
        self,
        broadcaster_id: str,
        title: str,
        game_id: str = None,
        language: str = "en"
    ):
        """Update stream title and category."""
        data = {
            "broadcaster_id": broadcaster_id,
            "title": title,
            "broadcaster_language": language
        }
        if game_id:
            data["game_id"] = game_id

        return requests.patch(
            f"{self.base_url}/channels",
            headers=self.headers,
            json=data
        )

    def get_stream_status(self, user_login: str) -> dict:
        """Check if channel is live."""
        response = requests.get(
            f"{self.base_url}/streams",
            headers=self.headers,
            params={"user_login": user_login}
        )
        data = response.json()['data']
        return data[0] if data else None

    def create_clip(self, broadcaster_id: str) -> dict:
        """Create clip from live stream."""
        response = requests.post(
            f"{self.base_url}/clips",
            headers=self.headers,
            params={"broadcaster_id": broadcaster_id}
        )
        return response.json()['data'][0]
```

## RTMP Streaming

### FFmpeg RTMP Push

```bash
# Stream to YouTube
ffmpeg -re -i input.mp4 \
    -c:v libx264 -preset veryfast -maxrate 4500k -bufsize 9000k \
    -pix_fmt yuv420p -g 60 \
    -c:a aac -b:a 160k -ar 44100 \
    -f flv "rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY"

# Stream to Twitch
ffmpeg -re -i input.mp4 \
    -c:v libx264 -preset veryfast -maxrate 6000k -bufsize 12000k \
    -pix_fmt yuv420p -g 60 \
    -c:a aac -b:a 160k -ar 44100 \
    -f flv "rtmp://live.twitch.tv/app/YOUR_STREAM_KEY"

# Stream desktop (macOS)
ffmpeg -f avfoundation -framerate 30 -i "1:0" \
    -c:v libx264 -preset ultrafast -tune zerolatency \
    -c:a aac -b:a 128k \
    -f flv "rtmp://destination/stream_key"

# Stream desktop (Linux)
ffmpeg -f x11grab -framerate 30 -video_size 1920x1080 -i :0.0 \
    -f pulse -i default \
    -c:v libx264 -preset ultrafast -tune zerolatency \
    -c:a aac -b:a 128k \
    -f flv "rtmp://destination/stream_key"
```

### Multi-Platform Streaming

```bash
# Using tee muxer to stream to multiple platforms
ffmpeg -re -i input.mp4 \
    -c:v libx264 -preset veryfast -b:v 4500k \
    -c:a aac -b:a 160k \
    -f tee -map 0:v -map 0:a \
    "[f=flv]rtmp://a.rtmp.youtube.com/live2/YT_KEY|\
     [f=flv]rtmp://live.twitch.tv/app/TWITCH_KEY|\
     [f=flv]rtmp://live-api-s.facebook.com:443/rtmp/FB_KEY"
```

### Python RTMP Handler

```python
import subprocess
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class StreamDestination:
    name: str
    rtmp_url: str
    stream_key: str

    @property
    def full_url(self) -> str:
        return f"{self.rtmp_url}/{self.stream_key}"


class MultiStreamer:
    def __init__(
        self,
        input_source: str,
        destinations: List[StreamDestination],
        video_bitrate: str = "4500k",
        audio_bitrate: str = "160k"
    ):
        self.input_source = input_source
        self.destinations = destinations
        self.video_bitrate = video_bitrate
        self.audio_bitrate = audio_bitrate
        self.process: Optional[subprocess.Popen] = None

    def build_command(self) -> List[str]:
        """Build FFmpeg command for multi-platform streaming."""
        cmd = [
            "ffmpeg",
            "-re", "-i", self.input_source,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-b:v", self.video_bitrate,
            "-maxrate", self.video_bitrate,
            "-bufsize", str(int(self.video_bitrate[:-1]) * 2) + "k",
            "-pix_fmt", "yuv420p",
            "-g", "60",
            "-c:a", "aac",
            "-b:a", self.audio_bitrate,
            "-ar", "44100"
        ]

        if len(self.destinations) == 1:
            cmd.extend(["-f", "flv", self.destinations[0].full_url])
        else:
            # Use tee muxer for multiple destinations
            tee_outputs = "|".join(
                f"[f=flv]{dest.full_url}" for dest in self.destinations
            )
            cmd.extend([
                "-f", "tee",
                "-map", "0:v", "-map", "0:a",
                tee_outputs
            ])

        return cmd

    def start(self):
        """Start streaming."""
        cmd = self.build_command()
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def stop(self):
        """Stop streaming."""
        if self.process:
            self.process.terminate()
            self.process.wait()
```

## OBS WebSocket Integration

```python
import obswebsocket
from obswebsocket import obsws, requests as obs_requests

class OBSController:
    def __init__(self, host: str = "localhost", port: int = 4455, password: str = ""):
        self.ws = obsws(host, port, password)

    def connect(self):
        self.ws.connect()

    def disconnect(self):
        self.ws.disconnect()

    def start_streaming(self):
        """Start OBS streaming."""
        self.ws.call(obs_requests.StartStream())

    def stop_streaming(self):
        """Stop OBS streaming."""
        self.ws.call(obs_requests.StopStream())

    def start_recording(self):
        """Start OBS recording."""
        self.ws.call(obs_requests.StartRecord())

    def stop_recording(self):
        """Stop OBS recording."""
        self.ws.call(obs_requests.StopRecord())

    def switch_scene(self, scene_name: str):
        """Switch to a different scene."""
        self.ws.call(obs_requests.SetCurrentProgramScene(sceneName=scene_name))

    def get_scenes(self) -> list:
        """Get list of available scenes."""
        response = self.ws.call(obs_requests.GetSceneList())
        return [scene['sceneName'] for scene in response.getScenes()]

    def set_source_visibility(self, scene: str, source: str, visible: bool):
        """Show or hide a source in a scene."""
        self.ws.call(obs_requests.SetSceneItemEnabled(
            sceneName=scene,
            sceneItemId=self._get_source_id(scene, source),
            sceneItemEnabled=visible
        ))

    def _get_source_id(self, scene: str, source: str) -> int:
        """Get source ID by name."""
        response = self.ws.call(obs_requests.GetSceneItemId(
            sceneName=scene,
            sourceName=source
        ))
        return response.getSceneItemId()

    def set_stream_settings(self, server: str, key: str):
        """Update stream settings."""
        self.ws.call(obs_requests.SetStreamServiceSettings(
            streamServiceType="rtmp_common",
            streamServiceSettings={
                "server": server,
                "key": key
            }
        ))
```

## Stream Automation

### Scheduled Stream

```python
import asyncio
from datetime import datetime, timedelta
from typing import Callable

class StreamScheduler:
    def __init__(self):
        self.scheduled_streams = []

    async def schedule_stream(
        self,
        start_time: datetime,
        duration: timedelta,
        start_callback: Callable,
        stop_callback: Callable
    ):
        """Schedule a stream for a specific time."""
        now = datetime.now()
        delay = (start_time - now).total_seconds()

        if delay > 0:
            await asyncio.sleep(delay)

        # Start stream
        await start_callback()

        # Wait for duration
        await asyncio.sleep(duration.total_seconds())

        # Stop stream
        await stop_callback()


# Usage
async def main():
    scheduler = StreamScheduler()
    obs = OBSController()
    obs.connect()

    start_time = datetime.now() + timedelta(minutes=5)
    duration = timedelta(hours=2)

    await scheduler.schedule_stream(
        start_time=start_time,
        duration=duration,
        start_callback=lambda: obs.start_streaming(),
        stop_callback=lambda: obs.stop_streaming()
    )
```

### Chat Bot Integration

```python
from twitchio.ext import commands

class StreamBot(commands.Bot):
    def __init__(self, token: str, prefix: str, channels: list):
        super().__init__(token=token, prefix=prefix, initial_channels=channels)
        self.obs = OBSController()
        self.obs.connect()

    async def event_ready(self):
        print(f'Bot is ready | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    @commands.command(name='scene')
    async def scene_command(self, ctx, scene_name: str):
        """Switch OBS scene via chat command."""
        if ctx.author.is_mod:
            try:
                self.obs.switch_scene(scene_name)
                await ctx.send(f"Switched to scene: {scene_name}")
            except Exception as e:
                await ctx.send(f"Error switching scene: {e}")

    @commands.command(name='brb')
    async def brb_command(self, ctx):
        """Switch to BRB scene."""
        if ctx.author.is_mod:
            self.obs.switch_scene("BRB")
            await ctx.send("Be right back!")

    @commands.command(name='back')
    async def back_command(self, ctx):
        """Switch back to main scene."""
        if ctx.author.is_mod:
            self.obs.switch_scene("Main")
            await ctx.send("We're back!")
```

## Stream Quality Presets

```python
from dataclasses import dataclass
from enum import Enum

class StreamQuality(Enum):
    LOW = "480p"
    MEDIUM = "720p"
    HIGH = "1080p"
    ULTRA = "1440p"

@dataclass
class EncodingPreset:
    resolution: str
    video_bitrate: str
    audio_bitrate: str
    framerate: int
    preset: str

QUALITY_PRESETS = {
    StreamQuality.LOW: EncodingPreset(
        resolution="854x480",
        video_bitrate="1500k",
        audio_bitrate="96k",
        framerate=30,
        preset="veryfast"
    ),
    StreamQuality.MEDIUM: EncodingPreset(
        resolution="1280x720",
        video_bitrate="3000k",
        audio_bitrate="128k",
        framerate=30,
        preset="veryfast"
    ),
    StreamQuality.HIGH: EncodingPreset(
        resolution="1920x1080",
        video_bitrate="4500k",
        audio_bitrate="160k",
        framerate=60,
        preset="veryfast"
    ),
    StreamQuality.ULTRA: EncodingPreset(
        resolution="2560x1440",
        video_bitrate="9000k",
        audio_bitrate="192k",
        framerate=60,
        preset="fast"
    )
}
```

## Health Monitoring

```python
import asyncio
from dataclasses import dataclass
from datetime import datetime

@dataclass
class StreamHealth:
    bitrate: float
    dropped_frames: int
    fps: float
    cpu_usage: float
    timestamp: datetime

class StreamMonitor:
    def __init__(self, obs: OBSController):
        self.obs = obs
        self.health_history: list[StreamHealth] = []

    async def monitor(self, interval: float = 5.0):
        """Continuously monitor stream health."""
        while True:
            try:
                stats = self.obs.ws.call(obs_requests.GetStats())
                health = StreamHealth(
                    bitrate=stats.getKbitsPerSec(),
                    dropped_frames=stats.getOutputSkippedFrames(),
                    fps=stats.getActiveFps(),
                    cpu_usage=stats.getCpuUsage(),
                    timestamp=datetime.now()
                )
                self.health_history.append(health)

                # Alert on issues
                if health.dropped_frames > 100:
                    print(f"Warning: High dropped frames: {health.dropped_frames}")
                if health.fps < 25:
                    print(f"Warning: Low FPS: {health.fps}")

            except Exception as e:
                print(f"Monitor error: {e}")

            await asyncio.sleep(interval)
```

## References

- [YouTube Live Streaming API](https://developers.google.com/youtube/v3/live)
- [Twitch API Documentation](https://dev.twitch.tv/docs/api)
- [OBS WebSocket Protocol](https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md)
- [FFmpeg Streaming Guide](https://trac.ffmpeg.org/wiki/StreamingGuide)
