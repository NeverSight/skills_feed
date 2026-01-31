---
name: podcast-production
description: Podcast production patterns and workflows. Use when recording podcasts, editing audio, transcribing episodes, generating show notes, RSS feed management, or podcast distribution.
---

# Podcast Production Patterns

Best practices for podcast production, editing, and distribution.

## Recording Setup

### Audio Configuration

```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class AudioSettings:
    sample_rate: int = 48000  # Hz
    bit_depth: int = 24
    channels: int = 1  # Mono per track
    format: str = "wav"  # Lossless for recording

@dataclass
class RecordingTrack:
    name: str
    input_device: str
    settings: AudioSettings
    file_path: str


class RecordingSession:
    def __init__(self, project_name: str, output_dir: str):
        self.project_name = project_name
        self.output_dir = output_dir
        self.tracks: List[RecordingTrack] = []

    def add_track(self, name: str, input_device: str) -> RecordingTrack:
        """Add recording track for participant."""
        settings = AudioSettings()
        file_path = f"{self.output_dir}/{self.project_name}_{name}.wav"

        track = RecordingTrack(
            name=name,
            input_device=input_device,
            settings=settings,
            file_path=file_path
        )
        self.tracks.append(track)
        return track
```

### Remote Recording

```python
import asyncio
import websockets
from dataclasses import dataclass

@dataclass
class RemoteParticipant:
    name: str
    connection_url: str
    local_recording: bool = True  # Record locally for best quality


class RemoteRecordingSession:
    """Coordinate remote podcast recording."""

    def __init__(self):
        self.participants: List[RemoteParticipant] = []
        self.sync_server = None

    async def start_sync_server(self, port: int = 8765):
        """Start sync server for coordinating recording."""
        async def handler(websocket, path):
            async for message in websocket:
                if message == "SYNC":
                    # Broadcast sync signal to all participants
                    await asyncio.gather(*[
                        ws.send("START") for ws in self.connected_clients
                    ])

        self.sync_server = await websockets.serve(handler, "0.0.0.0", port)

    def generate_recording_instructions(self) -> str:
        """Generate instructions for remote participants."""
        return """
## Remote Recording Setup

### Equipment
- Use a USB microphone or audio interface
- Wear headphones to prevent echo
- Choose a quiet room with minimal echo

### Software
- Use Audacity, GarageBand, or similar
- Settings: 48kHz sample rate, 24-bit
- Record in WAV format (not MP3)

### Before Recording
1. Test audio levels (peaks around -12dB)
2. Disable notifications
3. Close unnecessary applications

### During Recording
- Wait for sync signal before speaking
- Clap at start for sync alignment
- Note any interruptions

### After Recording
- Export as WAV
- Upload to shared folder: {upload_link}
- Name file: {episode}_YourName.wav
        """
```

## Audio Editing

### FFmpeg Audio Processing

```bash
# Normalize audio levels
ffmpeg -i input.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.wav

# Remove background noise (using noise profile)
ffmpeg -i input.wav -af "afftdn=nf=-25" cleaned.wav

# Apply compression for consistent levels
ffmpeg -i input.wav -af "acompressor=threshold=-20dB:ratio=4:attack=5:release=50" compressed.wav

# Apply podcast EQ
ffmpeg -i input.wav -af "equalizer=f=100:t=h:w=200:g=-3,equalizer=f=3000:t=h:w=1000:g=2,equalizer=f=8000:t=h:w=2000:g=1" eq.wav

# High-pass filter (remove low rumble)
ffmpeg -i input.wav -af "highpass=f=80" filtered.wav

# De-ess (reduce sibilance)
ffmpeg -i input.wav -af "adeclick=w=55:o=50" deessed.wav

# Complete podcast processing chain
ffmpeg -i input.wav -af "\
    highpass=f=80,\
    afftdn=nf=-25,\
    acompressor=threshold=-20dB:ratio=4:attack=5:release=50,\
    equalizer=f=100:t=h:w=200:g=-3,\
    equalizer=f=3000:t=h:w=1000:g=2,\
    loudnorm=I=-16:TP=-1.5:LRA=11\
" processed.wav
```

### Python Audio Processing

