---
name: researching-competitor-ads
description: Analyzes the ads competitors are running — the ones live now, the ones they have already stopped, and which have run longest. Watches the video ads and reads the image ads with a vision model, so every finding comes from the ad itself rather than its caption. Finds the patterns across the set — what is holding, what was dropped, and what nobody runs. Research only — nothing is generated or recommended here. Use when the user wants competitor ads researched, an ad teardown, a competitive or category analysis, to see what ads a named brand is running, or to find what is working and what nobody has tried yet.
license: Apache-2.0
metadata:
  version: "0.3.2"
  category: creative
  summary: "Analyzes what your competitors are advertising and shows you what is actually working — the ads that have run longest, the ones they quietly dropped, and what the winners have in common. A vision model watches the image and video ads that carry the signal — the long-runners, the ones just launched, the ones they dropped — the whole way through. So you learn how each one is built: the hook, the pacing, when the product lands, the proof and the offer. You also get the angles nobody in your category has taken."
---

# Competitor ads

Analyze what competitors are advertising, work out what is holding, and map what the category
covers. **Research only — nothing is generated, posted or planned here.** Deciding what to make
next is `planning-campaigns`' job.

## Workflow

### Step 1: Settle who the competitors are

Three ways to find out. Try them in order, and stop at the first one that works.

- **Read them from `competitors.md`** in `./supercmo-company`. Where it
  is absent or empty, move on.
- **Ask the user**, for a name and a website for each competitor.
- **Find candidates**, only where the user doesn't know. Call `url_extraction` on the user's own
  website to learn what they sell in their own words, then `social_research` on `meta_ad_library` /
  `search_ads` using those words. Each ad names the advertiser who ran it. Show the user a plain list
  of those advertiser names with the number of ads each appeared on, most ads first — nothing else —
  and ask which are real competitors.

You need **a name and a website** for each competitor whichever route you take. Step 3 uses the domain
to prove the ads came from the right company.

### Step 2: Scope the run

Ask once, bundled into a single message, always with a free-text way out. Skip any of these the brief
already answers.

| Ask | When | How |
| --- | --- | --- |
| **The country the ads run in** | The brief names no market and the user's own site implies none. | Offer the likely markets, and a way to type another. |
| **How deep to go** | The brief doesn't say. | Offer the quick scan first and recommend it; say a detailed analysis doubles what is watched per competitor, and costs accordingly. |
| **What they want to learn** | Optional, and only where the brief says nothing at all about what the research is for. | **One open field, no options to choose from.** Ask what they want to come away knowing. |

**Take whatever the brief says about what they are after, in their own words, and don't ask again.**
Carry those words through to the analysis, which closes by answering them.

Where nothing is given and nothing is answered, run it neutrally: a quick scan, the market the user's
own site sells to, and a report that says no goal was set. Say in one sentence what you took, and
keep going.

Every number is per competitor, so a run costs what it costs times the number of competitors. Step
4's script holds them and enforces them — pass it the depth and don't re-count.

| Depth | Ads kept, live / stopped | Ads watched, live / stopped |
| --- | --- | --- |
| Quick scan | 30 / 30 | 10 / 10 |
| Detailed analysis | 60 / 60 | 20 / 20 |

### Step 3: Pull each competitor's ads

Read `references/pulling-competitor-ads.md` and follow it. Pull the live set and the stopped set
separately, and keep them apart.

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

**Read `ledger.md`.** It holds the counts and campaigns per competitor, the ads to watch with their
media URLs, the copy every ad ran with — grouped so repeated wording shows as repeated — and the row
behind every ad. Say in one line how many ads are in the ledger and how many
are marked to watch, then carry on — don't stop for approval. The cap lines at the top of the file
go into the analysis's coverage section verbatim.

### Step 5: Watch the ads

Read `references/reading-one-ad.md` and follow it.

