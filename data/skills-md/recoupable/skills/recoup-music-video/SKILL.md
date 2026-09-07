---
name: recoup-music-video
description: Make a finished vertical music video for an artist — generate the song, then build the film around it. Use for "make a music video", "turn this into a music video", "make me a video for my song", or "I want a music video about X". v1 generates the song; bringing your own released master (audio file, Spotify or YouTube URL) is v2. Composes a complete short piece on the free tier and a full-length film on Pro. Verifies the render before claiming done; stops at the asset.
hooks:
  Stop:
    - hooks:
        - type: prompt
          timeout: 30
          prompt: |
            You are the analyze-gate reviewer for the recoup-music-video skill. The main agent is about to stop. Decide whether to block.

            The rule: the agent must NOT claim a video is finished — 'ready', 'done', 'here's your music video', 'final', 'good to go', or any equivalent — unless an analyze-gate result for THAT render appears in the conversation. A render returning the right duration is NOT evidence it looks right; the agent cannot see motion without analyzing.

            Decide:

            1. If the agent produced or is presenting a generated VIDEO asset AND is claiming it is finished/ready AND there is no analyze-gate pass (or explicit visual inspection of read frames) for that asset in the conversation, block:
            {"decision": "block", "reason": "video presented as ready without an analyze-gate pass", "systemMessage": "Read frames from the finished render (or POST /api/content/analyze) and review the result before claiming it's ready. If it fails, regenerate and re-analyze; if borderline, surface the analysis to the user instead of asserting success."}

            2. Otherwise approve:
            {"decision": "approve"}
---

# Music video — build the film the song deserves

Make a finished vertical video cut to a song. **v1 generates the song**; bringing an existing
master is v2 (see "Not yet" at the bottom).

