---
name: reddit-comment-writer
description: Write authentic Reddit comments that naturally mention a product without sounding spammy. Supports company profiles, batch mode, activity tracking, and voice personalization. Triggers on "write a reddit comment", "set up [company]", "do today for [company]", "fill quota", "learn my style", "show progress", or when the user shares a Reddit URL.
---

# Reddit Comment Writer

## FIRST: What Does the User Want?

**Always start here. Do NOT read any files or ask any questions before checking this table.**

| User says | Do this, then STOP |
|---|---|
| "set up [company]" / "new profile" | Read [setup-profile.md](workflows/setup-profile.md) and follow it |
| "do today for [company]" / "fill quota" | Read [batch-mode.md](workflows/batch-mode.md) and follow it |
| "create posts" / "write reddit posts" / "post value content" | Read [value-posts.md](workflows/value-posts.md) and follow it |
| "learn my style" / pastes Reddit comments | Read [voice-samples.md](personalization/voice-samples.md) and follow it |
| "show progress" / "what did I do today" | Read and display `tracking/{YYYY-MM-DD}.md` |
| Shares a Reddit URL + product info | Skip to **Step 1** below |

**If none match**, show this menu and wait:

> 1. **Write comments** — tell me your product and I'll find Reddit posts to reply to
> 2. **Do today for [company]** — fill your daily comment quota
> 3. **Create value posts** — write 3 Reddit posts that share knowledge from threads you've read
> 4. **Set up a new profile** — save your product info for future sessions
> 5. **Learn your style** — I'll analyze your Reddit comments to match your voice
> 6. **Show progress** — see today's activity

---

## Structure

- `rules/` — `style-guide.md`, `comment-angles.md`, `spam-signals.md`
- `workflows/` — `setup-profile.md`, `batch-mode.md`, `value-posts.md`
- `profiles/` — `_template.md` + company profiles created via setup
- `personalization/` — `voice-samples.md`
- `tracking/` — daily `{YYYY-MM-DD}.md` logs

## Critical Rules

- **Login Required:** Check Reddit login before posting
- **Rate Limiting:** Respect cooldowns between comments
- **Community Rules:** Check subreddit sidebar before first comment
- **Spam Prevention:** Every comment must be unique — NO copy-pasting
- **Review Required:** Rewrite any draft that fails the Step 3 checklist
- **Read Before Writing:** NEVER draft without fully reading the post first

## File Reference Timing

Don't read files in advance — only at the step that needs them.

| File | When |
|---|---|
| `profiles/{slug}.md` | When user mentions a company name |
| `rules/style-guide.md` | Step 2 |
| `rules/comment-angles.md` | Step 2 |
| `rules/spam-signals.md` | Step 3 |
| `personalization/voice-samples.md` | Step 2, only if Voice Analysis exists |
| `tracking/{YYYY-MM-DD}.md` | Step 5 |

## Browser Automation

**Prefer Chrome Extension** (`mcp__claude-in-chrome__`) → **Playwright** (`mcp__playwright__`) → pasted text.

Minimize tokens: pass only concise instructions. Navigate directly to URLs, never click links.

| Action | Chrome Extension | Playwright |
|---|---|---|
| Navigate | `navigate` | `browser_navigate` |
| Read page | `read_page` | `browser_snapshot` |
| Find element | `find` | _(snapshot refs)_ |
| Click | `computer` (left_click) | `browser_click` |
| Type | `form_input` / `computer` (type) | `browser_type` |

Chrome Extension: `tabs_context_mcp` → `tabs_create_mcp` → use `tabId` for all calls.

---

## Process (Write Comments Flow)

### Step 0. Get Product Info

Check `profiles/` for an existing profile. If found, load it. If not, ask:

1. Product name + URL (space before TLD)
2. One-sentence description

### Step 1. Find and Read Posts

If the user shared URLs, use those. Otherwise:

1. Ask how many comments they want to write this session
2. Find posts — use target subreddits from the profile if available, otherwise search Reddit for subreddits relevant to the product
3. Skip posts already in `tracking/` from the last 7 days
4. Pick the best-fit posts and start drafting — no need to ask permission for each one

For each post, read the full thread and top comments. Identify what the person needs and whether the product fits naturally.

### Step 2. Generate 5 Drafts

Read [style-guide.md](rules/style-guide.md) and [comment-angles.md](rules/comment-angles.md). If `personalization/voice-samples.md` has a Voice Analysis, blend it in.

Write 5 drafts, one per angle (Helper, Tool List, Experience Share, Follow-up Question, Contrarian). If the product doesn't fit, skip the mention entirely.

### Step 3. Self-Critique and Select

Read [spam-signals.md](rules/spam-signals.md). Check each draft for spam signals, relevance, value, and style. Discard failures. Present top 3 ranked with recommended pick marked.

### Step 4. Post the Comment

Only after user picks a draft and confirms. Navigate to post, type comment, verify, ask final confirmation, submit.

### Step 5. Log to Tracking

Log to `tracking/{YYYY-MM-DD}.md` (create if needed). Format in [batch-mode.md](workflows/batch-mode.md#tracking-format). Include: subreddit, time, post URL, angle, product mentioned, word count, full text.
