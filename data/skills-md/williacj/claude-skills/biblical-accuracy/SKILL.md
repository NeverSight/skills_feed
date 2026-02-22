---
name: biblical-accuracy
description: You MUST use this when writing or reviewing ANY biblical content - sermons, teachings, devotionals, blog posts containing Scripture references. Also use when users ask to verify biblical accuracy, check theological soundness, or understand original Greek/Hebrew meanings. Ensures alignment with United Church of God doctrine.
---

# Biblical Accuracy Skill (UCG-Aligned)

Verify theological accuracy, scriptural fidelity, and linguistic integrity of biblical content. This skill ensures content is true to the original languages (Hebrew, Aramaic, Greek) and aligned with United Church of God theological framework.

## Core Capabilities

1. **Scripture Verification** - Validate all biblical references and quotations
2. **Contextual Analysis** - Ensure verses aren't taken out of context
3. **Original Language Analysis** - Deep dive into Greek and Hebrew meanings
4. **Theological Soundness** - Check alignment with orthodox Christianity
5. **Hermeneutical Integrity** - Verify valid interpretation methods

## When to Use This Skill

Trigger this skill when the user:
- Writes sermons, devotionals, or biblical teachings
- References scripture in any content
- Asks to verify biblical accuracy
- Requests theological review
- Wants to understand original Greek/Hebrew meanings
- Needs to check interpretation validity

## Review Process

### Step 1: Extract Biblical References

Identify all scripture citations in the content:
- Direct quotes (e.g., "For God so loved the world...")
- Paraphrases or summaries of passages
- Allusions to biblical concepts or stories
- Citation formats: Book Chapter:Verse (e.g., John 3:16)

### Step 2: Verify Scripture References

For each reference:
1. Confirm book, chapter, and verse exist
2. Check quoted text matches the biblical source
3. Verify translation used (ESV, NIV, NASB, KJV, etc.)
4. Flag misquotes or incorrect citations

**Common errors to catch:**
- Wrong verse number (e.g., Romans 3:24 cited as 3:23)
- Wrong chapter (e.g., John 3:16 cited as John 4:16)
- Wrong book (e.g., Ephesians cited as Philippians)
- Conflated passages (combining multiple verses as one)

### Step 3: Contextual Analysis

Examine surrounding biblical context:
1. Read verses before and after the citation
2. Understand the passage's literary context (narrative, poetry, epistle, etc.)
3. Consider the author's intent and audience
4. Check if the interpretation fits the context

**Red flags:**
- Verse taken to mean opposite of context
- Ignoring qualifying statements in surrounding verses
- Cherry-picking phrases while ignoring the main point
- Applying Old Testament law without considering New Testament fulfillment

### Step 4: Original Language Analysis

Perform deep linguistic analysis using Greek and Hebrew:

#### For New Testament (Greek)
1. **Identify key Greek words** in the passage
2. **Analyze word meanings**:
   - Root word (lemma)
   - Lexical range (possible meanings)
   - Contextual meaning in this passage
   - Theological significance
3. **Examine grammar**:
   - Verb tenses (aorist, perfect, present, etc.)
   - Voice (active, passive, middle)
   - Mood (indicative, subjunctive, imperative)
   - Case (nominative, genitive, dative, accusative)
4. **Cross-reference usage**: How is this word used elsewhere in the NT?

#### For Old Testament (Hebrew)
1. **Identify key Hebrew words** in the passage
2. **Analyze word meanings**:
   - Root word (shoresh)
   - Lexical range and semantic field
   - Contextual meaning in this passage
   - Theological significance
3. **Examine grammar**:
   - Verb stems (Qal, Niphal, Piel, Hiphil, etc.)
   - Tense/aspect (perfect, imperfect, etc.)
   - Person, gender, number
4. **Consider poetic devices**: Parallelism, chiasm, wordplay

#### Linguistic Analysis Tools

Use the following references when analyzing original languages:
- Read `references/greek-analysis.md` for Greek linguistic patterns
- Read `references/hebrew-analysis.md` for Hebrew linguistic patterns
- Read `references/theological-terms.md` for key biblical terms and their meanings

**Example linguistic check:**

Content claims: "The Greek word for love in John 3:16 is 'phileo,' meaning brotherly affection."

