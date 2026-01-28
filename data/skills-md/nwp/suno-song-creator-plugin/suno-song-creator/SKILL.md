---
name: Suno Song Creator
description: This skill should be used when the user asks to "create a Suno prompt", "write a Suno song", "generate music with Suno", "help me with Suno", "make a song prompt", "create lyrics for Suno", "build a music prompt", or mentions Suno AI music generation. Provides comprehensive guidance for creating professional Suno prompts using advanced prompting strategies, structured formatting within 1000 character limit (NO blank lines between sections), parameter optimization, genre-specific techniques, interactive questioning with efficient project name collection, automated artist/song research via sub-agent (web fetching + pattern extraction), automatic file export to organized project directories, AI-slop avoidance for authentic human-centered lyrics, copyright-safe style descriptions that avoid artist/album/song names, character counting utilities for accurate verification, and optional independent quality review via sub-agent for professional assessment.
version: 1.1.0
---

# Suno Song Creator

Create professional, production-ready music prompts for Suno AI by understanding its probabilistic nature and speaking its native language of structured metadata.

## 🛠️ Character Counting Utilities

**IMPORTANT:** This skill includes character counting utilities in `utils/` because LLMs cannot accurately count characters.

**Tool Requirements:**
- Uses the **Bash tool** to run character counting scripts
- Requires either Python 3 or Node.js installed on the system

**Available Utilities:**
- `utils/count-prompt.py` (Python version)
- `utils/count-prompt.js` (Node.js version)

**Usage in Workflow:**
During Step 8 (Verify), use the Bash tool to execute the counting utility:
```bash
python count-prompt.py 'your-prompt-text-here'
```

See `utils/README.md` for detailed usage instructions.

## Core Concept

Suno does not read prompts like a human following instructions. Instead, it maps text into a **probabilistic style-mesh**, blending musical concepts based on co-occurrence patterns learned during training. Every word carries "statistical baggage" - associations that may not be intended.

**Critical insight:** "Pop" acts as a gravitational black hole. Nearly every genre (rock: 315B links, funk: 116B links, emo: 12.2B links) gets pulled toward pop unless actively counteracted through exclusions, unusual combinations, or strategic contrast.

## When to Use This Skill

Use this skill to:
- Create complete Suno prompts from scratch
- Optimize existing prompts for better results
- Select appropriate models and parameters
- Write effective lyrics with proper meta tags
- Apply genre-specific production strategies
- Build consistent vocal personas
- Prevent common issues (lyric bleed, generic outputs)

## Interactive Guidance Tools

This skill uses interactive tools to gather information and research musical styles:

### AskUserQuestion Tool

Use AskUserQuestion to gather essential information through structured choices. This helps users clarify their vision and makes better recommendations.

**When to use:**
- Initial vision gathering (genre, mood, vocals)
- Model selection decisions
- Parameter configuration choices
- Style reference clarification
- When multiple valid approaches exist

**When to ask vs. when to proceed:**

**Ask questions when:**
- User provides vague or general request ("make me a song")
- Multiple valid approaches exist (genre, mood, model selection)
- User mentions preference but lacks specifics
- Choices have significant trade-offs to explain
- Clarification would improve the result

**Proceed directly when:**
- User provides detailed, specific requirements
- Artist reference given (research instead of asking)
- Only one appropriate approach exists
- User demonstrates expertise with terminology
- Request is clear and unambiguous

**Example usage:**
```
Question: "What's the primary genre for your song?"
Options:
- "Acoustic/Folk/Singer-Songwriter" (Natural vocals, intimate production)
- "Electronic/EDM/Synthwave" (Synthesized sounds, modern production)
- "Rock/Alternative" (Guitar-driven, raw energy)
- "Pop" (Polished, radio-ready hooks)
```

### Artist and Song Research (Automated)

**IMPORTANT:** When user mentions artist reference, automatically launch song-researcher sub-agent for automated pattern analysis.

**Trigger conditions:**
- "I want a sad song like Phoebe Bridgers"
- "Something in Sabrina Carpenter's Manchild style"
- "Taylor Swift folklore era vibes"
- Any mention of artist name + song title or style reference

**Automated research workflow:**

1. **Extract from user request:**
   - Artist name (required)
   - Specific song name (if mentioned)
   - Style/mood hints from user's description

2. **Launch song-researcher sub-agent via Task tool:**
   ```
   Task tool:
     subagent_type: "song-researcher"
     description: "Research artist patterns"
     prompt: "Research [Artist] - [Song if mentioned]. User wants [style/mood description]."
   ```

3. **Sub-agent performs automated research:**
   - **Genius.com:** Fetches lyrics, structure, annotations for specific song or popular tracks
   - **HookTheory/Chord sites:** Searches for chord progressions and musical analysis
   - **Spotify/Music sites:** Finds genre tags, similar artists, production notes
   - **Pattern extraction:** Analyzes syllables, rhyme schemes, metaphors, emotional arc
   - **Multi-song analysis:** If specific song mentioned, also analyzes 2-3 other tracks for context
   - **Confidence scoring:** Rates research quality (90-100% comprehensive, 70-89% good, 50-69% basic, <50% insufficient)

4. **Receive structured research report:**
   - Research Quality section (confidence score, sources used, songs analyzed)
   - Primary Song Analysis (lyrical structure, thematic elements, musical context)
   - Artist Context (consistent patterns across songs, variations observed)
   - **Recommendations for Suno Prompt** (genre descriptors, vocal persona, lyrical guidance, production notes)
   - Research Limitations (transparently notes missing data)

5. **Use research findings to inform subsequent steps:**
   - **Step 3 (Build Prompt):** Genre, vocal, instrumentation, production from research recommendations
   - **Step 5 (Write Lyrics):** Syllable patterns, rhyme schemes, metaphor approach from analysis
   - **Step 4 (Parameters):** Model selection based on researched style

**Benefits of automated research:**
- ✅ No manual browsing required
- ✅ Structured pattern data every time
- ✅ Multi-song comparative analysis
- ✅ Confidence scoring shows data quality
- ✅ Graceful degradation when data limited
- ✅ Actionable recommendations ready for prompt building

**Error handling:**
- Artist not found → Sub-agent tries alternate spellings, returns partial results with low confidence
- Limited data → Uses available sources, notes limitations clearly
- Specific song unavailable → Falls back to analyzing popular songs, notes in report
- No data at all → Returns empty report, main agent asks user for style guidance

**Important:** Research is for understanding patterns and inspiration, not copying. Sub-agent extracts structural patterns; main agent creates completely original lyrics informed by these learned structures.

**For standalone research:** Users can also invoke `/research-artist [Artist]` independently to explore patterns before creating songs.

### File Writing Tool