```python
import subprocess
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AudioEdit:
    """Represents an audio edit operation."""
    start_time: float  # seconds
    end_time: float
    operation: str  # cut, silence, crossfade


class PodcastEditor:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.edits: List[AudioEdit] = []

    def cut(self, start: float, end: float):
        """Mark section for removal."""
        self.edits.append(AudioEdit(start, end, "cut"))

    def silence(self, start: float, end: float):
        """Replace section with silence."""
        self.edits.append(AudioEdit(start, end, "silence"))

    def process_edits(self, output_file: str):
        """Apply all edits and export."""
        # Sort edits by start time
        self.edits.sort(key=lambda e: e.start_time)

        # Build filter complex for cuts
        if not self.edits:
            subprocess.run([
                "ffmpeg", "-i", self.input_file,
                "-c:a", "copy", output_file
            ])
            return

        # Generate segments to keep
        segments = []
        current_time = 0

        for edit in self.edits:
            if edit.operation == "cut" and edit.start_time > current_time:
                segments.append((current_time, edit.start_time))
            current_time = edit.end_time

        # Add final segment
        segments.append((current_time, None))

        # Build FFmpeg filter
        filter_parts = []
        for i, (start, end) in enumerate(segments):
            if end:
                filter_parts.append(f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}]")
            else:
                filter_parts.append(f"[0:a]atrim=start={start},asetpts=PTS-STARTPTS[a{i}]")

        # Concatenate segments
        concat_inputs = "".join(f"[a{i}]" for i in range(len(segments)))
        filter_complex = ";".join(filter_parts) + f";{concat_inputs}concat=n={len(segments)}:v=0:a=1[out]"

        subprocess.run([
            "ffmpeg", "-i", self.input_file,
            "-filter_complex", filter_complex,
            "-map", "[out]",
            output_file
        ])

    def normalize(self, output_file: str):
        """Apply loudness normalization."""
        subprocess.run([
            "ffmpeg", "-i", self.input_file,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            output_file
        ])

    def add_intro_outro(
        self,
        intro_file: str,
        outro_file: str,
        output_file: str
    ):
        """Add intro and outro music."""
        subprocess.run([
            "ffmpeg",
            "-i", intro_file,
            "-i", self.input_file,
            "-i", outro_file,
            "-filter_complex",
            "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]",
            "-map", "[out]",
            output_file
        ])

    def mix_background_music(
        self,
        music_file: str,
        output_file: str,
        music_volume: float = 0.1
    ):
        """Mix background music under voice."""
        subprocess.run([
            "ffmpeg",
            "-i", self.input_file,
            "-i", music_file,
            "-filter_complex",
            f"[1:a]volume={music_volume}[music];[0:a][music]amix=inputs=2:duration=first[out]",
            "-map", "[out]",
            output_file
        ])
```

## Transcription

### Whisper Transcription

```python
import whisper
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str
    speaker: Optional[str] = None


class PodcastTranscriber:
    def __init__(self, model_size: str = "medium"):
        self.model = whisper.load_model(model_size)

    def transcribe(
        self,
        audio_file: str,
        language: str = "en"
    ) -> List[TranscriptSegment]:
        """Transcribe audio file."""
        result = self.model.transcribe(
            audio_file,
            language=language,
            word_timestamps=True
        )

        segments = []
        for seg in result["segments"]:
            segments.append(TranscriptSegment(
                start=seg["start"],
                end=seg["end"],
                text=seg["text"].strip()
            ))

        return segments

    def to_srt(self, segments: List[TranscriptSegment]) -> str:
        """Convert to SRT subtitle format."""
        def format_time(seconds: float) -> str:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            millis = int((seconds % 1) * 1000)
            return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

        lines = []
        for i, seg in enumerate(segments, 1):
            lines.append(str(i))
            lines.append(f"{format_time(seg.start)} --> {format_time(seg.end)}")
            lines.append(seg.text)
            lines.append("")

        return "\n".join(lines)

    def to_chapters(
        self,
        segments: List[TranscriptSegment],
        min_gap: float = 5.0
    ) -> List[dict]:
        """Generate chapter markers from transcript."""
        chapters = []
        current_chapter_start = 0
        current_text = []

        for i, seg in enumerate(segments):
            current_text.append(seg.text)

            # Check for chapter break (long pause or topic change)
            if i < len(segments) - 1:
                gap = segments[i + 1].start - seg.end
                if gap > min_gap:
                    chapters.append({
                        "start": current_chapter_start,
                        "end": seg.end,
                        "title": self._summarize_text(" ".join(current_text)[:100])
                    })
                    current_chapter_start = segments[i + 1].start
                    current_text = []

        return chapters

    def _summarize_text(self, text: str) -> str:
        """Extract first sentence as chapter title."""
        sentences = text.split(". ")
        return sentences[0][:50] if sentences else "Chapter"
```

### Speaker Diarization

