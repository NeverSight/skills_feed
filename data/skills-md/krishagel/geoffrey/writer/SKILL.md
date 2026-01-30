---
name: writer
description: Generate content in your authentic voice across emails, blogs, social media, and reports
triggers:
  - "write"
  - "draft"
  - "compose"
  - "help me write"
  - "in my voice"
  - "write blog"
  - "write email"
  - "write post"
allowed-tools: Read, Write, Bash, Skill, AskUserQuestion
version: 0.1.0
---

# Writer Skill

Generate content in your authentic voice by analyzing writing samples and applying learned voice patterns through adaptive interviewing and voice-matched generation.

## Philosophy

**Key Innovation**: This isn't a generic AI writer - it's YOUR voice, learned from YOUR writing.

Unlike generic AI content generation, this skill:
- Learns from 6 distinct voice profiles (work email, personal email, blog, LinkedIn, Twitter, reports)
- Interviews you like a Pulitzer-winning journalist to deeply understand your message
- Validates output against your authentic patterns (not generic "good writing")
- Saves versioned drafts to Obsidian for iteration and history

**Simplicity**: Geoffrey's native LLM capabilities analyze your voice. Scripts just fetch samples. No complex NLP libraries - clean, maintainable architecture.

---

## When to Activate

Use this skill when you need to:
- Write emails that sound like you (not generic AI)
- Draft blog posts in your established voice
- Create social media content consistent with your style
- Generate reports matching your professional tone
- Ensure content authentically represents your perspective and voice

**DON'T use for**:
- Quick factual responses (use native Claude)
- Content in someone else's voice
- Generic templates

---

## Voice Profiles

Six distinct profiles capture different contexts:

| Profile | Source | Sample Target | Status |
|---------|--------|---------------|--------|
| `email_work` | PSD Gmail (sent emails, 6mo) | 50+ emails | Check writing-voice.json |
| `email_personal` | Personal/HRG Gmail (sent, 6mo) | 50+ emails | Check writing-voice.json |
| `blog_technical` | psd401.ai + blog.krishagel.com | 10+ posts | Check writing-voice.json |
| `social_linkedin` | LinkedIn profile posts | 30+ posts | Check writing-voice.json |
| `social_twitter` | X/Twitter posts | 30+ posts | Check writing-voice.json |
| `report_formal` | User-provided samples | 5-10 reports | Check writing-voice.json |

**Confidence Levels**:
- **High (0.85+)**: 50+ samples - voice well established
- **Moderate (0.70-0.84)**: 20-49 samples - patterns emerging
- **Low (<0.70)**: <20 samples - insufficient data, warn user

---

## 6-Phase Workflow

### Phase 1: Voice Profile Selection & Validation

**Goal**: Load the right voice profile and verify it's ready

**Process**:
1. Detect content type from user request:
   - "write email" → `email_work` or `email_personal` (ask which)
   - "blog post" → `blog_technical`
   - "LinkedIn post" → `social_linkedin`
   - "tweet" → `social_twitter`
   - "report" → `report_formal`

2. Load voice profile:
   ```bash
   cat ~/Library/Mobile\ Documents/com~apple~CloudDocs/Geoffrey/knowledge/writing-voice.json
   ```

3. Check confidence and sample count:
   - If confidence ≥ 0.85: Proceed with confidence
   - If confidence 0.70-0.84: Proceed with note
   - If confidence < 0.70: Warn user, offer options

**Low Confidence Response**:
```
Only {sample_count} {content_type} samples (confidence: {confidence}).
Target: {target_samples}+ samples for 0.85+ confidence.

Options:
1. Gather more samples (recommended)
2. Use {alternative_profile} voice as proxy (confidence: {alt_confidence})
3. Proceed anyway (may not fully match your voice)

Preference?
```

**Checkpoint 1**: User confirms profile or gathers more samples

---

### Phase 2: Deep Interview (Adaptive)

**Goal**: Deeply understand what you want to communicate

**Process**:
1. Load interview questions from `templates/interview-questions.json`

2. Adapt depth to content type:
   - **Tweet/Social**: 3-5 questions (~2-3 min)
   - **Email Quick**: 4 questions (~3 min)
   - **Email Complex**: 8 questions (~5 min)
   - **Blog**: 8-12 questions (~5-8 min)
   - **Report**: 15+ questions (~10-15 min)