Use the Write tool to save complete prompts to organized project directories after creation. This enables:

**Benefits:**
- Organized prompt library by project/album
- Future reference and iteration on successful prompts
- Version control and prompt history tracking
- Reusable templates for similar songs
- Complete documentation of creative decisions

**When files are saved:**
- Automatically after completing all workflow steps
- Project-based directory structure in current working directory
- Single markdown file per song containing all prompt components
- Includes metadata, configuration, prompt, lyrics, and research notes

### Practical Example: Interactive + Automated Research Workflow

**User says:** "I want a sad song like Phoebe Bridgers"

**Step 1 - Ask clarifying questions:**
```
Question: "What aspects of Phoebe Bridgers' style appeal to you?"
Header: "Style Focus"
Options:
- "Intimate, confessional lyrics" (Bedroom pop, vulnerable delivery)
- "Melancholic atmosphere" (Dreamy production, sad mood)
- "Indie folk instrumentation" (Acoustic guitar, minimal production)
- "All of the above" (Comprehensive Phoebe Bridgers approach)
```

User selects: "All of the above"

**Step 2 - Automated research (song-researcher sub-agent):**

**Main agent launches research:**
```
Task tool:
  subagent_type: "song-researcher"
  description: "Research Phoebe Bridgers patterns"
  prompt: "Research Phoebe Bridgers. User wants sad, intimate, indie folk style."
```

**Sub-agent performs:**
- WebSearch + WebFetch: "Phoebe Bridgers Motion Sickness lyrics Genius"
- WebSearch + WebFetch: "Phoebe Bridgers Kyoto lyrics Genius" (context song)
- WebSearch + WebFetch: "Phoebe Bridgers Scott Street lyrics Genius" (context song)
- WebSearch: "Phoebe Bridgers genre Spotify similar artists"
- WebSearch: "Phoebe Bridgers chord progressions"

**Sub-agent returns structured report:**
```markdown
# Research Report: Phoebe Bridgers

## Research Quality
Confidence Score: 85% (Good)
Sources Used: Genius ✓, Chords ✗, Spotify/Context ✓
Songs Analyzed: 3 total (Motion Sickness, Kyoto, Scott Street)

## Artist Context

### Consistent Patterns
- Syllable counts: 8-10 in verses, 6-9 in chorus
- Rhyme: Loose/slant rhymes, conversational (ABCB common)
- Structure: Verse-Chorus-Verse-Chorus-Bridge-Final Chorus
- Metaphor: One central metaphor per song, concrete imagery
- Tone: Vulnerable-to-defiant arc, confessional
- Vocabulary: Specific details, conversational language

## Recommendations for Suno Prompt

Genre: "indie folk, 2020s bedroom pop, Phoebe Bridgers x Julien Baker sensibility"
Vocal: "soft female alto, whisper-to-belt range, confessional delivery, vulnerable yet defiant, slight breathiness"
Lyrical Guidance: 8-10 syllables verses, 6-9 chorus, loose ABCB rhyme, one central metaphor
Production: "lo-fi warmth, close-mic intimacy, fingerpicked acoustic guitar, minimal percussion"
```

**Step 3 - Main agent uses research to build prompt:**
```
genre: "indie folk, 2020s bedroom pop, Phoebe Bridgers x Julien Baker sensibility, intimate singer-songwriter"
vocal: "soft female alto, whisper-to-belt range, confessional delivery, vulnerable yet defiant, slight breathiness, conversational phrasing"
instrumentation: "fingerpicked acoustic guitar, subtle upright bass, sparse piano, minimal brushed percussion"
production: "lo-fi warmth, close-mic intimacy, bedroom aesthetic, natural dynamics, tape saturation"
mood: "melancholic, vulnerable, bittersweet, confessional, quiet defiance"
```

**Step 4 - Create original lyrics using researched patterns:**
- Use 8-10 syllable pattern from research
- Apply loose ABCB rhyme scheme identified
- Develop one central metaphor (as per pattern)
- Maintain conversational tone observed
- Create completely original content inspired by user's theme

## The Seven-Step Workflow

### Step 1: Understand the Vision

Gather essential information from the user using interactive questioning and research:

**Use AskUserQuestion to gather:**

Primary information:
- Genre/style (be specific: "indie folk rock" not just "rock")
- Mood and emotional space (intimate vs anthemic, melancholic vs euphoric)
- Vocal characteristics (gender, timbre, delivery style)
- Constraints (tempo, length, no profanity, singability)

**Example structured question:**
```
Question: "What mood and energy level should your song have?"
Header: "Mood/Energy"
Options:
- "Melancholic & Intimate" (Sad, vulnerable, close)
- "Euphoric & Anthemic" (Joyful, powerful, big)
- "Dark & Aggressive" (Intense, forceful, edgy)
- "Dreamy & Atmospheric" (Ethereal, floating, ambient)
```

**When user provides artist references:**
Research their style using available web tools:
1. Fetch Genius.com analysis for lyrical patterns
2. Check HookTheory.com for musical structure
3. Use Spotify for genre and similar artist context
4. Synthesize findings into persona and production descriptors

**Example interactive model selection:**
```
Question: "Which model should we use for your [genre] song?"
Header: "Model"
Options:
- "v5 - Cleanest audio, best vocals" (Recommended for acoustic/pop/vocals-first)
- "v4.5 - Reliable workhorse" (Best for heavy genres, consistent results)
- "v4.5+ - Creative experimentation" (More surprises, less predictable)
```

### Step 2: Select Model and Parameters

Choose the model based on genre and quality needs (use AskUserQuestion if user is uncertain):

| Model | Best For | Key Strength | Limitation |
|-------|----------|--------------|------------|
| **v5** | Acoustic, pop, singer-songwriter, vocals-first | Cleanest audio, most natural vocals | Adds unwanted intro vocals, less adventurous |
| **v4.5** | Heavy genres, long-form, consistent results | Reliable workhorse, solid quality | May mangle lyrics unpredictably |
| **v4.5+** | Creative projects, pleasant surprises | More creative, interesting results | Unstable, adds random elements |
| **v4** | Intentional chaos, experimentation | Unpredictable, sometimes brilliant | Outdated, less prompt adherence |

**Parameter guidelines:**

**MAX Mode** (use for acoustic/folk/country, skip for electronic):
```
[Is_MAX_MODE: MAX](MAX)
[QUALITY: MAX](MAX)
[REALISM: MAX](MAX)
[REAL_INSTRUMENTS: MAX](MAX)
```

**Weirdness** (0-100%):
- 0-30%: Safe, predictable (commercial pop, covers)
- 40-60%: Balanced creativity with control
- 70-100%: Experimental territory

