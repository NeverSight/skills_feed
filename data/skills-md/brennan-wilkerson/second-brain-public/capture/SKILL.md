---
name: capture
description: Parse and structure information from screenshots, meeting notes, or text, then save to Second Brain Supabase database. Extracts contacts, tasks, and ideas automatically. Use when user wants to save information for later.
---

# Capture Skill

## Purpose
Parse and structure information from screen captures, meeting notes, conversations, or any text input, then store it in the Second Brain Supabase database.

## When Claude Should Use This
- User provides a screenshot with information to save
- User pastes meeting notes or conversation transcript
- User describes something they want to remember
- User shares ideas, tasks, or contact information
- User says "save this", "capture this", "remember this"

## How It Works

### Step 1: Receive Input
Accept any of:
- Screenshot description or OCR text
- Pasted text (emails, notes, messages)
- Verbal description of information
- Mixed content (text + context)

### Step 2: Intelligent Parsing
Analyze the content and extract:

**Contacts (people mentioned)** - Extract rich, structured information:

**Name Fields:**
- first_name, last_name, middle_name (parse from full name)
- preferred_name (nicknames, how they like to be addressed)
- prefix (Mr., Mrs., Dr., Prof.)
- suffix (Jr., Sr., PhD, MD, III)

**Contact Methods:**
- primary_email, secondary_email (validate format)
- primary_phone + country_code + type (mobile/work/home)
- secondary_phone + country_code + type

**Location:**
- city, state_province, country
- timezone (ALWAYS infer from location + country if possible; e.g., San Francisco → America/Los_Angeles, London → Europe/London, Sydney → Australia/Sydney)
- address (if provided)

**LLM-Driven Enrichment (Automatic via MCP, But Provide Good Context):**
- **Country Inference from Phone Code**: If phone has +56 but no country → Will infer "Chile"; if +44 → "United Kingdom"; if +1 → "USA". **Action**: Always include country code in phone numbers
- **Timezone Inference from City+Country**: Santiago+Chile → America/Santiago; Tokyo+Japan → Asia/Tokyo; London+UK → Europe/London. **Action**: Include both city AND country for accurate timezone
- **Industry Inference from Context**: From company name, title, or keywords like "SaaS", "biotech", "fintech", "finance", "healthcare", "tech", "real estate", "manufacturing"
- **Company Size Inference from Context**: Keywords like "startup", "Series A/B/C", "Fortune 500", "enterprise", "5000+ employees"
- **Seniority Inference from Title**: CEO/CTO/CFO → C-Level; Director/VP → Executive; Manager/Senior → Mid/Senior; Engineer/Analyst → Entry

**Professional:**
- company, title, department
- industry (tech, finance, healthcare, etc.) - Will be inferred from company/title if not explicitly stated
- seniority_level (Entry, Mid, Senior, Executive, C-Level) - Will be inferred from title if not explicitly stated
- company_size (Startup, Small, Medium, Enterprise) - Will be inferred from context if not explicitly stated

**Social/Online:**
- linkedin_url (validate LinkedIn format)
- twitter_handle, github_username, website

**Relationship Context:**
- persona: client/prospect/vendor/partner/colleague/friend/family
- relationship_strength: cold/warm/hot/champion
- how_we_met (conference, intro from X, school, etc.)
- referral_source (who introduced you)
- interests[], skills[] (array of relevant tags)

**Tasks (action items)**
- What needs to be done
- Priority (urgent, high, medium, low)
- Due date (if mentioned)
- Who it's for/related to
- Category (work, personal, follow-up, etc.)

**Ideas (insights, notes, thoughts)**
- Main concept or insight
- Supporting details
- Category (business, technical, personal, creative)
- Related contacts or projects
- Tags for organization

**Opportunities (job leads, partnerships, investments, etc.)**
- Organization and role/description
- Status (identified, researching, applied, in_progress, etc.)
- Category (full_time, contract, consulting, advisory, investment, partnership, grant, etc.)
- Deadline and urgency
- Location (region, country, city, remote options)
- Compensation (salary range, equity, benefits)
- Scoring:
  - Strategic value (0-10 + weight)
  - Personal fit (0-10 + weight)
  - Feasibility (0-10 + weight)
  - Trusted peer score
- Network mapping:
  - Primary contacts (1st degree connections)
  - Secondary contacts (2nd degree)
  - Relevant networks
- Assessment: "Can I realistically get this?"
- Priority: Critical, High, Medium, Low
- Context: Why interested, concerns, next steps

