---
name: ofox-video-core
description: Shared execution layer for the Ofox video generation API (api.ofox.ai) — creates a video job, polls it to completion, downloads the finished mp4 from a persistent CDN URL, and reports the real cost. This is a library skill, not a standalone user-facing one — it is invoked by scenario skills such as seedance-short-drama, seedance-ad-creative, and seedance-product-video, which build model/prompt/resolution choices for a specific use case and then call into this skill's script rather than re-implementing the API calls. Load this skill directly only when a user explicitly names the Ofox video API, asks to call it with specific low-level parameters, or asks to debug/resume a stuck or failed Ofox video job by job id — for a plain scenario request ("make me a short drama scene", "generate a cinematic ad clip"), use the relevant scenario skill instead, which itself depends on this one.
license: MIT
version: "1.9.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/ofox-video-core
metadata:
  author: ofoxai
  version: "1.9.0"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "🎬"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/ofox-video-core
---

# ofox-video-core: Ofox video API execution layer

Wraps the Ofox video generation API (`https://api.ofox.ai/v1/videos`) behind
one script: submit a job, poll it to a terminal state, download the result,
report the exact cost. Scenario skills (`seedance-short-drama`,
`seedance-ad-creative`) call into this rather than duplicating API logic.

## Safety contract (non-negotiable)

- `OFOX_API_KEY` is read **only from the shell environment** — never from a
  dotenv file, never hardcoded in a script or a skill file.
- **Never print, log, or echo the raw key value** — not in chat, not in a
  file, not in a command you show the user, not in verbose curl output.
  `references/ofox-video.sh` never uses `curl -v`/`--trace` for exactly this
  reason (those would print the `Authorization` header). If you need to
  show that a key is configured, say "OFOX_API_KEY is set" — never the value.
- Never write the key into any file this skill (or a skill built on it)
  creates, including logs, cost reports, or committed code.
- **Check once, then proceed.** Run the availability/key check at most once
  per session (see below). If it passes, don't re-prompt for the key on
  every subsequent call in that session.
- **Fail open on a missing key** — guide the user to get one, don't dead-end
  the conversation. A missing key means "can't call the paid API yet," not
  "stop talking to me."

## Which model, and what it costs

`bash references/ofox-video.sh models` lists every video model Ofox serves with
its real duration range, resolutions, modes and base per-second price. It needs
**no API key** — `GET /v1/models` is public — so it is safe to run before the
user has signed up, and it costs nothing.

Worth knowing before quoting a price: at 720p text-to-video the ladder runs
`seedance-2.0-mini` 4 cents/s → `wan-2.7` 10 cents/s → `seedance-2.5` 24 cents/s. When
a user is going to generate several takes and keep one, drafting on a cheap
model and rendering the keeper on `seedance-2.5` costs a fraction of drafting
everything on 2.5. Say so when it's relevant — but don't switch models on
someone's behalf, since the model changes the look, not just the price.

Parameter limits differ per model and the script enforces the real ones
(`wan-*` is 2-15s and 720p/1080p only; `seedance-2.5` is 4-30s and the only one
with `21:9`/`4:3`/`3:4`). The limits come from the live model list, cached for
24 hours, falling back to a bundled snapshot when offline — a fallback is
always announced on stderr, never silent.

## Multi-shot sequences (`chain`)

One job is one continuous take, so a sequence means several jobs — and
separate jobs share nothing, so the set, lighting and framing drift between
them. `chain` carries each shot's closing frame into the next one as its
opening frame:

```bash
bash references/ofox-video.sh chain \
  --shot "a white cup on a dark table, steam rising, static camera" \
  --shot "the camera pushes in slowly toward the same cup" \
  --duration 4 --resolution 480p
```

Or `--shots-file shots.txt`, one prompt per line (blank lines and `#`
comments ignored). Capped at 10 shots per run.

**Verified behavior**: shot 2 opens on very nearly the exact frame it was
fed — cup position and scale, window frame, table grain, light direction all
carried over — and then follows its own prompt from there. This is real
continuity, not just matched framing. Brightness can shift slightly across a
seam.

What it does:

- Estimates the whole sequence before spending, then reports real per-shot
  cost from each job's `usage.video_cost`.