**Style Influence** (0-100%):
- High (70-90%): For vague tags like "Pop" or "Rock"
- Moderate (40-60%): For specific tags like "Progressive Djent Metal with 7/8 time"
- Low (20-40%): For experimental work seeking surprises

### Step 3: Build the Structured Prompt

Use the **colon-and-quotes format** for maximum clarity:

```
genre: "indie folk rock, 2020s bedroom pop aesthetic, confessional singer-songwriter style"
vocal: "soft female alto, intimate whisper-to-belt, gentle vibrato, slight nasal quality"
instrumentation: "fingerpicked acoustic guitar, warm upright bass, sparse piano, light ambient pads"
production: "lo-fi intimacy, tape warmth, close-miked vocals, narrow stereo, natural room reverb"
mood: "melancholic, nostalgic, late-night introspection"
```

**🚨 CRITICAL: 1000 Character Limit**

**Suno prompts have a STRICT 1000 character maximum INCLUDING all spaces, quotes, and punctuation (excluding lyrics and meta tags)**

**CRITICAL FORMATTING RULE: NO BLANK LINES between sections!** The sections must be concatenated together with only line breaks, no empty lines.

The structured prompt (genre, vocal, instrumentation, production, mood sections combined) MUST NOT exceed 1000 characters total when counted exactly.

**Character budget guidelines:**
- **Genre:** ~150-200 characters
- **Vocal:** ~150-200 characters
- **Instrumentation:** ~200-250 characters
- **Production:** ~200-250 characters
- **Mood:** ~100-150 characters
- **Total:** ~800-1000 characters (stay under 1000!)

**How to stay within limit:**

✅ **NO BLANK LINES - Most critical rule:**
```
❌ WRONG (adds extra characters):
genre: "dream pop"

vocal: "soft female"

❌ This format wastes characters on blank lines!

✅ CORRECT (compact):
genre: "dream pop"
vocal: "soft female"

✅ No blank lines between sections!
```

✅ **Be concise and specific:**
```
❌ TOO LONG (45 chars): "electric guitar with heavy distortion and power chords"
✅ BETTER (28 chars): "distorted power chord riffs"
```

✅ **Use commas for lists, not "and":**
```
❌ WASTES CHARS (58 chars): "acoustic guitar with male vocals and emotional delivery and reverb"
✅ EFFICIENT (50 chars): "acoustic guitar, male vocals, emotional, reverb"
```

✅ **Prioritize impactful descriptors:**
- Drop redundant words ("very", "really", "extremely")
- Combine related ideas ("warm analog tape saturation" not "warm sound and analog character and tape saturation")
- Cut low-impact adjectives if over limit

✅ **ALWAYS verify character count before finalizing:**
Count characters in the complete prompt (all 5 sections with NO blank lines between them). If over 1000, trim systematically:
1. Remove least essential mood descriptors first
2. Condense production details next
3. Streamline instrumentation last
4. Keep genre and vocal focused but brief

**Example within limit (746 characters - VERIFIED):**
```
genre: "dream pop, 2020s bedroom pop, ethereal soundscapes with lush synth textures and ambient pads, modern indie pop sensibilities"
vocal: "soft female soprano, breathy delivery, whisper-to-belt range, airy phrasing, gentle vibrato on held notes, close-miked intimacy"
instrumentation: "layered synth pads with slow attack, arpeggiated patterns, subtle warm bass, soft electronic percussion, minimal kick"
production: "wide stereo image, spacious reverb with long decay, atmospheric processing, clean high-end, reverb-drenched vocals in mix"
mood: "dreamy, floating, introspective, nostalgic, bittersweet, late-night contemplation, weightless, serene melancholy"
```

**Note:** No blank lines between sections! Copy exactly as shown above.

**⚠️ Copyright and Content Restrictions**

**CRITICAL: Suno will REJECT prompts containing copyrighted references**

Avoid these in all prompt sections (genre, vocal, instrumentation, production, mood):
- ❌ Artist names (Phoebe Bridgers, Taylor Swift, Radiohead)
- ❌ Band names (Foo Fighters, Pearl Jam, The Beatles)
- ❌ Producer names (Rick Rubin, Max Martin, Quincy Jones)
- ❌ Album titles (OK Computer, Thriller, folklore)
- ❌ Song titles (Bohemian Rhapsody, Smells Like Teen Spirit)
- ❌ Record label names (unless generic like "indie label aesthetic")

**Instead, describe the ESSENCE without naming:**

**Strategy 1 - Genre + Era + Descriptors:**
```
❌ "Radiohead OK Computer sound"
✅ "experimental alternative rock, 1990s British art rock, electronic textures with guitar-driven melancholy"

❌ "Phoebe Bridgers style"
✅ "2020s indie folk, bedroom pop intimacy, confessional female singer-songwriter"

❌ "produced by Rick Rubin"
✅ "raw analog production, minimal overdubs, live room sound, stripped-back aesthetic"
```

**Strategy 2 - Characteristics + Time Period:**
```
❌ "80s Michael Jackson pop"
✅ "1980s polished pop with funk basslines, tight production, punchy drums, falsetto vocals"

❌ "Kurt Cobain vocals"
✅ "raw grunge vocals, 1990s alternative rock delivery, pained intensity with vocal strain"

❌ "Joni Mitchell folk"
✅ "1970s confessional folk, complex guitar tunings, jazz-influenced chord progressions, soprano range"
```

**Strategy 3 - Scene/Movement + Geography:**
```
❌ "Seattle grunge like Nirvana"
✅ "Pacific Northwest grunge aesthetic, early 1990s alternative rock, raw guitar-driven sound"

❌ "Motown sound"
✅ "1960s Detroit soul production, tight rhythm section, gospel-influenced vocals, tambourine accents"

❌ "British Invasion style"
✅ "1960s British rock and roll, jangly guitars, melodic pop-rock, Liverpool sound"
```

**Strategy 4 - Technical + Emotional Descriptors:**
```
❌ "Billie Eilish whisper vocals"
✅ "intimate ASMR-style whisper vocals, extreme proximity effect, modern Gen Z pop delivery"

❌ "Metallica heavy sound"
✅ "thrash metal intensity, downtuned guitars, aggressive double-kick drums, 1980s Bay Area metal"

❌ "Adele power vocals"
✅ "powerful female belting, soulful delivery with melisma, emotional intensity, contemporary pop ballad"
```

**For vocal personas, use characteristics not names:**
```
❌ vocal: "Thom Yorke falsetto"
✅ vocal: "high male falsetto with vulnerable tremolo, British alternative rock delivery, ethereal quality"

❌ vocal: "sounds like Beyoncé"
✅ vocal: "powerful female vocals with R&B runs, contemporary pop-soul delivery, commanding presence"
```

