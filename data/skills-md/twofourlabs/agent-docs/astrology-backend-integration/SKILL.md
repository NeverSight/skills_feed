---
name: astrology-backend-integration
description: This skill provides a comprehensive approach for building astrology-specific backend systems with AI integration. Use when implementing vedic astrology features including kundli generation, dasha analysis, dosha detection, and astrological predictions. Builds on the ai-integrated-api-backend skill with astrology domain expertise.
license: Complete terms in LICENSE.txt
related_skills: ai-integrated-api-backend
---

This skill guides the implementation of vedic astrology backends that integrate astrology APIs with AI/LLM systems for predictions and consultations. It captures domain-specific patterns, data structures, and best practices for astrology applications.

## When to Use This Skill

Apply this skill when you need to:
- Build vedic astrology consultation platforms
- Integrate astrology APIs (AstrologyAPI.com, Prokerala, etc.)
- Generate and store kundlis (birth charts)
- Implement dasha-based predictions
- Detect doshas (Manglik, Pitra, etc.)
- Provide gemstone/rudraksha recommendations
- Create AI-powered astrology consultants
- Support family/member chart management
- Build compatibility/matching systems

## Prerequisites

Before using this skill, you should have:
- Completed the `ai-integrated-api-backend` skill (or understand external API + AI integration)
- Basic understanding of vedic astrology concepts
- Access to an astrology API provider

## Astrology Domain Fundamentals

### Core Concepts

**Kundli (Birth Chart)**
- Complete astrological profile of a person
- Requires: Date, Time, Location (lat/long) of birth
- Timezone: Critical for accuracy (default IST = 5.5 for India)
- Components: Charts, planets, dasha, doshas, remedies

**Charts (Divisional Charts)**
- **D1 (Rashi Chart)**: Main birth chart, 12 houses
- **D9 (Navamsa)**: Marriage and spiritual chart
- Other divisional charts (D10, D60, etc.) for specific life areas

**Houses (Bhava)**
- 12 houses representing life domains
- Critical mappings:
  - House 1: Self, health, personality
  - House 2: Wealth, family, speech
  - House 4: Mother, property, happiness
  - House 5: Children, education, creativity
  - House 7: Marriage, partnerships
  - House 10: Career, reputation, father
  - House 11: Gains, friends, aspirations
  - House 12: Losses, spirituality, foreign lands

**Planets (Grahas)**
- 9 planets in vedic astrology:
  - Sun (Surya): Authority, self, ego
  - Moon (Chandra): Mind, emotions, mother
  - Mars (Mangal): Energy, courage, conflicts
  - Mercury (Budha): Communication, intellect
  - Jupiter (Guru): Wisdom, expansion, luck
  - Venus (Shukra): Love, relationships, luxury
  - Saturn (Shani): Discipline, karma, delays
  - Rahu: Desires, obsessions, foreign
  - Ketu: Detachment, spirituality, past life

**Sign Lords (Zodiac Rulers)**
- Each zodiac sign is ruled by a planet:
  - Aries → Mars
  - Taurus → Venus
  - Gemini → Mercury
  - Cancer → Moon
  - Leo → Sun
  - Virgo → Mercury
  - Libra → Venus
  - Scorpio → Mars
  - Sagittarius → Jupiter
  - Capricorn → Saturn
  - Aquarius → Saturn
  - Pisces → Jupiter

**Dasha (Planetary Periods)**
- Vimshottari Dasha: 120-year cycle
- Structure: Major (Mahadasha) → Minor (Antardasha) → Sub-minor (Pratyantar)
- Each planet rules for specific years
- Critical for timing predictions: "When will X happen?"

**Doshas (Afflictions)**
- **Manglik Dosha**: Mars in specific houses (1, 2, 4, 7, 8, 12)
  - Affects marriage compatibility
  - Measured as percentage (0-100%)
  - Cancellations exist (e.g., both partners Manglik)
- **Pitra Dosha**: Ancestral debt
  - Sun/Moon afflicted by Rahu/Ketu
  - Remedies: Puja, charity

**Remedies**
- **Gemstones**: Strengthen weak planets
  - Each planet has a gemstone (Ruby for Sun, Pearl for Moon, etc.)
  - Worn on specific finger, day, metal
  - Weight in carats specified
- **Rudraksha**: Beads for spiritual remedies
  - Different mukhi (faces) for different planets
  - Worn for protection and balance
- **Puja/Mantras**: Ritual remedies

## Astrology API Integration Pattern

### Step 1: Choose Astrology API Provider

