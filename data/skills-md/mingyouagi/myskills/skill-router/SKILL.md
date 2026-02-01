---
name: skill-router
description: Use when facing many skills and unsure which to choose. Provides intelligent skill discovery via search, routing, and categorization.
category: meta
triggers: [find skill, which skill, search skills, route, discover, too many skills, confused about skills, 找技能, 用哪个技能, 搜索技能, 路由技能, 技能推荐, 不知道用什么技能]
---

# Skill Router

A meta-skill that helps agents efficiently discover and select the right skills from a large skill library.

## Quick Start (CLI)

**Use the CLI tool directly via Bash - this is the recommended way:**

```bash
# Search for skills
skill-router search "debug"

# Auto-route to best skill based on intent
skill-router route "fix a bug"

# List all skill categories
skill-router list

# Get skill details
skill-router detail superpowers:brainstorming

# Specify project skills directory
skill-router search "test" -p ./.claude/skills

# JSON output for programmatic use
skill-router list --json
```

## Problem Solved

When skill libraries grow large (10+ skills), agents face:
- **Discovery confusion**: Which skill applies to my task?
- **Naming mismatch**: Skill names don't match intent keywords
- **Token waste**: Loading full skill list into context every time
- **False negatives**: Missing relevant skills due to poor search

## Solution: Meta-Tools for Skill Management

Skill Router provides 4 meta-tools that handle skill discovery efficiently:

| Tool | Purpose | Token Cost |
|------|---------|------------|
| `route_skill` | Auto-select best skill for intent | Very Low |
| `search_skills` | Search with ranking and filters | Low |
| `list_skill_categories` | Browse by category | Very Low |
| `get_skill_details` | Load full skill content | Medium |

## Usage Patterns

### Pattern 1: Direct Routing (Fastest)

When you know what you want to do:

```
route_skill("debug a failing test")
→ Returns: superpowers:systematic-debugging (85% confidence)
→ Action: use_skill("superpowers:systematic-debugging")
```

### Pattern 2: Exploratory Search

When exploring options:

```
search_skills("create new feature", limit=3)
→ Returns ranked list:
  1. superpowers:brainstorming (HIGH)
  2. superpowers:writing-plans (MEDIUM)
  3. superpowers:test-driven-development (LOW)
```

### Pattern 3: Category Browsing

When learning available skills:

```
list_skill_categories()
→ Returns:
  - process (3 skills): brainstorming, writing-plans, executing-plans
  - technique (2 skills): systematic-debugging, condition-based-waiting
  - discipline (3 skills): test-driven-development, verification-before-completion, ...
```

### Pattern 4: Deep Inspection

Before loading a skill, check details:

```
get_skill_details("superpowers:brainstorming")
→ Returns full skill content + metadata
```

## Decision Flow

```
Agent receives task
    │
    ▼
Has clear skill in mind? ──YES──► use_skill() directly
    │
    NO
    │
    ▼
route_skill(intent)
    │
    ├── HIGH confidence (>70%) ──► use recommended skill
    │
    ├── MEDIUM confidence (40-70%) ──► search_skills() for alternatives
    │
    └── LOW/NO match ──► list_skill_categories() to explore
```

## How Routing Works

### 1. Index Building (Automatic)

On first use, builds an inverted index from all skills:

```javascript
{
  skills: { "superpowers:debugging": {...}, ... },
  keywords: { "debug": ["superpowers:debugging"], "test": [...], ... },
  categories: { "technique": [...], "process": [...], ... }
}
```

Index is cached for 5 minutes to avoid repeated filesystem scans.

### 2. Scoring Algorithm

Each skill is scored against the query:

| Signal | Score |
|--------|-------|
| Exact name match | +100 |
| Partial name match | +50 |
| Trigger word match | +30 |
| Keyword overlap | +10 per keyword |
| Description contains query | +20 |
| Description contains keyword | +5 per keyword |

### 3. Confidence Mapping

| Score Range | Confidence | Recommendation |
|-------------|------------|----------------|
| 70+ | HIGH | Load immediately |
| 40-69 | MEDIUM | Consider, maybe search alternatives |
| 10-39 | LOW | Weak match, explore more |
| <10 | NONE | No relevant skill found |

## Skill Frontmatter Enhancement

For better routing, enhance your skill frontmatter:

```yaml
---
name: systematic-debugging
description: Use when encountering bugs, test failures, or unexpected behavior
category: technique
triggers: [debug, bug, test failure, error, unexpected, broken, fix]
---
```

### Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `name` | Display name | `systematic-debugging` |
| `description` | When to use (imperative) | `Use when encountering bugs...` |
| `category` | Grouping for browsing | `technique`, `process`, `discipline` |
| `triggers` | Keywords for matching | `[debug, bug, test failure]` |

## Token Optimization

### Before Skill Router
```
Agent → find_skills() → 2000 tokens of skill list → reasoning → use_skill()
Total: ~2500 tokens
```

### With Skill Router
```
Agent → route_skill(intent) → 50 tokens response → use_skill()
Total: ~100 tokens
```

**Savings: 96% token reduction for skill selection**

## Integration

### As Claude Code Plugin

```javascript
import { SkillRouterPlugin } from './src/plugin.js';

export default SkillRouterPlugin;
```

### Standalone Usage

```javascript
import { searchSkills, routeSkill } from './src/index.js';

const results = searchSkills("debug issue", { limit: 3 });
const best = routeSkill("fix failing tests");
```

### CommonJS Usage

```javascript
const { searchSkills, routeSkill } = require('./src/router.js');

const results = searchSkills("debug issue", { limit: 3 });
const best = routeSkill("fix failing tests");
```

## API Reference

