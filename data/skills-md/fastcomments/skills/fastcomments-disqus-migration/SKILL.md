---
name: fastcomments-disqus-migration
description: >
  Use when moving comments off Disqus, Commento, Hyvor Talk, IntenseDebate, Muut, Just-Comments, Cusdis,
  AnyComment, or WordPress native comments onto FastComments, or when evaluating a Disqus alternative.
  Covers exporting from each provider, the self-service import, the automated WordPress plugin migration
  with sync-back, mapping old page URLs onto urlId so threads land on the right pages, moving comments
  between pages or domains after the fact, re-running an import without creating duplicates, and migrating
  users and moderators.
---

# Migrating to FastComments

Most migrations are self-service. Support can help, but you do not need to open a ticket to do this.

Three things move, and only the first two are automated: comment data including replies, user accounts
including avatars, and custom styling. Styling is a rewrite against
`https://docs.fastcomments.com/guide-customizations-and-configuration.html`.

## Supported sources

Native importers exist for:

- Disqus
- Commento
- Hyvor Talk
- Muut Comments
- IntenseDebate
- Just-Comments
- Cusdis
- WordPress, through the plugin - no manual export at all
- AnyComment, through the WordPress import/export

Upload the export file at `https://fastcomments.com/auth/my-account/manage-data/import`.

## The general flow

1. Export from the current provider. For Disqus this is the XML export from its admin area; each provider
   has its own export screen.
2. Upload it on the import page and pick the matching provider.
3. Watch the job. Imports and exports run through a job system that reports status in the UI, visible to
   every administrator on the account.
4. Check a handful of threads against the live site.
5. Re-run the import shortly before cutover to catch comments posted in the meantime.
6. Swap the embed. See `fastcomments-comment-widget`, or `fastcomments-static-sites` for a generated site.

**Re-importing the same content does not create duplicates.** A test pass now and a final pass at cutover is
the intended workflow, not a risk.

A failed job is not retried automatically - run the import again. Our system administrators are notified
automatically when an import or export fails, and will reach out if we spot the problem.

Import files are not reachable by outside requests and are deleted as soon as the import completes.

## urlId is what decides where comments land

FastComments groups comments by `urlId`. Your old provider grouped them by its own identifier, usually the
page URL or a thread ID. The import maps those across, and the mapping is the part worth checking.

Left unset in the widget, `urlId` defaults to a cleaned version of the current page URL. So if the imported
comments carry the old URLs and your new site uses different paths, the threads exist but no page displays
them. Two fixes:

- Set `urlId` explicitly in the widget to whatever the import used, which is usually the old URL or post ID.
  This is the more robust option, because it survives future URL changes too.
- Or rewrite the imported values with the domain migration tool.

Export your comments to see exactly what `urlId` values they carry.

## Moving comments after an import

Two self-service tools, both under Manage Data:

- **Domain migration** - enter old and new values in `from` and `to`. Despite the name it works for a single
  page as well as a whole domain, so it doubles as a bulk `urlId` rewrite.
- **Copy comments** - `https://fastcomments.com/auth/my-account/manage-data/copy-comments`. Takes a source
  `URL ID`, and a target `URL ID` plus `URL`. The URL ID is the bucket the comments go into; the URL is what
  moderation tools and notification emails link to.

On WordPress, put article IDs in the URL ID fields rather than URLs.

## WordPress

The WordPress plugin has the best migration path of any source, because nothing is exported or downloaded by
hand. Install `https://wordpress.org/plugins/fastcomments/`, and it walks you through linking the site to
FastComments and copying the existing comments across. Most migrations finish in a couple of minutes, and
the process is designed not to load the WordPress install heavily.

**Data ownership.** New and updated comments are synced back into your WordPress database behind the scenes.
FastComments serves the comments so WordPress does not have to, but your database stays current. If you ever
leave, your data is already there and up to date.

**Firewalls.** The automated setup calls into your WordPress install, so Cloudflare and similar can block
it and fail the integration. Ask via `https://fastcomments.com/auth/my-account/help` for the IP list to
allowlist.

The plugin also uses server-side rendering as a fallback by default since version 3.10.2, so readers with
JavaScript disabled can still comment.

## Users and moderators

Users are added to your tenant through the dashboard, with permissions matching their role. If you have a
lot of them, support can bulk-import them. Moderators are added separately - see the
`fastcomments-moderation` skill.

There is no password to migrate. FastComments logs people in with magic links, so anyone hunting for a
password field will not find one.

Commenters themselves are a different thing from dashboard users: they arrive with the imported comments, or
you supply them yourself with SSO. If your site already has accounts, wire up SSO so the imported history
attaches to the right people. See `fastcomments-sso`.

## Checklist before flipping the switch

- Comments visible on the pages you spot-checked, with replies nested correctly.
- `urlId` in the widget matches what the import wrote.
- Region correct: `region: "eu"` if the account lives on `eu.fastcomments.com`.
- Domains configured on the account, or the widget refuses to load.
- Moderation settings reviewed, since imported comments arrive under your current rules.
- A final import run after the last comment on the old provider.

Guide: `https://docs.fastcomments.com/guide-migrations.html`.
