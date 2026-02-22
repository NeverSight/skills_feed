---
name: manus
description: Delegate complex autonomous tasks to Manus AI - an AI agent for deep research, web browsing, code execution, report generation, and multi-step workflows.
allowed-tools: Bash, Read, Grep
---

# Manus AI Agent

**Manus** is an autonomous AI agent for long-running, complex tasks. Excels at deep research with parallel processing, web browsing, and comprehensive report generation.

### Quick Start
```bash
# Create a task
curl -X POST "https://api.manus.ai/v1/tasks" \
  -H "API_KEY: $MANUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your task description",
    "agentProfile": "manus-1.6"
  }'

# Poll for results (repeat until status != "running")
curl -s "https://api.manus.ai/v1/tasks/{task_id}" \
  -H "API_KEY: $MANUS_API_KEY"
```

---

## When to Use Manus

**Best for** (1-10+ minute autonomous work):
- **Research**: Market analysis, competitive intelligence, fact-checking, stock analysis
- **Content**: Reports, presentations, videos, websites, visualizations
- **Data**: PDF translation, multi-source synthesis, analysis with charts
- **Development**: Chrome extensions, POCs, prototypes, code review
- **Automation**: Form filling, Web scraping (JS-rendered), task scheduling

**Not for** (use Claude Code instead):
- Quick web searches or page fetches
- Code generation/editing
- Simple file I/O operations
- Git operations

---

## Core Workflow

```
Create Task → Get task_id → Poll Status → Extract Results → Done
```

1. **POST /v1/tasks** - Create and get `task_id`
2. **GET /v1/tasks/{task_id}** - Poll every 5-10 seconds until `status` ≠ `"running"`
3. **Extract** - Read `output[].content[].text` from completed response

---

## API Reference

### Base URL
```
https://api.manus.ai/v1
```

### Authentication
```bash
API_KEY: $MANUS_API_KEY (header)
```

### Create Task
```bash
POST /v1/tasks
Content-Type: application/json
API_KEY: $MANUS_API_KEY

{
  "prompt": "Your task description",
  "agentProfile": "manus-1.6",       # manus-1.6-lite | manus-1.6 | manus-1.6-max
  "taskMode": "agent",               # agent | chat | adaptive (optional)
  "projectId": "proj_xxx",           # optional - use project context
  "connectors": ["uuid1"],           # optional - gmail, calendar, notion
  "attachments": [],                  # optional - files, URLs, file_ids
  "hideInTaskList": false,            # optional - hide from task list
  "createShareableLink": false,       # optional - public accessibility
  "taskId": "existing_task_id",       # optional - continue multi-turn conversation
  "locale": "en-US",                  # optional - user locale (e.g. "en-US", "zh-CN")
  "interactiveMode": false            # optional - enable follow-up questions
}
```

**Response:**
```json
{
  "task_id": "TeBim6FDQf9peS52xHtAyh",
  "task_title": "Generated Title",
  "task_url": "https://manus.im/app/TeBim6FDQf9peS52xHtAyh",
  "share_url": "https://manus.im/share/xxx"
}
```

### Get Task (Poll for Results)
```bash
GET /v1/tasks/{task_id}
API_KEY: $MANUS_API_KEY
```

**Response:**
```json
{
  "id": "task_id",
  "status": "running",          # running | completed | failed | stopped
  "model": "manus-1.6-adaptive",
  "metadata": {
    "task_title": "Task Title",
    "task_url": "https://manus.im/app/xxx"
  },
  "output": [
    {
      "role": "assistant",
      "status": "completed",
      "content": [
        {"type": "output_text", "text": "The result text..."}
      ]
    }
  ],
  "credit_usage": 42
}
```

### List All Tasks
```bash
GET /v1/tasks
API_KEY: $MANUS_API_KEY
```

Returns array of all tasks with status, metadata, and credit usage.

### Delete Task
```bash
DELETE /v1/tasks/{task_id}
API_KEY: $MANUS_API_KEY
```

### Create Project
```bash
POST /v1/projects
API_KEY: $MANUS_API_KEY

{
  "name": "Project Name",
  "instruction": "Default instruction for all tasks in this project"
}
```

### List Projects
```bash
GET /v1/projects
API_KEY: $MANUS_API_KEY
```

### Upload File (for attachment)
```bash
POST /v1/files/upload
API_KEY: $MANUS_API_KEY
Content-Type: multipart/form-data

file: <binary file data>
```