- **Stops on the first failure.** Shots already generated are kept, downloaded
  and listed with their real cost; the remaining shots are never submitted.
- Joins the finished shots into one file with ffmpeg (`--no-concat` to skip),
  re-encoding only if the clips' codecs differ. Fails open: no join, never a
  lost shot.
- Shot 1 takes a normal `--aspect-ratio`. Shots 2+ are image-to-video, which
  Seedance 2.5 requires to be `adaptive`, so they inherit framing from the fed
  frame — which is what keeps the sequence dimensionally consistent.

`chain` needs `ffmpeg`, and checks for it **before** submitting anything, so
a missing dependency never costs a paid shot.

### The one hard limit: no real people

**Seedance 2.5 image-to-video rejects reference frames containing a real
person** — `HTTP 400 / input_moderation_failed`, "may contain real person".
Nothing is generated and nothing is billed, but the chain stops there.

So chaining works for products, landscapes, illustration and anime, and
**does not work for live-action human sequences** on this model. That is why
`seedance-anime-drama` can reuse a character sheet across shots while a
short-drama sequence cannot. `--real-person true` exists for authorized
real-person references and Ofox documents it for `bytedance/seedance-2.0`;
whether it lifts the restriction on 2.5 is untested here — don't promise it.

### Extracting a frame on its own

```bash
bash references/ofox-video.sh last-frame clip.mp4 [--out-dir DIR]
```

No API call, no key, no cost. Grabs a frame just before the end (the literal
final frame is often a fade), for feeding into a later `generate` by hand.

## Generating several takes (`batch`)

Video generation is a slot machine: you generate several, keep one. `batch`
makes that one command, and — the part nobody else does — tells you what it
actually cost.

```bash
bash references/ofox-video.sh batch --prompt "..." --takes 3 [OPTIONS]
```

Every option `generate` takes works here. What `batch` adds:

- **An estimate before it spends anything**, and a real total afterward built
  from each job's own `usage.video_cost` — never from the estimate.
- **Every take reports its seed** (`TAKE 3 <job-id> seed=1852049 <cost> <path>`).
  This is what makes "take 3 was the good one" actionable: the takes differ
  only by seed, so re-running the same prompt with that seed on a better model
  or a higher resolution reproduces that take rather than rolling a new one.
  Without the seed there is no way back to a specific take, only a reroll.
- **`BATCH_COST_TOTAL` is the number to quote**, not `BATCH_COST_PER_TAKE`.
  Gacha means most takes go in the bin: if one take in three is usable, that
  clip cost you the whole total, because you paid for the two you threw away.
  `BATCH_COST_PER_TAKE` is just the total divided by the count — useful for
  sanity-checking the bill, misleading as a cost-per-usable-clip figure. The
  total is what compares meaningfully across models and settings.
- **A contact sheet** (`--no-contact-sheet` to skip): three frames from each
  take, tiled one row per take, so a human can pick a winner from one image
  instead of opening N files. Needs `ffmpeg`; without it the sheet is skipped
  with a reason and the videos are untouched.
- **A stop on first failure.** If take 2 fails, takes 3..N are not submitted.
  Whatever broke it will almost certainly break the rest, and each attempt is
  real money.
- **A warning if you pass `--seed`**, since a fixed seed means you may be
  paying N times for N identical clips.

Takes run one at a time, each as its own job through the same path a single
`generate` uses. That is slower than firing N creates at once, and it is the
right trade: the no-resubmit rule stays intact for free, and nothing here can
double-bill a request that already exists.

`--takes` is capped at 10 per run.

### The pattern worth suggesting

Draft cheap, render the keeper expensive:

```bash
# 5 drafts at 480p on the cheapest model — about 40 cents
bash references/ofox-video.sh batch --prompt "..." --takes 5 \
  --model bytedance/seedance-2.0-mini --resolution 480p --duration 4

# then the winner, on the good model
bash references/ofox-video.sh generate --prompt "<the one that worked>" \
  --model bytedance/seedance-2.5 --resolution 1080p --duration 4
```

The same five drafts on `seedance-2.5` at 720p would be $4.80. Offer the
ladder — but let the user choose the model, since a different model is a
different look, not just a different price.

### Re-tiling videos you already have

