---
name: opened-weekly-newsletter-writer
description: Creates Friday OpenEd Weekly digest newsletters consolidating the week's content. This skill should be used when creating the weekly newsletter, Friday digest, or compiling weekly content. Not for daily newsletters.
---

# OpenEd Weekly Newsletter Writer

Creates Friday digest newsletters synthesizing the week's content into six distinct newsletter sections, plus a bonus Phase 4 for creating Ed's Roundup Twitter thread strategy.

**Not for:** Monday-Thursday daily newsletters (use `opened-daily-newsletter-writer`).

**Requirements:** Flexible length (typically 1,500-2,500 words) • NO EMOJIS in body • Pirate Wires-influenced voice • All external links include source attribution in parentheses

## Workflow

### Phase 1: Gather & Organize Source Material

**IMPORTANT EFFICIENCY NOTE:** When the user provides source material directly (copy-pasted content, transcripts, links), DO NOT regenerate it token-by-token. Instead:
- Ask the user to create the `Source_Material.md` file themselves by copy-paste
- OR use Read tool if they've already created it
- OR acknowledge what they've provided and move directly to Phase 2

**Only create/write source material files when:**
- User asks you to organize scattered notes
- User needs help structuring raw data
- Content requires significant reorganization

Collect from the week:
- Opening letter context (timely announcements, promotions, deadlines)
- Deep Dive article with full text and author info
- Deep Dive Podcast episode transcript or description
- Additional curated links, tools, and other resources

If creating `Source_Material.md`, include:
- All URLs, descriptions, and key quotes
- Author names and titles
- Statistics and data points
- Engagement context (why this content matters)
- Names and Twitter handles of people/organizations mentioned (for Phase 4 Twitter thread)

### Phase 2: Draft Opening Letter

Create opening section that:
- Opens with greeting ("Greetings Eddies!" or similar)
- Features the main giveaway/announcement winner/deadline
- Includes light humor (corny joke, relatable observation)
- States what's NOT you (if applicable - "you didn't win")
- Explains the fairness/transparency (e.g., Python script selection)
- Mentions consolation prizes/alternatives
- Ends with clear CTA and links
- Signs off: "– Charlie (the OpenEd newsletter guy)"

**Opening Letter Example Structure:**
1. Greeting + Main announcement
2. Light humor about the "you didn't win" situation
3. Context/transparency about selection process
4. Consolation prizes or alternatives
5. Clear deadline + CTA link
6. Charlie signature

### Phase 3: Draft All Remaining Newsletter Sections

Create `Weekly_Newsletter_Draft.md` with six sections:

**DEEP DIVE: [Article Title]**
- Feature the week's main article/guide
- 3-4 paragraphs, third-person or narrative style
- Hook with compelling angle (can reference notable figures like Adam Savage)
- Include key data point(s)
- End with link to full article: `[Read the full guide on OpenEd](URL)`

**[PODCAST TITLE]: [Episode Title]**
- Brief setup (guest, host, topic)
- One compelling moment or key insight
- 2-3 direct quotes from transcript
- Practical takeaway or hook
- Link to listen: `[Listen to the full episode](URL)`

**Trends We're Following**
- 4-6 data-driven trends/stories from the week
- Each with compelling headline and 1-2 sentence description
- Include relevant data/stats that support the trend
- Source attribution in parentheses: `([Source Name](URL))`
- Focus on what makes each trend noteworthy, not just what happened

**Tools We're Bookmarking**
- 6-10 resources, tools, curricula, or recommendations
- NO category grouping (list sequentially)
- Each with: Tool name (hyperlinked) + benefit-first description (1-2 sentences)
- Attribution woven into text naturally (see Phase 5 attribution style)
- Write to earn the click: hint at value without explaining everything
- Use Pirate Wires tone: observational, slightly irreverent
- **Reddit posts: MAX ONE per newsletter** — pick the best insight, not multiple threads
- If featuring tools from the Deep Dive, consolidate into one summary entry

**Ed's Stable**
- Social media highlights from the week
- Reference recent Instagram/social posts from OpenEd
- Include quirky brand moments (horse mask, chalkboard, etc.)
- 2-3 specific post examples with themes
- Close with reflection that ties newsletter theme to community/brand energy

**Closing:**
```
---

That's all for this week!

– Charlie (the OpenEd newsletter guy)

P.S. [Link to manage email preferences](#)
```

### Phase 4: Create Ed's Roundup Twitter Thread Strategy

**NEW PHASE:** Create `Twitter_Thread_Roundup.md` (or `Twitter_Thread_Roundup_V2.md` if iterating)

This phase creates a multi-tweet thread that recaps the week's key stories and creators featured in the newsletter.

**Step 1: Identify All Twitter Handles**
- Create a comprehensive list of every person/organization mentioned in the newsletter
- Search Twitter/X for each to find active accounts and verify handles
- Prioritize people who are:
  - Featured guests (podcasters, experts)
  - Content creators referenced (Austin Scholar, Adam Savage, Henrik Wes, etc.)
  - Organizations mentioned (LearningRx, Simply Charlotte Mason, etc.)
