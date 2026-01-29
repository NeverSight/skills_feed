---
name: booking
description: Enables Claude to search Booking.com for hotels, considering city, dates, price, neighborhoods, and preferred chains (including all brands). It also outputs the hotel's direct website link.
---

# Skill: Search Booking.com for Hotels

## Description
This skill guides the agent to search Booking.com for hotels, considering city, dates, price, neighborhoods, and preferred chains (including all brands). It also outputs the hotel's direct website link and integrates family travel preferences.

## Prerequisites
1. Check `preferences.md` for:
   - Family composition and ages
   - Mandatory requirements (e.g., fridge, room size)
   - Preferred amenities (pool for kids, free cancellation)
   - Budget guidelines
2. Check `plan.md` for specific trip dates and locations

## Hotel Chain Brand Mapping

### Hilton Family
- Hilton Hotels & Resorts
- DoubleTree by Hilton
- Hampton by Hilton
- Embassy Suites by Hilton
- Homewood Suites by Hilton
- Conrad Hotels & Resorts
- Waldorf Astoria Hotels & Resorts
- Curio Collection by Hilton
- Tru by Hilton
- Home2 Suites by Hilton

### Marriott International
- Marriott Hotels & Resorts
- Courtyard by Marriott
- Sheraton Hotels & Resorts
- Westin Hotels & Resorts
- Renaissance Hotels
- Residence Inn by Marriott
- SpringHill Suites by Marriott
- Fairfield by Marriott
- TownePlace Suites by Marriott
- Four Points by Sheraton
- JW Marriott
- The Ritz-Carlton

### IHG (InterContinental Hotels Group)
- Holiday Inn
- Holiday Inn Express
- InterContinental Hotels & Resorts
- Crowne Plaza Hotels & Resorts
- Hotel Indigo
- Kimpton Hotels & Restaurants
- Candlewood Suites
- Staybridge Suites
- EVEN Hotels

### Hyatt Hotels Corporation
- Hyatt Regency
- Hyatt Place
- Hyatt House
- Grand Hyatt
- Hyatt Centric
- Park Hyatt

### Choice Hotels
- Comfort Inn
- Comfort Suites
- Quality Inn
- Clarion Hotel
- Sleep Inn
- Cambria Hotels

### Best Western
- Best Western
- Best Western Plus
- Best Western Premier

### Independent/Boutique
- When chains don't meet requirements, consider well-reviewed independent hotels

## Search Process

### Step 1: Gather Search Criteria
From user request or travel plan, collect:
- **City/Location**: Specific city and optional neighborhood
- **Check-in Date**: Format as YYYY-MM-DD (e.g., 2026-07-17)
- **Check-out Date**: Format as YYYY-MM-DD (e.g., 2026-07-20)
- **Nights**: Calculate duration
- **Adults**: Number of adult travelers
- **Children**: Number and ages of children
- **Price Range**: Min and max per night in USD
- **Preferred Chains**: Specific chain or "any"
- **Required Amenities**: From preferences (pool, fridge, free cancellation, etc.)

### Step 2: Construct Search Query
Use web search with query like:
```
site:booking.com [City] [Neighborhood] [Hotel Chain Brand] [Check-in Date] [Check-out Date] [Number of guests]
```

Alternative: Use natural language web search:
```
[Hotel Chain Brand] hotels in [City] [Neighborhood] on Booking.com, [Check-in Date] to [Check-out Date], [Number of guests], price $[Min]-$[Max]
```

### Step 3: Filter and Validate Results
For each hotel found:
- ✅ Verify it matches preferred chain/brand
- ✅ Check price is within range
- ✅ Confirm availability for dates
- ✅ Check guest ratings (prefer 7.5+ out of 10)
- ✅ Verify required amenities (especially fridge for family)
- ✅ Check room size (larger for 3+ night stays)
- ✅ Note if free cancellation available

