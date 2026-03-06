---
name: daily-news-caster
description: Fetches the latest news using news-aggregator-skill, formats it into a podcast script in Markdown format, and uses the tts skill to generate a podcast audio file. Use when the user asks to get the latest news and read it out as a podcast.
---

# Daily News Caster Skill

This skill allows the agent to fetch real-time news, organize it into a conversational podcast script, and generate an audio file reading the script out loud.

## Workflow Instructions

When the user asks to get the latest news and make a podcast out of it, follow these steps strictly:

### Step 1: Ensure Skills are Installed
If the `news-aggregator-skill` and `tts` skills are not already installed in the workspace, run the following commands to install them:
```bash
npx skills add https://github.com/cclank/news-aggregator-skill --skill news-aggregator-skill -y
npx skills add https://github.com/noizai/skills --skill tts -y
```

### Step 2: Fetch the Latest News
Find the `fetch_news.py` script from the `news-aggregator-skill` (usually located in `.cursor/skills/news-aggregator-skill/scripts/fetch_news.py` or `skills/news-aggregator-skill/scripts/fetch_news.py`).

Run the script to fetch real-time news. You can specify a source (e.g., `hackernews`, `github`, `all`) or keywords based on the user's request.
Example command:
```bash
python3 path/to/fetch_news.py --source all --limit 10 --deep
```

### Step 3: Draft the Podcast Script (Internal Step)
Read the fetched news data and rewrite the information into a **Markdown podcast script**. 
**Crucially, prioritize a dual-host (two-person) conversational format** (e.g., Host A and Host B) in a dynamic **Q&A style**.
The script should be:
- **Dual-Host Conversational yet concise:** Write an engaging back-and-forth between two hosts. **Host A should ask insightful, high-value questions** to guide the conversation, and **Host B should provide informative, concise answers**. It should feel like a smart, fast-paced Q&A dialogue.
- **Avoid fluff:** Do not include unnecessary fluff or overly long transitions. Keep it to the point (言简意赅) while retaining all critical information and facts.
- **Clearly Labeled Speakers:** Start each line or paragraph with the speaker's name (e.g., `Host A:` or `Host B:`).
- **Clear text for speech:** Avoid complex URLs, raw markdown links, or unpronounceable characters in the spoken text.

Save this script to a local file named `podcast_script.md`. **Do NOT output the full markdown script to the user yet.**

**Example `podcast_script.md` Content:**
```markdown
**Host A:** Welcome to today's news roundup. We have some exciting tech updates today. To start things off, there's a big update from [Company Name]. What are the core implications of their new release for everyday users?

**Host B:** The main takeaway is that... [Insert concise answer and summary of News Item 1]. This completely changes how we approach [Topic].

**Host A:** That's fascinating. But does this new approach raise any security concerns, especially given recent data breaches?

**Host B:** Exactly. Experts are pointing out that... [Insert analysis or context]. 

**Host A:** Moving on to the open-source world, what's trending on GitHub today that developers should pay attention to?

**Host B:** A standout project is... [Insert concise summary of News Item 2].

**Host A:** Great insights. That's all for today's quick update. Thanks for tuning in!
```

### Step 4: Generate the Podcast Audio Line-by-Line
To avoid sending the entire script to the API at once, you must generate the audio **sentence by sentence (一人一句地生成)** and then concatenate them.

Find the `tts.sh` script (usually located in `skills/tts/scripts/tts.sh` or `.cursor/skills/tts/scripts/tts.sh`).

**1. Generate Audio for Each Line**:
For each dialogue line in the script, run the `speak` command. Use the appropriate voice or reference audio for the respective host. **If the user provided reference audio files or URLs for the two roles**, use them via the `--ref-audio` flag (requires `noiz` backend).
```bash
# Example for Line 1 (Host A)
bash path/to/tts.sh speak -t "Welcome to today's news roundup..." --backend noiz --ref-audio path/to/host_A.wav -o line_01.wav

# Example for Line 2 (Host B)
bash path/to/tts.sh speak -t "The main takeaway is that..." --backend noiz --ref-audio path/to/host_B.wav -o line_02.wav
```

**2. Concatenate the Audio Files**:
Create a text file (e.g., `list.txt`) listing all the generated audio files in order:
```text
file 'line_01.wav'
file 'line_02.wav'
```
Then use `ffmpeg` to merge them into a single podcast audio file:
```bash
ffmpeg -f concat -safe 0 -i list.txt -c copy podcast_output.wav
```

### Step 5: Present the Final Result
After the full audio has been generated and merged, present the results to the user. You **MUST** provide both pieces of content:
- Output the fully drafted **Markdown podcast script** into the chat so the user can read it.
- Provide the path to the final `podcast_output.wav` file so they can listen to the audio.
- Briefly summarize the headlines that were included in the podcast.
