---
name: post
description: |
  Quick Twitter/X content generation using brand profile.
  Generates on-brand posts mixing product updates with valuable content.

  Auto-invoke when: user wants to post about a product, share an update,
  generate social content, or needs post ideas.
argument-hint: "[product] \"message\" | --ideas [product]"
---

# /post

Generate on-brand social content. Fast.

## Usage

```bash
# Generate posts for a specific update
/post volume "just shipped interval timer feature"

# Generate content ideas from git history
/post --ideas volume

# Generate a thread
/post volume "launched v2.0" --thread

# Generate without brand profile (generic)
/post "excited to announce our new feature"
```

## What This Does

1. Loads `brand-profile.yaml` if available
2. Applies brand voice, tone, and topics
3. Generates 3-5 post variants
4. Includes relevant hashtags
5. Outputs ready-to-copy content

## Process

### If Brand Profile Exists

Read `brand-profile.yaml` from:
1. Current directory
2. Or `~/.claude/skills/brand-builder/profiles/[product].yaml`

Apply:
- **Voice**: Match tone (casual, professional, playful, technical)
- **Personality**: Incorporate personality traits
- **Avoid**: Skip anything in the "avoid" list
- **Hashtags**: Include primary + product hashtags
- **Topics**: Ensure content fits established topics

### Post Generation

For a product update like "shipped interval timer":

**Variant 1: Feature-focused**
```
New in Volume: Interval timers for rest periods.

No more watching the clock between sets. Set your rest time, get notified when you're ready.

#fitness #strengthtraining #volumeapp
```

**Variant 2: Problem-solution**
```
"How long was I resting again?"

Volume now has interval timers. Set your rest, focus on your form, we'll tell you when to go.

#gymlife #strengthtraining
```

**Variant 3: Casual/Building in public**
```
Just shipped rest timers to Volume.

Small feature, but I've wanted this for months. Sometimes the simple stuff makes the biggest difference.

What's a small feature that made a big difference for you?

#buildinpublic #indiedev
```

**Variant 4: Direct/Short**
```
Rest timers are live in Volume.

Track your lifts. Time your rest. See your gains.

volume.app
```

### Ideas Generation (--ideas)

When user runs `/post --ideas volume`:

1. Read recent git history:
```bash
git log --oneline --since="2 weeks ago" | head -20
```

2. Identify postable updates:
   - New features
   - Bug fixes (if significant)
   - Milestones

3. Pull from brand profile topics:
   - Domain content ideas
   - Evergreen topics

4. Output ideas list:
```
POST IDEAS FOR VOLUME (Week of Jan 20)

From Git History:
1. "Shipped interval timer feature" - Feature announcement
2. "Fixed chart rendering on mobile" - Could mention improved mobile experience
3. "Added 50 new exercises" - Library expansion

From Brand Topics:
4. Strength training tip: Progressive overload basics
5. Gym culture: Rest periods and why they matter
6. Motivation: Celebrating small PR wins
7. Behind the scenes: Why we built the timer feature

Recommended mix: 2 product updates + 3 valuable content this week
```

## Output Format

```
───────────────────────────────────────────────────
POST OPTIONS FOR: Volume - Interval Timer Launch
───────────────────────────────────────────────────

OPTION 1 (Feature-focused):
New in Volume: Interval timers for rest periods.

No more watching the clock between sets. Set your rest time, get notified when you're ready.

#fitness #strengthtraining #volumeapp

───────────────────────────────────────────────────

OPTION 2 (Problem-solution):
"How long was I resting again?"

Volume now has interval timers. Set your rest, focus on your form, we'll tell you when to go.

#gymlife #strengthtraining

───────────────────────────────────────────────────

OPTION 3 (Building in public):
Just shipped rest timers to Volume.

Small feature, but I've wanted this for months. Sometimes the simple stuff makes the biggest difference.

What's a small feature that made a big difference for you?

#buildinpublic #indiedev

───────────────────────────────────────────────────

OPTION 4 (Short & direct):
Rest timers are live in Volume.

Track your lifts. Time your rest. See your gains.

volume.app

───────────────────────────────────────────────────

Account: @MistyStepLLC (from brand profile)
Character counts: 1) 167  2) 148  3) 201  4) 75
```

## Thread Generation (--thread)

For larger announcements, generate a thread:

```
/post volume "launched v2.0 with charts, timer, and exercise library" --thread
```

Output:
```
THREAD: Volume 2.0 Launch (5 tweets)

1/5
Volume 2.0 is here.

6 months of work. Completely rebuilt from scratch.

Here's what's new:

🧵

2/5
📊 Progress Charts

Finally see your gains over time.

Track any exercise. See your 1RM progression. Know when to add weight.

3/5
⏱️ Rest Timers

Set your rest period between sets. Get notified when you're ready.

No more watching the clock. Just lift.

4/5
📚 Exercise Library

50+ exercises with proper form guides.

Don't know how to do a Romanian deadlift? We've got you.

5/5
Try it free at volume.app

Built for lifters who want to track progress without the complexity.

#fitness #strengthtraining #volumeapp
```

## Content Mix Guidance

From brand profile, respect the mix ratio:
- ~30% product updates
- ~70% valuable content

When running `--ideas`, suggest accordingly:
- If last 3 posts were product updates → suggest valuable content
- If no product posts recently → suggest a feature highlight

## Without Brand Profile

If no profile exists, generate generic posts:
- Use neutral professional tone
- Skip product-specific hashtags
- Note: "Run /brand-builder to create on-brand content"

## Related Skills

- `/brand-builder` - Create the brand profile first
- `/announce` - Full launch announcement (more elaborate)
- `/social-content` - Existing skill for content strategy
- `/copywriting` - Existing skill for marketing copy
