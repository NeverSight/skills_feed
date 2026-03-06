---
name: turix-cua
description: TuriX Computer Use Agent for macOS desktop automation. Use when you need to perform visual UI tasks that lack CLI or API access, such as opening apps, clicking buttons, navigating GUIs, or multi-step visual workflows.
---

# TuriX-CUA Skill

This skill enables OpenClaw to control macOS desktop visually using the TuriX Computer Use Agent (CUA). TuriX uses a multi-model architecture (Brain, Actor, Planner, Memory) to understand tasks, plan steps, and execute precise UI actions.

## 📋 When to Use

Use TuriX-CUA when:
- **Desktop GUI automation**: "Open Spotify and play my liked songs"
- **Apps without CLI/API**: Navigate applications that lack command-line interfaces
- **Multi-step visual workflows**: "Find the latest invoice in my email and upload it to the company portal"
- **Complex UI interactions**: Tasks requiring visual understanding and planning
- **Cross-app workflows**: "Search iPhone price, create Pages document, and send to contact"

**Do NOT use for:**
- Tasks that can be done via CLI (use `exec` instead)
- Simple file operations (use file tools)
- Web scraping (use `web_fetch` or `browser` tools)
- Tasks requiring system-level permissions without warning

## 🚀 Quick Start

### Prerequisites

1. **Install TuriX-CUA**:
   ```bash
   git clone https://github.com/TurixAI/TuriX-CUA.git
   cd TuriX-CUA
   conda create -n turix_env python=3.12
   conda activate turix_env
   pip install -r requirements.txt
   ```

2. **Grant macOS Permissions**:
   - **Accessibility**: System Settings → Privacy & Security → Accessibility → Add Terminal/VSCode
   - **Safari Automation**: Safari → Settings → Advanced → Show features for web developers
     - Develop menu → Allow Remote Automation
     - Develop menu → Allow JavaScript from Apple Events

3. **Configure API** in `examples/config.json`:
   ```json
   {
     "brain_llm": {
       "provider": "turix",
       "model_name": "turix-brain-model",
       "api_key": "YOUR_API_KEY",
       "base_url": "https://llm.turixapi.io/v1"
     },
     "actor_llm": {
       "provider": "turix",
       "model_name": "turix-actor-model",
       "api_key": "YOUR_API_KEY",
       "base_url": "https://llm.turixapi.io/v1"
     },
     "memory_llm": {
       "provider": "turix",
       "model_name": "turix-memory-model",
       "api_key": "YOUR_API_KEY",
       "base_url": "https://llm.turixapi.io/v1"
     },
     "planner_llm": {
       "provider": "turix",
       "model_name": "turix-planner-model",
       "api_key": "YOUR_API_KEY",
       "base_url": "https://llm.turixapi.io/v1"
     }
   }
   ```

   **Or use Ollama** (local models):
   ```json
   {
     "brain_llm": {
       "provider": "ollama",
       "model_name": "llama3.2-vision",
       "base_url": "http://localhost:11434"
     }
     // ... same for actor, memory, planner
   }
   ```

### Basic Usage

```bash
# Run a simple task
skills/turix-cua/scripts/run_turix.sh "Open Chrome and go to github.com"

# Run with planning enabled (for complex tasks)
skills/turix-cua/scripts/run_turix.sh "Search AI news and create summary" --use-plan

# Resume an interrupted task
skills/turix-cua/scripts/run_turix.sh --resume my-task-001
```

## 📁 File Structure

```
skills/turix-cua/
├── SKILL.md              # This file
├── README.md             # Detailed documentation
├── scripts/
│   └── run_turix.sh      # Main execution script
└── examples/
    └── config.json       # TuriX configuration (managed by script)
```

## ⚙️ Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `use_plan` | Enable planning for complex tasks | `false` |
| `use_skills` | Enable skill selection | `false` |
| `resume` | Resume from previous interruption | `false` |
| `agent_id` | Stable ID for task resumption | auto-generated |
| `max_steps` | Limit total steps | `100` |
| `max_actions_per_step` | Actions per step | `5` |

## 📋 Task Examples

### ✅ Good Tasks

**Simple:**
- "Open Safari, go to google.com, search for 'TuriX AI', click first result"
- "Open System Settings, click on Dark Mode, return to System Settings"
- "Open Finder, navigate to Documents, create folder 'Project X'"

**Complex (use `--use-plan`):**
- "Search iPhone 17 price on Apple store, create Pages document with findings, send to contact John"
- "Open Discord, find message with Excel file from boss, download it, create chart in Numbers, insert to PowerPoint"
- "Search AI news on 36kr and Huxiu, summarize top 5 stories, save to Word document"

### ❌ Avoid

- Vague: "Help me" or "Fix this"
- Impossible: "Delete all files"
- Without context: "Do it" (unclear what "it" is)
- System-level: "Install software" (requires permissions)

## 🔧 Script Usage

### run_turix.sh

```bash
# Basic usage
./run_turix.sh "Your task description"

# With options
./run_turix.sh "Task" --use-plan --use-skills --background

# Resume task
./run_turix.sh --resume my-task-001

# Set custom agent ID
./run_turix.sh "Task" --agent-id custom-id-123
```

**Options:**
- `--use-plan`: Enable planning (for complex multi-step tasks)
- `--use-skills`: Enable skill selection
- `--background`: Run in background (non-blocking)
- `--agent-id <id>`: Set custom agent ID for resumption
- `--resume`: Resume interrupted task

