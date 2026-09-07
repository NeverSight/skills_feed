---
name: generating-image-ads
description: |
  Turns a product photo or URL into a static image ad — one image, or a set. Reads the real product first and holds it identical across every frame and ratio. Triggers: "image ad", "make an ad", "static ad", "promo graphic", "offer graphic", "sale creative", "social ad", "banner ad", "ad creative", "before/after ad", "testimonial ad". Not for generating product photography.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: creative
  summary: "Produces a scroll-stopping image ads for your product — one image, or a set in every placement ratio your feed needs. It keeps your real product and your brand identity perfectly consistent across every frame, and shapes the offer and claims you give it into a well designed ad, following industry best practices."
---

# Image ads

Turn a product into finished static ad(s).

## Workflow

### Step 1: Read what you have

- **A product image or URL is available** → hand it to `analyzing-products`, and take four things
  back: what the product is; **how a person physically uses it** — sprayed, pumped,
  worn, etc.; which parts open or move, and in what order; and the details that have to stay identical wherever it appears.
- **Look at the image before you describe it.** Take the product only from what the image shows. Run `image_analysis` and ask it for everything this ad needs that the product facts leave out — how the surfaces take light, and whatever else the frame you end up building will have to describe.
- **Product not supplied** → don't guess at the product. It becomes the first thing Step 2 asks for.

### Step 2: Interview

**Skip this entirely when the brief already makes the ad obvious** — a clear product, a clear message,
and nothing load-bearing missing. The interview exists to close real gaps, not to confirm what you
were already told.

Otherwise ask once, bundled into a single message. Always leave a free-text way out so the user can answer off-menu. Anything this skill already settles is not a question.

**Do ask, when the answer is genuinely missing:**

| Ask | When |
| --- | --- |
| **The product** — what it is, and whatever else identifies it: packaging, colour, distinguishing features | No image and no URL. Offer to wait for an upload first; a photographed product beats a described one. |
| **Brand guidelines, if they have any** — the color palette, the art direction they shoot to, anything they never put in frame, the typeface where text is drawn, and the register they want the frame to read at | The brief mentions none and the packaging doesn't imply them. Treat as optional: plenty of brands have none, so take what they give and move on. |
| **The offer and the one claim** — a discount, a launch, a benefit, the words they can stand behind | The ad has to say something and the brief doesn't say what. Only claims the user supplies are used, and used as written. |
| **Where it runs** — the placement and the ratios | The brief doesn't say, and the placement decides the crop and the safe zones. |

**When the user waives questions** and the product is already in hand, go straight to generating.
Take a single image at `1:1`, a product-hero direction, and one benefit-led line drawn from the product facts. Say in a sentence which settings you took, then keep going. It is a statement, not a checkpoint.

A missing product image is the one thing still worth raising.

### Step 3: Find the idea

Read `references/ad-craft.md` first. Work in the discipline of the single-minded proposition: every ad resolves one tension between a consumer truth and a product truth.

- **The insight** — a human truth about how a person uses or feels about this kind of product, something true enough that it feels slightly uncomfortable to say out loud. Let that truth create tension.
- **The idea** — resolve the tension into one sentence describing what the ad is about. If you cannot say it in one sentence, you have two ads, not one. Where the brief carries a promotion — a price, a discount, a launch — weave it into the idea as a real element, not bolted on afterwards.
- **The treatment** — only then decide how the idea becomes a single still frame: the mood, the register, the visual approach, chosen because it serves this idea. Treatment follows idea, never the other way round. It may take a familiar shape — a hero frame, a lifestyle scene, a before/after, an offer — but it is chosen to serve the idea, not picked first.

For a set, each ad works from a different **insight** — a different human truth, a different angle into the product — not a different visual treatment of the same insight. If two ads share an insight, you have shipped one ad twice. Nothing is generated here.

### Step 4: Write the copy

Write the copy last — say only what the picture leaves unsaid. From the claims the user supplied and no others:

- **A headline** — the dominant text element, always present. Could be one word, a short sentence, or a wordmark-style brand line — whatever the ad needs.
- **Support** — an optional second tier of text. Use only when the headline alone leaves a real question unanswered. Most ads do not need this.
- **A call to action** — an optional 2–4 word direct-response action, rendered as a **button** (a filled shape with the action inside, set in the accent colour — never floating text).

Every drawn string is one the brand can stand behind. **Don't invent a claim, a statistic, a rating or a badge** to fill the layout.

### Step 5: Write the product description

Write one description of the product, and reuse it unchanged in every prompt you send.

**How much to write depends on whether a photo is going with the call.** With a reference attached,
the photo carries identity and the description covers only what it cannot: the angle you want, the
state the moving parts are in, the action being performed. With no reference, the description is all
the model has, so it carries the product in full from the list below.

- **Form** — shape, proportion, how it sits or stands, or whatever else pins the silhouette down.
- **Closure and moving parts** — a cap, a hinge, a zip, whatever this product has, and whether the
  shot wants it open or shut.
- **Materials and finish, surface by surface** — matte or gloss, brushed, woven, translucent or
  something else.
- **The action, wherever the frame has one** — the specific thing being done to the product, taken
  from the mechanic Step 1 established rather than invented to suit the composition. Write it as the
  physical movement it is, and say what the product is doing at that instant: what has left it, what
  is about to, which part has moved, etc.

**Don't transcribe what the label says.** Spelling out the printing invites the model to redraw it,
and redrawn text comes back warped.

### Step 6: Design the ad

You read `references/ad-craft.md` at Step 3; hold to it here for the design it governs — the one focal point, figure-and-ground separation, where the copy sits relative to the product, the type and colour discipline, the grid and the negative space, and the safe zones each ratio has to respect.

Decide, and write down:

- **How many** — one ad, or a set: the ratio family below, plus any variants the brief asked for. Each is its own separate image.
- **The ratio family** — every placement ratio the ad ships in, generated natively. Where the user named no ratio or placement, deliver a single `1:1`. 
- **The layout** — the focal point, the reading path, where each piece of copy lands, the palette and the type, held to `references/ad-craft.md`.

### Step 7: Select the model

| Model | Use it when | How it wants the prompt |
| --- | --- | --- |
| `gpt-image-2` | the ad is a designed, text-forward layout — drawn headline, offer, callouts, a composed page | short labelled segments on separate lines, every string quoted exactly |
| `nano-banana-pro` | the ad leads on a photoreal product or a person, and carries lighter text | connected sentences in one narrative paragraph, the drawn copy quoted |
| `seedream-5` | a photoreal ad another model refused or keeps failing | a description leading with whatever matters most |

If the user has explicitly named a model, then use that first. Call `list_image_models` for accepted `aspect_ratio` values, `resolution` tiers and per-model `reference_images` limits rather than guessing — a wrong enum fails a billed call.

### Step 8: Show the concept and wait

Nothing has been generated yet, and everything after this step costs money. Get the concept approved first.

Show, written out, in one brief, to the point message:

- **The direction and the product** — the angle, and the look being held.
- **The copy** — the headline, offer, benefits and call to action, word for word.
- **The layout** — what sits where, the format, and the ratios it ships in. Keep this to the high-level concept, not every technical detail.

Then ask whether it's right, and say plainly that they can change any of it — the direction, a line, the offer, the layout, a ratio. **Expect edits.** Rewrite what they change, show it again, and keep going until they approve.

Wait for an answer. Don't generate a frame.

Where the user has said they don't want to be asked, say in one line what you're going with and carry on.

### Step 9: Generate

Call `image_generate` with a `requests` list, all in the same call so they render at once:

- **One object per deliverable** — one per ratio in the family, one per variant the user asked for.
- Per object: `prompt`; `model`; `aspect_ratio`; `resolution`; `reference_images`.
- **`resolution` is `1k`** unless the user asked for a higher tier.
- **The product photo(s) goes in `reference_images` every time.** It holds identity; the prompt alone
  will not.
- **One deliverable per request.** Never generate a second to compare models, to try a different
  look, or to correct an output you judged poor — every one of those bills again. Where the brief
  does ask for several — a ratio family, variants — send them as several request
  objects in the one call.
- **Don't run a vision or analysis call on the image you just generated.** Judging your own output
  is not part of this workflow: it costs another call, and anything it finds you are not permitted to
  act on. Hand the result to the user and let them decide.
- **An unanswered question is not a yes.** If you ask whether to regenerate and no answer comes back,
  the answer is no — deliver what you have and say what you would have changed. A run with nobody
  watching cannot consent to being billed twice.
- Call `list_image_models` for accepted `aspect_ratio` values, `resolution` tiers and per-model
  `reference_images` limits rather than guessing — a wrong enum fails a billed call.

Images are polled for you, but a heavy one can come back as `{status: "pending", …}`. That is a job handle, not a failure. Pass that exact handle to `job_status` to retrieve the finished image, and if it comes back pending again, call `job_status` again with the same handle. **Never re-run a pending image** through `image_generate`: that abandons the job you are already paying for and starts a second, separately billed one.

### Step 10: Return

Share the image URLs and local file paths, once every frame has finished — never a partial set. For a set, present them in the order you outlined.

## Common mistakes

- Filling the layout with an invented claim, rating or badge the user never supplied.
- Letting copy cross the product's focal area instead of sitting in the space it leaves.
- Carrying more than one message, so nothing lands.
- Placing the call to action where the platform's own button sits, so it is covered in-feed.
- Skipping the interview when something load-bearing is missing.
- Naming a brand, a photographer or a competitor in the prompt in place of describing the look.
- Re-running a rejected frame without first finding out what was wrong with it.

## Edge cases

**Never regenerate a deliverable without the user asking.** Every re-run is billed again. Hand back
what came out, say what looks wrong, and wait — including in the cases below.

- **No product supplied, and the user wants to proceed anyway** — ask for the product first; an ad for
  an invented product held across a family is worse than stopping.
- **The image came back not as intended** — the drawn text warped, a look you didn't ask for → deliver
  it anyway and say what you think is off. For warped or misspelled text, quote the copy exactly, cut
  the amount, raise the resolution, and route to `gpt-image-2`. Do not regenerate on your own
  judgement: a second generation bills again, and the user may be happy with the first.
- **One deliverable in the batch fails while the others succeed** — send a new call with only that
  request. Re-running the whole list bills every one again.
- **A rejection that names no reason** → ask what missed before re-running, with options drawn from the
  direction you just built, plus free text. A blind re-run bills again and lands elsewhere at random.
- **Safety or policy rejection** → name a workable stand-in and resubmit; on a second, try another
  model from Step 7; on a third, say which element is blocked rather than retrying blind. 
- **`reference_images` rejected on count** → the error states the limit; drop to it.
- **The user changes something after approving the concept** — redo from the earliest step the change
  touches. A different direction or layout means a new design; a different line means only the copy and
  the prompt; a different ratio means only that object.
- **The brief is a plain product photograph with no ad message** → `generating-product-photos`. **A
  video ad** → `generating-ad-videos`. **General artwork or a poster not selling a product** →
  `generating-images`. Route out rather than forcing it into an ad.
- **`error: "no_provider_configured"`** on any tool → relay the tool's `hint` (the user must set their key).

## Reference

- `references/ad-craft.md` — the design craft, read at Step 3 and held to the final frame: the single-minded proposition, the focal point, figure and ground, visual hierarchy, type and colour, the grid and negative space, the ratio family, the safe zones per placement, brand anchors, the anti-patterns, the compliance lens, keeping the product real, and how the prompt is assembled.