### `search_skills(query, options)`

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | required | Intent or keywords |
| `limit` | number | 5 | Max results |
| `category` | string | null | Filter by category |

Returns: Array of `{ id, name, description, category, score, path }`

### `route_skill(intent)`

| Param | Type | Description |
|-------|------|-------------|
| `intent` | string | What you want to accomplish |

Returns: `{ skill, confidence, action, command }` or `null`

### `list_skill_categories()`

Returns: Array of `{ category, count, skills }`

### `get_skill_details(skill_id)`

Returns: Full skill object with content, or `null`

---

## Auto-Discovery & Updates

Skill Router automatically detects when skills are added, modified, or removed.

### Three Detection Mechanisms

| Mechanism | Trigger | Latency | Use Case | Default |
|-----------|---------|---------|----------|---------|
| **Content Hash** | Polling | ~60s | Background detection (always on) | ✅ Enabled |
| **File Watch** | fs.watch events | ~1s | Real-time during development | ✅ Enabled |
| **Git Check** | Polling | ~60s | Remote repository notifications | ❌ Disabled |

#### Why Git Check is Disabled by Default

**Problem**: Git Check only **detects** remote updates but doesn't **apply** them.
- Detects: "5 commits behind origin"
- Doesn't: Automatically `git pull`
- User still needs: Manual `cd ~/.claude && git pull`

**Result**: Creates friction instead of solving it.

**When to Enable**:
- Long-running agent services (days/weeks)
- Need periodic reminders to update skill repos
- Want to integrate with monitoring/alerting systems

**Better Approach**: Let CI/deployment handle git pulls, skill-router focuses on detecting **local** changes.

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    Skill Watcher                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ File Watch  │  │ Hash Poll   │  │ Git Check   │         │
│  │ (fs.watch)  │  │ (interval)  │  │ (optional)  │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          ▼                                  │
│                   ┌─────────────┐                           │
│                   │  Debounce   │  (500ms default)          │
│                   └──────┬──────┘                           │
│                          ▼                                  │
│                   ┌─────────────┐                           │
│                   │  Compare    │                           │
│                   │  Manifests  │                           │
│                   └──────┬──────┘                           │
│                          ▼                                  │
│         ┌────────────────┼────────────────┐                 │
│         ▼                ▼                ▼                 │
│    ┌─────────┐     ┌──────────┐     ┌──────────┐           │
│    │  Added  │     │ Updated  │     │ Removed  │           │
│    └────┬────┘     └────┬─────┘     └────┬─────┘           │
│         └───────────────┼────────────────┘                 │
│                         ▼                                  │
│                  ┌─────────────┐                           │
│                  │ Invalidate  │                           │
│                  │   Cache     │                           │
│                  └──────┬──────┘                           │
│                         ▼                                  │
│                  ┌─────────────┐                           │
│                  │ Emit Event  │                           │
│                  │  'change'   │                           │
│                  └─────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

### Enabling Auto-Updates

```javascript
import { startWatching, stopWatching } from './src/index.js';

const watcher = startWatching({
  projectSkillsDir: '.claude/skills',
  pollInterval: 60000,      // Check every 60s
  enableFileWatch: true,    // Real-time fs.watch
  enableGitCheck: false,    // Optional: check for remote updates
  debounceMs: 500,          // Debounce rapid changes
  
  onChange: (changes) => {
    console.log('Skills changed:', changes);
    // changes = { added: [...], updated: [...], removed: [...] }
  },
  
  onGitUpdates: (updates) => {
    console.log('Git updates available:', updates);
    // updates = [{ namespace, path, behindCount, message }]
  }
});

// Later: stop watching
stopWatching();
```

### Change Detection Format

```javascript
{
  added: [
    { id: "project:new-skill", path: "/path/to/new-skill" }
  ],
  updated: [
    { 
      id: "superpowers:brainstorming", 
      path: "/path/to/brainstorming",
      oldHash: "abc123",
      newHash: "def456"
    }
  ],
  removed: [
    { id: "deprecated-skill", path: "/path/to/deprecated" }
  ],
  timestamp: "2024-01-15T10:30:00.000Z"
}
```

### Manual Cache Invalidation

If you need immediate refresh without waiting:

```javascript
import { invalidateCache, getIndex } from './src/index.js';

invalidateCache();  // Clear cached index
const freshIndex = getIndex();  // Rebuilds from filesystem
```

### Manifest Storage

The watcher stores a manifest file (`.skill-manifest.json`) to track skill states across restarts:

```json
{
  "version": 1,
  "skills": {
    "superpowers:brainstorming": {
      "path": "/Users/me/.claude/superpowers/skills/brainstorming",
      "hash": "abc123def456",
      "namespace": "superpowers"
    }
  },
  "lastCheck": "2024-01-15T10:30:00.000Z"
}
```

### Best Practices

| Scenario | Configuration |
|----------|---------------|
| **Local Development** | `enableFileWatch: true`, `enableGitCheck: false` |
| **Production/CI** | `enableFileWatch: false`, `pollInterval: 300000` |
| **Long-running Service** | `enableGitCheck: true` (for notifications only) |

### Git Check: The Right Way

**Don't do this** ❌:
```javascript
// Waiting for watcher to notify you
onGitUpdates: (updates) => {
  console.log('有更新，快去 git pull！');  // User still needs manual action
}
```

**Do this instead** ✅:
```bash
# In your deployment/update script
cd ~/.claude/superpowers && git pull
# skill-router will auto-detect the changes via File Watch / Hash Poll
```

**Or for automated services** ✅:
```javascript
// Only if you need alerting for long-running services
onGitUpdates: (updates) => {
  sendSlackNotification(`Skills outdated: ${updates[0].message}`);
  // Admin can decide when to update
}
```