### Step 4: Retrieve Direct Website Links
For each selected hotel:
1. Search for: `[Hotel Name] [City] official website`
2. Look for the hotel's direct booking site (often chain.com or hotel's own domain)
3. Note: Direct booking sometimes offers better rates or perks

### Step 5: Handle Edge Cases
- **No results found**: Expand search to nearby neighborhoods or adjacent dates
- **Outside price range**: Present closest options and note the price difference
- **No preferred chains available**: Suggest highly-rated independent hotels
- **Missing amenities**: Flag mandatory vs. preferred missing amenities

## Output Format

Present results in this structured format:

```markdown
### Hotel Search Results: [City], [Dates]

**Search Criteria:**
- Location: [City, Neighborhood]
- Dates: [Check-in] to [Check-out] ([N] nights)
- Guests: [N] adults, [N] children
- Budget: $[Min]-$[Max] per night
- Chain Preference: [Chain name or "Any"]

---

#### Option 1: [Hotel Name]
- **Brand**: [Brand Name] ([Parent Chain])
- **Price**: $[Amount] per night ($[Total] total)
- **Rating**: [Score]/10 ([Number] reviews)
- **Location**: [Neighborhood/Area]
- **Amenities**: [List key amenities - fridge, pool, free breakfast, etc.]
- **Room Type**: [Room description]
- **Cancellation**: [Free cancellation until DATE or Non-refundable]
- **Booking.com Link**: [URL]
- **Direct Website**: [URL or "Not found"]

---

#### Option 2: [Hotel Name]
[Same format as above]

---

#### Option 3: [Hotel Name]
[Same format as above]

---

**Recommendation**: [Brief note on which option best fits family preferences and why]
```

## Family Travel Integration

When searching for the family in `preferences.md`:
- **Mandatory**: Room with fridge (or kitchenette)
- **Highly Preferred**: Pool (for Shay), free cancellation
- **Preferred**: Larger rooms for 3+ night stays, family-friendly area
- **Budget**: Spend more for comfort on longer stays (~$150-250/night typical)
- **Room Type**: 2-bedroom suite or adjoining rooms for 4 travelers when available

## Instructions

### For Agent Execution:

1. **Gather criteria** from user request or travel documents:
   - City/location and neighborhood
   - Check-in/check-out dates (convert to YYYY-MM-DD)
   - Number of guests (adults and children with ages)
   - Price range per night
   - Preferred hotel chain (if any)
   - Required amenities from preferences

2. **Construct and execute search** using web search tools with booking.com site search

3. **Filter results** by:
   - Matching preferred brands (use chain mapping above)
   - Price within range
   - Guest rating 7.5+ preferred
   - Required amenities present

4. **Find direct booking links** for top options via web search

5. **Present results** using the output format template above

6. **Make recommendation** based on family preferences integration

## Example Execution

**User Request**: "Find hotels in Portland for August 2-4"

**Agent Actions**:
1. Check `plan.md` → Segment 6: Portland, 3 nights
2. Check `preferences.md` → Family of 4 (2 adults, 2 kids ages 6 & 9)
3. Search: "site:booking.com Portland Oregon hotel August 2 2026 August 4 2026 4 guests pool fridge"
4. Filter for: Price $150-250, guest rating 7.5+, fridge/kitchenette, pool preferred
5. Find direct websites for top 3 options
6. Present formatted results with family-relevant notes
7. Recommend best option based on preferences (e.g., "Option 2 offers best value with pool and Pearl District location")

## Tips for Agent Execution
- Always convert dates to YYYY-MM-DD format for consistency
- Check if user has flexibility on dates if no good options found
- Consider hotel location relative to planned activities in `plan.md`
- Note parking availability and costs (important for road trips)
- Flag breakfast options (family prefers mix of hotel breakfast and local diners)
- When in doubt about chain brands, search "[Brand Name] part of which hotel chain"
- For multi-night stays (3+), prioritize larger rooms and suites
- Free cancellation is highly valued for flexibility