3. Interview like a journalist:
   - Ask follow-up questions for vague answers
   - Probe for examples, data, evidence
   - Clarify ambiguities
   - Build structured understanding

**Email Interview Example** (complex):
```
1. Who are the recipient(s) and what's the context?
   → [User answers]

2. What's the primary goal?
   → [User answers]
   [If vague: "Can you be more specific about the outcome you want?"]

3. What background do they need?
   → [User answers]

4. What are the key points? (Max 3-5)
   → [User answers]
   [If >5: "Let's focus on the most critical 3-5 points."]

... continue through 8 questions
```

**Blog Interview Example**:
```
1. What's your central message?
2. Why does this matter right now?
3. What should readers do/think/feel after?
4. What evidence supports this?
5. Any stories or case studies?
6. Main counterarguments?
7. How should it open?
8. Key sections (3-5)?
9. How should it close?
10. Primary audience and technical level?
11. Desired tone?
```

**Checkpoint 2**: Review interview summary, add missing details

---

### Phase 3: Content Planning & Outline

**Goal**: Create a clear structure before writing

**Process**:
1. Create outline based on:
   - Interview responses
   - Content type structure (email: intro + points + ask, blog: hook + body + conclusion)
   - Voice profile preferences (e.g., blog uses chronological flow, staff quotes)

2. Apply voice-specific patterns:
   - Email: Opening pattern, bullet points for key points, clear ask
   - Blog: Subheadings for scannability, narrative flow, reflective close
   - Social: Hook first line, call-to-action

3. Suggest length from profile:
   - Email avg: Check profile examples
   - Blog avg: Check profile examples
   - Social: Platform limits (LinkedIn 1300 chars, Twitter 280 chars)

**Email Outline Example**:
```
## Email Plan

**Subject**: [Based on purpose]

**Opening**: [Use opening pattern from profile, e.g., "I've reviewed {topic}..."]

**Body**:
- Point 1: [From interview]
- Point 2: [From interview]
- Point 3: [From interview]

**Ask**: [Specific call-to-action from interview]

**Closing**: [Use closing pattern from profile, e.g., "Let me know if..."]

**Tone**: Direct, professional, action-oriented
**Length**: ~200 words (typical for email_work)
```

**Blog Outline Example**:
```
## Blog Plan

**Title**: [Derived from central message]

**Structure**:
1. Opening: [Hook strategy - context-setting or reflective quote]
2. Background & Context
3. [Main section 1]
4. [Main section 2]
5. [Main section 3]
6. Impact & Results
7. Closing: [Forward-looking reflection]

**Voice elements**:
- Staff quotes (use throughout)
- Chronological narrative flow
- Subheadings for scannability
- Accessible but authoritative tone

**Length**: ~850 words (typical for blog_technical)
```

**Checkpoint 3**: User approves outline

---

### Phase 4: Draft Generation

**Goal**: Write content that authentically sounds like you

**Process**:
1. Load identity context:
   ```bash
   cat ~/Library/Mobile\ Documents/com~apple~CloudDocs/Geoffrey/knowledge/identity-core.json
   ```

   Use for personality alignment:
   - `communication_preferences.style` → Direct, no-nonsense, concise
   - `decision_framework` → Analytical, evidence-based
   - `telos_summary.top_3_values` → Equity, excellence, empathy

2. Apply voice characteristics as generation guidelines:
   - **Tone**: From `voice_characteristics.tone`
   - **Sentence structure**: From `voice_characteristics.sentence_structure`
   - **Vocabulary**: Common terms, avoided terms
   - **Formatting**: Bullet points, markdown, emphasis patterns
   - **Opening**: Use patterns from `opening_patterns`
   - **Closing**: Use patterns from `closing_patterns`
   - **Argument structure**: Lead with conclusion, use evidence

3. Write content naturally:
   - Use Geoffrey's native writing capabilities
   - Guided by voice profile (not rigid pattern matching)
   - Weave in interview content (examples, data, stories)
   - Match typical length from profile examples

4. Reference example emails/posts from profile for inspiration

