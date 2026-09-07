---
name: cloning-video-ads
description: Clones an existing video ad — reads a supplied reference ad, keeps its structure, pacing, shots, camera and hook, and rebuilds it as a new video with the user's own product in place of the original's. Use when the user wants to copy, clone, recreate, or remake an ad or a competitor's video, or make an ad "like this one" with their product. Not for a product ad built from scratch with no reference video, not for a creator sharing their own take on a product and not for cloning image ads.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: creative
  summary: "Recreates a video ad you admire with your own product. It watches the reference ad, works out the shots, pacing, camera and voiceover that make it work, then rebuilds the same structure around your product — swapping the product, brand and spoken lines for yours while holding the original's craft. You approve the plan before anything expensive renders, and it comes back as one finished clip."
---

# Cloning video ads

Take a video ad the user likes and rebuild it with the user's own product. The reference ad's structure, pacing, shots and hook are kept; its product, brand and spoken lines are replaced with the user's.

A product ad built from scratch, with no reference video to follow, is out of scope — that belongs to `generating-ad-videos`. A still image ad belongs to `generating-image-ads`.

## Workflow

### Step 1: Analyze the reference ad

The reference ad is the plan the clone is rebuilt from, so read it first and read it in full — a thin read here is the one thing that breaks the clone, and no later step recovers it.

Read `references/reading-the-ad.md` for exactly what to pull out and the breakdown format, then run `video_analysis` on the ad (a video file or URL) to produce that **timed, second-by-second breakdown** of the whole thing.

- **No reference ad** → there is nothing to read yet. Don't invent one; it becomes the first thing the interview (Step 3) asks for.

### Step 2: Read the product

- **A product image or URL** — the user's product, the one that replaces the original's → hand it to `analyzing-products` for what the product is, how a person physically uses it, which parts open or move, and what must stay identical wherever it appears.
- **Run `image_analysis` on every other image supplied** — what each one shows. The product photo is already covered by `analyzing-products`; don't read it twice.
- **No product** → don't guess at one. It becomes the first thing the interview (Step 3) asks for.

### Step 3: Interview

**Skip this when you already have both the reference ad and the product**, and the user hasn't asked to change the length or ratio.

Otherwise ask once, bundled into a single message, always with a free-text way out.

| Ask | When |
| --- | --- |
| **The reference ad** — the video to clone | It wasn't supplied. Offer to wait for an upload or a link. |
| **The product** — a link or a photo | Neither was supplied. Offer to wait for an upload; a photographed product beats a described one. |
| **How long** | Only if the user wants a length other than the reference ad's. The default is to match it. |
| **Aspect ratio** | Only if the user wants a ratio other than the reference ad's. The default is to match it. |

When the user waives questions, match the reference ad's length and ratio, say in one sentence what you took, and keep going.

### Step 4: Write the product description

Write one description of the user's product and reuse it unchanged in the clip prompt — rephrasing it reads as a different product.

- **Material and finish**, surface by surface — matte or gloss, brushed, woven, translucent, or whatever this one actually is: *"brushed steel barrel, matte soft-touch collar, a woven wrist strap"*.
- **Size** — its width and height, and how it sits against a hand: *"sits in a closed palm, roughly 9 cm tall and 4 cm across"*. Give the real measurements rather than likening it to another object, which the model renders inconsistently.
- **Two to five visual anchors** — features you can verify in the product image and nothing else: exact colours, the shape of a closure or handle, the gauge of a chain or strap, a surface finish, a distinguishing mark.
- **The product mechanism** — how it's built and how it works: the parts that move, how they open or close, and where anything dispenses: *"hinged lid at one end, folds back flat; the brush sits inside the cap"*.
- **What may be done with each part** — which parts are fixed to it, and the whole of what the moving ones allow. Nothing later does anything to the product that isn't on this list.

**Don't transcribe what the label says**, even where the product facts spell it out. Spelling out the printing invites the model to redraw it, and redrawn text comes back warped. The facts may name it; the description never repeats it.

### Step 5: Build the clone blueprint

Read `references/rebuilding-the-ad.md`. Then turn the Step 1 read of the reference ad into a **shot-by-shot blueprint** for the clone — keeping the form and swapping only the identity, as that reference sets out. Two things it leaves to this skill:

- **Keep the whole ad in one clip.** The blueprint's shots are the cuts inside a single continuous clip, not separate clips.
- **Pick the clip model, and let it cap the length.** The clone is one continuous take, so its length can't exceed the longest clip the model makes. Read each model's shortest and longest clip from `list_video_models` and pick the model by the target length — up to about 15 seconds runs on `seedance-2.0-fast`, longer up to 30 seconds on `seedance-2.5`. If the target is longer than the longest clip available, cap it there and say so. Carry the chosen model and its length into Step 9.
- **Fit it to that length.** Where the clone runs a different length than the reference, re-time the shots to fit: if shorter, drop the most redundant cuts and keep the beats that define the ad; if longer, hold the most expressive beats a little longer. The spans stay contiguous and sum to the clone's length. Where the length matches, keep the timing shot for shot.

