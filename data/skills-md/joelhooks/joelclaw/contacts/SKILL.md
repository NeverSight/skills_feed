---
name: contacts
displayName: Contacts
description: "Add, enrich, and manage contacts in Joel's Vault. Fire the Inngest enrichment pipeline for full multi-source dossiers, or create quick contacts manually. Use when: 'add a contact', 'enrich this person', 'who is X', 'VIP contact', 'update contact', or any task involving the Vault/Contacts directory."
version: 1.0.0
author: joel
tags: [joelclaw, contacts, vault, enrichment, people]
---

# Contacts

Manage contacts in `~/Vault/Contacts/`. Each contact is a markdown file with YAML frontmatter.

## Contact File Location

```
~/Vault/Contacts/<Name>.md
```

Index file: `~/Vault/Contacts/index.md` — wikilink list of all contacts.

## Frontmatter Schema

```yaml
---
name: Full Name
aliases: [nickname, handle]
role: Current Role / Title
organizations: [Org1, Org2]
vip: true  # or false
slack_user_id: U0XXXXXXX
slack_dm_channel: D0XXXXXXX  # null if unknown
website: https://example.com
github: username
twitter: handle
email: user@example.com
tags: [vip, instructor, creator, family, employee]
---
```

## Sections

```markdown
# Name

## Contact Channels
- Slack, email, social handles, website

## Projects
- Active projects, courses, collaborations

## Key Context
- Relationship notes, working style, history

## Recent Activity
- YYYY-MM-DD | channel | summary
```

See `~/Vault/Contacts/Matt Pocock.md` for a fully enriched example.

## Adding a Contact

### Option 1: Fire the Enrichment Pipeline (preferred)

Send an Inngest event. The `contact-enrich` function fans out across 7 sources (Slack, Roam, web/GitHub, Granola, recall memory, Typesense), synthesizes with LLM, and writes the Vault file.

```bash
# Via curl (CLI has OTEL import bug under Bun v1.3.9)
curl -s -X POST http://localhost:8288/e/37aa349b89692d657d276a40e0e47a15 \
  -H "Content-Type: application/json" \
  -d '[{
    "name": "contact/enrich.requested",
    "data": {
      "name": "Person Name",
      "depth": "full",
      "hints": {
        "slack_user_id": "U0XXXXXXX",
        "github": "username",
        "twitter": "handle",
        "email": "user@example.com",
        "website": "https://example.com"
      }
    },
    "ts": EPOCH_MS
  }]'
```

**Depth modes:**
- `full` (~60s, ~$0.05): All 7 sources + LLM synthesis. Use for new contacts or periodic refresh.
- `quick` (~10s, ~$0.01): Slack + memory only. Good for real-time VIP detection.

**Hints are optional but help:** Any known identifiers (Slack ID, GitHub, email, Twitter, website) seed the search and improve results.

### Option 2: Quick Manual Create

For simple contacts where enrichment is overkill:

```markdown
---
name: Person Name
aliases: []
role: Role
organizations: [Org]
vip: false
slack_user_id: null
website: null
github: null
twitter: null
email: null
tags: [tag1]
---

# Person Name

## Contact Channels
- ...

## Key Context
- ...
```

Write to `~/Vault/Contacts/Person Name.md` and add `[[Person Name]]` to `index.md`.

## Updating Contacts

Re-run enrichment with the existing vault path:

```json
{
  "name": "contact/enrich.requested",
  "data": {
    "name": "Person Name",
    "vault_path": "Contacts/Person Name.md",
    "depth": "full"
  }
}
```

The synthesizer merges new data with existing content — it won't discard existing facts unless contradicted.

## VIP Contacts (ADR-0151)

Mark `vip: true` in frontmatter. VIPs get **deep enrichment + ongoing monitoring**.

### Deep Enrichment Playbook (one-time)

Every VIP gets the full treatment. This is what we did for Kent C. Dodds (Feb 26, 2026):

| Step | Source | What to Capture |
|---|---|---|
| 1. Web presence | Web search `{name} + {org}` | Bio, role, location, personal details |
| 2. Podcast/interviews | Web search `{name} podcast interview` | Appearance list, own podcasts, audiences |
| 3. Joel collaborations | Their website, appearances pages | Joint podcasts, co-organized events, shared projects |
| 4. Career timeline | Defuddle 2-3 key interview transcripts | Origin story, career arc, key decisions, values |
| 5. GitHub profile | GitHub API or web | Repos, followers, orgs, contribution patterns |
| 6. X/Twitter profile | X API v2 (use x-api skill) | Bio, followers, recent tweets, engagement |
| 7. Key relationships | Cross-reference transcripts + contacts | Who they work with, who they mention, who we know in common |
| 8. Content catalog | Website crawl (defuddle) | Courses, blog posts, open source projects |
| 9. Audience reach | Podcast counts, social followers | Conference circuit, community presence |