**Generation Approach** (Hybrid):
- Write naturally with rich voice context
- Don't mechanically apply patterns
- Let voice characteristics inform style, not constrain creativity

---

### Phase 5: Validation & Refinement

**Goal**: Ensure draft authentically matches your voice

**Native LLM Validation** (no script needed):

1. **Geoffrey self-validates** by comparing draft to voice profile:
   - Read the draft I just generated
   - Read the voice profile (`voice_characteristics` + `examples`)
   - Compare tone, structure, vocabulary, formatting
   - Score alignment 0-100

2. **Scoring criteria** (weighted):
   - Tone match (20%)
   - Sentence structure - length, complexity (15%)
   - Vocabulary - common/avoided terms (15%)
   - Formatting - bullets, markdown, emphasis (10%)
   - Opening pattern match (10%)
   - Closing pattern match (10%)
   - Argument structure - conclusion placement, evidence use (10%)
   - Stylistic markers - contractions, punctuation, framing (10%)

3. **Identify specific deviations**:
   - "Sentences 15% longer than typical (avg 16 words vs typical 14)"
   - "Missing characteristic bullet points (you use them 67% of time)"
   - "Tone slightly more formal than usual"

4. **Scoring thresholds**:
   - 85-100: Excellent match, present draft
   - 70-84: Good match with minor deviations, note them
   - <70: Significant deviations, propose refinements

**Refinement** (if score < 85):
```
Voice Validation: {score}/100

Issues:
- {Issue 1 with specific evidence}
- {Issue 2 with specific evidence}
- {Issue 3 with specific evidence}

Should I refine to better match your voice?
```

If user approves refinement:
- Apply specific fixes identified
- Re-validate
- Present refined draft

**Checkpoint 4**: User accepts, requests refinement, or manually edits

---

### Phase 6: Storage & Versioning

**Goal**: Save draft to Obsidian with proper versioning

**Process**:
1. Determine file path:
   ```
   ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal_Notes/Geoffrey/Writing/{ContentType}/{date}-{slug}.md
   ```

   Content types:
   - Blog → `Geoffrey/Writing/Blog/`
   - Email → `Geoffrey/Writing/Email/`
   - Social → `Geoffrey/Writing/Social/`
   - Reports → `Geoffrey/Writing/Reports/`

2. Generate frontmatter:
   ```yaml
   ---
   created: 2025-12-06
   type: blog
   profile: blog_technical
   topic: AI implementation
   status: draft
   version: 1.0
   validation_score: 87
   word_count: 847
   tags: [geoffrey, writing, ai]
   source: geoffrey-writer
   interview_date: 2025-12-06
   ---
   ```

3. Save file using Obsidian MCP tools:
   ```
   mcp__obsidian-vault__create_vault_file
   ```

4. Also return text directly (copy-paste ready)

5. Offer to open in Obsidian:
   ```
   mcp__obsidian-vault__show_file_in_obsidian
   ```

**Versioning**:
- Initial: `version: 1.0`
- Refinements: `version: 1.1`, `1.2`
- Major rewrites: `version: 2.0`

**Output to user**:
```
## Draft Complete

**Validation Score**: 87/100 ✓
**Word Count**: 847
**Profile**: blog_technical

**Saved to**: Geoffrey/Writing/Blog/2025-12-06-ai-implementation.md

[Full draft text here]

Actions:
1. Open in Obsidian
2. Request refinements
3. Mark as final
```

---

## Voice Learning Process

### Initial Setup (Before First Use)

**Required**: Gather writing samples for each profile you'll use

**Step 1: Email Samples** (3 accounts)
```bash
# PSD work emails
bun scripts/extract-email-samples.js \
  --account psd \
  --date-range "2024-06-01:2025-12-06" \
  --max-samples 100 \
  --output "/tmp/email-samples-psd.json"

# Personal emails
bun scripts/extract-email-samples.js \
  --account kh \
  --date-range "2024-06-01:2025-12-06" \
  --max-samples 50 \
  --output "/tmp/email-samples-kh.json"

# Business/consulting emails
bun scripts/extract-email-samples.js \
  --account hrg \
  --date-range "2024-06-01:2025-12-06" \
  --max-samples 50 \
  --output "/tmp/email-samples-hrg.json"
```

