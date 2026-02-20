---
name: release-management
description: Manage music releases using RELEASE.md documents stored in releases/{release-slug}/ within an artist workspace. Triggers when the user mentions an artist's album, EP, single, or project — or asks about release planning, DSP pitches, metadata, marketing, press materials, physical production, or tour coordination. First infer which artist and release the user means, then find or create the RELEASE.md. Use this skill to create, update, or pull data from release documents, and to generate deliverables like DSP pitches, press one-sheets, and production specs.
---

# Music Release Management

Manage music release campaigns using RELEASE.md as the single source of truth.

## Folder Structure

Releases live inside an artist workspace under `releases/`. The full path from the sandbox root:

```
orgs/{org}/
└── artists/
    └── {artist-slug}/
        └── releases/
            └── {release-slug}/
            └── RELEASE.md
```

Use lowercase-kebab-case for release slugs (e.g. `blue-slide-park`, `debut-ep`).

**Example:**
```
orgs/recoup-records/artists/gatsby-grace/releases/adhd-ep/
            └── RELEASE.md
```

## Step 1: Identify the Release

When the user mentions a release, infer:

1. **Organization** — From the sandbox structure or conversation context
2. **Artist** — From the current workspace, conversation history, or ask
3. **Release Name** — Album title, EP name, single title
4. **Release slug** — Derive from the name (e.g. "Blue Slide Park" → `blue-slide-park`)

**If unclear, ask:**
> "Which artist and release are you referring to?"

## Step 2: Check if RELEASE.md Exists

Once artist and release are identified:

```
1. Navigate to: orgs/{org}/artists/{artist-slug}/releases/{release-slug}/
2. Check if RELEASE.md exists
3. If YES → Read it and proceed
4. If NO → Ask: "No RELEASE.md found for [Release]. Should I create one?"
```

## Step 3: Create, Update, or Pull

| User Intent | Action |
|-------------|--------|
| Discussing a release | Read RELEASE.md, use as context |
| Adding information | Update the relevant section(s) |
| Asking for a deliverable | Pull data from RELEASE.md, generate output |
| Starting a new release | Create folder structure + RELEASE.md from template |

### Creating a New Release

```bash
# 1. Create the folder structure (from sandbox root)
mkdir -p "orgs/{org}/artists/{artist-slug}/releases/{release-slug}"

# 2. Create RELEASE.md from template
# 3. Fill Section 1 (Project Snapshot) first
```

### Updating an Existing Release

1. Read the current RELEASE.md
2. Identify which section(s) need updates
3. Update only those sections
4. Note changes in Document History (Section 18)

## Core Principles

1. **Never fabricate data** — Leave sections blank if information is missing
2. **Be proactive** — Fill sections as information becomes available
3. **Respect sharing tags** — `[INTERNAL]`, `[SHAREABLE]`, `[OPS]` control distribution
4. **One document per release** — All release info lives in RELEASE.md
5. **Always confirm the release** — Before making changes, confirm which release.

## Sharing Tags

| Tag | Meaning |
|-----|---------|
| `[INTERNAL]` | Scrub before sharing externally |
| `[SHAREABLE]` | Safe for publicists, DSPs, management, agents |
| `[OPS]` | Operations/production team reference |

## Document Sections

| Section | Purpose | Sharing |
|---------|---------|-------|
| 1. Project Snapshot | Core release info | SHAREABLE |
| 2. Release Identifiers & Metadata | UPCs, ISRCs, track data | OPS |
| 3. Narrative & Positioning | Pitch, story, comparables | SHAREABLE |
| 4. Artist Background | Bio, streaming history | SHAREABLE |
| 5. Audience & Market Data | Demographics, geo data | SHAREABLE |
| 6. DSP & Streaming Strategy | Pitches, playlist targets | SHAREABLE |
| 7. Marketing Strategy | Campaign goals, KPIs | INTERNAL |
| 8. Social & Digital Marketing | Organic, paid, influencer | INTERNAL |
| 9. PR & Media Relations | Press targets, materials | SHAREABLE |
| 10. Visual & Creative Assets | Artwork, videos, canvases | SHAREABLE |
| 11. Physical Production | Vinyl, CD, cassette specs | OPS/INTERNAL |
| 12. Merch | Items, strategy | INTERNAL |
| 13. Experiential & OOH | Events, billboards | INTERNAL |
| 14. Touring & Live | Dates, venues, routing | SHAREABLE |
| 15. Team Contacts | All stakeholders | INTERNAL |
| 16. Budget Overview | Allocated/spent/remaining | INTERNAL |
| 17. Performance Tracking | Weekly KPIs, learnings | INTERNAL |
| 18. Links & Resources Hub | All asset links | — |

