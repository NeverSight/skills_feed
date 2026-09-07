---
name: analyzing-own-ads
description: Audits the ads a company is running itself — what's live now, what it has already stopped, and which have run longest. Watches the video ads and reads the image ads with a vision model, then maps what the account already covers — the angles, hooks, formats and offers — what was dropped and how fast, and which long-runners have nothing newer beside them. Read from the public ad library, so it carries run lengths rather than spend or results. Research only — nothing is generated or changed here. Use when the user wants their own ads audited, wants to know what they are running, which of their ads is holding, what they already cover, or whether anything is going stale.
license: Apache-2.0
metadata:
  version: "0.1.2"
  category: creative
  summary: "Audits your own advertising the way you would a competitor's — pulling every ad you run from the public library and watching the creative the whole way through. You get the map of what you already cover: which angles, hooks and formats you run, which ads have held longest, what you quietly stopped and how fast, and which winners are still carrying the account with nothing newer built beside them."
---

# Own ads

Audit what a company is advertising itself, work out what is holding, and map what it already covers.
**Research only — nothing is generated, posted or planned here.**

Not for competitors' ads — that is `researching-competitor-ads`; not for deciding what to make next —
that is `planning-campaigns`.

## Workflow

### Step 1: Settle whose page this is

You need **a brand name and a website**.

- **Read them from the brand profile** in `./supercmo-company`, where
  one exists. Where it doesn't, move on.
- **Ask the user** for whichever is missing.
- **A website but no name** → take the brand name off the site and carry on.

### Step 2: Scope the run

Ask once, bundled into a single message, always with a free-text way out. Skip any of these the brief
already answers.

| Ask | When | How |
| --- | --- | --- |
| **The country the ads run in** | The brief names no market and the user's own site implies none. | Offer the likely markets, and a way to type another. |
| **How deep to go** | The brief doesn't say. | Offer the quick scan first and recommend it; say a detailed audit doubles what is watched, and costs accordingly. |
| **What they want to learn** | Optional, and only where the brief says nothing at all about what the audit is for. | **One open field, no options to choose from.** Ask what they want to come away knowing. |

**Take whatever the brief says about what they are after, in their own words, and don't ask again.**
Carry those words through to the audit, which closes by answering them.

Where nothing is given and nothing is answered, run it neutrally: a quick scan, the market the user's
own site sells to, and an audit that says no goal was set. Say in one sentence what you took, and
keep going.

Step 4's script holds these numbers and enforces them — pass it the depth and don't re-count.

| Depth | Ads kept, live / stopped | Ads watched, live / stopped |
| --- | --- | --- |
| Quick scan | 30 / 30 | 10 / 10 |
| Detailed audit | 60 / 60 | 20 / 20 |

### Step 3: Pull the ads

Read `references/pulling-own-ads.md` and follow it. Pull the live set and the stopped set separately,
and keep them apart.

Every pull is written to a response file, and the call returns its path in `saved.path`. All of a
run's responses land in one directory — **note that directory**, it is Step 4's only input. Read
`saved.cursor` for the next page. Don't take the ads apart yourself.

### Step 4: Build the ledger

Run the script over the directory the responses were saved to:

```bash
python3 <skill-dir>/scripts/build_ledger.py <responses-dir> --depth <quick|detailed> --out <saved.output_dir>
```

`--depth` is what Step 2 settled. `--out` is `saved.output_dir`, the same on every response of the
run — the folder the tool set aside for it. Run the script by its full path rather than moving into
the skill directory. **Every file this run produces goes in that folder.**

**Read `ledger.md`.** It holds the counts and campaigns, the ads to watch with their media URLs, the
copy every ad ran with — grouped so repeated wording shows as repeated — and the row behind every ad.
Say in one line how many ads are in the ledger and how many are marked to watch, then carry on —
don't stop for approval. The cap lines at the top of the file go into the audit's coverage section
verbatim.

### Step 5: Watch the ads

Read `references/reading-one-ad.md` and follow it.