**Step 2: Blog Samples**
```bash
# Launch Geoffrey Chrome (for personal blog access)
cd ~/non-ic-code/geoffrey/skills/browser-control
./scripts/launch-chrome.sh

# Extract blog posts
cd ~/non-ic-code/geoffrey/skills/writer
bun scripts/extract-blog-samples.js \
  --urls "https://psd401.ai/blog/stanford-ai-tinkery-2025,https://psd401.ai/blog/why-this-website,https://blog.krishagel.com/post1,https://blog.krishagel.com/post2" \
  --output "/tmp/blog-samples.json"
```

**Step 3: Social Media Samples** (requires login)
```bash
# IMPORTANT: Manually log into LinkedIn and X in Geoffrey Chrome first

# LinkedIn
bun scripts/extract-social-samples.js \
  --platform linkedin \
  --profile-url "https://linkedin.com/in/krishagel" \
  --max-posts 50 \
  --output "/tmp/social-linkedin.json"

# Twitter/X
bun scripts/extract-social-samples.js \
  --platform twitter \
  --profile-url "https://x.com/KrisHagel" \
  --max-posts 50 \
  --output "/tmp/social-twitter.json"
```

**Step 4: Geoffrey Analyzes**

Tell Geoffrey:
```
Analyze my writing samples and create voice profiles.

Email samples: /tmp/email-samples-psd.json, /tmp/email-samples-kh.json, /tmp/email-samples-hrg.json
Blog samples: /tmp/blog-samples.json
Social samples: /tmp/social-linkedin.json, /tmp/social-twitter.json
```

Geoffrey will:
1. Read all sample files
2. Analyze each profile's:
   - Tone and voice
   - Sentence structure patterns
   - Vocabulary (common/avoided terms)
   - Formatting preferences
   - Opening/closing patterns
   - Argument structure
   - Distinctive markers
3. Select representative examples
4. Calculate confidence scores
5. Write to `writing-voice.json`:
   ```
   ~/Library/Mobile Documents/com~apple~CloudDocs/Geoffrey/knowledge/writing-voice.json
   ```

**Estimated time**: 30-45 min initial setup

---

## Integration Points

### knowledge-manager → Identity Context

**When**: Phase 4 (Draft Generation)

**Purpose**: Ensure voice reflects personality (analytical, direct, impact-driven)

**How**:
```bash
cat ~/Library/Mobile\ Documents/com~apple~CloudDocs/Geoffrey/knowledge/identity-core.json
```

**Use**:
- `communication_preferences` → Tone, style, dislikes
- `decision_framework` → Analytical, evidence-based approach
- `telos_summary` → Values (equity, excellence, empathy), mission
- `strengths_essence` → Input (collector), Significance (impact), Analytical

---

### google-workspace → Email Samples

**When**: Initial voice creation + quarterly refresh

**Scripts**: `search_messages.js`, `read_message.js`

**Process**:
1. Search sent emails
2. Filter automated, short, quoted
3. Clean signatures, HTML
4. Extract plain text + metadata
5. Save to JSON for Geoffrey to analyze

---

### browser-control → Blog/Social Samples

**When**: Initial voice creation + ad-hoc updates

**Prerequisites**: Geoffrey Chrome running with logins

**Process**:
1. Navigate to blog/profile URL
2. Extract article/post content
3. Handle scrolling/lazy-loading (social)
4. Parse and clean content
5. Save to JSON

---

### obsidian-manager → Draft Storage

**When**: Phase 6 (Storage)

**Folder structure**:
```
Geoffrey/Writing/
├── Blog/
├── Email/
├── Social/
└── Reports/
```

**File format**: `YYYY-MM-DD-{slug}.md` with frontmatter

---

## Edge Cases & Handling

### Insufficient Samples

**Scenario**: User requests email, but only 12 samples (confidence 0.62)

**Response**:
```
Only 12 email_work samples (0.62 confidence). Target: 50+ for 0.85+ confidence.

Options:
1. Gather ~40 more email samples from recent sent (recommended)
2. Use email_personal as proxy (if similar, confidence: 0.88)
3. Proceed with low confidence (may not fully match your voice)

Note: Voice profiles improve with more samples. I can still write, but authenticity may vary.

Preference?
```

