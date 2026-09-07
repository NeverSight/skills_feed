---
name: seedance-ad-creative
description: Generate a cinematic brand/product ad clip from a product description or photo using the Ofox video API (Seedance 2.5) — writes a shot-craft prompt (product framing, camera language, brand tone), shows a cost estimate, then calls ofox-video-core to submit, poll, download, and report the real cost. Use when a user asks for a commercial-style product or brand video, e.g. "give this perfume bottle a 10-second cinematic brand ad", "make a product ad for our new sneaker", "turn this product photo into a hero video for the landing page", or "I need a 15-second brand video with a slow orbit around the bottle". Do not use for dialogue-driven scenes with people talking (see seedance-short-drama).
license: MIT
version: "1.5.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-ad-creative
metadata:
  author: ofoxai
  version: "1.5.0"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "📺"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-ad-creative
---

# seedance-ad-creative: cinematic product/brand ad clips

Turns a product description (or a product photo) into a commercial-style
video clip: camera language, product framing, and brand tone become a
Seedance 2.5 prompt, which this skill submits, polls, downloads, and reports
the cost for.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the ad-creative
prompt craft, recommended defaults, and the pre-generation cost estimate;
`ofox-video-core` owns talking to the Ofox API correctly and safely (the
`OFOX_API_KEY` handling, the no-resubmit rule, error-code mapping,
download/verification). **Read that skill's safety contract before using
this one** — it is not restated here.

## Before generating: the availability check

Run this once per session (not on every request):

```bash
bash ../ofox-video-core/references/ofox-video.sh check
```

If it fails, follow `ofox-video-core`'s guidance (install `curl`/`jq`, or get
an `OFOX_API_KEY` at `https://app.ofox.ai`) — don't dead-end the
conversation, and don't re-run this check on every subsequent request once
it has passed.

## Writing a good ad-creative prompt

Order the prompt product-first, then camera, then mood — in practice this
keeps the model's attention on rendering the product correctly before it
spends effort on the environment:

### 1. Product framing, described precisely

State the product's shape, material, color, and how it sits in frame before
anything else. Be exact about surface/finish (glass, brushed metal, matte
plastic) since that drives how light behaves on it.

```
A tall clear glass perfume bottle with a gold cap, centered on a reflective
black surface.
```

### 2. Camera language, stated as a real shot

Use concrete cinematography terms rather than vague adjectives — they steer
the model far more reliably than "make it look cool":

