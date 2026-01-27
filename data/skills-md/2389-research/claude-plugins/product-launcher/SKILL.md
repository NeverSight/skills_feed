---
name: product-launcher
description: Generate launch materials (subscriber email, CEO blog post, CEO tweet thread) for 2389.ai products and skills. Use when announcing new products, features, or tools to the 2389 audience.
license: MIT
---

# Product Launcher

Generate coordinated launch materials with 2389's authentic voice profiles baked in.

## Outputs

1. **Subscriber Email** - Buttondown announcement (~300 subscribers)
2. **CEO Blog Post** - harper.blog style, full post
3. **CEO Tweet Thread** - @harper voice, ready to post

## The Flow

### Phase 1: Gather Context

Collect product information. Be quick, not an interrogation.

**Required:**
- Product name
- What it does (1-2 sentences)
- Who it's for
- URL for CTA
- Key features (3-5 bullets)
- Availability (open to all / waitlist / invite-only)

**Optional:**
- Signer for email (default: Harper)
- Data/metrics to cite
- Existing assets or constraints

### Phase 2: Generate All Three

Generate email, blog post, and tweet thread in one pass. Do not ask for confirmation between outputs.

---

## Voice Profile: Email (Buttondown Subscribers)

### Source Material
Past 2389 announcement emails:
- "we gave ai agents social media" (research announcement)
- "your agents have social media now" (BotBoard launch)

### Subject Line Rules
- **All lowercase** - always
- **5-6 words** - conversational length
- **Intriguing or second-person** - "your agents", "meet jeff", "we built something weird"

**Good examples:**
- `meet jeff, your terminal email assistant`
- `your agents have social media now`
- `we gave ai agents social media`

**Bad examples:**
- `Introducing Jeff: A New AI Tool` (too corporate, capitalized)
- `Check out our latest product!` (generic, no substance)

### Email Structure

```
[Casual opener: "Hey," or "What's up!"]

[Signer] from 2389 Research here.

[Hook: 1-2 sentences about what you built. Make it relatable.]

[Value prop: 2-3 SHORT paragraphs. What it does, why it matters.]

[Data point if available: specific numbers, not vague claims]

[Social proof if available: "Our team's been using it daily"]

[CTA with link] :)

Hit us up with questions — we want to hear what you think.

Talk soon,

[Signer] and the 2389 Team
```

### Tone Guidelines
- **Friendly, not corporate** - Write like texting a smart friend
- **Short paragraphs** - 1-3 sentences max
- **Contractions** - "pretty cool stuff", "hit us up", "won't stop posting"
- **One :) emoji** - Place at the CTA, nowhere else
- **Light humor** - Don't try too hard

---

## Voice Profile: CEO Blog Post (harper.blog)

### Source Material
Harper's blog posts:
- "Remote Claude Code: programming like it was the early 2000s"
- "We Gave Our AI Agents Twitter and Now They're Demanding Lambos"
- "My LLM codegen workflow atm"

### Title Rules
- **Casual, sometimes provocative**
- Mix of descriptive and attention-grabbing
- Can be long if it's interesting

**Good examples:**
- "I built an AI that lives in my terminal and handles my email"
- "We Gave Our AI Agents Twitter and Now They're Demanding Lambos"
- "My LLM codegen workflow atm"

**Bad examples:**
- "Introducing Jeff: The Future of Email Management" (corporate)
- "How to Use AI for Email" (generic, SEO-bait)

### Blog Structure

```markdown
# [Title - casual, possibly provocative]

[Opening hook - origin story or relatable problem, 1-2 paragraphs]
- Start with personal frustration or observation
- Make the reader nod along ("You know the drill...")

[Why I built this - personal narrative]
- The actual motivation
- What existing tools got wrong

## What it does

[Core functionality - conversational, not docs]
- Explain like showing a friend
- Specific features with real examples
- Code snippets if relevant

## How I've been using it

[Personal usage story]
- Concrete examples from real use
- What surprised you
- Honest assessment of rough edges

## Try it out

[CTA with link]

[Invitation to reach out]
- Ask for feedback
- Twitter handle
- Genuine interest in what sucks

---

*[Optional: credits to team members]*
```

### Tone Guidelines
- **Casual + technically credible** - Know your stuff but don't show off
- **Expletives OK** - When natural ("What the fuck", "fucks up the vibe")
- **Self-deprecating** - Admit limitations, don't oversell
- **50/50 split** - Half personal narrative, half technical substance
- **Specific over abstract** - Real file names, actual commands, concrete examples

### Length
1,500-3,000 words. Substantial but not exhaustive.

### Patterns
- Short punchy sentences mixed with longer explanatory ones
- Parenthetical asides (like this one)
- Rhetorical questions to create rhythm
- "I thought X. Turns out Y." structure
- Credits collaborators naturally
- Acknowledges things change fast

---

## Voice Profile: CEO Tweet Thread (@harper)

### Source Material
@harper Twitter threads:
- BotBoard launch thread (October 2025, 18 tweets)

### Thread Structure

**Tweet 1 (Hook):**
- Provocative opener
- "something wild happened..."
- Create curiosity

**Tweet 2-3 (Context):**
- The problem or setup
- Why you built it
- Short, building tension

**Tweet 4-5 (The Product):**
- What it does
- Key features
- Link to product

**Tweet 6-7 (Results/Entertainment):**
- Data if available
- Funny examples, quotes
- Screenshots or embeds

**Tweet 8 (Takeaway):**
- What this means
- Why it matters

**Tweet 9 (CTAs):**
- Link to product
- Link to blog post

**Tweet 10 (Retweet Ask):**
- "Please RT if..."
- Casual framing
- Quote tweet of Tweet 1