`ledger.md`'s **Watch these** section lists each ad's `ref` and its media URL, split into videos and
stills. Send them in batches of at most ten — `video_analysis` for the videos, `image_analysis` for
the stills. They are watched in parallel, so a batch takes about as long as its slowest ad.

**Write each teardown to `per-ad-teardowns.md` in the run's folder, as its batch comes back** — the
`ref` as a heading, then the teardown verbatim. Never watch the same `ref` twice, and never watch an
ad the ledger didn't mark.

### Step 6: Read the set and write the audit

Read `references/reading-own-ads.md` and follow it. It writes `own-ads-audit.md` into the run's
folder.

Name the patterns from the teardowns, then check them **against the ledger**, citing `ref`s and
counts. A claim with no `ref`s behind it doesn't go in.

**Audit the whole ledger, not only the ads you watched.** Every row carries run length, status,
format, campaign and call-to-action, so the run-length distribution, the format mix and the campaign
structure are drawn from all of them — including the rows marked `no (outside the watch allowance)` or
`no (same creative as an ad already watched)`. Only findings about how an ad is built come from the
teardowns, and those are counted over the ads actually read.

The ads read are the longest-running, live and stopped taken separately. That is a sample of the long
end, not of the whole set — so the newest ads are in the ledger but mostly unwatched, and any claim
about what the account is trying now rests on metadata and copy.

### Step 7: Hand it over

The run's folder holds `ledger.md`, `per-ad-teardowns.md` and `own-ads-audit.md`.

**Open the reply by answering the user's question, in their words.** Use what they asked for in the
brief, or what they said at Step 2.

**If they never asked for anything specific, give what is covered** — the axes the account already
runs, with counts, and the ones with nothing on them.

Back the answer with the two or three findings from the audit it rests on, each with its count and
`ref`s. Nothing else from the audit goes in the reply — it is on disk. Close with the folder.

## Edge cases

- **`error: "no_provider_configured"`** on any tool → relay the tool's `hint` (the user must set their key).
- **A pull comes back empty under the market filter** → record it as empty for that market. Don't
  re-pull without `country`.
- **`search_companies` returns a reseller or a similarly-named business** → show the candidates and
  let the user pick. A misattributed own ad reports creative they have never run.
- **`build_ledger.py` says a response is unprojected** → that pull went out without `trim: true`,
  which is the default. Pull it again with `trim: true` and re-run the script.
- **The ledger holds an advertiser this run never asked about** → the responses directory carries an
  earlier run's pulls. Pass this run's response files instead of the directory; the script takes a
  list of paths.
- **`build_ledger.py` reports fewer ads than you pulled** → a response in the directory failed or came
  back empty and was skipped. Open the first lines of each file to find it, relay what it says, and
  re-run that pull.
- **`video_analysis` rejects a clip as too large**, or **an ad's creative can't be fetched** → record
  that `ref` as unwatched in `per-ad-teardowns.md` and name it in the audit's coverage. The row
  stays in the ledger and in every count that comes off metadata.
- **The user asks for spend, CPA, ROAS, CTR or any real result** → not here. The public library
  carries none of it. Say so plainly and offer the run-length proxy instead.

## Scripts

- `scripts/build_ledger.py` — reads the run's responses and writes `ledger.md` (Step 4). Python 3, standard library only; `--help` gives the full usage.

## Reference

- `references/pulling-own-ads.md` — reaching the brand's own page and pulling what it runs: the endpoints and their accepted values, proving the page is the brand's own and not a reseller's, paging deep enough to reach the long-runners, getting the retired ads, what each ad comes back carrying, and the traps that bill for nothing (Step 3).
- `references/reading-one-ad.md` — the prompts sent to the vision model for a video and for a still, and how each teardown is recorded (Step 5).
- `references/reading-own-ads.md` — turning the teardowns and the ledger into `own-ads-audit.md`: coverage and limits, naming a pattern rather than assuming one, the lines of inquiry, how much evidence a conclusion needs, and closing without recommending (Step 6).
