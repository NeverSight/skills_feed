---
name: FigFox-Gen-skill
description: Use when turning a scientific Methodology, with an optional reference image, into one evidence-grounded, human-editable final PNG figure.
metadata:
  short-description: Build evidence-guided single-pass scientific figures
---

# FigFox-Gen-skill

## Core workflow

Run exactly one image-generation pass and stop at PNG1:

```text
Methodology + optional reference
  -> Context 1: recurring domain visual language
  -> Context 2: content-to-visual plan
  -> Context 3: inspected FigureBench construction evidence + selected palette group
  -> Creative Director prompt: brief + targeted scholarly paper-SVG crops
  -> Prompt 1 bundle
  -> direct image generation
  -> final PNG1
  -> stop
```

There is no post-generation conversion, temporary render, repair loop, or second
image. The local helpers validate files, provenance, and prompt contracts; they do
not observe model calls or guarantee scientific correctness.

## Canonical visual examples

When the user cites the bundled examples, treat these exact files as a style canon:

- `assets/generated-figures/02-latent-diffusion.png`
- `assets/generated-figures/01-figfox-gen-workflow.png`
- `assets/generated-figures/01-figfox-gen-workflow-zh.png`
- `assets/generated-figures/03-musicot.png`
- `assets/generated-figures/04-alphafold3.png`

Inspect the closest example before choosing a visual language. Borrow its restrained
composition, alignment, spacing, flat construction, readable labels, and plain arrows;
do not merge unrelated examples into a collage or invent a more decorative aesthetic.
These examples are visual references, not active palette sources, and they never override
scientific meaning or explicit user constraints.

Start a run with `input/methodology.md` and, when supplied,
`input/user-reference.<ext>`. Use the exact JSON fields in
[artifact schemas](references/artifact-schemas.md). Before work begins, run:

```bash
python scripts/figure_workflow.py check-installation --root .
```

## 1. Context 1: recurring domain visual conventions

Read the Methodology with the language model and extract the scientific domain,
core topic, mainline, likely figure class, named concepts, and explicit user
constraints. Search for 3–4 scholarly papers in that domain. Prefer arXiv and native
SVG/HTML figures; otherwise use credible papers with clearly extractable panels.
Inspect actual figure regions, not titles or abstracts alone.

Use the first representative paper figure selected during this domain search as the
colour-count anchor. Inspect its visible panel, record its dominant-colour count as
`dominant_colour_count` (a positive integer supported by an eligible palette group), and
carry that count into Context 3.
Use the remaining 2–3 papers to corroborate the anchor and the visual conventions; do
not replace the anchored count with a subjective guess or copy source colours. A broad
field may justify a larger count only when the representative figure visibly uses more
dominant roles and the retained papers support that reading. Record source URLs and crop
paths in `references/web/manifest.json` and `references/web/crops/`. Every mapped crop
states its target component, what to borrow, what must change, and why the result remains
human-editable.

If fewer than three credible figures remain, continue searching or report
insufficient evidence. Do not invent recurrence.

```bash
python scripts/figure_workflow.py validate-context --run RUN --context 1
```

## 2. Context 2: content-to-visual plan

Combine the Methodology, Context 1, and optional user reference. The user reference
has strong authority for structure, layout, emphasis, and visibly human-made basic
visual treatment. When a user reference is attached or explicitly cited, enter a
**reference-fidelity lock**: treat it as the canonical visual specification, match its
composition, spacing, hierarchy, and visual grammar, and preserve its line weight,
corner-radius, fill treatment, typography scale, arrow grammar, and sample treatment
wherever the Methodology permits. Change only labels, scientific content, and geometry
required by the Methodology. Do not beautify, complicate, stylize, recompose, or switch
to a different visual language because the model prefers it. Ignore only generated-looking,
fake, or decorative parts, and never take active palette colours from it.

Express the scientific mainline in text, then map every block, structure,
relationship, and required label to an exact visual treatment in
`context/context-2-content-visual-plan.json`. In-image text is limited to concise
block names, structure names, necessary scientific labels, terms, and relationships;
explanatory prose stays in planning.

Normal treatments are human-producible basic geometry, recurring domain-paper
constructions, deliberate manual/stylus drawings, draw.io-like editable structures,
or real photographic crops when scientifically necessary. Mark any other treatment
as special and explain whether a human would construct it geometrically, draw it by
hand, or obtain it as a real photo. Every visual must have a semantic role and
construction provenance.