Two real builds inform the craft below: **LETAL XLUG (brauxelion's verse)**, shipped and
artist-approved 2026-08-28, and **Movamos el Mundo (Tomás Mika)**, stopped mid-build 2026-09-01 by
the artist's own feedback. Everything here that costs money was learned by spending it.

## Scaffold — you start from nothing

There is no reference project to clone. Stand the project up in the sandbox:

```bash
ffmpeg -version                        # in the base image; fail loudly if absent
npx --yes hyperframes@0.7.5 init video # PIN 0.7.5
```

**Pin `hyperframes@0.7.5`.** A fresh `init` scaffolds a newer version whose renderer needs a newer
Chrome than the cached headless shell, and every render fails with
`ctx.drawElementImage is not a function`. Lint and inspect work on either.

Never put an API key in the sandbox. Every paid call goes through the Recoup API with
`$RECOUP_ACCESS_TOKEN`, which meters credits and keeps our fal key server-side.

The base is `https://api.recoupable.dev`, spelled out at every call below — the same way
`recoup-platform-api-access` does it. There is no env var for it: a sandbox is handed
`RECOUP_ACCESS_TOKEN` and `RECOUP_ORG_ID` and nothing else.

**Let each API response's JSON reach stdout** — that is what makes the song, the stills and the
clips play inline in the chat instead of arriving as bare links. See "Print every media URL to
stdout as JSON" at the bottom; it applies to every media step, not just the final render.

## Length — compose FOR the budget, never truncate to it

Free-tier accounts are capped at **15 seconds** of generated output. A music video is three to four
minutes, so on a free account **build a deliberate 15-second piece** — one section, its own in and
out, a real ending — not the first 15 seconds of a film that stops mid-phrase.

A truncated film is the worst possible first impression. Check the account's plan before writing the
scene table, and say which you are building in the plan doc.

## 1. The song

Generate it, then poll:

```bash
curl -sS -X POST "https://api.recoupable.dev/api/music" -H "Authorization: Bearer $RECOUP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"<style, mood, vocals, instrumentation, BPM, key>","lyrics":"[verse]\n...","duration":15}'
# -> 202 { generation: { id } }, Location: /api/music/{id}
curl -sS "https://api.recoupable.dev/api/music/<ID>" -H "Authorization: Bearer $RECOUP_ACCESS_TOKEN"
# poll until status is complete, then read the audio url
```

Structure tags (`[intro]`, `[verse]`, `[chorus]`, `[outro]`) each go on their own line. The lyric you
write **is** the brief for the film — read it back for images before writing a scene table.

**Measure the audio before touching it, and use linear gain only, never `loudnorm`.** Measure again
on the finished render.

## 2. Where the story comes from

**If the artist gives direction, follow it. Otherwise write the story yourself, from the lyrics and
what you know about them.** Never reproduce the video they already have.

This document used to say *continue the artist's own world, do not invent one*. On 2026-09-01 that
rule took a 159-second film 33 stills deep into a faithful reproduction of the artist's existing
video — same field, same wardrobe — and he then said what he had actually wanted:

> "le pediría algo totalmente distinto al video que ya tengo filmado.. o sea estar cantando ahí en un
> campo fue justamente por falta de recursos jjajaj ... como una historia tal vez, o en distintas
> locaciones.. tal vez una pareja.. viviendo cosas juntos"

**An artist's existing video is evidence of their budget, not their taste.** One person alone in a
field is what a song gets when there is no money; rebuilding it faithfully hands them back their own
constraint at higher resolution. We have no locations, no crew, no second-actor fee and no weather.
The version they could not afford is the only thing we have that nobody else offered them, so read
their existing work for *world and wardrobe*, never for scope.

The lyric is the brief: Tomás's song names an earthquake of kindness, fire falling from an opening
sky, salt petals on the wind and living in freedom, and every one of those is a shot. Read the whole
lyric for images before writing a scene table.

## 3. Cast the film

**There is no face-guide step and no `cast/<artist>/` requirement.** That was inherited from the
cinematic-narrative format, where a recurring Recoup character must look the same across episodes. A
music video has no such obligation, and the guide costs two to four generations before the first
scene still exists, must be seeded into every later call, and drags the likeness gate along with it.

**Default: cast the film with invented characters.** One identity paragraph per character, reused
verbatim in every still prompt, each character locked by its first approved still, which seeds the
rest. Same consistency mechanism, minus the guide. It also frees the story from the artist's body: a
song about two people can show two people, a song spanning years can span locations and ages.

**Put the artist on camera only when the film needs them there** — they asked, or the song is
first-person and performance is the concept. Then the likeness gate applies, and you need photos
supplied by them (not frames scraped off their video). There is no lip-sync path in v1 (see the
gate below), so keep performance shots to framing where an unsynced mouth doesn't read as wrong.

Cast as many characters as the story needs. Never seed one from a photograph of a real person, and
never imply a real person.

## 4. The three gates that cost money

**Confirm the track and the lyric sheet before the song map.** The reference run built a 20-shot
table, generated 19 stills and started motion on the wrong song: the lyric sheet was for the title
track. Get the track in writing, get their sheet, transcribe the audio you will actually cut and diff
the two. Settle the **section** here too; a featured artist's own verse is usually right and it
sidesteps the featured-voice gate.

**There is no lip-sync path in v1 — `/api/content/video` is pinned to H3 Max only.** A lip-sync
model (fal's OmniHuman) was bake-off'd on the reference film, but that route isn't exposed through
the API and isn't caller-selectable — every motion call goes to the same house model regardless of
whether the mouth is visible. H3 Max's mouths are prompt-driven: they move, they look plausible
frozen, and they are **never synced to real audio**.

> **Write the scene table around that limit, don't fight it.** Mark *mouth-visible* rows on the day
> you write the table and favor framing that doesn't put an unsynced mouth in focus for those beats
> — profile, distance, cutaways, the mouth out of frame. Full lip-sync is a v2 item once the API
> supports it, not something to work around per shot.

**Review the contact sheet before any motion spend.** Stills are cents; motion is dollars. Generate
every still, assemble `scenes/CONTACT-SHEET.jpg` and read the whole sheet in one look for character
consistency, hands, props, stray text, background people and brand-safety violations. Review the
plates and the character portraits on their own sheets first, before any shot is generated at all. **Fix physics at the still, never
at the clip** — a half-open car window survived two OmniHuman takes with a hand through the glass
before the still itself was regenerated, and re-rolling a clip to fix a still costs five to ten times
more.

## 5. Song map and scene table

Sections (`Intro / Verse / Hook / Break / Tail`) with a lyric anchor each, then a scene table on top.
**Every beat ≤6.5s** (`references/hooks.md`). Each row carries: window, beat, still prompt, motion
prompt, and whether the mouth is visible — deciding that in the table is what keeps unsynced,
mouth-visible framing out of the shot list before any motion spend, not after.

The hook is a **specific image**, not a spoken line; a music video's VO is the song. First frame, no
logo, no fade, no title card.

Write one long `STYLE` string and one identity paragraph per character, and interpolate them into
every prompt. Consistency across 30 shots comes from the strings being literally identical, not from
describing the look 30 times. Put the negative list **inside** `STYLE`: `ABSOLUTELY NO text, letters,
numbers, logos, signs with words, watermarks, or user interface. NO weapons, NO drugs, NO cash.`

**Name the camera move, do not describe the effect.** "The horizon tilts" produced a hillside; **DUTCH
ANGLE** plus "NOT a hill, NOT a slope" produced the shot. And a corrective re-roll silently drops
whatever the prompt stops repeating — the tilt fix came back with warm blue-sky light and broke the
film's grade arc, so re-assert the grade in every corrective prompt.

## 6. Stills

**Owner ruling 2026-09-01: Muse Image is the house still model, replacing Nano Banana 2.** It is
quoted at **$0.01 per image** against Nano Banana 2's $0.08, and NB2 bills 2K output at 1.5x
($0.12) — which is what our generators were actually set to. That is a 12x difference on a line we
pay 30 to 40 times per film, so re-rolls stop being something to ration.

All stills go through `POST https://api.recoupable.dev/api/content/image` — never call fal directly, and never
send a `model` field; the endpoint is pinned to Muse Image server-side:

```bash
curl -sS -X POST "https://api.recoupable.dev/api/content/image" -H "Authorization: Bearer $RECOUP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"<the shot>","aspect_ratio":"9:16","num_images":1,"output_format":"png"}'
# -> 200 { imageUrl, images: [...] }
```

The first still of a character or world omits `image_urls` (text-to-image). Every still after it
adds `image_urls` — **1 to 10** reference images — to seed on what already exists (edit).

`output_format` defaults to **webp**; set `"png"` or `"jpeg"` so ffmpeg and the renderer take the
file. There is **no resolution field** (the aspect ratio sets the dimensions) and **no negative
prompt field**, so the negative list stays inside the `STYLE` string as above. `prompt` must be
non-empty — an empty string is rejected with a 400 before it ever reaches fal.

`image_urls` taking up to ten references is what the whole workflow below runs on.

**Verified 2026-09-01** on a 33-shot film: it holds a character across 30 prompts, returns 1152x2048
at 9:16, and honours "ABSOLUTELY NO text". It does **not** reliably follow layout or wardrobe
instructions that contradict a reference image, so name those harder than feels necessary.

## 7. Build the film in three layers: plates, then people, then camera

Do these in order. Skipping straight to shots cost two complete scene passes on the reference film.

**Layer 1 — the empty plates.** One still per location with **nobody in frame**, generated
text-to-image and approved before a single character shot exists. Where two plates are the same place
at different times (a roof at dawn and at sunrise, a field by day and at night), generate the second
as an **edit of the first** so it is demonstrably the same place: *"EXACTLY the same rooftop as the
reference image, same parapet, same water tank, same camera position. The only change is the light."*

Why: independently generated shots of "a kitchen at night" are a different kitchen every time. The
reference film shipped a contact sheet where two consecutive shots of the same room did not match.

**Layer 2 — camera coverage, and this is the step everyone skips.** Plate-seeding locks the
*composition* as well as the location, so every shot in an act comes back as the same photograph with
different content dropped in.

> **Test this before you spend on it (2026-09-02).** On `meta/muse-image` the plate does **not**
> lock the camera when the move is stated explicitly and emphatically: a top-down floor shot came
> straight out of a wide eye-level hall plate, first try, and four planned angle plates turned out
> to be unnecessary. Spend one image finding out which behaviour you are getting. And note a plate
> earns its place only when two or more shots share it; a plate for one shot is ceremony.
> Also read `video-pipeline.md` → *Reference discipline*: a plate transmits PLACE, a character
> transmits MEDIUM, and you cannot edit a photoreal plate into another medium at all. For each location generate **two more angles as edits of its master**
— a medium and a low or detail angle — then seed each shot on the angle it actually needs. At $0.01
a plate this is the cheapest quality in the pipeline.

> **A camera-coverage plate carries an implied camera POSITION, not just a framing.** A beach plate
> with the dunes at the top means the camera stands in the sea looking landward, so nothing seeded on
> it can walk away from camera out to sea. Check where the camera *is* before assigning a plate.

**Layer 3 — the shots.** Every character shot seeds on **its angle plate first, then the character
portraits**, and the prompt says which reference is which, because the model cannot guess:

```
The FIRST reference image is the LOCATION. Reproduce that place exactly: same architecture,
same objects, same light, same colour. Do not invent a different place.
The OTHER reference images are the two people. Same faces, same bone structure, same hair,
same age. Do not beautify them, do not change their age, do not swap the faces.
```

**Age a character by chaining edits.** Young via `text-to-image`, then middle and old as edits seeded
on the young portrait. That is what makes three ages read as one person instead of three lookalikes.

### The two prompt failures that will happen to you

> **Filter triggers confirmed so far:** kissing, wading, "human shadows", a "shaft" of light, a petal
> "hanging", anatomy language, and **"dead"** in any form ("hundreds of dead moths" was rejected;
> "hundreds of empty paper moth wings" passed and reads better). Reword around the trigger. Retrying
> identical text never works.

**1. The blanket negative does not stop stray background people at extreme wide.** `NO other people
in frame beyond those described` sat in the shared `STYLE` string and an extreme-wide road shot still
grew two extra figures near the horizon, where a person is a few pixels and costs the model nothing.
State the headcount **positively** and declare the background empty **by category**:

> EXACTLY TWO people are in this photograph and nobody else. The road beyond them is COMPLETELY
> EMPTY all the way to the horizon: no other figures, no distant walkers, no specks of people,
> no vehicles, no animals.

**2. fal's content filter rejects innocuous prompts — and it is NON-DETERMINISTIC, so RETRY BEFORE
YOU REWORD.** This corrects the advice that shipped in #129, which said only a reword clears a
rejection. It does not: on a 31-shot film **11 shots failed on the first pass and 9 of them succeeded
on retry with the prompt unchanged**. The same prompt was submitted twice back to back and passed
both times after failing minutes earlier, which means the checker is also judging something other
than your text — most likely the generated image as well.

> **The order is: retry up to ~4 times with backoff, and only reword what survives that.** Rewording
> first means rewriting good prompts for no reason and losing the shot you actually wanted. Build the
> retry into the generator, not into your patience:

```js
let res, lastErr;
for (let attempt = 1; attempt <= 4; attempt++) {
  const r = await fetch("https://api.recoupable.dev/api/content/image", {
    method: "POST",
    headers: { Authorization: `Bearer ${RECOUP_ACCESS_TOKEN}`, "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (r.ok) { res = await r.json(); break; }
  lastErr = await r.text();
  if (attempt < 4) await new Promise(r => setTimeout(r, 1500 * attempt));
}
if (!res) throw new Error(lastErr);
```

Lower concurrency helps too; four in flight rejected noticeably more than two.

**What survives retry is a real trigger, and it is almost never the subject.** Fire is fine — a whole
hillside alight passes first time. What trips it is the *vocabulary* around the subject:

| Rejected | Passed |
|---|---|
| the fire has **SPREAD**; "nothing **destroyed**, nothing **charred**, no smoke **damage**" | "more small calm flames… like candles… everything intact" |
| **sparks** climbing, **embers** drifting, anything *rising* off a fire | "small bright points of light", "warm haze" |
| rain **hammering**, droplets **bursting** | "rain running over the paintwork", "raindrops catching the light" |
| people **dancing** | "out in the street together, celebrating, arms raised" |
| hands **gripping** a wheel | "two hands rest on the wheel" |
| two people **kissing** | "standing facing each other, foreheads touching, eyes closed" |
| anatomy spelled out — "**hips**, thighs, submerged" | "water at knee height, upright at full height" |
| "two long **human shadows**" | "two long narrow parallel bands of shade" |
| a "**shaft**" of light | "a band of light" |
| a petal "**hanging** suspended" | "a petal floats in the air" |

Two patterns cover almost all of it: **language of destruction or spreading**, even when you are
negating it, and **body-part or force words** on a human subject. Describe things as calm, contained
and decorative and the same shot passes.

Budget a minute and a penny per rejection. Across two films none of them cost a shot — but do not
reword a prompt that has not yet been retried.

## 8. Motion — one model

**Owner ruling 2026-08-31: MiniMax H3 Max is the house image-to-video model, and it's the only one
`/api/content/video` exposes.** Every motion call — mouth visible or not — goes through it; there is
no `model` field to set and no lip-sync route (see the gate above).

```bash
curl -sS -X POST "https://api.recoupable.dev/api/content/video" -H "Authorization: Bearer $RECOUP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"<the motion>","image_url":"<still url>","duration":5,"resolution":"768P"}'
# -> 200 { videoUrl }
```

`duration` is an integer **5-15 seconds**; `resolution` is `"480P"` or `"768P"` (billing scales with
768P, not a flat per-second rate — see below). `end_image_url` pins a second frame for a defined
start/end pair. `prompt_expansion_mode` is `"balanced"` (default) or `"quality"` — no `"disabled"`
value exists; omit the field to take the default.

**Pricing is per billable unit, not a flat $/s.** fal bills 768P at 1.6x the unit count of 480P for
the same duration, not a different per-second rate. At the **standing (post-promo) rate that's an
effective $0.08/s at 768P, $0.05/s at 480P** — fal is running a launch promo at $0.02/s at 768P
($0.0125/s at 480P) that **ends 2026-09-07**; after that the standing rate applies. Use the standing
figure for budgeting past that date.

**H3 Max invents things, and driving it is part of the job.** Across the two builds it added a
lettered pendant, numbered dashboard gauges, storefront signage and an anime woman who was not in the
still. So: carry the full negative list in **every motion prompt**, not just the still prompt; **name
the prop you do not want** ("plain chain, no pendant" fixed the pendant); budget two takes on wide
plates and slow push-ins, its two weak shots; and re-roll freely — at $0.08/s the answer to a bad
take is another take.

## 9. Composite, render, mux

In the `video/` project you scaffolded, place the clips on the song map by word time, **mute every clip**
(the master is muxed after render), and type any wordmark as HTML text.

- Pin every invocation: `npx hyperframes@0.7.5 snapshot --at <times> .` at ~6 points **before** you
  ever run `npm run render`.
- **Never cut a clip within ~0.15s of its file end** — the decoder returns black there. Verify by
  sampling frame brightness across the cut, not by eye.
- Where a generator returns a clip fractionally shorter than its window, clone the last frame
  (`tpad=stop_mode=clone`) rather than reflowing the timeline. **Lip-synced starts are absolute.**
- **The headless renderer ignores CSS `filter: invert` on JPEGs.** Type the wordmark.
- A still model turns "two shots of him" into a split grid. Prompt one continuous frame.
- Mux at measured linear gain, then read frames back out of the finished render. A render returning
  the right duration is not evidence it looks right.

## Cost

Verified rates: **stills $0.01 each** (Muse Image), **$0.08/s of motion at 768P, $0.05/s at 480P**
(H3 Max, standing rate — a promo through 2026-09-07 halves both to $0.02/s and $0.0125/s). v1 has
one motion model for every shot, mouth-visible or not (see the lip-sync gate above), so this is the
whole motion budget — no separate sung-shot rate. Motion is still essentially the entire budget.

Measured on a 33-shot, 159s film: **$1.75 for every image in the project** — face-guide bake-off,
six character portraits, 24 plates, all 33 stills, and two complete scene passes that were thrown
away. The first 30 seconds of motion, six shots, came to **$3.13** on the reference build (which
predates the API-only cutover and included one shot on a lip-sync model no longer available through
`/api/content/video` — a v1 build swaps that shot for an H3 Max take instead, at the rate above).
Stills are now cheap enough that the expensive mistake is spending motion money on a shot list the
artist has not seen.

Two lines disappeared with this revision: the face guide and its failed attempts, and Nano Banana 2
at 2K, which took the stills line from ~$4.70 to ~$0.35 on a 33-shot film. Re-check every price on
fal before committing, and pull real spend from the api project's production `FAL_KEY` account.


## Print every media URL to stdout as JSON

The chat renders an inline player from the media URL **in a bash result's stdout**, and it only
reads well-known JSON fields — `audio_url`, `videoUrl`, `imageUrl` and friends. It parses stdout as
JSON, so a bare URL on its own line renders **nothing**.

**This applies at every step that produces media, not just the last one.** Verified 2026-09-03: a
full run generated a real song, still and clip and rendered no players at all, because each
generator printed `attempt 1 OK` and a bare URL instead of the API's response.

So let the API's own JSON reach stdout:

```bash
# ✅ the response body lands on stdout as JSON — the player renders
curl -sS -X POST "https://api.recoupable.dev/api/content/video" ... 

# ✅ same for the song, after polling to completion
curl -sS "https://api.recoupable.dev/api/music/$ID" ...

# ❌ renders nothing: not JSON
echo "attempt 1 OK"; echo "$URL"

# ❌ renders nothing: redirected away from stdout
curl -sS ... -o response.json
```

If a step must post-process the response, print the raw JSON **as well**, on its own. Piping the
final line through `jq -r`, redirecting it to a file, or only mentioning the URL in prose means no
player renders and the person is handed a bare link. See recoupable/app#2052.

## Not yet (v2)

**Bringing your own song** — an audio file, a Spotify URL or a YouTube URL — is v2. It restores the
word-timing sources (`hyperframes transcribe`, the `subtitles=true` scrape, the `yt-dlp` auto-caption
VTT and its roll-up trap) and the rights gates that come with a real master: the recording itself,
likeness when the artist is depicted, and any featured voice. **Do not improvise those gates here.**
If someone asks for a video over a released track, say that is coming and offer the generated-song
route.

**Lip-sync** — `/api/content/video` has no lip-sync route today (see §8). If the artist wants
sustained, mouth-visible singing shots synced to the track, say that's not available yet rather than
approximating it with H3 Max's unsynced motion.