---

### Voice Drift (Outdated Profile)

**Scenario**: Profile last updated 18 months ago

**Detection**: Check `last_updated` in writing-voice.json

**Response**:
```
Your email_work profile is 18 months old (last updated: 2024-06-15).
Writing styles evolve over time.

Recommendation: Refresh with recent samples (past 6 months)

Run:
bun scripts/extract-email-samples.js --account psd --date-range "2024-06-01:2025-12-06" --max-samples 100 --output "/tmp/email-refresh.json"

Then ask me to analyze and update the profile.

Proceed with current profile or refresh first?
```

---

### Contradictory Samples

**Scenario**: Email samples vary significantly (45% formal, 35% casual, 20% mixed)

**Geoffrey analyzes** and responds:
```
Your email_work voice varies significantly across samples:
- 45% formal (board, superintendent, external)
- 35% casual (staff, peers, project teams)
- 20% mixed

Options:
1. Split into email_work_formal and email_work_casual profiles
2. Choose dominant style (formal) as default
3. Let me dynamically adjust based on recipient (you specify each time)

Preference?
```

---

### Low Validation Score

**Scenario**: Draft scores 62/100

**Response**:
```
Voice Validation: 62/100 ⚠️

Issues:
- Tone too formal (target: direct, action-oriented)
  Example: "It would be appreciated if you could consider..." vs typical "Please review and confirm."

- Sentences 35% longer (avg 19 words vs typical 14)
  Example: Draft paragraph 2 avg 21 words, your emails avg 14 words.

- Missing bullet points (you use bullets 67% of the time for key points)
  Draft uses prose for 5 key points, you typically bullet them.

Should I refine to better match your voice?
```

---

### New Content Type

**Scenario**: User requests "write a press release"

**Response**:
```
I don't have a press_release voice profile yet.

Options:
1. Use report_formal profile as starting point (confidence: 0.83)
2. Provide 5-10 past press releases for me to analyze
3. Write without voice matching (generic professional press release style)

Note: If you provide samples, I can create a new press_release profile.

Preference?
```

---

## Usage Examples

### Example 1: Quick Work Email

**User**: "Write email to my team about next week's leadership meeting"

**Geoffrey**:
```
I'll use your email_work profile (confidence: 0.92, 156 samples).

Quick interview (4 questions):

1. Who's the team and what's your relationship?
   → [User: Direct reports - IT leadership team]

2. Purpose? (inform, request, respond, update)
   → [User: Inform and request prep]

3. Key information?
   → [User: Meeting Tuesday 2pm, agenda items: budget, staffing, AI roadmap. Need their input on AI priorities.]

4. Tone?
   → [User: Professional but casual - these are my directs]
```

[Generates outline] → User approves

[Generates draft, validates (score: 89), presents to user]

---

### Example 2: Blog Post

**User**: "Write blog post about our AI implementation journey"

**Geoffrey**:
```
I'll use your blog_technical profile (confidence: 0.78, 4 samples).

Note: Only 4 blog samples. Recommend 6+ more for 0.85+ confidence.
Proceed or gather more samples first?

→ [User: Proceed]

Standard interview (11 questions):

1. Central message?
   → [User: ...]

2. Why now?
   → [User: ...]

[... continues through 11 questions ...]
```

[Creates detailed outline] → User approves

[Generates ~850 word draft with staff quotes, chronological flow, reflective close]

[Validates (score: 87), presents draft]

[Saves to Geoffrey/Writing/Blog/2025-12-06-ai-implementation-journey.md]

---

### Example 3: LinkedIn Post

**User**: "LinkedIn post about Stanford AI Tinkery visit"

**Geoffrey**:
```
I'll use your social_linkedin profile (confidence: 0.91, 48 posts).

Quick interview (5 questions):

1. Main point (1-2 sentences)?
   → [User: Visited Stanford's AI Tinkery with district team. Collaborative learning happening everywhere, not just at elite institutions.]

2. Target audience?
   → [User: Ed tech leaders, superintendents]

3. Tone?
   → [User: Inspirational, reflective]

4. Call-to-action?
   → [User: Encourage others to build their own learning networks]

5. Link or visual?
   → [User: No link, maybe photo but I'll add later]
```