**Index to Typesense** after enrichment:
- Batch-import appearances/content to `discoveries` collection (NDJSON, `action=upsert`)
- Tag all docs with person's name slug (e.g. `kent-c-dodds`) for filtering
- Fields: `id`, `title`, `url`, `summary`, `tags[]`, `timestamp`
- Write a `Vault/Resources/{name}-media-appearances.md` reference doc linking back to contact

**Output sections** in the vault note:
- Background & Story (origin, career timeline)
- Teaching/Work Philosophy (or equivalent for non-educators)
- Key Relationships (cross-linked `[[wikilinks]]` to other contacts)
- Audience & Reach
- Content/Products
- Podcast/Collaboration History with Joel
- Recent Activity (timestamped)

### Ongoing Monitoring (Phase 2-4 of ADR-0151)

| Channel | Tool | Signal |
|---|---|---|
| Google Alerts | joelclawbot Google account | Name mentions in news, blogs, press |
| X/Twitter list | joelclaw X account | Tweets, engagement |
| GitHub activity | GitHub API (polling) | New repos, releases |
| Podcast RSS | Feed monitoring | New episodes |
| Website changes | Periodic defuddle + diff | Blog posts, launches, bio changes |

**High-signal** (immediate): course launches, role changes, mentions of Joel/egghead/Skill, fundraising.
**Low-signal** (daily/weekly digest): regular tweets, blog posts, OSS activity.

### Current VIPs
- Get notified to Joel via gateway after enrichment
- Are refreshed weekly via scheduled cron
- Have priority in channel intelligence pipeline (ADR-0131, ADR-0132)
- Get ongoing monitoring when ADR-0151 Phase 2+ is implemented

## Roam Research Enrichment

Joel's Roam archive (`~/Code/joelhooks/egghead-roam-research/`) contains the full egghead-era graph (2019-2024). Many contacts have extensive history there.

### Quick Search (Python regex)
```bash
cd ~/Code/joelhooks/egghead-roam-research
python3 -c "
import re
with open('egghead-2026-01-19-13-09-38.edn', 'r') as f:
    content = f.read()
pattern = r':block/string\s+\"([^\"]*?)\"'
matches = []
for m in re.findall(pattern, content):
    if '[[SEARCH_TAG]]' in m.lower():
        matches.append(m)
print(f'Found {len(matches)} blocks')
for m in matches[:30]:
    print(f'  - {m[:200]}')
"
```

### People Taxonomy
People are tagged with relationship prefixes in Roam:
- `[[collaborator/Name]]` — Strategic partners (Ian Jones, Alex Hillman)
- `[[client/Name]]` — egghead instructors (Matt Pocock, Jacob Paris)
- `[[staff/Name]]` — egghead team (Will Johnson, Daniel Miller, Maggie Appleton)
- `[[name]]` (no prefix) — Informal references (Zac is `[[zac]]`)

### Page Title Search
```bash
python3 -c "
import re
with open('egghead-2026-01-19-13-09-38.edn', 'r') as f:
    content = f.read()
pattern = r':node/title\s+\"([^\"]*?SEARCH_TERM[^\"]*?)\"'
for m in re.findall(pattern, content):
    print(f'  page: {m}')
"
```

### Adding to Contacts
When extracting person data from Roam, add `roam_tag` to frontmatter:
```yaml
roam_tag: "[[collaborator/Ian Jones]]"
```
This enables future re-queries and cross-referencing.

### Datalog Queries (advanced)
The EDN file is Datomic-style. Clojure scripts exist at `scripts/` for structured analysis. See the `roam-research` skill for full Datalog patterns.

## Resolving Unknown People

When you encounter a Slack user ID (`<@U0XXXXXXX>`):

```bash
# Lease token and look up profile
SLACK_USER=$(secrets lease slack_user_token --ttl 5m)
curl -s "https://slack.com/api/users.info?user=U0XXXXXXX" \
  -H "Authorization: Bearer $SLACK_USER" | jq '.user.real_name, .user.profile.email'
secrets revoke --all
```

Then fire enrichment with the resolved name and hints.

## Inngest Function

- Function: `contact-enrich` (`packages/system-bus/src/inngest/functions/contact-enrich.ts`)
- Event: `contact/enrich.requested`
- ADR: `~/Vault/docs/decisions/0133-contact-enrichment-pipeline.md`
- Concurrency: 3 max
- Sources: Slack, Slack Connect, Roam archive, GitHub/web, Granola meetings, recall memory, Typesense

## Privacy

- Contact files are in Vault (private, not in public repos)
- Slack data stays private — never surface in public content
- Email/phone are stored for Joel's reference only