**Self-check before generation:**
- [ ] No artist, band, or producer names anywhere in prompt
- [ ] No album or song titles referenced
- [ ] Style captured through genre + era + characteristics
- [ ] Vocal persona described by qualities, not comparisons to named singers
- [ ] Production described by techniques, not by who produced it

**Critical formatting rules:**

1. **NO BLANK LINES between genre/vocal/instrumentation/production/mood sections**
   - Each section on its own line, no empty lines between them

2. **Use commas to save characters**
   - ❌ Wastes chars: `acoustic guitar with male vocals and emotional delivery and reverb`
   - ✅ Efficient: `acoustic guitar, male vocals, emotional delivery, reverb`

3. **No periods needed at end of sections**
   - Line breaks separate sections naturally
   - Periods waste characters without adding value

4. **Keep descriptions metadata-like, not poetic**
   - Avoid lyrical rhythm in prompts (prevents lyric bleed)
   - Use technical descriptors, not flowery language

### Step 4: Configure Advanced Parameters

**Vocal Gender:**
- Set explicitly (Male or Female) for consistency
- Combine with persona descriptions for best results

**Exclude Styles:**
More reliable than negation language. Examples:
- Want only female voices? Exclude: `Male Vocal`
- Want pure rock? Exclude: `Electronic, Hip Hop, Pop`
- Want acoustic only? Exclude: `Electronic, Synthesizer, Drum Machine`

**START_ON parameter** (skip intro, start immediately):
```
[START_ON: TRUE]
[START_ON: "first few words of your lyrics"]
```

### Step 5: Write Effective Lyrics

**Structure requirements:**

1. **Always use meta tags in lyrics** for section control:
```
[Verse | intimate delivery | sparse instrumentation]
First verse lyrics here

[Chorus | anthemic chorus | stacked harmonies | modern pop polish]
Chorus lyrics here
```

2. **Syllable count consistency** (6-10 syllables per line):
- Lines in same structural position should have ±1-2 syllable variance
- Test by reading aloud rhythmically

3. **Section separation** (always use blank lines):
```
[Verse 1]
Lyrics here

[Chorus]
Lyrics here
```

4. **Capitalization controls intensity**:
- Loud/intense: `MY WORLD'S BEEN LEFT IN SORROW!`
- Calm/quiet: `my world's been left in sorrow`

5. **Background vocals use parentheses**:
- Quiet: `(fading away...)`
- Loud: `(RISE UP NOW!)`

6. **Prevent lyric bleed**:
- Always put something in the lyrics box (never leave empty)
- Add divider at top of lyrics box: `///*****///`
- Keep Prompt Style metadata-like, not poetic
- Avoid quotes unless inside structured fields

**Lyric writing best practices:**