```python
from pyannote.audio import Pipeline
from dataclasses import dataclass

@dataclass
class SpeakerSegment:
    speaker: str
    start: float
    end: float
    text: Optional[str] = None


class SpeakerDiarizer:
    def __init__(self, auth_token: str):
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=auth_token
        )

    def diarize(self, audio_file: str) -> List[SpeakerSegment]:
        """Identify different speakers."""
        diarization = self.pipeline(audio_file)

        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append(SpeakerSegment(
                speaker=speaker,
                start=turn.start,
                end=turn.end
            ))

        return segments

    def merge_with_transcript(
        self,
        speaker_segments: List[SpeakerSegment],
        transcript_segments: List[TranscriptSegment]
    ) -> List[SpeakerSegment]:
        """Assign speakers to transcript segments."""
        result = []

        for trans in transcript_segments:
            # Find overlapping speaker segment
            best_speaker = None
            best_overlap = 0

            for spk in speaker_segments:
                overlap = min(trans.end, spk.end) - max(trans.start, spk.start)
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_speaker = spk.speaker

            result.append(SpeakerSegment(
                speaker=best_speaker or "Unknown",
                start=trans.start,
                end=trans.end,
                text=trans.text
            ))

        return result
```

## Show Notes Generation

```python
from typing import List
from dataclasses import dataclass

@dataclass
class ShowNotes:
    title: str
    description: str
    highlights: List[str]
    timestamps: List[dict]
    links: List[dict]
    guests: List[dict]


class ShowNotesGenerator:
    def __init__(self, llm_client):
        self.llm = llm_client

    def generate(
        self,
        transcript: str,
        episode_title: str,
        guest_names: List[str] = None
    ) -> ShowNotes:
        """Generate show notes from transcript."""

        # Generate description
        description = self._generate_description(transcript)

        # Extract highlights
        highlights = self._extract_highlights(transcript)

        # Generate timestamps
        timestamps = self._generate_timestamps(transcript)

        # Extract mentioned links/resources
        links = self._extract_resources(transcript)

        return ShowNotes(
            title=episode_title,
            description=description,
            highlights=highlights,
            timestamps=timestamps,
            links=links,
            guests=[{"name": name} for name in (guest_names or [])]
        )

    def _generate_description(self, transcript: str) -> str:
        """Generate episode description."""
        prompt = f"""
        Write a compelling 2-3 paragraph description for this podcast episode.
        Focus on the main topics discussed and key takeaways.

        Transcript excerpt:
        {transcript[:3000]}
        """
        return self.llm.generate(prompt)

    def _extract_highlights(self, transcript: str) -> List[str]:
        """Extract key highlights from episode."""
        prompt = f"""
        Extract 5-7 key highlights or takeaways from this podcast episode.
        Format as bullet points.

        Transcript:
        {transcript[:5000]}
        """
        response = self.llm.generate(prompt)
        return [line.strip("- ") for line in response.split("\n") if line.strip()]

    def _generate_timestamps(self, transcript: str) -> List[dict]:
        """Generate chapter timestamps."""
        # This would use the transcript with timing info
        return []

    def _extract_resources(self, transcript: str) -> List[dict]:
        """Extract mentioned resources and links."""
        prompt = f"""
        Extract any books, websites, tools, or resources mentioned in this podcast.
        Format as: Name | Type | URL (if mentioned)

        Transcript:
        {transcript[:5000]}
        """
        return []

    def to_markdown(self, notes: ShowNotes) -> str:
        """Format show notes as markdown."""
        lines = [
            f"# {notes.title}",
            "",
            notes.description,
            "",
            "## Key Highlights",
            ""
        ]

        for highlight in notes.highlights:
            lines.append(f"- {highlight}")

        if notes.timestamps:
            lines.extend(["", "## Timestamps", ""])
            for ts in notes.timestamps:
                lines.append(f"- [{ts['time']}] {ts['title']}")

        if notes.links:
            lines.extend(["", "## Resources Mentioned", ""])
            for link in notes.links:
                lines.append(f"- [{link['name']}]({link.get('url', '#')})")

        if notes.guests:
            lines.extend(["", "## Guests", ""])
            for guest in notes.guests:
                lines.append(f"- {guest['name']}")

        return "\n".join(lines)
```

## RSS Feed Management

