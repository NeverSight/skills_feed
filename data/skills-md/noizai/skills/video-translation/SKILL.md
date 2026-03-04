---
name: video-translation
description: Translate and dub videos from one language to another, replacing the original audio with TTS while keeping the video intact.
---

# Video Translation

Translate a video's speech into another language, using TTS to generate the dubbed audio and replacing the original audio track.

## Triggers

- translate this video
- dub this video to English
- 把视频从 X 语译成 Y 语
- 视频翻译

## Use Cases

- The user wants to watch a foreign language YouTube video but prefers to hear it in their native language.
- The user provides a video link and explicitly requests changing the audio language.

## Workflow

When the user asks to translate a video:

1. **Download Video & Subtitles**:
   Use the `youtube-downloader` skill to download the video and its subtitles as SRT. Make sure you specify the source language to fetch the correct subtitle.
   ```bash
   python path/to/youtube-downloader/scripts/download_video.py "VIDEO_URL" --subtitles --sub-lang <source_lang_code> -o /tmp/video-translation
   ```

2. **Translate Subtitles**:
   Read the downloaded `.srt` file. Translate its contents sentence by sentence into the target language using the following fixed prompt. Keep the exact same SRT index and timestamp format!

   **Translation Prompt**:
   > Translate the following subtitle text from <Source Language> to <Target Language>.
   > Provide ONLY the translated text. Do not explain, do not add notes, do not add index numbers.
   > The translation must be colloquial, natural-sounding, and suitable for video dubbing.

   Save the translated text into a new file `translated.srt`.

3. **Generate Dubbed Audio**:
   Use the `tts` skill to render the timeline-accurate audio from the translated SRT. The Noiz backend automatically aligns the duration of each sentence to the original video's subtitle timestamps.
   
   To ensure the cloned voice matches the original speaker's exact tone and emotion for each sentence, pass the original video file to `--ref-audio-track`. The TTS engine will automatically slice the original audio at each subtitle's exact timestamp and use it as the reference for that specific segment.
   
   Create a basic `voice_map.json`:
   ```json
   {
     "default": {
       "target_lang": "<target_lang_code>"
     }
   }
   ```
   Render the timeline-accurate audio:
   ```bash
   bash skills/tts/scripts/tts.sh render --srt translated.srt --voice-map voice_map.json --backend noiz --auto-emotion --ref-audio-track original_video.mp4 -o dubbed.wav
   ```

4. **Replace Audio in Video**:
   Use the `replace_audio.sh` script to merge the original video with the new dubbed audio. To keep the original video's non-speech audio background outside of translated segments, pass the `--srt` file.
   ```bash
   bash skills/video-translation/scripts/replace_audio.sh --video original_video.mp4 --audio dubbed.wav --output final_video.mp4 --srt translated.srt
   ```

5. **Present the Result**:
   Return the `final_video.mp4` file path to the user.

## Inputs

- **Required inputs**:
  - `VIDEO_URL`: The URL of the video to translate.
  - `target_language`: The language to translate the audio to.
- **Optional inputs**:
  - `source_language`: The language of the original video (if not auto-detected or specified).
  - `reference_audio`: Specific audio file/URL to use for voice cloning instead of the dynamic original video track.

## Outputs

- Success: Path to the final video file with replaced audio.
- Failure: Clear error message specifying whether download, TTS, or audio replacement failed.

## Requirements

- **Dependencies (other skills)**  
  - **youtube-downloader** ([crazynomad/skills](https://github.com/crazynomad/skills)) — [SKILL.md](https://github.com/crazynomad/skills/blob/master/youtube-downloader/SKILL.md)  
    Install: clone or copy the `skills/youtube-downloader` directory from [crazynomad/skills](https://github.com/crazynomad/skills) into your `skills/` folder so that `skills/youtube-downloader/scripts/download_video.py` is available.
  - **tts** ([NoizAI/skills](https://github.com/NoizAI/skills)) — [SKILL.md](https://github.com/NoizAI/skills/blob/main/skills/tts/SKILL.md)  
    If not already in this repo: clone or copy the `skills/tts` directory from [NoizAI/skills](https://github.com/NoizAI/skills) into your `skills/` folder. Ensure `skills/tts/scripts/tts.sh` and related scripts are present.
- `NOIZ_API_KEY` configured for the Noiz backend. If it is not set, first guide the user to get an API key from `https://developers.noiz.ai/api-keys`. After the user provides the key, ask whether they want to persist it; if they agree, either write/update `NOIZ_API_KEY=...` in the project's `.env` file or run `bash skills/tts/scripts/tts.sh config --set-api-key YOUR_KEY` to store it.
- `ffmpeg` installed.

## Limitations

- The source video must have subtitles (or auto-generated subtitles) available on the platform for the source language.
- Very long videos may take a significant amount of time to translate and dub.
