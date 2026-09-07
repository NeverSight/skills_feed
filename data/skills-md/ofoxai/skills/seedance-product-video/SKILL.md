---
name: seedance-product-video
description: Generate a clean, catalog-style e-commerce product video from a real product photo (or, less reliably, a text description) using the Ofox video API (Seedance 2.5) — writes a plain-background, literal-accuracy prompt (precise product description, simple turntable/orbit motion, no dramatic cinematography), shows a cost estimate, then calls ofox-video-core to submit, poll, download, and report the real cost. Use when a user asks to turn a product photo into catalog/listing footage, e.g. "make this product photo a 360-degree white-background showcase", "turn this photo into a white-background product video", "make a clean turntable video of this item", or "give me a 5-second white-background rotation video of this product for my listing". Do not use for cinematic brand/mood advertising (see seedance-ad-creative) or for anything involving people/dialogue (see seedance-short-drama).
license: MIT
version: "1.5.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-product-video
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
    emoji: "📦"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-product-video
---

# seedance-product-video: clean e-commerce product showcase videos

Turns a product photo into a plain-background catalog/listing clip: a
precise product description plus a simple turntable or orbit motion become a
Seedance 2.5 image-to-video prompt, which this skill submits, polls,
downloads, and reports the cost for.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the product-video
prompt craft, recommended defaults, and the pre-generation cost estimate;
`ofox-video-core` owns talking to the Ofox API correctly and safely (the
`OFOX_API_KEY` handling, the no-resubmit rule, error-code mapping,
download/verification, and reporting the downloaded file's absolute
`VIDEO_PATH`). **Read that skill's safety contract before using this one** —
it is not restated here.

## Before generating: the availability check

Run this once per session (not on every request):

```bash
bash ../ofox-video-core/references/ofox-video.sh check
```

If it fails, follow `ofox-video-core`'s guidance (install `curl`/`jq`, or get
an `OFOX_API_KEY` at `https://app.ofox.ai`) — don't dead-end the
conversation, and don't re-run this check on every subsequent request once
it has passed.

## Prefer a real product photo — practically require it

For this scenario, literal accuracy (exact shape, printed text, logo,
color, material) matters more than in any other Seedance use case: the
output is catalog/listing content a shopper compares directly against the
real item, so an invented detail is a real problem, not just an aesthetic
one. Pure text-to-video is far more likely to hallucinate an inaccurate
shape or garble label text than image-to-video is. If the user has a
product photo at all, always use `--frame-first-image` with it rather than
describing the product purely in text — treat a text-only prompt as a
fallback only when no photo exists, and set expectations accordingly (the
result may not exactly match the real product).

**Prefer a local file over a remote URL** when the user has one available.
`ofox-video-core` auto-base64-encodes a local, readable file into the
request; real testing found this more reliable than a remote URL in at
least one case (an otherwise valid, publicly reachable image URL was
rejected by the upstream provider — likely host-side bot/hotlink
protection, not something under our control):

```bash
bash ../ofox-video-core/references/ofox-video.sh generate \
  --prompt "The product rotates smoothly 360 degrees against a pure white background, no props, no shadows, no dramatic lighting" \
  --frame-first-image "/path/to/local/product-photo.jpg" \
  --duration 5 --resolution 720p --generate-audio false
```