`ledger.md`'s **Watch these** section lists each ad's `ref` and its media URL, split into videos and
stills. Send them in batches of at most ten — `video_analysis` for the videos, `image_analysis` for
the stills. They are watched in parallel, so a batch takes about as long as its slowest ad.

**Write each teardown to `per-ad-teardowns.md` in the run's folder, as its batch comes back** — the
`ref` as a heading, then the teardown verbatim. Never watch the same `ref` twice, and never watch an
ad the ledger didn't mark.

### Step 6: Read the set and write the analysis

Read `references/reading-the-set.md` and follow it. It writes `ad-set-analysis.md` into the run's
folder.

Name the patterns from the teardowns, then check them **against the ledger**, citing `ref`s and
counts. A claim with no `ref`s behind it doesn't go in.

**Analyse the whole ledger, not only the ads you watched.** Every row carries run length, status,
format, campaign and call-to-action, so the run-length distribution, the format mix and the campaign
structure are drawn from all of them — including the rows marked `no (outside the watch allowance)`
or `no (same creative as an ad already watched)`. Only findings about how an ad is built come from
the teardowns, and those are counted over the ads actually read.

The ads read are each competitor's longest-running, live and stopped taken separately. That is a
sample of the long end, not of the whole set — so the newest ads are in the ledger but mostly
unwatched, and any claim about what a competitor is trying now rests on metadata and copy.

### Step 7: Hand it over

The run's folder holds `ledger.md`, `per-ad-teardowns.md` and `ad-set-analysis.md`.

**Open the reply by answering the user's question, in their words.** Use what they asked for in the
brief, or what they said at Step 2.

**If they never asked for anything specific, give what the category covers** — the patterns that
dominate, each with its counts, and the space nobody runs.

Back the answer with the two or three findings from the analysis it rests on, each with its count and
`ref`s. Nothing else from the analysis goes in the reply — it is on disk. Close with the folder.

## Edge cases

- **`error: "no_provider_configured"`** on any tool → relay the tool's `hint` (the user must set their key).
- **A pull comes back empty under the market filter** → record it as empty for that market. Don't
  re-pull without `country`.
- **`build_ledger.py` says a response is unprojected** → that pull went out without `trim: true`,
  which is the default. Pull it again with `trim: true` and re-run the script.
- **The ledger holds a competitor this run never asked about** → the responses directory carries an
  earlier run's pulls. Pass this run's response files instead of the directory; the script takes a
  list of paths.
- **`build_ledger.py` reports fewer ads than you pulled** → a response in the directory failed or came
  back empty and was skipped. Open the first lines of each file to find it, relay what it says, and
  re-run that pull.
- **`video_analysis` rejects a clip as too large**, or **an ad's creative can't be fetched** → record
  that `ref` as unwatched in `per-ad-teardowns.md` and name it in the analysis's coverage. The row
  stays in the ledger and in every count that comes off metadata.
- **`url_extraction` isn't available** → Step 1's discovery route can't run; ask the user instead.
- **Discovery returns advertisers unrelated to the category** → drop that route and ask the user.
- **The user gives a website but no name** → take the brand name off the site and carry on.

## Scripts

- `scripts/build_ledger.py` — reads the run's responses and writes `ledger.md` (Step 4). Python 3, standard library only; `--help` gives the full usage.

## Reference

- `references/pulling-competitor-ads.md` — reaching the right advertiser and pulling what it runs: the endpoints and their accepted values, proving the page belongs to the competitor, paging deep enough to reach the long-runners, what each ad comes back carrying, and the traps that bill for nothing (Step 3).
- `references/reading-one-ad.md` — the prompts sent to the vision model for a video and for a still, and how each teardown is recorded (Step 5).
- `references/reading-the-set.md` — turning the teardowns and the ledger into `ad-set-analysis.md`: coverage and limits, naming a pattern rather than assuming one, the lines of inquiry, how much evidence a conclusion needs.