## Generating Deliverables

See `references/deliverables.md` for output patterns:

- **DSP Pitch** — Pull from Sections 1, 3, 4, 5, 6
- **Press One-Sheet** — Pull from Sections 1, 3, 4, 9, 10
- **Physical Production Spec** — Pull from Sections 2, 11
- **Marketing Brief** — Pull from Sections 1, 3, 5, 6, 7, 8
- **Tour Marketing Brief** — Pull from Sections 1, 3, 5, 14

When generating any deliverable:
1. Check RELEASE.md for required data
2. Identify missing fields
3. Request missing info from user OR generate with gaps noted
4. Format per deliverable spec

## Template

The full release template is in `references/release-template.md`. Copy this file to start a new release.

## Section Deep-Dive

See `references/section-guide.md` for detailed guidance on each section, including:
- What each field means
- Common data sources
- Best practices for filling out
- Red flags to watch for

## Workflows

### New Release Setup

1. Copy template → RELEASE.md
2. Fill Section 1 (Project Snapshot)
3. Fill Section 2.2 (Track Metadata) as available
4. Draft Section 3 (Narrative & Positioning)
5. Pull artist data for Sections 4-5
6. Build DSP pitch (Section 6)
7. Continue through remaining sections as timeline progresses

### Pre-Release Checklist

Before announcement, verify these sections are complete:

- [ ] Section 1: All dates confirmed
- [ ] Section 2: UPC assigned, ISRCs for all tracks
- [ ] Section 3: Pitch and narrative finalized
- [ ] Section 6: DSP pitch submitted
- [ ] Section 9: Press materials ready
- [ ] Section 10: All visual assets delivered

### Release Week Checklist

- [ ] Section 6: Pre-save links live
- [ ] Section 7: Phase 2 actions executing
- [ ] Section 8: Paid ads launched
- [ ] Section 9: Press embargo lifted
- [ ] Section 17: Tracking dashboard ready

### Post-Release

- [ ] Section 17: Weekly KPIs logged
- [ ] Section 17: Wins and learnings documented
- [ ] Document History updated

## Example Interactions

### Creating a new release
> **User:** "Create a RELEASE.md for the new album 'Decisions'"
> 
> **Process:**
> 1. Release = "Decisions", slug = `decisions`
> 2. Create `releases/decisions/RELEASE.md` from template
> 3. Ask: "What's the release date?" (to fill Section 1)

### Adding metadata
> **User:** "Update the 'Sunrise' RELEASE.md with these ISRCs"
>
> **Process:**
> 1. Release = "Sunrise", slug = `sunrise`
> 2. Open `releases/sunrise/RELEASE.md`
> 3. Update Section 2.2 with ISRC data
> 4. If file not found → "No RELEASE.md for 'Sunrise'. Should I create one?"

### Generating a deliverable
> **User:** "Generate a DSP pitch from the Midnights RELEASE.md"
>
> **Process:**
> 1. Read `releases/midnights/RELEASE.md`
> 2. Pull data from Sections 1, 3, 4, 5, 6
> 3. Format per `deliverables.md` spec
> 4. If missing fields → "Missing [fields]. Proceed with gaps noted?"

### Checking release status
> **User:** "What's missing from the 'For All The Dogs' release doc?"
>
> **Process:**
> 1. Read `releases/for-all-the-dogs/RELEASE.md`
> 2. Run through Pre-Release Checklist
> 3. Report incomplete sections
