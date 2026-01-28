---
name: announce
description: |
  Launch post generator for multiple platforms.
  Creates Twitter, HN, Reddit, and Indie Hackers announcements.

  Use for product launches, major updates, or milestone announcements.
argument-hint: "[url] [description]"
---

# /announce

Launch announcements for every platform. One command.

## What This Does

Generates launch posts optimized for:
- Twitter/X
- Hacker News (Show HN)
- Reddit (relevant subreddits)
- Indie Hackers
- Product Hunt (draft)

Each post formatted for platform norms and best practices.

## Usage

```bash
# Basic announcement
/announce https://volume.app "Fitness tracking app for lifters"

# With more context
/announce https://volume.app "Track your lifts, see your progress" --features "Progress charts, Exercise library, Rest timers"

# Specific platform only
/announce https://volume.app --twitter-only
```

## Process

### 1. Gather Context

**From URL** (browser automation or fetch):
- Page title and description
- Key features from content
- Screenshots/visuals

**From Brand Profile** (if exists):
- Voice and tone
- Target audience
- Hashtags

**From User Input**:
- One-line description
- Key features (if provided)

### 2. Generate Platform-Specific Posts

#### Twitter/X

Short, punchy, visual-friendly:

```
Just launched: Volume

Track your lifts. See your gains.

✅ Progress charts
✅ 50+ exercises
✅ Rest timers

Free at volume.app

#fitness #strengthtraining #buildinpublic
```

Variants:
- Feature-focused
- Story-focused (why I built this)
- Question/engagement opener

#### Hacker News (Show HN)

Title + context that HN appreciates:

```
TITLE:
Show HN: Volume – Simple strength training tracker

BODY:
Hey HN,

I built Volume because existing fitness apps are either too complex or focused on cardio.

Volume is dead simple:
- Log your lifts (exercise, weight, reps)
- See progress over time
- Get notified when to rest

Built with Next.js, TypeScript, and Convex. Happy to answer any questions about the stack or the fitness tracking space.

https://volume.app
```

Key elements:
- "Show HN:" prefix in title
- Technical context (HN loves this)
- Open to questions
- No marketing fluff

#### Reddit

Subreddit-specific and authentic:

**r/fitness**
```
TITLE:
I built a simple lifting tracker because every app was too complicated

BODY:
After years of using spreadsheets and apps that wanted me to track calories, sleep, water, AND workouts, I built something focused:

Volume tracks just your lifts. That's it.

- Log exercise, weight, reps
- See charts of your progress
- Simple rest timer

It's free, no account required to start.

Would love feedback from the community: https://volume.app

What features would make a lifting tracker actually useful for you?
```

**r/selfhosted** or **r/SideProject**
```
TITLE:
[Project] Volume - Open source strength training tracker

BODY:
Built this over the last few months as a side project. Stack is Next.js + TypeScript + Convex.

Focused on simplicity - just tracking lifts and showing progress.

Source: github.com/MistyStep/volume
Try it: volume.app

Happy to discuss architecture decisions or take feature requests.
```

#### Indie Hackers

Founder story + metrics + ask:

```
TITLE:
🚀 Just launched Volume - Strength training tracker for people who hate complex apps

BODY:
Hey IH!

**The problem:**
Every fitness app wants to track everything - calories, sleep, water, mood. I just want to remember how much I lifted last time.

**The solution:**
Volume does one thing: tracks your lifts. Log the exercise, weight, and reps. See your progress over time.

**The stack:**
- Next.js + TypeScript
- Convex for backend
- Vercel for hosting
- Total monthly cost: ~$0 (free tiers)

**Current status:**
- Launched today
- 0 users (it's launch day!)
- Free forever, considering pro tier later

**The ask:**
Would love early feedback. What would make you actually use a lifting tracker?

Link: https://volume.app
```

#### Product Hunt (Draft)

For later submission:

```
TAGLINE:
Track your lifts. See your gains.

DESCRIPTION:
Volume is a strength training tracker built for people who hate complex fitness apps.

No calorie counting. No meal plans. No social features. Just:
✅ Log your exercises, weights, and reps
✅ See progress charts over time
✅ Rest timer between sets

Built by a lifter, for lifters.

FIRST COMMENT:
Hey PH! 👋

I'm [name], and I built Volume because I was frustrated with fitness apps trying to do everything.

I've been lifting for [X] years, and all I wanted was a simple way to track my progress. Volume is what I wish existed when I started.

Would love your feedback - what would make the perfect lifting tracker for you?
```

### 3. Output Format

```
LAUNCH ANNOUNCEMENTS FOR: Volume
═══════════════════════════════════════════════════════════════

TWITTER/X
─────────────────────────────────────────
Just launched: Volume

Track your lifts. See your gains.

✅ Progress charts
✅ 50+ exercises
✅ Rest timers

Free at volume.app

#fitness #strengthtraining #buildinpublic
─────────────────────────────────────────
Character count: 178
Account: @MistyStepLLC

HACKER NEWS
─────────────────────────────────────────
Title: Show HN: Volume – Simple strength training tracker

[Full body text]
─────────────────────────────────────────
Submit at: https://news.ycombinator.com/submit

REDDIT
─────────────────────────────────────────
Subreddit: r/fitness
Title: I built a simple lifting tracker because every app was too complicated

[Full body text]
─────────────────────────────────────────
Other relevant subreddits: r/GYM, r/strength_training, r/SideProject

INDIE HACKERS
─────────────────────────────────────────
[Full post]
─────────────────────────────────────────
Submit at: https://www.indiehackers.com/new-post

PRODUCT HUNT (DRAFT)
─────────────────────────────────────────
[Draft for later]
─────────────────────────────────────────
Prepare at: https://www.producthunt.com/posts/new

═══════════════════════════════════════════════════════════════

LAUNCH CHECKLIST:
□ Post to Twitter first (engage with replies)
□ Submit to HN (morning EST best)
□ Post to Reddit (read subreddit rules first!)
□ Post to Indie Hackers
□ Save Product Hunt draft for later (schedule properly)

TIMING TIPS:
- Twitter: Anytime, engage quickly
- HN: Tuesday-Thursday, 9am EST
- Reddit: Check each subreddit's active hours
- Indie Hackers: Weekdays
- Product Hunt: Tuesday-Thursday, midnight PST
```

## Platform Guidelines

### Twitter
- Keep under 280 chars (or use thread)
- Emojis OK but don't overdo
- Visual content performs better
- Reply to comments quickly

### Hacker News
- No marketing speak
- Technical details appreciated
- Be ready to answer questions
- Don't ask for upvotes

### Reddit
- Read subreddit rules first
- Be authentic, not promotional
- Engage with comments
- Don't spam multiple subreddits

### Indie Hackers
- Founder story matters
- Be specific about stack/costs
- Ask genuine questions
- Follow up on feedback

### Product Hunt
- Schedule carefully (midnight PST)
- Prepare maker comment
- Get hunter if possible
- Engage all day

## Related Skills

- `/post` - Quick posts (not full launches)
- `/launch-strategy` - Full launch planning
- `/copywriting` - Better marketing copy
- `/brand-builder` - Establish voice first