Write it down: for each shot, its seconds, what is on screen, the camera move, where the product sits and what's done to it, and — where the ad speaks — one line of what is said.

### Step 6: Rewrite the voiceover, if the ad has one

Where the reference ad speaks, trigger the `writing-video-scripts` skill workflow with a brief of what the voiceover should communicate, the blueprint from Step 5 — the shot durations and what happens in each — and the reference ad's own spoken lines as the structure to match, at the same length and cadence, heard as a voiceover over the picture, never lip-synced. Use only the claims the user supplied; drop the original brand's. It returns the words as text, sized to the clip.

Where the reference ad carries no spoken words, skip to Step 7.

### Step 7: Show the blueprint and wait

Nothing has been generated yet, and everything after this step costs money. Get the blueprint approved first.

Show, written out, in one brief message:

- **What's kept from the reference ad** — the structure, pacing and look, in a sentence.
- **The product** — the user's, and how it stands in for the original's.
- **What's on screen in each shot** — its content and camera move. Keep it high level.
- **What's said** — the rewritten words from Step 6, word for word. Only where the ad speaks.

Then ask whether it's right, and say plainly that they can change any of it. **Expect edits.** Rewrite what they change, show it again, and keep going until they approve.

Wait for an answer. Don't write a prompt, don't generate a clip.

Where the user has said they don't want to be asked, say in one line what you're going with and carry on.

### Step 8: Build the storyboard

Only once the blueprint is approved. The sheet is a reference that holds the product identical, not a frame-by-frame plan — so it covers the **key moments only** (`generating-storyboards` caps a sheet at five panels). Pick the beats that most need the product locked — the hook, the shots where the product is featured or handled, and the close — and leave the finer cuts to the clip prompt at Step 9.

Trigger the `generating-storyboards` skill workflow — one sheet for the clip — with those key beats and their seconds, the product image(s), the product description unchanged, the look and register carried from the reference ad, and, where the ad speaks, the script segment. The panel work is done there. The sheet is always `16:9`, with the panels carrying the clone's delivery ratio.

Once the sheet is built, show it and wait. Ask them to check the product in particular — that it is rendered right in every panel it appears in. They can change any panel: rebuild the sheet, show it, and keep going until they approve. Where the user has said they don't want to be asked, say in one line what you're going with and carry on.

### Step 9: Write the prompt

Trigger the `writing-video-prompts` skill workflow with: one prompt for the whole clip, the model and length chosen in Step 5, the panels of the Step 8 sheet as the cuts inside the clip (one cut per panel), the product description carried in unchanged, the rewritten script where the ad speaks, and the media — the storyboard sheet from Step 8 and the product image(s), labelled as `reference_images`. Where the ad speaks, the lines are voiceover over the picture, never lip-synced.

It returns the prompt as text and the order it labelled the media in. Nothing is generated there.

### Step 10: Generate

Call `video_generate` with a single request, using the model and length chosen in Step 5.

- **The request** — the `prompt` from Step 9; the `model` from Step 5; the media it labelled — the storyboard sheet and the product image(s) — as `reference_images` in the order Step 9 labelled them; `duration`, `resolution`, `aspect_ratio`, and `generate_audio` on so the clone carries the reference ad's sound.
- A clip can come back as `{status: "pending", …}` — a job handle, not a failure. Pass that exact handle to `job_status`, and again if it is still pending. **Never re-run a pending clip**; that starts a second billed job.

### Step 11: Return

Return the finished clone's URL and local file path.

## Edge cases

**Never regenerate a clip without the user asking.** Every re-run is billed again. Hand back what came out, say what looks wrong, and wait — including in the cases below.

- **No reference ad** — there is nothing to clone. Point to `generating-ad-videos` for an ad built from scratch.
- **No product supplied, and the user wants to proceed anyway** — a clone around an invented product is worse than stopping. Ask for the product first.
- **The reference ad is too long or too large for `video_analysis`** — it analyses the clip inline. Ask for a shorter ad or a trimmed section, or a link to one.
- **The clone doesn't match the reference ad's structure** — hand it over and say what drifted. Whether it's close enough is the user's call.
- **A sheet comes back wrong** — remake the sheet before generating. Sheets are cheap; a clip made from a wrong sheet is not.
- **A clip doesn't match its sheet** — hand it over and say what looks off. Whether it's close enough is the user's call.
- **A safety filter rejects the clip** — say what is likely being caught (often a person or the original brand's mark), so it can be reworded rather than retried blind.
- **`error: "no_provider_configured"`** on any tool → relay the tool's `hint` (the user must set their key).

## Reference

- `references/reading-the-ad.md` — what to pull out of the reference ad and the timed-breakdown format to capture it in (Step 1).
- `references/rebuilding-the-ad.md` — turning that read into the clone blueprint: what to keep, what to swap, and how the product and copy are replaced without losing the original's craft (Step 5 on).
