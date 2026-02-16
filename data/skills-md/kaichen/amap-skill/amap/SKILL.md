---
name: amap
description: 通过脚本直连高德 Web Service API 完成地理编码、逆地理编码、IP 定位、天气、路径规划、距离测量和 POI 查询。用户要求“高德/AMap 查询”“路线规划”“地理编码”“POI 搜索”或需要用命令行脚本调用高德 API 时使用。
---

# AMap Skill

## Quick Start
1. Ensure `AMAP_MAPS_API_KEY` is set.
2. Run `bun scripts/amap.ts --help` in this skill directory.
3. Pick the matching command from `references/command-map.md`.

## Workflow
1. Validate user intent and select one command.
2. Prefer address commands for route planning when users provide plain addresses.
3. Keep output as raw AMap JSON without wrapping fields.
4. Treat any non-zero API business state as failure.

## Commands
- Full command mapping: `references/command-map.md`
- Ready-to-run examples: `references/examples.md`

## Notes
- This skill is script-first and does not run an MCP server.
- Only `AMAP_MAPS_API_KEY` is supported.
