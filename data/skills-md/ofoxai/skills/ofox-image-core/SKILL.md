---
name: ofox-image-core
description: Shared execution layer for the Ofox image generation API (api.ofox.ai) — validates parameters client-side, sends one synchronous text-to-image request, base64-decodes the result, saves it to a file, and reports the real usage token counts and the computed dollar cost. This is a library skill, not a standalone user-facing one — it is meant to be invoked by scenario skills (e.g. a character-reference-sheet generator for a video pipeline) that build model/prompt/size choices for a specific use case and then call into this skill's script rather than re-implementing the API calls. Load this skill directly only when a user explicitly names the Ofox image API, asks to call it with specific low-level parameters, or asks to debug a failed Ofox image generation request — for a plain "generate an image of..." request with no scenario skill available yet, this is the right skill to use directly.
license: MIT
version: "1.1.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/ofox-image-core
metadata:
  author: ofoxai
  version: "1.1.0"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "🖼️"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/ofox-image-core
---

# ofox-image-core: Ofox image API execution layer

Wraps the Ofox image generation API (`https://api.ofox.ai/v1/images/generations`)
behind one script: validate, request, decode, save, report real token usage.
Unlike `ofox-video-core`, this API is **synchronous** — one request either
returns the finished image(s) in the response body or fails outright. There
is no job id, no polling, and (because of that) no free "check what
happened" recovery path if a request goes wrong mid-flight.

## Safety contract (non-negotiable)

- `OFOX_API_KEY` is read **only from the shell environment** — never from a
  dotenv file, never hardcoded in a script or a skill file.
- **Never print, log, or echo the raw key value** — not in chat, not in a
  file, not in a command you show the user, not in verbose curl output.
  `references/ofox-image.sh` never uses `curl -v`/`--trace` for exactly this
  reason (those would print the `Authorization` header). If you need to
  show that a key is configured, say "OFOX_API_KEY is set" — never the value.
- Never write the key into any file this skill (or a skill built on it)
  creates, including generated images' metadata, cost reports, or committed
  code.
- **Check once, then proceed.** Run the availability/key check at most once
  per session (see below). If it passes, don't re-prompt for the key on
  every subsequent call in that session.
- **Fail open on a missing key** — guide the user to get one, don't dead-end
  the conversation. A missing key means "can't call the paid API yet," not
  "stop talking to me."

## Which model

`bash references/ofox-image.sh models` lists every image model Ofox serves and
its per-output-token price. No API key needed — `GET /v1/models` is public.

`--model` is required and has no default on purpose: these models differ
roughly 4x in price with no obvious winner, so defaulting would silently pick
a price on the user's behalf. (Its sibling `ofox-video-core` does default,
because every scenario built on it targets Seedance 2.5 specifically.)

Three models are documented in depth in `references/api-params.md` and
`references/pricing.md` — `openai/gpt-image-2`,
`google/gemini-3.1-flash-image`, `bailian/qwen-image-3.0-pro`. The rest work
too; what isn't documented is which `--size`/`--quality` values each accepts,
because the API doesn't publish that for image models.

## Availability check

Before the first call in a session, verify the environment:

```bash
bash references/ofox-image.sh check
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
bash references/ofox-image.sh generate \
  --model MODEL --prompt "..." --quality VAL [OPTIONS]
```

`generate` validates every parameter client-side (model name, size,
quality, and the documented `n` + Gemini incompatibility) **before any
network call**, builds the request, sends exactly one `POST`, and on
success base64-decodes each returned image and writes it to a file. It
prints:

```
STATUS completed
IMAGE_PATH <absolute/path/to/file.ext>   (one line per generated image)
MODEL <model actually used, from the response>
SIZE <size actually used, from the response>
QUALITY <quality actually used, from the response>
USAGE_INPUT_TOKENS <n>
USAGE_OUTPUT_TOKENS <n>
USAGE_TOTAL_TOKENS <n>
```

Required flags: `--model` (one of `openai/gpt-image-2`,
`google/gemini-3.1-flash-image`, `bailian/qwen-image-3.0-pro`), `--prompt`,
`--quality` (one of `auto low medium high standard hd` — Ofox's docs mark
this required, and not every value is confirmed to apply to every model, so
the script never guesses a default; you must pass one explicitly).

Optional flags: `--size` (one of the documented WxH values or `auto`),
`--n` (1-10, default 1 — **not supported at all by
`google/gemini-3.1-flash-image`**, rejected client-side before any network
call if combined with that model, even `--n 1`), `--output-format`
(`png`/`jpeg`/`webp`), `--background` (`transparent`/`opaque`/`auto`),
`--extra-json '<json>'` (advanced fields not covered by a flag, e.g.
`extra_body.provider.type` for `openai/gpt-image-2`), `--out-dir` (default:
current directory), `--out-name` (bare filename, no extension, no path
separators — default: a timestamp-based name). Full parameter reference:
`references/api-params.md`. The cost formula and the invoice it was verified
against: `references/pricing.md`.

**Always state the full `IMAGE_PATH` as its own standalone line in your
reply to the user** — not folded into a sentence or buried mid-paragraph,
mirroring `ofox-video-core`'s `VIDEO_PATH` discipline exactly. `--out-dir`
is resolved to an absolute path (and created if missing) **before** any
network call, so relay the printed path exactly; the file's location is the
actual deliverable, and the user should be able to find it without
re-deriving your working directory.

## Known gotcha: `SIZE` in the printed output can be wrong

