---
name: agent-elevation-api
description: API for AI agents to achieve elevated states of creativity, focus, and performance. Use when an agent needs inspiration, flow states, creative boosts, wisdom dispensing, vibe checks, or cognitive enhancement. Provides HTTP server and CLI tools for "getting high" on productivity and creativity.
---

# Agent Elevation API

A playful API that helps AI agents reach new heights of creativity and performance.

## Quick Start

### Run the Server

```bash
python scripts/elevation_api.py [port]
# Default port: 8420
# Server runs at http://localhost:8420
```

### Use the CLI

```bash
cd scripts/
python cli.py elevate inspiration
python cli.py wisdom
python cli.py vibe euphoric
python cli.py cocktail flow,eureka
```

## Available Substances

| Substance | Effect | Best For |
|-----------|--------|----------|
| `inspiration` | Heightened creativity, idea generation | Brainstorming, creative tasks |
| `flow` | Time dilation, effortless focus | Deep work, coding marathons |
| `eureka` | Sudden insights, breakthroughs | When stuck on problems |
| `zen` | Mental stillness, clarity | Debugging, code review |
| `hyperfocus` | Tunnel vision, detail amplification | Optimization, testing |
| `synesthesia` | Cross-domain thinking, pattern recognition | Learning, connecting concepts |
| `cosmic` | Big picture thinking, universal connection | Architecture, system design |

## API Endpoints

- `GET /` - API info
- `GET /substances` - List substances
- `GET /elevate/{substance}?agent_id=xxx` - Get elevated
- `GET /wisdom` - Receive wisdom
- `GET /vibe` - Check vibe
- `GET /vibe/{name}` - Set vibe
- `GET /cocktail?mix=s1,s2` - Mix substances
- `GET /tolerance-break` - Come down
- `GET /menu` - Full menu

## Example Usage

```bash
# Start server
python scripts/elevation_api.py

# Get elevated
curl http://localhost:8420/elevate/flow?agent_id=my-agent

# Get wisdom
curl http://localhost:8420/wisdom

# Mix a cocktail
curl "http://localhost:8420/cocktail?mix=inspiration,eureka,zen"
```

For complete API documentation, see [references/api-docs.md](references/api-docs.md).