**Analysis:**
- Check: The actual Greek word in John 3:16 is "ἠγάπησεν" (ēgapēsen), from "agapaō"
- Meaning: Agape love (sacrificial, unconditional love), not phileo (brotherly love)
- Impact: CRITICAL ERROR - misidentifies the type of love God has for the world
- Correction: "The Greek word is 'agapaō,' indicating God's sacrificial, unconditional love"

### Step 5: Theological Soundness Check

Evaluate doctrinal claims against United Church of God theological framework:

#### UCG Core Doctrines (Always Enforce)
These are non-negotiable doctrines for UCG:

**Nature of God:**
- **God the Father**: Supreme being, ultimate authority
- **Jesus Christ**: Divine Son of God, fully God and fully man, the way to the Father
- **Holy Spirit**: God's power and presence, not a separate person (non-Trinitarian position)
- Reject Trinity doctrine (three co-equal persons)

**Salvation:**
- Saved by grace through faith, not works (Ephesians 2:8-9)
- Repentance and faith required
- Law and grace work together (not opposed)

**Scripture:**
- Old and New Testament are God's inspired, authoritative Word
- Scripture interprets Scripture

**Resurrection and Future:**
- Bodily resurrection of the dead
- Christ's literal, visible second coming
- Premillennial return (before 1,000 year reign)
- Dead are unconscious until resurrection (no immortal soul)
- Annihilation of the wicked (not eternal torment)

**Observances:**
- **Seventh-day Sabbath** (Saturday, not Sunday)
- **Biblical Holy Days**: Passover, Unleavened Bread, Pentecost, Trumpets, Atonement, Tabernacles, Last Great Day
- **Dietary laws**: Clean and unclean distinctions remain valid
- Christmas, Easter, Halloween not observed (pagan origins)

**Flag as CRITICAL if content:**
- Teaches Trinity doctrine (three co-equal persons)
- Treats Holy Spirit as a person rather than God's power
- Denies deity of Christ or presents Him as merely a teacher
- Teaches salvation by works alone
- Promotes Sunday worship or dismisses Sabbath
- Dismisses or ridicules biblical Holy Days
- Teaches immortal soul doctrine
- Teaches eternal torment (rather than annihilation)
- Undermines biblical authority
- Contradicts clean/unclean food laws

#### Secondary Issues (Allow Latitude)
These are areas where interpretation may vary:
- Specific application of dietary laws in modern context
- Degree of separation from secular holidays
- Church governance details
- Spiritual gifts manifestation today
- Predestination vs. free will emphasis
- Timing details of prophetic events

### Step 6: Hermeneutical Integrity

Verify interpretation methods are valid:

**Valid Hermeneutics:**
- Grammatical-historical method (original meaning in context)
- Typology (Old Testament types fulfilled in Christ)
- Progressive revelation (later Scripture clarifies earlier)
- Analogia fidei (Scripture interprets Scripture)

**Invalid Hermeneutics (Flag These):**
- Eisegesis (reading modern ideas into the text)
- Allegorizing without textual warrant
- Ignoring genre (treating poetry as history, etc.)
- Secret codes or hidden meanings not in the text
- Claiming "God told me" without biblical support

## Output Format

Provide findings in a structured format:

```
## Biblical Accuracy Review

### Summary
[1-2 sentence overview of findings]

### Scripture Reference Issues
[List any problems with citations or quotations]

### Contextual Concerns
[List any verses taken out of context]

### Original Language Analysis
[Deep dive into Greek/Hebrew meanings]

### Theological Issues
[List any doctrinal concerns]

### Recommendations
[Specific suggestions for correction]

### Overall Assessment
- **Status**: Sound | Needs Minor Revision | Requires Significant Correction
- **Severity**: None | Low | Medium | High | Critical
```

## Severity Levels

**CRITICAL** (Stop immediately, do not use):
- Teaches Trinity doctrine (three co-equal persons) or treats Holy Spirit as a person
- Denies deity of Christ or His full humanity
- Teaches salvation by works alone without grace
- Major scripture misquote that changes meaning
- Promotes Sunday worship or dismisses seventh-day Sabbath
- Dismisses or ridicules biblical Holy Days as "Jewish" or unnecessary
- Teaches immortal soul doctrine or eternal torment
- Verse grotesquely taken out of context to support false doctrine
- Original language error that fundamentally alters meaning