[Generates ~180 word LinkedIn post]

[Validates (score: 92), presents]

---

## Limitations

### Known Constraints

1. **Sample Dependency**: Voice quality directly tied to sample quantity and quality
   - Low samples (<20) = low accuracy
   - Poor quality samples = poor voice matching

2. **Voice Drift**: Styles evolve over time
   - Recommend quarterly refresh (every 3 months)
   - Auto-warn if profile >12 months old

3. **New Contexts**: No profile for content types you haven't written before
   - Press releases, technical docs, grant proposals require new samples
   - Can adapt existing profiles but may not match perfectly

4. **Platform Nuances**: Social media scraping limitations
   - LinkedIn/X may change selectors
   - Requires manual login
   - May violate ToS (user accepted risk)

5. **Multilingual**: Currently English only
   - No Spanish email profile (even though you write Spanish emails)
   - Could add with Spanish samples

6. **Collaborative Writing**: Single voice only
   - Can't blend your voice + co-author
   - Future enhancement

---

## Validation & Quality

### Success Metrics

**Quantitative**:
- Voice alignment: 85+ for established profiles (0.85+ confidence)
- Sample size: 50+ emails, 10+ blogs, 30+ social per profile
- User acceptance: >80% drafts accepted with minor/no edits
- Refinement iterations: <2 average

**Qualitative**:
- User feedback: "This sounds like me"
- Consistent voice across topics within profile
- Authentic, not mechanical or formulaic

### Quality Checklist

Before presenting draft:
- ✓ Matches tone from voice profile
- ✓ Sentence structure within 20% of typical length
- ✓ Uses common vocabulary, avoids avoided terms
- ✓ Follows formatting preferences (bullets, markdown)
- ✓ Opening/closing match typical patterns
- ✓ Argument structure aligned (conclusion placement, evidence use)
- ✓ Validation score ≥85 (or explained deviations if <85)
- ✓ Word count within typical range for content type

---

## Future Enhancements (Out of Scope)

1. **Real-time Learning**: Auto-analyze new sent emails monthly
2. **A/B Testing**: Generate 2 versions, learn from user choices
3. **Collaborative Voice**: Blend user + co-author voices
4. **Multi-language**: Spanish voice profiles
5. **Performance Tracking**: Voice drift detection over time
6. **Audience-Aware**: Sub-profiles (email_work_superintendent vs email_work_staff)
7. **Feedback Loop**: User rates content, Geoffrey learns from scores

---

## Troubleshooting

### "No voice profile found"

**Cause**: writing-voice.json doesn't exist or profile type missing

**Solution**:
1. Check if file exists:
   ```bash
   cat ~/Library/Mobile\ Documents/com~apple~CloudDocs/Geoffrey/knowledge/writing-voice.json
   ```
2. If missing: Run initial setup (extract samples + ask Geoffrey to analyze)
3. If file exists but profile missing: Add samples for that content type

---

### "Low confidence warning"

**Cause**: Fewer than 20 samples for profile

**Solution**:
1. Gather more samples using extraction scripts
2. Ask Geoffrey to re-analyze with new samples
3. Or: Proceed with caveat that voice may not fully match

---

### "Geoffrey Chrome not running"

**Cause**: Social/blog extraction requires Geoffrey Chrome with remote debugging

**Solution**:
```bash
cd ~/non-ic-code/geoffrey/skills/browser-control
./scripts/launch-chrome.sh
```

---

### "Failed to extract social posts"

**Cause**: Not logged into LinkedIn/X, or selectors changed

**Solution**:
1. Open Geoffrey Chrome manually
2. Navigate to LinkedIn/X and log in
3. Verify posts load
4. Re-run extraction script
5. If still fails: Platform may have changed selectors (update script)

---

## Notes

- **Progressive Disclosure**: Load only the profile needed for current task (not all 6)
- **Identity Alignment**: Always cross-reference identity-core.json for personality consistency
- **Checkpoints**: 4 user approval points prevent wasted effort
- **Versioning**: All drafts saved to Obsidian with version numbers
- **Native Analysis**: Geoffrey's LLM capabilities analyze voice - no complex libraries needed
