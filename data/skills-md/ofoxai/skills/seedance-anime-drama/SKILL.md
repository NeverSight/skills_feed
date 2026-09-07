---
name: seedance-anime-drama
description: Turn a novel/script excerpt into an anime- or manga-style storyboard shot using the Ofox image and video APIs — generates one character reference image with ofox-image-core, then reuses that exact same image as `--frame-first-image` across every shot of that character via ofox-video-core, for real visual consistency instead of relying on repeated text description alone. Use when a user asks to turn a story excerpt into an anime video, e.g. "turn this novel excerpt into an anime video", "make an anime-style storyboard clip of this scene", "generate a manga-drama shot with this character", or "turn this chapter into an anime short with the same character in every shot". Do not use for realistic-human dialogue scenes with no anime/manga styling (see seedance-short-drama), silent product/brand shots (see seedance-ad-creative), or plain catalog footage (see seedance-product-video).
license: MIT
version: "1.5.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-anime-drama
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
    emoji: "🎨"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-anime-drama
---

# seedance-anime-drama: anime/manga storyboard shots with real character consistency

Turns one shot of a novel/script excerpt into an anime- or manga-style video
clip, using a genuine image-based mechanism for character consistency across
every shot of the same character — not just a repeated text description.

This is the first scenario skill in this repo that orchestrates **two**
execution-layer skills rather than one:

1. [`ofox-image-core`](../ofox-image-core/SKILL.md) generates ONE character
   reference image (text-to-image).
2. [`ofox-video-core`](../ofox-video-core/SKILL.md) generates each shot,
   passing that same image back in as `--frame-first-image`.

Neither core skill's request-building, error-mapping, or download/reporting
logic is duplicated here — this skill owns only the anime-specific prompt
craft, the two-step orchestration order, and the combined cost estimate.
**Read both core skills' safety contracts before using this one** — neither
is restated here.

## The mechanism — the whole point of this skill

Generate the character once as an image in Step 1, then pass that **exact
same image file** to `--frame-first-image` on every Step-2 call for every
shot of that character. This is what produces real visual consistency,
instead of `seedance-short-drama`'s text-only approach of repeating the same
description across stateless jobs and hoping the model renders it the same
way twice. Reusing the identical `IMAGE_PATH` is not an optional refinement
of this skill — it is the mechanism this skill exists to provide. See "When
NOT to use" below for the full comparison with `seedance-short-drama`.

## Before generating: two availability checks

Run each once per session (not on every request):

```bash
bash ../ofox-image-core/references/ofox-image.sh check
bash ../ofox-video-core/references/ofox-video.sh check
```

If either fails, follow that core skill's own guidance (install `curl`/`jq`,
or get an `OFOX_API_KEY` at `https://app.ofox.ai`) — don't dead-end the
conversation, and don't re-run either check on every subsequent request once
both have passed.

## One job = one continuous shot

Seedance 2.5 generates a single continuous clip per job (4–30 seconds). A
multi-scene "storyboard" from a novel excerpt maps to **one `generate` call
per shot** — never try to cram multiple hard cuts into one call. If a story
beat spans multiple hard cuts (e.g. an establishing shot then a close-up),
either:

- describe it as one continuous camera move within a single clip (a
  push-in, a pan, a walk-and-follow), or
- generate one clip per cut as **separate `generate` calls** (each a
  separately billed job), or
- use **`ofox-video-core`'s `chain`**, which feeds each shot's closing frame
  into the next as its opening frame and joins the results into one file.

**Chaining works for this skill specifically**, and that is not a given:
Seedance 2.5 image-to-video refuses reference frames containing a real person,
so a live-action sequence cannot be chained — but an anime/manga character is
not a photoreal person, so these shots chain fine. Verified continuity is
strong: the next shot opens on very nearly the exact frame it was fed, then
follows its own prompt.

Two ways to keep a character consistent, and they compose:

- **The character sheet** (Step 1 below) locks *who* the character is across
  shots that are otherwise unrelated.
- **`chain`** locks *where everything is* between consecutive shots — set,
  framing, lighting.

Use the sheet for shots that cut to a new setup, and `chain` for shots that
continue the same moment.

Don't assume how many shots a novel excerpt needs — confirm the shot count
and content with the user first; deciding that is the user's/calling
agent's job, not this skill's.

