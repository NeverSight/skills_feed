---
name: dribl-crawling
description: Document patterns for crawling dribl.com fixtures website using playwright-core to extract clubs and fixtures data with Cloudflare protection. Covers extraction (crawling with API interception) and transformation (Zod validation, data merging) phases.
---

# Dribl Crawling

## Overview

Extract clubs and fixtures data from https://fv.dribl.com/fixtures/ (SPA with Cloudflare protection) using real browser automation with playwright-core. Two-phase workflow: extraction (raw API data) → transformation (validated, merged data).

**Purpose**: Crawl dribl.com to maintain up-to-date clubs and fixtures data for Williamstown SC website.

## Architecture

**Data flow:**

```
dribl API → data/external/fixtures/{team}/ (raw) → transform → data/matches/ (validated)
dribl API → data/external/clubs/ (raw) → transform → data/clubs/ (validated)
```

**Two-phase pattern:**

1. **Extraction**: Playwright intercepts API requests, saves raw JSON
2. **Transformation**: Read raw data, validate with Zod, transform, deduplicate, save

**Key technologies:**

- playwright-core (real Chrome browser)
- Zod validation schemas
- TypeScript with tsx runner

## Clubs Extraction

**Reference**: `bin/crawlClubs.ts`

**Pattern:**

```typescript
// Launch browser
const browser = await chromium.launch({
	headless: false,
	channel: 'chrome'
});

// Custom user agent (bypass detection)
const context = await browser.newContext({
	userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
	viewport: { width: 1280, height: 720 }
});

// Intercept API request
const [clubsResponse] = await Promise.all([
	page.waitForResponse((response) => response.url().startsWith(clubsApiUrl) && response.ok(), {
		timeout: 60_000
	}),
	page.goto(url, { waitUntil: 'domcontentloaded' })
]);

// Validate and save
const rawData = await clubsResponse.json();
const validated = externalApiResponseSchema.parse(rawData);
writeFileSync(outputPath, JSON.stringify(validated, null, '\t') + '\n');
```

**API endpoint:**

- URL: `https://mc-api.dribl.com/api/list/clubs?disable_paging=true`
- Response: JSON with `data` array of club objects
- Validation: `externalApiResponseSchema` (src/types/matches.ts)

**Output:**

- Path: `data/external/clubs/clubs.json`
- Format: Single JSON file with all clubs

**CLI args:**

- `--url <fixtures-page-url>` (optional, defaults to standard fixtures page)

## Fixtures Extraction

**Pattern (implemented in bin/crawlFixtures.ts):**

**Steps:**

1. Navigate to https://fv.dribl.com/fixtures/
2. Wait for SPA to load (`waitUntil: 'domcontentloaded'`)
3. Apply filters (REQUIRED):
   - Season (e.g., "2025")
   - Competition (e.g., "FFV")
   - League (e.g., "state-league-2-men-s-north-west")
4. Intercept `/api/fixtures` responses
5. Handle pagination:
   - Detect "Load more" button in DOM
   - Click button to load next chunk
   - Wait for new API response
   - Repeat until no more data
6. Save each chunk as `chunk-{index}.json`

**API endpoint:**

- URL: `https://mc-api.dribl.com/api/fixtures`
- Query params: season, competition, league (from filters)
- Response: JSON with `data` array, `links` (next/prev), `meta` (cursors)
- Validation: `externalFixturesApiResponseSchema`

**Output:**

- Path: `data/external/fixtures/{team}/chunk-0.json`, `chunk-1.json`, etc.
- Format: Multiple JSON files (one per "Load more" click)
- Naming: `chunk-{index}.json` where index starts at 0

**CLI args:**

- `--team <slug>` (required) - Team slug for output folder (e.g., "state-league-2-men-s-north-west")
- `--league <slug>` (required) - League slug for filtering (e.g., "State League 2 Men's - North-West")
- `--season <year>` (optional, default to current year)
- `--competition <id>` (optional, default to FFV)