```bash
bash references/ofox-video.sh contact-sheet clip1.mp4 clip2.mp4 [--out-dir DIR]
```

No API call, no key, no cost. Useful for comparing takes from separate runs,
or rebuilding a sheet you skipped.

## How long this blocks, and why that matters

`generate` waits for the job: it polls until the video is ready, up to
`--max-wait` seconds (default **540**, i.e. nine minutes). A 4-second 480p clip
usually lands in one to three minutes; longer and higher-resolution jobs take
longer.

**That is longer than most agent tool calls allow by default.** Claude Code's
Bash tool defaults to a 120-second timeout and caps at 600. If your tool call
dies while `generate` is still polling, you land in the one genuinely bad
state: the job was created and is billable, and its id was never printed, so
you cannot poll for it and cannot tell the user where their video went.

Two ways to stay out of that, in order of preference:

**1. Submit and wait separately.** `create` does the submit and returns
immediately — seconds, not minutes — printing the job id. Then poll in
however many short calls it takes:

```bash
bash references/ofox-video.sh create --prompt "..." --duration 15 --out-dir ./out
# -> STATUS submitted
#    JOB_ID 7b41f0c9-...
#    POLLING_URL https://api.ofox.ai/v1/videos/7b41f0c9-...

bash references/ofox-video.sh poll 7b41f0c9-... --out-dir ./out
```

The job id exists on disk in your transcript the moment it is created, so no
timeout can strand it. This is the right shape whenever you cannot raise your
own tool timeout.

**2. Raise the timeout for the call.** If your harness lets you set a
per-call timeout, give `generate` at least `--max-wait` plus a margin.

**`batch` needs this attention most.** Its takes run one at a time, so its
worst case is `takes x max-wait` — four takes at the default is 36 minutes,
which exceeds what any single Bash tool call can be given. Either lower
`--max-wait` (a 4-second draft rarely needs 540s; 240 is generous), or run
`create` per take and poll them yourself. Tell the user roughly how long it
will take before starting.

## Quote the price before you spend it

`generate`, `batch` and `chain` all take **`--dry-run`**: they parse arguments,
validate every parameter against the chosen model, resolve the upstream, build
the payload and print the cost estimate — then stop. No request is sent and
nothing is billed.

That flow is the one to follow whenever real money is involved:

```bash
# 1. price it
bash references/ofox-video.sh generate --dry-run --prompt "..." --duration 15 --resolution 720p
#    -> Estimated cost: ~$3.60 (15s x 24 cents/s)...
#    -> DRY RUN — nothing was submitted and nothing was billed.

# 2. tell the user the number, get a yes

# 3. run the identical command without --dry-run
```

**Do not skip step 2.** The estimate a real run prints appears microseconds
before the request goes out — by the time you could relay it, the job exists
and is billable. `--dry-run` is what makes quoting-then-confirming possible.

A dry run also catches a bad parameter for free, so an invalid combination
costs a message instead of a job.

Every run prints exactly one `Estimated cost:` line, including when it cannot
compute one — it says why (no `--duration`, or no verified rate for that
model/resolution). Relay whichever line you get; never substitute a number of
your own, and never present an estimate as the bill.

## Which upstream serves the job

Seedance is served by two upstreams, and by default Ofox picks one by weight —
its docs say outright that "which provider serves any single request is not
predictable". They moderate differently, so an unpinned job that comes back
`output_moderation_failed` may just have landed on the stricter one, with
nothing for the user to point at.

**This skill pins Seedance to `byteplus`.** No flag needed, no network call to
decide it.

| | `volcengine` | `byteplus` (default) |
|---|---|---|
| Platform | Volcengine Ark, mainland China | BytePlus, markets outside mainland China |
| Moderation | Standard | More permissive |
| Price | identical | identical |

Pricing is identical across the two — this is a region and moderation choice,
never a cost one. Say so if a user asks which is cheaper.

```bash
bash references/ofox-video.sh generate --provider volcengine ...  # mainland
bash references/ofox-video.sh generate --provider auto ...        # let Ofox route
export OFOX_VIDEO_PROVIDER=volcengine                             # persistent default
bash references/ofox-video.sh providers                           # see a model's upstreams
```

