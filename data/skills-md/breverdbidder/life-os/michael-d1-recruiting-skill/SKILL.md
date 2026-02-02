---
name: michael-d1-recruiting-skill
description: D1 swimming recruiting workflows including coach outreach, program research, SwimCloud tracking, and timeline management
---

# Michael D1 Recruiting Skill

Manages Michael Shapira's D1 swimming recruiting process with coach outreach, program research, and timeline tracking.

## When to Use This Skill

- Researching D1 swimming programs
- Drafting coach outreach emails
- Tracking recruiting timelines
- Analyzing competition (SwimCloud rivals)
- Logging recruiting activities to Supabase

## Michael's Profile

**Name:** Michael Shapira  
**DOB:** July 22, 2009 (16 years old)  
**School:** Satellite Beach High School, Class of 2027  
**SwimCloud ID:** 3250085

**Primary Events:**
- 50 Free
- 100 Free
- 200 Free
- 100 Fly
- 100 Back

**Current Times (verify via SwimCloud):**
- Check latest meet results
- Track improvement trends
- Compare to recruiting standards

**Diet:** Kosher-adapted keto (Mon-Thu), moderate carbs (Fri-Sun for Shabbat)  
**Model:** Following Michael Andrew's nutrition approach

## Verified Rivals (SwimCloud IDs)

**Key Competitors:**
1. **Soto** (ID: 2928537) - PI 47
2. **Gordon** (ID: 1733035) - PI 90  
3. **Domboru** (ID: 1518102)

**Data Location:** `/life-os/michael_d1_agents_v3/data/`

## Coach Outreach Templates

### Initial Contact Template

```
Subject: Satellite Beach HS 2027 | 50/100/200 Free | [Time]

Coach [Last Name],

My name is Michael Shapira, and I'm a junior at Satellite Beach High School 
in Florida (Class of 2027). I'm reaching out to express my strong interest in 
[University Name]'s swimming program.

Current Times:
- 50 Free: [time]
- 100 Free: [time]
- 200 Free: [time]
- 100 Fly: [time]

I'm particularly drawn to [University] because of [specific reason - academic 
program, team culture, coaching philosophy, etc.].

My SwimCloud profile: https://www.swimcloud.com/swimmer/3250085/

I'd welcome the opportunity to discuss how I could contribute to the [Team Name]. 
Are you available for a brief call in the coming weeks?

Best regards,
Michael Shapira
Satellite Beach High School '27
Email: [email]
Phone: [phone]
```

### Follow-Up Template

```
Subject: Re: Satellite Beach HS 2027 | Following Up

Coach [Last Name],

I wanted to follow up on my email from [date] regarding my interest in 
[University]'s program. 

Recent Update:
- [Recent meet/time drop/achievement]
- [Any relevant news]

I remain very interested in [University] and would appreciate any guidance 
on your recruiting timeline and how I can stay on your radar.

Best,
Michael Shapira
```

### Post-Meet Update Template

```
Subject: Time Update | [Event] [New Time]

Coach [Last Name],

Quick update from [Meet Name]:
- [Event]: [New Time] ([improvement from previous])

[Brief 1-2 sentence context if relevant]

Looking forward to staying in touch as the recruiting process continues.

Best,
Michael Shapira
```

## Program Research Workflow

### Target Program Criteria

**Academic:**
- Strong [Michael's intended major] program
- Academic support for student-athletes
- Graduation rates

**Athletic:**
- Conference strength
- Recruiting times alignment
- Team culture/coaching philosophy
- Facility quality

**Practical:**
- Location (proximity to family)
- Campus environment
- Kosher food options (important!)
- Jewish student life (if relevant)

### Research Template

```json
{
  "university": "University of Florida",
  "conference": "SEC",
  "coach_name": "Anthony Nesty",
  "recruiting_times": {
    "50_free": "20.50",
    "100_free": "44.50",
    "200_free": "1:36.00"
  },
  "team_culture": "High-performance, sprint-focused",
  "academic_fit": "Strong engineering program",
  "distance_from_home": "2.5 hours",
  "kosher_options": "Hillel on campus, kosher meal plan available",
  "notes": "Strong sprint tradition, recent NCAA success"
}
```

## Recruiting Timeline

### Sophomore Year (2025-2026)
- ✓ Build relationship with current coach
- ✓ Attend recruiting camps/clinics
- ✓ Initial coach outreach to target schools
- ✓ Focus on time drops

### Junior Year (2026-2027) - CURRENT
- **Fall:** Verbal commitment window opens
- **Winter:** Continue coach contact, visit schools
- **Spring:** Key championship meets for times
- **Summer:** Final time trials before senior year

### Senior Year (2027-2028)
- **Fall:** Sign National Letter of Intent (November)
- **Spring:** Final high school season
- **Summer:** Prepare for college transition

## SwimCloud Integration

### Tracking Competitors

```python
# Check rival progress
rivals = [
    {'name': 'Soto', 'id': 2928537, 'pi': 47},
    {'name': 'Gordon', 'id': 1733035, 'pi': 90},
    {'name': 'Domboru', 'id': 1518102}
]

for rival in rivals:
    # Get latest times from SwimCloud
    # Compare to Michael's times
    # Track improvement trends
```

### Meet Results Logging

After each meet, log:
- Event, time, place
- Improvement from previous
- National/conference ranking
- Notify coaches of significant drops

## Supabase Logging

Log recruiting activities:

```python
supabase.table('activities').insert({
    'category': 'michael_swim',
    'subcategory': 'recruiting',
    'title': f"Coach Outreach: {university}",
    'content': json.dumps({
        'coach_name': coach_name,
        'university': university,
        'date_sent': datetime.now(),
        'type': 'initial_contact',
        'follow_up_date': datetime.now() + timedelta(days=14)
    })
})
```

## Key Considerations

### Shabbat Observance
**CRITICAL:** No swimming competitions Friday night through Saturday havdalah

When researching programs:
- Ask about meet schedules
- Confirm Shabbat accommodation
- Look for precedent (other observant swimmers)

### Kosher Diet Maintenance
- Verify campus dining options
- Check proximity to kosher restaurants
- Hillel/Chabad presence on campus

### Academic Balance
- Engineering/science program strength
- Athletic academic support
- Summer training vs internship flexibility

## Target Program Tiers

### Tier 1 (Reach)
- Top 10 programs nationally
- Very competitive recruiting times
- Example: Florida, Texas, Cal

### Tier 2 (Target)
- Top 25 programs
- Times align with current trajectory
- Example: Florida State, NC State, Louisville

### Tier 3 (Safety)
- Strong programs, achievable times
- Great academic fit
- Example: [Specific schools based on current times]

## Example Usage

```
"Use michael-d1-recruiting-skill to draft outreach email to UF coach"

"Research D1 programs with strong engineering and kosher options"

"Log meet results and generate coach update emails"
```

## Next Key Dates

**Harry Meisel Meet:** December 13-14, 2025  
**Recruiting Priority:** Junior year = critical time for commitments  
**Action Items:** 
- Update times after each meet
- Monthly coach touchpoints
- Visit top 3 schools by spring 2026

## Critical Reminders

1. **Shabbat First:** No compromises on Friday night/Saturday meets
2. **Academic Priority:** D1 swimming supports education, not replaces it
3. **Honest Assessment:** Target schools matching realistic progression
4. **Coach Relationships:** Quality over quantity in outreach
5. **Family Input:** Ariel and Mariam involved in all decisions