```bash
python scripts/figure_workflow.py validate-context --run RUN --context 2
```

## 3. Context 3: construction evidence, palette groups, and taste

Read [FigureBench visual selection](references/figurebench-visual-selection.md) and
[taste rules](references/taste-rules.md).

The installed FigureBench pack contains exactly 30 complete development images.
Inspect at least two distinct complete references, then continue adaptively until
every Context 2 need has credible evidence: shapes, frame/container families,
connectors, layout relationships, and special visualizations. There is no fixed
target or maximum image count. Stop only at complete coverage.

Complete references are inspection sources, never unexplained Prompt 1 attachments.
For every useful region, preserve normalized coordinates and a component-specific
contract in `references/figurebench/crops/request.json`. The contract names what to
borrow, what must change so the result is a variant, and why the treatment is human
editable. Materialize and validate the crops:

```bash
python scripts/figure_workflow.py rank-references --run RUN
python scripts/figure_workflow.py crop-references --run RUN
python scripts/figure_workflow.py validate-reference-coverage --run RUN
```

FigureBench supplies geometry, layout, spacing, connectors, and human-edited finish.
It never supplies active palette colours.

The local `references/palette-library.json` stores named palette groups; each group
contains several role-labelled colours, not one colour. At the start of each run,
randomly select one eligible named group and record its id; use multiple colours from
that group as needed. Use `select-palette --run RUN` for an unseeded selection or
`select-palette --run RUN --seed SEED` when the run must be reproducible. This is a
palette-group lineage rule, not a monochrome or single-colour rule. If the selected group lacks a
required functional role, only an evidenced tint, shade, tone, analogous neighbour,
compatible neutral, or controlled contrast may extend it. Never mix a second library
group or take colours from the user reference, FigureBench, or domain papers. Taste
is a low-priority soft constraint for spacing, hierarchy, rhythm, balance, restraint,
and human-edited finish. The final figure must use exactly Context 1's observed
dominant-colour count from the selected group. Other swatches are subordinate neutral,
tint, shade, or support roles and must not be promoted beyond that anchored count. If a
group cannot provide enough roles, select another eligible group or report that no palette
group can support the evidence.

Write `context/context-3-visual-kit.json` from the materialized crops, coverage
matrix, selected palette-group lineage, and taste constraints, then validate:

```bash
python scripts/figure_workflow.py validate-palette --run RUN
python scripts/figure_workflow.py validate-context --run RUN --context 3
```

## 4. Creative Director: pre-PNG1 visual ideation

The Creative Director runs once after Contexts 1–3 and before PNG1. It is a bounded
ideation pass, not an image-generation pass. It may propose a concrete,
scientifically relevant treatment for a planned component, but it must not redraw
the whole figure or invent decorative assets.

Before choosing a style, the Creative Director must model how a human would actually
build the figure in an editor. Use this construction order as a hard planning
sequence:

1. **Choose the base:** establish the main canvas, containers, and simple geometry
   first (usually rectangles or deliberately adjusted rounded rectangles). A subtle
   fill variation is allowed only when it belongs to the base shape and remains
   editable; never use a gradient to hide an unplanned structure.
2. **Build the content on the base:** add the planned structures and modules. Use
   the simplest geometry that carries the meaning. If the method needs a topology,
   grid, model block, or other known construction, look for a real scholarly SVG or
   extractable figure and reuse a targeted crop as evidence instead of inventing a
   fake topology. If it needs an input sample, use a real or explicitly documented
   sample-like crop (text, image, audio, or data), not generic placeholder lines.
3. **Add restrained arrows:** draw plain, readable connectors after the objects are
   placed. Arrowheads and paths must express direction and relation; do not make
   arrows decorative, glossy, multi-coloured, or needlessly curved.
4. **Place exact text:** add concise block names, terms, and relationship labels
   after the structure is stable. Never replace real labels with repeated horizontal
   filler lines.
5. **Place the visual below/next to its label:** keep each explanatory visual close
   to the text it explains. Prefer a real sample, a paper-derived editable crop, a
   regular copied geometry, or a library symbol with clear provenance. A person,
   warning, chat symbol, or other special object must follow its human source and
   semantic role; it may not become a pasted sticker.

Construction invariants: a regular grid or copied geometry must have consistent
spacing and no accidental missing cells or broken lines; a geometric block uses a
flat fill or one controlled fill per block, never multiple arbitrary colours inside
one block; noise is shown with deliberate repeated points or a real noise image only
when the Methodology calls for it; photographs are real photographs when a photo is
scientifically necessary. These rules are planning gates, not post-hoc taste advice.

