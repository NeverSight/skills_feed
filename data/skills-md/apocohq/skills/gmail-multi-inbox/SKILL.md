---
name: gmail-multi-inbox
description: |
  Set up and maintain Gmail Multiple Inboxes with auto-discovered sender filters. Scans the user's Gmail to discover senders, suggests inbox categories, generates a Google Apps Script that creates labels and filters. Use this skill for: organizing Gmail, setting up multiple inboxes, managing Gmail labels and filters, categorizing email senders, updating inbox filters with new senders, or unsubscribing from noisy emails. Trigger phrases: "Gmail sections", "inbox categories", "email organization", "sender filters", "multiple inboxes", "clean up my inbox".
---

# Gmail Multi-Inbox Setup & Maintenance

## Overview

Gmail's Multiple Inboxes displays up to 5 custom sections alongside the main inbox. Each section shows emails matching a search query. This skill uses a **label + filter** approach: label-based sections get Gmail filters that auto-label incoming mail by sender domain. The output is always a Google Apps Script the user pastes into script.google.com.

The generated script is idempotent — safe to re-run after adding or removing senders. When senders are removed from the lists, `setupAll()` automatically deletes the corresponding Gmail filters.

## Prerequisites

This skill requires a **Gmail MCP connector** (e.g. `search_gmail_messages`) to scan the user's inbox. Gmail does not have an official MCP server — the user must have a third-party Gmail connector configured. If no Gmail connector is available, the skill can still work in a limited way: skip the scanning steps and let the user provide sender domains manually, or import from an existing script.

## Configuration

The skill stores its current configuration in `assets/config.json` inside this skill's directory. This file tracks:
- The section definitions (name, query, label)
- The sender domains assigned to each label
- Timestamp of last scan

Always read `assets/config.json` before starting. If it exists, this is a returning user — go to Update Mode. If it doesn't exist, check if the user has an existing script (see Import Existing Script). Otherwise, this is a new user — go to Initial Setup.

## Import Existing Script

If the user already has a Gmail Multi-Inbox Apps Script (set up manually or from a previous run before config tracking existed), ask them to paste it. Parse the script to extract:

1. **Sender arrays** — find all `var xxxSenders = [...]` declarations, extract the domain lists and map each to its label name
2. **Labels** — find all `createLabelIfNeeded('...')` calls to identify the label names
3. **Section config** — find the `__MULTI_INBOX_CONFIG__` comment block or any section query/name comments

Build `assets/config.json` from the parsed data and confirm the reconstructed config with the user before proceeding to Update Mode.

## Initial Setup (New Users)

### Step 1: Scan Gmail

Search the user's Gmail history using `search_gmail_messages` to build a comprehensive picture of who emails them. Run multiple queries and merge the results — the goal is to discover **all** non-personal sender domains.

**Broad sweep (most important — do this first):**
- `newer_than:6m` — all emails from the last 6 months. Paginate through results to collect as many senders as possible.
- `newer_than:1m` — recent emails, captures current high-frequency senders

**Category-based (catches things the broad sweep may paginate past):**
- `category:promotions` — marketing, newsletters
- `category:updates` — notifications, shipping, orders
- `category:social` — social media notifications
- `category:forums` — mailing lists, digests

**Signal-based:**
- `unsubscribe` — anything with an unsubscribe link (broad, catches most automated mail)
- `from:noreply OR from:no-reply OR from:notifications OR from:info@` — automated senders