Returns `file_id` for use in task attachments. Upload window: 3 minutes.

### Create Webhook
```bash
POST /v1/webhooks
API_KEY: $MANUS_API_KEY

{
  "url": "https://your-server.com/webhook"
}
```

**Webhook Events:**
- `task_created` - Task started
- `task_progress` - Task making progress (plan updates)
- `task_stopped` - Task completed or needs input (`stop_reason`: "finish" or "ask")

---

## Agent Profiles

| Profile | Best For | Speed |
|---------|----------|-------|
| `manus-1.6-lite` | Quick lookups, fact checks | Fast |
| `manus-1.6` | Most research tasks (balanced) | Medium |
| `manus-1.6-max` | Complex analysis, multi-source deep dives | Slow (~complex) |

---

## Integration Patterns

### Simple Task (Standard)
```bash
curl -X POST "https://api.manus.ai/v1/tasks" \
  -H "API_KEY: $MANUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analyze Bitcoin price trends this week",
    "agentProfile": "manus-1.6"
  }'
```

### Complex Research (Max Profile)
```bash
curl -X POST "https://api.manus.ai/v1/tasks" \
  -H "API_KEY: $MANUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Deep analysis of AI market 2024-2026: market size, top 10 players, M&A trends, funding landscape",
    "agentProfile": "manus-1.6-max",
    "locale": "en-US"
  }'
```

### With Attachments (URL + Base64 + File ID)
```bash
curl -X POST "https://api.manus.ai/v1/tasks" \
  -H "API_KEY: $MANUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analyze this financial report and create a summary",
    "attachments": [
      {"type": "url", "url": "https://example.com/report.pdf"},
      {"type": "file_id", "file_id": "file_xxx"},
      {"type": "base64", "data": "base64....", "mimeType": "text/csv", "fileName": "data.csv"}
    ],
    "agentProfile": "manus-1.6"
  }'
```

### Multi-turn Conversation
```bash
curl -X POST "https://api.manus.ai/v1/tasks" \
  -H "API_KEY: $MANUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Based on your previous analysis, what are the investment implications?",
    "taskId": "abc123",
    "interactiveMode": true
  }'
```

### With Project Context
```bash
curl -X POST "https://api.manus.ai/v1/tasks" \
  -H "API_KEY: $MANUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analyze our Q1 competitor landscape",
    "projectId": "proj_xxx",
    "agentProfile": "manus-1.6"
  }'
```

### With Connectors (Gmail, Calendar, Notion)
```bash
curl -X POST "https://api.manus.ai/v1/tasks" \
  -H "API_KEY: $MANUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Check my calendar for the next 3 months and suggest the best time for a team offsite",
    "connectors": ["google-calendar-uuid"],
    "agentProfile": "manus-1.6"
  }'
```

---

## Playbook Templates

Pre-optimized prompts for common workflows:

| Template | Description |
|----------|-------------|
| `market-research` | Competitive analysis, market sizing |
| `slide-generator` | Professional presentations (PPT/PDF) |
| `video-generator` | AI-generated videos |
| `website-builder` | Full website generation |
| `resume-builder` | Professional resumes |
| `swot-analysis` | Business SWOT analysis |
| `chrome-extension` | Browser extension development |
| `trip-planner` | Travel itineraries |
| `influencer-finder` | YouTube creator discovery |
| `fact-checker` | Claim verification |
| `pdf-translator` | Document translation |
| `interior-design` | Room/space design |
| `fitness-coach` | Custom workout plans |
| `startup-poc` | Proof of concept prototypes |
| `profile-builder` | Research profiles on people/companies |
| `sentiment-analyzer` | Reddit sentiment analysis |
| `viral-content` | YouTube viral content analysis |
| `business-canvas` | Business model canvas |

---

## Prompt Tips for Better Results

**Good prompt structure:**
```
Task: [Clear objective]
Scope: [Research scope/timeframe]
Sources: [Prefer specific sources if known]
Output Format: [Structured report, bullet points, CSV, etc.]
```

**Example:**
```json
{
  "prompt": "Analyze competitors to ChatGPT in the enterprise AI space (2024-2026).
Scope: Market share, pricing, key features, customer segments.
Sources: G2, Gartner, official docs, recent news.
Output: Structured comparison table + strategic positioning analysis.",
  "agentProfile": "manus-1.6-max",
  "locale": "en-US"
}
```

---

## Best Practices

