---
name: seedance-short-drama
description: Generate a single realistic-human, dialogue-driven short-drama shot from a script or scene description using the Ofox video API (Seedance 2.5) — writes a shot-craft prompt (character appearance, quoted dialogue, scene-cut timing cues), shows a cost estimate, then calls ofox-video-core to submit, poll, download, and report the real cost. Use when a user asks to turn a script beat into video, e.g. "generate scene 3 of this script, two characters talking, 15 seconds", "make a vertical short-drama clip of these two arguing in a kitchen", "turn this dialogue into a 12-second video", or "give me a realistic short-drama shot of a couple breaking up at a train station". Do not use for silent product/brand shots (see seedance-ad-creative) or for anything not involving people/dialogue.
license: MIT
version: "1.5.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-short-drama
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
    emoji: "🎭"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/seedance-short-drama
---

# seedance-short-drama: dialogue-driven short-drama shots

Turns one scene/shot of a script into a realistic-human video clip: a character
description, quoted dialogue, and pacing cues become a Seedance 2.5 prompt,
which this skill submits, polls, downloads, and reports the cost for.

This skill is a thin, scenario-specific layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the short-drama
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

## One job = one continuous shot

Seedance 2.5 generates a single continuous clip per job (4–30 seconds). "Scene
3 of this script" maps to **one `generate` call per shot**. If a script beat
spans multiple hard cuts (e.g. exterior establishing shot, then interior
close-up), either:

- describe it as one continuous camera move within a single clip (a push-in,
  a whip-pan, a walk-and-follow — see timing cues below), or
- generate one clip per cut as **separate `generate` calls** (each is a
  separately billed job) and stitch them with an external video tool — this
  skill does not do multi-clip editing/stitching.

**`ofox-video-core`'s `chain` subcommand does not help here.** It carries one
shot's closing frame into the next for visual continuity, but Seedance 2.5
image-to-video **refuses reference frames containing a real person**
(`input_moderation_failed`) — and this skill is realistic-human by definition.
Nothing is billed when that happens, but the chain stops. Tell the user that
straight rather than letting them discover it mid-sequence: consecutive
short-drama shots have to be generated independently, and continuity comes
from repeating the same character description word for word.

Don't try to cram an entire multi-scene script into one call; ask the user
which single scene/shot to render if the request spans more than one.


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

## Writing a good short-drama prompt

A short-drama prompt needs three things a generic prompt usually skips:

### 1. Character appearance, stated once, per character

Describe age, gender, hair, build, and clothing for each character so the
model renders a consistent, recognizable person — and reuse the *same*
wording across multiple shots of the same scene/script so the character
doesn't visibly change between clips (Seedance has no persistent character
memory across separate jobs; consistent wording is the only lever you have).

```
A woman in her late 20s, shoulder-length black hair, wearing a cream
turtleneck sweater. A man in his early 30s, short dark hair, wearing a
grey wool coat.
```

### 2. Dialogue in quotes, attributed to a character

Put spoken lines in quotes and say who says them. Keep the total spoken word
count realistic for the clip length — roughly **2–3 spoken words per second**
is a safe budget for natural-sounding pacing; more than that tends to make
the generated speech sound rushed or garbled.

```
The woman says, "Where were you last night?" The man replies, "I told you,
I was working late."
```

For a 15-second clip that's a comfortable ceiling of ~30–40 spoken words
total across both lines — trim the dialogue if the script beat has more than
that.

### 3. Scene-cut / timing cues

Since one job is one continuous take, use timestamped beats to shape pacing
and camera movement within the clip rather than implying a hard edit:

```
0-4s: wide shot of a dim kitchen, the woman stands by the counter.
4-10s: camera slowly pushes in to a medium two-shot as the man enters and
the dialogue plays. 10-15s: close-up on the woman's face as she turns away.
```

Treat these as strong hints, not a guaranteed edit list — Seedance may not
honor a hard cut mid-clip. If a literal hard cut matters more than a
continuous take, generate it as two separate clips instead (see above).

### Putting it together

```
A woman in her late 20s, shoulder-length black hair, wearing a cream
turtleneck sweater, stands in a dim kitchen. A man in his early 30s, short
dark hair, grey wool coat, enters. 0-4s: wide shot, she waits by the
counter. 4-10s: camera pushes in to a medium two-shot; she says, "Where were
you last night?" He replies, "I told you, I was working late." 10-15s:
close-up on her face as she turns away, unconvinced. Naturalistic lighting,
handheld camera feel.
```

