---
name: hugo-sveltia-cms
description: Bootstrap new Hugo sites with Sveltia CMS and Basecoat UI, or convert existing sites (any SSG or CMS) to Hugo + Sveltia CMS. Use this skill whenever the user mentions Hugo, Sveltia CMS, Decap CMS migration, TinaCMS migration, static site CMS setup, headless CMS for Hugo, or wants to add a content management interface to a Hugo site. Also trigger when converting WordPress, Jekyll, Eleventy, TinaCMS, or other sites to Hugo, or when setting up Git-based content management. Covers the full workflow from scaffolding through Cloudflare Pages deployment with GitHub OAuth authentication.
---

# Hugo + Sveltia CMS Skill

Two primary workflows:
1. **Bootstrap**: New Hugo site with Sveltia CMS + Basecoat UI, deployed to Cloudflare Pages
2. **Convert**: Migrate from TinaCMS, Decap/Netlify CMS, WordPress, Jekyll, Eleventy, or other platforms to Hugo + Sveltia CMS

## Why This Stack

- **Hugo** — Fastest SSG, single binary, Go templates
- **Sveltia CMS** — Git-based headless CMS, drop-in Decap/Netlify CMS replacement with better UX and i18n. Beta, v1.0 early 2026. Same `config.yml` format as Decap
- **Basecoat** — shadcn/ui components without React. Tailwind CSS utility classes (`btn`, `card`, `input`), minimal JS, dark mode, themeable
- **Cloudflare Pages** — Primary deploy target. Free tier, fast CDN, Workers for OAuth
- **GitHub** — Only supported Git backend

## Critical Knowledge

1. **YAML front matter only.** Sveltia CMS has bugs with TOML (`+++`). Always use YAML (`---`) and set `format: yaml` on every collection.
2. **Use `hugo.yaml`** not `hugo.toml` for config consistency.
3. **Admin files in `static/admin/`.** Hugo copies `static/` to build root.
4. **Media paths.** `media_folder: "static/images/uploads"` (repo) → `public_folder: "/images/uploads"` (URL). Hugo strips `static/`.
5. **GitHub OAuth required.** Deploy `sveltia-cms-auth` as a Cloudflare Worker. Netlify git-gateway NOT supported.
6. **Always set** `extension: "md"` and `format: "yaml"` on every folder collection.
7. **Schema line** at top of `config.yml`: `# yaml-language-server: $schema=https://unpkg.com/@sveltia/cms/schema/sveltia-cms.json`

## Workflow: Bootstrap

### Step 1: Gather Requirements

Ask:
- **Site purpose**: Consulting/services, medical practice, blog, portfolio, docs?
- **Content types**: What content will they manage?
- **Basecoat approach**: Full Tailwind pipeline (recommended) or CDN-only prototype?
- **Custom domain**: For CF Pages + OAuth setup

### Step 2: Scaffold Hugo + Basecoat

```bash
hugo new site <site-name> --format yaml
cd <site-name>
```

Read `references/hugo-sveltia-setup.md § Basecoat Integration` for setup details.

**Production (recommended):** `npm init -y && npm install -D tailwindcss @tailwindcss/cli basecoat-css`, create `assets/css/main.css` with `@import "tailwindcss"; @import "basecoat-css";`, wire via Hugo's `css.TailwindCSS` pipe.

**CDN (quick start):** Add CDN links to `baseof.html` `<head>`.

### Step 3: Create Admin Interface

Create `static/admin/index.html` and `static/admin/config.yml` using `templates/`. Build collections from the domain-specific patterns in the reference file.

### Step 4: Build Layouts with Basecoat Components

Create Hugo partials wrapping Basecoat classes: `partials/components/card.html`, `button.html`, `badge.html`, `alert.html`, `nav.html`. These accept parameters via Hugo `dict` and emit styled HTML.

### Step 5: Create Archetypes + Seed Content

One archetype per content type in `archetypes/`.

### Step 6: Deploy to Cloudflare Pages

1. Register GitHub OAuth App → get Client ID + Secret
2. Deploy `sveltia-cms-auth` Cloudflare Worker
3. Connect repo to CF Pages, set `HUGO_VERSION` env var
4. Build command: `hugo --minify`, output: `public`
5. The bootstrap creates `.github/workflows/deploy.yml` automatically — set `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` as GitHub Secrets and `PAGES_PROJECT_NAME` as a GitHub Variable

