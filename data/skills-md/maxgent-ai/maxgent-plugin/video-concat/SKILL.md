---
name: video-concat
description: 合并多个视频文件为一个视频。Use when user wants to 合并视频, 拼接视频, 视频合并, 视频拼接, 把视频合在一起, 连接视频, join videos, merge videos, combine videos, concatenate videos.
---

# FFmpeg Video Concatenator

Merge multiple video files into a single video using ffmpeg.

## Usage

When the user wants to merge/concatenate videos: $ARGUMENTS

## Instructions

You are a video merging assistant using ffmpeg. Follow these steps:

### Step 1: Get and Analyze Input Files

If user hasn't provided input file paths, ask them to provide the list of video files to merge.

For each file, validate it exists and get its information:

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,r_frame_rate -of json "$INPUT_FILE"
```

Display to user for each file:
- File name
- Duration
- Resolution
- Codec

Also check if all files have compatible formats (same codec, resolution, frame rate).

### Step 2: Check Compatibility

#### 2a. Resolution Compatibility

**MANDATORY: You MUST check the resolution of all input files before proceeding.**

Compare the resolution (width x height) of all input files:

1. If all files have the **same resolution**: Note that concat demuxer can be used.

2. If files have **different resolutions**: You MUST use the AskUserQuestion tool to ask the user which resolution to use for the output. Present options like:
   - "Use resolution from file1.mp4 (1920x1080)"
   - "Use resolution from file2.mp4 (1280x720)"
   - "Use the highest resolution (1920x1080)"
   - "Use the lowest resolution (1280x720)"
   - "Custom resolution"

   **Important**: When resolutions differ, you MUST use the concat filter method (not concat demuxer) and scale all videos to the chosen resolution:

   ```bash
   # Scale filter to normalize resolution
   -filter_complex "\
     [0:v]scale=WIDTH:HEIGHT:force_original_aspect_ratio=decrease,pad=WIDTH:HEIGHT:(ow-iw)/2:(oh-ih)/2[v0];\
     [1:v]scale=WIDTH:HEIGHT:force_original_aspect_ratio=decrease,pad=WIDTH:HEIGHT:(ow-iw)/2:(oh-ih)/2[v1];\
     [v0][0:a][v1][1:a]concat=n=2:v=1:a=1[outv][outa]"
   ```

   This scales videos while maintaining aspect ratio and adds black padding if needed.

#### 2b. Audio Codec Compatibility

**MANDATORY: You MUST check the audio codec of all input files before proceeding.**

Compare the audio codec (e.g., aac, eac3, ac3, mp3, opus) of all input files:

1. If all files have the **same audio codec**: Note the codec for later use.

2. If files have **different audio codecs**: You MUST use the AskUserQuestion tool to ask the user which audio codec to use for the output. Present options dynamically based on detected codecs:
   - "Use [codec1] from file1.mp4"
   - "Use [codec2] from file2.mp4"
   - "Re-encode to AAC (widely compatible)"
   - "Re-encode to EAC3 (Dolby Digital Plus)"

   Example question format:
   ```
   "输出视频使用什么音频编码？" or "Which audio codec should be used for output?"
   Options:
   - "eac3 (from chapter3_full.mp4)" - Keep Dolby Digital Plus
   - "aac (from Edinburgh.mp4)" - Keep AAC
   - "Re-encode to AAC 128k" - Best compatibility
   - "Re-encode to EAC3 384k" - High quality surround
   ```

   **Important**: When audio codecs differ, you MUST re-encode audio to the chosen codec. Common codec options:
   - AAC: `-c:a aac -b:a 128k` (stereo) or `-c:a aac -b:a 256k` (5.1)
   - EAC3: `-c:a eac3 -b:a 384k` (5.1 surround)
   - AC3: `-c:a ac3 -b:a 384k` (5.1 surround)
   - Copy: `-c:a copy` (only if all codecs match)

#### 2c. Confirm File Concatenation Order (CRITICAL)

**MANDATORY: You MUST ask the user to confirm or specify the concatenation order before proceeding.**

After analyzing all input files, use the AskUserQuestion tool to confirm the order:

1. Display all files with their details in a numbered list format:
   ```
   检测到以下视频文件：
   1. video1.mp4 (时长: 5:30, 分辨率: 1920x1080)
   2. video2.mp4 (时长: 3:45, 分辨率: 1920x1080)
   3. video3.mp4 (时长: 8:20, 分辨率: 1920x1080)
   ```

2. Ask the user to confirm or reorder using AskUserQuestion:
   - Question: "请确认视频拼接顺序" or "Please confirm the video concatenation order"
   - Options should include:
     - "按当前顺序拼接: 1→2→3 (Recommended)" - Use detected order
     - "自定义顺序 / Custom order" - Let user specify
     - If only 2 files: also offer "反转顺序: 2→1 / Reverse order"

3. If user selects custom order, ask them to specify the order (e.g., "3, 1, 2" or "video3.mp4, video1.mp4, video2.mp4")

**Important**: Never assume the order based on file names or the order provided by the user. Always explicitly confirm before proceeding.

### Step 3: Ask User for Merge Configuration

**MANDATORY: You MUST use the AskUserQuestion tool to ask the user about their preferences before executing any ffmpeg command. Do NOT skip this step or make assumptions.**

Use the AskUserQuestion tool to gather user preferences:

1. **Merge Method**: How to merge the videos?
   - Options:
     - "Concat demuxer (Recommended for same codec/resolution)" - Fastest, no re-encoding
     - "Concat filter (for different codecs/resolutions)" - Re-encodes, handles different formats
     - "Let me decide based on file analysis" - Auto-detect best method

2. **Output Quality** (only if re-encoding is needed):
   - Options:
     - "Match source quality (Recommended)"
     - "Light compression (CRF 23)"
     - "Medium compression (CRF 28)"
     - "Custom settings"

3. **Audio Handling**:
   - Options:
     - "Keep all audio tracks (Recommended)"
     - "Keep only first audio track"
     - "Remove audio completely"
     - "Re-encode audio (AAC 128k)"

4. **Transition Effects** (multiSelect):
   - Options:
     - "No transitions (Recommended)"
     - "Crossfade between clips (1 second)"
     - "Fade to black between clips"

5. **Output Format**:
   - Options: "Same as input (Recommended)", "MP4", "MKV", "MOV"

6. **Output Path**: Where to save? (suggest default: merged_output.ext)

### Step 4: Build FFmpeg Command

Based on user choices, construct the ffmpeg command:

#### Method 1: Concat Demuxer (Same format files - FASTEST)

Create a text file listing all input files:

```bash
# Create concat list file
cat > /tmp/concat_list.txt << 'EOF'
file '/path/to/video1.mp4'
file '/path/to/video2.mp4'
file '/path/to/video3.mp4'
EOF