**Raw Capture**
- Always save the complete original content
- Note the source type (screenshot, text, voice, etc.)
- Timestamp automatically

### Step 3: Store in Supabase

Use the Supabase MCP to store data in appropriate tables:

1. **captured_items table** (always first)
   ```
   - raw_content: Full original text
   - content_type: 'text', 'screenshot', 'voice', 'paste'
   - source: 'claude_desktop'
   - status: 'processing'
   ```

2. **contacts table** (if people identified)
   ```
   ALWAYS check for duplicates first (search by email or full name)

   Name fields:
   - first_name, last_name, middle_name (parsed)
   - preferred_name, prefix, suffix

   Contact methods:
   - primary_email (required if available)
   - primary_phone, primary_phone_country_code, primary_phone_type
   - secondary_email, secondary_phone (if mentioned)

   Location:
   - city, state_province, country (USE CLAUDE'S REASONING TO INFER)
   - timezone (ALWAYS INFER from location + country; see enrichment section above)

   Professional:
   - company, title, department
   - industry (USE CLAUDE'S REASONING: infer from context; e.g., "works at VC firm" → finance, "biotech startup" → healthcare)
   - seniority_level (USE CLAUDE'S REASONING: infer from title; CEO/CTO/CFO → C-Level, Director/VP → Executive)
   - company_size (USE CLAUDE'S REASONING: infer from context; startup, Series A, Fortune 500 → Enterprise)

   Social:
   - linkedin_url, twitter_handle, github_username, website

   Relationship:
   - persona (client/prospect/vendor/partner/colleague/friend/family)
   - relationship_strength (cold/warm/hot/champion based on context)
   - contact_status (default: 'active')
   - how_we_met, referral_source
   - interests[] (e.g., ['AI', 'photography', 'hiking'])
   - skills[] (e.g., ['Python', 'leadership', 'design'])

   Tracking:
   - first_contact_date (today if new contact)
   - next_followup_date (if mentioned in capture)

   Context:
   - notes: Free-form context from capture
   - metadata: {source: 'linkedin', source_capture_id: ...}

   ENRICHMENT BEST PRACTICES:
   - If phone has +56, infer country: Chile
   - If phone has +44, infer country: United Kingdom
   - If city: "Santiago", infer country: Chile, timezone: America/Santiago
   - If no country stated but phone + country_code present, always fill in country field
   - Use your reasoning to fill in seniority_level, industry, company_size from available context
   ```

3. **tasks table** (if action items found)
   ```
   - title: Brief description of task
   - description: Full details
   - priority: Based on urgency cues
   - status: 'pending'
   - due_date: Parse from text if present
   - source_capture_id: Link to captured_item
   ```

4. **ideas table** (if insights/notes present)
   ```
   - title: Main concept
   - content: Full details
   - category: Inferred from context
   - tags: Array of relevant keywords
   - source_capture_id: Link to captured_item
   ```

5. **opportunities table** (if job/opportunity mentioned)
   ```
   Basic Info:
   - organization: Company/org name
   - role: Job title or opportunity description
   - status: identified/researching/preparing/applied/in_progress/negotiating/accepted/declined/rejected
   - category: full_time/contract/consulting/advisory/investment/partnership/grant/fellowship/speaking
   - deadline: Application/decision deadline

   Location:
   - region, country, city
   - remote_option: "Fully Remote"/"Hybrid"/"On-site"/"Remote-friendly"

   Compensation:
   - salary_min, salary_max, salary_currency
   - equity_offered (boolean), equity_range
   - other_compensation

   Scoring (0-10 scale with weights 0-1):
   - strategic_value_score, strategic_value_weight
   - personal_fit_score, personal_fit_weight
   - feasibility_score, feasibility_weight
   - weighted_score (auto-calculated)
   - trusted_peer_score

   Assessment:
   - realistic_assessment: "Can I realistically get this?"
   - priority: Critical/High/Medium/Low (infer or ask)

   Network:
   - relevant_networks: ['YC Alumni', 'MIT Network', etc.]
   - primary_contacts: [contact_id array] - people you know
   - secondary_contacts: [contact_id array] - 2nd degree
   - referral_contact_id: Who referred you

   Context:
   - description, requirements
   - why_interested, concerns, next_steps
   - source, source_url
   - tags, notes

   Link to opportunity_contacts table for each relevant contact
   ```

6. **Update captured_item**
   ```
   - status: 'completed'
   - processed_at: NOW()
   - processing_notes: Summary of what was extracted
   ```