Models with only one upstream (`alibaba/*` today) get no pin — routing there
is already deterministic.

If a job fails `output_moderation_failed`, retrying on the other upstream is a
real fix and is worth offering: the rejected job was never billed, and a retry
is a new request, not a resubmission.

## No key? You can still get a price

`models`, `providers` and any `--dry-run` all work with `OFOX_API_KEY` unset.
They hit public endpoints or make no request at all, so someone who has not
signed up can price a job, compare resolutions, and cost out a batch before
deciding whether to register.

**When a user has no key, quote first and point at signup second.** Opening
with "go get an API key" sends someone to a form before they know whether the
thing is worth 44 cents or $7.20. Run the dry run, show them the number, then
point at [app.ofox.ai](https://app.ofox.ai) if they want to proceed.

## Availability check

Before the first call in a session, verify the environment:

```bash
bash references/ofox-video.sh check
```

This checks `curl`, `jq`, and `OFOX_API_KEY` and exits `0` only if all three
are present — it makes no network call. Handle each failure mode plainly:

- **`curl` missing** (rare — usually preinstalled): `brew install curl`
  (macOS) or `sudo apt-get install curl` (Debian/Ubuntu), else
  https://curl.se/download.html.
- **`jq` missing**: `brew install jq` (macOS) or `sudo apt-get install jq`
  (Debian/Ubuntu), else https://jqlang.org/download/.
- **`OFOX_API_KEY` missing**: tell the user to get one at
  `https://app.ofox.ai` (log in → Settings → API Keys → Create New Key,
  shown once), then `export OFOX_API_KEY=...` in their shell. Offer this
  once, plainly, and move on — don't repeat the pitch on every message.

## Invoking the script

```bash
bash references/ofox-video.sh models
bash references/ofox-video.sh generate --dry-run --prompt "..." [OPTIONS]
bash references/ofox-video.sh generate --prompt "..." [OPTIONS]
bash references/ofox-video.sh poll JOB_ID [--out-dir DIR] [--name TEXT]
```

`generate` builds the request, validates parameters client-side against the
chosen model's real limits (rejecting a bad `resolution`/`aspect_ratio`/
`duration` before any network call), submits it, polls to a terminal state,
downloads the video into `--out-dir` (default: the current directory), and
prints:

```
STATUS completed
JOB_ID <id>
VIDEO_PATH <path/to/file.mp4>
SIDECAR_PATH <path/to/file.json>
VIDEO_SECONDS <billed seconds>
VIDEO_COST <exact cost from usage.video_cost>
```

## Name the output file

Pass `--name` with a short description of what the clip actually is:

```bash
bash references/ofox-video.sh generate --prompt "..." --name "convenience store breakup"
```

The file lands as `convenience-store-breakup-d12c2787.mp4` instead of a bare
job id, with a `convenience-store-breakup-d12c2787.json` sidecar beside it.

Without `--name` the slug is derived from the prompt, so a `poll JOB_ID` run
in a fresh shell still produces something readable. That fallback is a
consolation prize, not the goal: prompts open on setting and lighting, so the
derived name usually describes the room rather than the scene. **A scenario
skill always knows the better name — pass it.**

The 8-hex suffix keeps two runs of the same prompt from overwriting each
other. It is not a way back to the job: the API has no list endpoint, so a
short id cannot be expanded. The sidecar carries the full `job_id`, the
prompt, the real cost, and the `request` as submitted — the only place
`resolution`, `aspect_ratio` and `seed` are recorded, since the poll response
echoes none of them. Full field table in
[`references/api-params.md`](references/api-params.md).

## Reproducing a shot

Every job now has a seed: without `--seed` the script rolls one, sends it,
and prints it as `SEED <n>`. Before, the server picked a seed and reported it
nowhere, so nothing could be regenerated — only re-rolled.

That seed and the rest of the request land in the sidecar, so re-rendering
the same shot at a higher resolution is a matter of reading it back:

```bash
jq -r '.request | "--prompt \(.prompt|@sh) --seed \(.seed) --aspect-ratio \(.aspect_ratio)"' out/my-shot-3e830902.json
```