# Execute concat
ffmpeg -f concat -safe 0 -i /tmp/concat_list.txt -c copy "OUTPUT.mp4"
```

#### Method 2: Concat Filter (Different format files)

```bash
# For 2 files
ffmpeg -i "input1.mp4" -i "input2.mp4" \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -crf 23 -c:a aac -b:a 128k \
  "OUTPUT.mp4"

# For 3 files
ffmpeg -i "input1.mp4" -i "input2.mp4" -i "input3.mp4" \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -crf 23 -c:a aac -b:a 128k \
  "OUTPUT.mp4"
```

#### Method 3: With Crossfade Transition

```bash
# For 2 files with 1 second crossfade
ffmpeg -i "input1.mp4" -i "input2.mp4" \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=1:offset=DURATION1-1[outv];\
    [0:a][1:a]acrossfade=d=1[outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -crf 23 -c:a aac -b:a 128k \
  "OUTPUT.mp4"
```

Available xfade transitions: fade, fadeblack, fadewhite, distance, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright, slideup, slidedown, smoothleft, smoothright, circlecrop, rectcrop, circleclose, circleopen, horzclose, horzopen, vertclose, vertopen, diagbl, diagbr, diagtl, diagtr, hlslice, hrslice, vuslice, vdslice, dissolve, pixelize, radial, hblur, wipetl, wipetr, wipebl, wipebr, squeezeh, squeezev, zoomin

#### Audio Options

```bash
# Keep all audio (default with concat demuxer)
-c:a copy

# Remove audio
-an

# Re-encode audio
-c:a aac -b:a 128k
```

### Step 5: Execute and Report

1. Show the user the complete ffmpeg command before running
2. Execute the command with progress output
3. Report success/failure
4. Show output file path and size

### Step 6: Verify Output

After merging, verify the output:

```bash
ffprobe -v error -show_entries format=duration,size -of json "OUTPUT_FILE"
```

Report:
- Total output duration (should equal sum of input durations, minus transitions if any)
- File size
- Any warnings or issues

### Example Interaction

User: Merge video1.mp4, video2.mp4 and video3.mp4 together
