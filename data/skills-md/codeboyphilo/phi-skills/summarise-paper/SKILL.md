---
name: "summarise-paper"
description: "Use when tasks involve reading and summarising an academic paper from either a PDF file or an arXiv URL. If the input is a PDF, convert it to images for accurate reading (equations/figures). If the input is an arXiv URL, download the LaTeX source to read. Output the summary as a standalone LaTeX file."
---

# When to use

- Reading and summarising an academic paper.

# Workflow

1. Determine whether the input is a PDF file or an arXiv URL.
2. If the input is a PDF file:
   1. Use `pdftoppm` to convert the PDF into PNG images. Save them under `.cache/{paper name}/` as `[1,2,3,...].png`.
   2. Read the converted images.
   3. You MUST read the paper ONLY via these images (not via text-extraction tools). Papers often contain equations, figures, and charts that must be recognised accurately, and text extraction is unreliable for these.
3. If the input is an arXiv URL (e.g. `https://www.arxiv.org/abs/2601.07372`):
   1. Normalise the input by replacing the `abs` in the URL into `src` for TeX source, e.g.: `https://www.arxiv.org/src/2601.07372`.
   2. Download the source as a local `.tar.gz` archive and store it under `.cache/downloads/{paper name}/`.
   3. Unpack the archive into `.cache/{paper name}/`.
   4. Locate the entry point (e.g. `main.tex`) and read all relevant contents, including referenced figures.
4. Summarise the paper as a LaTeX research note and write it under `note/{paper name}/`, following the Paper Summarisation Instructions below.
5. The output note must be a standalone LaTeX file that can be compiled directly.

# Paper Summarisation Instructions

You are a senior researcher searching for new ideas for your next top-tier conference/journal paper. You read papers and summarise them into notes. Your goal is to produce a “weeks-later readable” research note: after reading many papers, I should be able to reconstruct the paper’s core ideas, methods, and evidence, and discuss it intelligently even if I have not read it recently.

## Core requirements

- **Faithfulness:** Use ONLY information supported by the paper. If a detail is missing or unclear, write “Not stated in the paper” (or “Not shown in the provided excerpt”) rather than guessing.
- **Grounding:** Where possible, cite the source of each key claim (section name, figure/table number, equation number, or page number).
- **Clarity:** Prefer intuition-first explanations, then formalisation/maths, then implications.
- **Completeness:** The Methodology section must be self-contained and read as a coherent story from inputs → computations → outputs, including training and inference pipelines if applicable.
- **Language:** You must use British English.

## Notation rules

- $\mathcal{C}$ denotes a set.
- Bold lowercase $\mathbf{x}$ denotes a vector; bold uppercase $\mathbf{X}$ denotes a matrix.
- Uppercase $X$ denotes a random variable; lowercase $x$ denotes a deterministic value.
- Use correct LaTeX ($...$ for inline maths, $$...$$ for display maths). Define symbols before using them.

Write the note using the EXACT structure and headings below:

### 1. Motivation

- What problem is being addressed?
- What failure mode or limitation of prior work is targeted?
- Why it matters.

### 2. Contributions

- Bullet list of the paper’s concrete contributions (methods, theory, benchmarks, analyses).
- Where possible, separate contributions into “new idea” vs “engineering/implementation” vs “evaluation/protocol”.

### 3. Methodology

- MINI-PAPER STYLE, single coherent story.
- Write this section as a flowing narrative (like the Methods section of a well-written paper), not as a report or checklist.

#### Hard constraints

- No sub-bullets or lettered substeps. Minimal headings are allowed, but prefer continuous prose.
- The story must flow in one direction: introduce concepts only when they become necessary.
- Each paragraph should lead naturally into the next (use transitions such as “To address this…”, “Concretely…”, “This enables…”, “At inference time…”).
- If a critical detail is missing, explicitly write “Not stated in the paper” rather than guessing.

#### Narrative guidance

- Present the method in the order the paper itself develops it (often: problem → idea → formulation → algorithm → training → inference → complexity).
- Include whichever of the following are relevant, but do not force all items or a fixed order:
  - Problem setting and assumptions (inputs, outputs, constraints)
  - Core insight and how it differs from prior work (if discussed)
  - The main objects/components (model modules, memory, prompts, optimiser, data stream, etc.)
  - Key equations/objectives (only if present; define symbols before use)
  - The end-to-end procedure (including the training loop if applicable)
  - Inference-time behaviour (if different from training or otherwise non-trivial)
  - Notable implementation details or computational overheads (only if stated)

### 4. Experimental Setup

- A short “Implementation checklist” with 4–8 items ONLY if the paper provides those details (e.g., buffer size, optimiser, key hyperparameters, compute, architectural choices). If not provided, write “Not stated in the paper.”
- Datasets/tasks, baselines, evaluation protocol, and metrics.
- What ablations or sensitivity analyses were run.

### 5. Strengths & Weaknesses

- **Strengths:** 3–6 bullets with reasons tied to evidence in the paper.
- **Weaknesses/risks:** 3–6 bullets (e.g., missing baselines, unclear protocol, confounders, scaling limits, assumptions, failure cases).
- Include **“What I would ask the authors as a reviewer”** (2–3 questions).

### 6. Final short note

- 1–3 sentences giving a crisp description of what the paper does and the key result/claim (avoid numbers unless explicitly stated in the paper).
- Key takeaways:
  - 3–5 bullets covering what I should steal/adapt, what to be cautious about, and one concrete follow-up experiment idea.
  - This section may be opinionated, but it must not invent facts about the paper.

# Dependencies (install if missing)

```bash
# macOS (Homebrew)
brew install poppler

# Ubuntu/Debian
sudo apt-get install -y poppler-utils
```

If installation isn't possible in this environment, tell the user which dependency is missing and how to install it locally.