Compile its prompt:

```bash
python scripts/figure_workflow.py build-creative-director-prompt --run RUN
```

The model returns `creative-director/brief.json`. Validate it:

```bash
python scripts/figure_workflow.py validate-creative-director --run RUN
```

If a new idea needs a construction not already covered by Contexts 1–3, the Creative
Director must locate a real scholarly paper figure available as SVG or extractable
SVG/HTML, inspect its pixels, and request only a targeted crop under
`references/web/crops/creative-director/`. Each crop must include the target
component, HTTPS `source_url` and `evidence_url`, `source_format: "svg"`,
nonempty `borrow` and `must_change` lists, and a human-editability reason.
Never invent a source, attach a complete paper figure, copy its labels or palette,
or use a sticker-like cutout. If no new treatment is needed, return an explicit
`no_external_svg_needed` brief with no crop. Palette lineage and all Prompt 1
anti-AI constraints remain in force.

## 5. Prompt 1 and final PNG1

Compile Prompt 1 only after Contexts 1–3, the Creative Director brief, and every
mapped crop file exist:

```bash
python scripts/figure_workflow.py build-prompt1 --run RUN
```

The bundle contains the Methodology, Contexts 1–3, the Creative Director brief,
the optional reference, mapped scholarly crops, every mapped FigureBench crop, and
any Creative Director paper-SVG crop. A crop guides only its declared component and
its `borrow`/`must_change` contract. It cannot donate source labels, source
colours, source proportions, or a complete composition.

Prompt 1 contains exact mainline, block names, relationships, content-to-visual
mapping, crop contracts, selected palette-group lineage, layout/taste constraints, concise
labels, and anti-AI invariants. Enforce these defaults:

- when a user reference is attached or cited, the reference-fidelity lock is hard:
  match its composition, spacing, hierarchy, and visual grammar before making any
  stylistic choice; preserve its human-made construction cues and change only what
  the Methodology requires;
- do not beautify, complicate, stylize, recompose, or switch visual language merely
  because the image model prefers a different look; reject any output that drifts from
  the reference without a scientific reason;

- no meaningless dots, tiles, floating symbols, purposeless boxes, irrelevant
  ornament, unjustified extreme contrast, decorative gradients, glow, decorative
  shadow, fake cartoons, or shapes without human construction provenance;
- no default numbered `1/2/3/4` planning labels and no generic blue
  title-strip/content-box cards unless the Methodology explicitly requires them;
- never box off the upper portion of a module with a horizontal divider and centered
  title;
- never paste a sticker-like cutout, clip-art badge, medal, seal, or raster badge;
- every visual must be semantically related to its text and editable by a human.
- follow the human construction order: base geometry first, then meaningful content,
  plain arrows, concise text, and a nearby explanatory visual; do not reverse this
  into decorative cards with filler content;
- use real samples or targeted scholarly-paper construction crops for inputs,
  topologies, grids, and model diagrams when they exist; never invent a fake topology
  or pseudo-sample when a faithful human-editable source can be found;
- keep grids and repeated geometry exact and regular, keep each geometric block to a
  flat or single controlled fill, except that a single base/container may use a
  subtle deliberate fill transition when it is part of the planned geometry; never
  use gradients inside a block or as decorative polish. Keep arrows visually
  subordinate to the objects and text.

The first and only image-generation pass receives `prompt-1/prompt.md` and all
manifest attachments. Save the complete labelled result as `png1.png`. PNG1 is
the final deliverable for this workflow. Do not convert it to SVG, render a
temporary derivative, diagnose a later pass, or generate another image.

## 6. Completion and deterministic validation

Write `run-manifest.json` with the canonical paths in
[artifact schemas](references/artifact-schemas.md), then run:

```bash
python scripts/figure_workflow.py validate-run --run RUN
```

A valid run contains exactly one image artifact, `png1.png`; one Prompt 1 root;
the Creative Director prompt and brief; the three Contexts; the scholarly web
manifest; the FigureBench request and materialized crop manifest; and the final
Prompt 1 attachment manifest. The validator checks path safety, provenance,
palette lineage, crop replay, Creative Director source contracts, prompt
determinism, and PNG validity. It does not prove image-generation call counts or
scientific truth. Authors must inspect PNG1 before publication.
