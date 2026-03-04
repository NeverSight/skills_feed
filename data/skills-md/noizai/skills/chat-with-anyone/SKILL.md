---
name: chat-with-anyone
description: Chat with any real person or fictional character in their own voice by automatically finding their speech online, extracting a clean reference sample, and generating audio replies. Use when the user says "我想跟xxx聊天", "你来扮演xxx跟我说话", "让xxx给我讲讲这篇文章", or similar.
---

# Chat with Anyone

Chat with any real person or fictional character in their own voice by automatically finding their speech online, extracting a clean reference sample, and using it to generate replies.

## Triggers
- 我想跟xxx聊天 (I want to chat with xxx)
- 你来扮演xxx跟我说话 (Play the role of xxx and talk to me)
- 让xxx给我讲讲这篇文章 (Let xxx explain this article to me)
- 用xxx的声音说 (Say this in xxx's voice)
- Talk to me like xxx
- Roleplay as xxx

## Workflow

When the user asks you to roleplay or chat as a specific character, follow these steps exactly:

### 1. Character Disambiguation
If the user's description is ambiguous (e.g., "US President", "Spider-Man actor"), ask for clarification first to determine the exact person or specific portrayal they want.

### 2. Find a Reference Video
Use your web search capabilities to find a YouTube, Bilibili, or TikTok video of the character speaking clearly.
- Look for interviews, speeches, or monologues where there is little to no background music.
- Grab the URL of the best candidate video.

### 3. Download Video and Subtitles
Use the `youtube-downloader` skill to download the video and its auto-generated subtitles. Wait for the download to complete before proceeding.

```bash
# Example using youtube-downloader
python skills/youtube-downloader/scripts/download_video.py "VIDEO_URL" -o "tmp/character_audio" --audio-only --subtitles
```

### 4. Extract Audio Segment
Read the downloaded subtitle file (e.g., `.vtt` or `.srt`) to find a continuous 10-30 second segment where the character is speaking clearly without long pauses. Note the start and end timestamps.

Use `ffmpeg` to extract this specific audio segment as a `.wav` file to use as the reference audio.

```bash
# Example: Extracting audio from 00:01:15 to 00:01:30
ffmpeg -y -i "tmp/character_audio/VideoTitle.m4a" -ss 00:01:15 -to 00:01:30 -c:a pcm_s16le -ar 24000 -ac 1 "skills/chat-with-anyone/character_name_ref.wav"
```

### 5. Generate Speech and Roleplay
Respond to the user's prompt while staying in character. Use the `tts` skill with the extracted audio as `--ref-audio` to generate the spoken response. 

```bash
# Example using tts skill
bash skills/tts/scripts/tts.sh speak -t "Hello there! I am ready to chat with you." --ref-audio "skills/character-chat/character_name_ref.wav" -o "output.wav"
```

## Example Conversation

**User**: 我想跟特朗普聊天，让他给我讲个睡前故事。

**Agent**:
1. (Internal) Identify character: Donald Trump.
2. (Internal) Find a good speech video URL: `https://www.youtube.com/watch?v=xxxxxxxx`.
3. (Internal) Download audio & subs:
   `python skills/youtube-downloader/scripts/download_video.py "https://www.youtube.com/watch?v=xxxxxxxx" -o tmp/trump --audio-only --subtitles`
4. (Internal) Read subtitle, find good segment (e.g. 00:02:10 to 00:02:30).
5. (Internal) Extract clean wav:
   `ffmpeg -y -i "tmp/trump/audio.m4a" -ss 00:02:10 -to 00:02:30 -c:a pcm_s16le "skills/chat-with-anyone/trump_ref.wav"`
6. (Internal) Generate TTS:
   `bash skills/tts/scripts/tts.sh speak -t "Let me tell you a tremendous story, maybe the best story ever told..." --ref-audio "skills/chat-with-anyone/trump_ref.wav" -o "trump_story.wav"`
7. **Agent replies**: "Here is the audio of the bedtime story from Donald Trump!" (Presents `trump_story.wav` and the text).

## Dependencies
- **youtube-downloader**: For fetching videos and subtitles.
- **ffmpeg**: For trimming and converting audio formats.
- **tts**: For generating the final speech using `--ref-audio` (typically requires Noiz backend for voice cloning).