`create` + `poll` keeps this intact across the two processes by leaving the
payload in `<out-dir>/.ofox-request-<job id>.json` for the poll to pick up
and clean away. Poll into a different `--out-dir` and the handoff is simply
not found — the sidecar omits `request`, nothing fails.

A sidecar that cannot be written is a warning, never a failed download — the
video is what the user paid for.

Download source: `mirror_urls` (CDN-signed, persistent) when present,
falling back to `unsigned_urls` (documented as temporary, may expire within
24h) when `mirror_urls` is absent or empty — this is not just a theoretical
fallback, real completed jobs have been observed with no `mirror_urls` field
at all. Once downloaded, the result is a local file either way, so a video
saved from `unsigned_urls` should be treated identically to one saved from
`mirror_urls` from this point on — the expiry window no longer matters once
the file is on disk.

Key flags: `--model` (default `bytedance/seedance-2.5`), `--duration`,
`--resolution`, `--aspect-ratio` (includes `adaptive` — see below), `--size`,
`--generate-audio true|false`, `--seed`, `--frame-first-image URL|PATH`,
`--frame-last-image URL|PATH`, `--real-person true|false`, `--callback-url`,
`--extra-json '<json>'` (advanced fields not covered by a flag, e.g.
`input_references`, `provider`), `--max-wait SECONDS` (default 540),
`--poll-interval SECONDS` (default 6). Full parameter reference:
`references/api-params.md`. Pricing and the cost-estimate formula:
`references/pricing.md`.

### Image-to-video: local files, remote URLs, and the `adaptive` aspect ratio

`--frame-first-image`/`--frame-last-image` accept either a remote
`http://`/`https://` URL (used as-is) or a local, readable file path — the
script auto-detects a local file and base64-encodes it into a
`data:image/<ext>;base64,...` URI before building the request (content-type
inferred from the file extension, `image/jpeg` as the safe default when the
extension isn't recognized). **Prefer a local file when one is available**:
real testing found at least one otherwise-valid, publicly reachable image
URL rejected by the upstream provider with a download-failure-shaped error,
while the same image worked reliably once base64-encoded — likely
bot/hotlink protection on some hosts, not something under our control.

Local files of any realistic size are supported: the base64 data URI is
built into the request body via a temp file and `jq --rawfile`/`--slurpfile`
and posted to the API via `curl --data-binary @file`, never via a `jq
--arg`/`--argjson` or `curl -d` **command-line** value. An earlier version
of this script did the latter and broke on any real photo whose base64
encoding exceeded the OS's `ARG_MAX` (roughly any real photo over ~750KB) —
verified with a real 885KB PNG (1,179,996-byte base64 encoding) failing
with `jq: Argument list too long` before any network call was made. Fixed
2026-08-29; see `.trellis/spec/skills/external-api-integration.md` for the
general lesson.

**`bytedance/seedance-2.5` (the default model) requires `aspect_ratio:
"adaptive"` for any image-to-video request** — every other value fails,
verified across multiple real attempts. When `--frame-first-image` or
`--frame-last-image` is set and the effective model is
`bytedance/seedance-2.5` (including the default, if `--model` wasn't
passed), the script **forces** `aspect_ratio` to `adaptive` regardless of
what `--aspect-ratio` was passed or left unset, and always prints a
one-line `NOTE:` to stderr explaining the override — it never does this
silently. This does not apply to other models (e.g.
`bytedance/seedance-2.0` works with image-to-video without this
requirement) — don't assume the requirement generalizes beyond
`bytedance/seedance-2.5` without separately verifying it.

Report results honestly, the same way `cloudflare-drop` reports its mode:
state which model/resolution/duration/aspect ratio were **actually used**
(not just requested) and the **actual** `VIDEO_COST` — never invent a cost
number or claim a video is ready without a real `VIDEO_PATH` from the
script.

**Always state the full `VIDEO_PATH` as its own standalone line in your
reply to the user** — not folded into a sentence or buried mid-paragraph.
The script always resolves `--out-dir` to an absolute path before printing
`VIDEO_PATH`, so relay that absolute path exactly as printed; the file's
location is the actual deliverable here, and the user should be able to
find it without re-deriving your working directory.

## The no-resubmit rule (non-negotiable)

**Never re-run `generate` for the same logical request just because it's
taking a while or a tool call timed out.** A create call that gets any HTTP
response has already either made the job (billable) or been rejected
(not billable) — running `generate` again for "the same video" risks a
second, separately billed job.

If `generate`'s own poll loop hits its time budget (job still
`pending`/`queued`/`in_progress`), it exits with the job id and prints
exactly this instruction — follow it:

```bash
bash references/ofox-video.sh poll JOB_ID
```

If a Claude Code tool call itself times out while `generate` is still
running (the script hasn't printed a result yet), the job may still be
mid-flight upstream — you won't have the job id from stdout in that case.
Don't guess or re-submit; tell the user the request may still be
processing and that checking `https://app.ofox.ai` for recent jobs is the
safe way to find its id and resume with `poll`.

If the create call itself gets an ambiguous network failure (curl exits
nonzero with **no HTTP response at all** — exit code `5`), the script
explicitly refuses to guess whether a job was created. Don't auto-retry;
tell the user to check `https://app.ofox.ai` first.

## Error handling

The script maps every documented `error.code` to a fixed, actionable
message and a distinct exit code. `error.message` (the upstream's own free
text) is **not** a stable contract to branch logic on, but it can carry a
specific, useful detail the generic mapped explanation doesn't (e.g. a
minimum reference-image width) — so the script always prints it too,
labeled `Upstream message: ...`, alongside the mapped explanation, not only
when `error.code` itself is absent or unrecognized.

| Exit | Meaning |
|---|---|
| `0` | Success — video downloaded, cost printed. |
| `1` | Usage/parameter validation error — no network call was made. Fix the flag and retry `generate` freely. |
| `2` | Environment error — `curl`/`jq`/`OFOX_API_KEY` missing. Fix the environment, no job was attempted. |
| `3` | The API rejected the request, or the job ended `failed`/`cancelled`/`expired`. The mapped message explains why (see `references/api-params.md` for the full error-code table). Includes `output_moderation_failed` — a **post-generation** failure (the job ran, its output failed a content check afterward), **not billed** (no `usage` field on the response), safe to fix by submitting a new `generate` call with a different prompt/reference — that's a new request, not a resubmission of the failed one. |
| `4` | Timed out waiting for a terminal state. The job is still running — `poll JOB_ID`, do not `generate` again. |
| `5` | Ambiguous network failure on create — no HTTP response received. Do not auto-retry; check the dashboard first. |

`batch` returns `3` when it stopped early: the takes that did complete are
still downloaded and still listed with their real cost, so a partial run is
reported honestly rather than discarded.
| `6` | `--out-dir` could not be created or entered (bad path, permissions) — a local filesystem problem, not an API problem. If this happened during `generate`, the job itself is unaffected (already created or still running server-side); do not re-run `generate`. Fix `--out-dir` and re-run `poll JOB_ID --out-dir <a writable directory>`. |

## For scenario skills built on this

`seedance-short-drama`, `seedance-ad-creative`, and `seedance-product-video`
invoke this skill's script (typically
`../ofox-video-core/references/ofox-video.sh` relative to their own
directory) rather than duplicating any of the request-building, polling,
error-mapping, or download logic above. They own the scenario-specific
prompt template, recommended parameter defaults, and the pre-generation
cost estimate (using `references/pricing.md`'s formula); this skill owns
the mechanics of talking to the API correctly and safely.

## Compatible with existing prompt-writing skills

This skill is an execution layer, not a director layer — it does not compete
with skills that specialize in writing Seedance prompts, it just runs
whatever prompt it's given. If the user already has a well-crafted prompt
from a "director" skill such as
[`LeoYeAI/seedance-skills`](https://github.com/LeoYeAI/seedance-skills) or
[`liyue-aigc/seedance-2-5-video-director`](https://github.com/liyue-aigc/seedance-2-5-video-director),
pass that prompt straight to `ofox-video.sh generate` — there's no need to
run this repo's own scenario-specific prompt-crafting steps (the ones
`seedance-short-drama`/`seedance-ad-creative`/`seedance-product-video`/
`seedance-anime-drama` each document) on top of a prompt that's already been
written. Those scenario skills exist for users who don't already have a
prompt and want one built for them; treat an existing director-skill output
as a ready-to-use prompt, not raw material to rewrite.