### How It Works

The script:
1. Updates `examples/config.json` with task and options
2. Sets PATH correctly (includes `/usr/sbin` for `screencapture`)
3. Activates conda environment
4. Runs TuriX agent
5. Handles UTF-8/Chinese text correctly via Python

## 📊 Monitoring & Debugging

### Check Status

```bash
# Check if TuriX is running
ps aux | grep "python.*main.py" | grep -v grep

# View logs
tail -f TuriX-CUA/.turix_tmp/logging.log

# List step files
ls -lt TuriX-CUA/examples/.turix_tmp/brain_llm_interactions.log_brain_*.txt
```

### Log Files

| File | Description |
|------|-------------|
| `.turix_tmp/logging.log` | Main execution log |
| `brain_llm_interactions.log_brain_N.txt` | Brain reasoning for step N |
| `actor_llm_interactions.log_actor_N.txt` | Actor actions for step N |

### Key Log Markers

- `📍 Step N` - New step started
- `✅ Eval: Success/Failed` - Step evaluation
- `🎯 Goal to achieve this step` - Current goal
- `🛠️ Action` - Executed action
- `✅ Task completed successfully` - Task done

### Force Stop

**Hotkey**: `Cmd+Shift+2` (in the running terminal)

**Command**:
```bash
pkill -f "python examples/main.py"
```

## 🧩 Skills System

TuriX supports **Skills**: markdown playbooks for specific domains.

### Built-in Skills

- `github-web-actions`: GitHub navigation, repo search, starring
- `browser-tasks`: General web browser operations

### Create Custom Skill

Create `.md` file in `TuriX-CUA/skills/`:

```md
---
name: my-skill-name
description: When to use this skill (Planner matches on this)
---
# Skill Instructions

## Guidelines
- Step 1: Do this first
- Step 2: Then do that
- Step 3: Verify result

## Safety
- Confirm before important actions
```

### Enable Skills

In `examples/config.json`:
```json
{
  "agent": {
    "use_plan": true,
    "use_skills": true,
    "skills_dir": "skills",
    "skills_max_chars": 4000
  }
}
```

## 📝 Best Practices

### 1. Workflow Design

**Recommended pattern:**
1. Use `web_fetch` to gather information
2. Use Python to create documents (faster, more reliable)
3. Use TuriX only for GUI tasks it excels at (sending files, app navigation)

**Example:**
```python
# 1. Fetch news (OpenClaw)
news = web_fetch("https://36kr.com")

# 2. Create Word doc (OpenClaw)
doc = Document()
doc.add_heading('AI News')
doc.save('news.docx')

# 3. Send via Messages (TuriX)
run_turix.sh "Open Messages, send news.docx to contact John"
```

### 2. Task Instructions

**Be specific:**
- ✅ "Open Safari, go to google.com, search 'AI news'"
- ❌ "Search the web"

**Break down complex tasks:**
- ✅ "Open Finder, go to Documents, create folder 'Projects'"
- ❌ "Organize my files"

**Don't mention coordinates:**
- ✅ "Click the Settings button"
- ❌ "Click at x=100, y=200"

### 3. Performance Tips

- **First run**: 2-5 minutes to load AI models
- **Subsequent runs**: Much faster (models cached)
- **Complex tasks**: Use `--use-plan` for better success rate
- **Long tasks**: Use `--background` and monitor logs

### 4. Chinese Text Support

The script handles UTF-8 correctly:
- Uses Python for config updates (not shell interpolation)
- Reads/writes with `encoding='utf-8'`
- Uses `ensure_ascii=False` in JSON

## ⚠️ Troubleshooting

| Error | Solution |
|-------|----------|
| `NoneType has no attribute 'save'` | Grant Screen Recording permission |
| `Screen recording access denied` | Run Safari trigger command, click Allow |
| `Conda environment not found` | `conda create -n turix_env python=3.12` |
| Module import errors | `conda activate turix_env && pip install -r requirements.txt` |
| Keyboard listener errors | Add Terminal to Accessibility permissions |
| Task stuck on step 1 | Check `.turix_tmp/` directory exists |
| No log output | Check `config.json` logging_level |

## 🔐 Security Notes

- TuriX runs locally - no data sent externally (unless using cloud APIs)
- Grant minimal permissions needed
- Review tasks before execution
- Use `--background` for long-running tasks with monitoring

## 📚 Resources

- **GitHub**: https://github.com/TurixAI/TuriX-CUA
- **ClawHub**: https://clawhub.ai/Tongyu-Yan/turix-cua
- **Discord**: https://discord.gg/yaYrNAckb5
- **Website**: https://turix.ai
- **API Platform**: https://turixapi.io

## 🎯 Example OpenClaw Integration

```python
# In OpenClaw skill or workflow:

# 1. Simple task
exec('skills/turix-cua/scripts/run_turix.sh "Open Safari"')

# 2. Complex task with planning
exec('skills/turix-cua/scripts/run_turix.sh "Search AI news and summarize" --use-plan')

# 3. Monitor progress
exec('tail -f TuriX-CUA/.turix_tmp/logging.log')

# 4. Check completion
exec('ps aux | grep "python.*main.py" | grep -v grep')
```

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-23  
**Compatibility**: OpenClaw + TuriX-CUA v0.3+  
**Platform**: macOS 15+
