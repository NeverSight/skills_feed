---
name: onboarding-user
description: Onboards a new user — sets up their brand for the first time from their website. Analyzes the brand, finds its competitors, and saves both to the company profile that every later session reads from. Use when the user wants to onboard, get started, or set up their brand or company profile. Not for just analyzing a brand from its website — that is analyzing-brand.
license: Apache-2.0
metadata:
  version: "0.2.0"
  category: creative
  summary: "Sets your brand up from one link. Give it your website and it works out who you are — your voice, your audience, what you sell — finds who you compete with, and writes both where every future session will find them."
---

# Onboarding

Turn one website into a working brand profile, then hand the user their first next steps.

## Workflow

### Step 1: Get the website

Ask for the user's website, unless the conversation already carries it.

A user with no website still onboards. Ask what the brand is called, what it sells, and who buys it — plus anything they want to add about how it sounds or what sets it apart. A short answer is fine; they can give as much or as little as they like. Write what they give into the matching sections of `brand.md` in `./supercmo-company`, leave the sections they didn't cover marked `unconfirmed — needs user input`, then skip the rest of the steps.

### Step 2: Analyze the brand

Trigger the `analyzing-brand` skill in quick mode with the website. It writes `./supercmo-company/brand.md` itself. Don't copy or re-save it; read it back where you need its contents for the summary.

### Step 3: Identify the competitors

Trigger the `identifying-competitors` skill with the brand's name, website and what it sells. **Say the run is write-first** so it saves the shortlist without pausing to confirm. It writes `./supercmo-company/competitors.md` itself. Don't copy or re-save it.

### Step 4: Show what was written

**One summary for the whole run.** Compact — not the files read back:

- The brand: its name and what it sells, in a line.
- The voice, in a sentence.
- The audience, as the site evidenced it.
- The competitors, as a plain list.
- Everything marked `unconfirmed — needs user input`, so the gaps are visible rather than silent.

Then invite corrections, and apply each one directly to the file in `./supercmo-company`. **Corrections are edits** — patch the section that changed. Don't re-analyze the site, and don't re-run the sub-skill, to apply a correction.

### Step 5: Suggest what to do next

Close with this list:

- **Create a UGC video** — a creator-style video for your product.
- **Create a product ad video** — a produced ad or commercial for your product.
- **Generate product photos** — packshots and lifestyle shots from one product photo.
- **Research competitor ads** — what's working in your category, and what nobody runs.

## Edge cases

- **`error: "no_provider_configured"`** on any tool → relay the tool's `hint` (the user must set their key).
- **The brand is already onboarded** — `brand.md` exists in `./supercmo-company` → don't re-run the analysis. Summarize what is stored and ask whether anything needs updating. Still run Step 3 where `competitors.md` is missing: a half-finished onboarding gets completed, not restarted.
- **A sub-skill comes back empty** — the site won't extract, search names nobody → carry on with the steps that can run, say plainly what is missing, and still give the summary and the next steps.
- **The site won't load at all** → don't guess the brand from its name. Ask for a working URL, or handle it as the no-website case in Step 1.
- **The user asks to skip** → stop, and say the brand can be set up any time by asking. Don't leave a partial profile behind.