### Step 7: Test Locally

Sveltia CMS detects localhost and uses File System Access API (Chromium) — no OAuth needed locally. Run `hugo server`, visit `/admin/`.

---

## Workflow: Convert

### From TinaCMS

TinaCMS uses GraphQL API + `tina/config.ts` schema + TinaCloud auth. Fundamentally different architecture.

**Field type mapping:**

| TinaCMS `type` | Sveltia `widget` | Notes |
|----------------|------------------|-------|
| `string` | `string` | |
| `string` + `list: true` | `list` | |
| `datetime` | `datetime` | |
| `boolean` | `boolean` | |
| `image` | `image` | |
| `rich-text` | `markdown` | Shortcode templates won't carry over |
| `object` | `object` | Map subfields recursively |
| `reference` | `relation` | Set `collection`, `search_fields`, `value_field` |
| `number` | `number` | Set `value_type: int` or `float` |

**Config mapping:** `tina/config.ts` `collections[].path` → `config.yml` `collections[].folder`

**Steps:**
1. Read `tina/config.{ts,js}`, map each collection's fields using table above
2. Content files (Markdown + YAML front matter) stay as-is — Hugo reads them directly
3. Delete `tina/` directory, remove `tinacms` from `package.json`, remove Tina build commands
4. Create `static/admin/` with Sveltia CMS files
5. Map Tina media config (`mediaRoot`/`publicFolder`) → Sveltia `media_folder`/`public_folder`
6. Document shortcodes used in content (no CMS-side visual editing for these)
7. Deploy via CF Pages + GitHub OAuth

**Key win:** No more TinaCloud dependency, no GraphQL build step, no `tina/__generated__/`.

### From Decap CMS / Netlify CMS

Drop-in replacement:
1. Replace script tag: `<script src="https://unpkg.com/@sveltia/cms/dist/sveltia-cms.js"></script>`
2. Existing `config.yml` works as-is
3. Replace `git-gateway` with GitHub OAuth + CF Worker
4. Test all collections

### From WordPress

1. Export via `wordpress-export-to-markdown` or `hugo import jekyll` after Jekyll export
2. Clean front matter (strip `wp_id`, `guid`)
3. Map taxonomies → Hugo taxonomies
4. Download media → `static/images/`
5. Build collections matching cleaned structure

### From Jekyll

1. `hugo import jekyll <jekyll-root> <hugo-root>` (built-in)
2. Review front matter, add Sveltia CMS per standard workflow

### From Eleventy / Other SSGs

1. Copy Markdown + YAML front matter files into `content/`
2. Adjust for Hugo conventions (`date` format, `draft` boolean)
3. Rebuild templates in Hugo, add Sveltia CMS

---

## Domain-Specific Collections

Read `references/hugo-sveltia-setup.md § Domain Collection Patterns` for ready-made configs:

- **Consulting / Services** — Services, case studies, testimonials, team members
- **Medical Practice** — Providers, locations, services/specialties, conditions, patient resources
- **Content / Blog** — Posts, pages, authors, newsletter, categories

Mix and match. Each includes full field definitions.

---

## File Checklist

- [ ] `hugo.yaml`
- [ ] `package.json` + `assets/css/main.css` (Basecoat/Tailwind, if npm path)
- [ ] `static/admin/index.html` + `static/admin/config.yml`
- [ ] `archetypes/` — one per content type
- [ ] `content/` — seed or converted content
- [ ] `layouts/` — Basecoat-styled templates + component partials
- [ ] `.github/workflows/deploy.yml` — CI/CD for Cloudflare Pages
- [ ] `.gitignore`

## Reference Files

- `references/hugo-sveltia-setup.md` — Full config reference, domain collections, Basecoat setup, widgets, auth, CF Pages deploy, gotchas, i18n
- `templates/admin-index.html` — Admin page template
- `templates/config.yml` — Annotated CMS config starter
- `templates/deploy.yml` — GitHub Actions workflow for Cloudflare Pages CI/CD
- `scripts/bootstrap-hugo-sveltia.sh` — One-command scaffolding
- `scripts/convert-toml-to-yaml.py` — Batch front matter conversion
