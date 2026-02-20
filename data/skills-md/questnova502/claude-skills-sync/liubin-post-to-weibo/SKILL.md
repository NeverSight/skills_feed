---
name: liubin-post-to-weibo
description: Post content to Weibo (微博). Supports text posts with images. Uses real Chrome with CDP to bypass anti-automation.
---

# Post to Weibo (发微博)

Post content and images to Weibo using real Chrome browser (bypasses anti-bot detection).

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/weibo-browser.ts` | Regular posts (text + images) |
| `scripts/copy-to-clipboard.ts` | Copy content to clipboard |
| `scripts/paste-from-clipboard.ts` | Send real paste keystroke |

## Prerequisites

- Google Chrome or Chromium installed
- `bun` installed (for running scripts)
- First run: log in to Weibo in the opened browser window

---

## Regular Posts

Text + up to 9 images.

```bash
# Preview mode (doesn't post)
npx -y bun ${SKILL_DIR}/scripts/weibo-browser.ts "Hello from Claude!"

# With images
npx -y bun ${SKILL_DIR}/scripts/weibo-browser.ts "Check this out!" --image ./photo.png

# Multiple images (max 9)
npx -y bun ${SKILL_DIR}/scripts/weibo-browser.ts "Photos" --image a.png --image b.png --image c.png

# Actually post
npx -y bun ${SKILL_DIR}/scripts/weibo-browser.ts "发布微博!" --image ./photo.png --submit
```

> **Note**: `${SKILL_DIR}` represents this skill's installation directory. Agent replaces with actual path at runtime.

**Parameters**:
| Parameter | Description |
|-----------|-------------|
| `<text>` | Post content (positional argument) |
| `--image <path>` | Image file path (can be repeated, max 9) |
| `--submit` | Actually post (default: preview only) |
| `--profile <dir>` | Custom Chrome profile directory |

---

## Notes

- First run requires manual login (session is saved)
- Always preview before using `--submit`
- Browser closes automatically after operation
- Supports macOS, Linux, and Windows
- Weibo has a 2000 character limit for regular posts

## Extension Support

Custom configurations via EXTEND.md.

**Check paths** (priority order):
1. `.liubin-skills/liubin-post-to-weibo/EXTEND.md` (project)
2. `~/.liubin-skills/liubin-post-to-weibo/EXTEND.md` (user)

If found, load before workflow. Extension content overrides defaults.