## Clubs Transformation

**Reference**: `bin/syncClubs.ts`

**Pattern:**

```typescript
// Load external data
const externalResponse = loadExternalData(); // from data/external/clubs/
const validated = externalApiResponseSchema.parse(externalResponse);

// Transform to internal format
const apiClubs = externalResponse.data.map((externalClub) => transformExternalClub(externalClub));

// Load existing clubs
const existingFile = loadExistingClubs(); // from data/clubs/

// Merge (deduplicate by externalId)
const clubsMap = new Map<string, Club>();
for (const club of existingClubs) {
	clubsMap.set(club.externalId, club);
}
for (const apiClub of apiClubs) {
	clubsMap.set(apiClub.externalId, apiClub); // update or add
}

// Sort by name
const mergedClubs = Array.from(clubsMap.values()).sort((a, b) => a.name.localeCompare(b.name));

// Save
writeFileSync(CLUBS_FILE_PATH, JSON.stringify({ clubs: mergedClubs }, null, '\t'));
```

**Transform service**: `src/lib/clubService.ts`

- `transformExternalClub()`: Converts external club format to internal format
- Maps fields: id→externalId, attributes.name→name/displayName, etc.
- Normalizes address (combines address_line_1 + address_line_2)
- Maps socials array (name→platform, value→url)
- Validates output with `clubSchema`

**Output:**

- Path: `data/clubs/clubs.json`
- Format: `{ clubs: Club[] }`

## Fixtures Transformation

**Reference**: `bin/syncFixtures.ts`

**Pattern:**

```typescript
// Read all chunk files
const teamDir = path.join(EXTERNAL_DIR, team);
const files = await fs.readdir(teamDir);
const chunkFiles = files.filter((f) => f.match(/^chunk-\d+\.json$/)).sort(); // natural number sort

// Load and validate each chunk
const responses: ExternalFixturesApiResponse[] = [];
for (const file of chunkFiles) {
	const content = await fs.readFile(path.join(teamDir, file), 'utf-8');
	const validated = externalFixturesApiResponseSchema.parse(JSON.parse(content));
	responses.push(validated);
}

// Transform all fixtures
const allFixtures = [];
for (const response of responses) {
	for (const externalFixture of response.data) {
		const fixture = transformExternalFixture(externalFixture);
		allFixtures.push(fixture);
	}
}

// Deduplicate (by round + homeTeamId + awayTeamId)
const seen = new Set<string>();
const deduplicated = allFixtures.filter((f) => {
	const key = `${f.round}-${f.homeTeamId}-${f.awayTeamId}`;
	if (seen.has(key)) return false;
	seen.add(key);
	return true;
});

// Sort by round, then date
const sorted = deduplicated.sort((a, b) => {
	if (a.round !== b.round) return a.round - b.round;
	return a.date.localeCompare(b.date);
});

// Calculate metadata
const totalRounds = Math.max(...sorted.map((f) => f.round), 0);

// Save
const fixtureData = {
	competition: 'FFV',
	season: 2025,
	totalFixtures: sorted.length,
	totalRounds,
	fixtures: sorted
};
writeFileSync(outputPath, JSON.stringify(fixtureData, null, '\t'));
```

**Transform service**: `src/lib/matches/fixtureTransformService.ts`

- `transformExternalFixture()`: Converts external fixture format to internal format
- Parses round number (e.g., "R1" → 1)
- Formats date/time/day strings (ISO date, 24h time, weekday name)
- Combines ground + field names for address
- Finds club external IDs by matching team names/logos
- Validates output with `fixtureSchema`

**Output:**

- Path: `data/matches/{team}.json`
- Format: `{ competition, season, totalFixtures, totalRounds, fixtures: Fixture[] }`

**CLI args:**

- `--team <slug>` (required) - Team slug to sync (e.g., "state-league-2-men-s-north-west")