**Popular Options**:
- AstrologyAPI.com (https://json.astrologyapi.com/)
- Prokerala API
- GeoVedic API
- AstroSage API

**Common Features Needed**:
- Birth chart generation (D1, D9)
- Planetary positions with nakshatra
- Vimshottari Dasha
- Dosha analysis (Manglik, Pitra, Kaal Sarp, etc.)
- Gemstone/Rudraksha suggestions
- Panchang (daily calendar)
- Compatibility/matching

### Step 2: API Endpoint Mapping

**Essential Endpoints** (AstrologyAPI.com example):

```
Base URL: https://json.astrologyapi.com/

1. POST /v1/horo_chart/{chart_id}
   - Get D1 (chart_id=D1), D9 (chart_id=D9), etc.
   - Returns: List of 12 houses with sign and planets

2. POST /v1/planets
   - Get detailed planetary positions
   - Returns: Planet positions, retrograde status, nakshatra, longitude

3. POST /v1/astro_details
   - Get basic astrological details
   - Returns: Ascendant, rasi, nakshatra, etc.

4. POST /v1/current_vdasha
   - Get current dasha period
   - Returns: Major, minor, sub-minor planet and dates

5. POST /v1/current_vdasha_all
   - Get complete dasha timeline
   - Returns: All major/minor/sub-minor periods from birth to 120 years

6. POST /v1/manglik
   - Check Manglik dosha
   - Returns: Manglik status, percentage, explanation

7. POST /v1/pitra_dosha_report
   - Check Pitra dosha
   - Returns: Present/absent, explanation

8. POST /v1/basic_gem_suggestion
   - Get gemstone recommendation
   - Returns: Gemstone, metal, finger, day, deity, mantra, carat weight

9. POST /v1/rudraksha_suggestion
   - Get Rudraksha recommendation
   - Returns: Mukhi number, ruling planet, benefits

10. POST /v1/puja_suggestion
    - Get puja recommendations
    - Returns: Puja type, purpose, timing
```

### Step 3: Base Payload Structure

**Standard Birth Details Payload**:
```json
{
  "day": 15,           // Day of birth (1-31)
  "month": 6,          // Month (1-12)
  "year": 1990,        // Year (YYYY)
  "hour": 14,          // Hour in 24-hour format (0-23)
  "min": 30,           // Minute (0-59)
  "lat": 28.7041,      // Latitude (decimal)
  "lon": 77.1025,      // Longitude (decimal)
  "tzone": 5.5         // Timezone offset (5.5 for IST)
}
```

**Critical Considerations**:
- **Timezone**: MUST be accurate. Default IST = 5.5 for India
- **Time Format**: 24-hour format, NOT 12-hour AM/PM
- **Coordinates**: Use Google Maps Geocoding API or similar for accurate lat/long
- **Date Validation**: Ensure valid dates (no Feb 30, etc.)

### Step 4: API Manager Implementation

**Responsibilities**:
- Authenticate with API (usually HTTP Basic Auth or API Key)
- Build payloads from user birth details
- Call multiple endpoints (charts, dasha, dosha, remedies)
- Handle API rate limits and errors
- Return structured responses

**Key Pattern**:
```
API Manager Methods:
- get_horo_chart(birth_details, chart_id) → D1/D9 chart
- get_planets(birth_details) → Planet positions
- get_dasha(birth_details) → Current dasha
- get_dasha_all(birth_details) → Complete timeline
- get_manglik(birth_details) → Dosha status
- get_gem_suggestion(birth_details) → Remedies
```

**Parallel Fetching**:
- Most endpoints are independent
- Fetch in parallel using async tasks (Celery, etc.)
- Reduces total time from 9×3s = 27s to ~3s

## Data Storage Pattern

### Database Schema Design

**Collection 1: User Birth Details** (user_metadata)
```json
{
  "user_id": 12345,
  "dob_full_name": "John Doe",
  "dob_gender": "male",
  "dob_day": 15,
  "dob_month": 6,
  "dob_year": 1990,
  "dob_hour": 14,
  "dob_minute": 30,
  "dob_lat": 28.7041,
  "dob_long": 77.1025,
  "dob_city": "New Delhi",
  "dob_state": "Delhi",
  "created_on": "2024-01-15T10:00:00Z",
  "updated_on": "2024-01-15T10:00:00Z"
}
```

**Collection 2: Raw Astrology Data** (user_astro_metadata)
```json
{
  "user_id": 12345,
  "astro_details": { /* API response */ },
  "horo_d1_chart_data": { /* D1 chart response */ },
  "horo_d9_chart_data": { /* D9 chart response */ },
  "planet_chart_data": { /* Planets response */ },
  "current_vdasha": { /* Current dasha */ },
  "current_vdasha_all": { /* Complete dasha */ },
  "manglik": { /* Manglik dosha */ },
  "pitra_dosha_report": { /* Pitra dosha */ },
  "basic_gem_suggestion": { /* Gemstone */ },
  "rudraksha_suggestion": { /* Rudraksha */ },
  "created_on": "2024-01-15T10:05:00Z",
  "updated_on": "2024-01-15T10:05:00Z"
}
```

**Why Two Collections?**
- Birth details rarely change (immutable)
- Astrology data can be refreshed (dasha changes over time)
- Separation allows independent updates

### Family/Member Support

**Collection 3: Family Member Birth Details** (user_member_metadata)
```json
{
  "_id": "member_unique_id",
  "user_id": 12345,
  "relation": "spouse",
  "dob_full_name": "Jane Doe",
  "dob_gender": "female",
  "age": 32,
  "dob_day": 20,
  "dob_month": 8,
  "dob_year": 1992,
  // ... same birth detail fields
}
```

**Collection 4: Family Member Astrology Data** (user_member_astro_metadata)
```json
{
  "user_id": 12345,
  "member_id": "member_unique_id",
  // ... same astro data fields as user_astro_metadata
}
```

**Relation Types**:
- "self" (primary user)
- "spouse", "mother", "father"
- "son", "daughter", "child"
- "brother", "sister"
- Custom relations as needed

## Kundli Transformation Pattern

### Problem Statement

**Challenge**: API responses are nested, verbose, and use inconsistent key naming. Need to transform into clean, AI-friendly structure.

**Example API Response Issues**:
- Mixed case keys: "Sign", "sign", "SIGN"
- Verbose: "The person is 28.5% Manglik due to Mars in 7th house..."
- Nested deeply: houses → sign → planets → details
- String format: "Mars(Retrograde)" instead of structured data

### Solution: Multi-Step Transformation Pipeline

**Step 1: Normalize Keys**
- Convert all keys to lowercase
- Recursively process nested objects
- Standardize array structures

**Step 2: Transform Charts**
- Convert house list to dictionary (house number → details)
- Extract sign from each house
- Map sign to sign lord (Aries → Mars)
- Extract planets in each house

**Step 3: Enrich Planets**
- Parse planet strings: "Mars(Retrograde)" → {name: "Mars", isRetrograde: true}
- Add nakshatra, longitude, position
- Mark benefic/malefic status

**Step 4: Build Dasha Timeline**
- Parse date strings to ISO format
- Filter realistic window (e.g., 2010 to current_year + 25)
- Structure major → minor → sub-minor hierarchy

**Step 5: Extract Dosha Values**
- Reduce verbose reports to key values
- Manglik: Extract percentage only
- Pitra: Extract present/absent only

**Step 6: Format Remedies**
- Gemstone: Extract name, metal, finger, day, carat
- Rudraksha: Extract mukhi, planet, benefits

### Output: Complete Kundli Structure

```yaml
Relation with user: self

Birth Details:
  name: John Doe
  gender: male
  date_of_birth: 15 Jun 1990
  time_of_birth: 02:30 PM
  place_of_birth: New Delhi, Delhi

D1 Chart:
  House 1:
    sign: Aries
    sign_lord: Mars
    planets:
      - name: Sun
        isRetrograde: false
        nakshatra: Ashwini
        longitude: 65.23
      - name: Mercury
        isRetrograde: true
        nakshatra: Bharani
        longitude: 72.45
  House 2:
    sign: Taurus
    sign_lord: Venus
    planets: []
  # ... Houses 3-12

D9 Chart:
  # Same structure as D1

Dasha Timeline:
  - major_planet: Venus
    start_date: 2015-05-01
    end_date: 2035-05-01
    minor_periods:
      - planet: Venus
        start_date: 2015-05-01
        end_date: 2018-09-01
      - planet: Sun
        start_date: 2018-09-01
        end_date: 2019-09-01
      # ... more minor periods

Current Dasha:
  major: Venus
  minor: Moon
  sub_minor: Mars

Doshas:
  manglik_percentage: 28.5
  pitra_dosha_present: false

Remedies:
  gemstone:
    name: Diamond
    metal: Silver
    finger: Middle
    day: Friday
    carat: 2-3
  rudraksha:
    mukhi: 6
    ruling_planet: Venus
    benefits: "Harmony, love, relationships"
```

## AI Prompt Integration Pattern

### Context Assembly

**Components to Inject**:
1. Complete kundli (YAML format above)
2. Query-specific house mapping
3. Gender-aware interpretation rules
4. Current dasha for timing
5. Language preference (Hindi/English)

**System Prompt Structure**:
```
You are an expert Vedic astrologer with deep knowledge of:
- Planetary positions and aspects
- House significations
- Dasha timing predictions
- Dosha analysis and remedies

User's Complete Birth Chart:
<kundli>
[YAML kundli structure here]
</kundli>

Query Analysis Rules:
- Marriage questions → Focus on House 7, Venus, Jupiter
- Career questions → Focus on House 10, Saturn, Sun
- Finance questions → Focus on House 2, 11, Jupiter
- Health questions → Focus on House 1, 6, planets in these houses
- Children questions → Focus on House 5, Jupiter
- Property questions → Focus on House 4, Mars

Gender-Specific Rules:
- For females: Jupiter = husband, Venus = marriage
- For males: Venus = wife, Mars = passion

Timing Predictions:
- Use current dasha: [Major/Minor/Sub-minor]
- Consider transits for immediate events
- Dasha changes indicate life phase shifts

Response Format:
- Provide predictions based on chart analysis
- Cite specific planetary positions
- Mention relevant dasha periods
- Suggest remedies if doshas present
- Answer in [Hindi/English] as per user preference
```

### Query-Specific Context

**Marriage Query Example**:
```
Query: "When will I get married?"

Additional Context:
- House 7 analysis: [Sign, Lord, Planets]
- Venus position: [House, Sign, Strength]
- Jupiter position: [House, Sign, Strength]
- Current dasha: [Will marriage planet dasha start soon?]
- Manglik dosha: [If yes, mention in prediction]

Prediction Approach:
1. Check House 7 lord strength
2. Check Venus/Jupiter periods in dasha
3. Look for favorable transits
4. Consider dosha impacts
```

**Career Query Example**:
```
Query: "What career is best for me?"

Additional Context:
- House 10 analysis: [Sign, Lord, Planets]
- Sun position: [Authority, leadership]
- Saturn position: [Discipline, perseverance]
- Mercury position: [Communication, intellect]
- Strongest planet in chart: [Natural talent]

Prediction Approach:
1. Identify dominant planets
2. Map to career domains (Sun→govt, Mercury→business, etc.)
3. Check House 10 lord placement
4. Consider current dasha planet's signification
```

## Advanced Features

### Compatibility/Matching (Kundli Milan)

**Ashtakoot System** (8-point matching):
1. Varna (1 point): Spiritual compatibility
2. Vashya (2 points): Mutual attraction
3. Tara (3 points): Birth star compatibility
4. Yoni (4 points): Physical compatibility
5. Graha Maitri (5 points): Mental compatibility
6. Gana (6 points): Temperament
7. Bhakoot (7 points): Love and affection
8. Nadi (8 points): Health and progeny

**Total**: 36 points maximum
- 18-24: Average match
- 25-32: Good match
- 33-36: Excellent match

**Implementation**:
- Requires both kundlis
- Call matching API endpoint
- Display point breakdown
- Highlight manglik cancellation if both Manglik

### Panchang (Daily Calendar)

**Components**:
- Tithi (lunar day)
- Vara (weekday)
- Nakshatra (lunar mansion)
- Yoga (sun-moon combination)
- Karana (half-tithi)

**Use Cases**:
- Muhurat selection (auspicious timing)
- Festival dates
- Daily horoscope context

### Transit Predictions

**Current Planetary Positions**:
- Fetch current date planetary positions
- Compare with birth chart
- Identify aspects (conjunction, opposition, trine, square)
- Predict short-term events

## Implementation Checklist

### Phase 1: API Setup
- [ ] Choose astrology API provider
- [ ] Set up authentication credentials
- [ ] Test all required endpoints
- [ ] Map API responses to internal models
- [ ] Implement error handling for API failures

### Phase 2: Data Models
- [ ] Create birth details schema (user_metadata)
- [ ] Create astrology data schema (user_astro_metadata)
- [ ] Create member schemas for family support
- [ ] Add indexes (user_id, member_id)
- [ ] Plan data retention policy

### Phase 3: Kundli Builder
- [ ] Implement key normalization
- [ ] Transform charts (D1, D9)
- [ ] Enrich planet details
- [ ] Build dasha timeline
- [ ] Extract dosha values
- [ ] Format remedies
- [ ] Test with sample API responses

### Phase 4: AI Integration
- [ ] Design system prompt with kundli context
- [ ] Map query types to house focus
- [ ] Add gender-aware rules
- [ ] Include dasha in timing predictions
- [ ] Support Hindi/English responses
- [ ] Test predictions for accuracy

### Phase 5: Features
- [ ] User onboarding (birth details collection)
- [ ] Location autocomplete (Google Maps API)
- [ ] Kundli generation and display
- [ ] Family member management
- [ ] Compatibility matching
- [ ] Dosha detection and remedies
- [ ] Panchang integration
- [ ] Daily horoscope

### Phase 6: Optimization
- [ ] Cache kundli data (10-60 min TTL)
- [ ] Parallel API calls (async tasks)
- [ ] Compress large kundli context
- [ ] Monitor API usage and costs
- [ ] Implement rate limiting

### Phase 7: Quality Assurance
- [ ] Validate timezone accuracy
- [ ] Test edge cases (midnight births, DST)
- [ ] Verify dasha calculations
- [ ] Check dosha logic
- [ ] User acceptance testing with astrologers
- [ ] Multilingual testing

## Best Practices

### Accuracy First
1. **Timezone is Critical**: Always use accurate timezone offset
2. **Coordinates Matter**: Get precise lat/long from geocoding
3. **Time Format**: Use 24-hour format, validate AM/PM conversions
4. **Date Validation**: Check for valid dates, leap years

### Data Management
1. **Separate Birth Data from Astrology Data**: Birth details immutable, astro data refreshable
2. **Cache Wisely**: Kundli doesn't change often, cache for hours
3. **Version Kundli Format**: Add version field for future schema changes
4. **Audit Trail**: Log all kundli generations for debugging

### AI Prompt Engineering
1. **Structured Context**: Use YAML/XML tags for clear sections
2. **Query Classification**: Pre-process query to determine focus area
3. **Citation**: Instruct AI to cite planetary positions in answers
4. **Fallback**: Handle cases where chart doesn't support query

### User Experience
1. **Progressive Loading**: Show basic chart while detailed analysis loads
2. **Explanation**: Explain astrological terms in simple language
3. **Remedies**: Always provide actionable remedies
4. **Consent**: Privacy for sensitive birth data

## Common Pitfalls

1. **Wrong Timezone**: Results in completely different chart
2. **12-hour AM/PM Confusion**: 2:30 PM ≠ 14:30, causes 12-hour error
3. **Ignoring Retrograde**: Planetary retrograde changes interpretation
4. **Static Dasha**: Dasha changes over time, refresh periodically
5. **Oversimplified Predictions**: AI needs detailed context, not just sun sign
6. **Missing Gender Context**: Venus/Jupiter interpretation differs by gender
7. **Ignoring Dosha**: Manglik dosha critical for marriage predictions

## Framework Adaptations

### Django
- MongoDB for document storage
- Celery for async API calls
- Django cache for kundli caching
- REST API for frontend

### FastAPI
- Motor (async MongoDB driver)
- Background tasks or Celery
- Redis caching
- WebSocket for real-time predictions

### Node.js (Express)
- Mongoose for MongoDB
- Bull for job queue
- Redis caching
- Socket.io for real-time

### Spring Boot
- Spring Data MongoDB
- Spring Async or RabbitMQ
- Spring Cache
- WebFlux for reactive

## Related Resources

- **Vedic Astrology Texts**: Brihat Parashara Hora Shastra, Jaimini Sutras
- **API Providers**: AstrologyAPI.com, Prokerala, GeoVedic
- **Libraries**: Swiss Ephemeris (planetary calculations)
- **Terminology**: https://en.wikipedia.org/wiki/Hindu_astrology

## Summary

Building an astrology backend requires:
1. **Domain Knowledge**: Understand houses, planets, dasha, doshas
2. **Accurate Data**: Timezone and coordinates are critical
3. **Structured Transformation**: Convert verbose API data to clean kundli
4. **Rich AI Context**: Provide complete birth chart to LLM
5. **Query Intelligence**: Map user questions to relevant chart sections
6. **Remedies**: Always provide actionable guidance

This skill provides the patterns and domain knowledge to build production-grade vedic astrology systems with AI integration. Combine with the `ai-integrated-api-backend` skill for complete implementation guidance.

IMPORTANT ASTRO DATA POINTS: 
- astro_details — Basic birth chart details
- horo_d1_chart_data — Main birth chart (Rashi chart)
- horo_d9_chart_data — Navamsa divisional chart
- planet_chart_data — Detailed planetary positions
- current_vdasha — Current Vimshottari dasha period
- current_vdasha_all — Complete dasha timeline
- manglik — Manglik dosha analysis
- pitra_dosha_report — Pitra dosha analysis
- basic_gem_suggestion — Gemstone recommendations
- rudraksha_suggestion — Rudraksha bead suggestions