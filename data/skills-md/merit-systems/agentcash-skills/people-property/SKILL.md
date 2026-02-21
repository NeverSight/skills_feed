---
name: people-property
description: |
  Search for people and properties using Whitepages APIs via x402.

  USE FOR:
  - Finding people by name and location
  - Address lookups and verification
  - Property owner information
  - Background research (with legitimate purpose)

  TRIGGERS:
  - "find person", "lookup person", "who lives at"
  - "property owner", "property search", "address lookup"
  - "person at address", "contact info for"

  IMPORTANT: These endpoints contain personal information. Use responsibly and only for legitimate purposes.
  See rules/privacy.md for guidance.

  Use `npx agentcash fetch` for Whitepages endpoints. Both endpoints are $0.44 per call.
---

# People & Property Search with Whitepages

Access people and property search through x402-protected endpoints.

## Setup

See [rules/getting-started.md](rules/getting-started.md) for installation and wallet setup.

**Important:** This skill provides access to personal information. Review [rules/privacy.md](rules/privacy.md) before use.

## Quick Reference

| Task | Endpoint | Price | Description |
|------|----------|-------|-------------|
| Person search | `https://stableenrich.dev/api/whitepages/person-search` | $0.44 | Find people by name/location |
| Property search | `https://stableenrich.dev/api/whitepages/property-search` | $0.44 | Property and owner info |

## Person Search

Search for a person by name and location:

```bash
npx agentcash fetch https://stableenrich.dev/api/whitepages/person-search -m POST -b '{
  "firstName": "John",
  "lastName": "Smith",
  "city": "Seattle",
  "state": "WA"
}'
```

**Parameters:**
- `firstName` - First name (required)
- `lastName` - Last name (required)
- `city` - City name
- `state` - State abbreviation (US)
- `zip` - ZIP code
- `address` - Street address

**Returns:**
- Full name and age range
- Current and previous addresses
- Phone numbers
- Associated people (relatives, associates)

### More Specific Search

Include more details for better matches:

```bash
npx agentcash fetch https://stableenrich.dev/api/whitepages/person-search -m POST -b '{
  "firstName": "John",
  "lastName": "Smith",
  "address": "123 Main St",
  "city": "Seattle",
  "state": "WA",
  "zip": "98101"
}'
```

## Property Search

Search for property information:

```bash
npx agentcash fetch https://stableenrich.dev/api/whitepages/property-search -m POST -b '{
  "address": "123 Main Street",
  "city": "Seattle",
  "state": "WA"
}'
```

**Parameters:**
- `address` - Street address (required)
- `city` - City name
- `state` - State abbreviation
- `zip` - ZIP code

**Returns:**
- Property address (standardized)
- Owner name
- Property type (single family, condo, etc.)
- Property details

## Response Data

### Person Search Fields
- `name` - Full legal name
- `ageRange` - Estimated age range
- `currentAddress` - Current residence
- `historicalAddresses` - Previous addresses
- `phoneNumbers` - Associated phone numbers
- `associatedPeople` - Relatives and associates

### Property Search Fields
- `address` - Standardized address
- `owner` - Property owner name
- `propertyType` - Type of property
- `yearBuilt` - Construction year (if available)
- `bedrooms` / `bathrooms` - Property details
- `squareFootage` - Size (if available)

## Workflows

### Verify Contact Information

- [ ] Confirm legitimate purpose (see [rules/privacy.md](rules/privacy.md))
- [ ] (Optional) Check balance: `npx agentcash wallet info`
- [ ] Search with available details
- [ ] Verify results match expected person

```bash
npx agentcash fetch https://stableenrich.dev/api/whitepages/person-search -m POST -b '{"firstName": "Jane", "lastName": "Doe", "city": "Portland", "state": "OR"}'
```

### Property Research

- [ ] (Optional) Check balance: `npx agentcash wallet info`
- [ ] Search by address
- [ ] Review owner and property details

```bash
npx agentcash fetch https://stableenrich.dev/api/whitepages/property-search -m POST -b '{"address": "456 Oak Avenue", "city": "Austin", "state": "TX"}'
```

### Reconnect with Someone

- [ ] Confirm legitimate purpose
- [ ] Provide as much detail as possible for accuracy
- [ ] Review results for correct match

```bash
npx agentcash fetch https://stableenrich.dev/api/whitepages/person-search -m POST -b '{"firstName": "Michael", "lastName": "Johnson", "state": "CA"}'
```

## Cost Considerations

At $0.44 per call, Whitepages is the most expensive endpoint in the x402 suite.

| Scenario | Cost |
|----------|------|
| Single lookup | $0.44 |
| Verify address + person | $0.88 |
| Multiple candidates | $1.32+ |

**Tips to reduce costs:**
- Provide as much info as possible for accurate first-try results
- Use free sources first (LinkedIn, company websites)
- Use apollo, clado, firecrawl, WebSearch, WebFetch, to get data that will make the queries more accurate
- Only use for essential lookups

## Limitations

- US-focused data
- Results depend on public records availability
- Some individuals may have limited information
- Recently moved individuals may show old addresses
- Unlisted/private numbers not included