## Validation Schemas

**Reference**: `src/types/matches.ts`

**External schemas (API responses):**

- `externalApiResponseSchema`: Clubs API response
- `externalClubSchema`: Single club object
- `externalFixturesApiResponseSchema`: Fixtures API response
- `externalFixtureSchema`: Single fixture object

**Internal schemas (transformed data):**

- `clubSchema`: Single club
- `clubsSchema`: Clubs file (`{ clubs: Club[] }`)
- `fixtureSchema`: Single fixture
- `fixtureDataSchema`: Fixtures file (`{ competition, season, totalFixtures, totalRounds, fixtures }`)

**Pattern**: Always validate at boundaries (API → external schema, transform → internal schema)

## CI Integration

**Reference**: `.github/workflows/crawl-clubs.yml`

**Linux setup (GitHub Actions):**

```yaml
- name: Install Chrome
  run: npx playwright install --with-deps chrome

- name: Crawl clubs
  run: npm run crawl:clubs:ci -- ${{ inputs.url && format('--url "{0}"', inputs.url) || '' }}
```

**Key points:**

- Use `xvfb-run` prefix on Linux for headless Chrome (e.g., `xvfb-run npm run crawl:clubs`)
- Install with `--with-deps` flag to get system dependencies
- Set appropriate timeout (5 min for clubs, may need more for fixtures)
- Upload artifacts for data files

**Package.json scripts pattern:**

```json
{
	"crawl:clubs": "tsx bin/crawlClubs.ts",
	"crawl:clubs:ci": "xvfb-run tsx bin/crawlClubs.ts",
	"sync:clubs": "tsx bin/syncClubs.ts",
	"sync:fixtures": "tsx bin/syncFixtures.ts"
}
```

## Best Practices

**Logging:**

- Use emoji logging for clarity:
  - ✓ / ✅ - Success
  - ❌ - Error
  - 📂 - File operations
  - 🔄 - Processing/transformation
- Log counts and progress for large operations

**Error handling:**

- Try/catch at top level
- Special handling for ZodError (print issues)
- Exit with code 1 on failure
- Close browser in finally block

**File operations:**

- Always use `mkdirSync(path, { recursive: true })` before writing
- Format JSON with tabs: `JSON.stringify(data, null, '\t')`
- Add newline at end of file: `content + '\n'`
- Use absolute paths with `resolve(__dirname, '../relative/path')`

**Data separation:**

- Keep raw external data in `data/external/` (gitignored)
- Keep transformed data in `data/` (committed)
- Never commit external API responses directly

**Validation:**

- Validate immediately after receiving API data
- Validate before writing transformed data
- Use descriptive error messages with file paths

**CLI arguments:**

- Use Commander library for consistent CLI parsing
- Define options with `.option()` or `.requiredOption()`
- Provide defaults for optional args
- Commander auto-generates help text and validates required args

## Common Patterns

**Reading chunks:**

```typescript
const files = await fs.readdir(dir);
const chunks = files
	.filter((f) => f.match(/^chunk-\d+\.json$/))
	.sort((a, b) => {
		const numA = parseInt(a.match(/\d+/)?.[0] || '0', 10);
		const numB = parseInt(b.match(/\d+/)?.[0] || '0', 10);
		return numA - numB;
	});
```

**Deduplication:**

```typescript
const seen = new Set<string>();
const unique = items.filter((item) => {
	const key = computeKey(item);
	if (seen.has(key)) return false;
	seen.add(key);
	return true;
});
```

**Merge with existing:**

```typescript
const map = new Map<string, T>();
existing.forEach((item) => map.set(item.id, item));
incoming.forEach((item) => map.set(item.id, item)); // update or add
const merged = Array.from(map.values());
```

**Browser cleanup:**

```typescript
let browser: Browser | undefined;
try {
  browser = await chromium.launch(...);
  // work
} finally {
  if (browser) await browser.close();
}
```