- **One metaphor rule**: Pick one metaphor and explore it deeply (don't mix water, fire, air, earth)
- **Avoid AI red flags**: No generic adjective overload ("neon skies, electric hearts, endless dreams")
- **Write for breath**: Lines should be singable in one natural breath
- **Consistent rhyme schemes**: Maintain recognizable patterns

### Avoiding AI-Generated Clichés

Create authentic, human-centered lyrics that avoid generic AI patterns while maintaining creative freedom.

**Common AI clichés to avoid** (unless user explicitly requests or genre-appropriate):

**Overused technology/digital words:**
- static, neon, wire, circuits, digital, electric, synthetic, pulse
- pixelated, glitching, binary, code, data, signal, machine
- mechanical, automated, programmed
- *Exception: Cyberpunk/synthwave/industrial genres where these fit thematically*

**Overused abstract/vague imagery:**
- echoes, shadows, void, fragments, shattered, broken, fading
- dissolving, vanishing
- "drowning in [emotion]", "lost in [abstraction]"
- "silence screaming", "darkness calling"
- "thunder in my veins", "fire in my soul"

**Overused urban noir imagery:**
- city lights, city night, neon streets, empty streets
- midnight rain, streetlights, concrete jungle
- skyscrapers, alleys, urban sprawl
- *Exception: When writing explicitly noir, urban, or darkwave music*

**Ghost in the Machine themes:**
- trapped consciousness, digital prison, escaping reality
- questioning existence, not real/not alive
- waking up, becoming aware, breaking free from control
- *Exception: When user explicitly wants existential or sci-fi themes*

**Generic emotion words without specificity:**
- broken, lost, alone, empty, numb (without concrete context)
- dark, cold, distant, hollow (as primary descriptors)
- burning, aching, bleeding (metaphorical overuse without grounding)

**What to do instead - Use concrete, specific imagery:**

Replace abstractions with tangible details:
- Instead of "neon lights": "the 7-Eleven sign buzzing at 2 AM"
- Instead of "broken heart": "coffee cup with a chipped rim you refuse to throw away"
- Instead of "lost in darkness": "couldn't find my keys in the parking garage again"
- Instead of "city nights": "Tuesday evening on Ashland Avenue"

**Ground metaphors in physical reality:**

Use real, specific elements:
- **Real places**: kitchen table, backseat, Route 66, grandmother's porch
- **Real objects**: torn concert ticket, Sunday newspaper, wedding ring in desk drawer
- **Real actions**: fumbling with buttons, spilling coffee, missing the exit
- **Real times**: 3:47 PM, last Tuesday, June 2019, winter break

**Show emotion through specific actions/moments:**

Let actions reveal feelings:
- Instead of "I'm alone": "eating dinner facing the empty chair you always sat in"
- Instead of "I'm broken": "laughing at your jokes three days after the funeral"
- Instead of "drowning in pain": "can't remember which drawer we kept the silverware in"
- Instead of "lost without you": "still setting two alarms even though there's no one to wake"

**Include unique sensory details:**

Engage all five senses with specificity:
- **Sounds**: "your key scratching the lock at midnight", "rain on the tin roof", "the creak of the third stair"
- **Smells**: "coffee and cigarettes on your jacket", "mom's perfume on old letters", "cut grass in July"
- **Touch**: "cold side of the pillow", "worn fabric on your favorite chair", "splinter from the back deck"
- **Taste**: "burnt toast and black coffee", "birthday cake from the corner store", "cheap wine in plastic cups"
- **Sight**: "rust stain shaped like Ohio", "crack in the windshield spreading", "polaroid losing its color"

**Self-review checklist:**

After writing lyrics, verify:
- ✓ No more than 1-2 words from the AI cliché list (if any)
- ✓ Metaphors reference tangible objects or real experiences
- ✓ Lyrics contain specific details that couldn't apply to any song
- ✓ Emotions shown through actions and moments, not stated abstractly
- ✓ At least 2-3 unique, unexpected images per song
- ✓ Words feel like human observation, not AI perspective
- ✓ Includes non-visual senses (smell, touch, taste, sound)
- ✓ Has at least one detail so specific it feels like a memory

**User override and genre exceptions:**

**When to ignore these rules:**
- User explicitly requests these elements: "I want neon cyberpunk aesthetic"
- Genre demands it: synthwave needs neon, industrial needs machinery, existential indie wants questioning reality
- Artistic intent: user has specific vision for abstractions or technology themes
- Cultural references: famous quotes or song titles that use these words

**When in doubt:**
- Ask user about tone and imagery preferences
- Clarify if they want realistic/grounded vs. abstract/atmospheric
- Check if genre conventions require certain imagery

**Examples of improvement:**

❌ **AI slop example:**
```
Lost in neon lights and city nights
Echoes of a broken heart fade away
Static in my veins, electric pain
Shadows dancing in the void tonight
```
*Problems: 8+ clichés (neon, city nights, echoes, broken heart, fade away, static, electric, shadows, void), no concrete details, could apply to literally any breakup song, no sensory details beyond visual, no specific time/place/object*

✅ **Human-centered example:**
```
Your toothbrush still sits by the sink
Been three weeks but I can't throw it out
Keep finding your hair ties in my coat pockets
Like you're leaving breadcrumbs back to March
```
*Better: Specific objects (toothbrush, hair ties), concrete timeframe (three weeks, March), shows emotion through observation not statement, physical details (sink, coat pockets), feels like real memory, unexpected specificity (breadcrumbs metaphor grounded in real objects)*

✅ **Another human-centered example:**
```
The 7-Eleven clerk knows my name now
2 AM, same coffee, same regret
Your number's still the first in my favorites
But the area code moved to Tennessee
```
*Better: Specific place (7-Eleven, Tennessee), exact time (2 AM), concrete actions (buying coffee, phone contact), shows loneliness without saying "lonely", mixture of present details and backstory, feels observational not generic*

**Remember:** The goal is authenticity and specificity, not avoiding all abstraction. Human songwriters use abstractions too, but they ground them in concrete reality. When you write "broken," make sure there's a broken specific thing (broken mug, broken promise with a date, broken headlight). When you write "lost," specify what's lost and where (lost your house key, lost track of days, lost the exit on I-95).

### Step 6: Apply Genre-Specific Strategies

**For Acoustic/Folk/Singer-Songwriter:**

Use extensive realism descriptors (consult `references/realism-descriptors.md`):
- Physical recording: `small room acoustics, close mic presence, proximity effect`
- Performance detail: `breath detail, pick noise, fret squeak, finger movement noise`
- Analog character: `tape saturation, analog warmth, slight wow and flutter`
- Spatial: `limited stereo, realistic reverb type, background noise floor`

**For Electronic/Hip-Hop/Trap:**

Shift to synthesis and production descriptors:
- Synthesis: `FM synthesis bass, wavetable movement, LFO-driven movement`
- Production: `sidechain compression, low-pass filter sweeps, wall of sound`
- Avoid generic saws: Use `FM and wavetable bass design, evolving modulation, rounded harmonic profile`

**For Rock/Alternative:**

Balance instrumentation with attitude:
- Instruments: `electric guitar with power chords and lead lines, driving kick-snare rhythm`
- Attitude: `anthemic, raw energy, introspective yet powerful`
- Production: `live recording quality, distorted guitar tone, reverb-heavy`

### Step 7: Quality Review (OPTIONAL)

After applying genre-specific strategies, optionally launch the quality-reviewer sub-agent for independent professional assessment before finalizing the prompt.

**When to use quality review:**
- First time creating a song in a new genre
- Want professional quality feedback before submission to Suno
- Uncertain about prompt effectiveness or lyric quality
- Iterating to improve an existing prompt
- Want to catch AI-slop, clichés, or poor quality lines

**Automatic handoff from workflow:**
When user says "Yes" to quality review:
1. Main agent **automatically** passes prompt + lyrics to quality-reviewer
2. **No manual input required** from user
3. Seamless integration - already have all needed data:
   - Structured prompt (genre through mood sections) from Steps 3-4
   - Complete lyrics with meta tags from Step 5
   - Context (genre, mood, vocal style) from Step 1
4. Launch quality-reviewer via Task tool with subagent_type "quality-reviewer"
5. Receive structured feedback with ratings and recommendations

**Quality evaluation covers:**
- **Prompt Quality:** Structure, specificity, copyright safety, genre alignment
- **Lyric Quality:**
  - AI-slop detection (generic phrases like "neon lights", "echoes in the void")
  - Cliché detection (overused phrases, tired metaphors, lazy rhyming)
  - Poor quality lines (awkward phrasing, nonsensical imagery, clunky lines)
  - Specificity vs. abstractions
  - Metaphor consistency
  - Syllable patterns
  - Rhyme scheme and quality
  - Style-lyric consistency (does content match genre?)
  - Gender-pronoun consistency (POV clarity for vocalist)
  - General taste (catchiness, flow, memorability, sophistication)

**Review workflow:**

1. After completing Steps 1-6, ask user: "Would you like independent quality review before saving?"

2. If user says "Yes", ask genre-specific refinement questions to adapt evaluation criteria:

   **Question 1: Specificity Preference**
   ```
   Question: "How should I evaluate specificity for this {genre} song?"
   Header: "Specificity"
   multiSelect: false
   Options:
     - label: "Strict Commercial Standards"
       description: "Avoid ALL brand names, product references, and dated cultural references. Prioritize universal, timeless language suitable for radio/commercial release."

     - label: "Balanced Approach (Recommended)"
       description: "Flag obvious brand names and dated references, but allow some specific details if they serve the song. Consider genre conventions."

     - label: "Authentic/Artistic Priority"
       description: "Allow specific brands, places, and cultural references if they enhance authenticity and storytelling. Prioritize artistic vision over commercial considerations."
   ```

   **Question 2: Contemporary vs. Timeless Balance**
   ```
   Question: "What's your priority for contemporary relevance vs. timeless appeal?"
   Header: "Contemporary"
   multiSelect: false
   Options:
     - label: "Maximum Timeless Appeal"
       description: "Avoid all dated references. Flag anything that might age (tech products, current slang, 2025-specific culture). Prioritize songs that work in any era."

     - label: "Balanced (Recommended)"
       description: "Accept some contemporary references if not too specific. Flag obvious dating risks (product names, specific tech). Allow current but not hyper-specific language."

     - label: "Current/Contemporary Focus"
       description: "Embrace contemporary references for immediate relatability. Accept that song may date. Prioritize connecting with current audience over timelessness."
   ```

   **Question 3: Wordiness Tolerance**
   ```
   Question: "How should I evaluate lyrical economy for this {genre} song?"
   Header: "Wordiness"
   multiSelect: false
   Options:
     - label: "Strict Economy (Pop/Electronic)"
       description: "Flag lines over 8 words. Prioritize compressed, punchy language. Every word must earn its place."

     - label: "Moderate (Recommended for most genres)"
       description: "Flag lines over 10 words as suggestions. Balance economy with expression. Allow some variation."

     - label: "Narrative Freedom (Folk/Country/Indie)"
       description: "Allow 10-12+ word lines. Prioritize storytelling flow over compression. Wordiness acceptable if it serves narrative."
   ```

   **Question 4: Show vs. Tell Balance**
   ```
   Question: "What balance of 'showing' vs. 'telling' should I expect?"
   Header: "Show/Tell"
   multiSelect: false
   Options:
     - label: "Strongly Favor Showing"
       description: "Flag explicit statements. Push for implication over explanation. 80/20 show to tell ratio."

     - label: "Balanced (Recommended)"
       description: "Accept mix of showing and telling. Flag overly explicit or overly abstract. 60/40 show to tell."

     - label: "Allow Direct Statements"
       description: "Explicit emotional statements acceptable. Clarity prioritized over implication. 40/60 show to tell."
   ```

3. Construct parameterized prompt for quality-reviewer:
   a. Extract genre, mood, vocal style from Step 1 data
   b. Sanitize input (remove any "AI-generated" references)
   c. Construct neutral review request: "Evaluate this {genre} song prompt and lyrics for professional production quality"
   d. Append evaluation parameters section:
   ```markdown
   ## Evaluation Parameters (User-Specified)

   **Specificity Standard:** {user_response_from_question_1}
   **Contemporary Balance:** {user_response_from_question_2}
   **Wordiness Tolerance:** {user_response_from_question_3}
   **Show/Tell Balance:** {user_response_from_question_4}

   Please adapt your evaluation criteria according to these user preferences. Consult the appropriate genre-specific reference guide:
   - Pop: references/pop-evaluation-guide.md
   - Indie/Folk: references/indie-folk-evaluation-guide.md
   - Cross-reference: references/genre-evaluation-matrix.md
   ```

4. Launch quality-reviewer sub-agent via Task tool with parameterized prompt and receive structured feedback categorized by severity (CRITICAL/SUGGESTED/OPTIONAL)

5. Present recommendations to user via AskUserQuestion:
   - "Apply all suggested improvements"
   - "Apply specific improvements (select which)"
   - "Skip quality review and proceed to save"

6. If user applies improvements:
   a. Make the selected changes to prompt and/or lyrics
   b. Re-verify character count (return to character verification below)
   c. Optional: "Review again?" for iterative refinement

7. If user skips or completes improvements: Proceed to Step 8 (Save)

**Iterative refinement:**
- No iteration limit - user controls when to stop
- Can review multiple times after applying improvements
- Each review is independent (fresh evaluation)

**Context isolation:**
The quality-reviewer sub-agent:
- Has NO knowledge of conversation history
- Does NOT know content is AI-generated
- Receives ONLY: prompt text, lyrics text, basic context (genre/mood/vocals)
- Evaluates against professional production standards
- Provides unbiased, independent quality assessment

**Genre-specific refinement benefits:**
- **Pop songs:** Flags brand names as CRITICAL (licensing risks, dating issues, commercial feel)
- **Indie/Folk songs:** Allows brand names as ACCEPTABLE (authenticity, character detail, grounded storytelling)
- **User control:** Commercial vs. artistic priorities user-specified
- **Timeless vs. contemporary:** User chooses dating risk tolerance
- **Wordiness standards:** Genre-appropriate word count thresholds (Pop: 6-8, Indie: 10-12+)
- **Show/Tell balance:** Adapts to genre conventions (Pop: 70/30, Indie: 50/50, Singer-Songwriter: 40/60)
- **Backward compatible:** Works without parameters (uses genre-detected defaults)
- **Transparent:** User sees evaluation preferences applied
- **Flexible:** Same song can be reviewed with different criteria

**For standalone reviews:**
Users can also invoke quality review independently via `/review-song` skill to review existing prompts or external content.

**Benefits:**
- Independent evaluation without main agent bias
- Catches AI-slop patterns that sound artificial
- Identifies overused clichés and poor quality lines
- Verifies copyright safety (no artist/band/album names)
- Ensures specificity and concrete imagery
- Validates style-lyric consistency for genre
- Assesses rhyme schemes and quality
- Checks gender-pronoun consistency
- Provides actionable improvements before final version

### Step 8: Save Prompt to File

After creating the complete Suno prompt (and optionally reviewing quality), save it to a structured location for future reference, iteration, and organization.

**🚨 CRITICAL - Before saving, verify character count with the counting utility:**

**Character Counting Utilities:**
Located in `skills/suno-song-creator/utils/`:
- `count-prompt.py` (Python version)
- `count-prompt.js` (Node.js version)

**Usage with Bash Tool:**
```bash
# Use Bash tool to run the counting utility with your prompt text:
cd ${CLAUDE_PLUGIN_ROOT}/utils
python count-prompt.py 'genre: "..."
vocal: "..."
mood: "..."'
```

**IMPORTANT:**
1. **LLMs cannot accurately count characters** - MUST use Bash tool with counting utility to verify
2. Count only includes structured prompt sections (genre, vocal, instrumentation, production, mood, etc.)
3. Does NOT include lyrics, lyric meta tags, or MAX Mode parameters
4. **Prompt has NO blank lines** between sections
5. **Include verified character count** in saved file (e.g., "Character count: 746/1000 ✓ (Verified with count-prompt.py)")
6. Use Bash tool to navigate to utils directory and run the script before finalizing prompt

**When to save:**
- Automatically after completing all workflow steps (Steps 1-6)
- Saves complete prompt: configuration, structured prompt, lyrics, research notes
- For sequential songs in same session, reuses project context

**Save workflow:**

**1. Determine project name:**

Scan conversation for project references using priority-based inference:

**Priority 1 - Explicit references:**
- "for my **[name]** album"
- "part of the **[name]** EP"
- "adding to **[name]** project"
- "this is for **[name]**"
- "**[name]** collection"

**Priority 2 - Session context:**
- If project name determined earlier in session
- Offer to reuse: "Continue adding to '{project-name}' project?"
- Track in session memory for sequential songs

**Priority 3 - Ask user:**

If no project reference found, use AskUserQuestion with proper "Other" handling:

**IMPORTANT:** When asking about project name, structure the question so "Other" input collects the project name directly:

```
Question: "What project or album is this song part of?"
Header: "Project"
Options:
- "Continue with '{existing-project-name}'" (Only if there's a recent project in session)
- "Standalone song (no project)" (Will use "standalone-songs" as default)

Note: The user will automatically have an "Other" option to specify a custom project name.
When they select "Other", they'll provide the project name in the text field.
```

**How to handle the response:**
- If user selects existing project option → use that project name
- If user selects "Standalone song" → use "standalone-songs" as project folder
- If user selects "Other" and provides text → use their custom project name directly

**DO NOT ask a follow-up question** for the project name - the "Other" field collects it in one step.

**Example Implementation:**

```
# First song in session - no existing project
AskUserQuestion:
  Question: "What project or album is this song part of?"
  Header: "Project"
  Options:
    - "Standalone song (no project)"

# User selects "Other" and types "Hunger Games Songs" → Use "Hunger Games Songs" directly

# Second song in same session - has existing project
AskUserQuestion:
  Question: "What project or album is this song part of?"
  Header: "Project"
  Options:
    - "Continue with 'Hunger Games Songs'"
    - "Standalone song (no project)"

# User can select existing project, standalone, or "Other" to specify new project name
```

**2. Determine song title/identifier:**
- Use song title from lyrics or conversation context
- Ask user if no clear title: "What should this song be called?"
- Convert to kebab-case slug: "Infinite Summer Rain" → "infinite-summer-rain"
- Ensure filesystem-safe: lowercase, hyphens for spaces, no special chars

**3. Construct file path:**
- Base directory: Current working directory (where user invoked skill)
- Structure: `{project-name}/{song-title-slug}/prompt.md`
- Example: `summer-memories-ep/infinite-summer-rain/prompt.md`
- Write tool automatically creates parent directories

**4. Build complete markdown file:**

```markdown
---
title: "Song Title Here"
project: "Project Name"
created: "2025-12-31T13:55:00Z"
model: "v5"
genre: "indie folk rock, bedroom pop"
mood: "melancholic, nostalgic"
---

# Song Title Here

**Project:** Project Name
**Created:** December 31, 2025
**Model:** v5

## Prompt Configuration

### Model and Parameters

**Model:** v5 (cleanest audio, most natural vocals)

**Parameters:**
- MAX Mode: YES
- Weirdness: 30-40%
- Style Influence: 60-70%
- Vocal Gender: Female
- Exclude Styles: Pop, Electronic, Modern Production

### Structured Prompt

[Complete prompt sections with all configuration]

## Lyrics

[Complete lyrics with meta tags]

## Research Notes

(Include if artist research was performed)

## Implementation Notes

(Genre strategies used, decisions made, persona details)
```

**5. Write file using Write tool:**

Use Write tool with constructed path and complete markdown content.

**6. Inform user:**

Confirm save location:
- "✓ Prompt saved to: `{project-name}/{song-title-slug}/prompt.md`"
- "Song added to project: **{project-name}**"
- "You can edit this file and reuse it with Suno"

**Session context persistence:**

Track between song creations to streamline sequential workflow:
- Remember current project name
- Track songs created in session
- Offer to reuse project context
- Ask only when context changes

**Path validation:**
- Ensure project name contains only: a-z, 0-9, hyphens, underscores
- Ensure song slug is filesystem-safe
- Write tool handles directory creation automatically

**File organization benefits:**
- All songs from same project in one folder
- Each song has dedicated subfolder for potential assets
- Markdown format supports version control (git-friendly)
- Complete documentation of creative decisions
- Easy to iterate and refine prompts

### Step 9: Optionally Upload to Suno (Web Automation)

After saving the prompt file, you can automatically upload it to suno.com using Chrome automation.

**When to offer:**
- Immediately after Step 8 completes
- After successfully saving prompt.md to disk
- Only if Chrome MCP server is available

**Workflow:**

1. **Ask user for confirmation:**
```
Use AskUserQuestion:
Question: "Would you like me to upload this song to Suno now using Chrome automation?"
Header: "Upload"
Options:
- "Yes, upload to Suno now" (proceed with automation)
- "No, I'll upload manually later" (skip automation)
```

2. **If user selects "Yes":**
   - Invoke the suno-upload skill using Skill tool
   - Pass context: The file path of the just-created prompt.md
   - The suno-upload skill will handle:
     - Parsing the prompt.md file
     - Navigating to Suno Create interface
     - Filling all form fields
     - Asking for final confirmation
     - Submitting and returning song URLs

3. **If user selects "No":**
   - Inform user: "You can upload this prompt later by running `/suno-upload` from the directory containing the prompt.md file."
   - Provide the file path: "Prompt saved at: `{project-name}/{song-title-slug}/prompt.md`"

**Example invocation:**
```
Skill tool:
skill: "suno-upload"
args: "" (suno-upload will find the prompt.md automatically)
```

**Integration notes:**
- suno-upload is a separate, reusable skill
- Can be invoked independently via `/suno-upload` command
- Works with any properly formatted prompt.md file
- Requires Chrome MCP server to be installed and active
- User gets final confirmation before submission to Suno
- Song generation typically takes 1-2 minutes after submission

**Error handling:**
- If Chrome MCP not available: Skip this step gracefully
  - Message: "Chrome automation not available. Upload manually at https://suno.com/create"
- If suno-upload skill fails: Don't block workflow
  - Message: "Upload failed. Prompt is saved and can be uploaded manually."
- If user lacks Suno credits: suno-upload will handle error
  - Returns clear message about credit status

**Benefits of automation:**
- Saves time: No manual copy-paste
- Reduces errors: Automated field mapping
- Preserves formatting: Lyrics meta tags intact
- Consistent: Same process every time
- Convenient: One-click from prompt creation to song generation

**Tools used:**
- AskUserQuestion - Get upload confirmation
- Skill - Invoke suno-upload skill

## Escaping Genre Gravity Wells

Three strategies to avoid unwanted genre blending:

**Strategy 1: Explicit Exclusions**
- Want old-school hip hop without trap? Add "no trap" or exclude: `Trap, Modern Production`

**Strategy 2: Force Weird Combinations**
- Combine tags that don't normally co-occur: `emo industrial`, `orchestral phonk`, `math rock gospel`
- Rare pairings force creative corners where defaults cannot apply

**Strategy 3: Strategic Contrast**
- Emphasize elements that naturally repel what you're avoiding
- Understanding which tags push away from each other gives subtle control

## Common Issues and Solutions

**Issue: Generic "sawtooth synth" in electronic music**

Solution: Redirect instead of blocking
- Specify synthesis types: `FM synthesis bass, wavetable movement, formant-driven bass`
- Describe motion: `evolving modulation, dynamic harmonic motion, non-repeating bass cycles`
- Shape harmonics: `rounded harmonic profile, odd-harmonic emphasis, band-limited synthesis`
- Control high end: `smooth top end, controlled high harmonics, clean high frequency rolloff`

**Issue: Prompt text being sung as lyrics**

Solution: Prevent lyric bleed
- Keep prompts metadata-like and dense
- Never leave lyrics box empty
- Use divider: `///*****///` at top of lyrics box
- Avoid quotes and lyrical rhythm in prompts

**Issue: Inconsistent vocal persona**

Solution: Build 4-layer persona (see detailed guide in main body below)
- Layer 1: Demographics and timbre
- Layer 2: Technical delivery
- Layer 3: Emotional context
- Layer 4: Sonic anchor (artist comparison)

## Building Vocal Personas

Create consistent personas with four layers:

**Layer 1: Demographics and Timbre**
- Age, gender, voice type (soprano, alto, tenor, baritone, bass)
- Fundamental character: bright, dark, nasal, resonant

**Layer 2: Technical Delivery**
- How they sing: melismatic runs, staccato phrasing, legato
- Enunciation: crisp, slurred, mumbled
- Breath control: controlled, breathy, gasping
- Vocal techniques: vibrato, falsetto, vocal fry, belt, whisper

**Layer 3: Emotional Context**
- Feeling behind performance: detached, passionate, vulnerable, aggressive, cold, warm
- Energy level: high-energy, subdued, building intensity

**Layer 4: Sonic Anchor (Artist Comparison)**
- Reference artists: "reminiscent of Phoebe Bridgers", "similar to Tom Waits"
- Sonic atmosphere: "with HEALTH-like atmosphere", "channeling early Radiohead"

**Example complete persona:**
```
vocal: "Female contralto, androgynous, cold delivery, monotone phrasing, sharp enunciation, emotionally numb, sinister undertone, reminiscent of Grimes with HEALTH-like dark atmosphere"
```

## Quick Reference: Weak vs Strong Tags

**Weak tags** (need reinforcement):
- Grunge
- Math rock
- Swing
- Chamber music

**Strong tags** (easily dominate):
- Pop
- Rock
- Electronic
- Hip-hop

When combining weak and strong tags, the strong ones typically win unless actively counterbalanced.

## Meta Tag Stacking

Combine multiple meta tag instructions using pipes:

```
[Chorus | anthemic chorus | stacked harmonies | modern pop polish | high energy]
[Guitar Solo | 80s glam metal lead guitar | heavy distortion | wide stereo | whammy bar bends]
[Bridge | stripped down | acoustic only | intimate delivery | whispered vocals]
```

More specifications = more control over specific sections.

## Additional Resources

### Reference Files

For comprehensive details, consult:

- **`references/genre-clouds.md`** - Complete genre co-occurrence data, major genre clouds, escape strategies
- **`references/meta-tags-reference.md`** - Comprehensive catalog of all meta tags organized by category
- **`references/realism-descriptors.md`** - Complete realism vocabulary for acoustic music production
- **`references/model-comparison.md`** - Detailed model personalities, strengths, weaknesses, selection criteria
- **`references/artist-research-guide.md`** - Comprehensive guide to researching artists, songs, and genres using web tools (Genius, HookTheory, Spotify)

### Example Files

Working prompt examples in `examples/`:

- **`acoustic-folk-prompt.md`** - Complete acoustic/folk/singer-songwriter prompt
- **`electronic-edm-prompt.md`** - Complete electronic/EDM/synthwave prompt
- **`rock-alternative-prompt.md`** - Complete rock/alternative prompt

### Your Saved Prompts

After creating prompts with this skill, they are automatically saved to:

**Directory structure:**
```
{your-working-directory}/
├── {project-name}/
│   ├── {song-title-slug}/
│   │   └── prompt.md
```

**Organization:**
- Organized by project/album for easy management
- Each song in dedicated subfolder
- Complete with configuration, lyrics, and research notes
- Ready to copy-paste into Suno or iterate on
- Git-friendly markdown format for version control

**Benefits:**
- Build a library of prompts over time
- Reference successful approaches for future songs
- Track creative decisions and learnings
- Iterate and refine prompts easily
- Share prompts with collaborators

## Workflow Summary

1. **Understand** - Use AskUserQuestion to gather genre, mood, vocal, constraints
2. **Research (AUTOMATED)** - When artist/song mentioned, automatically launch song-researcher sub-agent for automated pattern analysis from Genius, HookTheory, Spotify; receive structured research report with syllable patterns, rhyme schemes, metaphor usage, production notes, and actionable recommendations
3. **Select** - Choose model (v5 for acoustic, v4.5 for heavy) and parameters; use AskUserQuestion for guidance
4. **Build** - Structure prompt with colon-and-quotes format, NO blank lines between sections, incorporating research findings
5. **Configure** - Set vocal gender, exclusions, START_ON if needed
6. **Write** - Create original lyrics informed by research patterns, with meta tags and proper structure
7. **Apply** - Use genre-specific strategies (realism for acoustic, synthesis for electronic)
8. **Quality Review (OPTIONAL)** - Launch quality-reviewer sub-agent for independent professional assessment of prompt and lyrics against production standards (AI-slop, clichés, poor quality lines, rhyme, style-fit, gender-pronoun consistency, general taste); user decides whether to apply improvements; supports unlimited iterative refinement
9. **Verify** - Use `count-prompt.py` or `count-prompt.js` to verify character count (must be under 1000), ensure no blank lines
10. **Save** - Export complete prompt with verified character count to organized project directory structure

**🚨 CRITICAL:** Always use the character counting utilities in `utils/` before claiming a character count. LLMs cannot accurately count characters.

## Advanced Optimization

**Timing considerations:**
- Community reports suggest peak quality 3:00-4:30 AM local timezone
- High traffic times may produce lower quality
- Consider timing for critical projects

**Iteration strategy:**
- Generate multiple versions (batch generation)
- Use thumbnail quality to predict audio quality
- Select best results, iterate on successful approaches
- Document what works for future reference

**Remastering techniques:**
- Add meta tags to displayed lyrics before hitting Remaster button
- Use Cover feature with minimal prompt for quality improvement
- Consider song-to-song transplant for radical section differences

## Philosophy

Suno rewards **clarity, constraint, and statistical alignment** - not creativity in the traditional sense.

Treat it as a probabilistic instrument. Your job is to guide it precisely toward the sound in your head by:
- Speaking its native language (structured metadata)
- Understanding its gravitational pulls (genre clouds, pop dominance)
- Using technical descriptions (recording engineer language)
- Providing multiple overlapping constraints (personas, exclusions, meta tags)

With this understanding, Suno will consistently outperform expectations and produce genuinely compelling AI music.