- Format as: `@handle (Name/Organization) - [brief context]`

**Step 2: Research Active Accounts**
- For each identified person/org, verify:
  - Do they have a Twitter account?
  - Is it active (posted in last 30 days)?
  - Should they be tagged in the thread?
- Document in the Twitter thread file which handles are taggable

**Step 3: Draft Twitter Thread**

**Opening Tweet (Hook):**
- Opens with brand identity: "Ed's Roundup: The most clicked education links from this week"
- Or: "Here's what 10K+ readers of OpenEd Weekly are paying attention to"
- States number of creators: "13 creators. 1 thread."
- Includes emoji (horse/roundup theme): 🪶 or 🐴
- Clear call to action: "(thread)"

**Creator Tweets (One per major theme/person):**
- Feature person's name: @handle
- Their contribution/insight (1 sentence max)
- Direct quote if available
- Link to their content or OpenEd's content about them
- Use proven tweet structures: Direct Quote, Problem Recognition, Data Point, Contrarian Take, Observation Post

**Closing Tweets:**
- Wrap-up tweet with CTA to OpenEd Daily/Weekly
- Engagement tweet asking readers to reply with their favorite creators

**Format Examples:**

*Tweet with direct quote:*
```
"When we teach science as memorization, we're missing the point."

— @AdamSavage (MythBusters)

That quote started a conversation about why wonder matters more than worksheets.

Full deep dive: https://opened.co/blog/best-homeschool-science-curriculum
```

*Tweet with problem/insight:*
```
The reason your kid won't listen when you yell?

It's not defiance. It's neurology.

Dr. Amy Moore explains auditory exclusion: https://opened.co/blog/why-your-adhd-kid-wont-listen-its-not-what-you-think
```

*Tweet with data:*
```
1.5M students are now in microschools.

That's the same as Catholic schools.

Same enrollment. Different satisfaction rates.

@rebeleducator mapped it: [URL]
```

**Reference Guide:** See `references/eds-roundup-example.md` for complete real-world example from Nov 14, 2025 newsletter

### Phase 5: Integrate Source Attributions

As sections are drafted, embed source attributions directly in the newsletter text. No separate `URL_Mappings.md` file needed.

**Attribution Style:**
Mention the source by name EARLY in the blurb with a hyperlink woven naturally into the text. Avoid parenthetical citations at the end.

- **Good:** "A Reddit mom of five shares her hard-won advice..."
- **Good:** "[New EdChoice polling](URL) found overwhelming support..."
- **Good:** "[A Penn Foster survey reported by USA Today](URL) found..."
- **Avoid:** "...bouncing around opens you to gaps. (Reddit)"
- **Avoid:** "...found overwhelming support for teaching debate. ([EdChoice](URL))"

The goal is conversational flow, not academic citation style.

**Hyperlinking Rules:**
When provided a link, always hyperlink it **in the body of the text** (never at the end). Link the **main action or subject** using only **2-3 key words max**.

**Good:** "Ken Danford has been [running North Star](URL) since 1996..."
**Bad:** "[Ken Danford has been running North Star, a physical community center where teens can legally homeschool](URL)"

When multiple sources are provided with body text to reference, **hyperlink ALL links** where the referenced content is used. Don't let any provided link go unhyperlinked.

### Phase 6: QA & Finalization

**Quality Checklist:**
- [ ] NO EMOJIS in newsletter body text (OK in Twitter thread)
- [ ] All external links include source attribution
- [ ] Deep Dive article is compelling (not just a summary)
- [ ] Podcast highlight is one moment, not overview
- [ ] Trends section is data-driven with sources
- [ ] Tools section leads with benefit, not features
- [ ] Ed's Stable reflects actual brand moments
- [ ] All links are verified and working
- [ ] No duplicate content between sections
- [ ] Pirate Wires tone consistent throughout
- [ ] Opening letter includes all key announcements
- [ ] Twitter thread handles are verified and active

**Archive:**
```bash
cp [working-folder]/Weekly_Newsletter_DRAFT.md [archive-folder]/[YYYY-MM-DD]-newsletter-final.md
cp [working-folder]/Social_Media.md [archive-folder]/[YYYY-MM-DD]-social-media.md
cp [working-folder]/X_Article_Format.md [archive-folder]/[YYYY-MM-DD]-x-article.md
```

## Reference Files

Each section of the newsletter has an example reference file with the actual format, real examples from a published newsletter, and specific instructions for writing that section:

- [Opening Letter Example](references/example-opening-letter.md) - How to write warm, inclusive openings with clear CTAs
- [Deep Dive Example](references/example-deep-dive.md) - Third-person teaser format that makes readers curious
- [Podcast Highlight Example](references/example-podcast-highlight.md) - One compelling moment with quotes
- [Trends We're Following Example](references/example-trends.md) - Data-driven stories with source attribution
- [Tools We're Bookmarking Example](references/example-tools.md) - Benefit-first descriptions with sequential ordering
- [Ed's Stable Example](references/example-eds-stable.md) - Social media highlights and brand moments
- [Ed's Roundup Twitter Thread Example](references/eds-roundup-example.md) - Complete Twitter thread with all creators tagged

## Key Distinctions

**Weekly vs Daily:**
- Daily: 500-800 words, 1 each Trend/Tool, shorter sections
- Weekly: 1,500-2,500 words, 4-6 Trends, 10-15 Tools, deeper analysis

**Newsletter Structure:**
- Opening Letter
- Deep Dive Article (Wed article)
- Podcast Highlight (Thu episode - one moment) — **OPTIONAL: skip if no episode that week**
- Trends We're Following (data-driven stories, 4-5 items)
- Tools We're Bookmarking (resources, curricula, 6-10 items, max 1 Reddit)
- Ed's Stable (brand moments, social highlights, engagement ask)

**Social Media Outputs (Phase 4):**
- Social_Media.md (handles table, X thread, single posts)
- X_Article_Format.md (long-form article for X)

**What's Removed:**
- "Listen for the Listeners" (too redundant with Trends)
- "Reddit Corner" (content integrated into other sections as relevant)
- "Parting Thought" (function now served by Ed's Stable closing)

## Critical Reminders

❌ NO EMOJIS in newsletter body
❌ Don't skip Phase 1 (source material gathering)
❌ Deep Dive = Wed article ONLY (not podcast)
❌ Trends must have data
❌ No duplicate content between sections
❌ Twitter handles must be verified before tagging (never guess)
❌ No parenthetical attributions — weave source names early with hyperlinks
❌ Max ONE Reddit post in Tools section

✅ 1,500-2,500 words for newsletter
✅ Humanize stats with context
✅ Benefit-first approach for tools
✅ Create Social_Media.md with handles table, thread, single posts
✅ Create X_Article_Format.md for long-form posting
✅ Archive newsletter, social media, AND X article files

## Phase 4: Social Media Protocol (UPDATED)

Create `Social_Media.md` with the following sections:

### 4.1 Verified Handles Table

Search and verify X/Twitter handles for all people and organizations mentioned in the newsletter. Document in a table:

| Person/Org | Handle | Context | Tag in thread? |
|------------|--------|---------|----------------|
| [Name] | @handle | [Role/quote] | ✅ or ❌ |

Note which are Instagram-only or Substack-only (no Twitter).

### 4.2 X Thread (8-12 tweets)

**Structure:**
1. **Hook tweet** — List the main topics, end with "Thread 👇"
2. **Feature tweets** — One per key person/insight, tag them directly
3. **CTA tweet** — Links to newsletter, deep dive, subscribe

**Tweet formats that work:**
- Direct quote + attribution + link
- Contrarian observation + source
- Data point + implication
- "Meanwhile, @handle shared this..."

### 4.3 Single-Post Options (2-3 standalone posts)

Create 2-3 self-contained posts that can go out independently:
- Best for viral potential (contrarian takes, surprising data)
- Don't require the full thread context
- Can be scheduled throughout the weekend

### 4.4 X Article Format

Create `X_Article_Format.md` — the full newsletter reformatted for X's long-form Articles feature:
- Remove markdown formatting that doesn't render
- Add @ mentions inline where people are quoted
- Keep section headers
- Ensure all links are full URLs

### Expected Output Files:
```
[working-folder]/
├── Weekly_Newsletter_DRAFT.md
├── Social_Media.md          # Handles + thread + single posts
└── X_Article_Format.md      # Long-form X Article version
```

### Success Metrics:
- All mentioned creators identified with verified handles
- Thread tags real, active accounts (not guessed)
- Single posts have standalone viral potential
- X Article is copy-paste ready

---

## Related Skills

- `hook-and-headline-writing` - For generating newsletter subject lines
- `social-content-creation` - For repurposing newsletter sections into individual posts
- `video-caption-creation` - For creating captions for clips featured in newsletter

---

## Version History

- **v2.1** (2026-01-09): Social & Attribution Update
  - **Attribution style changed**: Source name early with hyperlink woven into text (not parenthetical at end)
  - **Phase 4 expanded**: Now includes X Article format, single-post options, handles verification table
  - **Output files**: Now creates Social_Media.md AND X_Article_Format.md
  - **Tools section**: Max ONE Reddit post per newsletter; 6-10 tools (down from 10-15)
  - **Podcast section**: Now optional (skip if no episode that week)

- **v2.0** (2025-11-14): MAJOR UPDATE
  - Simplified from 8 sections to 6 newsletter sections
  - Headers updated: "Trends We're Following" (not "What's Moving")
  - Headers updated: "Ed's Stable" (not "Parting Thought")
  - Removed: "Listen for the Listeners" and "Reddit Corner" (redundant)
  - ADDED: Phase 4 Twitter Thread Strategy ("Ed's Roundup")
  - Added comprehensive Twitter handle verification process
  - Added tweet structure examples and reference guide

- **v1.0** (Previous): Original 8-section structure with separate Podcast Corner and Reddit Corner

---

*For detailed examples of the current structure, see the reference files folder and the Nov 14, 2025 newsletter implementation.*