```python
from feedgen.feed import FeedGenerator
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PodcastEpisode:
    title: str
    description: str
    audio_url: str
    pub_date: datetime
    duration: int  # seconds
    episode_number: int
    season: int = 1
    image_url: Optional[str] = None
    explicit: bool = False


@dataclass
class PodcastFeed:
    title: str
    description: str
    author: str
    email: str
    website: str
    image_url: str
    category: str
    language: str = "en"
    explicit: bool = False


class PodcastRSSGenerator:
    def __init__(self, feed_info: PodcastFeed):
        self.feed_info = feed_info
        self.fg = FeedGenerator()
        self._setup_feed()

    def _setup_feed(self):
        """Configure feed metadata."""
        self.fg.load_extension('podcast')

        self.fg.title(self.feed_info.title)
        self.fg.description(self.feed_info.description)
        self.fg.author({'name': self.feed_info.author, 'email': self.feed_info.email})
        self.fg.link(href=self.feed_info.website, rel='alternate')
        self.fg.logo(self.feed_info.image_url)
        self.fg.language(self.feed_info.language)

        # iTunes specific
        self.fg.podcast.itunes_category(self.feed_info.category)
        self.fg.podcast.itunes_author(self.feed_info.author)
        self.fg.podcast.itunes_owner(
            name=self.feed_info.author,
            email=self.feed_info.email
        )
        self.fg.podcast.itunes_image(self.feed_info.image_url)
        self.fg.podcast.itunes_explicit('yes' if self.feed_info.explicit else 'no')

    def add_episode(self, episode: PodcastEpisode):
        """Add episode to feed."""
        fe = self.fg.add_entry()

        fe.title(episode.title)
        fe.description(episode.description)
        fe.enclosure(episode.audio_url, 0, 'audio/mpeg')
        fe.published(episode.pub_date)
        fe.podcast.itunes_duration(episode.duration)
        fe.podcast.itunes_episode(episode.episode_number)
        fe.podcast.itunes_season(episode.season)

        if episode.image_url:
            fe.podcast.itunes_image(episode.image_url)

        fe.podcast.itunes_explicit('yes' if episode.explicit else 'no')

    def generate(self, output_file: str):
        """Generate RSS XML file."""
        self.fg.rss_file(output_file)

    def to_string(self) -> str:
        """Return RSS as string."""
        return self.fg.rss_str(pretty=True).decode('utf-8')
```

## Distribution

```python
from dataclasses import dataclass
from typing import List, Optional
import requests

@dataclass
class DistributionPlatform:
    name: str
    feed_url: str
    dashboard_url: str
    status: str = "pending"


class PodcastDistributor:
    """Manage podcast distribution to platforms."""

    PLATFORMS = {
        "apple": {
            "name": "Apple Podcasts",
            "submit_url": "https://podcastsconnect.apple.com/",
            "requirements": ["RSS feed", "Apple ID", "Artwork 3000x3000"]
        },
        "spotify": {
            "name": "Spotify",
            "submit_url": "https://podcasters.spotify.com/",
            "requirements": ["RSS feed", "Spotify account"]
        },
        "google": {
            "name": "Google Podcasts",
            "submit_url": "https://podcastsmanager.google.com/",
            "requirements": ["RSS feed", "Google account"]
        },
        "amazon": {
            "name": "Amazon Music",
            "submit_url": "https://podcasters.amazon.com/",
            "requirements": ["RSS feed", "Amazon account"]
        },
        "stitcher": {
            "name": "Stitcher",
            "submit_url": "https://partners.stitcher.com/",
            "requirements": ["RSS feed", "Account"]
        }
    }

    def __init__(self, rss_feed_url: str):
        self.rss_feed_url = rss_feed_url
        self.platforms: List[DistributionPlatform] = []

    def validate_feed(self) -> dict:
        """Validate RSS feed for distribution requirements."""
        response = requests.get(self.rss_feed_url)
        # Parse and validate feed structure
        issues = []

        # Check required elements
        required = [
            "title", "description", "language",
            "itunes:author", "itunes:image", "itunes:category"
        ]

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    def generate_submission_guide(self) -> str:
        """Generate submission guide for all platforms."""
        guide = ["# Podcast Distribution Guide\n"]
        guide.append(f"RSS Feed: {self.rss_feed_url}\n")

        for key, platform in self.PLATFORMS.items():
            guide.append(f"\n## {platform['name']}")
            guide.append(f"Submit at: {platform['submit_url']}")
            guide.append("Requirements:")
            for req in platform['requirements']:
                guide.append(f"  - {req}")

        return "\n".join(guide)
```

## References

- [Podcast RSS Best Practices](https://help.apple.com/itc/podcasts_connect/#/itcb54353390)
- [Whisper OpenAI](https://github.com/openai/whisper)
- [PyAnnote Audio](https://github.com/pyannote/pyannote-audio)
- [FFmpeg Audio Filters](https://ffmpeg.org/ffmpeg-filters.html#Audio-Filters)
- [Podcast Hosting Comparison](https://www.podcastinsights.com/best-podcast-hosting/)