**Localized subject searches (adapt based on user's language):**
- `subject:order OR subject:invoice OR subject:receipt OR subject:shipping OR subject:confirmation`
- Czech: `subject:objednávka OR subject:faktura OR subject:potvrzení OR subject:doručení`

**Aggregate results:** collect all sender addresses, extract domains, group by domain, count frequency. Ignore generic providers (`gmail.com`, `outlook.com`, `yahoo.com`, `hotmail.com`, `icloud.com`, `seznam.cz`, etc.) — these are personal contacts, not automated senders.

### Step 2: Suggest Categories

Based on the scan results, propose up to 5 sections. Start with these defaults and adjust based on what the scan actually found:

| # | Name | Query | Label | Description |
|---|------|-------|-------|-------------|
| 1 | Important | `(is:starred OR is:important)` | *(none — query-based)* | Starred and important emails |
| 2 | Work | `label:work in:inbox` | `work` | Emails from the user's company domain |
| 3 | Newsletters | `label:newsletter in:inbox` | `newsletter` | Subscriptions, digests, marketing |
| 4 | Orders | `label:orders in:inbox` | `orders` | E-shops, shipping, travel, invoices |
| 5 | *(available)* | | | Suggest based on scan or leave empty |

Present the proposed sections with the discovered sender domains grouped under each category. Ask the user to:
- Confirm, rename, or remove sections
- Move misclassified domains between categories
- Add missing domains
- Name the work label after their actual company if applicable
- Choose label colors (suggest distinct, visually clear defaults). Only Gmail's predefined colors are allowed — see the list in Important Notes

For section 1 (Important): this is query-based, no label or filters needed.

### Step 3: Generate the Apps Script

Read the template from `scripts/gmail-multi-inbox-template.js` in this skill's directory.

Fill in the placeholders:
- `__SENDER_ARRAYS__` — one `var` array per label-based section with the confirmed sender domains
- `__LABEL_CONFIGS__` — `createLabelIfNeeded('labelname', { backgroundColor: '#hex', textColor: '#hex' })` calls for each label-based section. The color object is optional — if the section has a `color` in the config, pass it; otherwise omit the second argument. Only Gmail's predefined hex colors are allowed (see template comments).
- `__STALE_FILTER_CLEANUP__` — a `removeStaleFilters([...])` call listing all managed label/sender pairs. This lets the script detect and delete Gmail filters whose sender was removed from the lists. Example:
  ```
  removeStaleFilters([
    { senders: workSenders, label: 'work' },
    { senders: newsletterSenders, label: 'newsletter' }
  ]);
  ```
- `__FILTER_CREATION__` — for each label-based section: loop over its sender array calling `createFilterIfNeeded(sender, label)`. Do NOT include `retroLabel` calls here — those go in `__RETRO_LABEL__`.
- `__RETRO_LABEL__` — for each label-based section: call `retroLabel(senderArray, label)`. If the section has `matchToAndCc` in the config, pass it as `{ matchToAndCc: [...] }`. This is placed inside the separate `retroLabelAll()` function.
- `__MULTI_INBOX_CONFIG__` — comment block listing each section's query and name for the user to enter in Gmail Settings

Save the generated script as `assets/gmail-multi-inbox-setup.js` inside this skill's directory.

### Step 4: Save Configuration

Write `assets/config.json` with the full configuration:

```json
{
  "sections": [
    { "name": "Important", "query": "(is:starred OR is:important)", "label": null },
    { "name": "Work", "query": "label:work in:inbox", "label": "work", "senders": ["companydomain.com"], "matchToAndCc": ["companydomain.com"], "color": { "backgroundColor": "#4a86e8", "textColor": "#ffffff" } },
    { "name": "Newsletters", "query": "label:newsletter in:inbox", "label": "newsletter", "senders": ["substack.com", "beehiiv.com"], "color": { "backgroundColor": "#fad165", "textColor": "#000000" } },
    { "name": "Orders", "query": "label:orders in:inbox", "label": "orders", "senders": ["amazon.com", "ups.com"], "color": { "backgroundColor": "#16a766", "textColor": "#ffffff" } }
  ],
  "lastScan": "2026-02-18"
}
```

### Step 5: Provide Setup Instructions

Tell the user:

**Part A — Run the script:**

1. Go to **script.google.com** → New project → paste the script
2. In the sidebar, click **+** next to "Services" and enable **Gmail API**
3. Run `setupAll()` and authorize when prompted — this creates labels, updates filters, and retro-labels existing emails

**Part B — Configure Multiple Inboxes manually:**

> The Gmail API does not expose Multiple Inboxes settings, so this part must be done by hand in Gmail.

4. In Gmail: **Settings (⚙️) → See all settings → Inbox tab**
5. Set **Inbox type** to **Multiple Inboxes**
6. For each section, enter the **Search query** and **Section name** exactly as listed in the script's header comment. Present these to the user in a clear table, e.g.:

   | Section | Search query | Section name |
   |---------|-------------|--------------|
   | 1 | `is:starred OR is:important` | Starred / Important |
   | 2 | `label:work in:inbox` | Work |
   | 3 | `label:newsletter in:inbox` | Newsletters |
   | 4 | `label:orders in:inbox` | Orders |
   | 5 | *(leave empty)* | |

7. Set **Multiple Inbox position** to **"Right of inbox"** (recommended)
8. Click **Save Changes**

Always present the full table with the actual section values from the config — do not just say "see the script header".

## Update Mode (Returning Users)

When `assets/config.json` exists:

1. Show the user their current configuration (sections + sender counts)
2. Ask what they want to do: scan for new senders, add specific senders manually, remove senders, modify sections, or get unsubscribe suggestions
3. If scanning: re-run the Gmail searches from Step 1, compare against existing sender lists, and present only **new** domains not yet in the config
4. Let the user confirm which new domains to add and to which categories
5. **Before generating the script**, compare the new sender lists against the previous `assets/config.json`. If any senders were removed, explicitly list them with their section names and ask the user to confirm. The generated script will delete the corresponding Gmail filters when run — make sure the user understands this. Do NOT generate the script until the user confirms the removals.
6. Regenerate the Apps Script with the updated sender lists and save to `assets/gmail-multi-inbox-setup.js`
7. Update `assets/config.json`
8. User pastes the updated script and re-runs `setupAll()` (this handles filters and retro-labeling in one go)
9. If any section queries or names changed, remind the user to update their Multiple Inboxes settings manually in Gmail (see Step 5, Part B from Initial Setup). Present the updated table of sections.

## Unsubscribe Suggestions

When the user asks for inbox cleanup or unsubscribe suggestions:

### Step 1: Identify noisy senders

Search Gmail for senders that pollute the inbox. Focus on:

- **High volume, low engagement** — many emails, most unread. Compare `from:domain.com` (total) vs `is:unread from:domain.com` (unread) to estimate open rate.
- **Never replied to** — `from:domain.com -in:sent` has the same count as `from:domain.com`, meaning the user never interacts with this sender.
- **Promotional / transactional noise** — marketing emails, "we miss you" campaigns, loyalty programs, app notifications that duplicate push/in-app notifications (e.g. social media activity digests, app usage summaries, "someone liked your post").
- **Redundant notifications** — emails that duplicate information available elsewhere: order status (check the app), shipping updates (carrier app), calendar reminders, password change confirmations, login alerts from low-risk services.

Use broad queries to discover candidates:
- `unsubscribe newer_than:6m` — anything with an unsubscribe link in the last 6 months (widest net)
- `category:promotions` — marketing and newsletters
- `category:updates` — transactional notifications
- `category:social` — social media digests and notifications
- `from:noreply OR from:no-reply OR from:notifications` — automated senders
- `subject:newsletter OR subject:digest OR subject:weekly OR subject:monthly`

Then for each discovered domain, measure engagement:
- Total emails: `from:domain.com newer_than:6m`
- Unread emails: `is:unread from:domain.com newer_than:6m`
- Any replies: compare count of `from:domain.com` vs `from:domain.com -in:sent`

Exclude senders already managed in the config (they're already categorized).

### Step 2: Present recommendations

Group the noisy senders into tiers:

1. **Unsubscribe** — high volume, never read, no value (e.g. marketing from a store you bought from once, app notification digests)
2. **Consider unsubscribing** — moderate volume, rarely read, value is questionable or available elsewhere
3. **Keep but categorize** — useful but noisy — suggest adding to a section in the multi-inbox config instead

For each sender, show:
- Sender domain and example "From" name
- Email count (last 6 months)
- Estimated open rate (read vs total)
- Why it's flagged (e.g. "94 emails, 2% opened", "duplicates push notifications")

### Step 3: Act on user choices

- **Unsubscribe**: the action is manual — provide the sender info so the user can unsubscribe themselves. Do NOT generate script code to delete or archive emails without explicit user approval.
- **Categorize**: add the sender to the appropriate section in the config and regenerate the script.
- **Block**: explain how to block in Gmail (three dots → Block "sender"). This is also manual.

## Important Notes

- **The Gmail API cannot configure Multiple Inboxes settings.** The script handles labels, filters, and retroactive labeling. The user must always configure section queries, names, and position manually in Gmail Settings → Inbox → Multiple Inboxes. Always present the full configuration table after generating or updating the script.
- Emails in labeled sections also appear in the main inbox — sections are views, not separate inboxes. Adding `in:inbox` to section queries ensures archived mail doesn't appear in sections.
- `from:domain.com` matches any `@domain.com` address and subdomains.
- One filter per sender domain (no complex boolean logic in a single Gmail filter).
- Check the user's email for language clues and adapt search queries accordingly.
- **Label colors must use Gmail's predefined hex values.** Arbitrary colors will be rejected by the API. Allowed background colors (pair with `#000000` or `#ffffff` text for contrast):
  - Reds: `#fb4c2f`, `#e66550`, `#cc3a21`, `#ac2b16`, `#822111`, `#f6c5be`, `#efa093`
  - Oranges: `#ffad47`, `#ffbc6b`, `#eaa041`, `#cf8933`, `#a46a21`, `#ffe6c7`, `#ffd6a2`
  - Yellows: `#fad165`, `#fcda83`, `#f2c960`, `#d5ae49`, `#aa8831`, `#fef1d1`, `#fce8b3`
  - Greens: `#16a766`, `#44b984`, `#149e60`, `#0b804b`, `#076239`, `#b9e4d0`, `#89d3b2`, `#43d692`, `#68dfa9`, `#3dc789`, `#2a9c68`, `#1a764d`, `#c6f3de`, `#a0eac9`
  - Blues: `#4a86e8`, `#6d9eeb`, `#3c78d8`, `#285bac`, `#1c4587`, `#c9daf8`, `#a4c2f4`
  - Purples: `#a479e2`, `#b694e8`, `#8e63ce`, `#653e9b`, `#41236d`, `#e4d7f5`, `#d0bcf1`
  - Pinks: `#f691b3`, `#f7a7c0`, `#e07798`, `#b65775`, `#83334c`, `#fcdee8`, `#fbc8d9`
  - Grays: `#000000`, `#434343`, `#666666`, `#999999`, `#cccccc`, `#efefef`, `#f3f3f3`, `#ffffff`
