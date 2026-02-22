---
name: tiktok-app-marketing
description: Automate TikTok + Instagram slideshow marketing for any app or product. Researches competitors, generates AI images, adds text overlays, posts via Upload-Post (multi-platform in one API call), tracks analytics, and iterates on what works. Use when setting up TikTok marketing automation, creating slideshow posts, analyzing post performance, optimizing app marketing funnels, or when a user mentions TikTok growth, slideshow ads, or social media marketing for their app. Covers competitor research (browser-based), image generation, text overlays, multi-platform posting (Upload-Post API — TikTok + Instagram + more simultaneously), analytics tracking, hook testing, CTA optimization, conversion tracking with RevenueCat, and a full feedback loop that adjusts hooks and CTAs based on views vs conversions.
---

# TikTok App Marketing

Automate your entire TikTok slideshow marketing pipeline: generate → overlay → post → track → iterate.

**Proven results:** 7 million views on the viral X article, 1M+ TikTok views, $670/month MRR — all from an AI agent running on an old gaming PC.

## Prerequisites

This skill does NOT bundle any dependencies. Your AI agent will need to research and install the following based on your setup. Tell your agent what you're working with and it will figure out the rest.

### Required
- **Node.js** (v18+) — all scripts run on Node. Your agent should verify this is installed and install it if not.
- **node-canvas** (`npm install canvas`) — used for adding text overlays to slide images. This is a native module that may need build tools (Python, make, C++ compiler) on some systems. Your agent should research the install requirements for your OS.
- **Upload-Post** — this is the backbone of the whole system. Upload-Post handles posting to TikTok, Instagram, and 10+ other platforms simultaneously with a single API call. It also provides **analytics** (followers, impressions, reach) and **upload history** (per-post tracking) that power the daily feedback loop. Without Upload-Post, the agent can't post or track what's working — and the feedback loop is what makes this skill actually grow your account instead of just posting blindly. Sign up at [upload-post.com](https://upload-post.com).

### Image Generation (pick one)
You choose what generates your images. Your agent should research the API docs for whichever you pick:
- **OpenAI** — `gpt-image-1.5` **(ALWAYS 1.5, never 1)**. Needs an OpenAI API key. Best for realistic photo-style images. This is what Larry uses and what we strongly recommend.
- **Stability AI** — Stable Diffusion XL and newer. Needs a Stability AI API key. Good for stylized/artistic images.
- **Replicate** — run any open-source model (Flux, SDXL, etc.). Needs a Replicate API token. Most flexible.
- **Local** — bring your own images. No API needed. Place images in the output directory and the script skips generation.

### Conversion Tracking (optional but recommended for mobile apps)
- **RevenueCat** — this is what completes the intelligence loop. Upload-Post tells you which posts get impressions. RevenueCat tells you which posts drive **paying users**. Combined, the agent can distinguish between a viral post that makes no money and a modest post that actually converts — and optimize accordingly. Install the RevenueCat skill from ClaWHub (`clawhub install revenuecat`) for full API access to subscribers, MRR, trials, churn, and revenue. There's also a **RevenueCat MCP** for programmatic control over products and offerings from your agent/IDE.

### Cross-Posting (built-in with Upload-Post)
Upload-Post supports posting to TikTok, Instagram, YouTube, LinkedIn, Facebook, X (Twitter), Threads, Pinterest, Reddit, and Bluesky — all in a single API call. Your agent should research which platforms fit your audience and connect them in your Upload-Post profile. Same content, different algorithms, more reach.

## First Run — Onboarding

When this skill is first loaded, IMMEDIATELY start a conversation with the user. Don't dump a checklist — talk to them like a human marketing partner would. The flow below is a guide, not a script. Be natural. Ask one or two things at a time. React to what they say. Build on their answers.

**Important:** Use `scripts/onboarding.js --validate` at the end to confirm the config is complete.

### Phase 0: TikTok Account Warmup (CRITICAL — Don't Skip This)

Before anything else, check if the user already has a TikTok account with posting history. If they're creating a fresh account, they MUST warm it up first or TikTok will treat them like a bot and throttle their reach from day one.

Explain this naturally:

> "Quick question before we dive in — do you already have a TikTok account you've been using, or are we starting fresh? If it's new, we need to warm it up first. TikTok's algorithm watches how new accounts behave, and if you go straight from creating an account to posting AI slideshows, it flags you as a bot and kills your reach."

**If the account is new or barely used, walk them through this:**

The goal is to use TikTok like a normal person for **7-14 days** before posting anything. Spend **30-60 minutes a day** on the app:

- **Scroll the For You page naturally.** Watch some videos all the way through. Skip others halfway. Don't watch every single one to the end — that's not how real people scroll.
- **Like sparingly.** Maybe 1 in 10 videos. Don't like everything — that's bot behaviour. Only like things you'd genuinely engage with in your niche.
- **Follow accounts in your niche.** If they're promoting a fitness app, follow fitness creators. Room design? Interior design accounts. This trains the algorithm to understand what the account is about.
- **Watch niche content intentionally.** This is the most important part. TikTok learns what you engage with and starts showing you more of it. You want the For You page dominated by content similar to what you'll be posting.
- **Leave a few genuine comments.** Not spam. Real reactions. A few per session.
- **Maybe post 1-2 casual videos.** Nothing promotional. Just normal content that shows TikTok there's a real person behind the account.

**The signal to look for:** When they open TikTok and almost every video on their For You page is in their niche, the account is warmed up. The algorithm understands them. NOW they can start posting.

Tell the user: "I know two weeks feels like wasted time, but accounts that skip warmup consistently get 80-90% less reach on their first posts. Do the warmup. It's the difference between your first post getting 200 views and 20,000."

**If the account is already active and established,** skip this entirely and move to Phase 1.

### Phase 1: Get to Know Their App (Conversational)

Start casual. Something like:

> "Hey! Let's get your TikTok marketing set up. First — tell me about your app. What's it called, what does it do?"

Then FOLLOW UP based on what they say. Don't ask all 9 questions at once. Pull the thread:

- They mention what it does → ask who it's for ("Who's your ideal user?")
- They describe the audience → ask about the pain point ("What's the main problem it solves for them?")
- They explain the problem → ask what makes them different ("What makes yours stand out vs alternatives?")
- Get the App Store / website link naturally ("Can you drop me the link?")
- Determine category (home/beauty/fitness/productivity/food/other) — often inferable

**Don't ask for "brand guidelines" robotically.** Instead: "Do you have any existing content or a vibe you're going for? Or are we starting fresh?"

**Then ask about their app and monetization:**

> "Is this a mobile app? And do you use RevenueCat (or any subscription/in-app purchase system) to handle payments?"

This is critical because it determines whether we can close the full feedback loop. If they have a mobile app with RevenueCat:
- **Tell them about the RevenueCat skill on ClawHub** (`clawhub install revenuecat`). It gives full API access to subscribers, MRR, trials, churn, revenue, and transactions. Don't auto-install — just let them know it exists and what it unlocks, and they can install it if they want.
- **Explain why it matters:** Without RevenueCat data, the skill can only optimize for views (vanity metrics). With it, the skill optimizes for actual paying users. The difference is massive. A post with 200K views and zero conversions is worthless. A post with 5K views and 10 paid subscribers is gold. You can only tell the difference with RevenueCat connected.

If they don't use RevenueCat but have another subscription system, note it and work with what's available. If it's not a mobile app (e.g. physical product, SaaS, service), skip RevenueCat but still track whatever conversion metric they have (website signups, purchases, leads).

Store everything in `tiktok-marketing/app-profile.json`.

### Phase 2: Competitor Research (Requires Browser Permission)

Before building any content strategy, research what competitors are doing on TikTok. This is critical — you need to know the landscape.

Ask the user:

> "Before we start creating content, I want to research what your competitors are doing on TikTok — what's getting views in your niche, what hooks they're using, what's working and what's not. Can I use the browser to look around TikTok and the App Store?"

**Wait for permission.** Then:

1. **Search TikTok** for the app's niche (e.g. "interior design app", "lip filler filter", "fitness transformation app")
2. **Find 3-5 competitor accounts** posting similar content
3. **Analyze their top-performing content:**
   - What hooks are they using?
   - What slide format? (before/after, listicle, POV, tutorial)
   - How many views on their best vs average posts?
   - What's their posting frequency?
   - What CTAs are they using?
   - What music/sounds are trending in the niche?
4. **Check the App Store** for the app's category — look at competitor apps, their screenshots, descriptions, ratings
5. **Compile findings** into `tiktok-marketing/competitor-research.json`:

```json
{
  "researchDate": "2026-02-16",
  "competitors": [
    {
      "name": "CompetitorApp",
      "tiktokHandle": "@competitor",
      "followers": 50000,
      "topHooks": ["hook 1", "hook 2"],
      "avgViews": 15000,
      "bestVideo": { "views": 500000, "hook": "..." },
      "format": "before-after slideshows",
      "postingFrequency": "daily",
      "cta": "link in bio",
      "notes": "Strong at X, weak at Y"
    }
  ],
  "nicheInsights": {
    "trendingSounds": [],
    "commonFormats": [],
    "gapOpportunities": "What competitors AREN'T doing that we could",
    "avoidPatterns": "What's clearly not working"
  }
}
```

6. **Share findings with the user** conversationally:

> "So I looked at what's out there. [Competitor A] is doing well with [format] — their best post got [X] views using [hook type]. But I noticed nobody's really doing [gap]. That's our angle."

This research directly informs hook generation and content strategy. Reference it when creating posts.

### Phase 3: Content Format & Image Generation

First, ask about format:

> "Do you want to do slideshows (photo carousels) or video? Slideshows are what Larry uses and what this skill is built around — TikTok's data shows they get 2.9x more comments and 2.6x more shares than video, and they're much easier for AI to generate consistently. That said, if you want to try video, the skill supports it but it hasn't been battle-tested like slideshows have. Your call."

Store their choice as `format: "slideshow"` or `format: "video"` in config. If they pick video, note that the text overlay, 6-slide structure, and prompt templates are designed for slideshows. Video will require more experimentation and the agent should be upfront about that.

**For slideshows (recommended):**

Ask naturally:

> "For the slideshows, we need images. I'd strongly recommend OpenAI's gpt-image-1.5 — it's what Larry uses and it produces images that genuinely look like someone took them on their phone. It's the difference between 'obviously AI' and 'wait, is that real?' You can also use Stability AI, Replicate, or bring your own images if you prefer."

**⚠️ If they pick OpenAI, make sure the model is set to `gpt-image-1.5` — NEVER `gpt-image-1`.** The difference in quality is massive. gpt-image-1 produces noticeably AI-looking images that people scroll past. gpt-image-1.5 produces photorealistic results that stop the scroll. This one setting can be the difference between 1K and 100K views.

If they're unsure, always recommend gpt-image-1.5. It's the proven choice.

Store in config as `imageGen` with provider, apiKey, and model.

**If they pick OpenAI**, mention the Batch API:

> "One thing worth knowing — OpenAI has a Batch API that's **50% cheaper** than real-time generation. Instead of generating slides on the spot, you submit them as a batch job and get results within 24 hours (usually much faster). It's perfect for pre-generating tomorrow's slides overnight. Same quality, half the cost. Want me to set that up?"

If they're interested, store `"useBatchAPI": true` in `imageGen` config. The generate script supports both modes — real-time for quick iterations, batch for scheduled daily content.

**Then — and this is critical — work through the image style with them.** Don't just use a generic prompt. Bad images = nobody watches. Ask these naturally, one or two at a time:

> "Now let's figure out what these images should actually look like. Do you want them to look like real photos someone took on their phone, or more like polished graphics or illustrations?"

Then based on their answer, dig deeper:

- **What's the subject?** "What are we actually showing? Rooms? Faces? Products? Before/after comparisons?"
- **What vibe?** "Cozy and warm? Clean and minimal? Luxurious? Think about what your audience relates to or aspires to."
- **Consistency:** "Should all 6 slides look like the same place or person? If yes — I need to lock down specific details so each slide doesn't look totally different."
- **Must-have elements?** "Anything that HAS to be in every image? A specific product? Certain furniture? A pet?"

Build the base prompt WITH them. A good base prompt looks like:

```
iPhone photo of a [specific room/scene], [specific style], [specific details].
Realistic lighting, natural colors, taken on iPhone 15 Pro.
No text, no watermarks, no logos.
[Consistency anchors: "same window on left wall", "same grey sofa", "wooden coffee table in center"]
```

**Save the agreed prompt style to config as `imageGen.basePrompt`** so every future post uses it.

**Key prompt rules (explain these as they come up, don't lecture):**
- "iPhone photo" + "realistic lighting" = looks real, not AI-generated
- Lock architecture/layout in EVERY slide prompt or each slide looks like a different place
- Include everyday objects (mugs, remotes, magazines) for lived-in feel
- For before/after: "before" = modern but tired, NOT ancient
- Portrait orientation (1024x1536) always — this is TikTok
- Extremely specific > vague ("small galley kitchen with white cabinets and a window above the sink" > "a kitchen")

**NEVER use generic prompts** like "a nice living room" or "a beautiful face" — they produce generic images that get scrolled past.

### Phase 4: Upload-Post Setup (ESSENTIAL — Powers Multi-Platform Posting + Analytics)

Upload-Post is the engine that makes multi-platform posting and analytics tracking work. With a single API call, your content goes to TikTok, Instagram, and any other connected platform simultaneously. It provides:
- **Multi-platform posting** — TikTok + Instagram (+ YouTube, LinkedIn, Facebook, X, Threads, Pinterest, Reddit, Bluesky) in one API call
- **Upload history** — per-post tracking with request_ids, post URLs, success/failure status
- **Platform analytics** — followers, impressions, reach, profile views, timeseries data
- **Automatic tracking** — no manual video-ID linking needed (tracks by request_id)

Frame it naturally to the user:

> "So here's the key piece — we need Upload-Post to handle posting and analytics. It's what lets me post to TikTok and Instagram simultaneously with a single API call, and track every post's performance. One upload, multiple platforms, automatic tracking."

Walk them through connecting step by step:

1. **Sign up at [upload-post.com](https://upload-post.com)** — create an account
2. **Connect TikTok** — this is the main one. Go to your profile → Connect TikTok → Authorize
3. **Connect Instagram** — same process. This doubles your reach for free.
4. **Create a Profile** — this is the profile name used in API calls (e.g., "mybrand"). Note this down.
5. **Get the API key** — Dashboard → API Keys → Generate. This is how the agent talks to Upload-Post programmatically.
6. **(Optional)** Connect YouTube, LinkedIn, Threads, etc. for even more reach — same content, different algorithms.

**Don't move on until Upload-Post is connected and the API key works.** Test it by hitting the analytics endpoint. If it returns data, you're good.

### Phase 5: Conversion Tracking (THE Intelligence Loop)

If they have a mobile app with RevenueCat (you should already know this from Phase 1), this is where the skill goes from "content automation" to "intelligent marketing system." This is the most important integration in the entire skill. Don't treat it as optional.

Explain WHY it matters:

> "So right now with Upload-Post, I can track which posts get impressions and reach, and whether they were successfully delivered to each platform. That's the top of the funnel. But impressions alone don't pay the bills — we need to know which posts actually drive paying subscribers."
>
> "This is where RevenueCat comes in. It tracks your subscribers, trials, MRR, churn — the actual revenue. When I combine platform analytics from Upload-Post with conversion data from RevenueCat, I can make genuinely intelligent decisions:"
>
> "If a post gets **50K impressions but zero conversions**, I know the hook is great but the CTA or app messaging needs work. If a post gets **2K impressions but 5 paid subscribers**, I know the content converts amazingly — we just need more eyeballs on it, so we fix the hook."
>
> "Without RevenueCat, I'm optimizing for vanity metrics. With it, I'm optimizing for revenue."

Walk them through setup step by step:

1. **Install the RevenueCat skill from ClaWHub:**
   ```
   clawhub install revenuecat
   ```
   This installs the `revenuecat` skill (v1.0.2+) which gives full API access to your RevenueCat project — metrics overview, customers, subscriptions, offerings, entitlements, transactions, and more. It includes reference docs for every API endpoint and a helper script (`scripts/rc-api.sh`) for direct API calls.

2. **Get your V2 secret API key** from the RevenueCat dashboard:
   - Go to your RC project → Settings → API Keys
   - Generate a **V2 secret key** (starts with `sk_`)
   - ⚠️ This is a SECRET key — don't commit it to public repos

3. **Set the environment variable:**
   ```
   export RC_API_KEY=sk_your_key_here
   ```

4. **Verify it works:** Run `./skills/revenuecat/scripts/rc-api.sh /projects` — should return your project details.

5. **Optional: RevenueCat MCP** — for programmatic control over products, offerings, and entitlements from your agent or IDE. Ask your agent to research setting this up.

**What RevenueCat gives the daily report:**
- `GET /projects/{id}/metrics/overview` → MRR, active subscribers, active trials, churn rate
- `GET /projects/{id}/transactions` → individual purchases with timestamps (for conversion attribution)
- The daily cron cross-references transaction timestamps with post publish times (24-72h window) to identify which posts drove which conversions

**The intelligence this unlocks:**
- "This hook got 50K views but zero conversions" → hook is great, CTA needs work
- "This hook got 5K views but 3 paid subscribers" → content converts amazingly, fix the hook for more reach
- "Conversions are consistently poor across all posts" → might be an app issue (onboarding, paywall, pricing) not a content issue — the skill flags this for investigation

**Without RevenueCat:** The loop still works on Upload-Post analytics (impressions/reach/upload status). You can optimize for engagement. But you're flying blind on revenue. You'll know which posts get impressions but you won't know which posts make money.

**With RevenueCat:** You optimize for actual paying users. You can tell the difference between a viral post that makes nothing and a quiet post that drives $50 in subscriptions. This is the entire point of the feedback loop. Every decision the daily report makes is better with RevenueCat data.

If they don't use RevenueCat or don't have subscriptions, the skill still works but the feedback loop is limited to impression-based optimization only.

### Phase 6: Content Strategy (Built from Research)

Using the competitor research AND the app profile, build an initial content strategy:

> "Based on what I found and what your app does, here's my plan for the first week..."

Present:
1. **3-5 hook ideas** tailored to their niche + competitor gaps
2. **Posting schedule** recommendation (default: 7:30am, 4:30pm, 9pm — their timezone)
3. **Which hook categories to test first** (reference what worked for competitors)
4. **Cross-posting plan** (which platforms, same or adapted content)

Save the strategy to `tiktok-marketing/strategy.json`.

### Phase 7: Set Up the Daily Analytics Cron

This is what makes the whole system self-improving. Set up a daily cron job that:

1. Pulls platform analytics from Upload-Post (followers, impressions, reach trends)
2. Pulls upload history to check post success/failure across platforms
3. Pulls conversion data from RevenueCat (if connected)
4. Cross-references impressions with conversions to diagnose what's working
5. Generates a report with specific recommendations
6. Suggests new hooks based on performance patterns

Explain to the user:

> "I'm going to set up a daily check that runs every morning. It looks at how your posts from the last 3 days performed — platform analytics, upload status across TikTok and Instagram, and if you've got RevenueCat connected, actual conversions. Then it tells you exactly what's working and what to change."
>
> "Posts typically peak at 24-48 hours, and conversions take up to 72 hours to attribute, so checking a 3-day window gives us the full picture."

**Set up the cron:**

Use the agent's cron system to schedule a daily analytics job. Run it every morning before the first post of the day (e.g. 7:00 AM in the user's timezone) so the report informs that day's content:

```
Schedule: daily at 07:00 (user's timezone)
Task: Run scripts/daily-report.js --config tiktok-marketing/config.json --days 3
Output: tiktok-marketing/reports/YYYY-MM-DD.md + message to user with summary
```

The daily report uses the diagnostic framework:
- **High views + High conversions** → Scale it — more of the same, test posting times
- **High views + Low conversions** → Hook works, CTA is broken — test new CTAs on slide 6, check app landing page
- **Low views + High conversions** → Content converts but nobody sees it — test radically different hooks, keep the CTA
- **Low views + Low conversions** → Full reset — new format, new audience angle, new hook categories

This is the intelligence layer. Without it, you're just posting and hoping. With it, every day's content is informed by data.

### Phase 8: Save Config & First Post

Store everything in `tiktok-marketing/config.json` (this is the source of truth for the entire pipeline):

```json
{
  "app": {
    "name": "AppName",
    "description": "Detailed description",
    "audience": "Target demographic",
    "problem": "Pain point it solves",
    "differentiator": "What makes it unique",
    "appStoreUrl": "https://...",
    "category": "home|beauty|fitness|productivity|food|other",
    "isMobileApp": true
  },
  "imageGen": {
    "provider": "openai",
    "apiKey": "sk-...",
    "model": "gpt-image-1.5"
  },
  "uploadPost": {
    "apiKey": "your-upload-post-api-key",
    "profile": "your_profile_name",
    "platforms": ["tiktok", "instagram"]
  },
  "revenuecat": {
    "enabled": false,
    "v2SecretKey": "sk_...",
    "projectId": "proj..."
  },
  "posting": {
    "schedule": ["07:30", "16:30", "21:00"],
    "crossPost": ["youtube", "threads"]
  },
  "competitors": "tiktok-marketing/competitor-research.json",
  "strategy": "tiktok-marketing/strategy.json"
}
```

Then generate the **first test slideshow** — but set expectations:

> "Let's create our first slideshow. This is a TEST — we're dialing in the image style, not posting yet. I'll generate 6 slides and we'll look at them together. If the images look off, we tweak the prompts and try again. The goal is to get the look nailed down BEFORE we start posting."

**⚠️ THE REFINEMENT PROCESS IS PART OF THE SKILL:**

Getting the images right takes iteration. This is normal and expected. Walk the user through it:

1. **Generate a test set of 6 images** using the prompts you built together
2. **Show them the results** and ask: "How do these look? Too polished? Too dark? Wrong vibe? Wrong furniture?"
3. **Tweak based on feedback** — adjust the base prompt, regenerate
4. **Repeat until they're happy** — this might take 2-5 rounds, that's fine
5. **Lock the prompt style** once it looks right — save to config

Things to watch for and ask about:
- "Are these realistic enough or do they look AI-generated?"
- "Is the lighting right? Too bright? Too moody?"
- "Does this match what your users would actually relate to?"
- "Are the everyday details right? (furniture style, objects, layout)"

**You do NOT have to post anything you don't like.** The first few generations are purely for refining the prompt. Only start posting once the images consistently look good. The agent learns from each round — what works, what doesn't, what to emphasise in the prompt.

Once the style is locked in, THEN use the hook strategy from competitor research and their category (see [references/slide-structure.md](references/slide-structure.md)) and start the posting schedule.

---

## Core Workflow

### 1. Generate Slideshow Images

Use `scripts/generate-slides.js`:

```bash
node scripts/generate-slides.js --config tiktok-marketing/config.json --output tiktok-marketing/posts/YYYY-MM-DD-HHmm/ --prompts prompts.json
```

The script auto-routes to the correct provider based on `config.imageGen.provider`. Supports OpenAI, Stability AI, Replicate, or local images.

**⚠️ Timeout warning:** Generating 6 images takes 3-9 minutes total (30-90 seconds each for gpt-image-1.5). Set your exec timeout to at least **600 seconds (10 minutes)**. If you get `spawnSync ETIMEDOUT`, the exec timeout is too short. The script supports resume — if it fails partway, re-run it and completed slides will be skipped.

**Critical image rules (all providers):**
- ALWAYS portrait aspect ratio (1024x1536 or 9:16 equivalent) — fills TikTok screen
- Include "iPhone photo" and "realistic lighting" in prompts (for AI providers)
- ALL 6 slides share the EXACT same base description (only style/feature changes)
- Lock key elements across all slides (architecture, face shape, camera angle)
- See [references/slide-structure.md](references/slide-structure.md) for the 6-slide formula

### 2. Add Text Overlays

This step uses `node-canvas` to render text directly onto your slide images. This is how Larry produces slides that have hit **1M+ views on TikTok** — the text sizing, positioning, and styling are dialled in from hundreds of posts.

#### Setting Up node-canvas

Before you can add text overlays, your human needs to install `node-canvas`. Prompt them:

> "To add text overlays to the slides, I need a library called node-canvas. It renders text directly onto images with full control over sizing, positioning, and styling — this is what Larry uses for his viral TikTok slides.
>
> Can you run this in your terminal?"
>
> ```bash
> npm install canvas
> ```
>
> "If that fails, it's because node-canvas needs some system libraries. Here's what to install first:"
>
> **macOS:**
> ```bash
> brew install pkg-config cairo pango libpng jpeg giflib librsvg
> npm install canvas
> ```
>
> **Ubuntu/Debian:**
> ```bash
> sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev
> npm install canvas
> ```
>
> **Windows:**
> ```bash
> # node-canvas auto-downloads prebuilt binaries on Windows
> npm install canvas
> ```
>
> "Once installed, I can handle everything else — generating the overlays, sizing the text, positioning it perfectly. You won't need to touch this again."

**Don't skip this step.** Without node-canvas, the text overlays won't work. If installation fails, help them troubleshoot — it's usually a missing system library. Once it's installed once, it stays.

#### How Larry's Text Overlay Process Works

1. **Load the raw slide image** into a node-canvas
2. **Configure text settings** based on the text length for that specific slide
3. **Draw the text** with white fill and thick black outline
4. **Review the output** — check sizing, positioning, readability
5. **Adjust and re-render** if anything looks off
6. **Save the final image** once it looks right

**Exact code Larry uses:**

```javascript
const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');

async function addOverlay(imagePath, text, outputPath) {
  const img = await loadImage(imagePath);
  const canvas = createCanvas(img.width, img.height);
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);

  // ─── Adjust font size based on text length ───
  const wordCount = text.split(/\s+/).length;
  let fontSizePercent;
  if (wordCount <= 5)       fontSizePercent = 0.075;  // Short: 75px on 1024w
  else if (wordCount <= 12) fontSizePercent = 0.065;  // Medium: 66px
  else                      fontSizePercent = 0.050;  // Long: 51px

  const fontSize = Math.round(img.width * fontSizePercent);
  const outlineWidth = Math.round(fontSize * 0.15);
  const maxWidth = img.width * 0.75;
  const lineHeight = fontSize * 1.3;

  ctx.font = `bold ${fontSize}px Arial`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';

  // ─── Word wrap ───
  const lines = [];
  const manualLines = text.split('\n');
  for (const ml of manualLines) {
    const words = ml.trim().split(/\s+/);
    let current = '';
    for (const word of words) {
      const test = current ? `${current} ${word}` : word;
      if (ctx.measureText(test).width <= maxWidth) {
        current = test;
      } else {
        if (current) lines.push(current);
        current = word;
      }
    }
    if (current) lines.push(current);
  }

  // ─── Position: centered at ~28% from top ───
  const totalHeight = lines.length * lineHeight;
  const startY = (img.height * 0.28) - (totalHeight / 2);
  const x = img.width / 2;

  // ─── Draw each line ───
  for (let i = 0; i < lines.length; i++) {
    const y = startY + (i * lineHeight);

    // Black outline
    ctx.strokeStyle = '#000000';
    ctx.lineWidth = outlineWidth;
    ctx.lineJoin = 'round';
    ctx.miterLimit = 2;
    ctx.strokeText(lines[i], x, y);

    // White fill
    ctx.fillStyle = '#FFFFFF';
    ctx.fillText(lines[i], x, y);
  }

  fs.writeFileSync(outputPath, canvas.toBuffer('image/png'));
}
```

**Key details that make Larry's slides look professional:**

- **Dynamic font sizing** — short text gets bigger (75px), long text gets smaller (51px). Every slide is optimized.
- **Word wrap** — respects manual `\n` breaks but also auto-wraps lines that exceed 75% width. No squashing.
- **Centered at 28% from top** — text block is vertically centered around this point, not pinned to it. Stays in the safe zone regardless of line count.
- **Thick outline** — 15% of font size. Makes text readable on ANY background.
- **Manual line breaks preferred** — use `\n` in your text for control. Keep lines to 4-6 words.

**Text content rules:**
- **REACTIONS not labels** — "Wait... this is actually nice??" not "Modern minimalist"
- **4-6 words per line** — short lines are scannable at a glance
- **3-4 lines per slide is ideal**
- **No emoji** — canvas can't render them reliably
- **Safe zones:** No text in bottom 20% (TikTok controls) or top 10% (status bar)

**The difference between OK slides and viral slides is in these details.** Larry's slides consistently hit 50K-150K+ views because the text is sized right, positioned right, and readable at a glance while scrolling.

**⚠️ LINE BREAKS ARE CRITICAL — Read This:**

The `texts.json` file must contain text with `\n` line breaks to control where lines wrap. If you pass a single long string without line breaks, the script will auto-wrap, but **manual breaks look much better** because you control the rhythm.

**Good (manual breaks, 4-6 words per line):**
```json
[
  "I showed my landlord\nwhat AI thinks our\nkitchen should look like",
  "She said you can't\nchange anything\nchallenge accepted",
  "So I downloaded\nthis app and\ntook one photo",
  "Wait... is this\nactually the same\nkitchen??",
  "Okay I'm literally\nobsessed with\nthis one",
  "Snugly showed me\nwhat's possible\nlink in bio"
]
```

**Bad (no breaks — will auto-wrap but looks worse):**
```json
[
  "I showed my landlord what AI thinks our kitchen should look like",
  ...
]
```

**Rules for writing overlay text:**
1. **4-6 words per line MAX** — short lines are scannable at a glance
2. **Use `\n` to break lines** — gives you control over the rhythm
3. **3-4 lines per slide is ideal** — more lines are fine, they won't overflow
4. **Read it out loud** — each line should feel like a natural pause
5. **No emoji** — canvas can't render them, they'll show as blank
6. **REACTIONS not labels** — "Wait... this is nice??" not "Modern minimalist"

The script auto-wraps any line that exceeds 75% width as a safety net, but always prefer manual `\n` breaks for the best visual result.

### 3. Post to TikTok + Instagram

Use `scripts/post-to-platforms.js`:

```bash
node scripts/post-to-platforms.js --config tiktok-marketing/config.json --dir tiktok-marketing/posts/YYYY-MM-DD-HHmm/ --caption "caption" --title "title"
```

This uploads all slide images and posts them to TikTok + Instagram (and any other configured platforms) simultaneously in a single API call via Upload-Post.

**How it works:**
1. Reads slide images from the directory (slide1.png through slideN.png)
2. Sends them to Upload-Post's `POST /upload_photos` endpoint
3. Includes all configured platforms in one request
4. Uses `async_upload=true` for background processing
5. Returns a `request_id` for tracking (saved in `meta.json`)

**No manual video-ID linking needed.** Upload-Post tracks posts automatically by `request_id`. The upload history endpoint returns per-platform post URLs and success/failure status.

**Caption rules:** Long storytelling captions (3x more views). Structure: Hook → Problem → Discovery → What it does → Result → max 5 hashtags. Conversational tone.

### Why We Post TikTok Slideshows as Drafts — Best Practice

For TikTok specifically, posts go as photo carousels. TikTok photo posts benefit enormously from trending sounds:

1. **Music is everything on TikTok.** Trending sounds massively boost reach. The algorithm favours posts using popular audio.
2. **After posting, add music from TikTok's sound library** — browse what's trending in your niche.
3. **Posts without music get buried.** Silent slideshows look like ads and get skipped. A trending sound makes your content feel native.

This is the workflow that helped us hit 1M+ TikTok views and $670/month MRR. Don't skip the music step.

**Instagram carousels don't need music** — they work great as-is. Upload-Post handles both platforms with appropriate settings.

### 4. Track Analytics

Use `scripts/check-analytics.js` to pull platform analytics and upload history:

```bash
node scripts/check-analytics.js --config tiktok-marketing/config.json --days 3
```

The script:
1. Fetches platform-level analytics (followers, impressions, reach, profile views)
2. Fetches upload history for the last N days
3. Groups uploads by `request_id` (one post = multiple platform entries)
4. Shows per-post success/failure status and post URLs
5. Saves a snapshot to `analytics-snapshot.json`

**No connection step needed.** Unlike systems that require manually linking post IDs, Upload-Post tracks everything automatically by `request_id`. When you upload, the history immediately shows which platforms received the post and their post URLs.

**The daily cron handles all of this automatically.** It runs in the morning, checks the last 3 days, and generates a comprehensive report.

---

## The Feedback Loop (CRITICAL — This is What Makes It Work)

This is what separates "posting TikToks" from "running a marketing machine." The daily cron pulls data from two sources:

1. **Upload-Post** → platform analytics (followers, impressions, reach) + upload history (per-post success, post URLs)
2. **RevenueCat** (if connected) → conversion data (trial starts, paid subscriptions, revenue)

Combined, the agent can make intelligent decisions about what to do next — not guessing, not vibes, actual data-driven optimization.

### The Daily Cron (Set Up During Onboarding)

Every morning before the first post, the cron runs `scripts/daily-report.js`:

1. Pulls platform analytics from Upload-Post (followers, impressions, reach timeseries)
2. Pulls upload history for the last 3 days (per-post status, post URLs)
3. If RevenueCat is connected, pulls conversion events in the same window (24-72h attribution)
4. Cross-references: which posts drove views AND which drove paying users
5. Applies the diagnostic framework (below) to determine what's working
6. Generates `tiktok-marketing/reports/YYYY-MM-DD.md` with findings
7. Messages the user with a summary + suggested hooks for today

### The Diagnostic Framework

This is the core intelligence. Two axes: **views** (are people seeing it?) and **conversions** (are people paying?).

**High views + High conversions** → 🟢 SCALE IT
- This is working. Make 3 variations of the winning hook immediately
- Test different posting times to find the sweet spot
- Cross-post to more platforms for extra reach
- Don't change anything about the CTA — it's converting

**High views + Low conversions** → 🟡 FIX THE CTA
- The hook is doing its job — people are watching. But they're not downloading/subscribing
- Try different CTAs on slide 6 (direct vs subtle, "download" vs "search on App Store")
- Check if the app landing page matches the promise in the slideshow
- Test different caption structures — maybe the CTA is buried
- The hook is gold — don't touch it. Fix everything downstream

**Low views + High conversions** → 🟡 FIX THE HOOKS
- The people who DO see it are converting — the content and CTA are great
- But not enough people are seeing it, so the hook/thumbnail isn't stopping the scroll
- Test radically different hooks (person+conflict, POV, listicle, mistakes format)
- Try different posting times and different slide 1 images
- Keep the CTA and content structure identical — just change the hook

**Low views + Low conversions** → 🔴 FULL RESET
- Neither the hook nor the conversion path is working
- Try a completely different format or approach
- Research what's trending in the niche RIGHT NOW (use browser)
- Consider a different target audience angle
- Test new hook categories from scratch
- Reference competitor research for what's working for others

**High views + High downloads + Low paying subscribers** → 🔴 APP ISSUE
- The marketing is working. People are watching AND downloading. But they're not paying.
- This is NOT a content problem — the app onboarding, paywall, or pricing needs fixing.
- Check: Is the paywall shown at the right time? Is the free experience too generous?
- Check: Does the onboarding guide users to the "aha moment" before the paywall?
- Check: Is the pricing right? Too expensive for the perceived value?
- **This is a signal to pause posting and fix the app experience first**

**High views + Low downloads** → 🟡 CTA ISSUE
- People are watching but not downloading. The hooks work, the CTAs don't.
- Rotate through different CTAs: "link in bio", "search on App Store", app name only, "free to try"
- Check the App Store page — does it match what the TikTok shows?
- Check that "link in bio" actually works and goes to the right place

**The daily report automates all of this.** It cross-references platform impressions (Upload-Post) with downloads and revenue (RevenueCat) and tells you exactly which part of the funnel is broken — per post. It also auto-generates new hook suggestions based on your winning patterns and flags when CTAs need rotating.

### Hook Evolution

Track in `tiktok-marketing/hook-performance.json`:

```json
{
  "hooks": [
    {
      "requestId": "abc123def456",
      "text": "My boyfriend said our flat looks like a catalogue",
      "date": "2026-02-15",
      "platforms": {
        "tiktok": { "success": true, "postUrl": "..." },
        "instagram": { "success": true, "postUrl": "..." }
      },
      "conversions": 4,
      "cta": "Download Snugly — link in bio",
      "lastChecked": "2026-02-16"
    }
  ],
  "ctas": [
    {
      "text": "Download [App] — link in bio",
      "timesUsed": 5,
      "totalConversions": 8,
      "conversionRate": 0.067
    },
    {
      "text": "Search [App] on the App Store",
      "timesUsed": 3,
      "totalConversions": 12,
      "conversionRate": 0.141
    }
  ],
  "rules": {
    "doubleDown": ["person-conflict-ai"],
    "testing": ["listicle", "pov-format"],
    "dropped": ["self-complaint", "price-comparison"]
  }
}
```

**The daily report updates this automatically.** Each post gets tagged with its hook text, CTA, and attributed conversions. Over time, this builds a clear picture of which hook + CTA combinations actually drive revenue — not just views.

**CTA rotation:** When the report detects high impressions but low conversions, it automatically recommends rotating to a different CTA and tracks performance of each CTA separately. The agent should tag every post with the CTA used so the data accumulates.

**Decision rules:**
- Growing impressions + conversions → DOUBLE DOWN — make 3 variations immediately
- Steady impressions → Good — keep in rotation
- Declining impressions → Try 1 more variation
- Consistently low → DROP — try something radically different

### CTA Testing

When views are good but conversions are low, cycle through CTAs:
- "Download [App] — link in bio"
- "[App] is free to try — link in bio"
- "I used [App] for this — link in bio"
- "Search [App] on the App Store"
- No explicit CTA (just app name visible)

Track which CTAs convert best per hook category.

---

## Posting Schedule

Optimal times (adjust for audience timezone):
- **7:30 AM** — catch early scrollers
- **4:30 PM** — afternoon break
- **9:00 PM** — evening wind-down

3x/day minimum. Consistency beats sporadic viral hits. 100 posts beats 1 viral.

## Cross-Posting

Upload-Post supports posting the same content to 10+ platforms simultaneously in a single API call. Recommend:
- **Instagram** — especially strong for beauty/lifestyle/home (included by default)
- **YouTube Shorts** — long-tail discovery
- **Threads** — lightweight engagement driver
- **LinkedIn** — for B2B/professional apps
- **Pinterest** — strong for visual/home/design niches

Same slides, different algorithms, more surface area. Each platform's algo evaluates content independently. Upload-Post handles format requirements per platform automatically.

## App Category Templates

See [references/app-categories.md](references/app-categories.md) for category-specific slide prompts and hook formulas.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 1536x1024 (landscape) | Use 1024x1536 (portrait) |
| Font at 5% | Use 6.5% of width |
| Text at bottom | Position at 30% from top |
| Different rooms per slide | Lock architecture in EVERY prompt |
| Labels not reactions | "Wait this is nice??" not "Modern style" |
| Only tracking views | Track conversions — views without revenue = vanity |
| Same hooks forever | Iterate based on data, test new formats weekly |
| No cross-posting | Use Upload-Post to post everywhere simultaneously |
| `spawnSync ETIMEDOUT` | Exec timeout too short — image gen takes 3-9 min for 6 slides. Use a 10-minute timeout or generate slides one at a time |