- **Framing/move**: slow dolly-in, orbit (specify degrees, e.g. "orbits 30
  degrees left"), macro close-up, rack focus from background to product,
  slow pull-back reveal.
- **Lighting**: soft rim light, backlit silhouette, single hard key light,
  studio softbox lighting.

```
Camera slowly orbits 30 degrees around the bottle, soft rim light along the
glass edge, shallow depth of field with the background gently blurred.
```

### 3. Brand tone, as a short mood/style tag

One or two tone words steer the color grade and pacing more reliably than a
paragraph of adjectives:

- Luxury: slow movement, dark/moody background, warm gold highlights.
- Playful/consumer: bright saturated colors, faster movement, upbeat energy.
- Minimalist/tech: clean white or grey background, precise/steady camera,
  cool light.

```
Minimalist, high-end product photography style, dark background, cinematic
color grade.
```

### Putting it together

```
A tall clear glass perfume bottle with a gold cap, centered on a reflective
black surface. Camera slowly orbits 30 degrees around the bottle, soft rim
light along the glass edge, shallow depth of field with the background
gently blurred. Minimalist, high-end product photography style, dark
background, cinematic color grade, no dialogue, soft ambient music.
```

Since ad-creative clips are typically silent-of-dialogue (ambient
music/sound only), say so explicitly in the prompt ("no dialogue") to steer
away from any voice generation.

### If the user has an actual product photo

Prefer image-to-video over describing the product purely in text — Seedance
renders the real product (label text, exact shape) far more faithfully from
a reference image than from a text description, which can distort fine
label detail or logos. Prefer a local file over a remote URL when the user
has one: `ofox-video-core` auto-base64-encodes a local file, which real
testing found more reliable than depending on the upstream provider being
able to fetch an arbitrary third-party URL (some hosts' bot/hotlink
protection can reject an otherwise valid, publicly reachable image URL).

```bash
bash ../ofox-video-core/references/ofox-video.sh generate \
  --prompt "Camera slowly orbits 30 degrees around the product, soft rim light, cinematic color grade" \
  --frame-first-image "/path/to/local/product-photo.jpg" \
  --duration 10 --resolution 1080p
```

**Note on `--aspect-ratio` with an attached image**: don't pass
`--aspect-ratio` here for the default model — `ofox-video-core` forces
`aspect_ratio` to `adaptive` whenever an image (`--frame-first-image`/
`--frame-last-image`) is combined with `bytedance/seedance-2.5` (this
skill's default model), overriding anything else with a printed notice.
`--aspect-ratio` (`16:9`/`9:16`/`1:1`/etc., see Recommended defaults below)
only takes effect on the **pure text-to-video** path, when no image is
attached.

If the reference image includes an actual person (e.g. a spokesperson or
model in the shot, not just the product), add `--real-person true` per the
API contract. That path validates the image server-side and can fail with
`bad_data_uri`/`download_failed`/`unreachable`/`not_image`/`too_large` if the
image isn't a small, valid file the API can use — see the failure table
below.

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--model` | `bytedance/seedance-2.5` (script default, no flag needed) | current-generation model |
| `--duration` | `10` (adjust to match the request, e.g. `15` if asked for 15 seconds) | typical short-ad length; Seedance 2.5 accepts 4–30 |
| `--resolution` | `1080p` for a deliverable brand asset; suggest `720p` as a cheaper draft/preview pass | brand assets are usually published, so higher fidelity is worth the extra cost — but confirm with the user given the price difference (see cost estimate below) |
| `--aspect-ratio` | `16:9` (landscape) — **pure text-to-video only** | cinematic/hero framing for websites and YouTube; pass `--aspect-ratio 9:16` for a vertical social-ad cut or `1:1` for feed placements. **Does not apply once an image is attached** with the default model — `ofox-video-core` forces `adaptive` in that case (see above) |
| `--generate-audio` | `true` (server default, no flag needed) | ambient/music track; the prompt should say "no dialogue" if that matters |


## Which upstream renders it

Jobs are pinned to the `byteplus` upstream (ByteDance's platform for markets
outside mainland China). Ofox otherwise picks between it and Volcengine Ark by
weight, and the two moderate differently, so pinning keeps results consistent.
Pass `--provider volcengine` for the mainland platform, or `--provider auto` to
let Ofox choose. Pricing is identical either way. See
`ofox-video-core/references/api-params.md` for the detail.


## Multi-shot ad sequences

`ofox-video-core`'s `chain` subcommand builds a sequence where each shot opens
on the previous shot's closing frame — set, lighting and framing carry over —
and joins them into one file. Useful for a beat sequence (establishing, then
push-in, then hero) that would otherwise cut between unrelated renders.

It works as long as no shot carries a photoreal person: Seedance 2.5
image-to-video refuses real-person reference frames, so a sequence built
around a human model can't be chained, while product and environment shots
can. Each shot is a separately billed job; the run estimates the total before
spending.

## Cost: quote it, get a yes, then spend it

Never submit a paid job without the user having seen the number first. The
script makes that possible with `--dry-run`, which validates everything and
prints the estimate **without sending a request**:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." --duration 15 --resolution 720p --out-dir ./out
```

Relay the `Estimated cost:` line it prints, wait for a yes, then re-run the
identical command with `--dry-run` removed.

The estimate a *real* run prints comes microseconds before the request goes
out, so it is not something you can relay in time — that is what `--dry-run`
is for. Every run prints exactly one `Estimated cost:` line, including when it
can't compute one (it says why). Relay whatever you get; never invent a number.

Afterwards, the **actual** bill is `VIDEO_COST` from the finished job, read
from `usage.video_cost`. Report it as money (`$3.60`), not as the raw
ten-decimal string. An estimate is never a bill.

## Several takes to choose from

Video generation is a slot machine — most takes go in the bin. When the user
wants options rather than one clip, use `batch` instead of running `generate`
repeatedly:

```bash
bash ../ofox-video-core/references/ofox-video.sh batch --dry-run \
  --prompt "..." --takes 4 --duration 8 --resolution 480p --out-dir ./out
```

It prices the whole batch up front, stops on the first failure instead of
burning the remaining takes, and produces a contact sheet — three frames per
take, one row each — so the user picks from one image instead of opening N
files.

**Quote `BATCH_COST_TOTAL`, not `BATCH_COST_PER_TAKE`.** If one take in four
is usable, that clip cost the whole total; the per-take figure understates it
by 4x.

Hand the user the `CONTACT_SHEET` path on its own line, the same way you hand
over a video — in this flow it is the artifact they actually look at first,
since it is how they pick. Then list the individual take paths beneath it.

Each `TAKE` line carries `seed=N`. That seed is the handle for "take 3 was the
good one": re-run the same prompt with that seed on a better model or higher
resolution to reproduce that take rather than rolling a new one.

A single `generate` prints a `SEED` line too, and records it in the clip's
`.json` sidecar along with the resolution and aspect ratio. So "that one was
good, give me it at 1080p" works off one clip — you do not need a batch to
get a reusable handle.


Worth offering when the user is exploring: draft cheap on
`bytedance/seedance-2.0-mini` at 480p, then render the winner on
`bytedance/seedance-2.5`. Four 8-second drafts cost about 64 cents on mini versus
$7.68 on 2.5 at 720p. But **don't switch models on their behalf** — a
different model is a different look, not just a different price.



## Pricing a job with no API key

**No API key needed** to find out what something costs. All three of these
work with `OFOX_API_KEY` unset:

```bash
bash ../ofox-video-core/references/ofox-video.sh models      # models and rates
bash ../ofox-video-core/references/ofox-video.sh providers   # full price matrix
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." --duration 15 --resolution 720p             # a real quote
```

So when a user hasn't signed up yet, **quote the job first and let them decide
whether it's worth registering.** Don't open by sending them to a signup form
— price it, show them the number, then point at
[app.ofox.ai](https://app.ofox.ai) if they want to proceed.

## If the script isn't found

```
bash: ../ofox-video-core/references/ofox-video.sh: No such file or directory
```

This means `ofox-video-core` isn't installed alongside this skill — not that
anything is broken. This skill delegates all execution to it and reaches it by
relative path. Fix: `npx skills add ofoxai/skills` (the whole repo). Say that
plainly rather than relaying the raw path error, which names neither the
missing skill nor the fix.

## Before you spend: show the prompt, not just the price

The user is paying for **the prompt** — what the characters look like, how the
camera moves, whether their lines survived word for word. The price is the
smaller half of what they are agreeing to.

So put both in front of them: the prompt you built, and the `--dry-run`
estimate. A clip that costs exactly what you quoted and shows a character the
user never pictured is still a wasted job.

## Exit codes worth knowing

Full table in [`../ofox-video-core/SKILL.md`](../ofox-video-core/SKILL.md) —
the ones that come up:

| Code | Meaning | What to do |
|---|---|---|
| `1` | Parameter rejected locally, no network call, nothing billed | Fix the flag and retry freely |
| `2` | Environment problem — `curl`/`jq` missing, or no `OFOX_API_KEY` | Ask the user to fix it; `check` reports the same |
| `3` | API rejected it, or the job ended failed/cancelled/expired | Read the mapped message; a rejected create was not billed |
| `4` | Timed out waiting — **the job is still running and billable** | `poll JOB_ID`, never re-run `generate` |
| `5` | Ambiguous network failure on create | Do not retry blindly; check https://app.ofox.ai first |
| `6` | `--out-dir` unusable | Fix the path; if it happened after a create, `poll JOB_ID` instead of regenerating |

## How long to tell the user it will take

`generate` blocks while it polls, up to `--max-wait` (default 540s). A short
480p draft is usually one to three minutes; longer or higher-resolution jobs
take longer. Say so before starting, so the wait isn't silent.

If your tool call can't stay open that long, use `create` (submits and returns
a job id in seconds) followed by `poll`, instead of `generate`. That way a
timeout can never strand a job whose id you never saw. For `batch`, the worst
case is `takes x max-wait` — lower `--max-wait` for drafts, or create and poll
each take yourself.

## Where the file lands

Always pass `--out-dir`. Without it the script writes to the current working
directory, which is usually the user's project root. Pick something sensible
(`./out`, or wherever the user asked) and relay the absolute `VIDEO_PATH` the
script prints, on its own line.

Pass `--name` too. You know what the shot is — you just wrote the prompt for
it — so name the file after the scene rather than leaving the script to guess
from the prompt's opening words, which describe the setting and the lighting.
The clip lands as `<name>-<short job id>.mp4` with a `.json` sidecar beside
it holding the full job id, the prompt and the real cost.

## Running the script

Paths in the examples above are written relative to **this skill's own
directory** (`skills/<this-skill>/`), which is where `../ofox-video-core/...`
resolves from. If you are running from somewhere else, adjust accordingly —
from the repo root it is `skills/ofox-video-core/references/ofox-video.sh`.

## Generating

```bash
bash ../ofox-video-core/references/ofox-video.sh generate \
  --prompt "<the ad-creative prompt built above>" \
  --name "<short spot name, e.g. perfume bottle hero ad>" \
  --duration 10 \
  --resolution 1080p \
  --aspect-ratio 16:9
```

This one call validates the parameters, submits the job, polls to
completion, downloads the mp4, and prints `STATUS`, `JOB_ID`, `VIDEO_PATH`,
`VIDEO_SECONDS`, and `VIDEO_COST`. Report the **actual** values from that
output to the user — never the estimate, and never a path/cost you didn't
see the script print. Do not re-implement any of the request/poll/download
logic here; always call into `ofox-video.sh`.

## Common failure modes and fixes

These are `ofox-video-core`'s documented exit codes and error codes
(full table: [`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)),
plus the ad-creative-specific ones:

| Symptom | Cause | Fix |
|---|---|---|
| Exit `1`, no network call made | Bad `--duration`/`--resolution`/`--aspect-ratio`, or missing `--prompt` | Fix the flag per the error message and re-run `generate` — free to retry, nothing was submitted |
| Exit `2` | `curl`/`jq` missing, or `OFOX_API_KEY` not set | Re-run `ofox-video-core`'s `check` and follow its install/signup guidance |
| Exit `3`, `error.code: insufficient_credits` | Ofox balance too low, especially likely at 1080p | No charge was made; suggest a cheaper 720p draft or adding credits at `https://app.ofox.ai` |
| Exit `3`, job ends `failed`, or `invalid_request` on create, with no other error code hint | Likely a moderation rejection: prompts referencing a real celebrity/spokesperson likeness without consent, another brand's trademarked logo, or copyrighted characters are commonly rejected | Remove the flagged real-person/trademark/copyrighted reference from the prompt (or reference image), then call `generate` again — this is a **new** request, not a resubmission of the failed one, so it's safe to retry immediately |
| Exit `3`, job ends `failed`, `error.code: output_moderation_failed` | The generated **output** failed a post-generation content check — happens after the job ran, not at submission. Not billed (no `usage` field on the response) | Retry with a brand-new `generate` call using a different prompt or reference image — a new request, not a resubmission of the failed one, so it's safe |
| `bad_data_uri` / `download_failed` / `unreachable` / `not_image` / `too_large` on an image-to-video job | The `--frame-first-image`/`--frame-last-image` reference isn't a small, valid image the API can use (a remote URL that isn't publicly reachable, or a local file that failed to read/encode) | Prefer a local file (auto-base64'd, more reliable than some remote URLs — see above); confirm it's a real image file under the size limit and retry |
| Product label text or logo looks distorted/illegible in the result | Pure text-to-video can't render fine label detail reliably | Switch to image-to-video with `--frame-first-image` pointing at the real product photo instead of describing the label in text |
| Exit `4`, timed out waiting for completion | Job is still running upstream, not failed | Do **not** re-run `generate`; run `bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID` using the job id printed before the timeout |
| Exit `5`, ambiguous network failure on create | No HTTP response received at all — can't tell if a job was created | Do not guess or retry `generate`; tell the user to check `https://app.ofox.ai` for a job that may already be running, per `ofox-video-core`'s no-resubmit rule |

## When NOT to use

- Dialogue-driven scenes with characters talking — use `seedance-short-drama`
  instead.
- Plain catalog/listing footage (white background, literal turntable
  rotation, no mood or camera language) rather than a cinematic brand ad —
  use `seedance-product-video` instead.