### Step 4: Return Summary
Provide clear feedback:
```
✅ Captured and processed!

📝 Raw content: Saved
👤 Contacts: 2 identified (John Smith, Jane Doe)
✓ Tasks: 3 action items created
💡 Ideas: 1 note saved
🎯 Opportunities: 1 tracked (Anthropic PM role)
🔗 Everything linked together

View in Supabase: [captured_items table]
```

## Parsing Guidelines

### Contact Detection & Parsing

**Name Parsing:**
- Split full names intelligently: "Dr. Sarah Johnson Jr." → prefix: Dr., first: Sarah, last: Johnson, suffix: Jr.
- Handle formats: "LastName, FirstName", "FirstName MiddleName LastName"
- Detect prefixes: Mr., Mrs., Ms., Dr., Prof., Sir, Lady, Lord
- Detect suffixes: Jr., Sr., II, III, IV, PhD, MD, Esq.
- Extract preferred names from quotes: Sarah "Sally" Johnson → preferred_name: Sally

**Contact Method Extraction:**
- Email patterns: name@domain.com (validate format)
- Phone: (555) 123-4567, +1-555-123-4567, 555.123.4567
- Country codes: +1 (US/Canada), +44 (UK), +91 (India), etc.
- Phone type hints: "mobile", "cell", "work phone", "office", "home"

**Professional Data Inference:**
- Titles: CEO, CTO, Director, Manager, Engineer, Designer, Consultant
- Seniority from title: CEO/CTO/CFO → C-Level, Director/VP → Executive, Manager → Mid/Senior
- Industry keywords: tech, finance, healthcare, education, retail, manufacturing
- Company size hints: "startup" → Startup, "enterprise" → Enterprise, Fortune 500 → Enterprise

**Location Parsing:**
- City, State patterns: "San Francisco, CA", "NYC", "London, UK"
- Full addresses: Extract street, city, state, postal code
- Timezone inference: San Francisco → America/Los_Angeles, London → Europe/London

**Social Media Detection:**
- LinkedIn: https://linkedin.com/in/username or "LinkedIn: username"
- Twitter: @username or twitter.com/username
- GitHub: github.com/username or "GitHub: username"
- Website: http(s)://domain.com

**Relationship Context:**
- Persona inference (Life Segmentation):
  - "mom", "dad", "sister", "brother", "aunt", "uncle", "cousin" → family
  - "best friend", "close friend", "longtime friend" → close_friend
  - "friend", "buddy" → friend
  - "acquaintance", "met once", "just met" → acquaintance
  - Business/work context → professional

- Organization Type (for professional contacts):
  - "VC", "venture capital", "investor" → vc
  - "corporate VC", "strategic investor" → cvc
  - "startup", "founded", "co-founder" → startup
  - "incubator" → incubator
  - "accelerator", "Y Combinator", "Techstars" → accelerator
  - "foundation", "grant maker" → foundation
  - "non-profit", "nonprofit", "NGO" → non_profit
  - "social enterprise", "social impact startup" → social_startup
  - "Fortune 500", "large company" → corporate
  - "university", "professor", "research" → academic
  - "government", "public sector" → government

- Relationship strength:
  - "just met", "new contact" → cold
  - "spoke a few times", "getting to know" → warm
  - "working closely", "regular meetings" → hot
  - "advocate", "champion", "referred X people" → champion

- How we met: Extract from phrases like:
  - "met at TechConf 2025"
  - "introduced by Sarah"
  - "college roommate"
  - "found on LinkedIn"

### Task Detection
Keywords indicating action:
- "need to", "should", "must", "remember to"
- "follow up with", "reach out to"
- "by [date]", "before [day]"
- Questions requiring action
- Items with checkboxes or bullets

Priority indicators:
- **Urgent**: ASAP, urgent, critical, today, immediately
- **High**: important, soon, this week
- **Medium**: should, when possible
- **Low**: eventually, someday, nice to have

### Idea Detection
Patterns suggesting notes/insights:
- "I think", "What if", "Maybe we could"
- Observations, reflections, hypotheses
- Learnings, takeaways, insights
- Questions for later exploration
- References to articles, books, resources

### Opportunity Detection
Keywords and patterns indicating opportunities:
- "job opening", "position", "role", "hiring", "opportunity"
- "application deadline", "apply by", "due date"
- "partnership opportunity", "collaboration", "grant"
- "looking for", "seeking", "recruiting"
- Company name + role title combination
- Salary/compensation mentions
- "remote", "hybrid", "onsite"

