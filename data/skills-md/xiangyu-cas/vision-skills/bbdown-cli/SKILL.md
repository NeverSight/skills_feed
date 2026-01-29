---
name: bbdown-cli
description: Install and use the BBDown CLI on Linux/macOS for Bilibili downloads, including login/cookies/access_token, downloading by URL, preferring 720p when available, and writing output under a local data/ directory.
---

# BBDown CLI

## Quick start (data/ output, prefer 720p)

- Prefer running from the repo root so `data/` exists.
- List available streams and the exact 720p label:
  - `BBDown --only-show-info <url>`
- Download to `data/` with 720p preference (use the label you saw above):
  - `BBDown --work-dir data -q "<720p label>" <url>`
- If you are unsure about labels, use interactive selection:
  - `BBDown --work-dir data -ia <url>`

## Install or update (Linux/macOS)

- Install via .NET global tool:
  - `dotnet tool install --global BBDown`
- Update:
  - `dotnet tool update --global BBDown`
- Alternative: download a release binary and add it to PATH.

## Dependencies

- Install `ffmpeg` or `mp4box` for muxing.
- For Dolby Vision muxing, use `ffmpeg` 5.0+ or a recent `mp4box`.
- Optional: install `aria2c` if you plan to use `-aria2`.

## Auth and cookies

- Web QR login:
  - `BBDown login`
- TV QR login:
  - `BBDown logintv`
- Use a web cookie string when needed:
  - `BBDown -c "SESSDATA=..." <url>`
- Use TV/APP access token:
  - `BBDown -tv -token "..." <url>`

## Common download workflow

- Basic download:
  - `BBDown --work-dir data <url>`
- Prefer 720p and hide extra streams for cleaner output:
  - `BBDown --work-dir data -q "<720p label>" -hs <url>`
- For multi-part videos, select pages:
  - `BBDown --work-dir data -p 1,3,5 <url>`

## Troubleshooting

- If muxing fails, verify `ffmpeg`/`mp4box` availability or pass explicit paths:
  - `BBDown --ffmpeg-path <path> --work-dir data <url>`
- If member-only content fails, retry with `-c` cookie (web) or `-token` (TV/APP).