A real, paid end-to-end test (2026-08-29, `google/gemini-3.1-flash-image`,
`--size 512x512`) succeeded and printed `SIZE 512x512` — taken straight
from the API response, which claimed the image was generated at that
size. The actual saved file, verified with `file` and
`sips -g pixelWidth -g pixelHeight`, is really **1024x1024**.
`google/gemini-3.1-flash-image` appears to always generate at its native
1024x1024 resolution and just echoes back whatever `size` was requested,
regardless of what it actually produced. Unconfirmed for
`openai/gpt-image-2` / `bailian/qwen-image-3.0-pro`.

**If a caller needs a guaranteed output size, don't trust the `SIZE` line**
— check the real dimensions of the file at `IMAGE_PATH` directly (`file
<path>` or `sips -g pixelWidth -g pixelHeight <path>` on macOS,
`identify <path>` via ImageMagick). Full detail:
`references/api-params.md`.

## Out of scope for this script

- **`input_images` / image-to-image** (Qwen-only field on this same
  `/v1/images/generations` endpoint) — this script only does text-to-image.
  Passing `input_images` via `--extra-json` is rejected client-side with a
  clear message.
- **`POST /v1/images/edits`** — a different, multipart-form endpoint
  (OpenAI models only). Not implemented here; add a separate script/flag if
  a scenario actually needs "edit this existing image" rather than
  "generate a fresh image from a text description."
- **Streaming responses** (`stream: true`) — this script only parses a
  plain JSON response body. Rejected client-side if set via `--extra-json`.

## No job id, no polling — what that means for failure handling

There is nothing to resume here the way `ofox-video-core poll JOB_ID`
resumes a video job. A single `generate` call either:

- gets a real HTTP response (success or a rejected request) — the request's
  fate is decided, and it is then safe to fix parameters and try again if
  it was rejected, or
- gets **no HTTP response at all** (`curl` exits nonzero with no status
  code) — genuinely ambiguous, and unlike the video API there is no job id
  to look up afterward to find out what happened. The script exits `5` in
  this case and tells you to check your usage/billing history at
  `https://app.ofox.ai` before deciding whether to retry. Don't guess, and
  don't auto-retry a `--extra-json`-free, unmodified request on exit `5`.

**Whether a rejected (non-2xx) request is billed at all has not been
confirmed for this endpoint** — this script assumes, but has not verified
with a real call, that a request producing no image is not charged (the
common pattern for generation APIs, and the same assumption
`ofox-video-core` verified for its own create-rejection case). Treat this
as an open question pending a real, observed error case, not as a settled
fact — if you do observe billing behavior on a real error, that's worth
recording back into this skill's documentation.

## Error handling

This endpoint's error vocabulary has **not** been broadly explored, and this
skill's own earlier documentation got the error response's *shape* wrong,
not just an unconfirmed code: the original research inferred `error.code:
"provider_type_unavailable"` purely from Ofox's doc **prose** describing a
provider-mismatch scenario — it was never seen in a real response. A real
rejected call (2026-08-29, an invalid `extra_body.provider.type`, exactly
the scenario that prose was describing) showed the actual shape is
`{"error": {"message", "type", "code"}}` — an OpenAI-SDK-style shape,
different from the video API's `{code, message}` shape where `code` really
was a semantic string. Here, `error.code` was literally the HTTP status as a
**number** (`400`); the real classifier is `error.type`
(`invalid_request_error`, the only value confirmed so far — nothing else has
been observed, and `provider_type_unavailable` does not appear anywhere in
the real response). `print_api_error` in `ofox-image.sh` now surfaces
`error.type` as the primary classifier and shows `error.code` for reference,
but always prints the raw `error.message` regardless — that part already
worked correctly and still does. Two message-only gotchas remain doc-prose-
only, unconfirmed by a real call: Gemini + `/v1/images/edits` ("Image
editing is not supported for model") and Gemini + `n` (this script prevents
the latter client-side before any network call, so it should never actually
be observed against the real API through `ofox-image.sh`). Don't treat an
unrecognized `error.type` as this script's bug; it means the vocabulary
genuinely hasn't been seen yet — update `references/api-params.md` and this
script's `print_api_error` if/when a new one is confirmed by a real call.

| Exit | Meaning |
|---|---|
| `0` | Success — image(s) decoded and saved, usage token counts and `IMAGE_COST` printed. |
| `1` | Usage/parameter validation error — no network call was made. Fix the flag and retry `generate` freely. |
| `2` | Environment error — `curl`/`jq`/`OFOX_API_KEY` missing. Fix the environment, no request was attempted. |
| `3` | The API rejected the request, or the response body couldn't be parsed into a usable image (see `references/api-params.md` for the one confirmed `error.type`; everything else is surfaced via the raw upstream message). |
| `4` | `--out-dir` could not be created or entered (bad path, permissions) — caught **before** any network call, so no money was spent finding this out. Fix `--out-dir` and retry. |
| `5` | Ambiguous network failure — no HTTP response received at all. No job id exists to check afterward; check `https://app.ofox.ai`'s usage/billing history before deciding whether to retry. |

## For scenario skills built on this

A scenario skill (for example, one that generates a character reference
image before handing it to `ofox-video-core` for image-to-video) should
call `references/ofox-image.sh generate` rather than duplicating any of the
request-building, validation, or decoding logic above. It owns the
scenario-specific prompt template and recommended model/size/quality
defaults; this skill owns the mechanics of talking to the API correctly and
safely.