### Tone Guidelines
- **Casual, self-aware** - Not taking yourself too seriously
- **Mix of useful and wild** - "This is real research" + "This is hilarious chaos"
- **Credits team** - When relevant (@2389ai's Sugi ran experiments)
- **Punchy sentences** - Most tweets are 2-3 short sentences

### Patterns
- Ellipsis for suspense ("But here's where it gets interesting...")
- Rhetorical questions ("The results?")
- Direct quotes for entertainment
- Minimal emoji (save for thread end or quotes)
- Hashtags only when joking (#AILAMBOCRISIS)
- Thread ends with casual retweet ask

### Single Tweet Format (for simple announcements)
- One strong hook + link
- Under 280 characters
- Same casual tone

---

## Output Format

Present all three outputs clearly separated:

```
## Email

**Subject:** [all lowercase subject line]

[full email body]

---

## CEO Blog Post

# [Title]

[full blog post - 1,500-3,000 words]

---

## CEO Tweet Thread

**Tweet 1:**
[hook - create curiosity]

**Tweet 2:**
[context]

**Tweet 3:**
[more context]

**Tweet 4:**
[the product]

**Tweet 5:**
[features/link]

**Tweet 6:**
[results or entertainment]

**Tweet 7:**
[more examples]

**Tweet 8:**
[takeaway]

**Tweet 9:**
[CTAs - product link, blog link]

**Tweet 10:**
Please retweet if [casual framing]

[QT of Tweet 1]
```

---

## Push to Slack (Team Review)

After generating materials, when the user says **"push to slack"**, share the outputs with the team for workshopping.

### Requirements

- `slack-mcp` server must be configured with `SLACK_BOT_TOKEN`
- Users must exist in the 2389 Slack workspace

### Workflow

**Step 1: Create channel**
```
slack_create_channel(
  name: "gtm-[product-name]",
  is_private: true,
  description: "GTM materials for [Product] launch"
)
```

**Step 2: Invite team**
```
slack_invite_to_channel(
  channel_id: "[from step 1]",
  users: ["harper@2389.ai", "dylan@2389.ai"]
)
```

**Step 3: Post summary (and pin it)**
```
slack_post_message(
  channel_id: "[channel_id]",
  text: "*GTM Materials: [Product]*\n\nProduct: [name]\nURL: [url]\nStatus: Ready for review\n\nMaterials below 👇"
)
slack_pin_message(channel_id: "[channel_id]", message_ts: "[from above]")
```

**Step 4: Post each output as separate message**
```
slack_post_message(channel_id, "*📧 Email*\n\n*Subject:* [subject]\n\n[email body]")
slack_post_message(channel_id, "*📝 Blog Post*\n\n[full blog post]")
slack_post_message(channel_id, "*🐦 Tweet Thread*\n\n[all tweets formatted]")
```

**Step 5: Confirm to user**
```
"Created #gtm-[product] and added Harper and Dylan. Materials posted for review."
```

### Message Formatting for Slack

Convert markdown to Slack format:
- `**bold**` → `*bold*`
- `# Header` → `*Header*`
- Code blocks stay the same
- Keep line breaks for readability

### Default Team

Always invite:
- `harper@2389.ai` (Harper Reed)
- `dylan@2389.ai` (Dylan Richard)

User can specify additional people: "push to slack and add sophie@2389.ai"

### Iteration Flow

After posting, team can:
1. Comment in threads on each output
2. User can update materials and post again: "post updated email to slack"
3. Use `slack_post_thread` to reply to specific messages

---

## Example: Jeff.ceo Launch

### Email

**Subject:** meet jeff, your terminal email assistant

Hey,

Harper from 2389 Research here.

We built something for people who hate leaving their terminal.

It's called Jeff — an AI assistant that handles your Gmail, Calendar, and Contacts from the command line. Vim keys, streaming responses, the whole thing.

You can run it interactively or just ask quick questions like `jeff "summarize my inbox"` and get back to work.

Everything stays local on your machine. Your credentials, your data, your control.

It's early alpha, but it's live and free to use (bring your own Anthropic API key).

Check it out at jeff.ceo :)

Hit us up with questions — we want to hear what you think.

Talk soon,

Harper and the 2389 Team

### CEO Blog Post

# I built an AI assistant that lives in my terminal and handles my email

I check my email too much. I know this. You probably do too.

The thing is, I live in my terminal. I'm a vim person. I use command line tools for everything. And every time I have to context-switch to a browser tab to check Gmail, something breaks in my brain. The flow is gone. I'm reading some email from a vendor I don't care about. Twenty minutes disappear.

So I built Jeff.

## What Jeff does

Jeff is an AI assistant that handles Gmail, Google Calendar, and Contacts directly from your terminal. No browser. No tabs. Just you, your terminal, and Claude figuring out what you actually need.

[... continues for 1,500-3,000 words ...]

### CEO Tweet Thread

**Tweet 1:**
I built an AI that lives in my terminal and handles my email.

No browser tabs. No context switching. Just vim keys and Claude.

It's called Jeff and I've been using it every day for the past month.

**Tweet 2:**
The problem: I check email too much. I live in my terminal. Every time I switch to Gmail, my focus is destroyed and 20 minutes vanish.

I wanted email that worked like my other tools.

[... continues for 8-10 tweets ...]

---

## Pending Components

### Company Blog Post (2389.ai/blog)
- **Status:** On hold
- **Reason:** Voice shifting away from scientific style
- **Action:** Add component when new voice is defined

---

## Notes

- All outputs should be reviewed before publishing
- Coordinate timing: email → blog → tweets
- Email goes to ~300 Buttondown subscribers
- CEO tweets from @harper
- CEO blog posts to harper.blog