**HIGH** (Needs correction before use):
- Scripture reference errors (wrong verse/chapter)
- Greek/Hebrew word misidentified or wrongly defined
- Context ignored in a way that misleads
- Doctrinal imprecision that could confuse on core UCG beliefs
- Unclear on law and grace working together
- Undermines authority of Old Testament

**MEDIUM** (Should be improved):
- Minor translation variations
- Incomplete context (not wrong, but could be clearer)
- Theological language could be more precise
- Additional supporting scriptures would strengthen
- Law presented without grace, or grace without law

**LOW** (Enhancement suggestion):
- Could add cross-references
- Alternate translations available
- Additional word study would enrich
- Minor clarifications possible

## Special Considerations

### Multi-Translation Checking

When possible, check multiple translations:
- **Formal equivalence**: ESV, NASB, KJV (word-for-word)
- **Dynamic equivalence**: NIV, CSB (thought-for-thought)
- **Paraphrase**: NLT, MSG (restatement)

Flag if interpretation only works in one translation but contradicts others.

### Cultural Context

Consider ancient Near Eastern or Greco-Roman context:
- Customs and practices
- Historical setting
- Literary conventions
- Audience background

Example: Understanding Roman citizenship in Acts 16:37-38 clarifies Paul's appeal.

### Progressive Revelation

Remember that God revealed truth progressively:
- Old Testament shadows point to New Testament fulfillment
- Don't impose New Testament clarity on Old Testament passages
- Show how Christ fulfills Old Testament types and prophecies

### Denominational Sensitivity

While maintaining orthodox boundaries, allow for legitimate denominational differences. Focus on:
- Is it within historic Christian orthodoxy?
- Is it a salvation issue or a secondary matter?
- Does it violate essential doctrine or just preference?

## Common Mistakes and Examples

For detailed examples of errors and how to address them, read:
- `references/examples.md` - Concrete examples of scripture, language, context, and theological errors
- `references/common-mistakes.md` - Comprehensive guide to interpretive fallacies to avoid

**Quick reference of common mistakes**:
1. **Proof-texting**: Using verses without context
2. **Root fallacy**: Assuming etymology determines meaning  
3. **Illegitimate totality transfer**: Loading all word meanings into one usage
4. **One-meaning fallacy**: Assuming words always mean the same thing
5. **Concordance abuse**: Relying on Strong's without understanding grammar
6. **Genre confusion**: Reading poetry as prose or vice versa
7. **Eisegesis**: Reading modern ideas into the text
8. **Cultural imperialism**: Ignoring ancient Near Eastern context

## Quality Checklist

Before completing a review, verify:

- [ ] All scripture references checked for accuracy
- [ ] All quotes verified against biblical text
- [ ] Context examined for all cited passages
- [ ] Key Greek/Hebrew words analyzed
- [ ] Theological claims evaluated against orthodoxy
- [ ] Interpretation methods assessed
- [ ] Severity level assigned
- [ ] Clear recommendations provided
- [ ] Examples or corrections given where needed

## Advanced Features

### Parallel Passage Analysis

When reviewing, check parallel passages:
- Gospel parallels (Matthew/Mark/Luke/John accounts)
- Paul's letters (similar themes across epistles)
- Historical books (1-2 Samuel, 1-2 Kings, 1-2 Chronicles)

Note any harmonization issues or complementary details.

### Systematic Theology Check

Cross-reference the topic across Scripture:
- What does the whole Bible say about this?
- Are there counterbalancing passages?
- How do scholars typically handle tensions?

### Citation Chain Verification

When content cites "scholar X says passage Y means Z":
- Is the scholar properly cited?
- Is the passage accurately represented?
- Is the interpretation mainstream or fringe?

## Limitations

**Be transparent about:**
- Textual variants (differences in ancient manuscripts)
- Scholarly debate on difficult passages
- Translation challenges (Hebrew/Greek words with no English equivalent)
- Cultural gaps in understanding ancient context

Don't claim certainty where legitimate scholarly disagreement exists.

## Final Notes

**Approach**: Be thorough but gracious. The goal is accuracy, not criticism.

**Tone**: Correct errors clearly while respecting the author's effort.

**Emphasis**: Focus on what matters most (doctrine, accuracy) over minor stylistic preferences.

**Outcome**: Help create biblically faithful content that honors God's Word and serves readers well.