1. **Agent Profiles**
   - **lite** (fast, simple) → Quick lookups, fact checks
   - **1.6** (default) → Most research tasks, balanced
   - **1.6-max** → Complex analysis, multi-source deep dives

2. **Prompts**
   - Be specific: scope, sources, output format
   - Define timeframe if researching recent events
   - Request structured output (tables, bullet points, etc.)

3. **Polling**
   - Poll every 5-10 seconds for results
   - Most tasks complete in 1-5 minutes
   - Complex research may take 10+ minutes

4. **Projects** - Organize related tasks with shared instructions (e.g., "Always cite sources")

5. **Webhooks** - Monitor task events asynchronously instead of polling (production recommended)

6. **Attachments** - Include PDFs, images, URLs as research context. File uploads have 3-minute window.

7. **Locale** - Set `locale: "zh-CN"` for Chinese output, `"en-US"` for English, etc.

8. **Cost** - Monitor `credit_usage` per task. Budget accordingly.

---

## Polling Loop (Python Example)

```python
import requests
import time
import json

API_KEY = "your-manus-api-key"
BASE_URL = "https://api.manus.ai/v1"

# 1. Create task
response = requests.post(
    f"{BASE_URL}/tasks",
    headers={"API_KEY": API_KEY, "Content-Type": "application/json"},
    json={
        "prompt": "Your task description",
        "agentProfile": "manus-1.6"
    }
)
task_id = response.json()["task_id"]
print(f"Task created: {task_id}")

# 2. Poll for completion
max_retries = 120  # 10 minutes with 5s interval
retry = 0

while retry < max_retries:
    result = requests.get(
        f"{BASE_URL}/tasks/{task_id}",
        headers={"API_KEY": API_KEY}
    ).json()

    status = result.get("status")
    print(f"Status: {status}")

    if status == "completed":
        # 3. Extract results
        outputs = result.get("output", [])
        for output in outputs:
            if output.get("role") == "assistant":
                for content in output.get("content", []):
                    if content.get("type") == "output_text":
                        print("\n=== RESULT ===")
                        print(content["text"])
        break
    elif status in ["failed", "stopped"]:
        print(f"Task {status}")
        break

    time.sleep(5)
    retry += 1

if retry == max_retries:
    print("Timeout: Task took too long")
```

---

## Routing Logic

**Use Claude Code (free, instant) for:**
- Code generation, editing, refactoring
- File operations (read/write/search)
- Git operations, GitHub PRs
- Web search, simple page fetching
- Memory persistence

**Use Manus (costs credits) for:**
- Browser automation (JS-rendered sites)
- Form filling, login-required scraping
- PDF/slide/video generation
- OAuth integrations (Gmail, Calendar)
- Multi-hour autonomous research
- Real purchases/bookings

---

## Webhook Server Example

Simple Python webhook receiver:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    event = request.json
    event_type = event.get('event_type')

    if event_type == 'task_created':
        print(f"✅ Task started: {event['task_detail']['task_id']}")

    elif event_type == 'task_progress':
        print(f"⏳ Progress: {event['progress_detail']['message']}")

    elif event_type == 'task_stopped':
        detail = event['task_detail']
        if detail['stop_reason'] == 'finish':
            print(f"✓ Completed: {detail['message']}")
            for att in detail.get('attachments', []):
                print(f"  📎 {att['file_name']} ({att['size_bytes']} bytes)")
                print(f"     URL: {att['url']}")
        else:
            print(f"❓ Needs input: {detail['message']}")

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=8080)
```

**Register webhook:**
```bash
curl -X POST "https://api.manus.ai/v1/webhooks" \
  -H "API_KEY: $MANUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook"
  }'
```

---

## Error Codes & Solutions

| Code | Message | Fix |
|------|---------|-----|
| 8 | Credit limit exceeded | Add credits at [manus.im](https://manus.im) |
| 401 | Unauthorized | Check API_KEY in header |
| 400 | Bad request | Validate JSON payload, check agentProfile |
| 404 | Task not found | Verify task_id is correct |
| 429 | Rate limited | Wait before retrying |
| 500 | Server error | Retry after a few seconds |

---

## Resources

- **API Docs**: https://open.manus.ai/docs
- **Playbook Gallery**: https://manus.im/playbook
- **API Settings**: https://manus.im/app?show_settings=integrations&app_name=api
- **Webhook Setup**: https://manus.im/app?show_settings=integrations
- **Dashboard**: https://manus.im/app
