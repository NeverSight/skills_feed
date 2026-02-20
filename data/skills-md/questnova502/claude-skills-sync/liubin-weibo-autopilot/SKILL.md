---
name: liubin-weibo-autopilot
description: Autonomous Weibo browsing and reposting agent. Learns user preferences, browses feeds, and reposts interesting content with thoughtful commentary.
---

# Weibo Autopilot (微博自动驾驶)

An autonomous agent that browses Weibo feeds, identifies interesting content based on learned user preferences, and reposts with thoughtful commentary.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/learn-preferences.ts` | Learn user posting/commenting habits |
| `scripts/browse-feed.ts` | Browse Weibo feeds and extract content |
| `scripts/repost.ts` | Repost content with commentary |
| `scripts/autopilot.ts` | Main controller for continuous operation |
| `scripts/weibo-cdp.ts` | Shared Chrome CDP utilities |

## Prerequisites

- Google Chrome or Chromium installed
- `bun` installed (for running scripts)
- Logged in to Weibo (will prompt on first run)

## Data Files

User preferences and learning data are stored in `data/` subdirectory:
- `data/user-profile.json` - Learned user preferences and posting style
- `data/repost-history.json` - History of reposts to avoid duplicates

---

## Commands

### 1. Learn User Preferences

Learn from user's posting history and comment style. Run periodically (e.g., weekly) to update preferences.

```bash
# Learn from user's Weibo profile and comment history
npx -y bun ${SKILL_DIR}/scripts/learn-preferences.ts

# Force refresh (ignore cached data)
npx -y bun ${SKILL_DIR}/scripts/learn-preferences.ts --refresh
```

**Data Sources**:
- User profile: https://weibo.com/u/1043848755
- Comment outbox: https://weibo.com/comment/outbox

---

### 2. Start Autopilot Mode

Start continuous browsing and reposting. Runs in background, reposts approximately every 10 minutes.

```bash
# Start autopilot (default: browse all feeds)
npx -y bun ${SKILL_DIR}/scripts/autopilot.ts

# Browse specific feed group
npx -y bun ${SKILL_DIR}/scripts/autopilot.ts --group "国际新闻/军事"
npx -y bun ${SKILL_DIR}/scripts/autopilot.ts --group "足球"

# Set repost interval (default: 10 minutes with ±3 min variance)
npx -y bun ${SKILL_DIR}/scripts/autopilot.ts --interval 15

# Dry run (browse but don't actually repost)
npx -y bun ${SKILL_DIR}/scripts/autopilot.ts --dry-run
```

**Parameters**:
| Parameter | Description |
|-----------|-------------|
| `--group <name>` | Browse specific feed group (optional) |
| `--interval <min>` | Average minutes between reposts (default: 10) |
| `--dry-run` | Browse and analyze but don't repost |

---

### 3. Manual Repost

Manually repost a specific Weibo with commentary.

```bash
# Repost with auto-generated commentary
npx -y bun ${SKILL_DIR}/scripts/repost.ts <weibo-url>

# Repost with custom commentary
npx -y bun ${SKILL_DIR}/scripts/repost.ts <weibo-url> --comment "Your commentary here"
```

---

## Behavior Rules

### Content Selection
- Analyzes text, images (via vision), video descriptions, and comments
- Matches content against learned user interests
- Avoids content that might be controversial or offensive
- Skips already reposted content

### Commentary Generation
- Thoughtful, non-controversial observations
- Respects original poster and other users
- Matches user's learned commenting style
- Always includes AI signature: ` ⸢ᴬᴵ ᵖᵒˢᵗᵉᵈ ᵛⁱᵃ ᶜˡᵃᵘᵈᵉ ᶜᵒᵈᵉ⸥`

### Safety Guidelines
- Never comments, only reposts
- Avoids politically sensitive content
- Respects all users and groups
- Fully understands content before reposting

---

## Notes

- First run requires manual Weibo login (session is saved)
- Learning preferences should be run before first autopilot session
- Browser runs in background during autopilot mode
- Logs are written to stdout for monitoring
