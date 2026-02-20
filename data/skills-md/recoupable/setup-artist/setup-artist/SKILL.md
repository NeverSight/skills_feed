---
name: setup-artist
description: Set up the workspace for a new artist inside a sandbox. Creates the directory structure, context files, memory system, and placeholder content so agents can immediately start working. Use after setup-sandbox has created the org/artist folders, when RECOUP.md has status not-setup. Triggers on "set up artist", "create artist workspace", "initialize artist", or "onboard new artist".
---

# Setup Artist

Scaffold a complete artist workspace so agents can start working immediately.

## Prerequisites

- The sandbox has already been set up (see `setup-sandbox` skill)
- An artist folder exists at `orgs/{org}/artists/{artist-slug}/` with a `RECOUP.md` marker file
- The `RECOUP.md` file contains the artist's name, slug, and Recoup ID (created by `setup-sandbox`)

## Folder Structure

```
{artist-slug}/
├── RECOUP.md
├── README.md
├── .env.example
├── .env
├── context/
│   ├── artist.md
│   ├── audience.md
│   ├── era.json
│   ├── tasks.md
│   └── images/
│       └── README.md
├── memory/
│   ├── README.md
│   └── MEMORY.md
├── songs/
│   └── README.md
├── releases/
│   └── README.md
├── content/
│   ├── README.md
│   ├── images/
│   └── videos/
├── config/
│   ├── README.md
│   └── SERVICES.md
├── library/
│   └── README.md
└── apps/
    └── README.md
```

## Steps

### Step 1: Read `RECOUP.md` and create the directory structure

1. Navigate to the artist folder and read `RECOUP.md` to get the artist's name, slug, and ID:

```bash
cd orgs/{org}/artists/{artist-slug}
cat RECOUP.md
```

2. Create the directory structure:

```bash
mkdir -p {context/images,memory,songs,releases,content/images,content/videos,config,library,apps}
```

### Step 2: Update `RECOUP.md`

Update the `status` field from `not-setup` to `active` and replace the body with a brief description:

```markdown
---
artistName: {Artist Name}
artistSlug: {artist-slug}
artistId: {uuid-from-recoupable}
status: active
---

# {Artist Name}

Connects this workspace to the Recoupable platform. See `README.md` for the full directory guide and setup checklist.
```

### Step 3: Create context files

Create each file from the templates in `references/context-files.md`. The essential files:

| File | What to do |
|------|-----------|
| `context/artist.md` | Fill with artist identity, brand, visual world, voice, tone. Ask the user for details or research the artist. |
| `context/audience.md` | Fill with audience insights. Focus on WHY they listen, what they relate to, how they talk. |
| `context/era.json` | Set the current release, songs, phase, and career stage. |
| `context/tasks.md` | Leave blank — the user will add tasks as they come up. |
| `context/images/README.md` | Create with a note explaining this holds visual references like face guides. |

### Step 4: Create memory system

Create two files:

- `memory/README.md` — Full instructions for agents on how to use the memory system, **including the scope concept**. See `references/memory-system.md`.
- `memory/MEMORY.md` — Nearly empty starting point with frontmatter and guidelines comment (including scope rules).

The memory system uses three scopes to prevent knowledge bloat:
- **permanent** — true regardless of era (goes in `MEMORY.md`)
- **era** — true for the current release cycle (goes in `MEMORY.md`, tagged with era)
- **session** — about a specific piece of content or task (goes in `log/` only, never `MEMORY.md`)

Agents should **ask the user about scope** before saving feedback to long-term memory.

### Step 5: Create services and environment files

Services are tracked in `config/`, not pre-filled at setup. Create:

| File | What to do |
|------|-----------|
| `config/SERVICES.md` | Instructions for agents on how to add services as they're discovered. See `references/services-guide.md`. |
| `.env.example` | Reference list of common env var names (all commented out). See `references/env-template.md`. |
| `.env` | Empty file with a header comment. Agents add credentials here as services are connected. |

**Do NOT pre-fill service entries.** Services are added when the agent has real information — a handle, an API key, a confirmed account. The old approach of creating a massive JSON file with every possible service set to `not-setup` creates noise, not value.

### Step 6: Create README files for remaining directories

Each directory needs a `README.md` explaining its purpose. See `references/directory-readmes.md` for templates.

| Directory | README explains... |
|-----------|-------------------|
| `songs/` | Song folder format, naming conventions, what files to add |
| `releases/` | Release folder format, RELEASE.md as source of truth |
| `content/` | Generated content output — images and videos |
| `config/` | Per-artist config, services, and shared automation tools |
| `library/` | Deep-dive reference docs, research, reports |
| `apps/` | Artist-specific applications (not shared tools) |

### Step 7: Create root README

Create `README.md` at the artist root with:
- Artist name as heading
- Directory structure table
- Context files table
- Config & services table
- Setup checklist

See `references/root-readme.md` for the template.

### Step 8: Fill in what you can

If you have information about the artist (from the user, from research, or from the Recoup platform):

1. Fill `context/artist.md` with as much identity/brand info as possible
2. Fill `context/audience.md` with audience insights
3. Set `context/era.json` with the current release phase

**Don't fabricate information.** Leave placeholders for anything you don't know.

### Step 9: Commit

```bash
git add -A
git commit -m "setup: create {artist-name} artist workspace"
git push origin main
```

## Naming Conventions

- **Directories and slugs:** `lowercase-kebab-case` (e.g. `gatsby-grace`, `a-thing-called-love`)
- **Audio files:** Match the folder slug (e.g. `songs/a-thing-called-love/a-thing-called-love.mp3`)
- **Context files:** Use the names exactly as specified — agents and shared tools expect them

## Principles

- **Start lean.** Only create what's needed. Agents and pipelines will create additional files (like `content/videos/shortform/`) as they run.
- **Placeholders over empty.** Use `{placeholder}` syntax for unknown values — it's better than blank fields.
- **Don't pre-fill what you don't know.** A file full of `not-setup` and `null` isn't a placeholder — it's clutter. Services, accounts, and configs should be added when they're real.
- **README everything.** Every directory gets a README so agents know what belongs there.
- **Don't duplicate.** Songs live in `songs/`, releases reference them by slug. Content goes in `content/`, not copied elsewhere.
- **Scope your memories.** Not all knowledge lasts forever. Tag era-specific memories, keep session feedback in logs, and ask before promoting to long-term memory.