## Recommended defaults

| Parameter | Default | Why |
|---|---|---|
| `--model` | `bytedance/seedance-2.5` (script default, no flag needed) | current-generation model |
| `--duration` | `10` (adjust to match the requested length, e.g. `15` if the user says 15 seconds) | enough room for a short exchange; Seedance 2.5 accepts 4–30 |
| `--resolution` | `720p` | realistic detail on faces/lip movement at a reasonable cost; use `1080p` only for a hero shot the user will publish |
| `--aspect-ratio` | `9:16` (vertical) | short-drama content is overwhelmingly consumed vertically on mobile/social; pass `--aspect-ratio 16:9` if the user wants landscape instead |
| `--generate-audio` | `true` (server default, no flag needed) | dialogue needs an audio track — never set this `false` for a scene with spoken lines |
| `--real-person` | leave unset (`false`) | only set `true` if you're passing an actual photo of a real person via `--frame-first-image`/`--frame-last-image` as a likeness reference — a purely text-described fictional character does not need this flag |

Always confirm the actual duration/aspect ratio with the user's request first
(e.g. "15 seconds" in the trigger example overrides the 10s default).


## Which upstream renders it

Jobs are pinned to the `byteplus` upstream (ByteDance's platform for markets
outside mainland China). Ofox otherwise picks between it and Volcengine Ark by
weight, and the two moderate differently, so pinning keeps results consistent.
Pass `--provider volcengine` for the mainland platform, or `--provider auto` to
let Ofox choose. Pricing is identical either way. See
`ofox-video-core/references/api-params.md` for the detail.

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
  --prompt "<the short-drama prompt built above>" \
  --name "<short scene name, e.g. convenience store breakup>" \
  --duration 10 \
  --resolution 720p \
  --aspect-ratio 9:16
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
plus the short-drama-specific ones:

| Symptom | Cause | Fix |
|---|---|---|
| Exit `1`, no network call made | Bad `--duration`/`--resolution`/`--aspect-ratio`, or missing `--prompt` | Fix the flag per the error message and re-run `generate` — free to retry, nothing was submitted |
| Exit `2` | `curl`/`jq` missing, or `OFOX_API_KEY` not set | Re-run `ofox-video-core`'s `check` and follow its install/signup guidance |
| Exit `3`, `error.code: insufficient_credits` | Ofox balance too low | No charge was made; the user needs to add credits at `https://app.ofox.ai` before retrying |
| Exit `3`, job ends `failed`, or `invalid_request` on create, with no other error code hint | Likely a moderation rejection: prompts describing real/identifiable public figures, sexual content, or graphic violence are commonly rejected before or during generation | Rewrite the prompt: use a generic character description instead of naming a real person, tone down graphic detail, then call `generate` again — this is a **new** request with a new prompt, not a resubmission of the failed one, so it's safe to retry immediately |
| Generated speech sounds rushed, garbled, or cut off | Too many words of dialogue for the clip duration | Trim dialogue to roughly 2–3 spoken words per second of clip, or increase `--duration` (within 4–30s) |
| Character's appearance drifts between two clips of the "same" scene | Each `generate` call is stateless — no persistent character memory | Reuse the exact same character-description wording in every prompt for that script/character |
| Exit `4`, timed out waiting for completion | Job is still running upstream, not failed | Do **not** re-run `generate`; run `bash ../ofox-video-core/references/ofox-video.sh poll JOB_ID` using the job id printed before the timeout |
| Exit `5`, ambiguous network failure on create | No HTTP response received at all — can't tell if a job was created | Do not guess or retry `generate`; tell the user to check `https://app.ofox.ai` for a job that may already be running, per `ofox-video-core`'s no-resubmit rule |

## When NOT to use

- Silent product/brand footage with no characters or dialogue — use
  `seedance-ad-creative` instead.
- The user wants to animate an existing photo of a real person (a specific
  actor/likeness) rather than a described fictional character — still
  possible via `--frame-first-image`/`--frame-last-image` and `--real-person
  true`, but confirm the user has rights to use that likeness before
  proceeding.
- Multi-shot video editing/stitching across several generated clips — this
  skill produces individual clips only.
- Anime- or manga-style scenes, especially ones needing the same character
  to look identical across multiple shots — use `seedance-anime-drama`
  instead: it generates and reuses an actual reference image (not just
  repeated text) for character consistency.