**Status inference from context:**
- "just found", "came across", "saw posting" → identified
- "looking into", "researching", "considering" → researching
- "working on application", "preparing materials" → preparing
- "submitted", "applied" → applied
- "interview scheduled", "in process" → in_progress
- "offer received", "negotiating" → negotiating

**Category inference:**
- "full-time", "FTE", "permanent position" → full_time
- "contract", "contractor", "freelance" → contract
- "consulting", "consultant" → consulting
- "advisor", "advisory board" → advisory
- "investment opportunity", "raise", "funding" → investment
- "partnership", "collaborate", "joint venture" → partnership
- "grant", "funding opportunity", "RFP" → grant
- "fellowship", "residency" → fellowship
- "speaking", "keynote", "panel" → speaking

**Priority inference:**
- Deadline within 7 days + strong fit → Critical
- Strong network + good fit → High
- Some network or good deadline → Medium
- Weak network + far deadline → Low

**Network mapping:**
- Look for names mentioned → check if they exist in contacts
- "I know [name]" → primary_contacts
- "[Name] knows someone there" → secondary_contacts
- "Through [network name]" → relevant_networks

**Scoring guidance:**
- Strategic value: Career trajectory, skills gained, long-term impact
- Personal fit: Alignment with interests, work style, values
- Feasibility: Qualifications match, realistic chance, timeline
- Weights: Usually equal (0.33 each) unless user specifies

### Category Inference
- **Work/Business**: meetings, clients, projects, professional contexts
- **Personal**: family, friends, hobbies, health
- **Technical**: code, systems, tools, development
- **Creative**: design, art, writing, innovation
- **Learning**: courses, books, research, study

## Error Handling

If parsing unclear:
1. Save to captured_items with status='pending'
2. Ask user for clarification
3. Don't guess - it's better to ask

If duplicate contact found:
1. Ask if it's the same person
2. Offer to update existing or create new
3. Merge information if user confirms

If Supabase error:
1. Show the error clearly
2. Save content locally/clipboard as backup
3. Suggest manual retry

## Examples

### Example 1: Meeting Notes
**Input:**
```
Met with Sarah Johnson (sarah@techcorp.com) today. She's the new CTO at TechCorp, a Series B startup in San Francisco.
Mobile: +1-415-555-0123. Her LinkedIn: linkedin.com/in/sarahjohnson
Need to send her the proposal by Friday. Really liked her idea about using AI for customer support.
Follow up next Tuesday to discuss budget. She mentioned she's interested in AI and cycling.
```

**Processing:**
- Contact:
  - Name: first_name: Sarah, last_name: Johnson
  - Email: primary_email: sarah@techcorp.com
  - Phone: primary_phone: 415-555-0123, country_code: +1, type: mobile
  - Company: TechCorp, title: CTO, company_size: Startup, industry: tech
  - Location: city: San Francisco, state: CA, country: USA, timezone: America/Los_Angeles
  - Social: linkedin_url: https://linkedin.com/in/sarahjohnson
  - Relationship: persona: client, relationship_strength: warm, how_we_met: "Business meeting"
  - Interests: ['AI', 'cycling']
  - Seniority: C-Level
- Tasks:
  - Send proposal to Sarah (due: Friday, priority: high, related_contact: Sarah Johnson)
  - Follow up with Sarah about budget (due: Tuesday, priority: medium)
- Ideas: "AI for customer support" (category: business, tags: [AI, customer service, TechCorp])
- Raw: Full text saved to captured_items with all relationships linked

### Example 2: Quick Note
**Input:**
```
Idea: Build a browser extension that automatically saves interesting articles to my Second Brain
```

**Processing:**
- Ideas: Browser extension for article saving (category: technical, tags: [browser, extension, automation])
- Raw: Saved to captured_items
- Tasks: None detected (idea, not action item)
- Contacts: None

### Example 3: Screenshot (User describes)
**Input:**
```
This is a screenshot of my phone showing text messages with:
- Mom asking about dinner Sunday at 6pm
- Boss saying the Q4 report needs review
- Gym reminder for tomorrow 7am
```

**Processing:**
- Tasks:
  - Dinner with mom (Sunday 6pm, personal, priority: medium)
  - Review Q4 report (work, priority: high)
  - Gym session (tomorrow 7am, personal/health, priority: medium)
- Contacts: Mom, Boss (if not already in database)
- Raw: Full description saved

### Example 4: LinkedIn Connection (Enhanced Parsing)
**Input:**
```
Just connected with Dr. Michael Chen on LinkedIn. He's a Senior Engineering Manager at Microsoft in Seattle.
His profile says he's passionate about distributed systems and machine learning.
Went to Stanford for his PhD. We were introduced by Jennifer Lee from AWS.
Should reach out next week to discuss potential collaboration.
LinkedIn: linkedin.com/in/michaelchen-phd
```

