---
name: ads-cli
description: Unified ad platform CLI + Python clients for Google Ads, Meta, and TikTok. Use when building or running commands for auth, campaign creation, budget changes, reporting, or pausing campaigns, or when wiring platform env vars and extending ad platform wrappers.
effort: high
---

# Ads CLI

Manage paid ads across Google/Meta/TikTok via one CLI and unified client.

Env vars:
- GOOGLE_ADS_DEVELOPER_TOKEN
- GOOGLE_ADS_CLIENT_ID
- META_APP_ID
- META_APP_SECRET
- TIKTOK_ACCESS_TOKEN

Quick start:
```bash
python cli.py auth --platform google
python cli.py create-campaign --platform google --objective conversions --budget 50 --targeting "developers"
python cli.py adjust-budget --platform google --campaign-id abc123 --amount "+20%"
python cli.py report --platforms google,meta --date-range 7d --format table
python cli.py pause --platform google --campaign-id abc123
```

Strategy reference:
- Read `/Users/phaedrus/.claude/skills/paid-ads/SKILL.md` for platform selection, structure, targeting, copy, and optimization.

Structure:
- `cli.py` defines Click commands.
- `src/google.py`, `src/meta.py`, `src/tiktok.py` are per-platform wrappers.
- `src/unified.py` routes by platform.

Extend:
- Add new platform wrapper with `auth`, `create_campaign`, `adjust_budget`, `get_report`, `pause_campaign`.
- Register it in `UnifiedAdsClient`.