## Step 0: ask which visual look the user wants

Before building any prompt, ask whether the user wants:

- **Anime/animated-film style** — smooth cel-shading, clean line art,
  vibrant flat colors, expressive character animation. Example descriptors:
  "modern theatrical-anime style, cel-shaded, vibrant colors", "soft
  cinematic anime style, detailed backgrounds, gentle lighting", "90s-anime
  style, bold outlines, saturated colors".
- **Manga-panel/screentone style** — black-and-white or limited-color panel
  look, screentone shading, ink line art, comic-panel framing. Example
  descriptors: "black-and-white manga panel style, screentone shading, ink
  linework", "shoujo-manga style, delicate linework, soft screentone
  gradients", "seinen-manga style, high-contrast ink, dramatic screentone
  hatching".

Don't assume one over the other — the two produce visually very different
reference images and shots, and the choice belongs to the user. Carry the
chosen style descriptor into **both** steps below (the character reference
image prompt and every shot's video prompt), so the character image and
every shot stay visually consistent with each other, not just internally
consistent shot-to-shot.

## Step 1: generate the image the shot will actually start from

Extracting the character description is **this skill's calling agent's own
reasoning to do — not something a script performs**. Read the user's
story/script excerpt and write a precise, reusable character description
covering:

- age and build
- hair (color, length, style)
- clothing (exact garments, colors)
- distinguishing features (scars, accessories, eye color, etc.)

### Two different images, do not confuse them

`--frame-first-image` is the **literal first frame of the video**, not a
style hint. That makes the classic "character reference sheet" the wrong
thing to feed it:

| Image | What it is for | Prompt shape |
|---|---|---|
| **Character sheet** | Locking a design, showing the user, keeping one character consistent across shots that cut to unrelated setups | multi-view, labels, plain background |
| **Opening frame** | The frame the shot animates away from | one in-scene illustration, no text, no panels |

Asking for a "character reference sheet" gets you exactly that: a real
multi-panel sheet with front/side/back views, an expression row, a palette
swatch and printed labels — and models will happily invent a name and letter
it across the top. Fed to `--frame-first-image`, the clip opens on that
grid of thumbnails and text and animates out of it. **Verified on a real
run**: a sheet generated from the wording above came back with four views,
three expressions, a colour palette and the caption "HANA TANAKA", and had
to be thrown away and regenerated as a single in-scene image.

So pick by what you need:

**Generating one shot** (the common case) — you need an opening frame. Skip
the sheet: with a single shot there is no second shot to stay consistent
with, so the sheet buys nothing and costs an opening frame.

```bash
bash ../ofox-image-core/references/ofox-image.sh generate \
  --model google/gemini-3.1-flash-image \
  --prompt "<character description>, <the shot's opening moment: setting, pose, camera angle>, <anime/manga style descriptor>, cinematic composition, no text, no panels, single illustration" \
  --quality standard \
  --out-dir <a directory for this project's generated assets>
```

The `no text, no panels, single illustration` tail is what keeps the model
from drifting back into sheet mode — it is not optional padding.

**Generating several shots of one character** — generate the sheet as well,
once, and show it to the user to confirm the design. Then write each shot's
own opening frame using the **same character description word for word**, so
every shot inherits one design.

```bash
bash ../ofox-image-core/references/ofox-image.sh generate \
  --model google/gemini-3.1-flash-image \
  --prompt "<character description>, <anime/manga style descriptor>, character reference sheet, plain neutral background, front-facing full body" \
  --quality standard \
  --out-dir <a directory for this project's generated assets>
```

### The opening frame decides the output's shape

`bytedance/seedance-2.5` forces `aspect_ratio: adaptive` whenever an image is
attached, so the clip comes out at **the reference image's** aspect ratio,
whatever `--aspect-ratio` says. If the delivery needs a specific ratio
(9:16 for social, say), crop or pad the image before Step 2 — there is no
flag that fixes it afterwards.

`google/gemini-3.1-flash-image` is the recommended default for this step —
no strong reason to use `openai/gpt-image-2` or `bailian/qwen-image-3.0-pro`
unless the user asks for one of those specifically. Per `ofox-image-core`'s
own documented gotcha: whatever `--size` you pass (or omit), Gemini appears
to always actually generate at its native 1024x1024 resolution and just
echoes back the requested size — don't promise the user a specific output
size, and don't fight this if you do pass `--size`.

Take the printed `IMAGE_PATH` (an absolute path) and **show it to the user
as its own standalone line** — say whether it is the shot's opening frame or
a design sheet, since those get used differently. `ofox-image.sh` also prints
`IMAGE_COST`; relay it the same way you relay a video's cost.

Show the image to the user before spending on the shot. A wrong opening
frame is cheap to notice here and expensive to notice after the video is
paid for — a sheet that slipped through, an invented caption, a character
who is not who they pictured.

If the story needs more than one character, repeat Step 1 once per
character who needs their own reference image — see "Multiple characters in
one shot" below for the v1 scoping limit on this.

## Step 2: generate each shot from its opening frame

**Reuse the identical `IMAGE_PATH` from Step 1 across every shot of that
character.** Do not regenerate the character image per shot, and do not
swap in a different image between shots of the same character — that reuse
is the entire mechanism this skill provides.

For each shot, build an anime-style video prompt covering:

- scene action (what happens in the shot)
- dialogue in quotes, attributed, if the shot has any
- camera framing (wide/medium/close-up, pan/push-in), consistent with the
  chosen art style from Step 0

then call:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate \
  --prompt "<anime-style shot prompt built above>" \
  --frame-first-image "<the character reference image's ABSOLUTE path from Step 1>" \
  --duration 8 \
  --resolution 720p
```

`ofox-video-core` auto-base64-encodes a local file path like this one — no
need to upload it anywhere first. Always pass the **same absolute
`IMAGE_PATH`** printed in Step 1, never a relative path, a re-derived guess,
or a freshly generated image for this shot.

### `aspect_ratio: adaptive` will fire automatically here — expected, not a bug

Because every shot in this skill attaches a `--frame-first-image`, and the
default model is `bytedance/seedance-2.5`, `ofox-video-core` will force
`aspect_ratio` to `adaptive` and print a `NOTE:` every time, regardless of
whether `--aspect-ratio` is passed. **Don't pass `--aspect-ratio` here** —
it has no effect once an image is attached with this model. The output's
frame shape follows the character reference image's own aspect ratio
instead. If a specific output ratio matters for a platform, crop/pad the
character reference image to that ratio before Step 1, not after.

## Multiple characters in one shot: out of scope for v1

This skill scopes to one primary character reference per shot, matching
`ofox-video-core`'s single `--frame-first-image` slot. If a shot needs two
characters interacting:

- generate a reference image for the primary/foreground character only
  (Step 1),
- pass that image as `--frame-first-image` for the shot,
- describe the secondary character in the shot's video prompt text
  (appearance, action, dialogue) — the same text-only approach
  `seedance-short-drama` already uses for all of its characters.

This is a real accuracy tradeoff, not a full solution: the secondary
character has no image-based consistency guarantee across shots. Treat it
as the workaround it is, not as feature parity with the primary character's
mechanism.


## Which upstream renders it

Jobs are pinned to the `byteplus` upstream (ByteDance's platform for markets
outside mainland China). Ofox otherwise picks between it and Volcengine Ark by
weight, and the two moderate differently, so pinning keeps results consistent.
Pass `--provider volcengine` for the mainland platform, or `--provider auto` to
let Ofox choose. Pricing is identical either way. See
`ofox-video-core/references/api-params.md` for the detail.

## Cost: quote it, get a yes, then spend it

This skill spends money in **two** places, at different rates, and they scale
differently — so break them out rather than blending them into one number.

**Step 1 (image) — paid once per character, not once per shot.**
`ofox-image.sh generate` prints an `IMAGE_COST` line, computed from the
model's published rates and the response's own token counts and verified
against a real invoice (see `ofox-image-core/references/pricing.md`). Relay
that figure, the same way you relay `VIDEO_COST`.

For a `google/gemini-3.1-flash-image` reference sheet, observed calls land
around **6.7 cents** each — the output token count barely moves with prompt
length, so that is a good planning number rather than a coincidence. It is
paid **once per character**: generating N shots of that character does not
repeat it.

**Step 2 (video) — paid once per shot**, and this half you can quote exactly.

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

Image-to-video via `--frame-first-image` bills at **t2v** rates — v2v pricing
applies only when a *video* is the input, which this skill never does. The
script already picks the right tier.

Afterwards, the **actual** bill is `VIDEO_COST` from the finished job, read
from `usage.video_cost`. Report it as money (`$1.92`), not as the raw
ten-decimal string. An estimate is never a bill.

**Put both steps in front of the user before generating anything**, e.g.:
"1 character reference image (~7 cents, one-off) + 3 shots at 8s/720p (~$1.92
each) = ~$5.83 total." Breaking it out is what shows them the image cost does
not scale with shot count.


## Prompt language follows the audio

Audio is generated on by default, and the model speaks **whatever language the
prompt is written in**. So keep quoted dialogue in the user's own language —
if they give you Chinese lines, put Chinese in the prompt. Translating them to
match the English examples in this file produces an English-dubbed clip, and
the user only finds out after paying for it.

The rest of the prompt (setting, camera, lighting) can be English regardless;
it is the quoted speech that determines the spoken language.

The "2-3 spoken words per second" budget below is calibrated for English. For
Chinese and Japanese, count characters rather than words and budget roughly
5-6 characters per second.

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

## Generating: putting the two steps together

Example full sequence (the character/shot content is illustrative — the
calling agent fills in the real content extracted from the user's story):

```bash
# Step 1 — once per character
bash ../ofox-image-core/references/ofox-image.sh generate \
  --model google/gemini-3.1-flash-image \
  --prompt "A teenage girl, silver bob haircut, wearing a navy school uniform with a red ribbon, sharp green eyes, modern theatrical-anime style, cel-shaded, vibrant colors, character reference sheet, plain neutral background, front-facing full body" \
  --quality standard \
  --out-dir ./assets

# Step 2 — once per shot, reusing the SAME IMAGE_PATH printed by Step 1
bash ../ofox-video-core/references/ofox-video.sh generate \
  --prompt "The girl stands on a rooftop at sunset, wind blowing through her hair, she looks toward the horizon and says, \"I'm not going back.\" Medium shot, slow push-in, modern theatrical-anime style, cel-shaded" \
  --name "rooftop confession shot 1" \
  --frame-first-image "/absolute/path/to/assets/ofox_image_20260829_1234.png" \
  --duration 8 \
  --resolution 720p
```

Report the **actual** printed `IMAGE_PATH` / `VIDEO_PATH` / `VIDEO_COST`
from each script's own output — never an estimate, and never a path or cost
you didn't see a script print. Do not re-implement any of the
request/decode/poll/download logic here; always call into
`ofox-image.sh`/`ofox-video.sh`.

## Common failure modes and fixes

Combining both core skills' documented exit codes (full tables:
[`ofox-image-core/references/api-params.md`](../ofox-image-core/references/api-params.md),
[`ofox-video-core/references/api-params.md`](../ofox-video-core/references/api-params.md)),
plus this skill's own:

| Step | Symptom | Cause | Fix |
|---|---|---|---|
| 1 (image) | Exit `1`, no network call made | Missing `--quality`, bad `--model`, or `--n` combined with Gemini | Fix the flag per the error message and re-run `generate` — free to retry, nothing was submitted |
| 1 (image) | Exit `2` | `curl`/`jq` missing, or `OFOX_API_KEY` not set | Re-run `ofox-image-core`'s `check` and follow its install/signup guidance |
| 1 (image) | Exit `3`, `error.type: invalid_request_error` | The request was rejected as malformed/unsupported. The confirmed error shape is `{"error":{"message","type","code"}}` — `error.code` is just the HTTP status as a number here, `error.type` is the real classifier | Read the printed `Upstream message`, fix the prompt/flags, retry — a rejected request has not been confirmed to bill |
| 1 (image) | Exit `4` | `--out-dir` could not be created or entered | Caught before any network call, so no money was spent finding this out. Fix `--out-dir` and retry |
| 1 (image) | Exit `5`, ambiguous network failure | No HTTP response at all — this is a synchronous, no-job-id API, so there's nothing to poll afterward | Do not guess or retry blindly; check `https://app.ofox.ai`'s usage/billing history first |
| 1 (image) | `SIZE` in the printed output doesn't match what you asked for | `google/gemini-3.1-flash-image` always generates at its native 1024x1024 and just echoes back the requested `size` regardless of the real output | Don't promise the user a specific size; if a guaranteed size matters, check the real file's dimensions (`file <path>` / `sips -g pixelWidth -g pixelHeight <path>`), not the `SIZE` line |
| 2 (video) | Exit `1`, no network call made | Bad `--duration`/`--resolution`, or missing `--prompt` | Fix the flag per the error message and re-run `generate` — free to retry, nothing was submitted |
| 2 (video) | Exit `1`, "local image file ... exists but is not readable" | `--frame-first-image`'s path exists locally but this script/OS can't read it (permissions) — caught by `resolve_image_ref()` before any network call | Fix the file's permissions (confirm it's the exact `IMAGE_PATH` printed in Step 1) and retry — free, nothing was submitted |
| 2 (video) | Exit `2` | `curl`/`jq` missing, or `OFOX_API_KEY` not set | Re-run `ofox-video-core`'s `check` and follow its install/signup guidance |
| 2 (video) | Exit `3`, `error.code: insufficient_credits` | Ofox balance too low | No charge was made; the user needs to add credits at `https://app.ofox.ai` before retrying |
| 2 (video) | Exit `3`, job ends `failed`, `error.code: output_moderation_failed` | The generated output failed a post-generation content check, after the job ran — not billed (no `usage` field) | Retry with a brand-new `generate` call using a different prompt — a new request, safe to retry immediately |
| 2 (video) | Exit `3`, request rejected when the API tries to use the reference image (commonly `error.code: invalid_request`) | The `IMAGE_PATH` doesn't exist locally and isn't a URL either, so `resolve_image_ref()` passed it through unchanged and the API rejected it as an unusable value — `ofox-video-core`'s docs confirm `bad_data_uri`/`download_failed`/`unreachable`/`not_image`/`too_large` only for `--real-person`'s reference-photo validation, not for `--frame-first-image`/`frame_images`, so don't assume one of those five specific codes here | Confirm the exact `IMAGE_PATH` printed in Step 1 still exists and is a valid, readable image file, then retry |
| 2 (video) | Unexpected aspect ratio / frame shape in the output | `bytedance/seedance-2.5` + `--frame-first-image` always forces `aspect_ratio: adaptive` (printed as a `NOTE:`, never silent) — the output follows the reference image's own aspect ratio | Expected behavior, not a bug — see "`aspect_ratio: adaptive` will fire automatically" above; crop/pad the reference image before Step 1 if a specific ratio is required |
| 2 (video) | Exit `4`, timed out waiting for completion | Job is still running upstream, not failed | Do **not** re-run `generate`; run `bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID` using the job id printed before the timeout |
| 2 (video) | Exit `5`, ambiguous network failure on create | No HTTP response received at all — can't tell if a job was created | Do not guess or retry `generate`; check `https://app.ofox.ai` first, per `ofox-video-core`'s no-resubmit rule |
| 2 (video) | Exit `6`, `--out-dir` could not be created or entered | Local filesystem problem, not an API problem | The job itself is unaffected — fix `--out-dir` and re-run `poll JOB_ID --out-dir <a writable directory>`; do not re-run `generate` |
| both | Character looks visibly different between two shots | The same `IMAGE_PATH` wasn't reused, or Step 1 was accidentally re-run per shot | Reuse the exact same absolute path from the ONE Step-1 call for every shot of that character — this is the entire mechanism, see above |

## When NOT to use

- Realistic-human dialogue scenes with no anime/manga styling — use
  `seedance-short-drama` instead. That skill's character-consistency
  approach is text-only (repeating the same description across stateless
  jobs); this skill replaces that with a real, reused reference image, but
  only for an anime/manga art style — every prompt this skill builds bakes
  in the Step-0 style descriptor, so it is not a general-purpose "add image
  consistency to any style" tool.
- Silent product/brand footage with no characters — use `seedance-ad-creative`
  instead.
- Plain catalog/listing product shots — use `seedance-product-video` instead.
- More than one character needing independent image-based consistency in the
  same shot — out of scope for v1 (see "Multiple characters in one shot"
  above); only one primary character gets a reference image per shot.
- Editing an existing character's outfit/appearance mid-story — this skill
  only does fresh text-to-image generation (`ofox-image-core` doesn't
  implement `/v1/images/edits`); generate a new Step-1 reference image
  instead, treated as a new "version" of the character from that point on.