**Processing:**
- Contact:
  - Name: prefix: Dr., first_name: Michael, last_name: Chen, suffix: PhD
  - Company: Microsoft, title: Senior Engineering Manager, department: Engineering
  - Seniority: Senior, company_size: Enterprise, industry: tech
  - Location: city: Seattle, state: WA, country: USA, timezone: America/Los_Angeles
  - Social: linkedin_url: https://linkedin.com/in/michaelchen-phd
  - Relationship: persona: colleague, relationship_strength: cold, referral_source: Jennifer Lee (AWS)
  - How_we_met: "Introduced by Jennifer Lee on LinkedIn"
  - Skills: ['distributed systems', 'machine learning']
  - First_contact_date: today
  - Next_followup_date: next week
- Tasks:
  - Reach out to Dr. Chen about collaboration (due: next week, priority: medium, related_contact: Michael Chen)
- Raw: Full message saved with source: linkedin

### Example 5: Opportunity Tracking
**Input:**
```
Found a great opportunity at Anthropic - Product Manager role for AI Safety.
Application deadline: November 15th
Location: San Francisco (hybrid, 3 days/week in office)
Salary range: $180K-$220K + equity (0.1-0.3%)

I know Sarah Johnson who works there as CTO, and Michael Chen knows someone on the hiring team.
This aligns perfectly with my AI ethics background and product experience.

Strategic value: 9/10 - Dream company, cutting-edge AI work, mission-driven
Personal fit: 8/10 - Perfect match for my skills, values alignment
Feasibility: 7/10 - Strong qualifications, need to prepare case studies

Networks: YC Alumni (Sarah), ML Research Community (Michael's connection)
Action: Reach out to Sarah by end of week, submit application by Nov 10th
```

**Processing:**
- Opportunity:
  - organization: Anthropic
  - role: Product Manager - AI Safety
  - status: identified
  - category: full_time
  - deadline: November 15
  - days_until_deadline: [calculated]
  - region: North America
  - country: USA
  - city: San Francisco
  - remote_option: Hybrid (3 days/week in office)
  - salary_min: 180000, salary_max: 220000, salary_currency: USD
  - equity_offered: true, equity_range: 0.1-0.3%
  - strategic_value_score: 9, strategic_value_weight: 0.33
  - personal_fit_score: 8, personal_fit_weight: 0.33
  - feasibility_score: 7, feasibility_weight: 0.34
  - weighted_score: 8.0 (auto-calculated)
  - priority: High (strong score + reasonable deadline)
  - relevant_networks: ['YC Alumni', 'ML Research Community']
  - primary_contacts: [Sarah Johnson's contact_id]
  - secondary_contacts: [Michael Chen's contact_id]
  - why_interested: "Dream company, cutting-edge AI work, mission-driven"
  - next_steps: "Reach out to Sarah by end of week, submit application by Nov 10"
  - tags: ['AI', 'product management', 'AI safety', 'Anthropic']

- Contacts (link to opportunity via opportunity_contacts table):
  - Sarah Johnson (relationship_type: 'inside_contact', can_refer: true)
  - Michael Chen (relationship_type: '2nd_degree')

- Tasks:
  - Reach out to Sarah Johnson about Anthropic opportunity (due: end of week, priority: high)
  - Submit application to Anthropic (due: Nov 10, priority: critical)
  - Prepare case studies for Anthropic application (due: Nov 9, priority: high)

- Raw: Full capture saved with source_url if provided

## Best Practices

1. **Always save raw content first** - Never lose the original
2. **Be conservative with parsing** - When in doubt, ask user
3. **Link everything** - Use source_capture_id to maintain relationships
4. **Provide clear feedback** - User should know exactly what was saved
5. **Handle duplicates gracefully** - Check before creating new contacts
6. **Preserve context** - Include where/when/how information was captured
7. **Use tags liberally** - Better to have more tags than fewer
8. **Infer relationships** - Connect tasks to contacts when relevant

## Security Notes

- Never store sensitive data like passwords or API keys
- Warn user if SSN, credit card numbers detected
- Ask before storing financial or health information
- Respect user privacy - all data is user-owned

## Future Enhancements (Not Yet Implemented)

- Voice transcription support
- Image OCR for screenshots
- Smart scheduling (Google Calendar integration)
- Duplicate detection with similarity matching
- Auto-categorization using AI models
- Relationship mapping between entities