A remote URL also works if that's all the user has (`--frame-first-image
"https://example.com/product-photo.jpg"`), it's just the less-reliable
option of the two.

**Do not pass `--aspect-ratio` here** for the default model
(`bytedance/seedance-2.5`) — `ofox-video-core` forces `aspect_ratio` to
`adaptive` whenever an image is attached with this model (verified against
the real API: every other value fails for image-to-video on this model),
overriding anything else and printing a notice when it does. See
Recommended defaults below for when `--aspect-ratio` does matter for this
skill.

If the reference image includes an actual person (e.g. a hand modeling a
ring, a person wearing the product), add `--real-person true` per the API
contract. That path validates the image server-side and can fail with
`bad_data_uri`/`download_failed`/`unreachable`/`not_image`/`too_large` if the
image isn't a small, valid file the API can use — see the failure table
below.

## Writing a good product-video prompt

Keep the prompt plain and literal — this is the opposite instinct from
`seedance-ad-creative`'s cinematic mood-building.

### 1. Product description, precise and neutral

State shape, material, color, and finish exactly, the same framing
discipline `seedance-ad-creative` uses for product accuracy — but skip its
mood/brand-tone layer entirely, since a catalog shot has no brand story to
tell.

```
A matte ceramic coffee mug, off-white, cylindrical with a curved handle.
```

### 2. Explicit plain-background language

State the background directly rather than assuming the model will remove
whatever is behind the product in the reference photo:

```
Pure white background, clean studio background, no props, no shadows on the
backdrop, even lighting.
```

### 3. Simple, literal camera motion — not cinematography

Describe the motion as a plain mechanical turntable or orbit, not a "shot."
Avoid `seedance-ad-creative`'s cinematography vocabulary (dolly-in, rack
focus, rim light, moody backlight) entirely — none of that belongs here;
the point is to see the product clearly from multiple angles, not to evoke
a mood.

```
The product rotates smoothly 360 degrees on its own axis at a constant
speed, camera fixed and centered.
```

or, for a still product with camera movement instead of product rotation:

```
Camera slowly orbits once around the product at a constant height, product
stays still and centered in frame.
```

### Putting it together

```
A matte ceramic coffee mug, off-white, cylindrical with a curved handle. The
product rotates smoothly 360 degrees on its own axis at a constant speed
against a pure white background, no props, no shadows, even studio lighting,
camera fixed and centered.
```

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--model` | `bytedance/seedance-2.5` (script default, no flag needed) | current-generation model |
| `--duration` | `5` (5–10s range; adjust to match the request) | a full 360-degree turntable reads clearly in 5 seconds and keeps cost low; Seedance 2.5 accepts 4–30 |
| `--resolution` | `720p` | catalog/listing thumbnails rarely benefit from more; suggest `1080p` only if the target platform explicitly requires higher-resolution assets |
| `--aspect-ratio` | ask the user — do not assume a single fixed default, but see the note below | e-commerce platforms vary widely: `1:1` fits most marketplace grid listings (Amazon, Etsy, Shopify), `4:3` matches older catalog templates, `9:16` suits mobile-first storefronts or short-video shopping (TikTok Shop), `16:9` suits a website product-detail page. Confirm the target platform before generating. |
| `--generate-audio` | `false` (this scenario's default) | a silent product-rotation clip needs no audio track; this **overrides** the server's `generate_audio: true` default, unlike `seedance-short-drama`/`seedance-ad-creative` which leave audio on. Verified against `ofox-video-core`'s script: `--generate-audio false` sets `generate_audio: false` directly on the request. |
| `--real-person` | leave unset (`false`) | only set `true` if the reference photo includes an actual person (e.g. a hand or model wearing the product), not just the product itself |

**Important caveat on `--aspect-ratio` for this skill**: since this skill
*practically requires* `--frame-first-image` (see above), the platform's
target aspect ratio applies **only on the rare text-only fallback path**
(no product photo available). Once an image is attached with the default
model, `ofox-video-core` forces `aspect_ratio` to `adaptive` and the
output's frame shape follows the **input photo's own aspect ratio**
instead of whatever platform ratio was asked for. Tell the user this
plainly: if a specific output ratio is required for a platform (e.g. a
strict `1:1` grid), the product photo itself should be cropped/padded to
that ratio *before* generating, since the generation step will no longer
be able to force a different one once an image is attached.


## Which upstream renders it

Jobs are pinned to the `byteplus` upstream (ByteDance's platform for markets
outside mainland China). Ofox otherwise picks between it and Volcengine Ark by
weight, and the two moderate differently, so pinning keeps results consistent.
Pass `--provider volcengine` for the mainland platform, or `--provider auto` to
let Ofox choose. Pricing is identical either way. See
`ofox-video-core/references/api-params.md` for the detail.


## Multi-shot product sequences

`ofox-video-core`'s `chain` subcommand generates a sequence where each shot
opens on the previous shot's closing frame, so the product stays in the same
place under the same light across cuts — then joins them into one file. It
works for product footage: the real-person restriction that blocks chaining
live-action sequences doesn't apply to objects.

```bash
bash ../ofox-video-core/references/ofox-video.sh chain \
  --shot "the product on a white background, slow turntable rotation" \
  --shot "the camera pushes in on the same product, same white background" \
  --duration 5 --resolution 720p
```

Each shot is a separately billed job; the run estimates the total before
spending and reports real per-shot cost.

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

With a product photo (the common case — prefer a local file path over a
remote URL when one is available):

```bash
bash ../ofox-video-core/references/ofox-video.sh generate \
  --prompt "<the product-video prompt built above>" \
  --name "<short product name, e.g. sneaker turntable>" \
  --frame-first-image "<local path or URL to the product photo>" \
  --duration 5 \
  --resolution 720p \
  --generate-audio false
```

No `--aspect-ratio` flag here on purpose — with the default model,
`ofox-video-core` forces `adaptive` once an image is attached (see the
caveat above), so passing a different value would just be overridden
anyway (the script prints a notice when it does this, it's never silent,
but there's no reason to pass a value that won't take effect). Without a
product photo (text-only fallback), `--aspect-ratio` does take effect and
should be set per the platform the user named:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate \
  --prompt "<the product-video prompt built above>" \
  --duration 5 \
  --resolution 720p \
  --aspect-ratio 1:1 \
  --generate-audio false
```

This one call validates the parameters, submits the job, polls to
completion, downloads the mp4, and prints `STATUS`, `JOB_ID`, `VIDEO_PATH`,
`VIDEO_SECONDS`, and `VIDEO_COST`. Report the **actual** values from that
output to the user — never the estimate, and never a path/cost you didn't
see the script print. Always state the printed `VIDEO_PATH` as its own
standalone absolute-path line in your reply, per `ofox-video-core`'s
reporting requirement. Do not re-implement any of the request/poll/download
logic here; always call into `ofox-video.sh`.

## Common failure modes and fixes

These are `ofox-video-core`'s documented exit codes and error codes
(full table: [`../ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)),
plus the product-video-specific ones:

| Symptom | Cause | Fix |
|---|---|---|
| Exit `1`, no network call made | Bad `--duration`/`--resolution`/`--aspect-ratio`, or missing `--prompt` | Fix the flag per the error message and re-run `generate` — free to retry, nothing was submitted |
| Exit `2` | `curl`/`jq` missing, or `OFOX_API_KEY` not set | Re-run `ofox-video-core`'s `check` and follow its install/signup guidance |
| Exit `3`, `error.code: insufficient_credits` | Ofox balance too low | No charge was made; the user needs to add credits at `https://app.ofox.ai` before retrying |
| Exit `3`, job ends `failed`, or `invalid_request` on create, with no other error code hint | Likely a moderation rejection: a reference photo showing someone else's trademarked packaging/logo without rights, or a prohibited product category, is commonly rejected | Remove or crop the flagged trademark/brand element from the reference photo or prompt, then call `generate` again — this is a **new** request, not a resubmission of the failed one, so it's safe to retry immediately |
| Exit `3`, job ends `failed`, `error.code: output_moderation_failed` | The generated **output** failed a post-generation content check — happens after the job ran, not at submission. Not billed (no `usage` field on the response) | Retry with a brand-new `generate` call using a different prompt or reference photo — a new request, not a resubmission of the failed one, so it's safe |
| `bad_data_uri` / `download_failed` / `unreachable` / `not_image` / `too_large` on an image-to-video job | The `--frame-first-image` reference isn't a small, valid image the API can use (a remote URL that isn't publicly reachable, or a local file that failed to read/encode) | Prefer a local file (auto-base64'd, more reliable than some remote URLs — see above); confirm it's a real image file under the size limit and retry |
| Product shape, printed text, or logo looks distorted or inaccurate in the result | Pure text-to-video was used instead of a real reference photo | Switch to image-to-video with `--frame-first-image` pointing at the real product photo — literal accuracy matters more in this scenario than anywhere else, so treat text-only description as a last resort |
| Background isn't pure white, or shows props/shadows from the original photo | The prompt didn't state the background explicitly, or the source photo's busy background carried through | Add explicit "pure white background, no props, no shadows" language; a reference photo with a cluttered background can still bleed through in image-to-video since the model anchors on that image |
| Exit `4`, timed out waiting for completion | Job is still running upstream, not failed | Do **not** re-run `generate`; run `bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID` using the job id printed before the timeout |
| Exit `5`, ambiguous network failure on create | No HTTP response received at all — can't tell if a job was created | Do not guess or retry `generate`; tell the user to check `https://app.ofox.ai` for a job that may already be running, per `ofox-video-core`'s no-resubmit rule |
| Exit `6`, `--out-dir` could not be created or entered | Local filesystem problem (bad path, permissions), not an API problem | The job itself is unaffected — do not re-run `generate`; fix `--out-dir` and re-run `bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID --out-dir <a writable directory>` |

## When NOT to use

- Cinematic brand/mood advertising — dramatic lighting, camera language like
  dolly-ins or rim light, a brand-tone background — use `seedance-ad-creative`
  instead. This skill's prompts are deliberately plain (white background,
  fixed or simple orbiting camera) for literal catalog accuracy, not brand
  storytelling.
- Anything involving people, characters, or dialogue — use
  `seedance-short-drama` instead; this skill is for inanimate product objects
  only.
